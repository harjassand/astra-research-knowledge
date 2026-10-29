"""Exact rational qualification of the ordinary positive comparator."""
from fractions import Fraction as F
from pathlib import Path
import json,time,hashlib

HERE=Path(__file__).resolve().parent

def ldl(A):
    n=len(A);L=[[F(int(i==j)) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=A[j][j]-sum(L[j][k]**2*D[k] for k in range(j))
        assert d>0,(j,d);D.append(d)
        for i in range(j+1,n):L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/d
    assert all(sum(L[i][k]*D[k]*L[j][k] for k in range(n))==A[i][j] for i in range(n) for j in range(n))
    return D

def main():
    start=time.perf_counter();path=HERE/'ORDINARY_PC_a12_b3.975.json';raw=path.read_bytes();p=json.loads(raw)
    den=10**8;Q=[[F(round(x*den),den) for x in row] for row in p['Q']]
    k=[F(round(x*den),den) for x in p['k']];mons=[tuple(m) for m in p['monomials']];look={m:i for i,m in enumerate(mons)}
    rhs=[F(x) for x in p['rhs']]
    for ki,nu in zip(k,p['kmon']):
        for e,sign in [((1,0,0,1),1),((0,1,1,0),-1)]:
            rhs[look[tuple(nu)+e]]-=sign*ki
    z=[tuple(m) for m in p['z']];n=len(z);got=[F(0)]*len(mons);slots={}
    for i in range(n):
        for j in range(n):
            m=tuple(a+b for a,b in zip(z[i],z[j]));got[look[m]]+=Q[i][j]
            slots.setdefault(m,(i,j))
    for mon,index in look.items():
        delta=rhs[index]-got[index];i,j=slots[mon]
        if i==j:Q[i][j]+=delta
        else:Q[i][j]+=delta/2;Q[j][i]+=delta/2
    check=[F(0)]*len(mons)
    for i in range(n):
        for j in range(n):check[look[tuple(a+b for a,b in zip(z[i],z[j]))]]+=Q[i][j]
    assert check==rhs and all(Q[i][j]==Q[j][i] for i in range(n) for j in range(n))
    rho=F(1,200);shift=[[Q[i][j]-(rho if i==j else 0) for j in range(n)] for i in range(n)];pivots=ldl(shift)
    result=dict(input_sha256=hashlib.sha256(raw).hexdigest(),a='12',b='159/40',Q=[[str(x) for x in row] for row in Q],
                k=[str(x) for x in k],kmon=p['kmon'],z=p['z'],identity_exact=True,gram_shift=str(rho),
                ldl_pivots=[str(x) for x in pivots],strong_jensen_constant='1/400',seconds=time.perf_counter()-start,
                scope='This ordinary global polynomial minor-support certificate proves PC and a stronger QC margin for the nearby positive control; it does not certify the original non-PC target')
    (HERE/'ORDINARY_PC_EXACT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['Q','k','kmon','z','ldl_pivots']},indent=2))

if __name__=='__main__':main()
