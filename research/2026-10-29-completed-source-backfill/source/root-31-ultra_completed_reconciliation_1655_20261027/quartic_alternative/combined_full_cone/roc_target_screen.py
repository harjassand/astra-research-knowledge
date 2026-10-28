"""Separate the input-existence question from the combined QC method."""
import json,time
from fractions import Fraction as F
import numpy as np
import cvxpy as cp
from maps import load,SOURCE,ROOT
from models import Primal
from construct_target import evaluation
from exact_acoustic import acquire


def main():
    d=load();record=json.loads((SOURCE/'EXACT_HEAT_SEPARATOR.json').read_text())
    lh=np.array([float(F(x)) for x in record['lambda_xpair_zpair']]);gh=d['E'].T@lh
    results=[];epsilon=1e-5
    for index,A0 in enumerate([[1,0,0,1],[2,0,0,1],[1,1,0,1]]):
        start=time.monotonic();v=cp.Variable(15);delta=cp.Variable();ev=evaluation(A0)
        Q=sum(v[i]*d['Q'][i] for i in range(15))
        problem=cp.Problem(cp.Maximize(delta),[Q>>epsilon*np.eye(8),cp.trace(Q)==1,
                            ev@v[:9]<=-delta*np.linalg.norm(ev),gh@v[:9]<=-delta*np.linalg.norm(gh)])
        problem.solve(solver='CLARABEL',max_iter=120,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
        rec={'status':'NUMERICAL_ACOUSTIC_INPUT_EXISTENCE_SCREEN','A0':A0,'margin':float(delta.value),
             'solver_status':problem.status,'seconds':time.monotonic()-start}
        if delta.value>1e-7:
            p,replay=acquire(v.value,d['Q'],ROOT/f'roc_target_{index:02}.json',F(1,200000),10**10)
            pn=np.array(list(map(float,p)));rec['ROC_replay']=replay;rec['coefficients']=list(map(str,p))
            for kind in ['PC','heat','combined']:
                rec[kind]=Primal(d,kind).solve(pn,f'roc_target_{index:02}_{kind}')
        results.append(rec);print(json.dumps(rec),flush=True)
        (ROOT/'ROC_TARGET_SCREEN.json').write_text(json.dumps(results,indent=2)+'\n')
        if delta.value>1e-7:return


if __name__=='__main__':main()
