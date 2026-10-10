import pathlib,sys,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'python_packages'))
import numpy as np
from scipy.signal import savgol_filter
records=[]
# Test the frozen numerical rules, independently of any biological model fit.
for direction in [-1,1]:
 for truth in [None,0.0,0.25,0.5,0.7]:
  fs=4000;t=np.arange(0,3,1/fs);base=20.;edge=1.
  # External pulse ends at t=1. No mechanical relaxation is synthesized.
  angle=80*np.minimum(t,edge)
  if truth is not None: angle+=2*np.maximum(t-edge-truth,0)
  angle*=direction;v=savgol_filter(angle,401,1,deriv=1,delta=1/fs)*direction
  ts=t[::40];vs=v[::40];pos=vs>base*.05
  starts=np.r_[np.convolve(pos.astype(int),np.ones(15,dtype=int),mode='valid')>=14,np.zeros(14,dtype=bool)]
  guard=.1;initial=(ts>=edge+guard)&(ts<edge+guard+.1);init_v=vs[initial].mean()
  inds=np.flatnonzero(starts&(ts>=edge+guard)&(ts<=edge+.8));onset=ts[inds[0]]-edge if len(inds) else None
  immediate=onset is not None and ((init_v>base*.05) or onset<=guard+.05)
  delayed=onset is not None and not immediate and init_v<base*.025 and onset>=guard+.1
  category='immediate_or_unresolved' if immediate else 'resolved_off' if delayed else 'ambiguous' if onset is not None else 'none'
  expected='none' if truth is None else 'immediate_or_unresolved' if truth==0 else 'resolved_off'
  assert category==expected,(truth,category)
  if truth is not None and truth>0:assert abs(onset-truth)<=.03
  records.append(dict(direction=direction,truth=truth,detected=onset,category=category))
(ROOT/'results/synthetic_checks.json').write_text(json.dumps(records,indent=2));print('All ten synthetic classification checks passed.')
