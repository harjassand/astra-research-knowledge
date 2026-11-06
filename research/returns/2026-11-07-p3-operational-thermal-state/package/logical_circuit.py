"""Finite-dyadic Ry/Rz/CNOT emitter for block purification and CG decoding.

Angles are certified by outward Decimal interval arithmetic, with an explicit
arctan-series remainder, then stored as exact rational numbers. Binary64 is
used ONLY by the separate diagnostic state-vector simulator. This emitter
does not compile a native device, calibrate gates, or execute a preparation.
"""
from fractions import Fraction as Q
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from functools import lru_cache
from math import ceil,log2
from collections import Counter
import secrets
import numpy as np
from certified_blocks import multiplicity,round_q

DN=Context(prec=60,rounding=ROUND_FLOOR)
UP=Context(prec=60,rounding=ROUND_CEILING)
NEAR=Context(prec=60,rounding=ROUND_HALF_EVEN)

class Interval:
    def __init__(self,x=0,hi=None):
        if isinstance(x,Interval): self.lo,self.hi=x.lo,x.hi; return
        if hi is not None: self.lo,self.hi=x,hi; return
        x=Q(x); self.lo=DN.divide(D(x.numerator),D(x.denominator)); self.hi=UP.divide(D(x.numerator),D(x.denominator))
    def __add__(self,b):
        b=Interval(b); return Interval(DN.add(self.lo,b.lo),UP.add(self.hi,b.hi))
    __radd__=__add__
    def __neg__(self): return Interval(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,b): return self+-Interval(b)
    def __rsub__(self,b): return Interval(b)+-self
    def __mul__(self,b):
        b=Interval(b)
        lo=min(DN.multiply(x,y) for x in (self.lo,self.hi) for y in (b.lo,b.hi))
        hi=max(UP.multiply(x,y) for x in (self.lo,self.hi) for y in (b.lo,b.hi))
        return Interval(lo,hi)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=Interval(b); assert b.lo>0
        return self*Interval(DN.divide(D(1),b.hi),UP.divide(D(1),b.lo))
    def sqrt(self):
        assert self.lo>=0
        if self.lo==self.hi and self.lo in (D(0),D(1)): return Interval(self)
        lo=NEAR.next_minus(NEAR.sqrt(self.lo)) if self.lo else D(0)
        hi=NEAR.next_plus(NEAR.sqrt(self.hi)) if self.hi else D(0)
        return Interval(lo,hi)

def atan_small_rational(x,n):
    term=x; s=Q(0)
    for k in range(n):
        s+=term/(2*k+1); term*=-x*x
    tail=abs(term)/(2*n+1)
    return s-tail,s+tail

al,ah=atan_small_rational(Q(1,5),56)
bl,bh=atan_small_rational(Q(1,239),18)
PI=Interval(16*al-4*bh)
PI=Interval(PI.lo,Interval(16*ah-4*bl).hi)

def atan_unit(x):
    x=Interval(x); assert x.lo>=0 and x.hi<=1
    for _ in range(3): x=x/(1+(1+x*x).sqrt())
    assert x.hi<D('0.1')
    xx=x*x; term=x; total=Interval(0)
    for k in range(12):
        total=total+term/(2*k+1); term=-(term*xx)
    # Next alternating term <= .1^25/25; multiply by 8 for half-angle undo.
    return total*8+Interval(D('-1e-24'),D('1e-24'))

def phase_interval(y,x):
    if not y and not x: return Interval(0)
    if not x: return PI*(Q(1,2) if y>0 else -Q(1,2))
    if not y: return PI if x<0 else Interval(0)
    ax,ay=abs(x),abs(y)
    a=atan_unit(Interval(Q(ay,ax))) if ay<=ax else PI/2-atan_unit(Interval(Q(ax,ay)))
    if x<0: a=PI-a
    if y<0: a=-a
    return a

def probability_angle(p0,p1,negative_up=False):
    if p0+p1==0: return Interval(0)
    if not p1: a=Interval(0)
    elif not p0: a=PI
    elif p1<=p0: a=2*atan_unit(Interval(Q(p1,p0)).sqrt())
    else: a=PI-2*atan_unit(Interval(Q(p0,p1)).sqrt())
    return 2*PI-a if negative_up else a

class AngleFactory:
    def __init__(self,bits=48):
        self.bits=bits; self.max_error=Q(0); self.calls=0
        self.pi=self.quantize(PI)
    def quantize(self,a):
        lo,hi=Q(a.lo),Q(a.hi); q=Q(round_q((lo+hi)/2,1<<self.bits),1<<self.bits)
        self.max_error=max(self.max_error,abs(q-lo),abs(q-hi)); self.calls+=1
        assert self.max_error<=Q(1,1<<self.bits),'Increase arctan/Decimal precision for this angle budget.'
        return q
    @lru_cache(maxsize=100000)
    def probability(self,p0,p1,negative=False): return self.quantize(probability_angle(p0,p1,negative))
    @lru_cache(maxsize=100000)
    def phase(self,y,x): return self.quantize(phase_interval(y,x))

class Circuit:
    def __init__(self,nqubits,angles=None):
        self.nqubits=nqubits; self.gates=[]; self.angles=angles or AngleFactory()
        self.fixed_pi_weight=Q(0)
    def rot(self,axis,t,a):
        if a: self.gates.append((axis,t,Q(a)))
    def cx(self,c,t): self.gates.append(('CX',c,t))
    def pi_rot(self,axis,t,factor):
        self.rot(axis,t,factor*self.angles.pi); self.fixed_pi_weight+=abs(factor)/2
    def H(self,t):
        self.pi_rot('RZ',t,Q(1)); self.pi_rot('RY',t,Q(1,2))
    def X(self,t):
        self.pi_rot('RZ',t,Q(1)); self.pi_rot('RY',t,Q(1))
    def toffoli(self,a,b,t):
        self.H(t); self.cx(b,t); self.pi_rot('RZ',t,-Q(1,4))
        self.cx(a,t); self.pi_rot('RZ',t,Q(1,4)); self.cx(b,t)
        self.pi_rot('RZ',t,-Q(1,4)); self.cx(a,t)
        self.pi_rot('RZ',b,Q(1,4)); self.pi_rot('RZ',t,Q(1,4)); self.H(t)
        self.cx(a,b); self.pi_rot('RZ',a,Q(1,4)); self.pi_rot('RZ',b,-Q(1,4)); self.cx(a,b)
    def mcx(self,controls,t,work):
        k=len(controls)
        if k==0: self.X(t); return
        if k==1: self.cx(controls[0],t); return
        if k==2: self.toffoli(*controls,t); return
        assert len(work)>=k-2
        self.toffoli(controls[0],controls[1],work[0])
        for i in range(2,k-1): self.toffoli(work[i-2],controls[i],work[i-1])
        self.toffoli(work[k-3],controls[k-1],t)
        for i in reversed(range(2,k-1)): self.toffoli(work[i-2],controls[i],work[i-1])
        self.toffoli(controls[0],controls[1],work[0])
    def increment(self,reg,work,control=None,inverse=False,control_value=1):
        if control is not None and control_value==0: self.X(control)
        controls=[] if control is None else [control]
        seq=range(len(reg)) if inverse else reversed(range(len(reg)))
        for i in seq: self.mcx(controls+reg[:i],reg[i],work)
        if control is not None and control_value==0: self.X(control)
    def add_constant(self,reg,k,work):
        for j in range(len(reg)):
            if (k>>j)&1: self.increment(reg[j:],work)
    def multiplexer(self,axis,t,controls,table):
        m=len(table); assert m==1<<len(controls)
        # Exact fast Walsh-Hadamard transform; Gray ordering fixes CNOT order.
        vals=list(table); step=1
        while step<m:
            for base in range(0,m,2*step):
                for j in range(step):
                    a,b=vals[base+j],vals[base+j+step]
                    vals[base+j]=a+b; vals[base+j+step]=a-b
            step*=2
        for i in range(m):
            gray=i^(i>>1); self.rot(axis,t,vals[gray]/m)
            if controls:
                nxt=(i+1)%m; ng=nxt^(nxt>>1); change=gray^ng
                self.cx(controls[change.bit_length()-1],t)
    def prepare_vector(self,register,re,im):
        n=len(register); assert len(re)==1<<n
        weights=[int(a)**2+int(b)**2 for a,b in zip(re,im)]
        assert sum(weights)>0
        for q in reversed(range(n)):
            table=[]; width=1<<q
            for prefix in range(1<<(n-q-1)):
                start=prefix*(2*width)
                p0=sum(weights[start:start+width]); p1=sum(weights[start+width:start+2*width])
                table.append(self.angles.probability(p0,p1))
            self.multiplexer('RY',register[q],register[q+1:],table)
        phases=[self.angles.phase(int(y),int(x)) for x,y in zip(re,im)]
        if any(phases):
            for q in reversed(range(n)):
                table=[]; width=1<<q
                for prefix in range(1<<(n-q-1)):
                    start=prefix*2*width
                    table.append((sum(phases[start+width:start+2*width])-sum(phases[start:start+width]))/width)
                self.multiplexer('RZ',register[q],register[q+1:],table)
        return n
    def counts(self): return dict(Counter(g[0] for g in self.gates))

def unrank_path(N,L,rank):
    assert 0<=rank<multiplicity(N,L)
    path=[0]*(N+1); path[N]=L
    for k in range(N,0,-1):
        cur=path[k]; first=multiplicity(k-1,cur-1)
        if rank<first: path[k-1]=cur-1
        else: rank-=first; path[k-1]=cur+1
    assert path[0]==0 and rank==0
    return path

def uniform_index(m,randbits=secrets.randbits,retries=80):
    if m==1: return 0,False,0
    b=(m-1).bit_length()
    for r in range(retries):
        k=randbits(b)
        if k<m: return k,False,(r+1)*b
    return 0,True,retries*b

def sample_component(blocks,randbits=secrets.randbits,retries=80):
    bits=blocks[0]['probability_bits']; r=randbits(bits); subtotal=0
    for b in blocks:
        subtotal+=b['probability_count']
        if r<subtotal:
            rank,failed,used=uniform_index(b['multiplicity'],randbits,retries)
            return b,rank,failed,bits+used
    raise AssertionError('Bad dyadic probability table')

def emit_component(block,rank=0,angle_bits=48):
    N=block['N']; L=block['L']; d=block['d']; keep=block['keep']
    assert keep==list(range(keep[0],keep[0]+d))
    b=max(1,(N).bit_length()); r=(d-1).bit_length()
    main=list(range(b)); pur=list(range(b,b+r)); work=list(range(b+r,b+r+max(0,b-2)))
    base=b+r+len(work); phys=list(range(base,base+N))
    C=Circuit(base+N,AngleFactory(angle_bits)); size=1<<(2*r)
    re=[0]*size; im=[0]*size
    for i in range(d):
        for j in range(d):
            index=i+(j<<r); re[index]=int(block['A_re'][i,j]); im[index]=int(block['A_im'][i,j])
    prep_n=C.prepare_vector(main[:r]+pur,re,im)
    C.add_constant(main,keep[0],work)
    path=unrank_path(N,L,rank)
    for k in range(N,0,-1):
        prev,cur=path[k-1:k+1]; up=(cur==prev+1); table=[]
        for ell in range(1<<b):
            if ell>cur: table.append(Q(0)); continue
            p0,p1=(prev+1-ell,ell) if up else (ell+1,prev-ell)
            table.append(C.angles.probability(p0,p1,not up))
        C.multiplexer('RY',phys[k-1],main,table)
        if up: C.increment(main,work,phys[k-1],inverse=True)
        else: C.increment(main,work,phys[k-1],control_value=0)
    # Each multiplexer is one ideal controlled rotation; the exact Walsh
    # transform adds no numerical error. Phase reconstruction costs <=2delta
    # up to an irrelevant global phase. Fixed-pi gates are counted separately.
    error=C.angles.max_error*(Q(prep_n+N,2)+2+C.fixed_pi_weight)
    line_CX=sum(1+6*max(0,abs(g[1]-g[2])-1) for g in C.gates if g[0]=='CX')
    meta={'N':N,'L':L,'multiplicity_rank':str(rank),'path':path,'nqubits':C.nqubits,
          'main':main,'purifier':pur,'work':work,'physical':phys,
          'gate_counts':C.counts(),'gates':len(C.gates),'angle_bits':angle_bits,
          'angle_error_bound':str(C.angles.max_error),'logical_trace_error_bound':str(error),
          'fixed_pi_weight':str(C.fixed_pi_weight),'angle_calls':C.angles.calls,
          'line_routing_CX_count':line_CX,
          'line_routing_total_gates':line_CX+sum(g[0]!='CX' for g in C.gates)}
    return C,meta

def simulate(C,initial=None):
    """Binary64 diagnostic only. No claim of a numerical proof."""
    size=1<<C.nqubits
    state=np.zeros(size,complex) if initial is None else initial.copy()
    if initial is None: state[0]=1
    idx=np.arange(size)
    for g in C.gates:
        if g[0]=='CX':
            _,c,t=g; sel=idx[((idx>>c)&1).astype(bool)&~((idx>>t)&1).astype(bool)]
            other=sel^(1<<t); tmp=state[sel].copy(); state[sel]=state[other]; state[other]=tmp
        else:
            axis,t,a=g; angle=float(a); sel=idx[(idx&(1<<t))==0]; other=sel|(1<<t)
            x,y=state[sel].copy(),state[other].copy()
            if axis=='RY':
                co=np.cos(angle/2); si=np.sin(angle/2)
                state[sel]=co*x-si*y; state[other]=si*x+co*y
            else:
                state[sel]=np.exp(-.5j*angle)*x; state[other]=np.exp(.5j*angle)*y
    return state

def cg_isometry(path):
    """Independent small-system recurrence in physical computational order."""
    V=np.ones((1,1),complex)
    for k in range(1,len(path)):
        prev,cur=path[k-1:k+1]; up=cur==prev+1
        W=np.zeros((1<<k,cur+1),complex)
        for ell in range(cur+1):
            if up:
                if ell<=prev: W[:1<<(k-1),ell]+=np.sqrt((prev+1-ell)/(prev+1))*V[:,ell]
                if ell: W[1<<(k-1):,ell]+=np.sqrt(ell/(prev+1))*V[:,ell-1]
            else:
                W[:1<<(k-1),ell]-=np.sqrt((ell+1)/(prev+1))*V[:,ell+1]
                W[1<<(k-1):,ell]+=np.sqrt((prev-ell)/(prev+1))*V[:,ell]
        V=W
    return V
