"""Independent rational boundary-witness and recovery-obstruction fixtures.

The decision oracle here is a specially solved qubit J_z^2 slice, not CAD.
It does not implement the general ellipsoid or rational SDP algorithm.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def closest_zero(interval):
    l,h=interval
    return l if l>0 else h if h<0 else F(0)

def feasible(box,u,N,theta):
    """Exact exists-state decision for F_W=1/(2N)+(N-1)/(2N) z_sigma^2.

    W=2 J_z^2/N^2 has operator norm1/2. Tau has entries a,b+ic,1-a.
    Minimize b^2+c^2 independently in their boxes; positivity is
    (2a-1)^2 <=1-4(b^2+c^2). This is a exact fixed-variable slice.
    """
    lo=max(box[0][0],F(0));hi=min(box[0][1],F(1))
    if lo>hi:return False
    q=closest_zero(box[1])**2+closest_zero(box[2])**2
    M=1-4*q
    if M<0:return False
    zl,zh=2*lo-1,2*hi-1
    base=F(1,2*N);k=F(N-1,2*N)*(1-2*theta)**2
    if u<=base:
        return zl<=0<=zh or (zl>0 and zl*zl<=M) or (zh<0 and zh*zh<=M)
    if k==0:return False
    need=(u-base)/k
    if need>M:return False
    positive=zh>=0 and zh*zh>=need and max(zl,F(0))**2<=M
    negative=zl<=0 and zl*zl>=need and min(zh,F(0))**2<=M
    return positive or negative

def run(N,theta,t):
    queries=0
    def yes(box,u):
        nonlocal queries
        queries+=1
        return feasible(box,u,N,theta)
    box=[(F(-1),F(1)) for _ in range(3)]
    lo,hi=F(-1,2),F(1,2)
    assert yes(box,lo)
    while hi-lo>t/8:
        mid=(lo+hi)/2
        if yes(box,mid):lo=mid
        else:hi=mid
    u=lo
    gamma=t/F(80*4*N)
    for j in range(3):
        while box[j][1]-box[j][0]>gamma:
            a,b=box[j];mid=(a+b)/2
            trial=box.copy();trial[j]=(a,mid)
            if yes(trial,u):box=trial
            else:
                trial[j]=(mid,b)
                assert yes(trial,u)
                box=trial
    Q=[(a+b)/2 for a,b in box]
    delta=t/F(20*2*N)
    den=1+4*delta
    ahat=(Q[0]+2*delta)/den
    bhat=Q[1]/den;chat=Q[2]/den
    assert ahat>=0 and ahat<=1 and ahat*(1-ahat)>=bhat*bhat+chat*chat
    scale=1-2*theta
    asigma=theta+scale*ahat
    bsigma=scale*bhat;csigma=scale*chat
    assert asigma>=theta and 1-asigma>=theta
    assert (asigma-theta)*(1-asigma-theta)>=bsigma*bsigma+csigma*csigma
    value=F(1,2*N)+F(N-1,2*N)*(2*asigma-1)**2
    optimum=F(1,2*N)+F(N-1,2*N)*scale*scale
    assert value>=optimum-t/4
    qdet=Q[0]*(1-Q[0])-Q[1]**2-Q[2]**2
    return {'N':N,'theta':str(theta),'tolerance':str(t),'queries':queries,
            'box_center_not_psd':qdet<0,'exact_repaired_state_psd':True,
            'exact_restricted_state_ge_theta':True,
            'near_max_error':str(optimum-value),'error_le_tolerance_over_4':True,
            'output_max_entry_bits':max(v.numerator.bit_length()+v.denominator.bit_length()
                                        for v in [asigma,bsigma,csigma]),
            'scope':'Exactly solved degree-two support slice; no general CAD/ellipsoid/SDP execution.'}

if __name__=='__main__':
    # General-theta counter to repairing Q directly by the unrestricted recipe.
    theta=F(3,8);delta=F(1,100);qmin=theta-delta
    bad=(qmin+2*delta)/(1+4*delta)
    assert bad==F(77,208) and bad<theta
    # N=1 pure target: true iid distance0, retained-only-white distance1/2.
    # A correct true-dual point (W=0,a=0) by itself cannot certify that list.
    out={'ordinary_direct_repair_counter':{'theta':str(theta),'Q_min':str(qmin),
             'delta':str(delta),'repaired_min':str(bad),'violates_theta':True,
             'repair':'Parameterize sigma=theta I+(1-d theta)tau, then repair tau.'},
         'dual_point_alone_recovery_counter':{'d':2,'N':1,'target':'diag(1,0)',
             'true_iid_distance':'0','retained_atoms':['I/2'],
             'retained_distance':'1/2','true_dual_point':'W=0,a=0',
             'scope':'Refutes point-only recovery; full transcript and failed-run volume avoid it.'},
         'boundary_witness_cases':[run(3,th,F(1,2**k)) for th in [F(0),F(3,8),F(1,2)-F(1,2**40)]
                                   for k in [10,60]],
         'general_algorithm_executed':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
