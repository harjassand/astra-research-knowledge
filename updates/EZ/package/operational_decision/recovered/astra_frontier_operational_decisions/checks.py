"""Independent-coordinate falsification tests; no floating diagnostic is a proof.
Rebuild all exact certificates with --verify-witnesses. The forward solver uses
full Kronecker matrices, whereas the certificate compiler uses occupation pairs.
"""
from __future__ import annotations
import argparse,itertools,json,time,math,tempfile
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import solve,expm,eigh
from finite_certificates import matrices,pairs,ADEN,PARS,run_case
from decision_certificate import produce,polynomial
from explore_device import getA,Ns,S,Id


def main(folder='results',verify_witnesses=False):
    start=time.perf_counter(); folder=Path(folder); rng=np.random.default_rng(271013)
    records=json.loads((folder/'all_cases.json').read_text())
    large_indices=[a+16*b for a,b in pairs]
    reports={'seed':271013,'certificate_checks':0,'generator_comparisons':0,
             'stationary_polynomial_checks':0,'reflection_checks':0,
             'probe_checks':0,'random_POVM_checks':0,'maximum_forward_residual':0.,
             'maximum_polynomial_error_ratio':0.,'maximum_generator_error':0.}
    for rec in records:
        kind,k=rec['kind'],rec['kappa'];phi=math.pi if kind=='bad' else math.pi/3
        ar,ai,terms=matrices(kind,k)
        full,rhs=getA(phi,k,d=.01,pump=.4)
        small=np.asarray(ar,float)/ADEN+1j*np.asarray(ai,float)/ADEN
        err=float(np.max(np.abs(full[np.ix_(large_indices,large_indices)]-small)))
        reports['maximum_generator_error']=max(reports['maximum_generator_error'],err)
        assert err<5e-14
        reports['generator_comparisons']+=1
        pp=polynomial(rec)
        points=[np.zeros(6)]+[np.array(signs)*np.array(list(map(float,PARS))) for signs in itertools.product([-1,1],repeat=6)]
        points += [rng.uniform(-1,1,6)*np.array(list(map(float,PARS))) for _ in range(12)]
        for idx,ds in enumerate(points):
            xi=np.array([4,3,1,2])+ds[:4]
            aa,bb=getA(phi+ds[4],k+ds[5],d=.01,pump=.4,coeff=xi)
            xx=solve(aa,bb);rho=xx.reshape((16,16),order='F')
            true=float(((k+ds[5])*np.trace(Ns[3]@rho)).real)
            pred=sum(float(c)*np.prod([v**p for v,p in zip(ds,a)]) for a,c in pp.items())
            discrepancy=abs(true-pred); bound=float(F(rec['error']))
            assert discrepancy<=bound+2e-12,(kind,k,ds,discrepancy,bound)
            reports['maximum_polynomial_error_ratio']=max(reports['maximum_polynomial_error_ratio'],discrepancy/bound)
            reports['maximum_forward_residual']=max(reports['maximum_forward_residual'],float(np.linalg.norm(aa@xx-bb)))
            assert np.min(np.linalg.eigvalsh((rho+rho.conj().T)/2))>-1e-11
            reports['stationary_polynomial_checks']+=1
            if idx<5:
                aa2,bb2=getA(-phi-ds[4],k+ds[5],d=.01,pump=.4,coeff=xi)
                rr=solve(aa2,bb2).reshape((16,16),order='F')
                reflected=float(((k+ds[5])*np.trace(Ns[3]@rr)).real)
                assert abs(reflected-true)<2e-12
                reports['reflection_checks']+=1
        if verify_witnesses:
            new=run_case(kind,k,rec['degree'],witness=folder/f'{kind}_{k}_witness.npz')
            for field in rec:
                if field=='seconds':continue
                assert rec[field]==new[field],(kind,k,field)
            reports['certificate_checks']+=1
    # A corrupted proposed inverse must fail the exact inverse-residual certificate.
    if verify_witnesses:
        dat=np.load(folder/'good_4_witness.npz',allow_pickle=False)
        altered={k:dat[k].copy() for k in dat.files};altered['Rr'][:]=0;altered['Ri'][:]=0
        with tempfile.TemporaryDirectory() as tmp:
            bad=Path(tmp,'corrupted.npz');np.savez(bad,**altered)
            try:run_case('good',4,6,witness=bad)
            except ValueError as e:
                assert 'Neumann certificate failed' in str(e)
                reports['corrupted_inverse_rejected']=True
            else:raise AssertionError('corrupted inverse was accepted')
    # Nominal density is not restricted to a single excitation.
    aa,bb=getA(math.pi/3,4,d=.01,pump=.4)
    rho=solve(aa,bb).reshape((16,16),order='F')
    populations=[sum(float(rho[a,a].real) for a in range(16) if a.bit_count()==n) for n in range(5)]
    currents=[4*sum(float(rho[a,a].real) for a in range(16) if a.bit_count()==n and a&1) for n in range(5)]
    aa0,bb0=getA(math.pi/3,4,d=.01,pump=.4,coeff=[0,0,0,0])
    rho0=solve(aa0,bb0).reshape((16,16),order='F')
    reports['finite_density_diagnostic']={'probability_by_number':populations,'current_by_number':currents,
        'full_interacting_current':sum(currents),'zero_diagonal_interaction_current':float((4*np.trace(Ns[3]@rho0)).real)}
    # Isolated two-level physical Lindblad evolution and loss-compiled POVM.
    X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);I=np.eye(2)
    def diss(L):
        P=L.conj().T@L
        return np.kron(L.conj(),L)-.5*np.kron(I,P)-.5*np.kron(P.T,I)
    nvec=[np.sin(2*np.pi*j/3)*X+np.cos(2*np.pi*j/3)*Y for j in range(3)]
    effects=[(I-n)/3 for n in nvec]
    assert np.max(np.abs(sum(effects)-I))<1e-14
    assert min(np.linalg.eigvalsh(E)[0] for E in effects)>-1e-14
    for d in [.005,.01,.03,.2]:
        for T in [.2,np.pi/4,1.1]:
            om=np.sqrt(4-d*d/4);s=2/om*np.exp(-d*T/2)*np.sin(om*T)
            z=np.exp(-d*T/2)*(np.cos(om*T)+d/(2*om)*np.sin(om*T))
            for j in range(3):
                theta=2*np.pi*j/3;H=-np.cos(theta)*X+np.sin(theta)*Y
                L=-1j*(np.kron(I,H)-np.kron(H.T,I))+d/2*diss(Z)
                rr=(expm(T*L)@np.array([1,0,0,0],complex)).reshape((2,2),order='F')
                exact=(I+s*nvec[j]+z*Z)/2
                assert np.max(np.abs(rr-exact))<1e-13
                assert abs(np.trace(effects[j]@rr).real-(1-s)/3)<1e-13
                reports['probe_checks']+=1
    T=np.pi/4;d=.01;om=np.sqrt(4-d*d/4)
    s=2/om*np.exp(-d*T/2)*np.sin(om*T);z=np.exp(-d*T/2)*(np.cos(om*T)+d/(2*om)*np.sin(om*T))
    states=[(I+s*n+z*Z)/2 for n in nvec]
    anti_risk=sum(np.trace(E@r).real for E,r in zip(effects,states))/3
    for _ in range(120):
        Q=[]
        for i in range(3):
            A=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));Q.append(A@A.conj().T)
        vals,vec=eigh(sum(Q));R=(vec*(1/np.sqrt(vals)))@vec.conj().T
        es=[R@q@R for q in Q]
        risk=sum(np.trace(e@r).real for e,r in zip(es,states))/3
        assert risk>=anti_risk-1e-13
        reports['random_POVM_checks']+=1
    # Explicit phase-independent isometry for the 3-outcome POVM.
    rows=[]
    for E in effects:
        vals,V=eigh(E);rows.append(np.sqrt(2/3)*V[:,-1].conj())
    W=np.vstack(rows); assert np.linalg.norm(W.conj().T@W-I)<1e-13
    for a in range(3):assert np.linalg.norm(np.outer(rows[a].conj(),rows[a])-effects[a])<1e-13
    reports['POVM_isometry_dimension']=[3,2]
    # Direct full-device difference norm for all pairs, unknown common nuisance cancels.
    fullHs=[]
    # Four neutral interaction terms have no influence on this exact difference.
    for j in range(3):
        h=S[1].conj().T@S[3];theta=2*np.pi*j/3
        fullHs.append(-np.exp(1j*theta)*h-np.exp(-1j*theta)*h.conj().T)
    for i in range(3):
        for j in range(i):assert abs(np.linalg.norm(fullHs[i]-fullHs[j],2)-np.sqrt(3))<1e-13
    reports['full_Hamiltonian_difference_checks']=3
    # Exact decision set: minimal three-model conflict, any two share a good action.
    sets=[set(range(3))-{j} for j in range(3)]
    assert not set.intersection(*sets)
    for j in range(3):assert set.intersection(*(sets[k] for k in range(3) if k!=j))=={j}
    reports['minimal_conflict_exact_checks']=4
    reports['seconds']=time.perf_counter()-start
    (folder/'checks.json').write_text(json.dumps(reports,indent=2))
    print(json.dumps(reports,indent=2))
    return reports

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',default='results');p.add_argument('--verify-witnesses',action='store_true');a=p.parse_args()
    main(a.folder,a.verify_witnesses)
