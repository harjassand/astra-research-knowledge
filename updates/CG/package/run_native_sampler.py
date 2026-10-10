"""Finite-prime-field implementation; no enumeration of dual vectors or points.
The uniformity proof is in DUAL_KERNEL_COMPATIBILITY.md. This smoke test
checks native certificate acquisition, arithmetic, feasibility and trial counts.
It is not a statistical proof of exact uniformity.
"""
from pathlib import Path
import json,random,time
from verify_dual_kernel import acquire_qpoly,qpoly_matrix,rank,transpose,lincomb,mv,F,irreducible
ROOT=Path(__file__).resolve().parent

def affine_solve(A,b,p,n):
    a=[list(row)+[bb%p] for row,bb in zip(A,b)];nr=len(a);r=0;piv=[]
    for j in range(n):
        k=next((i for i in range(r,nr) if a[i][j]%p),None)
        if k is None:continue
        a[k],a[r]=a[r],a[k];inv=pow(a[r][j]%p,-1,p);a[r]=[(v*inv)%p for v in a[r]]
        for i in range(nr):
            if i!=r and a[i][j]:
                c=a[i][j];a[i]=[(u-c*v)%p for u,v in zip(a[i],a[r])]
        piv.append(j);r+=1
        if r==nr:break
    if any(not any(row[:n]) and row[n] for row in a):return r,None,None
    base=[0]*n
    for i,j in enumerate(piv):base[j]=a[i][n]
    basis=[]
    for j in range(n):
        if j in piv:continue
        v=[0]*n;v[j]=1
        for i,k in enumerate(piv):v[k]=-a[i][j]%p
        basis.append(v)
    return r,base,basis

def draw_affine(base,basis,p,rng):
    out=base[:]
    for v in basis:
        a=rng.randrange(p)
        if a:out=[(x+a*y)%p for x,y in zip(out,v)]
    return out

def digits(k,m,q):
    v=[]
    for _ in range(m):v.append(k%q);k//=q
    return v

def sample(A,c,g,R,p,rng):
    m=len(A);nx=len(A[0]);ny=len(A[0][0]);trials=0
    D=p**R+p**m-1
    while True:
        trials+=1;u=rng.randrange(D)
        if u<p**R:
            x=[rng.randrange(p) for _ in range(nx)]
        else:
            lam=digits(u-p**R+1,m,p);Al=lincomb(A,lam,p);cl=mv(transpose(c),lam,p)
            r,base,basis=affine_solve(transpose(Al),[-v%p for v in cl],p,nx)
            assert r>=R,'Invalid global rank envelope: no output is valid under this certificate.'
            if any(rng.randrange(p) for _ in range(r-R)):continue
            if base is None:continue
            x=draw_affine(base,basis,p,rng)
        Fx=[[(v+w)%p for v,w in zip(row,ci)] for row,ci in zip(F(A,x,p),c)]
        r,base,basis=affine_solve(Fx,g(x),p,ny)
        if base is None:continue
        y=draw_affine(base,basis,p,rng)
        assert mv(Fx,y,p)==g(x)
        return x,y,trials

def main():
    rng=random.Random(261010);n=16;m=6;s=8;poly=0x1100b;assert irreducible(poly,n)
    coeff=[[rng.randrange(1<<n) for _ in range(s+1)] for _ in range(m)]
    A=[qpoly_matrix(c,poly,n) for c in coeff]
    t=time.perf_counter();cert=acquire_qpoly(A,poly,n);cert_time=time.perf_counter()-t
    assert cert['independent'] and cert['certified_min_rank']==8
    c=[[rng.randrange(2) for _ in range(n)] for _ in range(m)]
    def g(x):return [(sum(x[(3*i+j)%n] for j in range(4))%2)^int(all(x[(i+j)%n] for j in range(i+2))) for i in range(m)]
    rows=[];t=time.perf_counter()
    for i in range(200):
        x,y,k=sample(A,c,g,8,2,rng);rows.append({'x':x,'y':y,'trials':k})
    elapsed=time.perf_counter()-t
    out={'q':2,'n':n,'m':m,'qdegree':s,'rank_bound':8,'samples':200,'total_trials':sum(x['trials'] for x in rows),
      'mean_trials':sum(x['trials'] for x in rows)/len(rows),'max_trials':max(x['trials'] for x in rows),
      'all_joint_constraints_verified':True,'enumerated_dual_vectors':False,'enumerated_assignments':False,
      'certificate_acquisition_seconds':cert_time,'sampling_seconds':elapsed,'field_polynomial':poly,
      'coefficients':coeff,'c':c,'native_certificate':cert,'sample_records':rows}
    (ROOT/'NATIVE_SAMPLER_RESULTS.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ('coefficients','c','native_certificate','sample_records')},indent=2))
if __name__=='__main__':main()
