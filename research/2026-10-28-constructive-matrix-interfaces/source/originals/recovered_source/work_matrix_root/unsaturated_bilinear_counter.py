#!/usr/bin/env python3
"""Acquired simple-nucleus evaluation on a proper binary subspace of Hom.

Manufacture the full Hom space, its reverse trace pairing, and the actual
annihilator of the right input.  Sum only 2**codimension characters.  Each
weighted product fiber is evaluated by three acquired ranks and a polynomial
Gaussian-binomial formula, without constructing field elements or matrix units.
"""
from pathlib import Path
import argparse,json,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path[:0]=[str(HERE),str(ROOT/'work_multiprimary_audit')]
from raw_bilinear_product_counter import *
from source_free_bilinear_split import acquire_source_free_bilinear_split,sparse_kernel


def rectangular_unpack(value,rows,columns):
    return [(value>>(rows*j))&((1<<rows)-1) for j in range(columns)]


def hom_space(source_operators,target_operators,source_dimension,target_dimension):
    """Acquire all actual binary matrices T with T A_i=C_i T."""
    U=source_dimension;M=target_dimension
    if len(source_operators)!=len(target_operators):raise ValueError('different generator labels')
    def equations():
        for aa,cc in zip(source_operators,target_operators):
            A=unpack(aa,U);C=unpack(cc,M)
            rows=[sum(((C[j]>>b)&1)<<j for j in range(M)) for b in range(M)]
            for a in range(U):
                spread=sum(((A[a]>>j)&1)<<(M*j) for j in range(U))
                for b in range(M):yield (spread<<b)^(rows[b]<<(M*a))
    return sparse_kernel(equations(),U*M)


def signed_universal_product(p,d,r,a,k,t,rho):
    """Sum_{XY=C} (-1)^Tr(DY), from ranks C,D,CD.

    Here X:p*d, Y:d*r, D:r*d. This is kernel-lattice Mobius inversion.
    All arithmetic is exact and all exponents are nonnegative.
    """
    if not (0<=k<=min(p,r) and 0<=t<=min(d,r) and
            max(0,k+t-r)<=rho<=min(k,t)):
        raise ValueError('inconsistent matrix-pair ranks')
    w=t-rho;answer=0
    for h in range(max(0,r-d),r-k+1):
        for ell in range(max(0,h-(r-k-w),h+t-r),min(h,w)+1):
            intersection_count=gaussian_binomial(w,ell,a)*gaussian_binomial(r-k-w,h-ell,a)
            exponent=(w-ell)*(h-ell)+p*(d-r+h)+(t-ell)*(t-ell-1)//2
            term=intersection_count*(1<<(a*exponent))
            for j in range(r-h-t+ell):term*=((1<<(a*d))-(1<<(a*(t-ell+j))))
            answer+=(-term if (t-ell)%2 else term)
    return answer


def acquire_hom_slice(split):
    begun=time.perf_counter();C=acquire_left_product_nucleus(split,require_saturated=False)
    U=C['left_dimension'];M=C['output_dimension'];V=C['right_dimension']
    A=C['nucleus_input_operators'];O=C['nucleus_output_operators']
    H,hm=hom_space(A,O,U,M);R,rm=hom_space(O,A,M,U);E,em=hom_space(A,A,U,U)
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];r=C['right_matrix_columns']
    if len(H)!=a*d*r or len(R)!=a*d*r or len(E)!=a*d*d:
        raise AssertionError('acquired module hom spaces have incompatible dimensions')
    HC=BinaryCoordinates(H);EC=BinaryCoordinates(E)
    EE=[unpack(e,U) for e in E]
    commutators=[(EC.coordinates(pack(product(x,y),U)^pack(product(y,x),U)),0)
        for i,x in enumerate(EE) for y in EE[:i]]
    trace_space=affine_solutions(commutators,len(E))[1]
    if len(trace_space)!=a:raise AssertionError('Morita endomorphism trace-space dimension')
    tau=trace_space[0]
    def trace(packed):return (tau&EC.coordinates(packed)).bit_count()%2
    HH=[rectangular_unpack(h,M,U) for h in H]
    RR=[rectangular_unpack(z,U,M) for z in R]
    pairing_columns=[sum(trace(pack(product(z,h),U))<<i for i,h in enumerate(HH)) for z in RR]
    PC=BinaryCoordinates(pairing_columns)
    if len(PC.basis)!=len(H):raise AssertionError('reverse-Hom trace pairing is degenerate')
    forms=[split['cross_matrices'][j] for j in C['output_basis_mark_indices']]
    embedded=[]
    for j in range(V):
        columns=[sum(((f[j]>>i)&1)<<b for b,f in enumerate(forms)) for i in range(U)]
        embedded.append(HC.coordinates(pack(columns,M)))
    if len(independent_basis(embedded))!=V:raise AssertionError('right embedding is not injective')
    dual=affine_solutions([(v,0) for v in embedded],len(H))[1]
    reverse_dual=[apply_binary(R,PC.coordinates(lam)) for lam in dual]
    return dict(nucleus=C,hom_basis=H,reverse_hom_basis=R,
        endomorphism_basis=E,trace_functional=tau,trace_space_dimension=a,
        right_embedding_columns=embedded,right_annihilator_basis=dual,
        dual_reverse_matrices=reverse_dual,codimension=len(dual),
        hom_acquisition=hm,reverse_hom_acquisition=rm,endomorphism_acquisition=em,
        trace_pairing_nondegenerate=True,canonical_field_or_matrix_units_constructed=False,
        seconds=time.perf_counter()-begun)


def transpose_split(split):
    """Swap the two manufactured halves; no extra decomposition is guessed."""
    U=split['left_dimension'];V=split['right_dimension'];C=dict(split)
    C['left_dimension']=V;C['right_dimension']=U
    C['coordinate_columns']=split['coordinate_columns'][U:]+split['coordinate_columns'][:U]
    C['cross_matrices']=[list(x) for x in split['cross_rows']]
    C['cross_rows']=[list(x) for x in split['cross_matrices']]
    C['centered_quadratics']=[sorted((x>>U)|((x&((1<<U)-1))<<V) for x in f)
        for f in split['centered_quadratics']]
    C['central_idempotent_columns']=split['adjoint_of_idempotent_columns']
    C['adjoint_of_idempotent_columns']=split['central_idempotent_columns']
    C['halves_swapped']=not split.get('halves_swapped',False)
    if 'left_linear_output_columns' in split:
        C['left_linear_output_columns']=split['right_linear_output_columns'][:]
        C['right_linear_output_columns']=split['left_linear_output_columns'][:]
    return C


def acquire_best_hom_slice(split):
    accepted=[];declines=[]
    for oriented in (split,transpose_split(split)):
        try:certificate=acquire_hom_slice(oriented)
        except ValueError as error:
            declines.append(str(error));continue
        accepted.append((certificate,oriented))
    if not accepted:raise ValueError('neither acquired orientation has a simple nucleus: '+'; '.join(declines))
    certificate,oriented=min(accepted,key=lambda pair:pair[0]['codimension'])
    certificate['orientations_examined']=2;certificate['orientation_declines']=declines
    return certificate,oriented


def slice_target_fiber(certificate,target,affine_hom_offset=0):
    """An optional offset is in the acquired full-Hom binary coordinates."""
    C=certificate['nucleus'];m=C['marked_quadratics'];U=C['left_dimension'];M=C['output_dimension']
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(certificate['hom_basis']):
        raise ValueError('invalid acquired Hom-space offset')
    rhs=target^C['output_constant']
    y=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['output_basis_mark_indices']))
    if any((row&y).bit_count()%2!=((rhs>>i)&1) for i,row in enumerate(C['marked_output_coordinates'])):
        return dict(population=0,reason='target violates actual affine output dependencies')
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];r=C['right_matrix_columns']
    input_actions=[unpack(x,U) for x in C['nucleus_input_operators']]
    output_actions=[unpack(x,M) for x in C['nucleus_output_operators']]
    k,remainder=divmod(len(independent_basis(apply_binary(x,y) for x in output_actions)),a*p)
    if remainder:raise AssertionError('target orbit has fractional rank')
    total=0;profiles={};c=certificate['codimension'];dual=certificate['right_annihilator_basis']
    for word in range(1<<c):
        D=rectangular_unpack(apply_binary(certificate['dual_reverse_matrices'],word),U,M)
        t,rem1=divmod(len(independent_basis(D)),a*p)
        Dy=apply_binary(D,y)
        rho,rem2=divmod(len(independent_basis(apply_binary(x,Dy) for x in input_actions)),a*p)
        if rem1 or rem2:raise AssertionError('dual module ranks are not integral')
        phase=(apply_binary(dual,word)&affine_hom_offset).bit_count()%2
        value=signed_universal_product(p,d,r,a,k,t,rho)
        total+=(-value if phase else value)
        key=f'{t},{rho},{phase}';profiles[key]=profiles.get(key,0)+1
    answer,remainder=divmod(total,1<<c)
    if remainder or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid exact slice population')
    return dict(population=answer,target_output_coordinates=y,matrix_target_rank=k,
        codimension=c,characters_evaluated=1<<c,rank_pair_profiles=profiles,
        universal_fiber_signed_sum=total,original_assignments_enumerated=0)


def count_unsaturated_native(program):
    begun=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('zero-common-radical admission requires every input in the explicit DAG')
    n,gates,output=validate_trace_program(program,n)
    reversible=acquire_reversible_terminal_and(program)
    split=acquire_source_free_bilinear_split(reversible['initial_quadratics'],n)
    C,split=acquire_best_hom_slice(split);target=invert_terminal(reversible);fiber=slice_target_fiber(C,target)
    count=fiber['population']
    return dict(original_input_bits=n,ordinary_gates=len(gates),ones=count,zeros=(1<<n)-count,
        gap=(1<<n)-2*count,target=target,fiber=fiber,split_certificate=split,
        slice_certificate=C,reversible_certificate=reversible,auxiliary_independent_inputs=0,
        original_assignments_enumerated=0,seconds=time.perf_counter()-begun)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_unsaturated_native(json.loads(args.source.read_text()));text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')


if __name__=='__main__':main()
