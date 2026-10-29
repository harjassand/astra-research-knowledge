from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sympy as S
# Exact native quaternion offset identity, including the action-independent record term.
q=S.symbols('q0:4');w,x,y,z=q;Q=sum(a*a for a in q)
Rot=S.Matrix([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)], [2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)], [2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])
u=[S.Rational(1,3),S.Rational(1,4),S.Rational(1,5)];den=1+sum(a*a for a in u);quat=[(1-sum(a*a for a in u))/den]+[2*a/den for a in u]
qs=[[1,0,0,0],[S.Rational(3,5),S.Rational(4,5),0,0],quat];p=S.Rational(1,3);native_checks=0
for a,b,c,d in product(range(3),repeat=4):
 for yz,uv in product([-1,1],repeat=2):
  hp=S.Poly(-S.Rational(9,4)*yz*Q*Rot[a,b]-S.Rational(81,4)*yz*uv*Rot[a,b]*Rot[c,d],q)
  coeff=hp.as_dict();gsum=sum(2*v/p for v in coeff.values());offset=S.Rational(3,4)/p-gsum/2;vals=[]
  for qq in qs:
   action={exp:(S.prod(qq[j]**exp[j] for j in range(4))+1)/2 for exp in coeff}
   via=S.simplify(offset+sum((2*v/p)*action[exp] for exp,v in coeff.items()))
   rab=Rot[a,b].subs(dict(zip(q,qq)));rcd=Rot[c,d].subs(dict(zip(q,qq)))
   direct=(S.Rational(3,4)-S.Rational(9,4)*yz*rab-S.Rational(81,4)*yz*uv*rab*rcd)/p
   assert S.simplify(via-direct)==0, (a,b,c,d,yz,uv,qq,via,direct,S.simplify(via-direct))
   assert -S.Rational(87,4)/p<=via<=S.Rational(93,4)/p
   vals.append(via);native_checks+=1
  assert -S.Rational(87,4)/p<=sum(vals)/3<=S.Rational(93,4)/p
# Exact adaptive scalar histories: retrospective selector never enters the martingale.
R=F(2);p=F(1,2)
def phi(G):
 return F(0) if G>=R else (G if G<=-R else -(R-G)**2/(4*R))
def grad(G):return max(F(0),min(F(1),(R-G)/(2*R)))
# G, memory, Cobs, actual selected loss, Vobs, bias sum, Y sum
states=[(F(0),0,F(0),F(0),F(0),F(0),F(0))];checks=0;center_checks=0
for t in range(4):
 nxt=[]
 for G,mem,C,loss,V,bias,Ysum in states:
  ell=F(1 if mem%2==0 else -1);c_true=(1-ell)/2;a0=grad(G)
  choices=[F(int(G+zz<F(3,2))) for zz in [-R/2,R/2]];xb=sum(choices)/2;meanY=F(0)
  for xx in choices:
   for role,prob in [('learn',F(1,2)),('service',F(1,4)),('validate',F(1,4))]:
    g=ell/p if role=='learn' else F(0);c=c_true/p if role=='learn' else F(0)
    actual=c_true+ell*xx;bb=ell*(xb-a0);yy=actual-(c+g*a0)-bb;meanY+=prob*yy/2
    ns=(G+g,(mem+int(xx)+(role=='service'))%3,C+c,loss+actual,V+g*g,bias+bb,Ysum+yy)
    G2,_,C2,loss2,V2,bias2,Y2=ns
    for retrospective_action in [F(0),F(1),F(int(G2<0))]:
     empirical=C2+G2*retrospective_action
     assert loss2<=empirical+R/4+V2/(4*R)+bias2+Y2;checks+=1
    nxt.append(ns)
  assert meanY==0;center_checks+=1
 states=nxt
out={'scope':'Exact native record-offset identities and exhaustive adaptive scalar potential/martingale checks. No large quantum experiment or empirical expected-gap inference.','native_quaternion_checks':native_checks,'conditional_centering_states':center_checks,'retrospective_pathwise_inequalities':checks,'final_histories':len(states),'data_chosen_selector_handled_pathwise':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
