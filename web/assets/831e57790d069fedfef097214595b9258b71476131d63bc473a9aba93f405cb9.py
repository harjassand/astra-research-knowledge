#!/usr/bin/env python3
"""Complete bounded classical seed/Euler/weight/Clifford-description fixture.

Certificate target is its declared fixed-R,fixed-T real Euler law.  The
continuous cutoff/Gibbs/statistical errors are separately reported, even
when their bound is vacuous.  No physical quantum device is controlled.
"""
import argparse
from fractions import Fraction as F
import importlib.util
import json
from math import isqrt
from pathlib import Path
import resource
import secrets
import time

HERE=Path(__file__).resolve().parent
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,HERE/file)
    out=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out
wc=module('compiler_wconstants','certified_weight_constant.py')
normal=module('compiler_normals','certified_normal.py')
base,IV,iv=wc.base,wc.IV,wc.iv
exp_scalar,exp_iv=wc.exp_scalar,wc.exp_iv
EPS_ACCEPT=F(1,1<<60)
EPS_SEED=F(1,1<<40)
EPS_UPDATE=F(1,1<<48)
EPS_V=F(1,1<<60)
EPS_PROJECT=F(1,1<<60)
EPS_X=F(1,1<<88)


def mid(x): return (x.lo+x.hi)/2
def error_to_interval(x,v): return max(abs(v-x.lo),abs(v-x.hi))
def square(x):
    x=iv(x)
    a,b=x.lo*x.lo,x.hi*x.hi
    return IV(F(0) if x.lo<=0<=x.hi else min(a,b),max(a,b))
def clip(x,a,b):
    x=iv(x)
    return IV(min(b,max(a,x.lo)),min(b,max(a,x.hi)))
def norm_iv(v): return base.sqrt_iv(sum((square(x) for x in v),iv(0)))
def dot(a,b): return sum((x*y for x,y in zip(a,b)),iv(0))
def matvec(A,v): return [dot(row,v) for row in A]
def mm(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(3)),iv(0)) for j in range(3)] for i in range(3)]
def transpose(A): return [[A[j][i] for j in range(3)] for i in range(3)]


def even_scalar(x,kind):
    assert x>=0
    base.ledger.add('extended_'+kind+'_calls')
    if x==0: return iv(1)
    offset=0 if kind=='cosh' else 1
    envelope=F(1<<max(1,normal.ceil_fraction(2*x)))
    tol=F(1,1<<(IV.P+12))
    total,term,n=F(1),F(1),0
    while True:
        following=term*x*x/((2*n+1+offset)*(2*n+2+offset))
        rem=envelope*following
        if rem<=tol: break
        term=following
        total+=term
        n+=1
        base.ledger.add('extended_'+kind+'_terms')
        base.ledger.see(total,term,rem)
    return IV(total,total+rem)


def even_iv(x,kind):
    x=iv(x)
    return IV(even_scalar(x.lo,kind).lo,even_scalar(x.hi,kind).hi,raw=True)


def log_near(z):
    assert F(1)<=z<=F(2)
    x=(z-1)/(z+1)
    term,total,n=x,F(0),0
    tol=F(1,1<<(IV.P+12))
    while True:
        total+=2*term/(2*n+1)
        following=term*x*x
        rem=2*abs(following)/((2*n+3)*(1-x*x))
        base.ledger.add('log_series_terms')
        base.ledger.see(total,term,rem)
        if rem<=tol: return IV(total-rem,total+rem)
        term=following
        n+=1


def log_scalar(z):
    assert z>0
    power=0
    while z<1: z*=2;power-=1
    while z>2: z/=2;power+=1
    return log_near(z)+power*log_near(F(2))


def log_iv(x):
    x=iv(x)
    return IV(log_scalar(x.lo).lo,log_scalar(x.hi).hi,raw=True)


def dyadic(x,bits=96):
    scaled=x*(1<<bits)+F(1,2)
    n=scaled.numerator//scaled.denominator
    base.ledger.add('completed_value_dyadic_roundings')
    return F(n,1<<bits)


def projected(v,radius):
    # All inputs are rational. Exact squared-radius comparison is an
    # evaluation of a finite node, never a continuous hitting-time oracle.
    if sum(x*x for x in v)<=radius*radius:
        return [iv(x) for x in v]
    r=norm_iv(v)
    return [iv(x)*radius/r for x in v]


def coefficients(v,C,b,N,s,sqrtN,radius):
    r=norm_iv(v)
    chi=clip(3-4*r/radius,F(0),F(1))
    z=projected(v,radius)
    Cv=matvec(C,z)
    q=dot(z,Cv)
    bm=dot(b,z)
    a=[chi*((N-1)*(Cv[i]-q*z[i])/(2*s*s)+(iv(b[i])-bm*z[i])/(2*s)) for i in range(3)]
    P=[[iv(int(i==j))-z[i]*z[j] for j in range(3)] for i in range(3)]
    cross=[[iv(0),-z[2],z[1]],[z[2],iv(0),-z[0]],[-z[1],z[0],iv(0)]]
    PCP=mm(mm(P,C),P)
    angular=mm(mm(cross,C),transpose(cross))
    D=[[PCP[i][j]-angular[i][j] for j in range(3)] for i in range(3)]
    # Cholesky radicands enclose the exact uniformly positive pivots.
    Fmat=[[iv(0) for _ in range(3)] for _ in range(3)]
    pivots=[]
    for i in range(3):
        rad=D[i][i]-sum((square(Fmat[i][k]) for k in range(i)),iv(0))
        assert rad.lo>0
        pivots.append(rad)
        Fmat[i][i]=base.sqrt_iv(rad)
        for j in range(i+1,3):
            numerator=D[j][i]-sum((Fmat[j][k]*Fmat[i][k] for k in range(i)),iv(0))
            Fmat[j][i]=numerator/Fmat[i][i]
    scale=1/(base.sqrt_iv(iv(2))*s)
    sigma=[[chi*x*scale for x in row] for row in Fmat]
    V=(N*(N-1)*q+N*sum(C[i][i] for i in range(3)))/(4*s*s)+N*bm/(2*s)
    return a,sigma,V,{'chi_interval':chi.json(),'Cholesky_pivot_intervals':[x.json() for x in pivots]}


class Draws:
    def __init__(self,L,ell,stream):
        self.L,self.ell,self.stream=L,ell,stream
        self.count=self.bits=0
        self.max_integer_bits=0
        self.counts={}
        self.coupling=None
        self.tail=None
    def scalar(self,origin):
        normal.base.ledger=normal.base.Ledger()
        start=time.perf_counter()
        data=normal.generate(self.L,self.ell)
        costs=normal.base.ledger.snapshot()
        data.update({'origin':origin,'actual_wall_seconds':time.perf_counter()-start,'costs':costs})
        self.stream.write(json.dumps(data,separators=(',',':'))+'\n')
        self.count+=1;self.bits+=data['exact_fair_random_bit_count']
        self.max_integer_bits=max(self.max_integer_bits,costs['max_observed_integer_bits'])
        for k,v in costs['explicit_operation_counts'].items(): self.counts[k]=self.counts.get(k,0)+v
        h=F(data['ideal_clipped_normal_coupling_error_upper'])
        tail=F(data['normal_tail_probability_upper'])
        self.coupling,self.tail=h,tail
        return F(data['output_rational']),h


def heat_seed(draws,N,fourthN,sqrtN,Lambda,radius,K,accept_bits,seed_id):
    a=F(2)/fourthN
    d0=1-Lambda/(2*sqrtN)
    assert 1+F(2)/(3*sqrtN)-Lambda/d0<=0 # uniform Gaussian envelope H=1
    inverse_root2=1/base.sqrt_iv(iv(2))
    attempts=[]
    max_numeric_accept_error=F(0)
    accepted=False
    for attempt in range(K):
        zs=[draws.scalar({'kind':'seed','seed':seed_id,'attempt':attempt,'axis':j}) for j in range(3)]
        xv=[iv(z)*inverse_root2 for z,_ in zs]
        x=[dyadic(mid(t)) for t in xv]
        x_numeric=sum(error_to_interval(t,v) for t,v in zip(xv,x))
        assert x_numeric<=EPS_X
        x_coupling=3*draws.coupling+x_numeric
        while True:
            r=norm_iv(x)
            cosh=even_iv(a*r,'cosh')
            sinch=even_iv(a*r,'sinch')
            logalpha=log_iv(sinch)+N*log_iv(cosh)-(2*sqrtN/d0-1)*square(r)
            # alpha<=1 is proved by the envelope, so intersect safely.
            alpha=clip(exp_iv(logalpha),F(0),F(1))
            probability=mid(alpha)
            ai=(probability*(1<<accept_bits)).numerator//(probability*(1<<accept_bits)).denominator
            ai=min(1<<accept_bits,max(0,ai))
            q=F(ai,1<<accept_bits)
            numeric_error=error_to_interval(alpha,q)
            if numeric_error<=EPS_ACCEPT: break
            IV.precision(2*IV.P)
            base.ledger.add('adaptive_completed_guard_refinements')
        max_numeric_accept_error=max(max_numeric_accept_error,numeric_error)
        raw=secrets.randbits(accept_bits)
        accept=raw<ai
        attempts.append({'attempt':attempt,'proposal_rational':[str(v) for v in x],
            'proposal_coupling_l2_upper':str(x_coupling),'log_acceptance_interval':logalpha.json(),
            'acceptance_probability_interval':alpha.json(),'quantized_acceptance':str(q),
            'accept_uniform_integer':raw,'accept_bits':accept_bits,'accepted':accept})
        if accept:
            # tanh(ar)/r = a sinch(ar)/cosh(ar), no zero division.
            while True:
                r=norm_iv(x)
                cosh=even_iv(a*r,'cosh');sinch=even_iv(a*r,'sinch')
                miv=[a*sinch/cosh*iv(v) for v in x]
                mr=norm_iv(miv)
                taper=clip(2-8*mr/radius,F(0),F(1))
                seediv=[taper*v for v in miv]
                seed=[dyadic(mid(v)) for v in seediv]
                numeric_seed_error=sum(error_to_interval(v,t) for v,t in zip(seediv,seed))
                # T_seed is 3-Lipschitz and x->Bloch has Lipschitz a.
                seed_error=3*a*x_coupling+numeric_seed_error
                # Guard inward if rounding puts a point on the outer edge.
                if sum(v*v for v in seed)>radius*radius/16:
                    shrink=F(1,2)
                    seed=[v*shrink for v in seed]
                    seed_error+=sum(abs(v) for v in seed)
                if seed_error<=EPS_SEED: break
                IV.precision(2*IV.P)
                base.ledger.add('adaptive_completed_guard_refinements')
            accepted=True
            assert seed_error<=EPS_SEED
            break
    if not accepted:
        seed=[F(0)]*3;seed_error=F(0)
    return seed,seed_error,{'attempts':attempts,'accepted':accepted,
        'exhaustion_fallback':'m=0','numeric_accept_error_upper':str(max_numeric_accept_error),
        'seed_pointwise_error_on_matching_decisions':str(seed_error)}


def clifford_emit(m,N,out):
    P=64;D=1<<P
    # Rounding each coordinate toward zero retains radius positivity exactly.
    integers=[]
    for x in m:
        y=abs(x)*D
        n=y.numerator//y.denominator
        integers.append(n if x>=0 else -n)
    emitted=[F(n,D) for n in integers]
    assert sum(abs(n) for n in integers)<D
    categories=[]
    for i,n in enumerate(integers):
        categories.append((i,1 if n>=0 else -1,abs(n)))
    categories.append((3,0,D-sum(abs(n) for n in integers)))
    counts={'+X':0,'-X':0,'+Y':0,'-Y':0,'+Z':0,'-Z':0}
    gates={'H':0,'S':0,'X':0}
    circuits={'+X':['H'],'-X':['X','H'],'+Y':['H','S'],
              '-Y':['X','H','S'],'+Z':[],'-Z':['X']}
    # Complete transcript: 65-bit words serialized in 9 bytes, unused high
    # bits are zero. A fresh word per qubit ensures conditional independence.
    with out.open('wb') as transcript:
        for _ in range(N):
            raw=secrets.randbits(P+1)
            transcript.write(raw.to_bytes(9,'big'))
            selector,coin=raw>>1,raw&1
            total=0
            for axis,sign,weight in categories:
                total+=weight
                if selector<total: break
            if axis==3: label='-Z' if coin else '+Z'
            else: label=('+' if sign>0 else '-')+'XYZ'[axis]
            counts[label]+=1
            for gate in circuits[label]: gates[gate]+=1
    assert sum(counts.values())==N
    return emitted,{'contract':'Independent local Pauli draws prepare tau_m^tensor N in the ideal fair-bit/Clifford model.',
        'Bloch_denominator_bits':P,'integer_Bloch_coefficients':integers,
        'axis_categories':[[a,s,w] for a,s,w in categories],'pure_state_counts':counts,
        'circuit_table':circuits,'actual_gate_description_counts':gates,
        'max_Clifford_gates_per_qubit':3,'ideal_fair_bits_actual':N*(P+1),
        'complete_random_word_transcript':str(out),'physical_emissions_executed':False,
        'native_device_error':'UNKNOWN; a per-qubit trace error d adds at most N*d.',
        'no_generic_angle_synthesis_required':True}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--N',type=int,default=65536)
    ap.add_argument('--proposals',type=int,default=32)
    ap.add_argument('--steps',type=int,default=4)
    ap.add_argument('--seed-cap',type=int,default=320)
    ap.add_argument('--name',default='cutoff_euler_fixture')
    args=ap.parse_args()
    N,R,T,K=args.N,args.proposals,args.steps,args.seed_cap
    fourthN=isqrt(isqrt(N))
    assert fourthN**4==N and N>=16 and R>=2 and T>=1
    rootT=isqrt(T);assert rootT*rootT==T
    sqrtN=F(fourthN**2);s=F(fourthN**3)
    dt,rootdt=F(1,T),F(1,rootT)
    M,B,Lambda,Lc=F(1,10),F(1,5),F(11,10),F(6,5)
    radius=F(1,8)
    assert radius*radius<=1/(16*(Lc+1))
    A=[[F(1,20),F(1,40),F(0)],[F(1,40),F(-1,20),F(1,80)],[F(0),F(1,80),F(0)]]
    assert max(sum(map(abs,row),F(0)) for row in A)<=M
    C=[[x+(Lambda if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(A)]
    b=[F(1,32),F(-1,16),F(1,8)]
    assert sum(v*v for v in b)<=B*B
    L,ell,accept_bits=F(7),48,80
    base.ledger=base.Ledger();IV.precision(96)
    start,cpu=time.perf_counter(),time.process_time()
    outdir=HERE/'evidence';outdir.mkdir(exist_ok=True)
    normal_path=outdir/(args.name+'_normal_transcript.jsonl')
    # Conservative acquired Cholesky Lipschitz constants, retaining N powers.
    Amag=Lc*radius/(2*sqrtN)+B/(2*s)
    La=Lc*(1+3*radius*radius)/(2*sqrtN)+B*radius/s+4*Amag/radius
    Smag=F(2)/s # sqrt(Tr C)/sqrt2 <2 at these public bounds
    Lsigma=(96*Lc*radius+8/radius)/s
    LV=Lc*radius*sqrtN/2+B*fourthN/2
    amplification_step=1+La*dt+2*L*Lsigma*rootdt
    paths=[];weights=[];endpoints=[];point_errors=[];log_errors=[]
    accept_random_bits=0
    with normal_path.open('w') as stream:
        draws=Draws(L,ell,stream)
        for i in range(R):
            m,error,seeddata=heat_seed(draws,N,F(fourthN),sqrtN,Lambda,radius,K,accept_bits,i)
            accept_random_bits+=accept_bits*len(seeddata['attempts'])
            logw=log_error=F(0)
            rows=[]
            for j in range(T):
                zs=[draws.scalar({'kind':'Euler','proposal':i,'step':j,'axis':k}) for k in range(3)]
                ziv=[IV(z-h,z+h) for z,h in zs]
                while True:
                    a,sigma,V,guard=coefficients(m,C,b,N,s,sqrtN,radius)
                    vmid=dyadic(mid(V))
                    update=[iv(m[k])+a[k]*dt+dot(sigma[k],ziv)*rootdt for k in range(3)]
                    next_m=[dyadic(mid(x)) for x in update]
                    update_error=sum(error_to_interval(x,v) for x,v in zip(update,next_m))
                    if error_to_interval(V,vmid)<=EPS_V and update_error<=EPS_UPDATE: break
                    IV.precision(2*IV.P)
                    base.ledger.add('adaptive_completed_guard_refinements')
                log_error+=dt*(LV*error+error_to_interval(V,vmid))
                logw+=dt*vmid
                error=amplification_step*error+update_error
                rows.append({'step':j,'node_before':[str(x) for x in m],
                    'potential_interval':V.json(),'numeric_update_l2_error_upper':str(update_error),
                    'accumulated_node_l2_error_upper':str(error),'guards':guard})
                m=next_m
            final_iv=projected(m,radius)
            final=[dyadic(mid(x),64) for x in final_iv]
            # Use certified inward rescaling only if rounding crosses rho.
            if sum(x*x for x in final)>radius*radius:
                norm_upper=norm_iv(final).hi
                final=[x*radius/norm_upper for x in final]
            projection_error=sum(error_to_interval(x,v) for x,v in zip(final_iv,final))
            assert projection_error<=EPS_PROJECT
            error+=projection_error
            endpoints.append(final);point_errors.append(error);log_errors.append(log_error)
            weights.append(logw)
            paths.append({'proposal':i,'seed':seeddata,'steps':rows,
                'endpoint_rational':[str(x) for x in final],'endpoint_coupling_l2_upper':str(error),
                'logweight_rational':str(logw),'logweight_coupling_error_upper':str(log_error)})
    maxlog=max(weights)
    selection_bits=64;D=1<<selection_bits
    categorical_budget=R*F(1,1<<60)
    while True:
        wiv=[exp_iv(x-maxlog) for x in weights]
        wmid=[mid(x) for x in wiv];total=sum(wmid,F(0))
        denom=sum(wiv,iv(0));probs=[x/denom for x in wiv]
        integers=[]
        for w in wmid[:-1]:
            p=w/total*D
            integers.append(p.numerator//p.denominator)
        integers.append(D-sum(integers))
        q=[F(n,D) for n in integers]
        categorical_error=sum((error_to_interval(p,x) for p,x in zip(probs,q)),F(0))/2
        if categorical_error<=categorical_budget: break
        IV.precision(2*IV.P)
        base.ledger.add('adaptive_completed_guard_refinements')
    raw=secrets.randbits(selection_bits);cumulative=0
    for selected,n in enumerate(integers):
        cumulative+=n
        if raw<cumulative: break
    emitted,gateplan=clifford_emit(endpoints[selected],N,outdir/(args.name+'_Clifford_words.bin'))
    local_round_error=sum(abs(x-y) for x,y in zip(emitted,endpoints[selected]))
    maxpoint=max(point_errors)+local_round_error
    max_logerror=max(log_errors)
    # Use assigned, globally enforced guards for the averaged-law certificate.
    # Observed tighter arithmetic enclosures are retained separately.
    uniform_point=EPS_SEED
    uniform_log=F(0)
    for _ in range(T):
        uniform_log+=dt*(LV*uniform_point+EPS_V)
        uniform_point=amplification_step*uniform_point+EPS_UPDATE
    uniform_point+=EPS_PROJECT+3*F(1,1<<64)
    weight_law_error=exp_scalar(2*uniform_log).hi-1
    # Global finite guards charge the maximum allowed draws, not realized ones.
    max_normals=3*R*(K+T)
    gaussian_tail=min(F(1),max_normals*draws.tail)
    d0=1-Lambda/(2*sqrtN)
    p0=F(1,16)*(1-F(1,12)-(Lambda/d0-1)/4)
    assert p0>0
    cap_error=min(F(1),R*(1-p0)**K)
    rmax=2*L
    seed_log_Lip=F(16,3)*rmax**3+(2*Lambda/d0+2+F(4)/(3*sqrtN))*rmax
    # xi includes proposal scaling/rounding, upper bounded here independently.
    proposal_coupling=3*draws.coupling+EPS_X
    accept_disagreement=min(F(1),R*K*(EPS_ACCEPT+seed_log_Lip*proposal_coupling))
    finite_output=min(F(1),gaussian_tail+cap_error+accept_disagreement+weight_law_error+
                      categorical_budget+F(N,2)*uniform_point)
    # Separately report discretization and averaged importance bounds.
    Q=4*La*La+16*Lsigma*Lsigma
    lag=Amag*Amag*dt*dt/3+Smag*Smag*dt/2
    strong=Q*exp_scalar(Q).hi*lag
    lambda_star=(1-radius)/2
    state_factor=base.sqrt_iv(iv(N/(8*lambda_star))).hi
    public_file=outdir/'certified_weight_constant.json'
    if N>=65536 and public_file.exists():
        public=json.loads(public_file.read_text())
        K2=F(public['constants']['weight_p_moment_upper'])
        inverse_mean=exp_scalar(B*B/2).hi
        statistical=min(F(1),inverse_mean*base.sqrt_iv(iv(K2/R)).hi)
        log_L2=2*LV*LV*(strong+lag)
        raw_euler=4*base.sqrt_iv(iv(K2*log_L2)).hi+2*state_factor*base.sqrt_iv(iv(K2*strong)).hi
        euler=min(F(1),inverse_mean*raw_euler)
    else:
        K2=None;statistical=euler=F(1)
    result={'worker_id':'c07_s03','status':'CERTIFIED_COMPLETE_FINITE_BIT_FIXED_R_T_EULER_AND_CLIFFORD_DESCRIPTIONS',
      'target_contract':'Averaged output of declared fixed-R,T heat-seed/cutoff-Euler/importance law, with ideal independent fair bits and Clifford gates. Continuous cutoff/Gibbs errors are separate.',
      'input':{'N':N,'R':R,'T':T,'seed_cap':K,'M':str(M),'B':str(B),'Lambda':str(Lambda),
        'A':[[str(x) for x in row] for row in A],'C':[[str(x) for x in row] for row in C],
        'b':[str(x) for x in b],'cutoff_radius':str(radius),'normal_cap':str(L),'normal_error_bits':ell,
        'known_parameters_supplied':True,'noncommuting_anisotropy_and_field':True},
      'certificates':{'normal_tail_union_upper':str(gaussian_tail),'heat_seed_exhaustion_union_upper':str(cap_error),
        'heat_seed_acceptance_lower':str(p0),'seed_decision_disagreement_union_upper':str(accept_disagreement),
        'max_path_endpoint_l2_error_upper':str(maxpoint),'max_path_logweight_error_upper':str(max_logerror),
        'uniform_enforced_endpoint_guard_upper':str(uniform_point),
        'uniform_enforced_logweight_guard_upper':str(uniform_log),
        'relative_logweight_law_TV_upper':str(weight_law_error),'categorical_TV_upper':str(categorical_error),
        'categorical_uniform_guard_upper':str(categorical_budget),
        'complete_finite_bit_output_trace_error_upper':str(finite_output),
        'continuous_cutoff_Euler_trace_error_upper':str(euler),'averaged_importance_trace_error_upper':str(statistical),
        'uniform_K2_used':str(K2) if K2 else 'UNAVAILABLE_BELOW_N_MIN',
        'Gibbs_or_stopped_seed_cutoff_trace_error_upper':'1; the available cone/cutoff bound is not numerically nonvacuous at this admitted fixture.',
        'full_Gibbs_trace_error_upper':'1; not an executed exponentially accurate Gibbs sampler.'},
      'acquired_constants':{'A_magnitude':str(Amag),'A_Lipschitz':str(La),'Sigma_F_magnitude':str(Smag),
        'Sigma_F_Lipschitz':str(Lsigma),'V_Lipschitz':str(LV),'Euler_Q':str(Q),
        'integrated_lag_L2_upper':str(lag),'strong_path_L2_upper':str(strong)},
      'paths':paths,'selection':{'integer_weights':integers,'denominator_bits':selection_bits,
        'uniform_integer':raw,'selected_index':selected,'scaled_weight_intervals':[x.json() for x in wiv]},
      'emitted_local_rational_Bloch':[str(x) for x in emitted],'Clifford_output':gateplan,
      'evidence':{'normal_transcript':str(normal_path),'complete_normal_draws':draws.count},
      'costs':{'actual_normal_fair_bits':draws.bits,'actual_seed_accept_fair_bits':accept_random_bits,
        'actual_categorical_fair_bits':selection_bits,'actual_local_Clifford_fair_bits':gateplan['ideal_fair_bits_actual'],
        'max_allowed_normal_draws':max_normals,'max_allowed_seed_accept_fair_bits':R*K*accept_bits,
        'max_normal_integer_bits':draws.max_integer_bits,'normal_helper_counts':draws.counts,
        'compiler_helper_counts':base.ledger.snapshot(),'wall_seconds':time.perf_counter()-start,
        'maximum_adaptive_working_dyadic_bits':IV.P,
        'cpu_seconds':time.process_time()-cpu,'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'physical_output_cells_charged':N,'physical_output_emissions_executed':False,
        'device_energy':'UNKNOWN','backend_tokens':'UNKNOWN'},
      'limitations':['Numerical certificates concern fixed R,T law and ideal output descriptions, not actual hardware.',
        'The full Gibbs error certificate is explicitly one; cone/seed cutoff constants are not upgraded by this finite run.',
        'Importance and Euler errors are separated from finite-bit errors, with their acquired public bounds retained.',
        'Random transcripts come from OS secrets; the theorem assumes ideal independent fair bits.']}
    out=outdir/(args.name+'.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(out),'status':result['status'],'selected':selected,
        'finite_bit_error_diagnostic':float(finite_output),'Euler_error_diagnostic':float(euler),
        'importance_error_diagnostic':float(statistical),'normal_draws':draws.count,
        'wall_seconds':result['costs']['wall_seconds']}))


if __name__=='__main__': main()
