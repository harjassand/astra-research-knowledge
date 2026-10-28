#!/usr/bin/env python3
"""Exact acquired matrix counting from a Boolean gate program.

Inputs are n original bits. Internal gate values are never independent inputs.
Every gate's ANF is computed exactly; an intermediate degree above three is
reported as outside this compiler, not silently truncated or counted.
"""
from pathlib import Path
import json,random
from raw_matrix_trace import compile_raw_matrix_trace

def multiply(a,b):
    # Comparison sorting gives a deterministic polynomial bound, including
    # adversarial integer hashes. Do not charge hash operations as free.
    products=sorted(x|y for x in a for y in b);out=[]
    i=0
    while i<len(products):
        j=i+1
        while j<len(products) and products[j]==products[i]:j+=1
        if (j-i)&1:out.append(products[i])
        i=j
    return out

def xor_sorted(a,b):
    i=j=0;out=[]
    while i<len(a) and j<len(b):
        if a[i]<b[j]:out.append(a[i]);i+=1
        elif a[i]>b[j]:out.append(b[j]);j+=1
        else:i+=1;j+=1
    return out+a[i:]+b[j:]

def compile_gate_anf(program):
    n=program['inputs'];gates=program['gates'];out=program['output']
    if not isinstance(n,int) or n<1:raise ValueError('invalid original input count')
    if not isinstance(out,int) or not 0<=out<n+len(gates):raise ValueError('invalid output')
    values=[[1<<i] for i in range(n)];peak=1
    for k,g in enumerate(gates):
        op=g['op'];args=g.get('args',[])
        if any(not isinstance(j,int) or not 0<=j<n+k for j in args):
            raise ValueError('circuit is not a topologically ordered Boolean program')
        if op=='const' and not args and g.get('value') in (0,1):v=[0] if g['value'] else []
        elif op=='not' and len(args)==1:v=xor_sorted(values[args[0]],[0])
        elif op in ('xor','and','or') and len(args)==2:
            a,b=(values[j] for j in args)
            if op=='xor':v=xor_sorted(a,b)
            elif op=='and':v=multiply(a,b)
            else:v=xor_sorted(xor_sorted(a,b),multiply(a,b))
        else:raise ValueError('unsupported or malformed Boolean gate')
        if any(m.bit_count()>3 for m in v):
            raise ValueError('an exact intermediate ANF has degree above three')
        values.append(v);peak=max(peak,len(v))
    return set(values[out]),dict(original_inputs=n,internal_gates=len(gates),
                            peak_intermediate_monomials=peak,auxiliary_inputs=0)

def count_matrix_program(program,allow_subexponential=False):
    poly,stats=compile_gate_anf(program)
    from invariant_quadratic_matrix import compile_raw_invariant_quadratic
    from two_invariant_quadratic_matrix import compile_raw_two_invariant_quadratics
    from operator_quadratic_counter import compile_raw_operator_quadratic
    from symplectic_minor_quadratic import compile_raw_symplectic_quadratic
    compilers=[
        lambda:compile_raw_matrix_trace(poly,program['inputs'],allow_subexponential),
        lambda:compile_raw_invariant_quadratic(poly,program['inputs']),
        lambda:compile_raw_two_invariant_quadratics(poly,program['inputs']),
        lambda:compile_raw_operator_quadratic(poly,program['inputs']),
        lambda:compile_raw_symplectic_quadratic(poly,program['inputs'])]
    errors=[]
    for compiler in compilers:
        try:result=compiler();break
        except ValueError as error:errors.append(str(error))
    else:raise ValueError('program is outside the certified matrix families: '+'; '.join(errors))
    result['program']=stats
    return result

def disguised_program(native,n,P,offset):
    gates=[]
    def gate(op,*args,**kw):
        gates.append(dict(op=op,args=list(args),**kw));return n+len(gates)-1
    zero=gate('const',value=0);one=gate('const',value=1);coords=[]
    for i in range(n):
        v=one if (offset>>i)&1 else zero
        for j,c in enumerate(P):
            if (c>>i)&1:v=gate('xor',v,j)
        coords.append(v)
    value=zero
    for mask in sorted(native):
        term=one
        for i in range(n):
            if (mask>>i)&1:term=gate('and',term,coords[i])
        value=gate('xor',value,term)
    return dict(inputs=n,gates=gates,output=value)

def checks():
    from raw_matrix_checks import native_anf
    from field_descent import random_invertible,polynomial_value,linear_apply
    from matrix_kloosterman import eye,matrix_trace_cubic_count
    A=eye(2);B=[[2,1],[3,0]];C=eye(2)
    native,n=native_anf(2,7,A,B,C);rng=random.Random(821)
    P=random_invertible(n,rng);offset=rng.randrange(1<<n)
    program=disguised_program(native,n,P,offset)
    result=count_matrix_program(program)
    expected=matrix_trace_cubic_count(A,B,C,7)[1]['signed_sum']
    assert result['gap']==expected
    poly,_=compile_gate_anf(program)
    for _ in range(100):
        x=rng.randrange(1<<n)
        assert polynomial_value(poly,x)==polynomial_value(native,linear_apply(P,x)^offset)
    Path(__file__).with_name('matrix_program_example.json').write_text(json.dumps(program,indent=2))
    Path(__file__).with_name('matrix_program_result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':checks()
