"""Acquire QC outside a pointwise-PC bound and a supplied heat normal.
Failure is not a no-go for other normals or the full cone.
"""
import json,time
from fractions import Fraction as F
import numpy as np
import cvxpy as cp
from maps import load,SOURCE,ROOT
from models import symmetric
from exact_acoustic import acquire


def evaluation(A):
    a,b,c,d=A;u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    return np.array([u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w],float)


def main():
    d=load();record=json.loads((SOURCE/'EXACT_HEAT_SEPARATOR.json').read_text())
    lh=np.array([float(F(x)) for x in record['lambda_xpair_zpair']]);gh=d['E'].T@lh
    assert abs(gh@np.array([1,1,16,-13,0,0,4,-4,0])-float(F(record['pair_F'])))<1e-12
    records=[]
    for index,A0 in enumerate([[1,0,0,1],[2,0,0,1],[1,1,0,1]]):
        start=time.monotonic();p=cp.Variable(9);k=cp.Variable(6);h=cp.Variable(9)
        pc=cp.Variable(1840);heat=cp.Variable(300);omega=cp.Variable(45);margin=cp.Variable()
        Q=symmetric(pc[:1830],60);R=symmetric(heat,24)
        acoustic=sum(p[i]*d['Q'][i] for i in range(9))+sum(k[i]*d['Q'][i+9] for i in range(6))
        ev=evaluation(A0)
        constraints=[d['A']@pc+d['B']@h==d['B']@p,
                     d['G']@heat-d['E']@h-d['ON']@omega==0,
                     Q-margin*np.eye(60)>>0,R-margin*np.eye(24)>>0,
                     acoustic>>.001*np.eye(8),cp.trace(acoustic)==1,
                     ev@p<=-margin*np.linalg.norm(ev),gh@p<=-margin*np.linalg.norm(gh)]
        problem=cp.Problem(cp.Maximize(margin),constraints)
        problem.solve(solver='CLARABEL',max_iter=180,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
        result={'status':'NUMERICAL_ONLY','A0':A0,'solver_status':problem.status,
                'margin':None if margin.value is None else float(margin.value),'seconds':time.monotonic()-start}
        if p.value is not None:
            result['point_value']=float(ev@p.value);result['heat_separator_pairing']=float(gh@p.value)
            np.savez(ROOT/f'target_{index:02}.npz',p=p.value,k=k.value,h=h.value,pc=pc.value,heat=heat.value,omega=omega.value,
                     dualPC=constraints[0].dual_value,dualheat=constraints[1].dual_value)
        records.append(result);print(json.dumps(result),flush=True)
        (ROOT/'CONSTRUCT_TARGET.json').write_text(json.dumps(records,indent=2)+'\n')
        if margin.value is not None and margin.value>1e-7:
            pexact,replay=acquire(np.r_[p.value,k.value],d['Q'],ROOT/f'target_{index:02}_ROC.json')
            print('EXACT_ROC_ACQUIRED_FOR_CONSTRUCTIVE_TARGET',index,replay['certificate_sha256'],flush=True)
            return


if __name__=='__main__':main()
