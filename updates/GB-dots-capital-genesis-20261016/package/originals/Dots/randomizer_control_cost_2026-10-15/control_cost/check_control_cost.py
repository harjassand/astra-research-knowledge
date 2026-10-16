#!/usr/bin/env python3
"""Bounded self-authored algebra checks; dimensionless examples are not hardware data."""
import itertools, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from scipy.stats import poisson, binom

OUT=Path(__file__).with_name('checks.json')
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
kron=np.kron
I4=np.eye(4,dtype=complex)

def bdet(J, widths):
    return .5*(math.prod(math.cosh(2*J*d) for d in widths)-1)

def all_bits(n):
    return list(itertools.product([0,1],repeat=n))

def fft_ops(U):
    # Dictionary indexed by tuples of independent initial bits.
    n=len(next(iter(U)))
    return {chi: sum(((-1)**sum(c*f for c,f in zip(chi,fs)))*v
                     for fs,v in U.items())/(2**n) for chi in all_bits(n)}

res={"scope":"Self-authored finite algebra checks only; all chosen numbers are dimensionless stress-test inputs, not device measurements."}
# Exact scalar moment for deterministic cells, including unequal cells.
errs=[]
for M in range(1,9):
    raw=np.arange(1,M+1,dtype=float)
    for widths in [np.ones(M)/M,raw/raw.sum()]:
        J=.37
        vals=[]
        for bs in all_bits(M-1):
            signs=[1]+[(-1)**b for b in bs]
            vals.append(math.sinh(J*sum(d*s for d,s in zip(widths,signs)))**2)
        errs.append(abs(np.mean(vals)-bdet(J,widths)))
res['deterministic_cell_mgf_max_abs_error']=max(errs)

# Resource identities: Poisson, capped, binomial, second moments.
mu,eps,c,M=2.7,.013,4,5
n=np.arange(100)
pn=poisson.pmf(n,mu)
s_exact=(1-eps)**c*math.exp(-mu*eps)
s_sum=float(np.sum(pn*(1-eps)**(c+n)))
s_cap=float(np.sum(pn[:M+1]*(1-eps)**(c+n[:M+1])))
s_cap_formula=(1-eps)**c*math.exp(-mu)*sum((mu*(1-eps))**k/math.factorial(k) for k in range(M+1))
K=12
bn=np.arange(K+1)
s_bin=float(np.sum(binom.pmf(bn,K,.5)*(1-eps)**(c+bn)))
s_bin_formula=(1-eps)**c*(1-eps/2)**K
res['resource_identities']={
 'poisson_survival_error':abs(s_exact-s_sum),
 'cap_survival_error':abs(s_cap-s_cap_formula),
 'binomial_survival_error':abs(s_bin-s_bin_formula),
 'poisson_second_moment_error':abs(float(np.sum(pn*(c+n)**2))-((c+mu)**2+mu)),
 'binomial_second_moment_error':abs(float(np.sum(binom.pmf(bn,K,.5)*(c+bn)**2))-((c+K/2)**2+K/4)),
 'cap_flag_mass':1-s_cap_formula,
 'cap_fault_plus_tail_direct':float(poisson.sf(M,mu)+np.sum(pn[:M+1]*(1-(1-eps)**(c+n[:M+1]))))
}
# The two-event feasible ordered-simplex volume.
t,beta,delta=1.3,.08,.11
vol2=quad(lambda x:max(0,t-beta-(x+delta)),beta,t-beta,points=[t-beta-delta],epsabs=1e-13,epsrel=1e-13)[0]
res['spacing_simplex_n2_error']=abs(vol2-max(0,t-2*beta-delta)**2/2)

# Two-parent coherent-effect test. Reused physical support, noncommuting baseline,
# arbitrary shared qubit bath. This checks the effect theorem, not a code geometry.
J=.23; r=.017; Mc=3; dt=1/Mc
H0=.11*kron(Y,X)+.07*kron(I,Y)
A=[kron(Z,X),kron(X,Z)]
D=[kron(X,Y),kron(Z,Y)]
E={S:np.zeros((4,4),complex) for S in [(0,),(1,),(0,1)]}
Eref={S:np.zeros((4,4),complex) for S in E}
paths=all_bits(2*(Mc-1))
for bits in paths:
    xis=[[1]+[(-1)**b for b in bits[k*(Mc-1):(k+1)*(Mc-1)]] for k in range(2)]
    maps={}; maps0={}
    for fs in all_bits(2):
        U=I4.copy(); U0=I4.copy()
        for l in range(Mc):
            H=H0.copy(); R=np.zeros((4,4),complex)
            for k in range(2):
                H+=((-1)**fs[k])*xis[k][l]*J*A[k]
                R+=((-1)**fs[k])*r*(.7+.3*xis[k][l])*D[k]
            U=expm(-1j*(H+R)*dt)@U
            U0=expm(-1j*H*dt)@U0
        maps[fs]=U; maps0[fs]=U0
    for full, out in [(fft_ops(maps),E),(fft_ops(maps0),Eref)]:
        for S in E:
            for chi,L in full.items():
                if all(chi[k] for k in S): out[S]+=L.conj().T@L/len(paths)
q=min(J*J,bdet(J,[dt]*Mc))
p=(math.sqrt(q)+r)**2
res['coherent_shared_bath_subset_check']={
 'reference_q':q,'residual_uniform_action':r,'charged_p':p,
 'subsets':[{"selected":list(S),"actual_effect_norm":float(np.linalg.eigvalsh(E[S])[-1]),
             "bound":p**len(S),"reference_effect_norm":float(np.linalg.eigvalsh(Eref[S])[-1]),
             "reference_bound":q**len(S)} for S in E]
}
assert all(np.linalg.eigvalsh(E[S])[-1] <= p**len(S)+1e-12 for S in E)
assert all(np.linalg.eigvalsh(Eref[S])[-1] <= q**len(S)+1e-12 for S in E)

# Complete actual CP-flag/Fourier check with one proposed boundary per parent.
# A flip executes an update; its exact reference control is identity in the common
# toggling representation. The bad branch is a noncommuting data-bath unitary.
eps_test=.041; Mtest=2; dt=.5
bad=[expm(-.43j*kron(Y,Z)),expm(-.31j*kron(Z,Y))]
Ecp={S:np.zeros((4,4),complex) for S in [(0,),(1,),(0,1)]}
complete=np.zeros((4,4),complex)
for flips in all_bits(2):
    for faults in all_bits(2):
        if any(faults[k] and not flips[k] for k in range(2)):continue
        weight=.25
        for k in range(2):
            if flips[k]:weight*=eps_test if faults[k] else 1-eps_test
        maps={}
        for fs in all_bits(2):
            Hfirst=H0.copy(); Hsecond=H0.copy()
            for k in range(2):
                Hfirst+=(-1)**fs[k]*J*A[k]
                Hsecond+=(-1)**(fs[k]+flips[k])*J*A[k]
            U=expm(-1j*Hfirst*dt)
            for k in range(2):
                if faults[k]:U=bad[k]@U
            U=expm(-1j*Hsecond*dt)@U
            maps[fs]=U
        for chi,L in fft_ops(maps).items():
            effect=weight*L.conj().T@L
            complete+=effect
            for S in Ecp:
                if all(faults[k] or chi[k] for k in S):Ecp[S]+=effect
qcp=min(J*J,bdet(J,[dt]*Mtest)); fcp=eps_test/2; pcp=qcp+fcp
res['cp_mixed_subset_check']={
 'q':qcp,'f_control':fcp,'p':pcp,
 'completeness_error':float(np.linalg.norm(complete-I4)),
 'subsets':[{"selected":list(S),"actual_effect_norm":float(np.linalg.eigvalsh(Ecp[S])[-1]),
             "bound":pcp**len(S)} for S in Ecp]
}
assert np.linalg.norm(complete-I4)<1e-12
assert all(np.linalg.eigvalsh(Ecp[S])[-1]<=pcp**len(S)+1e-12 for S in Ecp)

# Choi support obstructions to an exact ideal CP branch.
def vec(A):return A.reshape(-1,order='F')/math.sqrt(2)
theta=1/7; w=.1
u=vec(expm(-1j*theta*X)); ident=vec(I)
v=ident-u*np.vdot(u,ident);v/=np.linalg.norm(v)
Junit=np.outer(u,u.conj());Jid=np.outer(ident,ident.conj())
unit_witness=float(np.real(np.vdot(v,(Junit-w*Jid)@v)))
ad_p=.17;s=math.sqrt(1-ad_p)
K0=np.diag([1,s]);K1=np.array([[0,math.sqrt(ad_p)],[0,0]],complex)
Jad=sum(np.outer(vec(A),vec(A).conj()) for A in [K0,K1])
v_ad=np.array([s,0,0,-1],complex)/math.sqrt(1+s*s)
ad_witness=float(np.real(np.vdot(v_ad,(Jad-w*Jid)@v_ad)))
res['choi_obstructions']={
 'unitary_subtraction_witness':unit_witness,'unitary_formula':-w*math.sin(theta)**2,
 'amplitude_damping_subtraction_witness':ad_witness,
 'amplitude_damping_formula':-w*(s-1)**2/(2*(1+s*s))
}
assert unit_witness<0 and ad_witness<0

# Finite bath copies the current private frame; every reduced data control exact.
alpha=.37; XX=kron(X,X); XD=kron(X,I); H=alpha*kron(Z,Z)
plus=np.array([1,1],complex)/math.sqrt(2);zero=np.array([1,0],complex)
psi0=kron(plus,zero);target=expm(-1j*alpha*Z)@plus
rho_target=np.outer(target,target.conj());rho_initial=np.outer(plus,plus.conj())
copy_err=[]
for jump_times in [[],[.17],[.13,.57,.8]]:
 for f in [0,1]:
    psi=(XX if f else I4)@psi0
    last=0
    for time in jump_times:
      psi=expm(-1j*H*(time-last))@psi
      psi=XX@psi;last=time
    psi=expm(-1j*H*(1-last))@psi
    F=(f+len(jump_times))%2
    psi=(XD if F else I4)@psi
    rho=np.outer(psi,psi.conj()).reshape(2,2,2,2)
    reduced=np.einsum('abcb->ac',rho)
    copy_err.append(float(np.linalg.norm(reduced-rho_target)))
res['private_frame_copy_counterexample']={
 'max_reduced_state_error_vs_unsuppressed_rotation':max(copy_err),
 'trace_norm_distance_to_ideal':float(np.sum(abs(np.linalg.eigvalsh(rho_target-rho_initial)))),
 'exact_distance':2*abs(math.sin(alpha)),
 'bath_dimension':2
}
assert max(copy_err)<1e-12

# Explicit symbolic-region illustration only: numbers test inequalities, not hardware.
a=.2;m=2;M=24;c=4;eps=1e-5;u=1e-4;K=m*(M-1)
qd=min(a*a,m*bdet(a,[1/M]*M))
fd=1-(1-eps)**c*(1-eps/2)**K
br=u*math.sqrt((c+K/2)**2+K/4)
res['dimensionless_budget_sanity_check']={
 'label':'Synthetic dimensionless inequality check; no hardware interpretation',
 'a':a,'m':m,'M':M,'c':c,'epsilon':eps,'u':u,
 'old_action_squared':a*a,'reference_q':qd,
 'cp_paid_bound':qd+fd,'coherent_paid_bound':(math.sqrt(qd)+br)**2,
 'cp_improves':bool(qd+fd<a*a),'coherent_improves':bool((math.sqrt(qd)+br)**2<a*a)
}
assert max(errs)<1e-12
assert all(v<1e-11 for k,v in res['resource_identities'].items() if k.endswith('error'))
OUT.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
