#!/usr/bin/env python3
"""Exact structural admission and scalar sampled-core bounds; pending review.

No ODE, stationary fiber law, simulation, fiber enumeration or t^M expansion.
The optional budget caps proposed support-level power output bits only, not all
preprocessing, rational arithmetic, memory, or time. Semantic receivers share the
constructor; a separately written audit is needed for independent verification.
"""
from fractions import Fraction as F
import hashlib,json

FAMILY='common-seed-top-support-sampled-core-v1'


def rat(x):
    if type(x) not in (int,F):
        raise TypeError('exact int/Fraction required; no bool/float/string')
    return F(x)


def encode(x):
    if type(x) is F:return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x


def canonical(x):return json.dumps(encode(x),sort_keys=True,separators=(',',':'))
def ceilq(x):return -(-x.numerator//x.denominator)


def bits(x):
    if type(x) is F:return max(abs(x.numerator).bit_length(),x.denominator.bit_length())
    if type(x) is int:return abs(x).bit_length()
    if isinstance(x,dict):return max([0]+[bits(v) for v in x.values()])
    if isinstance(x,(list,tuple)):return max([0]+[bits(v) for v in x])
    return 0


def recognize(raw):
    if type(raw) not in (list,tuple) or not raw:raise ValueError('nonempty reaction list required')
    n=None;grouped={}
    for row in raw:
        if type(row) not in (tuple,list) or len(row)!=3:raise ValueError('reaction triple required')
        u,v,k=row
        if type(u) not in (tuple,list) or type(v) not in (tuple,list):raise TypeError('complex vector required')
        if n is None:n=len(u)
        if n<2 or len(u)!=n or len(v)!=n:raise ValueError('dimension n>=2 required')
        if any(type(z) is not int or z<0 for z in tuple(u)+tuple(v)):raise ValueError('integer nonnegative complexes required')
        k=rat(k)
        if k<=0:raise ValueError('positive rates required')
        u,v=tuple(u),tuple(v)
        if u!=v:grouped[u,v]=grouped.get((u,v),F(0))+k
    channels=tuple((u,v,k) for (u,v),k in sorted(grouped.items()))
    zero=(0,)*n;nc=[(u,v,k) for u,v,k in channels if sum(u)!=sum(v)];open_roles=[]
    for a in range(n):
        e=tuple(int(i==a) for i in range(n))
        if len(nc)==2 and {(u,v) for u,v,k in nc}=={(zero,e),(e,zero)}:open_roles.append(a)
    if len(open_roles)!=1:raise ValueError('one exact immigration/death pair required')
    a=open_roles[0];e=tuple(int(i==a) for i in range(n));internals=[]
    for u,v,k in channels:
        if sum(u)!=sum(v):continue
        if u[a]<1 or v[a]<1 or sum(u)<2:raise ValueError('conservative internals must preserve a common A')
        internals.append((tuple(z-int(i==a) for i,z in enumerate(u)),tuple(z-int(i==a) for i,z in enumerate(v)),k))
    graph={}
    for u,v,k in channels:graph.setdefault(u,set()).add(v);graph.setdefault(v,set())
    visits=0
    for u,v,k in channels:
        seen,todo={v},[v]
        while todo:
            z=todo.pop()
            for dest in sorted(graph[z]):
                visits+=1
                if dest not in seen:seen.add(dest);todo.append(dest)
        if u not in seen:raise ValueError('full graph is not weakly reversible')
    p=max([0]+[sum(u) for u,v,k in internals])
    return dict(n=n,a=a,lam=grouped[zero,e],mu=grouped[e,zero],channels=channels,
        stripped=tuple(internals),p=p,raw_sha256=hashlib.sha256(canonical(channels).encode()).hexdigest(),
        input_rows=len(raw),normalized_channels=len(channels),graph_edge_visits=visits)


def support(rec):
    n,a,p=rec['n'],rec['a'],rec['p'];top=[(i,u,v,k) for i,(u,v,k) in enumerate(rec['stripped']) if sum(u)==p]
    traces=[];reaction_tests=source_coordinate_tests=product_coordinate_tests=0
    for seed in range(n):
        active={seed};steps=[]
        while a not in active:
            chosen=None
            for row,u,v,k in top:
                reaction_tests+=1;enabled=True
                for j,z in enumerate(u):
                    source_coordinate_tests+=1
                    if z and j not in active:enabled=False;break
                if not enabled:continue
                added=[]
                for j,z in enumerate(v):
                    product_coordinate_tests+=1
                    if z and j not in active:added.append(j)
                if added:chosen=(row,added);break
            if chosen is None:break
            row,added=chosen
            steps.append(dict(stripped_channel=row,before=sorted(active),added=added))
            active.update(added)
        traces.append(dict(seed=seed,steps=steps,final_support=sorted(active),reaches_shifted_open=a in active))
        if a not in active:break
    success=all(z['reaches_shifted_open'] for z in traces) and len(traces)==n
    out=dict(accessible=success,traces=traces,reaction_tests=reaction_tests,
             source_coordinate_tests=source_coordinate_tests,product_coordinate_tests=product_coordinate_tests,
             top_order=p,top_channel_count=len(top))
    if not success:out['closed_face_support']=traces[-1]['final_support']
    return out


def _qualitative(rec):
    role=dict(dimension=rec['n'],open_coordinate=rec['a'],stripped_top_order=rec['p'],
              immigration=rec['lam'],death=rec['mu'])
    work=dict(input_rows=rec['input_rows'],normalized_channels=rec['normalized_channels'],
              graph_edge_visits=rec['graph_edge_visits'],numerical_support_powers=0,
              ODE_steps=0,stationary_fiber_laws=0,fiber_states_enumerated=0)
    base=dict(family=FAMILY,raw_sha256=rec['raw_sha256'],role=role,work=work)
    if rec['p']<2:
        return dict(status='UNKNOWN',reason='stripped top order below two is outside this theorem',**base)
    sw=support(rec)
    if not sw['accessible']:
        return dict(status='SUPPORT_CONDITION_FAILED_STABILITY_UNKNOWN',support=sw,
                    conclusion='no inference of instability or impossibility of another certificate',**base)
    return dict(status='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS',support=sw,
        conclusions=['nonexplosion','positive recurrence of every communicating class',
                     'every stationary exponential total-count moment finite for every finite exponent'],
        numerical_Foster_constants='not acquired by this interface',**base)


def qualitative(raw):return _qualitative(recognize(raw))


def receive_qualitative(raw,receipt):
    expected=qualitative(raw)
    return (expected['status']=='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS'
            and type(receipt) is dict and canonical(receipt)==canonical(expected))


def numerical(raw,t,max_power_bits=100000):
    t=rat(t)
    if t<=1:raise ValueError('rational t>1 required')
    if type(max_power_bits) is not int or max_power_bits<1:raise ValueError('positive integer power-bit cap required')
    rec=recognize(raw);qual=_qualitative(rec)
    if qual['status']!='CERTIFIED_ALL_FINITE_EXPONENTIAL_MOMENTS':
        return dict(status='NUMERICAL_UNKNOWN',reason='structural theorem not admitted',qualitative=qual)
    n,p=rec['n'],rec['p'];S=sum(k for u,v,k in rec['stripped']);kmin=min(k for u,v,k in rec['stripped'] if sum(u)==p)
    C=max(F(1),p**3*S);T=1/(4*C);factor=T*kmin/(4*n);ell=F(3,4*n);levels=[ell];powers=[]
    peak=bits([rec,t,C,T,factor,levels])
    for stage in range(n):
        nb=p*abs(ell.numerator).bit_length()+abs(factor.numerator).bit_length()
        db=p*ell.denominator.bit_length()+factor.denominator.bit_length()
        proposed=max(nb,db)
        if proposed>max_power_bits:
            return dict(status='NUMERICAL_UNKNOWN',reason='support-level power output bit upper bound exceeds declared cap',
                qualitative=qual,work=dict(support_powers_executed=len(powers),levels=levels,
                    attempted_stage=stage+1,proposed_power_result_bits_upper=proposed,
                    max_power_bits=max_power_bits,retained_rational_peak_bits=peak,
                    cap_scope='support-level power output preflight only; not all arithmetic, input, memory or wall time'))
        new=min(ell,factor*ell**p)
        powers.append(dict(stage=stage+1,exponent=p,power_product_bits_upper=proposed))
        ell=new;levels.append(ell);peak=max(peak,bits([ell,nb,db]))
    delta=ell;K0=64*n*C*T/(delta*delta);K=K0+2/delta
    M0=max(p,ceilq(8*C*T/delta));a=(rec['lam']+rec['mu'])*T+K*(1+rec['lam']/rec['mu'])
    rho=(1+1/t)/2;Mcut=max(1,M0,ceilq(2*a*(t+1)));H=1/rec['mu']+1/rec['lam']
    Lpref=(t-rho)/(1-rho)
    assert Lpref==2*t+1 and rho<1
    constants=dict(C=C,T=T,k_min=kmin,levels=levels,delta=delta,K0=K0,K=K,
        minimum_mass_for_activation=M0,combined_bad_event_constant=a,rho=rho,M_cut=Mcut,
        maximum_mean_physical_cycle=H,
        sampled_Foster_constant=dict(prefactor=t-rho,base=t,exponent=Mcut),
        sampled_stationary_moment_bound=dict(prefactor=Lpref,base=t,exponent=Mcut),
        continuous_stationary_bound_formula='H*L*(lambda+mu*(L-1)/(t-1)), L=(2*t+1)*t^M_cut',
        continuous_stationary_positive_upper_sum=[
            dict(prefactor=H*rec['lam']*Lpref,base=t,exponent=Mcut),
            dict(prefactor=H*rec['mu']*Lpref*Lpref/(t-1),base=t,exponent=2*Mcut)],
        stationary_mean_cycle_time_interval=dict(lower=1/(2*rec['lam']),upper=1/rec['lam']),
        stationary_mean_cycle_time_identity='lambda*E_pi_e H=(1+E_pi_e p_loss)/2',
        continuous_stationary_flow_bound=dict(prefactor=2*rec['lam']*H*Lpref,base=t,exponent=Mcut),
        finite_head_size_symbolic=dict(operation='binomial',upper=Mcut+n-1,lower=n),
        head_states_enumerated=False,stationary_power_expanded=False,
        interpretation='sampled-core drift and continuous stationary moment bound; not a one-step physical generator Lyapunov')
    peak=max(peak,bits(constants))
    return dict(status='CERTIFIED_SAMPLED_CORE_AND_STATIONARY_MOMENT_BOUND',t=t,qualitative=qual,constants=constants,
        work=dict(support_powers_executed=n,power_preflights=powers,max_power_bits=max_power_bits,
            retained_rational_peak_bits=peak,
            cap_scope='support-level power output preflight only; not all arithmetic, input, memory or wall time',
            finite_fiber_linear_systems_solved=0,ODE_steps=0,simulations=0))


def receive_numerical(raw,t,max_power_bits,receipt):
    expected=numerical(raw,t,max_power_bits)
    return (expected['status']=='CERTIFIED_SAMPLED_CORE_AND_STATIONARY_MOMENT_BOUND'
            and type(receipt) is dict and canonical(receipt)==canonical(expected))


def opposing_raw():
    raw=[((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1))]
    for u,v,k,l in [((1,2,0),(1,1,1),1,1),((1,1,1),(1,0,2),2,1),((1,1,1),(2,1,0),1,1)]:
        raw.extend([(u,v,F(k)),(v,u,F(l))])
    return raw


def catalytic_lift(raw):
    """Diagnostic raw lift: each stripped source/target gets every catalyst once."""
    rec=recognize(raw);a,n=rec['a'],rec['n'];z=(0,)*n;e=tuple(int(i==a) for i in range(n))
    out=[(z,e,rec['lam']),(e,z,rec['mu'])]
    for u,v,k in rec['stripped']:
        for j in range(n):
            out.append((tuple(x+int(i==a)+int(i==j) for i,x in enumerate(u)),
                        tuple(x+int(i==a)+int(i==j) for i,x in enumerate(v)),k))
    return out


if __name__=='__main__':
    print(json.dumps(encode(numerical(opposing_raw(),F(2))),indent=2,sort_keys=True))
