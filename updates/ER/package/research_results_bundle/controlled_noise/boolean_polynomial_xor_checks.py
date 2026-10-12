"""Exhaustive small-state check of the F2 polynomial XOR innovation sampler."""
import numpy as np

def expand(W,v): return tuple(sorted(set(W)|{w^v for w in W}))
def value(poly,u):
    result=0
    for mask,coefficient in poly.items():
        if mask&u==mask: result^=coefficient
    return result

def check(D=4):
    # Explicit Boolean multilinear coefficient maps: monomial mask -> output bit vector.
    types=[
        (1,3,{0:3,1:5,3:8}),
        (2,3,{3:1,6:2,5:4,7:8}),
        (3,3,{7:8}), # Degree-three minimum weight is attained.
        (1,1,{0:15}),
        (4,2,{}), # Identically-zero map is immediately absorbed.
    ]
    spaces={(0,)}; todo=[(0,)]
    while todo:
        W=todo.pop()
        for v in range(1<<D):
            V=expand(W,v)
            if V not in spaces: spaces.add(V);todo.append(V)
    spaces=sorted(spaces); wi={W:i for i,W in enumerate(spaces)}
    Q=np.zeros((1<<D,1<<D)); G=np.zeros((len(spaces),len(spaces))); R=np.zeros((len(spaces),1<<D))
    tested=0; min_ratio=10
    for W,i in wi.items():
        for x in W: R[i,x]=1/len(W)
        for rate,n,poly in types:
            images=[value(poly,u) for u in range(1<<n)]
            inactive=all(c in W for c in poly.values())
            assert inactive == all(v in W for v in images)
            degree=max([mask.bit_count() for mask in poly]+[0])
            if not inactive:
                prob=sum(v not in W for v in images)/len(images)
                assert prob >= 2**(-degree)
                min_ratio=min(min_ratio,prob/(2**(-degree)))
                for v in images:
                    G[i,wi[expand(W,v)]]+=2*rate/len(images)
                    G[i,i]-=2*rate/len(images)
            tested+=1
    for x in range(1<<D):
        for rate,n,poly in types:
            for u in range(1<<n):
                y=x^value(poly,u)
                Q[x,y]+=rate/(1<<n);Q[x,x]-=rate/(1<<n)
    residual=np.max(abs(G@R-R@Q))
    print(f'D={D}: {len(spaces)} span states, {1<<D} endpoint states')
    print(f'checked {tested} image-containment and innovation-weight instances')
    print(f'generator intertwining residual={residual:.3g}; minimum weight/bound ratio={min_ratio:.3g}')
    assert residual==0

if __name__=='__main__': check()
