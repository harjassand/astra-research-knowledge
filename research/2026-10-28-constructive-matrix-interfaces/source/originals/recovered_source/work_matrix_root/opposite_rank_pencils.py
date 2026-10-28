#!/usr/bin/env python3
"""Manufacture bounded-rank moments from an arbitrary operator.

The default backend acquires a finite family of Kronecker pencils closed
under images, counts Hom spaces by field linear algebra, then manufactures
all epimorphism/automorphism counts by exact integer LU. It enumerates no
field points, Hom elements, ambient subspaces, or ambient matrices.
The bit cost is polynomial in a,t for every FIXED maximum_rank, not
uniformly polynomial in that parameter. The old small-variety proposal
and a capped small-field enumerator remain solely as independent audits.
"""
from pathlib import Path
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
import sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent',
    'work_norm_slice_agent','work_ring_count_agent')]
from matrix_kloosterman import (Field,charpoly,factor_polynomial,kernel,rref,
    generalized_jordan,eye,mmul,mtrace,matrix_poly)
from invariant_quadratic_matrix import quadratic_sum,polynomial_value
from primary_rank_moments import gaussian_binomial


@dataclass(frozen=True)
class Pencil:
    u:int
    c:int
    A:tuple
    B:tuple
    label:tuple


def partitions(n,maximum=None):
    if not n:
        yield ();return
    for j in range(min(n,maximum if maximum is not None else n),0,-1):
        for tail in partitions(n-j,j):yield (j,)+tail


def direct_sum(blocks,label):
    u=sum(x[0] for x in blocks);c=sum(x[1] for x in blocks)
    A=[[0]*u for _ in range(c)];B=[[0]*u for _ in range(c)];i=j=0
    for v,w,C,E in blocks:
        for x in range(w):
            for y in range(v):A[i+x][j+y]=C[x][y];B[i+x][j+y]=E[x][y]
        i+=w;j+=v
    return Pencil(u,c,tuple(map(tuple,A)),tuple(map(tuple,B)),label)


def manufactured_types(D,F,r):
    """All possible generated image pencils of domain dimension <= r."""
    factors=[tuple(f) for f,_ in factor_polynomial(charpoly(D,F),F) if len(f)-1<=r]
    regular=[(0,(),[])]
    for f in factors:
        d=len(f)-1;new=[]
        for used,labels,blocks in regular:
            for size in range((r-used)//d+1):
                for shape in partitions(size):
                    if not size:new.append((used,labels,blocks));continue
                    B=generalized_jordan(list(f),shape);v=d*size
                    new.append((used+v,labels+((f,shape),),blocks+[(v,v,eye(v),B)]))
        regular=new
    out=[]
    for used,labels,blocks in regular:
        for left in range(r-used+1):
            for chains in partitions(left):
                parts=list(blocks)
                for k in chains:
                    A=[[int(i==j) for j in range(k)] for i in range(k+1)]
                    B=[[int(i==j+1) for j in range(k)] for i in range(k+1)]
                    parts.append((k,k+1,A,B))
                candidate=direct_sum(parts,(labels,chains))
                if candidate.c<=len(D):out.append(candidate)
    out.sort(key=lambda R:(R.u+R.c,R.u,R.c,repr(R.label)))
    return out


@lru_cache(None)
def hom_basis(R,T,field_h):
    F=Field(field_h);offset=T.u*R.u;n=offset+T.c*R.c;equations=[]
    for C,E in ((R.A,T.A),(R.B,T.B)):
        for i in range(T.c):
            for j in range(R.u):
                row=[0]*n
                for k in range(R.c):row[offset+i*R.c+k]^=C[k][j]
                for k in range(T.u):row[k*R.u+j]^=E[i][k]
                equations.append(row)
    return tuple(map(tuple,kernel(equations,F,n)))


def ambient_pencil(D):
    t=len(D)
    return Pencil(t,t,tuple(map(tuple,eye(t))),tuple(map(tuple,D)),('ambient',))


def canonical_hom_dimension(R,T):
    """Classical block Hom equations, evaluated without field enumeration."""
    regular_R,chains_R=R.label;regular_T,chains_T=T.label
    dimension=sum(max(l-k+1,0) for k in chains_R for l in chains_T)
    target_regular=sum((len(f)-1)*sum(shape) for f,shape in regular_T)
    dimension+=len(chains_R)*target_regular
    for f,shape in regular_R:
        for g,target in regular_T:
            if f==g:dimension+=(len(f)-1)*sum(min(e,h) for e in shape for h in target)
    return dimension


def acquired_ambient_hom_dimensions(D,F,types):
    """Acquire all required small polynomial-kernel dimensions from D."""
    t=len(D);needed={}
    for R in types:
        for f,shape in R.label[0]:needed[f]=max(needed.get(f,0),max(shape))
    nullities={}
    for f,maximum in needed.items():
        evaluation=matrix_poly(list(f),D,F);power=eye(t)
        for e in range(1,maximum+1):
            power=mmul(power,evaluation,F)
            nullities[f,e]=t-len(rref(power,F,t)[1])
    return {R:t*len(R.label[1])+sum(nullities[f,e] for f,shape in R.label[0] for e in shape)
            for R in types}


def _rank_flat(v,rows,cols,F):
    if not rows:return 0
    if F.q==2:
        basis={}
        for i in range(rows):
            row=sum(v[i*cols+j]<<j for j in range(cols))
            while row:
                k=row.bit_length()-1
                if k not in basis:basis[k]=row;break
                row^=basis[k]
        return len(basis)
    return len(rref([v[i*cols:(i+1)*cols] for i in range(rows)],F,cols)[1])


class SmallFieldAuditEpi:
    """EXHAUSTIVE reference on bounded pencils; refuses large Hom spaces."""
    def __init__(self,field_h,maximum_points=1<<20):
        self.F=Field(field_h);self.field_h=field_h;self.maximum_points=maximum_points
        self.cache={};self.calls=0;self.examined_homs=0;self.max_hom_dimension=0

    def __call__(self,R,T):
        if R.u<T.u or R.c<T.c:return 0
        key=(R,T)
        if key in self.cache:return self.cache[key]
        basis=hom_basis(R,T,self.field_h);h=len(basis);F=self.F;N=F.q**h
        if N>self.maximum_points:
            raise ValueError('audit Hom enumeration cap; a point-count backend is required')
        offset=T.u*R.u;width=offset+T.c*R.c;count=0
        for coefficients in product(range(F.q),repeat=h):
            v=[0]*width
            for coefficient,b in zip(coefficients,basis):
                if coefficient:
                    v=[x^F.mul(coefficient,y) for x,y in zip(v,b)]
            if (_rank_flat(v[:offset],T.u,R.u,F)==T.u and
                _rank_flat(v[offset:],T.c,R.c,F)==T.c):count+=1
        self.cache[key]=count;self.calls+=1;self.examined_homs+=N
        self.max_hom_dimension=max(self.max_hom_dimension,h)
        return count


class ManufacturedHomEpi:
    """Integral LU of the manufactured image-closed Hom matrix.

L[R,T] counts kernels in R with quotient T; U[R,T] counts injective
morphisms R->T. Thus U[T,T]=Aut(T), and Epi(R,T)=L[R,T]*U[T,T].
Every division below is an exact INTEGER division.
"""
    def __init__(self,D,field_h,r,types=None):
        begun=time.perf_counter();self.F=Field(field_h);self.field_h=field_h
        self.types=manufactured_types(D,self.F,r) if types is None else list(types)
        self.index={R:i for i,R in enumerate(self.types)}
        N=len(self.types);q=self.F.q
        U=[[q**canonical_hom_dimension(R,T) for T in self.types] for R in self.types]
        L=[[int(i==j) for j in range(N)] for i in range(N)]
        self.maximum_integer_bits=max(1,*(x.bit_length() for row in U for x in row));self.exact_divisions=0
        for j in range(N):
            pivot=U[j][j]
            if pivot<=0:raise AssertionError('nonpositive automorphism pivot')
            for i in range(j+1,N):
                coefficient,remainder=divmod(U[i][j],pivot);self.exact_divisions+=1
                if remainder or coefficient<0:raise AssertionError('nonintegral quotient population')
                L[i][j]=coefficient
                for k in range(j,N):
                    U[i][k]-=coefficient*U[j][k]
                    if U[i][k]<0:raise AssertionError('negative residual image population')
        self.L=L;self.U=U;self.seconds=time.perf_counter()-begun

    def __call__(self,R,T):
        i=self.index[R];j=self.index[T]
        return self.L[i][j]*self.U[j][j]


def epimorphism_variety(R,T,field_h):
    """Explicit quadratic equations for a homomorphism and two sections.

Each equation is a list [coefficient, variable-index monomial]. A zero
degree monomial is the constant. Dividing the number of common zeros by
section_fiber gives Epi(R,T). No inverse or inequality is left implicit.
"""
    if R.u<T.u or R.c<T.c:return dict(impossible=True,epimorphisms=0)
    F=Field(field_h);basis=hom_basis(R,T,field_h);h=len(basis)
    vertices=((R.u,T.u,0),(R.c,T.c,T.u*R.u));variables=h;equations=[]
    free=0
    for source,target,offset in vertices:
        start=variables;variables+=source*target;free+=(source-target)*target
        for i in range(target):
            for j in range(target):
                polynomial={():1} if i==j else {}
                for k in range(source):
                    entry=offset+i*source+k;section=start+k*target+j
                    for ell,b in enumerate(basis):
                        coefficient=b[entry]
                        if coefficient:
                            monomial=(ell,section)
                            polynomial[monomial]=polynomial.get(monomial,0)^coefficient
                equations.append([[coefficient,list(monomial)] for monomial,coefficient in
                    sorted(polynomial.items()) if coefficient])
    return dict(impossible=False,field_polynomial=field_h,variables=variables,
        equations=equations,maximum_total_degree=2,hom_dimension=h,
        section_fiber=F.q**free,section_fiber_exponent=free,
        source_dimensions=[R.u,R.c],target_dimensions=[T.u,T.c])


class VarietyEpi:
    """Adapter for an exact finite-field common-zero counter.

The callback must implement the declared point-count interface. No
claim that the included small-field enumerator is Lauder--Wan is made.
"""
    def __init__(self,field_h,count_common_zeros):
        self.field_h=field_h;self.counter=count_common_zeros;self.cache={}
    def __call__(self,R,T):
        key=(R,T)
        if key not in self.cache:
            system=epimorphism_variety(R,T,self.field_h)
            if system['impossible']:self.cache[key]=0
            else:
                value,remainder=divmod(self.counter(system),system['section_fiber'])
                if remainder:raise AssertionError('section fiber did not divide')
                self.cache[key]=value
        return self.cache[key]


def pencil_gaussian(R,F,beta,eta,phi):
    r=R.u;c=R.c;a=F.a;q=F.q
    def phase(packed):
        L=[[(packed>>(a*(i*c+j)))&(q-1) for j in range(c)] for i in range(r)]
        H=mmul(L,R.A,F);K=mmul(L,R.B,F);e2=0
        for i in range(r):
            for j in range(i):e2^=F.mul(H[i][i],H[j][j])^F.mul(H[i][j],H[j][i])
        z=F.mul(beta,e2)^mtrace(mmul(K,H,F))^F.mul(eta,mtrace(K))
        return F.trace(z)^polynomial_value(phi,mtrace(H))
    return quadratic_sum(phase,a*r*c)


def opposite_moments(D,field_h,beta,phi=(),eta=0,maximum_rank=2,epi_counter=None):
    """Exact C_t,...,C_(t-r), defaulting to manufactured integer LU."""
    begun=time.perf_counter();F=Field(field_h);q=F.q;t=len(D);r=maximum_rank;phi=set(phi)
    if not t or any(len(row)!=t or any(type(x) is not int or not 0<=x<q for x in row) for row in D):
        raise ValueError('nonempty explicit square operator required')
    if type(r) is not int or not 0<=r<=t:raise ValueError('0<=maximum_rank<=t required')
    if not 0<=beta<q or not 0<=eta<q or any(type(x) is not int or x<0 or x.bit_length()>F.a or x.bit_count()>2 for x in phi):
        raise ValueError('field coefficients and an explicit Boolean quadratic are required')
    if epi_counter is None:epi_counter=ManufacturedHomEpi(D,field_h,r)
    types=epi_counter.types if isinstance(epi_counter,ManufacturedHomEpi) else manufactured_types(D,F,r)
    dimensions=acquired_ambient_hom_dimensions(D,F,types);multiplicities={};records=[]
    for R in types:
        h=dimensions[R];injections=q**h
        for T,number in multiplicities.items():
            if T.u+T.c<R.u+R.c and T.u<=R.u and T.c<=R.c:
                injections-=epi_counter(R,T)*number
        aut=epi_counter(R,R)
        number,remainder=divmod(injections,aut)
        if remainder or number<0:raise AssertionError(('image inversion',R.label,injections,aut))
        if R.c>t and number:raise AssertionError('impossible ambient dimension')
        multiplicities[R]=number
        records.append(dict(label=repr(R.label),domain=R.u,codomain=R.c,
            hom_dimension=h,automorphisms=aut,subspaces=number))
    moments=[0]*(r+1)
    for R,number in multiplicities.items():
        if number:
            moments[R.u]+=number*q**(R.u*(t-R.c))*pencil_gaussian(R,F,beta,eta,phi)
    for s in range(r+1):
        if sum(n for R,n in multiplicities.items() if R.u==s)!=gaussian_binomial(t,s,q):
            raise AssertionError('manufactured pencil populations do not partition the Grassmannian')
    layers=[]
    for s,c in enumerate(moments):
        layers.append(c-sum(layers[j]*gaussian_binomial(t-j,s-j,q) for j in range(s)))
    return dict(opposite_kernel_moments=moments,signed_rank_layers=layers,
        matrix_size=t,field_degree=F.a,maximum_rank=r,manufactured_pencil_types=records,
        enumerated_ambient_subspaces=0,enumerated_ambient_matrices=0,
        small_backend=type(epi_counter).__name__,uniform_polynomial_in_rank=False,
        polynomial_for_fixed_rank=isinstance(epi_counter,ManufacturedHomEpi),
        enumerated_field_elements=0 if isinstance(epi_counter,ManufacturedHomEpi) else None,
        hom_table_statistics=dict(types=len(types),integer_lu=True,
            maximum_integer_bits=epi_counter.maximum_integer_bits,
            exact_divisions=epi_counter.exact_divisions,seconds=epi_counter.seconds)
            if isinstance(epi_counter,ManufacturedHomEpi) else None,
        seconds=time.perf_counter()-begun)


def rank_restricted_cubic_count(result,padding=None):
    """Original-bit count for rank(X)<=r AND the matrix cubic has value 1."""
    t=result['matrix_size'];a=result['field_degree'];q=1<<a
    T=t if padding is None else padding
    if type(T) is not int or T<0:raise ValueError('nonnegative explicit padding required')
    ranks=[]
    for j in range(result['maximum_rank']+1):
        numerator=1;denominator=1
        for i in range(j):numerator*=(q**t-q**i)**2;denominator*=q**j-q**i
        count,remainder=divmod(numerator,denominator)
        if remainder:raise AssertionError('rank population division')
        ranks.append(count)
    domain=sum(ranks)*q**(2*t*T)
    gap=sum(b*q**(2*t*T-T*j) for j,b in enumerate(result['signed_rank_layers']))
    return dict(satisfying_count=(domain-gap)//2,restricted_domain_size=domain,gap=gap,
        original_independent_bits=a*(t*t+2*t*T),rank_cap=result['maximum_rank'],padding=T)
