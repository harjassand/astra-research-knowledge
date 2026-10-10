import pathlib,sys,json,os,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'python_packages'));os.environ['MPLCONFIGDIR']=str(ROOT/'analysis/mplcache')
import numpy as np,pandas as pd
from scipy.signal import savgol_filter
from scipy.stats import fisher_exact

def analyze(split):
 s=pd.read_csv(ROOT/'raw/selected_manifest.csv');s=s[s.split==split];out=[]
 for _,r in s.iterrows():
  f=ROOT/'raw/extracted'/r.path
  if not f.exists():continue
  x=np.loadtxt(f,usecols=(0,4));t=x[:,0]/4000;ang=x[:,1];v=savgol_filter(ang,401,1,deriv=1,delta=1/4000)
  base=np.median(v[(t>1)&(t<9)]);sgn=np.sign(base);ang=ang*sgn;v=v*sgn;base=abs(base)
  # Observations on a fixed 100Hz grid. Slopes use +/-50ms; hence edges are excluded by >=100ms.
  ts=t[::40];vs=v[::40];aa=ang[::40]
  for frac in [.025,.05,.075]:
   for guard in [.1,.2]:
    threshold=base*frac
    # 150ms positive persistence with at most one low sample; event timestamp is run start.
    pos=vs>threshold
    persistent=np.convolve(pos.astype(int),np.ones(15,dtype=int),mode='valid')>=14
    starts=np.r_[persistent,np.zeros(14,dtype=bool)]
    intervals=[(20,50)] if '01_Without' in r.group else [(20,21)]+[(float(a),float(a+1)) for a in np.arange(21.5,50,1.5)]
    for pulse,(start,end) in enumerate(intervals):
     # Any autonomous motion at the first fully resolved sample cannot be attributed to OFF activation.
     initial=(ts>=start+guard)&(ts<start+guard+.1)
     init_v=np.mean(vs[initial]); init_disp=(aa[np.flatnonzero(initial)[-1]]-aa[np.flatnonzero(initial)[0]])
     inds=np.flatnonzero(starts&(ts>=start+guard)&(ts<=end-.2))
     onset=float(ts[inds[0]]-start) if len(inds) else np.nan
     immediate=(init_v>threshold) or (np.isfinite(onset) and onset<=guard+.05)
     # Testable late onset: initial OFF motion below half threshold, not marginally already active.
     delayed=np.isfinite(onset) and not immediate and init_v<threshold/2 and onset>=guard+.1
     category='immediate_or_unresolved' if immediate else 'resolved_off' if delayed else 'ambiguous' if np.isfinite(onset) else 'none'
     risk_end=onset if np.isfinite(onset) else end-start-.2
     exposure_early=max(0,min(risk_end,.5)-(guard+.1)) if not immediate else 0
     exposure_late=max(0,min(risk_end,.8)-max(.5,guard+.1)) if not immediate else 0
     out.append(dict(split=split,cell=r.cell,file=r.file,group=r.group,baseline=base,baseline_sign=int(sgn),frac=frac,guard=guard,pulse=pulse,start=start,end=end,init_v=init_v,threshold=threshold,onset=onset,category=category,exposure_early=exposure_early,exposure_late=exposure_late))
     if category!='none':break
 d=pd.DataFrame(out);d.to_csv(ROOT/f'results/{split}_off_memory.csv',index=False)
 for guard in [.1,.2]:
  a=d[(d.frac==.05)&(d.guard==guard)];print(split,'guard',guard)
  print(a[a.category!='none'][['cell','group','pulse','category','onset','baseline_sign']].to_string(index=False))
 return d
if __name__=='__main__': analyze(sys.argv[1])
