#!/usr/bin/env python3
"""Bounded exact receiver of the reviewed rate-2 clearance confidence theorem.
Only the literal flat schema below is accepted. No SSA or floating arithmetic.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODEL = 'exact_rate2_corner_clearance_v1'
MAX_BYTES = 16384
MAX_SOURCE_BYTES = 2097152
MAX_BITS = 32768
ARITHMETIC_RESERVE = 10**24
ACQUISITION_RESERVE = 10**27
MAX_WORK = 10**31
KEYS = {'schema','model','N','K','a_num','a_den','error_num','error_den','work_budget'}
TOKEN = re.compile(r'\s*"([A-Za-z_]+)"\s*:\s*"([A-Za-z_0-9]+)"\s*')
DIGITS = re.compile(r'(0|[1-9][0-9]*)\Z')

class Refusal(Exception): pass

class Ledger:
    def __init__(self):
        self.counts = Counter()
        self.max_operand_bits = 0
        self.max_result_bits = 0
        self.root_trials = {}
        self.root_rejected_candidates = {}
        self.source_bytes = 0
        self.source_files = 0
        self.input_bytes = 0
    def record(self, name, values=(), result=None):
        self.counts[name] += 1
        for v in values:
            if isinstance(v, F):
                bs = (abs(v.numerator).bit_length(),v.denominator.bit_length())
            else: bs = (abs(v).bit_length(),)
            self.max_operand_bits = max(self.max_operand_bits,*bs)
        if result is not None:
            if isinstance(result,F):
                bits = max(abs(result.numerator).bit_length(),result.denominator.bit_length())
            else: bits = abs(result).bit_length()
            self.max_result_bits = max(self.max_result_bits,bits)
            if bits > MAX_BITS: raise Refusal('arithmetic bit ceiling')
        return result
    def root(self,n,k,label):
        lo,hi = 0,1 << ((n.bit_length()+k-1)//k)
        trials = rejected = 0
        while hi-lo > 1:
            mid=(lo+hi)//2
            p=self.record('integer_power',(mid,k),mid**k)
            self.record('integer_compare',(p,n))
            if p <= n: lo=mid
            else: hi=mid; rejected+=1
            trials+=1
            if trials > 16384: raise Refusal('root work ceiling')
        if self.record('integer_power',(hi,k),hi**k) <= n: lo=hi
        # Explicit receiving invariant, including the exact-root and upper tests.
        if not lo**k <= n < (lo+1)**k: raise Refusal('root invariant failure')
        self.root_trials[label]=trials
        self.root_rejected_candidates[label]=rejected
        return lo
    def obj(self):
        return {'input_bytes':self.input_bytes,'source_bytes_read_and_hashed':self.source_bytes,
                'source_files_read_and_hashed':self.source_files,
                'tracked_high_level_operations':dict(self.counts),
                'root_trial_counts':self.root_trials,
                'root_rejected_candidates_charged':self.root_rejected_candidates,
                'max_recorded_operand_bits':self.max_operand_bits,
                'max_recorded_result_bits':self.max_result_bits,
                'all_intermediate_integer_bit_upper':MAX_BITS,
                'receiving_high_level_operation_upper':10000000,
                'preinteger_parser_bit_charge_upper':str(MAX_BYTES*1048576),
                'receiving_arithmetic_and_control_bit_charge':str(ARITHMETIC_RESERVE),
                'source_and_input_scan_hash_bit_charge':str((self.source_bytes+self.input_bytes)*1048576),
                'cold_scalar_acquisition_bit_charge':str(ACQUISITION_RESERVE),
                'historical_scalar_acquisitions_bit_charge':str(2*ACQUISITION_RESERVE),
                'loader_repair_and_regression_bit_charge':str(ARITHMETIC_RESERVE),
                'historical_scalar_acquisition_runs_not_hidden':2,
                'total_cold_work_upper':str(3*ACQUISITION_RESERVE+2*ARITHMETIC_RESERVE+(self.source_bytes+self.input_bytes)*1048576),
                'rejected_adaptive_refinements':0,
                'cost_model':'conservative schoolbook bit-operation upper charges, not CPU instructions or seconds'}


def parse(raw,ledger):
    ledger.input_bytes=len(raw)
    if len(raw)>MAX_BYTES: raise Refusal('input byte ceiling')
    try: s=raw.decode('ascii').strip()
    except UnicodeDecodeError: raise Refusal('ASCII input required')
    if not (s.startswith('{') and s.endswith('}')): raise Refusal('flat object required')
    content=s[1:-1]; pos=0; out={}
    while pos<len(content):
        m=TOKEN.match(content,pos)
        if not m: raise Refusal('flat string-only schema; no nested values, escapes or bare numbers')
        k,v=m.groups()
        if k not in KEYS or k in out: raise Refusal('unknown or duplicate key')
        out[k]=v; pos=m.end()
        if pos==len(content): break
        if content[pos]!=',': raise Refusal('invalid separator')
        pos+=1
        if pos==len(content): raise Refusal('trailing comma')
    if set(out)!=KEYS: raise Refusal('missing schema field')
    if out['schema']!='1' or out['model']!=MODEL: raise Refusal('unsupported model or schema')
    limits={'N':2048,'K':128,'a_num':64,'a_den':64,'error_num':64,'error_den':64,'work_budget':32}
    for k,limit in limits.items():
        v=out[k]
        if len(v)>limit or not DIGITS.fullmatch(v): raise Refusal('invalid bounded integer '+k)
        out[k]=int(v)
    if not all(out[k]>0 for k in limits): raise Refusal('positive integers required')
    if out['work_budget']>MAX_WORK: raise Refusal('work budget exceeds schema maximum')
    if out['work_budget']<3*ACQUISITION_RESERVE+2*ARITHMETIC_RESERVE+MAX_SOURCE_BYTES*1048576+MAX_BYTES*1048576:
        raise Refusal('cold acquisition and receiving work budget insufficient')
    return out


def read_bound(relative,sha,ledger):
    path=ROOT/relative
    if not path.is_file() or path.is_symlink(): raise Refusal('missing or symbolic source '+relative)
    with path.open('rb') as f:
        data=f.read(MAX_SOURCE_BYTES-ledger.source_bytes+1)
    if ledger.source_bytes+len(data)>MAX_SOURCE_BYTES: raise Refusal('source byte ceiling')
    ledger.source_bytes+=len(data); ledger.source_files+=1
    if hashlib.sha256(data).hexdigest()!=sha: raise Refusal('source hash mismatch '+relative)
    return data


def source_gate(ledger):
    # The manifest is a receiving-code dependency, not an untrusted source of new
    # authorities. Its hash is pinned below after both independent receipts seal.
    manifest=HERE/'SOURCE_BINDINGS.json'
    if not manifest.is_file(): raise Refusal('source receipt manifest pending')
    with manifest.open('rb') as f:
        data=f.read(MAX_SOURCE_BYTES+1)
    if len(data)>MAX_SOURCE_BYTES: raise Refusal('source manifest byte ceiling')
    if hashlib.sha256(data).hexdigest()!=SOURCE_MANIFEST_SHA256:
        raise Refusal('source receipt manifest hash mismatch or pending')
    payload=json.loads(data)
    if payload['status']!='ALL_REQUIRED_SOURCE_RECEIPTS_FINAL_PASS':
        raise Refusal('source receipts not final')
    ledger.source_bytes+=len(data); ledger.source_files+=1
    files={}
    for row in payload['files']:
        files[row['path']]=read_bound(row['path'],row['sha256'],ledger)
    fine=json.loads(files['inverse_clearance_clock_20261101/CERTIFICATE_FINE.json'])
    acquisition=json.loads(files['clearance_window_receiver_20261101/SCALAR_ACQUISITION.json'])
    if acquisition['status']!='PASS_EXACT_METERED_INDEPENDENT_SCALAR_REPLAY':
        raise Refusal('scalar acquisition failed')
    if int(acquisition['total_acquisition_charge'])>ACQUISITION_RESERVE:
        raise Refusal('scalar acquisition exceeds charged reserve')
    return F(fine['s_star_lower']),F(fine['s_star_upper']),payload


def outward(x,places,up):
    scaled=x*10**places
    n=-((-scaled.numerator)//scaled.denominator) if up else scaled.numerator//scaled.denominator
    sign='-' if n<0 else ''; n=abs(n)
    return sign+str(n//10**places)+'.'+str(n%10**places).zfill(places)


def receive(raw):
    led=Ledger(); start=time.monotonic_ns(); tests={}; tails=[]
    try:
        v=parse(raw,led); N=v['N']; K=v['K']; a=F(v['a_num'],v['a_den']); error=F(v['error_num'],v['error_den'])
        def gate(name,condition):
            tests[name]=bool(condition)
            if not condition: raise Refusal(name)
        gate('a_in_(0,1/4]',0<a<=F(1,4))
        gate('requested_failure_in_(0,1)',0<error<1)
        gate('N_at_least_10^200',N>=10**200)
        gate('K_at_least_10^40',K>=10**40)
        T=led.root(N,5,'N_fifth_root')
        gate('N_is_exact_fifth_power',T**5==N)
        r=led.root(K+1,2,'K_plus_1_sqrt')
        rceil=r+(r*r<K+1)
        p=K+1; q=2*rceil+1; H=p+q+1
        rootK=led.root(K,2,'K_sqrt')
        b=F(1,K*rootK)
        delta_den=10**100; h=1600*delta_den**2
        gate('T_squared_ge_16_H_ceiling',T*T>=16*H)
        gate('T_cubed_ge_64_p_squared',T**3>=64*p*p)
        gate('T_squared_ge_4_p_q_ceiling_over_a',a*T*T>=4*p*q)
        gate('K_T_le_delta_N',K*T*delta_den<=N)
        gate('N_ge_32_h',N>=32*h)
        gate('delta_N_ge_4',N>=4*delta_den)
        gate('K_ge_4_and_beta_domination',K>=4 and K**3<=27*(K-2)**3)
        gate('m0_le_10^-6',F(1,2*delta_den)<=F(1,10**6))
        gate('harmonic_N_ge_200000',N>=200000)
        gate('dyadic_exponent_ge_1',K*T>=3*10**12)
        gate('dyadic_delay_less_than_T',32*b<1)
        gate('whole_upper_horizon_within_4T_plus_h',F(2)+a+32*b<=4)
        clock=led.record('rational_clock_bound',(H,a,T),F(10**5*H**6,T)/a**6)
        # For nonnegative rational x, e^-x <= 2^-floor(x).
        # P<=2^prefbits and floor(x)>=prefbits+40 -> P e^-x<=2^-40.
        def exp_tail(name,x,pref=1):
            if x<0: raise Refusal(name+' negative exponent')
            pref_bits=0 if pref==1 else pref.bit_length()
            floorx=x.numerator//x.denominator
            led.record('exponential_bit_comparison',(x,pref,floorx))
            gate(name+'_at_most_2^-40',floorx>=pref_bits+40)
            tails.append({'name':name,'method':'prefactor <= 2^b; exp(-x) <= 2^-floor(x)',
                          'prefactor_bit_upper':pref_bits,'exponent_floor_bit_length':floorx.bit_length(),
                          'required_exponent_floor':pref_bits+40,'upper':'1/1099511627776'})
        def poisson(name,lam,r):
            # theta=log 2: P(X>=r)<=exp(lam-r log2)<=exp(lam-r/2).
            # Here r is the exact integer crossing threshold; no continuity shortcut.
            x=F(r,2)-lam
            exp_tail(name,x)
            tails[-1]['method']='Poisson Chernoff at log 2, log 2 >= 1/2; exponent r/2-lambda'
            tails[-1]['integer_threshold_bit_length']=r.bit_length()
        exp_tail('B_A_fast_cap',F(K*T,64)-1,36*H**3*T**3)
        lam=4*T+h
        # P(Pois(lambda)>delta N/2-2) equals P(Pois(lambda)>=floor(delta N/2-2)+1).
        imm_r=N//(2*delta_den)-1
        poisson('B_imm_original_whole_horizon',F(lam),imm_r)
        exp_tail('B_stage_all_dyadic_good_events',F(K*T,3*10**12),32)
        band_r=(N+delta_den-1)//delta_den
        poisson('B_band_actual_death_count',F(40000,10**50),band_r)
        exp_tail('B_harm_persistence_excursions',F(N,2000*delta_den),32*N*N*h)
        exp_tail('B_harm_A_martingale',F(600*N*N,96*h+20))
        exp_tail('B_harm_actual_death_clock',F(N,2))
        exp_tail('B_harm_immigration_and_unused_waiting',F(N,96))
        fail=led.record('rational_failure_sum',(clock,),clock+F(8,1<<40))
        gate('total_failure_le_requested',fail<=error)
        # Numeric work may be staged before this authority gate, but no theorem
        # admission is emitted until every frozen accepted source is bound.
        sL,sU,sources=source_gate(led)
        lower=max(F(0),sL-a-b); upper=sU+a+32*b+F(h,T)
        physical_lower=led.record('rational_physical_endpoint',(lower,T),lower*T)
        physical_upper=led.record('rational_physical_endpoint',(upper,T),upper*T)
        result={'status':'AUTHOR_ADMISSION_PASS_PENDING_INDEPENDENT_CODE_REVIEW',
          'model':MODEL,'initial_state':'(A,B,C,D,E)=(0,N,1,1,0)',
          'target':'first actual S <= 15(N+2)/16',
          'N_decimal_digits':len(str(N)),'N_bits':N.bit_length(),'T':str(T),'K':str(K),'a':str(a),
          'p':str(p),'q_integer_ceiling':str(q),'H_integer_ceiling':str(H),
          'sqrt_K_floor':str(rootK),'beta_and_K^-3/2_upper':str(b),'h':str(h),
          's_star_interval_exact':[str(sL),str(sU)],
          'normalized_window_exact':[str(lower),str(upper)],
          'normalized_window_decimal_outward':[outward(lower,18,False),outward(upper,18,True)],
          'physical_window_exact':[str(physical_lower),str(physical_upper)],
          'B_clock_rational_upper':str(clock),'B_clock_decimal_upper':outward(clock,20,True),
          'tail_receipts':tails,'failure_upper_exact':str(fail),'failure_decimal_upper':outward(fail,18,True),
          'requested_failure':str(error),'requested_work_budget':str(v['work_budget']),'admission_tests':tests,
          'source_manifest_sha256':SOURCE_MANIFEST_SHA256,
          'source_files':len(sources['files']),
          'not_claimed':['CDF/KS/TV point-mass approximation','CLT','practical chemistry population','universal solver lower bound','arbitrary N support','changing rates','novel numerical method']}
    except (Refusal,OSError,ValueError,KeyError,TypeError,ZeroDivisionError) as e:
        result={'status':'UNKNOWN','reason':str(e),'admission_tests':tests,'tail_receipts':tails}
    result['cost_ledger']=led.obj()
    result['elapsed_ns_nonproof']=time.monotonic_ns()-start
    return result

SOURCE_MANIFEST_SHA256 = 'ec0bd61d36ff51dfe39090ae67e22b9cb94dfb4208ee2b58b8370cdf24fda016'

def main():
    if len(sys.argv)!=2:
        print(json.dumps({'status':'UNKNOWN','reason':'one bounded JSON input file required'})); return
    try:
        with open(sys.argv[1],'rb') as f: raw=f.read(MAX_BYTES+1)
        result=receive(raw)
    except OSError as e: result={'status':'UNKNOWN','reason':str(e)}
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
