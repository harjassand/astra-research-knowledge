#!/usr/bin/env python3
"""Acquire a semisimple multiplier algebra to compress a large dual code.

The character space may have unbounded dimension and unbounded matrix rank.
Its actual left multipliers manufacture a unit map and field components.
Checked target-rank additivity permits polynomial rank-profile aggregation.
"""
from pathlib import Path
import argparse,json,sys,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from unsaturated_bilinear_counter import *
from adjoint_matrix_product_counter import linear_kernel


def remainder(span,value):
    for p,(row,word) in sorted(span.pivots.items(),reverse=True):
        if value>>p&1:value^=row
    return value


def acquire_semisimple_dual(certificate):
    begun=time.perf_counter();C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension']
    if U!=M:raise ValueError('this multiplier branch requires equal module dimensions')
    dual=certificate['dual_reverse_matrices'];c=len(dual)
    if not c:raise ValueError('zero dual needs no multiplier compression')
    DS=BinaryCoordinates(dual);Dmat=[rectangular_unpack(x,U,M) for x in dual]
    L=certificate['endomorphism_basis'][:];dimensions=[len(L)]
    for D in Dmat:
        images=[remainder(DS,pack(product(unpack(X,U),D),U)) for X in L]
        L=[apply_binary(L,v) for v in linear_kernel(images,U*M)];dimensions.append(len(L))
    LC=BinaryCoordinates(L);decoded=[unpack(x,U) for x in L];K=len(L)
    identity=pack([1<<j for j in range(U)],U);unit=LC.coordinates(identity)
    table=[[LC.coordinates(pack(product(A,B),U)) for B in decoded] for A in decoded]
    if any(table[i][j]!=table[j][i] for i in range(K) for j in range(i)):
        raise ValueError('actual dual multiplier algebra is not commutative')
    def mul(a,b):return apply_binary([apply_binary(row,b) for row in table],a)
    squares=[mul(1<<i,1<<i) for i in range(K)]
    if len(independent_basis(squares))!=K:raise ValueError('dual multiplier algebra has a nilpotent radical')
    fixed=linear_kernel([x^(1<<i) for i,x in enumerate(squares)],K);atoms=[unit]
    for e in fixed:
        refined=[]
        for f in atoms:
            a=mul(e,f);b=f^a
            if a:refined.append(a)
            if b:refined.append(b)
        atoms=refined
    if len(atoms)!=len(fixed):raise AssertionError('idempotents did not separate all field factors')
    pieces=[];unit_map=0;ap=C['field_degree']*C['left_matrix_rows']
    for e in atoms:
        projector=apply_binary(L,e);P=unpack(projector,U)
        field=independent_basis(mul(e,1<<j) for j in range(K))
        component=independent_basis(pack(product(P,D),U) for D in Dmat)
        if len(component)!=len(field):raise ValueError('dual component is not one copy of its multiplier field')
        selected=component[0];unit_map^=selected
        h,rem=divmod(len(independent_basis(P)),ap)
        if rem or not h:raise AssertionError('invalid component module multiplicity')
        pieces.append(dict(projector=projector,field_degree=len(field),rank=h,
            component_basis=component,selected_map=selected,
            dual_coordinate_basis=[DS.coordinates(x) for x in component]))
    if len(independent_basis(rectangular_unpack(unit_map,U,M)))!=U:
        raise ValueError('manufactured component sum is not an isomorphism')
    if sum(x['field_degree'] for x in pieces)!=c:raise AssertionError('components do not exhaust actual dual')
    if any(pack(product(unpack(x['projector'],U),rectangular_unpack(unit_map,U,M)),U)!=x['selected_map']
        for x in pieces):raise AssertionError('unit map has wrong component')
    return dict(components=pieces,multiplier_basis=L,multiplier_dimensions=dimensions,
        multiplier_dimension=K,component_count=len(pieces),codimension=c,
        manufactured_isomorphism=unit_map,unit_map_supplied=False,
        multiplier_frobenius_injective=True,field_elements_enumerated=0,
        seconds=time.perf_counter()-begun)


def compressed_semisimple_target(certificate,compression,target,affine_hom_offset=0):
    C=certificate['nucleus'];U=C['left_dimension'];M=C['output_dimension'];m=C['marked_quadratics']
    if type(target) is not int or target<0 or target.bit_length()>m:raise ValueError('invalid target')
    if type(affine_hom_offset) is not int or affine_hom_offset<0 or affine_hom_offset.bit_length()>len(certificate['hom_basis']):
        raise ValueError('invalid Hom offset')
    rhs=target^C['output_constant'];y=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['output_basis_mark_indices']))
    if any((row&y).bit_count()%2!=((rhs>>i)&1) for i,row in enumerate(C['marked_output_coordinates'])):
        return dict(population=0,reason='target violates actual affine output dependencies')
    a=C['field_degree'];p=C['left_matrix_rows'];d=C['inner_dimension'];r=C['right_matrix_columns'];ap=a*p
    actions=[unpack(x,U) for x in C['nucleus_input_operators']]
    def rank_vector(z):
        rank,rem=divmod(len(independent_basis(apply_binary(A,z) for A in actions)),ap)
        if rem:raise AssertionError('nonintegral target module rank')
        return rank
    z=apply_binary(rectangular_unpack(compression['manufactured_isomorphism'],U,M),y)
    k=rank_vector(z);local=[]
    for piece in compression['components']:
        zi=apply_binary(rectangular_unpack(piece['selected_map'],U,M),y);rho=rank_vector(zi)
        phase_nontrivial=any((apply_binary(certificate['right_annihilator_basis'],word)&affine_hom_offset).bit_count()%2
            for word in piece['dual_coordinate_basis'])
        weight=-1 if phase_nontrivial else (1<<piece['field_degree'])-1
        local.append(dict(rank=piece['rank'],target_rank=rho,nonzero_character_weight=weight))
    if sum(x['target_rank'] for x in local)!=k:
        raise ValueError('target component column spaces are not independent')
    histogram={(0,0):1}
    for item in local:
        updated=dict(histogram)
        for (t,rho),count in histogram.items():
            key=t+item['rank'],rho+item['target_rank']
            updated[key]=updated.get(key,0)+count*item['nonzero_character_weight']
        histogram=updated
    total=sum(count*signed_universal_product(p,d,r,a,k,t,rho) for (t,rho),count in histogram.items())
    answer,rem=divmod(total,1<<compression['codimension'])
    if rem or not 0<=answer<=1<<C['input_bits']:raise AssertionError('invalid reconstructed count')
    return dict(population=answer,matrix_target_rank=k,codimension=compression['codimension'],
        local_profiles=local,rank_pair_histogram={f'{t},{rho}':v for (t,rho),v in histogram.items()},
        histogram_states=len(histogram),characters_enumerated=0,
        target_component_rank_additivity_verified=True,original_assignments_enumerated=0)


def count_semisimple_dual_native(program):
    begun=time.perf_counter();n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:raise ValueError('explicit input-size admission failed')
    n,gates,output=validate_trace_program(program,n)
    reversible=acquire_reversible_terminal_and(program)
    split=acquire_source_free_bilinear_split(reversible['initial_quadratics'],n,
        allow_paired_components=True)
    certificate,split=acquire_best_hom_slice(split)
    compression=acquire_semisimple_dual(certificate);target=invert_terminal(reversible)
    fiber=compressed_semisimple_target(certificate,compression,target);ones=fiber['population']
    return dict(original_input_bits=n,ordinary_gates=len(gates),ones=ones,zeros=(1<<n)-ones,
        gap=(1<<n)-2*ones,target=target,fiber=fiber,compression_certificate=compression,
        slice_certificate=certificate,split_certificate=split,reversible_certificate=reversible,
        auxiliary_independent_inputs=0,original_assignments_enumerated=0,seconds=time.perf_counter()-begun)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args();out=json.dumps(count_semisimple_dual_native(json.loads(args.source.read_text())),indent=2)+'\n'
    if args.output:args.output.write_text(out)
    else:print(out,end='')


if __name__=='__main__':main()
