#!/usr/bin/env python3
"""Contact-hyperplane and critical-ray acquisition; audit helpers, not raw compiler."""
from rank_five_stationary import *
from field_descent import kernel_columns,solve
from field_kloosterman import gf_trace


def field_nullspace(rows,h,width):
    a=[row[:] for row in rows];pivots=[];at=0;q=1<<(h.bit_length()-1)
    for j in range(width):
        pivot=next((i for i in range(at,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[at],a[pivot]=a[pivot],a[at];inverse=gf_pow(a[at][j],q-2,h)
        a[at]=[gf_mul(x,inverse,h) for x in a[at]]
        for i in range(len(a)):
            if i!=at and a[i][j]:
                c=a[i][j];a[i]=[x^gf_mul(c,y,h) for x,y in zip(a[i],a[at])]
        pivots.append(j);at+=1
    out=[]
    for free in range(width):
        if free in pivots:continue
        vector=[0]*width;vector[free]=1
        for i,j in enumerate(pivots):vector[j]=a[i][free]
        out.append(vector)
    return out


def tensor_field(T,u,v,w,h):
    value=0
    for indices,c in T.items():
        for i,j,k in itertools.permutations(indices):
            value^=gf_mul(c,gf_mul(u[i],gf_mul(v[j],w[k],h),h),h)
    return value


def acquire_contact_hyperplane(T,b,h):
    if b<5 or b%2==0:raise ValueError('requires odd module rank at least five')
    rows=[]
    for four in itertools.combinations(range(b),4):
        row=[0]*b
        for j in four:row[j]=T.get(tuple(i for i in four if i!=j),0)
        rows.append(row)
    kernel=field_nullspace(rows,h,b)
    if len(kernel)!=1:raise ValueError('exterior annihilator is not a line')
    ell=kernel[0];pivot=next(i for i,x in enumerate(ell) if x)
    inverse=gf_pow(ell[pivot],(1<<(h.bit_length()-1))-2,h)
    ell=[gf_mul(inverse,x,h) for x in ell];v0=[0]*b;v0[pivot]=1;W=[]
    for j in range(b):
        if j==pivot:continue
        v=[0]*b;v[j]=1;v[pivot]=ell[j];W.append(v)
    def omega(u,v):return tensor_field(T,v0,u,v,h)
    symplectic=[]
    while W:
        u=W.pop(0);at=next((j for j,v in enumerate(W) if omega(u,v)),None)
        if at is None:raise ValueError('contact hyperplane form is degenerate')
        v=W.pop(at);scale=gf_pow(omega(u,v),(1<<(h.bit_length()-1))-2,h)
        v=[gf_mul(scale,x,h) for x in v];nextW=[]
        for w in W:
            a=omega(w,v);c=omega(w,u)
            nextW.append([x^gf_mul(a,y,h)^gf_mul(c,z,h) for x,y,z in zip(w,u,v)])
        symplectic.extend([u,v]);W=nextW
    columns=symplectic+[v0]
    for indices in itertools.combinations(range(b),3):
        actual=tensor_field(T,*(columns[i] for i in indices),h)
        expected=int(indices[2]==b-1 and indices[0]%2==0 and indices[1]==indices[0]+1)
        if actual!=expected:raise AssertionError('contact tensor normalization failed')
    return ell,columns,dict(exterior_rows=len(rows),exterior_columns=b,
                           exterior_kernel_dimension=1,transverse_symplectic_rank=b-1)


def substitute_ring_polynomial(R,P,columns):
    b=len(columns);zero=(0,)*b
    linears=[{tuple(int(j==k) for j in range(b)):columns[k][i]
              for k in range(b) if columns[k][i]} for i in range(b)]
    def multiply(A,B):
        out={}
        for e,c in A.items():
            for f,d in B.items():
                a=tuple(x+y for x,y in zip(e,f));out[a]=out.get(a,0)^R.mul(c,d)
        return {a:c for a,c in out.items() if c}
    out={}
    for exponent,c in P.items():
        product={zero:c}
        for i,power in enumerate(exponent):
            for _ in range(power):product=multiply(product,linears[i])
        for e,c in product.items():out[e]=out.get(e,0)^c
    return {e:c for e,c in out.items() if c}


def ordinary_gradient(R,P,values,direction):
    value=0
    for exponent,c in P.items():
        if exponent[direction]&1:
            a=list(exponent);a[direction]-=1
            value^=ring_polynomial(R,{tuple(a):c},values)
    return value


def residue_critical_rays(R,P):
    b=len(next(iter(P)));m=b-1
    T={tuple(i for i,x in enumerate(e) if x):c&R.mask for e,c in P.items()
       if max(e)==1 and sum(e)==3 and c&R.mask}
    ell,columns,certificate=acquire_contact_hyperplane(T,b,R.h)
    transformed=substitute_ring_polynomial(R,P,columns)
    F=ChainRing(R.h,1);P0={e:c&R.mask for e,c in transformed.items() if c&R.mask}
    M=[[0]*m for _ in range(m)];B=[[0]*m for _ in range(m)];constant=[]
    for i in range(m):
        for j in range(m):
            exponent=[0]*b;exponent[i]+=1;exponent[j]+=2
            M[i][j]=P0.get(tuple(exponent),0)
            if i!=j:
                exponent=[0]*b;exponent[i]=exponent[j]=exponent[-1]=1
                B[i][j]=P0.get(tuple(exponent),0)
        exponent=[0]*b;exponent[i]=1;exponent[-1]=2
        constant.append(P0.get(tuple(exponent),0))
    if field_matrix_rank(M,R.h)!=m:raise ValueError('homogeneous gradient on hyperplane is singular')
    if field_matrix_rank(B,R.h)!=m:raise AssertionError('transverse Hessian lost rank')
    width=m*R.d
    def unpack(x):return [(x>>(R.d*i))&R.mask for i in range(m)]
    def gradient(bits):
        x=unpack(bits);out=[]
        for i in range(m):
            c=constant[i]
            for j in range(m):
                c^=gf_mul(M[i][j],gf_mul(x[j],x[j],R.h),R.h)^gf_mul(B[i][j],x[j],R.h)
            out.append(c)
        return sum(c<<(R.d*i) for i,c in enumerate(out))
    offset=gradient(0);binary_columns=[gradient(1<<i)^offset for i in range(width)]
    particular=solve(binary_columns,offset);null=kernel_columns(binary_columns)
    if len(null)>m:raise AssertionError('additive root fiber exceeds Bezout bound')
    candidates=[];roots=[]
    if particular is not None:
        for mask in range(1<<len(null)):
            x=particular
            for i,v in enumerate(null):
                if mask>>i&1:x^=v
            assert gradient(x)==0
            w=unpack(x);v=w+[1]
            assert all(ordinary_gradient(F,P0,v,i)==0 for i in range(m))
            value=ring_polynomial(F,P0,v);candidates.append(w)
            if value==0:roots.append(w)
    certificate.update(binary_root_unknowns=width,binary_root_kernel_dimension=len(null),
        transverse_roots=len(candidates),critical_rays=len(roots),hyperplane_square_rank=m,
        hyperplane=ell,field_columns=columns,transverse_square_coefficients=M,
        transverse_hessian=B,transverse_constant=constant)
    return transformed,roots,certificate


def lift_transverse_center(R,P,root,B):
    m=len(root);w=list(root)
    for depth in range(1,R.e):
        g=[ordinary_gradient(R,P,w+[1],i) for i in range(m)]
        assert all(not c&((1<<(R.d*depth))-1) for c in g)
        rhs=[(c>>(R.d*depth))&R.mask for c in g]
        correction=field_linear_solve(B,rhs,R.h)
        if correction is None:raise AssertionError('unit Hessian failed to lift')
        for i,c in enumerate(correction):w[i]^=c<<(R.d*depth)
    assert all(ordinary_gradient(R,P,w+[1],i)==0 for i in range(m))
    return w,ring_polynomial(R,P,w+[1])


def hasse_square_coefficient(R,P,v,i):
    value=0
    for exponent,c in P.items():
        if exponent[i] not in (2,3):continue
        e=list(exponent);e[i]-=2
        value^=ring_polynomial(R,{tuple(e):c},v)
    return value&R.mask


def acquire_lifted_rays(R,P):
    transformed,roots,certificate=residue_critical_rays(R,P)
    B=certificate['transverse_hessian'];rays=[]
    for root in roots:
        center,c=lift_transverse_center(R,transformed,root,B)
        A=[hasse_square_coefficient(R,transformed,center+[1],i) for i in range(len(root))]
        arf=0
        for i in range(0,len(root),2):arf^=gf_mul(A[i],A[i+1],R.h)
        rays.append(dict(residue_center=root,center=center,critical_value=c,
                         arf_bit=gf_trace(arf,R.h)))
    return transformed,rays,certificate


def uniform_contact_polynomial(pair_count,constant=0):
    b=2*pair_count+1;P={}
    if constant:
        e=[0]*b;e[-1]=3;P[tuple(e)]=constant
    for j in range(pair_count):
        i=2*j
        for ei,ej,ez in [(1,1,1),(2,1,0),(1,2,0)]:
            e=[0]*b;e[i]=ei;e[i+1]=ej;e[-1]=ez;P[tuple(e)]=1
    return P


def unique_ray_polynomial(pair_count):
    b=2*pair_count+1;P={}
    for j in range(pair_count):
        i=2*j
        for ei,ej,ez in [(3,0,0),(1,2,0),(0,3,0),(1,1,1)]:
            e=[0]*b;e[i]=ei;e[i+1]=ej;e[-1]=ez;P[tuple(e)]=1
    return P


def gold_gaussian(h):
    d=h.bit_length()-1
    return quadratic_sum(lambda x:gf_trace(gf_mul(x,gf_mul(x,x,h),h),h),d)


def uniform_field_sum(h,pair_count):
    q=1<<(h.bit_length()-1);G=gold_gaussian(h)
    n3=(q-2+G)//6;n1=(q-G)//2;n0=(q+1+G)//3
    assert 6*n3==q-2+G and 2*n1==q-G and 3*n0==q+1+G
    assert min(n0,n1,n3)>=0 and n0+n1+n3==q
    return q**pair_count*(n0+(1<<pair_count)*n1+(1<<(2*pair_count))*n3)


def uniform_chain_sum(h,e,pair_count):
    if e<1 or pair_count<2:raise ValueError('requires e>=1 and pair_count>=2')
    q=1<<(h.bit_length()-1);b=2*pair_count+1
    N=(1<<(2*pair_count-1))+(1<<(pair_count-1))
    if e==1:return uniform_field_sum(h,pair_count)
    if e<=3:origin=q**(b*(e-1))
    else:origin=q**(2*b)*uniform_chain_sum(h,e-3,pair_count)
    return origin+N*(q-1)*q**((pair_count+1)*e-1)
