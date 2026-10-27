#!/usr/bin/env python3
"""Raw chain-ring cubic acquisition and counting through a contact hyperplane.

The module rank is not fixed. Candidate rays are enumerated in a manufactured
binary kernel, not in the whole residue field. Every structural gate is checked.
"""
from stationary_chain_counter import *
from field_descent import kernel_columns
sys.path.insert(0,str(ROOT/'work_stationary_prior_agent'))
from homogeneous_chain_counter import derivative,restrict_origin_quadratic,weighted_radial_sum


def degree_exponents(b,total):
    if b==1:return [(total,)]
    return [(i,)+a for i in range(total+1) for a in degree_exponents(b-1,total-i)]


def squarefree_cubic(acquired):
    b=acquired['module_dimension']
    return {tuple(int(i in row['indices']) for i in range(b)):row['coefficient']
            for row in acquired['cubic'] if row['coefficient']}


def ordinary_models(R,b,exponents):
    """Binary coefficient columns for binary-quadratic ordinary monomials."""
    n=b*R.m;gram=R.gram();models=[];labels=[]
    for exponent in exponents:
        support=[i for i in range(n) if exponent[i//R.m]]
        columns=[set() for _ in range(R.m)]
        zero=monomial(R,exponent,[0]*b);singles={}
        for j in bits(linear_apply(gram,zero)):columns[j].add(0)
        for i in support:
            values=[0]*b;values[i//R.m]=1<<(i%R.m)
            singles[i]=monomial(R,exponent,values)^zero
            for j in bits(linear_apply(gram,singles[i])):columns[j].add(1<<i)
        for i,k in itertools.combinations(support,2):
            values=[0]*b;values[i//R.m]^=1<<(i%R.m);values[k//R.m]^=1<<(k%R.m)
            polar=monomial(R,exponent,values)^zero^singles[i]^singles[k]
            for j in bits(linear_apply(gram,polar)):columns[j].add((1<<i)|(1<<k))
        models.extend(columns);labels.extend((exponent,1<<j) for j in range(R.m))
    return models,labels


def fit_rank_homogeneous_quotient(acquired,*,height=None):
    R=ChainRing(acquired['h'],acquired['e']);b=acquired['module_dimension'];n=b*R.m
    if R.d<3:raise ValueError('complete ordinary quotient acquisition requires d>=3')
    if height is None:height=(R.e+1)//3
    if not 0<=height<=R.e:raise ValueError('invalid quotient height')
    canonical=squarefree_cubic(acquired);remainder=set(acquired['quadratic_remainder'])
    lowmask=sum(((1<<(R.d*height))-1)<<(R.m*i) for i in range(b))
    exponents=[a for total in range(4) for a in degree_exponents(b,total)
               if not(total==3 and max(a)<=1) and not(total==2 and 2 in a)]
    models,labels=ordinary_models(R,b,exponents)
    protected=[sum(1<<i for i in pair) for degree in (1,2)
               for pair in itertools.combinations(range(n),degree)
               if any((1<<i)&~lowmask for i in pair)]
    positions={term:j for j,term in enumerate(protected)}
    def vector(anf):return sum(1<<positions[m] for m in anf if m in positions)
    columns=[vector(model) for model in models];solution=solve(columns,vector(remainder))
    if solution is None:raise ValueError('no homogeneous cubic lift modulo the acquired quotient')
    P=dict(canonical)
    for j in bits(solution):
        exponent,coefficient=labels[j];P[exponent]=P.get(exponent,0)^coefficient
    H={a:c for a,c in P.items() if c and sum(a)==3}
    # Deep cross coefficients need not lie in the contraction image. Determine
    # the center modulo J^(e-height), which is exactly what counting needs.
    pairs=list(itertools.combinations(range(b),2));kept_m=R.d*(R.e-height)
    kept_mask=(1<<kept_m)-1;contraction=[]
    for k in range(b):
        for bit in range(kept_m):
            image=0
            for row,(i,j) in enumerate(pairs):
                if k in (i,j):continue
                a=tuple(int(z in (i,j,k)) for z in range(b))
                image|=(R.mul(canonical.get(a,0),1<<bit)&kept_mask)<<(row*kept_m)
            contraction.append(image)
    target=0
    for row,(i,j) in enumerate(pairs):
        a=tuple(int(z in (i,j)) for z in range(b))
        target|=(P.get(a,0)&kept_mask)<<(row*kept_m)
    if len(span(contraction))!=b*kept_m:
        raise ValueError('residue third tensor does not inject its contraction map')
    center_solution=solve(contraction,target)
    if center_solution is None:raise ValueError('cross coefficients have no center modulo the quotient')
    center=[(center_solution>>(kept_m*i))&kept_mask for i in range(b)]
    encoded=sum(a<<(R.m*i) for i,a in enumerate(center));mask=(1<<R.m)-1
    def residual(x):
        values=[(x>>(R.m*i))&mask for i in range(b)]
        original=R.functional(ring_polynomial(R,canonical,values))^polynomial_value(remainder,x)
        shifted=[a^c for a,c in zip(values,center)]
        return original^R.functional(ring_polynomial(R,H,shifted))
    noise=quadratic_coefficients(residual,n)
    if any(term&~lowmask for term in noise):
        raise ValueError('manufactured center leaves a coefficient outside the quotient')
    centered=quadratic_coefficients(lambda x:polynomial_value(noise,x^encoded),n)
    assert all(not(term&~lowmask) for term in centered)
    certificate=dict(quotient_height=height,quotient_binary_variables=b*R.d*height,
        fit_columns=len(columns),fit_rank=len(span(columns)),fit_constraints=len(protected),
        center_congruence_depth=R.e-height,center_contraction_rank=b*kept_m,
        acquired_center=center,exact_third_tensor_identity=True,
        exact_quadratic_and_affine_identity=True,verified_quotient_support=True,
        uncentered_noise=sorted(noise),centered_noise=sorted(centered))
    return H,centered,certificate


def polynomial_linear_change(R,P,columns):
    """Ordinary substitution x=sum_j columns[j]*y_j."""
    b=len(columns);zero=(0,)*b;result={}
    for exponent,c in P.items():
        expanded={zero:c}
        for i,power in enumerate(exponent):
            for _ in range(power):
                new={}
                for a,value in expanded.items():
                    for j in range(b):
                        if columns[j][i]:
                            z=list(a);z[j]+=1;z=tuple(z)
                            new[z]=new.get(z,0)^R.mul(value,columns[j][i])
                expanded={a:v for a,v in new.items() if v}
        for a,v in expanded.items():result[a]=result.get(a,0)^v
    return {a:c for a,c in result.items() if c}


def contact_geometry(R,H,b,*,require_infinity=True):
    if b<5 or b%2!=1:raise ValueError('contact acquisition requires odd module rank >=5')
    m=b-1
    cubic={indices:H.get(tuple(int(j in indices) for j in range(b)),0)&R.mask
           for indices in itertools.combinations(range(b),3)}
    wedges=list(itertools.combinations(range(b),4));columns=[]
    for i in range(b):
        for bit in range(R.d):
            image=0
            for row,indices in enumerate(wedges):
                if i in indices:
                    c=cubic[tuple(j for j in indices if j!=i)]
                    image|=gf_mul(c,1<<bit,R.h)<<(R.d*row)
            columns.append(image)
    kernel=kernel_columns(columns)
    if len(kernel)!=R.d:raise ValueError('third form has no unique contact covector')
    ell=[(kernel[0]>>(R.d*i))&R.mask for i in range(b)]
    pivot=next(i for i,c in enumerate(ell) if c);inverse=gf_pow(ell[pivot],(1<<R.d)-2,R.h)
    ell=[gf_mul(c,inverse,R.h) for c in ell]
    chart=[]
    for i in range(b):
        if i==pivot:continue
        v=[0]*b;v[i]=1;v[pivot]=ell[i];chart.append(v)
    v=[0]*b;v[pivot]=1;chart.append(v)
    changed=polynomial_linear_change(R,H,chart)
    f={}
    for a,c in changed.items():f[a[:-1]]=f.get(a[:-1],0)^c
    f={a:c for a,c in f.items() if c};grad=[derivative(f,i) for i in range(m)]
    M=[[0]*m for _ in range(m)];B=[[0]*m for _ in range(m)];constant=[]
    for i,g in enumerate(grad):
        constant.append(g.get((0,)*m,0)&R.mask)
        for a,c in g.items():
            c&=R.mask
            if not c:continue
            if sum(a)==2:
                if 2 not in a:raise ValueError('contact chart retained a mixed transverse cubic')
                M[i][a.index(2)]=c
            elif sum(a)==1:B[i][a.index(1)]=c
            elif sum(a)!=0:raise AssertionError('invalid gradient degree')
    if field_matrix_rank(B,R.h)!=m:
        raise ValueError('contact transverse Hessian is degenerate')
    if any(B[i][i] or B[i][j]!=B[j][i] for i in range(m) for j in range(m)):
        raise AssertionError('ordinary Hessian is not alternating')
    square_rank=field_matrix_rank(M,R.h)
    if require_infinity and square_rank!=m:
        raise ValueError('square coefficient matrix does not exclude the missing hyperplane')
    rhs=sum(c<<(R.d*i) for i,c in enumerate(constant));binary=[]
    for j in range(m):
        for bit in range(R.d):
            x=1<<bit;x2=gf_mul(x,x,R.h)
            binary.append(sum((gf_mul(M[i][j],x2,R.h)^gf_mul(B[i][j],x,R.h))
                              <<(R.d*i) for i in range(m)))
    solution=Solver(binary)(rhs);critical_kernel=kernel_columns(binary)
    if len(critical_kernel)>m:raise AssertionError('semilinear kernel exceeds its Bezout degree')
    inverse_columns=[]
    for i in range(m):
        answer=field_linear_solve(B,[int(i==j) for j in range(m)],R.h)
        if answer is None:raise AssertionError('invertible Hessian solve failed')
        inverse_columns.append(answer)
    return dict(covector=ell,covector_kernel_dimension=len(kernel),chart_columns=chart,
        chart_polynomial=f,gradient=grad,square_matrix=M,hessian=B,
        hessian_inverse_columns=inverse_columns,critical_solution=solution,
        critical_kernel=critical_kernel,critical_kernel_dimension=len(critical_kernel),
        binary_gradient_dimension=m*R.d,transverse_rank=m,
        square_matrix_rank=square_rank,missing_hyperplane_excluded=(square_rank==m))


def translated_quadratic(R,P,point):
    """Formal degree-two Taylor part; ordinary and binary degree are different."""
    m=len(point);out={}
    for beta in degree_exponents(m,2):
        value=0
        for alpha,c in P.items():
            if any(v>u or (v&~u) for u,v in zip(alpha,beta)):continue
            residual=tuple(u-v for u,v in zip(alpha,beta))
            value^=R.mul(c,monomial(R,residual,point))
        if value:out[beta]=value
    return out


def lift_contact_ray(R,geometry,point):
    f=geometry['chart_polynomial'];grad=geometry['gradient'];m=len(point);a=point[:]
    inverse=geometry['hessian_inverse_columns']
    for layer in range(1,R.e):
        errors=[(ring_polynomial(R,g,a)>>(R.d*layer))&R.mask for g in grad]
        correction=[0]*m
        for j,error in enumerate(errors):
            for i in range(m):correction[i]^=gf_mul(error,inverse[j][i],R.h)
        for i,value in enumerate(correction):a[i]^=value<<(R.d*layer)
    if any(ring_polynomial(R,g,a) for g in grad):raise AssertionError('critical Hensel lift failed')
    v=[0]*(m+1)
    for coordinate,c in zip(a+[1],geometry['chart_columns']):
        for i in range(m+1):v[i]^=R.mul(coordinate,c[i])
    F=ChainRing(R.h,1);residue={alpha:c&R.mask for alpha,c in f.items() if c&R.mask}
    Q2=translated_quadratic(F,residue,point)
    def quadratic(x):
        values=[(x>>(R.d*i))&R.mask for i in range(m)]
        return F.functional(ring_polynomial(F,Q2,values))
    gauss=quadratic_sum(quadratic,m*R.d);magnitude=1<<(R.d*(m//2))
    if abs(gauss)!=magnitude:raise AssertionError('nondegenerate transverse Gaussian has wrong magnitude')
    return dict(transverse_residue=point,transverse_lift=a,ring_lift=v,
        critical_value=ring_polynomial(R,f,a),arf_sign=gauss//magnitude,
        exact_hensel_gradient_identity=True)


def quotient_height_rank(Q,R,b):
    height=0
    for term in Q:
        if term<0 or term>>(b*R.m) or term.bit_count()>2:raise ValueError('invalid quotient quadratic')
        for i in bits(term):height=max(height,(i%R.m)//R.d+1)
    return height


def contact_field_sum(h,H,b,chart,*,field_bit_budget=24):
    """Sum q exact quadratic fibers in the acquired chart; never scan q^b."""
    F=ChainRing(h,1)
    if F.d>field_bit_budget:raise ValueError('field-coordinate enumeration exceeds explicit bit budget')
    residue={a:c&F.mask for a,c in H.items() if c&F.mask}
    changed=polynomial_linear_change(F,residue,chart)
    if any(a[-1]==0 and max(a)<=1 for a in changed):
        raise AssertionError('field fiber retained a squarefree transverse cubic')
    transverse=(b-1)*F.d;total=0;samples=[]
    for z in range(1<<F.d):
        def value(w):
            values=[(w>>(F.d*i))&F.mask for i in range(b-1)]+[z]
            return F.functional(ring_polynomial(F,changed,values))
        gaussian=quadratic_sum(value,transverse);total+=gaussian
        if len(samples)<8:samples.append(dict(field_coordinate=z,gaussian=gaussian))
    return total,dict(method='quadratic Gaussian fibers over one acquired field coordinate',
        field_values_enumerated=1<<F.d,gaussian_fiber_variables=transverse,
        sample_gaussians=samples,sample_limit=8,full_assignments_enumerated=0)


def weighted_contact_sum(h,e,H,Q,b,*,terminal_bit_budget=24,field_terminal=None):
    R=ChainRing(h,e);q=1<<R.d;Q=set(Q)
    if any(len(a)!=b or sum(a)!=3 for a in H):raise ValueError('expected an ordinary homogeneous cubic')
    if 3*quotient_height_rank(Q,R,b)>e+1:raise ValueError('quotient height exceeds the certified range')
    geometry=contact_geometry(R,H,b,require_infinity=e>=2);F=ChainRing(h,1);m=b-1
    residue={a:c&R.mask for a,c in geometry['chart_polynomial'].items() if c&R.mask}
    states=[];depth=e;multiplier=1;current_Q=Q
    while depth>=2:
        current=ChainRing(h,depth)
        if 2*quotient_height_rank(current_Q,current,b)>depth:raise AssertionError('lost transverse weight invariance')
        states.append(dict(depth=depth,multiplier=multiplier,quadratic=current_Q,
                           ray_sum=0,ray_count=0))
        if depth<=3:
            leaf=(1-2*int(0 in current_Q))*q**(b*(depth-1))
            total=multiplier*leaf;kind='constant origin';enumerated=0;field_certificate=None;break
        current_Q=restrict_origin_quadratic(current_Q,current,depth-3)
        depth-=3;multiplier*=q**(2*b)
    else:
        if quotient_height_rank(current_Q,F,b):raise AssertionError('nonconstant field-terminal noise')
        field_H={a:c&R.mask for a,c in H.items() if c&R.mask}
        if field_terminal is not None:
            leaf=field_terminal(h,b,field_H);kind='supplied exact field terminal';enumerated=0;field_certificate=None
        else:
            leaf,field_certificate=contact_field_sum(h,field_H,b,geometry['chart_columns'],
                                                    field_bit_budget=terminal_bit_budget)
            kind='exact field-coordinate Gaussian fibers';enumerated=0
        leaf*=1-2*int(0 in current_Q);total=multiplier*leaf
    samples=[];candidate_count=0;ray_count=0
    if states and geometry['critical_solution'] is not None:
        for selector in range(1<<geometry['critical_kernel_dimension']):
            candidate_count+=1
            x=geometry['critical_solution']^linear_apply(geometry['critical_kernel'],selector)
            point=[(x>>(R.d*i))&R.mask for i in range(m)]
            if ring_polynomial(F,residue,point):continue
            ray=lift_contact_ray(R,geometry,point);ray_count+=1
            if len(samples)<8:samples.append(ray)
            for state in states:
                current=ChainRing(h,state['depth']);radial,_=weighted_radial_sum(current,ray,state['quadratic'])
                sign=ray['arf_sign'] if state['depth']&1 else 1
                value=(1<<(R.d*m*state['depth']//2))*sign*radial
                state['ray_sum']+=value;state['ray_count']+=1
                total+=state['multiplier']*value
    records=[dict(depth=s['depth'],multiplier=s['multiplier'],ray_sum=s['ray_sum'],
                  ray_count=s['ray_count'],quotient_height=quotient_height_rank(s['quadratic'],ChainRing(h,s['depth']),b))
             for s in states]
    certificate=dict(module_rank=b,geometry={k:v for k,v in geometry.items()
        if k not in ('chart_polynomial','gradient','hessian_inverse_columns')},
        candidate_count=candidate_count,projective_ray_count=ray_count if states else None,
        sample_rays=samples,sample_limit=8,all_rays_streamed=True,
        stages=records,terminal=kind,terminal_value=leaf,field_points_enumerated=enumerated,
        field_terminal_certificate=field_certificate,
        walsh_leaves=0,recursive_origin_states=len(states),binary_kernel_candidates_only=True)
    return total,certificate


def compile_contact(poly,n,*,terminal_bit_budget=24,field_terminal=None):
    started=time.perf_counter();poly=set(poly);acquired=acquire_chain(poly,n)
    b=acquired['module_dimension'];H,Q,fit=fit_rank_homogeneous_quotient(acquired)
    signed,certificate=weighted_contact_sum(acquired['h'],acquired['e'],H,Q,b,
        terminal_bit_budget=terminal_bit_budget,field_terminal=field_terminal)
    if abs(signed)>1<<n or ((1<<n)+signed)&1:raise AssertionError('invalid exact count')
    return dict(original_variables=n,raw_anf_terms=len(poly),module_dimension=b,
        field_degree=acquired['d'],chain_length=acquired['e'],field_modulus=acquired['h'],
        centroid_dimension=acquired['algebra_dimension'],coordinate_columns=acquired['coordinate_columns'],
        homogeneous_cubic=[dict(exponents=list(a),coefficient=c) for a,c in sorted(H.items())],
        quotient_quadratic=sorted(Q),fit=fit,count_certificate=certificate,
        signed_count=signed,zero_count=((1<<n)+signed)//2,seconds=time.perf_counter()-started)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--terminal-bit-budget',type=int,default=24)
    args=parser.parse_args();source=json.loads(args.input.read_text())
    result=compile_contact(source['polynomial'],source['n'],terminal_bit_budget=args.terminal_bit_budget)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
