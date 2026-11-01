"""Exact raw mixed-degree dilation acquisition and partition-free rate bounds.
Standard library only; no internal partition, matrix, sampler, or Gamma oracle.
"""
from fractions import Fraction as F
from math import gcd,isqrt
from pathlib import Path
from time import perf_counter
import hashlib,json

class Unknown(ValueError): pass

def positive_int(x,name):
    if type(x)is not int or x<=0:raise Unknown(name+' must be a strict positive integer')

def bits(x):return max(abs(x.numerator).bit_length(),x.denominator.bit_length())

def fs(x):
    try:return str(x)
    except ValueError as exc:raise Unknown('exact serialization digit budget') from exc

def decode_rational(x,max_bits):
    if type(x)is int:
        if abs(x).bit_length()>max_bits:raise Unknown('coefficient integer bit budget')
        return F(x)
    if type(x)is not str or len(x)>2*max_bits+4:raise Unknown('canonical rational string or strict integer required')
    try:
        z=F(x)
        if str(z)!=x:raise Unknown('noncanonical rational')
    except (ValueError,ZeroDivisionError) as exc:raise Unknown('rational decoding/serialization budget') from exc
    if bits(z)>max_bits:raise Unknown('coefficient rational bit budget')
    return z

def profile_coefficients(kappa,degree):
    a=[F(1)];s=[1+kappa,-2*kappa,kappa]
    for _ in range(degree):
        b=[F(0)]*(len(a)+2)
        for i,x in enumerate(a):
            for j,y in enumerate(s):b[i+j]+=x*y
        a=b
    return a

def acquire(raw,max_dimension=1024,max_terms=100000,max_coefficient_bits=65536,
            max_exponent_entries=16000000,max_total_coefficient_bits=16000000):
    start=perf_counter()
    for k,v in [('dimension',max_dimension),('terms',max_terms),('coefficient bits',max_coefficient_bits),
                ('exponent entries',max_exponent_entries),('total coefficient bits',max_total_coefficient_bits)]:positive_int(v,k)
    if type(raw)is not dict or set(raw)!={'n','terms'}:raise Unknown('raw polynomial schema')
    n=raw['n'];records=raw['terms']
    if type(n)is not int or not 2<=n<=max_dimension:raise Unknown('physical dimension budget, m>=1 required')
    if type(records)is not list or not 0<len(records)<=max_terms or n*len(records)>max_exponent_entries:
        raise Unknown('raw term/exponent-entry budget')
    terms={};total_bits=0
    for rec in records:
        if type(rec)is not dict or set(rec)!={'powers','coefficient'}:raise Unknown('monomial schema')
        powers=rec['powers']
        if type(powers)is not list or len(powers)!=n or any(type(k)is not int or not 0<=k<=20 for k in powers):
            raise Unknown('strict bounded exponent vector')
        p=tuple(powers)
        if p in terms or not 2<=sum(p)<=20:raise Unknown('duplicate or out-of-grammar degree')
        c=decode_rational(rec['coefficient'],max_coefficient_bits)
        if not c:raise Unknown('zero raw term')
        total_bits+=bits(c)
        if total_bits>max_total_coefficient_bits:raise Unknown('total input coefficient bit budget')
        terms[p]=c
    quadratic={p:c for p,c in terms.items() if sum(p)==2}
    diagonal={}
    for p,c in quadratic.items():
        support=[i for i,k in enumerate(p) if k]
        if len(support)!=1 or p[support[0]]!=2 or c<=0:raise Unknown('aligned positive quadratic grammar')
        diagonal[support[0]]=c
    absent=set(range(n))-set(diagonal)
    if len(absent)!=1:raise Unknown('no unique aligned null axis from positive quadratic Hessian')
    axis=next(iter(absent));i0=next(iter(diagonal));p0=[0]*n;p0[i0]=2;p0[axis]=2
    t=-terms.get(tuple(p0),F(0))/(4*diagonal[i0])
    if not 0<t<1:raise Unknown('positive dilation parameter acquisition')
    kappa=t/(1-t);s0=1+kappa
    U2={};U4={};diags4={};edges=[]
    for i,c in diagonal.items():
        p=[0]*n;p[i]=2;U2[tuple(p)]=c/s0**2
    for p,c in terms.items():
        if p[axis]!=0 or sum(p)!=4:continue
        support=[i for i,k in enumerate(p) if k];u=c/s0**4
        if len(support)==1 and p[support[0]]==4 and u>0:diags4[support[0]]=u
        elif len(support)==2 and all(p[i]==2 for i in support) and u>0:edges.append((support[0],support[1],u))
        else:raise Unknown('nonnegative quartic-component grammar')
        U4[p]=u
    expected={}
    for degree,component in [(2,U2),(4,U4)]:
        coeff=profile_coefficients(kappa,degree)
        for p,u in component.items():
            for j,c in enumerate(coeff):
                if c:
                    pp=list(p);pp[axis]=2*j;expected[tuple(pp)]=u*c
    if terms!=expected:raise Unknown('ENTIRE raw dilation polynomial identity failed')
    digest=hashlib.sha256(('dilation_raw.v1;n='+str(n)+'\n').encode())
    for p in sorted(terms):digest.update((json.dumps([list(p),fs(terms[p])],separators=(',',':'))+'\n').encode())
    qmin=min(U2.values());degree_cap=4 if U4 else 2
    return {'route':'aligned_quadratic_null_axis_full_s2_U2_plus_s4_U4_identity',
            'n':n,'m':n-1,'axis':axis,'kappa':fs(kappa),'degree_cap':degree_cap,
            'active_energy_degrees':[2,4] if U4 else [2],
            'energy_is_mixed_degree':bool(U4),'coercivity':'U(z)>=q_min*||z||^2','q_min':fs(qmin),
            'quadratic_diagonals':[[i,fs(diagonal[i]/s0**2)] for i in sorted(diagonal)],
            'quartic_diagonals':[[i,fs(diags4[i])] for i in sorted(diags4)],
            'quartic_couplings':[[i,j,fs(c)] for i,j,c in sorted(edges)],
            'raw_terms':len(terms),'raw_exponent_entries':n*len(terms),
            'total_input_coefficient_bits':total_bits,'max_input_coefficient_bits':max(bits(c) for c in terms.values()),
            'raw_polynomial_sha256':digest.hexdigest(),'seconds':perf_counter()-start}

def show(x):
    try:a=float(x)
    except OverflowError:return None
    return None if a==0 and x!=0 else a

def interval(pair):return {'lower':fs(pair[0]),'upper':fs(pair[1]),'lower_display':show(pair[0]),'upper_display':show(pair[1])}

class Integrator:
    def __init__(self,m,kappa,degree_cap,precision,max_evaluations,max_power_bits):
        self.m=m;self.kappa=kappa;self.d=degree_cap;self.P=precision
        self.max_evaluations=max_evaluations;self.max_power_bits=max_power_bits
        self.cache={};self.profiles={};self.power_calls=0;self.max_power_integer_bits=0;self.tail_calls=0
        self.s0=1+kappa;self.s0p=self.power(self.s0,self.d);self.s02p=self.power(self.s0,2*self.d)
    def power(self,x,n,shift_bits=0):
        if type(x)is not F or x<=0 or type(n)is not int:raise Unknown('internal rational power arguments')
        if bits(x)*abs(n)+shift_bits>self.max_power_bits:raise Unknown('high-degree power/root-shift budget before exponentiation')
        a=x**n;self.power_calls+=1;self.max_power_integer_bits=max(self.max_power_integer_bits,bits(a));return a
    def bounds(self,x,n,d=1):
        g=gcd(abs(n),d);nn=n//g;dd=d//g
        if dd not in (1,2,4):raise Unknown('unsupported exact root degree')
        a=self.power(x,nn,dd*self.P);num=a.numerator<<(dd*self.P);z=num//a.denominator
        if dd==1:k=z
        elif dd==2:k=isqrt(z)
        else:k=isqrt(isqrt(z))
        return k,k if k**dd*a.denominator==num else k+1
    def profile(self,y):
        if y not in self.profiles:self.profiles[y]=1+self.kappa*(1-y*y)**2
        return self.profiles[y]
    def point(self,kind,y):
        key=(kind,y)
        if key in self.cache:return self.cache[key]
        if len(self.cache)>=self.max_evaluations:raise Unknown('total distinct scalar-evaluation budget')
        s=self.profile(y)
        if kind=='q':ans=self.bounds(s,-self.m)
        elif kind=='r0':
            if not 0<=y<=F(1,2):raise Unknown('resistance outside proven half slab')
            ans=self.bounds(s,self.m)
        elif kind=='rplus':
            if not 0<=y<=F(1,2):raise Unknown('extra resistance outside proven half slab')
            sp=self.power(s,self.d);r=self.s02p/(2*self.s0p-sp)
            ans=self.bounds(r,self.m,self.d)
        else:raise Unknown('unknown scalar integrand')
        self.cache[key]=ans;return ans
    def integrate(self,a,b,N,kind):
        if not a<b or type(N)is not int or N<=0:raise Unknown('monotone interval/grid')
        h=(b-a)/N;previous=self.point(kind,a);lo=hi=0
        for j in range(1,N+1):
            current=self.point(kind,a+j*h);lo+=min(previous[0],current[0]);hi+=max(previous[1],current[1]);previous=current
        return h*F(lo,1<<self.P),h*F(hi,1<<self.P)
    def tail(self,T):
        self.tail_calls+=1
        b=1/(self.kappa*(1-1/(T*T))**2)
        return self.power(b,self.m)*self.power(T,1-4*self.m)/(4*self.m-1)

def family_descriptor():
    return {'quantifier':'for every finite constant SPD transverse matrix M',
            'longitudinal_mobility':'1','cross_mobility':'zero',
            'drift_noise_relation':'reversible block mobility with covariance 2*diag(1,M)/beta',
            'actual_physical_membership':'not authenticated',
            'parallel_endpoint_status':'not evaluated; no angular-independent exact endpoint equality claimed'}

def certify(raw,beta=F(1),quad_relative=F(1,100),full_ratio=None,max_dimension=1024,
            max_terms=100000,max_coefficient_bits=65536,max_exponent_entries=16000000,
            max_total_coefficient_bits=16000000,max_grid=131072,max_evaluations=1000000,
            max_cutoff=65536,max_precision=16384,max_power_bits=2000000):
    start=perf_counter()
    task={'beta':beta,'quad_relative':quad_relative,'full_ratio':full_ratio,
          'max_dimension':max_dimension,'max_terms':max_terms,'max_coefficient_bits':max_coefficient_bits,
          'max_exponent_entries':max_exponent_entries,'max_total_coefficient_bits':max_total_coefficient_bits,
          'max_grid':max_grid,'max_evaluations':max_evaluations,'max_cutoff':max_cutoff,
          'max_precision':max_precision,'max_power_bits':max_power_bits}
    for k in ['beta','quad_relative']:
        if type(task[k])is not F or task[k]<=0:raise Unknown('strict positive Fraction task: '+k)
    if full_ratio is not None and (type(full_ratio)is not F or full_ratio<=1):raise Unknown('requested TOTAL ratio must be Fraction>1 or None')
    for k,v in task.items():
        if k not in ['beta','quad_relative','full_ratio']:positive_int(v,k)
    if max_grid<64 or max_cutoff<2:raise Unknown('initial grid/cutoff budget')
    if max(bits(beta),bits(quad_relative),bits(full_ratio) if full_ratio is not None else 0)>max_coefficient_bits:raise Unknown('task coefficient bit budget')
    acq=acquire(raw,max_dimension,max_terms,max_coefficient_bits,max_exponent_entries,max_total_coefficient_bits)
    m=acq['m'];kappa=F(acq['kappa']);d=acq['degree_cap'];P=max(192,m*(bits(kappa)+4)+128)
    if P>max_precision:raise Unknown('fixed precision budget')
    ii=Integrator(m,kappa,d,P,max_evaluations,max_power_bits)
    seed=ii.integrate(F(1),F(5,4),32,'q')[0]
    if seed<=0:raise Unknown('unresolved positive seed at fixed precision')
    T=F(2)
    while ii.tail(T)>quad_relative*seed/8:
        T*=2
        if T>max_cutoff:raise Unknown('tail cutoff budget')
    N=64
    while True:
        if N>max_grid:raise Unknown('quadrature grid budget')
        if N*(T.numerator.bit_length()+2)+3>max_evaluations:raise Unknown('necessary final scalar-evaluation count exceeds budget')
        ml,mu=ii.integrate(F(1,2),F(1),N,'q');a=F(1)
        while a<T:
            lo,hi=ii.integrate(a,2*a,N,'q');ml+=lo;mu+=hi;a*=2
        mass=ml,mu+ii.tail(T)
        a,b=ii.integrate(F(0),F(1,2),N,'r0');r0=2*a,2*b
        a,b=ii.integrate(F(0),F(1,2),N,'rplus');rp=2*a,2*b
        if min(mass[0],r0[0],rp[0])>0 and mass[1]*r0[1]*rp[1]<=(1+quad_relative)*mass[0]*r0[0]*rp[0]:break
        N*=2
    free=1/(beta*mass[1]*r0[1]),1/(beta*mass[0]*r0[0])
    full=1/(beta*mass[1]*rp[1]),free[1];ratio=full[1]/full[0]
    if full_ratio is not None and ratio>full_ratio:raise Unknown('finite comparison bracket does not meet requested TOTAL ratio; not an arbitrary-accuracy guarantee')
    return {'schema':'mixed_degree_geometric_dilation_capacity.v1',
            'method':'spatial_Jacobian_fixed_fiber_Cauchy_radial_degree_concavity_Jensen',
            'task':{k:fs(v) if type(v)is F else v for k,v in task.items()},'acquisition':acq,
            'mobility_family':family_descriptor(),'observable':'for every declared M: cap_mu,M(A,B)/mu(A)',
            'basins':'x[axis]<=-1/2 and x[axis]>=1/2, full physical fibers','b':'1/2',
            'marginal':'q(y)=s(y)^(-m); spatial dilation, not homogeneous-energy scaling',
            'mass':interval(mass),'resistance':interval(r0),'jensen_resistance':interval(rp),
            'free_rate':interval(free),'uniform_rate_enclosure':interval(full),
            'structural_ratio':interval((max(F(1),rp[0]/r0[1]),rp[1]/r0[0])),
            'full_ratio_exact':fs(ratio),'N':N,'T':fs(T),'precision_bits':P,'tail_upper':fs(ii.tail(T)),
            'scalar_evaluations':len(ii.cache),'profile_evaluations':len(ii.profiles),'power_calls':ii.power_calls,
            'tail_calls':ii.tail_calls,'max_power_integer_bits':ii.max_power_integer_bits,
            'numerical_product_ratio_display':show(mass[1]*r0[1]*rp[1]/(mass[0]*r0[0]*rp[0])),
            'seconds':perf_counter()-start}

def same_typed(a,b):
    if type(a)is not type(b):return False
    if type(a)is list:return len(a)==len(b) and all(same_typed(x,y) for x,y in zip(a,b))
    if type(a)is dict:return set(a)==set(b) and all(same_typed(a[k],b[k]) for k in a)
    return a==b

def verify(raw,certificate,**external_task):
    expected=certify(raw,**external_task)
    if type(certificate)is not dict:raise Unknown('certificate schema')
    for k in ['schema','method','task','mobility_family','observable','basins','b','marginal','full_ratio_exact','N','T','precision_bits','tail_upper']:
        if not same_typed(certificate.get(k),expected[k]):raise Unknown('strict original task/model binding: '+k)
    got=certificate.get('acquisition')
    if type(got)is not dict or not same_typed({k:v for k,v in got.items() if k!='seconds'},
                                             {k:v for k,v in expected['acquisition'].items() if k!='seconds'}):raise Unknown('complete raw-acquisition binding')
    for k in ['mass','resistance','jensen_resistance','free_rate','uniform_rate_enclosure','structural_ratio']:
        if type(certificate.get(k))is not dict:raise Unknown('interval schema')
        for side in ['lower','upper']:
            if not same_typed(certificate[k].get(side),expected[k][side]):raise Unknown('exact endpoint binding')
    return {'status':'PASS','scope':'mixed-degree geometric-dilation universal fixed-SPD family outer capacity interval',
            'physical_m':expected['acquisition']['m'],'degree_cap':expected['acquisition']['degree_cap'],
            'actual_physical_membership':'not authenticated','full_ratio_exact':expected['full_ratio_exact']}

def fixture(m,kappa=F(1),quadratic=F(1),quartic=F(1),coupling=F(20),graph='chain',axis=0):
    n=m+1;fiber=[i for i in range(n) if i!=axis];U2=[];U4=[]
    for i in fiber:
        p=[0]*n;p[i]=2;U2.append((p,quadratic))
        if quartic:
            p=[0]*n;p[i]=4;U4.append((p,quartic))
    if graph=='chain':edges=list(zip(fiber[:-1],fiber[1:]))
    elif graph=='complete':edges=[(i,j) for i in fiber for j in fiber if i<j]
    elif graph=='none':edges=[]
    else:raise ValueError('fixture graph')
    if coupling:
        for i,j in edges:
            p=[0]*n;p[i]=p[j]=2;U4.append((p,coupling))
    records=[]
    for d,component in [(2,U2),(4,U4)]:
        coeff=profile_coefficients(kappa,d)
        for p,u in component:
            for j,c in enumerate(coeff):
                if u*c:
                    pp=p.copy();pp[axis]=2*j;records.append({'powers':pp,'coefficient':fs(u*c)})
    return {'n':n,'terms':records}

def main():
    results=[]
    for m,delta,target in [(1,F(1,100),None),(2,F(1,100),None),(3,F(1,100),None),(4,F(1,100),None),
                           (16,F(1,100),None),(64,F(1,100),None),(128,F(1,100),None),
                           (256,F(1,200),F(103,100)),(512,F(1,1000),F(101,100))]:
        t=perf_counter();raw=fixture(m);input_seconds=perf_counter()-t;c=certify(raw,quad_relative=delta,full_ratio=target)
        results.append({'m':m,'quad_relative':fs(delta),'requested_full_ratio':None if target is None else fs(target),
                        'fixture_seconds':input_seconds,'certificate':c})
        print(json.dumps({'m':m,'raw_terms':c['acquisition']['raw_terms'],'low':c['uniform_rate_enclosure']['lower_display'],
                          'high':c['uniform_rate_enclosure']['upper_display'],'ratio':show(F(c['full_ratio_exact'])),
                          'evaluations':c['scalar_evaluations'],'seconds':c['seconds']}),flush=True)
    Path('results.json').write_text(json.dumps(results,indent=2))
    raw=fixture(3,axis=2);c=certify(raw)
    Path('small_raw_fixture.json').write_text(json.dumps(raw,indent=2));Path('small_certificate.json').write_text(json.dumps(c,indent=2))
if __name__=='__main__':main()
