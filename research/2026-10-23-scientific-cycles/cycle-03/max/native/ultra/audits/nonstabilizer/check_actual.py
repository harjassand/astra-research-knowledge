"""Bounded actual-state checks; single BLAS thread, no scalar relaxation."""
import os
for _k in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_k] = "1"
import json, math, platform, resource, time
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

OUT=Path(__file__).resolve().parent
START=time.perf_counter(); CPU=time.process_time(); RNG=np.random.default_rng(20261022)
m=math.log(2.0); C=2-m

def entropy(lam):
    p=np.asarray(lam); p=p[p>0]
    return float(-np.sum(p*np.log(p)))

def reduced(A, sites, n):
    """Ordinary partial trace by independent paired-axis traces."""
    out=A.reshape([2]*(2*n)); left=n
    for site in sorted(sites,reverse=True):
        out=np.trace(out,axis1=site,axis2=site+left);left-=1
    return out.reshape(2**left,2**left)

def scores(X,N):
    n=2*N; result=[]
    for a in range(2):
        row=[]
        for i in range(1,N+1):
            R=reduced(X,list(range(a*N,a*N+i)),n)
            row.append(float(np.vdot(R,R).real/(2**i)))
        result.append(row)
    return result

def actual(U,lam,N):
    c=np.sqrt(lam); X=(U*c)@U.conj().T; p=scores(X,N)
    return X,p,float(m*np.sum(p)-entropy(lam))

def stock(N,coherent=False):
    """Actual diagonal paired-complementary-stock mixture or coherent sum."""
    q=2**(2*N); vec=np.zeros(q)
    for index in range(q):
        bits=[(index>>(2*N-1-j))&1 for j in range(2*N)]
        for k in range(N+1):
            if not any(bits[k:N]) and not any(bits[N+N-k:2*N]):
                vec[index]+=2.0**(-N/2 if coherent else -N)
    if coherent: vec=vec**2
    return vec/np.sum(vec)

def complement_unitary(N):
    q=2**(2*N); U=np.zeros((q,q),complex)
    for x in range(q//2):
        y=q-1-x; theta=math.pi*(1+(x%7))/(17+(x%3));phi=math.pi*(1+(x%5))/11
        c=math.cos(theta);s=math.sin(theta);e=np.exp(1j*phi)
        U[x,x]=c;U[y,x]=e*s;U[x,y]=-np.conj(e)*s;U[y,y]=c
    return U

def kernel(U,sites,n):
    """Actual projector reductions: q eigenvectors, then their Gram matrix."""
    q=U.shape[0]; rest=[j for j in range(n) if j not in sites]
    V=U.reshape([2]*n+[q]).transpose(sites+rest+[n])
    V=V.reshape(2**len(sites),2**len(rest),q)
    R=np.einsum("saj,sbj->jab",V,V.conj(),optimize=True).reshape(q,-1)
    return (R@R.conj().T).real/(2**len(sites))

def classical_Q(sites,n):
    q=2**n; out=np.zeros((q,q))
    for x in range(q):
        for y in range(q):
            if all(((x>>(n-1-j))&1)==((y>>(n-1-j))&1) for j in range(n) if j not in sites):
                out[x,y]=1/(2**len(sites))
    return out

def apply_gate(U,G,sites,n):
    rest=[j for j in range(n) if j not in sites]; perm=sites+rest+[n]
    z=U.reshape([2]*n+[2**n]).transpose(perm)
    z=(G@z.reshape(2**len(sites),-1)).reshape([2]*n+[2**n])
    return z.transpose(np.argsort(perm)).reshape(U.shape)

def circuit(N,depth):
    n=2*N;q=2**n;U=np.eye(q,dtype=complex)
    H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
    sx=np.array([[0,1],[1,0]],complex);sz=np.diag([1,-1]);sy=np.array([[0,-1j],[1j,0]])
    for j in range(n):U=apply_gate(U,H,[j],n)
    order=[k for i in range(N) for k in (i,N+i)]
    for ell in range(depth):
        for j in range(n):
            theta=math.pi*(1+(j+ell)%3)/13
            axis=(sx+2*sz)/math.sqrt(5)
            U=apply_gate(U,math.cos(theta)*np.eye(2)-1j*math.sin(theta)*axis,[j],n)
        for j in range(n-1):
            angle=math.pi*(1+(ell+j)%4)/17
            pauli=np.kron(sx,sy if (j+ell)%2 else sz)
            G=math.cos(angle)*np.eye(4)-1j*math.sin(angle)*pauli
            U=apply_gate(U,G,order[j:j+2],n)
    return U

rows=[];max_identity_error=0.0
for N in range(1,5):
    U=complement_unitary(N);q=len(U);B=abs(U)**2
    lam_list=[("stock_mixture",stock(N)),("stock_coherent",stock(N,True)),
              ("full_rank",RNG.dirichlet(np.full(q,0.3)))]
    for name,lam in lam_list:
        X,p,F=actual(U,lam,N);diagonal=np.diag(B@np.sqrt(lam));cp=scores(diagonal,N)
        error=float(np.max(abs(np.array(p)-np.array(cp))));max_identity_error=max(max_identity_error,error)
        assert error<1e-12 and F<=2*C+1e-10
        rows.append(dict(family="global_complement_rotations",N=N,spectrum=name,entropy=entropy(lam),
                         score=p,defect=F,erasure_identity_error=error))

N=2;U=complement_unitary(N);B=abs(U)**2
K0=kernel(U,[0],4);K1=kernel(U,[2],4)
compressed=dict(K0_projection_defect=float(np.linalg.norm(K0@K0-K0)),
                K1_projection_defect=float(np.linalg.norm(K1@K1-K1)),
                commutator_norm=float(np.linalg.norm(K0@K1-K1@K0)),
                common_Gram_identity_error=float(np.linalg.norm(K0-B.T@classical_Q([0],4)@B)))
assert compressed["commutator_norm"]>1e-5
assert compressed["common_Gram_identity_error"]<1e-12

# Exact rational nonstabilizer example. Every U entry is rational, so the
# noncommutation statement below is exact and does not rely on floating error.
q=16;Bfrac=[[Fraction(0) for _ in range(q)] for _ in range(q)];Urat=np.zeros((q,q))
for x in range(q//2):
    y=q-1-x;t=Fraction(x+1,x+3);a=(1-t*t)/(1+t*t);b=2*t/(1+t*t)
    Urat[x,x]=float(a);Urat[y,x]=float(b);Urat[x,y]=-float(b);Urat[y,y]=float(a)
    Bfrac[x][x]=Bfrac[y][y]=a*a;Bfrac[y][x]=Bfrac[x][y]=b*b
def rational_kernel(site):
    flip=1<<(3-site)
    return [[sum((Bfrac[x][j]*(Bfrac[x][k]+Bfrac[x^flip][k])/2 for x in range(q)),Fraction(0))
             for k in range(q)] for j in range(q)]
R0=rational_kernel(0);R1=rational_kernel(2)
nonzero=[]
for j in range(q):
    for k in range(q):
        entry=sum((R0[j][x]*R1[x][k]-R1[j][x]*R0[x][k] for x in range(q)),Fraction(0))
        if entry:nonzero.append((j,k,entry))
assert nonzero
j,k,entry=nonzero[0];lam=np.arange(1,17,dtype=float)/136
Xrat,prat,Frat=actual(Urat,lam,2)
rat_example=dict(dimension=16,r=2,N=2,
    rotation="for pair x,15-x (0<=x<=7): t=(x+1)/(x+3), a=(1-t*t)/(1+t*t), b=2*t/(1+t*t), U_pair=[[a,-b],[b,a]]",
    spectrum="lambda_j=(j+1)/136, 0<=j<=15; exact distinct positive eigenvalues",
    first_commutator_nonzero_row=j,first_commutator_nonzero_column=k,
    exact_commutator_entry=str(entry),number_nonzero_commutator_entries=len(nonzero),
    actual_Gram_commutator_norm=float(np.linalg.norm(kernel(Urat,[0],4)@kernel(Urat,[2],4)-kernel(Urat,[2],4)@kernel(Urat,[0],4))),
    entropy=entropy(lam),score=prat,defect=Frat,
    nonstabilizer_reason="Every eigenvector has exactly two unequal nonzero computational amplitudes; a two-support qubit stabilizer vector must have equal moduli. Distinct eigenvalues preclude an alternative stabilizer eigenbasis.")
np.savez_compressed(OUT/"RATIONAL_NONCOMMUTING.npz",U=Urat,lam=lam,X=Xrat)

optimization=[]
for N in (2,3):
    for depth in (N,2*N):
        U=circuit(N,depth);q=len(U);A=np.zeros((q,q))
        for a in range(2):
            for i in range(1,N+1):A+=kernel(U,list(range(a*N,a*N+i)),2*N)
        for coherent in (False,True):
            lam=stock(N,coherent);lam=.999*lam+.001/q
            def objective(z):
                z=z-np.max(z);p=np.exp(z);p/=np.sum(p);c=np.sqrt(p);v=A@c
                f=m*np.dot(c,v)+np.dot(p,np.log(p))
                g=m*v/c+np.log(p)+1;grad=p*(g-np.dot(p,g))
                return -f,-grad
            result=minimize(objective,np.log(lam),jac=True,method="L-BFGS-B",options={"maxiter":80,"ftol":1e-11,"gtol":1e-7})
            z=result.x-np.max(result.x);p=np.exp(z);p/=p.sum()
            X,actual_p,F=actual(U,p,N)
            predicted=m*np.dot(np.sqrt(p),A@np.sqrt(p))-entropy(p)
            assert abs(F-predicted)<1e-10
            optimization.append(dict(family="nonClifford_intertask_circuit",N=N,depth=depth,
                start="stock_coherent" if coherent else "stock_mixture",defect=F,entropy=entropy(p),
                score=actual_p,iterations=int(result.nit),evaluations=int(result.nfev),success=bool(result.success),
                status=str(result.message),common_kernel_score_error=abs(F-predicted)))
            np.savez_compressed(OUT/f"witness_N{N}_depth{depth}_coh{int(coherent)}.npz",U=U,lam=p)

# Direct larger actual matrix check; no optimization/Gram construction at q=256.
N=4;U=circuit(N,N)
for coherent in (False,True):
    lam=stock(N,coherent);X,p,F=actual(U,lam,N)
    rows.append(dict(family="nonClifford_intertask_circuit",N=N,depth=N,
                     spectrum="stock_coherent" if coherent else "stock_mixture",
                     entropy=entropy(lam),score=p,defect=F))

raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss=int(raw if platform.system()=="Darwin" else raw*1024)
result=dict(scope="bounded actual quantum matrices; no physical counterexample found or theorem inferred from optimization",
            D=2,r=2,C_D=C,max_matrix_dimension=256,seed=20261022,exact_class=rows,
            compressed_noncommuting_example=compressed,variational_checks=optimization,
            rational_noncommuting_example=rat_example,
            max_erasure_identity_error=max_identity_error,
            body_wall_seconds=time.perf_counter()-START,body_CPU_seconds=time.process_time()-CPU,
            process_peak_RSS_bytes=rss,numpy=np.__version__,python=platform.python_version(),
            BLAS_threads="1 set before NumPy import",optimization_global_optimality="NOT_ESTABLISHED")
assert result["body_CPU_seconds"]<45
(OUT/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ("body_wall_seconds","body_CPU_seconds","process_peak_RSS_bytes","compressed_noncommuting_example")},indent=2))
print("max tested circuit defect",max(x["defect"] for x in optimization))
