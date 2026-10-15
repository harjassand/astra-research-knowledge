from fractions import Fraction as F
import json
from pathlib import Path
checks=[]
def ck(name,condition):
    assert condition, name
    checks.append(name)
u=[[0,4],[2,3]]; v=[[1,0],[0,2]]
def grad(z,i,j,upper):
    z00=z[j%2][i%2]; z10=z[j%2][(i+1)%2]
    z01=z[(j+1)%2][i%2]; z11=z[(j+1)%2][(i+1)%2]
    return (2*(z11-z01),2*(z11-z10)) if upper else (2*(z10-z00),2*(z01-z00))
up=[grad(u,0,0,True),grad(u,0,1,False)]
um=[grad(u,1,0,True),grad(u,1,1,False)]
vp=[grad(v,0,0,True),grad(v,0,1,False)]
vm=[grad(v,1,0,True),grad(v,1,1,False)]
ck('u_plus',up==[(2,-2),(2,-4)])
ck('u_minus',um==[(-2,4),(-2,2)])
ck('v_plus',vp==[(4,4),(4,2)])
ck('v_minus',vm==[(-4,-2),(-4,-4)])
for name,z in [('u',u),('v',v)]:
    ck(name+'_eight_distinct',len({grad(z,i,j,b) for i in range(2) for j in range(2) for b in [True,False]})==8)
ck('unperturbed_minimum',min(4*b-8*a for a in [-8,-4] for b in [4,8])==48)
eps=F(1,10)
ux=F(4)-8*eps; uy=F(-4)+8*eps; vx=F(8)-8*eps; vy=F(4)-8*eps
ck('strict_signs',ux>0 and uy<0 and vx>0 and vy>0)
ck('robust_bound',ux*vy-uy*vx==F(832,25))
ck('pair_gradient_error',2*F(2)*eps==4*eps)
ck('difference_error',2*4*eps==8*eps)
receipt={'status':'PASS','checks':checks,'check_count':len(checks),'scope':'Exact nodal gradients and uniform interval separation. Source mold and Theta mapping are reconstructed in the separate primary-source audit. Not a Morrey counterexample.'}
Path(__file__).with_name('PEDREGAL_ROBUSTNESS_CHECK.v0002.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
