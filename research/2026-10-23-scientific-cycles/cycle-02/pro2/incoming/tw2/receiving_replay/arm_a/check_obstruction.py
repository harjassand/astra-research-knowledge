"""Supplementary checks of the proof's identities; no numerical output proves the theorem."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import time, json, math, resource, signal
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
signal.alarm(45)
from fractions import Fraction as Q
from pathlib import Path
start=time.monotonic()
out=Path(__file__).resolve().parent

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def matvec(A,x): return [dot(a,x) for a in A]
def edges(n): return [(i,j) for i in range(n) for j in (i+1,i+2) if j<n]
A=[[[0,-1,0],[1,0,0],[0,0,0]],[[0,0,-1],[0,0,0],[1,0,0]],[[0,0,0],[0,0,-1],[0,1,0]]]
records=[]
for m in (1,2,3,7,13):
    f={i:max(0,m-abs(i)) for i in range(-m-3,m+4)}
    S=sum(v*v for v in f.values())
    E1=sum((f.get(i+1,0)-v)**2 for i,v in f.items())
    E2=sum((f.get(i+2,0)-v)**2 for i,v in f.items())
    assert S==Q(2*m**3+m,3)
    assert E1==2*m
    assert E2==8*m-6
    assert E1+E2<=10*m
    records.append({'m':m,'bump_square_sum':S,'adjacent_difference_energy':E1,'distance_two_difference_energy':E2})
# Exact rational adjoint identity and rotation-field residual identity, n=16.
n=16; m=2
X=[[Q(((i+2)*(j+3)+i*i+3*j*j)%7-3,6) for j in range(3)] for i in range(n)]
assert all(0<dot(x,x)<=1 for x in X)
E=edges(n)
diag=[Q((i*7)%9-4,5) for i in range(n)]
b={e:Q((e[0]*3+e[1]*5)%11-5,7) for e in E}
DX=[[diag[i]*v for v in X[i]] for i in range(n)]
for (i,j),v in b.items():
    for k in range(3): DX[i][k]+=v*X[j][k]; DX[j][k]+=v*X[i][k]
checks=0
for block in range(4):
    center=(2*block+1)*m
    f=[max(0,m-abs(i+1-center)) for i in range(n)]
    for rot in A:
        Y=[[f[i]*v for v in matvec(rot,X[i])] for i in range(n)]
        ad=[dot(Y[i],X[i]) for i in range(n)]
        ae={(i,j):(dot(Y[i],X[j])+dot(Y[j],X[i]))/2 for i,j in E}
        assert all(v==0 for v in ad)
        lhs=sum(dot(Y[i],DX[i]) for i in range(n))
        rhs=sum(diag[i]*ad[i] for i in range(n))+2*sum(b[e]*ae[e] for e in E)
        assert lhs==rhs
        actual=sum(v*v for v in ad)+2*sum(v*v for v in ae.values())
        predicted=Q(1,2)*sum((f[j]-f[i])**2*dot(X[i],matvec(rot,X[j]))**2 for i,j in E)
        assert actual==predicted
        assert actual<=5*m
        checks+=1
    for x in X: assert sum(dot(matvec(rot,x),matvec(rot,x)) for rot in A)==2*dot(x,x)
report={'exact_checks_passed':True,'adjoint_and_rotation_cases':checks,'bump_energy_checks':records,'numerical_checks':[]}
# A modest sanity check only: use an orthonormal supported-symmetric matrix basis.
try:
    import numpy as np
    rng=np.random.default_rng(20261021)
    for m in (1,2,4,8):
        n=8*m; E=edges(n)
        X=rng.normal(size=(n,3)); X/=np.linalg.norm(X,axis=1)[:,None]
        X*=rng.uniform(.5,1,size=(n,1))
        r=float(np.linalg.norm(X,axis=1).min())
        M=np.zeros((3*n,n+len(E)))
        for i in range(n): M[3*i:3*i+3,i]=X[i]
        for k,(i,j) in enumerate(E):
            M[3*i:3*i+3,n+k]=X[j]/math.sqrt(2)
            M[3*j:3*j+3,n+k]=X[i]/math.sqrt(2)
        U,s,Vh=np.linalg.svd(M,full_matrices=True)
        assert M.shape==(3*n,3*n-3)
        W=[]
        for block in range(4):
            center=(2*block+1)*m
            f=np.maximum(0,m-np.abs(np.arange(1,n+1)-center))
            YY=[f[:,None]*(X@np.array(rot).T) for rot in A]
            Y=max(YY,key=lambda y:np.linalg.norm(y))
            W.append((Y/np.linalg.norm(Y)).ravel())
        W=np.stack(W,axis=1)
        assert np.max(np.abs(W.T@W-np.eye(4)))<1e-12
        restricted=float(np.linalg.norm(M.T@W,2))
        epsilon=3*math.sqrt(5)/(r*m)
        assert restricted<=epsilon*(1+1e-12)
        assert s[-1]<=restricted*(1+1e-12)
        # Intersection W with range(M): annihilate all three exact left-null vectors.
        N=U[:,-3:]
        _,_,V=np.linalg.svd(N.T@W,full_matrices=True)
        y=W@V[-1]
        assert np.linalg.norm(N.T@y)<1e-12
        assert np.linalg.norm(M.T@y)<=epsilon*(1+1e-12)
        v=Vh[-1]
        D=np.diag(v[:n])
        for k,(i,j) in enumerate(E): D[i,j]=D[j,i]=v[n+k]/math.sqrt(2)
        ratio=float(np.linalg.norm(D,2)/np.linalg.norm(D@X))
        report['numerical_checks'].append({'n':n,'domain_dimension':M.shape[1],'adjoint_nullity':3,'smallest_singular_value':float(s[-1]),'four_field_residual_bound':restricted,'analytic_epsilon':epsilon,'operator_ratio_of_singular_vector':ratio,'universal_operator_lower_bound':max(1,m**.25/math.sqrt(6*math.sqrt(10)))})
except ImportError as e:
    report['numerical_checks_unavailable']=str(e)
report['peak_resident_memory_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
report['address_space_limit_bytes']=1024**3
report['per_calculation_time_limit_seconds']=45
report['calculation_seconds']=time.monotonic()-start
(out/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
