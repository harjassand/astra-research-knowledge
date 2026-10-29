#!/usr/bin/env python3
"""Actual terminal states; compare ideal decoder extensions, not gate-noise claims."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import sys,json,hashlib
import numpy as np
HERE=Path(__file__).parent;Q=HERE.parent
sys.path.insert(0,str(Q/'clocked_flagged_storage_20261028'))
import clocked_channel_v1 as m
c=m.c
CLOCK={'one':1.,'two':2.,'prep':2.,'measure':4.,'feedback':1.}
def signed_mul(a,b,extra=1):
 w,p=c.mulword(a[0],b[0]);p=complex(extra*a[1]*b[1]*p)
 assert abs(p.imag)<1e-12 and abs(abs(p.real)-1)<1e-12
 return w,int(round(p.real))
def rep(axis,k):return signed_mul(((axis,)*5,1),c.STAB[k])
def decoder(kx,kz):
 x=rep(1,kx);z=rep(3,kz);y=signed_mul(x,z,1j)
 D=np.zeros((4,1024));D[0,0]=.5
 for j,(w,s) in enumerate([x,y,z],1):D[j,np.ravel_multi_index(w,[4]*5)]=s/2
 return D,[{'pauli':''.join(c.chars[a] for a in w),'sign':s} for w,s in [x,y,z]]
def main():
 initial,R=m.code_coordinates();family=[]
 for kx in range(16):
  for kz in range(16):
   D,reps=decoder(kx,kz)
   assert np.max(abs(D@initial-np.eye(4)))<1e-12
   family.append((kx,kz,D,reps))
 rows=[];mts=m.native()
 for bg,rbest in [(.03,2),(.1,4),(.3,8)]:
  F,timing=m.build_ec(.001,bg/201,CLOCK)
  for r in [1,rbest]:
   T=32;A=initial.copy();local=[np.linalg.matrix_power(M,r) for M in mts]
   for _ in range(T//r):
    for q,M in enumerate(local):A=m.local(A,M,[q],5)
    A=F@A
   scores=[]
   for kx,kz,D,reps in family:
    score=m.old.metrics(D@A)
    scores.append({'kx':kx,'kz':kz,'representatives':reps,**score})
   best=min(scores,key=lambda s:s['entanglement_infidelity'])
   rows.append({'background_integral':bg,'T':T,'r':r,'elapsed_time':2*T+201*(T//r),'ideal_recovery_decode':m.old.metrics(R@A),'bare_all_site_normalizers':scores[0],'best_ideal_Clifford_extension':best,'all_256_extensions':scores})
   print(bg,r,'recovery Fe',1-rows[-1]['ideal_recovery_decode']['entanglement_infidelity'],'all-site Fe',1-scores[0]['entanglement_infidelity'],'best Clifford Fe',1-best['entanglement_infidelity'],flush=True)
 out={'status':'AUTHOR_DIAGNOSTIC_NO_NOISY_ENDPOINT_IMPLEMENTATION','logical_frame':'Xbar XXXXX, Zbar ZZZZZ; 256 physical normalizer-pair extensions','rows':rows,'source_hashes':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Q/'clocked_flagged_storage_20261028/clocked_channel_v1.py',Q/'five_qubit_acquired_frame_pilot_20261028/code_and_channels.py',Q/'five_qubit_acquired_frame_pilot_20261028/models.npz']}}
 (HERE/'results_v1.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
