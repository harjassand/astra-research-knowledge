"""Phase-calibrated baselines, actual SPAM, no-click audit and Wick remainder."""
from pathlib import Path
import itertools,json,sys
import numpy as np
from scipy.optimize import minimize
from functools import lru_cache
from gaussian_cross_engine import symplectic
from joint_gaussian_instrument import gate_choi

BASE=Path(__file__).parent
def dec(x):return np.array(x['real'])+1j*np.array(x['imag'])


def phase_oracle(branches):
    perm=[0,1,3,2];idx=[4*j+perm[j] for j in range(4)]
    total=0.;phases={}
    for label,J in branches.items():
        A=J[np.ix_(idx,idx)]
        def loss(x):
            u=np.exp(1j*np.r_[0,x])
            return -np.real(u.conj()@A@u)/4
        ev,vec=np.linalg.eigh(A);seed=np.angle(vec[:,-1]);seed=seed[1:]-seed[0]
        candidates=[minimize(loss,x,method='BFGS',options={'gtol':1e-11}) for x in (np.zeros(3),seed,-seed)]
        best=min(candidates,key=lambda r:r.fun)
        total-=best.fun;phases[str(label)]=best.x.tolist()
    return float(1-total),phases


def no_click_sector(W0,S):
    out={}
    for s in (-1,1):
        ids=np.flatnonzero(S==s);A=W0[np.ix_(ids,ids)]
        probability=np.trace(A).real/4
        norm=np.trace(A).real
        raw=1-np.sum(A).real/(4*norm)
        def loss(x):
            u=np.exp(1j*np.r_[0,x]);return -np.real(u.conj()@A@u)/(4*norm)
        ev,v=np.linalg.eigh(A);a=np.angle(v[:,-1]);seed=a[1:]-a[0]
        opt=min([minimize(loss,x,method='BFGS') for x in (np.zeros(3),seed,-seed)],key=lambda r:r.fun)
        out[str(s)]={'probability_uniform_input':float(probability),
                     'conditional_infidelity':float(raw),
                     'conditional_infidelity_after_oracle_phases':float(1+opt.fun),
                     'branch_probability_ratio':float(np.max(np.diag(A).real)/np.min(np.diag(A).real))}
    return out


def pauli_diagnostic(J):
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    P={'I':I,'X':X,'Y':Y,'Z':Z}
    U=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    out={}
    for a,b in itertools.product(P,repeat=2):
        v=(np.kron(P[a],P[b])@U).reshape(-1,order='F')/2
        out[a+b]=float(np.real(v.conj()@J@v))
    return out


def wick_remainder(label,params,S,centered=False):
    snapshots=json.loads((BASE/f'joint_{label}_moments.json').read_text())['snapshots']
    O=symplectic(6)
    ops=np.zeros((12,12),complex)
    for j in range(6):
        ops[2*j,2*j]=ops[2*j+1,2*j]=1/np.sqrt(2)
        ops[2*j,2*j+1]=1j/np.sqrt(2);ops[2*j+1,2*j+1]=-1j/np.sqrt(2)
    monos=[]
    for j in range(3):monos.extend([(2*j,2*j,2*(j+3)+1),(2*j+1,2*j+1,2*(j+3))])
    monos.extend([(0,2,4),(1,3,5)])
    times=[0.];norms=[np.full(8,params['g3'])];devs=[np.full(8,params['g3'])]
    max_imag=0.
    for snap in snapshots:
        t=snap['time'];means=np.array(snap['mean']);covs=np.array(snap['covariance'])
        nr=[];vr=[]
        for k in range(8):
            mu=np.zeros(12,complex) if centered else ops@means[k]
            C=ops@(covs[k]+.5j*O)@ops.T
            @lru_cache(None)
            def moment(tup):
                if not tup:return 1.+0j
                first,rest=tup[0],tup[1:]
                ans=mu[first]*moment(rest)
                for j,v in enumerate(rest):ans+=C[first,v]*moment(rest[:j]+rest[j+1:])
                return ans
            coeff=np.r_[np.full(6,params['g2']),np.full(2,params['g3']*S[k] if t<params['drive_time'] else 0.)]
            avg=sum(c*moment(m) for c,m in zip(coeff,monos))
            sq=sum(c1*c2*moment(m1+m2) for c1,m1 in zip(coeff,monos) for c2,m2 in zip(coeff,monos))
            max_imag=max(max_imag,abs(sq.imag))
            nr.append(np.sqrt(max(sq.real,0.)))
            vr.append(np.sqrt(max(sq.real-avg.real**2,0.)))
        times.append(t);norms.append(nr);devs.append(vr)
    norms=np.array(norms);devs=np.array(devs)
    return {'max_integrated_raw_Duhamel_bound':float(np.trapezoid(norms,x=times,axis=0).max()),
            'max_integrated_phase_stripped_bound':float(np.trapezoid(devs,x=times,axis=0).max()),
            'max_instantaneous_remainder_rms':float(norms.max()),
            'Wick_square_max_imaginary_roundoff':float(max_imag),
            'centered_about_exact_classical_mean':centered,
            'qualification':'These are coarse-sampled Gaussian-moment diagnostics, not rigorous quadrature upper bounds. A value above one does not certify nonlinear-device accuracy; most remainder is common within each parity sector.'}


def main(labels):
    result={}
    for label in labels:
        p=BASE/f'joint_{label}_results.json'
        if not p.exists():continue
        x=json.loads(p.read_text());Wp=dec(x['reported_plus_instrument']);Wm=dec(x['reported_minus_instrument'])
        J,e,branches=gate_choi([Wp,Wm],return_branches=True)
        oracle,ph=phase_oracle(branches)
        Js,es,bs=gate_choi([Wp,Wm],qx=.001,qprep=.001,return_branches=True)
        os,_=phase_oracle(bs)
        S=np.prod(np.array(list(itertools.product((1.,-1.),repeat=3))),axis=1)
        result[label]={'raw_CNOT_infidelity':e,'oracle_branch_phase_calibrated_CNOT_infidelity':oracle,
                       'oracle_phases':ph,'raw_CNOT_with_noisy_X_readout_and_ancilla_preparation':es,
                       'oracle_CNOT_with_noisy_X_readout_and_ancilla_preparation':os,
                       'Pauli_diagonal_diagnostic_not_a_twirl':pauli_diagnostic(J),
                       'no_click_within_parity':no_click_sector(dec(x['no_click_Gram']),S)}
        if label=='mod_odd_1e4' or label.startswith('nonlinear_mean'):
            result[label]['nonlinear_remainder_diagnostic']=wick_remainder(label,x['parameters'],S,centered=label.startswith('nonlinear_mean'))
    (BASE/'joint_comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main(sys.argv[1:] or ['unmod','mod','mod_odd_1e4','unmod_independent','mod_independent_odd_1e4','mod_odd_1e4_fine','nonlinear_mean_unmod','nonlinear_mean_mod'])
