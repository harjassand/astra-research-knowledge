#!/usr/bin/env python3
"""Acquire a hidden quadratic defect from a manufactured scalar orbit.

All matrices use binary column lists. The raw input polar matrix is symmetric,
so its row list is also its column list. This is a support-product decoder,
with ancestry in LRPC rank-support recovery; it is not a new rank-metric code.
The new interface manufactures its syndrome directly from a field-band matrix.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'work_field_root'))
from field_bandwidth import *
from field_kloosterman import irreducible_binary


def independent(columns):
    piv=span(columns)
    return [value[0] for _,value in sorted(piv.items())]


def intersection(a,b):
    a=independent(a); b=independent(b)
    relations=kernel_columns(a+b)
    return independent(linear_apply(a,z&((1<<len(a))-1)) for z in relations)


def solve_with_pivots(piv,target):
    result=0
    while target:
        k=(target&-target).bit_length()-1
        if k not in piv: return None
        target^=piv[k][0]; result^=piv[k][1]
    return result


def block_apply(columns,x,width,blocks):
    mask=(1<<width)-1
    return sum(linear_apply(columns,(x>>(width*j))&mask)<<(width*j) for j in range(blocks))


def scalar_vector(c,x,h,b):
    d=h.bit_length()-1; mask=(1<<d)-1
    return sum(gf_mul(c,(x>>(d*j))&mask,h)<<(d*j) for j in range(b))


def scalar_matrix(c,h,b):
    d=h.bit_length()-1
    local=[gf_mul(c,1<<j,h) for j in range(d)]
    return [v<<(i*d) for i in range(b) for v in local]


def band_operator(L,h,b,coefficients,a):
    n=len(L); powers=[1]
    for _ in range(len(coefficients)-1): powers.append(gf_mul(powers[-1],a,h))
    result=[0]*n
    for c,power in zip(coefficients,powers):
        if not c: continue
        right=scalar_matrix(power,h,b)
        result=[x^scalar_vector(c,linear_apply(L,y),h,b) for x,y in zip(result,right)]
    return result


def certificate_operator(L,h,b,certificate):
    if certificate.get('operator')!='selfadjoint bandwidth one':
        return band_operator(L,h,b,certificate['coefficients'],certificate['a'])
    result=[0]*len(L)
    for left,right in zip(certificate['coefficients'],certificate['operator_right']):
        R=scalar_matrix(right,h,b)
        result=[x^scalar_vector(left,linear_apply(L,y),h,b) for x,y in zip(result,R)]
    return result


def selfadjoint_scalar_certificate(h):
    d=h.bit_length()-1
    if not irreducible_binary(h): raise ValueError('reducible field modulus')
    if d<7: raise ValueError('selfadjoint scalar certificate requires field degree at least seven')
    z=2; z2=gf_mul(z,z,h); z3=gf_mul(z,z2,h); z4=gf_mul(z2,z2,h)
    p=z^z2; q=z^z3; C=[1,z4,p,q]
    cC=[gf_mul(p,x,h) for x in C]
    if len(span(C))!=4 or len(intersection(C,cC))!=1 or solve(intersection(C,cC),p) is None:
        raise ValueError('selfadjoint scalar certificate failed')
    S=independent(C+cC)
    assert len(S)==7
    return dict(z=z,a=z,c=p,coefficients=C,operator_right=[z4,1,q,p],
        operator='selfadjoint bandwidth one',deconvolution_block=1,
        scalar_support=C,scalar_orbit_basis=S,scalar_orbit_dimension=7,
        field_degree=d,frobenius_bandwidth=1,polynomial_degree_sufficient_bound=7,
        generator_trials=1,bounded_small_field_search=False)


def _scalar_certificate_for_generator(h,bandwidth,z):
    d=h.bit_length()-1
    if not irreducible_binary(h): raise ValueError('reducible field modulus')
    if not isinstance(bandwidth,int) or bandwidth<1 or 2*bandwidth>=d:
        raise ValueError('requires 1 <= bandwidth < field degree / 2')
    if any(gf_pow(z,1<<(d//prime),h)==z for prime,_ in prime_powers(d)):
        raise ValueError('chosen scalar does not generate the full field')
    a=gf_pow(z,1<<bandwidth,h); roots=[]
    coefficients=[1]
    for j in range(2*bandwidth+1):
        root=gf_pow(z,1<<j,h); roots.append(root)
        new=[0]*(len(coefficients)+1)
        for i,value in enumerate(coefficients):
            new[i]^=gf_mul(root,value,h); new[i+1]^=value
        coefficients=new
    if len(set(roots))!=len(roots): raise ValueError('Frobenius roots collided')
    k=len(roots); c=coefficients[-2]
    C=independent(coefficients)
    if len(C)!=k+1: raise ValueError('scalar annihilator coefficients dependent')
    cC=[gf_mul(c,x,h) for x in C]
    overlap=intersection(C,cC)
    if len(overlap)!=1 or solve(overlap,c) is None:
        raise ValueError('scalar support intersection larger than intended')
    powers=[1]
    for _ in range(k): powers.append(gf_mul(powers[-1],a,h))
    if len(span(powers))!=k+1: raise ValueError('right scalar powers dependent')
    S=independent(C+cC+powers)
    return dict(z=z,a=a,c=c,roots=roots,coefficients=coefficients,
        operator='one-sided general bandwidth',deconvolution_block=0,
        scalar_support=C,scalar_orbit_basis=S,scalar_orbit_dimension=len(S),
        field_degree=d,frobenius_bandwidth=bandwidth,
        polynomial_degree_sufficient_bound=3*(1<<(2*bandwidth)))


def scalar_certificate(h,bandwidth=1,*,method='auto'):
    """Default selfadjoint bandwidth-one certificate; preserve the first route.

    ``method='one_sided'`` reproduces the older coefficient-power operator.
    Only that legacy route uses a bounded search in degrees7 through11.
    The primary selfadjoint operator uses z=X for every d>=7.
    """
    d=h.bit_length()-1
    if method not in ('auto','selfadjoint','one_sided'): raise ValueError('unknown operator method')
    if method=='selfadjoint' and bandwidth!=1: raise ValueError('selfadjoint method implemented for bandwidth one')
    if method=='selfadjoint' or (method=='auto' and bandwidth==1): return selfadjoint_scalar_certificate(h)
    candidates=range(2,1<<d) if bandwidth==1 and 7<=d<=11 else [2]
    first_failure=None
    for trial,z in enumerate(candidates,1):
        try: cert=_scalar_certificate_for_generator(h,bandwidth,z)
        except ValueError as error:
            if first_failure is None: first_failure=error
            continue
        cert['generator_trials']=trial
        cert['bounded_small_field_search']=trial>1
        return cert
    raise first_failure or ValueError('no scalar certificate')


def recover_band_coefficients(B,h,bandwidth):
    d=h.bit_length()-1; n=len(B); b=n//d; gram=trace_gram(h)
    gram_piv=span(gram); certificates=[]
    k=2*bandwidth+1
    evaluation=[]
    for j in range(d):
        x=1<<j; row=[]
        for _ in range(k): row.append(x); x=gf_mul(x,x,h)
        evaluation.append(row)
    for i in range(b):
        for j in range(b):
            local=[]
            for col in range(d):
                functional=(B[j*d+col]>>(i*d))&((1<<d)-1)
                local.append(solve_with_pivots(gram_piv,functional))
            received=[linear_apply(local,gf_pow(1<<v,1<<bandwidth,h)) for v in range(d)]
            decoded=field_linear_solve(evaluation,received,h)
            if decoded is None or any(linearized_value(decoded,1<<v,h)!=received[v] for v in range(d)):
                raise ValueError('recovered base is outside the Frobenius band')
            certificates.append(dict(row_block=i,column_block=j,decoded_coefficients=decoded,
                frobenius_bandwidth=bandwidth,method='manufactured Sylvester support'))
    return certificates


def acquire_sylvester_base(B,h,bandwidth=1,*,method='auto'):
    """B alone is the quadratic input; no error, support or rank is supplied.

    Success is a verified exact band + alternating defect decomposition.
    The direct scalar-orbit condition in the proof guarantees planted recovery.
    A failed support test rejects; no exhaustive fallback is hidden here.
    """
    start=time.perf_counter(); n=len(B); d=h.bit_length()-1
    if not n or n%d: raise ValueError('incomplete field blocks')
    if any(not isinstance(x,int) or x<0 or x>>n for x in B): raise ValueError('invalid binary matrix')
    if any(x>>i&1 for i,x in enumerate(B)) or any((B[i]>>j^B[j]>>i)&1 for i in range(n) for j in range(i)):
        raise ValueError('input polar matrix must be alternating')
    b=n//d; cert=scalar_certificate(h,bandwidth,method=method); gram=trace_gram(h)
    gram_inv=[solve(gram,1<<j) for j in range(d)]
    L=[block_apply(gram_inv,x,d,b) for x in B]
    H=certificate_operator(L,h,b,cert)
    W=independent(H)
    if not W:
        base=B[:]; defect=[0]*n
        cert.update(manufactured_syndrome_rank=0,recovered_support=[],recovered_rank=0,
            recovered_orbit_rank=0,seconds=time.perf_counter()-start)
        return base,defect,recover_band_coefficients(base,h,bandwidth),cert
    k=len(cert['coefficients'])-1
    if len(W)%(k+1): raise ValueError('syndrome rank is not the promised scalar expansion')
    cW=[scalar_vector(cert['c'],w,h,b) for w in W]
    cU=intersection(W,cW)
    cinverse=gf_pow(cert['c'],(1<<d)-2,h)
    U=independent(scalar_vector(cinverse,w,h,b) for w in cU)
    r=len(U)
    if len(W)!=(k+1)*r: raise ValueError('support intersection has incompatible dimension')
    S=cert['scalar_orbit_basis']
    expanded=[scalar_vector(s,u,h,b) for s in S for u in U]
    if len(span(expanded))!=len(S)*r: raise ValueError('recovered scalar orbit is not direct')
    CU=[scalar_vector(c,u,h,b) for c in cert['coefficients'] for u in U]
    piv=span(CU)
    if len(piv)!=(k+1)*r: raise ValueError('recovered coefficient orbit is not direct')
    coordinates=[solve_with_pivots(piv,column) for column in H]
    if any(x is None for x in coordinates): raise ValueError('syndrome leaves the manufactured support')
    # The chosen left-support block has right scalar 1, so is K U^*.
    block_shift=cert['deconvolution_block']*r
    E=[linear_apply(U,(x>>block_shift)&((1<<r)-1)) for x in coordinates]
    defect=[block_apply(gram,x,d,b) for x in E]
    base=[x^y for x,y in zip(B,defect)]
    if any(defect[i]>>i&1 for i in range(n)) or any((defect[i]>>j^defect[j]>>i)&1 for i in range(n) for j in range(i)):
        raise ValueError('recovered defect is not alternating')
    if len(span(defect))!=r: raise ValueError('recovered defect rank inconsistent')
    if certificate_operator([x^y for x,y in zip(L,E)],h,b,cert)!=[0]*n:
        raise ValueError('recovered base does not annihilate')
    decoding=recover_band_coefficients(base,h,bandwidth)
    cert.update(manufactured_syndrome_rank=len(W),recovered_support=U,recovered_rank=r,
        recovered_orbit_rank=len(S)*r,seconds=time.perf_counter()-start)
    return base,defect,decoding,cert


def acquire_sylvester_trace_form(poly,n,*,bandwidth=1,method='auto'):
    """Raw ANF -> acquired field, acquired defect, exact trace representative."""
    if not isinstance(n,int) or n<1 or any(not isinstance(x,int) or x<0 or x>>n or x.bit_count()>3 for x in poly):
        raise ValueError('input must be an explicit Boolean cubic ANF')
    start=time.perf_counter(); algebra,pair,trail=centroid(poly,n)
    h,columns,module_basis=acquire_field(algebra,n)
    d=h.bit_length()-1; b=len(module_basis); gram=trace_gram(h)
    B=quadratic_matrix(poly,n,columns)
    base,defect,decoding,cert=acquire_sylvester_base(B,h,bandwidth,method=method)
    result=quadratic_trace_representative(decoding,h,b,bandwidth)
    for i,j,k in itertools.combinations(range(b),3):
        functional=sum(tensor_value(pair,columns[i*d+t],columns[j*d],columns[k*d])<<t for t in range(d))
        coefficient=solve(gram,functional); assert coefficient is not None
        exponent=[0]*b; exponent[i]=exponent[j]=exponent[k]=1
        if coefficient: result[tuple(exponent)]=coefficient
    constant=polynomial_value(poly,0)
    for i in range(b):
        target=0
        for t in range(d):
            point=[0]*b; point[i]=1<<t
            discrepancy=polynomial_value(poly,columns[i*d+t])^constant^gf_trace(field_polynomial_value(result,point,h),h)
            target|=discrepancy<<t
        coefficient=solve(gram,target)
        if coefficient:
            exponent=tuple(int(j==i) for j in range(b)); result[exponent]=result.get(exponent,0)^coefficient
    if constant: result[(0,)*b]=next(1<<i for i in range(d) if gf_trace(1<<i,h))
    factors,linear=symplectic_factors(defect)
    return dict(original_variables=n,raw_polynomial=sorted(poly),field_modulus=h,
        field_extension_degree=d,module_dimension=b,frobenius_bandwidth=bandwidth,
        certified_field_degree=max(3,(1<<bandwidth)+1),centroid_dimension=len(algebra),
        centroid_kernel_dimensions=trail,coordinate_columns=columns,quadratic_matrix=B,
        acquired_field_quadratic=base,acquired_defect=defect,acquired_defect_rank=len(factors),
        symplectic_factors=factors,linear_correction=linear,decoding=decoding,support_certificate=cert,
        field_polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(result.items()) if c],
        seconds=time.perf_counter()-start,
        count_backend_executed=False)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('input'); parser.add_argument('--output',required=True)
    parser.add_argument('--bandwidth',type=int,default=1)
    parser.add_argument('--operator',choices=['auto','selfadjoint','one_sided'],default='auto')
    args=parser.parse_args(); source=json.loads(Path(args.input).read_text())
    result=acquire_sylvester_trace_form(set(source['polynomial_masks']),source['n'],bandwidth=args.bandwidth,method=args.operator)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['original_variables','field_extension_degree','module_dimension','acquired_defect_rank','seconds']}))
