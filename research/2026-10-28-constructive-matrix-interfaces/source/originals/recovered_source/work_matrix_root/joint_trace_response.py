#!/usr/bin/env python3
"""Exact one-trace counter and a separately labeled two-trace oracle reduction.
The two-trace target count is not computed by this program.
"""
from pathlib import Path
import sys,json,argparse,time,random
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_chain_root'),str(ROOT/'work_ring_count_agent')]
from universal_circuit_phase import circuit_value,compile_circuit_phase,gate_anf
from circuit_field_packing import power_two_field_modulus,BinaryField
from diagonal_operator_boolean_circuit import BooleanDAG,FieldCircuit,evaluate_boolean

SOURCE_OPERATOR=[[0,0,1],[1,0,1],[0,1,0]]

def response_weights(q):
    if q<2 or q&(q-1):raise ValueError('power-of-two field size required')
    return (q**3-1)*(q*q-1)*(q-1),q*q*(q*q+q+1)*(q**3-1)

def prepare_query(circuit,minimum_field_degree=1):
    compile_circuit_phase(circuit) # Local syntax/causality validation only.
    if type(minimum_field_degree) is not int or minimum_field_degree<1:
        raise ValueError('positive minimum field degree required')
    n=circuit['n'];a=1<<(max(n,minimum_field_degree)-1).bit_length();h=power_two_field_modulus(a)
    E,O=response_weights(1<<a)
    return dict(source_circuit=circuit,field_degree=a,field_modulus=h,
        matrix_size=3,source_operator=SOURCE_OPERATOR,original_target_bits=27*a,
        E=E,O=O,normalization_q_exponent=12,
        original_circuit_inputs=n,uniform_trace_padding_power=a-n,
        original_circuit_count_computed=False)

def prepare_quadratic_marker_query(circuit):
    query=prepare_query(circuit,minimum_field_degree=2)
    query['reduction_kind']='fixed-quadratic-second-trace'
    query['readout_denominator']=(1<<query['field_degree'])**11*query['O']*(1<<(query['field_degree']//2))
    return query

def paired_coordinate_quadratic(bits,a):
    if a%2:raise ValueError('the bent marker requires even field degree')
    return sum(((bits>>i)&1)*((bits>>(i+1))&1) for i in range(0,a,2))%2

def trace_dual_coordinates(F,s):
    return sum(F.trace(F.mul(s,1<<i))<<i for i in range(F.n))

def read_quadratic_marker_count(query,target_ones):
    """One target-oracle answer yields the original count; no oracle is run."""
    if query.get('reduction_kind')!='fixed-quadratic-second-trace':
        raise ValueError('wrong reduction certificate')
    N=query['original_target_bits'];a=query['field_degree'];q=1<<a;n=query['original_circuit_inputs']
    if a%2 or type(target_ones) is not int or not 0<=target_ones<=1<<N:
        raise ValueError('invalid field degree or target count')
    c0=circuit_value(query['source_circuit'],0)
    remainder_gap=(1<<N)-2*target_ones-q**12*query['E']*(1-2*c0)
    trace_gap,remainder=divmod(remainder_gap,q**11*query['O']*(1<<(a//2)))
    if remainder or abs(trace_gap)>q:raise ValueError('invalid inferred trace gap')
    count,remainder=divmod(q-trace_gap,1<<(a-n+1))
    if remainder or not 0<=count<=1<<n:raise ValueError('invalid original-input count')
    return count

def count_one_trace_program(circuit,eta=0):
    """Count the matrix program, not the source circuit on its own inputs."""
    query=prepare_query(circuit);a=query['field_degree'];q=1<<a
    if type(eta) is not int or not 0<=eta<q:raise ValueError('eta is outside the acquired field')
    p0=circuit_value(circuit,0);pe=circuit_value(circuit,eta&((1<<circuit['n'])-1))
    gap=q**12*(query['E']*(1-2*p0)+query['O']*(1-2*pe));N=27*a
    return dict(original_matrix_inputs=N,source_trace_program_inputs=circuit['n'],
        source_trace_program_gates=len(circuit['gates']),trace_program_evaluations=2,
        eta=eta,gap=gap,ones=((1<<N)-gap)//2,zeros=((1<<N)+gap)//2,
        query=query,counted_source='Tr(tr(XYZ)+tr(DX^2)+eta tr(DX))+C(trX)',
        uniform_polynomial_time=True,arbitrary_circuit_count_computed=False)

def read_original_circuit_count(query,target_ones):
    """Read the two-trace target oracle answer; do not compute that answer."""
    N=query['original_target_bits'];a=query['field_degree'];q=1<<a;n=query['original_circuit_inputs']
    if type(target_ones) is not int or not 0<=target_ones<=1<<N:raise ValueError('invalid target count')
    scaled,remainder=divmod((1<<N)-2*target_ones,q**12)
    if remainder:raise ValueError('target gap lacks its exact normalizer')
    c0=circuit_value(query['source_circuit'],0)
    trace_gap,remainder=divmod(scaled-query['E']*(1-2*c0),query['O'])
    if remainder or abs(trace_gap)>q:raise ValueError('invalid inferred trace gap')
    count,remainder=divmod(q-trace_gap,1<<(a-n+1))
    if remainder or not 0<=count<=1<<n:raise ValueError('original-input count is not integral or bounded')
    return count

def _xor_all(dag,values):
    out=dag.zero
    for value in values:out=dag.xor(out,value)
    return out

def _attach_program(dag,circuit,input_wires):
    wires=list(input_wires[:circuit['n']])
    for index,gate in enumerate(circuit['gates']):
        value=dag.zero
        for mask in gate_anf(gate,circuit['n']+index):
            term=dag.one
            while mask:
                bit=mask&-mask;term=dag.and_(term,wires[bit.bit_length()-1]);mask^=bit
            value=dag.xor(value,term)
        wires.append(value)
    return wires[circuit['output']]

def literal_matrix_query(query,*,two_observables=True,eta=0,quadratic_marker=False):
    """Emit ordinary Boolean gates with exactly 27a independent inputs."""
    a=query['field_degree'];F=BinaryField(query['field_modulus']);dag=BooleanDAG(27*a)
    fc=FieldCircuit(dag,F.h);m=3
    X,Y,Z=[[[tuple(group*9*a+(3*i+j)*a+k for k in range(a))
            for j in range(m)] for i in range(m)] for group in range(3)]
    def matrix_product(A,B):
        out=[[fc.zero for _ in range(m)] for _ in range(m)]
        for i in range(m):
            for j in range(m):
                for k in range(m):out[i][j]=fc.add(out[i][j],fc.multiply(A[i][k],B[k][j]))
        return out
    XY=matrix_product(X,Y);XX=matrix_product(X,X);phase=fc.zero;s=fc.zero;v=fc.zero
    for i in range(m):
        s=fc.add(s,X[i][i])
        for j in range(m):
            phase=fc.add(phase,fc.multiply(XY[i][j],Z[j][i]))
            if SOURCE_OPERATOR[i][j]:
                phase=fc.add(phase,XX[j][i]);v=fc.add(v,X[j][i])
    if quadratic_marker:
        if a%2 or query.get('reduction_kind')!='fixed-quadratic-second-trace':
            raise ValueError('a validated even-degree quadratic marker query is required')
    elif two_observables:phase=fc.add(phase,fc.multiply(s,v))
    else:
        if not 0<=eta<F.q:raise ValueError('eta is outside target field')
        phase=fc.add(phase,fc.multiply(fc.constant(eta),v))
    traced=_xor_all(dag,[phase[i] for i in range(a) if F.trace_mask>>i&1])
    output=dag.xor(traced,_attach_program(dag,query['source_circuit'],s))
    if quadratic_marker:
        dual_s=[_xor_all(dag,[s[j] for j in range(a) if F.trace(F.mul(1<<i,1<<j))])
                for i in range(a)]
        for i in range(0,a,2):
            output=dag.xor(output,dag.and_(dual_s[i],dual_s[i+1]))
            output=dag.xor(output,dag.and_(v[i],v[i+1]))
    return dict(n=27*a,gates=dag.gates,output=output,query=query,
        target_kind=('fixed-quadratic-second-trace oracle' if quadratic_marker else
            'two-trace universal oracle' if two_observables else 'one-trace polynomial counter'),
        eta=None if two_observables or quadratic_marker else eta,internal_gates_are_free_inputs=False)

def literal_quadratic_marker_query(query):
    return literal_matrix_query(query,two_observables=False,quadratic_marker=True)

def direct_field_value(program,packed):
    query=program['query'];F=BinaryField(query['field_modulus']);a=F.n;m=3
    X,Y,Z=[[[ (packed>>((group*9+3*i+j)*a))&(F.q-1) for j in range(m)]
             for i in range(m)] for group in range(3)]
    s=X[0][0]^X[1][1]^X[2][2];v=X[2][0]^X[0][1]^X[2][1]^X[1][2];phase=0
    for i in range(m):
        for j in range(m):
            for k in range(m):
                phase^=F.mul(F.mul(X[i][j],Y[j][k]),Z[k][i])
                if SOURCE_OPERATOR[i][j]:phase^=F.mul(X[j][k],X[k][i])
    if program['target_kind']=='two-trace universal oracle':phase^=F.mul(s,v)
    elif program['target_kind']=='one-trace polynomial counter':phase^=F.mul(program['eta'],v)
    elif program['target_kind']!='fixed-quadratic-second-trace oracle':
        raise ValueError('unknown matrix target kind')
    source=query['source_circuit'];bit=circuit_value(source,s&((1<<source['n'])-1))
    if program['target_kind']=='fixed-quadratic-second-trace oracle':
        bit^=paired_coordinate_quadratic(v,a)^paired_coordinate_quadratic(trace_dual_coordinates(F,s),a)
    return F.trace(phase)^bit

def literal_matrix_histogram(h):
    """Exponential independent X scan; Y,Z summed by their rank fibers."""
    sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
    from audit_cyclic_quadratic_primary import physical_quadratic,quadratic_value
    from matrix_kloosterman import Field,rref
    F=Field(h);a=F.a;q=F.q;source=physical_quadratic(SOURCE_OPERATOR,F,0,0,set())
    hist=[[0]*q for _ in range(q)];rank_weights=[q**(3*(3-r)) for r in range(4)]
    for packed in range(1<<(9*a)):
        X=[[(packed>>(a*(3*i+j)))&(q-1) for j in range(3)] for i in range(3)]
        s=X[0][0]^X[1][1]^X[2][2];v=X[2][0]^X[0][1]^X[2][1]^X[1][2]
        rank=len(rref(X,F,3)[1]);hist[s][v]+=(1-2*quadratic_value(packed,*source))*rank_weights[rank]
    hist=[[value*q**9 for value in row] for row in hist]
    E,O=response_weights(q)
    for s in range(q):
        for v in range(q):
            expected=q**12*E*int(s==v==0)+q**11*O*(1-2*F.trace(F.mul(s,v)))
            assert hist[s][v]==expected,(h,s,v,hist[s][v],expected)
    return hist,dict(field_modulus=h,field_degree=a,actual_X_assignments=1<<(9*a),
        original_matrix_inputs=27*a,joint_signed_histogram=hist,E=E,O=O,
        full_original_XYZ_truth_table_enumerated=False)

def checks():
    begun=time.perf_counter();rng=random.Random(482197);histograms={};physical=[];cases=[]
    for h in (3,7):
        hist,record=literal_matrix_histogram(h);histograms[h]=hist;physical.append(record)
        print(json.dumps(dict(field_modulus=h,actual_X_assignments=record['actual_X_assignments'],
            all_joint_trace_bins_passed=True)),flush=True)
    circuits=[dict(n=1,gates=[],output=0),dict(n=2,gates=[['AND',0,1]],output=2),
        dict(n=2,gates=[['XOR',0,1]],output=2),dict(n=2,gates=[['OR',0,1]],output=2),
        dict(n=4,gates=[['AND',0,1],['AND',2,3],['AND',4,5]],output=6)]
    for index,C in enumerate(circuits):
        query=prepare_query(C);F=BinaryField(query['field_modulus']);compiled=literal_matrix_query(query)
        for _ in range(256):
            x=rng.getrandbits(compiled['n'])
            assert evaluate_boolean(compiled,x)==direct_field_value(compiled,x)
        eta=F.q-1;single=literal_matrix_query(query,two_observables=False,eta=eta)
        for _ in range(256):
            x=rng.getrandbits(single['n'])
            assert evaluate_boolean(single,x)==direct_field_value(single,x)
        record=dict(source_circuit=C,target_inputs=compiled['n'],target_gates=len(compiled['gates']),
            one_trace_target_gates=len(single['gates']),literal_assignment_checks=512,
            one_trace_count=count_one_trace_program(C,eta),physical_target_count_checked=False)
        if F.h in histograms:
            hist=histograms[F.h];mask=(1<<C['n'])-1
            gap=sum(hist[s][v]*(1-2*(F.trace(F.mul(s,v))^circuit_value(C,s&mask)))
                    for s in range(F.q) for v in range(F.q))
            ones=((1<<compiled['n'])-gap)//2;recovered=read_original_circuit_count(query,ones)
            expected=sum(circuit_value(C,x) for x in range(1<<C['n']));assert recovered==expected
            single_gap=sum(hist[s][v]*(1-2*(F.trace(F.mul(eta,v))^circuit_value(C,s&mask)))
                           for s in range(F.q) for v in range(F.q))
            assert single_gap==record['one_trace_count']['gap']
            record.update(physical_target_count_checked=True,target_ones=ones,
                recovered_source_count=recovered,literal_source_count=expected)
        cases.append(record)
        Path(__file__).with_name(f'joint_trace_circuit_fixture_{index}.json').write_text(json.dumps(compiled,indent=2)+'\n')
        print(json.dumps(dict(original_inputs=C['n'],target_inputs=compiled['n'],
            target_gates=len(compiled['gates']),physical_count=record['physical_target_count_checked'])),flush=True)
    n=128;gates=[['AND',0,1]]
    for i in range(2,n):gates.append(['AND',n+len(gates)-1,i])
    large=dict(n=n,gates=gates,output=n+len(gates)-1)
    large_result=count_one_trace_program(large,(1<<n)-1)
    output=dict(status='joint histogram, circuit reduction and one-trace counter passed',
        physical_histograms=physical,cases=cases,large_degree_128_one_trace=large_result,
        general_polynomial_circuit_counter=False,seconds=time.perf_counter()-begun)
    Path(__file__).with_name('joint_trace_response_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status=output['status'],large_original_matrix_inputs=large_result['original_matrix_inputs'],
        large_trace_program_evaluations=large_result['trace_program_evaluations'],seconds=output['seconds'])),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checks',action='store_true');parser.add_argument('--circuit',type=Path)
    parser.add_argument('--mode',choices=['count-one-trace','compile-two-trace'],default='count-one-trace')
    parser.add_argument('--eta',type=int,default=0);parser.add_argument('--output',type=Path);args=parser.parse_args()
    if args.checks:checks()
    elif args.circuit:
        C=json.loads(args.circuit.read_text())
        result=count_one_trace_program(C,args.eta) if args.mode=='count-one-trace' else literal_matrix_query(prepare_query(C))
        text=json.dumps(result,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:parser.error('provide --checks or --circuit')
