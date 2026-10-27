"""Independent exact local determinant criterion on hidden parity K4 fixtures.
No compiler/Pfaffian solver is claimed. Root's finite checks support only the
local algebraic reduction in LOCAL_CRITERION.md.
"""
from pathlib import Path
from itertools import product,combinations
import json,time
import sympy as S
HERE=Path(__file__).resolve().parent
BITS=list(product(range(2),repeat=3))
EDGES=list(combinations(range(4),2))
NEIGHBORS={v:[w for w in range(4) if w!=v] for v in range(4)}
def simp(x):return S.simplify(S.expand(x))
def leg(v,w):return NEIGHBORS[v].index(w)
def transform(T,axis,G):
    out={}
    for b in BITS:
        out[b]=sum(G[b[axis],j]*T[tuple(j if a==axis else b[a] for a in range(3))] for j in range(2))
    return out
def parity_tensors(odd=False,perturb=False):
    tensors={}
    for v in range(4):
        parity=1 if odd and v==0 else 0
        entries=iter([S.Integer(v+1),S.Integer(v+2),S.Integer(v+3),S.Integer(v+5)])
        tensors[v]={b:(next(entries) if sum(b)%2==parity else S.Integer(0)) for b in BITS}
    if perturb:tensors[0][0,0,1]=S.Integer(1)
    for k,(v,w) in enumerate(EDGES):
        a=k%3+1;b=(k+1)%2+1
        G=S.Matrix([[1,a],[b,1+a*b]])
        tensors[v]=transform(tensors[v],leg(v,w),G)
        tensors[w]=transform(tensors[w],leg(w,v),G.inv().T)
    return tensors
def cp(T):
    M=[S.Matrix(2,2,lambda i,j:T[x,i,j]) for x in range(2)]
    t=next(S.Integer(z) for z in [0,1,-1,2] if (M[0]+z*M[1]).det()!=0)
    A=M[0]+t*M[1];C=M[1]*A.inv()
    eig=C.eigenvects();assert len(eig)==2 and all(mult==1 for _,mult,_ in eig)
    values=[r[0] for r in eig];U=S.Matrix.hstack(*(r[2][0] for r in eig));V=U.inv()*A
    factors=[ [S.Matrix([1-t*values[s],values[s]]) for s in range(2)],
              [U[:,s] for s in range(2)],[V[s,:].T for s in range(2)] ]
    for b in BITS:
        assert simp(sum(product_scalar(factors[a][s][b[a]] for a in range(3)) for s in range(2))-T[b])==0
    return factors
def product_scalar(xs):
    out=S.Integer(1)
    for x in xs:out*=x
    return out
def qform(T,axis,x):
    other=[a for a in range(3) if a!=axis]
    def entry(i,j):
        b=[0]*3;b[other[0]]=i;b[other[1]]=j
        out=0
        for h in range(2):
            b[axis]=h;out+=x[h]*T[tuple(b)]
        return out
    return simp(S.Matrix(2,2,entry).det())
def full_contraction(tensors):
    total=0
    for bits in product(range(2),repeat=len(EDGES)):
        values=dict(zip(EDGES,bits));term=1
        for v in range(4):term*=tensors[v][tuple(values[tuple(sorted((v,w)))] for w in NEIGHBORS[v])]
        total+=term
    return simp(total)
def test(odd=False,perturb=False):
    start=time.perf_counter();tensors=parity_tensors(odd,perturb)
    factors={v:cp(T) for v,T in tensors.items()}
    beta={}
    for v in range(4):
        value=S.Integer(1)
        for w in NEIGHBORS[v]:
            f=factors[v][leg(v,w)]
            value*=qform(tensors[w],leg(w,v),f[1])/qform(tensors[w],leg(w,v),f[0])
        beta[v]=simp(value)
    passes=all(simp(b-1)==0 for b in beta.values())
    assert passes== (not perturb)
    R=S.Integer(1)
    for v,w in EDGES:
        left=factors[v][leg(v,w)];right=factors[w][leg(w,v)]
        M=S.Matrix(2,2,lambda a,b:simp((left[a].T*right[b])[0]))
        assert all(x!=0 for x in M)
        R*=M[1,1]/M[0,0]
    numeric=complex(S.N(R,30));truth=full_contraction(tensors)
    if not perturb:
        assert abs(numeric-(-1 if odd else 1))<1e-20
        assert (truth==0)==odd
    return {'odd_vertex':odd,'perturbed':perturb,'local_beta':[str(beta[v]) for v in range(4)],
      'balance_test_passes':passes,'global_R_numeric':[numeric.real,numeric.imag],
      'exact_original_contraction':str(truth),'seconds':time.perf_counter()-start}
if __name__=='__main__':
    result=[]
    for odd,perturb in [(False,False),(True,False),(False,True)]:
        r=test(odd,perturb);result.append(r);print(json.dumps(r),flush=True)
    (HERE/'LOCAL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
