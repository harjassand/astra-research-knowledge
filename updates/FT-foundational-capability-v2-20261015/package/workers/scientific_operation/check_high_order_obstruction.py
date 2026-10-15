#!/usr/bin/env python3
"""Dissipative plants invisible to every proper-subset control experiment."""
import json
from pathlib import Path
import numpy as np


def build(m, sign):
    d=1+1/m
    H=d*np.eye(m)
    for i in range(m):
        H[i,(i+1)%m]=1
    H[0,1]=sign
    w=np.eye(m)[0]
    G=np.block([[np.array([[2*m]]),w[None,:]],[w[:,None],H]])
    return G,H


def formula(m, sign, u):
    d=1+1/m
    ratios=u/(1+d*u)
    return 2*m-ratios[0]/(1+(-1)**(m-1)*sign*np.prod(ratios))


results=[]
for m in (4,6,10,16,32,64):
    Gp,Hp=build(m,1)
    Gn,Hn=build(m,-1)
    Ap,An=np.linalg.inv(Gp),np.linalg.inv(Gn)
    rng=np.random.default_rng(900+m)
    errors=[]; sparse_differences=[]
    for _ in range(100):
        u=rng.uniform(0,2*m,m)
        u[rng.integers(m)]=0
        fp=formula(m,1,u); fn=formula(m,-1,u)
        sparse_differences.append(abs(fp-fn))
        for A,sign in ((Ap,1),(An,-1)):
            D=np.diag(np.r_[0.,u]); b=np.eye(m+1)[0]
            errors.append(abs(np.linalg.solve(A+D,b)[0]-formula(m,sign,u)))
    u=np.full(m,float(m)); v=np.full(m,float(2*m))
    pf,pv=formula(m,1,u),formula(m,1,v)
    nf,nv=formula(m,-1,u),formula(m,-1,v)
    results.append({"m":m,
       "min_symmetric_G_plus_eigenvalue":float(np.linalg.eigvalsh((Gp+Gp.T)/2).min()),
       "min_symmetric_G_minus_eigenvalue":float(np.linalg.eigvalsh((Gn+Gn.T)/2).min()),
       "condition_number_A_plus":float(np.linalg.cond(Ap)),
       "condition_number_A_minus":float(np.linalg.cond(An)),
       "maximum_direct_matrix_formula_error":float(max(errors)),
       "maximum_sparse_query_difference":float(max(sparse_differences)),
       "all_m_controls_at_m_prediction_difference":float(abs(pf-nf)),
       "plus_response_change_m_to_2m":float(pv-pf),
       "minus_response_change_m_to_2m":float(nv-nf),
       "opposite_ranking_of_two_admissible_actions":bool((pv-pf)*(nv-nf)<0)})
output={"status":"exact_analytic_construction_and_synthetic_checks_only", "results":results}
Path(__file__).with_name("high_order_obstruction_results.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps(output,indent=2))
