"""Adversarial controls for warm gain, Casimir drift and hidden pure controllers.

Finite controls support, but do not independently audit, the analytic proofs.
"""
import json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm,eigh
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
def opnorm(x):return float(np.linalg.norm(x,2))
def maxeig(x):return float(np.linalg.eigvalsh((x+x.conj().T)/2)[-1])
def spin_ops(ell):
    sm=np.array([[0,1],[0,0]],complex);n=sm.conj().T@sm;allsm=[];alln=[]
    for i in range(ell):
        s=np.ones((1,1),complex);p=s.copy()
        for j in range(ell):s=np.kron(s,sm if i==j else np.eye(2));p=np.kron(p,n if i==j else np.eye(2))
        allsm.append(s);alln.append(p)
    Ns=sum(alln);Sz=Ns-ell/2*np.eye(2**ell);Sminus=sum(allsm)
    S2=Sz@Sz-Sz+Sminus.conj().T@Sminus
    e,v=eigh(S2+.25*np.eye(2**ell));J=(v*np.sqrt(np.maximum(e,0)))@v.conj().T-.5*np.eye(2**ell)
    return allsm,alln,Ns,Sz,S2,J,Sz+J
def adj_diss(K,L):
    LL=L.conj().T@L
    return L.conj().T@K@L-(LL@K+K@LL)/2
def gain_checks():
    X=np.array([[0,1],[1,0]],complex);Z=np.diag([1.,-1.]);delta=.1;G=np.eye(2)+delta*Z;T=math.pi/2
    rows=[]
    for omega in (0.,1.,10.,1000.):
        H=omega*X
        for m in (1,2,5,10):
            vs={j:expm(-1j*(H+j*G)*T) for j in range(-m,m+1,2)}
            A=sum(math.comb(m,k)/2**m*vs[2*k-m] for k in range(m+1))
            residual=opnorm(A);eff=1-residual**2
            assert residual<=math.sin(math.pi*delta/2)+1e-10
            rows.append({'source_frequency':omega,'photons':m,'no_transfer_operator_norm':residual,'worst_source_nonvac_transfer_lower':eff})
    # Full two-boson m=3 sector, not the binomial formula implementation.
    m=3;Jb=np.zeros((m+1,m+1),complex)
    for k in range(m):Jb[k,k+1]=Jb[k+1,k]=math.sqrt((k+1)*(m-k))
    U=expm(-1j*T*(np.kron(Jb,G)+np.kron(np.eye(m+1),10*X)))
    fullblock=U[:2,:2]
    vs={j:expm(-1j*(10*X+j*G)*T) for j in range(-m,m+1,2)}
    formula=sum(math.comb(m,k)/2**m*vs[2*k-m] for k in range(m+1))
    full_error=opnorm(fullblock-formula);assert full_error<1e-12
    # Smooth control with rapidly noncommuting source dynamics.
    TT=math.pi;js=np.arange(-4,5,2);initial=np.tile(np.eye(2).reshape(1,4),(len(js),1)).ravel().astype(complex)
    def rhs(t,v):
        vv=v.reshape(len(js),2,2);H=20*X+.7*math.sin(13*t)*Z;gg=math.sin(math.pi*t/TT)**2*G
        return np.array([-1j*(H+j*gg)@u for j,u in zip(js,vv)]).ravel()
    sol=solve_ivp(rhs,(0,TT),initial,method='DOP853',rtol=2e-12,atol=2e-13)
    vv=sol.y[:,-1].reshape(len(js),2,2);AA=sum(math.comb(4,k)/16*vv[k] for k in range(5))
    smooth=opnorm(AA);assert smooth<math.sin(math.pi*delta/2)+1e-9
    # Missing positive gain: arbitrarily fast source dynamics suppress read.
    bad={j:expm(-1j*(100*X+j*Z)*T) for j in (-1,1)}
    negative_transfer=1-opnorm((bad[-1]+bad[1])/2)**2
    assert negative_transfer<1e-3
    # Photon-presence transfer is weaker than a uniform quantum SWAP.
    coherence1000=abs(math.sin((1+delta)*T))**1000
    return {'gain_interval':[.9,1.1],'source_unprepared_operator_tests':rows,
            'direct_m3_sector_vs_binomial_operator_residual':full_error,
            'smooth_noncommuting_source_no_transfer_norm':smooth,
            'nonpositive_gain_fast_source_transfer':negative_transfer,
            'scalar_gain_1000_photon_all_transferred_coherence_factor':coherence1000}
def casimir_checks():
    rows=[]
    for ell in (2,4,8):
        sms,ns,N,Sz,S2,J,K=spin_ops(ell);I=np.eye(2**ell)
        down=sum(adj_diss(K,L) for L in sms)
        up=sum(adj_diss(K,L.conj().T) for L in sms)
        phase=sum(adj_diss(K,math.sqrt(2)*L) for L in ns)
        jensen=2*(ell/2*I-S2+Sz@Sz)@np.linalg.inv(2*J+I)
        uniform=opnorm(J@Sz-Sz@J)
        low=np.flatnonzero(np.diag(N).real<=ell/4)
        diff=(phase-4*N/ell)[np.ix_(low,low)]
        vals={'ell':ell,'cold_loss_K_drift_max_eigenvalue':maxeig(down),
              'raising_K_drift_minus_2ell_max_eigenvalue':maxeig(up-2*ell*I),
              'Jensen_generator_difference_max_eigenvalue':maxeig(phase-jensen),
              'low_density_dephasing_bound_max_eigenvalue':maxeig(diff),
              'J_Sz_commutator':uniform}
        assert max(vals[k] for k in vals if 'eigenvalue' in k)<2e-10
        therm=[]
        nvals=np.diag(N).real
        for p in (.001,.1,.3):
            weights=p**nvals*(1-p)**(ell-nvals)
            exact=float(np.dot(weights,np.diag(K).real));bound=p/(1-2*p)
            assert exact<=bound+1e-10
            therm.append({'p':p,'actual_accessible_spin_charge':exact,'dimension_independent_upper':bound})
        vals['thermal_charge_checks']=therm;rows.append(vals)
    return rows
def controller_counterexample():
    ell=4;p=.01;dR=ell+1;d=2**ell*2*dR;U=np.eye(d)
    def ix(spin,cav,reg):return (spin*2+cav)*dR+reg
    for i in range(ell):
        left=ix(1<<i,0,0);right=ix(0,1,i+1)
        U[left,left]=U[right,right]=0;U[left,right]=U[right,left]=1
    charges=np.array([s.bit_count()+c for s in range(2**ell) for c in range(2) for r in range(dR)])
    nerr=opnorm(U*charges[None,:]-charges[:,None]*U)
    weights=np.zeros(d)
    for s in range(2**ell):weights[ix(s,0,0)]=p**s.bit_count()*(1-p)**(ell-s.bit_count())
    outgoing=(abs(U)**2)@weights
    prob=float(sum(outgoing[ix(s,1,r)] for s in range(2**ell) for r in range(dR)))
    expected=ell*p*(1-p)**(ell-1);false_without_register=p/(1-2*p)
    assert nerr==0 and abs(prob-expected)<1e-14 and prob>false_without_register
    return {'pure_zero_charge_controller_dimension':dR,'total_number_commutator':nerr,
            'false_click':prob,'spin_fugacity_bound_without_controller':false_without_register,
            'conclusion':'number conservation alone does not exclude entropy-assisted false concentration; collective Casimir is essential for the warm-controller theorem'}
def main():
    result={'status':'PASS finite source-operator and full-spin controls',
            'warm_gain':gain_checks(),'Casimir':casimir_checks(),
            'pure_controller_counterexample':controller_counterexample(),
            'scope':'finite algebraic/ODE controls, not independent theorem audit or device qualification',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'warm_gain_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
