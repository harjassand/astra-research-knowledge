"""Strong ordinary matched-path baseline, not an excluded rival.

Requires all selected paired paths to have actually met; otherwise UNKNOWN, never
invents missing continuations. Independent internal geometric coins can then be
applied to the retained paths with zero new source calls. Confidence is fixed-N,
conditional on source/coin provenance, not conditional on observed completion.
"""
from copy import deepcopy
import random
import sympy as S
import clock_response as R
C=R.C


def receive_endpoint(record,*,expected_design,coin_seed):
    # Full label receiving paid again, not trusted scalar consumption.
    received=R.receive(record,expected_design=expected_design);d=expected_design
    C.integer(coin_seed);rng=random.Random(coin_seed);gamma=C.rational(d['gamma']);t=gamma/(1-gamma)
    n,m,N=d['n'],d['m'],d['N'];Z,W,which=C.partitions(d['parts'],n);r=Z.cols;F=n*(m-1);delta=C.rational(d['delta']);bits=d['root_bits']
    selected=[(row,tr) for row in record['rows'] for tr in row['trials'][:N]]
    if any(tr['x'][-1]!=tr['y'][-1] for _,tr in selected):return dict(status='UNKNOWN_INCOMPLETE_RETAINED_PATH',new_source_calls=0)
    p,q=int(gamma.p),int(gamma.q);U=[S.zeros(n,r) for _ in range(m)];bounds=[];coins=counterfactual_calls=0
    for row in record['rows']:
        samples=[]
        for tr in row['trials'][:N]:
            tau=len(tr['x'])-1;s=0;v=[S.Integer(0)]*r
            while s<tau:
                coins+=1
                if rng.randrange(q)>=p:
                    v[which[tr['x'][s]]]+=t;v[which[tr['y'][s]]]-=t;break
                s+=1
            counterfactual_calls+=2+2*s;samples.append(v)
        means=[sum(x[j] for x in samples)/N for j in range(r)];vars=[sum((x[j]-means[j])**2 for x in samples)/(N-1) for j in range(r)]
        lh=C.ceil_log2(S.Integer(2)**(r+1)*F/(delta/2));le=C.ceil_log2(S.Integer(4)*F*r/(delta/2))
        eh=C.sqrt_up(8*t*t*lh/N,bits);ee=sum(C.sqrt_up(2*v*le/N,bits)+14*t*le/(3*(N-1)) for v in vars)
        U[row['action']][row['state'],:]=S.Matrix([means]);bounds.append(dict(state=row['state'],action=row['action'],hoeffding=str(eh),empirical_bernstein=str(ee),total=str(min(eh,ee)),sample_variances=[str(v) for v in vars]))
    BU=[W*A for A in U];measured=max(C.row_l1(A-Z*B) for A,B in zip(U,BU));error=max(C.rational(b['total']) for b in bounds)
    return dict(status='PASS_ORDINARY_ENDPOINT_RADIUS_ARITHMETIC',eta_U=str(measured+error),row_radii=bounds,empirical_scaled_rows=[C.serial(A) for A in U],new_source_calls=0,already_paid_retained_source_calls=received['retained_source_calls'],counterfactual_fresh_geometric_stopped_calls_on_matched_paths=counterfactual_calls,internal_geometric_coins=coins,statistical_failure_budget=str(delta),joint_prefix_and_baseline_failure_budget_at_most=str(2*delta),scope='Ordinary method also receives and may use the paired-prefix certificate unchanged. This individual endpoint estimate is not a claim of exclusive-method superiority. Counterfactual stopped calls do not erase full-bank calls already paid.')
