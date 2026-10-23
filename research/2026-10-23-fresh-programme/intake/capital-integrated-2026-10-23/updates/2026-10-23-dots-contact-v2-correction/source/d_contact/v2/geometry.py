"""Arrival-distance predictions only; not an electrochemical performance simulation."""
import numpy as np,json,time,resource
from pathlib import Path
start=time.monotonic();out=[]
for n in [600,1200,2400]:
 # deterministic equal-area polar quadrature; no fitted rate.
 r=np.sqrt((np.arange(n)+.5)/n)[:,None];theta=2*np.pi*(np.arange(n)+.5)/n
 x=r*np.cos(theta);y=r*np.sin(theta)
 center=np.broadcast_to(r,(n,n))
 four=np.sqrt((abs(x)-.5)**2+(abs(y)-.5)**2)
 ring=abs(r-.5)
 # A contact ring at radius R/2 and a single diametral line are idealized boundaries.
 line=abs(y)
 for name,d,tmax in [('center',center,1),('four',four,2**-.5),('ring',ring,.5),('line',line,1)]:
  mean=float(d.mean());mean2=float((d*d).mean())
  out.append(dict(n=n,geometry=name,max_distance_exact=tmax,mean_distance=mean,metal_exposure_constant_speed=tmax-mean,metal_exposure_diffusive=tmax*tmax-mean2,mean_distance_squared=mean2))
res={'scope':'Normalized zero-width contacts, disk R=1, homogeneous deterministic arrival; HER proxy proportional to already-converted volume; this is not measured HER area or actual electrolyte kinetics. No claimed rate/saving.','results':out,'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_name('geometry_result.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
