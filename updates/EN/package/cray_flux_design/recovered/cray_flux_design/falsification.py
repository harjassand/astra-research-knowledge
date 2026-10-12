"""Independent adversarial fixtures and operational measurement comparisons."""
from pathlib import Path
from fractions import Fraction
import json,time
import numpy as np
from scipy.linalg import solve
from exact_integer_assay import sample_integer
from opaque_assay import generate_instance
from benchmark import stationary,matrices

ROOT=Path(__file__).resolve().parent

def additive_pooled_indistinguishability():
    # Two physically distinct affine-control models. Same visible source flags,
    # same output detector, same reset, same tagged-event records on either axis.
    # Only doubly-activated trajectories reach success vs failure.
    rho=1.;nu=np.array([1.,0,0,0,0]);f=np.array([0.,0,0,1.,0])
    sources=np.array([[1.,0,1.,0,0],[1.,1.,0,0,0]])
    def columns(success):
        target=3 if success else 4
        b1=np.zeros((5,5));b2=b1.copy()
        for src,dst in [(0,1),(2,target)]:b1[dst,src]+=1;b1[src,src]-=1
        for src,dst in [(0,2),(1,target)]:b2[dst,src]+=1;b2[src,src]-=1
        return b1,b2
    def readout(u,success):
        b1,b2=columns(success)
        p=solve(np.eye(5)-u[0]*b1-u[1]*b2,nu)
        return np.r_[sources@p,f@p,u*(sources@p)]
    for s in [0.,.01,1.,100.,1e6]:
        for u in [np.array([s,0.]),np.array([0.,s])]:
            assert np.max(abs(readout(u,True)-readout(u,False)))<1e-12
    joint=[]
    for s in [1.,10.,100.]:
        first=readout(np.repeat(s,2),True)[2];second=readout(np.repeat(s,2),False)[2]
        exact=1-2/(1+s)+1/(1+2*s)
        assert abs(first-exact)<1e-12 and second==0
        joint.append(dict(rate=s,model_A_reward=float(first),model_B_reward=float(second),gap=float(first-second)))
    return dict(joint=joint,statement='All baseline and isolated-control path laws and readouts match, at all isolated strengths. Additive generators alone do not imply a rank-one source interface; the paired-source generator columns have rank two.')

def nonlinear_crosstalk():
    # Three states: independent channels 0->2 and 1->2 at rate 1.
    # A hidden cross term adds 2->0 at rate M*u1*u2. Axes see no cross term.
    return dict(at_unit_rates=[dict(cross_coefficient=m,reward=1/(2+m)) for m in [0,9,100]],
                statement='A generator term u1*u2*C vanishes on every isolated-control experiment, but changes the combined response.')

def strength_independent_count_test():
    inst=generate_instance(160,4,714032,background_rate=1,reset_rate=1);n=200000;out=[];pre=matrices(inst)
    for j,s in enumerate([1,100,10000,100000000]):
        u=[s,0,0,0];start=time.perf_counter();sample,res=sample_integer(inst,u,n,991001+j)
        duration=time.perf_counter()-start;p=stationary(inst,u,pre);r=s*p[0]
        tagged=sample.intervention_counts[0]/n;endpoint=s*sample.source_counts[0]/n
        out.append(dict(rate=s,episodes=n,source_endpoint_hits=sample.source_counts[0],
            tagged_events=sample.intervention_counts[0],true_flux=float(r),
            tagged_flux_estimate=tagged,endpoint_flux_estimate=endpoint,
            naive_endpoint_estimator_variance_per_episode=float(s*r-r*r),
            uniform_tagged_variance_upper=8.,race_integer_max_bits=res['race_integer_max_bits'],
            background_events=sample.background_events,controlled_events=sample.intervention_events,
            seconds=duration))
    assert out[-1]['source_endpoint_hits']==0 and abs(out[-1]['tagged_flux_estimate']-out[-1]['true_flux'])<.01
    return out

def fast_loop_counterexample():
    # Two active sources jump directly to one another at the same rate s, with
    # stopping clock rate rho=1; controlled count mean=s, not bounded by bg+rho.
    return dict(reset_rate=1,mean_control_count_at_rates={str(s):s for s in [1,100,1000000]},
                statement='Dropping ejection permits arbitrarily many controlled events per episode; numerical strength then enters acquisition work.')

if __name__=='__main__':
    result=dict(additive_pooled=additive_pooled_indistinguishability(),cross_talk=nonlinear_crosstalk(),
                measurement_comparison=strength_independent_count_test(),fast_loop=fast_loop_counterexample())
    (ROOT/'falsification_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
