#!/usr/bin/env python3
"""Recognize and exactly count a raw matrix scaffold with a trace circuit.

Input is an ordinary Boolean gate program. No matrix, field, grouping,
source unit, trace map, or small polynomial degree is supplied. The
recognizer tries the two operands of the output XOR as a cubic scaffold,
manufactures its algebra, and verifies every affine cut of the remaining
program against the manufactured matrix trace. Outside this admitted
family it rejects; it is not a general polynomial #CircuitSAT algorithm.
"""
from pathlib import Path
import argparse,itertools,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/p) for p in ('work_matrix_root','work_norm_frontier_agent',
    'work_norm_slice_agent','work_norm_glue_agent')]
from equidegree_trace_program import validate_trace_program
from minimal_polynomial_compiler import acquire_raw_minimal_source
from arbitrary_operator_hall import quotient_matrix,transpose_partition
from raw_matrix_trace import inverse,linear_apply,solve
from lie_source_unit import Intrinsic
from pencil_trace_program_counter import compile_trace_count_response,evaluate_trace_count_response
from multiprimary_fat_hook_counter import compile_multiprimary_trace_response
from mixed_degree_squarefree_counter import compile_mixed_squarefree_trace_response
from beta_zero_operator_counter import compile_beta_zero_trace_response
from beta_zero_fourier_response import compile_beta_zero_fourier_response


def positions(value):
    while value:
        bit=value&-value;yield bit.bit_length()-1;value^=bit


class CubicGateTable:
    """Exact low-degree ANFs, stored as dense coefficient bit sets.

    Unknown means that an exact intermediate exceeded degree three, or
    depended on one that did. It never means a degree truncation. A gate
    marked known is always exactly its stored Boolean polynomial.
    """
    def __init__(self,program,degree_limit=3,targets=None):
        n=program.get('inputs',program.get('n'));n,gates,_=validate_trace_program(program,n)
        if degree_limit not in (1,2,3):raise ValueError('the supported exact degree limits are one, two and three')
        self.n=n;self.limit=degree_limit;self.monomials=[0]
        for degree in range(1,degree_limit+1):
            self.monomials.extend(sum(1<<i for i in indices) for indices in itertools.combinations(range(n),degree))
        self.index={mask:i for i,mask in enumerate(self.monomials)}
        needed=None
        if targets is not None:
            needed=set();pending=list(targets)
            while pending:
                wire=pending.pop()
                if wire in needed:continue
                needed.add(wire)
                if wire>=n:pending.extend(gates[wire-n].get('args',[]))
        self.coefficients=[1<<(i+1) for i in range(n)]
        for gate in gates:
            if needed is not None and len(self.coefficients) not in needed:
                self.coefficients.append(None);continue
            op=gate['op'];args=gate.get('args',[])
            values=[self.coefficients[i] for i in args]
            if op=='const':value=gate['value']
            elif op=='not':value=None if values[0] is None else values[0]^1
            elif op=='xor':
                value=0 if args[0]==args[1] else None if None in values else values[0]^values[1]
            elif op=='and':value=self.multiply(*values)
            elif op=='or':
                product=self.multiply(*values)
                if 1 in values:value=1
                elif args[0]==args[1]:value=values[0]
                elif None in values or product is None:value=None
                else:value=values[0]^values[1]^product
            self.coefficients.append(value)

    def multiply(self,left,right):
        if left==0 or right==0:return 0
        if left==1:return right
        if right==1:return left
        if left is None or right is None:return None
        if left==right:return left  # Every Boolean function is idempotent.
        output=0;higher=set()
        for i in positions(left):
            for j in positions(right):
                mask=self.monomials[i]|self.monomials[j]
                if mask.bit_count()<=self.limit:output^=1<<self.index[mask]
                elif mask in higher:higher.remove(mask)
                else:higher.add(mask)
        return None if higher else output

    def affine(self,wire):
        value=self.coefficients[wire]
        return value is not None and value.bit_length()<=self.n+1

    def polynomial(self,wire):
        value=self.coefficients[wire]
        if value is None:raise ValueError('the candidate core has an unacquired high-degree intermediate')
        return {self.monomials[i] for i in positions(value)}


def residual_cut(program,wire,table):
    n=table.n;needed=set();cuts={};pending=[wire]
    while pending:
        current=pending.pop()
        if current in needed:continue
        needed.add(current)
        if table.affine(current):
            coefficient=table.coefficients[current]
            cuts[current]=(coefficient>>1,coefficient&1)
        else:
            if current<n:raise AssertionError('original input lost its affine form')
            pending.extend(program['gates'][current-n].get('args',[]))
    return sorted(needed),cuts


def manufacture_raw_trace(acquired):
    """Construct s(x)=tr(W*T_group*(P^-1*x+offset)_group)."""
    algebra=acquired['algebra'];A=Intrinsic(algebra);d=algebra.d
    n=acquired['original_bits'];group=acquired['quadratic_group']
    back=inverse(acquired['group_map']);unit=acquired['evidence']['acquired_unit']
    if not algebra.is_unit(unit):raise AssertionError('fitted source unit is singular')
    local_map=acquired['local_to_algebra'];mask=(1<<d)-1
    def trace_at_centered(y):
        local=(y>>(group*d))&mask
        return A.trace(algebra.mul(unit,linear_apply(local_map,local)))
    columns=[trace_at_centered(column) for column in back]
    offset=trace_at_centered(acquired['affine_offset'])
    rows=[sum(((column>>j)&1)<<i for i,column in enumerate(columns)) for j in range(algebra.a)]
    if solve(rows,0) is None:raise AssertionError('zero not in trace span')
    # The matrix trace is onto, including even matrix sizes: E_11 gives
    # every field value. The acquired unit and coordinate maps are units.
    pivots={}
    for row in rows:
        value=row
        while value:
            pivot=value.bit_length()-1
            if pivot not in pivots:pivots[pivot]=value;break
            value^=pivots[pivot]
    if len(pivots)!=algebra.a:raise AssertionError('manufactured field trace is not onto')
    return dict(input_columns=columns,offset=offset,coordinate_rows=rows,
        field_degree=algebra.a,original_input_bits=n,trace_rank=len(pivots))


def rewrite_residual(program,wire,table,plan,cuts,trace,phi):
    a=trace['field_degree'];gates=[];translated={};bindings=[];constant_cache={}
    def gate(op,*args):
        gates.append(dict(op=op,args=list(args)));return a+len(gates)-1
    def constant(value):
        if value not in constant_cache:
            gates.append(dict(op='const',args=[],value=value));constant_cache[value]=a+len(gates)-1
        return constant_cache[value]
    for original in plan:
        if original in cuts:
            mask,bit=cuts[original];frequency=solve(trace['coordinate_rows'],mask)
            if frequency is None:
                raise ValueError('a residual affine gate is outside the acquired field-trace span')
            shifted=bit^((frequency&trace['offset']).bit_count()%2)
            inputs=list(positions(frequency))
            output=inputs[0] if inputs else constant(0)
            for index in inputs[1:]:output=gate('xor',output,index)
            if shifted:output=gate('not',output)
            translated[original]=output
            bindings.append(dict(original_wire=original,original_mask=mask,original_constant=bit,
                trace_binary_frequency=frequency,trace_constant=shifted))
        else:
            specification=program['gates'][original-table.n]
            translated[original]=gate(specification['op'],*(translated[x] for x in specification.get('args',[])))
    output=translated[wire];correction=None
    for monomial in sorted(phi):
        inputs=list(positions(monomial));term=inputs[0] if inputs else constant(1)
        for index in inputs[1:]:term=gate('and',term,index)
        correction=term if correction is None else gate('xor',correction,term)
    if correction is not None:output=gate('xor',output,correction)
    return dict(inputs=a,gates=gates,output=output),bindings


def compile_raw_trace_circuit(program,maximum_field_evaluations=0,maximum_summary_points=0):
    begun=time.perf_counter();n=program.get('inputs',program.get('n'))
    n,gates,output=validate_trace_program(program,n)
    if output<n or gates[output-n]['op']!='xor':
        raise ValueError('this recognizer requires an output XOR with a cubic scaffold operand')
    # Affine acquisition across the residual is cheap and never expands
    # its nonlinear states. Cubic expansion is confined to a candidate
    # scaffold's ancestors; attempting it on the whole arbitrary program
    # would be both unnecessary and a poor execution strategy.
    affine_table=CubicGateTable(program,degree_limit=1)
    left,right=gates[output-n]['args'];failures=[]
    for core,residual in ((left,right),(right,left)):
        table=CubicGateTable(program,targets=[core])
        if table.coefficients[core] is None:
            failures.append('candidate core has degree above three');continue
        plan,cuts=residual_cut(program,residual,affine_table)
        try:
            acquired=acquire_raw_minimal_source(table.polynomial(core),n,
                (mask for mask,bit in cuts.values()),allow_zero_beta=True)
            trace=manufacture_raw_trace(acquired)
            translated,bindings=rewrite_residual(program,residual,affine_table,plan,cuts,trace,acquired['phi'])
            algebra=acquired['algebra'];polynomial,components=algebra.primary_data(acquired['D'])
            shapes=[transpose_partition(item['jordan_columns']) for item in components]
            D=quotient_matrix(components,shapes,algebra.F)
            # Acquire the requested observable before choosing a response
            # representation. A full trace histogram can be exponentially
            # larger than the exact quotient needed by this quadratic.
            # Unknown high-degree intermediates remain unknown; no degree
            # truncation or promised final cancellation is used.
            quadratic_table=CubicGateTable(translated,degree_limit=2,
                targets=[translated['output']])
            quadratic_value=quadratic_table.coefficients[translated['output']]
            gauged_count=None
            if acquired['beta'] and quadratic_value is not None:
                sys.path.insert(0,str(ROOT/'work_multiprimary_audit'))
                from full_gauged_trace_counter import count_full_gauged_trace
                requested=quadratic_table.polynomial(translated['output'])
                gauged_count=count_full_gauged_trace(D,algebra.h,acquired['beta'],
                    requested,acquired['eta'],profile_backend='defect')
                response=dict(kind='observable_gauged_trace_algebra',
                    field_degree=algebra.a,full_matrix_domain=True,
                    computed_full_trace_histogram=False,
                    acquired_full_gauged_quotient=gauged_count['acquired_full_gauged_quotient'],
                    acquired_power_modes=gauged_count['acquired_power_modes'],
                    profile_backend=gauged_count['profile_backend'],
                    final_quotient_symbols=gauged_count['final_quotient_symbols'],
                    profile_kernel=gauged_count['profile_kernel'])
            elif not acquired['beta'] and all(len(item['irreducible'])>=3 and
                    (len(item['irreducible'])!=3 or algebra.F.mul(algebra.F.mul(acquired['eta'],acquired['eta']),
                     item['irreducible'][1])!=1) for item in components):
                response=compile_beta_zero_trace_response(D,algebra.h,acquired['eta'])
            elif not acquired['beta']:
                response=compile_beta_zero_fourier_response(D,algebra.h,acquired['eta'])
            elif acquired['beta'] and all((len(item['irreducible'])-1)%2==0 for item in components):
                response=compile_multiprimary_trace_response(D,algebra.h,acquired['beta'],acquired['eta'])
            else:response=compile_trace_count_response(D,algebra.h,acquired['beta'],acquired['eta'])
            if gauged_count is not None:
                count=dict(gauged_count)
                count.update(full_matrix_domain=True,trace_program_evaluations=0,
                    trace_program_evaluation_kind='exact acquired quadratic and gauged trace algebra')
            elif maximum_summary_points and response['remaining_walsh_terms']:
                sys.path.insert(0,str(ROOT/'work_trace_frontier'))
                from quadratic_program_response import evaluate_trace_response_quadratic_program
                count=evaluate_trace_response_quadratic_program(response,translated,maximum_summary_points)
                if count['status']!='counted':
                    raise ValueError('acquired quadratic summary exceeds the supplied point budget')
                count.update(full_matrix_domain=response['full_matrix_domain'],
                    auxiliary_independent_inputs=0,
                    trace_program_evaluations=0,
                    trace_program_evaluation_kind='retained DAG on manufactured quadratic fibers')
            else:count=evaluate_trace_count_response(response,translated,maximum_field_evaluations)
        except ValueError as error:
            failures.append(str(error));continue
        if count['original_independent_bits']!=n:raise AssertionError('original gate input domain changed')
        count.update(raw_gate_program=True,original_gate_count=len(gates),
            discovered_cubic_operand=core,discovered_trace_operand=residual,
            raw_core_monomials=acquired['raw_monomials'],trace_affine_cut_count=len(cuts),
            original_trace_circuit_nodes=len(plan),full_source_coefficient_identity_verified=True,
            every_residual_affine_gate_verified=True,supplied_matrix_or_trace_representation=False,
            source_acquisition=acquired['stats'],trace_coordinate_witness=trace,
            affine_gate_bindings=bindings,compiled_trace_program=translated,
            manufactured_response=response,acquisition_seconds=acquired['acquisition_seconds'],
            total_seconds=time.perf_counter()-begun)
        return count
    raise ValueError('no verified matrix-trace decomposition: '+'; '.join(failures))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path);parser.add_argument('--field-evaluation-budget',type=int,default=0)
    parser.add_argument('--quadratic-summary-budget',type=int,default=0)
    args=parser.parse_args();program=json.loads(args.source.read_text())
    result=compile_raw_trace_circuit(program,args.field_evaluation_budget,args.quadratic_summary_budget)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')


if __name__=='__main__':main()
