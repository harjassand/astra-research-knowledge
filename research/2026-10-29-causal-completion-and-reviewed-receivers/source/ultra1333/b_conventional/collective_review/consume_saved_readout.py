"""Independent exact consumption of saved native readout intervals.

No producer imports, new source case, matrix/Fock/RNG/dynamics execution.
The upstream matrix-function enclosures are analytically whole-code reviewed;
their numerical acquisition is NOT replayed here.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

START=time.perf_counter()
HERE=Path(__file__).resolve().parent
SRC=HERE.parent.parent/'a_independent/collective_critical'
raw=(SRC/'READOUT_RECEIPT.json').read_bytes()
receipt=json.loads(raw)
assert hashlib.sha256(raw).hexdigest()=='1e06c2a4ed9e7746cfb53fe8515b025b46df77aa30caf00b7952e1e35468978b'


def dyadic(x):
    m,e=int(x['mantissa']),int(x['exponent'])
    assert abs(e)<100000, 'Do not materialize the tiny Poisson-tail endpoints.'
    return F(m*2**e) if e>=0 else F(m,2**(-e))


def interval(x): return dyadic(x['lower_dyadic']),dyadic(x['upper_dyadic'])
def add(x,y): return x[0]+y[0],x[1]+y[1]
def mul(x,y):
    a=[x[i]*y[j] for i in (0,1) for j in (0,1)]
    return min(a),max(a)
def scale(x,a): return mul(x,(F(a),F(a)))


def coarsen(x,bits=80):
    den=2**bits
    lo=(x[0]*den).__floor__()
    hi=(x[1]*den).__ceil__()
    return F(lo,den),F(hi,den)


def concise_upper(x,bits=80):
    """Outward dyadic summary; do not serialize giant Taylor LCMs in decimal."""
    return F((x*2**bits).__ceil__(),2**bits)


def exp_negative_point(x,terms=96):
    assert 0<=x<=8
    v=S=F(1)
    for k in range(1,terms+1):
        v=v*x/k;S+=v
    next_term=v*x/(terms+1)
    tail=next_term/(1-x/F(terms+2))
    return 1/(S+tail),1/S


def exp_negative(x):
    return exp_negative_point(x[1])[0],exp_negative_point(x[0])[1]


# cos(2*pi*j/5) uses only one outward square-root interval.
bits=80; den=2**bits
root=math.isqrt(5*den*den)
sqrt5=(F(root,den),F(root+1,den))
c1=scale(add(sqrt5,(F(-1),F(-1))),F(1,4))
c2=scale(add(sqrt5,(F(1),F(1))),F(-1,4))
cosines=[(F(1),F(1)),c1,c2,c2,c1]
results=[]
for c in receipt['cases']:
    inp=(SRC/c['input']).read_bytes()
    assert hashlib.sha256(inp).hexdigest()==c['input_sha256']
    model=json.loads(inp);M=model['M'];K=int(model['K_each'])
    T=[[F(x) for x in r] for r in model['T']]
    assert len(T)==M and all(sum(r)==0 for r in T)
    assert all(T[i][j]==T[j][i] for i in range(M) for j in range(M))
    D=math.comb(K+M-1,M-1)
    assert D.bit_length()==c['one_flavor_hilbert_dimension_bits']
    assert K==2**(c['K_bit_length']-1)
    assert (c['K_bit_length']-1)%4==0
    w=c['matrix_acquisition']['query_vector']
    assert sum(w)==0
    assert sum(x*x for x in w)==c['matrix_acquisition']['query_vector_norm_squared']
    if M==32:
        assert w==[17]*15+[-15]*17
        # Direct exact core action; no new matrix-function computation.
        core=[[3,1,-4],[1,3,-4],[-4,-4,8]]
        for start in range(0,M-2,3):
            assert all(sum(core[i][j]*w[start+j] for j in range(3))==0 for i in range(3))
    var=coarsen(interval(c['gaussian_theta_variance']))
    assert 0<var[0]<=var[1]<1
    exps=[None]+[exp_negative(scale(var,F(h*h,2))) for h in range(1,5)]
    probs=[]
    for j in range(5):
        p=(F(1),F(1))
        for h in range(1,5):
            p=add(p,scale(mul(exps[h],cosines[(h*j)%5]),2*F(5-h,5)))
        probs.append(scale(p,F(1,5)))
    table=c['dyadic_table'];denom=int(table['denominator']);nums=table['numerators']
    assert denom==2**table['bits'] and sum(nums)==denom and min(nums)>=0
    assert all(lo>0 and hi<1 for lo,hi in probs)
    exact_table_error=sum(max(abs(F(a,denom)-lo),abs(F(a,denom)-hi))
                          for a,(lo,hi) in zip(nums,probs))/2
    assert exact_table_error<F(1,10**12)
    # Independently verify the published table error from its OWN endpoints.
    published_prob_intervals=[interval(p) for p in c['proxy_probabilities']]
    published_error=sum(max(abs(F(a,denom)-lo),abs(F(a,denom)-hi))
                        for a,(lo,hi) in zip(nums,published_prob_intervals))/2
    assert published_error==F(c['arithmetic_table_tv_upper'])
    assert all(max(x[0],y[0])<=min(x[1],y[1])
               for x,y in zip(probs,published_prob_intervals))
    theorem=interval(c['finite_instrument_tv_theorem'])
    total=theorem[1]+exact_table_error
    ceiling=F(2131,10**6) if M==3 else F(783,10**6)
    assert total<ceiling
    first=probs[0][1]+total
    if M==32: assert first<F(4544,10000)
    results.append({'M':M,'K_bits':K.bit_length()-1,
        'dyadic_table_normalized':True,
        'independent_table_error_upper':str(concise_upper(exact_table_error)),
        'independent_table_error_decimal_display':float(exact_table_error),
        'independent_total_tv_upper':str(concise_upper(total)),
        'independent_total_tv_decimal_display':float(total),
        'first_outcome_upper_decimal_display':float(first),
        'saved_arithmetic_error_identity':True,
        'all_independent_proxy_intervals_intersect_saved_intervals':True})

binding=json.loads((SRC/'EXECUTION_BINDING.json').read_text())
current=(SRC/'compile_readout.py').read_bytes()
executed=(SRC/'EXECUTED_compile_readout.py').read_bytes()
assert hashlib.sha256(current).hexdigest()==binding['current_source_sha256']
assert hashlib.sha256(executed).hexdigest()==binding['executed_source_sha256']
guard=b'    assert K >= 4*d+4\n'
assert current.count(guard)==1 and current.replace(guard,b'',1)==executed
out={'status':'SAVED_NATIVE_FINITE_LAWS_INDEPENDENTLY_CONSUMED',
    'cases':results,'receipt_sha256':hashlib.sha256(raw).hexdigest(),
    'current_executed_code_difference_exactly_declared_guard':True,
    'method':'Fractions, outward 80-bit variance/sqrt5, positive exponential Taylor series and exact remainder; no producer imports.',
    'matrix_acquisition_replayed':False,'new_model_cases':0,
    'Fock_states':0,'random_draws':0,'trajectory_steps':0,
    'elapsed_seconds':time.perf_counter()-START,
    'consumer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'EXACT_CONSUMER.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'total_tv_displays':[x['independent_total_tv_decimal_display'] for x in results],'seconds':out['elapsed_seconds']},indent=2))
