"""Exact small reconstruction diagnostic; NOT the full N51 generator.

The learner sees only matrix outputs of x1^-1 x2 and a supplied regular
centre. For this tiny check its detector enumerates short tail words,
which is exponential in a general state bound. REPORT.txt replaces that
detector by N51 plus nilpotent grading to obtain the polynomial theorem.
"""
from fractions import Fraction as Q
from itertools import product
import json
import random
from pathlib import Path


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum((x*y for x,y in zip(row,col)), Q(0))
             for col in zip(*b)] for row in a]


def inv(a):
    n=len(a)
    z=[list(row)+list(e) for row,e in zip(a,eye(n))]
    for j in range(n):
        p=next((i for i in range(j,n) if z[i][j]),None)
        if p is None:
            raise ZeroDivisionError("singular")
        z[j],z[p]=z[p],z[j]
        v=z[j][j]
        z[j]=[x/v for x in z[j]]
        for i in range(n):
            if i!=j:
                v=z[i][j]
                z[i]=[x-v*y for x,y in zip(z[i],z[j])]
    return [row[n:] for row in z]


def coordinates(basis, v):
    """Solve sum_i c_i basis_i=v, returning None on independence."""
    if not basis:
        return [] if not any(v) else None
    h=len(basis)
    z=[[basis[j][i] for j in range(h)]+[v[i]] for i in range(len(v))]
    r=0
    piv=[]
    for j in range(h):
        p=next((i for i in range(r,len(z)) if z[i][j]),None)
        if p is None:
            continue
        z[r],z[p]=z[p],z[r]
        t=z[r][j]
        z[r]=[x/t for x in z[r]]
        for i in range(len(z)):
            if i!=r:
                t=z[i][j]
                z[i]=[x-t*y for x,y in zip(z[i],z[r])]
        piv.append(j)
        r+=1
    if any(not any(row[:h]) and row[h] for row in z):
        return None
    c=[Q(0)]*h
    for i,j in enumerate(piv):
        c[j]=z[i][h]
    return c


oracle_calls=0
def oracle(x):
    global oracle_calls
    oracle_calls+=1
    return mul(inv(x[0]),x[1])


centre=[Q(2),Q(3)]
coefficient_cache={}
def coefficient(w):
    if w in coefficient_cache:
        return coefficient_cache[w]
    t=len(w)+1
    x=[]
    for j,a in enumerate(centre):
        z=[[a*v for v in row] for row in eye(t)]
        for h,letter in enumerate(w):
            if letter==j:
                z[h][h+1]=Q(1)
        x.append(z)
    c=oracle(x)[0][-1]
    coefficient_cache[w]=c
    return c


bound=4
tails=[w for length in range(bound) for w in product(range(2),repeat=length)]
def feature(p):
    return [coefficient(p+w) for w in tails]


prefixes=[]
basis=[]
if any(feature(())):
    prefixes=[()]
    basis=[feature(())]
cursor=0
while cursor<len(prefixes):
    p=prefixes[cursor]
    for j in range(2):
        w=p+(j,)
        v=feature(w)
        if coordinates(basis,v) is None:
            prefixes.append(w)
            basis.append(v)
    cursor+=1
assert len(prefixes)<=bound
q=len(prefixes)
B=[[] for _ in range(2)]
for p in prefixes:
    for j in range(2):
        c=coordinates(basis,feature(p+(j,)))
        assert c is not None
        B[j].append(c)
alpha=[Q(int(i==0)) for i in range(q)]
beta=[coefficient(p) for p in prefixes]
C=eye(q)
for i in range(q):
    for h in range(q):
        C[i][h]+=sum(centre[j]*B[j][i][h] for j in range(2))


def descriptor(x):
    d=len(x[0])
    P=[[Q(0) for _ in range(q*d)] for _ in range(q*d)]
    for i in range(q):
        for h in range(q):
            for a in range(d):
                for b in range(d):
                    P[i*d+a][h*d+b]=(C[i][h] if a==b else Q(0)) \
                        -sum(B[j][i][h]*x[j][a][b] for j in range(2))
    Pinv=inv(P)
    return [[sum((alpha[i]*Pinv[i*d+a][h*d+b]*beta[h]
                  for i in range(q) for h in range(q)),Q(0))
             for b in range(d)] for a in range(d)]


rng=random.Random(5107)
tests=0
for a in range(-3,4):
    if not a:
        continue
    for b in range(-2,3):
        x=[[[Q(a)]],[[Q(b)]]]
        assert descriptor(x)==oracle(x)
        tests+=1
for d in [2,3]:
    accepted=0
    while accepted<20:
        x=[[[Q(rng.randrange(-3,4)) for _ in range(d)] for _ in range(d)]
           for _ in range(2)]
        try:
            expected=oracle(x)
        except ZeroDivisionError:
            continue
        assert descriptor(x)==expected
        tests+=1
        accepted+=1
result={"scope":"tiny exact finite diagnostic; exhaustive short-word detector",
        "N51_generator_executed":False,"oracle_calls":oracle_calls,
        "learned_state_dimension":q,"prefix_basis":[list(p) for p in prefixes],
        "B":[[[str(v) for v in row] for row in b] for b in B],
        "C":[[str(v) for v in row] for row in C],
        "beta":[str(v) for v in beta],"exact_domain_and_value_cases":tests}
path=Path(__file__).with_name("toy_acquisition_results.json")
path.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
