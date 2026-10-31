#!/usr/bin/env python3
"""Independent exact finite certificate audit; no simulations or float proposals."""
import importlib.util, pathlib,sys,json,hashlib,copy
from fractions import Fraction as F
from itertools import product
from math import prod,ceil
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_phase',HERE/'frozen_phase_boundary.py')
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
    assert all(d[h]>0 for h in H) and all(d[i]==0 for i in I)
    T=F(cert['T']);eta=F(cert['eta']);c=F(cert['c']);R=cert['R'];eps=F(cert['epsilon']);C=F(cert['foster_C'])
    q=list(map(F,cert['q']));v=list(map(F,cert['v']));thit=list(map(F,cert['hitting_times']));L=F(cert['common_level_L'])
    assert T>1 and eta>0 and c>0 and R>=2 and eps>0 and C>=0
    assert all(thit[h]==0 for h in H) and all(thit[i]>0 for i in I)
    for i in I:assert sum(k[i][j]*(thit[j]-thit[i]) for j in range(m))==-1
    assert all(v[i]==L+thit[i] and q[i]==1+eta*v[i] for i in range(m))
    assert all(q[h]==T for h in H) and all(qi>=T for qi in q)
    Qv=[sum(k[i][j]*(v[j]-v[i]) for j in range(m))-d[i]*v[i] for i in range(m)]
    assert all(z<=-1 for z in Qv)
    delta=F(cert['delta']);al=F(cert['alpha_max']);D=F(cert['death_weight_max']);B=F(cert['immigration_bound'])
    teps=F(cert['tail_epsilon']);margin=F(cert['tail_margin'])
    assert 0<delta<=min(eta/qi for qi in q)
    assert al>=max(sum(alpha[h]) for h in H) and D>=max(d[i]/q[i] for i in range(m))
    assert B>=sum(lam[i]*(q[i]-1) for i in range(m))
    assert margin==delta-c*al>0 and B+2*c*D-margin*R<=-teps and 0<eps<=teps
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
    def h(y):
        return head[y] if y in head else prod((q[i]**y[i] for i in range(m)),start=F(1))*gg(sum(y))
    def cj(y):
        for s,t,a in core:
            rate=a*ff(y,s)
            if rate:yield tuple(y[i]-s[i]+t[i] for i in range(m)),rate
    for y,u in head.items():assert sum(rate*(h(yp)-u) for yp,rate in cj(y))==-1
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

def main():
    sp,raw=p.demo_network();out=[]
    rec,cert,r=run_case('five_species_frozen_demo',sp,raw);out.append(r)
    for T in [F(3,2),F(4)]:out.append(run_case('same_network_different_requested_exponent',sp,raw,T)[2])
    # Hub return conversions and unequal death rates challenge common plateau L.
    alt=[]
    for s,t,k in raw:
        if s==(0,0,1,0,0) and t==(0,0,0,0,0):k=F(1,2)
        if s==(0,0,0,0,0):k=F(1,100)
        alt.append((s,t,k))
    alt += [((0,0,1,0,0),(1,0,0,0,0),F(1,3)),((0,0,0,1,0),(0,1,0,0,0),F(2,5))]
    out.append(run_case('hub_returns_and_unequal_deaths',sp,alt)[2])
    # Multiple satellites and seventh-order neutral mixing.
    sp2=sp+['F'];multi=[(s+(0,),t+(0,),k) for s,t,k in raw]
    for h,a,b in [(2,F(3,2),F(5,4)),(3,F(1,3),F(7,6))]:
        aa=tuple(2*int(i==h) for i in range(6));az=tuple(int(i==h)+int(i==5) for i in range(6))
        multi += [(aa,az,a),(az,aa,b)]
    s=(0,0,0,0,5,2);t=(0,0,0,0,4,3)
    multi += [(s,t,F(3,4)),(t,s,F(5,6))]
    mr,mc,r=run_case('two_satellites_high_order_neutral',sp2,multi);out.append(r)
    # Empty inactive set: finite head consists only of zero.
    allhub=[((0,0,0),(1,0,0),F(1,10)),((1,0,0),(0,0,0),1),
      ((0,0,0),(0,1,0),F(1,5)),((0,1,0),(0,0,0),F(2)),
      ((2,0,0),(1,0,1),F(1)),((1,0,1),(2,0,0),F(2)),
      ((0,2,0),(0,1,1),F(3)),((0,1,1),(0,2,0),F(4))]
    out.append(run_case('no_inactive_service_species',['B','D','C'],allhub)[2])
    # Default implementation budget is explicit; no expensive solve is attempted.
    declined=p.construct(rec,F(100));assert not declined['accepted'] and 'budget' in declined['reason']
    # Corrupt the exact Dirichlet function, then coverage: verifier must fail.
    for kind in ['weight','coverage']:
        bad=copy.deepcopy(cert)
        if kind=='weight':bad['head_weights'][0]+=1
        else:bad['active_layer_rows']=bad['active_layer_rows'][1:]
        try:verify(rec,bad)
        except AssertionError:pass
        else:raise AssertionError('tamper accepted: '+kind)
    # Full WR can hold while a required direct reverse row is incomplete.
    missing=[r for r in multi if not(r[0]==(0,0,1,0,0,1) and r[1]==(0,0,2,0,0,0))]
    missing += [((0,0,1,0,0,1),(0,0,1,0,1,0),F(1))]
    assert wr(missing) and not p.recognize(sp2,missing)['accepted']
    print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_phase_boundary.py').read_bytes()).hexdigest(),
      'independent_exact_certificate_verifier':True,'cases':out,'budget_decline':declined,
      'head_weight_and_layer_coverage_tampering_rejected':True,
      'incomplete_reverse_row_despite_full_WR_rejected':True,'finite_tests_not_theorem_proof':True},default=p.encode,indent=2))
if __name__=='__main__':main()
