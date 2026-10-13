#!/usr/bin/env python3
"""Autonomous capacitive chemomotor: conditional model, not material prediction.

Requires numpy and scipy. All reported device/catalytic parameters are design
assumptions unless explicitly identified in README.md. No experimental data are
simulated or represented as observations. Positive resistor power is computed
from an autonomous, thermodynamically consistent two-state/two-channel model.
"""
from __future__ import annotations
import argparse, csv, json
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre

E = 1.602176634e-19
KB = 1.380649e-23
EPS0 = 8.8541878128e-12

@dataclass(frozen=True)
class Params:
    name: str = 'high_coupling_hypothesis'
    temperature_K: float = 423.
    sites_per_m2: float = 1e18
    q_over_e: float = .3
    gamma: float = 3.
    affinity_kBT: float = 12.
    k_per_s: float = 50.
    capacitance_F_per_m2: float = 1e18*.3*E/2.
    load_S_per_m2: float = 5.
    leakage_S_per_m2: float = 0.

    def validate(self):
        if min(self.temperature_K,self.sites_per_m2,self.q_over_e,self.k_per_s,
               self.capacitance_F_per_m2,self.load_S_per_m2) <= 0:
            raise ValueError('Temperature, density, charge, rate, C and load must be positive.')
        if self.leakage_S_per_m2 < 0:
            raise ValueError('Leakage cannot be negative.')

    @property
    def q(self): return self.q_over_e*E
    @property
    def kbt(self): return KB*self.temperature_K
    @property
    def theta_F(self): return (1-self.gamma)/2
    @property
    def theta_P(self): return (1+self.gamma)/2
    @property
    def lam(self): return 2*self.k_per_s*(1+np.exp(-self.affinity_kBT/2))
    @property
    def G(self): return self.load_S_per_m2+self.leakage_S_per_m2
    @property
    def Cr(self):
        return self.sites_per_m2*self.q**2/(4*self.kbt)*(1-self.gamma*np.tanh(self.affinity_kBT/4))


def rates(v, p: Params):
    x=p.q*np.asarray(v)/p.kbt
    k=p.k_per_s; r=np.exp(-p.affinity_kBT/2)
    return (k*np.exp(p.theta_F*x), k*r*np.exp((p.theta_F-1)*x),
            k*np.exp((p.theta_P-1)*x), k*r*np.exp(p.theta_P*x))


def rhs(t, y, p):
    occ,v=y
    af,ar,bf,br=rates(v,p)
    d=(af+br)*(1-occ)-(ar+bf)*occ
    return [d,(-p.G*v-p.sites_per_m2*p.q*d)/p.capacitance_F_per_m2]


def metrics(p, rtol=1e-8, method='DOP853', seed_V=1e-4):
    p.validate()
    # Scale duration inversely with rate; high-rate run is an explicitly
    # conditional time-rescaling, not an independent material calculation.
    end=3.*50/p.k_per_s
    def upward(t,y): return y[1]
    upward.direction=1
    # Explicit adaptive solvers can try and reject remote overflowing stages.
    # Suppress only these floating warnings; require success and validate all
    # accepted states below. Physical rates are not clipped or regularized.
    with np.errstate(over="ignore",invalid="ignore"):
        sol=solve_ivp(lambda t,y:rhs(t,y,p),(0,end),[.5,seed_V],method=method,
                      rtol=rtol,atol=rtol*1e-2,dense_output=True,events=upward,
                      max_step=.001*50/p.k_per_s)

    if not sol.success: raise RuntimeError(sol.message)
    if not np.all(np.isfinite(sol.y)) or np.min(sol.y[0]) < -1e-10 or np.max(sol.y[0]) > 1+1e-10:
        raise RuntimeError('Invalid accepted trajectory.')
    crossings=sol.t_events[0]
    late=crossings[crossings>.5*end]
    tail=np.linspace(.8*end,end,1001)
    amp=float(np.max(np.abs(sol.sol(tail)[1])))
    oscillatory=len(late)>=4 and amp>1e-3
    if oscillatory:
        t0=late[-min(11,len(late))]; t1=late[-1]
        frequency=float(1/np.diff(late[-min(11,len(late)):]).mean())
    else:
        t0=.8*end; t1=end; frequency=None
    # Integrate on adaptive solver intervals: uniform sampling misses narrow
    # power/entropy spikes in the high-coupling relaxation oscillation.
    knots=np.r_[t0,sol.t[(sol.t>t0)&(sol.t<t1)],t1]
    z,w=roots_legendre(12)
    half=np.diff(knots)/2
    mid=(knots[:-1]+knots[1:])/2
    tq=(mid[:,None]+half[:,None]*z).ravel()
    weights=(half[:,None]*np.broadcast_to(w,(len(half),len(w)))).ravel()
    t=np.r_[t0,tq,t1]
    weights=np.r_[0.,weights,0.]
    occ,v=sol.sol(t)
    af,ar,bf,br=rates(v,p)
    jf=af*(1-occ)-ar*occ
    jp=bf*occ-br*(1-occ)
    d=jf-jp
    pc=p.sites_per_m2*(p.affinity_kBT*p.kbt/2)*(jf+jp)
    pl=p.load_S_per_m2*v*v
    leak=p.leakage_S_per_m2*v*v
    # Each term (a-b) log(a/b) is nonnegative.
    ep=p.sites_per_m2*p.kbt*(jf*np.log(af*(1-occ)/(ar*occ))+
                                 jp*np.log(bf*occ/(br*(1-occ))))
    entropy=-p.sites_per_m2*KB*(occ*np.log(occ)+(1-occ)*np.log1p(-occ))
    U=.5*p.capacitance_F_per_m2*v*v
    dt=t1-t0
    avg=lambda a:float(np.dot(weights,a)/dt)
    # Exact integrated identity: Pchem-Pload-Pleak-Tsigma = (Delta U - T Delta S)/dt.
    boundary=(U[-1]-U[0]-p.temperature_K*(entropy[-1]-entropy[0]))/dt
    residual=avg(pc-pl-leak-ep)-boundary
    D=p.capacitance_F_per_m2*p.lam+p.G+p.Cr*p.lam
    roots=np.roots([p.capacitance_F_per_m2,D,p.G*p.lam])
    qcrit=np.sqrt(4*p.kbt*(p.capacitance_F_per_m2+p.G/p.lam)/
                (p.sites_per_m2*(p.gamma*np.tanh(p.affinity_kBT/4)-1))) \
                if p.gamma*np.tanh(p.affinity_kBT/4)>1 else np.inf
    result={
        'parameters':asdict(p), 'oscillatory':bool(oscillatory),
        'frequency_Hz':frequency, 'voltage_abs_peak_V':float(np.max(np.abs(v))),
        'voltage_rms_V':float(np.sqrt(avg(v*v))),
        'occupancy_min':float(occ.min()),'occupancy_max':float(occ.max()),
        'Pload_W_per_m2':avg(pl),'Pchemical_W_per_m2':avg(pc),
        'Pleak_W_per_m2':avg(leak),'T_entropy_production_W_per_m2':avg(ep),
        'chemical_to_load_efficiency':avg(pl)/avg(pc) if avg(pc)>1e-12 else None,
        'energy_balance_residual_W_per_m2':float(residual),
        'min_T_entropy_production_W_per_m2':float(ep.min()),
        'lambda_per_s':p.lam,'reaction_capacitance_F_per_m2':p.Cr,
        'full_occupancy_open_circuit_swing_V':p.sites_per_m2*p.q/p.capacitance_F_per_m2,
        'linear_pole_real_per_s':[float(a.real) for a in roots],
        'linear_pole_imag_per_s':[float(a.imag) for a in roots],
        'critical_load_plus_leak_S_per_m2':float(-p.lam*(p.capacitance_F_per_m2+p.Cr)),
        'critical_q_over_e_fixed_gamma':float(qcrit/E) if np.isfinite(qcrit) else None,
        'single_cycle_work_ceiling_fraction':float(p.q*(v.max()-v.min())/(p.affinity_kBT*p.kbt)) if p.affinity_kBT>0 else None,
    }
    return result, (t,occ,v,pl,pc,ep)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    nominal=Params()
    c70=EPS0*20/70e-9
    cases=[nominal,
           replace(nominal,name='same_model_100x_rates_NOT_material_forecast',k_per_s=5000,load_S_per_m2=500),
           Params(name='small_charge_hypothesis',sites_per_m2=1e19,q_over_e=.003,gamma=50,
                  capacitance_F_per_m2=c70,load_S_per_m2=.1),
           Params(name='hydrogen_charge_magnitude_control',sites_per_m2=1e19,q_over_e=.0019,gamma=3,
                  capacitance_F_per_m2=c70,load_S_per_m2=.1),
           replace(nominal,name='equilibrium_control',affinity_kBT=0),
           replace(nominal,name='no_barrier_overshoot_control',gamma=1),
           replace(nominal,name='heavy_load_control',load_S_per_m2=nominal.lam*(-nominal.Cr-nominal.capacitance_F_per_m2)*1.1),
           Params(name='REJECTED_as_material_forecast_large_Voc',sites_per_m2=1e19,q_over_e=.02,gamma=3,
                  capacitance_F_per_m2=c70,load_S_per_m2=.5)]
    reports=[]; checks={}
    for case in cases:
        print("Solving",case.name,flush=True)
        result,trace=metrics(case)
        print("Finished",case.name,flush=True)
        reports.append(result)
        if case.name in ['high_coupling_hypothesis','small_charge_hypothesis']:
            np.savetxt(args.out/(case.name+'_trace.csv'),np.column_stack(trace),delimiter=',',
                       header='t_s,occupancy,V_V,Pload_W_m2,Pchem_W_m2,Tentropy_W_m2',comments='')
        checks[case.name+'_entropy_nonnegative']=result['min_T_entropy_production_W_per_m2']>=-1e-10
        checks[case.name+'_balance']=abs(result['energy_balance_residual_W_per_m2'])<1e-6*max(1.,abs(result['Pchemical_W_per_m2']))
    # Exact detailed-balance ratios evaluated over a modest voltage grid.
    p=nominal
    v=np.linspace(-.8,.8,401);af,ar,bf,br=rates(v,p)
    checks['local_detailed_balance_F']=bool(np.max(np.abs(np.log(af/ar)-(p.affinity_kBT/2+p.q*v/p.kbt)))<1e-12)
    checks['local_detailed_balance_P']=bool(np.max(np.abs(np.log(bf/br)-(p.affinity_kBT/2-p.q*v/p.kbt)))<1e-12)
    checks['cycle_affinity_voltage_independent']=bool(np.max(np.abs(np.log(af*bf/(ar*br))-p.affinity_kBT))<1e-12)
    # Numerical derivative check on the analytic response coefficient.
    h=1e-6
    def ss(v):
        af,ar,bf,br=rates(v,p);return (af+br)/(af+ar+bf+br)
    cr_fd=p.sites_per_m2*p.q*(ss(h)-ss(-h))/(2*h)
    checks['reaction_capacitance_derivative']=bool(abs(cr_fd-p.Cr)<1e-7*abs(p.Cr))
    # Tighter-tolerance and different-seed convergence check; SAME DOP853 method.
    other,_=metrics(nominal,rtol=2e-10,method='DOP853',seed_V=1e-6)
    base=reports[0]
    convergence_comparison={key:abs(base[key]-other[key])/max(abs(base[key]),1e-15)
                       for key in ['frequency_Hz','Pload_W_per_m2','Pchemical_W_per_m2']}
    checks['tolerance_and_seed_agreement']=max(convergence_comparison.values())<1e-6
    for name in ['equilibrium_control','no_barrier_overshoot_control','heavy_load_control','hydrogen_charge_magnitude_control']:
        checks[name+'_no_oscillation']=not next(x for x in reports if x['parameters']['name']==name)['oscillatory']
    checks['nominal_oscillates']=base['oscillatory']
    # Expected time-rescaling is a property of this assumed model, not a discovery.
    fast=reports[1]
    checks['conditional_rate_scaling']=abs(fast['Pload_W_per_m2']/base['Pload_W_per_m2']-100)<1e-4
    all_pass=all(checks.values())
    payload={'status':'conditional theoretical model; no measured candidate catalyst',
             'cases':reports,'checks':checks,'all_checks_pass':all_pass,
             'tolerance_and_seed_relative_differences':convergence_comparison}
    (args.out/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
    for x in reports:
        print(x['parameters']['name'], 'f=',x['frequency_Hz'],'P=',x['Pload_W_per_m2'],
              'eta=',x['chemical_to_load_efficiency'],'Vpeak=',x['voltage_abs_peak_V'],
              'balance=',x['energy_balance_residual_W_per_m2'])
    print('CHECKS:',sum(bool(x) for x in checks.values()),'/',len(checks))
    if not all_pass:
        raise AssertionError({k:v for k,v in checks.items() if not v})

if __name__=='__main__': main()
