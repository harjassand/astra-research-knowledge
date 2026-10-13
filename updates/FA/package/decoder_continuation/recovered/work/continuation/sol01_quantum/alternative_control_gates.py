"""Finite control and matched comparator gates; no operational success claim.

1. G106 finite-frequency pump ramp, actual RWA Duffing/JC Schrödinger dynamics.
2. Finite200ns ancilla syndrome SWAP with data relaxation, then an empirical
   alpha=.02,beta=.07 ancilla readout channel over1.4us. An explicit favorable
   comparator abstraction, not a fit to the complete experimental instrument.
3. GF->EF shelving via finite80ns Gaussian DRAG GE pulses. Even granting ideal
   ground-selective readout, f->e remains an invisible logical amplitude decay.
   The ideal filter is used ONLY to reject an alternative, never to claim an
   implementable low-error readout.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json
import argparse
import time
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
SOURCE=Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery')
sys.path.insert(0,str(SOURCE/'work/phase5/quantum_operation'))
import echoed_curvature_readout as ecr
import floquet_erasure_readout as f
import floquet_bias_and_ramp as ramps
ROOT=Path(__file__).resolve().parent


def lindblad(d,jumps):
    I=np.eye(d);L=np.zeros((d*d,d*d),complex)
    for C in jumps:
        Q=C.conj().T@C
        L+=np.kron(C,C.conj())-.5*(np.kron(Q,I)+np.kron(I,Q.T))
    return L


def decay(d):
    jumps=[]
    for n in range(1,d):
        rate=1/55 if n==1 else n/(2*26)
        C=np.zeros((d,d),complex);C[n-1,n]=np.sqrt(rate);jumps.append(C)
    return lindblad(d,jumps)


def prep(d,code=(0,2),erase=1):
    z=[]
    for a,b in [(code[0],code[0]),(code[1],code[1]),(erase,erase),(code[0],code[1])]:
        rho=np.zeros((d,d),complex);rho[a,b]=1;z.append(rho.ravel())
    return np.array(z).T


def channel_metrics(z,d,code=(0,2)):
    mats=z.T.reshape(4,d,d)
    acc=(np.trace(mats[0])+np.trace(mats[1])).real/2
    overlap=(mats[0,code[0],code[0]].real+mats[1,code[1],code[1]].real+2*abs(mats[3,code[0],code[1]]))/4
    leakage=sum((np.trace(mats[i]).real-mats[i,code[0],code[0]].real-mats[i,code[1],code[1]].real) for i in [0,1])/2
    return {'acceptance_mixed_code':float(acc),'accepted_Choi_infidelity':float(1-overlap/acc),
            'accepted_leakage_mass_per_input':float(leakage),
            'diagnostic_code_projected_infidelity':float(1-overlap/(acc-leakage)),
            'prepared_erasure_flag_probability':float(1-np.trace(mats[2]).real),
            'accepted_populations_by_g_f_e_input':np.diagonal(mats[:3],axis1=1,axis2=2).real.tolist()}


def ancilla_cycle(total=3.8,alpha=.02,beta=.07,initial=None):
    # Data x binary ancilla register. The driven two-level syndrome transition
    # is the experimentally used |e,gA><->|g,fA>, not a terminal data projector.
    d=6;I=np.eye(d);D=[]
    for dest,src,rate in [(0,1,1/55),(1,2,1/26)]:
        C=np.zeros((3,3));C[dest,src]=np.sqrt(rate)
        D.append(np.kron(C,np.eye(2)))
    L=lindblad(d,D);gate=.2;readout=1.4
    z=prep(3) if initial is None else initial;data=[]
    for col in z.T:data.append(np.kron(col.reshape(3,3),np.diag([1.,0.])).ravel())
    z=np.array(data).T
    columns=z.shape[1]
    z=expm(L*(total-gate-readout))@z
    H0=np.zeros((d,d),complex);H0[2,1]=H0[1,2]=.5
    # Truncated Gaussian envelope, zero endpoints, total rotation pi.
    sigma=gate/4;end=np.exp(-.5*(gate/2/sigma)**2)
    grid=np.linspace(0,gate,2001)
    norm=np.trapezoid(np.exp(-.5*((grid-gate/2)/sigma)**2)-end,grid)
    def rhs(t,v):
        amp=np.pi*(np.exp(-.5*((t-gate/2)/sigma)**2)-end)/norm
        H=amp*H0
        G=L-1j*(np.kron(H,I)-np.kron(I,H.T))
        return (G@v.reshape(d*d,columns)).ravel()
    sol=solve_ivp(rhs,[0,gate],z.ravel(),rtol=2e-10,atol=2e-12,method='DOP853',max_step=gate/100)
    assert sol.success
    z=expm(L*readout)@sol.y[:,-1].reshape(d*d,columns)
    # Readout effects are a classical calibrated channel on the ancilla.
    # Empirical beta includes ancilla-readout misses; no artificial data flag.
    out=[]
    for rho in z.T.reshape(columns,d,d):
        out.append(((1-alpha)*rho[::2,::2]+beta*rho[1::2,1::2]).ravel())
    z=np.array(out).T
    return z,{'cycle_us':total,'finite_SWAP_us':gate,'ancilla_readout_us':readout,
              'pre_SWAP_idle_us':total-gate-readout,'readout_false_positive':alpha,
              'readout_false_negative_given_ancilla_excitation':beta,
              'metrics':channel_metrics(z,3) if columns==4 else None,
              'scope':'Gaussian effective FWM two-state SWAP plus all data relaxation during gate/readout. Favorable comparator; no claimed full-device channel calibration or XY4 pulse-error fit.'}


def ef_exact(a,b,T):
    se=np.exp(-b*T);sf=np.exp(-a*T)
    u=a*T*sf if abs(a-b)<1e-12 else a*(sf-se)/(b-a)
    p=(se+sf+u)/2
    overlap=(se+sf+2*np.sqrt(se*sf))/4
    return p,1-overlap/p,u/2


def ge_pulse(params,d=5,T=.08,with_decay=False,initial=None):
    # Actual weakly anharmonic ladder in the drive rotating frame. Parameters
    # are amplitude multiplier, derivative quadrature multiplier, detuningMHz.
    a,drag,det=params;alpha=-2*np.pi*180
    n=np.arange(d);b=np.diag(np.sqrt(np.arange(1,d)),1)
    sigma=T/4;edge=np.exp(-.5*(T/2/sigma)**2)
    grid=np.linspace(0,T,2001)
    norm=np.trapezoid(np.exp(-.5*((grid-T/2)/sigma)**2)-edge,grid)
    static=np.diag(alpha*n*(n-1)/2-2*np.pi*det*n)
    I=np.eye(d)
    L=decay(d) if with_decay else None
    if initial is None:initial=np.eye(d,dtype=complex)
    def rhs(t,y):
        gauss=np.exp(-.5*((t-T/2)/sigma)**2)
        x=a*np.pi*(gauss-edge)/norm
        dx=-a*np.pi*(t-T/2)/sigma**2*gauss/norm
        omega=x-1j*drag*dx/alpha
        H=static+(omega*b.conj().T+omega.conjugate()*b)/2
        if with_decay:
            G=L-1j*(np.kron(H,I)-np.kron(I,H.T))
            return (G@y.reshape(d*d,-1)).ravel()
        return (-1j*H@y.reshape(d,d)).ravel()
    sol=solve_ivp(rhs,[0,T],initial.ravel(),rtol=1e-9,atol=1e-11,method='DOP853',max_step=T/80)
    assert sol.success
    return sol.y[:,-1].reshape(initial.shape)


def shelving_test():
    def objective(x):
        U=ge_pulse(x)
        return float(1-(abs(U[1,0])**2+abs(U[0,1])**2+abs(U[2,2])**2)/3)
    fit=minimize(objective,[1.,1.,-.1],method='Nelder-Mead',options={'maxiter':160,'xatol':1e-7,'fatol':1e-11})
    U=ge_pulse(fit.x);z=ge_pulse(fit.x,with_decay=True,initial=prep(5))
    cases=[]
    P=np.diag([0,1,1,0,0]);M=np.kron(P,P)
    D=decay(5)
    for T in [.15,.35,1.1,1.4,3.]:
        # Grant a perfect ground-only flag and perfect return mapping. This is
        # an optimistic FAIL gate, not a purported hardware readout.
        out=M@expm(D*T)@z
        back=np.zeros((3,5));back[0,1]=1;back[1,0]=1;back[2,2]=1
        recovered=np.array([(back@rho.reshape(5,5)@back.T).ravel() for rho in out.T]).T
        p,err,jump=ef_exact(1/26,1/55,T)
        cases.append({'EF_hold_us':T,'ideal_instantaneous_shelving_exact':{
            'acceptance':float(p),'accepted_Choi_infidelity':float(err),
            'invisible_f_to_e_mass_per_mixed_input':float(jump)},
            'finite_GE_pulse_then_perfect_flag_and_return':channel_metrics(recovered,3)})
    # Independent exact matrix check for the closed-form EF accepted channel.
    maxerr=0.
    for a in [.01,1/26,.08]:
        for b in [.01,1/55,.08]:
            L=np.zeros((9,9),complex)
            for dest,src,rate in [(0,1,b),(1,2,a)]:
                C=np.zeros((3,3));C[dest,src]=np.sqrt(rate);L+=lindblad(3,[C])
            for T in [.15,1.4,3.]:
                z0=prep(3,code=(1,2),erase=0)
                P3=np.diag([0,1,1]);out=np.kron(P3,P3)@expm(L*T)@z0
                m=channel_metrics(out,3,code=(1,2));p,err,_=ef_exact(a,b,T)
                maxerr=max(maxerr,abs(m['acceptance_mixed_code']-p),abs(m['accepted_Choi_infidelity']-err))
    return {'finite_GE_duration_us':.08,'Gaussian_DRAG_parameters':fit.x.tolist(),
            'unitary_transfer_objective':objective(fit.x),'optimizer_success':bool(fit.success),
            'transfer_probabilities_g_to_e_e_to_g_f_to_f':[float(abs(U[1,0])**2),float(abs(U[0,1])**2),float(abs(U[2,2])**2)],
            'cases':cases,'independent_EF_matrix_checks':27,'max_EF_formula_matrix_error':maxerr,
            'scope':'Different EF storage/readout mechanism rejected even with free perfect selective flag and return. Finite initial GE pulse is explicit RWA Duffing control. No physical perfect flag is claimed.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='ALTERNATIVE_CONTROL_RESULTS.json')
    args=parser.parse_args()
    start=time.perf_counter();ecr.MEASURED_HALF_GE_CAVITY_SHIFT_MHZ=.5
    f.G=ecr.calibrate_g();f.DELTA=-2203.
    ramp=[]
    for ns in [50.,100.]:
        for N,q in [(1,0),(2,2),(3,2)]:ramp.append(ramps.finite_ramp(N,q,217.28013507543088,2503.,ns))
    ancilla=[]
    for T in [3.52,3.8]:
        _,case=ancilla_cycle(T);ancilla.append(case)
    z,case=ancilla_cycle(3.8)
    # Repeated accepted source-ancilla comparator includes residual leakage.
    # Build the complete superoperator by nine data matrix units.
    # One-cycle metrics suffice for current retirement; repetitions are in the
    # record-model script and no EOL ideal projection enters this comparator.
    result={'status':'FINITE_CONTROL_AND_ALTERNATIVE_FAIL_GATES_IN_EXPLICIT_MODELS',
            'G_MHz':f.G,'ramp_tests':ramp,'ancilla_comparator':ancilla,
            'EF_shelving_alternative':shelving_test(),
            'runtime_seconds':time.perf_counter()-start,
            'limitations':['Source empirical FPR/FNR do not specify a complete ancilla quantum channel. The effective SWAP model is favorable and illustrative, not an acquired accepted-Choi comparator.',
                           'Finite pump ramps are low-excitation unitary turn-on tests, not a validated pumped bright-state readout or pump-off.',
                           'The EF alternative is granted an ideal flag only for a negative bound. No positive operational result uses a terminal projector.']}
    (ROOT/args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
