#!/usr/bin/env python3
"""Exact affine character aggregation by two acquired kernel moments.

For the same certified one-copy target family as noncommutative_dual_counter,
an arbitrary affine Hom offset is handled without enumerating any dual matrix.
The rank and target-intersection invariants of its character are acquired from
actual left-module actions and the kernel of evaluation at the actual target.
"""
from pathlib import Path
import argparse,json,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path[:0]=[str(HERE),str(ROOT/'work_matrix_root'),str(ROOT/'work_multiprimary_audit')]
from noncommutative_dual_counter import *
from affine_unsaturated_bilinear_counter import acquire_best_affine_hom_slice


def signed_projected_rank_histogram(s,k,a,t,w):
    """sum_A (-1)^Tr(tr(BA)) by rank A and rank(A|E).

    dim E=k, rank B=t, dim(E intersect im B)=w. Character orthogonality
    determines two Gaussian-binomial moments, inverted by finite triangular
    elimination. No matrices or subspaces are enumerated.
    """
    if not (0<=k<=s and 0<=t<=s and max(0,k+t-s)<=w<=min(k,t)):
        raise ValueError('invalid phase/target subspace dimensions')
    gb={(n,j):gaussian_binomial(n,j,a) for n in range(s+1) for j in range(n+1)}
    def choose(n,j):return gb.get((n,j),0)
    moments={}
    for h in range(s+1):
        for x in range(k+1):
            value=0
            for u in range(max(0,x-(k-w)),min(x,w)+1):
                choose_K=choose(w,u)*choose(k-w,x-u)*(1<<(a*(w-u)*(x-u)))
                for v in range(max(0,h+x-s),min(h,x)+1):
                    image=choose(s-x-t+u,h-v-t+u)
                    if not image:continue
                    exponent=(h-v)*(x-v)+s*(s-h-x+v)
                    value+=choose_K*choose(x,v)*image*(1<<(a*exponent))
            moments[h,x]=value
    kernels={}
    for h in range(s,-1,-1):
        for x in range(k,-1,-1):
            value=moments[h,x]
            for n in range(h,s+1):
                for z in range(x,k+1):
                    if (n,z)==(h,x):continue
                    value-=choose(n,h)*choose(z,x)*kernels.get((n,z),0)
            kernels[h,x]=value
    histogram={(s-h,k-x):value for (h,x),value in kernels.items() if value}
    if any(not (0<=rho<=min(k,j) and j-rho<=s-k) for j,rho in histogram):
        raise AssertionError('signed rank histogram has an impossible rank pair')
    if histogram.get((0,0))!=1:raise AssertionError('zero matrix has incorrect character weight')
    if sum(histogram.values())!=(1<<(a*s*s) if not t else 0):
        raise AssertionError('signed rank histogram has incorrect total character sum')
    return histogram


def acquire_phase_target_invariants(certificate,compression,y,affine_hom_offset):
    C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension']
    a=C['field_degree'];s=compression['matrix_degree'];dual=certificate['dual_reverse_matrices']
    DS=BinaryCoordinates(dual);matrices=[rectangular_unpack(D,U,M) for D in dual]
    phase=sum(((lam&affine_hom_offset).bit_count()%2)<<j
        for j,lam in enumerate(certificate['right_annihilator_basis']))
    orbit=[]
    for A in compression['multiplier_basis']:
        AA=unpack(A,U)
        orbit.append(sum(((DS.coordinates(pack(product(AA,D),U))&phase).bit_count()%2)<<j
            for j,D in enumerate(matrices)))
    t,rem=divmod(len(independent_basis(orbit)),a*s)
    if rem:raise AssertionError('phase orbit has nonintegral matrix rank')
    target_kernel=linear_kernel([apply_binary(D,y) for D in matrices],U)
    restricted=[sum(((ell&v).bit_count()%2)<<j for j,v in enumerate(target_kernel)) for ell in orbit]
    projected,rem=divmod(len(independent_basis(restricted)),a*s)
    if rem:raise AssertionError('restricted phase orbit has nonintegral rank')
    return dict(phase_rank=t,phase_image_target_intersection=t-projected,
        target_evaluation_kernel_dimension=len(target_kernel),
        phase_orbit_dimension=a*s*t,restricted_phase_orbit_dimension=a*s*projected,
        phase_zero=(phase==0),phase_and_target_matrices_supplied=False)


def compressed_noncommutative_affine_target(certificate,compression,target,affine_hom_offset=0):
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(certificate['hom_basis']):
        raise ValueError('invalid acquired Hom offset')
    base=compressed_noncommutative_target(certificate,compression,target)
    if 'reason' in base:return base
    C=certificate['nucleus'];a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension']
    m=C['marked_quadratics'];s=compression['matrix_degree'];h=compression['natural_multiplicity']
    rhs=target^C['output_constant'];y=sum(((rhs>>j)&1)<<i for i,j in enumerate(C['output_basis_mark_indices']))
    phase=acquire_phase_target_invariants(certificate,compression,y,affine_hom_offset)
    k=base['matrix_target_rank']
    if phase['target_evaluation_kernel_dimension']!=a*s*(s-k):
        raise AssertionError('target kernel has wrong one-copy module dimension')
    if phase['phase_zero']:return dict(base,acquired_phase_target_invariants=phase)
    histogram={(h*j,rho):weight for (j,rho),weight in signed_projected_rank_histogram(
        s,k,a,phase['phase_rank'],phase['phase_image_target_intersection']).items()}
    total=sum(weight*signed_universal_product(p,d,d,a,k,t,rho) for (t,rho),weight in histogram.items())
    answer,rem=divmod(total,1<<compression['codimension'])
    if rem or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid acquired affine-slice population')
    return dict(base,population=answer,acquired_phase_target_invariants=phase,
        rank_pair_histogram={f'{t},{rho}':v for (t,rho),v in histogram.items()},
        histogram_states=len(histogram),affine_phase_moment_inversion=True,
        matrices_or_subspaces_enumerated=0)


def count_noncommutative_affine_native(program):
    began=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('explicit input-size admission failed')
    n,gates,output=validate_trace_program(program,n);reversible=acquire_reversible_terminal_and(program)
    C,split=acquire_best_affine_hom_slice(reversible['initial_quadratics'],n)
    compression=acquire_noncommutative_dual(C);target=invert_terminal(reversible)
    fiber=compressed_noncommutative_affine_target(C,compression,target,C['affine_hom_offset']);ones=fiber['population']
    return dict(original_input_bits=n,ordinary_gates=len(gates),ones=ones,zeros=(1<<n)-ones,
        gap=(1<<n)-2*ones,target=target,fiber=fiber,compression_certificate=compression,
        affine_slice_certificate=C,split_certificate=split,reversible_certificate=reversible,
        auxiliary_independent_inputs=0,original_assignments_enumerated=0,seconds=time.perf_counter()-began)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_noncommutative_affine_native(json.loads(args.source.read_text()));text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
