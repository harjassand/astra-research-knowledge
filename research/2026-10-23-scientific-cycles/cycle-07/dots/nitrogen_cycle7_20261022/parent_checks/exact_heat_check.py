"""Independent exact fixtures for heat availability and countercurrent pinch.
No thermochemical fitting or reactor trajectory. Python standard library.
"""
from fractions import Fraction as F
import json,time,resource
from pathlib import Path
start=time.perf_counter()
hot=[(F(300),F(400),F(1)),(F(400),F(500),F(10)),(F(500),F(600),F(1))]
cold=[(F(300),F(500),F(1)),(F(500),F(600),F(10))]
def H(T,stream):
 return sum(c*max(F(0),min(T,b)-a) for a,b,c in stream)
def T(h,stream):
 for a,b,c in stream:
  e=c*(b-a)
  if h<=e:return a+h/c
  h-=e
 raise ValueError('outside fixed fixture')
def min_gap(Q):
 # Gap is piecewise affine in q. Test all endpoints and every inverse-enthalpy breakpoint.
 q={F(0),Q}
 for a,b,c in hot:q.add(H(F(600),hot)-H(a,hot));q.add(H(F(600),hot)-H(b,hot))
 for a,b,c in cold:q.add(Q-H(a,cold));q.add(Q-H(b,cold))
 q=sorted(v for v in q if 0<=v<=Q)
 vals=[(v,T(H(F(600),hot)-v,hot)-T(Q-v,cold)) for v in q]
 return min(vals,key=lambda x:x[1]),vals
end_bound=min(H(F(600),hot)-H(F(320),hot),H(F(580),cold))
assert end_bound==1000
bad, _=min_gap(end_bound)
assert bad==(F(100),F(-70))
good, samples=min_gap(F(280))
assert good[1]==F(20)
# Necessity: at q=100 hot=500, so cold<=480 means Q-100<=Hcold480=180.
assert H(F(480),cold)+100==280
for eps in [F(1),F(1,1000),F(1,10**12)]:assert min_gap(280+eps)[0][1]<20
# Nonuniform enthalpy availability, [a-b]+ >= a-b, sum finite species parcels.
fixtures=[[(F(1),F(100),F(50))],[(F(1),F(100),F(50)),(F(1),F(0),F(50))],[(F(1,3),F(100),F(60)),(F(2,3),F(20),F(60))]]
checks=[]
for f in fixtures:
 avail=sum(w*max(F(0),a-b) for w,a,b in f)
 bound=max(F(0),sum(w*(a-b) for w,a,b in f))
 assert avail>=bound
 checks.append({'available':str(avail),'lower_bound':str(bound)})
out={'scope':'Exact conditional mathematical fixtures, not reactor heat capacities or performance','two_end_bound':str(end_bound),'violating_q_and_gap':[str(x) for x in bad],'exact_all_position_maximum_duty':'280','at_optimum_q_and_gap':[str(x) for x in good],'all_breakpoints_at_optimum':[[str(v),str(g)] for v,g in samples],'availability_checks':checks,'elapsed_seconds':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
