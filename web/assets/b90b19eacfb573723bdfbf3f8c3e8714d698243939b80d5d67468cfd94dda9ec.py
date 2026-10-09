import json,os,sys,time
import numpy as np
sys.path.insert(0,os.path.dirname(__file__))
from online_entropy import MutableHopfLax,Query,finite_volume_godunov,interval_average_from_grid
breaks=np.array([-3.,-1.,-.2,.8,2.,3.])
states=np.array([0.,.9,-.7,.45,0.])
sensors=[(-1.5,-1.1),(-.8,-.4),(-.1,.2),(.4,.7),(1.1,1.5)]
q=[]
for a,b in sensors:q += [Query(a,.35),Query(b,.35)]
e=MutableHopfLax(breaks,states,q)
exact=np.array([e.interval_average(2*k,2*k+1,b-a) for k,(a,b) in enumerate(sensors)])
out=[]
for r in (1,2,4,8,16):
 t0=time.perf_counter(); x,u=finite_volume_godunov(breaks,states,.35,0,refinement=r); elapsed=time.perf_counter()-t0
 pred=np.array([interval_average_from_grid(x,u,a,b) for a,b in sensors])
 out.append({'refinement':r,'N_x':len(x),'max_sensor_mean_abs_error':float(np.max(np.abs(pred-exact))), 'rms_sensor_mean_abs_error':float(np.sqrt(np.mean((pred-exact)**2))), 'forward_seconds':elapsed})
print(json.dumps({'exact_sensor_means':exact.tolist(),'fv':out},indent=2))
