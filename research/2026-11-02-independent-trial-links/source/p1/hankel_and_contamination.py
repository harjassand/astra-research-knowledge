#!/usr/bin/env python3
"""Exact Hankel rank implications and an invisible high-propensity contaminant."""
import json
from fractions import Fraction as F
from math import sqrt

def det3(h):
 a,b,c=h[0]; d,e,f=h[1];g,i,j=h[2]
 return a*(e*j-f*i)-b*(d*j-f*g)+c*(d*i-e*g)

def moments(p,w,maxn=4):
 return [sum(wj*pj**k for wj,pj in zip(w,p)) for k in range(maxn+1)]
p2=[F(7,10),F(1,20)];w2=[F(1,2),F(1,2)]
p3=[F(1,10),F(1,2),F(9,10)];w3=[F(1,3)]*3
m2=moments(p2,w2);m3=moments(p3,w3)
h2=[[m2[i+j] for j in range(3)] for i in range(3)]
h3=[[m3[i+j] for j in range(3)] for i in range(3)]
assert det3(h2)==0 and det3(h3)>0
# A law with epsilon mass at an unseen stable higher-propensity mode.
eps=F(1,10**9); p_rare=F(99,100)
pa=[F(4,5),F(13,200)]; pb=[F(18,25),F(11,50)]
L=75
yA2=sum(w*p**(L-1)*a for w,p,a in zip(w2,p2,pa))
yB2=sum(w*p**(L-1)*b for w,p,b in zip(w2,p2,pb))
yAc=(1-eps)*yA2 + eps*p_rare**(L-1)*F(2,5)
yBc=(1-eps)*yB2 + eps*p_rare**(L-1)*F(1,2)
assert yA2>yB2 and yAc<yBc
# The total shifts in observed short assays are <= 1e-9 because each probability in [0,1]
res={'two_mode_moments':[str(t) for t in m2],'two_mode_Hankel3_det':str(det3(h2)),
     'three_mode_moments':[str(t) for t in m3],'three_mode_Hankel3_det':str(det3(h3)),
     'contamination_epsilon':str(eps),'rare_mode_baseline':str(p_rare),
     'short_assay_shift_absolute_upper':float(eps),
     'L':L,'clean_A':float(yA2),'clean_B':float(yB2),
     'contaminated_A':float(yAc),'contaminated_B':float(yBc),
     'contamination_flips_decision':bool(yA2>yB2 and yAc<yBc),
     'third_mode_long_total_contribution_scale':float(eps*p_rare**(L-1)),
     'type':'exact rational proof of sign flip; short experimental shift only bounded analytically'}
with open('producer-workspace/hankel_and_contamination_results.json','w') as f:json.dump(res,f,indent=2)
print(json.dumps(res,indent=2))
