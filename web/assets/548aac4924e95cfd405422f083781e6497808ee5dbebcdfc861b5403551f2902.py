"""Fixed supplied-lead finite-p controls, separate from frozen entropy checks."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE=Path(__file__).resolve().parent
helper_source=(HERE/"CHECK_FORWARD_ENTROPY_CONTROLS.py").read_bytes()
assert hashlib.sha256(helper_source).hexdigest()=="53129c08d408a834b04a50a5c2dc8d1035bb24d976ecffe0b774fd18fcbe83db"
helper_prefix=helper_source.decode().split('\nB=np.array([[.3j,1,1j]',1)
assert len(helper_prefix)==2
helper={"__file__":str(HERE/"CHECK_FORWARD_ENTROPY_CONTROLS.py"),"__name__":"definition_only_read_only_reuse"}
exec(compile(helper_prefix[0],str(HERE/"CHECK_FORWARD_ENTROPY_CONTROLS.py"),"exec"),helper)
positive_f=helper["positive_f"]
root_kernel=helper["root_kernel"]
PS=(1.25,1.5,2.0,3.0,5.0)


def p_kernel(x,y,r):
    z,w=(x+y)/2,(x-y)/2
    a,b=np.full_like(w,1-r),np.full_like(w,r)
    mask=np.abs(w)>1e-10
    a[mask]=np.sinh(2*(1-r)*w[mask])/np.sinh(2*w[mask])
    b[mask]=np.sinh(2*r*w[mask])/np.sinh(2*w[mask])
    return np.exp(-z)*a+np.exp(z)*b-np.exp((2*r-1)*z)


def check_case(name,sig,B,rho,tau):
    sv=np.sqrt(sig)
    s=np.diag(sv)
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
    omega=np.kron(tau,np.diag(sig))
    st=positive_f(omega,np.sqrt)
    dt=positive_f(omega,lambda v:v**.25)
    dit=positive_f(omega,lambda v:v**(-.25))
    def H(x):
        return (Af.conj().T@x+x@Af)/2-Bf.conj().T@x@Bf
    def HA(x):
        return (Af@x+x@Af.conj().T)/2-Bf@x@Bf.conj().T
    def L(x):
        return dit@H(dt@x@dt)@dit
    sqrho=positive_f(rho,np.sqrt)
    Eroot=np.trace(sqrho@H(sqrho)).real
    val,U=np.linalg.eigh(rho)
    roots=np.sqrt(val)
    freqs={}
    for i in range(n):
        for j in range(n):
            if B[i,j]!=0:
                alpha=round(float(math.log(sv[i]/sv[j])),13)
                freqs.setdefault(alpha,np.zeros_like(B))[i,j]+=B[i,j]
    alphas=np.asarray(sorted(freqs))
    components=np.array([U.conj().T@np.kron(np.eye(nr),freqs[a])@U for a in alphas])
    rows=[]
    for p in PS:
        r,a=1/p,.5-1/p
        eta=math.sin(math.pi*r)/(1+abs(math.cos(math.pi*r)))
        cp=eta/(2*(1-r))
        sr=positive_f(omega,lambda v:v**(r/2))
        sinvr=positive_f(omega,lambda v:v**(-r/2))
        f=sinvr@positive_f(rho,lambda v:v**r)@sinvr
        bare=sr@f@sr
        outq=positive_f(omega,lambda v:v**(-(1-r)/2))
        iq=outq@positive_f(bare,lambda v:v**(p-1))@outq
        i2=dit@positive_f(bare,lambda v:v**(p/2))@dit
        Ep=p/(2*(p-1))*np.trace(st@iq@st@L(f)).real
        E_direct=np.trace(st@i2@st@L(i2)).real
        sa=positive_f(omega,lambda v:v**(a/2))
        sma=positive_f(omega,lambda v:v**(-a/2))
        h=sa@positive_f(rho,lambda v:v**r)@sa
        g=sma@positive_f(rho,lambda v:v**(1-r))@sma
        Tr=np.trace(g@H(h)).real
        gram=0j
        minimum_difference=0.0
        for i in range(len(val)):
            for j in range(len(val)):
                nodes=math.log(roots[i]/roots[j])-alphas
                xx,yy=nodes[:,None],nodes[None,:]
                kp,ke=p_kernel(xx,yy,r),root_kernel(xx,yy)
                minimum_difference=min(minimum_difference,float(np.linalg.eigvalsh(kp-eta*ke).min()))
                c=components[:,i,j]
                gram+=roots[i]*roots[j]*np.vdot(c,kp@c)
        norm_error=abs(Ep-Tr/(2*(1-r)))
        identity_error=abs(gram-Tr)
        transport_error=max(np.linalg.norm(dt@f@dt-h),np.linalg.norm(dt@iq@dt-g),np.linalg.norm(dt@i2@dt-sqrho))
        root_error=abs(E_direct-Eroot)
        dual_appropriate=np.trace(h@HA(g)).real/(2*r)
        adjoint_duality_error=abs(dual_appropriate-(p-1)*Ep)
        assert max(norm_error,identity_error,transport_error,root_error,adjoint_duality_error)<1e-9*(1+abs(Tr)+abs(Eroot))
        gap=Ep-cp*Eroot
        assert gap>=-1e-9 and minimum_difference>=-1e-8
        if p==2:
            assert abs(Ep-Eroot)<1e-10
        rows.append({"p":p,"c_nr":cp,"kernel_eta":eta,"E_p":float(Ep),"E_root":float(Eroot),
            "profile_gap":float(gap),"normalization_error":float(norm_error),
            "weighted_transport_error":float(transport_error),"root_energy_error":float(root_error),
            "full_complex_gram_error":float(identity_error),"full_gram_imaginary":float(gram.imag),
            "minimum_difference_kernel_eigenvalue":minimum_difference,
            "conjugate_duality_with_KMS_adjoint_error":float(adjoint_duality_error)})
    incorrect_same_L_duality={}
    for p,q in ((1.25,5.0),(1.5,3.0)):
        ep=next(v["E_p"] for v in rows if v["p"]==p)
        eq=next(v["E_p"] for v in rows if v["p"]==q)
        incorrect_same_L_duality[str(p)]=float(eq-(p-1)*ep)
    return {"case":name,"local_dimension":n,"reference_dimension":nr,"p_checks":rows,
            "incorrect_fixed_L_conjugate_difference":incorrect_same_L_duality}


quadrature_grids={}
def integral_log_line(fn,count):
    if count not in quadrature_grids:
        x,w=np.polynomial.legendre.leggauss(count)
        quadrature_grids[count]=(30*x,30*w)
    x,w=quadrature_grids[count]
    t=np.exp(x)
    return float(np.dot(w,np.asarray([fn(float(a)) for a in t])*t))


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
        ("entangled_full_reference",sig,B,rho6,tau),
        ("stationary_reference",sig,B,np.kron(tau,np.diag(sig)),tau),
        ("tracial_directed_cycle",np.ones(3)/3,cycle,rho3,np.ones((1,1)))]
rows=[check_case(*x) for x in inputs]
assert abs(rows[0]["incorrect_fixed_L_conjugate_difference"]["1.5"])>1e-4
RR=np.array([.25,.6,1,2,5.])
XX=np.log(RR)
v=np.array([1,.2j,-.3,.5-.1j,-.2],complex)
scalar=[]
for p in PS:
    r=1/p
    eta=math.sin(math.pi*r)/(1+abs(math.cos(math.pi*r)))
    K,E=p_kernel(XX[:,None],XX[None,:],r),root_kernel(XX[:,None],XX[None,:])
    I=np.empty_like(K)
    resolution_change=0.0
    tail_bound=0.0
    for i,R in enumerate(RR):
        for j,S in enumerate(RR):
            fn=lambda a:a**(1-r)/((1+a)*(R*R+a)*(S*S+a))
            I[i,j]=integral_log_line(fn,512)
            resolution_change=max(resolution_change,abs(I[i,j]-integral_log_line(fn,256)))
            tail_bound=max(tail_bound,math.exp(-30*(2-r))/((2-r)*R*R*S*S)+math.exp(-30*(1+r))/(1+r))
    factor=RR**(r-.5)*(RR**2-1)
    integral_error=float(np.linalg.norm(K-(math.sin(math.pi*r)/math.pi)*np.outer(factor,factor)*I))
    assert integral_error<1e-9
    br=RR**(1.5-r)/(1+RR)
    def norm_integrand(t):
        U=np.sum(v/(RR**2+t*t))
        return t**(3-2*r)/(1+t*t)*abs(U)**2
    Gnorm=2*integral_log_line(norm_integrand,512)
    Pnorm=float((math.pi/2)*np.vdot(v,((np.outer(br,br)/(np.outer(RR,RR)*(RR[:,None]+RR[None,:])))@v)).real)
    fraction_gap=Gnorm-2*Pnorm/(1+abs(math.cos(math.pi*r)))
    assert fraction_gap>=-1e-9
    if p==2:
        assert abs(fraction_gap)<1e-9
    scalar.append({"p":p,"integral_kernel_congruence_error":integral_error,
        "fixed_256_512_resolution_change_max":float(resolution_change),"integral_truncation_tail_bound_max":float(tail_bound),
        "minimum_difference_kernel_eigenvalue":float(np.linalg.eigvalsh(K-eta*E).min()),
        "G_boundary_norm_squared":float(Gnorm),"exact_minus_projection_norm_squared":Pnorm,
        "improved_projection_fraction_gap":float(fraction_gap),
        "quadrature_scope":"Fixed logarithmic [-30,30] quadrature; tail bound exact, resolution change is not a rigorous quadrature error bound"})
out={"status":"PASS_FIXED_FINITE_P_DIAGNOSTICS_ONLY","no_optimization":True,"case_p_count":len(rows)*len(PS),
     "p_values":list(PS),"cases":rows,"fixed_scalar_hardy_controls":scalar,
     "proof_sha256":hashlib.sha256((HERE/"EXPOSED_FINITE_P_IMPROVED_PROFILE_PROOF.txt").read_bytes()).hexdigest(),
     "helper_reused_read_only_sha256":hashlib.sha256(helper_source).hexdigest(),
     "limitations":["Finite checks are not a universal proof","No sharpness assertion","No nonpositive all-p extension","No external/formal or historical-priority certification"]}
with (HERE/"NONKMS_FINITE_P_CONTROLS.json").open("x") as f:
    json.dump(out,f,indent=2)
    f.write("\n")
print(json.dumps({"status":out["status"],"case_p_count":out["case_p_count"],
    "maximum_p_gram_error":max(v["full_complex_gram_error"] for a in rows for v in a["p_checks"]),
    "maximum_sigma_transport_error":max(v["weighted_transport_error"] for a in rows for v in a["p_checks"]),
    "maximum_fractional_integral_error":max(v["integral_kernel_congruence_error"] for v in scalar),
    "incorrect_fixed_L_duality_control":rows[0]["incorrect_fixed_L_conjugate_difference"]}))
