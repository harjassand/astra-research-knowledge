#!/usr/bin/env python3
"""Acquire raw support witnesses and exact physical-return/head data.

The mathematical proof is in the two support-principle files. This constructor
does not acquire the true finite-head trace or a numerical stationary constant.
Large rationals use exact hex tags. Budget refusal is separate from raw scope.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import json

P=Path(__file__).resolve().parent
BIT_BUDGET=200000
MAX_BITS=0

class Budget(Exception):pass
def cq(v):
    v=F(v);return -(-v.numerator//v.denominator)
def bounded(v):
    global MAX_BITS
    v=F(v);bits=max(abs(v.numerator).bit_length(),v.denominator.bit_length())
    MAX_BITS=max(MAX_BITS,bits)
    if bits>BIT_BUDGET:raise Budget('constructed rational exceeds bit budget')
    return v
def power(v,n):
    n=int(n);v=F(v)
    if n<0:return power(1/v,-n)
    if n*max(v.numerator.bit_length(),v.denominator.bit_length())>BIT_BUDGET:
        raise Budget('power upper bit cost exceeds budget')
    return bounded(v**n)
def p2(n):
    n=int(n)
    if abs(n)+1>BIT_BUDGET:raise Budget('power-of-two exponent exceeds bit budget')
    return bounded(F(2)**n)
def csqrt(v):
    v=F(v);n=isqrt(v.numerator//v.denominator)
    return n if n*n*v.denominator>=v.numerator else n+1
def enc(v):
    v=F(v)
    def integer(n):return str(n) if abs(n).bit_length()<=4096 else hex(n)
    return {'numerator':integer(v.numerator),'denominator':integer(v.denominator)}

def canon(raw):
    table={};d=None
    for y,z,c in raw:
        if d is None:d=len(y)
        if len(y)!=d or len(z)!=d or any(type(v) is not int or v<0 for v in tuple(y)+tuple(z)):
            raise ValueError('invalid integer endpoints')
        if type(c) not in (int,str,F):raise ValueError('rate must be an exact rational, not float/bool')
        c=F(c)
        if c<=0:raise ValueError('nonpositive rate')
        if tuple(y)==tuple(z):continue
        key=(tuple(y),tuple(z));table[key]=table.get(key,F(0))+c
    if d is None or not table:raise ValueError('empty genuine list')
    return d,[(y,z,c) for (y,z),c in sorted(table.items())]

def weakly_reversible(raw):
    adj={}
    for y,z,c in raw:adj.setdefault(y,set()).add(z);adj.setdefault(z,set())
    for y,z,c in raw:
        seen={z};todo=[z]
        while todo:
            v=todo.pop()
            for w in adj[v]-seen:seen.add(w);todo.append(w)
        if y not in seen:return False
    return True

def support_witnesses(d,leading):
    witnesses=[]
    for initial in range(d):
        active={initial};steps=[]
        while 0 not in active:
            found=False
            for index,(y,z,c) in enumerate(leading):
                if all(not a or i in active for i,a in enumerate(y)):
                    added=[i for i,a in enumerate(z) if a and i not in active]
                    if added:
                        steps.append({'leading_channel_index':index,'added_species':added})
                        active.update(added);found=True;break
            if not found:return None,initial
        assert len(steps)<=d-1
        witnesses.append({'initial_singleton':initial,'support_steps':steps})
    return witnesses,None

def classify(raw):
    d,raw=canon(raw);zero=(0,)*d;A=(1,)+(0,)*(d-1)
    if not weakly_reversible(raw):return None,'full raw list is not weakly reversible'
    lam=next((c for y,z,c in raw if y==zero and z==A),None)
    mu=next((c for y,z,c in raw if y==A and z==zero),None)
    if lam is None or mu is None:return None,'missing sole port 0<->A'
    internal=[e for e in raw if (e[0],e[1]) not in [(zero,A),(A,zero)]]
    if not internal:return None,'ordinary one-species birth/death baseline'
    if any(sum(y)!=sum(z) for y,z,c in internal):return None,'additional count-changing reaction'
    gate=min(v[0] for y,z,c in internal for v in [y,z])
    residual=[((y[0]-gate,)+y[1:],(z[0]-gate,)+z[1:],c) for y,z,c in internal]
    ell=max(sum(y) for y,z,c in residual)
    if ell<2:return None,'ordinary linear residual baseline, outside this constructor'
    leading=[e for e in residual if sum(e[0])==ell]
    witness,bad=support_witnesses(d,leading)
    if witness is None:return None,'leading residual singleton '+str(bad)+' does not activate A'
    return {'d':d,'raw':raw,'internal':internal,'residual':residual,'leading':leading,
            'gate':gate,'ell':ell,'D':gate+ell,'lambda':lam,'mu':mu,'witnesses':witness},None

def stirling(n):
    s=[[0]*(n+1) for _ in range(n+1)];s[0][0]=1
    for i in range(1,n+1):
        for j in range(1,i+1):s[i][j]=s[i-1][j-1]+j*s[i-1][j]
    return s
def shifted_poisson_bound(m,z,u):
    s=stirling(m+1)
    return bounded(p2(cq(2*z*(u-1)))*sum(F(s[m+1][j+1])*power(z*u,j) for j in range(m+1)))

def activation_data(info,eps_kind):
    d,ell=info['d'],info['ell'];leading=info['leading'];K=sum(e[2] for e in info['residual'])
    Kh=sum(e[2] for e in leading);Kl=K-Kh;kmin=min(e[2] for e in leading);T=d+1
    b=p2(-cq(2*ell*Kh*T));delta=bounded(b/d)
    for _ in range(d-1):delta=min(delta,bounded(kmin*power(delta,ell)*b*b))
    if eps_kind=='catalytic':
        a=info['gate'];birth=info['lambda']/factorial(a);death=info['mu']/factorial(a-1)
        epsilon=bounded(delta*b/(16*d));port_error=birth+death;port_rate=birth+death
    else:
        birth=info['lambda'];death=info['mu'];epsilon=delta/2
        port_error=birth+2*death;port_rate=birth+2*death
    LF=ell*ell*F(2)**ell*Kh;CE=ell**3*F(3)**(ell-1)*Kh+ell*F(2)**(ell-1)*Kl+port_error
    Q=F(2)**ell*K+port_rate;bF=p2(-cq(2*LF*T));h=bounded(epsilon*bF/2)
    gamma=bounded(h*h/(4*(ell*ell*Q*T+ell*h)));c=min(gamma,F(1,2))
    C=2*d+p2(cq(2*birth*T));track=cq(max(ell,2*CE*T/(epsilon*bF)))
    return {'T':F(T),'b':b,'delta':delta,'epsilon':epsilon,'C_E':CE,'Q':Q,
            'b_F':bF,'gamma':gamma,'c':c,'C':C,'n_track':F(track),
            'K':K,'birth_op_bound':birth,'death_op_bound':death}

def acquire(raw,u=F(21,20),t=F(11,10),bit_budget=200000):
    global BIT_BUDGET,MAX_BITS
    BIT_BUDGET=bit_budget;MAX_BITS=0
    try:info,reason=classify(raw)
    except (ValueError,TypeError,ZeroDivisionError) as e:return {'scope_status':'UNKNOWN','reason':str(e)}
    if info is None:return {'scope_status':'UNKNOWN','reason':reason}
    summary={'d':info['d'],'gate':info['gate'],'residual_degree':info['ell'],'original_degree':info['D'],
             'rates':[{'source':y,'product':z,'rate':enc(c)} for y,z,c in info['raw']],
             'support_witnesses':info['witnesses']}
    try:
        u,t=F(u),F(t)
        if not 1<u<t:raise ValueError('need exact 1<u<t')
        if info['d']>8 or info['ell']>8 or info['gate']>16 or len(info['raw'])>128:
            raise Budget('prototype quantitative dimension/degree/list budget')
        a,ell,D=info['gate'],info['ell'],info['D'];lam,mu=info['lambda'],info['mu'];dt=1-1/t;zeta=1-u/t
        data=activation_data(info,'catalytic' if a else 'ungated');T=data['T'];delta=data['delta'];K=data['K'];c=data['c'];C=data['C']
        req={}
        if a:
            b=data['b'];astar=bounded(delta*b/8);H=cq((a*(t-1)+4)/(dt*mu*astar));Bt=p2(cq(lam*(t*t-1)))
            Jc=bounded(2+power(3,a)*power(2,ell-1)*H/T);CJ=bounded(C*Jc+p2(cq(2*lam)));cm=min(c/2,F(1,2))
            eb=bounded(1/(16*power(t,a)*Bt));Cp=(data['birth_op_bound']+data['death_op_bound'])*T
            nreq={'n_positive':F(1),'gate_size':F(a),'mature_time':F(H),'tracking':2*data['n_track'],
                  'mature_immigration':2*lam*H*(t-1),'favorable_lower_exit':2*a+8/dt,
                  'mature_error_polynomial':power(2*(D-2)/cm,2),'mature_error_size':bounded(2*CJ/(cm*eb*eb)),
                  'activation_port_error':16*power(t,a+1)*Cp,'activation_tracking_error':16*power(t,a)*C/c}
            p=power(lam/(lam+mu*a),a);Cseed=bounded(F(a)/p*(1+1/lam)*power(u,a))
            Camp=bounded(T*(K+data['birth_op_bound']+data['death_op_bound']+F(1,factorial(a))))
            Cmat=bounded(H*power(2,D)*(1+lam+mu+K)*shifted_poisson_bound(D,lam,u))
            Call=bounded(Cseed+power(u,a)*(Camp+Cmat))
            req={'all_phase_thresholds':a+max(cq(v) for v in nreq.values()),
                 'occupation_polynomial':cq(power(2*(D-1)/zeta,2)),
                 'occupation_size':cq(8*Call/zeta),'unit_margin':cq(4/dt)}
            data.update({'a_star':astar,'mature_H':F(H),'mature_J_coefficient':Jc,'mature_error_C':CJ,
                         'mature_error_c':cm,'bad_tolerance':eb,'C_seed':Cseed,'C_amp':Camp,'C_mat':Cmat,'C_all':Call})
            theorem='CATALYTIC_SUPPORT_PRINCIPLE.md';outmargin='1/2';costpow=D-1
        else:
            bt=dt*mu*delta/4;eta=min(bt,F(1))/2;ao=eta/2
            Ct=csqrt(C)*p2(cq(lam*T*(t*t-1)));p=ell-2
            Co=bounded(T*(1+lam+mu+K)*shifted_poisson_bound(ell,lam*T,u))
            req={'tracking':cq(data['n_track']),'port_output':cq(4*lam*T*t/(mu*delta)),
                 'output_error_polynomial':cq(power(4*p/c,2)), 'output_error_size':cq(8*Ct/(c*eta)),
                 'occupation_polynomial':cq(power(2*(ell-1)/zeta,2)),
                 'occupation_size':cq(4*Co/(zeta*ao)), 'unit_margin':csqrt(2*factorial(ell)/(ao*power(dt,ell)))}
            data.update({'output_margin_coefficient':ao,'C_occ':Co});nreq={}
            theorem='HYDRO_ACTIVATION_RECEIVER.md';outmargin='a_out*N^(2-m)';costpow=1
        head=max(req.values())+1;bounded(head)
        return {'scope_status':'RAW_SUPPORT_MATCH','quantitative_status':'GLOBAL_RETURN_REWARD_HEAD_ACQUIRED',
                'scope':'Same-principal ordinary theorem/certificate; no independent audit or priority claim.',
                'raw':summary,'theorem':theorem,'u':enc(u),'t':enc(t),'parameters':{k:enc(v) for k,v in data.items()},
                'residual_phase_thresholds':{k:enc(v) for k,v in nreq.items()},
                'head_requirements':{k:enc(v) for k,v in req.items()},'head_N':enc(head),
                'contract':'E[entire integral (1+q)*u^N + V(actual output)] <= V(input)-1 outside acquired head; V=t^N outside and zero inside.',
                'output_margin':outmargin,'occupation_polynomial_degree':costpow,
                'finite_head_trace_and_stationary_constant':'NOT_ACQUIRED; theorem uses proved finite irreducible head trace existentially.',
                'materialized_head_bits':head.bit_length(),'largest_recorded_rational_bits':MAX_BITS,
                'stationary_powers_materialized':False,'not_claimed':['unrestricted weak-reversibility admission','mixing gap','stationary fiber','practical head','numerical stationary normalizer']}
    except Budget as e:
        return {'scope_status':'RAW_SUPPORT_MATCH','raw':summary,'quantitative_status':'REFUSED_BUDGET','reason':str(e),'head_N':'NOT_ACQUIRED'}
    except ValueError as e:return {'scope_status':'RAW_SUPPORT_MATCH','quantitative_status':'INVALID_PARAMETERS','reason':str(e)}

def diagnostic(gate=0):
    A=(1,0,0,0);zero=(0,0,0,0)
    pairs=[((0,2,0,0),(0,1,0,1),2),((0,0,0,2),(0,1,0,1),1),
           ((0,1,0,1),(0,0,2,0),1),((0,0,2,0),(1,0,1,0),1)]
    raw=[(zero,A,1),(A,zero,1)]
    for y,z,c in pairs:
        yy=(y[0]+gate,)+y[1:];zz=(z[0]+gate,)+z[1:]
        raw.extend([(yy,zz,c),(zz,yy,1)])
    return raw

if __name__=='__main__':
    rows=[]
    for gate in [0,1,2]:
        cert=acquire(diagnostic(gate));assert cert['quantitative_status']=='GLOBAL_RETURN_REWARD_HEAD_ACQUIRED'
        f=P/'results'/('support_receiver_gate'+str(gate)+'.json');f.write_text(json.dumps(cert,indent=2)+'\n')
        rows.append({'gate':gate,'head_bits':cert['materialized_head_bits'],'largest_rational_bits':cert['largest_recorded_rational_bits'],'file':f.name})
    bad=diagnostic(1);bad=[e for e in bad if set([e[0],e[1]])!={ (1,0,0,2),(1,1,0,1)}]
    no=acquire(bad);assert no['scope_status']=='UNKNOWN' and 'singleton' in no['reason']
    limited=acquire(diagnostic(1),bit_budget=100);assert limited['quantitative_status']=='REFUSED_BUDGET' and limited['head_N']=='NOT_ACQUIRED'
    print(json.dumps({'certificates':rows,'unsupported_support_control':no,'budget_control':{'scope_status':limited['scope_status'],'quantitative_status':limited['quantitative_status']}},indent=2))
