#!/usr/bin/env python3
"""Intrinsic unit acquisition for cyclic primary operators of odd exponent.

The input is a certified matrix algebra and its trace-dual source polar.
No matrix units, coefficient field, source matrix, or source unit are supplied.
The newly covered case has residue degree >=2 and odd exponent >=3.
The full ANF/source-type check remains a mandatory caller responsibility.
"""
from lie_source_unit import *
from matrix_kloosterman import factor_polynomial


def coordinates_in(A,basis,x):
    columns=[A.coordinates(v) for v in basis]
    result,rank=field_solve(list(map(list,zip(*columns))),A.coordinates(x),A.F,len(basis))
    if result is None or rank!=len(basis):raise ValueError('element outside the acquired independent space')
    return result


def binary_column_rank(columns):
    rows={}
    for value in columns:
        while value:
            p=value.bit_length()-1
            if p not in rows:rows[p]=value;break
            value^=rows[p]
    return len(rows)


def refine_quadratic_intertwiners(A,stabilizer,U):
    """Remove the two singular socle directions in residue degree two."""
    n=len(U);identity=[int(i==j) for i in range(n) for j in range(n)]
    for left,right in stabilizer:
        cols=[coordinates_in(A,U,A.mul(right,x)^A.mul(x,left)) for x in U]
        T=[list(row) for row in zip(*cols)]
        flat=sum(T,[])
        if field_solve(list(map(list,zip(identity))),flat,A.F,1)[0] is not None:continue
        square=[[xor(A.F.mul(T[i][k],T[k][j]) for k in range(n)) for j in range(n)] for i in range(n)]
        relation,rank=field_solve(list(map(list,zip(identity,flat))),sum(square,[]),A.F,2)
        if relation is None or rank!=2:raise ValueError('projective stabilizer action is not quadratic')
        roots=[]
        for f,multiplicity in factor_polynomial([relation[0],relation[1],1],A.F):
            if len(f)!=2 or multiplicity!=1:raise ValueError('projective stabilizer action does not split simply')
            roots.append(A.F.mul(f[0],A.F.inv(f[1])))
        if len(roots)!=2:raise ValueError('two scalar-shift roots required')
        for root in roots:
            M=[[T[i][j]^(root if i==j else 0) for j in range(n)] for i in range(n)]
            space=kernel(M,A.F,n)
            if len(space)==A.t:
                return [combination(A,v,U) for v in space],dict(
                    refinement_eigenvalues=roots,refinement_eigenspace_dimension=A.t)
        raise ValueError('no expected dominant projective-stabilizer eigenspace')
    raise ValueError('no nonscalar projective-stabilizer action was acquired')


class CoefficientField:
    """An acquired subfield, represented by coordinates in its displayed basis."""
    def __init__(self,A,basis):
        self.A=A;self.F=A.F;self.basis=basis;self.degree=len(basis)
        self.a=A.F.a*self.degree;self.q=1<<self.a
        if basis[0]!=A.one:raise ValueError('coefficient field must start with its identity')
        self.columns=[scale(A,1<<b,x) for x in basis for b in range(A.F.a)]
        self.structure=[[self.coordinates(A.mul(x,y)) for y in basis] for x in basis]
    def coordinates(self,x):
        result=binary_solve(self.columns,x)
        if result is None:raise ValueError('not in acquired coefficient field')
        return result
    def embed(self,x):return linear_apply(self.columns,x)
    def mul(self,x,y):
        F=self.F;a=F.a;out=0
        for i in range(self.degree):
            u=(x>>(a*i))&(F.q-1)
            if not u:continue
            for j in range(self.degree):
                v=(y>>(a*j))&(F.q-1)
                if not v:continue
                c=F.mul(u,v);w=self.structure[i][j]
                out^=sum(F.mul(c,(w>>(a*k))&(F.q-1))<<(a*k) for k in range(self.degree))
        return out
    def pow(self,x,n):
        out=1
        while n:
            if n&1:out=self.mul(out,x)
            x=self.mul(x,x);n>>=1
        return out
    def inv(self,x):
        if not x:raise ZeroDivisionError
        return self.pow(x,self.q-2)


def acquire_coefficient_field(A,E):
    """Frobenius kills the nilradical and manufactures the unique residue field."""
    exponent=1
    while exponent<A.t:exponent*=A.F.q
    image=[power(A,e,exponent) for e in E]
    Kbasis=[A.one]
    for x in image:
        trial=[A.coordinates(v) for v in Kbasis+[x]]
        if len(independent(trial,A.F,A.m))>len(Kbasis):Kbasis.append(x)
    K=CoefficientField(A,Kbasis);R=[];span=[]
    for x in E:
        new=[A.mul(k,x) for k in Kbasis]
        rank=len(independent([A.coordinates(v) for v in span+new],A.F,A.m))
        if rank==len(span):continue
        if rank!=len(span)+K.degree:raise ValueError('acquired coefficient ring is not a field')
        R.append(x);span+=new
    if len(span)!=A.t:raise ValueError('primary algebra is not free over acquired coefficient field')
    return K,R,dict(coefficient_field_degree=K.degree,primary_exponent=len(R),
                    coefficient_field_frobenius_exponent=exponent)


def restricted_sandwich_coefficients(A,S,K,R,domain):
    """Acquire the unique E-by-E envelope on a nontrivial semilinear component."""
    a=A.F.a;columns=[]
    for left in R:
        for right in R:
            values=[A.mul(left,A.mul(x,right)) for x in domain]
            for scalar in K.basis:
                vector=sum((A.coordinates(A.mul(scalar,v)) for v in values),[])
                for bit in range(a):
                    columns.append(sum(A.F.mul(1<<bit,v)<<(a*i) for i,v in enumerate(vector)))
    vector=sum((A.coordinates(S(x)) for x in domain),[])
    target=sum(v<<(a*i) for i,v in enumerate(vector))
    rank=binary_column_rank(columns)
    if rank!=len(columns):raise ValueError('restricted primary envelope is not faithful')
    result=binary_solve(columns,target)
    if result is None:raise ValueError('source restriction is outside the primary sandwich envelope')
    e=len(R);ka=K.a
    C=[[(result>>(ka*(i*e+j)))&(K.q-1) for j in range(e)] for i in range(e)]
    rows,pivots=rref(C,K,e)
    if len(pivots)!=1:raise ValueError('acquired semilinear sandwich tensor is not rank one')
    column=next(j for j in range(e) if any(C[i][j] for i in range(e)))
    H0=xor(A.mul(K.embed(C[i][column]),R[i]) for i in range(e))
    if not A.is_unit(H0):raise ValueError('rank-one sandwich column does not give a unit')
    return H0,dict(restricted_envelope_binary_rank=rank,semilinear_sandwich_rank=1)


def recover_primary_source_unit(A,P):
    """Recover a scalar multiple of W for odd e>=3, residue degree d>=2."""
    if A.t<6:raise ValueError('new odd-primary route requires size at least six')
    stabilizer=polar_stabilizer(A,P)
    E=[A.pack(v) for v in independent([A.coordinates(b) for a,b in stabilizer],A.F,A.m)]
    if len(E)!=A.t or any(A.mul(x,y)!=A.mul(y,x) for x in E for y in E):
        raise ValueError('right polar normalizer is not the expected commutative primary algebra')
    K,R,meta=acquire_coefficient_field(A,E);d=K.degree;e=len(R)
    if d<2 or e<3 or not e%2:raise ValueError('outside the odd nontrivial primary source route')
    pairs=[(power(A,a,A.F.q)^a,power(A,b,A.F.q)^b) for a,b in stabilizer]
    U=intertwiner_space(A,pairs)
    evidence=dict(stabilizer_dimension=len(stabilizer),right_normalizer_dimension=len(E),
        initial_unit_intertwiner_dimension=len(U),matrix_size=A.t,field_degree=A.F.a,
        supplied_matrix_units=False,supplied_source_unit=False,**meta)
    if len(U)!=A.t:
        if d!=2 or len(U)!=A.t+2:raise ValueError('unexpected primary intertwiner defect')
        U,extra=refine_quadratic_intertwiners(A,stabilizer,U);evidence.update(extra)
    V=next((x for x in U if A.is_unit(x)),None)
    if V is None:raise ValueError('manufactured local-ring coset has no displayed unit')
    Vinv=A.inv(V)
    normalized=lambda x:A.mul(P(A.mul(Vinv,x)),Vinv)
    S=reshuffle(A,normalized)
    semilinear=intertwiner_space(A,[(x,power(A,x,A.F.q)) for x in K.basis])
    diagonal=intertwiner_space(A,[(x,x) for x in K.basis])
    expected=d*e*e
    if len(semilinear)!=expected or len(diagonal)!=expected:raise ValueError('coefficient-field components have wrong dimensions')
    H0,extra=restricted_sandwich_coefficients(A,S,K,R,semilinear);evidence.update(extra)
    annihilator=kernel([A.coordinates(x) for x in E],A.F,A.m)
    def projected(x):
        values=A.coordinates(x)
        return [xor(A.F.mul(v,w) for v,w in zip(row,values)) for row in annihilator]
    target=sum((projected(S(x)) for x in diagonal),[])
    columns=[sum((projected(A.mul(k,A.mul(H0,A.mul(x,H0)))) for x in diagonal),[]) for k in K.basis]
    gamma,rank=field_solve(list(map(list,zip(*columns))),target,A.F,d)
    if gamma is None or rank!=d:raise ValueError('diagonal sandwich scale was not uniquely acquired')
    packed=sum(c<<(A.F.a*i) for i,c in enumerate(gamma))
    if not packed:raise ValueError('zero sandwich scale')
    scalar=K.pow(packed,1<<(K.a-1))
    H=A.mul(K.embed(scalar),H0);W=A.mul(H,V)
    if not A.is_unit(W):raise ValueError('manufactured primary source unit is singular')
    evidence.update(route='odd-primary Lie algebra, coefficient-field semilinear tensor, and quotient scale',
        semilinear_component_dimension=expected,diagonal_scale_rank=rank,
        unit_intertwiner_dimension=len(U))
    return W,evidence


def recover_from_raw_primary_source(poly,algebra):
    d=algebra.d;polar=[0]*d
    for monomial in poly:
        if monomial.bit_count()==2:
            i,j=bits(monomial);polar[i]^=1<<j;polar[j]^=1<<i
    columns=[binary_solve(algebra.gram,v) for v in polar]
    P=lambda x:linear_apply(columns,x);A=Intrinsic(algebra)
    for e in A.basis:
        for bit in range(A.F.a):
            if P(scale(A,1<<bit,e))!=scale(A,1<<bit,P(e)):
                raise ValueError('source polar is not linear over the acquired center')
    return recover_primary_source_unit(A,P)
