"""Independent FC criticism fixtures. No producer imports; floats are diagnostic.

Exact fractions build finite marked-partition rates. Matrix exponentials and
physical numerical sensitivities use double precision, not interval arithmetic.
"""
from fractions import Fraction as F
from pathlib import Path
import json, math
import numpy as np
from scipy.linalg import expm, eigh
from scipy.integrate import solve_ivp, quad
from scipy.special import eval_genlaguerre
from scipy.constants import c, elementary_charge as ev, atomic_mass, m_e

out = {"status": "PASS", "scope": "Independent finite diagnostics, not universal proof or external validation"}
rng = np.random.default_rng(813172)

def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for q in range(minimum, n+1):
        for tail in partitions(n-q, q):
            yield (q,)+tail

collision=[]
for n in range(1,9):
    states=list(partitions(n)); lookup={s:i for i,s in enumerate(states)}
    rates=[[F(0) for _ in states] for _ in states]
    for i,s in enumerate(states):
        for a,q in enumerate(s):
            if q==1: continue
            rates[i][i]-=F(q-1,q+1)
            for j in range(1,q):
                target=tuple(sorted(s[:a]+s[a+1:]+(j,q-j)))
                rates[i][lookup[target]]+=F(1,q+1)
        assert sum(rates[i])==0
    Q=np.array([[float(x) for x in row] for row in rates])
    # Initial P takes 0 or 1 with mean .37, so E[P^q]=.37 for all q>=1.
    initial=np.array([.37**len(s) for s in states])
    sumsquares=np.array([sum(q*q for q in s)/n**2 for s in states])
    m0=np.r_[1.,np.full(n,.37)]
    def rhs(t,m):
        dm=np.zeros(n+1)
        for k in range(2,n+1):
            dm[k]=(-(k-1)*m[k]+sum(m[j]*m[k-j] for j in range(1,k)))/(k+1)
        return dm
    sol=solve_ivp(rhs,(0,20),m0,t_eval=[0,.5,2,20],rtol=1e-11,atol=1e-12)
    for l,t in enumerate(sol.t):
        dist=expm(t*Q)[lookup[(n,)]]
        moment=float(dist@initial)
        target=float(sol.y[n,l])
        variance_factor=float(dist@sumsquares)
        expected=math.exp(-t/3)+(1-math.exp(-t/3))/n
        assert abs(moment-target)<3e-10
        assert abs(variance_factor-expected)<1e-12
        assert np.min(dist)>-1e-14 and abs(dist.sum()-1)<1e-12
        collision.append({"n":n,"t":float(t),"moment_error":abs(moment-target),"variance_factor_error":abs(variance_factor-expected)})
out["marked_partition_checks"]=collision

a,b,rho=1.,1.1,.2
r=1-a/b; g=b*(1+rho)
C=((1+rho)/(1-rho))**1.5/(1-r/rho)
I=(a*b/(g*(2*a-g)))**1.5
radial=lambda x:4*math.pi*x*x*(2*math.pi*g)**-1.5*(g/b)**-1.5*math.exp(-x*x*(2/g-1/a)/2)
integral,quaderr=quad(radial,0,np.inf,epsabs=1e-12)
assert abs(integral-I)<1e-10
envelope_max=0.
for k in range(41):
    for x in np.linspace(0,80,81):
        normalized=(1-rho)**1.5*math.exp(-x*rho/(1+rho))*rho**k*eval_genlaguerre(k,.5,x)
        envelope_max=max(envelope_max,abs(normalized))
assert envelope_max<=1+1e-12
out["collision_envelope_diagnostics"]={"C":C,"I":I,"integral_error":abs(integral-I),"reported_quad_error":quaderr,"signed_calls_bound":19*C*C*I,"grid_points":41*81,"max_envelope_ratio":envelope_max}

def gibbs(H,beta):
    E,U=eigh(H); w=np.exp(-beta*(E-E[0])); w/=w.sum()
    rho=(U*w)@U.conj().T
    logz=-beta*E[0]+math.log(np.exp(-beta*(E-E[0])).sum())
    return rho,logz

quantum=[]
sharp=[]
for test in range(96):
    k=2+test%4; sizes=rng.integers(1,5,size=k); n=int(sizes.sum())
    labels=np.repeat(np.arange(k),sizes); beta=float(rng.uniform(.05,2))
    A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    H=(A+A.conj().T)/5
    # Include substantial unequal diagonal energy offsets to stress block weights.
    H+=np.diag(rng.uniform(-4,4,size=k)[labels])
    D=H*(labels[:,None]==labels[None,:]); T=H-D
    rho,lz=gibbs(H,beta); _,ld=gibbs(D,beta)
    p=np.array([np.trace(rho[np.ix_(labels==i,labels==i)]).real for i in range(k)])
    z=np.array([math.exp(gibbs(D[np.ix_(labels==i,labels==i)],beta)[1]) for i in range(k)])
    ci=p*math.exp(lz)
    normgraph=np.zeros((k,k))
    for i in range(k):
        for j in range(k):
            if i!=j: normgraph[i,j]=np.linalg.norm(T[np.ix_(labels==i,labels==j)],2)
    Cn=float(np.diag(expm(beta*normgraph)).max())
    tau=float(np.trace(rho@T).real)
    Ck=math.exp(-beta*tau)
    Cuse=min(Cn,Ck)
    M=beta*normgraph+np.diag(np.log(z))
    compressed=expm(M)
    ratio=math.exp(lz-ld)
    assert tau<=1e-11 and ratio>=1-1e-11
    assert ratio<=Cuse*(1+2e-10)
    assert np.all(ci>=z*(1-1e-10)) and np.all(ci<=np.diag(compressed)*(1+2e-10))
    for design in range(4):
        v=rng.uniform(-12,12,size=k); V=np.diag(v[labels])
        actual=-(gibbs(H+V,beta)[1]-lz)/beta
        u=np.exp(-beta*(v-v.min())); mass=1/Cuse; L=0.
        for i in np.argsort(u):
            take=min(p[i],mass); L+=take*u[i]; mass-=take
        low=max(v.min(),v.min()-math.log(p@u)/beta)
        high=min(v.max(),v.min()-math.log(L)/beta)
        assert low-2e-10<=actual<=high+2e-10
        quantum.append({"test":test,"labels":k,"dimension":n,"design":design,"margin_below":actual-low,"margin_above":high-actual})
    # Scalar blocks attain the sharp upper partition compression exactly.
    scalar=-M/beta
    assert np.max(np.abs(expm(-beta*scalar)-compressed))/max(1.,np.max(np.abs(compressed)))<1e-12
    sharp.append({"test":test,"relative_partition_gap":float((compressed.trace().real-ci.sum())/ci.sum())})
out["quantum_reweighting_checks"]=quantum
out["block_compression_checks"]=sharp

# Source histogram-only witness, independently recomputed without its code.
sx=np.array([[0.,1.],[1.,0.]])
sz=np.diag([1.,-1.]); V=.2*np.eye(2)+sz
flips=[]
for J in (0.,10.):
    R,L=gibbs(J*sx,1.)
    df=-(gibbs(J*sx+V,1.)[1]-L)
    flips.append({"J":J,"histogram":np.diag(R).tolist(),"delta_F":df})
assert flips[0]["delta_F"]<0 and flips[1]["delta_F"]>0
out["histogram_without_coherence_sign_reversal"]=flips

# New audit qualification: a stationary-looking metastable label histogram and
# exactly T=0 do not establish that the reference is the global Gibbs state.
# Order (label0,b0),(label1,b0),(label0,b1),(label1,b1).
H=np.diag([0.,0.,-10.,10.]); labels=np.array([0,1,0,1]); v=np.array([.2,-.8])
R,L=gibbs(H,1.); ptrue=np.array([R[labels==i,labels==i].sum() for i in range(2)])
actual=-(gibbs(H+np.diag(v[labels]),1.)[1]-L)
wrong=-math.log(.5*math.exp(-v[0])+.5*math.exp(-v[1]))
assert wrong<0<actual
out["metastable_histogram_counterexample"]={"H_diagonal":[0,0,-10,10],"T_norm":0,"measured_metastable_histogram":[.5,.5],"true_equilibrium_histogram":ptrue.tolist(),"incorrect_reweighting_delta":wrong,"true_delta_F":actual,"scope":"Refutes substituting a trapped stationary histogram for the theorem's actual equilibrium input; does not refute the theorem"}

M=127.60*atomic_mass
kinematics=[]
for Ekev in (100,300,500):
    E=Ekev*1e3*ev; momentum=math.sqrt(E*(E+2*m_e*c*c))/c
    q=2*momentum; T0=q*q/(2*M)/ev
    f=3.24e12; A=1e-12; velocity=2*math.pi*f*A
    delta=q*velocity/ev
    derivative=4*(E+m_e*c*c)/(M*c*c) # d(T0_eV)/d(E_eV)
    kinetic=M*velocity*velocity/(2*ev)
    assert abs(delta-2*math.sqrt(T0*kinetic))<1e-12
    kinematics.append({"electron_keV":Ekev,"T0_eV":T0,"one_pm_delta_eV":delta,"one_pm_basis_splitting_eV":1.5*delta,"equivalent_shift_keV":delta/derivative/1e3})
absorbed=1.4e21/2.94e22*1.57
amplitude=24e-12; velocity=2*math.pi*3.24e12*amplitude
coherent=.5*M*velocity**2/ev
timing=[]
for fwhm in (50,100,200):
    sigma=fwhm*1e-15/(2*math.sqrt(2*math.log(2)))
    timing.append({"FWHM_fs":fwhm,"modulation":math.exp(-.5*(2*math.pi*3.24e12*sigma)**2)})
hazard=-math.log(.01)/(-math.log(.99))
assert 458<hazard<459 and coherent>2*absorbed
out["phonon_kinematics"]={"recoil_values":kinematics,"coherent_eV_per_atom":coherent,"estimated_absorbed_eV_per_atom":absorbed,"ratio":coherent/absorbed,"equal_amplitude_energy_ceiling_m_s":math.sqrt(2*absorbed*ev/M),"timing":timing,"hazard_ratio_99_to_1":hazard}

Path('independent_results.json').write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"PASS","partition_cases":len(collision),"quantum_enclosures":len(quantum),"block_compressions":len(sharp),"laguerre_grid_points":41*81,"metastable_reversal":True,"Te_electron_energies":len(kinematics)},indent=2))
