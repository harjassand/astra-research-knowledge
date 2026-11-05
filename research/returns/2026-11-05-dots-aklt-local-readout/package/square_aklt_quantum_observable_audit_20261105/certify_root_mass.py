"""Reconstruct an exact root generating-function bound from the saved witness."""
from pathlib import Path
from fractions import Fraction as F
import numpy as np,sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'square_aklt_loop_audit_20261105'))
from weighted_trail_bound import enumerate_states,D,edge,build
base=ROOT/'square_aklt_loop_audit_20261105';z=np.load(base/'resolvent_tau0p06.npz');m=int(z['m']);nums=z['q'].astype(object);den=int(z['q_den']);rp=int(z['r_num']);rd=int(z['r_den'])
states,to,w=build(m)
assert np.all(5*rd*z['q']>=5*rd*den+rp*(w*z['q'][to]).sum(1))
for k in range(m-1,0,-1):
 prev=enumerate_states(k);ix={d:i for i,d in enumerate(states)};vals=[]
 for ds in prev:
  ps=[(0,0)]
  for d in ds:ps.append((ps[-1][0]+D[d][0],ps[-1][1]+D[d][1]))
  used={edge(ps[i],ps[i+1])for i in range(k)};inside=set(ps[1:-1]);tot=0
  for j,(dx,dy)in enumerate(D):
   p=(ps[-1][0]+dx,ps[-1][1]+dy)
   if edge(ps[-1],p)not in used:tot+=(3 if p in inside else 5)*nums[ix[ds+(j,)]]
  vals.append(5*rd*den+rp*tot)
 nums=np.array(vals,dtype=object);den*=5*rd;states=prev
root=1+4*F(rp,rd)*F(int(nums[0]),den);cap=F(12246,125)
assert root<cap
out={'tau':'3/50','root_mass_exact':str(root),'convenient_upper':str(cap),'convenient_upper_decimal':float(cap),'spin_correlation_prefactor':str(9*cap),'quadrupole_prefactor':str(F(42,5)*cap)}
Path(__file__).with_name('root_mass_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
