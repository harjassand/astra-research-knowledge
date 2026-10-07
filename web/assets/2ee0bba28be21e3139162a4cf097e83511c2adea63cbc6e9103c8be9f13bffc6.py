#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import json,pathlib,time,math
ROOT=pathlib.Path(__file__).resolve().parent;t0=time.monotonic()
d=8;theta=F(1,2);groups=[[0,1,2],[3,4,5],[6,7]];m=len(groups)
def channel(x):
 out=[F(0)]*d
 for g in groups:
  avg=sum(x[i] for i in g)/len(g)
  for i in g:out[i]=avg
 return out
experiments=[];maxerr=F(0)
for plus in combinations(range(d),d//2):
 h=[F(1 if i in plus else -1) for i in range(d)]
 rho=[(1+theta*v)/d for v in h];out=channel(rho)
 err=sum(abs(a-b) for a,b in zip(rho,out))/2;maxerr=max(maxerr,err)
 assert sum(rho)==1 and min(rho)>0
 experiments.append({'h':list(map(int,h)),'coarse_EB_half_trace_error':str(err)})
h=list(map(F,[1,-1,0,1,-1,0,1,-1]))
assert sum(h)==0 and channel(h)==[F(0)]*d
rp=[(1+theta*v)/d for v in h];rm=[(1-theta*v)/d for v in h]
assert channel(rp)==channel(rm)
pairdist=sum(abs(a-b) for a,b in zip(rp,rm))/2
err=sum(abs(a-b) for a,b in zip(rp,channel(rp)))/2
assert pairdist==2*err
assert err>=theta*(d-m)/(2*d)
# The non-saturated kernel witness is the mean of two balanced sign vectors.
h1=h[:];h2=h[:];h1[2]=1;h1[5]=-1;h2[2]=-1;h2[5]=1
assert sum(h1)==sum(h2)==0 and [(a+b)/2 for a,b in zip(h1,h2)]==h
chi_bound=((1+float(theta))*math.log(1+float(theta))+(1-float(theta))*math.log(1-float(theta)))/2
out={'status':'DIAGNOSTIC_ONLY; GENERAL_BOUND_PROVED_IN_REVISION','d':d,'theta':str(theta),'finite_family_size':len(experiments),'EB_outcome_count':m,'coarse_channel_groups':groups,'exact_kernel_witness':list(map(str,h)),'exact_kernel_pair_trace_distance':str(pairdist),'exact_witness_error':str(err),'general_lower_bound':str(theta*(d-m)/(2*d)),'finite_family_max_coarse_EB_error':str(maxerr),'capacity_upper_nats_float_display':chi_bound,'capacity_exact_formula':'((1+theta)log(1+theta)+(1-theta)log(1-theta))/2','wall_seconds':time.monotonic()-t0}
(ROOT/'alphabet_cost_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
