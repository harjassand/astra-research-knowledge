"""Exact raw-list acquisition of a normalized weighted-mass Foster certificate.
Trusted int/Fraction research API; no stationary-fiber or supplied-weight oracle.
"""
from fractions import Fraction as F
from itertools import combinations
from math import prod,comb,ceil
import json

def wr(rs):
    vertices={u for u,v,k in rs}|{v for u,v,k in rs};adj={u:[] for u in vertices}
    for u,v,k in rs:adj[u].append(v)
    for u,v,k in rs:
        seen={v};todo=[v]
        while todo:
            for w in adj[todo.pop()]:
                if w not in seen:seen.add(w);todo.append(w)
        if u not in seen:return False
    return True

def solve(A,b):
    n=len(b);M=[[F(x) for x in row]+[F(z)] for row,z in zip(A,b)]
    for j in range(n):
        piv=next((i for i in range(j,n) if M[i][j]),None)
        if piv is None:return None
        M[j],M[piv]=M[piv],M[j];d=M[j][j];M[j]=[x/d for x in M[j]]
        for i in range(n):
            if i!=j and M[i][j]:
                d=M[i][j];M[i]=[x-d*y for x,y in zip(M[i],M[j])]
    return [row[-1] for row in M]

def recognize(species,reactions):
    n=len(species);rs=[]
    assert n>=2
    for u,v,k in reactions:
        assert len(u)==len(v)==n and all(type(a)==int and a>=0 for a in (*u,*v))
        assert isinstance(k,(int,F)) and F(k)>0
        if tuple(u)!=tuple(v):rs.append((tuple(u),tuple(v),F(k)))
    if not wr(rs):return {'accepted':False,'reason':'raw graph is not weakly reversible'}
    zero=(0,)*n;trials=[]
    for pivot in range(n):
        unit=tuple(int(i==pivot) for i in range(n));lam=F(0);death=F(0);internal=[];bad=[]
        for u,v,k in rs:
            if u==zero and v==unit:lam+=k
            elif u==unit and v==zero:death+=k
            elif sum(u)==sum(v):internal.append((u,v,k))
            else:bad.append((u,v))
        if bad or not lam or not death:
            trials.append({'pivot':pivot,'reason':'not one immigrating/dying coordinate plus conservative internal channels'});continue
        return {'accepted':True,'species':species,'pivot':pivot,'satellites':[i for i in range(n) if i!=pivot],
          'immigration':lam,'death':death,'internal':internal,'reactions':rs,'recognition_trials':len(trials)+1}
    return {'accepted':False,'reason':'no acquired open-coordinate partition','trials':trials}

def acquire_weight(rec,max_bases=200000):
    n=len(rec['species']);pivot=rec['pivot'];J=rec['satellites'];dim=len(J)+1
    # Last variable is beta; last affine-form entry is its constant.
    groups={}
    for u,v,k in rec['internal']:
        a=[k*(v[j]-u[j]) for j in J]+[F(0),k*(v[pivot]-u[pivot])]
        groups.setdefault(u,[F(0)]*(dim+1))
        groups[u]=[x+y for x,y in zip(groups[u],a)]
    constraints=[]
    def add(a,label):
        a=list(map(F,a))
        if any(a):constraints.append({'label':label,'form':a})
    for j in range(len(J)):
        a=[F(0)]*(dim+1);a[j]=-1;add(a,['weight_lower',J[j]])
        a=[F(0)]*(dim+1);a[j]=1;a[-1]=-1;add(a,['weight_upper',J[j]])
    upper=max(F(1),2*sum(k for u,v,k in rec['internal'] if sum(u)==2))
    a=[F(0)]*(dim+1);a[-2]=-1;add(a,['beta_lower'])
    a=[F(0)]*(dim+1);a[-2]=1;a[-1]=-upper;add(a,['beta_upper'])
    for j in J:
        u=tuple(2*int(i==j) for i in range(n));a=[-z for z in groups.get(u,[F(0)]*(dim+1))];a[-2]+=1
        add(a,['pure_satellite_production',j])
    for j,l in combinations(J,2):
        u=tuple(int(i==j)+int(i==l) for i in range(n));add([-z for z in groups.get(u,[F(0)]*(dim+1))],['mixed_satellite_production',j,l])
    for row,(u,v,k) in enumerate(rec['internal']):
        if sum(u)<=2:continue
        a=[F(v[j]-u[j]) for j in J]+[F(0),F(v[pivot]-u[pivot])]
        add(a,['higher_order_neutral_plus',row]);add([-z for z in a],['higher_order_neutral_minus',row])
    count=comb(len(constraints),dim);attempts=0;nonsingular=0;maxbits=0
    for basis in combinations(range(len(constraints)),dim):
        if max_bases is not None and attempts>=max_bases:
            return {'accepted':False,'reason':'explicit exact-basis work budget exceeded','basis_budget':max_bases,
              'basis_attempts':attempts,'total_candidate_bases':count,'constraints':constraints}
        attempts+=1;rows=[constraints[i]['form'] for i in basis]
        x=solve([a[:-1] for a in rows],[-a[-1] for a in rows])
        if x is None:continue
        nonsingular+=1;maxbits=max(maxbits,max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in x))
        if x[-1]<=0:continue
        residuals=[sum(a*b for a,b in zip(row['form'][:-1],x))+row['form'][-1] for row in constraints]
        if max(residuals)>0:continue
        v=[F(0)]*n;v[pivot]=1
        for j,a in zip(J,x[:-1]):v[j]=a
        return {'accepted':True,'weights':v,'beta':x[-1],'constraints':constraints,'active_basis':basis,'basis_solution':x,
          'exact_residuals':residuals,'basis_attempts':attempts,'nonsingular_bases':nonsingular,'total_candidate_bases':count,
          'largest_basis_fraction_bits':maxbits,'lp_dimension':dim}
    return {'accepted':False,'reason':'exhausted linear-composition polytope has no positive beta',
      'network_stability':'UNKNOWN','algebraic_cone_exhausted':True,'basis_attempts':attempts,'nonsingular_bases':nonsingular,
      'total_candidate_bases':count,'constraints':constraints}

def construct(rec,t=F(2),max_bases=200000,max_expanded_constant_bits=100000):
    assert rec['accepted'] and isinstance(t,(int,F)) and t>1;t=F(t)
    weight=acquire_weight(rec,max_bases)
    if not weight['accepted']:return weight
    v=weight['weights'];beta=weight['beta'];n=len(v);pivot=rec['pivot'];m=n-1
    coefficients={}
    for u,w,k in rec['internal']:
        drift=k*sum(v[i]*(w[i]-u[i]) for i in range(n));coefficients[u]=coefficients.get(u,F(0))+drift
        if sum(u)>2:assert drift==0
    K1=max([F(0)]+[-a for u,a in coefficients.items() if sum(u)==1])
    K2=max([F(0)]+[-a for u,a in coefficients.items() if sum(u)==2 and u[pivot]>0])
    D=rec['death']*(1-1/t)
    eps=min(F(1,2),D/(4*K2)) if K2 else F(1,2)
    C=rec['immigration']*(t-1)+rec['death']*eps/(t*(1-eps))+eps*(K1+beta)/(1-eps)
    kappa=min(D/4,eps*beta/(8*m));zeta=kappa;R=max(1,ceil((C+zeta)/kappa))
    coefficient=C+zeta
    numerator_bound=coefficient.numerator.bit_length()+R*t.numerator.bit_length()
    denominator_bound=coefficient.denominator.bit_length()+R*t.denominator.bit_length()
    foster={'coefficient':coefficient,'base':t,'exponent':R,'meaning':'coefficient * base**exponent',
      'unreduced_numerator_bits_upper':numerator_bound,'unreduced_denominator_bits_upper':denominator_bound,
      'expanded':max(numerator_bound,denominator_bound)<=max_expanded_constant_bits}
    if foster['expanded']:foster['value']=coefficient*t**R
    return {'accepted':True,'t':t,'weight_acquisition':weight,'weights':v,'beta':beta,'K1':K1,'K2':K2,'death_exponential_coefficient':D,
      'epsilon_composition':eps,'constant_quotient_bound':C,'radial_dissipation':kappa,'foster_epsilon':zeta,'exception_radius':R,
      'source_drift_coefficients':[{'source':u,'coefficient':a} for u,a in sorted(coefficients.items())],
      'foster_constant':foster,'work':{'recognition_trials':rec['recognition_trials'],'exact_basis_attempts':weight['basis_attempts'],
       'nonsingular_bases':weight['nonsingular_bases'],'LP_dimension':weight['lp_dimension'],'LP_constraints':len(weight['constraints']),
       'largest_basis_fraction_bits':weight['largest_basis_fraction_bits'],'total_count_exception_states_upper':comb(R+n-1,n)}}

def compositions(total,n):
    if n==1:yield(total,)
    else:
        for a in range(total+1):
            for rest in compositions(total-a,n-1):yield(a,)+rest

def ff(x,u):
    if any(a<b for a,b in zip(x,u)):return 0
    return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))

def h(cert,x):return 1-cert['epsilon_composition']*sum(a*b for a,b in zip(cert['weights'],x))/(sum(x)+1)
def value(cert,x):return cert['t']**sum(x)*h(cert,x)
def quotient(rec,cert,x):
    hx=h(cert,x);out=F(0)
    for u,v,k in rec['reactions']:
        rate=k*ff(x,u)
        if not rate:continue
        xp=tuple(a-b+c for a,b,c in zip(x,u,v))
        out+=rate*(cert['t']**(sum(v)-sum(u))*h(cert,xp)/hx-1)
    return out

def demo_network():
    sp=['A','B','C'];z=(0,0,0);A=(1,0,0);AB=(1,1,0);BC=(0,1,1);AC=(1,0,1);BB=(0,2,0);CC=(0,0,2)
    rs=[(z,A,1),(A,z,1),(AB,BC,1),(BC,AB,1),(AC,BB,1),(BB,AC,1),(BC,CC,2),(CC,BC,1)]
    return sp,rs

def encode(x):
    if isinstance(x,F):return str(x)
    raise TypeError(type(x))

def main():
    sp,rs=demo_network();rec=recognize(sp,rs);assert rec['accepted'];cert=construct(rec);assert cert['accepted']
    checks=0
    for N in range(31):
      for x in compositions(N,len(sp)):
        q=quotient(rec,cert,x);bound=cert['constant_quotient_bound']-cert['radial_dissipation']*N
        assert q<=bound,(x,q,bound);checks+=1
    targeted=[]
    for N in [cert['exception_radius']-1,cert['exception_radius'],cert['exception_radius']+1,10**6,10**50]:
      for x in [(0,0,N),(1,0,N-1),(0,N,0),(N,0,0),(N//3,N//3,N-2*(N//3))]:
        q=quotient(rec,cert,x);bound=cert['constant_quotient_bound']-cert['radial_dissipation']*N
        assert q<=bound
        targeted.append({'state':x,'exact_quotient':q,'linear_bound':bound})
    print(json.dumps({'recognition':rec,'certificate':cert,'exact_quotient_checks':checks,'targeted_checks':targeted},default=encode,sort_keys=True,indent=2))
if __name__=='__main__':main()
