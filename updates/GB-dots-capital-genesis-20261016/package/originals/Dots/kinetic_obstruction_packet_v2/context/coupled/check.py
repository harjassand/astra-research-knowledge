from fractions import Fraction as R
from math import prod
import json
D=R('8.2207');b=lambda n:R('2.676')*n*(n-1)+R('108.102');a=lambda n:R('.040')*n*(n-1)*(n-2)+R('37.881')*n
edges=[(i,j) for i in range(8) for j in range(i+1,8) if abs(i//4-j//4)+abs(i%4-j%4)==1]
deg=[sum(i in e for e in edges) for i in range(8)]
fall=lambda n,k:prod(n-j for j in range(k))
def stats(x):
 S=sum(x);F2=sum(fall(n,2) for n in x)
 return S,F2,8*(F2+S)-S*S

def direct(x):
 old=stats(x);out=[R(0)]*3
 def jump(y,q):
  sy=stats(y)
  for k in range(3):out[k]+=q*(sy[k]-old[k])
 for i in range(8):
  y=x.copy();y[i]+=1;jump(y,b(x[i]))
  if x[i]:y=x.copy();y[i]-=1;jump(y,a(x[i]))
 for i,j in edges:
  for u,v in [(i,j),(j,i)]:
   if x[u]:y=x.copy();y[u]-=1;y[v]+=1;jump(y,D*x[u])
 return out
states=[[50]*8,[60]*8,[16,0,0,0,0,0,0,0],[0,16,0,0,0,0,0,0],[20,0,3,3,0,0,0,0],[20,1,1,4,0,0,0,0],[162,1,20,9,43,0,150,25]]
for x in states:
 S,F2,C=stats(x);F3=sum(fall(n,3) for n in x);F4=sum(fall(n,4) for n in x)
 B=sum(b(n) for n in x);A=sum(a(n) for n in x)
 QS=-R('.040')*F3+R('2.676')*F2-R('37.881')*S+R('864.816')
 QF2=-R('.080')*F4+R('5.192')*F3-R('65.058')*F2+R('216.204')*S+2*D*(sum(deg[i]*x[i] for i in range(8))-sum((x[i]-x[j])**2 for i,j in edges))
 QC=8*QF2+(8-2*S)*QS-(B+A)
 assert direct(x)==[QS,QF2,QC]
x,y=states[4:6];assert stats(x)==stats(y);assert direct(y)[0]-direct(x)[0]==-R(12,25)
assert stats(states[2])==stats(states[3]);assert direct(states[2])[1]!=direct(states[3])[1]
m=60;c_theta=8*(a(m)-b(m));c_eta=56*(a(m)+b(m))+320*D*m
assert c_theta>280 and c_eta>0
print(json.dumps({'generator_checks':len(states),'same_S_C_different_total_drift_exact':'-12/25','uniform_60_birth_exact':str(b(m)),'uniform_60_death_exact':str(a(m)),'lambda_theta_lower_coefficient':str(c_theta),'lambda_eta_lower_coefficient':str(c_eta),'log_initial_envelope_theta_lower_coefficient':str(c_theta-280),'minimal_family_initial_value_at_least_one':True},indent=2))
