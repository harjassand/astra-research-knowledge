"""Small exhaustive algebra diagnostic, NOT an affine compiler.

Brute-force solves intentionally restrict this diagnostic to small dimensions.
The mathematical polynomial construction is reviewed separately.
"""
import itertools,json,random
from pathlib import Path
import numpy as np

def basis(vs):
    out={}
    for v in vs:
        while v:
            p=v.bit_length()-1
            if p in out:v^=out[p]
            else:out[p]=v;break
    return list(out.values())

def lin(cs,v):
    out=0
    for j,c in enumerate(cs):
        if v>>j&1:out^=c
    return out

def dot(v,w):return (v&w).bit_count()%2
def rows_apply(rs,v):return sum(dot(r,v)<<j for j,r in enumerate(rs))

def acquire(F,G,n):
    span=[];power=G[:]
    for _ in range(n):span+=power;power=[lin(F,v) for v in power]
    if len(basis(span))<n:return None
    R=basis([v for v in range(1<<n) if all(dot(v,g)==0 for g in G)])
    Hcols=[rows_apply(R,col) for col in F]
    h=lambda v:lin(Hcols,v)
    A0=[next(v for v in range(1<<n) if h(v)==rows_apply(R,1<<j)) for j in range(n)]
    B=basis([v for v in range(1<<n) if h(v)==0]);g=len(B)
    vs=[B[0]];us=[]
    for i in range(n-1):
        for u in [0]+[1<<j for j in range(g)]:
            v=lin(A0,vs[-1])^lin(B,u)
            if len(basis(vs+[v]))>len(vs):break
        else:raise AssertionError('cyclic reduction failed')
        vs.append(v);us.append(u)
    us.append(0)
    inv=[next(v for v in range(1<<n) if lin(vs,v)==1<<j) for j in range(n)]
    L0=[lin(us,v) for v in inv]
    A1=[A0[j]^lin(B,L0[j]) for j in range(n)]
    w=sum(((inv[j]>>(n-1))&1)<<j for j in range(n))
    k=0
    for j in range(n):
        v=1<<j
        for _ in range(n):v=lin(A1,v)
        k|=dot(w,v)<<j
    A=[A1[j]^(B[0] if k>>j&1 else 0) for j in range(n)]
    assert all(h(A[j])==rows_apply(R,1<<j) for j in range(n))
    assert len(basis(A+B))==n
    for j in range(n):
        v=1<<j
        for _ in range(n):v=lin(A,v)
        assert v==0
    return A,B

def check_kernel(F,G,A,B,n,b):
    g=len(B);d=1<<n;a=lin(A,b)
    maps=[[lin(A,y)^lin(B,z)^a for y in range(d)] for z in range(1<<g)]
    forward=np.zeros((d,d))
    kraus=[]
    for f in maps:
        k=np.zeros((d,d))
        for y,x in enumerate(f):k[y,x]=2**(-g/2);forward[y,x]+=2**(-g)
        kraus.append(k)
    expected=np.zeros((d,d))
    for x in range(d):
        for r in range(1<<len(G)):expected[lin(F,x)^lin(G,r)^b,x]+=2**(-len(G))
    assert np.max(abs(forward-expected))<1e-12
    assert np.linalg.norm(sum(k.T@k for k in kraus)-np.eye(d))<1e-12
    # Test the entire n-step superoperator, not only diagonal inputs.
    channel=sum(np.kron(k,k) for k in kraus)
    pure=np.ones((d,d))/d
    reset=np.outer(pure.reshape(-1),np.eye(d).reshape(-1))
    assert np.linalg.norm(np.linalg.matrix_power(channel,n)-reset)<1e-10
    # Affine-permutation completion: rows A,B plus standard independent rows.
    rows=[sum(((A[j]>>i)&1)<<j for j in range(n))+sum(((B[j]>>i)&1)<<(n+j) for j in range(g)) for i in range(n)]
    for j in range(n+g):
        if len(basis(rows+[1<<j]))>len(rows):rows.append(1<<j)
    assert len(rows)==n+g
    inverse_map={rows_apply(rows,v)^a:v for v in range(1<<(n+g))}
    assert len(inverse_map)==1<<(n+g)
    actual=np.zeros((d,d))
    for x in range(d):
        for rr in range(1<<g):actual[inverse_map[x+(rr<<n)]&(d-1),x]+=2**(-g)
    assert np.max(abs(actual-expected))<1e-12

def run():
    total=accepted=dense=0;rng=random.Random(88411)
    for n in range(1,4):
        for F in itertools.product(range(1<<n),repeat=n):
            for v in range(1,1<<n):
                total+=1;result=acquire(list(F),[v],n)
                if result is not None:
                    accepted+=1
                    if dense<100 and (n<3 or rng.random()<.1):
                        for b in range(1<<n):check_kernel(list(F),[v],*result,n,b)
                        dense+=1
    multi=0
    for _ in range(120):
        n=3;F=[rng.randrange(8) for j in range(n)]
        G=[rng.randrange(8) for j in range(rng.randrange(2,5))]
        result=acquire(F,G,n)
        if result is not None:
            multi+=1
            for b in range(8):check_kernel(F,G,*result,n,b)
    record={'exhaustive_single_input_pairs':total,'controllable_single_input_pairs':accepted,
            'single_input_dense_cases_all_offsets':dense,'multi_input_dense_cases_all_offsets':multi,
            'passed':True,'scope':'Small brute-force diagnostic, not polynomial compiler implementation'}
    out=Path(__file__).with_name('affine_independent_checks.json');out.write_text(json.dumps(record,indent=2)+'\n');print(out.read_text())

if __name__=='__main__':run()
