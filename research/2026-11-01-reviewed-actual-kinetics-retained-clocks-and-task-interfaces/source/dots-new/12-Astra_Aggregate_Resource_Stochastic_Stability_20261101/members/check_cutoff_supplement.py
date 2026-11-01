"""Additional actual-jump cutoff checks, with synthetic widths only.
Frozen82-member author source is read, never edited. This is not full-tail testing.
"""
from fractions import Fraction as F
from copy import deepcopy
import json
import aggregate_mass as A
G=A.G
counts=dict(states=0,positive_cutoff_jumps=0,zero_crossings=0,one_crossings=0,last_copy_deaths=0,core_death_resource_two=0)
for nf in (1,2):
 r=A.recognize(A.fixture(nf));p=A.tail_plan(r,F(2))
 for K in (8,17):
  sp=deepcopy(p);sp['mass']['K']=K;hd=A.geometric_head(sp,r);rho=sp['mass']['rho'];CZ=hd['C']*hd['Q']**K+2+rho/2
  def coords(x):
   aa=x[r['a']];ff=sum(x[v]for v in r['free']);uu=sum(x)-ff;return aa,ff,uu,uu+aa
  def Z(x):
   aa,ff,uu,j=coords(x);return A.mass_g(sp,hd,j)-1+rho*F(aa,(j+1)**2)
  for width in (1,2,7):
   L0=4
   def phi(x):
    aa,ff,uu,j=coords(x);return max(F(0),min(F(1),(G.dyadic(ff+1)-G.dyadic(uu+1)-L0)/width))
   for U in (0,1,2,3,8,17,100):
    for aa in sorted(set((0,min(1,U),min(2,U),U))):
     for pattern in ('pure','mixed'):
      base=[0]*r['n'];base[r['a']]=aa;left=U-aa
      if pattern=='pure':base[r['rare'][0]]=left
      else:
       for v in r['rare']:base[v]=left//len(r['rare'])
       base[r['rare'][0]]+=left-sum(base[v]for v in r['rare'])
      for power in (L0-1,L0,L0+width,L0+width+1):
       for off in (-1,0,1):
        x=list(base);f=max(0,((U+1)<<power)+off-1)
        for fi in r['free']:x[fi]=f//nf
        x[r['free'][0]]+=f-sum(x[v]for v in r['free']);x=tuple(x)
        ph=phi(x);cross=F(0)
        for src,dst,k in r['channels']:
         rate=k*G.C.B.falling(x,src)
         if not rate:continue
         y=tuple(a-b+c for a,b,c in zip(x,src,dst));pp=phi(y);d=pp-ph
         cross+=rate*sp['t']**(sum(dst)-sum(src))*Z(y)*d
         if d<=0:continue
         counts['positive_cutoff_jumps']+=1;counts['zero_crossings']+=int(ph==0);counts['one_crossings']+=int(pp==1 and ph<1)
         ap,fp,up,jp=coords(y);a,f,u,j=coords(x)
         if sum(dst)==sum(src)-1:
          assert jp==j-2 and j-1>=u and Z(y)<=CZ/F(u)
          assert rate*sp['t']**(-1)*Z(y)*d<=2*CZ*r['mu']/width
          counts['last_copy_deaths']+=int(a==1);counts['core_death_resource_two']+=1
         else:assert jp==j and fp==f+1 and up==u-1 and Z(y)<=CZ/F(u)
        assert cross<=4*CZ*(r['ell']*len(r['edges'])+r['mu'])/width
        counts['states']+=1
print(json.dumps(dict(status='PASS_AUTHOR_CUTOFF_SUPPLEMENT',counts=counts,scope='Synthetic widths and finite heads test the exact cutoff cross lemma, not the full acquired Foster certificate or huge global tail'),indent=2))
