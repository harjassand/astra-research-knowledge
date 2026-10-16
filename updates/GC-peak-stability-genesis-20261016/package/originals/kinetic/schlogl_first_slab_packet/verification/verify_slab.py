#!/usr/bin/env python3
"""Independent rejection gate for the unchanged eight-site Schlogl slab.

Saved binary64 arrays define the exact mathematical trajectory. Spatial TT
contractions use directed Decimal arithmetic; polynomial/model arithmetic uses
exact rational interval endpoints. A rejection concerns the forward l1 defect
certificate, NOT a lower bound on the actual probability error.

No imports from the candidate solver or previous residual implementation.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import time
import zipfile
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np

D = 163
ORDER = [0, 4, 1, 5, 2, 6, 3, 7]
EDGES = [(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7)]
DIFF = F('8.2207')
INITIAL = (50,) * 8

def birth(n): return F('2.676') * n * (n-1) + F('108.102')
def death(n): return F('0.040') * n * (n-1) * (n-2) + F('37.881') * n
def target(x): return all(n <= 15 for n in x)
def escape(x):
    return sum((birth(n)+death(n) for n in x), F(0)) + DIFF * sum(x[i]+x[j] for i,j in EDGES)

def column(x):
    """Exact generator column on frozen-target grid plus overflow scalar."""
    if target(x): return {}, F(0)
    out = {x: -escape(x)}
    overflow = F(0)
    def put(y, v):
        nonlocal overflow
        if any(n < 0 or n >= D for n in y): overflow += v
        else:
            y = tuple(y)
            out[y] = out.get(y, F(0)) + v
    for i, n in enumerate(x):
        y = list(x); y[i] += 1; put(y, birth(n))
        if n:
            y = list(x); y[i] -= 1; put(y, death(n))
    for i,j in EDGES:
        for a,b in ((i,j),(j,i)):
            if x[a]:
                y = list(x); y[a] -= 1; y[b] += 1; put(y, DIFF*x[a])
    return out, overflow

def predecessors(x):
    """All nonzero full, UNPROJECTED G[x,y], with true outward losses."""
    out = {}
    if not target(x): out[x] = -escape(x)
    def put(y, v):
        y = tuple(y)
        if v and not target(y): out[y] = out.get(y, F(0)) + v
    for i, n in enumerate(x):
        if n:
            y=list(x); y[i]-=1; put(y,birth(n-1))
        if n < D-1:
            y=list(x); y[i]+=1; put(y,death(n+1))
    for i,j in EDGES:
        for a,b in ((i,j),(j,i)):
            if x[a] < D-1 and x[b] > 0:
                y=list(x); y[a]+=1; y[b]-=1; put(y,DIFF*y[a])
    return out

@dataclass(frozen=True)
class RI:
    lo: F
    hi: F
    @classmethod
    def exact(cls,x): return cls(F(x),F(x))
    def __add__(self, other):
        if not isinstance(other, RI): other=RI.exact(other)
        return RI(self.lo+other.lo,self.hi+other.hi)
    __radd__=__add__
    def __neg__(self): return RI(-self.hi,-self.lo)
    def __sub__(self,other): return self+-other if isinstance(other,RI) else self+(-F(other))
    def __mul__(self,other):
        if not isinstance(other,RI): other=RI.exact(other)
        p=(self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi)
        return RI(min(p),max(p))
    __rmul__=__mul__
    def abs_lower(self): return max(self.lo,-self.hi,F(0))
    def abs_upper(self): return max(abs(self.lo),abs(self.hi))

ZERO = RI.exact(0)

def p_add(a,b):
    z=[ZERO]*max(len(a),len(b))
    for i,c in enumerate(a): z[i]=z[i]+c
    for i,c in enumerate(b): z[i]=z[i]+c
    return z
def p_scale(a,s): return [x*s for x in a]
def p_eval(a,x):
    y=ZERO
    for v in reversed(a): y=y*x+v
    return y
def p_derivative(a): return [a[i]*i for i in range(1,len(a))] or [ZERO]

def cheb_to_power_u(c):
    """T_k(2u-1), using exact integer recurrence and rational intervals."""
    t0=[RI.exact(1)]
    ans=p_scale(t0,c[0])
    if len(c)==1: return ans
    t1=[RI.exact(-1),RI.exact(2)]
    ans=p_add(ans,p_scale(t1,c[1]))
    for k in range(2,len(c)):
        # 2(2u-1) T_{k-1} - T_{k-2}
        t=p_add(p_add(p_scale(t1,-2),[ZERO]+p_scale(t1,4)),p_scale(t0,-1))
        ans=p_add(ans,p_scale(t,c[k])); t0,t1=t1,t
    return ans

def integrated_abs_lower(p,h,bins):
    """h sum |integral_bin p| <= integral_0^h |p(t/h)| dt.

    All signed temporal terms survive until exact bin integration. Increasing
    dyadic bins gives monotone exact-value lower bounds; interval widths may
    prevent practical monotonicity but cannot invalidate any returned bound.
    """
    anti=[ZERO]+[c*F(1,k+1) for k,c in enumerate(p)]
    last=p_eval(anti,F(0)); s=F(0)
    for j in range(1,bins+1):
        v=p_eval(anti,F(j,bins)); s+=(v-last).abs_lower(); last=v
    return h*s

def integrated_square(p,h):
    """Full signed temporal Gram sum, INCLUDING every cross term."""
    v=ZERO
    for i,a in enumerate(p):
        for j,b in enumerate(p): v=v+a*b*F(1,i+j+1)
    return v*h

class DecimalContractor:
    def __init__(self, precision):
        self.down=Context(prec=precision,rounding=ROUND_FLOOR,Emin=-999999999,Emax=999999999)
        self.up=Context(prec=precision,rounding=ROUND_CEILING,Emin=-999999999,Emax=999999999)
        self.constants={}
    def value(self,x):
        # Decimal.from_float is exact, independent of context precision.
        return Decimal.from_float(float(x))
    def mul_exact(self,lo,hi,c):
        if c>=0: return self.down.multiply(lo,c),self.up.multiply(hi,c)
        return self.down.multiply(hi,c),self.up.multiply(lo,c)
    def row_mat(self,vec,mat):
        out=[]
        for j in range(mat.shape[1]):
            lo=hi=Decimal(0)
            for i,(a,b) in enumerate(vec):
                c=self.value(mat[i,j])
                if not c or (not a and not b): continue
                l,u=self.mul_exact(a,b,c)
                lo=self.down.add(lo,l); hi=self.up.add(hi,u)
            out.append((lo,hi))
        return out
    def point(self,cores,x,order):
        vec=[(Decimal(1),Decimal(1))]
        for i,g in enumerate(cores): vec=self.row_mat(vec,g[:,x[order[i]],:])
        if len(vec)!=1: raise ValueError('Each basis TT must have terminal rank 1')
        a,b=vec[0]; return RI(F(a),F(b))
    def functional(self,cores,weights=None):
        """Outward full-grid sum; no positivity is assumed for the TT."""
        vec=[(Decimal(1),Decimal(1))]
        for site,g in enumerate(cores):
            w=None if weights is None else weights[site]
            out=[]
            for j in range(g.shape[2]):
                lo=hi=Decimal(0)
                for i,(a,b) in enumerate(vec):
                    if not a and not b: continue
                    ml=mh=Decimal(0)
                    row=g[i,:,j]
                    for n in np.flatnonzero(row):
                        c=self.value(row[n])
                        if w is None:
                            lower=upper=c
                        else:
                            # Supplied Decimal weights must represent exact
                            # constants, not rounded evaluations of a function.
                            lower=self.down.multiply(c,w[n]);upper=self.up.multiply(c,w[n])
                        ml=self.down.add(ml,lower); mh=self.up.add(mh,upper)
                    if not ml and not mh: continue
                    pairs=((a,ml),(a,mh),(b,ml),(b,mh))
                    lower=min(self.down.multiply(x,y) for x,y in pairs)
                    upper=max(self.up.multiply(x,y) for x,y in pairs)
                    lo=self.down.add(lo,lower); hi=self.up.add(hi,upper)
                out.append((lo,hi))
            vec=out
        if len(vec)!=1: raise ValueError('Functional requires terminal rank 1')
        return RI(F(vec[0][0]),F(vec[0][1]))

class Slab:
    def __init__(self,manifest,precision=80):
        self.manifest_path=Path(manifest)
        self.m=json.loads(self.manifest_path.read_text())
        if self.m.get('schema')!='schlogl-chebyshev-basis-v1': raise ValueError('Unrecognized export schema')
        self.order=self.m['order']
        if sorted(self.order)!=list(range(8)): raise ValueError('Invalid physical ordering')
        if self.m['cap']!=162 or self.m['target_max']!=15 or self.m['semantics']!='frozen_target_grid_plus_overflow': raise ValueError('Model semantics mismatch')
        self.a=F(self.m['t_start']); self.h=F(self.m['h'])
        if self.h<=0: raise ValueError('Slab length must be positive')
        expected_rates={'birth_quadratic':'2.676','birth_constant':'108.102','death_cubic':'0.040','death_linear':'37.881','diffusion':'8.2207'}
        if 'rates' in self.m and any(F(self.m['rates'][k])!=F(value) for k,value in expected_rates.items()): raise ValueError('Physical rate mismatch')
        if 'physical_edges' in self.m and set(tuple(sorted(e)) for e in self.m['physical_edges'])!=set(EDGES): raise ValueError('Physical graph mismatch')
        self.npz_path=self.manifest_path.parent/self.m['npz']
        self.z=np.load(self.npz_path,allow_pickle=False)
        self.C=self.z['time_coefficients']
        if self.C.ndim!=2: raise ValueError('time_coefficients must be matrix')
        self.basis=[]
        for j in range(self.C.shape[0]):
            cores=[self.z[f'basis_{j}_core_{i}'] for i in range(8)]
            last=1
            for g in cores:
                if g.ndim!=3 or g.shape[:2]!=(last,D): raise ValueError('TT shape mismatch')
                if g.dtype!=np.float64 or not np.isfinite(g).all(): raise ValueError('Require finite binary64 cores')
                last=g.shape[2]
            if last!=1: raise ValueError('Basis terminal rank must be 1')
            self.basis.append(cores)
        if self.C.dtype!=np.float64 or not np.isfinite(self.C).all(): raise ValueError('Require finite binary64 time coefficients')
        self.overflow=self.z['overflow_coefficients']
        if self.overflow.dtype!=np.float64 or not np.isfinite(self.overflow).all(): raise ValueError('Require finite binary64 overflow coefficients')
        self.anchored=bool(self.m.get('anchored_chebyshev',False))
        if self.anchored:
            self.initial=self.z['initial_coefficients']
            self.initial_overflow=float(self.z['initial_overflow'])
            if self.initial.shape!=(self.C.shape[0],) or self.initial.dtype!=np.float64 or not np.isfinite(self.initial).all(): raise ValueError('Invalid anchored initial coefficients')
            if np.any(self.C[:,0]!=0) or self.overflow[0]!=0 or not math.isfinite(self.initial_overflow): raise ValueError('Invalid anchored constant columns')
        self.time_power=[self.scalar_power(self.C[j],float(self.initial[j]) if self.anchored else None) for j in range(self.C.shape[0])]
        self.contractor=DecimalContractor(precision)
        self.cache={}
    def scalar_power(self,c,initial=None):
        c=[F.from_float(float(v)) for v in c]
        if initial is not None:
            c[0]=F.from_float(initial)-sum((c[k]*(-1)**k for k in range(1,len(c))),F(0))
        return cheb_to_power_u([RI.exact(v) for v in c])
    def coordinate(self,x):
        x=tuple(x)
        if x not in self.cache:
            vals=[self.contractor.point(g,x,self.order) for g in self.basis]
            power=[ZERO]
            for j,v in enumerate(vals): power=p_add(power,p_scale(self.time_power[j],v))
            self.cache[x]=power
        return self.cache[x]
    def residual_coordinate(self,x):
        q=self.coordinate(x)
        r=p_scale(p_derivative(q),1/self.h)
        for y,rate in predecessors(x).items(): r=p_add(r,p_scale(self.coordinate(y),-rate))
        return r
    def overflow_power(self): return self.scalar_power(self.overflow,self.initial_overflow if self.anchored else None)

def fraction_json(x):
    # Exact string is authoritative; float is a human-readable diagnostic only.
    return {'exact':str(x),'approximate':float(x)}
def interval_json(x): return {'lower':fraction_json(x.lo),'upper':fraction_json(x.hi)}

def verify(args):
    start=time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(args.memory_mib*1024**2,args.memory_mib*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(args.cpu_seconds,args.cpu_seconds+1))
    mf=json.loads(Path(args.manifest).read_text())
    npzpath=Path(args.manifest).parent/mf['npz']
    with zipfile.ZipFile(npzpath) as z:
        export_bytes=sum(x.file_size for x in z.infolist())
    if export_bytes>args.memory_mib*1024**2*0.60:
        raise MemoryError('Export exceeds 60% of declared memory cap; no contraction started')
    slab=Slab(args.manifest,args.precision)
    prev=Slab(args.previous,args.precision) if args.previous else None
    if prev:
        if prev.a+prev.h!=slab.a: raise ValueError('Slab join times do not match exactly')
    elif slab.a!=0: raise ValueError('Noninitial slab requires previous export for join accounting')
    coords=[INITIAL]
    if args.initial_support: coords=sorted(column(INITIAL)[0])
    if args.coordinates:
        coords=[tuple(map(int,x.split(','))) for x in args.coordinates]
    if any(len(x)!=8 or any(n<0 or n>=D for n in x) for x in coords): raise ValueError('Invalid physical coordinates')
    coords=sorted(set(coords))
    results=[]; init=F(0); residual=F(0)
    for x in coords:
        incoming=p_eval(prev.coordinate(x),F(1)) if prev else RI.exact(int(x==INITIAL))
        jump=p_eval(slab.coordinate(x),F(0))-incoming
        r=slab.residual_coordinate(x)
        lower=integrated_abs_lower(r,slab.h,args.bins)
        initial=jump.abs_lower(); init+=initial; residual+=lower
        results.append({'coordinate_physical':x,'initial_or_join_interval':interval_json(jump),'initial_or_join_l1_lower':fraction_json(initial),'integrated_abs_residual_lower':fraction_json(lower),'integrated_residual_square_interval':interval_json(integrated_square(r,slab.h)),'residual_power_u_coefficients':[interval_json(c) for c in r]})
    incoming=p_eval(prev.overflow_power(),F(1)) if prev else RI.exact(0)
    sinkjump=p_eval(slab.overflow_power(),F(0))-incoming
    init+=sinkjump.abs_lower()
    lower=init+residual
    budget=F(args.budget)
    exact_initial=None
    if not prev and slab.a==0 and slab.anchored and slab.initial_overflow==0:
        nz=np.flatnonzero(slab.initial)
        if len(nz)==1 and slab.initial[nz[0]]==1:
            exact_initial=all(g.shape==(1,D,1) and np.array_equal(g[0,:,0],np.eye(D)[50]) for g in slab.basis[int(nz[0])])
    digest=hashlib.sha256()
    with slab.npz_path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''): digest.update(block)
    report={'status':'REJECT_FORWARD_L1_DEFECT_BUDGET' if lower>budget else 'INCONCLUSIVE_LOWER_BOUND_ONLY','warning':'A rejection is not a lower bound on the true probability error; inconclusive is not certification.','manifest':str(slab.manifest_path),'npz_sha256':digest.hexdigest(),'h':str(slab.h),'coordinates_checked':len(coords),'full_operator_coordinate_evaluations':len(slab.cache),'precision_decimal':args.precision,'bins':args.bins,'initial_join_selected_lower':fraction_json(init),'overflow_initial_join_interval':interval_json(sinkjump),'integrated_l1_residual_selected_lower':fraction_json(residual),'forward_defect_selected_lower':fraction_json(lower),'declared_budget':str(budget),'overflow_residual_evaluated':False,'global_upper_bound_produced':False,'arithmetic':'Exact dyadic inputs; directed Decimal TT point contractions; exact rational interval model and polynomial algebra. No floating BLAS contraction.','export_uncompressed_bytes':export_bytes,'resource_limit_mib':args.memory_mib,'cpu_limit_seconds':args.cpu_seconds,'elapsed_seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'coordinates':results}
    report['global_initial_defect_exact']='0' if exact_initial else None
    report['full_1e9_interior_budget_rejected']=lower>F('1e-9')
    Path(args.output).write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='coordinates'},indent=2))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest'); ap.add_argument('--previous')
    ap.add_argument('--output',required=True)
    ap.add_argument('--precision',type=int,default=80)
    ap.add_argument('--bins',type=int,default=256)
    ap.add_argument('--budget',default='1e-13')
    ap.add_argument('--memory-mib',type=int,default=512)
    ap.add_argument('--cpu-seconds',type=int,default=120)
    ap.add_argument('--initial-support',action='store_true')
    ap.add_argument('--coordinates',nargs='+')
    a=ap.parse_args()
    if a.bins<=0 or a.bins&(a.bins-1): ap.error('bins must be positive power of two')
    if a.precision<30: ap.error('precision must be at least 30 decimal digits')
    verify(a)
if __name__=='__main__': main()
