"""Bounded cone attack. Searches are not containment or separation proofs."""
from pathlib import Path
import json,time
import numpy as np
from maps import load,ROOT
from models import CommonDual,Acoustic,Primal
from exact_acoustic import acquire


def main():
    d=load();dual=CommonDual(d);acoustic=Acoustic(d);pc=Primal(d,'PC');heat=Primal(d,'heat');joint=Primal(d,'combined')
    starts=[np.array([0,0,0,0,1,-1,0,0,0.]),
            np.array([0,0,0,0,1,1,0,0,1.]),
            np.array([1,-2,1,-1,2,-1,1,2,-2.])]
    history=[];count=0
    for seed,p0 in enumerate(starts):
        current=p0.copy()
        for iteration in range(3):
            start=time.monotonic();dd=dual.solve(current);aa=acoustic.solve(dd['g']);name=f'candidate_{count:02}'
            p_exact,replay=acquire(aa['v'],d['Q'],ROOT/(name+'_ROC.json'));p=np.array(list(map(float,p_exact)))
            purepc=pc.solve(p,name+'_PC');pureheat=heat.solve(p,name+'_heat');combined=joint.solve(p,name+'_combined')
            np.savez(ROOT/(name+'_directed.npz'),lp=dd['lp'],lh=dd['lh'],g=dd['g'],v=aa['v'])
            record={'status':'EXACT_ROC_ONLY_OTHER_FIELDS_NUMERICAL','index':count,'seed':seed,'iteration':iteration,
                    'coefficients':list(map(str,p_exact)),'ROC_receipt':replay,
                    'dual_value_on_previous_direction':dd['value'],'dual_value_on_new_ROC':float(dd['g']@p),
                    'purePC':purepc,'pureheat_with_minor_removal':pureheat,'combined':combined,'seconds':time.monotonic()-start}
            history.append(record);(ROOT/'DIRECTED_SEARCH.json').write_text(json.dumps(history,indent=2)+'\n')
            print(json.dumps({'index':count,'exact_ROC':'PASS','PC':purepc['margin'],'heat':pureheat['margin'],
                              'joint':combined['margin'],'dual_on_ROC':record['dual_value_on_new_ROC'],'seconds':record['seconds']}),flush=True)
            count+=1
            if combined['margin']< -1e-7 or (purepc['margin']< -1e-6 and pureheat['margin']< -1e-6 and combined['margin']>1e-6):
                print('CONSEQUENTIAL_CANDIDATE_REQUIRES_EXACT_RECONSTRUCTION',name,flush=True);return
            current=p


if __name__=='__main__':main()
