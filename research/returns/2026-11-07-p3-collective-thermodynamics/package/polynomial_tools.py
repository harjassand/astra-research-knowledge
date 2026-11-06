"""Exact rational three-variable polynomials and the tagged-probe inverse."""
from fractions import Fraction as Q
from itertools import product
from math import prod


def indices(K,constant=False):
    return [a for a in product(range(K+1),repeat=3) if (0 if constant else 1)<=sum(a)<=K]


def evaluate(p,r):
    return sum((c*prod(x**n for x,n in zip(r,a)) for a,c in p.items()),Q(0))


def derivative(p,j):
    result={}
    for a,c in p.items():
        if a[j]:
            b=list(a); b[j]-=1; result[tuple(b)]=c*a[j]
    return result


def combine(base,controls,u):
    p=dict(base)
    for f,x in zip(controls,u):
        for a,c in f.items(): p[a]=p.get(a,Q(0))-x*c
    return {a:c for a,c in p.items() if c}


def interval_mul(x,y):
    z=[a*b for a in x for b in y]
    return min(z),max(z)


def interval_pow(x,n):
    if n==0: return Q(1),Q(1)
    a,b=x
    if n%2: return a**n,b**n
    return (Q(0) if a<=0<=b else min(a**n,b**n)),max(a**n,b**n)


def enclose(p,box):
    low=Q(0); high=Q(0)
    for a,c in p.items():
        term=(Q(1),Q(1))
        for x,n in zip(box,a): term=interval_mul(term,interval_pow(x,n))
        if c>=0: low+=c*term[0]; high+=c*term[1]
        else: low+=c*term[1]; high+=c*term[0]
    return low,high


def lagrange_coefficients(nodes):
    result=[]
    for j,x in enumerate(nodes):
        coeff=[Q(1)]
        for l,y in enumerate(nodes):
            if l==j: continue
            nxt=[Q(0)]*(len(coeff)+1)
            for k,c in enumerate(coeff):
                nxt[k]-=y*c/(x-y); nxt[k+1]+=c/(x-y)
            coeff=nxt
        result.append(coeff)
    return result


class ProbeInverse:
    def __init__(self,K,a=Q(1,4)):
        self.K=K
        self.nodes=([Q(0)] if K==1 else [-a+2*a*j/(K-1) for j in range(K)])
        self.grid=list(product(self.nodes,repeat=3)); self.alphas=indices(K)
        self.records=[(j,r) for j in range(3) for r in self.grid]
        L=lagrange_coefficients(self.nodes)
        triples=list(product(range(K),repeat=3)); count=len(triples)
        self.rows=[]
        for alpha in self.alphas:
            row=[Q(0)]*(3*count)
            for j in range(3):
                if not alpha[j]: continue
                power=list(alpha); power[j]-=1
                for l,triple in enumerate(triples):
                    row[j*count+l]=prod(L[t][v] for t,v in zip(triple,power))/sum(alpha)
            self.rows.append(row)
        self.row_norms=[sum(abs(x) for x in row) for row in self.rows]
        self.condition=sum(self.row_norms)

    def reconstruct(self,gradient_values,gradient_error):
        assert len(gradient_values)==len(self.records)
        p={a:sum((w*y for w,y in zip(row,gradient_values)),Q(0))
           for a,row in zip(self.alphas,self.rows)}
        return p,self.condition*gradient_error


def encode_polynomial(p):
    return [{'powers':list(a),'coefficient':str(c)} for a,c in sorted(p.items())]


def decode_polynomial(items):
    return {tuple(v['powers']):Q(v['coefficient']) for v in items}
