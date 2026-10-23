#!/usr/bin/env python3
"""Exact sharp examples for one-cell border/forest decoder; stdlib only."""
from fractions import Fraction as Q
from pathlib import Path
import time,json,resource
start=time.perf_counter();cpu=time.process_time()
fixtures=[]
for s in (0,1,3):
 t=2;n=s+t;q=s+3
 colors=list(range(s))+[s,s+1]
 E=[[Q(0) for j in range(q)] for i in range(n)]
 D=[[Q(0) for j in range(n)] for i in range(n)]
 if s:
  active=[0,s,s+1];diag=Q(1,3);edge=Q(2,3);ratio2=Q(5,3)
 else:
  active=[0,1];diag=Q(1,2);edge=Q(1);ratio2=Q(3,2)
 for i in active: E[i][colors[i]]=diag
 if s:
  E[s][0]=edge;E[s+1][0]=edge
 E[s+1][s]=edge
 for i in range(n): D[i][i]=E[i][colors[i]]
 if s:
  for v in (s,s+1): D[v][0]=D[0][v]=E[v][0]
 D[s][s+1]=D[s+1][s]=E[s+1][s]
 for i in active:
  for j in active: assert D[i][j]==(diag if i==j else edge)
 # Matrix on the active clique is edge*J+(diag-edge)*I.
 lam=diag+(len(active)-1)*edge
 assert lam>abs(diag-edge)
 e2=sum(e*e for row in E for e in row)
 assert lam*lam/e2==ratio2
 fixtures.append({'s':s,'n':n,'queries':q,'action_error_squared':str(e2),'operator_error':str(lam),'ratio_squared':str(ratio2)})
report={'passed':True,'fixtures':fixtures,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'scope':'Exact sharpness examples for the stated linear decoder, not optimal-decoder lower bounds.'}
out=Path(__file__).resolve().parents[1]/'results'/'border_decoder_checks.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
