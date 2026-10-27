"""Post-acquisition private scoring only: full-transcript DP, not moments."""
import ast
import json
import math
from pathlib import Path
import numpy as np
from plant import core_and_shifts

ROOT=Path(__file__).resolve().parent
cert=json.loads((ROOT/'rational_certificate.json').read_text())['selected']
W={ast.literal_eval(z):np.array([[x['decimal'] for x in row] for row in m])
   for z,m in cert['W'].items()}
s=cert['s']['decimal']; S=np.array([[1+s,-s],[-s,1+s]])
H,Hz=core_and_shifts(); V=H@S
Wtrue={z:np.linalg.solve(V,v@S) for z,v in Hz.items()}
c0=np.linalg.solve(S,np.array([1.,0.]))

def policy_tv(horizon,delta=0.,macros=1):
    """Supremum over deterministic feedback policies; total native cap H.

    At the cap both sources output a public CAP symbol. Disjoint full
    outcome/abort transcript branches add in L1. A maximizing action can be
    selected separately at every observed prefix, so this optimizes all
    deterministic feedback trees. Convexity covers randomized policies.
    """
    calls=[0]
    def visit(x,y,h,m):
        calls[0]+=1
        if h==0 or m==0: return abs(x.sum()-y.sum())
        terminate=delta*visit(x,y,h,m-1) if delta else 0.
        cont=max(sum(visit(Wtrue[a,o]@x,W[a,o]@y,h-1,m) for o in range(2))
                 for a in range(2))
        return terminate+(1-delta)*cont
    return visit(c0,c0,horizon,macros)/2,calls[0]

def negative_binomial_tail(h,m,delta):
    gamma=1-delta
    return max(0.,1-sum(math.comb(n+m-1,m-1)*delta**m*gamma**n for n in range(h+1)))

out={'actual_one_step_tv':max(0.5*sum(np.abs(Wtrue[a,o][:,j]-W[a,o][:,j]).sum()
                                    for o in range(2)) for a in range(2) for j in range(2)),
     'true_positive_margin':min(float(v.min()) for v in Wtrue.values()),
     'finite_all_policy_full_transcript':[]}
for horizon,delta,macros in [(1,0.,1),(5,0.,1),(8,0.,1),(8,.4,1),(8,.4,2),(10,.4,1)]:
    tv,nodes=policy_tv(horizon,delta,macros)
    tail=negative_binomial_tail(horizon,macros,delta) if delta else None
    out['finite_all_policy_full_transcript'].append(dict(native_cap=horizon,abort_probability=delta,
        macros=macros,tv=tv,recursive_nodes=nodes,cap_tail=tail,
        infinite_macro_upper_from_evaluator=None if tail is None else min(1.,tv+tail)))
(ROOT/'post_acquisition_score.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
