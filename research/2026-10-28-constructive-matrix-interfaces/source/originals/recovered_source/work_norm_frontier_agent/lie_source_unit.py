#!/usr/bin/env python3
"""Intrinsic unit recovery for beta!=0, affine-trace matrix square sources.

Uses left/right infinitesimal polar stabilizers, a commutant, and either a
linear envelope lift (regular nilpotent) or two Frobenius intertwiners
(irreducible operator). No matrix units or simple module are required.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
from raw_matrix_trace import solve as binary_solve, linear_apply, bits
from matrix_kloosterman import Field,rref,kernel,minverse


def xor(values):
    result=0
    for value in values:result^=value
    return result


def independent(rows,F,width):
    R,pivots=rref(rows,F,width)
    return R[:len(pivots)]


def field_solve(rows,target,F,width):
    R,pivots=rref([list(row)+[value] for row,value in zip(rows,target)],F,width)
    if any(not any(row[:width]) and row[width] for row in R):return None,len(pivots)
    out=[0]*width
    for i,p in enumerate(pivots):out[p]=R[i][width]
    return out,len(pivots)


def relations(columns,F):
    if not columns:return []
    return kernel(list(map(list,zip(*columns))),F,len(columns))


class Intrinsic:
    def __init__(self,algebra):
        self.A=algebra;self.F=algebra.F;self.t=algebra.t;self.m=algebra.D
        self.basis=algebra.field_module_basis;self.one=algebra.one
        self.mul=algebra.mul
        self.cache={};self.trace_coefficients=None
    def coordinates(self,x):
        if x not in self.cache:
            v=binary_solve(self.A.field_columns,x)
            if v is None:raise AssertionError('field-coordinate acquisition')
            self.cache[x]=[(v>>(self.F.a*i))&(self.F.q-1) for i in range(self.m)]
        return self.cache[x]
    def pack(self,v):
        return linear_apply(self.A.field_columns,sum(x<<(self.F.a*i) for i,x in enumerate(v)))
    def trace(self,x):
        # Reduced trace is F-linear. Manufacture its basis coefficients once,
        # rather than recomputing a reduced characteristic polynomial at
        # every sandwich-envelope evaluation.
        if self.trace_coefficients is None:
            self.trace_coefficients=[self.A.relative_trace(e) for e in self.basis]
        return xor(self.F.mul(c,t) for c,t in zip(self.coordinates(x),self.trace_coefficients))
    def inv(self,x):
        result=binary_solve(self.A.left_matrix(x),self.one)
        if result is None:raise ValueError('nonunit')
        return result
    def is_unit(self,x):return self.A.is_unit(x)


class Explicit:
    """Only the test adapter supplies split matrix coordinates."""
    def __init__(self,t,h):
        self.F=Field(h);self.t=t;self.m=t*t;a=self.F.a
        self.basis=[1<<(a*i) for i in range(self.m)]
        self.one=sum(1<<(a*(i*t+i)) for i in range(t))
    def coordinates(self,x):return [(x>>(self.F.a*i))&(self.F.q-1) for i in range(self.m)]
    def pack(self,v):return sum(x<<(self.F.a*i) for i,x in enumerate(v))
    def mul(self,x,y):
        x=self.coordinates(x);y=self.coordinates(y);t=self.t;F=self.F
        return self.pack([xor(F.mul(x[i*t+k],y[k*t+j]) for k in range(t)) for i in range(t) for j in range(t)])
    def trace(self,x):
        v=self.coordinates(x);return xor(v[i*self.t+i] for i in range(self.t))
    def inv(self,x):
        v=self.coordinates(x);answer=minverse([v[i*self.t:(i+1)*self.t] for i in range(self.t)],self.F)
        if answer is None:raise ValueError('nonunit')
        return self.pack(sum(answer,[]))
    def is_unit(self,x):
        try:self.inv(x);return True
        except ValueError:return False


def scale(A,c,x):return A.pack([A.F.mul(c,v) for v in A.coordinates(x)])
def combination(A,coefficients,basis):return xor(scale(A,c,x) for c,x in zip(coefficients,basis))
def power(A,x,n):
    out=A.one
    while n:
        if n&1:out=A.mul(out,x)
        x=A.mul(x,x);n>>=1
    return out


def polar_stabilizer(A,P):
    columns=[];px=[P(x) for x in A.basis]
    for a in A.basis:
        columns.append(sum((A.coordinates(P(A.mul(a,x))^A.mul(y,a)) for x,y in zip(A.basis,px)),[]))
    for b in A.basis:
        columns.append(sum((A.coordinates(P(A.mul(x,b))^A.mul(b,y)) for x,y in zip(A.basis,px)),[]))
    return [(A.pack(v[:A.m]),A.pack(v[A.m:])) for v in relations(columns,A.F)]


def intertwiner_space(A,pairs):
    columns=[]
    for z in A.basis:
        columns.append(sum((A.coordinates(A.mul(b,z)^A.mul(z,a)) for a,b in pairs),[]))
    return [A.pack(v) for v in relations(columns,A.F)]


def reshuffle(A,P):
    columns=[];a=A.F.a
    for l in A.basis:
        for r in A.basis:
            vector=sum((A.coordinates(A.mul(l,A.mul(x,r))) for x in A.basis),[])
            for bit in range(a):
                columns.append(sum(A.F.mul(1<<bit,value)<<(a*i) for i,value in enumerate(vector)))
    vector=sum((A.coordinates(P(x)) for x in A.basis),[])
    target=sum(value<<(a*i) for i,value in enumerate(vector))
    packed=binary_solve(columns,target)
    if packed is None:raise AssertionError('central simple envelope is not faithful')
    coefficients=[(packed>>(a*i))&(A.F.q-1) for i in range(A.m*A.m)]
    M=[coefficients[i*A.m:(i+1)*A.m] for i in range(A.m)]
    def S(x):
        traces=[A.trace(A.mul(e,x)) for e in A.basis]
        return A.pack([xor(A.F.mul(v,w) for v,w in zip(row,traces)) for row in M])
    return S


def nilpotent_commutative_hyperplane(A,normalizer):
    n=len(normalizer);brackets=[[A.coordinates(A.mul(x,y)^A.mul(y,x)) for y in normalizer] for x in normalizer]
    kernel_rows=[];nonzero=0
    for coordinate in range(A.m):
        M=[[brackets[i][j][coordinate] for j in range(n)] for i in range(n)]
        rank=len(rref(M,A.F,n)[1])
        if rank:
            if rank!=2:raise ValueError('normalizer bracket does not have the regular-chain pencil form')
            nonzero+=1;kernel_rows.extend(kernel(M,A.F,n))
    line=kernel(kernel_rows,A.F,n)
    if len(line)!=1 or not nonzero:raise ValueError('no unique commutative normalizer hyperplane')
    return [combination(A,v,normalizer) for v in kernel(line,A.F,n)]


def lift_nilpotent_sandwich(A,S,R,E):
    annihilator=kernel([A.coordinates(e) for e in E],A.F,A.m)
    columns=[]
    for l in R:
        for r in R:
            col=[]
            for x in A.basis:
                value=A.coordinates(A.mul(l,A.mul(x,r)))
                col.extend(xor(A.F.mul(v,w) for v,w in zip(ell,value)) for ell in annihilator)
            columns.append(col)
    target=[]
    for x in A.basis:
        value=A.coordinates(S(x))
        target.extend(xor(A.F.mul(v,w) for v,w in zip(ell,value)) for ell in annihilator)
    coefficients,rank=field_solve(list(map(list,zip(*columns))),target,A.F,len(R)**2)
    if coefficients is None or rank!=len(R)**2:raise ValueError('sandwich lift is not unique')
    matrix=[coefficients[i*len(R):(i+1)*len(R)] for i in range(len(R))]
    rows,pivots=rref(matrix,A.F,len(R))
    if len(pivots)!=1:raise ValueError('lifted sandwich tensor does not have rank one')
    if any(matrix[i][j]!=matrix[j][i] for i in range(len(R)) for j in range(len(R))):
        raise ValueError('lifted sandwich tensor is not symmetric')
    return combination(A,rows[0],R),dict(sandwich_lift_variables=len(R)**2,
        sandwich_lift_rank=rank,sandwich_coefficient_rank=1)


def lift_field_sandwich(A,S,E):
    values=[]
    for j in (1,2):
        pairs=[(e,power(A,e,A.F.q**j)) for e in E]
        space=intertwiner_space(A,pairs)
        if len(space)!=A.t:raise ValueError('Frobenius intertwiner has the wrong dimension')
        x=next((v for v in space if A.is_unit(v)),None)
        if x is None:raise ValueError('Frobenius intertwiner has no displayed unit')
        values.append(A.mul(S(x),A.inv(x)))
    r1,r2=values
    square=A.mul(A.mul(r1,r2),A.inv(power(A,r1,A.F.q)))
    h=power(A,square,1<<(A.F.a*A.t-1))
    if A.mul(h,h)!=square:raise ValueError('acquired commutant is not the required field')
    return h,dict(frobenius_intertwiner_dimensions=[A.t,A.t],
                  square_root_binary_degree=A.F.a*A.t)


def recover_source_unit(A,P):
    """Return a scalar multiple of W; callers must verify the full source fit.

    Completeness: t>=4, beta!=0, and either D is cyclic with one primary
    factor of even exponent, or D has irreducible degree t. The first
    case includes every full even Jordan chain. Only the polar map P and
    the algebra are supplied. Odd nilpotent sources use the separate
    scalar-radical acquisition route. The even-primary extension is proved
    in CYCLIC_QUADRATIC_PRIMARY_INDEPENDENT_AUDIT.tex, Section 6.
    """
    if A.t<4:raise ValueError('Lie unit route requires matrix size at least four')
    stabilizer=polar_stabilizer(A,P)
    normalizer=[A.pack(v) for v in independent([A.coordinates(b) for a,b in stabilizer],A.F,A.m)]
    frobenius_pairs=[(power(A,a,A.F.q)^a,power(A,b,A.F.q)^b) for a,b in stabilizer]
    units=intertwiner_space(A,frobenius_pairs)
    v=next((x for x in units if A.is_unit(x)),None)
    if v is None:raise ValueError('no displayed unit in the manufactured intertwiner space')
    vinv=A.inv(v)
    R=[A.mul(x,vinv) for x in units]
    normalized=lambda x:A.mul(P(A.mul(vinv,x)),vinv)
    S=reshuffle(A,normalized)
    evidence=dict(stabilizer_dimension=len(stabilizer),right_normalizer_dimension=len(normalizer),
        unit_intertwiner_dimension=len(units),matrix_size=A.t,field_degree=A.F.a,
        supplied_matrix_units=False,supplied_source_unit=False)
    if len(normalizer)==A.t+1 and len(R)==A.t//2 and A.t%2==0:
        E=nilpotent_commutative_hyperplane(A,normalizer)
        if len(E)!=A.t:raise ValueError('regular-chain commutative hyperplane has wrong dimension')
        h,more=lift_nilpotent_sandwich(A,S,R,E);evidence.update(more)
        evidence['route']='Lie normalizer and unique linear sandwich lift'
    elif len(normalizer)==A.t and len(R)==A.t:
        h,more=lift_field_sandwich(A,S,R);evidence.update(more)
        evidence['route']='Lie commutant and two Frobenius sandwich products'
    else:raise ValueError('polar normalizer is outside the admitted operator types')
    w=A.mul(h,v)
    if not A.is_unit(w):raise ValueError('reconstructed source unit is singular')
    return w,evidence


def recover_from_raw_source(poly,algebra):
    d=algebra.d;polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    columns=[binary_solve(algebra.gram,v) for v in polar]
    P=lambda x:linear_apply(columns,x)
    A=Intrinsic(algebra)
    # The tensor construction requires linearity over the acquired center.
    for e in A.basis:
        for bit in range(A.F.a):
            if P(scale(A,1<<bit,e))!=scale(A,1<<bit,P(e)):
                raise ValueError('source polar is not linear over the acquired center')
    return recover_source_unit(A,P)


def count_lie_source(poly,algebra):
    """Certified source fit and existing exact backend after unit recovery."""
    from operator_quadratic_counter import acquire_operator_linear_refinement,count_acquired_cyclic_refinement
    unit,evidence=recover_from_raw_source(poly,algebra)
    inverse_unit=binary_solve(algebra.left_matrix(unit),algebra.one)
    beta,D,phi,eta,fit=acquire_operator_linear_refinement(poly,algebra,inverse_unit)
    if not beta:raise ValueError('Lie source route requires a nonzero e2 coefficient')
    gap,backend=count_acquired_cyclic_refinement(algebra,beta,D,phi,eta)
    fit.update(evidence);fit['unit_acquisition_route']=evidence['route']
    return gap,backend,fit
