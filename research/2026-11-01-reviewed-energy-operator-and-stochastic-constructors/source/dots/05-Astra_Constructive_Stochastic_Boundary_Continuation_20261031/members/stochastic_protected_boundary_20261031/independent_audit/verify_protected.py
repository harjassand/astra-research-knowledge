#!/usr/bin/env python3
"""Independent exact finite certificate audit; no simulations or float proposals."""
import importlib.util, pathlib,sys,json,hashlib,copy
from fractions import Fraction as F
from itertools import product
from math import prod,ceil
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_phase',HERE/'frozen_protected_boundary.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def comps(r,m):
    if m==0:
        if r==0:yield ()
    elif m==1:yield (r,)
    else:
        for i in range(r+1):
            for rest in comps(r-i,m-1):yield (i,)+rest

def ff(x,s):
    if any(a<b for a,b in zip(x,s)):return 0
    return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,s))

def wr(raw):
    C={s for s,t,k in raw}|{t for s,t,k in raw};adj={s:[] for s in C}
    for s,t,k in raw:adj[s].append(t)
    for s,t,k in raw:
        seen={t};stack=[t]
        while stack:
            y=stack.pop()
            for v in adj[y]:
                if v not in seen:seen.add(v);stack.append(v)
        if s not in seen:return False
    return True

def verify(rec,cert):
    """Does not call construct(), solve(), recognize(), value(), or generator()."""
    assert cert['accepted'];S=tuple(rec['service']);Z=tuple(rec['satellites'])
    H=tuple(rec['hubs']);I=tuple(rec['inactive']);m=len(S);nz=len(Z);n=m+nz
    assert set(S).isdisjoint(Z) and sorted(S+Z)==list(range(n)) and H and nz
    assert sorted(H+I)==list(range(m)) and set(H).isdisjoint(I)
    raw=[(tuple(s),tuple(t),F(k)) for s,t,k in rec['reactions']]
    assert wr(raw)
    core=[];linear=[];univariate=[];alpha=[[F(0)]*nz for _ in range(m)];beta=copy.deepcopy(alpha);neutral=[]
    for s,t,k in raw:
        if all(s[i]==t[i]==0 for i in Z) and sum(s)<=1 and sum(t)<=1:
            edge=(tuple(s[i] for i in S),tuple(t[i] for i in S),k)
            core.append(edge);linear.append(edge);continue
        local_s=tuple(s[i] for i in S);local_t=tuple(t[i] for i in S)
        support_s={i for i,a in enumerate(local_s) if a};support_t={i for i,a in enumerate(local_t) if a}
        if all(s[i]==t[i]==0 for i in Z) and len(support_s)==1 and support_s==support_t:
            edge=(local_s,local_t,k);core.append(edge);univariate.append(edge);continue
        matched=False
        for h in range(m):
            aa=tuple(2*int(i==S[h]) for i in range(n))
            for j in range(nz):
                az=tuple(int(i==S[h])+int(i==Z[j]) for i in range(n))
                if s==aa and t==az:alpha[h][j]+=k;matched=True
                if s==az and t==aa:beta[h][j]+=k;matched=True
        if not matched:
            assert all(s[i]==t[i] for i in S) and sum(s)==sum(t)
            neutral.append((s,t,k))
    assert all(alpha[h][j]>0 and beta[h][j]>0 for h in H for j in range(nz))
    assert all(alpha[i][j]==beta[i][j]==0 for i in I for j in range(nz))
    zero=(0,)*m;units=[tuple(int(i==j) for i in range(m)) for j in range(m)]
    allC={zero,*units};adj={y:[] for y in allC}
    for s,t,k in linear:adj[s].append(t)
    for source in allC:
        seen={source};stack=[source]
        while stack:
            y=stack.pop()
            for z in adj[y]:
                if z not in seen:seen.add(z);stack.append(z)
        assert seen==allC
    d=[sum(k for s,t,k in linear if s==units[i] and t==zero) for i in range(m)]
    lam=[sum(k for s,t,k in linear if s==zero and t==units[i]) for i in range(m)]
    k=[[sum(a for s,t,a in linear if s==units[i] and t==units[j]) if i!=j else F(0) for j in range(m)] for i in range(m)]
    assert all(d[h]>0 for h in H)
    for i in range(m):
        edges=[((sum(s),),(sum(t),),k) for s,t,k in univariate if s[i]]
        assert not edges or wr(edges)
    T=F(cert['T']);eta=F(cert['eta']);c=F(cert['c']);R=cert['R'];eps=F(cert['epsilon']);C=F(cert['foster_C'])
    q=list(map(F,cert['q']));v=list(map(F,cert['v']));thit=list(map(F,cert['hitting_times']));L=F(cert['common_level_L'])
    assert T>1 and eta>0 and c>0 and R>=2 and eps>0 and C>=0
    assert all(thit[h]==0 for h in H) and all(thit[i]>0 for i in I)
    for i in I:assert sum(k[i][j]*(thit[j]-thit[i]) for j in range(m))-d[i]*thit[i]==-1
    assert all(v[i]==L+thit[i] and q[i]==1+eta*v[i] for i in range(m))
    assert all(q[h]==T for h in H) and all(qi>=T for qi in q)
    Qv=[sum(k[i][j]*(v[j]-v[i]) for j in range(m))-d[i]*v[i] for i in range(m)]
    assert all(z<=-1 for z in Qv)
    delta=F(cert['delta']);al=F(cert['alpha_max']);D=F(cert['death_weight_max']);B=F(cert['immigration_bound'])
    teps=F(cert['tail_epsilon']);margin=F(cert['tail_margin'])
    assert 0<delta<=min(eta/qi for qi in q)
    assert al>=max(sum(alpha[h]) for h in H) and D>=max(d[i]/q[i] for i in range(m))
    assert B>=sum(lam[i]*(q[i]-1) for i in range(m))
    def gg0(r):
        assert r>=1
        return prod((F(i)/(i+c) for i in range(1,r)),start=F(1))
    jump=max([1]+[abs(sum(t)-sum(s)) for s,t,k in univariate]);assert jump==cert['max_service_jump']
    nonlin=cert['nonlinear_tail_radius'];assert nonlin>=max(2,jump+1) and R>=nonlin
    ratio_expected=[]
    for s,t,k in univariate:
        a=sum(s);b=sum(t)
        if a>b:
            i=next(i for i,z in enumerate(s) if z);djump=a-b
            ratio=q[i]**(-djump)*gg0(nonlin-djump)/gg0(nonlin)
            bound=(1+q[i]**(-djump))/2;assert ratio<=bound
            ratio_expected.append((i,a,b,ratio,bound))
    last=cert['nonlinear_ratio_trials'][-1]
    assert last['passed'] and last['radius']==nonlin
    assert [(row['phase'],row['source'],row['target'],F(row['ratio']),F(row['threshold'])) for row in last['ratios']]==ratio_expected
    extra=F(0);boundrows={row['phase']:row for row in cert['univariate_polynomial_bounds']}
    expected_phases={i for i in range(m) if any(s[i] for s,t,k in univariate)}
    assert set(boundrows)==expected_phases and len(boundrows)==len(cert['univariate_polynomial_bounds'])
    for i,row in boundrows.items():
        edges=[(sum(s),sum(t),k) for s,t,k in univariate if s[i]]
        degree=max(a for a,b,k in edges);coeff=[F(0)]*(degree+1);terms=[]
        for a,b,k0 in edges:
            factor=k0*(q[i]**(b-a)-1)/(2 if b<a else 1)
            terms.append((a,b,factor));fall=[F(1)]
            for root in range(a):
                nxt=[F(0)]*(len(fall)+1)
                for j,v0 in enumerate(fall):nxt[j]-=root*v0;nxt[j+1]+=v0
                fall=nxt
            for j,v0 in enumerate(fall):coeff[j]+=factor*v0
        assert coeff==list(map(F,row['coefficients'])) and coeff[-1]<0
        assert terms==[(t['source'],t['target'],F(t['coefficient'])) for t in row['terms']]
        lower=sum(max(F(0),a) for a in coeff[:-1]);cut=row['cutoff']
        assert lower==F(row['positive_lower_coefficient_sum']) and cut>=max(1,lower/(-coeff[-1]))
        values=[sum(a*n0**j for j,a in enumerate(coeff)) for n0 in range(cut)]
        assert values==list(map(F,row['finite_values']))
        bound=F(row['global_upper_bound']);assert bound>=max([F(0)]+values);extra+=bound
    assert extra==F(cert['extra_core_tail_constant']) and B+extra==F(cert['effective_immigration_constant'])
    Beff=B+extra
    assert margin==delta-c*al>0 and Beff+2*c*D-margin*R<=-teps and 0<eps<=teps/2
    head={tuple(y):F(u) for y,u in zip(cert['head_states'],cert['head_weights'])}
    expected=set()
    for r in range(R):
        for yi in comps(r,len(I)):
            y=[0]*m
            for i,a in zip(I,yi):y[i]=a
            expected.add(tuple(y))
    assert set(head)==expected and len(head)==len(cert['head_states'])
    assert all(u>0 and eps*u<=1 for u in head.values())
    def gg(r):
        assert r>=1
        return prod((F(i)/(i+c) for i in range(1,r)),start=F(1))
    def base(y):
        return prod((q[i]**y[i] for i in range(m)),start=F(1))*gg(sum(y)) if sum(y) else F(1)
    def h(y):
        return head[y] if y in head else base(y)
    def cj(y):
        for s,t,a in core:
            rate=a*ff(y,s)
            if rate:yield tuple(y[i]-s[i]+t[i] for i in range(m)),rate
    for y,u in head.items():assert sum(rate*(h(yp)-u) for yp,rate in cj(y))==-1
    # The formerly unguarded inactive fringe is now checked exhaustively.
    fringe={tuple(row['service_state']):row for row in cert['inactive_fringe_rows']}
    expected_fringe=set()
    for level in range(R,R+jump):
      for yi in comps(level,len(I)):
        y=[0]*m
        for i,a in zip(I,yi):y[i]=a
        expected_fringe.add(tuple(y))
    assert set(fringe)==expected_fringe and len(fringe)==len(cert['inactive_fringe_rows'])
    for y,row in fringe.items():
        actual=sum(rate*(h(yp)-base(y)) for yp,rate in cj(y))/base(y)
        assert actual==F(row['exact_core_quotient']) and row['passed'] and actual<=-teps/2
    # Reconstruct autonomous protected binary clock using set updates.
    clock=cert['activation_clock'];ell=len(I)
    assert clock['accepted'] and clock['method']=='protected-binary-support-domination'
    expected_clock=set()
    for bits in product([0,1],repeat=ell):
        y=[0]*m
        for i,a in zip(I,bits):y[i]=a
        expected_clock.add(tuple(y))
    states=list(map(tuple,clock['clock_states']));index={y:i for i,y in enumerate(states)};nc=len(states)
    assert set(states)==expected_clock and nc==2**ell and len(index)==nc and clock['clock_linear_system_dimension']==nc
    mat=[[F(0)]*nc for _ in states];exitrows=[]
    for b,row in index.items():
        occupied={i for i,a in enumerate(b) if a}
        for source,target,rate in linear:
            nxt=occupied.copy()
            if sum(source):
                i=source.index(1)
                if i not in occupied:continue
                nxt.remove(i)
            if sum(target):nxt.add(target.index(1))
            bp=tuple(int(i in nxt) for i in range(m))
            if bp==b:continue
            mat[row][row]+=rate
            if bp in index:mat[row][index[bp]]-=rate
            else:
                assert any(bp[h] for h in H);exitrows.append((b,bp,rate))
    assert mat==[list(map(F,row)) for row in clock['clock_matrix']]
    assert exitrows==[(tuple(a),tuple(b),F(k)) for a,b,k in clock['clock_hub_exits']]
    times=list(map(F,clock['clock_hitting_means']))
    assert len(times)==nc and min(times)>0
    assert all(sum(a*t for a,t in zip(row,times))==1 for row in mat)
    mean=times[index[(0,)*m]]
    assert F(clock['uniform_activation_mean_upper'])==mean
    # Finite positive-forcing support and a sufficient scalar-radius witness.
    term=cert['termination_witness'];K=term['forcing_radius_K']
    assert K>=nonlin and delta*K>=Beff+2*c*D+1 and K>=c/(T-1) and T**K*gg(K)>=1
    forcing={tuple(row['service_state']):F(row['forcing']) for row in term['forcing_rows']}
    expected_forcing=set()
    for r in range(K):
        for yi in comps(r,len(I)):
            y=[0]*m
            for i,a in zip(I,yi):y[i]=a
            expected_forcing.add(tuple(y))
    assert set(forcing)==expected_forcing and len(forcing)==len(term['forcing_rows'])
    for y,f in forcing.items():assert f==1+sum(rate*(base(yp)-base(y)) for yp,rate in cj(y))
    M=F(term['positive_forcing_bound_M']);excess=F(term['uniform_positive_head_excess_bound'])
    assert M>=max([F(0)]+list(forcing.values())) and excess>=M*mean
    assert all(u-base(y)<=excess for y,u in head.items())
    di=max((d[i] for i in I),default=F(0));rb=term['guaranteed_scalar_radius']
    down=[(sum(s),k0) for s,t,k0 in univariate if sum(s)>sum(t) and any(s[i] for i in I)]
    degree=max([1]+[a for a,k0 in down]);leak=di+sum(k0 for a,k0 in down)
    assert F(term['inactive_death_max'])==di and term['leakage_degree']==degree
    assert F(term['leakage_coefficient'])==leak and rb>=max(cert['initial_R'],K)
    lhs=T**rb*gg(rb);rhs=2*leak*rb**degree*excess/teps
    assert lhs==F(term['radius_inequality_lhs']) and rhs==F(term['radius_inequality_rhs']) and lhs>=rhs
    assert T*rb**(degree+1)>=(rb+c)*(rb+1)**degree
    # Finite active layer coverage is independently enumerated.
    rows={tuple(row['service_state']):row for row in cert['active_layer_rows']}
    expect_active={y for r in range(1,R+jump) for y in comps(r,m) if any(y[j] for j in H)}
    assert set(rows)==expect_active and len(rows)==len(cert['active_layer_rows'])
    for y,row in rows.items():
        r=sum(y);hy=h(y)
        constant=sum(rate*(h(yp)-hy) for yp,rate in cj(y))/hy
        if r>=2:constant+=c/(r-1)*sum(sum(alpha[j])*y[j]*(y[j]-1) for j in H)
        slopes=[c/(r+c)*sum(beta[j][z]*y[j] for j in H) for z in range(nz)]
        assert constant==F(row['constant_quotient']) and slopes==list(map(F,row['satellite_slopes']))
        assert min(slopes)>0
        zmax=row['satellite_head_bound'];assert constant-min(slopes)*max(0,zmax+1)<=-eps
        if zmax>=0:assert C>=hy*T**zmax*max(F(0),constant+eps)
    # Readable independent V and generator closures for stress tests.
    def val(x):
        y=tuple(x[i] for i in S);return T**sum(x[i] for i in Z)*h(y)
    def gen(x):
        a=val(x);lv=F(0)
        for s,t,k0 in raw:
            rate=k0*ff(x,s)
            if rate:
                xp=tuple(x[i]-s[i]+t[i] for i in range(n));lv+=rate*(val(xp)-a)
        return a,lv
    return gen

def run_case(name,sp,raw,T=F(2)):
    rec=p.recognize(sp,raw);assert rec['accepted'],(name,rec)
    cert=p.construct(rec,T);assert cert['accepted'],(name,cert)
    gen=verify(rec,cert);m=len(rec['service']);nz=len(rec['satellites']);S=rec['service'];Z=rec['satellites'];count=0
    for r in range(cert['R']+cert['max_service_jump']+2):
        for y in comps(r,m):
            for totalz in [0,1,17,300]:
                zs=[(totalz,)+(0,)*(nz-1)]
                if nz>1:zs += [(0,)*(nz-1)+(totalz,),tuple(totalz//nz+int(i<totalz%nz) for i in range(nz))]
                for z in zs:
                    x=[0]*len(sp)
                    for i,a in zip(S,y):x[i]=a
                    for i,a in zip(Z,z):x[i]=a
                    V,LV=gen(tuple(x));assert LV<=-cert['epsilon']*V+cert['foster_C'];count+=1
    return rec,cert,{'name':name,'T':str(T),'R':cert['R'],'inactive_head_states':len(cert['head_states']),
      'active_layer_states':len(cert['active_layer_rows']),'exact_states':count,
      'Foster_C_bits':max(cert['foster_C'].numerator.bit_length(),cert['foster_C'].denominator.bit_length())}


def coupling_challenge(rec,raw):
    """Independent marked-event coupling audit, with counts large enough for 4->1."""
    from collections import defaultdict
    S=tuple(rec['service']);Z=tuple(rec['satellites']);m=len(S);n=len(S)+len(Z)
    linear=[(tuple(s[i] for i in S),tuple(t[i] for i in S),F(k)) for s,t,k in raw
            if all(s[i]==t[i]==0 for i in Z) and sum(s)<=1 and sum(t)<=1]
    cases=events=decreasing_extra=coalescences=0
    for counts in product(range(5),repeat=m):
      for zcount in [0,1]:
        x=[0]*n
        for i,a in zip(S,counts):x[i]=a
        if Z:x[Z[0]]=zcount
        for bits in product([0,1],repeat=m):
            if any(a>b for a,b in zip(bits,counts)):continue
            occupied={i for i,a in enumerate(bits) if a};actual=defaultdict(F);projected=defaultdict(F);binary=defaultdict(F)
            for s,t,k in raw:
                rate=F(k)*ff(x,s)
                if not rate:continue
                xp=tuple(a-u+v for a,u,v in zip(x,s,t));local_s=tuple(s[i] for i in S);local_t=tuple(t[i] for i in S)
                islinear=all(s[j]==t[j]==0 for j in Z) and sum(s)<=1 and sum(t)<=1
                split=[]
                if not islinear:
                    if any(local_s[i]>local_t[i] for i in range(m)):decreasing_extra+=1
                    split=[(bits,rate)]
                elif sum(local_s)==0:
                    dest=local_t.index(1);nxt=occupied|{dest};split=[(tuple(int(i in nxt) for i in range(m)),rate)]
                else:
                    origin=local_s.index(1);pr=F(k)*bits[origin]
                    if pr:
                        nxt=occupied-{origin}
                        if sum(local_t):
                            dest=local_t.index(1)
                            if dest in occupied and dest!=origin:coalescences+=1
                            nxt.add(dest)
                        split.append((tuple(int(i in nxt) for i in range(m)),pr))
                    if rate-pr:split.append((bits,rate-pr))
                assert sum(k0 for bp,k0 in split)==rate
                actual[xp]+=rate
                for bp,k0 in split:
                    assert k0>0 and all(bp[i]<=xp[S[i]] for i in range(m))
                    projected[xp]+=k0
                    if bp!=bits:binary[bp]+=k0
                    events+=1
            expected=defaultdict(F)
            for s,t,k in linear:
                nxt=occupied.copy()
                if sum(s):
                    origin=s.index(1)
                    if origin not in occupied:continue
                    nxt.remove(origin)
                if sum(t):nxt.add(t.index(1))
                bp=tuple(int(i in nxt) for i in range(m))
                if bp!=bits:expected[bp]+=k
            assert actual==projected and binary==expected
            cases+=1
    # A concretely bad occupied-destination rule violates dominance, not just a matrix identity.
    x=(1,1,0,0);b=(1,1,0,0);xp=(0,2,0,0);wrong=b;correct=(0,1,0,0)
    assert any(a>c for a,c in zip(wrong,xp)) and all(a<=c for a,c in zip(correct,xp))
    return {'joint_states':cases,'split_event_terms':events,'enabled_extra_decrease_events':decreasing_extra,
      'occupied_destination_events':coalescences,'actual_marginal_exact':True,'binary_marginal_autonomous':True,
      'coordinate_dominance_preserved':True,'occupied_destination_tamper':{'service_state':x,'tokens':b,
        'conversion':'A->E','post_state':xp,'incorrect_tokens':wrong,'correct_tokens':correct,'dominance_failure_detected':True}}

def main():
    sp,raw=p.demo_network();out=[]
    rec,cert,row=run_case('positive_count_three_cycle_with_linear_inactive_phase',sp,raw);out.append(row)
    assert len(rec['inactive'])==2 and cert['activation_clock']['clock_linear_system_dimension']==4
    assert cert['activation_clock']['uniform_activation_mean_upper']==24 and cert['max_service_jump']==3
    assert len(cert['inactive_fringe_rows'])==18
    coupling=coupling_challenge(rec,raw)
    # Affine recovery: neither inactive phase has an extra nonlinear subnetwork.
    linear=[(s,t,k) for s,t,k in raw if not (s[0]>0 and t[0]>0 and sum(s)==s[0] and sum(t)==t[0])]
    out.append(run_case('affine_recovery_without_extra_subnetworks',sp,linear)[2])
    # Empty I, but a positive-count nonlinear subnetwork in a hub.
    def u(i,a,n):return tuple(a*int(j==i) for j in range(n))
    allhub=[((0,0,0),u(0,1,3),F(1,10)),(u(0,1,3),(0,0,0),F(1)),
       ((0,0,0),u(1,1,3),F(1,5)),(u(1,1,3),(0,0,0),F(2)),
       (u(0,2,3),(1,0,1),F(1)),((1,0,1),u(0,2,3),F(1)),
       (u(1,2,3),(0,1,1),F(2)),((0,1,1),u(1,2,3),F(1)),
       (u(0,1,3),u(0,3,3),F(1,100)),(u(0,3,3),u(0,1,3),F(10))]
    hr,hc,row=run_case('empty_inactive_set_with_nonlinear_hub',['B','D','C'],allhub);out.append(row)
    assert not hr['inactive'] and hc['activation_clock']['clock_linear_system_dimension']==1
    assert hc['activation_clock']['uniform_activation_mean_upper']==F(10,3)
    # Add an independent positive-count two-cycle in an active hub to the main demo.
    hubraw=raw+[(u(2,2,5),u(2,3,5),F(1,100)),(u(2,3,5),u(2,2,5),F(10))]
    out.append(run_case('nonlinear_active_hub_and_inactive_cycle',sp,hubraw)[2])
    out.append(run_case('larger_exponential_base',sp,raw,F(3))[2])
    # Two satellites and high-degree neutral support rearrangement.
    multi=[(s+(0,),t+(0,),k) for s,t,k in raw];sp2=sp+['F']
    for h,a,b in [(2,F(3,2),F(5,4)),(3,F(1,3),F(7,6))]:
        aa=u(h,2,6);az=tuple(int(i==h)+int(i==5) for i in range(6));multi += [(aa,az,a),(az,aa,b)]
    a=(0,0,0,0,5,2);b=(0,0,0,0,4,3);multi += [(a,b,F(3,4)),(b,a,F(5,6))]
    out.append(run_case('two_satellites_high_degree_neutral_and_nonlinear_core',sp2,multi)[2])
    # Reversible support-erasing channels violate the recognized architecture.
    badraw=raw+[(u(0,4,5),(0,)*5,F(1)),((0,)*5,u(0,4,5),F(1))]
    assert wr(badraw) and not p.recognize(sp,badraw)['accepted']
    rejected=[]
    for kind in ['collar_omission','clock_coalescence','clock_mean','polynomial_bound','negative_jump_radius','head_value']:
        bad=copy.deepcopy(cert)
        if kind=='collar_omission':bad['inactive_fringe_rows']=[row for row in bad['inactive_fringe_rows'] if sum(row['service_state'])==bad['R']]
        elif kind=='clock_coalescence':
            # Remove A->E coalescence at occupied binary A+E.
            row=3;col=1;bad['activation_clock']['clock_matrix'][row][row]-=1;bad['activation_clock']['clock_matrix'][row][col]+=1
        elif kind=='clock_mean':bad['activation_clock']['uniform_activation_mean_upper']-=1
        elif kind=='polynomial_bound':bad['univariate_polynomial_bounds'][0]['global_upper_bound']=0
        elif kind=='negative_jump_radius':bad['nonlinear_tail_radius']=3
        else:bad['head_weights'][0]+=1
        try:verify(rec,bad)
        except AssertionError:rejected.append(kind)
        else:raise AssertionError('bad certificate accepted: '+kind)
    budget=[]
    for name,args in [('clock',{'max_clock_states':3}),('polynomial',{'max_polynomial_states':11}),('head',{'max_head_states':9})]:
        decline=p.construct(rec,**args);assert not decline['accepted'];budget.append({'budget':name,'receipt':decline})
    # Test receipt is independently checked as parsed JSON as well as live rationals.
    original=json.loads((HERE/'frozen_results.json').read_text());verify(original['recognition'],original['certificate'])
    print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_protected_boundary.py').read_bytes()).hexdigest(),
       'independent_exact_certificate_verifier':True,'frozen_JSON_independently_verified':True,
       'cases':out,'coupling_challenge':coupling,'tampered_fields_rejected':rejected,
       'support_erasing_WR_mutation_rejected':True,'all_three_budget_UNKNOWN_receipts':budget,
       'finite_tests_not_theorem_proof':True},default=p.encode,indent=2))

if __name__=='__main__':main()
