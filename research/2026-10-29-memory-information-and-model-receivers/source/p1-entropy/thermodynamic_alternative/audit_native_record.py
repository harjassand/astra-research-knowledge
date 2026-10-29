"""Independent public-record audit. Never imports or reads the private source.

Uses a different exact log truncation and an alternating exponential bracket.
Source producer inspection is deliberately a later, separately saved audit.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json
import numpy as np

BASE=Path(__file__).resolve().parent.parent/'native_entropy'
RUN=BASE/'run'
DEN=1<<80


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def rf(obj): return F(obj['rational'])
def ceil_grid(x): return F(-(-x.numerator*DEN//x.denominator),DEN)


def log_bracket(x):
    def core(y):
        z=(y-1)/(y+1); square=z*z; power=z; total=F(0)
        for k in range(96):
            total+=2*power/(2*k+1); power*=square
        return total,total+2*power/(193*(1-square))
    k=0
    while x>=2: x/=2; k+=1
    lo,hi=core(x); a,b=core(F(2))
    return lo+k*a,hi+k*b


def exact_log_round(x):
    lo,hi=log_bracket(x)
    assert ceil_grid(lo)==ceil_grid(hi)
    return ceil_grid(hi)


def check_ceil_sqrt(bound,x):
    assert (bound*DEN).denominator==1
    assert bound*bound>=x
    if bound: assert (bound-F(1,DEN))**2<x


def exp_negative_bracket(x):
    # Taylor's remainder sign for exp(-x): even partial sum is upper;
    # next odd partial sum is lower. No floating arithmetic or source rate.
    term=F(1); total=F(1)
    for k in range(1,202):
        term*=-x/k; total+=term
        if k==200: upper=total
    lower=total
    assert 0<lower<=upper and ceil_grid(lower)==ceil_grid(upper)
    return lower,upper


def convert(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):convert(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [convert(v) for v in x]
    return x


def main():
    cp=RUN/'PUBLIC_CONTRACT.json'; rp=RUN/'native_record.npz'
    contract=json.loads(cp.read_text())
    old=json.loads((RUN/'ACQUIRED_ENTROPY_CERTIFICATE.json').read_text())
    reuse=json.loads((RUN/'REUSED_ENTROPY_CERTIFICATE.json').read_text())
    raw=np.load(rp,allow_pickle=False)
    assert set(raw.files)=={'start_port','end_port','native_hold_upper_ticks','interior_duration_upper_ticks'}
    arrays={k:[int(x) for x in raw[k]] for k in raw.files}
    i=arrays['start_port']; j=arrays['end_port']; u=arrays['interior_duration_upper_ticks']; hold=arrays['native_hold_upper_ticks']
    N=len(i); scale=int(contract['timestamp_scale'])
    assert N==262144==contract['acquired_trials']==contract['native_preparations']
    assert all(len(v)==N for v in arrays.values())
    assert all(0<=x<5 for x in i+j)
    assert contract['port_weights_up_to_scale']==['1']*5
    assert contract['native_port_rates']==['32/15']*5
    assert contract['selection']=='Each port chosen uniformly; calibrated stationary departure fluxes are equal.'
    assert old['record_sha256']==reuse['record_sha256']==digest(rp)
    assert old['contract_sha256']==digest(cp)
    assert old['consumer_sha256']==reuse['helper_sha256']==digest(BASE/'certify_native_entropy.py')
    assert reuse['consumer_sha256']==digest(BASE/'certify_native_entropy_reuse.py')
    counts=Counter(zip(i,j)); inside_counts=Counter(); window=[]; all_score=[]; ambiguous=0
    for x,y,t in zip(i,j,u):
        h=-1 if (y-x)%5 in (1,4) else 1
        lower=max(0,t-1)
        if t>0 and t<=scale:
            z=h; inside_counts[(x,y)]+=1
        elif t==0 or lower>scale: z=0
        else:
            z=max(h,0); ambiguous+=1
        window.append(z); all_score.append(h if t>0 else 0)
    matrix=lambda c:[[c[(x,y)] for y in range(5)] for x in range(5)]
    assert matrix(counts)==old['all_endpoint_counts']
    assert matrix(inside_counts)==old['bin_counts']
    assert ambiguous==old['timestamp_ambiguous_trials']==0
    assert sum(window)==old['score_sum']==-10380
    assert sum(all_score)==-16678
    assert all(t>0 for t in u)
    empirical_window=F(sum(window),N); empirical_all=F(sum(all_score),N)
    assert rf(old['score_empirical_upper'])==empirical_window
    ds=F(contract['confidence_score_failure']); dm=F(contract['confidence_mean_failure'])
    log_s=exact_log_round(1/ds); log_m=exact_log_round(1/dm)
    rad_s=rf(old['score_radius_outward'])
    check_ceil_sqrt(rad_s,2*log_s/N)
    assert rf(old['score_expectation_upper'])==empirical_window+rad_s
    gap=max(F(0),-empirical_window-rad_s)
    assert rf(old['copositive_gap_lower'])==gap
    assert rf(old['entropy_per_native_departure_lower_nats'])==4*gap
    H=F(contract['mean_truncation']); cap=int(H*scale)
    sum_cap=sum(min(t,cap) for t in u)
    empirical_mean=F(sum_cap,N*scale)
    assert rf(old['empirical_censored_duration_upper'])==empirical_mean
    rad_m=rf(old['mean_radius_outward'])
    check_ceil_sqrt(rad_m/H,log_m/(2*N))
    exp_lo,exp_hi=exp_negative_bracket(H/2)
    tail=2*ceil_grid(exp_hi)
    assert rf(old['tail_bias_outward'])==tail
    hold_mean=F(15,32)
    assert rf(old['native_hold_mean_from_calibration'])==hold_mean
    mean_cycle=hold_mean+empirical_mean+rad_m+tail
    assert rf(old['cycle_mean_upper'])==mean_cycle
    assert rf(old['entropy_rate_lower_nats_per_native_time'])==4*gap/mean_cycle
    assert rf(old['confidence_failure_total'])==ds+dm==F(1,1000)
    # Independent simultaneous two-score reuse audit.
    failure=F(1,3000); log_reuse=exact_log_round(1/failure)
    radius=None
    for name,emp in [('duration_at_most_1',empirical_window),('all_positive_duration_returns',empirical_all)]:
        score=reuse['scores'][name]
        assert score['score_sum']==int(emp*N)
        assert rf(score['empirical_score_upper'])==emp
        r=rf(score['confidence_radius']); check_ceil_sqrt(r,2*log_reuse/N)
        if radius is not None: assert r==radius
        radius=r
        gap=max(F(0),-emp-r)
        assert rf(score['gap_lower'])==gap
        assert rf(score['entropy_per_departure_lower'])==4*gap
    reuse_rad=rf(reuse['mean_radius'])
    check_ceil_sqrt(reuse_rad/H,log_reuse/(2*N))
    reuse_mean=hold_mean+empirical_mean+reuse_rad+tail
    assert rf(reuse['truncated_mean_upper'])==empirical_mean
    assert rf(reuse['tail_allowance'])==tail
    assert rf(reuse['mean_cycle_upper'])==reuse_mean
    for score in reuse['scores'].values():
        assert rf(score['entropy_rate_lower'])==rf(score['entropy_per_departure_lower'])/reuse_mean
    best=max(reuse['scores'],key=lambda name:rf(reuse['scores'][name]['entropy_per_departure_lower']))
    assert best==reuse['stronger_certificate']=='all_positive_duration_returns'
    assert rf(reuse['confidence_failure_total'])==3*failure==F(1,1000)
    # Raw instrument intervals also bound the elapsed total, without private truth.
    duration_lower=F(sum(max(0,t-1) for t in hold+u),scale)
    duration_upper=F(sum(hold)+sum(u),scale)
    result=dict(status='PASS',audit_phase='PUBLIC INPUTS AND CERTIFICATES ONLY; before private truth inspection',
        private_source_reads=0,source_redraws=0,N=N,raw_record_sha256=digest(rp),contract_sha256=digest(cp),
        endpoint_counts=matrix(counts),window_counts=matrix(inside_counts),start_counts=[i.count(k) for k in range(5)],
        window_score_sum=sum(window),all_positive_score_sum=sum(all_score),direct_atom_markers=u.count(0),
        ambiguous_timestamp_trials=ambiguous,hold_upper_tick_sum=sum(hold),interior_upper_tick_sum=sum(u),
        truncated_tick_sum=sum_cap,elapsed_time_interval=[duration_lower,duration_upper],
        window_entropy_rate=rf(old['entropy_rate_lower_nats_per_native_time']),
        reused_entropy_per_departure=rf(reuse['scores'][best]['entropy_per_departure_lower']),
        reused_entropy_rate=rf(reuse['scores'][best]['entropy_rate_lower']),
        simultaneous_reuse_failure=3*failure,
        independent_arithmetic='96-term rational atanh brackets; integer grid/square conditions; alternating 200/201-term exp(-12) Taylor brackets',
        source_and_instrument_premises='Taken from public contract, not inferred from data or private generator',
        audit_script_sha256=digest(Path(__file__)))
    out=Path(__file__).with_name('NATIVE_RECORD_PUBLIC_AUDIT.json')
    out.write_text(json.dumps(convert(result),indent=2)+'\n')
    print(json.dumps(convert({k:result[k] for k in ['status','private_source_reads','source_redraws','N','window_score_sum','all_positive_score_sum','elapsed_time_interval','window_entropy_rate','reused_entropy_per_departure','reused_entropy_rate']}),indent=2))


if __name__=='__main__': main()
