#!/usr/bin/env python3
"""Acquire matrix-product fibers from an adjoint-paired quadratic algebra.

No matrix dimensions, basis, product map, or target rank are supplied.
This is a recognized family, not arbitrary polynomial #SAT.
"""
from pathlib import Path
from math import isqrt
import argparse,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_multiprimary_audit','work_trace_frontier','work_matrix_root')]
from central_quadratic_tensor_compiler import (pack,unpack,product,transpose,
    algebra_basis,apply_binary,polar_rows,affine_solutions,linear_kernel,
    independent_basis,compose_quadratic,quadratic_gap)
from raw_trace_circuit_compiler import CubicGateTable
from projector_quadratic_fibers import (acquire_reversible_terminal_and,
    invert_terminal,validate_trace_program)
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)


class BinaryCoordinates:
    def __init__(self,values=()):
        self.pivots={};self.basis=[]
        for value in values:self.insert(value)
    def insert(self,value):
        reduced=value;coordinates=0
        while reduced:
            j=reduced.bit_length()-1
            if j in self.pivots:
                old,label=self.pivots[j];reduced^=old;coordinates^=label
            else:
                index=len(self.basis);self.basis.append(value)
                self.pivots[j]=(reduced,coordinates^(1<<index));return index
        return None
    def coordinates(self,value):
        result=0
        while value:
            j=value.bit_length()-1
            if j not in self.pivots:raise ValueError('vector lies outside the acquired span')
            old,label=self.pivots[j];value^=old;result^=label
        return result


def gaussian_binomial(n,k,field_degree=1):
    if not 0<=k<=n:return 0
    numerator=denominator=1
    for j in range(k):
        numerator*=((1<<(field_degree*(n-j)))-1)
        denominator*=((1<<(field_degree*(k-j)))-1)
    answer,remainder=divmod(numerator,denominator)
    if remainder:raise AssertionError('nonintegral Gaussian binomial')
    return answer


def matrix_product_fiber_population(t,d,k,field_degree=1):
    if min(t,d)<k:return 0
    total=0
    for r in range(k,min(t,d)+1):
        onto=1
        for j in range(r):onto*=((1<<(field_degree*d))-(1<<(field_degree*j)))
        total+=gaussian_binomial(t-k,r-k,field_degree)*onto*(1<<(field_degree*t*(d-r)))
    if not 0<=total<=1<<(2*field_degree*t*d):raise AssertionError('invalid product fiber population')
    return total


def acquire_adjoint_product_algebra(source_anf,quadratics,n):
    begun=time.perf_counter();source=set(source_anf);marks=list(map(set,quadratics));m=len(marks)
    if n<4 or n%2:raise ValueError('an even nontrivial source space is required')
    if any(a<0 or a.bit_length()>n or a.bit_count()>2 for f in [source]+marks for a in f):
        raise ValueError('explicit Boolean quadratics required')
    B=polar_rows(source,n);inverse=[]
    for i in range(n):
        solved=affine_solutions([(row,int(j==i)) for j,row in enumerate(B)],n)
        if solved is None or solved[1]:raise ValueError('nonsingular source polar required')
        inverse.append(solved[0])
    operators=[product(inverse,polar_rows(f,n)) for f in marks]
    algebra,products=algebra_basis(operators,n);width=n*n;commutators=[]
    for value in algebra:
        A=unpack(value,n);image=0
        for j,G in enumerate(operators):
            image|=(pack(product(A,G),n)^pack(product(G,A),n))<<(width*j)
        commutators.append(image)
    center=[apply_binary(algebra,c) for c in linear_kernel(commutators,width*m)]
    if len(center)<2 or len(center)%2:
        raise ValueError('this route requires one adjoint-exchanged central pair')
    frobenius=[pack(product(unpack(z,n),unpack(z,n)),n)^z for z in center]
    idempotents=[apply_binary(center,c) for c in linear_kernel(frobenius,width)]
    if len(idempotents)!=2:raise ValueError('the center does not have exactly two field factors')
    identity=[1<<i for i in range(n)];I=pack(identity,n)
    candidate=next((z for z in idempotents if z and z!=I),None)
    if candidate is None:raise AssertionError('split center supplied no proper idempotent')
    E=unpack(candidate,n);adjoint=product(inverse,product(transpose(E),B))
    complement=[x^y for x,y in zip(identity,E)]
    if adjoint!=complement or product(E,E)!=E:
        raise ValueError('central factors are not exchanged by the source adjoint')
    left=independent_basis(E);right=independent_basis(complement);D=len(left)
    if D!=len(right) or 2*D!=n:raise AssertionError('adjoint pair has inconsistent dimensions')
    coordinates=BinaryCoordinates(left+right)
    if len(coordinates.basis)!=n:raise AssertionError('paired coordinates are not invertible')
    for half in (left,right):
        if any((x&apply_binary(B,y)).bit_count()%2 for x in half for y in half):
            raise AssertionError('acquired half is not source-isotropic')
    restricted=[]
    for A in operators:
        columns=[coordinates.coordinates(apply_binary(A,x)) for x in left]
        if any(x.bit_length()>D for x in columns):raise AssertionError('central half not invariant')
        restricted.append(pack(columns,D))
    S=BinaryCoordinates();basis_indices=[]
    for i,value in enumerate(restricted):
        if S.insert(value) is not None:basis_indices.append(i)
    K=len(S.basis);unit_coordinates=S.coordinates(pack([1<<i for i in range(D)],D))
    decoded=[unpack(a,D) for a in S.basis];multiplication=[]
    for A in decoded:
        multiplication.append([S.coordinates(pack(product(A,C),D)) for C in decoded])
    def multiply(a,b):return apply_binary([apply_binary(row,b) for row in multiplication],a)
    center_images=[sum((multiplication[i][j]^multiplication[j][i])<<(K*j)
        for j in range(K)) for i in range(K)]
    center_coordinates=linear_kernel(center_images,K*K);a=len(center_coordinates)
    Z=BinaryCoordinates(center_coordinates)
    squaring=[Z.coordinates(multiply(z,z)) for z in center_coordinates]
    if len(independent_basis(squaring))!=a or len(linear_kernel(
        [value^(1<<i) for i,value in enumerate(squaring)],a))!=1:
        raise ValueError('restricted center is not a field')
    if not a or K%a:raise AssertionError('invalid center dimension')
    t=isqrt(K//a)
    if t<2 or a*t*t!=K or D%(a*t):
        raise ValueError('restricted mark span has no integral matrix shape')
    d=D//(a*t)
    # Full sandwich rank certifies central simplicity in the actual table.
    sandwich=BinaryCoordinates()
    for i in range(K):
        for j in range(K):
            right_action=[multiplication[a][j] for a in range(K)]
            columns=[apply_binary(right_action,multiplication[i][k]) for k in range(K)]
            sandwich.insert(pack(columns,K))
    if len(sandwich.basis)!=K*K//a:
        raise ValueError('restricted algebra failed the central-simple sandwich certificate')
    equations=[(multiplication[i][j]^multiplication[j][i],0) for i in range(K) for j in range(i)]
    trace_space=affine_solutions(equations,K)[1]
    if len(trace_space)!=a:raise AssertionError('central-simple algebra has wrong trace space')
    trace=trace_space[0]
    gram=[sum(((trace&multiplication[i][j]).bit_count()%2)<<j for j in range(K)) for i in range(K)]
    if affine_solutions([(row,0) for row in gram],K)[1]:
        raise AssertionError('intrinsic trace pairing is singular')
    if a==1 and (trace&unit_coordinates).bit_count()%2!=t%2:
        raise AssertionError('intrinsic trace does not have the acquired degree')
    # Center the actual affine source in the manufactured isotropic coordinates.
    columns=left+right;local_source=compose_quadratic(source,0,columns)
    local_polar=polar_rows(local_source,n)
    shifted=affine_solutions([(row,int((1<<i) in local_source)) for i,row in enumerate(local_polar)],n)
    if shifted is None or shifted[1]:raise AssertionError('source affine center is not unique')
    offset=apply_binary(columns,shifted[0])
    centered_source=compose_quadratic(source,offset,columns)
    centered_marks=[compose_quadratic(f,offset,columns) for f in marks]
    lower=(1<<D)-1
    def bilinear_only(terms):
        return all(a==0 or (a.bit_count()==2 and (a&lower) and (a>>D)) for a in terms)
    if not bilinear_only(centered_source):raise AssertionError('source centering did not produce a bilinear form')
    if any(not bilinear_only(f) for f in centered_marks):
        raise ValueError('some marked affine terms do not share the acquired bilinear center')
    if len(algebra)!=2*K or len(center)!=2*a:
        raise AssertionError('full adjoint algebra has inconsistent dimension')
    return dict(input_bits=n,marked_quadratics=m,matrix_size=t,inner_dimension=d,field_degree=a,
        half_dimension=D,generated_algebra_dimension=len(algebra),algebra_products=products,
        ordinary_center_dimension=2*a,self_adjoint_center_dimension=a,
        central_idempotent_columns=E,adjoint_exchanges_central_factors=True,
        coordinate_columns=columns,affine_offset=offset,source_constant=int(0 in centered_source),
        output_constant=sum(int(0 in f)<<i for i,f in enumerate(centered_marks)),
        restricted_algebra_basis=S.basis,restricted_algebra_dimension=K,
        marked_operator_coordinates=[S.coordinates(a) for a in restricted],
        basis_mark_indices=basis_indices,unit_coordinates=unit_coordinates,
        multiplication_table=multiplication,intrinsic_trace=trace,trace_gram_rows=gram,
        restricted_center_basis=center_coordinates,restricted_center_dimension=a,
        center_frobenius_columns=squaring,center_frobenius_injective=True,
        center_frobenius_fixed_dimension=1,
        sandwich_span_dimension=len(sandwich.basis),sandwich_space_dimension=K*K//a,
        supplied_matrix_shape_or_decomposition=False,matrix_units_constructed=False,
        field_generator_or_multiplication_table_constructed=False,
        global_output_values_enumerated=0,seconds=time.perf_counter()-begun)


def adjoint_product_target_fiber(certificate,target):
    C=certificate;m=C['marked_quadratics']
    if type(target) is not int or target<0 or target.bit_length()>m:
        raise ValueError('invalid original output target')
    rhs=target^C['output_constant'];K=C['restricted_algebra_dimension']
    functional=sum(((rhs>>i)&1)<<j for j,i in enumerate(C['basis_mark_indices']))
    for i,a in enumerate(C['marked_operator_coordinates']):
        if (a&functional).bit_count()%2!=((rhs>>i)&1):
            return dict(population=0,signed_fiber=0,reason='inconsistent marked output relations')
    solved=affine_solutions([(row,(functional>>i)&1)
        for i,row in enumerate(C['trace_gram_rows'])],K)
    if solved is None or solved[1]:raise AssertionError('target trace dual is not unique')
    dual=apply_binary(C['restricted_algebra_basis'],solved[0])
    represented_rank=len(independent_basis(unpack(dual,C['half_dimension'])))
    rank,remainder=divmod(represented_rank,C['field_degree']*C['inner_dimension'])
    if remainder:raise AssertionError('module rank is not divisible by multiplicity')
    population=matrix_product_fiber_population(C['matrix_size'],C['inner_dimension'],rank,C['field_degree'])
    source_bit=C['source_constant']^((functional&C['unit_coordinates']).bit_count()%2)
    return dict(population=population,signed_fiber=(1-2*source_bit)*population,
        target_functional=functional,target_dual_coordinates=solved[0],
        represented_target_rank=represented_rank,matrix_target_rank=rank,
        source_value_on_fiber=source_bit,reason='intrinsic reduced-trace matrix-product fiber',
        original_assignments_enumerated=0,global_output_values_enumerated=0)


def count_adjoint_product_target(source,quadratics,n,target):
    certificate=acquire_adjoint_product_algebra(source,quadratics,n)
    fiber=adjoint_product_target_fiber(certificate,target)
    source_total=quadratic_gap(set(source),n)
    expected=(1-2*certificate['source_constant'])*(1<<certificate['half_dimension'])
    if source_total!=expected:raise AssertionError('source bilinear normalization failed')
    gap=source_total-2*fiber['signed_fiber'];domain=1<<n
    if abs(gap)>domain or (domain-gap)%2:raise AssertionError('invalid original Boolean population')
    return dict(original_input_bits=n,ones=(domain-gap)//2,zeros=(domain+gap)//2,
        gap=gap,source_total=source_total,target=target,fiber=fiber,
        certificate=certificate,auxiliary_independent_inputs=0,
        original_assignments_enumerated=0,global_output_values_enumerated=0)


def count_adjoint_product_native(program):
    n=program.get('inputs',program.get('n'))
    if type(n) is not int or n<1 or n>len(program.get('gates',[]))+1:
        raise ValueError('this nonsingular-source family requires every declared input in the explicit DAG')
    n,gates,out=validate_trace_program(program,n)
    if out<n or gates[out-n]['op']!='xor':raise ValueError('exposed source XOR required')
    failures=[]
    for core,residual in (gates[out-n]['args'],list(reversed(gates[out-n]['args']))):
        try:
            table=CubicGateTable(program,degree_limit=2,targets=[core])
            if table.coefficients[core] is None:raise ValueError('source not acquired as quadratic')
            source=table.polynomial(core)
            reversible=acquire_reversible_terminal_and(dict(inputs=n,gates=gates,output=residual))
            target=invert_terminal(reversible)
            result=count_adjoint_product_target(source,reversible['initial_quadratics'],n,target)
            result.update(ordinary_gates=len(gates),source_operand=core,
                reversible_certificate=reversible,native_circuit_acquired=True)
            return result
        except ValueError as error:failures.append(str(error))
    raise ValueError('no admitted adjoint-product route: '+'; '.join(failures))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=count_adjoint_product_native(json.loads(args.source.read_text()))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    else:print(rendered,end='')


if __name__=='__main__':main()
