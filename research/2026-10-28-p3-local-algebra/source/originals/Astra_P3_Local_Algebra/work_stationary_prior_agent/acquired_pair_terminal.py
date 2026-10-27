#!/usr/bin/env python3
"""Acquire a two-type repeated-pair residue; finite Gaussian-state terminal.

The acquisition is polynomial and performs no field enumeration.  The
reference terminal explicitly enumerates q field values.  The separate
moment interfaces accept eight exact point-count moments (or 49 as an
independent reference); the proof explains
why fixed-variable point counting gives a polynomial-in-d theorem.
"""
from homogeneous_chain_counter import *
from field_descent import span
from fractions import Fraction
import itertools


def xor_all(xs):
    result=0
    for x in xs:result^=x
    return result


def matrix_product(A,B,h):
    return [[xor_all(gf_mul(a,b,h) for a,b in zip(row,col)) for col in zip(*B)] for row in A]


def transpose(A):return [list(x) for x in zip(*A)]


def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]


def matrix_inverse(A,h):
    n=len(A); q=1<<(h.bit_length()-1)
    rows=[list(row)+unit for row,unit in zip(A,identity(n))]
    for j in range(n):
        p=next((i for i in range(j,n) if rows[i][j]),None)
        if p is None:raise ValueError('singular field matrix')
        rows[j],rows[p]=rows[p],rows[j]
        c=gf_pow(rows[j][j],q-2,h);rows[j]=[gf_mul(c,x,h) for x in rows[j]]
        for i in range(n):
            if i!=j and rows[i][j]:
                c=rows[i][j];rows[i]=[x^gf_mul(c,y,h) for x,y in zip(rows[i],rows[j])]
    return [row[n:] for row in rows]


def vector_apply(A,v,h):return [xor_all(gf_mul(a,x,h) for a,x in zip(row,v)) for row in A]


def add_coefficient(P,a,c):
    P[a]=P.get(a,0)^c
    if not P[a]:del P[a]


def exponent(b,indices):
    out=[0]*b
    for i in indices:out[i]+=1
    return tuple(out)


def polynomial_multiply(P,Q,h):
    out={}
    for a,c in P.items():
        for b,d in Q.items():add_coefficient(out,tuple(x+y for x,y in zip(a,b)),gf_mul(c,d,h))
    return out


def substitute(P,B,h):
    """B has old coordinates as rows, new coordinates as columns."""
    b=len(B);out={}
    linears=[{exponent(b,[j]):c for j,c in enumerate(row) if c} for row in B]
    for a,c in P.items():
        term={(0,)*b:c}
        for i,power in enumerate(a):
            for _ in range(power):term=polynomial_multiply(term,linears[i],h)
        for v,w in term.items():add_coefficient(out,v,w)
    return out


def field_kernel(columns,h):
    d=h.bit_length()-1;rows=len(columns[0]) if columns else 0
    binary=[sum(gf_mul(1<<j,c,h)<<(d*i) for i,c in enumerate(col))
        for col in columns for j in range(d)]
    basis=kernel_columns(binary)
    return [[(a>>(d*i))&((1<<d)-1) for i in range(len(columns))] for a in basis]


def acquire_chart(h,P):
    b=len(next(iter(P)));d=h.bit_length()-1;q=1<<d;m=b-1
    if b<5 or b%2!=1:raise ValueError('requires odd b>=5')
    T={a:P.get(exponent(b,a),0) for a in itertools.combinations(range(b),3)}
    fours=list(itertools.combinations(range(b),4))
    wedge_columns=[[T[tuple(j for j in a if j!=i)] if i in a else 0 for a in fours] for i in range(b)]
    kernel=field_kernel(wedge_columns,h)
    if len(kernel)!=d:raise ValueError('contact factor is not a unique field line')
    ell=kernel[0]
    pivot=next(i for i,x in enumerate(ell) if x);inverse=gf_pow(ell[pivot],q-2,h)
    ell=[gf_mul(inverse,x,h) for x in ell]
    vectors=[]
    for i in range(b):
        if i==pivot:continue
        v=[0]*b;v[i]=1;v[pivot]=ell[i];vectors.append(v)
    v=[0]*b;v[pivot]=1;vectors.append(v)
    chart=transpose(vectors);Pchart=substitute(P,chart,h)
    Omega=[[Pchart.get(exponent(b,[i,j,m]),0) if i!=j else 0 for j in range(m)] for i in range(m)]
    matrix_inverse(Omega,h)
    if any(c for a,c in Pchart.items() if sum(int(x==1) for x in a)==3 and a[m]==0):
        raise ValueError('residue third form does not factor through the acquired line')
    M=[[Pchart.get(exponent(b,[j,j,i]),0) for j in range(m)] for i in range(m)]
    constants=[Pchart.get(exponent(b,[i,m,m]),0) for i in range(m)]
    def gradient(v):
        square=[gf_mul(x,x,h) for x in v]
        a=vector_apply(M,square,h);c=vector_apply(Omega,v,h)
        return [x^y for x,y in zip(a,c)]
    columns=[]
    for i in range(m):
        for j in range(d):
            v=[0]*m;v[i]=1<<j
            columns.append(sum(c<<(d*k) for k,c in enumerate(gradient(v))))
    target=sum(c<<(d*i) for i,c in enumerate(constants))
    solution=Solver(columns)(target)
    if solution is None or kernel_columns(columns):raise ValueError('chart gradient does not have one affine root')
    point=[(solution>>(d*i))&(q-1) for i in range(m)]
    R=ChainRing(h,1)
    critical_value=ring_polynomial(R,Pchart,point+[1])
    shift=identity(b)
    for i,x in enumerate(point):shift[i][m]=x
    Pcenter=substitute(Pchart,shift,h)
    if Pcenter.get(exponent(b,[m,m,m]),0)!=critical_value or any(Pcenter.get(exponent(b,[i,m,m]),0) for i in range(m)):
        raise AssertionError('critical centering failed')
    return Pcenter,M,Omega,matrix_product(chart,shift,h),dict(line=ell,critical_point_in_chart=point,
        affine_critical_value=critical_value)


def acquire_pair_template(h,P):
    d=h.bit_length()-1;q=1<<d
    if d%3==0:raise ValueError('this certificate requires 3 not dividing d')
    centered,M,Omega,chart,geometry=acquire_chart(h,P)
    m=len(M);b=m+1;A=matrix_product(matrix_inverse(Omega,h),M,h)
    K=identity(m)
    for _ in range(d):K=matrix_product(A,[[gf_mul(x,x,h) for x in row] for row in K],h)
    K2=matrix_product(K,K,h)
    if any(K2[i][j]^K[i][j]^int(i==j) for i in range(m) for j in range(m)):
        raise ValueError('semilinear norm does not have the order-three polynomial')
    D=K if d%3==1 else K2
    F=matrix_product(matrix_inverse(D,h),A,h)
    binary_columns=[]
    for i in range(m):
        for j in range(d):
            v=[0]*m;v[i]=gf_mul(1<<j,1<<j,h)
            column=sum(c<<(d*k) for k,c in enumerate(vector_apply(F,v,h)))^(1<<(d*i+j))
            binary_columns.append(column)
    fixed=kernel_columns(binary_columns)
    if len(fixed)!=m:raise ValueError('semilinear fixed space has incorrect binary dimension')
    U=transpose([[(a>>(d*i))&(q-1) for i in range(m)] for a in fixed])
    Uinv=matrix_inverse(U,h)
    omega_u=matrix_product(matrix_product(transpose(U),Omega,h),U,h)
    gamma=next((c for row in omega_u for c in row if c),0)
    if not gamma or any(c not in (0,gamma) for row in omega_u for c in row):
        raise ValueError('symplectic form does not descend to one binary scalar')
    omega_bin=[[int(c==gamma) for c in row] for row in omega_u]
    D_u=matrix_product(matrix_product(Uinv,D,h),U,h)
    if any(c not in (0,1) for row in D_u for c in row):raise AssertionError('D did not preserve the fixed space')
    if matrix_product(matrix_product(transpose(D_u),omega_bin,h),D_u,h)!=omega_bin:
        raise ValueError('order-three map does not preserve the descended symplectic form')
    omega_rows=[sum(c<<i for i,c in enumerate(row)) for row in omega_bin]
    D_columns=[sum(c<<i for i,c in enumerate(col)) for col in zip(*D_u)]
    def omega(x,y):
        return xor_all((omega_rows[i]&y).bit_count()&1 for i in range(m) if (x>>i)&1)
    basis=[1<<i for i in range(m)];pairs=[]
    while basis:
        v=next((x for x in basis if omega(x,linear_apply(D_columns,x))),None)
        if v is None:
            v=next(x^y for x,y in itertools.combinations(basis,2)
                   if omega(x^y,linear_apply(D_columns,x^y)))
        w=linear_apply(D_columns,v);pairs.extend([v,w])
        residual=[]
        for x in basis:
            y=x^(v if omega(x,w) else 0)^(w if omega(x,v) else 0)
            if Solver(residual)(y) is None:residual.append(y)
        basis=residual
    B=matrix_product(U,transpose([[((x>>i)&1) for i in range(m)] for x in pairs]),h)
    full=identity(b)
    for i in range(m):
        for j in range(m):full[i][j]=B[i][j]
    normal=substitute(centered,full,h)
    inverse_gamma=gf_pow(gamma,q-2,h);types=[];expected={}
    tau=normal.get(exponent(b,[m,m,m]),0)
    if tau:add_coefficient(expected,exponent(b,[m,m,m]),tau)
    for i in range(0,m,2):
        for indices in [(i,i,i),(i,i+1,i+1),(i+1,i+1,i+1),(i,i+1,m)]:
            add_coefficient(expected,exponent(b,indices),gamma)
        a=gf_mul(normal.get(exponent(b,[i,i,m]),0),inverse_gamma,h)
        c=gf_mul(normal.get(exponent(b,[i+1,i+1,m]),0),inverse_gamma,h)
        if a not in (0,1) or c not in (0,1):raise ValueError('quadratic square coefficients do not descend to F2')
        if a:add_coefficient(expected,exponent(b,[i,i,m]),gamma)
        if c:add_coefficient(expected,exponent(b,[i+1,i+1,m]),gamma)
        types.append([a,c])
    if normal!=expected:raise AssertionError('manufactured pair-template identity failed')
    return dict(field_modulus=h,field_degree=d,ring_variables=b,gamma=gamma,radial_cubic=tau,
        positive_pairs=sum(x!=[1,1] for x in types),negative_pairs=types.count([1,1]),
        pair_square_types=types,coordinate_matrix=matrix_product(chart,full,h),
        normalized_polynomial=[dict(exponents=a,coefficient=c) for a,c in normal.items()],
        field_elements_enumerated_during_acquisition=0,**geometry)


def pair_phase(h,gamma,z,negative,packed):
    d=h.bit_length()-1;mask=(1<<d)-1;x=packed&mask;y=packed>>d
    x2=gf_mul(x,x,h);y2=gf_mul(y,y,h)
    value=gf_mul(x2,x,h)^gf_mul(x,y2,h)^gf_mul(y2,y,h)^gf_mul(z,gf_mul(x,y,h),h)
    if negative:value^=gf_mul(z,x2^y2,h)
    return gf_trace(gf_mul(gamma,value,h),h)


def gaussian_state_values(h,gamma):
    d=h.bit_length()-1;q=1<<d;allowed={0,q,-q,2*q,-2*q,4*q,-4*q};values=[]
    for z in range(q):
        row=[quadratic_sum(lambda x:pair_phase(h,gamma,z,negative,x),2*d) for negative in (False,True)]
        if any(x not in allowed for x in row):raise AssertionError('seven-state Gaussian bound failed')
        values.append(row)
    return values


def rational_inverse(A):
    n=len(A);rows=[[Fraction(x) for x in row]+[Fraction(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        p=next(i for i in range(j,n) if rows[i][j]);rows[j],rows[p]=rows[p],rows[j]
        c=rows[j][j];rows[j]=[x/c for x in rows[j]]
        for i in range(n):
            if i!=j and rows[i][j]:
                c=rows[i][j];rows[i]=[x-c*y for x,y in zip(rows[i],rows[j])]
    return [row[n:] for row in rows]


def reconstruct_from_moments(q,moments,positive_pairs,negative_pairs,*,signed=False):
    values=[0,q,-q,2*q,-2*q,4*q,-4*q]
    V=[[Fraction(value**j) for value in values] for j in range(7)]
    inverse=rational_inverse(V)
    first=[[sum(inverse[i][j]*moments[j][k] for j in range(7)) for k in range(7)] for i in range(7)]
    counts=[[sum(first[i][k]*inverse[j][k] for k in range(7)) for j in range(7)] for i in range(7)]
    if any(c.denominator!=1 or (not signed and c<0) for row in counts for c in row):raise ValueError('moments are not a Gaussian-state distribution')
    if sum(sum(row) for row in counts)!=moments[0][0]:raise ValueError('state multiplicities do not sum to the zeroth moment')
    if sum(abs(c) for row in counts for c in row)>q:raise ValueError('signed state mass exceeds the field size')
    total=sum(counts[i][j]*values[i]**positive_pairs*values[j]**negative_pairs for i in range(7) for j in range(7))
    if total.denominator!=1:raise AssertionError('nonintegral final character sum')
    return int(total),[[int(c) for c in row] for row in counts]


EIGHT_MOMENT_INDICES=[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]


def symmetry_state_nodes(d):
    q=1<<d;epsilon=1 if d%2==0 else -1
    return [(-q,epsilon*q),(q,epsilon*q)]+[(u,v)
        for amplitude,v in [(2*q,-2*epsilon*q),(4*q,4*epsilon*q)]
        for u in (-amplitude,0,amplitude)]


def reconstruct_from_eight_moments(d,moments,positive_pairs,negative_pairs,*,signed=False):
    q=1<<d;nodes=symmetry_state_nodes(d)
    matrix=[[u**i*v**j for u,v in nodes] for i,j in EIGHT_MOMENT_INDICES]
    inverse=rational_inverse(matrix)
    counts=[sum(row[k]*moments[index] for k,index in enumerate(EIGHT_MOMENT_INDICES)) for row in inverse]
    if any(c.denominator!=1 or (not signed and c<0) for c in counts):raise ValueError('eight moments do not define integral Gaussian states')
    if sum(abs(c) for c in counts)>q or sum(counts)!=moments[(0,0)]:raise ValueError('invalid signed Gaussian-state mass')
    total=sum(c*u**positive_pairs*v**negative_pairs for c,(u,v) in zip(counts,nodes))
    if total.denominator!=1:raise AssertionError('nonintegral eight-state character sum')
    return int(total),[dict(positive_value=u,negative_value=v,signed_multiplicity=int(c)) for c,(u,v) in zip(counts,nodes)]


def enumerated_terminal(certificate):
    h=certificate['field_modulus'];q=1<<certificate['field_degree']
    tau=certificate['radial_cubic'];pairs=gaussian_state_values(h,certificate['gamma'])
    weights=[1-2*gf_trace(gf_mul(tau,gf_mul(z,gf_mul(z,z,h),h),h),h) for z in range(q)]
    moments=[[sum(w*a**i*b**j for w,(a,b) in zip(weights,pairs)) for j in range(7)] for i in range(7)]
    result,counts=reconstruct_from_moments(q,moments,certificate['positive_pairs'],certificate['negative_pairs'],signed=bool(tau))
    direct=sum(w*a**certificate['positive_pairs']*b**certificate['negative_pairs'] for w,(a,b) in zip(weights,pairs))
    assert result==direct
    nodes=symmetry_state_nodes(certificate['field_degree'])
    if any(tuple(pair) not in nodes for pair in pairs):raise AssertionError('order-three Gaussian sign certificate failed')
    eight={index:moments[index[0]][index[1]] for index in EIGHT_MOMENT_INDICES}
    short_result,short_counts=reconstruct_from_eight_moments(certificate['field_degree'],eight,
        certificate['positive_pairs'],certificate['negative_pairs'],signed=bool(tau))
    assert short_result==result
    for row in short_counts:
        expected=sum(w for w,pair in zip(weights,pairs) if pair==[row['positive_value'],row['negative_value']])
        assert row['signed_multiplicity']==expected
    return result,dict(exact_joint_moments=moments,gaussian_state_multiplicities=counts,
        eight_state_multiplicities=short_counts,
        eight_moments=[dict(positive_exponent=i,negative_exponent=j,value=eight[(i,j)]) for i,j in EIGHT_MOMENT_INDICES],
        field_elements_enumerated=q,terminal_backend='explicit Gaussian-fiber reference')


def moment_terminal_reference49(certificate,exact_moment_backend):
    """Backend(h,gamma,tau,i,j) returns the exact expanded character moment.

    A general polynomial-time fixed-variable point-count backend is NOT
    implemented here.  This interface never silently enumerates the field.
    """
    h=certificate['field_modulus'];d=certificate['field_degree'];q=1<<d;gamma=certificate['gamma'];tau=certificate['radial_cubic']
    zeroth=quadratic_sum(lambda z:gf_trace(gf_mul(tau,gf_mul(z,gf_mul(z,z,h),h),h),h),d)
    moments=[[exact_moment_backend(h,gamma,tau,i,j) if i or j else zeroth for j in range(7)] for i in range(7)]
    return reconstruct_from_moments(q,moments,certificate['positive_pairs'],certificate['negative_pairs'],signed=bool(tau))


def moment_terminal_eight(certificate,exact_moment_backend):
    """Eight moments, at most three pair copies / eight AS field variables.

    Backend(h,gamma,tau,i,j) must return the exact expanded moment. A
    general fixed-variable point-count implementation is not supplied.
    """
    h=certificate['field_modulus'];d=certificate['field_degree'];gamma=certificate['gamma'];tau=certificate['radial_cubic']
    zeroth=quadratic_sum(lambda z:gf_trace(gf_mul(tau,gf_mul(z,gf_mul(z,z,h),h),h),h),d)
    moments={index:(exact_moment_backend(h,gamma,tau,*index) if any(index) else zeroth)
        for index in EIGHT_MOMENT_INDICES}
    return reconstruct_from_eight_moments(d,moments,certificate['positive_pairs'],certificate['negative_pairs'],signed=bool(tau))


# The production entry point uses the reduced eight-state theorem.  The
# rectangular 49-moment implementation remains separately named above.
moment_terminal=moment_terminal_eight
