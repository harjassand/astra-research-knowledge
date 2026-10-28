#!/usr/bin/env python3
"""Refine the demonstrated packet-span and time-freeze obstructions."""
import json
from continuous_galerkin import run,compare,OUT

if __name__=='__main__':
    cfg=[('continuous_three_K2_s320',[0.,.3,.6],2,320),
         ('continuous_three_K3_s160',[0.,.3,.6],3,160),
         ('continuous_four_K1_s160',[0.,.2,.4,.6],1,160)]
    runs=[]
    for name,nodes,K,steps in cfg:
        rec,b,y=run(nodes,K,steps=steps,label=name);runs.append((rec,b,y))
        print(name,'rank',b.rank,'residual',rec['residual_integral_diagnostic'],
              'basis',rec['basis_residual_integral_diagnostic'],
              'freeze',rec['time_freeze_residual_integral_diagnostic'],flush=True)
        (OUT/(name+'_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
    comparisons=[]
    for i in range(len(runs)):
        for j in range(i+1,len(runs)):
            comparisons.append({'a':runs[i][0]['label'],'b':runs[j][0]['label'],
                **compare(runs[i][1],runs[i][2],runs[j][1],runs[j][2])})
    (OUT/'continuous_refinement_summary.json').write_text(json.dumps({'runs':[x[0] for x in runs],'comparisons':comparisons},indent=2)+'\n')
