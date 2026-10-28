"""Independent exact checker: stdlib only; reads final rational JSON alone.

No acquisition, symbolic generator, numerical Gram or optimizer imports.
The full analytic QC/polyconvexity implication is in POLYCONVEX_PROOF.md.
"""
from fractions import Fraction as F
import hashlib,json,time
from pathlib import Path

N=8
def clean(p):return {e:c for e,c in p.items() if c}
def add(*polynomials):
    result={}
    for p in polynomials:
        for e,c in p.items():result[e]=result.get(e,F(0))+c
    return clean(result)
def scale(p,c):return clean({e:c*v for e,v in p.items()})
def mul(p,q):
    result={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(x+y for x,y in zip(e,f));result[g]=result.get(g,F(0))+c*d
    return clean(result)
def diff(p,j):
    result={}
    for e,c in p.items():
        if e[j]:
            g=list(e);g[j]-=1;result[tuple(g)]=c*e[j]
    return result
def evaluate(p,values):
    total=F(0)
    for e,c in p.items():
        term=c
        for j in range(N):term*=values[j]**e[j]
        total+=term
    return total
def var(j):
    e=[0]*N;e[j]=1;return {tuple(e):F(1)}
def invariants(y):
    a,b,c,d=y
    return add(mul(a,a),mul(c,c)),add(mul(b,b),mul(d,d)),add(mul(a,b),mul(c,d)),add(mul(a,d),scale(mul(b,c),-1))
def energy(y):
    u,v,w,q=invariants(y)
    return add(mul(u,u),mul(v,v),scale(mul(w,w),3),scale(mul(q,q),16),scale(mul(q,add(u,scale(v,-1))),4))

def positive_ldl(Q):
    n=len(Q);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        pivot=Q[j][j]-sum(L[j][k]*D[k]*L[j][k] for k in range(j))
        assert pivot>0,(j,pivot)
        D.append(pivot)
        for i in range(j+1,n):
            L[i][j]=(Q[i][j]-sum(L[i][k]*D[k]*L[j][k] for k in range(j)))/pivot
    assert all(Q[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(n))
               for i in range(n) for j in range(n))
    return D

def main():
    start=time.monotonic();root=Path(__file__).resolve().parent
    path=root/'EXACT_POLYCONVEX_SUPPORT.json';raw=path.read_bytes();record=json.loads(raw)
    assert record['input_nine_vector']==['1','1','16','-13','0','0','4','-4','0']
    a=[var(j) for j in range(4)];x=[var(j+4) for j in range(4)]
    f=energy(a);u,v,w,q=invariants(a);qx=invariants(x)[3]
    lam=add(scale(add(u,scale(v,-1)),F(record['alpha'])),scale(q,F(record['delta'])))
    target=add(energy([add(t,s) for t,s in zip(a,x)]),scale(f,-1),
               *(scale(mul(diff(f,j),x[j]),-1) for j in range(4)),scale(mul(lam,qx),-1))
    z=[mul(t,s) for t in a for s in x]+[mul(x[i],x[j]) for i in range(4) for j in range(i,4)]
    Q=[[F(c) for c in row] for row in record['gram']];n=len(z)
    assert n==26 and len(Q)==n and all(len(row)==n for row in Q)
    assert all(Q[i][j]==Q[j][i] for i in range(n) for j in range(n))
    rebuilt={}
    for i in range(n):
        for j in range(i,n):rebuilt=add(rebuilt,scale(mul(z[i],z[j]),Q[i][j]*(1 if i==j else 2)))
    assert target==rebuilt
    rho=F(record['gram_margin']);assert rho==F(1,200)
    D=positive_ldl([[Q[i][j]-(rho if i==j else F(0)) for j in range(n)] for i in range(n)])
    assert D==list(map(F,record['shifted_LDL_pivots']))
    assert F(record['QC_gap_constant'])==rho/2
    interface_path=root/'EXACT_SUPPORT_INTERFACE.json'
    interface_status='NOT_PRESENT'
    if interface_path.exists():
        interface=json.loads(interface_path.read_text())
        assert interface['input_nine_coefficients']==record['input_nine_vector']
        assert interface['multiplier_basis']==['u-v','q']
        values=[Q[i][j] for i in range(n) for j in range(i,n)]+[F(record['alpha']),F(record['delta'])]
        assert len(values)==interface['total_variables']
        assert all(sum(F(c)*values[j] for j,c in row['entries'])==F(row['rhs']) for row in interface['rows'])
        interface_status='ALL215_EXACT_AFFINE_EQUATIONS_REPLAYED'
    atI=[F(1),F(0),F(0),F(1)]+[F(0)]*4
    h=[evaluate(diff(diff(f,i),j),atI) for i,j in [(0,0),(0,3),(3,3)]]
    detsq=mul(q,q)
    hq=[evaluate(diff(diff(detsq,i),j),atI) for i,j in [(0,0),(0,3),(3,3)]]
    assert h==[68,64,20] and hq==[2,4,2]
    coeff=[h[0]*h[2]-h[1]**2,-h[0]*hq[2]-hq[0]*h[2]+2*h[1]*hq[1],hq[0]*hq[2]-hq[1]**2]
    assert coeff==[-2736,336,-12]==[-12*(14**2+32),-12*(-28),-12]
    output={
        'status':'EXACT_SUPPORT_AND_STRICT_GRAM_VERIFIED',
        'certificate_sha256':hashlib.sha256(raw).hexdigest(),
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'features':n,'strict_positive_pivots':len(D),
        'polynomial_identity':'RECONSTRUCTED_EXACTLY_FROM_LITERAL_F',
        'exported_interface':interface_status,
        'alpha':record['alpha'],'delta':record['delta'],
        'gram_margin':str(rho),'QC_gap_constant':str(rho/2),
        'all_real_det_square_convex_subtractions':'EXCLUDED_BY_EXACT_NEGATIVE_HESSIAN_MINOR',
        'maximum_pivot_numerator_or_denominator_bits':max(max(abs(d.numerator).bit_length(),d.denominator.bit_length()) for d in D),
        'imports':'PYTHON_STDLIB_ONLY','wall_seconds':time.monotonic()-start,
        'scope':'GLOBAL_POLYNOMIAL_SUPPORT_AND_QC_FOR_THIS_F; FULL_NINE_COEFFICIENT_QC_NOT_PROVED',
    }
    (root/'VERIFY_SUPPORT.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))

if __name__=='__main__':main()
