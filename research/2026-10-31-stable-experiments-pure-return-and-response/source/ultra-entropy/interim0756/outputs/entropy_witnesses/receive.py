#!/usr/bin/env python3
"""Exact finite controls for entropy-cone certificates and their transfer.

The analytic consistency theorem is in PROOF.txt. This receiver does not
turn finite fixtures into a universal proof or an independent audit.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import random
import time

from entropy_cone import load,verify,conjugate_bounds,prepare,exponential_bounds
from general_trace import evaluate,from_statistic
from quadratic_trace import evaluate as quadratic
from family import evaluate as family_evaluate

HERE=Path(__file__).resolve().parent


def kernel_controls():
    rng=random.Random(2026110105);checks=0
    for theta,p,q,wp,wq in [(Q(1,4),Q(14641,24641),Q(10000,24641),Q(13310,24641),Q(11000,24641)),
                            (Q(1,2),Q(4,5),Q(1,5),Q(2,5),Q(2,5))]:
        for trial in range(8):
            m=4;ha=[[Q(0)]*m for _ in range(m)]
            for i in range(m):
                j=(i+1)%m
                ha[i][j]=Q(rng.randrange(-12,13),8);ha[j][i]=-ha[i][j]
            M=max(abs(x) for row in ha for x in row)
            H=[[ha[i][j]-ha[i][j]**2/8 for j in range(m)] for i in range(m)]
            K=[[Q(0)]*m for _ in range(m)]
            for i in range(m):
                K[i][(i+1)%m]=wp*exponential_bounds(theta*H[i][(i+1)%m])[1]
                K[i][(i-1)%m]=wq*exponential_bounds(theta*H[i][(i-1)%m])[1]
            row=[Q(1,m)]*m
            for n in range(1,13):
                row=[sum((row[i]*K[i][j] for i in range(m)),Q(0)) for j in range(m)]
                rhs=exponential_bounds(n*theta*theta*M*M/2)[0]
                assert sum(row)<=rhs
                checks+=1
    # Omitting entropy from the tilted expectation gives a false claim.
    theta=Q(1,2);h=Q(1)
    wrong_lower=Q(4,5)*exponential_bounds(theta*(h-h*h/8))[0]+Q(1,5)*exponential_bounds(theta*(-h-h*h/8))[0]
    rhs_upper=exponential_bounds(theta*theta*h*h/2)[1]
    assert wrong_lower>rhs_upper
    # Stationary averaging cannot be replaced by an arbitrary initial state:
    # both exits from one state have h=+1, making that row exceed the bound.
    nonstationary_lower=Q(4,5)*exponential_bounds(Q(7,16))[0]
    assert nonstationary_lower>rhs_upper
    return {'exact_tilted_kernel_power_inequalities':checks,
        'theta_values':['1/4','1/2'],'entropy_tilt_cannot_be_omitted':True,
        'nonstationary_initial_state_invalidates_stationary_reference_bound':True,
        'negative_control_scope':'stationary-reference entropy functional; not a claim of zero actual nonstationary total entropy'}


def rounding(p,k):
    value=p*k;lo=value.numerator//value.denominator;rem=value-lo
    return [(lo,Q(1))] if rem==0 else [(lo,1-rem),(lo+1,rem)]


def model_control(cert,P,pi,labels):
    assert cert['depth']==1 and cert['alphabet']==2
    m=len(P);k=cert['mesh'];d=len(cert['descriptors'])
    back=[[pi[j]*P[j][i]/pi[i] for j in range(m)] for i in range(m)]
    plus=[[sum((P[i][j] for j in range(m) if labels[j]==b),Q(0)) for b in (0,1)] for i in range(m)]
    minus=[[sum((back[i][j] for j in range(m) if labels[j]==b),Q(0)) for b in (0,1)] for i in range(m)]
    index={node:i for i,node in enumerate(cert['nodes'])};R=[];Phi=[];W=[];fp=[];fm=[]
    a=dict(zip(cert['words'],cert['a']))
    for x in range(m):
        row={}
        for (p,np),(q,nq) in product(rounding(plus[x][0],k),rounding(minus[x][0],k)):
            row[index[labels[x],(p,k-p),(q,k-q)]]=np*nq
        assert sum(row.values())==1
        R.append(row)
        Phi.append(sum((mass*cert['potential'][i] for i,mass in row.items()),Q(0)))
        W.append(cert['z']+sum((minus[x][p]*plus[x][q]*a[p,labels[x],q] for p,q in product((0,1),repeat=2)),Q(0)))
        sides=[]
        for side in (0,1):
            f=[Q(0),Q(0)]
            for i,mass in row.items():
                for value,(q,b,w,sign) in zip(cert['y'][i*d:(i+1)*d],cert['descriptors']):
                    if q==side:
                        assert w==()
                        f[b]+=mass*sign*value
            assert sum(map(abs,f))<=cert['B'][side]
            sides.append(f)
        fp.append(sides[0]);fm.append(sides[1])
    margins=[];maximum_cone=Q(-10**9)
    for x,y in product(range(m),repeat=2):
        Hxy=cert['z']+sum((px*py*cert['without_z'](i,j) for i,px in R[x].items() for j,py in R[y].items()),Q(0))
        Hyx=cert['z']+sum((px*py*cert['without_z'](j,i) for i,px in R[x].items() for j,py in R[y].items()),Q(0))
        Mp=sum((fp[x][b]*((labels[y]==b)-plus[x][b]) for b in (0,1)),Q(0))
        Mm=sum((fm[y][b]*((labels[x]==b)-minus[y][b]) for b in (0,1)),Q(0))
        margins.append(Hxy-W[x]-Phi[x]+Phi[y]-Mp-Mm)
        hs,ha=(Hxy+Hyx)/2,(Hxy-Hyx)/2
        upper=hs+conjugate_bounds(ha,24)[1]
        assert upper<=0
        maximum_cone=max(maximum_cone,upper)
    assert min(margins)>=0
    for x in range(m):
        assert sum((P[x][y]*sum((fp[x][b]*((labels[y]==b)-plus[x][b]) for b in (0,1)),Q(0)) for y in range(m)),Q(0))==0
        assert sum((back[x][y]*sum((fm[x][b]*((labels[y]==b)-minus[x][b]) for b in (0,1)),Q(0)) for y in range(m)),Q(0))==0
    return {'hidden_states':m,'minimum_exact_transfer_margin':str(min(margins)),
        'maximum_averaged_entropy_cone_upper':str(maximum_cone),
        'population_word_bound':str(sum((pi[x]*W[x] for x in range(m)),Q(0)))}


def main():
    start=time.perf_counter();path=HERE/'compact_entropy_dual.json'
    data=json.loads(path.read_text());cert=load(path)
    target=list(map(Q,data['input_probabilities']))
    source_bound=sum((p*w for p,w in zip(target,cert['W'])),Q(0))
    assert source_bound==Q(data['exact_lower_bound'])>0
    # Do not rely on the floating primal/dual status: poison two different
    # necessary certificate properties and demand exact rejection.
    poisoned=dict(data);rows=list(data['row_duals']);rows[0]='1';poisoned['row_duals']=rows
    rejected_sign=False
    try:verify(poisoned)
    except ValueError:rejected_sign=True
    assert rejected_sign
    maxdiag=max(cert['z']+cert['without_z'](i,i) for i in range(len(cert['nodes'])))
    poisoned=dict(data);poisoned['normalization_dual']=str(cert['z']+1-maxdiag)
    rejected_cone=False
    try:verify(poisoned)
    except ValueError:rejected_cone=True
    assert rejected_cone
    conjugates=[]
    for h in (Q(0),Q(1,100),Q(1,2),Q(2),Q(20)):
        lo,hi=conjugate_bounds(h,16);lo2,hi2=conjugate_bounds(h,24)
        assert lo<=lo2<=hi2<=hi
        conjugates.append({'h':str(h),'lower_preview':float(lo2),'upper_preview':float(hi2)})
    nullP=[[Q(1,2),Q(1,4),Q(1,4)],[Q(1,4),Q(3,4),Q(0)],[Q(1,4),Q(0),Q(3,4)]]
    controls=[model_control(cert,nullP,[Q(1,3)]*3,[0,0,1])]
    assert Q(controls[0]['population_word_bound'])<=0
    rng=random.Random(2026110104)
    for trial in range(8):
        m=3+trial%3;flow=[[Q(0)]*m for _ in range(m)]
        for i in range(m):
            for j in range(i,m):flow[i][j]=flow[j][i]=Q(rng.randrange(1,12))
        circulation=rng.randrange(1,6)
        for i in range(m):flow[i][(i+1)%m]+=circulation
        rows=list(map(sum,flow));total=sum(rows);pi=[x/total for x in rows]
        P=[[flow[i][j]/rows[i] for j in range(m)] for i in range(m)]
        controls.append(model_control(cert,P,pi,[rng.randrange(2) for _ in range(m)]))
    entries=[{'kind':'quadratic','weight':'1/4'},{'kind':'grid','weight':'1/4','path':str(path)}]
    replays=[]
    for name in ('fresh_driven_ring','fresh_reversible_ring'):
        record=json.loads((HERE/(name+'_record.json')).read_text())
        generic=evaluate(cert,record,Q(1,80))
        band=family_evaluate(record,entries)
        replays.append({'name':name,'generic':generic,'time_uniform_finite_family':band,
            'scope':'implementation replay on existing synthetic records, not another independent acquisition'})
    # On the supplied exact-law fixture the finite-grid score limit is its
    # bound, not the complete-law minimum. No synthetic observations acquired.
    diagnostics=[]
    for N in (1000,1000000,1000000000):
        n=N-1
        result=from_statistic(cert,N,n*source_bound,Q(1,40),True)
        diagnostics.append({'transitions':N,'constructed_expected_word_sum':True,
            'per_step_lower_preview':result['lower_preview']/N,
            'finite_certificate_population_limit':float(source_bound),
            'sample_status':'algebraic sufficient-statistic input; no acquired record or power claim'})
    output={'scope':__doc__,'certificate':path.name,'exact_entropy_columns_checked':cert['columns_checked'],
        'exact_positive_word_bound':str(source_bound),'positive_word_bound_preview':float(source_bound),
        'constants':{k:str(cert[k]) for k in ('R','O','C','M','H_min')},
        'conjugate_controls':conjugates,'continuous_field_transfer_controls':controls,
        'entropy_kernel_controls':kernel_controls(),
        'corrupt_row_sign_rejected':rejected_sign,'corrupt_entropy_normalization_rejected':rejected_cone,
        'synthetic_replays':replays,'finite_certificate_limit_diagnostics':diagnostics,
        'status':'ALL_FULL_ENTROPY_FINITE_CONTROLS_PASSED','seconds':time.perf_counter()-start}
    (HERE/'entropy_receipt.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'seconds':output['seconds'],
        'exact_entropy_columns_checked':cert['columns_checked'],'positive_word_bound':float(source_bound),
        'continuous_model_controls':len(controls),'replays':[{'name':r['name'],
            'generic_lower':r['generic']['lower_preview'],
            'family_best':r['time_uniform_finite_family']['best']['lower_preview']} for r in replays],
        'finite_certificate_limit_diagnostics':diagnostics},indent=2))


if __name__=='__main__':main()
