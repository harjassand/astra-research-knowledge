"""Small fixed exposed-audit diagnostics; never imported by a frozen writer."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE=Path(__file__).resolve().parent
EXPOSED=HERE.parent.parent/"complexity_proof_recon"/"cycle09_lp_falsification"
PS=(1.25,1.5,2.0,3.0,5.0)


def positive_power(a,p):
    val,U=np.linalg.eigh((a+a.conj().T)/2)
    assert val.min()>0
    return (U*val**p)@U.conj().T


def signed_power(a,p):
    val,U=np.linalg.eigh((a+a.conj().T)/2)
    val[np.abs(val)<1e-13*max(1,float(np.max(np.abs(val))))]=0
    return (U*(np.sign(val)*np.abs(val)**p))@U.conj().T


def polar_power(a,p):
    U,val,Vh=np.linalg.svd(a)
    val[val<1e-13*max(1,float(val.max()))]=0
    return (U*val**p)@Vh


def signed_kernel(x,y,t,sign):
    return np.cosh((x+y)/2)*np.cosh(t*(x-y)/2)/np.cosh((x-y)/2)-sign*np.cosh(t*(x+y)/2)


B=np.array([[.3,1,1j],[1,-.2,1+.5j],[-1j,1-.5j,.4]],complex)
sig=np.array([1,4,9])/14
sv=np.sqrt(sig)
s=np.diag(sv)
V=2*(B@s@B)/(sv[:,None]+sv[None,:])
tau=np.array([[.6,.2j],[-.2j,.4]],complex)
X=np.array([[1,.2j,.4],[.3,1.2,-.5j],[.1j,.2,.8]],complex)
_,U3=np.linalg.eigh(X@X.conj().T+.15*np.eye(3))
Q3=(U3*np.array([-.7,.3,.9]))@U3.conj().T
psi=np.array([1,0,.4,0,1j,.3],complex)
psi/=np.linalg.norm(psi)
rho6=.63*np.outer(psi,psi.conj())+.37*np.diag(np.arange(1,7)/21)
_,U6=np.linalg.eigh(rho6)
Q6=(U6*np.array([-1,-.4,-.1,.2,.6,1.1]))@U6.conj().T
Qs=(U3*np.array([-1,0,.6]))@U3.conj().T
cases=[("complex_signed_qutrit",Q3,np.ones((1,1)),False),
       ("full_signed_reference",Q6,tau,False),
       ("singular_signed_qutrit_continuity_control",Qs,np.ones((1,1)),True)]
parts={}
for i in range(3):
    for j in range(3):
        if B[i,j]!=0:
            alpha=round(float(math.log(sv[i]/sv[j])),13)
            parts.setdefault(alpha,np.zeros_like(B))[i,j]+=B[i,j]
alphas=np.array(sorted(parts))
partlist=[parts[a] for a in alphas]
signed_rows=[]
for name,Q,ta,has_zero in cases:
    nr=len(ta)
    omega=np.kron(ta,np.diag(sig))
    st=positive_power(omega,.5)
    dt=positive_power(omega,.25)
    dit=positive_power(omega,-.25)
    BF,VF=np.kron(np.eye(nr),B),np.kron(np.eye(nr),V)
    def H(a):
        return (VF@a+a@VF)/2-BF@a@BF
    def L(a):
        return dit@H(dt@a@dt)@dit
    qr,U=np.linalg.eigh(Q)
    absv,signs=np.abs(qr),np.sign(qr)
    Eroot=np.trace(Q@H(Q)).real
    components=np.array([U.conj().T@np.kron(np.eye(nr),ba)@U for ba in partlist])
    for p in PS:
        r,t=1/p,1-2/p
        theta=t
        sinvr=positive_power(omega,-r/2)
        f=sinvr@signed_power(Q,2*r)@sinvr
        sr=positive_power(omega,r/2)
        A=sr@f@sr
        eqouter=positive_power(omega,-(1-r)/2)
        iq=eqouter@signed_power(A,p-1)@eqouter
        i2=dit@signed_power(A,p/2)@dit
        Ep=p/(2*(p-1))*np.trace(st@iq@st@L(f)).real
        root_direct=np.trace(st@i2@st@L(i2)).real
        h=dt@f@dt
        g=dt@iq@dt
        AT=np.trace(g@H(h)).real
        cp=p*math.sin(math.pi/p)/(2*(p-1))
        identity_error=None
        if not has_zero:
            gram=0j
            for i in range(len(qr)):
                for j in range(len(qr)):
                    nodes=math.log(absv[i]/absv[j])-alphas
                    kt=signed_kernel(nodes[:,None],nodes[None,:],theta,signs[i]*signs[j])
                    c=components[:,i,j]
                    gram+=absv[i]*absv[j]*np.vdot(c,kt@c)
            identity_error=float(abs(gram-AT))
            assert identity_error<=1e-9*(1+abs(AT))
        factor_error=abs((1+theta)*Ep-AT)
        root_error=abs(root_direct-Eroot)
        root_map_error=np.linalg.norm(dt@i2@dt-Q)
        assert max(factor_error,root_error,root_map_error)<=1e-9*(1+abs(Ep)+abs(Eroot))
        gap=Ep-cp*Eroot
        assert gap>=-1e-9
        signed_rows.append({"case":name,"p":p,"E_p_signed":float(Ep),"E_root_signed":float(Eroot),
            "profile_gap":float(gap),"factor_error":float(factor_error),"root_error":float(root_error),
            "signed_root_map_error":float(root_map_error),"complete_signed_gram_error":identity_error,
            "singular_zero_threshold_used":has_zero})

nodes=np.array([-3,-.2,0,.4,2.2])
vv=np.tanh(nodes/2)
cosh_rows=[]
for p in PS:
    t=1-2/p
    eta=math.sin(math.pi/p)
    ct=np.cosh(t*nodes/2)
    bb=1/ct
    phi=vv*np.tanh(t*nodes/2)
    nn=(1-np.outer(phi,phi)-eta*np.outer(bb,bb))/(1-np.outer(vv,vv))
    exact=signed_kernel(nodes[:,None],nodes[None,:],t,-1)-eta*signed_kernel(nodes[:,None],nodes[None,:],0,-1)
    congruent=2*np.outer(ct,ct)*nn
    err=float(np.linalg.norm(exact-congruent))
    low=float(np.linalg.eigvalsh(exact).min())
    assert err<1e-12 and low>=-1e-12
    cosh_rows.append({"p":p,"minimum_cosh_difference_eigenvalue":low,"exposed_two_multiplier_congruence_error":err})

complex_inputs=[("complex_full_rank",np.array([[1,.2j,.4],[.3,-1.2,.5j],[1j,.2,.8]],complex)),
                ("complex_rank_one",np.outer(np.array([1,.3j,-.4]),np.array([.2,1j,.5]).conj()))]
dt=np.diag(np.sqrt(sv))
dit=np.diag(1/np.sqrt(sv))
Sigma=np.kron(np.eye(2)/2,np.diag(sig))
sS=positive_power(Sigma,.5)
dS=positive_power(Sigma,.25)
def Hlocal(a):
    return (V@a+a@V)/2-B@a@B
def Llocal(a):
    return dit@Hlocal(dt@a@dt)@dit
def Lhat(a):
    out=np.zeros_like(a)
    for i in range(2):
        for j in range(2):
            out[3*i:3*(i+1),3*j:3*(j+1)]=Llocal(a[3*i:3*(i+1),3*j:3*(j+1)])
    return out
def dil(a):
    zero=np.zeros_like(a)
    return np.block([[zero,a],[a.conj().T,zero]])
polar_rows=[]
for name,f in complex_inputs:
    for p in (1.5,3.0):
        r=1/p
        sr=np.diag(sv**r)
        A=sr@f@sr
        h=dil(f)
        Xhat=positive_power(Sigma,r/2)@h@positive_power(Sigma,r/2)
        outq=np.diag(sv**(-(1-r)))
        iq=outq@polar_power(A,p-1)@outq
        i2=dit@polar_power(A,p/2)@dit
        outqS=positive_power(Sigma,-(1-r)/2)
        iqS=outqS@signed_power(Xhat,p-1)@outqS
        diS=positive_power(Sigma,-.25)
        i2S=diS@signed_power(Xhat,p/2)@diS
        map_error=max(np.linalg.norm(iqS-dil(iq)),np.linalg.norm(i2S-dil(i2)))
        ep=p/(2*(p-1))*np.trace(iq.conj().T@s@Llocal(f)@s).real
        eroot=np.trace(i2.conj().T@s@Llocal(i2)@s).real
        epS=p/(2*(p-1))*np.trace(iqS@sS@Lhat(h)@sS).real
        erootS=np.trace(i2S@sS@Lhat(i2S)@sS).real
        ep_error=abs(epS-ep)
        root_error=abs(erootS-eroot)
        cp=p*math.sin(math.pi/p)/(2*(p-1))
        assert max(map_error,ep_error,root_error)<1e-10
        assert ep-cp*eroot>=-1e-10
        polar_rows.append({"case":name,"p":p,"polar_map_dilation_error":float(map_error),
            "polar_energy_dilation_error":float(ep_error),"root_energy_dilation_error":float(root_error),
            "E_p_polar":float(ep),"E_root_polar":float(eroot),"profile_gap":float(ep-cp*eroot),
            "singular_zero_threshold_used":name=="complex_rank_one"})

out={"status":"PASS_FINITE_EXPOSED_AUDIT_DIAGNOSTICS_ONLY","no_optimization":True,
    "signed_case_p_count":len(signed_rows),"opposite_sign_cosh_kernel_count":len(cosh_rows),
    "polar_dilation_count":len(polar_rows),"signed_checks":signed_rows,"cosh_checks":cosh_rows,
    "polar_dilation_checks":polar_rows,
    "exposed_baseline_sha256":hashlib.sha256((EXPOSED/"INDEPENDENT_BASELINE.txt").read_bytes()).hexdigest(),
    "exposed_root_dilation_audit_sha256":hashlib.sha256((EXPOSED/"EXPOSED_ROOT_DILATION_AUDIT.txt").read_bytes()).hexdigest(),
    "limitations":["Finite checks do not prove universal statements","No p1 signed or complex entropy claim",
                    "Singular checks use explicitly reported numerical zero threshold"]}
with (HERE/"EXPOSED_SIGNED_POLAR_CONTROLS.json").open("x") as f:
    json.dump(out,f,indent=2)
    f.write("\n")
print(json.dumps({"status":out["status"],"signed_checks":len(signed_rows),"cosh_checks":len(cosh_rows),
    "polar_checks":len(polar_rows),"max_signed_gram_error":max(x["complete_signed_gram_error"] or 0 for x in signed_rows),
    "max_polar_map_dilation_error":max(x["polar_map_dilation_error"] for x in polar_rows),
    "max_cosh_congruence_error":max(x["exposed_two_multiplier_congruence_error"] for x in cosh_rows)}))
