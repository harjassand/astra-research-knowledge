"""Frozen-model post-acquisition test of a retained-memory feedback operation."""
import ast,json
from pathlib import Path
import numpy as np
from plant import core_and_shifts

ROOT=Path(__file__).resolve().parent
selected=json.loads((ROOT/'rational_certificate.json').read_text())['selected']
W={ast.literal_eval(k):np.array([[v['decimal'] for v in row] for row in m]) for k,m in selected['W'].items()}
s=selected['s']['decimal'];S=np.array([[1+s,-s],[-s,1+s]])
H,Hz=core_and_shifts();V=H@S
true={z:np.linalg.solve(V,v@S) for z,v in Hz.items()}
c0=np.linalg.solve(S,np.array([1.,0.]));delta=.4;gamma=1-delta

def compile_operation(maps):
    # Controller chooses action equal to its last observed outcome; starts0.
    # A 1 followed by a 0 is success. Every pre-call abort retains memory.
    Q=np.zeros((4,4));A=np.zeros((2,4))
    for state,a in [(0,0),(1,1)]:
        for o in range(2):
            if state==1 and o==0:A[:,2*state:2*state+2]+=maps[a,o]
            else:Q[2*o:2*o+2,2*state:2*state+2]+=maps[a,o]
    entry=np.vstack([np.eye(2),np.zeros((2,2))]);merge=np.hstack([np.eye(2),np.eye(2)])
    resolvent=np.linalg.inv(np.eye(4)-gamma*Q)
    success=gamma*A@resolvent@entry;abort=delta*merge@resolvent@entry
    calls=gamma*np.ones(4)@resolvent@entry
    assert np.max(abs(np.ones(2)@(success+abort)-np.ones(2)))<1e-12
    assert min(success.min(),abort.min())>=-1e-12
    return success,abort,calls

def evaluate(maps):
    success,abort,calls=compile_operation(maps)
    x=success@c0;xx=success@x
    return {'success_probability':float(x.sum()),
            'success_and_future_action1_outcome1':float((maps[1,1]@x).sum()),
            'future_outcome1_conditional_success':float((maps[1,1]@x).sum()/x.sum()),
            'two_invocations_both_success':float(xx.sum()),
            'future_outcome1_conditional_two_success':float((maps[1,1]@xx).sum()/xx.sum()),
            'expected_native_calls_first_invocation':float(calls@c0)}

out={'scope':'Post-acquisition private scorer, not input to the learner',
     'abort_probability_before_each_native_call':delta,
     'learned':evaluate(W),'true':evaluate(true),
     'certified_one_operation_transcript_tv':selected['one_macro_tv']['decimal'],
     'certified_two_operation_joint_transcript_tv':selected['two_macro_tv']['decimal'],
     'conditioning_costs_not_included_in_the_unconditional_bound':True}
(ROOT/'pattern_operation_score.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
