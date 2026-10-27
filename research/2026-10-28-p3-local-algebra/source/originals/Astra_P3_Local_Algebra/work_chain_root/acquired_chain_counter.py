#!/usr/bin/env python3
"""Raw Boolean cubic -> acquired chain-ring coordinates -> exact count."""
from pathlib import Path
import argparse,itertools,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
for folder in ('work_field_root','work_local_algebra_agent','work_ring_count_agent','work_rank_frontier_agent'):
    sys.path.insert(0,str(ROOT/folder))
from field_descent import bits,linear_apply,polynomial_value,solve,span,factor_cubic,gf_mul,gf_pow
from field_rank_decoder import acquire_quadratic_base,quadratic_vector,symplectic_factors
from local_algebra_acquisition import acquire_chain,ChainRing,Solver
from chain_ring_kloosterman import ChainRing as SumRing,cubic_sum
from sylvester_support import acquire_sylvester_base
from nilpotent_support import acquire_nilpotent_base

def ring_pow(R,a,exponent):
    out=1
    while exponent:
        if exponent&1:out=R.mul(out,a)
        a=R.mul(a,a);exponent>>=1
    return out

def ring_inv(R,a):
    coefficients=[(a>>(R.d*i))&R.mask for i in range(R.e)]
    if not coefficients[0]:raise ValueError('ring inverse requires a unit')
    inverse=[gf_pow(coefficients[0],(1<<R.d)-2,R.h)]
    for i in range(1,R.e):
        acc=0
        for j in range(1,i+1):acc^=gf_mul(coefficients[j],inverse[i-j],R.h)
        inverse.append(gf_mul(inverse[0],acc,R.h))
    return sum(c<<(R.d*i) for i,c in enumerate(inverse))

def monomial(R,exponent,values):
    out=1
    for e,x in zip(exponent,values):
        if e:out=R.mul(out,ring_pow(R,x,e))
    return out

def ring_polynomial(R,poly,values):
    out=0
    for exponent,coefficient in poly.items():out^=R.mul(coefficient,monomial(R,exponent,values))
    return out

def poly_mul(R,a,b):
    out={}
    for e,x in a.items():
        for f,y in b.items():
            g=tuple(i+j for i,j in zip(e,f));out[g]=out.get(g,0)^R.mul(x,y)
    return {e:c for e,c in out.items() if c}

def substitute(R,poly,columns):
    linears=[{tuple(int(j==k) for j in range(3)):columns[k][i]
              for k in range(3) if columns[k][i]} for i in range(3)]
    out={}
    for exponent,coefficient in poly.items():
        term={(0,0,0):coefficient}
        for i,e in enumerate(exponent):
            for _ in range(e):term=poly_mul(R,term,linears[i])
        for e,c in term.items():out[e]=out.get(e,0)^c
    return {e:c for e,c in out.items() if c}

def matrix_inverse(R,rows):
    a=[list(row)+[int(i==j) for j in range(3)] for i,row in enumerate(rows)]
    for j in range(3):
        pivot=next((i for i in range(j,3) if a[i][j]&R.mask),None)
        if pivot is None:raise ValueError('factor plane matrix is not invertible')
        a[j],a[pivot]=a[pivot],a[j];inverse=ring_inv(R,a[j][j])
        a[j]=[R.mul(inverse,x) for x in a[j]]
        for i in range(3):
            if i!=j and a[i][j]:
                c=a[i][j];a[i]=[x^R.mul(c,y) for x,y in zip(a[i],a[j])]
    return [row[3:] for row in a]

def quadratic_matrix_from_anf(poly,n):
    B=[0]*n
    for term in poly:
        if term.bit_count()==2:
            i,j=bits(term);B[i]^=1<<j;B[j]^=1<<i
    return B

def fit_ordinary_cubic(acquired,base_matrix=None):
    """Exact coefficient fit; homogeneous ordinary cubic is unique for d>=3."""
    R=ChainRing(acquired['h'],acquired['e']);n,m=acquired['n'],R.m
    if acquired['module_dimension']!=3 or R.d<3:
        raise ValueError('requires three ring coordinates and d>=3')
    remainder=set(acquired['quadratic_remainder'])
    target_B=quadratic_matrix_from_anf(remainder,n) if base_matrix is None else base_matrix
    target=quadratic_vector(target_B);gram=R.gram();gram_solver=Solver(gram)
    exponents=[(1,1,0),(1,0,1),(0,1,1)]
    for i in range(3):
        e=[0]*3;e[i]=3;exponents.append(tuple(e))
        for j in range(3):
            if i!=j:
                e=[0]*3;e[i],e[j]=2,1;exponents.append(tuple(e))
    pair_index={pair:t for t,pair in enumerate(itertools.combinations(range(n),2))}
    candidates,unary_parts,labels=[],[],[]
    for exponent in exponents:
        support=[i for i in range(n) if exponent[i//m]]
        singles,columns,unary={},[0]*m,[0]*m
        for i in support:
            point=[0]*3;point[i//m]=1<<(i%m)
            value=monomial(R,exponent,point);singles[i]=value
            for c in bits(linear_apply(gram,value)):unary[c]^=1<<i
        for i,j in itertools.combinations(support,2):
            point=[0]*3;point[i//m]^=1<<(i%m);point[j//m]^=1<<(j%m)
            value=monomial(R,exponent,point)^singles[i]^singles[j]
            for c in bits(linear_apply(gram,value)):columns[c]^=1<<pair_index[i,j]
        candidates.extend(columns);unary_parts.extend(unary)
        labels.extend((exponent,1<<i) for i in range(m))
    combination=solve(candidates,target)
    if combination is None:raise ValueError('no ordinary chain-ring degree-three lift')
    cubic=acquired['cubic']
    if len(cubic)!=1 or cubic[0]['indices']!=[0,1,2]:raise AssertionError('not a volume form')
    lam=cubic[0]['coefficient']
    if not lam&R.mask:raise AssertionError('radical-free volume coefficient must be a unit')
    result={(1,1,1):lam};linear=sum(term for term in remainder if term.bit_count()==1)
    for j in bits(combination):
        exponent,coefficient=labels[j];result[exponent]=result.get(exponent,0)^coefficient
        linear^=unary_parts[j]
    for i in range(3):
        coefficient=gram_solver((linear>>(m*i))&((1<<m)-1))
        if coefficient is None:raise AssertionError('unary pairing failed')
        if coefficient:result[tuple(int(j==i) for j in range(3))]=coefficient
    if 0 in remainder:result[(0,0,0)]=next(1<<i for i in range(m) if R.functional(1<<i))
    if linear_apply(candidates,combination)!=target:raise AssertionError('quadratic identity failed')
    return {e:c for e,c in result.items() if c},dict(binary_fit_columns=len(candidates),
        binary_fit_rank=len(span(candidates)),binary_fit_constraints=n*(n-1)//2,
        homogeneous_cubic_unique=True,
        identity='all third coefficients acquired; all quadratic and affine coefficients solved')

def factor_chain_cubic(R,poly):
    """Residue factorization followed by seven coefficient corrections per layer."""
    cubic={e:c for e,c in poly.items() if sum(e)==3}
    residue={e:c&R.mask for e,c in cubic.items() if c&R.mask}
    _,field_columns,residue_certificate=factor_cubic(residue,R.h)
    initial=substitute(R,poly,field_columns)
    target={e:c for e,c in initial.items() if sum(e)==3}
    rows=[[int(i==j) for j in range(3)] for i in range(3)]
    lam=target.get((1,1,1),0)&R.mask
    if not lam:raise ValueError('residue cubic is not a unit split volume')
    inverse_residue=gf_pow(lam,(1<<R.d)-2,R.h);layers=[]
    for layer in range(1,R.e):
        current={(0,0,0):lam}
        for row in rows:
            current=poly_mul(R,current,{tuple(int(j==k) for j in range(3)):row[k]
                                       for k in range(3) if row[k]})
        error={e:((target.get(e,0)^current.get(e,0))>>(R.d*layer))&R.mask
               for e in set(target)|set(current)}
        error={e:c for e,c in error.items() if c}
        if any(error.get(tuple(3*int(j==i) for j in range(3)),0) for i in range(3)):
            raise ValueError('residue factors do not lift to independent ring planes')
        lam^=error.get((1,1,1),0)<<(R.d*layer)
        for i in range(3):
            for j in range(3):
                if i==j:continue
                exponent=[1]*3;exponent[i]-=1;exponent[j]+=1
                coefficient=gf_mul(error.get(tuple(exponent),0),inverse_residue,R.h)
                rows[i][j]^=coefficient<<(R.d*layer)
        layers.append(dict(layer=layer,corrected_coefficients=len(error)))
    product={(0,0,0):lam}
    for row in rows:
        product=poly_mul(R,product,{tuple(int(j==k) for j in range(3)):row[k]
                                   for k in range(3) if row[k]})
    if product!=target:raise ValueError('full ring factor identity failed')
    inverse=matrix_inverse(R,rows)
    lift_columns=[[inverse[i][j] for i in range(3)] for j in range(3)]
    columns=[[0]*3 for _ in range(3)]
    for j in range(3):
        for i in range(3):
            for k in range(3):columns[j][i]^=R.mul(field_columns[k][i],lift_columns[j][k])
    transformed=substitute(R,poly,columns)
    if {e for e in transformed if sum(e)==3}!={(1,1,1)}:
        raise AssertionError('factor substitution did not balance cubic')
    return transformed,columns,dict(residue=residue_certificate,lifting_layers=layers,
                                   lifted_normals=rows,full_coefficient_identity=True)

def square_adjoint(R,coefficient):
    """Return a with lambda(c X^2)=lambda(a X), including nilpotent layers."""
    result=0
    for j in range((R.e-1)//2+1):
        c=(coefficient>>(R.d*(R.e-1-2*j)))&R.mask
        result^=gf_pow(c,1<<(R.d-1),R.h)<<(R.d*(R.e-1-j))
    return result

def balanced_count(R,poly):
    allowed={(1,1,1),(1,1,0),(1,0,1),(0,1,1),(1,0,0),(0,1,0),(0,0,1),(0,0,0),
             (2,0,0),(0,2,0),(0,0,2)}
    if any(e not in allowed for e in poly):raise ValueError('unbalanced local polynomial')
    coefficients=[poly.get(e,0) for e in [(1,1,1),(1,1,0),(1,0,1),(0,1,1)]]
    for i in range(3):
        single=tuple(int(j==i) for j in range(3));square=tuple(2*int(j==i) for j in range(3))
        coefficients.append(poly.get(single,0)^square_adjoint(R,poly.get(square,0)))
    coefficients.append(poly.get((0,0,0),0));S=SumRing(R.h,R.e)
    return cubic_sum(S,*(S.packed(c) for c in coefficients))

def shifted_polynomial(R,poly,columns,parity,gram_solver):
    old=[gram_solver((parity>>(R.m*i))&((1<<R.m)-1)) for i in range(3)]
    if any(c is None for c in old):raise AssertionError('parity trace lift failed')
    result=poly.copy()
    for j in range(3):
        coefficient=0
        for i in range(3):coefficient^=R.mul(old[i],columns[j][i])
        exponent=tuple(int(i==j) for i in range(3))
        result[exponent]=result.get(exponent,0)^coefficient
    return {e:c for e,c in result.items() if c}

def compile_chain(poly,n,*,decode_rank_error=True,error_decoder='auto'):
    started=time.perf_counter();poly=set(poly);acquired=acquire_chain(poly,n)
    R=ChainRing(acquired['h'],acquired['e'])
    if acquired['module_dimension']!=3 or R.d<3:
        raise ValueError('complete counter requires three ring coordinates and d>=3')
    B=quadratic_matrix_from_anf(acquired['quadratic_remainder'],n)
    methods=['none'] if not decode_rank_error else (
        ['gabidulin']+(['sylvester'] if R.d>=7 else [])+(['nilpotent'] if R.e>=7 else [])
        if error_decoder=='auto' else [error_decoder])
    candidates=[];attempts=[]
    for method in methods:
        decoding=[];support_certificate=None
        try:
            if method=='nilpotent':base,defect,support_certificate=acquire_nilpotent_base(B,R.h,R.e,module_dimension=3)
            elif method=='sylvester':base,defect,decoding,support_certificate=acquire_sylvester_base(B,R.h,bandwidth=1)
            elif method=='gabidulin':base,defect,decoding=acquire_quadratic_base(B,R.h,bandwidth=1)
            elif method=='none':base,defect=B,[0]*n
            else:raise ValueError('unknown quadratic error decoder')
            polynomial,fit=fit_ordinary_cubic(acquired,base)
            balanced,factor_columns,factor_certificate=factor_chain_cubic(R,polynomial)
        except ValueError as error:
            attempts.append(dict(method=method,accepted=False,reason=str(error)))
            if error_decoder!='auto':raise
            continue
        rank=len(span(defect));attempts.append(dict(method=method,accepted=True,rank=rank))
        candidates.append((rank,method,defect,decoding,support_certificate,polynomial,fit,
                           balanced,factor_columns,factor_certificate))
    if not candidates:raise ValueError('no verified chain representation: '+str(attempts))
    (_,selected,defect,decoding,support_certificate,polynomial,fit,balanced,
     factor_columns,factor_certificate)=min(candidates,key=lambda item:item[0])
    factors,unary=symplectic_factors(defect);rank=len(factors)
    gram_solver=Solver(R.gram());numerator=0
    for selector in range(1<<rank):
        parity=unary^linear_apply(factors,selector)
        sign=-1 if sum(((selector>>(2*j))&3)==3 for j in range(rank//2))&1 else 1
        shifted=shifted_polynomial(R,balanced,factor_columns,parity,gram_solver)
        numerator+=sign*balanced_count(R,shifted)
    denominator=1<<(rank//2)
    if numerator%denominator:raise AssertionError('Walsh reconstruction is not integral')
    signed=numerator//denominator
    if abs(signed)>1<<n or ((1<<n)+signed)&1:raise AssertionError('invalid exact count')
    return dict(original_variables=n,raw_anf_terms=len(poly),
        raw_cubic_terms=sum(x.bit_count()==3 for x in poly),field_degree=R.d,chain_length=R.e,
        module_dimension=3,centroid_dimension=R.m,field_modulus=R.h,
        coordinate_columns=acquired['coordinate_columns'],
        uniformizer_operator=acquired['uniformizer_operator'],
        acquired_defect=defect,acquired_defect_rank=rank,decoding_blocks=len(decoding),
        error_decoder=selected,decoder_attempts=attempts,support_certificate=support_certificate,
        polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(polynomial.items())],
        balanced_polynomial=[dict(exponents=list(e),coefficient=c) for e,c in sorted(balanced.items())],
        factor_columns=factor_columns,factor_certificate=factor_certificate,fit=fit,
        signed_count=signed,zero_count=((1<<n)+signed)//2,walsh_leaf_count=1<<rank,
        retained_walsh_leaves=0,exact_numerator=numerator,exact_denominator=denominator,
        backend='coefficient stationary phase; actual finite Dwork for residue field',
        seconds=time.perf_counter()-started)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('--output',type=Path)
    parser.add_argument('--no-rank-decoding',action='store_true')
    parser.add_argument('--error-decoder',choices=['auto','gabidulin','sylvester','nilpotent'],default='auto')
    args=parser.parse_args()
    data=json.loads(args.input.read_text())
    result=compile_chain(data['polynomial'],data['n'],decode_rank_error=not args.no_rank_decoding,
                         error_decoder=args.error_decoder)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
