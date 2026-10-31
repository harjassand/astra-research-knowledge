"""Exact acquisition hierarchy for normalized polynomial composition corrections.
Trusted integer/Fraction mathematical research API, not an adversarial parser.
"""
from fractions import Fraction as F
from itertools import combinations,count
from math import comb,factorial,ceil,prod
import json

def comps(N,n):
    if n==1:yield (N,)
    else:
        for a in range(N+1):
            for z in comps(N-a,n-1):yield (a,)+z

def add(p,q):
    out=dict(p)
    for a,b in q.items():
        out[a]=out.get(a,F(0))+b
        if not out[a]:del out[a]
    return out

def scale(p,c):return {a:b*c for a,b in p.items() if b*c}
def mul(p,q,work):
    work['formal_multiplication_term_pairs']+=len(p)*len(q);out={}
    for a,b in p.items():
      for c,d in q.items():
        ac=tuple(x+y for x,y in zip(a,c));out[ac]=out.get(ac,F(0))+b*d
    return {a:b for a,b in out.items() if b}
def mono(a,c=F(1)):return {tuple(a):F(c)} if c else {}
def shift(a,nu,work):
    n=len(a);zero=(0,)*n;p={zero:F(1)}
    for j,r in enumerate(a):
        q={tuple(k if i==j else 0 for i in range(n)):F(comb(r,k)*nu[j]**(r-k)) for k in range(r+1)}
        p=mul(p,{a:b for a,b in q.items() if b},work)
    return p

def falling(u,work):
    n=len(u);zero=(0,)*n;p={zero:F(1)}
    for j,r in enumerate(u):
      for k in range(r):
        q={tuple(int(i==j) for i in range(n)):F(1)}
        if k:q[zero]=F(-k)
        p=mul(p,q,work)
    return p

def weak_reversible(raw):
    vs={u for u,v,k in raw}|{v for u,v,k in raw};adj={u:[] for u in vs}
    for u,v,k in raw:adj[u].append(v)
    for u,v,k in raw:
        seen={v};todo=[v]
        while todo:
            for w in adj[todo.pop()]:
                if w not in seen:seen.add(w);todo.append(w)
        if u not in seen:return False
    return True

def recognize(species,reactions):
    n=len(species);assert n>=2;raw=[]
    for u,v,k in reactions:
        assert len(u)==len(v)==n and all(type(z)==int and z>=0 for z in (*u,*v))
        assert isinstance(k,(int,F)) and k>0
        if tuple(u)!=tuple(v):raw.append((tuple(u),tuple(v),F(k)))
    if not weak_reversible(raw):return {'accepted':False,'reason':'not weakly reversible'}
    zero=(0,)*n;trials=[]
    for A in range(n):
        unit=tuple(int(j==A) for j in range(n));lam=death=F(0);internal=[];bad=[]
        for u,v,k in raw:
            if u==zero and v==unit:lam+=k
            elif u==unit and v==zero:death+=k
            elif sum(u)==sum(v):internal.append((u,v,k))
            else:bad.append((u,v))
        if bad or not lam or not death:
            trials.append(A);continue
        return {'accepted':True,'species':list(species),'pivot':A,'satellites':[j for j in range(n) if j!=A],
          'immigration':lam,'death':death,'internal':internal,'reactions':raw,'recognition_trials':len(trials)+1,
          'leading_order':max([2]+[sum(u) for u,v,k in internal])}
    return {'accepted':False,'reason':'not one open coordinate with conservative internals','trials':trials}

def support_certificate(rec,include_formal_bounds=True):
    """Finite leading-support test; its failure rules out every strict cone degree."""
    assert rec['accepted'];n=len(rec['species']);A=rec['pivot'];p=rec['leading_order']
    leading=[(i,u,v,k) for i,(u,v,k) in enumerate(rec['internal']) if sum(u)==p]
    trials=[];checks=0
    for seed in range(n):
        support={seed};steps=[]
        while A not in support:
            found=False
            for i,u,v,k in leading:
                checks+=1
                if all(not u[j] or j in support for j in range(n)):
                    new={j for j in range(n) if v[j] and j not in support}
                    if new:
                        steps.append({'internal_row':i,'before':sorted(support),'added':sorted(new)})
                        support.update(new);found=True;break
            if not found:break
        trials.append({'seed':seed,'support':sorted(support),'steps':steps,'reaches_open_species':A in support})
        if A not in support:
            assert all(not all(not u[j] or j in support for j in range(n)) or all(not v[j] or j in support for j in range(n)) for i,u,v,k in leading)
            return {'accessible':False,'leading_order':p,'closed_face_support':sorted(support),'trials':trials,
              'support_reaction_tests':checks,'all_degree_strict_cone_impossible':True,'network_stability':'UNKNOWN'}
    assert leading
    if not include_formal_bounds:
        return {'accessible':True,'leading_order':p,'trials':trials,'support_reaction_tests':checks}
    rate_sum=sum(k for i,u,v,k in leading);rate_min=min(k for i,u,v,k in leading)
    C=max(F(1),p**3*rate_sum);T=1/(4*C);levels=[F(3,4*n)]
    for j in range(n):levels.append(min(levels[-1],T*rate_min*levels[-1]**p/(4*n)))
    delta=levels[-1];M=n*max(1,ceil(3*C**3*T**3/(n*delta)))
    error=3*C**3*T**3/(2*M);assert error<=delta/2
    return {'accessible':True,'leading_order':p,'trials':trials,'support_reaction_tests':checks,
      'norm_bound_C':C,'time_T':T,'minimum_leading_rate':rate_min,'leading_rate_sum':rate_sum,
      'support_lower_levels':levels,'terminal_A_lower_delta':delta,'Euler_steps_M':M,'Euler_step_h':T/M,
      'directional_Taylor_error_upper':error,'boundary_derivative_margin':delta/(2*T),
      'formal_initial_polynomial_degree':{'base':p,'exponent':M-1,'meaning':'p**(M-1); not expanded',
        'degree_integer_bit_upper':p.bit_length()*(M-1)+1},
      'formal_elevation_bound':'q=d+p-1; S=2*p*sum_leading_rates*d*n**(d-1); choose r>=max(q,q*(q-1),4*S*q*(q-1)/(delta/(2*T))); final degree r-p+1',
      'formal_construction_executed':False,
      'guarantee':'Unbudgeted exact degree-cone search terminates positively; no practical worst-case cost claim'}

def solve(A,b):
    n=len(b);M=[[F(x) for x in row]+[F(z)] for row,z in zip(A,b)]
    for j in range(n):
        p=next((i for i in range(j,n) if M[i][j]),None)
        if p is None:return None
        M[j],M[p]=M[p],M[j];z=M[j][j];M[j]=[x/z for x in M[j]]
        for i in range(n):
            if i!=j and M[i][j]:
                z=M[i][j];M[i]=[x-z*y for x,y in zip(M[i],M[j])]
    return [row[-1] for row in M]

def build_cone(rec,degree):
    assert type(degree)==int and degree>=1
    n=len(rec['species']);A=rec['pivot'];J=rec['satellites'];allmon=list(comps(degree,n))
    variable=allmon;leading_degree=degree+rec['leading_order']-1
    # There are len(variable) coefficient variables, then beta, then affine constant.
    dimension=len(variable)+1;work={'formal_multiplication_term_pairs':0}
    internal=[(u,v,k,falling(u,work)) for u,v,k in rec['internal']]
    generators={};multinomial={}
    for a in allmon:
        c=F(factorial(degree),prod(factorial(z) for z in a));multinomial[a]=c;g={}
        for u,v,k,rate in internal:
            nu=tuple(y-x for x,y in zip(u,v));delta=add(shift(a,nu,work),mono(a,-1))
            g=add(g,scale(mul(rate,delta,work),k*c))
        assert all(sum(z)<=leading_degree for z in g);generators[a]=g
    boundary=[]
    for z in comps(leading_degree,len(J)):
        a=[0]*n
        for j,c in zip(J,z):a[j]=c
        boundary.append(tuple(a))
    coeff_forms={}
    for z in boundary:
        coeff_forms[z]=[generators[a].get(z,F(0)) for a in variable]+[F(0),F(0)]
    upper=max([F(1)]+[sum(abs(c) for c in form) for z,form in coeff_forms.items() if max(z)==leading_degree])
    rows=[]
    def row(label,form):
        form=list(map(F,form))
        if any(form):rows.append({'label':label,'form':form})
    for i,a in enumerate(variable):
        v=[F(0)]*(dimension+1);v[i]=-1;row(['coefficient_lower',a],v)
        v=[F(0)]*(dimension+1);v[i]=1;v[-1]=-1;row(['coefficient_upper',a],v)
    v=[F(0)]*(dimension+1);v[-2]=-1;row(['beta_lower'],v)
    v=[F(0)]*(dimension+1);v[-2]=1;v[-1]=-upper;row(['beta_upper'],v)
    for z,form in coeff_forms.items():
        v=[-a for a in form]
        if max(z)==leading_degree:v[-2]=1
        row(['pure_boundary' if max(z)==leading_degree else 'mixed_boundary',z],v)
    feasible=[F(1)]*len(variable)+[F(0)]
    assert all(sum(a*b for a,b in zip(r['form'][:-1],feasible))+r['form'][-1]<=0 for r in rows)
    work.update({'homogeneous_basis_polynomials':len(allmon),'raw_internal_channels':len(internal),
      'generator_nonzero_monomials':sum(map(len,generators.values())),
      'largest_generator_coefficient_bits':max([0]+[max(c.numerator.bit_length(),c.denominator.bit_length()) for g in generators.values() for c in g.values()])})
    return {'degree':degree,'leading_degree':leading_degree,'variable':variable,'multinomial':multinomial,'generators':generators,
      'constraints':rows,'dimension':dimension,'work':work}

def acquire_degree(rec,degree,max_bases=200000):
    cone=build_cone(rec,degree);rows=cone['constraints'];dim=cone['dimension'];attempts=nonsingular=bits=0
    total=comb(len(rows),dim)
    for basis in combinations(range(len(rows)),dim):
        if max_bases is not None and attempts>=max_bases:
            return {'accepted':False,'degree':degree,'reason':'exact basis budget exhausted','network_stability':'UNKNOWN',
              'basis_attempts':attempts,'total_candidate_bases':total,'formal_work':cone['work']}
        attempts+=1;forms=[rows[i]['form'] for i in basis]
        x=solve([r[:-1] for r in forms],[-r[-1] for r in forms])
        if x is None:continue
        nonsingular+=1;bits=max(bits,max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in x))
        if x[-1]<=0:continue
        residual=[sum(a*b for a,b in zip(r['form'][:-1],x))+r['form'][-1] for r in rows]
        if max(residual)>0:continue
        coefficients=dict(zip(cone['variable'],x[:-1]));H={};LH={}
        for a,c in coefficients.items():
            H=add(H,mono(a,cone['multinomial'][a]*c));LH=add(LH,scale(cone['generators'][a],c))
        G={a:c for a,c in LH.items() if sum(a)==cone['leading_degree']};remainder={a:c for a,c in LH.items() if sum(a)<cone['leading_degree']}
        K=sum(-c for a,c in G.items() if a[rec['pivot']]>0 and c<0);CR=sum(abs(c) for c in remainder.values())
        return {'accepted':True,'degree':degree,'bernstein_coefficients':coefficients,'H':H,'LH':LH,'G':G,'remainder':remainder,
          'beta':x[-1],'K':K,'remainder_bound':CR,'active_basis':basis,'basis_solution':x,'exact_residuals':residual,
          'constraints':rows,'LP_dimension':dim,'basis_attempts':attempts,'nonsingular_bases':nonsingular,
          'total_candidate_bases':total,'largest_solved_fraction_bits':bits,'formal_work':cone['work']}
    return {'accepted':False,'degree':degree,'reason':'exact cone exhausted; no positive beta','network_stability':'UNKNOWN',
      'algebraic_cone_exhausted':True,'basis_attempts':attempts,'nonsingular_bases':nonsingular,
      'total_candidate_bases':total,'formal_work':cone['work']}

def construct(rec,t=F(2),max_degree=2,max_bases=200000,max_expanded_bits=100000):
    assert rec['accepted'] and isinstance(t,(int,F)) and t>1;t=F(t)
    assert max_degree is None or (type(max_degree)==int and max_degree>=1)
    support=support_certificate(rec)
    if not support['accessible']:return {'accepted':False,'reason':'invariant leading-support face obstructs every strict cone degree','network_stability':'UNKNOWN','support_certificate':support,'basis_attempts':0}
    trials=[];used=0
    degrees=count(1) if max_degree is None else range(1,max_degree+1)
    for degree in degrees:
        budget=None if max_bases is None else max_bases-used
        acq=acquire_degree(rec,degree,budget);used+=acq['basis_attempts']
        if acq['accepted']:break
        trials.append(acq)
        if not acq.get('algebraic_cone_exhausted',False):return {'accepted':False,'reason':'hierarchy work budget exhausted','explicit_certificate_status':'UNKNOWN','network_stability':'structural support theorem applies; explicit quantitative certificate not acquired','trials':trials,'basis_attempts':used,'support_certificate':support}
    else:return {'accepted':False,'reason':'all requested degree cones exhausted','explicit_certificate_status':'UNKNOWN','network_stability':'structural support theorem applies; explicit quantitative certificate not acquired','trials':trials,'basis_attempts':used,'support_certificate':support}
    d=degree;p=rec['leading_order'];m=len(rec['satellites']);D=rec['death']*(1-1/t);K=acq['K'];beta=acq['beta'];CR=acq['remainder_bound']
    eps=min(F(1,2),D/(4*K)) if K else F(1,2)
    C0=rec['immigration']*(t/(1-eps)-1)+rec['death']*eps*d/(t*(1-eps))+eps*CR/(1-eps)
    kappa=min(D/4,eps*beta/(2**(2*d+2*p-3)*m**(d+p-2)));R=max(1,ceil((C0+kappa)/kappa));coefficient=C0+kappa
    nb=coefficient.numerator.bit_length()+R*t.numerator.bit_length();db=coefficient.denominator.bit_length()+R*t.denominator.bit_length()
    foster={'coefficient':coefficient,'base':t,'exponent':R,'unreduced_numerator_bits_upper':nb,'unreduced_denominator_bits_upper':db,'serialization_bit_cap':12000,'requested_expansion_bit_cap':max_expanded_bits,'expanded':max(nb,db)<=min(max_expanded_bits,12000)}
    if foster['expanded']:foster['value']=coefficient*t**R
    return {'accepted':True,'acquisition':acq,'support_certificate':support,'prior_degree_trials':trials,'total_basis_attempts':used,'t':t,'degree':d,'leading_order':p,'denominator_degree':d+p-2,
      'epsilon':eps,'death_exponential_coefficient':D,'C0':C0,'kappa':kappa,'R':R,'foster_constant':foster,
      'finite_exception_count_upper':comb(R+len(rec['species'])-1,len(rec['species']))}

def evaluate(poly,x):return sum(c*prod(z**a for z,a in zip(x,u)) for u,c in poly.items())
def h(cert,x):return 1-cert['epsilon']*evaluate(cert['acquisition']['H'],x)/F((sum(x)+1)**cert['denominator_degree'])
def ff(x,u):
    if any(z<a for z,a in zip(x,u)):return 0
    return prod(prod(range(z-a+1,z+1)) for z,a in zip(x,u))
def quotient(rec,cert,x):
    hx=h(cert,x);out=F(0)
    for u,v,k in rec['reactions']:
        rate=k*ff(x,u)
        if not rate:continue
        y=tuple(z-a+b for z,a,b in zip(x,u,v))
        out+=rate*(cert['t']**(sum(v)-sum(u))*h(cert,y)/hx-1)
    return out

def demo_network():
    z=(0,0,0);A=(1,0,0);BB=(0,2,0);BC=(0,1,1);CC=(0,0,2);AB=(1,1,0)
    return ['A','B','C'],[(z,A,1),(A,z,1),(BB,BC,1),(BC,BB,1),(CC,BC,1),(BC,CC,2),(BC,AB,1),(AB,BC,1)]
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):
        if any(isinstance(k,tuple) for k in x):return [{'exponent':k,'coefficient':clean(v)} for k,v in sorted(x.items())]
        return {k:clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x

def main():
    sp,raw=demo_network();rec=recognize(sp,raw);cert=construct(rec);assert cert['accepted'] and cert['degree']==2
    checks=0
    for N in range(31):
      for x in comps(N,len(sp)):
        q=quotient(rec,cert,x);assert q<=cert['C0']-cert['kappa']*N,(x,q);checks+=1
    targets=[]
    for N in [cert['R']-1,cert['R'],cert['R']+1,10**6,10**50]:
      for x in [(0,N,0),(0,0,N),(1,N-1,0),(1,0,N-1),(0,N//2,N-N//2),(N,0,0)]:
        q=quotient(rec,cert,x);bound=cert['C0']-cert['kappa']*N;assert q<=bound
        targets.append({'state':x,'quotient':q,'bound':bound})
    print(json.dumps(clean({'recognition':rec,'certificate':cert,'ordinary_exact_checks':checks,'targeted_checks':targets}),indent=2,sort_keys=True))
if __name__=='__main__':main()
