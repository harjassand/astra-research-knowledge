#!/usr/bin/env python3
"""Literal Boolean circuits for the many-primary operator reduction.
This compiler does not count its output. Internal gates are deterministic
wire values; the free bits are the three full matrix input arrays.
"""
from pathlib import Path
import argparse,json,random,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
sys.path.insert(0,str(ROOT/'work_ring_count_agent'))
from diagonal_graph_reduction import compile_diagonal_graph,decode_even_hamming
from circuit_field_packing import BinaryField

class BooleanDAG:
    def __init__(self,n):
        self.n=n;self.gates=[];self.memo={}
        self.zero=self.node(('CONST',0));self.one=self.node(('CONST',1))
    def node(self,key):
        if key not in self.memo:
            self.memo[key]=self.n+len(self.gates);self.gates.append(list(key))
        return self.memo[key]
    def xor(self,x,y):
        if x==y:return self.zero
        if x==self.zero:return y
        if y==self.zero:return x
        return self.node(('XOR',min(x,y),max(x,y)))
    def and_(self,x,y):
        if x==self.zero or y==self.zero:return self.zero
        if x==self.one:return y
        if y==self.one or x==y:return x
        return self.node(('AND',min(x,y),max(x,y)))

class FieldCircuit:
    def __init__(self,dag,h):
        self.dag=dag;self.h=h;self.a=h.bit_length()-1
        self.lower=[i for i in range(self.a) if (h>>i)&1]
        self.zero=(dag.zero,)*self.a
    def constant(self,x):return tuple(self.dag.one if (x>>i)&1 else self.dag.zero for i in range(self.a))
    def add(self,x,y):return tuple(self.dag.xor(a,b) for a,b in zip(x,y))
    def multiply(self,x,y):
        d=self.dag;a=self.a;out=[d.zero]*(2*a-1)
        for i,xi in enumerate(x):
            for j,yj in enumerate(y):out[i+j]=d.xor(out[i+j],d.and_(xi,yj))
        for k in range(2*a-2,a-1,-1):
            for j in self.lower:out[k-a+j]=d.xor(out[k-a+j],out[k])
        return tuple(out[:a])

def compile_operator_circuit(query):
    m=query['matrix_size'];a=query['field_degree'];h=query['field_modulus'];n=3*a*m*m
    if query['original_bits']!=n:raise ValueError('inconsistent explicit input inventory')
    F=BinaryField(h)
    if F.n!=a:raise ValueError('wrong field degree')
    eigen=query['eigenvalues']
    if len(eigen)!=m or any(not 0<=x<F.q for x in eigen):raise ValueError('invalid spectrum')
    dag=BooleanDAG(n);fc=FieldCircuit(dag,h)
    matrices=[[[tuple(group*a*m*m+(i*m+j)*a+k for k in range(a))
                  for j in range(m)] for i in range(m)] for group in range(3)]
    X,Y,Z=matrices;XY=[[fc.zero for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for k in range(m):XY[i][j]=fc.add(XY[i][j],fc.multiply(X[i][k],Y[k][j]))
    value=fc.zero
    for i in range(m):
        for j in range(m):value=fc.add(value,fc.multiply(XY[i][j],Z[j][i]))
        value=fc.add(value,fc.multiply(fc.constant(eigen[i]),fc.multiply(X[i][i],X[i][i])))
        for j in range(i+1,m):
            value=fc.add(value,fc.multiply(X[i][i],X[j][j]))
            term=fc.multiply(X[i][j],X[j][i])
            value=fc.add(value,fc.multiply(fc.constant(1^eigen[i]^eigen[j]),term))
    output=dag.zero
    for i in range(a):
        if (F.trace_mask>>i)&1:output=dag.xor(output,value[i])
    return dict(n=n,gates=dag.gates,output=output,
        input_layout='X then Y then Z; each matrix row-major; field polynomial bits low-first',
        target_query=query,internal_gates_are_free_inputs=False,target_count_computed=False)

def evaluate_boolean(circuit,x):
    v=[(x>>i)&1 for i in range(circuit['n'])]
    for gate in circuit['gates']:
        op=gate[0]
        if op=='CONST':value=gate[1]
        elif op=='XOR':value=v[gate[1]]^v[gate[2]]
        elif op=='AND':value=v[gate[1]]&v[gate[2]]
        else:raise ValueError('unsupported literal gate')
        v.append(value)
    return v[circuit['output']]

def evaluate_field_source(query,bits):
    """Direct matrix arithmetic, independent of the Boolean gate expansion."""
    m=query['matrix_size'];a=query['field_degree'];F=BinaryField(query['field_modulus']);mask=F.q-1
    blocks=[[[ (bits>>((group*m*m+i*m+j)*a))&mask for j in range(m)]
             for i in range(m)] for group in range(3)]
    X,Y,Z=blocks;value=0
    for i in range(m):
        for j in range(m):
            for k in range(m):value^=F.mul(F.mul(X[i][j],Y[j][k]),Z[k][i])
            value^=F.mul(query['eigenvalues'][i],F.mul(X[i][j],X[j][i]))
        for j in range(i+1,m):value^=F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i])
    return F.trace(value)

def checks():
    begun=time.perf_counter();rng=random.Random(2026102717);records=[]
    graphs=[[[0]],[[0,0],[0,0]],[[0,1],[1,0]],[[0,1,0],[1,0,1],[0,1,0]]]
    physical=json.loads((ROOT/'work_norm_glue_agent/graph_operator_reduction_audit_results.json').read_text())['physical_m2']['cases']
    for index,A in enumerate(graphs):
        started=time.perf_counter();query=compile_diagonal_graph(A);circuit=compile_operator_circuit(query)
        n=circuit['n'];samples=range(1<<n) if n<=12 else [rng.getrandbits(n) for _ in range(512)]
        count=0
        for bits in samples:
            v=evaluate_boolean(circuit,bits)
            assert v==evaluate_field_source(query,bits)
            count+=v
        record=dict(adjacency=A,query=query,boolean_gates=len(circuit['gates']),
            assignments_checked=len(samples),full_truth_table_checked=n<=12)
        if n<=12:
            even,details=decode_even_hamming(query,ones=count)
            record.update(exact_ones=count,decoded_even_hamming=even)
        elif len(A)==2:
            source=next(r for r in physical if r['adjacency']==A)
            # Different manufactured presentations have the same exact count
            # by the audited Gram identity; no field-coordinate equality is used.
            assert source['gram']['field_degree']==query['field_degree']
            even,details=decode_even_hamming(query,ones=source['ones'])
            record.update(independent_physical_ones=source['ones'],decoded_even_hamming=even,
                physical_count_provenance='all 259 kernels; graph_operator_reduction_audit.py')
        record['seconds']=time.perf_counter()-started;records.append(record)
        Path(__file__).with_name(f'diagonal_operator_circuit_fixture_{index}.json').write_text(json.dumps(circuit,indent=2)+'\n')
        print(json.dumps({k:v for k,v in record.items() if k!='query'}),flush=True)
    output=dict(status='literal Boolean circuits match independent field source',cases=records,
        polynomial_general_counter=False,seconds=time.perf_counter()-begun)
    Path(__file__).with_name('diagonal_operator_boolean_circuit_results.json').write_text(json.dumps(output,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checks',action='store_true');parser.add_argument('--graph',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    if args.checks:checks()
    elif args.graph:
        data=json.loads(args.graph.read_text());A=data['adjacency'] if isinstance(data,dict) else data
        result=compile_operator_circuit(compile_diagonal_graph(A));text=json.dumps(result,indent=2)+'\n'
        if args.output:args.output.write_text(text)
        else:print(text,end='')
    else:parser.error('provide --checks or --graph')
