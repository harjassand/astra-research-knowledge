"""Exact native-bank and adaptive scalar checks. No quantum yield simulation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def rotation(q):
 w,x,y,z=map(F,q)
 assert w*w+x*x+y*y+z*z==1
 return [[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]]
qs=[[1,0,0,0],[F(3,5),F(4,5),0,0],[0,0,0,1]]
checks=0
for q in qs:
 C=rotation(q)
 for source in ['identity','reset00']:
  mean=F(0);mass=F(0)
  for a,b,c,d in product(range(3),repeat=4):
   for u,v,y,z in product([-1,1],repeat=4):
    if source=='identity':py=F(1+u*y*(a==c),2);pz=F(1+v*z*(b==d),2)
    else:py=F(1+y*(a==2),2);pz=F(1+z*(b==2),2)
    prob=py*pz/324
    hat=F(3,4)-F(9,4)*y*z*C[a][b]-F(81,4)*y*z*u*v*C[a][b]*C[c][d]
    assert F(-87,4)<=hat<=F(93,4)
    mass+=prob;mean+=prob*hat;checks+=1
  assert mass==1
  expected=F(0) if source=='identity' else F(3,4)-C[2][2]/4
  assert mean==expected
# Exhaustive adaptive histories, including noisy sign estimators, current-action randomization and stopped suffix.
p=F(1,3);states=[(0,0,F(0),F(0),0)];centers=0;paths=0
for t in range(5):
 nxt=[]
 for memory,services,selected,observed,stop in states:
  if stop:nxt.append((memory,services,selected,observed,1));continue
  for candidate in [0,1]:
   loss=F((memory+candidate)%3,2);conditional=F(0)
   for role,rp in [('learn',p),('service',1-p)]:
    for noise in [-1,1]:
     estimate=loss+noise;W=estimate/p if role=='learn' else F(0)
     conditional+=rp*(loss-W)/2
     newservices=services+(role=='service');newmemory=(memory+candidate+noise+(role=='learn'))%3
     nxt.append((newmemory,newservices,selected+loss,observed+W,int(newservices>=2)))
     paths+=1
   assert conditional==0;centers+=1
 states=nxt
# Explicit invalid ordering witness: choose current action after seeing fresh sign.
# Two zero-mean estimates +Z/-Z; hindsight current action selects -|Z|, while actual loss stays zero.
assert sum(min(F(z),-F(z)) for z in [-1,1])/2==-1
out={'native_record_checks':checks,'adaptive_conditional_centering_checks':centers,'adaptive_extensions':paths,'final_histories':len(states),'current_outcome_selection_counterexample_mean':-1,'scope':'Exact arithmetic/conditional-centering checks, not hardware, practical yield or a replacement for governing proof.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
