#!/usr/bin/env python3
"""Independent exact finite certificate audit; no simulations or float proposals."""
import importlib.util, pathlib,sys,json,hashlib,copy
from fractions import Fraction as F
from itertools import product
from math import prod,ceil
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_phase',HERE/'frozen_nonlinear_boundary.py')
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
    core=[];linear=[];restoring=[];birth2=[F(0)]*m;death3=[F(0)]*m;alpha=[[F(0)]*nz for _ in range(m)];beta=copy.deepcopy(alpha);neutral=[]
    for s,t,k in raw:
        if all(s[i]==t[i]==0 for i in Z) and sum(s)<=1 and sum(t)<=1:
            edge=(tuple(s[i] for i in S),tuple(t[i] for i in S),k)
            core.append(edge);linear.append(edge);continue
        local_s=tuple(s[i] for i in S);local_t=tuple(t[i] for i in S)
        found=False
        if all(s[i]==t[i]==0 for i in Z):
            for i in range(m):
                aa=tuple(2*int(j==i) for j in range(m));bb=tuple(3*int(j==i) for j in range(m))
                if local_s==aa and local_t==bb:birth2[i]+=k;found=True
                if local_s==bb and local_t==aa:death3[i]+=k;found=True
        if found:
            assert i not in () # loop variable is not used for classification
            edge=(local_s,local_t,k);core.append(edge);restoring.append(edge);continue
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
    assert I and all(birth2[i]>0 and death3[i]>0 for i in I)
    assert all(birth2[h]==death3[h]==0 for h in H)
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
    extra=F(0)
    boundrows={row['phase']:row for row in cert['restoring_pair_bounds']}
    assert set(boundrows)==set(I) and len(boundrows)==len(I)
    for i in I:
        row=boundrows[i];aa=birth2[i]*(q[i]-1);bb=death3[i]*(q[i]-1)/(2*q[i]);cut=row['cutoff']
        assert aa==F(row['quadratic_coefficient']) and bb==F(row['cubic_coefficient'])
        assert cut>=2+aa/bb and cut>=3
        vals=[aa*j*(j-1)-bb*j*(j-1)*(j-2) for j in range(cut)]
        assert vals==list(map(F,row['finite_values']))
        bound=F(row['global_upper_bound']);assert bound>=max([F(0)]+vals);extra+=bound
    assert extra==F(cert['extra_core_tail_constant']) and B+extra==F(cert['effective_immigration_constant'])
    Beff=B+extra;nonlin=cert['nonlinear_tail_radius']
    assert nonlin>=2 and nonlin>=1+2*c/(min(q)-1) and R>=nonlin
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
    for yi in comps(R,len(I)):
        y=[0]*m
        for i,a in zip(I,yi):y[i]=a
        expected_fringe.add(tuple(y))
    assert set(fringe)==expected_fringe and len(fringe)==len(cert['inactive_fringe_rows'])
    for y,row in fringe.items():
        actual=sum(rate*(h(yp)-base(y)) for yp,rate in cj(y))/base(y)
        assert actual==F(row['exact_core_quotient']) and row['passed'] and actual<=-teps/2
    # Reconstruct the bounded-return and exact finite activation clock.
    clock=cert['activation_clock'];ell=len(I);kc=clock['clock_radius']
    kap=max(birth2[i] for i in I);mu=min(death3[i] for i in I);total_lam=sum(lam)
    assert clock['accepted'] and clock['method']=='bounded-return-plus-finite-activation'
    assert clock['inactive_dimension']==ell and F(clock['immigration_total'])==total_lam
    assert F(clock['quadratic_birth_max'])==kap and F(clock['cubic_death_min'])==mu
    assert kc>=6*ell**2 and mu*kc>=4*ell**2*(total_lam+kap+1)
    assert F(clock['return_mean_bound'])==1
    expected_clock=set()
    for r in range(kc):
        for yi in comps(r,ell):
            y=[0]*m
            for i,a in zip(I,yi):y[i]=a
            expected_clock.add(tuple(y))
    states=list(map(tuple,clock['clock_states']));index={y:i for i,y in enumerate(states)};nc=len(states)
    assert set(states)==expected_clock and len(index)==nc and clock['clock_linear_system_dimension']==nc
    mat=[[F(0)]*nc for _ in states];success=[F(0)]*nc
    for y,row in index.items():
        for yp,rate in cj(y):
            mat[row][row]+=rate
            if yp in index:mat[row][index[yp]]-=rate
            elif any(yp[h] for h in H):success[row]+=rate
    assert mat==[list(map(F,row)) for row in clock['clock_matrix']]
    assert success==list(map(F,clock['clock_activation_rates']))
    times=list(map(F,clock['clock_exit_means']));probs=list(map(F,clock['clock_activation_probabilities']))
    assert len(times)==len(probs)==nc and min(times)>0 and 0<min(probs)<=max(probs)<=1
    assert all(sum(a*t for a,t in zip(row,times))==1 for row in mat)
    assert all(sum(a*p0 for a,p0 in zip(row,probs))==b for row,b in zip(mat,success))
    assert F(clock['clock_exit_mean_max'])==max(times) and F(clock['clock_activation_probability_min'])==min(probs)
    mean=(1+max(times))/min(probs)
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
    mu_max=max(death3[i] for i in I);leak=di+mu_max
    assert F(term['inactive_death_max'])==di and F(term['cubic_death_max'])==mu_max
    assert F(term['leakage_coefficient'])==leak and rb>=max(cert['initial_R'],K)
    lhs=T**rb*gg(rb);rhs=2*leak*rb**3*excess/teps
    assert lhs==F(term['radius_inequality_lhs']) and rhs==F(term['radius_inequality_rhs']) and lhs>=rhs
    assert T*rb**4>=(rb+c)*(rb+1)**3
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
          if all(s[i]==t[i]==0 for i in Z) ]
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
    weights=dict(zip(head,u));y=tuple(2*int(i==I[0]) for i in range(m));by=base(y)
    quotient=sum(rate*(weights.get(yp,base(yp))-by) for yp,rate in jumps(y))/by
    assert quotient==F(2775046,4141725)>0
    return {'R':R,'service_state':y,'exact_positive_generator_quotient':str(quotient),
            'all_satellite_counts_share_this_positive_quotient':True}


def one_phase_sharp_clock(rec):
    """Independent optional K=3 certificate; not a silent modification of candidate."""
    assert len(rec['inactive'])==1
    i=rec['inactive'][0];m=len(rec['service']);S=rec['service'];Z=rec['satellites'];H=rec['hubs']
    raw=[(tuple(s[j] for j in S),tuple(t[j] for j in S),F(k)) for s,t,k in rec['reactions'] if all(s[j]==t[j]==0 for j in Z)]
    lam=sum(rec['immigration']);kap=rec['birth2'][i];mu=rec['death3'][i];d=rec['death'][i]
    assert (lam,kap,mu,d)==(F(1,10),F(1,10),F(10),F(1))
    def P(r):return (-100*r**3+111*r*r+419*r-399)/F(10)
    def diff(r):return (-300*r*r-78*r+430)/F(10)
    assert P(2)>0 and P(3)<0 and diff(2)<0
    # diff(r+1)-diff(r)=(-600r-378)/10<0 for all r>=2.
    K=3;states=[tuple(r*int(j==i) for j in range(m)) for r in range(K)];idx={y:j for j,y in enumerate(states)}
    matrix=[[F(0)]*K for _ in states];success=[F(0)]*K
    for y,j in idx.items():
        for s,t,k in raw:
            rate=k*ff(y,s)
            if not rate:continue
            yp=tuple(y[z]-s[z]+t[z] for z in range(m));matrix[j][j]+=rate
            if yp in idx:matrix[j][idx[yp]]-=rate
            elif any(yp[h] for h in H):success[j]+=rate
    def independent_linear_solve(rhs):
        A=[row[:]+[b] for row,b in zip(matrix,rhs)]
        for j in range(K):
            piv=next(i for i in range(j,K) if A[i][j]);A[j],A[piv]=A[piv],A[j]
            for i in range(j+1,K):
                a=A[i][j]/A[j][j]
                A[i]=[x-a*y for x,y in zip(A[i],A[j])]
        ans=[F(0)]*K
        for j in range(K-1,-1,-1):ans[j]=(A[j][-1]-sum(A[j][l]*ans[l] for l in range(j+1,K)))/A[j][j]
        assert all(sum(a*x for a,x in zip(row,ans))==b for row,b in zip(matrix,rhs))
        return ans
    times=independent_linear_solve([F(1)]*K);probs=independent_linear_solve(success)
    return {'minimal_radius_for_exact_radial_bound':K,'clock_dimension':K,
      'P_coefficients_ascending':['-399/10','419/10','111/10','-10'],
      'P_at_two':P(2),'P_at_three':P(3),'forward_difference_at_two':diff(2),
      'forward_difference_monotone_decreasing_for_r_at_least_two':True,
      'matrix':matrix,'success_rates':success,'exit_times':times,'activation_probabilities':probs,
      'uniform_activation_mean_upper':(1+max(times))/min(probs),
      'candidate_unchanged':True}

def main():
    sp,raw=p.demo_network();out=[]
    rec,cert,r=run_case('nonlinear_inactive_phase_requires_repaired_head',sp,raw);out.append(r)
    assert cert['search_trials'][0]['passed'] is False and cert['R']==4
    assert cert['search_trials'][0]['largest_fringe_quotient']==F(2775046,4141725)>0
    failure=independent_failed_head(rec,cert)
    sharp=one_phase_sharp_clock(rec)
    out.append(run_case('larger_exponential_base',sp,raw,F(4))[2])
    out.append(run_case('smaller_exponential_base',sp,raw,F(3,2))[2])
    # Unequal hub deaths, hub return to inactive phase, and direct hub immigration.
    mod=[(s,t,F(3,2) if s==(0,1,0,0) and t==(0,0,0,0) else k) for s,t,k in raw]
    mod += [((0,0,1,0),(1,0,0,0),F(1,5)),((0,0,0,0),(0,1,0,0),F(1,7))]
    out.append(run_case('unequal_hubs_and_return_to_nonlinear_phase',sp,mod)[2])
    # Two satellites with high-degree neutral channels.
    sp2=sp+['F'];multi=[(s+(0,),t+(0,),k) for s,t,k in raw]
    def u(i,a,n=5):return tuple(a*int(j==i) for j in range(n))
    for h,a,b in [(1,F(3,2),F(5,4)),(2,F(1,3),F(7,6))]:
        aa=u(h,2);az=tuple(int(i==h)+int(i==4) for i in range(5));multi += [(aa,az,a),(az,aa,b)]
    s=(0,0,0,5,2);t=(0,0,0,4,3);multi += [(s,t,F(3,4)),(t,s,F(5,6))]
    out.append(run_case('two_satellites_and_seventh_order_neutral',sp2,multi)[2])
    perm=(3,1,0,2)
    permraw=[(tuple(s[i] for i in perm),tuple(t[i] for i in perm),k) for s,t,k in raw]
    out.append(run_case('species_permutation_acquired_partition',[sp[i] for i in perm],permraw)[2])
    # Mutations retain full graph WR where possible, so shape rejection is meaningful.
    missing_pair=[(s,t,k) for s,t,k in raw if not (s[0]>=2 and t[0]>=2)]
    assert wr(missing_pair) and not p.recognize(sp,missing_pair)['accepted']
    hub_pair=raw+[(u(1,2,4),u(1,3,4),F(1)),(u(1,3,4),u(1,2,4),F(1))]
    assert wr(hub_pair) and not p.recognize(sp,hub_pair)['accepted']
    missing_death=[(s,t,k) for s,t,k in raw if not (s==(0,1,0,0) and t==(0,0,0,0))]
    missing_death += [((0,1,0,0),(1,0,0,0),F(1))]
    assert wr(missing_death) and not p.recognize(sp,missing_death)['accepted']
    tampered=[]
    for kind in ['clock_probability','clock_time','clock_radius','restoring_bound','fringe_coverage','forcing_bound','head_value']:
        bad=copy.deepcopy(cert)
        if kind=='clock_probability':bad['activation_clock']['clock_activation_probabilities'][0]+=1
        elif kind=='clock_time':bad['activation_clock']['clock_exit_means'][0]+=1
        elif kind=='clock_radius':bad['activation_clock']['clock_radius']=1
        elif kind=='restoring_bound':bad['restoring_pair_bounds'][0]['global_upper_bound']=0
        elif kind=='fringe_coverage':bad['inactive_fringe_rows']=[]
        elif kind=='forcing_bound':bad['termination_witness']['positive_forcing_bound_M']=0
        else:bad['head_weights'][0]+=1
        try:verify(rec,bad)
        except AssertionError:tampered.append(kind)
        else:raise AssertionError('tamper accepted: '+kind)
    clock_decline=p.construct(rec,max_clock_states=5)
    assert not clock_decline['accepted'] and clock_decline['required_clock_states']==6
    head_decline=p.construct(rec,max_head_states=2)
    assert not head_decline['accepted'] and head_decline['R']==4 and len(head_decline['search_trials'])==1
    print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_nonlinear_boundary.py').read_bytes()).hexdigest(),
      'independent_exact_certificate_verifier':True,'cases':out,
      'independently_reconstructed_failed_patch':failure,'optional_sharp_one_phase_clock':sharp,
      'model_breaking_WR_mutations_rejected':['missing_inactive_restoring_pair','hub_restoring_pair','missing_direct_hub_death'],
      'tampered_fields_rejected':tampered,'clock_budget_decline':clock_decline,'head_budget_decline':head_decline,
      'finite_tests_not_theorem_proof':True},default=p.encode,indent=2))

if __name__=='__main__':main()
