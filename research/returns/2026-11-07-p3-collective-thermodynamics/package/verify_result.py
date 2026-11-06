"""Focused independent audits of normalization, records and certificates.

Exact-rational checks are labeled separately from binary64 diagnostics.
This script reads only files in this new result package.
"""
import json,time
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy.linalg import expm
from scipy.special import logsumexp
from threadpoolctl import threadpool_limits
from polynomial_tools import indices,derivative,decode_polynomial,evaluate,combine
from calibrated_source import pauli_terms,heisenberg_commutator,expectation_polynomial
from certified_thermodynamics import StateOracle,point_value,dot
from schur_diagnostic import full_matrix,schur_spectrum

ROOT=Path(__file__).resolve().parent


def main():
    start=time.perf_counter(); checks={}
    probes=[((1,1),(0,1)),((0,1),(1,0)),((1,0),(1,1))]
    count=0
    for a in indices(4):
        H=pauli_terms(5,{a:Q(1)})
        for j,(tag,measurement) in enumerate(probes):
            comm,_=heisenberg_commutator(H,{measurement:Q(1)})
            observed=expectation_polynomial(comm,tag,5)
            wanted={b:2*c for b,c in derivative({a:Q(1)},j).items()}
            assert observed==wanted,(a,j,observed,wanted)
            count+=1
    checks['exact_tagged_gradient_monomial_checks']=count
    record=json.loads((ROOT/'RECORDS.json').read_text())
    audit=json.loads((ROOT/'AUDIT_TRUTH.json').read_text())
    truth=decode_polynomial(audit['polynomial']); N=record['contract']['source_size']
    H=full_matrix(N,truth); t=float(Q(record['times'][-1])); U=expm(-1j*t*H)
    I=np.eye(2); X=np.array([[0,1],[1,0]],dtype=complex)
    Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1]); sigmas=[X,Y,Z]
    nodes=list(map(Q,record['bath_nodes'])); grid=[(a,b,c) for a in nodes for b in nodes for c in nodes]
    maxerror=0.0
    for j in range(3):
        for index in [0,17,63]:
            r=grid[index]; bath=(I+sum(float(v)*s for v,s in zip(r,sigmas)))/2
            tag=(I+sigmas[(j+1)%3])/2; measure=sigmas[(j+2)%3]
            rho=np.array([[1.0+0j]]); O=np.array([[1.0+0j]])
            # Bit 0 is the tagged spin, hence the final Kronecker factor.
            for site in reversed(range(N)):
                rho=np.kron(rho,tag if site==0 else bath)
                O=np.kron(O,measure if site==0 else I)
            value=float(np.trace(U@rho@U.conj().T@O).real)
            stored=float(Q(record['records'][j*len(grid)+index][-1]))
            maxerror=max(maxerror,abs(value-stored))
    assert maxerror<float(Q(record['record_radius']))
    checks['binary64_dense_source_audit_records']=9
    checks['binary64_dense_source_max_deviation']=maxerror
    acquired=json.loads((ROOT/'ACQUISITION_CERTIFICATE.json').read_text())
    base=decode_polynomial(acquired['learned_polynomial']); nu=Q(acquired['coefficient_l1_error'])
    controls=[{(1,0,0):Q(1)},{(0,0,1):Q(1)}]
    vertices=[(Q(g),Q(h,5)) for g in [0,Q(3,2)] for h in [-1,1]]
    recertified={}
    for name in ['GROUND','FINITE_TEMPERATURE']:
        d=json.loads((ROOT/('DECISION_'+name+'.json')).read_text())
        beta=None if d['beta'] is None else Q(d['beta']); u=tuple(map(Q,d['control']))
        lam=list(map(Q,d['simplex_weights'])); w=list(map(Q,d['dual_weights']))
        points=[tuple(map(Q,r)) for r in d['state_points']]
        assert sum(lam)==sum(w)==1 and min(lam+w)>=0
        assert all(dot(r,r)<=1 for r in points)
        assert u==tuple(sum(a*v[j] for a,v in zip(lam,vertices)) for j in range(2))
        energies=[point_value(base,r,beta)[1] for r in points]
        upper=max(sum(ww*(e-v[0]*r[0]-v[1]*r[2]+v[0]/2) for ww,e,r in zip(w,energies,points))
                  for v in vertices)+nu
        assert upper==Q(d['objective_upper'])
        state=StateOracle(combine(base,controls,u),beta).minimize(Q(1,400),initial_points=points)
        lower=state['lower']+u[0]/2-nu
        assert lower==Q(d['objective_lower'])
        assert upper-lower==Q(d['regret_bound'])<=Q(1,100)
        recertified[name]={'regret':float(upper-lower),'rational_primal_dual_checks':True,
                          'global_state_bound_replayed':True}
    checks['decision_certificates']=recertified
    # The analytic audit is not an input to either optimizer.
    exact_optimum=Q(-155,216)
    d=json.loads((ROOT/'DECISION_GROUND.json').read_text())
    assert Q(d['objective_lower'])<=exact_optimum<=Q(d['objective_upper'])
    checks['ground_analytic_optimum_in_certified_interval']=True
    finite=json.loads((ROOT/'FINITE_N_CERTIFICATE.json').read_text())
    g=Q(finite['Gamma']); h=Q(finite['h'])
    p={(0,0,4):Q(-1),(1,0,0):-g,(0,0,1):-h}
    vals,mults,dims=schur_spectrum(64,p,4)
    intervals=[tuple(map(Q,iv)) for sector in finite['sectors'] for iv in sector['energy_density_intervals']]
    assert len(intervals)==len(vals)==1089
    assert all(float(a)-1e-12<=v/64<=float(b)+1e-12 for (a,b),v in zip(intervals,vals))
    fv=float(-logsumexp(-2*vals+np.log(np.array(mults,dtype=float)))/128)
    flo,fhi=map(Q,finite['free_energy_interval'])
    assert float(flo)<=fv<=float(fhi)
    checks['binary64_finite_N_all_sector_eigenvalues_checked']=1089
    checks['binary64_finite_N_free_energy']=fv
    checks['seconds']=time.perf_counter()-start
    (ROOT/'VALIDATION.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=1): main()
