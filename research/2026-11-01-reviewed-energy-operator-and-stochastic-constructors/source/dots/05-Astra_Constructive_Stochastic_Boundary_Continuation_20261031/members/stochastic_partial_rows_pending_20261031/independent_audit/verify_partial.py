#!/usr/bin/env python3
"""Independent exact verification after floating proposals; no tolerance acceptance."""
from fractions import Fraction as F
from itertools import product
from math import prod,comb
from pathlib import Path
import importlib.util,json,hashlib,copy
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_partial',HERE/'frozen_partial_boundary.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def comps(r,m):
    if m==1:yield (r,)
    elif m==0:
        if r==0:yield ()
    else:
        for a in range(r+1):
            for rest in comps(r-a,m-1):yield (a,)+rest

def ff(x,s):
    if any(a<b for a,b in zip(x,s)):return 0
    return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,s))

def wr(raw):
    vertices={s for s,t,k in raw}|{t for s,t,k in raw};adj={s:[] for s in vertices}
    for s,t,k in raw:adj[s].append(t)
    for s,t,k in raw:
        seen={t};todo=[t]
        while todo:
            a=todo.pop()
            for b in adj[a]:
                if b not in seen:seen.add(b);todo.append(b)
        if s not in seen:return False
    return True

def verify(rec,cert):
    assert rec['accepted'] and cert['accepted']
    S=tuple(rec['service']);Z=tuple(rec['satellites']);H=tuple(rec['hubs']);I=tuple(rec['inactive'])
    m=len(S);nz=len(Z);n=m+nz
    assert m and nz and H and sorted(S+Z)==list(range(n)) and not set(S)&set(Z)
    assert sorted(H+I)==list(range(m)) and not set(H)&set(I)
    raw=[(tuple(s),tuple(t),F(k)) for s,t,k in rec['reactions']]
    assert all(len(s)==len(t)==n and k>0 and all(type(a)==int and a>=0 for a in s+t) for s,t,k in raw)
    assert wr(raw)
    core=[];alpha=[[F(0)]*nz for _ in range(m)];beta=copy.deepcopy(alpha)
    for s,t,k in raw:
        if all(s[i]==t[i]==0 for i in Z) and sum(s)<=1 and sum(t)<=1:
            core.append((tuple(s[i] for i in S),tuple(t[i] for i in S),k));continue
        found=False
        for h in range(m):
            aa=tuple(2*int(i==S[h]) for i in range(n))
            for j in range(nz):
                az=tuple(int(i==S[h])+int(i==Z[j]) for i in range(n))
                if s==aa and t==az:alpha[h][j]+=k;found=True
                if s==az and t==aa:beta[h][j]+=k;found=True
        if not found:assert all(s[i]==t[i] for i in S) and sum(s)==sum(t)
    derivedH={h for h in range(m) if any(alpha[h]) or any(beta[h])}
    assert derivedH==set(H)
    assert all((alpha[h][j]>0)==(beta[h][j]>0) for h in H for j in range(nz))
    assert all(any(beta[h][j]>0 for h in H) for j in range(nz))
    zero=(0,)*m;unit=[tuple(int(i==j) for i in range(m)) for j in range(m)];V={zero,*unit}
    for initial in V:
        seen={initial};todo=[initial]
        while todo:
            a=todo.pop()
            for s,t,k in core:
                if s==a and t not in seen:seen.add(t);todo.append(t)
        assert seen==V
    lam=[sum(k for s,t,k in core if s==zero and t==unit[i]) for i in range(m)]
    death=[sum(k for s,t,k in core if s==unit[i] and t==zero) for i in range(m)]
    conv=[[sum(k for s,t,k in core if s==unit[i] and t==unit[j]) if i!=j else F(0) for j in range(m)] for i in range(m)]
    assert all(death[h]>0 for h in H)
    T=F(cert['T']);q=list(map(F,cert['q']));v=list(map(F,cert['v']));times=list(map(F,cert['hitting_times']))
    L=F(cert['L']);eta=F(cert['eta']);c=F(cert['c']);delta=F(cert['delta']);R=cert['R'];R0=cert['initial_R']
    eps=F(cert['epsilon']);gamma=F(cert['gamma']);C=F(cert['foster_C']);teps=F(cert['tail_epsilon'])
    assert T>1 and eta>0 and 0<c<=1 and 0<eps<=teps and gamma>0 and C>=0 and R>=R0>=2
    assert all(times[h]==0 for h in H)
    for i in I:assert times[i]>0 and sum(conv[i][j]*(times[j]-times[i]) for j in range(m))-death[i]*times[i]==-1
    assert all(v[i]==L+times[i] and q[i]==1+eta*v[i] for i in range(m))
    assert all(q[h]==T for h in H) and all(qi>=T for qi in q)
    Qv=[sum(conv[i][j]*(v[j]-v[i]) for j in range(m))-death[i]*v[i] for i in range(m)]
    assert Qv==list(map(F,cert['Qv'])) and max(Qv)<=-1
    assert 0<delta<=min(eta/qi for qi in q)
    al=F(cert['alpha_max']);D=F(cert['death_weight_max']);B=F(cert['immigration_bound'])
    assert al>=max(sum(alpha[h]) for h in H) and D>=max(death[i]/q[i] for i in range(m))
    assert B>=sum(lam[i]*(q[i]-1) for i in range(m))
    margin=delta-c*al;assert margin>0 and B+2*c*D-margin*R0<=-teps
    states=list(map(tuple,cert['head_states']));weights=list(map(F,cert['head_weights']));index={y:i for i,y in enumerate(states)};N=len(states)
    assert len(weights)==N==len(index)==comb(R+m-1,m)
    assert set(states)=={y for r in range(R) for y in comps(r,m)} and min(weights)>0
    assert max(w.denominator for w in weights)<=cert['rationalization_denominator_limit']
    def gg(r):return prod((F(i)/(i+c) for i in range(1,r)),start=F(1))
    def base(y):
        assert sum(y)>=1
        return prod((q[i]**y[i] for i in range(m)),start=F(1))*gg(sum(y))
    def h(y):return weights[index[y]] if y in index else base(y)
    def hform(y):
        a=[F(0)]*(N+1)
        if y in index:a[index[y]]=1
        else:a[-1]=base(y)
        return a
    def actual_form(y,z):
        # Direct original-generator action on the symbolic h vector, divided by T^|z|.
        x=[0]*n
        for i,a in zip(S,y):x[i]=a
        for i,a in zip(Z,z):x[i]=a
        hy=hform(y);a=[F(0)]*(N+1)
        for s,t,k in raw:
            rate=k*ff(x,s)
            if not rate:continue
            xp=tuple(xx-u+w for xx,u,w in zip(x,s,t));yp=tuple(xp[i] for i in S)
            factor=T**(sum(xp[i] for i in Z)-sum(z));nextform=hform(yp)
            a=[v0+rate*(factor*v1-v2) for v0,v1,v2 in zip(a,nextform,hy)]
        return a
    def ev(a):return sum(x*y for x,y in zip(a[:-1],weights))+a[-1]
    rows={tuple(row['service_state']):row for row in cert['finite_state_rows']}
    assert set(rows)=={y for r in range(R+1) for y in comps(r,m)} and len(rows)==len(cert['finite_state_rows'])
    expected_constraints=[]
    for r in range(R+1):
      for y in comps(r,m):
        hy=h(y);hv=hform(y);constant=actual_form(y,(0,)*nz)
        # At z=0 and unit satellite populations, extract the exact affine coefficients.
        sat=[]
        for j in range(nz):
            z=tuple(int(i==j) for i in range(nz));v0=actual_form(y,z)
            sat.append([a-b for a,b in zip(v0,constant)])
        covered=all(any(beta[h0][j]*y[h0]>0 for h0 in H) for j in range(nz))
        row=rows[y];actualH=ev(constant)/hy;slopes=[-ev(a)/hy for a in sat]
        assert row['covered']==covered and actualH==F(row['constant_quotient']) and slopes==list(map(F,row['satellite_slopes']))
        if not covered:
            assert actualH<=-eps and min(slopes)>=0 and row['satellite_head_bound'] is None
            expected_constraints.append((['uncovered_constant',list(y)],[a+eps*b for a,b in zip(constant,hv)]))
        else:
            assert min(slopes)>=gamma
            zm=row['satellite_head_bound'];assert type(zm)==int and zm>=-1
            assert actualH-min(slopes)*max(0,zm+1)<=-eps
            if zm>=0:assert C>=hy*T**zm*max(F(0),actualH+eps)
        for j,a in enumerate(sat):
            constraint=[x+(gamma*z if covered else 0) for x,z in zip(a,hv)]
            if any(constraint):expected_constraints.append((['satellite',list(y),j,covered],constraint))
    assert len(expected_constraints)==len(cert['lp_inequalities'])==len(cert['exact_lp_residuals'])
    for (label,coeff),row,resid in zip(expected_constraints,cert['lp_inequalities'],cert['exact_lp_residuals']):
        assert json.dumps(label)==json.dumps(row['label']) and coeff==list(map(F,row['coefficients']))
        assert ev(coeff)==F(resid)<=0
    assert cert['search_trials'][-1]['exact_accepted'] and F(cert['search_trials'][-1]['max_exact_residual'])==max(map(F,cert['exact_lp_residuals']))
    def val(x):return T**sum(x[i] for i in Z)*h(tuple(x[i] for i in S))
    def gen(x):
        value=val(x);lv=F(0)
        for s,t,k in raw:
            rate=k*ff(x,s)
            if rate:lv+=rate*(val(tuple(a-b+d for a,b,d in zip(x,s,t)))-value)
        return value,lv
    return gen

def run_case(name,sp,raw,T=F(2),**kwargs):
    rec=p.recognize(sp,raw);assert rec['accepted'],(name,rec)
    cert=p.construct(rec,T,**kwargs)
    if not cert['accepted']:return rec,cert,{'name':name,'accepted':False,'receipt':cert}
    gen=verify(rec,cert);count=0
    for r in range(cert['R']+4):
      for y in comps(r,len(rec['service'])):
        for z in product([0,1,17,300],repeat=len(rec['satellites'])):
            x=[0]*len(sp)
            for i,a in zip(rec['service'],y):x[i]=a
            for i,a in zip(rec['satellites'],z):x[i]=a
            v,lv=gen(tuple(x));assert lv<=-cert['epsilon']*v+cert['foster_C'];count+=1
    return rec,cert,{'name':name,'accepted':True,'T':str(T),'R':cert['R'],'head_states':len(cert['head_states']),
      'inequalities':len(cert['lp_inequalities']),'finite_service_states':len(cert['finite_state_rows']),
      'exact_states':count,'strictly_covered_service_states':sum(row['covered'] for row in cert['finite_state_rows']),
      'maximum_exact_residual':cert['search_trials'][-1]['max_exact_residual'],
      'search_trials':cert['search_trials']}

def failed_float_control():
    """Capture the rejected numerical candidate, then diagnose directly from its raw generator."""
    old=json.loads((HERE/'frozen_failed_search_alpha2.json').read_text())
    rec0=old['recognition'];raw=[(tuple(s),tuple(t),F(k)) for s,t,k in rec0['reactions']]
    rec=p.recognize(rec0['species'],raw);original=p.linprog;captures=[]
    def capture(*args,**kwargs):
        out=original(*args,**kwargs)
        if out.success:captures.append([float(x) for x in out.x])
        return out
    p.linprog=capture
    try:outcome=p.construct(rec)
    finally:p.linprog=original
    assert not outcome['accepted'] and captures
    encoded=json.loads(json.dumps(outcome,default=p.encode))
    assert encoded==old['outcome']
    weights=[F(x).limit_denominator(10**9) for x in captures[-1]];R=outcome['search_trials'][-1]['R']
    assert R==32 and len(weights)==528
    # Independently reconstruct the coefficients for this particular raw two-hub case.
    assert rec['service']==(0,1) and rec['satellites']==(2,3)
    T=F(2);q=(F(2),F(2));c=F(1,16);epsilon=F(1,1000);gamma=min(epsilon,c/(2*(R+c)))
    heads={y:w for y,w in zip((y for r in range(R) for y in comps(r,2)),weights)}
    from functools import lru_cache
    @lru_cache(None)
    def h(y):
        if y in heads:return heads[y]
        return T**sum(y)*prod((F(i)/(i+c) for i in range(1,sum(y))),start=F(1))
    def generator_div_sat(y,z):
        x=y+z;value=T**sum(z)*h(y);lv=F(0)
        for s,t,k in raw:
            rate=k*ff(x,s)
            if rate:
                xp=tuple(a-b+d for a,b,d in zip(x,s,t));lv+=rate*(T**sum(xp[2:])*h(xp[:2])-value)
        return lv/T**sum(z)
    residuals=[]
    for r in range(R+1):
      for y in comps(r,2):
        constant=generator_div_sat(y,(0,0));covered=all(y)
        if not covered:residuals.append((constant+epsilon*h(y),['uncovered_constant',y]))
        for j in range(2):
            unit=tuple(int(i==j) for i in range(2));slope=generator_div_sat(y,unit)-constant
            # Exactly zero unoccupied reverse rows were not added by the proposal LP.
            if covered or y[j]:residuals.append((slope+(gamma*h(y) if covered else 0),['satellite',y,j,covered]))
    largest,label=max(residuals,key=lambda x:x[0])
    assert largest==F(352851,8388608000)>0
    positives=[{'label':lab,'exact_violation':v} for v,lab in residuals if v>0]
    return {'same_rejected_search_receipt_reproduced':True,'floating_success_did_not_accept':True,
      'R':R,'unknown_not_exact_infeasibility':True,'independently_recomputed_largest_violation':largest,
      'violating_label':label,'all_positive_violations':positives,
      'captured_rationalized_candidate_sha256':hashlib.sha256(json.dumps(list(map(str,weights))).encode()).hexdigest()}

def main():
    sp,raw=p.demo_network();cases=[]
    rec,cert,row=run_case('original_partial_rows',sp,raw);assert cert['accepted'];cases.append(row)
    assert cert['R']==8 and len(cert['head_states'])==36 and len(cert['lp_inequalities'])==89
    assert len(cert['finite_state_rows'])==45 and sum(r['covered'] for r in cert['finite_state_rows'])==28
    # Stronger complete-row shape is recovered by the same unconstrained finite LP machinery.
    def unit(i,a,n):return tuple(a*int(j==i) for j in range(n))
    complete=raw[:]
    for h,j in [(0,3),(1,2)]:
        aa=unit(h,2,4);az=tuple(int(i==h)+int(i==j) for i in range(4));complete += [(aa,az,F(1)),(az,aa,F(1))]
    cases.append(run_case('complete_row_recovery',sp,complete)[2])
    cases.append(run_case('larger_T_proposal_is_separate',sp,raw,F(3),max_radius_trials=4)[2])
    perm=(2,0,3,1);permuted=[(tuple(s[i] for i in perm),tuple(t[i] for i in perm),k) for s,t,k in raw]
    cases.append(run_case('species_permutation_reacquires_roles',[sp[i] for i in perm],permuted)[2])
    high=raw+[((0,0,5,2),(0,0,4,3),F(3,4)),((0,0,4,3),(0,0,5,2),F(5,6))]
    cases.append(run_case('seventh_order_neutral_channels',sp,high)[2])
    # An additional inactive service phase changes q and adds genuinely new finite fibers.
    n=5;phase=[(s+(0,),t+(0,),k) for s,t,k in raw];zero=(0,)*n
    phase += [(zero,unit(4,1,n),F(1,100)),(unit(4,1,n),zero,F(10))]
    for hub in [0,1]:phase += [(unit(4,1,n),unit(hub,1,n),F(1)),(unit(hub,1,n),unit(4,1,n),F(1,100))]
    cases.append(run_case('additional_inactive_service_phase',sp+['E'],phase,max_head_states=200,max_radius_trials=4)[2])
    rejected=[]
    for kind in ['weight_zero','boundary_coverage','covered_flag','false_exact_residual','LP_form','gamma_zero','Foster_constant_zero']:
        bad=copy.deepcopy(cert)
        if kind=='weight_zero':bad['head_weights'][0]=F(0)
        elif kind=='boundary_coverage':bad['finite_state_rows']=bad['finite_state_rows'][:-1]
        elif kind=='covered_flag':bad['finite_state_rows'][0]['covered']=True
        elif kind=='false_exact_residual':bad['exact_lp_residuals'][0]=-999
        elif kind=='LP_form':bad['lp_inequalities'][0]['coefficients'][0]+=1
        elif kind=='gamma_zero':bad['gamma']=0
        else:bad['foster_C']=0
        try:verify(rec,bad)
        except AssertionError:rejected.append(kind)
        else:raise AssertionError('tamper accepted '+kind)
    # Full WR is preserved by these mutations; structural rejection is separate from instability.
    nonlinear=raw+[(unit(0,2,4),unit(0,3,4),F(1)),(unit(0,3,4),unit(0,2,4),F(1))]
    assert wr(nonlinear) and not p.recognize(sp,nonlinear)['accepted']
    uncovered=[(s,t,k) for s,t,k in raw if not ((s==unit(1,2,4) and t==(0,1,0,1)) or (t==unit(1,2,4) and s==(0,1,0,1)))]
    assert wr(uncovered) and not p.recognize(sp,uncovered)['accepted']
    short=p.construct(rec,max_radius_trials=1);assert not short['accepted'] and len(short['search_trials'])==1
    budget=p.construct(rec,max_head_states=35);assert not budget['accepted'] and budget['required_head_states']==36 and len(budget['search_trials'])==2
    failed=failed_float_control()
    original=json.loads((HERE/'frozen_results.json').read_text());verify(original['recognition'],original['certificate'])
    print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_partial_boundary.py').read_bytes()).hexdigest(),
       'independent_raw_generator_affine_forms_verified':True,'frozen_JSON_independently_verified':True,
       'cases':cases,'tampered_fields_rejected':rejected,'raw_WR_nonlinear_service_and_uncovered_satellite_mutations_rejected':True,
       'radius_trial_budget_UNKNOWN':short,'head_budget_UNKNOWN':budget,'floating_success_exactly_rejected_control':failed,
       'accepted_T_only_no_all_exponents_claim':True,'no_termination_or_exact_infeasibility_claim':True,
       'finite_state_tests_not_theorem_proof':True},default=p.encode,indent=2))

if __name__=='__main__':main()
