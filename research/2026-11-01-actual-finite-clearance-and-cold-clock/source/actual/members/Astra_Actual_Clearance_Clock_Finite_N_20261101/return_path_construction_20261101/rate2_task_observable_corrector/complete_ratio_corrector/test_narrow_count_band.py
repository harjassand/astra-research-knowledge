#!/usr/bin/env python3
"""Exact rational replay of the outward states under narrow count bands.
This is not a uniform positivity proof or a probability claim for the count band.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib, sys
from exact_fraction_coefficients import h1,h2,h3,c0,c1,c2,c3
sys.set_int_max_str_digits(0)
P=Path(__file__).parent
rows=[(1,1,0,0,1),(-1,-1,0,0,-1),(-1,F(-1,2),0,1,0),(1,F(1,2),0,-1,0),(-1,F(-1,2),0,-1,0),(1,F(1,2),0,1,0),(-1,-1,1,0,0),(1,1,-1,0,0),(-1,0,-1,0,0),(1,0,1,0,0),(1,0,0,0,0),(-1,0,0,0,0)]
def iroot5(n):
 lo=0;hi=1
 while hi**5<=n:hi*=2
 while hi-lo>1:
  md=(lo+hi)//2
  if md**5<=n:lo=md
  else:hi=md
 assert lo**5<=n<(lo+1)**5
 return lo
hf=[h1,h2,h3];cf=[c0,c1,c2,c3]
def chi(x):rr,uu,tt,aa,zz,ss=x;return sum(fn(rr,uu,tt,zz,ss)*aa**j for j,fn in enumerate(hf,1))
def value(x):rr,uu,tt,aa,zz,ss=x;return rr*(1-aa*uu)+chi(x)
def moved(x,j):
 rr,uu,tt,aa,zz,ss=x;da,dl,de,dz,dn=j;ch=1+de*uu*tt/rr;lh=1+dl*tt
 return rr*ch*ch/lh,uu*ch,tt/lh,(aa+tt*da)/lh,(zz+tt*dz)/lh,ss+dn*uu*uu*tt/rr
def rates(x):
 rr,uu,tt,aa,zz,ss=x;cd=(1-aa)**2-zz*zz/4
 return [tt*tt,aa*tt,aa*(aa-tt),aa*(1-aa+zz/2),aa*(aa-tt),aa*(1-aa-zz/2),aa*(aa-tt),aa*rr/uu,aa*rr/uu,2*cd,cd,aa*(ss*rr/uu**2-2+aa-rr/uu)]
def gen(x):return sum(rate*(value(moved(x,j))-value(x))/(x[1]*x[2]) for rate,j in zip(rates(x),rows))
records=[]
for q,rr in [(6,F(2)),(8,F(1,2))]:
 LL=10**q;uu=F(1,10**q);NN=int(rr*LL/uu**2);EE=int(uu*NN);AA=LL//100;CC=DD=LL-AA
 TT=iroot5(NN);constant=100
 for sign in (-1,0,1):
  SS=NN+sign*constant*TT;BB=SS-AA-CC-DD-EE
  x=(rr,uu,F(1,LL),F(1,100),F(0),F(SS,NN));g=gen(x)
  assert abs(SS-NN)**5<=constant**5*NN
  lo,hi=(F(-3),F(-1)) if rr==2 else (F(2),F(3))
  assert lo<g<hi
  records.append({'counts':dict(N=NN,A=AA,B=BB,C=CC,D=DD,E=EE,S=SS,L=LL,Z=0),'C':constant,'floor_N_fifth_root':TT,'count_deviation':SS-NN,'exact_drift_interval':[str(lo),str(hi)],'normalized_drift_approx':float(g),'fraction_sha256':hashlib.sha256((str(g.numerator)+'/'+str(g.denominator)).encode()).hexdigest(),'domain_and_narrow_band_checks':'EXACT_PASS'})
  print('NARROW',rr,'S-N',SS-NN,'normalized drift',float(g),flush=True)
report={'status':'ALL_SIX_REPLAYED_WITNESSES_HAVE_INWARD_SIGN','method':'exact Fraction arithmetic, no floating-point sign acceptance','C':100,'records':records,'scope':'The broad-band counterexamples disappear at these same states with S=N and |S-N|<=100 N^(1/5). This is not a uniform theorem, and the count-band event/entrance charge must be supplied by the original count ledgers.'}
(P/'narrow_count_band_replays.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'])
