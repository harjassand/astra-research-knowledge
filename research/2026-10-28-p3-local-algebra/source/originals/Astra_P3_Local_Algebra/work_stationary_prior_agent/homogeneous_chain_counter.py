#!/usr/bin/env python3
"""Exact homogeneous ternary chain-ring sums by projective critical rays.

No smoothness or supplied factorization is required.  This module expects an
ordinary ring polynomial; raw Boolean representation acquisition is separate.
Field terminal enumeration is explicitly budgeted, never called at e=0,2 mod3.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_chain_root','work_field_root','work_ring_count_agent'):
    sys.path.insert(0,str(ROOT/folder))
from acquired_chain_counter import ChainRing,Solver,ring_polynomial,gf_mul,gf_pow,linear_apply,polynomial_value
from field_descent import kernel_columns
from field_kloosterman import gf_trace
from chain_ring_kloosterman import quadratic_sum


def dehomogenize(P,chart):
    others=[i for i in range(3) if i!=chart]
    result={}
    for exponent,c in P.items():
        powers=tuple(exponent[i] for i in others)
        result[powers]=result.get(powers,0)^c
    return {a:c for a,c in result.items() if c},others


def derivative(P,i):
    out={}
    for a,c in P.items():
        if a[i]&1:
            b=list(a);b[i]-=1;b=tuple(b)
            out[b]=out.get(b,0)^c
    return {a:c for a,c in out.items() if c}


def chart_critical_points(h,P,chart):
    R=ChainRing(h,1);q=1<<R.d
    P={a:c&R.mask for a,c in P.items() if c&R.mask}
    f,others=dehomogenize(P,chart)
    g=[derivative(f,i) for i in range(2)]
    def gradient(a):
        values=[a&R.mask,a>>R.d]
        return sum(ring_polynomial(R,poly,values)<<(R.d*i) for i,poly in enumerate(g))
    constant=gradient(0)
    columns=[gradient(1<<i)^constant for i in range(2*R.d)]
    solution=Solver(columns)(constant)
    if solution is None:return []
    kernel=kernel_columns(columns)
    # Two ordinary quadratics with invertible Jacobian have at most four roots.
    if len(kernel)>2:raise AssertionError('critical chart exceeds Bezout degree four')
    points=[]
    for selector in range(1<<len(kernel)):
        a=solution^linear_apply(kernel,selector)
        values=[a&R.mask,a>>R.d]
        if any(values[others.index(j)] for j in range(chart+1,3)):continue
        if ring_polynomial(R,f,values):continue
        point=[0]*3;point[chart]=1
        for j,v in zip(others,values):point[j]=v
        points.append(dict(chart=chart,residue=point,transverse_residue=values))
    return points


def critical_rays(h,P):
    mu=P.get((1,1,1),0)&((1<<(h.bit_length()-1))-1)
    if not mu:raise ValueError('XYZ coefficient must be a unit')
    points=sum((chart_critical_points(h,P,j) for j in range(3)),[])
    if len(points)>3:raise AssertionError('square-free cubic has too many projective singular points')
    return points


def lift_ray(R,P,point):
    f,others=dehomogenize(P,point['chart'])
    g=[derivative(f,i) for i in range(2)]
    a=point['transverse_residue'][:]
    mu=f[(1,1)];inverse=gf_pow(mu&R.mask,(1<<R.d)-2,R.h)
    for k in range(1,R.e):
        values=[(ring_polynomial(R,poly,a)>>(R.d*k))&R.mask for poly in g]
        a[0]^=gf_mul(inverse,values[1],R.h)<<(R.d*k)
        a[1]^=gf_mul(inverse,values[0],R.h)<<(R.d*k)
    if any(ring_polynomial(R,poly,a) for poly in g):raise AssertionError('critical Hensel lift failed')
    A=f.get((2,0),0)^R.mul(f.get((3,0),0),a[0])^R.mul(f.get((2,1),0),a[1])
    B=f.get((0,2),0)^R.mul(f.get((0,3),0),a[1])^R.mul(f.get((1,2),0),a[0])
    arf=gf_trace(gf_mul(gf_mul(A&R.mask,B&R.mask,R.h),gf_mul(inverse,inverse,R.h),R.h),R.h)
    v=[0]*3;v[point['chart']]=1
    for j,value in zip(others,a):v[j]=value
    return dict(**point,transverse_lift=a,ring_lift=v,critical_value=ring_polynomial(R,f,a),
                quadratic_diagonal=[A,B],arf_sign=1-2*arf)


def unit_radial_sum(h,e,c):
    R=ChainRing(h,e);q=1<<R.d;c&=(1<<R.m)-1
    if c&((1<<(R.d*(e-1)))-1):return 0
    b=c>>(R.d*(e-1))
    if not b:return (q-1)*q**(e-1)
    def phase(x):return gf_trace(gf_mul(b,gf_mul(x,gf_mul(x,x,h),h),h),h)
    return q**(e-1)*(quadratic_sum(phase,R.d)-1)


def homogeneous_sum(h,e,P,*,terminal_bit_budget=24,field_terminal=None):
    R=ChainRing(h,e);q=1<<R.d
    if any(sum(a)!=3 or len(a)!=3 for a in P):raise ValueError('ordinary polynomial must be homogeneous cubic')
    rays=[lift_ray(R,P,point) for point in critical_rays(h,P)]
    stages=[];multiplier=1;total=0;depth=e
    while depth>=2:
        contributions=[]
        for ray in rays:
            radial=unit_radial_sum(h,depth,ray['critical_value'])
            sign=ray['arf_sign'] if depth&1 else 1
            value=q**depth*sign*radial
            total+=multiplier*value
            contributions.append(dict(chart=ray['chart'],residue=ray['residue'],
                radial_sum=radial,gaussian_sign=sign,signed_contribution=value))
        stages.append(dict(depth=depth,projective_ray_count=len(rays),contributions=contributions))
        if depth<=3:
            origin=q**(3*(depth-1));total+=multiplier*origin
            return total,dict(stages=stages,rays=rays,terminal='quadratic/origin',
                terminal_value=origin,field_points_enumerated=0,branching_depth=0)
        multiplier*=q**6;depth-=3
    residue={a:c&R.mask for a,c in P.items() if c&R.mask}
    if field_terminal is not None:
        leaf=field_terminal(h,residue);points=0;kind='supplied exact finite-field backend'
    else:
        if 3*R.d>terminal_bit_budget:raise ValueError('finite-field terminal exceeds explicit enumeration budget')
        F=ChainRing(h,1)
        leaf=sum(1-2*F.functional(ring_polynomial(F,residue,
            [(x>>(R.d*i))&R.mask for i in range(3)])) for x in range(q**3))
        points=q**3;kind='explicit finite-field terminal'
    return total+multiplier*leaf,dict(stages=stages,rays=rays,terminal=kind,
        terminal_value=leaf,field_points_enumerated=points,branching_depth=0)


def quotient_height(Q,R):
    height=0
    for monomial in Q:
        if monomial.bit_count()>2 or monomial>> (3*R.m):raise ValueError('not a binary quadratic in the three ring coordinates')
        while monomial:
            bit=(monomial&-monomial).bit_length()-1
            height=max(height,(bit%R.m)//R.d+1);monomial&=monomial-1
    return height


def restrict_origin_quadratic(Q,R,new_e):
    out=set();new_m=R.d*new_e
    for monomial in Q:
        term=0;vanishes=False
        while monomial:
            bit=(monomial&-monomial).bit_length()-1;block,local=divmod(bit,R.m)
            if local<R.d:vanishes=True;break
            local-=R.d
            if local>=new_m:raise ValueError('origin restriction retains a discarded layer')
            term|=1<<(new_m*block+local);monomial&=monomial-1
        if not vanishes:
            if term in out:out.remove(term)
            else:out.add(term)
    return out


def weighted_radial_sum(R,ray,Q):
    mask=(1<<R.m)-1;v=[a&mask for a in ray['ring_lift']];c=ray['critical_value']&mask
    def phase(r):
        x=sum(R.mul(r,a)<<(R.m*i) for i,a in enumerate(v))
        return R.functional(R.mul(c,R.mul(r,R.mul(r,r))))^polynomial_value(Q,x)
    whole=quadratic_sum(phase,R.m)
    nonunits=quadratic_sum(lambda r:phase(r<<R.d),R.m-R.d)
    return whole-nonunits,dict(all_ring_gaussian=whole,nonunit_gaussian=nonunits,
        gaussian_variable_counts=[R.m,R.m-R.d])


def weighted_homogeneous_sum(h,e,P,Q,*,terminal_bit_budget=24,field_terminal=None,
                             residual_bit_budget=None):
    """Count H plus arbitrary binary quotient quadratic, 3*height<=e+1.

    The quotient is checked from its actual ANF. Singular residue cubics are
    permitted. No Walsh expansion, field scan, or ring scan occurs before an
    explicitly budgeted depth-one terminal.
    """
    R=ChainRing(h,e);q=1<<R.d;Q=set(Q)
    if any(sum(a)!=3 or len(a)!=3 for a in P):raise ValueError('ordinary polynomial must be homogeneous cubic')
    height=quotient_height(Q,R)
    if 3*height>e+1 and residual_bit_budget is None:
        raise ValueError('quotient quadratic exceeds the certified height')
    rays=[lift_ray(R,P,point) for point in critical_rays(h,P)]
    stages=[];multiplier=1;total=0;depth=e
    while depth>=2:
        current=ChainRing(h,depth);height=quotient_height(Q,current)
        if 2*height>depth:
            if residual_bit_budget is None or 3*current.m>residual_bit_budget:
                raise ValueError('remaining weighted state exceeds the explicit residual budget')
            mask=(1<<current.m)-1
            leaf=sum(1-2*(current.functional(ring_polynomial(current,P,
                [(x>>(current.m*i))&mask for i in range(3)]))^polynomial_value(Q,x))
                for x in range(1<<(3*current.m)))
            return total+multiplier*leaf,dict(stages=stages,rays=rays,
                terminal='explicit weighted residual',terminal_value=leaf,
                residual_depth=depth,residual_variables=3*current.m,
                residual_points_enumerated=1<<(3*current.m),field_points_enumerated=0,
                branching_depth=0,walsh_leaves=0)
        contributions=[]
        for ray in rays:
            radial,radial_certificate=weighted_radial_sum(current,ray,Q)
            sign=ray['arf_sign'] if depth&1 else 1
            value=q**depth*sign*radial;total+=multiplier*value
            contributions.append(dict(chart=ray['chart'],residue=ray['residue'],
                radial_sum=radial,gaussian_sign=sign,signed_contribution=value,
                radial_certificate=radial_certificate))
        stages.append(dict(depth=depth,quotient_height=height,projective_ray_count=len(rays),
                           contributions=contributions))
        if depth<=3:
            if height>1:raise AssertionError('nonconstant terminal origin weight')
            origin=(1-2*int(0 in Q))*q**(3*(depth-1));total+=multiplier*origin
            return total,dict(stages=stages,rays=rays,terminal='quadratic/origin',
                terminal_value=origin,field_points_enumerated=0,branching_depth=0,
                walsh_leaves=0)
        Q=restrict_origin_quadratic(Q,current,depth-3)
        multiplier*=q**6;depth-=3
    if quotient_height(Q,ChainRing(h,1)):
        if residual_bit_budget is None or 3*R.d>residual_bit_budget:
            raise ValueError('weighted field residual exceeds the explicit residual budget')
        F=ChainRing(h,1)
        leaf=sum(1-2*(F.functional(ring_polynomial(F,P,
            [(x>>(R.d*i))&R.mask for i in range(3)]))^polynomial_value(Q,x)) for x in range(q**3))
        return total+multiplier*leaf,dict(stages=stages,rays=rays,
            terminal='explicit weighted residual',terminal_value=leaf,residual_depth=1,
            residual_variables=3*R.d,residual_points_enumerated=q**3,
            field_points_enumerated=q**3,branching_depth=0,walsh_leaves=0)
    residue={a:c&R.mask for a,c in P.items() if c&R.mask}
    if field_terminal is not None:
        leaf=field_terminal(h,residue);points=0;kind='supplied exact finite-field backend'
    else:
        if 3*R.d>terminal_bit_budget:raise ValueError('finite-field terminal exceeds explicit enumeration budget')
        F=ChainRing(h,1)
        leaf=sum(1-2*F.functional(ring_polynomial(F,residue,
            [(x>>(R.d*i))&R.mask for i in range(3)])) for x in range(q**3))
        points=q**3;kind='explicit finite-field terminal'
    leaf*=1-2*int(0 in Q)
    return total+multiplier*leaf,dict(stages=stages,rays=rays,terminal=kind,
        terminal_value=leaf,field_points_enumerated=points,branching_depth=0,walsh_leaves=0)
