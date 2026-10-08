"""Internal diagnostics for the factorial-spin universal probe construction.
No finite diagnostic certifies the all-size proof. Python >=3.10; numpy/scipy/sympy.
"""
import json, math, platform
from fractions import Fraction
from pathlib import Path
import numpy as np
import scipy
from scipy.special import gammaln, logsumexp
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parent
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
I=np.eye(2,dtype=complex)
v=np.array([0,1,-1,0],complex)/np.sqrt(2)
S=np.outer(v,v.conj())

def channel(ks,x):
    return sum(k@x@k.conj().T for k in ks)

def invroot(x):
    ev,U=np.linalg.eigh((x+x.conj().T)/2)
    if min(ev)<=0: raise ValueError('Inverse root requires positive definite input')
    return (U/np.sqrt(ev))@U.conj().T

def sinkhorn(ks,tol=1e-12,maxiter=4000):
    A=I.copy(); B=I.copy(); ls=np.array(ks).copy()
    for it in range(maxiter):
        a=invroot(channel(ls,I)); ls=np.array([a@k for k in ls]); A=a@A
        b=invroot(sum(k.conj().T@k for k in ls)); ls=np.array([k@b for k in ls]); B=B@b
        err=max(np.linalg.norm(channel(ls,I)-I),np.linalg.norm(sum(k.conj().T@k for k in ls)-I))
        if err<tol: return A,B,ls,err,it+1
    raise RuntimeError(f'Sinkhorn failed: {err}')

def pt(rho,N,site=0):
    axes=list(range(2*N)); axes[site],axes[N+site]=axes[N+site],axes[site]
    return rho.reshape([2]*(2*N)).transpose(axes).reshape(rho.shape)

def apply_sites(rho,ks,N):
    """Tensor superoperator, avoiding enumeration of all Kraus strings."""
    E=np.einsum('kai,kbj->abij',np.array(ks),np.array(ks).conj())
    z=rho.reshape([2]*(2*N))
    for site in range(N):
        ax=[site,N+site]+[k for k in range(2*N) if k not in (site,N+site)]
        z=np.tensordot(E,z.transpose(ax),axes=([2,3],[0,1])).transpose(np.argsort(ax))
    return z.reshape(rho.shape)

def spin_ops(N):
    ops=[]
    for p in P:
        A=np.zeros((2**N,2**N),complex)
        for i in range(N):
            term=np.array([[1]],complex)
            for k in range(N):term=np.kron(term,p/2 if k==i else I)
            A+=term
        ops.append(A)
    return ops

def sector_exact(N):
    if N<2 or N%2: raise ValueError('N must be positive even >=2')
    f=Fraction(1); ws=[]
    for j in range(N//2+1):
        k=N//2-j
        mult=math.comb(N,k)-(math.comb(N,k-1) if k>0 else 0)
        ws.append(Fraction((2*j+1)*mult)*f)
        f/=2*j+3
    Z=sum(ws); ps=[w/Z for w in ws]
    m=sum(Fraction(j*(j+1))*p for j,p in enumerate(ps))
    return ps,m

def dense_probe(N):
    Js=spin_ops(N); J2=sum(J@J for J in Js)
    vals,U=np.linalg.eigh(J2)
    js=np.rint((np.sqrt(np.maximum(0,1+4*vals))-1)/2).astype(int)
    f=[1.0]
    for j in range(N//2): f.append(f[-1]/(2*j+3))
    w=np.array([f[j] for j in js]); rho=(U*(w/w.sum()))@U.conj().T
    return rho,Js,J2

def bloch(ks):
    c=np.array([np.trace(p@channel(ks,I)).real/2 for p in P])
    T=np.array([[np.trace(p@channel(ks,q)).real/2 for q in P] for p in P])
    return c,T

def depol(lam):
    return [np.sqrt((1+3*lam)/4)*I]+[np.sqrt((1-lam)/4)*p for p in P]

def gad(eta,w):
    return [np.sqrt(w)*np.diag([1,np.sqrt(eta)]),
            np.sqrt(w)*np.array([[0,np.sqrt(1-eta)],[0,0]]),
            np.sqrt(1-w)*np.diag([np.sqrt(eta),1]),
            np.sqrt(1-w)*np.array([[0,0],[np.sqrt(1-eta),0]])]

def main():
    rng=np.random.default_rng(8102027)
    out={'status':'internal numerical and exact diagnostics, not external verification',
         'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'seed':8102027}
    F=math.exp(.5)*math.sqrt(math.pi/2)*math.erf(1/math.sqrt(2))
    C=(23*F+15)/(6*F+4)
    out['limiting_moment']=C
    dense=[]; dep=[]; rnd=[]; exact=[]; LP=[]
    for N in [2,4,6,8]:
        rho,Js,J2=dense_probe(N)
        ps,m=sector_exact(N)
        ept=[float(np.linalg.eigvalsh(pt(rho,N,i)).min()) for i in range(N)]
        dense.append({'N':N,'moment':float(np.trace(rho@J2).real),'exact_moment':str(m),
                      'moment_error':abs(float(np.trace(rho@J2).real)-float(m)),
                      'min_eigenvalue':float(np.linalg.eigvalsh(rho).min()),'min_singleton_PT':min(ept)})
        for lam in [0.,.5,1/math.sqrt(3),.58,.7,.9,1.]:
            ks=depol(lam); z=apply_sites(rho,ks,N); s=3*lam**2
            got=sum(np.trace(z@J@J).real-np.trace(z@J).real**2 for J in Js)
            want=N*(3-s)/4+s*float(m)/3
            dep.append({'N':N,'lambda':lam,'got':float(got),'formula':want,'error':abs(float(got)-want)})
        for zidx in range(4):
            Z=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2)); ks=np.linalg.qr(Z)[0].reshape(4,2,2)
            A,B,ls,err,it=sinkhorn(ks)
            c,T=bloch(ls); s=float(np.sum(T*T))
            pair=channel([np.kron(a,b) for a in ks for b in ks],S)
            pair2=channel([np.kron(a,b) for a in ls for b in ls],S)
            congr=abs(np.linalg.det(B))**2*np.kron(A,A)@pair@np.kron(A,A).conj().T
            y=apply_sites(rho,[A@k for k in ks],N); norm=float(np.trace(y).real); y/=norm
            got=float(np.trace(y@J2).real)
            H=sum((A@k).conj().T@(A@k) for k in ks)
            hev=np.linalg.eigvalsh(H)
            p=float(np.prod(hev))
            weights=[]
            for j,pj in enumerate(ps):
                M=2*j
                hbar=sum(float(hev[0])**k*float(hev[1])**(M-k) for k in range(M+1))/(M+1)
                weights.append(float(pj)*p**(N/2-j)*hbar)
            pnorm=sum(weights); wt=np.array(weights)/pnorm
            mj=sum(j*(j+1)*w for j,w in enumerate(wt))
            upper=N*(3-s)/4+mj
            rnd.append({'N':N,'s_normal':s,'normalform_error':err,'pair_congruence_error':float(np.linalg.norm(pair2-congr)),
                        'normalizer_error':abs(pnorm-norm),'filtered_J2':got,'moment_upper_bound':upper,
                        'bound_slack':upper-got,'pair_pt_min':float(np.linalg.eigvalsh(pt(pair,2)).min())})
    for N in range(2,102,2):
        ps,m=sector_exact(N)
        assert float(m)<C
        assert (N==2 and m==N/2) or (N>=4 and m<Fraction(N,2))
        exact.append({'N':N,'moment':float(m),'moment_fraction':str(m)})
        # Independent linear optimization in spin probabilities, with PPT cone inequalities.
        dims=np.array([(2*j+1)*(math.comb(N,N//2-j)-(math.comb(N,N//2-j-1) if j<N//2 else 0)) for j in range(N//2+1)],float)
        Arows=[]
        for j in range(N//2):
            # p_j / dim_j <= (2j+3) p_{j+1}/dim_{j+1}; scale row.
            row=np.zeros(N//2+1); row[j]=1; row[j+1]=-(2*j+3)*dims[j]/dims[j+1]
            Arows.append(row)
        ans=linprog([j*(j+1) for j in range(N//2+1)],A_ub=Arows,b_ub=np.zeros(N//2),A_eq=np.ones((1,N//2+1)),b_eq=[1],bounds=(0,None),method='highs')
        assert ans.success
        LP.append({'N':N,'optimum':float(ans.fun),'exact':float(m),'error':abs(float(ans.fun)-float(m))})
    # Exact rational four-qubit certificate; no numerical eigensolver used here.
    import sympy as sp
    Ps=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    Js=[]
    for P0 in Ps:
        A=sp.zeros(16)
        for i in range(4):
            fac=[P0/2 if k==i else sp.eye(2) for k in range(4)]
            A+=sp.kronecker_product(*fac)
        Js.append(A)
    C4=sum((J*J for J in Js),sp.zeros(16)); Id=sp.eye(16)
    P0=(C4-2*Id)*(C4-6*Id)/12
    P1=-C4*(C4-6*Id)/8
    P2=C4*(C4-2*Id)/24
    R=sp.Rational(3,16)*(P0+P1/3+P2/15)
    RT=sp.zeros(16)
    for a in range(16):
        for b in range(16):
            aa=(b//8)*8+a%8; bb=(a//8)*8+b%8
            RT[a,b]=R[aa,bb]
    out['exact_N4']={'trace':str(sp.trace(R)),'J2':str(sp.trace(R*C4)),
                     'rho_eigenvalues':{str(k):int(v) for k,v in R.eigenvals().items()},
                     'singleton_PT_eigenvalues':{str(k):int(v) for k,v in RT.eigenvals().items()}}
    out.update(dense=dense,depolarizing=dep,random_filters=rnd,exact_moments=exact,linear_programs=LP)
    out['counts']={'dense_probes':len(dense),'singleton_partial_transposes':sum(r['N'] for r in dense),
                   'depolarizing_formulas':len(dep),'filtered_random_channel_tests':len(rnd),
                   'rational_moments':len(exact),'linear_programs':len(LP)}
    out['max_errors']={'dense_moment':max(r['moment_error'] for r in dense),
                       'depolarizing_formula':max(r['error'] for r in dep),
                       'normalization':max(r['normalizer_error'] for r in rnd),
                       'pair_congruence':max(r['pair_congruence_error'] for r in rnd),
                       'LP_objective':max(r['error'] for r in LP)}
    (ROOT/'universal_probe_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:out[k] for k in ['counts','max_errors','exact_N4','limiting_moment']},indent=2))

if __name__=='__main__': main()
