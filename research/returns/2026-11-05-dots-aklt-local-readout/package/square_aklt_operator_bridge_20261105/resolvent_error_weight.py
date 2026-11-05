"""Exact integer supersolution q >= 1 + T_backward q/3.
Controls l1 errors for every Fourier phase because |T(k)|<=T(0).
This certifies the residual-amplification factor, not floating residual evaluation.
"""
import numpy as np
from pathlib import Path

def get_q(m):
 path=Path(__file__).with_name(f'residual_supersolution_m{m}.npz')
 if path.exists():
  z=np.load(path);return z['q'].astype(float)/int(z['den'])
 z=np.load(Path(__file__).resolve().parents[1]/f'square_aklt_loop_audit_20261105/trail_certificate_m{m}.npz')
 to,w,vi=z['targets'],z['weights'],z['v'];q=np.ones(len(vi))
 for it in range(10000):
  nq=1+(w*q[to]).sum(1)/15
  if np.max(abs(nq-q))<1e-12:q=nq;break
  q=nq
 den=10**12;qi=np.ceil(q*den).astype(np.int64)
 res=15*den+(w*qi[to]).sum(1)-15*qi
 slack=15*vi-(w*vi[to]).sum(1)
 assert np.min(slack)>0
 correction=int(np.max(np.maximum(res,0)//slack+1));qi=qi+correction*vi
 assert np.all(15*qi>=15*den+(w*qi[to]).sum(1))
 np.savez_compressed(path,q=qi,den=den,correction=correction)
 return qi.astype(float)/den
