"""Exact rational check of overlapping arbitrary-node cumulative meter reduction.
This checks the physical finite-bin algebra, not a microscopic source simulation.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json,math
import numpy as np

HERE=Path(__file__).resolve().parent
nodes=[F(0),F(1,100),F(3,100),F(7,25),F(11,20),F(1)]
w=F(1,20)
n=7
M=len(nodes)
d=w/n
Fc=lambda t:t+t*t/2-F(2,3)*t**3
Xc=lambda t:t*t/10+t**4/4
Fmax=F(4)
Xmax=F(2)
force_events=defaultdict(lambda:defaultdict(F))
position_events=defaultdict(lambda:defaultdict(F))
separate=[]
force_exact=[]
position_exact=[]
for i,t in enumerate(nodes):
    value=F(0)
    for r in range(2*n):
        mid=F(2*r+1,2*n)
        psi=mid if r<n else 2-mid
        theta=psi/w
        a=t+r*d;b=a+d
        force_events[a][i]-=theta
        force_events[b][i]+=theta
        value+=theta*(Fc(b)-Fc(a))
    separate.append(value)
    force_exact.append(1+t+w-2*(t*t+2*t*w+F(7,6)*w*w))
    position_exact.append(F(1,5)+3*(t*t+2*t*w+F(7,6)*w*w))
    for endpoint,coefficient in [(t,1/w**2),(t+w,-2/w**2),(t+2*w,1/w**2)]:
        position_events[endpoint][i]+=coefficient

def accumulate(events,primitive):
    out=[F(0)]*M
    for t,items in sorted(events.items()):
        value=primitive(t)
        for i,coef in items.items():
            out[i]+=coef*value
    return out

force_merged=accumulate(force_events,Fc)
pos_merged=accumulate(position_events,Xc)
assert force_merged==separate
assert pos_merged==position_exact
assert all(abs(a-b)<=Fmax/n for a,b in zip(force_merged,force_exact))

def gram(events):
    theta=np.zeros(M)
    covariance=np.zeros((M,M))
    prev=None
    for t,items in sorted(events.items()):
        if prev is not None:
            covariance+=float(t-prev)*np.outer(theta,theta)
        for i,c in items.items():
            theta[i]-=float(c)
        prev=t
    assert np.max(np.abs(theta))<1e-10
    return covariance

CF=gram(force_events)
CX=gram(position_events)
assert np.allclose(np.diag(CF),float((F(2,3)-F(1,6*n*n))/w))
assert np.allclose(np.diag(CX),float(2/w**3))
assert np.min(np.linalg.eigvalsh(CF+CX))>-1e-8

clock=F(1,500)
tau=clock/2

def rounded_time(t):
    v=t/clock+F(1,2)
    return (v.numerator//v.denominator)*clock

def round_events(events):
    result=defaultdict(lambda:defaultdict(F))
    for t,items in events.items():
        for i,c in items.items():
            result[rounded_time(t)][i]+=c
    return result

FR=round_events(force_events)
XR=round_events(position_events)
force_round=accumulate(FR,Fc)
pos_round=accumulate(XR,Xc)
force_clock_error=max(abs(a-b) for a,b in zip(force_round,force_merged))
pos_clock_error=max(abs(a-b) for a,b in zip(pos_round,pos_merged))
assert force_clock_error<=2*Fmax*tau/w
assert pos_clock_error<=4*Xmax*tau/w**2
CFR=gram(FR);CXR=gram(XR)
force_proxy=(math.sqrt(2/(3*float(w)))+2*math.sqrt(float(tau))/float(w))**2
pos_proxy=(math.sqrt(2/float(w)**3)+4*math.sqrt(float(tau))/float(w)**2)**2
assert np.max(np.diag(CFR))<=force_proxy+1e-8
assert np.max(np.diag(CXR))<=pos_proxy+1e-8
endpoints=sorted(set(force_events)|set(position_events))
result={
 'rational_nodes':[str(t) for t in nodes], 'triangle_half_width':str(w),'force_subdivisions_per_half':n,
 'requested_force_boxes':2*n*M,'requested_position_boxes':2*M,
 'merged_endpoint_count':len(endpoints),
 'minimum_exact_endpoint_separation':str(min(b-a for a,b in zip(endpoints,endpoints[1:]))),
 'exact_merged_force_matches_separate_reduction':True,
 'exact_position_box_identity':True,
 'largest_force_midpoint_error':float(max(abs(a-b) for a,b in zip(force_merged,force_exact))),
 'force_quadrature_bound':float(Fmax/n),
 'overlap_noise':{'force_node_0_1_covariance':float(CF[0,1]),
                  'position_node_0_1_covariance':float(CX[0,1]),
                  'smallest_total_covariance_eigenvalue':float(np.min(np.linalg.eigvalsh(CF+CX)))},
 'finite_clock':{'tick':str(clock),'max_timing_error':str(tau),
                 'force_error':float(force_clock_error),'force_bound':float(2*Fmax*tau/w),
                 'position_error':float(pos_clock_error),'position_bound':float(4*Xmax*tau/w**2),
                 'maximum_force_noise_variance':float(np.max(np.diag(CFR))),'force_noise_proxy':force_proxy,
                 'maximum_position_noise_variance':float(np.max(np.diag(CXR))),'position_noise_proxy':pos_proxy}}
(HERE/'passive_arbitrary_node_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
