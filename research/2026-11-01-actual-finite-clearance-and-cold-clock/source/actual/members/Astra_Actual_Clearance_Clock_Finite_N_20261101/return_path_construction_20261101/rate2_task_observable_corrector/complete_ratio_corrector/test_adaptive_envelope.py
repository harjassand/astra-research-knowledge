#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json
from rational_runtime import rows,chi,val,moved,rates,mean,cert
P=Path(__file__).parent
def root5(n):
 lo=0;hi=1
 while hi**5<=n:hi*=2
 while hi-lo>1:
  m=(lo+hi)//2
  if m**5<=n:lo=m
  else:hi=m
 return lo
records=[]
for rr,uu,LL in [(F(2),F(1,10**6),10**6),(F(1,2),F(1,10**8),10**8),(F(1,2),F(128,10**16),10**8),(F(51,100),F(128,10**16),10**8)]:
 NN=int(rr*LL/uu**2);EE=int(uu*NN)
 cap=F(LL**3*EE,100*NN);AA=min(LL//100,isqrt(cap.numerator//cap.denominator));CC=DD=LL-AA
 TT=root5(NN)
 for sign in (-1,0,1):
  SS=NN+sign*100*TT;BB=SS-AA-CC-DD-EE
  x=(rr,uu,F(1,LL),F(AA,LL),F(0),F(SS,NN));g=sum(rate*(val(moved(x,j))-val(x))/(uu*x[2]) for rate,(name,j) in zip(rates(x),rows))
  theta=F(AA*AA*NN,LL**3*EE)
  assert theta<=F(1,100) and abs(SS-NN)**5<=100**5*NN
  assert (g<0 if rr>1 else g>0)
  records.append({'R':str(rr),'u':str(uu),'counts':dict(N=NN,A=AA,B=BB,C=CC,D=DD,E=EE,S=SS,L=LL),'theta_A':str(theta),'S_minus_N':SS-NN,'normalized_drift':cert(g),'status':'EXACT_INWARD_SIGN_PASS'})
  print('ADAPTIVE',rr,'L',LL,'A',AA,'S-N',SS-NN,'theta',float(theta),'drift',float(g),flush=True)
report={'status':'ALL_12_EXACT_REPLAYS_INWARD','scope':'Pointwise exact replay only, not the uniform theorem and not a probability statement for the adaptive/count gates.','records':records}
(P/'adaptive_exact_replays.json').write_text(json.dumps(report,indent=2)+'\n')
