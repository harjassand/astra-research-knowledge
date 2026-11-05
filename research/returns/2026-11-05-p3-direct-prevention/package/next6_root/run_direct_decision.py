"""Oracle-only acquired boundary decision on growing interacting rings.

Simulation of finite local holds, history-varying timing and read corruption;
not a physical experiment. The decision only receives local bits and bounds.
"""
import json,time,platform
from pathlib import Path
from fractions import Fraction
import numpy as np
from decision_certificate import mean_ratio_interval

class LocalHoldSource:
    def __init__(self,N,seed):
        self.N=N; self.rng=np.random.default_rng(seed); self.calls=0; self.dwell=0.
        ii=np.arange(N)
        self.fields=-2.0+0.25*np.sin(.73*ii)
        self.J=.12*np.cos(.41*ii+.3)
    def rate(self,action,indices,left,right):
        slow=.25+.05*(1+np.sin(.37*indices))/2
        fast=.85+.15*(1+np.cos(.19*indices))/2
        all_failed=np.asarray(left)*np.asarray(right)
        if action=='slow_near_failure': return np.where(all_failed,slow,fast)
        if action=='fast_near_failure': return np.where(all_failed,fast,slow)
        if action=='mixed_clock': return .5+.15*(1+np.sin(.23*indices+.2+np.asarray(left)-np.asarray(right)))/2
        raise ValueError(action)
    def boundary_reads(self,action,n,h=.25,omega=.01,read_corruption=.0005):
        indices=self.rng.integers(0,self.N,size=n)
        q=1/(1+np.exp(-(self.fields[indices]+self.J[(indices-1)%self.N]+self.J[indices])))
        r=self.rate(action,indices,1,1)
        # At other neighbor contexts the first two menus exchange their rates;
        # they are not coordinatewise ordered generators. Those contexts are
        # part of the declared source model but need not be experimentally used.
        sign=np.where((np.arange(n)+self.calls)%3==0,1.,-1.)
        t=h*(1+omega*sign)
        recovery=(1-q)*(-np.expm1(-r*t))
        y=self.rng.random(n)<recovery
        y=np.logical_xor(y,self.rng.random(n)<read_corruption)
        self.calls+=n; self.dwell+=float(t.sum())
        return int(y.sum())
    def private_truth_checks(self):
        max_logit=self.fields+np.abs(self.J)+np.abs(np.roll(self.J,1))
        return {'qmax_full_context_bound':float(np.max(1/(1+np.exp(-max_logit)))),
            'Dobrushin_margin':float(1-np.max(np.tanh(abs(self.J)/4)+np.tanh(abs(np.roll(self.J,1))/4))),
            'certificates_used':{'qbar':.25,'alpha':.7,'rmin':.2,'rmax':1.},
            'used_by_decision':False}

def main():
    t0=time.time(); results=[]
    actions=['slow_near_failure','fast_near_failure','mixed_clock']; trials=4096
    # Four sizes, three actions, two tails: total statistical failure <=.02.
    for N in [64,256,1024,4096]:
        src=LocalHoldSource(N,20261105+N)
        obs={u:(src.boundary_reads(u,trials),trials) for u in actions}
        cert=mean_ratio_interval(N,obs,alpha=Fraction(1,1200))
        cert['execution']={'local_calls':src.calls,'actual_hold_exposure_model_units':src.dwell,
            'nominal_hold':.25,'deadline_absolute_tolerance':.0025,
            'timer_contract':'exogenous to current cell path, allowed to depend on prior history',
            'simulated_read_corruption_probability':.0005,'allowed_conditional_bias':.001,
            'whole_source_failed_preparations':0,'virtual_trajectory_updates':0,
            'numerical_energies_or_clocks_acquired_for_decision':False,
            'private_truth_check':src.private_truth_checks()}
        results.append(cert)
        print(json.dumps({'N':N,'chosen':cert['chosen'],'certifies_best':cert['certifies_best'],
              'mean_ratio_lowers':cert['relative_mean_lower_vs_others'],'calls':src.calls}),flush=True)
    report={'status':'simulated local experiments and finite certificate; no hardware',
            'scope':'interacting nonuniform rings; three crossing reciprocal clock menus',
            'statistical_confidence_all_four_runs':.98,
            'coarse_acquisition':'proved finite operation; supplied validated envelopes in this execution',
            'PRNG':'NumPy default_rng with declared seeds, not a certified physical bit source',
            'python':platform.python_version(),'numpy':np.__version__,
            'wall_seconds':time.time()-t0,'results':results}
    Path(__file__).with_name('direct_decision_execution.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__': main()
