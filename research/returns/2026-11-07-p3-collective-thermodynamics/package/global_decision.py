"""Global thermodynamic design with independently checked rational bounds.

SciPy/HiGHS proposes primal and dual probabilities. Only their rounded,
exactly feasible rational values enter certificates. The state oracle is a
global interval calculation, not a local-minimum or phase-selection oracle.
"""
import json,time
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy.optimize import linprog
from polynomial_tools import evaluate,combine,decode_polynomial
from certified_thermodynamics import StateOracle,point_value,dot

ROOT=Path(__file__).resolve().parent


def rational_simplex(values,denominator=10**9):
    values=np.maximum(np.asarray(values,dtype=float),0)
    assert np.isfinite(values).all() and values.sum()>0
    values/=values.sum()
    units=[int(np.floor(x*denominator)) for x in values]
    deficit=denominator-sum(units)
    assert 0<=deficit<=len(values)+1
    units[int(np.argmax(values))]+=deficit
    result=[Q(x,denominator) for x in units]
    assert min(result)>=0 and sum(result)==1
    return result


def solve(base,controls,vertices,price,beta,nu,tolerance=Q(1,100)):
    start=time.perf_counter()
    points=[(Q(0),)*3]
    for j in range(3):
        for sign in [-1,1]: points.append(tuple(Q(sign if i==j else 0) for i in range(3)))
    for sign in [-1,1]: points.append((Q(3,5),Q(0),sign*Q(4,5)))
    iterations=[]; final=None
    while True:
        intercepts=[point_value(base,r,beta) for r in points]
        features=[[evaluate(f,r) for f in controls] for r in points]
        # Upper intercepts are safe for an upper approximation to the concave
        # free energy. Their exact rational values are re-used in the dual.
        matrix=[[intercepts[s][1]-dot(v,features[s])-dot(price,v) for v in vertices]
                for s in range(len(points))]
        arr=np.array([[float(v) for v in row] for row in matrix])
        q=len(vertices)
        result=linprog(np.r_[np.zeros(q),-1.0],A_ub=np.c_[-arr,np.ones(len(points))],
                       b_ub=np.zeros(len(points)),A_eq=np.array([[1.0]*q+[0.0]]),
                       b_eq=[1.0],bounds=[(0,None)]*q+[(None,None)],method='highs')
        assert result.success,result.message
        lam=rational_simplex(result.x[:q]); w=rational_simplex(-result.ineqlin.marginals)
        u=tuple(sum((a*v[j] for a,v in zip(lam,vertices)),Q(0)) for j in range(len(price)))
        upper=max(sum((a*matrix[s][j] for s,a in enumerate(w)),Q(0)) for j in range(q))+nu
        p=combine(base,controls,u)
        state=StateOracle(p,beta).minimize(tolerance/4,initial_points=points)
        lower=state['lower']-dot(price,u)-nu
        gap=upper-lower
        entry={'iteration':len(iterations)+1,'state_points':len(points),
               'control':[str(v) for v in u],'lower':str(lower),'upper':str(upper),
               'gap':str(gap),'gap_float':float(gap),'state_bounds':state['bounds'],
               'state_seconds':state['seconds']}
        iterations.append(entry)
        print('beta',('infinity' if beta is None else str(beta)),'iteration',len(iterations),
              'u',tuple(round(float(v),7) for v in u),'certified gap',round(float(gap),8),
              'state boxes',state['bounds'],flush=True)
        if gap<=tolerance:
            final={'control':[str(v) for v in u], 'simplex_weights':[str(v) for v in lam],
                   'state_points':[[str(v) for v in r] for r in points],
                   'dual_weights':[str(v) for v in w],
                   'objective_lower':str(lower),'objective_upper':str(upper),'regret_bound':str(gap),
                   'objective_lower_float':float(lower),'objective_upper_float':float(upper),
                   'regret_bound_float':float(gap),'minimizer_witness':[str(v) for v in state['point']]}
            break
        assert state['point'] not in points,'Candidate LP stalled: no unchecked success is returned.'
        points.append(state['point'])
        assert len(iterations)<200,'Candidate LP did not yield the requested certificate.'
    # Report an uncertainty-aware cover at the chosen control. This covers all
    # minimizing product macrostates compatible with the coefficient ball.
    cover=StateOracle(combine(base,controls,u),beta).minimize(tolerance/4,nu,Q(1,8),points)
    final.update({'beta':None if beta is None else str(beta),'coefficient_l1_error':str(nu),
                  'iterations':iterations,'phase_cover':cover['cover'],
                  'phase_cover_state_interval':[str(cover['lower']),str(cover['upper'])],
                  'phase_cover_bounds':cover['bounds'],'wall_seconds':time.perf_counter()-start})
    mixture_response=[sum((a*f[j] for a,f in zip(w,features)),Q(0)) for j in range(len(price))]
    mixture_energy=sum((a*intercepts[s][1] for s,a in enumerate(w)),Q(0))
    final['mixture_response']=[str(x) for x in mixture_response]
    final['target_response']=[str(-x) for x in price]
    final['mixture_response_error_linf']=str(max(abs(x+y) for x,y in zip(mixture_response,price)))
    final['mixture_equilibrium_deficit_upper']=str(mixture_energy-dot(u,mixture_response)-state['lower']+2*nu)
    return final


def main():
    acquired=json.loads((ROOT/'ACQUISITION_CERTIFICATE.json').read_text())
    base=decode_polynomial(acquired['learned_polynomial']); nu=Q(acquired['coefficient_l1_error'])
    controls=[{(1,0,0):Q(1)},{(0,0,1):Q(1)}]
    vertices=[(Q(g),Q(h,5)) for g in [0,Q(3,2)] for h in [-1,1]]
    price=(Q(-1,2),Q(0))
    outputs={}
    for label,beta in [('ground',None),('finite_temperature',Q(2))]:
        result=solve(base,controls,vertices,price,beta,nu)
        result['task']={'vertices':[[str(v) for v in u] for u in vertices],
                        'price':[str(v) for v in price],
                        'controls':['x','z'],'objective':'maximize F_beta(g,h)+g/2',
                        'interpretation':'bounded-field Legendre design for target collective response (1/2,0); the +g/2 term is a target-response multiplier, not a claim of monetary income'}
        (ROOT/('DECISION_'+label.upper()+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        outputs[label]={k:result[k] for k in ['control','objective_lower_float','objective_upper_float',
                                            'regret_bound_float','wall_seconds']}
    print(json.dumps(outputs,indent=2),flush=True)


if __name__=='__main__': main()
