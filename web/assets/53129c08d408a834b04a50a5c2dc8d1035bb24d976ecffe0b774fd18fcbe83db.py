"""Fixed distinct legal non-KMS controls; one exclusive-create output only."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE=Path(__file__).resolve().parent


def positive_f(a,fn):
    val,U=np.linalg.eigh((a+a.conj().T)/2)
    assert val.min()>0
    return (U*fn(val))@U.conj().T


def fwd_kernel(x,y):
    z,w=(x+y)/2,(x-y)/2
    aa,bb=np.full_like(w,.5),np.full_like(w,.5)
    mask=np.abs(w)>1e-10
    aa[mask]=w[mask]*np.cosh(2*w[mask])/np.sinh(2*w[mask])
    bb[mask]=w[mask]/np.sinh(2*w[mask])
    return 2*(np.exp(-z)*(-z-aa)+np.exp(z)*bb)


def root_kernel(x,y):
    return np.cosh((x+y)/2)/np.cosh((x-y)/2)-1


def choi(fn,n):
    out=np.zeros((n*n,n*n),complex)
    for i in range(n):
        for j in range(n):
            e=np.zeros((n,n),complex)
            e[i,j]=1
            out+=np.kron(fn(e),e)
    return out


def integral_half_line(fn,nodes=256):
    points,weights=np.polynomial.legendre.leggauss(nodes)
    q=(points+1)/2
    ts=q/(1-q)
    vals=np.asarray([fn(float(t)) for t in ts])/(1-q)**2
    return float(np.dot(weights/2,vals))


def check_case(name,sig,B,rho,tau):
    sig=np.asarray(sig,float)
    sv=np.sqrt(sig)
    s,df,di=np.diag(sv),np.diag(np.sqrt(sv)),np.diag(1/np.sqrt(sv))
    P,Q=B.conj().T@s@B,B@s@B.conj().T
    n,nr=len(sig),len(tau)
    A=np.zeros((n,n),complex)
    for i in range(n):
        for j in range(n):
            if abs(sv[i]-sv[j])<1e-13:
                assert abs(P[i,j]-Q[i,j])<1e-12
                A[i,j]=(P[i,j]+Q[i,j])/(sv[i]+sv[j])
            else:
                A[i,j]=2*(sv[i]*P[i,j]-sv[j]*Q[i,j])/(sv[i]**2-sv[j]**2)
    Bf,Af=np.kron(np.eye(nr),B),np.kron(np.eye(nr),A)
    K,C=df@B@di,df@A@di
    Kf,Cf=np.kron(np.eye(nr),K),np.kron(np.eye(nr),C)
    def H(x):
        return (Af.conj().T@x+x@Af)/2-Bf.conj().T@x@Bf
    def Hlocal(x):
        return (A.conj().T@x+x@A)/2-B.conj().T@x@B
    def LP(x):
        return (Cf@x+x@Cf.conj().T)/2-Kf@x@Kf.conj().T
    omega=np.kron(tau,np.diag(sig))
    omega_d=positive_f(omega,lambda v:v**.25)
    omega_di=positive_f(omega,lambda v:v**(-.25))
    log_rho=positive_f(rho,np.log)
    log_omega=positive_f(omega,np.log)
    sqrho=positive_f(rho,np.sqrt)
    J=np.trace(LP(rho)@(log_rho-log_omega)).real
    E=np.trace(sqrho@H(sqrho)).real
    Jadj=np.trace(omega_d@H(omega_di@rho@omega_di)@omega_d@(log_rho-log_omega)).real
    operator_lindblad_error=np.linalg.norm((C+C.conj().T)/2-K.conj().T@K)
    stationary_error=np.linalg.norm((C@np.diag(sig)+np.diag(sig)@C.conj().T)/2-K@np.diag(sig)@K.conj().T)
    h_stationary_error=np.linalg.norm((A.conj().T@s+s@A)/2-P)
    hadj_stationary_error=np.linalg.norm((A@s+s@A.conj().T)/2-Q)
    assert max(operator_lindblad_error,stationary_error,h_stationary_error,hadj_stationary_error)<1e-11
    freq={}
    for i in range(n):
        for j in range(n):
            if B[i,j]!=0:
                alpha=round(float(math.log(sv[i]/sv[j])),13)
                freq.setdefault(alpha,np.zeros_like(B))[i,j]+=B[i,j]
    alphas=np.asarray(sorted(freq))
    val,U=np.linalg.eigh(rho)
    roots=np.sqrt(val)
    comp=np.array([U.conj().T@np.kron(np.eye(nr),freq[a])@U for a in alphas])
    Jgram,Egram,diag_J=0j,0j,0j
    minimum_kernel_eigenvalue=0.0
    imaginary_cross_mass=0.0
    for i in range(len(val)):
        for j in range(len(val)):
            nodes=math.log(roots[i]/roots[j])-alphas
            xx,yy=nodes[:,None],nodes[None,:]
            kj,ke=fwd_kernel(xx,yy),root_kernel(xx,yy)
            c=comp[:,i,j]
            weight=roots[i]*roots[j]
            term=weight*np.vdot(c,kj@c)
            Jgram+=term
            Egram+=weight*np.vdot(c,ke@c)
            if i==j:
                diag_J+=term
            minimum_kernel_eigenvalue=min(minimum_kernel_eigenvalue,
                float(np.linalg.eigvalsh(kj-(math.pi/2)*ke).min()))
            imaginary_cross_mass+=float(np.abs(np.outer(c.conj(),c).imag).sum())
    Jerr,Eerr=abs(Jgram-J),abs(Egram-E)
    assert max(Jerr,Eerr)<1e-9*(1+abs(J)+abs(E)),(name,Jerr,Eerr)
    assert J-(math.pi/2)*E>=-1e-10
    assert (J+Jadj)/2-math.pi*E>=-1e-10
    hs=np.stack([Hlocal(np.eye(n*n)[k].reshape(n,n)).reshape(-1) for k in range(n*n)],axis=1)
    hs_sym=(hs+hs.conj().T)/2
    nonkms_norm=float(np.linalg.norm(hs-hs.conj().T))
    assert np.linalg.eigvalsh(hs_sym).min()>-1e-11
    et=np.eye(n*n,dtype=complex)
    term=et.copy()
    for order in range(1,81):
        term=(-.17*hs)@term/order
        et+=term
    assert np.linalg.norm(term)<1e-14
    def heis_t(x):
        return di@(et@(df@x@df).reshape(-1)).reshape(n,n)@di
    cp_min=float(np.linalg.eigvalsh(choi(heis_t,n)).min())
    unital_error=float(np.linalg.norm(heis_t(np.eye(n))-np.eye(n)))
    assert cp_min>=-1e-10 and unital_error<1e-10
    reference_log_conservation=0.0
    if nr>1:
        reference_log_conservation=float(abs(np.trace(LP(rho)@np.kron(positive_f(tau,np.log),np.eye(n)))))
        assert reference_log_conservation<1e-11
    return {"case":name,"local_dimension":n,"reference_dimension":nr,
        "J_forward":float(J),"J_KMS_adjoint":float(Jadj),"E_sym":float(E),
        "forward_pi_over_two_gap":float(J-(math.pi/2)*E),
        "symmetrized_KMS_pi_gap":float((J+Jadj)/2-math.pi*E),
        "J_identity_error":float(Jerr),"E_identity_error":float(Eerr),
        "J_gram_imaginary":float(Jgram.imag),"diagonal_J_gram_real":float(diag_J.real),
        "minimum_difference_kernel_eigenvalue":minimum_kernel_eigenvalue,
        "imaginary_cross_product_mass":imaginary_cross_mass,
        "physical_lindblad_error":float(operator_lindblad_error),
        "physical_stationarity_error":float(stationary_error),
        "H_stationarity_error":float(h_stationary_error),"H_adjoint_stationarity_error":float(hadj_stationary_error),
        "nonKMS_H_antisymmetry_norm":nonkms_norm,
        "physical_hamiltonian_norm":float(np.linalg.norm((C-C.conj().T)/(2j))),
        "finite_time_0_17_choi_min_eigenvalue":cp_min,"finite_time_unital_error":unital_error,
        "fixed_exponential_taylor_order":80,"exponential_last_term_norm":float(np.linalg.norm(term)),
        "reference_log_conservation_error":reference_log_conservation,
        "rho_min_eigenvalue":float(val.min())}


B=np.array([[.3j,1,1j],[1j,-.2,1+.5j],[1,-1+.5j,.4j]],complex)
sig=np.array([1,4,9])/14
X=np.array([[1,.2j,.4],[.3,1.2,-.5j],[.1j,.2,.8]],complex)
rho3=X@X.conj().T+.15*np.eye(3)
rho3/=np.trace(rho3).real
psi=np.array([1,0,.4,0,1j,.3],complex)
psi/=np.linalg.norm(psi)
rho6=.63*np.outer(psi,psi.conj())+.37*np.diag(np.arange(1,7)/21)
tau=np.array([[.6,.2j],[-.2j,.4]],complex)
cycle=np.array([[0,1,0],[0,0,1],[1,0,0]],complex)
inputs=[("distinct_nonHermitian_stationary_qutrit",sig,B,rho3,np.ones((1,1))),
        ("entangled_reference_distinct_nonHermitian_qutrit",sig,B,rho6,tau),
        ("stationary_quantum_reference",sig,B,np.kron(tau,np.diag(sig)),tau),
        ("tracial_directed_unitary_cycle",np.ones(3)/3,cycle,rho3,np.ones((1,1)))]
rows=[check_case(*a) for a in inputs]
assert rows[0]["nonKMS_H_antisymmetry_norm"]>1
assert abs(rows[0]["J_forward"]-rows[0]["J_KMS_adjoint"])>1e-3
rr=np.array([.25,.6,1,2,5.])
xx=np.log(rr)
Jmat,E_mat=fwd_kernel(xx[:,None],xx[None,:]),root_kernel(xx[:,None],xx[None,:])
Imat=np.empty((len(rr),len(rr)))
quaderr=0.0
for i,r in enumerate(rr):
    for j,u in enumerate(rr):
        fn=lambda a:a/((1+a)*(r*r+a)*(u*u+a))
        val=integral_half_line(fn,256)
        err=abs(val-integral_half_line(fn,128))
        Imat[i,j]=val
        quaderr=max(quaderr,float(err))
factor=(rr**2-1)/np.sqrt(rr)
loewner_error=float(np.linalg.norm(Jmat-np.outer(factor,factor)*Imat))
kernel_min=float(np.linalg.eigvalsh(Jmat-(math.pi/2)*E_mat).min())
assert loewner_error<1e-10 and kernel_min>=-1e-11
v=np.array([1,.2j,-.3,.5-.1j,-.2],complex)
br=rr**1.5/(1+rr)
def fn(t):
    f=np.sum(v/(rr**2+t*t))
    return t**3/(1+t*t)*abs(f)**2
half_norm=integral_half_line(fn,256)
err=abs(half_norm-integral_half_line(fn,128))
Gnorm=2*half_norm
Pnorm=float((math.pi/2)*np.vdot(v,((np.outer(br,br)/(np.outer(rr,rr)*(rr[:,None]+rr[None,:])))@v)).real)
assert Gnorm>=Pnorm-1e-12
scalar={"nodes_r":rr.tolist(),"fixed_node_count":len(rr),"loewner_integral_congruence_error":loewner_error,
        "quadrature_resolution_change_max":quaderr,"minimum_pi_over_two_difference_eigenvalue":kernel_min,
        "fixed_complex_coefficient_G_norm_squared":float(Gnorm),"exact_projected_norm_squared":Pnorm,
        "hardy_projection_gap":float(Gnorm-Pnorm),"hardy_quadrature_resolution_change":float(err),
        "quadrature_note":"Fixed Gauss-Legendre 128/256 resolution comparison; not a rigorous error bound"}
out={"status":"PASS_FIXED_FINITE_DIAGNOSTICS_ONLY","no_optimization":True,"case_count":len(rows),
     "independent_kernel_baseline_sha256":hashlib.sha256((HERE/"INDEPENDENT_FORWARD_KERNEL_BASELINE.txt").read_bytes()).hexdigest(),
     "hardy_proof_sha256":hashlib.sha256((HERE/"FORWARD_PI_OVER_TWO_HARDY_PROOF.txt").read_bytes()).hexdigest(),
     "cases":rows,"scalar_integral_and_complex_hardy_control":scalar,
     "limitations":["Finite controls are not a universal proof","No optimality conclusion","No external/formal or historical-priority certification"]}
with (HERE/"FORWARD_ENTROPY_CONTROLS.json").open("x") as f:
    json.dump(out,f,indent=2)
    f.write("\n")
print(json.dumps({"status":out["status"],"cases":len(rows),
    "maximum_J_identity_error":max(x["J_identity_error"] for x in rows),
    "maximum_E_identity_error":max(x["E_identity_error"] for x in rows),
    "distinct_nonKMS_H_antisymmetry_norm":rows[0]["nonKMS_H_antisymmetry_norm"],
    "loewner_integral_error":loewner_error,"hardy_projection_gap":scalar["hardy_projection_gap"]}))
