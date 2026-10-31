#!/usr/bin/env python3
"""Independent exact coefficient-cone acquisition and Foster audit; no float LP."""
from fractions import Fraction as F
from itertools import combinations
from math import prod,comb
from pathlib import Path
import importlib.util,json,hashlib,copy
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_adaptive',HERE/'frozen_adaptive_mass.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def comps(N,n):
    if n==1:yield (N,)
    else:
        for a in range(N+1):
            for z in comps(N-a,n-1):yield (a,)+z

def ff(x,u):
    if any(a<b for a,b in zip(x,u)):return 0
    return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))

def weak_reversible(raw):
    vertices={u for u,v,k in raw}|{v for u,v,k in raw};adj={u:[] for u in vertices}
    for u,v,k in raw:adj[u].append(v)
    for u,v,k in raw:
        seen={v};stack=[v]
        while stack:
            z=stack.pop()
            for w in adj[z]:
                if w not in seen:seen.add(w);stack.append(w)
        if u not in seen:return False
    return True

def unpack(rec):
    assert rec['accepted'];n=len(rec['species']);a=rec['pivot'];J=list(rec['satellites'])
    assert n>=2 and 0<=a<n and J==[j for j in range(n) if j!=a]
    raw=[(tuple(u),tuple(v),F(k)) for u,v,k in rec['reactions']]
    assert all(len(u)==len(v)==n and k>0 and all(type(x)==int and x>=0 for x in u+v) for u,v,k in raw)
    assert weak_reversible(raw);zero=(0,)*n;unit=tuple(int(j==a) for j in range(n));internal=[];lam=death=F(0)
    for u,v,k in raw:
        if u==zero and v==unit:lam+=k
        elif u==unit and v==zero:death+=k
        else:assert sum(u)==sum(v);internal.append((u,v,k))
    assert lam==F(rec['immigration'])>0 and death==F(rec['death'])>0
    assert internal==[(tuple(u),tuple(v),F(k)) for u,v,k in rec['internal']]
    return n,a,J,raw,internal,lam,death

def constraints_from_raw(rec):
    n,a,J,raw,internal,lam,death=unpack(rec);d=len(J)+1;source={}
    for u,v,k in internal:
        row=source.setdefault(u,[F(0)]*(d+1))
        for z,j in enumerate(J):row[z]+=k*(v[j]-u[j])
        row[-1]+=k*(v[a]-u[a])
    out=[]
    def add(label,row):
        row=list(map(F,row))
        if any(row):out.append((label,row))
    for z,j in enumerate(J):
        low=[F(0)]*(d+1);low[z]=-1;add(['weight_lower',j],low)
        high=[F(0)]*(d+1);high[z]=1;high[-1]=-1;add(['weight_upper',j],high)
    upper=max(F(1),2*sum(k for u,v,k in internal if sum(u)==2))
    low=[F(0)]*(d+1);low[-2]=-1;add(['beta_lower'],low)
    high=[F(0)]*(d+1);high[-2]=1;high[-1]=-upper;add(['beta_upper'],high)
    for j in J:
        u=tuple(2*int(i==j) for i in range(n));row=[-z for z in source.get(u,[F(0)]*(d+1))];row[-2]+=1
        add(['pure_satellite_production',j],row)
    for j,l in combinations(J,2):
        u=tuple(int(i==j)+int(i==l) for i in range(n));add(['mixed_satellite_production',j,l],[-z for z in source.get(u,[F(0)]*(d+1))])
    for idx,(u,v,k) in enumerate(internal):
        if sum(u)>2:
            row=[F(v[j]-u[j]) for j in J]+[F(0),F(v[a]-u[a])]
            add(['higher_order_neutral_plus',idx],row);add(['higher_order_neutral_minus',idx],[-z for z in row])
    allones=[F(1)]*len(J)+[F(0)]
    assert all(sum(x*y for x,y in zip(row[:-1],allones))+row[-1]<=0 for label,row in out)
    return out

def independent_solve(A,rhs):
    n=len(A);M=[list(map(F,row))+[F(b)] for row,b in zip(A,rhs)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if M[i][j]),None)
        if pivot is None:return None
        M[j],M[pivot]=M[pivot],M[j]
        for i in range(j+1,n):
            z=M[i][j]/M[j][j]
            if z:M[i]=[a-z*b for a,b in zip(M[i],M[j])]
    x=[F(0)]*n
    for i in range(n-1,-1,-1):x[i]=(M[i][-1]-sum(M[i][j]*x[j] for j in range(i+1,n)))/M[i][i]
    assert all(sum(a*b for a,b in zip(row,x))==b for row,b in zip(A,rhs))
    return x

def independent_acquire(rec):
    rows=constraints_from_raw(rec);d=len(rec['satellites'])+1;attempts=nonsing=maxbits=0
    for basis in combinations(range(len(rows)),d):
        attempts+=1;forms=[rows[i][1] for i in basis]
        x=independent_solve([f[:-1] for f in forms],[-f[-1] for f in forms])
        if x is None:continue
        nonsing+=1;maxbits=max(maxbits,max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in x))
        if x[-1]<=0:continue
        residuals=[sum(a*b for a,b in zip(row[:-1],x))+row[-1] for label,row in rows]
        if max(residuals)<=0:return rows,{'basis':basis,'x':x,'residuals':residuals,'attempts':attempts,'nonsingular':nonsing,'bits':maxbits,'total':comb(len(rows),d)}
    return rows,{'basis':None,'attempts':attempts,'nonsingular':nonsing,'bits':maxbits,'total':comb(len(rows),d)}

def verify(rec,cert):
    assert cert['accepted'];n,a,J,raw,internal,lam,death=unpack(rec);rows,found=independent_acquire(rec)
    assert found['basis'] is not None;ac=cert['weight_acquisition'];assert ac['accepted']
    assert [(row['label'],list(map(F,row['form']))) for row in ac['constraints']]==rows
    assert tuple(ac['active_basis'])==found['basis'] and list(map(F,ac['basis_solution']))==found['x']
    assert list(map(F,ac['exact_residuals']))==found['residuals'] and max(found['residuals'])<=0
    assert ac['basis_attempts']==found['attempts'] and ac['nonsingular_bases']==found['nonsingular']
    assert ac['largest_basis_fraction_bits']==found['bits'] and ac['total_candidate_bases']==found['total']
    v=list(map(F,cert['weights']));beta=F(cert['beta']);assert v==list(map(F,ac['weights'])) and beta==F(ac['beta'])==found['x'][-1]>0
    assert v[a]==1 and all(0<=v[j]<=1 for j in J) and [v[j] for j in J]==found['x'][:-1]
    coeff={}
    for u,w,k in internal:
        dot=sum(v[i]*(w[i]-u[i]) for i in range(n));coeff[u]=coeff.get(u,F(0))+k*dot
        if sum(u)>2:assert dot==0
    assert [(tuple(row['source']),F(row['coefficient'])) for row in cert['source_drift_coefficients']]==sorted(coeff.items())
    for j in J:assert coeff.get(tuple(2*int(i==j) for i in range(n)),F(0))>=beta
    for j,l in combinations(J,2):assert coeff.get(tuple(int(i==j)+int(i==l) for i in range(n)),F(0))>=0
    K1=max([F(0)]+[-c for u,c in coeff.items() if sum(u)==1]);K2=max([F(0)]+[-c for u,c in coeff.items() if sum(u)==2 and u[a]>0])
    assert K1==F(cert['K1']) and K2==F(cert['K2'])
    t=F(cert['t']);e=F(cert['epsilon_composition']);D=death*(1-1/t);C=F(cert['constant_quotient_bound']);kap=F(cert['radial_dissipation']);zeta=F(cert['foster_epsilon']);R=cert['exception_radius'];m=len(J)
    assert t>1 and 0<e<=F(1,2) and e*K2/(1-e)<=D/2 and D==F(cert['death_exponential_coefficient'])
    assert C==lam*(t-1)+death*e/(t*(1-e))+e*(K1+beta)/(1-e)
    assert kap==min(D/4,e*beta/(8*m))>0 and zeta>0 and R>=1 and C-kap*R<=-zeta
    fc=cert['foster_constant'];co=C+zeta
    assert F(fc['coefficient'])==co and F(fc['base'])==t and fc['exponent']==R
    assert fc['unreduced_numerator_bits_upper']==co.numerator.bit_length()+R*t.numerator.bit_length()
    assert fc['unreduced_denominator_bits_upper']==co.denominator.bit_length()+R*t.denominator.bit_length()
    if fc['expanded']:assert F(fc['value'])==co*t**R
    else:assert 'value' not in fc
    assert cert['work']['total_count_exception_states_upper']==comb(R+n-1,n)
    def hh(x):return 1-e*sum(v0*x0 for v0,x0 in zip(v,x))/(sum(x)+1)
    def quotient(x):
        h=hh(x);N=sum(x);assert 1-e<=h<=1;out=F(0);lint=F(0);internal_q=F(0)
        for u,w,k in raw:
            rate=k*ff(x,u)
            if not rate:continue
            xp=tuple(xx-s+tar for xx,s,tar in zip(x,u,w));change=rate*(t**(sum(w)-sum(u))*hh(xp)/h-1);out+=change
            if sum(u)==sum(w):
                lint+=rate*sum(v0*(tar-s) for v0,tar,s in zip(v,w,u));internal_q+=change
        lower=beta*sum(x[j]*(x[j]-1) for j in J)-K2*x[a]*N-K1*N
        assert lint>=lower and internal_q==-e*lint/((N+1)*h)
        b=sum(x[j] for j in J);intermediate=C-D*x[a]/2-e*beta*b*b/(m*(N+1))
        assert out<=intermediate<=C-kap*N
        return out
    def val(x):return t**sum(x)*hh(x)
    return quotient,val

def run_case(name,sp,raw,t=F(2),**kwargs):
    rec=p.recognize(sp,raw);assert rec['accepted'];cert=p.construct(rec,t,**kwargs);assert cert['accepted'],(name,cert)
    quotient,val=verify(rec,cert);count=0;expanded=0;n=len(sp);a=rec['pivot'];J=rec['satellites']
    for N in range(17):
      for x in comps(N,n):
        q=quotient(x);count+=1
        if N<=5:
            actual=sum(k*ff(x,u)*(val(tuple(xx-s+w for xx,s,w in zip(x,u,v)))-val(x)) for u,v,k in rec['reactions'] if ff(x,u))
            assert actual/val(x)==q;expanded+=1
    huge=0
    for N in [cert['exception_radius']-1,cert['exception_radius'],cert['exception_radius']+1,10**6,10**50]:
        points=[tuple(N*int(i==j) for i in range(n)) for j in range(n)]
        x=[0]*n;x[a]=1;x[J[-1]]=N-1;points.append(tuple(x))
        points.append(tuple(N//n+int(i<N%n) for i in range(n)))
        for x in points:quotient(x);huge+=1
    return rec,cert,{'case':name,'t':str(t),'weights':list(map(str,cert['weights'])),'beta':str(cert['beta']),
      'basis_attempts':cert['weight_acquisition']['basis_attempts'],'total_candidate_bases':cert['weight_acquisition']['total_candidate_bases'],
      'K1':str(cert['K1']),'K2':str(cert['K2']),'R':cert['exception_radius'],'ordinary_exact_checks':count,
      'huge_exact_checks':huge,'expanded_small_state_checks':expanded,'expanded_Foster_constant':cert['foster_constant']['expanded']}

def main():
    sp,raw=p.demo_network();cases=[]
    rec,cert,row=run_case('mediated_triangle',sp,raw);cases.append(row)
    assert cert['weights']==[F(1),F(1,3),F(0)] and cert['beta']==F(1,3)
    assert cert['weight_acquisition']['basis_attempts']==62 and cert['exception_radius']==431
    cases.append(run_case('small_requested_exponential_base',sp,raw,F(65,64))[2])
    cases.append(run_case('large_requested_base_compact_constant',sp,raw,F(100))[2])
    unary=raw+[((0,1,0),(0,0,1),F(5)),((0,0,1),(0,1,0),F(1))]
    ru,cu,row=run_case('negative_unary_weighted_drift_paid_by_K1',sp,unary);cases.append(row);assert cu['K1']>0
    high=raw+[((1,0,2),(0,3,0),F(3,7)),((0,3,0),(1,0,2),F(11,5))]
    rh,ch,row=run_case('third_order_individually_weight_neutral_pair',sp,high);cases.append(row)
    assert any(sum(u)>2 for u,v,k in rh['internal']) and ch['weights']==[F(1),F(1,3),F(0)]
    perm=(2,0,1);permuted=[(tuple(u[i] for i in perm),tuple(v[i] for i in perm),k) for u,v,k in raw]
    cases.append(run_case('permuted_open_coordinate_reacquired',[sp[i] for i in perm],permuted)[2])
    rates=[F(2,9),F(7,4),F(1,7),F(3,5),F(2),F(1,11),F(100),F(5,3)]
    ratefamily=[(u,v,k) for (u,v,old),k in zip(raw,rates)]
    rr,cr,row=run_case('strongly_unequal_rate_family',sp,ratefamily);cases.append(row)
    assert any(r['coefficient']==0 and sum(r['source'])==2 for r in cr['source_drift_coefficients'])
    direct=[((0,0,0),(1,0,0),F(1)),((1,0,0),(0,0,0),F(1)),
      ((1,1,0),(0,2,0),F(1)),((0,2,0),(1,1,0),F(1)),
      ((1,0,1),(0,0,2),F(2)),((0,0,2),(1,0,1),F(1)),
      ((0,1,0),(0,0,1),F(1)),((0,0,1),(0,1,0),F(1))]
    cases.append(run_case('direct_return_star_family_recovered',sp,direct)[2])
    four=[(u+(0,),v+(0,),k) for u,v,k in raw]+[((1,0,0,1),(0,0,0,2),F(1,2)),((0,0,0,2),(1,0,0,1),F(3))]
    cases.append(run_case('four_species_mediated_plus_direct_return',sp+['D'],four)[2])
    # A simple stable monomolecular chain lies outside this quadratic-production cone.
    mono=[((0,0),(1,0),F(1)),((1,0),(0,0),F(1)),((1,0),(0,1),F(1)),((0,1),(1,0),F(1))]
    rm=p.recognize(['A','B'],mono);assert rm['accepted'];decline=p.construct(rm)
    rows,exhaust=independent_acquire(rm);assert exhaust['basis'] is None and exhaust['attempts']==exhaust['total']==10
    assert decline['algebraic_cone_exhausted'] and decline['network_stability']=='UNKNOWN' and not decline['accepted']
    # Direct conventional Foster comparator V=3^A 4^B has exact quotient2−A/3−B/4.
    mono_checks=0
    for a in range(8):
      for b in range(8):
        x=(a,b);q=F(0)
        for u,v,k in mono:
            rate=k*ff(x,u)
            if rate:q+=rate*(F(3)**(v[0]-u[0])*F(4)**(v[1]-u[1])-1)
        assert q==2-F(a,3)-F(b,4);mono_checks+=1
    budget=p.construct(rec,max_bases=61);assert not budget['accepted'] and budget['basis_attempts']==61 and 'budget' in budget['reason']
    compact=p.construct(rec,max_expanded_constant_bits=0);assert compact['accepted'] and not compact['foster_constant']['expanded'];verify(rec,compact)
    bad=[]
    for kind in ['weight','beta','basis','constraint','residual','K2','higher_order_equality','Foster_coefficient','bit_bound']:
        cc=copy.deepcopy(ch if kind=='higher_order_equality' else cert);rr=rh if kind=='higher_order_equality' else rec
        if kind=='weight':cc['weights'][1]=F(1,2)
        elif kind=='beta':cc['beta']+=1
        elif kind=='basis':cc['weight_acquisition']['active_basis']=[0,1,2]
        elif kind=='constraint':cc['weight_acquisition']['constraints'][0]['form'][0]+=1
        elif kind=='residual':cc['weight_acquisition']['exact_residuals'][0]-=1
        elif kind=='K2':cc['K2']=0
        elif kind=='higher_order_equality':cc['weight_acquisition']['constraints']=cc['weight_acquisition']['constraints'][:-2]
        elif kind=='Foster_coefficient':cc['foster_constant']['coefficient']=0
        else:cc['foster_constant']['unreduced_numerator_bits_upper']=1
        try:verify(rr,cc)
        except AssertionError:bad.append(kind)
        else:raise AssertionError('tamper accepted '+kind)
    # Full WR does not allow an extra nonconservative channel in this raw architecture.
    unsupported=raw+[((0,2,0),(0,3,0),F(1)),((0,3,0),(0,2,0),F(1))]
    assert weak_reversible(unsupported) and not p.recognize(sp,unsupported)['accepted']
    # Check every claimed class-connecting edge and its enabled reverse.
    paths=[[(0,0,1),(1,0,1),(0,2,0),(1,2,0),(0,2,1),(0,1,2),(0,0,3)],
           [(0,0,2),(1,0,2),(1,1,1),(0,1,2),(0,0,3)]]
    for N in [2,3,10,10**6]:paths.append([(0,0,N),(1,0,N),(1,1,N-1),(0,1,N),(0,0,N+1)])
    edgechecks=0
    for path in paths:
      for x,y in zip(path,path[1:]):
        assert any(ff(x,u)>0 and tuple(a-b+c for a,b,c in zip(x,u,v))==y for u,v,k in raw)
        assert any(ff(y,u)>0 and tuple(a-b+c for a,b,c in zip(y,u,v))==x for u,v,k in raw);edgechecks+=1
    plain=[];onecoord=[]
    for N in [10,10**6,10**50]:
        q=F(2)*(1-F(1,8)/F(N+2))-1;assert q>0;plain.append({'pure_C_count':N,'plain_A_normalized_quotient':q})
        # H0=4,H1=1,H2=100/101 is the ordinary g(A) comparator from the easier family.
        q=3*N+(2*F(100,101)-1)+(F(4,2)-1);assert q>0
        onecoord.append({'state':(1,0,N),'ordinary_service_radial_quotient':q})
    original=json.loads((HERE/'frozen_results.json').read_text());verify(original['recognition'],original['certificate'])
    print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_adaptive_mass.py').read_bytes()).hexdigest(),
      'independent_exact_basis_acquisition_and_coefficient_verifier':True,'frozen_JSON_independently_verified':True,
      'cases':cases,'stable_monomolecular_cone_exhaustion':{'receipt':decline,'independently_exhausted_bases':exhaust['total'],
        'conventional_comparator':'V=3^A4^B, LV/V=2−A/3−B/4','exact_comparator_checks':mono_checks},
      'basis_budget_UNKNOWN':budget,'compact_constant_mode_verified':True,'tampered_fields_rejected':bad,
      'full_WR_unsupported_nonconservative_mutation_rejected':True,'closed_class_connecting_edges_and_reverses_checked':edgechecks,
      'plain_normalized_A_failure':plain,'unbounded_A_only_radial_failure':onecoord,
      'finite_tests_supplement_proofs':True},default=p.encode,indent=2))

if __name__=='__main__':main()
