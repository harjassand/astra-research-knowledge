"""Independent audit and stronger residence-time comparators.

Does not modify the root model. All rates remain illustrative. Static affinity
retuning and exponential-clock calculations are conditional model comparisons,
not claims of chemically independent tunability or an earned molecular timer.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parent.parent/'stage1_root'/'assembly_gate.py'
spec=importlib.util.spec_from_file_location('root_assembly_gate_audit',ROOT)
model=importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def static_retuned(beta,guide=1.2,horizon=15.):
    # All three bound-state energies change together. Forward/reverse guide
    # binding has the same equilibrium constant exp(beta), closing every cycle.
    E=np.array([0.,-3.,-4.,-12.,-beta,-3-beta,-4-beta])
    edges=[(0,1,1.),(0,2,3.),(1,3,2.),(1,2,.02),
           (4,5,1.),(4,6,.006),(5,6,.02)]
    def rhs(t,y):
        z=np.maximum(y,0.);d=np.zeros(9)
        for i,j,k in edges:
            v=k*z[i]-k*np.exp(E[j]-E[i])*z[j]
            d[i]-=v;d[j]+=v
        for a,b in [(0,4),(1,5),(2,6)]:
            v=50*z[a]*z[7]-50*np.exp(-beta)*z[b]
            d[a]-=v;d[b]+=v;d[7]-=v
        d[8]=z[3]
        return d
    y=np.zeros(9);y[0]=1.;y[7]=guide
    sol=solve_ivp(rhs,(0,horizon),y,method='LSODA',rtol=2e-8,atol=2e-10)
    assert sol.success
    y=sol.y[:,-1]
    assert abs(y[:7].sum()-1)<1e-7
    assert abs(y[[4,5,6,7]].sum()-guide)<1e-7
    return dict(binding_energy=-float(beta),guide=guide,
                native_time=float(y[8]),native_fraction=float(y[3]),
                unbinding_rate=float(50*np.exp(-beta)))


def reversible_audit():
    rng=np.random.default_rng(6041)
    RNA=np.r_[np.ones(7),np.zeros(5)]
    G=np.zeros(12);G[[4,5,6,7,9]]=1
    A=np.zeros(12);A[[8,9]]=1
    conservation=0.;max_fdot=-np.inf
    for _ in range(100):
        y=rng.uniform(.02,2,size=12)
        affinity=rng.uniform(8,25)
        d=model.rhs(0,y,selective=10**rng.uniform(-3,0),
                    release=10**rng.uniform(-2,2),affinity=affinity)
        conservation=max(conservation,*np.abs(np.array([RNA@d,G@d,A@d])))
        Echem=np.r_[model.E,0.,0.,-affinity]
        mu=np.log(y[:10])+Echem
        max_fdot=max(max_fdot,float(mu@d[:10]))
    eq=[]
    for shift in [0.,9.]:
        en=model.E.copy();en[model.N]+=shift
        y=np.zeros(12);r,g,a=1e-8,1e-6,1e-4
        y[:4]=r*np.exp(-en[:4]);y[4:7]=r*g*np.exp(-en[4:7])
        y[model.G]=g;y[model.A]=a;y[model.W]=np.exp(22)*g*a
        residual=np.max(np.abs(model.rhs(0,y,native_energy_shift=shift)[:10]))
        eq.append(dict(native_energy_shift=shift,residual=float(residual)))
    assert conservation<1e-9 and max_fdot<0
    assert max(x['residual'] for x in eq)<1e-15
    return dict(conservation_max_abs=float(conservation),
                largest_free_energy_derivative_in_random_closed_states=max_fdot,
                equilibrium_residuals=eq,
                scope='Counters omitted from chemical free energy. Pulses are external chemical additions; reset=0 for detailed balance.')


def early_antidote(pulse):
    def objective(logr):
        return -model.simulate(guide=1.2,pulse=pulse,release=np.exp(logr))[0]['integrated_native_time']
    grid=np.linspace(-8,6,61)
    i=int(np.argmin([objective(v) for v in grid]))
    o=minimize_scalar(objective,bounds=(grid[max(0,i-1)],grid[min(len(grid)-1,i+1)]),method='bounded')
    release=float(np.exp(o.x))
    r=model.simulate(guide=1.2,pulse=pulse,release=release)[0]
    return dict(pulse_time=pulse,release_second_order_rate=release,
                native_time=r['integrated_native_time'],native_fraction=r['native_fraction'],
                residue_bound=r['residual_bound_gate'],
                total_first_exit_hazard_bounds=[50*np.exp(-8)+1.2*release,
                                               50*np.exp(-8)+2.4*release],
                scope='Exact finite root model. After antidote addition A+W=2.4 and W<=1.2, so A is in [1.2,2.4]. Individual displacement hazards are bounded, broad, time-dependent; not claimed to be an exact constant-rate exponential.')


def random_global_pulse(order=80):
    H=15.;nodes,weights=leggauss(order)
    ts=(nodes+1)*H/2; ws=weights*H/2
    services=np.array([model.simulate(guide=1.2,pulse=float(t))[0]['integrated_native_time'] for t in ts])
    no_pulse=model.simulate(guide=1.2)[0]['integrated_native_time']
    def expectation(rate):
        return float(np.sum(ws*rate*np.exp(-rate*ts)*services)+np.exp(-rate*H)*no_pulse)
    o=minimize_scalar(lambda lograte:-expectation(np.exp(lograte)),bounds=(-6,4),method='bounded')
    rate=float(np.exp(o.x))
    return dict(exponential_rate=rate,mean_pulse_time=1/rate,
                expected_native_time=expectation(rate),quadrature_order=order,
                probability_no_pulse_before_horizon=float(np.exp(-rate*H)),
                scope='A SINGLE bulk antidote pulse at a random exponential time. This proves robustness to broad timer jitter; it is not independent molecule-by-molecule release and does not supply an autonomous chemical timer.')


def bound_resolvent():
    E=np.array([-8.,-11.,-12.]);Q=np.zeros((3,3))
    for i,j,k in [(0,1,1.),(0,2,.006),(1,2,.02)]:
        rev=k*np.exp(E[j]-E[i]);Q[i,j]+=k;Q[j,i]+=rev
        Q[i,i]-=k;Q[j,j]-=rev
    rows=[]
    for rate in [.1,.2,.5,1.,2.]:
        p=np.array([1.,0.,0.])@(rate*np.linalg.inv(rate*np.eye(3)-Q))
        assert abs(p.sum()-1)<1e-12 and np.min(p)>0
        rows.append(dict(rate=rate,release_state_probabilities=p.tolist()))
    return dict(bound_generator=Q.tolist(),rates=rows,
                identity='p_release=e_UG^T lambda(lambda I-Q_bound)^(-1)',
                scope='Exact reversible bound-state chain observed at an independent exponential clock. Assumes already captured RNA and a one-shot removal clock; their preparation/chemistry are NOT earned by this reduced identity. The finite early-antidote experiment separately tests acquisition and depletion.')


def main():
    base=model.simulate()[0]
    unstable=model.simulate(native_energy_shift=9.)[0]
    # Affinity retuning holds the illustrative selectivity/on-rate fixed. This
    # conditional comparator exposes a missing comparison, not molecular access.
    opt=minimize_scalar(lambda beta:-static_retuned(beta)['native_time'],bounds=(0.,8.),method='bounded')
    result=dict(root_source_sha256=hashlib.sha256(ROOT.read_bytes()).hexdigest(),
                balance=reversible_audit(),
                unassisted=dict(native_time=base['integrated_native_time'],native_fraction=base['native_fraction']),
                matched_unstable_unassisted=dict(native_time=unstable['integrated_native_time'],native_fraction=unstable['native_fraction']),
                static_retuned_beta2=static_retuned(2.),
                optimized_static_retuned=static_retuned(float(opt.x)),
                early_antidote=[early_antidote(0.),early_antidote(.1)],
                random_global_pulse=random_global_pulse(),
                exponential_resolvent=bound_resolvent())
    path=Path(__file__).with_name('assembly_gate_audit_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
