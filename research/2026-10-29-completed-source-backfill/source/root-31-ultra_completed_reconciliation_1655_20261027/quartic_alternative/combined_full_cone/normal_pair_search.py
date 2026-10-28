"""Target actual separate certificate normals on the strict acoustic lift."""
from fractions import Fraction as F
import json,time
import numpy as np
import cvxpy as cp
from maps import load,SOURCE,ROOT
from models import Primal,Acoustic
from exact_acoustic import acquire


def main():
    d=load();heat_source=json.loads((SOURCE/'EXACT_HEAT_SEPARATOR.json').read_text())
    gh=d['E'].T@np.array([float(F(x)) for x in heat_source['lambda_xpair_zpair']])
    pc_names=['control_DM_PC','candidate_05_PC','candidate_08_PC'];results=[]
    for index,name in enumerate(pc_names):
        source=np.load(ROOT/(name+'.npz'));gp=d['B'].T@source['dual_0']
        start=time.monotonic();v=cp.Variable(15);margin=cp.Variable()
        Q=sum(v[i]*d['Q'][i] for i in range(15))
        constraints=[Q>>1e-5*np.eye(8),cp.trace(Q)==1,
                     gp@v[:9]<=-margin*np.linalg.norm(gp),gh@v[:9]<=-margin*np.linalg.norm(gh)]
        problem=cp.Problem(cp.Maximize(margin),constraints)
        problem.solve(solver='CLARABEL',max_iter=120,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
        record={'status':'NUMERICAL_NORMAL_PAIR_TARGET','PC_normal_source':name,
                'margin':float(margin.value),'seconds':time.monotonic()-start}
        if margin.value>1e-7:
            p,replay=acquire(v.value,d['Q'],ROOT/f'normal_target_{index:02}_ROC.json',F(1,200000),10**10)
            pn=np.array(list(map(float,p)));record['coefficients']=list(map(str,p));record['ROC_replay']=replay
            for kind in ['PC','heat','combined']:record[kind]=Primal(d,kind).solve(pn,f'normal_target_{index:02}_{kind}')
            np.savez(ROOT/f'normal_target_{index:02}_normals.npz',gp=gp,gh=gh)
        results.append(record);print(json.dumps(record),flush=True)
        (ROOT/'NORMAL_PAIR_SEARCH.json').write_text(json.dumps(results,indent=2)+'\n')
        if margin.value>1e-7:return
    # Acquire a fresh difficult heat direction rather than more easy ROC samples.
    aa=Acoustic(d,1e-5).solve(gh)
    p,replay=acquire(aa['v'],d['Q'],ROOT/'heat_normal_extreme_ROC.json',F(1,200000),10**10)
    pn=np.array(list(map(float,p)));rec={'status':'EXACT_ROC_DIFFERENT_FIELDS_NUMERICAL','coefficients':list(map(str,p)),'ROC_replay':replay}
    for kind in ['PC','heat','combined']:rec[kind]=Primal(d,kind).solve(pn,'heat_normal_extreme_'+kind)
    (ROOT/'HEAT_NORMAL_EXTREME.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)


if __name__=='__main__':main()
