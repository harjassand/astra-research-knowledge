"""Independent tuple-cell and binary-matrix oracle, standard library only."""
import itertools as it, json, subprocess, random, time
from pathlib import Path
ROOT=Path(__file__).parent
ORI=list(it.combinations(range(4),2))
def toggle(s,v):
    if v in s:s.remove(v)
    else:s.add(v)
def cells(L,k):return [(x,a) for x in it.product(range(L),repeat=4) for a in it.combinations(range(4),k)]
def bd(chain,L):
    out=set()
    for x,a in chain:
        for d in a:
            b=tuple(v for v in a if v!=d);y=list(x);y[d]=(y[d]+1)%L
            toggle(out,(x,b));toggle(out,(tuple(y),b))
    return out
def hom(chain,cut=0):
    out=set()
    for x,a in chain:
        if all(x[d]==cut for d in a):toggle(out,a)
    return out
def rank(vectors):
    piv={}
    for v in vectors:
        while v:
            p=v.bit_length()-1
            if p in piv:v^=piv[p]
            else:piv[p]=v;break
    return len(piv)
def matrix_rank(L,k):
    index={c:i for i,c in enumerate(cells(L,k-1))}
    return rank(sum(1<<index[e] for e in bd({c},L)) for c in cells(L,k))
def algebra():
    out=[]
    for L in (2,3,4):
        n=0
        for k in (2,3):
            for c in cells(L,k):
                b=bd({c},L);assert not bd(b,L)
                if k==3:assert not hom(b)
                n+=1
        for a in ORI:
            for anchor in (0,L-1):
                sheet={(x,a) for x in it.product(range(L),repeat=4) if all(x[d]==anchor for d in range(4) if d not in a)}
                assert not bd(sheet,L)
                for cut in range(L):assert hom(sheet,cut)=={a}
        r2,r3=matrix_rank(L,2),matrix_rank(L,3)
        assert r2==r3==3*L**4-3
        assert 6*L**4-r2-r3==6
        out.append(dict(L=L,boundary_checks=n,rank_d2=r2,rank_d3=r3,H2=6))
    return out
if __name__=='__main__':
    t=time.monotonic();res={'algebra':algebra(),'status':'PASS','seconds':time.monotonic()-t}
    (ROOT/'independent_algebra_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res))

def literal_H(edges,L):
    result=set()
    for x,(k,) in edges:
        for j in range(4):
            if j==k or (k<j and x[k]!=L-1):continue
            coords=[]
            for d in range(4):
                if d<j:coords.append(range(L) if d==k else [0])
                elif d==j:coords.append(range(x[j]))
                else:coords.append([x[d]])
            for y in it.product(*coords):toggle(result,(y,tuple(sorted((j,k)))))
    return result

def encode(cell,L):
    x,a=cell;v=0
    for q in x:v=v*L+q
    # orientation-major bit arrays; caller confirms executable layout.
    return (a[0] if len(a)==1 else ORI.index(a))*L**4+v

def decode_id(idx,L,k):
    o,v=divmod(idx,L**4);x=[]
    for _ in range(4):x.append(v%L);v//=L
    return tuple(reversed(x)),((o,) if k==1 else ORI[o])
