"""Raw coupled-quartic acquisition and exact partition-free capacity bounds.
Standard library only. No fiber sampler, partition oracle or supplied axis.
"""
from fractions import Fraction as F
from math import isqrt
from time import perf_counter
from pathlib import Path
import hashlib
import json

class Unknown(ValueError):
    """Insufficient grammar, certificate, resolution or paid budget."""

def positive_int(x, name):
    if type(x) is not int or x <= 0: raise Unknown(name+" must be a strict positive integer")

def bits(a): return max(abs(a.numerator).bit_length(), a.denominator.bit_length())

def rational(x, max_bits):
    if type(x) is int:
        if abs(x).bit_length() > max_bits: raise Unknown("input integer bit budget")
        return F(x)
    if type(x) is not str or len(x) > 2*max_bits+4: raise Unknown("canonical rational string or strict integer required")
    try:
        a = F(x)
        if str(a) != x: raise Unknown("noncanonical rational")
    except (ValueError, ZeroDivisionError) as exc: raise Unknown("rational decoding or serialization digit budget") from exc
    if bits(a) > max_bits: raise Unknown("input rational bit budget")
    return a

def acquire(raw, max_dimension=1024, max_terms=100000, max_coefficient_bits=65536):
    start = perf_counter()
    for k,v in [("dimension",max_dimension),("terms",max_terms),("coefficient bits",max_coefficient_bits)]: positive_int(v,k)
    if type(raw) is not dict or set(raw) != {"n","terms"}: raise Unknown("raw input schema")
    n = raw["n"]
    if type(n) is not int or not 3 <= n <= max_dimension: raise Unknown("physical dimension outside admitted budget or m<2")
    records=raw["terms"]
    if type(records) is not list or not 0 < len(records) <= max_terms: raise Unknown("raw term budget/schema")
    terms={}
    for rec in records:
        if type(rec) is not dict or set(rec) != {"powers","coefficient"}: raise Unknown("raw monomial schema")
        p=rec["powers"]
        if type(p) is not list or len(p)!=n or any(type(k) is not int or not 0<=k<=8 for k in p): raise Unknown("strict bounded exponent vector")
        p=tuple(p)
        if sum(p) not in (4,6,8) or p in terms: raise Unknown("monomial degree or duplicate")
        a=rational(rec["coefficient"],max_coefficient_bits)
        if not a: raise Unknown("zero raw term")
        terms[p]=a
    quartic={p:a for p,a in terms.items() if sum(p)==4}
    if not quartic: raise Unknown("missing lowest homogeneous part")
    absent=[j for j in range(n) if all(p[j]==0 for p in quartic)]
    if len(absent)!=1: raise Unknown("no unique aligned absent direction; rotated grammar not supplied")
    y=absent[0]; p0,a0=next(iter(quartic.items())); top=list(p0);top[y]=4
    t=terms.get(tuple(top),F(0))/a0
    if not 0<t<1: raise Unknown("positive stiffness ratio acquisition failed")
    kappa=t/(1-t); U={p:a/(1+kappa) for p,a in quartic.items()}; diagonals={}; edges=[]
    for p,a in U.items():
        support=[i for i,k in enumerate(p) if k]
        if len(support)==1 and p[support[0]]==4 and a>0: diagonals[support[0]]=a
        elif len(support)==2 and all(p[i]==2 for i in support) and a>0: edges.append((support[0],support[1],a))
        else: raise Unknown("quartic sign or coercivity grammar")
    if set(diagonals)!=set(range(n))-{y}: raise Unknown("missing strictly positive fiber diagonal")
    expected={}
    for p,a in U.items():
        for e,c in [(0,1+kappa),(2,-2*kappa),(4,kappa)]:
            pp=list(p);pp[y]=e;expected[tuple(pp)]=a*c
    if terms!=expected: raise Unknown("full raw polynomial identity failed")
    serial=[[list(p),rational_string(terms[p])] for p in sorted(terms)]
    digest=hashlib.sha256(json.dumps(serial,separators=(",",":")).encode()).hexdigest()
    return {"route":"unique_absent_axis_full_coefficient_identity_positive_quartic",
            "n":n,"m":n-1,"homogeneous_degree":4,"axis":y,"kappa":rational_string(kappa),
            "d_min":rational_string(min(diagonals.values())),"coercivity_a":rational_string(min(diagonals.values())/(n-1)),
            "diagonals":[[i,rational_string(diagonals[i])] for i in sorted(diagonals)],
            "couplings":[[i,j,rational_string(a)] for i,j,a in sorted(edges)],"raw_terms":len(terms),
            "raw_polynomial_sha256":digest,"max_input_rational_bits":max(bits(a) for a in terms.values()),
            "seconds":perf_counter()-start}

def root_bounds(a,p,degree=4):
    """floor/ceil of 2**p a**(1/degree), using exact integer operations."""
    if type(a) is not F or a<0 or type(p) is not int or p<0 or type(degree)is not int or degree not in (2,4): raise Unknown("root arguments")
    num=a.numerator << (degree*p); z=num//a.denominator; k=isqrt(z)
    if degree==4:k=isqrt(k)
    return k,k if k**degree*a.denominator==num else k+1

def show(a):
    try:z=float(a)
    except OverflowError:return None
    return None if z==0 and a!=0 else z

def rational_string(a):
    try:return str(a)
    except ValueError as exc:raise Unknown("exact serialization exceeds interpreter digit budget") from exc

def interval(pair):
    return {"lower":rational_string(pair[0]),"upper":rational_string(pair[1]),
            "lower_display":show(pair[0]),"upper_display":show(pair[1])}

class Integrator:
    def __init__(self,m,kappa,precision,max_points,max_power_bits):
        self.m,self.kappa,self.p=m,kappa,precision;self.max_points,self.max_power_bits=max_points,max_power_bits
        self.cache={};self.power_calls=0;self.max_power_integer_bits=0
    def power(self,a,n):
        # Scope: high-degree point/tail powers and subsequent root shifts;
        # NOT every Fraction addition elsewhere in the program.
        bound=bits(a)*abs(n)
        if bound+4*self.p>self.max_power_bits:raise Unknown("power/root-shift bit budget exhausted before exponentiation")
        out=a**n;self.power_calls+=1;self.max_power_integer_bits=max(self.max_power_integer_bits,bits(out));return out
    def point(self,y):
        if y in self.cache:return self.cache[y]
        if len(self.cache)>=self.max_points:raise Unknown("total distinct point budget exhausted")
        v=1+self.kappa*(1-y*y)**2;a=self.power(v,self.m)
        out=root_bounds(1/a,self.p),root_bounds(a,self.p);self.cache[y]=out;return out
    def integrate(self,a,b,N,which):
        # Caller separates all turning points at0 and1.
        if not a<b or type(N)is not int or N<=0:raise Unknown("monotone quadrature arguments")
        h=(b-a)/N;prev=self.point(a)[which];lo=hi=0
        for j in range(1,N+1):
            cur=self.point(a+j*h)[which];lo+=min(prev[0],cur[0]);hi+=max(prev[1],cur[1]);prev=cur
        return h*F(lo,1<<self.p),h*F(hi,1<<self.p)
    def tail(self,T):
        # q<=kappa^(-m/4)(1-T^-2)^(-m/2)y^-m for y>=T>1.
        a=self.power(1/(self.kappa*(1-1/(T*T))**2),self.m);_,hi=root_bounds(a,self.p)
        return F(hi,1<<self.p)*self.power(T,1-self.m)/(self.m-1)

def certify(raw,beta=F(1),quad_relative=F(1,100),max_dimension=1024,max_terms=100000,
            max_coefficient_bits=65536,max_grid=131072,max_points=1000000,max_cutoff=65536,
            max_precision=16384,max_power_bits=2000000):
    start=perf_counter()
    task={"beta":beta,"quad_relative":quad_relative,"max_dimension":max_dimension,"max_terms":max_terms,
          "max_coefficient_bits":max_coefficient_bits,"max_grid":max_grid,"max_points":max_points,
          "max_cutoff":max_cutoff,"max_precision":max_precision,"max_power_bits":max_power_bits}
    for name in ["beta","quad_relative"]:
        if type(task[name])is not F or task[name]<=0:raise Unknown("positive exact Fraction task parameter required: "+name)
    for name,value in task.items():
        if name not in ("beta","quad_relative"):positive_int(value,name)
    if max_grid<64 or max_cutoff<2:raise Unknown("initial numerical grid/cutoff exceeds budget")
    if max(bits(beta),bits(quad_relative))>max_coefficient_bits:raise Unknown("task rational input bit budget")
    acq=acquire(raw,max_dimension,max_terms,max_coefficient_bits);m=acq["m"];kappa=F(acq["kappa"]);dmin=F(acq["d_min"])
    p=max(192,m*(bits(kappa)+2)+128)
    if p>max_precision:raise Unknown("fixed precision exceeds paid budget")
    ii=Integrator(m,kappa,p,max_points,max_power_bits);seed=ii.integrate(F(1),F(5,4),32,0)[0]
    if seed<=0:raise Unknown("fixed precision cannot resolve positive seed mass")
    T=F(2)
    while ii.tail(T)>quad_relative*seed/8:
        T*=2
        if T>max_cutoff:raise Unknown("tail cutoff budget exhausted")
    N=64
    while True:
        if N>max_grid:raise Unknown("quadrature grid budget exhausted")
        ml,mu=ii.integrate(F(1,2),F(1),N,0);a=F(1)
        while a<T:
            ll,uu=ii.integrate(a,2*a,N,0);ml+=ll;mu+=uu;a*=2
        mass=ml,mu+ii.tail(T);rl,ru=ii.integrate(F(0),F(1,2),N,1);resistance=2*rl,2*ru
        if ml>0 and rl>0 and mass[1]*resistance[1]<=(1+quad_relative)*mass[0]*resistance[0]:break
        N*=2
    vmin=1+F(9,16)*kappa;fa=1/(beta*dmin*vmin)
    if bits(fa)+2*p>max_power_bits:raise Unknown("factor root-shift bit budget")
    _,hi=root_bounds(fa,p,2);factor=1+kappa*F(hi,1<<p)/(2*vmin)
    rn,rd=isqrt(fa.numerator),isqrt(fa.denominator)
    if rn*rn==fa.numerator and rd*rd==fa.denominator:factor=1+kappa*F(rn,rd)/(2*vmin)
    free=1/(beta*mass[1]*resistance[1]),1/(beta*mass[0]*resistance[0]);full=free[0]/factor,free[1]
    return {"schema":"homogeneous_quartic_capacity.v1","task":{k:rational_string(v) if type(v)is F else v for k,v in task.items()},
            "acquisition":acq,"b":"1/2","observable":"cap_mu(A,B)/mu(A)",
            "basins":"x[axis]<=-1/2 and x[axis]>=1/2, full physical fibers",
            "not_claimed":"MFPT, arbitrary-start kinetics, angular mixing, projected Markov dynamics",
            "mass":interval(mass),"resistance":interval(resistance),"free_rate":interval(free),"full_rate":interval(full),
            "factor_upper":rational_string(factor),"N":N,"T":str(T),"tail_upper":rational_string(ii.tail(T)),
            "precision_bits":p,"point_evaluations":len(ii.cache),"power_calls":ii.power_calls,
            "max_power_integer_bits":ii.max_power_integer_bits,"quad_ratio_display":show(mass[1]*resistance[1]/(mass[0]*resistance[0])),
            "seconds":perf_counter()-start}

def same_typed(a,b):
    if type(a)is not type(b):return False
    if type(a)is list:return len(a)==len(b) and all(same_typed(x,y) for x,y in zip(a,b))
    if type(a)is dict:return set(a)==set(b) and all(same_typed(a[k],b[k]) for k in a)
    return a==b

def verify(raw,certificate,**external_task):
    expected=certify(raw,**external_task)
    if type(certificate)is not dict:raise Unknown("certificate record required")
    for k in ["schema","task","b","observable","basins","factor_upper","N","T","tail_upper","precision_bits"]:
        if not same_typed(certificate.get(k),expected[k]):raise Unknown("strict external task/numerical binding: "+k)
    got=certificate.get("acquisition")
    if type(got)is not dict or not same_typed({k:v for k,v in got.items() if k!="seconds"},{k:v for k,v in expected["acquisition"].items() if k!="seconds"}):raise Unknown("strict raw polynomial/acquisition binding")
    for k in ["mass","resistance","free_rate","full_rate"]:
        if type(certificate.get(k))is not dict:raise Unknown("interval schema")
        for side in ["lower","upper"]:
            if not same_typed(certificate[k].get(side),expected[k][side]):raise Unknown("exact recomputed interval binding")
    return {"status":"PASS","scope":"raw coupled quartic full-fiber capacity/mass","physical_m":expected["acquisition"]["m"]}

def fixture(m,kappa=F(1),dmin=F(1),graph="chain",coupling=F(20),axis=0):
    n=m+1;fiber=[i for i in range(n) if i!=axis];U=[]
    for i in fiber:
        p=[0]*n;p[i]=4;U.append((p,dmin))
    if graph=="chain":edges=list(zip(fiber[:-1],fiber[1:]))
    elif graph=="complete":edges=[(i,j) for i in fiber for j in fiber if i<j]
    elif graph=="none":edges=[]
    else:raise ValueError("fixture graph")
    for i,j in edges:
        p=[0]*n;p[i]=p[j]=2;U.append((p,coupling))
    terms=[]
    for p,a in U:
        for yp,c in [(0,1+kappa),(2,-2*kappa),(4,kappa)]:
            pp=p.copy();pp[axis]=yp;terms.append({"powers":pp,"coefficient":str(a*c)})
    return {"n":n,"terms":terms}

def main():
    output=[]
    for m in [2,3,4,16,64,128,256]:
        raw=fixture(m);cert=certify(raw);output.append({"fixture":{"m":m,"graph":"chain","coupling":"20"},"certificate":cert})
        print(json.dumps({"m":m,"terms":cert["acquisition"]["raw_terms"],"low":cert["full_rate"]["lower_display"],"high":cert["full_rate"]["upper_display"],"factor":cert["factor_upper"],"points":cert["point_evaluations"],"seconds":cert["seconds"]}),flush=True)
    Path("results.json").write_text(json.dumps(output,indent=2))
    raw=fixture(12,graph="complete",coupling=F(1000000),axis=5);cert=certify(raw)
    Path("dense_graph_raw.json").write_text(json.dumps(raw,indent=2));Path("dense_graph_certificate.json").write_text(json.dumps(cert,indent=2))
if __name__=="__main__":main()
