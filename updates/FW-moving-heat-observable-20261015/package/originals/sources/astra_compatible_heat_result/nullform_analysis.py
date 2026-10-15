from reconstruct import *
from itertools import permutations
T=s.symbols('T012 T013 T023 T123')
trip=list(combinations(range(4),3))
def signperm(v):return (-1)**sum(v[i]>v[j] for i in range(len(v)) for j in range(i+1,len(v)))
Tdict={}
for tr,tt in zip(trip,T):
 for prm in permutations(tr):Tdict[prm]=signperm(prm)*tt
# t_i=d omega(e_i,B1,B2)
tvec=[s.expand(sum(Tdict.get((i,k,l),0)*B1[k]*B2[l] for k in range(4) for l in range(4))) for i in range(4)]
# only terms involving third derivatives (T is frozen at A)
y=s.symbols('y0:8') # phi1 xxx,xxy,xyy,yyy then phi2
zx=[y[0],y[1],y[2],y[4],y[5],y[6]]
zy=[y[1],y[2],y[3],y[5],y[6],y[7]]
def dx(p):return s.expand(sum(s.diff(p,z[i])*zx[i] for i in range(6)))
def dy(p):return s.expand(sum(s.diff(p,z[i])*zy[i] for i in range(6)))
e1=dx(tvec[0])+dy(tvec[1]);e2=dx(tvec[2])+dy(tvec[3])
print('tvec',tvec)
print('E1 third part',s.factor(e1));print('E2 third part',s.factor(e2))
for idx,ei in enumerate([e1,e2]):
 print('E',idx)
 for mon,coef in s.Poly(ei,*list(z),*y).terms():
  if coef!=0:print(mon,coef)
