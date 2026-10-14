"""Independent exact reconstruction of finite Stieltjes-response nonidentifiability."""
from fractions import Fraction as F
import json
import independent_check as c

rates=[F(1),F(2),F(3),F(4)]
base=[F(1,4)]*4
shifts=[F(1),F(2),F(4)]
delta=F(1,1000)
base_response=[sum((p/(lam+s) for p,lam in zip(base,rates)),F(0)) for s in shifts]
base_mean=sum((p/lam for p,lam in zip(base,rates)),F(0))
# Unknown old masses solve normalization plus all three exact response constraints.
M=[[F(1) for _ in rates]] + [[F(1,1)/(lam+s) for lam in rates] for s in shifts]
rows=[]
for eps in [F(1,100),F(1,10000),F(1,10**8),F(1,10**12)]:
    rhs=[1-delta]+[f-delta/(eps+s) for f,s in zip(base_response,shifts)]
    q=c.solve(M,rhs)
    weights=q+[delta]
    assert all(w>0 for w in weights)
    assert sum(weights,F(0))==1
    got=[sum((weights[j]/((rates+[eps])[j]+s) for j in range(5)),F(0)) for s in shifts]
    assert got==base_response
    mean=sum((weights[j]/(rates+[eps])[j] for j in range(5)),F(0))
    rows.append({'epsilon':str(eps),'old_weights':[str(w) for w in q],'minimum_weight':str(min(weights)),
                 'responses':[str(z) for z in got],'mean':str(mean),'mean_float':float(mean)})
# A symbolic nonsingularity argument is recorded in the report: if c_i has sum
# zero and its resolvent sum vanishes at k distinct shifts, the numerator has
# degree at most k-1 and k roots, so all residues vanish.
print(json.dumps({'baseline_rates':[str(x) for x in rates],'baseline_weights':[str(x) for x in base],
 'shifts':[str(x) for x in shifts],'baseline_response':[str(x) for x in base_response],
 'baseline_mean':str(base_mean),'hidden_mass':str(delta),'exact_samples':rows,
 'status':'exactly equal finite regularized responses with positive masses; lifetime grows as delta/epsilon plus bounded correction'},indent=2))
