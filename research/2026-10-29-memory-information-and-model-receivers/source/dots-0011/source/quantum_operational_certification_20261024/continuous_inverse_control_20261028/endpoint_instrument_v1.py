#!/usr/bin/env python3
"""Expose all 16 actual terminal syndrome branches before output correction."""
from pathlib import Path
import sys,json,numpy as np
HERE=Path(__file__).parent
sys.path.insert(0,str(HERE));import pulse_pipeline_v1 as p
b=p.b;m=p.m

def branches(A,eta,rate):
 live=list(range(5))
 for q in range(1,5):
  A=m.background(A,rate,4,live,5);A=m.local(A,m.ptm(m.old.rotation(b.Y,eta)),[q],5);live.remove(q)
 A=m.background(A,rate,1,[0],5)
 out={}
 for a in range(16):
  bits=[(a>>(3-q))&1 for q in range(4)];B=np.zeros((4,A.shape[1]))
  for d in m.digits(5):
   if all(v in [0,3] for v in d[1:]):
    sign=(-1)**sum(bits[q] for q in range(4) if d[q+1]==3)
    B[d[0]]+=sign*A[np.ravel_multi_index(d,[4]*5)]/32
  out[a]=B
 return out

def generate(integrated=.03,eta=.001,eps=.001,T=32,r=2):
 rate=integrated/201;native,timing=p.build_native(rate,eps,eta);dec,enc,U=b.synthesize();A=b.circuit(b.initial(eta,rate),enc,eta,rate);F,_=m.build_ec(eta,rate,b.CLOCK)
 for step in range(T):
  for q,M in enumerate(native):A=m.local(A,M,[q],5)
  if (step+1)%r==0:A=F@A
 A=b.circuit(A,dec,eta,rate);B=branches(A,eta,rate);table=b.syndrome_table(U);recombined=np.zeros((4,4))
 for a,M in B.items():
  if table[a]:M=m.ptm(m.old.rotation(b.X,eta)@m.P[table[a]])@M
  M=np.diag([1,np.exp(-rate),np.exp(-rate),1])@M;recombined+=M
 return {'parameters':{'integrated':integrated,'eta':eta,'eps':eps,'T':T,'r':r},'branch_PTMs':{str(k):v.tolist() for k,v in B.items()},'branch_time_excludes_final_correction_window':1,'prior_correction_lookup':table,'recombined_prior_physical_output_PTM':recombined.tolist(),'branch_sum_TP_error':float(np.max(abs(sum(B.values())[0]-np.array([1,0,0,0]))))}
if __name__=='__main__':
 x=generate();old=json.loads((HERE/'results_v1.json').read_text())[1];err=float(np.max(abs(np.array(x['recombined_prior_physical_output_PTM'])-np.array(old['physical_output_PTM']))));assert err<1e-12;x['recombination_error_vs_frozen_pipeline']=err
 (HERE/'endpoint_instrument_v1.json').write_text(json.dumps(x,indent=2)+'\n');print(err,x['branch_sum_TP_error'])
