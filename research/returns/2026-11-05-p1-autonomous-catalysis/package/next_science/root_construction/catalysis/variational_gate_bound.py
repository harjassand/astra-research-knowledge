"""Exact-cost refinement evaluated numerically; not an interval certificate."""
from pathlib import Path
import json,math
from scipy.optimize import brentq,minimize_scalar
HERE=Path(__file__).resolve().parent
KB=8.617333262145e-5; T=298.; q=math.exp(-.126/(KB*T))
t=q/(1+q); gamma=1/41e-9; B=gamma*(1+q); A=4*.3/(KB*T)
def logit(p): return math.log(p)-math.log1p(-p)
lt=logit(t)
def cost(p): return B*(p-t)*(logit(p)-lt)
def deriv(p): return B*(logit(p)-lt+(p-t)/(p*(1-p)))
def inner(w,lam):
    p=brentq(lambda pp:w-lam*deriv(pp),1e-15,1-1e-15,xtol=1e-14)
    return w*(p-t)-lam*cost(p),p
rows=json.loads((HERE/'thermal_projection_checks.json').read_text())['cases']
out=[]
for row in rows:
    Jth=row['thermal_projected_total_current_s-1']
    W=row['max_complete_cycle_response_contrast_s-1']
    def objective(x):
        lam=x/A
        M=max(inner(W,lam)[0],inner(-W,lam)[0])
        return (Jth+M)/(1-x)
    opt=minimize_scalar(objective,bounds=(1e-7,1-1e-7),method='bounded',options={'xatol':1e-12})
    lam=opt.x/A
    vp,pp=inner(W,lam); vm,pm=inner(-W,lam)
    bound=objective(opt.x)
    assert row['actual_total_current_s-1']<=bound*(1+1e-10)
    out.append({'other_forward_rate_s-1':row['other_forward_rate_s-1'],'capture_fraction':row['capture_fraction'],
        'dual_lambda_dimensionless':lam,'lambda_times_affinity':opt.x,'inner_sup_positive_W':vp,'inner_sup_negative_W':vm,
        'positive_W_maximizing_gate_probability':pp,'negative_W_maximizing_gate_probability':pm,
        'thermal_current_s-1':Jth,'current_upper_bound_s-1':bound,'gain_upper_bound':bound/Jth,
        'actual_gain_over_thermal_projection':row['actual_over_thermal_projected_gain']})
(HERE/'variational_gate_bound_results.json').write_text(json.dumps({
    'status':'numerical evaluation of proved dual inequality; synthetic inputs; not an interval-arithmetic certificate or empirical result',
    'formula':'J <= (Jth + max_i sup_p [w_i(p-t_i)-lambda cost_i(p)])/(1-lambda*A)',
    'conservative_choice':'uniform +/-max|w|, without actual state occupation',
    'cases':out},indent=2))
print(json.dumps(out,indent=2))
