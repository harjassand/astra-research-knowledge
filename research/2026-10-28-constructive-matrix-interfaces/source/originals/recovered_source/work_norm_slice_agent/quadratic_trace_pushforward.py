#!/usr/bin/env python3
"""Manufacture the exact signed response of a quadratic to a linear output.

For Q:F2^n->F2 and T:F2^n->F2^a, the response at w is
sum_(Tx=w) (-1)^Q(x).  Its exact nonzero support is affine; on that
support it is a constant power of two times a manufactured quadratic
sign.  Compilation uses binary linear algebra, without output-domain
enumeration.  An arbitrary supplied Boolean program can subsequently be
evaluated on the actual support, with its cardinality explicitly charged.
"""
from pathlib import Path
import sys,time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'work_norm_frontier_agent'),str(ROOT/'work_matrix_root')]


def parity(x):return x.bit_count()&1


def selected(mask):
    while mask:
        b=mask&-mask;yield b.bit_length()-1;mask^=b


def apply_columns(columns,x):
    out=0
    for j in selected(x):out^=columns[j]
    return out


def anf_value(terms,x):
    value=0
    for term in terms:value^=(x&term)==term
    return int(value)


def affine_solutions(equations,width):
    """Return one solution and a kernel basis of (mask,rhs) equations."""
    pivots={}
    for mask,rhs in equations:
        while mask:
            j=mask.bit_length()-1
            if j not in pivots:pivots[j]=(mask,rhs);break
            row,value=pivots[j];mask^=row;rhs^=value
        if not mask and rhs:return None
    def finish(x,homogeneous):
        for j,(row,rhs) in sorted(pivots.items()):
            value=parity((row^(1<<j))&x)^(0 if homogeneous else rhs)
            if value:x^=1<<j
        return x
    offset=finish(0,False)
    basis=[finish(1<<j,True) for j in range(width) if j not in pivots]
    return offset,basis


def compile_quadratic_pushforward(quadratic_anf,output_columns,output_bits):
    """Return a fully explicit affine-quadratic response certificate.

ANF monomials are bit masks, with 0 denoting the constant. Output columns
are T(e_i), encoded in output_bits bits. No function identity is presumed:
the explicit source is checked to have degree at most two.
"""
    begun=time.perf_counter();columns=list(output_columns);n=len(columns);terms=set(quadratic_anf)
    if type(output_bits) is not int or output_bits<0 or any(type(x) is not int or x<0 or x.bit_length()>output_bits for x in columns):
        raise ValueError('explicit binary output columns of the declared width required')
    if any(type(x) is not int or x<0 or x.bit_length()>n or x.bit_count()>2 for x in terms):
        raise ValueError('the supplied ANF must be Boolean quadratic on the original inputs')
    constant=int(0 in terms);linear=0;rows=[0]*n;upper=[0]*n
    for term in terms:
        if term.bit_count()==1:linear^=term
        elif term.bit_count()==2:
            i,j=tuple(selected(term));rows[i]^=1<<j;rows[j]^=1<<i;upper[i]^=1<<j
    def covector(x):return apply_columns(rows,x)
    def qhat(x):
        value=parity(linear&x)
        for i in selected(x):value^=parity(upper[i]&x)
        return value
    image={};kernel=[]
    for i,column in enumerate(columns):
        y=column;x=1<<i
        while y:
            j=y.bit_length()-1
            if j not in image:image[j]=(y,x);break
            old,preimage=image[j];y^=old;x^=preimage
        if not y:kernel.append(x)
    image_data=[image[j] for j in sorted(image)]
    out_basis=[x for x,_ in image_data];section=[x for _,x in image_data]
    work=[(x,covector(x)) for x in kernel];pairs=[];radical=[]
    while work:
        u,cu=work.pop();mate=next((i for i,(v,_) in enumerate(work) if parity(cu&v)),None)
        if mate is None:radical.append((u,cu));continue
        v,cv=work.pop(mate);pairs.append((u,cu,v,cv,qhat(u),qhat(v)))
        next_work=[]
        for w,cw in work:
            av=parity(cw&v);au=parity(cw&u)
            next_work.append((w^(u if av else 0)^(v if au else 0),
                cw^(cu if av else 0)^(cv if au else 0)))
        work=next_work
    equations=[]
    for r,cr in radical:
        mask=sum(parity(cr&v)<<j for j,v in enumerate(section))
        equations.append((mask,qhat(r)))
    solution=affine_solutions(equations,len(section))
    common=dict(input_bits=n,output_bits=output_bits,output_rank=len(section),
        fiber_dimension=len(kernel),restricted_polar_rank=2*len(pairs),
        restricted_radical_dimension=len(radical),source_anf_terms=len(terms),
        compiled_without_output_enumeration=True,enumerated_original_assignments=0)
    if solution is None:
        return dict(**common,empty=True,support_offset=None,support_basis=[],
            support_dimension=0,support_cardinality=0,sign_anf=[],amplitude=0,
            amplitude_exponent=None,seconds=time.perf_counter()-begun)
    z0,directions=solution;v0=apply_columns(section,z0)
    lifts=[apply_columns(section,x) for x in directions]
    basis=[apply_columns(out_basis,x) for x in directions]
    offset=apply_columns(out_basis,z0);c0=covector(v0)
    alpha0=beta0=0
    for k,(u,cu,v,cv,qu,qv) in enumerate(pairs):
        alpha0|=(qu^parity(cu&v0))<<k;beta0|=(qv^parity(cv&v0))<<k
    sign_constant=constant^qhat(v0)^parity(alpha0&beta0)
    alpha=[];beta=[];covariants=[];sign={0} if sign_constant else set()
    for j,w in enumerate(lifts):
        aa=bb=0
        for k,(u,cu,v,cv,_,_) in enumerate(pairs):
            aa|=parity(cu&w)<<k;bb|=parity(cv&w)<<k
        alpha.append(aa);beta.append(bb);covariants.append(covector(w))
        value=qhat(w)^parity(c0&w)^parity(aa&beta0)^parity(bb&alpha0)^parity(aa&bb)
        if value:sign.add(1<<j)
    for j in range(len(lifts)):
        for k in range(j+1,len(lifts)):
            value=parity(covariants[j]&lifts[k])^parity(alpha[j]&beta[k])^parity(alpha[k]&beta[j])
            if value:sign.add((1<<j)|(1<<k))
    exponent=len(kernel)-len(pairs)
    return dict(**common,empty=False,support_offset=offset,support_basis=basis,
        support_dimension=len(basis),support_cardinality=1<<len(basis),
        sign_anf=sorted(sign),amplitude=1<<exponent,amplitude_exponent=exponent,
        seconds=time.perf_counter()-begun)


def response_value(response,output):
    if type(output) is not int or output<0 or output.bit_length()>response['output_bits']:
        raise ValueError('output outside the declared binary space')
    if response['empty']:return 0
    target=output^response['support_offset'];pivots={}
    for i,column in enumerate(response['support_basis']):
        x=1<<i;y=column
        while y:
            j=y.bit_length()-1
            if j not in pivots:pivots[j]=(y,x);break
            old,preimage=pivots[j];y^=old;x^=preimage
        if not y:raise AssertionError('dependent manufactured support basis')
    coordinates=0
    while target:
        j=target.bit_length()-1
        if j not in pivots:return 0
        old,x=pivots[j];target^=old;coordinates^=x
    return response['amplitude']*(1-2*anf_value(response['sign_anf'],coordinates))


def evaluate_program_on_response(response,program,maximum_support=1<<20):
    """Evaluate an arbitrary explicit Boolean program on certified support.

The support size is charged and checked before any program evaluations.
The program's intermediate wires are not new independent inputs.
"""
    from equidegree_trace_program import validate_trace_program
    n,gates,out=validate_trace_program(program,response['output_bits'])
    cardinality=response['support_cardinality']
    if type(maximum_support) is not int or maximum_support<0:raise ValueError('nonnegative explicit support budget required')
    if cardinality>maximum_support:
        raise ValueError('manufactured support exceeds the supplied evaluation budget')
    answer=0;observations=[]
    for coordinates in range(cardinality):
        point=response['support_offset']^apply_columns(response['support_basis'],coordinates)
        wires=[(point>>i)&1 for i in range(n)]
        for gate in gates:
            op=gate['op'];args=gate.get('args',[])
            if op=='const':value=gate['value']
            elif op=='not':value=1^wires[args[0]]
            elif op=='and':value=wires[args[0]]&wires[args[1]]
            elif op=='or':value=wires[args[0]]|wires[args[1]]
            else:value=wires[args[0]]^wires[args[1]]
            wires.append(value)
        bit=wires[out];answer+=response['amplitude']*(1-2*(bit^anf_value(response['sign_anf'],coordinates)))
        if cardinality<=32:observations.append([point,bit])
    total=1<<response['input_bits']
    assert abs(answer)<=total and (total-answer)%2==0
    return dict(gap=answer,ones=(total-answer)//2,zeros=(total+answer)//2,
        original_input_bits=response['input_bits'],auxiliary_independent_inputs=0,
        support_dimension=response['support_dimension'],program_evaluations=cardinality,
        trace_program_gates=len(gates),trace_program_anf_expanded=False,
        observations=observations)


def pencil_trace_response(R,field_h,beta,eta=0,trace_quadratic=()):
    """Push forward the small-pencil quadratic along tr(LA) in the field."""
    from matrix_kloosterman import Field,mmul,mtrace
    F=Field(field_h);a=F.a;q=F.q;r=R.u;c=R.c;n=a*r*c;phi=set(trace_quadratic)
    if not 0<=beta<q or not 0<=eta<q or any(type(x) is not int or x<0 or x.bit_length()>a or x.bit_count()>2 for x in phi):
        raise ValueError('field coefficients and optional Boolean trace quadratic required')
    def source(packed):
        L=[[(packed>>(a*(i*c+j)))&(q-1) for j in range(c)] for i in range(r)]
        H=mmul(L,R.A,F);K=mmul(L,R.B,F);e2=0
        for i in range(r):
            for j in range(i):e2^=F.mul(H[i][i],H[j][j])^F.mul(H[i][j],H[j][i])
        z=F.mul(beta,e2)^mtrace(mmul(K,H,F))^F.mul(eta,mtrace(K))
        return F.trace(z)^anf_value(phi,mtrace(H))
    constant=source(0);single=[source(1<<i)^constant for i in range(n)]
    anf={0} if constant else set();anf.update(1<<i for i,x in enumerate(single) if x)
    for i in range(n):
        for j in range(i+1,n):
            if source((1<<i)|(1<<j))^single[i]^single[j]^constant:anf.add((1<<i)|(1<<j))
    columns=[F.mul(R.A[j][i],1<<b) for i in range(r) for j in range(c) for b in range(a)]
    result=compile_quadratic_pushforward(anf,columns,a)
    result.update(field_polynomial=field_h,field_degree=a,pencil_domain=r,pencil_codomain=c,
        beta=beta,eta=eta,source_quadratic_anf=sorted(anf),trace_columns=columns,
        output_boolean_quadratic=sorted(phi),
        source_quadratic_certified_by_explicit_matrix_formula=True)
    if result['empty']:
        result['field_response_kind']='zero'
    elif result['support_cardinality']==1:
        result['field_response_kind']='point'
        result['field_response_point']=result['support_offset']
    else:
        # A single F-valued output of an F-quadratic, followed by the
        # absolute trace, has full-field support or a point.  On full
        # support, removing the supplied output-only Boolean quadratic
        # leaves one affine field character.
        if result['support_cardinality']!=q or result['support_offset']!=0:
            raise AssertionError('field-quadratic response has unexpected intermediate support')
        baseline=set(result['sign_anf']);basis=result['support_basis']
        cphi=anf_value(phi,0);single_phi=[anf_value(phi,x)^cphi for x in basis]
        composed={0} if cphi else set()
        composed.update(1<<i for i,x in enumerate(single_phi) if x)
        for i in range(a):
            for j in range(i+1,a):
                if anf_value(phi,basis[i]^basis[j])^single_phi[i]^single_phi[j]^cphi:
                    composed.add((1<<i)|(1<<j))
        baseline.symmetric_difference_update(composed)
        if any(x.bit_count()>1 for x in baseline):raise AssertionError('full-field base response is not an affine character')
        at_zero=int(response_value(result,0)<0)^cphi;frequency=0
        for i in range(a):
            value=int(response_value(result,1<<i)<0)^anf_value(phi,1<<i)^at_zero
            frequency|=value<<i
        trace_equations=[]
        for i in range(a):
            mask=sum(F.trace(F.mul(1<<i,1<<j))<<j for j in range(a))
            trace_equations.append((mask,(frequency>>i)&1))
        solution=affine_solutions(trace_equations,a)
        if solution is None or solution[1]:raise AssertionError('degenerate field trace pairing')
        result.update(field_response_kind='full_character',base_character_constant=at_zero,
            base_character_binary_frequency=frequency,base_character_field_frequency=solution[0],
            output_boolean_quadratic=sorted(phi))
    if result['amplitude_exponent'] is not None and result['amplitude_exponent']%a:
        raise AssertionError('field-quadratic fiber amplitude is not a power of q')
    return result
