"""Exact finite challenges of positive-rational cross-tail/norming bounds.

The theorem is proved in independent_noisy_rational_review.md. This program
deliberately permits coefficient-box models that need not have any PSD source.
It validates no physical device or asymptotic novelty claim.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import factorial, comb
import random, json
from pathlib import Path

RNG=random.Random(8317)

def compositions(total,parts):
    if parts==1:
        yield (total,)
    else:
        for j in range(total+1):
            for rest in compositions(total-j,parts-1):
                yield (j,)+rest

def subsets(n,r):
    return [s for j in range(min(n,r)+1) for s in combinations(range(n),j)]

def model(n,r,kappa,kind):
    d={():Q(1)}; nn={():Q(0)}
    for s in subsets(n,r):
        if not s: continue
        j=len(s)
        capd=kappa**j
        capn=Q(j*j)*kappa**(j-1)
        if kind=='max':
            d[s]=capd; nn[s]=capn
        elif kind=='zero':
            d[s]=Q(0); nn[s]=Q(0)
        else:
            d[s]=capd*Q(RNG.randrange(9),8)
            nn[s]=capn*Q(RNG.randrange(9),8)
    return nn,d

def mon(s,u):
    p=Q(1)
    for i in s:p*=u[i]
    return p

def evaluate(m,u):
    return sum(c*mon(s,u) for s,c in m.items())

def ratio(m,u):
    nn,d=m
    return evaluate(nn,u)/evaluate(d,u)

def crosspieces(m,mp,u,k):
    nn,d=m; nnp,dp=mp
    lo=Q(0);hi=Q(0);pos=Q(0);neg=Q(0)
    for a,ca in nn.items():
        for b,cb in dp.items():
            v=ca*cb*mon(a,u)*mon(b,u)
            if len(a)+len(b)>k:hi+=v;pos+=v
            else:lo+=v
    for a,ca in nnp.items():
        for b,cb in d.items():
            v=ca*cb*mon(a,u)*mon(b,u)
            if len(a)+len(b)>k:hi-=v;neg+=v
            else:lo-=v
    return lo,hi,pos,neg

def falling_binom(x,k):
    out=Q(1)
    for j in range(k):out*=x-j
    return out/factorial(k)

def lagrange(alpha,u,k):
    lam=(1-sum(u),)+tuple(u)
    out=Q(1)
    for a,x in zip(alpha,lam):out*=falling_binom(k*x,a)
    return out

def main():
    records=[];checks=0;worst_ratio=Q(0)
    for n,r,k,q in [(2,1,1,Q(1,2)),(3,2,2,Q(1)),(3,2,3,Q(2)),
                    (3,3,2,Q(3,2)),(2,2,4,Q(3)),(4,2,2,Q(0))]:
        # delta=G=1, so L=1 and kappa=q.
        A=sum(q**j/Q(factorial(j)) for j in range(r+1))
        B=sum(Q(a)*q**(a+b-1)/Q(factorial(a-1)*factorial(b))
              for a in range(1,r+1) for b in range(r+1) if a+b>k)
        C=comb(2*k-1,k)
        alpha=list(compositions(k,n+1))
        nodes=[tuple(Q(a,k) for a in aa[1:]) for aa in alpha]
        queries=[tuple(Q(a,7) for a in aa[1:]) for aa in compositions(7,n+1)]
        pairs=[(model(n,r,q,'max'),model(n,r,q,'zero'))]
        pairs += [(model(n,r,q,'random'),model(n,r,q,'random')) for _ in range(5)]
        for m,mp in pairs:
            h=max(abs(ratio(m,u)-ratio(mp,u)) for u in nodes)
            bound=Q(C)*A*A*h+Q(C+1)*B
            low_nodes=[crosspieces(m,mp,u,k)[0] for u in nodes]
            for u in queries:
                lo,hi,apos,cpos=crosspieces(m,mp,u,k)
                assert 0<=apos<=B and 0<=cpos<=B
                assert abs(hi)<=B
                weights=[lagrange(aa,u,k) for aa in alpha]
                assert sum(weights)==1
                assert sum(abs(w) for w in weights)<=C
                assert lo==sum(w*v for w,v in zip(weights,low_nodes))
                assert abs(ratio(m,u)-ratio(mp,u))<=bound
                if bound:worst_ratio=max(worst_ratio,abs(ratio(m,u)-ratio(mp,u))/bound)
                checks+=1
        records.append({'n':n,'r':r,'k':k,'q':str(q),'C':C,'A':str(A),
                        'B':str(B),'nodes':len(nodes),'query_points':len(queries)})
    result={'arithmetic':'fractions.Fraction exact rational',
            'seed':8317,'outer_pair_command_checks':checks,
            'largest_actual_gap_over_proved_bound':str(worst_ratio),
            'all_checks_passed':True,'cases':records}
    path=Path(__file__).with_name('rational_norming_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
