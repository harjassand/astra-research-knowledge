"""Exact finite full-record check plus proved heat-kernel resource arithmetic."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math

STATES=list(product(range(2), repeat=3))  # y,z,s
INDEX={x:i for i,x in enumerate(STATES)}
DIM=len(STATES)

def mm(a,b):
    return [[sum(a[i][h]*b[h][j] for h in range(DIM))
             for j in range(DIM)] for i in range(DIM)]

def kernel(j):
    t=[[F(0) for _ in STATES] for _ in STATES]
    cross={0:{0:(F(1,8),F(3,8)),1:(F(3,16),F(5,16))},
           1:{0:(F(1,8),F(5,8)),1:(F(1,4),F(1,2))}}[j]
    for i,(y,z,s) in enumerate(STATES):
        c=cross[s][z]
        r=F(1,8) if s==0 else F(1,16)
        t[i][INDEX[1-y,z,s]]=c
        t[i][INDEX[y,1-z,s]]=r
        t[i][i]=1-c-r
    assert all(sum(row)==1 and min(row)>=0 for row in t)
    assert all(t[i][h]==t[h][i] for i in range(DIM) for h in range(DIM))
    return t

T=[kernel(0),kernel(1)]
R=[[F(int(x[0]==v[0] and x[2]==v[2]),2) for v in STATES] for x in STATES]
I=[[F(int(i==j)) for j in range(DIM)] for i in range(DIM)]
p=F(7,8)
Ap=[[p*R[i][j]+(1-p)*I[i][j] for j in range(DIM)] for i in range(DIM)]
exact=[mm(R,t) for t in T]
approx=[mm(Ap,t) for t in T]
P=[F(1,4),F(3,8)]

for j in range(2):
    for i,(y,z,s) in enumerate(STATES):
        flip=sum(exact[j][i][h] for h,x in enumerate(STATES) if x[0]!=y)
        assert flip==P[j]

def visible_records(kernels, policy, start, n=3):
    # Binary action tree in heap order: children depend on actual next label.
    masses={(): [F(int(i==start)) for i in range(DIM)]}
    for depth in range(n):
        nxt={}
        for hist,mass in masses.items():
            idx=(1<<depth)-1+sum(v*(1<<(depth-1-l)) for l,v in enumerate(hist))
            j=policy[idx]
            moved=[sum(mass[i]*kernels[j][i][h] for i in range(DIM)) for h in range(DIM)]
            for y in range(2):
                nxt[hist+(y,)]=[v if STATES[h][0]==y else F(0) for h,v in enumerate(moved)]
        masses=nxt
    return {hist:sum(mass) for hist,mass in masses.items()}

def reference_records(policy, y0=0, n=3):
    masses={():F(1)}
    for depth in range(n):
        nxt={}
        for hist,mass in masses.items():
            idx=(1<<depth)-1+sum(v*(1<<(depth-1-l)) for l,v in enumerate(hist))
            j=policy[idx]
            y=hist[-1] if hist else y0
            for a in range(2):
                nxt[hist+(a,)]=mass*(P[j] if a!=y else 1-P[j])
        masses=nxt
    return masses

def tv(a,b): return sum(abs(a[k]-b[k]) for k in a)/2

max_exact=F(0)
max_approx=F(0)
max_joint_approx=F(0)
arg=None
for policy in product(range(2),repeat=7):
    ref=reference_records(policy)
    joint=F(0)
    for z,s in product(range(2),repeat=2):
        start=INDEX[0,z,s]
        err=tv(visible_records(exact,policy,start),ref)
        err_ap=tv(visible_records(approx,policy,start),ref)
        max_exact=max(max_exact,err)
        joint+=err_ap/4
        if err_ap>max_approx:
            max_approx=err_ap
            arg={'policy':policy,'initial_z':z,'frozen_s':s}
    max_joint_approx=max(max_joint_approx,joint)

delta=(1-p)/2
bound=1-(1-delta)**3
assert max_exact==0
assert max_approx<=bound

# Native one-action law from y=0, uniform z, fixed s is not Markov in y.
raw={}
for s in range(2):
    pr=F(0)
    for z in range(2):
        start=INDEX[0,z,s]
        rec=visible_records(T,(0,)*7,start)
        pr+=sum(v for hist,v in rec.items() if hist[:2]==(1,1))/2
    raw[str(s)]={'P_y1_1_y2_1':str(pr),'Markov_prediction':str(P[0]*(1-P[0])),
                 'discrepancy':str(abs(pr-P[0]*(1-P[0])))}
assert raw['0']['P_y1_1_y2_1']!=raw['1']['P_y1_1_y2_1']

# Retained key and reused-key failures. Averaging is valid only at its interface.
key_retained_tv=(abs(F(1,8)-P[0])+abs(F(3,8)-P[0]))/2
key_kernels=[]
for c in range(2):
    fc=[[F(int(v==(x[0],x[1]^c,x[2]))) for v in STATES] for x in STATES]
    key_kernels.append([mm(fc,t) for t in T])
policy=(0,)*7
start=INDEX[0,0,0]
reuse_laws=[visible_records(ks,policy,start) for ks in key_kernels]
reuse_law={h:(reuse_laws[0][h]+reuse_laws[1][h])/2 for h in reuse_laws[0]}
reused_key_tv=tv(reuse_law,reference_records(policy))
assert key_retained_tv>0 and reused_key_tv>0

resources=[]
Dtau=F(1,100)
eps=1e-3
for n in (10,1000,1_000_000,1_000_000_000_000):
    b=0
    while True:
        m=1<<b
        x=float(Dtau)*m*m
        delta_heat=math.exp(-x)/(-math.expm1(-3*x))
        if n*delta_heat<=eps: break
        b+=1
    resources.append({'stages':n,'target_TV':eps,'D_tau':str(Dtau),'bits_per_stage':b,
                      'phase_options':m,'local_analytic_upper_bound':delta_heat,
                      'full_record_analytic_upper_bound':n*delta_heat,
                      'phase_spacing_radians':2*math.pi/m})

result={'scope':'Exact population algebra; not physical trials or finite-sample acquisition',
        'microscopic_states':DIM,'frozen_s':True,'policies':128,'old_hidden_histories':4,
        'record_depth':3,'max_exact_full_record_TV':str(max_exact),
        'approximate_scramble_probability':str(p),'local_TV_bound':str(delta),
        'full_record_bound':str(bound),'max_approx_conditional_TV':str(max_approx),
        'max_approx_conditional_TV_decimal':float(max_approx),
        'max_joint_old_record_TV':str(max_joint_approx),'argmax':arg,
        'raw_native_nonmarkov_witness':raw,'finite_bit_heat_resource_table':resources}
result['retained_current_key_one_stage_TV']=str(key_retained_tv)
result['same_key_reused_three_stages_TV']=str(reused_key_tv)
out=Path(__file__).with_name('OPERATIONAL_SCRAMBLING_CHECKS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
