"""Exact integer supersolution for a spatially closed memory6 trail Green kernel."""
from pathlib import Path
import sys,time,json,argparse
import numpy as np
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_operator_bridge_20261105'))
from fourier_loop_return import setup

def build(side=16,iterations=500,bits=40):
 start=time.monotonic();ds,rows,cols,w,delta,pos,pw=setup(6);ns=4*len(ds);Q=2**bits
 ww=np.rint(w*5).astype(np.int64);mats=[];shifts=[]
 xx,yy=np.indices((side,side))
 for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
  mask=(delta[:,0]==dx)&(delta[:,1]==dy)
  mats.append(coo_matrix((ww[mask],(cols[mask],rows[mask])),shape=(ns,ns)).tocsr())
  shifts.append((((xx+dx)%side)*side+(yy+dy)%side).reshape(-1))
 cert=np.load(ROOT/'square_aklt_loop_audit_20261105/trail_certificate_m6.npz');vi=np.tile(cert['v'],4)
 an=int(cert['alpha_num']);ad=int(cert['alpha_den']);den=(3*ad-an)*int(vi.min())
 base=np.array([(2*3*ad*int(v)*Q+den-1)//den for v in vi],dtype=np.int64)
 q=np.broadcast_to(base[:,None],(ns,side*side)).copy()
 def step(q):
  assert 15*int(q.max())+15*Q<2**63
  num=sum((A@q[:,sh] for A,sh in zip(mats,shifts)))
  nxt=(num+14)//15;nxt[:,0]+=Q
  return nxt
 nxt=step(q);assert np.all(nxt<=q)
 for k in range(iterations):
  q=nxt;nxt=step(q)
  assert np.all(nxt<=q)
  if (k+1)%100==0:print('iteration',k+1,'max decrease',int((q-nxt).max()),'elapsed',time.monotonic()-start,flush=True)
 # q is a verified supersolution: source + ceil(Aq/15)<=q.
 assert np.all(q>=1)
 out=Path(__file__).parent/f'torus_green_m6_L{side}.npz'
 np.savez_compressed(out,q=q.reshape(ns,side,side),scale=Q,side=side,memory=6,iterations=iterations)
 result={'side':side,'memory':6,'states':ns*side*side,'scale':Q,'iterations':iterations,
  'max_supersolution_slack':int((q-nxt).max()),'min_q':int(q.min()),'max_q':int(q.max()),'elapsed_seconds':time.monotonic()-start,
  'scope':'Exact integer inequality. Torus return aliases only enlarge the target loop birth measure.'}
 out.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--side',type=int,default=16);ap.add_argument('--iterations',type=int,default=500);a=ap.parse_args();build(a.side,a.iterations)
