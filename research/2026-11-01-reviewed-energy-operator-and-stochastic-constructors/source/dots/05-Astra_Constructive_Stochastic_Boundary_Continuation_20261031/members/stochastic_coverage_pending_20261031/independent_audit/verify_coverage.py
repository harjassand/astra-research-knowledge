#!/usr/bin/env python3
"""Independent exact verification after floating proposals; no tolerance acceptance."""
from fractions import Fraction as F
from itertools import product
from math import prod,comb
from pathlib import Path
import importlib.util,json,hashlib,copy
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_partial',HERE/'frozen_coverage_boundary.py')
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

def unpack(rec):
    assert rec['accepted']
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
    return S,Z,H,I,core,lam,death,conv,alpha,beta,raw

def gauss(A,rhs):
    """Independent forward elimination/back substitution, not candidate solve."""
    N=len(A);M=[list(map(F,row))+[F(b)] for row,b in zip(A,rhs)]
    for j in range(N):
        i=next(i for i in range(j,N) if M[i][j]);M[i],M[j]=M[j],M[i]
        for i in range(j+1,N):
            a=M[i][j]/M[j][j]
            if a:M[i]=[v-a*w for v,w in zip(M[i],M[j])]
    x=[F(0)]*N
    for i in range(N-1,-1,-1):x[i]=(M[i][-1]-sum(M[i][j]*x[j] for j in range(i+1,N)))/M[i][i]
    assert all(sum(a*b for a,b in zip(row,x))==z for row,z in zip(A,rhs))
    return x

def binary_table(core,q,H,beta):
    m=len(q);states=list(product([0,1],repeat=m));nz=len(beta[0])
    good={b for b in states if all(any(beta[h][j]*b[h]>0 for h in H) for j in range(nz))}
    assert (1,)*m in good and (0,)*m not in good
    bad=[b for b in states if b not in good];index={b:i for i,b in enumerate(bad)}
    events={};A=[[F(0)]*len(bad) for b in bad]
    for b in states:
        occupied={i for i,a in enumerate(b) if a};ev=[]
        for s,t,k in core:
            nxt=occupied.copy()
            if sum(s):
                origin=s.index(1)
                if origin not in occupied:continue
                nxt.remove(origin)
            if sum(t):nxt.add(t.index(1))
            bp=tuple(int(i in nxt) for i in range(m))
            if bp==b:continue
            rate=k*prod((q[i]**(t[i]-s[i]) for i in range(m)),start=F(1));ev.append((bp,rate))
            if b in index:
                A[index[b]][index[b]]+=rate
                if bp in index:A[index[b]][index[bp]]-=rate
        events[b]=ev
    # Every binary state is independently checked to reach the upward target.
    reach=set(good)
    while True:
        new=reach|{b for b in states if any(bp in reach for bp,k in events[b])}
        if new==reach:break
        reach=new
    assert reach==set(states)
    times=gauss(A,[F(1)]*len(bad));assert min(times)>0
    f={b:F(1)+(times[index[b]] if b in index else 0) for b in states}
    Qf={b:sum(k*(f[bp]-f[b]) for bp,k in events[b]) for b in states}
    monotone=0;map_checks=0
    def arrow(b,s,t):
        occupied={i for i,a in enumerate(b) if a}
        if sum(s):
            origin=s.index(1)
            if origin not in occupied:return b
            occupied.remove(origin)
        if sum(t):occupied.add(t.index(1))
        return tuple(int(i in occupied) for i in range(m))
    for a in states:
      for b in states:
        if all(x<=y for x,y in zip(a,b)):
            assert f[a]>=f[b];monotone+=1
            assert a not in good or b in good
            for s,t,k in core:
                ap=arrow(a,s,t);bp=arrow(b,s,t)
                assert all(x<=y for x,y in zip(ap,bp));map_checks+=1
    assert all(Qf[b]==-1 for b in bad)
    return {'states':states,'good':good,'bad':bad,'A':A,'times':times,'f':f,'Qf':Qf,'events':events,
      'F':max(f.values()),'K':max(Qf[b] for b in good),'monotone':monotone,'map_checks':map_checks}

def verify(rec,cert):
    assert cert['accepted'];S,Z,H,I,core,lam,death,conv,alpha,beta,raw=unpack(rec);m=len(S);nz=len(Z)
    T=F(cert['T']);q=list(map(F,cert['q']));v=list(map(F,cert['v']));times=list(map(F,cert['linear_hitting_times']))
    L=F(cert['L']);eta=F(cert['eta']);c=F(cert['c']);delta=F(cert['delta']);eps=F(cert['epsilon']);R=cert['R'];zs=cert['satellite_exception_threshold']
    assert T>1 and eta>0 and 0<c<=1 and delta>0 and eps>0 and R>=1 and zs>=0
    assert all(times[h]==0 for h in H)
    for i in I:assert times[i]>0 and sum(conv[i][j]*(times[j]-times[i]) for j in range(m))-death[i]*times[i]==-1
    assert all(v[i]==L+times[i] and q[i]==1+eta*v[i] for i in range(m))
    assert eta==(T-1)/L and all(q[h]==T for h in H) and all(qi>=T for qi in q)
    Qv=[sum(conv[i][j]*(v[j]-v[i]) for j in range(m))-death[i]*v[i] for i in range(m)]
    assert Qv==list(map(F,cert['Qv'])) and max(Qv)<=-1 and delta==min(eta/qi for qi in q)
    B=sum(lam[i]*(q[i]-1) for i in range(m));D=max(death[i]/q[i] for i in range(m));al=max(sum(alpha[h]) for h in H)
    assert B==F(cert['immigration_bound']) and D==F(cert['death_weight_max']) and al==F(cert['alpha_max'])
    tab=binary_table(core,q,H,beta);stored=cert['support_table']
    assert stored['accepted'] and list(map(tuple,stored['states']))==tab['states'] and list(map(tuple,stored['bad_states']))==tab['bad']
    assert [list(map(F,row)) for row in stored['killed_matrix']]==tab['A']
    assert list(map(F,stored['hitting_times']))==tab['times']
    rows={tuple(row['support']):row for row in stored['support_rows']};assert set(rows)==set(tab['states']) and len(rows)==len(stored['support_rows'])
    for b,row in rows.items():
        assert row['covered']==(b in tab['good']) and F(row['f'])==tab['f'][b] and F(row['Qf'])==tab['Qf'][b]
        assert [(tuple(bp),F(rate)) for bp,rate in row['events']]==tab['events'][b]
    Fmax=tab['F'];K=tab['K'];assert Fmax==F(stored['F']) and K==F(stored['K']) and K>=0
    assert tab['monotone']==stored['monotonicity_checks'] and B*Fmax<=F(1,4)
    trials=cert['tilt_search_trials'];dims=[]
    for n,trial in enumerate(trials):
        tt=1+F(1,2**n);qq=[1+(tt-1)*a/L for a in v];bb=sum(lam[i]*(qq[i]-1) for i in range(m))
        old=binary_table(core,qq,H,beta);passed=bb*old['F']<=F(1,4)
        assert F(trial['T'])==tt and F(trial['B'])==bb and F(trial['F'])==old['F'] and F(trial['BF'])==bb*old['F']
        assert trial['passed']==passed and passed==(n==len(trials)-1)
        assert trial['binary_linear_system_dimension']==len(old['bad']);dims.append(len(old['bad']))
    assert T==F(trials[-1]['T']) and sum(d*d for d in dims)==cert['work']['total_binary_matrix_entries']
    assert c<=delta/(4*al) and c<=1/(4*D*Fmax**2)
    margin=delta-c*al;A=B+K+c*D*Fmax
    assert margin==F(cert['margin'])>0 and A==F(cert['covered_constant_bound_A'])
    assert eps<=min(delta/4,1/(4*Fmax)) and A-margin*R<=-eps
    bmin=min(b for row in beta for b in row if b>0);assert bmin==F(cert['reverse_rate_min'])
    assert c*bmin*zs/(R+c)>=A+eps
    expr=cert['foster_C_expression'];coef=Fmax*(A+eps);qmax=max(q)
    assert not expr['expanded'] and F(expr['coefficient'])==coef and F(expr['service_base'])==qmax
    assert expr['service_exponent']==R and F(expr['satellite_base'])==T and expr['satellite_exponent']==zs
    assert expr['unreduced_numerator_bits_upper']==coef.numerator.bit_length()+R*qmax.numerator.bit_length()+zs*T.numerator.bit_length()
    assert expr['unreduced_denominator_bits_upper']==coef.denominator.bit_length()+R*qmax.denominator.bit_length()+zs*T.denominator.bit_length()
    f=tab['f']
    def support(y):return tuple(int(a>0) for a in y)
    def quotient(x):
        y=tuple(x[i] for i in S);r=sum(y);b=support(y);lv=F(0)
        for s,t,k in raw:
            rate=k*ff(x,s)
            if not rate:continue
            xp=tuple(a-u+w for a,u,w in zip(x,s,t));yp=tuple(xp[i] for i in S);rr=sum(yp)
            assert abs(rr-r)<=1
            rad=(F(r+1)/(r+1+c)) if rr==r+1 else ((r+c)/r if rr==r-1 else F(1))
            ratio=rad*f[support(yp)]/f[b]*T**sum(t[i]-s[i] for i in Z)*prod((q[i]**(yp[i]-y[i]) for i in range(m)),start=F(1))
            lv+=rate*(ratio-1)
        return lv
    def master(x):
        y=tuple(x[i] for i in S);r=sum(y);b=support(y)
        reverse=sum(beta[h][j]*y[h]*x[Z[j]] for h in H for j in range(nz))
        return B+c*D*Fmax-margin*r+(K if b in tab['good'] else -1/Fmax)-c*reverse/(r+1+c)
    def support_generator(y):
        b=support(y);drift=F(0)
        for s,t,k in core:
            rate=k*ff(y,s)*prod((q[i]**(t[i]-s[i]) for i in range(m)),start=F(1))
            if rate:
                yp=tuple(a-u+w for a,u,w in zip(y,s,t));drift+=rate*(f[support(yp)]-f[b])
        assert drift<=tab['Qf'][b]
    return quotient,master,support_generator,tab

def run_case(name,sp,raw):
    rec=p.recognize(sp,raw);assert rec['accepted'],(name,rec)
    cert=p.construct(rec);assert cert['accepted'],(name,cert)
    quotient,master,sg,tab=verify(rec,cert);S=rec['service'];Z=rec['satellites'];m=len(S);nz=len(Z);count=0;phase=0
    for r in range(7):
      for y in comps(r,m):
        sg(y);phase+=1
        for z in product([0,1,37],repeat=nz):
            x=[0]*len(sp)
            for i,a in zip(S,y):x[i]=a
            for i,a in zip(Z,z):x[i]=a
            assert quotient(tuple(x))<=master(tuple(x));count+=1
    target=0;R=cert['R'];zz=cert['satellite_exception_threshold']
    # Exercise every support, each satellite axis, and service/satellite threshold crossings.
    for b in tab['states']:
        for scale in [0,max(0,R-m),R]:
            y=[bit*(1+scale) for bit in b]
            for j in range(nz):
              for total in [0,zz,zz+1]:
                x=[0]*len(sp)
                for i,a in zip(S,y):x[i]=a
                x[Z[j]]=total;bound=master(tuple(x));assert quotient(tuple(x))<=bound
                if b not in tab['good'] or sum(y)>=R or total>zz:assert bound<=-cert['epsilon']
                target+=1
    return rec,cert,{'name':name,'T':cert['T'],'tilt_trials':len(cert['tilt_search_trials']),
      'binary_states':len(tab['states']),'killed_states':len(tab['bad']),'monotone_pairs':tab['monotone'],
      'graphical_map_comparisons':tab['map_checks'],'ordinary_master_checks':count,'actual_support_generator_checks':phase,
      'targeted_large_master_checks':target,'R':R,'Zstar':zz,'expanded_C':False,
      'unreduced_C_numerator_bits_upper':cert['foster_C_expression']['unreduced_numerator_bits_upper']}

def explicit_small_value_check(rec,cert):
    """Use the expanded small-state V, independently of bounded-jump quotient evaluation."""
    S=rec['service'];Z=rec['satellites'];q=cert['q'];T=cert['T'];c=cert['c'];raw=rec['reactions']
    f={tuple(row['support']):row['f'] for row in cert['support_table']['support_rows']}
    def value(x):
        y=tuple(x[i] for i in S);r=sum(y);b=tuple(int(a>0) for a in y)
        return prod((q[i]**y[i] for i in range(len(y))),start=F(1))*T**sum(x[i] for i in Z)*f[b]*prod((F(k)/(k+c) for k in range(1,r+1)),start=F(1))
    quotient,master,sg,tab=verify(rec,cert);count=0
    for x in product(range(3),repeat=len(rec['species'])):
        v=value(x);lv=F(0)
        for s,t,k in raw:
            rate=k*ff(x,s)
            if rate:lv+=rate*(value(tuple(a-b+d for a,b,d in zip(x,s,t)))-v)
        assert lv/v==quotient(x) and lv/v<=master(x);count+=1
    return count

def main():
    sp,raw=p.demo_network();cases=[]
    rec,cert,row=run_case('original_partial_row_network',sp,raw);cases.append(row)
    assert cert['T']==F(65,64) and cert['R']==7581 and cert['satellite_exception_threshold']==3822285280
    small=explicit_small_value_check(rec,cert)
    def u(i,a,n):return tuple(a*int(j==i) for j in range(n))
    complete=raw[:]
    for h,j in [(0,3),(1,2)]:
        aa=u(h,2,4);az=tuple(int(i==h)+int(i==j) for i in range(4));complete += [(aa,az,F(1)),(az,aa,F(1))]
    cases.append(run_case('complete_row_target_recovery',sp,complete)[2])
    # Exactly the extra inactive phase on which the earlier LP search stopped UNKNOWN.
    phase=[(s+(0,),t+(0,),k) for s,t,k in raw];zero=(0,)*5
    phase += [(zero,u(4,1,5),F(1,100)),(u(4,1,5),zero,F(10))]
    for h in [0,1]:phase += [(u(4,1,5),u(h,1,5),F(1)),(u(h,1,5),u(4,1,5),F(1,100))]
    cases.append(run_case('previous_LP_budget_UNKNOWN_inactive_phase',sp+['E'],phase)[2])
    # Only one immigration entry; simultaneous hub coverage requires sequential filling.
    zero=(0,)*5;tree=[(zero,u(0,1,5),F(1,10)),(u(0,1,5),zero,F(1,2)),
      (u(0,1,5),u(1,1,5),F(1)),(u(0,1,5),u(2,1,5),F(1)),
      (u(1,1,5),zero,F(1)),(u(2,1,5),zero,F(1)),
      (u(1,1,5),u(0,1,5),F(1,5)),(u(2,1,5),u(0,1,5),F(3,10))]
    for h,j in [(1,3),(2,4)]:
        aa=u(h,2,5);az=tuple(int(i==h)+int(i==j) for i in range(5));tree += [(aa,az,F(1)),(az,aa,F(1))]
    cases.append(run_case('single_immigration_root_simultaneous_hub_filling',['A','B','D','C','F'],tree)[2])
    # Coverage by any two of three hubs, with coalescing cyclic conversion arrows.
    zero=(0,)*6;overlap=[]
    for h in range(3):overlap += [(zero,u(h,1,6),F(h+1,10)),(u(h,1,6),zero,F(h+1)),(u(h,1,6),u((h+1)%3,1,6),F(1))]
    for h,js in [(0,[3,4]),(1,[4,5]),(2,[5,3])]:
      for j in js:
        aa=u(h,2,6);az=tuple(int(i==h)+int(i==j) for i in range(6));overlap += [(aa,az,F(1)),(az,aa,F(2,3))]
    rr,cc,row=run_case('three_hub_overlapping_coverage',['B','D','E','C','F','G'],overlap);cases.append(row)
    assert len(cc['support_table']['bad_states'])==4
    high=raw+[((0,0,5,2),(0,0,4,3),F(3,4)),((0,0,4,3),(0,0,5,2),F(5,6))]
    cases.append(run_case('seventh_order_neutral_motion',sp,high)[2])
    perm=(2,0,3,1);permuted=[(tuple(s[i] for i in perm),tuple(t[i] for i in perm),k) for s,t,k in raw]
    cases.append(run_case('species_permutation_reacquired_partition',[sp[i] for i in perm],permuted)[2])
    tamper=[]
    for kind in ['wrong_coverage','coalescing_event_omission','hitting_table','false_halving_acceptance','radial_c','compact_coefficient','compact_exponent','compact_bit_bound']:
        bad=copy.deepcopy(cert)
        if kind=='wrong_coverage':bad['support_table']['support_rows'][0]['covered']=True
        elif kind=='coalescing_event_omission':bad['support_table']['support_rows'][-1]['events']=bad['support_table']['support_rows'][-1]['events'][1:]
        elif kind=='hitting_table':bad['support_table']['hitting_times'][0]+=1
        elif kind=='false_halving_acceptance':bad['tilt_search_trials'][0]['passed']=True
        elif kind=='radial_c':bad['c']=F(1)
        elif kind=='compact_coefficient':bad['foster_C_expression']['coefficient']=F(0)
        elif kind=='compact_exponent':bad['foster_C_expression']['satellite_exponent']=0
        else:bad['foster_C_expression']['unreduced_numerator_bits_upper']=1
        try:verify(rec,bad)
        except AssertionError:tamper.append(kind)
        else:raise AssertionError('bad receipt accepted '+kind)
    support_decline=p.construct(rec,max_support_states=3);assert not support_decline['accepted'] and support_decline['required_states']==4
    trial_decline=p.construct(rec,max_tilt_trials=6);assert not trial_decline['accepted'] and len(trial_decline['search_trials'])==6
    # Architectural guards are checked on full-WR modifications.
    nonlinear=raw+[(u(0,2,4),u(0,3,4),F(1)),(u(0,3,4),u(0,2,4),F(1))]
    assert wr(nonlinear) and not p.recognize(sp,nonlinear)['accepted']
    uncovered=[(s,t,k) for s,t,k in raw if not ((s==u(1,2,4) and t==(0,1,0,1)) or (t==u(1,2,4) and s==(0,1,0,1)))]
    assert wr(uncovered) and not p.recognize(sp,uncovered)['accepted']
    original=json.loads((HERE/'frozen_results.json').read_text());verify(original['recognition'],original['certificate'])
    print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_coverage_boundary.py').read_bytes()).hexdigest(),
      'independent_exact_full_certificate_verifier':True,'frozen_JSON_independently_verified':True,'cases':cases,
      'expanded_small_state_generator_checks':small,'tampered_fields_rejected':tamper,
      'support_budget_UNKNOWN':support_decline,'tilt_budget_UNKNOWN':trial_decline,
      'full_WR_nonlinear_and_uncovered_satellite_mutations_rejected':True,
      'no_giant_C_power_expansion_attempted':True,'only_acquired_positive_exponential_range_not_all_exponents':True,
      'finite_checks_supplement_ordinary_proof':True},default=p.encode,indent=2))

if __name__=='__main__':main()
