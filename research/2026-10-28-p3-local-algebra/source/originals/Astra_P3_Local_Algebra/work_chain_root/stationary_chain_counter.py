#!/usr/bin/env python3
"""Raw hidden-chain cubic counter using certified stationary reductions."""
from acquired_chain_counter import *
from field_descent import trace_gram
from field_rank_decoder import field_linear_solve
from chain_ring_kloosterman import quadratic_sum

def field_matrix_rank(rows,h):
    rows=[row[:] for row in rows];rank=0;q=1<<(h.bit_length()-1)
    for col in range(len(rows[0]) if rows else 0):
        pivot=next((j for j in range(rank,len(rows)) if rows[j][col]),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        inverse=gf_pow(rows[rank][col],q-2,h)
        rows[rank]=[gf_mul(inverse,c,h) for c in rows[rank]]
        for j in range(rank+1,len(rows)):
            if rows[j][col]:
                c=rows[j][col];rows[j]=[a^gf_mul(c,b,h) for a,b in zip(rows[j],rows[rank])]
        rank+=1
    return rank

def monomials_of_degree(degree):
    return [(i,j,degree-i-j) for i in range(degree+1) for j in range(degree-i+1)]

def macaulay_certificate(M,mu,h):
    quadratics=[]
    for i in range(3):
        g={tuple(2*int(j==k) for j in range(3)):M[i][k] for k in range(3) if M[i][k]}
        g[tuple(int(j!=i) for j in range(3))]=mu;quadratics.append(g)
    index={e:i for i,e in enumerate(monomials_of_degree(4))};rows=[]
    for g in quadratics:
        for factor in monomials_of_degree(2):
            row=[0]*15
            for exponent,c in g.items():row[index[tuple(a+b for a,b in zip(exponent,factor))]]^=c
            rows.append(row)
    rank=field_matrix_rank(rows,h)
    if rank!=15:raise ValueError('residue gradient lacks a projective zero-free certificate')
    return dict(rows=18,columns=15,rank=rank,homogeneous_gradient_coefficients=M)

def residue_center(R,mu,Q):
    if R.e<2:raise ValueError('requires e>=2')
    B=quadratic_matrix_from_anf(Q,3*R.m);gram_solver=Solver(trace_gram(R.h))
    residue_mask=sum(R.mask<<(R.m*i) for i in range(3))
    if R.d==1:
        tops=[R.m*i+R.e-1 for i in range(3)]
        if any(B[top]&~residue_mask for top in tops):
            raise ValueError('highest digit derivative depends on nonresidue digits')
        zeros=[]
        for a in range(8):
            center=[(a>>i)&1 for i in range(3)]
            encoded=sum(center[i]<<(R.m*i) for i in range(3))
            if all((int((1<<tops[i]) in Q)^((B[tops[i]]&encoded).bit_count()&1)
                    ^((mu&1)*center[(i+1)%3]*center[(i+2)%3]))==0 for i in range(3)):
                zeros.append(center)
        if len(zeros)!=1:raise ValueError('binary residue gradient has no unique zero')
        return zeros[0],dict(center=zeros[0],residue_points_tested=8,
            critical_points=1,method='exact binary-residue derivative equations')
    M=[[0]*3 for _ in range(3)];linear=[[0]*3 for _ in range(3)];constant=[]
    evaluation=[[1<<k,gf_mul(1<<k,1<<k,R.h)] for k in range(R.d)]
    for i in range(3):
        top=R.m*i+R.d*(R.e-1)
        if any(B[top+a]&~residue_mask for a in range(R.d)):
            raise ValueError('highest digit derivative depends on nonresidue digits')
        constant.append(gram_solver(sum(int((1<<(top+a)) in Q)<<a for a in range(R.d))))
        for j in range(3):
            images=[]
            for k in range(R.d):
                functional=sum(((B[top+a]>>(R.m*j+k))&1)<<a for a in range(R.d))
                images.append(gram_solver(functional))
            coefficients=field_linear_solve(evaluation,images,R.h)
            if coefficients is None:raise ValueError('residue derivative is not ordinary field-quadratic')
            linear[i][j],M[i][j]=coefficients
    mu0=mu&R.mask
    if not mu0:raise ValueError('residue volume is not a unit')
    inverse=gf_pow(mu0,(1<<R.d)-2,R.h)
    center=[gf_mul(inverse,linear[1][2],R.h),gf_mul(inverse,linear[0][2],R.h),
            gf_mul(inverse,linear[0][1],R.h)]
    for i in range(3):
        for j in range(3):
            expected=0 if i==j else gf_mul(mu0,center[3-i-j],R.h)
            if linear[i][j]!=expected:raise ValueError('gradient has no translated homogeneous center')
        others=[j for j in range(3) if j!=i]
        value=constant[i]^gf_mul(mu0,gf_mul(center[others[0]],center[others[1]],R.h),R.h)
        for j in range(3):
            value^=gf_mul(M[i][j],gf_mul(center[j],center[j],R.h),R.h)
            value^=gf_mul(linear[i][j],center[j],R.h)
        if value:raise ValueError('manufactured center is not critical')
    certificate=macaulay_certificate(M,mu0,R.h)
    certificate.update(center=center,linear_coefficients=linear,constant_coefficients=constant)
    return center,certificate

def quadratic_coefficients(value,n):
    constant=value(0);singles=[value(1<<i)^constant for i in range(n)]
    Q={0} if constant else set()
    Q.update(1<<i for i,c in enumerate(singles) if c)
    for i,j in itertools.combinations(range(n),2):
        if value((1<<i)|(1<<j))^constant^singles[i]^singles[j]:Q.add((1<<i)|(1<<j))
    return Q

def state_value(R,mu,Q,x):
    mask=(1<<R.m)-1;values=[(x>>(R.m*i))&mask for i in range(3)]
    cubic=R.mul(mu,R.mul(values[0],R.mul(values[1],values[2])))
    return R.functional(cubic)^polynomial_value(Q,x)

def stationary_count_state(h,e,mu,Q,*,terminal_bit_budget=24):
    stages=[];multiplier=1
    while True:
        R=ChainRing(h,e);Q=set(Q)
        if e==1:
            if 3*R.d>terminal_bit_budget:raise ValueError('field terminal exceeds explicit enumeration budget')
            signed=sum(1-2*state_value(R,mu,Q,x) for x in range(1<<(3*R.d)))
            return multiplier*signed,dict(stages=stages,terminal='explicit field terminal',
                terminal_points=1<<(3*R.d),terminal_signed=signed,exact_multiplier=multiplier,
                walsh_leaves=0,branching_residue_points=0)
        center,certificate=residue_center(R,mu,Q)
        free_m=R.d*(e-1);free_n=3*free_m
        def restricted(y):
            x=0
            for i in range(3):
                yi=(y>>(free_m*i))&((1<<free_m)-1)
                x^=(center[i]^(yi<<R.d))<<(R.m*i)
            return state_value(R,mu,Q,x)
        if e<=3:
            # The restricted cubic is multiplied by t^3 and vanishes exactly.
            residual=quadratic_coefficients(restricted,free_n)
            signed=quadratic_sum(lambda y:polynomial_value(residual,y),free_n)
            certificate.update(depth=e,free_variables=free_n,quadratic_terms=len(residual))
            stages.append(certificate)
            return multiplier*signed,dict(stages=stages,terminal='exact binary quadratic elimination',
                terminal_points=0,terminal_signed=signed,exact_multiplier=multiplier,
                walsh_leaves=0,branching_residue_points=0)
        next_e=e-3;next_R=ChainRing(h,next_e);next_mu=mu&((1<<next_R.m)-1)
        small_mask=(1<<next_R.m)-1
        def compress(y):
            return sum(((y>>(free_m*i))&small_mask)<<(next_R.m*i) for i in range(3))
        def discrepancy(y):return restricted(y)^state_value(next_R,next_mu,set(),compress(y))
        residual=quadratic_coefficients(discrepancy,free_n)
        kept=sum(small_mask<<(free_m*i) for i in range(3))
        if any(term&~kept for term in residual):
            raise ValueError('restriction retains a variable in the two layers proposed for elimination')
        new_Q={compress(term) for term in residual}
        certificate.update(depth=e,next_depth=next_e,discarded_free_bits=6*R.d,
                           quadratic_terms=len(new_Q),exact_variable_elimination=True)
        stages.append(certificate);multiplier<<=6*R.d
        e,mu,Q=next_e,next_mu,new_Q

def compile_stationary(poly,n,*,terminal_bit_budget=24):
    started=time.perf_counter();acquired=acquire_chain(set(poly),n)
    if acquired['module_dimension']!=3:
        raise ValueError('requires a rank-three acquired chain module')
    cubic=acquired['cubic']
    if len(cubic)!=1 or cubic[0]['indices']!=[0,1,2]:raise AssertionError('missing volume coefficient')
    signed,certificate=stationary_count_state(acquired['h'],acquired['e'],cubic[0]['coefficient'],
        acquired['quadratic_remainder'],terminal_bit_budget=terminal_bit_budget)
    if abs(signed)>1<<n or ((1<<n)+signed)&1:raise AssertionError('invalid count')
    return dict(original_variables=n,raw_anf_terms=len(poly),field_degree=acquired['d'],
        chain_length=acquired['e'],field_modulus=acquired['h'],centroid_dimension=acquired['algebra_dimension'],
        coordinate_columns=acquired['coordinate_columns'],canonical_cubic=cubic,
        quadratic_remainder=acquired['quadratic_remainder'],certificate=certificate,
        signed_count=signed,zero_count=((1<<n)+signed)//2,seconds=time.perf_counter()-started)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--terminal-bit-budget',type=int,default=24)
    args=parser.parse_args();source=json.loads(args.input.read_text())
    result=compile_stationary(source['polynomial'],source['n'],terminal_bit_budget=args.terminal_bit_budget)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
