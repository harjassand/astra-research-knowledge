#!/usr/bin/env python3
"""Exact circuit packing, trace-orbit normalization, and acquired norm descent.
No general polynomial-time Boolean counter is asserted. Expansion has an
explicit term budget. Gaussian/norm leaves are certified special classes.
"""
from pathlib import Path
import sys,json,math,random,itertools
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_field_root'))
sys.path.insert(0,str(ROOT/'work_local_algebra_agent'))
from field_kloosterman import gf_mul,gf_pow,gf_trace,irreducible_binary
from field_descent import solve,span,kernel_columns,linear_apply
from local_algebra_acquisition import Solver
from chain_ring_kloosterman import quadratic_sum


def tower_multiply(a,b,degree):
    if degree==1:return a&b
    half=degree//2;mask=(1<<half)-1
    a0,a1=a&mask,a>>half;b0,b1=b&mask,b>>half
    ac=tower_multiply(a0,b0,half);bd=tower_multiply(a1,b1,half)
    total=tower_multiply(a0^a1,b0^b1,half)
    constant=ac^tower_multiply(bd,1<<(half-1),half)
    return constant|((total^ac)<<half)


def power_two_field_modulus(degree):
    """Deterministic quadratic-tower construction; degree must be a power of two."""
    if degree<1 or degree&(degree-1):raise ValueError('power-of-two degree required')
    if degree==1:return 3
    generator=1<<(degree//2);powers=[];current=1
    for j in range(degree+1):
        relation=solve(powers,current)
        if relation is not None:
            if j!=degree:raise AssertionError('tower generator has insufficient absolute degree')
            modulus=(1<<degree)|relation
            assert irreducible_binary(modulus)
            return modulus
        powers.append(current);current=tower_multiply(current,generator,degree)
    raise AssertionError('missing tower dependence')


class BinaryField:
    def __init__(self,h):
        if not irreducible_binary(h):raise ValueError('irreducible binary modulus required')
        self.h=h;self.n=h.bit_length()-1;self.q=1<<self.n
        self.trace_mask=sum(gf_trace(1<<i,h)<<i for i in range(self.n))
        self.eta=self.trace_mask&-self.trace_mask
        if not self.eta:raise AssertionError('field trace is zero')
    def mul(self,a,b):return gf_mul(a,b,self.h)
    def square(self,a):return self.mul(a,a)
    def power(self,a,e):return gf_pow(a,e,self.h)
    def trace(self,a):return (a&self.trace_mask).bit_count()&1
    def frobenius(self,a,k):
        for _ in range(k%self.n):a=self.square(a)
        return a
    def relative_trace(self,a,subdegree):
        if self.n%subdegree:raise ValueError('subdegree must divide field degree')
        result=0
        for _ in range(self.n//subdegree):result^=a;a=self.frobenius(a,subdegree)
        return result
    def subfield_trace(self,a,subdegree):
        result=0
        for _ in range(subdegree):result^=a;a=self.square(a)
        if result not in (0,1):raise ValueError('argument is not in the stated subfield')
        return result
    def dual_basis(self):
        columns=[sum(self.trace(self.mul(1<<i,1<<j))<<i for i in range(self.n))
                 for j in range(self.n)]
        solver=Solver(columns);dual=[solver(1<<i) for i in range(self.n)]
        if any(c is None for c in dual):raise AssertionError('trace pairing is degenerate')
        return dual


class ArithmeticDAG:
    def __init__(self,F):self.F=F;self.nodes=[dict(op='x')];self.memo={}
    def const(self,a):return self.node('const',a)
    def node(self,op,*args):
        if op in ('add','mul') and args[0]>args[1]:args=tuple(reversed(args))
        key=(op,)+args
        if key not in self.memo:
            self.memo[key]=len(self.nodes)
            self.nodes.append(dict(op=op,args=list(args)))
        return self.memo[key]
    def add(self,a,b):return self.node('add',a,b)
    def mul(self,a,b):return self.node('mul',a,b)
    def square(self,a):return self.node('square',a)


def pack_boolean_circuit(circuit,h=None):
    n=circuit['n']
    if n<1:raise ValueError('at least one input required')
    degree=n if h is not None else 1<<(n-1).bit_length()
    if h is None:h=power_two_field_modulus(degree)
    F=BinaryField(h)
    if F.n<n:raise ValueError('field has too few binary coordinates')
    dag=ArithmeticDAG(F);zero=dag.const(0);one=dag.const(1);dual=F.dual_basis()
    powers=[0]
    for _ in range(1,F.n):powers.append(dag.square(powers[-1]))
    wires=[]
    for beta in dual[:n]:
        acc=zero;c=beta
        for p in powers:
            acc=dag.add(acc,dag.mul(dag.const(c),p));c=F.square(c)
        wires.append(acc)
    for gate in circuit['gates']:
        op=gate['op'];args=gate.get('args',[])
        if any(not isinstance(i,int) or not 0<=i<len(wires) for i in args):
            raise ValueError('gate uses a nonpreceding wire')
        a=[wires[i] for i in args]
        if op=='const':value=dag.const(gate['value']&1)
        elif op=='not' and len(a)==1:value=dag.add(one,a[0])
        elif op=='xor' and len(a)==2:value=dag.add(a[0],a[1])
        elif op=='and' and len(a)==2:value=dag.mul(a[0],a[1])
        elif op=='or' and len(a)==2:value=dag.add(dag.add(a[0],a[1]),dag.mul(a[0],a[1]))
        else:raise ValueError('unsupported Boolean gate')
        wires.append(value)
    output=circuit['output']
    if not 0<=output<len(wires):raise ValueError('invalid output wire')
    phase=dag.mul(dag.const(F.eta),dag.add(one,wires[output]))
    return dict(original_inputs=n,field_degree=F.n,field_modulus=h,dual_basis=dual[:n],
        trace_one=F.eta,arithmetic_nodes=dag.nodes,phase_node=phase,
        packed_boolean_output=wires[output],uniform_fiber=1<<(F.n-n),
        artin_schreier_point_multiplier=1<<(F.n-n+1))


def evaluate_boolean(circuit,x):
    wires=[(x>>i)&1 for i in range(circuit['n'])]
    for gate in circuit['gates']:
        a=[wires[i] for i in gate.get('args',[])];op=gate['op']
        if op=='const':y=gate['value']&1
        elif op=='not':y=1^a[0]
        elif op=='xor':y=a[0]^a[1]
        elif op=='and':y=a[0]&a[1]
        elif op=='or':y=a[0]|a[1]
        else:raise ValueError(op)
        wires.append(y)
    return wires[circuit['output']]


def evaluate_packing(packed,x,F=None):
    F=BinaryField(packed['field_modulus']) if F is None else F;values=[]
    for node in packed['arithmetic_nodes']:
        op=node['op'];a=node.get('args',[])
        if op=='x':v=x
        elif op=='const':v=a[0]
        elif op=='add':v=values[a[0]]^values[a[1]]
        elif op=='mul':v=F.mul(values[a[0]],values[a[1]])
        elif op=='square':v=F.square(values[a[0]])
        else:raise ValueError(op)
        values.append(v)
    return values[packed['phase_node']]


def positive_exponent(exponent,q):
    return 0 if exponent==0 else 1+(exponent-1)%(q-1)


def expand_packing(packed,term_budget=4096):
    """Explicit bounded expansion in Fq[X]/(X^q-X); never a hidden free step."""
    F=BinaryField(packed['field_modulus']);values=[];peak=0
    for index,node in enumerate(packed['arithmetic_nodes']):
        op=node['op'];args=node.get('args',[])
        if op=='x':P={1:1}
        elif op=='const':P={0:args[0]} if args[0] else {}
        elif op=='add':
            P=values[args[0]].copy()
            for e,c in values[args[1]].items():P[e]=P.get(e,0)^c
            P={e:c for e,c in P.items() if c}
        elif op=='square':
            P={}
            for e,c in values[args[0]].items():
                exponent=positive_exponent(2*e,F.q)
                P[exponent]=P.get(exponent,0)^F.square(c)
            P={e:c for e,c in P.items() if c}
        elif op=='mul':
            P={}
            for e,c in values[args[0]].items():
                for f,d in values[args[1]].items():
                    exponent=positive_exponent(e+f,F.q)
                    coefficient=P.get(exponent,0)^F.mul(c,d)
                    if coefficient:P[exponent]=coefficient
                    else:P.pop(exponent,None)
                    if len(P)>term_budget:
                        raise ValueError(f'expansion term budget exceeded during node {index}: {len(P)} terms')
            P={e:c for e,c in P.items() if c}
        else:raise ValueError(op)
        peak=max(peak,len(P))
        if len(P)>term_budget:raise ValueError(f'expansion term budget exceeded at node {index}: {len(P)} terms')
        values.append(P)
    return values[packed['phase_node']],dict(expansion_peak_terms=peak,
        expanded_phase_terms=len(values[packed['phase_node']]),term_budget=term_budget)


def polynomial_value_field(P,x,F):
    out=0
    for e,c in P.items():out^=F.mul(c,F.power(x,e))
    return out


def artin_schreier_reduce(P,F):
    """True polynomial AS coboundaries; no finite-field exponent reduction."""
    out={}
    for e,c in P.items():
        while e and e%2==0:e//=2;c=F.frobenius(c,F.n-1)
        out[e]=out.get(e,0)^c
    return {e:c for e,c in out.items() if c}


def normalize_trace_polynomial(P,F):
    """Finite-field phase identity, including short-orbit coefficient aliases."""
    reduced={}
    for e,c in P.items():
        k=positive_exponent(e,F.q);reduced[k]=reduced.get(k,0)^c
    accumulated={};lengths={}
    for e,c in reduced.items():
        if not c:continue
        if e==0:accumulated[0]=accumulated.get(0,0)^c;continue
        orbit=[e];current=positive_exponent(2*e,F.q)
        while current!=e:orbit.append(current);current=positive_exponent(2*current,F.q)
        representative=min(orbit);current=representative;a=0
        while current!=e:current=positive_exponent(2*current,F.q);a+=1
        coefficient=F.frobenius(c,F.n-a)
        accumulated[representative]=accumulated.get(representative,0)^coefficient
        lengths[representative]=len(orbit)
    out={};solvers={};aliases=0
    for exponent,c in accumulated.items():
        if exponent==0:
            if F.trace(c):out[0]=F.eta
            continue
        length=lengths[exponent];coefficient=F.relative_trace(c,length)
        if not coefficient:aliases+=1;continue
        if length not in solvers:
            solvers[length]=Solver([F.relative_trace(1<<i,length) for i in range(F.n)])
        canonical=solvers[length](coefficient)
        if canonical is None:raise AssertionError('relative trace has no preimage')
        out[exponent]=canonical
    return out,dict(input_terms=len(P),normalized_terms=len(out),
        normalized_degree=max(out,default=0),binary_degree=max((e.bit_count() for e in out),default=0),
        short_orbit_aliases_removed=aliases,orbit_lengths={str(e):lengths[e] for e in out if e})


def acquire_norm_quotient(P,F):
    """Manufacture a count-preserving subfield power-image quotient by gcd."""
    positive=[e for e,c in P.items() if e and c]
    if not positive:return None
    fiber=F.q-1
    for e in positive:fiber=math.gcd(fiber,e)
    suborder=(F.q-1)//fiber
    if (suborder+1)&suborder:return None
    a=(suborder+1).bit_length()-1
    if a<1 or F.n%a or a==F.n:return None
    coefficients={}
    for e,c in P.items():
        if e%fiber:raise AssertionError('exponent is not divisible by acquired gcd')
        coefficient=F.relative_trace(c,a)
        if coefficient:coefficients[e//fiber]=coefficient
    basis=kernel_columns([F.frobenius(1<<i,a)^(1<<i) for i in range(F.n)])
    if len(basis)!=a:raise AssertionError('fixed-field dimension mismatch')
    return dict(subfield_degree=a,fiber=fiber,subfield_basis=basis,
                subfield_coefficients=coefficients,
                constant_sign=1-2*F.trace(P.get(0,0)))


def count_sparse_phase(P,F):
    """Exact certified Gaussian and norm-quotient leaves; unsupported otherwise."""
    P,normalization=normalize_trace_polynomial(P,F)
    if all(e.bit_count()<=2 for e in P):
        value=quadratic_sum(lambda x:F.trace(polynomial_value_field(P,x,F)),F.n)
        return value,dict(method='binary quadratic',**normalization)
    positive=[e for e in P if e]
    if len(positive)==1 and math.gcd(positive[0],F.q-1)==1:
        return 0,dict(method='power permutation',**normalization)
    quotient=acquire_norm_quotient(P,F)
    if quotient is None:raise ValueError('no certified Gaussian or subfield norm leaf')
    a=quotient['subfield_degree'];sub=quotient['subfield_coefficients'];basis=quotient['subfield_basis']
    def value(bits):
        y=linear_apply(basis,bits)
        return F.subfield_trace(polynomial_value_field(sub,y,F),a)
    positive=[e for e in sub if e]
    if all(e.bit_count()<=2 for e in sub):inner=quadratic_sum(value,a);method='norm quotient then Gaussian'
    elif len(positive)==1 and math.gcd(positive[0],(1<<a)-1)==1:
        inner=0;method='norm quotient then power permutation'
    else:raise ValueError('norm quotient acquired but its residual phase needs another exact counter')
    result=quotient['fiber']*inner-(quotient['fiber']-1)*quotient['constant_sign']
    return result,dict(method=method,inner_signed_sum=inner,quotient=quotient,**normalization)
