#!/usr/bin/env python3
"""Uniform cyclic-primary kernel via finite Schur Pfaffians.

Formal q is packed in an integer base independently of the actual field.
All precision and signed coefficient bounds are charged. The odd sentinel
uses a square-zero coefficient and the parent's independently audited signs.
This backend enumerates
no field elements, profiles or subspaces.
"""
from math import factorial,comb
from functools import lru_cache
import time
import numpy as np

def coefficient_degree_bound(t,c):
    return max(k*(t+c-k)-k*(k-1)//2 for k in range(c+1))

def _conv(A,B,degree,modulus):
    out=[0]*(degree+1)
    for i,a in enumerate(A):
        if a:
            for j,b in enumerate(B[:degree-i+1]):
                if b:out[i+j]+=a*b
    return [v%modulus for v in out]

def _center(A,modulus):
    half=modulus//2
    return (A+half)%modulus-half

def _balanced_coefficients(value,base,degree):
    out=[]
    for _ in range(degree+1):
        r=value%base
        if 2*r>base:r-=base
        out.append(r);value=(value-r)//base
    return out


def _third_trace_sentinel_rank_two(ordinary,sentinel,sentinel_skew,top_column,degree,modulus):
    """The epsilon coefficient of tr((M0+epsilon M1)^3), epsilon^2=0.

    C1=u e_*^T-e_* u^T and M1=B C1.  Matrix-vector products give every
    required trace; no dense matrix product is formed.
    """
    last=len(top_column)-1
    us=[A[:,last] for A in sentinel_skew]
    bs=[A[:,last] for A in sentinel]
    right_v=[_center(A@top_column,modulus) for A in ordinary]
    right_b={(j,k):_center(ordinary[j]@bs[k],modulus)
             for j in range(degree+1) for k in range(degree-j+1)}
    left_u={(k,i):_center(us[k]@ordinary[i],modulus)
            for k in range(degree+1) for i in range(degree-k+1)}
    answer=[0]*(degree+1)
    for i in range(degree+1):
        for j in range(degree-i+1):
            for k in range(degree-i-j+1):
                value=ordinary[i][last,:]@right_b[j,k]-left_u[k,i]@right_v[j]
                answer[i+j+k]+=3*value
    return [value%modulus for value in answer]

def _general_alphabet_data(value):
    if value is None:return None
    if not isinstance(value,(tuple,list)) or len(value)!=2 or any(not isinstance(row,(tuple,list)) for row in value):
        raise ValueError('general alphabets are a pair of integer tuples')
    if any(type(x) is not int for row in value for x in row):
        raise ValueError('general alphabet entries are ordinary integers')
    return tuple(tuple(row) for row in value)


def _kernel_geometry(t,d,maximum,semisimple,power_sum,pair_alphabet,hybrid_alphabet=None,general_alphabets=None):
    if type(t) is not int or t<1 or type(d) is not int or d<1:
        raise ValueError('positive ambient size and positive primary degree required')
    if semisimple and power_sum:raise ValueError('choose one specialization')
    if pair_alphabet is not None and (type(pair_alphabet) is not int or power_sum):
        raise ValueError('a second ordinary cyclic or semisimple alphabet requires an integer scalar')
    if hybrid_alphabet is not None and (type(hybrid_alphabet) is not int or pair_alphabet is not None or power_sum or semisimple):
        raise ValueError('a hybrid alphabet is an integer and requires the otherwise ordinary cyclic mode')
    general=_general_alphabet_data(general_alphabets)
    if general is not None and (pair_alphabet is not None or hybrid_alphabet is not None or semisimple or power_sum):
        raise ValueError('general alphabets are mutually exclusive with existing specializations')
    if maximum is None:maximum=t//d
    if not 0<=d*maximum<=t:raise ValueError('degree exceeds ambient size')
    e=maximum;cmax=d*e;odd=t%2;r=t//2;m=(t+1)//2
    shift=r*r if odd else r*(r-1)
    R=max(coefficient_degree_bound(t,c) for c in range(cmax+1))
    # For two semisimple alphabets common (q^d;q^d)_k clearing introduces
    # [k choose j]_(q^d), of degree d*j*(k-j).  Charge it before truncating.
    if semisimple and pair_alphabet is not None:R+=d*(e*e//4)
    # The hybrid coefficient has denominator (Q;Q)_j; clearing at total
    # degree e introduces a ratio of degree at most d*e*(e+1)/2.
    if hybrid_alphabet is not None:R+=d*e*(e+1)//2
    if general is not None and general[1]:R+=d*e*(e+1)//2
    precision=R+shift;L=2*R+t+cmax;size=L+odd;components=1+odd
    return e,cmax,odd,r,m,shift,R,precision,L,size,components


def _packing_bound_bits(t,size,boundary,power_sum,pair_alphabet,hybrid_alphabet=None,general_alphabets=None):
    # Exponential specialization also multiplies degree dj by j!.
    bits=2*size+3*t+(1+int(power_sum))*factorial(t).bit_length()+t*max(1,abs(boundary)).bit_length()+6
    alphabet=pair_alphabet if pair_alphabet is not None else hybrid_alphabet
    if alphabet is not None:
        bits+=t*(2+(t+1).bit_length()+max(1,abs(alphabet)).bit_length())
    general=_general_alphabet_data(general_alphabets)
    if general is not None:
        entries=general[0]+general[1];K=len(entries);magnitude=max([1]+[abs(x) for x in entries])
        bits+=t*(2+K*(2+(t+1).bit_length())+magnitude.bit_length())
    return bits


def kernel_primary_boundary(t,d,boundary,actual_q,maximum=None,semisimple=False,power_sum=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None,
                            _packing=None,_packed_only=False,_dense_sentinel_reference=False):
    """Degree-dj values weighted by boundary^(c-2H), with unchanged defaults.

    The private shared-packing path returns normalized residues before any
    balanced q decoding, for the four-character projection below.
    """
    begun=time.perf_counter()
    e,cmax,odd,r,m,shift,R,precision,L,size,components=_kernel_geometry(
        t,d,maximum,semisimple,power_sum,pair_alphabet,hybrid_alphabet,general_alphabets)
    general=_general_alphabet_data(general_alphabets)
    formal_alphabet=bool(_packing is not None and _packing.get('formal_alphabet',False))
    bound_pair=1 if formal_alphabet and pair_alphabet is not None else pair_alphabet
    bound_hybrid=1 if formal_alphabet and hybrid_alphabet is not None else hybrid_alphabet
    bits=_packing_bound_bits(t,size,1 if _packing is not None else boundary,power_sum,bound_pair,bound_hybrid,general)
    if _packing is None:
        if _packed_only:raise ValueError('normalized packed output requires an explicit shared packing context')
        base=(1<<bits)*factorial(2*t)+1
    else:
        if not _packed_only:raise ValueError('shared-character residues must be projected before balanced decoding')
        base=_packing['base']
        coefficient_base=_packing.get('coefficient_base',base)
        if _packing['precision']!=precision or coefficient_base<=(1<<bits)*factorial(2*t) or base%factorial(2*t)!=1:
            raise ValueError('incompatible or undersized shared packing context')
        if not formal_alphabet and coefficient_base!=base:
            raise ValueError('distinct coefficient and q bases require formal-alphabet packing')
        if formal_alphabet and (general is not None or power_sum or
                (pair_alphabet is None and hybrid_alphabet is None) or
                (pair_alphabet if pair_alphabet is not None else hybrid_alphabet)!=coefficient_base or
                base!=coefficient_base**(e+1)):
            raise ValueError('invalid formal-alphabet Kronecker packing context')
    modulus=base**(precision+1)
    qpowers=[1]
    for _ in range(precision+1):qpowers.append(qpowers[-1]*base)
    bottom=np.zeros((L,L),dtype=object)
    for x in range(1-odd,L,2):
        for y in range(odd,x,2):
            power=x//2+y//2
            if power<=precision:
                bottom[x,y]=qpowers[power];bottom[y,x]=-qpowers[power]
    if power_sum:
        hs=[pow(base**d-1,k,modulus)*pow(factorial(k),-1,modulus)%modulus for k in range(e+1)]
    elif semisimple and e:hs=[1,-1]+[0]*(e-1)
    else:hs=[1]+[(qpowers[d*k]-qpowers[d*(k-1)])%modulus for k in range(1,e+1)]
    if pair_alphabet is not None:
        old=hs
        hs=[sum(old[i]*old[k-i]*pair_alphabet**(k-i) for i in range(k+1))%modulus for k in range(e+1)]
    if hybrid_alphabet is not None:
        old=hs
        hs=[(old[k]-(hybrid_alphabet*old[k-1] if k else 0))%modulus for k in range(e+1)]
    if general is not None:
        cyclic=hs;hs=[1]+[0]*e
        for x in general[0]:
            factor=[cyclic[k]*x**k%modulus for k in range(e+1)]
            hs=_conv(hs,factor,e,modulus)
        for y in general[1]:
            old=hs
            hs=[(old[k]-(y*old[k-1] if k else 0))%modulus for k in range(e+1)]
    C=[[],[]] if odd else [[]]
    for degree in range(e+1):
        A=np.zeros((size,size),dtype=object)
        for k in range(degree+1):
            ell=degree-k;u=d*k;v=d*ell
            if u<L and v<L and hs[k] and hs[ell]:A[u:L,v:L]+=hs[k]*hs[ell]*bottom[:L-u,:L-v]
        C[0].append(_center(A,modulus))
        if odd:
            A=np.zeros((size,size),dtype=object)
            for x in range(L):
                y=x-d*degree
                if y>=0 and not y%2 and y//2<=precision:
                    A[x,L]=hs[degree]*qpowers[y//2];A[L,x]=-A[x,L]
            C[1].append(_center(A,modulus))
    # Multiply the top semiseparable skew matrix using prefix sums.
    f=[boundary if x%2==odd else 1 for x in range(L)]
    g=[boundary if x%2!=odd else 1 for x in range(L)];M=[[] for _ in range(components)]
    for component in range(components):
        for C0 in C[component]:
            total=np.zeros(size,dtype=object)
            for x in range(L):total+=f[x]*C0[x,:]
            pf=np.zeros(size,dtype=object);pg=np.zeros(size,dtype=object)
            A=np.zeros((size,size),dtype=object)
            for x in range(L):
                A[x,:]=f[x]*pg-g[x]*(total-pf-f[x]*C0[x,:])
                if odd:A[x,:]+=f[x]*C0[L,:]
                pf+=f[x]*C0[x,:];pg+=g[x]*C0[x,:]
            if odd:A[L,:]=-total
            M[component].append(_center(A,modulus))
    traces=[None,[[sum(A[i,i] for i in range(size))%modulus for A in part] for part in M]]
    power=M;matrix_products=0
    for j in range(2,m+1):
        tr=[[0]*(e+1) for _ in range(components)]
        for component in range(components):
            for part in range(component+1):
                for r in range(e+1):
                    for k in range(r+1):tr[component][r]+=sum((power[part][k]*M[component-part][r-k].T).flat)
        traces.append([[v%modulus for v in row] for row in tr])
        if j<m:
            if m==3 and odd and not _dense_sentinel_reference:
                top_column=np.array(f+[0],dtype=object)
                cubic=_third_trace_sentinel_rank_two(M[0],M[1],C[1],top_column,e,modulus)
                # At the final Newton step the constant top trace is
                # multiplied by F0's zero sentinel coefficient.  It cannot
                # affect the requested sentinel output and is not computed.
                traces.append([[0]*(e+1),cubic])
                break
            if m==3 and not odd:
                # tr(B C_i B C_j B C_k) is invariant under reversal and
                # cyclic permutation (B and every C are skew), hence under
                # all permutations of three indices.  Only these unordered
                # products are needed for the final cubic trace.
                cubic=[0]*(e+1)
                for i in range(e//3+1):
                    for k in range(i,(e-i)//2+1):
                        product=_center(M[0][i]@M[0][k],modulus);matrix_products+=1
                        for ell in range(k,e-i-k+1):
                            multiplicity=1 if i==ell else (3 if i==k or k==ell else 6)
                            cubic[i+k+ell]+=multiplicity*sum((product*M[0][ell].T).flat)
                traces.append([[v%modulus for v in cubic]])
                break
            new=[[] for _ in range(components)]
            for component in range(components):
                for r in range(e+1):
                    A=np.zeros((size,size),dtype=object)
                    for part in range(component+1):
                        for k in range(r+1):
                            A+=power[part][k]@M[component-part][r-k];matrix_products+=1
                    new[component].append(_center(A,modulus))
            power=new
    # F(v)^2=det(I-v*M), kF_k=-1/2 sum_j tr(M^j)F_(k-j).
    coeff=[[[1]+[0]*e]+([[0]*(e+1)] if odd else [])]
    for k in range(1,m+1):
        out=[[0]*(e+1) for _ in range(components)]
        for j in range(1,k+1):
            for component in range(components):
                for part in range(component+1):
                    term=_conv(traces[j][part],coeff[k-j][component-part],e,modulus)
                    for r in range(e+1):out[component][r]-=term[r]
        inv=pow(2*k,-1,modulus)
        coeff.append([[(v*inv)%modulus for v in row] for row in out])
    small_modulus=base**(R+1);prefactor=1
    for j in range(1,t+1):prefactor=prefactor*(1-base**j)%small_modulus
    results=[];polynomials=[]
    for r in range(e+1):
        packed=coeff[m][odd][r]
        if packed%(base**shift):raise AssertionError('bottom shift failed to divide')
        packed=(packed//(base**shift))*prefactor%small_modulus
        if semisimple or hybrid_alphabet is not None or (general is not None and general[1]):
            for j in range(1,r+1):packed=packed*(1-base**(d*j))%small_modulus
        if power_sum:packed=packed*factorial(r)%small_modulus
        if _packed_only:
            results.append(packed)
            continue
        polynomial=_balanced_coefficients(packed,base,R);value=0
        for x in reversed(polynomial):value=value*actual_q+x
        results.append(value);polynomials.append(polynomial)
    if results[0]!=1:raise AssertionError('empty-kernel normalization failed')
    return results,dict(ambient_size=t,primary_degree=d,maximum_exponent=e,
        boundary=None if _packed_only else boundary,
        source_type='general cyclic and semisimple alphabets' if general is not None else ('cyclic plus semisimple alphabets' if hybrid_alphabet is not None else (('two semisimple alphabets' if semisimple else 'two cyclic alphabets') if pair_alphabet is not None else ('squarefree equidegree' if power_sum else ('semisimple primary' if semisimple else 'cyclic primary')))),
        second_alphabet=pair_alphabet,hybrid_alphabet=hybrid_alphabet,general_alphabets=general,
        sentinel_degree=odd,normalization_q_shift=shift,
        q_degree_bound=R,formal_q_precision=precision,particle_positions=L,
        packing_base_bits=base.bit_length(),ring_modulus_bits=modulus.bit_length(),
        coefficient_base_bits=(_packing.get('coefficient_base',base) if _packing is not None else base).bit_length(),
        formal_alphabet_variable_packed=formal_alphabet,q_stride=e+1 if formal_alphabet else 1,
        pfaffian_particle_pairs=m,dense_matrix_products=matrix_products,
        odd_cubic_rank_two_shortcut=bool(m==3 and odd and not _dense_sentinel_reference),
        unused_top_constant_trace_omitted=bool(m==3 and odd and not _dense_sentinel_reference),
        normalized_packed_residues=bool(_packed_only),
        formal_q_polynomials=polynomials,seconds=time.perf_counter()-begun,
        profiles_enumerated=0,subspaces_enumerated=0,field_elements_enumerated=0)


def _lift_fourth_root_minus_one(seed,digits):
    """Lift seed^4=-1 mod (seed^4+1), allowing a composite base."""
    if type(seed) is not int or seed<2 or seed%2 or type(digits) is not int or digits<1:
        raise ValueError('an even positive seed and positive precision are required')
    base=seed**4+1;rho=seed;precision=1;steps=0
    while precision<digits:
        precision=min(2*precision,digits);modulus=base**precision
        derivative=4*pow(rho,3,modulus)%modulus
        rho=(rho-(pow(rho,4,modulus)+1)*pow(derivative,-1,modulus))%modulus
        if (pow(rho,4,modulus)+1)%modulus:raise AssertionError('fourth-root Hensel lift failed')
        steps+=1
    return base,rho,steps


def _project_four_characters(evaluations,rho,base,original_degree,q_degree_bound):
    """Project normalized packed values onto H mod 4 before q decoding."""
    if len(evaluations)!=4:raise ValueError('four character values are required')
    modulus=base**(q_degree_bound+1);rho%=modulus
    if (pow(rho,4,modulus)+1)%modulus:raise ValueError('the lifted root has insufficient precision')
    powers=[pow(rho,j,modulus) for j in range(8)];inverse_four=pow(4,-1,modulus)
    return [sum(powers[(j*(2*h-original_degree))%8]*evaluations[j] for j in range(4))*inverse_four%modulus
            for h in range(4)]


def kernel_primary_refined_character(t,d,actual_q,maximum=None,semisimple=False,power_sum=False,pair_alphabet=None,hybrid_alphabet=None,general_alphabets=None):
    """Exact refinement using four shared-ring lifted boundary characters.

    No extension ring, prime search, or field-element enumeration is used.
    All four evaluations stay packed until the inverse four-point transform.
    """
    started=time.perf_counter()
    e,cmax,odd,r,m,shift,R,precision,L,size,components=_kernel_geometry(
        t,d,maximum,semisimple,power_sum,pair_alphabet,hybrid_alphabet,general_alphabets)
    bits=_packing_bound_bits(t,size,1,power_sum,pair_alphabet,hybrid_alphabet,general_alphabets)
    seed_binary_exponent=(bits+3)//4;seed=(1<<seed_binary_exponent)*factorial(2*t)
    base,rho,steps=_lift_fourth_root_minus_one(seed,precision+1)
    modulus=base**(precision+1);packing=dict(base=base,precision=precision)
    evaluations=[];records=[]
    for j in range(4):
        values,record=kernel_primary_boundary(t,d,pow(rho,j,modulus),actual_q,e,
            semisimple,power_sum,pair_alphabet,hybrid_alphabet,general_alphabets,_packing=packing,_packed_only=True)
        evaluations.append(values);record=dict(record)
        record.pop('formal_q_polynomials',None);record['boundary_character_power']=j
        records.append(record)
    weights=[];formal=[]
    for k in range(e+1):
        projected=_project_four_characters([row[k] for row in evaluations],rho,base,d*k,R)
        row=[];polynomials=[]
        for packed in projected:
            polynomial=_balanced_coefficients(packed,base,R);value=0
            for coefficient in reversed(polynomial):value=value*actual_q+coefficient
            row.append(value);polynomials.append(polynomial)
        weights.append(row);formal.append(polynomials)
    if weights[0]!=[1,0,0,0]:raise AssertionError('empty four-character normalization failed')
    return weights,dict(route='four lifted boundary characters in a shared integer packing ring',
        ambient_size=t,primary_degree=d,maximum_exponent=e,boundary_evaluations=4,
        second_alphabet=pair_alphabet,hybrid_alphabet=hybrid_alphabet,general_alphabets=_general_alphabet_data(general_alphabets),
        q_degree_bound=R,formal_q_precision=precision,packing_base_bits=base.bit_length(),
        ring_modulus_bits=modulus.bit_length(),base_construction='A0^4+1 with (2t)! dividing A0',
        base_seed_binary_exponent=seed_binary_exponent,base_seed_factorial=2*t,
        root_lift_steps=steps,root_lift_verified=True,projection_before_balanced_decoding=True,
        normalized_character_evaluations=records,formal_q_polynomials=formal,
        profiles_enumerated=0,subspaces_enumerated=0,field_elements_enumerated=0,
        uniform_polynomial_time=True,seconds=time.perf_counter()-started)


def kernel_primary_alphabet_coefficients(t,d,actual_q,maximum=None,semisimple=False,hybrid=False,refined=True):
    """Extract every two-alphabet coefficient using one or four Pfaffians.

    The output maps (first_degree,second_degree) to four H residues (with
    their sum in slot zero when refined=False).  For
    semisimple/hybrid modes these are the COMMON-DENOMINATOR-CLEARED
    coefficients, just as in the ordinary numeric-alphabet kernel.
    Formal q is packed at B^(e+1), the alphabet variable at B.  Modulus
    size grows by e+1; this is an optional exact batching method, not an
    asymptotic speed claim or the default counter path.
    """
    started=time.perf_counter()
    if semisimple and hybrid:raise ValueError('choose a cyclic pair, semisimple pair, or hybrid')
    pair_marker=None if hybrid else 1;hybrid_marker=1 if hybrid else None
    e,cmax,odd,r,m,shift,R,precision,L,size,components=_kernel_geometry(
        t,d,maximum,semisimple,False,pair_marker,hybrid_marker)
    bits=_packing_bound_bits(t,size,1,False,pair_marker,hybrid_marker)
    seed_binary_exponent=(bits+3)//4;seed=(1<<seed_binary_exponent)*factorial(2*t)
    stride=e+1;digits=stride*(precision+1)
    if refined:coefficient_base,rho,steps=_lift_fourth_root_minus_one(seed,digits)
    else:coefficient_base=seed**4+1;rho=None;steps=0
    q_base=coefficient_base**stride;modulus=q_base**(precision+1)
    packing=dict(base=q_base,precision=precision,coefficient_base=coefficient_base,formal_alphabet=True)
    evaluations=[];records=[]
    for j in range(4 if refined else 1):
        boundary=pow(rho,j,modulus) if refined else 1
        values,record=kernel_primary_boundary(t,d,boundary,actual_q,e,semisimple,False,
            None if hybrid else coefficient_base,coefficient_base if hybrid else None,
            _packing=packing,_packed_only=True)
        evaluations.append(values);record=dict(record);record.pop('formal_q_polynomials',None)
        record['boundary_character_power']=j if refined else None;records.append(record)
    weights={};formal=[]
    for k in range(e+1):
        projected=(_project_four_characters([row[k] for row in evaluations],rho,q_base,d*k,R)
            if refined else [evaluations[0][k],0,0,0])
        decoded=[_balanced_coefficients(value,coefficient_base,stride*(R+1)-1) for value in projected]
        for h in range(4):
            if any(decoded[h][stride*a+j] for a in range(R+1) for j in range(k+1,stride)):
                raise AssertionError('an alphabet coefficient exceeded the retained total degree')
        degree_polynomials=[]
        for j in range(k+1):
            row=[];polynomials=[]
            for h in range(4):
                polynomial=[decoded[h][stride*a+j] for a in range(R+1)];value=0
                for coefficient in reversed(polynomial):value=value*actual_q+coefficient
                row.append(value);polynomials.append(polynomial)
            weights[k-j,j]=row;degree_polynomials.append(polynomials)
        if not hybrid:
            for j in range(k+1):
                if degree_polynomials[j]!=degree_polynomials[k-j]:
                    raise AssertionError('the extracted pair polynomial is not palindromic')
        formal.append(degree_polynomials)
    if weights[0,0]!=[1,0,0,0]:raise AssertionError('empty alphabet coefficient normalization failed')
    normalization=('(Q;Q)_m/(Q;Q)_j' if hybrid else ('Gaussian binomial [m choose j]_Q' if semisimple else 'none'))
    return weights,dict(route='packed alphabet coefficient extraction with shared boundary characters',
        ambient_size=t,primary_degree=d,maximum_exponent=e,semisimple=semisimple,hybrid=hybrid,
        profile_residue_refinement=bool(refined),boundary_evaluations=4 if refined else 1,
        total_pfaffian_evaluations=len(records),ordinary_alphabet_interpolation=False,
        alphabet_encoding='v=B; formal q=B^(e+1)',q_stride=stride,
        coefficient_normalization=normalization,q_degree_bound=R,formal_q_precision=precision,
        coefficient_base_bits=coefficient_base.bit_length(),formal_q_base_bits=q_base.bit_length(),
        ring_modulus_bits=modulus.bit_length(),particle_positions=L,
        base_seed_binary_exponent=seed_binary_exponent,base_seed_factorial=2*t,root_lift_steps=steps,
        normalized_packed_evaluations=records,formal_q_polynomials=formal,
        profiles_enumerated=0,subspaces_enumerated=0,field_elements_enumerated=0,
        modulus_growth_factor=stride,uniform_polynomial_time=True,
        speed_improvement_claim=False,seconds=time.perf_counter()-started)

def kernel_even_boundary(t,d,boundary,actual_q,maximum=None):
    if t%2:raise ValueError('legacy even-size entry point')
    return kernel_primary_boundary(t,d,boundary,actual_q,maximum)

def _integer_interpolate(values):
    """Recover monomial coefficients from values at 0,...,n exactly."""
    n=len(values)-1;out=[0]*(n+1)
    for i,value in enumerate(values):
        poly=[1]
        for j in range(n+1):
            if j==i:continue
            new=[0]*(len(poly)+1)
            for k,c in enumerate(poly):new[k]-=j*c;new[k+1]+=c
            poly=new
        multiplier=value*comb(n,i)*((-1)**(n-i))
        for k,c in enumerate(poly):out[k]+=multiplier*c
    answer=[];denominator=factorial(n)
    for x in out:
        y,r=divmod(x,denominator)
        if r:raise AssertionError('nonintegral boundary interpolation')
        answer.append(y)
    return answer

@lru_cache(None)
def cyclic_primary_weights_interpolation(t,d,q,refined=True,semisimple=False,power_sum=False):
    """Preserved ordinary-boundary interpolation reference implementation."""
    e=t//d
    if not refined:return kernel_primary_boundary(t,d,1,q,e,semisimple,power_sum)
    evaluations=[];metas=[]
    for boundary in range(t+1):
        values,meta=kernel_primary_boundary(t,d,boundary,q,e,semisimple,power_sum)
        evaluations.append(values);metas.append(meta)
    weights=[]
    for j in range(e+1):
        c=d*j;polynomial=_integer_interpolate([v[j] for v in evaluations]);row=[0]*4
        for k,value in enumerate(polynomial):
            if k>c or (c-k)%2:
                if value:raise AssertionError('boundary polynomial parity/degree mismatch')
            else:row[((c-k)//2)%4]+=value
        weights.append(row)
    return weights,dict(route='uniform finite Schur Pfaffian with parity sentinel',
                        boundary_evaluations=metas,uniform_polynomial_time=True)


@lru_cache(None)
def cyclic_primary_weights(t,d,q,refined=True,semisimple=False,power_sum=False):
    """Default primary weights, with four-character refinement when needed."""
    if not refined:return kernel_primary_boundary(t,d,1,q,t//d,semisimple,power_sum)
    weights,metadata=kernel_primary_refined_character(t,d,q,semisimple=semisimple,power_sum=power_sum)
    metadata=dict(metadata)
    metadata['ordinary_interpolation_reference']='cyclic_primary_weights_interpolation'
    return weights,metadata

def cyclic_primary_weights_even(t,d,q,refined=True):
    if t%2:raise ValueError('legacy even-size entry point')
    return cyclic_primary_weights(t,d,q,refined)

def cyclic_primary_gap(exponent,field_h,irreducible,beta,phi,eta=0,semisimple=False):
    from pathlib import Path
    import sys
    ROOT=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(ROOT/'work_matrix_root'))
    sys.path.insert(0,str(ROOT/'work_norm_frontier_agent'))
    from simple_operator_quadratic import matrix_source_anf
    from krylov_square_source import Field,companion,quadratic_anf_sum,factor_polynomial
    from feedback_nilpotent_gaussians import shifted_trace_polynomial
    from cyclic_quadratic_primary_counter import polynomial_product
    from two_invariant_quadratic_matrix import gaussian_rows
    F=Field(field_h);q=F.q;f=list(irreducible);d=len(f)-1;t=d*exponent;phi=set(phi)
    if exponent<1:raise ValueError('positive explicit exponent required')
    if factor_polynomial(f,F)!=[(f,1)]:raise ValueError('irreducible primary polynomial required')
    if not 0<=beta<q or not 0<=eta<q or any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):raise ValueError('invalid coefficients or trace polynomial')
    weights,meta=cyclic_primary_weights(t,d,q,refined=bool(eta),semisimple=semisimple)
    if not eta:weights=[[v,0,0,0] for v in weights]
    powers=[[1]]
    for _ in range(exponent):powers.append(polynomial_product(powers[-1],f,F))
    phase=F.trace(F.mul(beta,F.mul(eta,eta)));answer=0;terms=[]
    choose=gaussian_rows(exponent,q**d) if semisimple else None
    for j in range(exponent+1):
        c=d*j;b=t-c
        if semisimple:
            D=[[0]*b for _ in range(b)];A=companion(f)
            for block in range(exponent-j):
                for row in range(d):
                    for col in range(d):D[d*block+row][d*block+col]=A[row][col]
        else:D=companion(powers[exponent-j]) if b else []
        value=0;gaussians=[]
        for r in range(4):
            shifted=shifted_trace_polynomial(phi,F,eta if r%2 else 0,beta)
            source=matrix_source_anf(D,F,beta,shifted,eta)
            G=quadratic_anf_sum(source,F.a*b*b)
            sign=-1 if phase*(r*(r-1)//2)%2 else 1
            value+=weights[j][r]*sign*G;gaussians.append(G)
        factor=q**(c*(c-1)//2+c*b)
        if semisimple:factor*=choose[exponent][j]
        answer+=factor*value
        terms.append(dict(controlled_dimension=c,profile_weights=weights[j],gaussians=gaussians,
                          contribution=factor*value))
    gap=q**(t*t)*answer
    return gap,dict(profile_backend=meta,terms=terms,primary_degree=d,primary_exponent=exponent,
                    source_type='semisimple primary' if semisimple else 'cyclic primary',
                    field_modulus=field_h,beta=beta,eta=eta,phi=sorted(phi),original_bits=3*F.a*t*t)

def cyclic_primary_gap_even(exponent,field_h,irreducible,beta,phi,eta=0):
    if exponent*(len(irreducible)-1)%2:raise ValueError('legacy even-size entry point')
    return cyclic_primary_gap(exponent,field_h,irreducible,beta,phi,eta)
