#!/usr/bin/env python3
"""Independent exact finite certificate audit; no simulations or float proposals."""
import importlib.util, pathlib,sys,json,hashlib,copy
from fractions import Fraction as F
from itertools import product
from math import prod,ceil
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_phase',HERE/'frozen_phase_boundary_general.py')
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
    core=[];alpha=[[F(0)]*nz for _ in range(m)];beta=copy.deepcopy(alpha);neutral=[]
    for s,t,k in raw:
        if all(s[i]==t[i]==0 for i in Z) and sum(s)<=1 and sum(t)<=1:
            core.append((tuple(s[i] for i in S),tuple(t[i] for i in S),k));continue
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
    for s,t,k in core:adj[s].append(t)
    for source in allC:
        seen={source};stack=[source]
        while stack:
            y=stack.pop()
            for z in adj[y]:
                if z not in seen:seen.add(z);stack.append(z)
        assert seen==allC
    d=[sum(k for s,t,k in core if s==units[i] and t==zero) for i in range(m)]
    lam=[sum(k for s,t,k in core if s==zero and t==units[i]) for i in range(m)]
    k=[[sum(a for s,t,a in core if s==units[i] and t==units[j]) if i!=j else F(0) for j in range(m)] for i in range(m)]
    assert all(d[h]>0 for h in H)
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
    assert margin==delta-c*al>0 and B+2*c*D-margin*R<=-teps and 0<eps<=teps/2
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
    for yi in comps(R,len(I)):
        y=[0]*m
        for i,a in zip(I,yi):y[i]=a
        expected_fringe.add(tuple(y))
    assert set(fringe)==expected_fringe and len(fringe)==len(cert['inactive_fringe_rows'])
    for y,row in fringe.items():
        actual=sum(rate*(h(yp)-base(y)) for yp,rate in cj(y))/base(y)
        assert actual==F(row['exact_core_quotient']) and row['passed'] and actual<=-teps/2
    # Reconstruct the paid successful-immigrant clock directly from the raw core.
    clock=cert['activation_clock'];path=clock['phase_path']
    assert path and path[-1] in H and all(i in I for i in path[:-1]) and lam[path[0]]>0
    prob=F(1);delay=F(0)
    for i,j in zip(path,path[1:]):
        exit_rate=sum(k[i])+d[i];assert k[i][j]>0 and exit_rate>0
        prob*=k[i][j]/(2*exit_rate);delay+=1/exit_rate
    mean=delay+1/(lam[path[0]]*prob)
    assert F(clock['immigration_rate'])==lam[path[0]]
    assert F(clock['success_probability_lower'])==prob and F(clock['success_delay_upper'])==delay
    assert F(clock['uniform_activation_mean_upper'])==mean
    # Finite positive-forcing support and a sufficient scalar-radius witness.
    term=cert['termination_witness'];K=term['forcing_radius_K']
    assert K>=2 and delta*K>=B+2*c*D+1 and K>=c/(T-1) and T**K*gg(K)>=1
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
    assert F(term['inactive_death_max'])==di and rb>=cert['initial_R']
    lhs=T**rb*gg(rb);rhs=2*di*rb*excess/teps
    assert lhs==F(term['radius_inequality_lhs']) and rhs==F(term['radius_inequality_rhs']) and lhs>=rhs
    assert T*rb**2>=(rb+c)*(rb+1)
    # Finite active layer coverage is independently enumerated.
    rows={tuple(row['service_state']):row for row in cert['active_layer_rows']}
    expect_active={y for r in range(1,R+1) for y in comps(r,m) if any(y[j] for j in H)}
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
    for r in range(cert['R']+3):
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

def independent_failed_head(rec,cert):
    """Reconstruct the invalid R=2 patch and its positive all-satellite ray."""
    S=rec['service'];Z=rec['satellites'];I=rec['inactive'];m=len(S);R=2
    core=[(tuple(s[i] for i in S),tuple(t[i] for i in S),F(k)) for s,t,k in rec['reactions']
          if all(s[i]==t[i]==0 for i in Z) and sum(s)<=1 and sum(t)<=1]
    q=cert['q'];c=cert['c']
    def base(y):
        r=sum(y)
        return prod((q[i]**y[i] for i in range(m)),start=F(1))*prod((F(i)/(i+c) for i in range(1,r)),start=F(1)) if r else F(1)
    head=[]
    for r in range(R):
        for yi in comps(r,len(I)):
            y=[0]*m
            for i,a in zip(I,yi):y[i]=a
            head.append(tuple(y))
    idx={y:i for i,y in enumerate(head)};n=len(head)
    A=[[F(0)]*(n+1) for _ in range(n)]
    def jumps(y):
        for s,t,k in core:
            rate=k*ff(y,s)
            if rate:yield tuple(y[i]-s[i]+t[i] for i in range(m)),rate
    for y,i in idx.items():
        A[i][-1]=1
        for yp,rate in jumps(y):
            A[i][i]+=rate
            if yp in idx:A[i][idx[yp]]-=rate
            else:A[i][-1]+=rate*base(yp)
    # Independent exact Gaussian elimination with forward and back substitution.
    for j in range(n):
        pivot=next(i for i in range(j,n) if A[i][j]);A[j],A[pivot]=A[pivot],A[j]
        for i in range(j+1,n):
            mult=A[i][j]/A[j][j]
            A[i]=[u-mult*v for u,v in zip(A[i],A[j])]
    u=[F(0)]*n
    for j in range(n-1,-1,-1):u[j]=(A[j][-1]-sum(A[j][k]*u[k] for k in range(j+1,n)))/A[j][j]
    weights=dict(zip(head,u));y=(2,0,0,0);by=base(y)
    quotient=sum(rate*(weights.get(yp,base(yp))-by) for yp,rate in jumps(y))/by
    assert quotient==F(2159109577,927605760)>0
    return {'R':R,'service_state':y,'exact_positive_generator_quotient':str(quotient),
            'all_satellite_counts_share_this_positive_quotient':True}

def main():
    sp,base_raw=p.demo_network()
    raw=base_raw+[((1,0,0,0,0),(0,0,0,0,0),1)]
    out=[]
    rec,cert,r=run_case('inactive_death_requires_repaired_head',sp,raw);out.append(r)
    assert cert['search_trials'][0]['passed'] is False and cert['R']==4
    assert cert['search_trials'][0]['largest_fringe_quotient']==F(2159109577,927605760)>0
    failed_head=independent_failed_head(rec,cert)
    # The former guarded subclass is retained without unnecessary radius growth.
    oldrec,oldcert,r=run_case('no_inactive_death_recovery',sp,base_raw);out.append(r)
    assert oldcert['R']==oldcert['initial_R'] and oldcert['termination_witness']['inactive_death_max']==0
    out.append(run_case('larger_exponential_base',sp,raw,F(4))[2])
    # Both inactive phases now have death and the clock must charge them.
    two_deaths=raw+[((0,1,0,0,0),(0,0,0,0,0),F(2,3))]
    out.append(run_case('death_at_both_inactive_phases',sp,two_deaths)[2])
    # Two satellite coordinates and nonlinear neutral mixing, with inactive death.
    sp2=sp+['F'];multi=[(s+(0,),t+(0,),k) for s,t,k in raw]
    for h,a,b in [(2,F(3,2),F(5,4)),(3,F(1,3),F(7,6))]:
        aa=tuple(2*int(i==h) for i in range(6));az=tuple(int(i==h)+int(i==5) for i in range(6))
        multi += [(aa,az,a),(az,aa,b)]
    s=(0,0,0,0,5,2);t=(0,0,0,0,4,3)
    multi += [(s,t,F(3,4)),(t,s,F(5,6))]
    out.append(run_case('two_satellites_neutral_and_inactive_death',sp2,multi)[2])
    # Empty inactive set gives a direct-hub immigration path with p=1,D=0.
    allhub=[((0,0,0),(1,0,0),F(1,10)),((1,0,0),(0,0,0),1),
      ((0,0,0),(0,1,0),F(1,5)),((0,1,0),(0,0,0),F(2)),
      ((2,0,0),(1,0,1),F(1)),((1,0,1),(2,0,0),F(2)),
      ((0,2,0),(0,1,1),F(3)),((0,1,1),(0,2,0),F(4))]
    hr,hc,r=run_case('all_hubs_direct_immigration_clock',['B','D','C'],allhub);out.append(r)
    assert hc['activation_clock']['success_probability_lower']==1 and hc['activation_clock']['success_delay_upper']==0
    # Pointwise drift acceptance must not ignore the fringe or head data.
    for kind in ['fringe_coverage','clock_probability','forcing_bound','head_value']:
        bad=copy.deepcopy(cert)
        if kind=='fringe_coverage':bad['inactive_fringe_rows']=bad['inactive_fringe_rows'][1:]
        elif kind=='clock_probability':bad['activation_clock']['success_probability_lower']=1
        elif kind=='forcing_bound':bad['termination_witness']['positive_forcing_bound_M']=0
        else:bad['head_weights'][0]+=1
        try:verify(rec,bad)
        except AssertionError:pass
        else:raise AssertionError('tamper accepted: '+kind)
    decline=p.construct(rec,F(2),max_head_states=3)
    assert not decline['accepted'] and decline['R']==4 and len(decline['search_trials'])==1
    print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_phase_boundary_general.py').read_bytes()).hexdigest(),
      'independent_exact_certificate_verifier':True,'cases':out,'budget_after_failed_patch':decline,
      'fringe_clock_forcing_head_tampering_rejected':True,
      'old_unrepaired_patch_has_positive_inactive_fringe':failed_head,'finite_tests_not_theorem_proof':True},default=p.encode,indent=2))
if __name__=='__main__':main()
