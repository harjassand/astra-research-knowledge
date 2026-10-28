#!/usr/bin/env python3
"""Proved polynomial evaluation of every nilpotent matrix Kloosterman pair.

See POLYNOMIAL_NILPOTENT_PAIR_THEOREM.tex. The core uses O(n^5) integer
arithmetic operations and two adjacent column heights, with no partition,
field-element, subspace, or map enumeration. The nilpotent string formula
holds for every prime power q. The explicit-field/full-pair wrappers use
the existing characteristic-two field and regular-Kloosterman backend.
"""
from functools import lru_cache
from math import prod

def columns(partition):
    return tuple(sum(x>=j for x in partition) for j in range(1,max(partition,default=0)+1))

@lru_cache(None)
def qpower(q,e):
    return q**e

@lru_cache(None)
def choose(n,k,q):
    if not 0<=k<=n:return 0
    k=min(k,n-k);value=1
    for j in range(1,k+1):
        value=value*(qpower(q,n-k+j)-1)//(qpower(q,j)-1)
    return value

@lru_cache(None)
def gl_order(n,q):
    return qpower(q,n*(n-1)//2)*prod(qpower(q,j)-1 for j in range(1,n+1))

def pair_height_transition(q,a,b,e,f,c,d,t,u):
    """One local positive weight for columns (a,b,e,f), current (c,d), next (t,u)."""
    if not (0<=t<=c<=min(a,b) and 0<=u<=d<=min(e,f)):return 0
    exponent=c+t*(a+b+e+f-t)+d+u*(e+f-u)+d*(a+b-c-t)
    return (qpower(q,exponent)*choose(a-t,c-t,q)*choose(b-t,c-t,q)*gl_order(c-t,q)
            *choose(e-u,d-u,q)*choose(f-u,d-u,q)*gl_order(d-u,q))

def polynomial_nilpotent_pair(parts,q,stats=None):
    """Exact K(A,B) from acquired (length, terminal_color) nilpotent strings."""
    if not isinstance(q,int) or q<2:raise ValueError('q must be an integer at least two (prime power for counting)')
    parts=tuple(tuple(p) for p in parts)
    if any(len(p)!=2 or not isinstance(p[0],int) or p[0]<1 or p[1] not in (0,1) for p in parts):
        raise ValueError('invalid string data')
    odd=[[(l+1)//2 for l,c in parts if l%2 and c==i] for i in (0,1)]
    even=[[l//2 for l,c in parts if l%2==0 and c==i] for i in (0,1)]
    o=len(odd[0])
    if len(odd[1])!=o:raise ValueError('unbalanced strings')
    seq=[columns(p) for p in odd+even];L=max(map(len,seq),default=0)
    a,b,e,f=[s+(0,)*(L-len(s)) for s in seq]
    states={(0,0):1};transitions=0;peak_states=1
    for aj,bj,ej,fj in reversed(tuple(zip(a,b,e,f))):
        new={}
        for (t,u),tail in states.items():
            for c in range(t,min(aj,bj)+1):
                co=qpower(q,c+t*(aj+bj+ej+fj-t))*choose(aj-t,c-t,q)*choose(bj-t,c-t,q)*gl_order(c-t,q)
                for d in range(u,min(ej,fj)+1):
                    ce=qpower(q,d+u*(ej+fj-u)+d*(aj+bj-c-t))*choose(ej-u,d-u,q)*choose(fj-u,d-u,q)*gl_order(d-u,q)
                    key=c,d;new[key]=new.get(key,0)+co*ce*tail;transitions+=1
        states=new;peak_states=max(peak_states,len(states))
    weighted=sum(v for (c,d),v in states.items() if c==o)
    divisor=q**(o*(o+1)//2)
    if weighted%divisor:raise ArithmeticError('nonintegral marked-quotient normalization')
    n=sum(l for l,c in parts)//2
    value=(-1)**(n+o)*q**(n*(n-1)//2)*(weighted//divisor)
    if stats is not None:
        stats.update(algorithm='Hall Fourier two-height transfer',matrix_rank=n,
                     field_size=q,field_size_bits=q.bit_length(),
                     field_degree=(q.bit_length()-1 if not q&(q-1) else None),odd_strings_per_color=o,
                     columns=L,transitions=transitions,peak_height_states=peak_states,
                     enumerated_partitions=0,enumerated_subspaces=0,enumerated_maps=0,
                     enumerated_field_elements=0)
    return value

def nilpotent_pair_polynomial_degree(parts):
    """Exact degree in q; leading coefficient is (-1)^(n+odd_pairs)."""
    parts=tuple(tuple(p) for p in parts)
    odd=[[(l+1)//2 for l,c in parts if l%2 and c==i] for i in (0,1)]
    even=[[l//2 for l,c in parts if l%2==0 and c==i] for i in (0,1)]
    o=len(odd[0])
    if len(odd[1])!=o:raise ValueError('unbalanced strings')
    seq=[columns(p) for p in odd+even];L=max(map(len,seq),default=0)
    a,b,e,f=[s+(0,)*(L+1-len(s)) for s in seq]
    n=sum(l for l,c in parts)//2
    return n*(n-1)//2-o*(o+1)//2+sum(
        a[j]*b[j]+e[j]*f[j]+min(a[j],b[j])+min(e[j],f[j])
        +min(a[j+1],b[j+1])*max(e[j],f[j])+min(e[j],f[j])*max(a[j],b[j])
        for j in range(L))

class PolynomialNilpotentPairCounter:
    """Adapter for callers that repeatedly evaluate acquired string types."""
    def __init__(self,q):
        self.q=q;self.calls=0;self.transitions=0;self.peak_states=0
    def count(self,parts):
        stats={};value=polynomial_nilpotent_pair(parts,self.q,stats)
        self.calls+=1;self.transitions+=stats['transitions']
        self.peak_states=max(self.peak_states,stats['peak_height_states'])
        return value
    def metadata(self):
        return dict(algorithm='Hall Fourier two-height transfer',calls=self.calls,
                    transitions=self.transitions,peak_height_states=self.peak_states,
                    enumerated_partitions=0,enumerated_subspaces=0,
                    enumerated_maps=0,enumerated_field_elements=0)

def matrix_pair_from_primary_and_alternating_ranks(primary_data,matrix_rank,field_h,
                                                   ranks_start_A,ranks_start_B):
    """Full pair intrinsic interface: reduced AB primary data and alternating ranks.

    Rank sequences are A,AB,ABA,... and B,BA,BAB,..., ending at regular rank.
    Ranks of a regular algebra action must first be divided by matrix size.
    """
    from matrix_kloosterman import Field,matrix_kloosterman_from_primary
    from cyclic_endpoint_cubic import cyclic_strings_from_source_ranks
    Fq=Field(field_h);n=matrix_rank
    if sum((len(p['irreducible'])-1)*p['multiplicity'] for p in primary_data)!=n:
        raise ValueError('primary dimension')
    regular=[p for p in primary_data if list(p['irreducible'])!=[0,1]]
    u=sum((len(p['irreducible'])-1)*p['multiplicity'] for p in regular);v=n-u
    x=list(ranks_start_A);y=list(ranks_start_B)
    if not x or len(x)!=len(y) or x[-1]!=u or y[-1]!=u:
        raise ValueError('nonterminated alternating ranks')
    if any(not isinstance(r,int) or not u<=r<=n for r in x+y):raise ValueError('invalid ranks')
    ranks=[[v],[v]]
    for k in range(1,len(x)+1):
        ranks[0].append((y if k%2 else x)[k-1]-u)
        ranks[1].append((x if k%2 else y)[k-1]-u)
    parts=cyclic_strings_from_source_ranks([v,v],ranks,2)
    stats={};nil=polynomial_nilpotent_pair(parts,Fq.q,stats)
    reg,reg_meta=matrix_kloosterman_from_primary(regular,u,field_h)
    return Fq.q**(u*v)*reg*nil,dict(matrix_rank=n,field_degree=Fq.a,
        regular_dimension=u,nilpotent_dimension=v,nilpotent_strings=parts,
        nilpotent_backend=stats,regular_backend=reg_meta)

def matrix_pair_all_sources(A,B,field_h=3):
    """Exact polynomial K_n(A,B) for arbitrary explicit field matrices A,B."""
    from matrix_kloosterman import Field,mmul,rref,charpoly,factor_polynomial,primary_columns
    Fq=Field(field_h);n=len(A)
    if len(B)!=n or any(len(row)!=n for row in A+B):raise ValueError('matrix shape')
    AB=mmul(A,B,Fq);primary=[]
    for g,b in factor_polynomial(charpoly(AB,Fq),Fq):
        primary.append(dict(irreducible=g,multiplicity=b,jordan_columns=primary_columns(AB,g,b,Fq)))
    x=[];y=[];P=A;Q=B
    for k in range(1,2*n+2):
        x.append(len(rref(P,Fq)[1]));y.append(len(rref(Q,Fq)[1]))
        P=mmul(P,B if k%2 else A,Fq);Q=mmul(Q,A if k%2 else B,Fq)
    return matrix_pair_from_primary_and_alternating_ranks(primary,n,field_h,x,y)
