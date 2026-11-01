#!/usr/bin/env python3
"""Independent raw/support/work and rational scalar receiving, stdlib only.
Does not import the candidate implementation. Ordinary Python assertions enabled.
"""
from fractions import Fraction as F
import json,hashlib,sys

# Trusted local exact research process; mirror the documented wire-domain setting.
# This process-wide decimal conversion setting is not a resource/security budget.
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)

FAMILY='common-seed-top-support-sampled-core-v1'
CAP='support-level power output preflight only; not all arithmetic, input, memory or wall time'
def rat(x):
    if type(x)not in (int,F):raise ValueError('exact rational domain')
    return F(x)
def wire(x):return json.loads(json.dumps(x,default=lambda z:str(z) if type(z)is F else (_ for _ in ()).throw(TypeError(type(z)))))
def canon(x):return json.dumps(wire(x),sort_keys=True,separators=(',',':'))
def peak(x):
    out=0;stack=[x]
    while stack:
        z=stack.pop()
        if type(z)is F:out=max(out,abs(z.numerator).bit_length(),z.denominator.bit_length())
        elif type(z)is int:out=max(out,abs(z).bit_length())
        elif isinstance(z,dict):stack.extend(z.values())
        elif isinstance(z,(list,tuple)):stack.extend(z)
    return out
def ceilq(z):return (z.numerator+z.denominator-1)//z.denominator

def recognize(raw):
    assert type(raw)in (list,tuple) and raw
    grouped={};n=None
    for row in raw:
        assert type(row)in (list,tuple) and len(row)==3
        u,v,k=row;assert type(u)in (list,tuple) and type(v)in (list,tuple)
        if n is None:n=len(u)
        assert n>=2 and len(u)==len(v)==n
        assert all(type(x)is int and x>=0 for x in tuple(u)+tuple(v))
        k=rat(k);assert k>0;u,v=tuple(u),tuple(v)
        if u!=v:grouped[u,v]=grouped.get((u,v),F(0))+k
    channels=tuple((u,v,k)for (u,v),k in sorted(grouped.items()));zero=(0,)*n
    nonconservative=[(u,v,k)for u,v,k in channels if sum(u)!=sum(v)]
    births=[(u,v,k)for u,v,k in nonconservative if u==zero and sum(v)==1]
    assert len(nonconservative)==2 and len(births)==1
    _,e,lam=births[0];a=e.index(1);assert (e,zero)in grouped
    stripped=[]
    for u,v,k in channels:
        if sum(u)!=sum(v):assert (u,v)in [(zero,e),(e,zero)];continue
        assert u[a]>=1 and v[a]>=1 and sum(u)>=2
        stripped.append((tuple(z-int(j==a)for j,z in enumerate(u)),tuple(z-int(j==a)for j,z in enumerate(v)),k))
    adj={u:set()for u,v,k in channels}|{v:set()for u,v,k in channels};reach={}
    for u,v,k in channels:adj[u].add(v)
    for start in adj:
        active={start};front={start}
        while front:
            new=set().union(*(adj[z]for z in front))-active;active|=new;front=new
        reach[start]=active
    assert all(u in reach[v]for u,v,k in channels)
    visits=sum(sum(len(adj[z])for z in reach[v])for u,v,k in channels)
    return dict(n=n,a=a,lam=lam,mu=grouped[e,zero],channels=channels,stripped=tuple(stripped),
                p=max([0]+[sum(u)for u,v,k in stripped]),raw_sha256=hashlib.sha256(canon(channels).encode()).hexdigest(),
                input_rows=len(raw),normalized_channels=len(channels),graph_edge_visits=visits)

def support(rec):
    n,a,p=rec['n'],rec['a'],rec['p'];top=[(i,u,v,k)for i,(u,v,k)in enumerate(rec['stripped'])if sum(u)==p]
    traces=[];tests=source=target=0
    for seed in range(n):
        active={seed};steps=[]
        while a not in active:
            eligible=[h for h,(_,u,v,k)in enumerate(top)
                      if {j for j,z in enumerate(u)if z}<=active and not {j for j,z in enumerate(v)if z}<=active]
            chosen=min(eligible)if eligible else None
            # Reconstruct the declared first-enabled scan's work from its tested prefix.
            for i,u,v,k in top[:chosen+1 if chosen is not None else len(top)]:
                tests+=1;absent=[j for j,z in enumerate(u)if z and j not in active]
                source+=min(absent)+1 if absent else n
                if not absent:target+=n
            if chosen is None:break
            i,u,v,k=top[chosen];added=sorted({j for j,z in enumerate(v)if z}-active)
            steps.append(dict(stripped_channel=i,before=sorted(active),added=added));active.update(added)
        traces.append(dict(seed=seed,steps=steps,final_support=sorted(active),reaches_shifted_open=a in active))
        if a not in active:
            # Also check the algebraic closed-face meaning independently of scan choice.
            assert all(not {j for j,z in enumerate(u)if z}<=active or {j for j,z in enumerate(v)if z}<=active for i,u,v,k in top)
            break
    success=len(traces)==n and all(z['reaches_shifted_open']for z in traces)
    out=dict(accessible=success,traces=traces,reaction_tests=tests,source_coordinate_tests=source,
             product_coordinate_tests=target,top_order=p,top_channel_count=len(top))
    if not success:out['closed_face_support']=traces[-1]['final_support']
    return out

def qual_from_record(rec):
    base=dict(family=FAMILY,raw_sha256=rec['raw_sha256'],
              role=dict(dimension=rec['n'],open_coordinate=rec['a'],stripped_top_order=rec['p'],immigration=rec['lam'],death=rec['mu']),
              work=dict(input_rows=rec['input_rows'],normalized_channels=rec['normalized_channels'],graph_edge_visits=rec['graph_edge_visits'],
                        numerical_support_powers=0,ODE_steps=0,stationary_fiber_laws=0,fiber_states_enumerated=0))
    if rec['p']<2:return dict(status='UNKNOWN',reason='stripped top order below two is outside this theorem',**base)
    sw=support(rec)
    if not sw['accessible']:return dict(status='SUPPORT_CONDITION_FAILED_STABILITY_UNKNOWN',support=sw,
                                       conclusion='no inference of instability or impossibility of another certificate',**base)
    return dict(status='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS',support=sw,
                conclusions=['nonexplosion','positive recurrence of every communicating class',
                             'every stationary exponential total-count moment finite for every finite exponent'],
                numerical_Foster_constants='not acquired by this interface',**base)
def qualitative(raw):return qual_from_record(recognize(raw))
def receive_qualitative(raw,receipt):
    try:z=qualitative(raw)
    except (AssertionError,ValueError,TypeError,KeyError):return False
    return type(receipt)is dict and z['status']=='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS' and canon(z)==canon(receipt)

def numerical(raw,t,cap):
    t=rat(t);assert t>1 and type(cap)is int and cap>=1
    rec=recognize(raw);qual=qual_from_record(rec)
    if qual['status']!='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS':return dict(status='NUMERICAL_UNKNOWN',reason='structural theorem not admitted',qualitative=qual)
    n,p=rec['n'],rec['p'];S=sum(k for u,v,k in rec['stripped']);kmin=min(k for u,v,k in rec['stripped']if sum(u)==p)
    C=max(F(1),p*p*p*S);T=1/(4*C);factor=T*kmin/(4*n);level=F(3,4*n);levels=[level];preflights=[]
    retained=peak([rec,t,C,T,factor,levels])
    for step in range(1,n+1):
        nb=p*abs(level.numerator).bit_length()+abs(factor.numerator).bit_length()
        db=p*level.denominator.bit_length()+factor.denominator.bit_length();bound=max(nb,db)
        if bound>cap:return dict(status='NUMERICAL_UNKNOWN',reason='support-level power output bit upper bound exceeds declared cap',qualitative=qual,
                                 work=dict(support_powers_executed=len(preflights),levels=levels,attempted_stage=step,
                                           proposed_power_result_bits_upper=bound,max_power_bits=cap,retained_rational_peak_bits=retained,cap_scope=CAP))
        new=factor*pow(level,p);level=min(level,new);levels.append(level)
        preflights.append(dict(stage=step,exponent=p,power_product_bits_upper=bound));retained=max(retained,peak([level,nb,db]))
    delta=level;K0=64*n*C*T/(delta*delta);K=K0+2/delta;M0=max(p,ceilq(8*C*T/delta))
    bad=(rec['lam']+rec['mu'])*T+K*(1+rec['lam']/rec['mu']);rho=(1+1/t)/2;cut=max(1,M0,ceilq(2*bad*(t+1)))
    H=1/rec['mu']+1/rec['lam'];Lpref=2*t+1
    assert (t-rho)/(1-rho)==Lpref
    constants=dict(C=C,T=T,k_min=kmin,levels=levels,delta=delta,K0=K0,K=K,minimum_mass_for_activation=M0,
        combined_bad_event_constant=bad,rho=rho,M_cut=cut,maximum_mean_physical_cycle=H,
        sampled_Foster_constant=dict(prefactor=t-rho,base=t,exponent=cut),
        sampled_stationary_moment_bound=dict(prefactor=Lpref,base=t,exponent=cut),
        continuous_stationary_bound_formula='H*L*(lambda+mu*(L-1)/(t-1)), L=(2*t+1)*t^M_cut',
        continuous_stationary_positive_upper_sum=[dict(prefactor=H*rec['lam']*Lpref,base=t,exponent=cut),dict(prefactor=H*rec['mu']*Lpref*Lpref/(t-1),base=t,exponent=2*cut)],
        stationary_mean_cycle_time_interval=dict(lower=1/(2*rec['lam']),upper=1/rec['lam']),
        stationary_mean_cycle_time_identity='lambda*E_pi_e H=(1+E_pi_e p_loss)/2',
        continuous_stationary_flow_bound=dict(prefactor=2*rec['lam']*H*Lpref,base=t,exponent=cut),
        pointwise_mean_cycle_time_upper=1/rec['lam'],
        pointwise_mean_cycle_time_identity='lambda*E_x H=p_up+p_loss',
        continuous_stationary_first_birth_bound=dict(prefactor=2*Lpref,base=t,exponent=cut),
        finite_head_size_symbolic=dict(operation='binomial',upper=cut+n-1,lower=n),head_states_enumerated=False,stationary_power_expanded=False,
        interpretation='sampled-core drift and continuous stationary moment bound; not a one-step physical generator Lyapunov')
    retained=max(retained,peak(constants))
    return dict(status='CERTIFIED_SAMPLED_CORE_AND_STATIONARY_MOMENT_BOUND',t=t,qualitative=qual,constants=constants,
        work=dict(support_powers_executed=n,power_preflights=preflights,max_power_bits=cap,retained_rational_peak_bits=retained,cap_scope=CAP,
                  finite_fiber_linear_systems_solved=0,ODE_steps=0,simulations=0))

def receive_numerical(raw,t,cap,receipt):
    try:z=numerical(raw,t,cap)
    except (AssertionError,ValueError,TypeError,KeyError):return False
    return type(receipt)is dict and z['status']=='CERTIFIED_SAMPLED_CORE_AND_STATIONARY_MOMENT_BOUND' and canon(z)==canon(receipt)

def check_scalar_proof(receipt):
    z=wire(receipt);c=z['constants'];role=z['qualitative']['role'];n=role['dimension'];p=role['stripped_top_order'];t=F(z['t'])
    C,T,d,K0,K=map(F,[c['C'],c['T'],c['delta'],c['K0'],c['K']]);M0=c['minimum_mass_for_activation'];cut=c['M_cut'];bad=F(c['combined_bad_event_constant']);rho=F(c['rho'])
    assert C*T==F(1,4) and d>0 and M0>=p and C*T/M0<=d/8
    assert (d/4+C*T/M0)*F(4,3)<=d/2
    checked=[]
    for M in [cut,cut+1,2*cut,10**50*cut]:
        ratio=1/t+(t-1/t)*bad/M;assert ratio<=rho<1;checked.append(dict(M=M,ratio=ratio))
    # Exact symbolic power z=t^cut: compare coefficients, never expand z.
    H=F(c['maximum_mean_physical_cycle']);lam=F(role['immigration']);mu=F(role['death']);l=2*t+1
    upper=c['continuous_stationary_positive_upper_sum']
    assert F(upper[0]['prefactor'])==H*lam*l and F(upper[1]['prefactor'])==H*mu*l*l/(t-1)
    assert H*mu*l/(t-1)>0 # amount by which the positive upper sum exceeds the sharper bound, per z
    assert c['stationary_mean_cycle_time_identity']=='lambda*E_pi_e H=(1+E_pi_e p_loss)/2'
    assert F(c['stationary_mean_cycle_time_interval']['lower'])==1/(2*lam)
    assert F(c['stationary_mean_cycle_time_interval']['upper'])==1/lam
    assert c['continuous_stationary_flow_bound']==wire(dict(prefactor=2*lam*H*l,base=t,exponent=cut))
    assert mu*cut>=lam # Bernoulli implies the former Jensen bound is no smaller.
    assert F(c['pointwise_mean_cycle_time_upper'])==1/lam
    assert c['pointwise_mean_cycle_time_identity']=='lambda*E_x H=p_up+p_loss'
    assert c['continuous_stationary_first_birth_bound']==wire(dict(prefactor=2*l,base=t,exponent=cut))
    return checked
