#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import json,pathlib,time,math
ROOT=pathlib.Path(__file__).resolve().parent;t0=time.monotonic()
d=8;q=2;theta=F(1,2);groups=[list(range(q))]+[[i] for i in range(q,d)];m=len(groups)
R=[[F(0) for _ in range(d)] for _ in range(d)]
for g in groups:
 for i in g:
  for j in g:R[i][j]=F(1,len(g))
assert all(sum(R[i][j] for i in range(d))==1 for j in range(d))
trace=sum(R[i][i] for i in range(d));assert trace==m
maxerr=F(0);hscores=[];fixtures=0
for plus in combinations(range(d),d//2):
 h=[F(1 if i in plus else -1) for i in range(d)]
 Rh=[sum(R[i][j]*h[j] for j in range(d)) for i in range(d)]
 err=theta*sum(abs(a-b) for a,b in zip(h,Rh))/(2*d)
 maxerr=max(maxerr,err);hscores.append(sum(a*b for a,b in zip(h,Rh))/d);fixtures+=1
assert maxerr==theta*q/(2*d)
assert sum(hscores)/len(hscores)==(trace-1)/(d-1)
eta=2*maxerr/theta;ad=eta*F(d-1,d)
assert trace>=d-eta*(d-1)
p=[F(len(g),d) for g in groups]
H=-sum(float(v)*math.log2(float(v)) for v in p)
h2=lambda v:0.0 if v in (0,1) else -v*math.log2(v)-(1-v)*math.log2(1-v)
lower=math.log2(d)-h2(float(ad))-float(ad)*math.log2(d-1)
formula=(1-float(F(q,d)))*math.log2(d)-float(F(q,d))*math.log2(float(F(q,d)))
assert abs(H-formula)<1e-12 and H>=lower
C=((1+float(theta))*math.log(1+float(theta))+(1-float(theta))*math.log(1-float(theta)))/2
result={'status':'EXACT_SMALL_DIAGNOSTIC; GENERAL_THEOREM_IN_REVISION','d':d,'q':q,'theta':str(theta),'family_size':fixtures,'exact_max_half_trace_error':str(maxerr),'eta':str(eta),'exact_trace_R':str(trace),'exact_average_balanced_capture':str(sum(hscores)/len(hscores)),'alphabet_bound':str(d-eta*(d-1)),'outcomes':m,'outcome_probabilities':list(map(str,p)),'outcome_entropy_bits_float':H,'entropy_lower_bound_bits_float':lower,'capacity_nats_float':C,'wall_seconds':time.monotonic()-t0}
(ROOT/'expected_record_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
