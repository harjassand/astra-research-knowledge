#!/usr/bin/env python3
"""Acquire a hidden three-dimensional field cubic from raw Boolean ANF.
No field, coordinate maps, factor planes or quadratic coefficients supplied.
Restricted compiler using established centroid and Dwork machinery.
"""
import itertools, json, random, time
from pathlib import Path
from field_kloosterman import gf_mul, gf_pow, gf_trace, kloosterman_dwork


def bits(x):
    while x:
        b=x&-x; yield b.bit_length()-1; x^=b

def xor_all(xs):
    out=0
    for x in xs: out^=x
    return out

def linear_apply(columns,x): return xor_all(columns[i] for i in bits(x))
def compose(a,b): return [linear_apply(a,x) for x in b]
def flat(cols,n): return sum(x<<(n*i) for i,x in enumerate(cols))
def unflat(x,n): return [(x>>(n*i))&((1<<n)-1) for i in range(n)]

def span(columns):
    piv={}
    for j,original in enumerate(columns):
        x=original; c=1<<j
        while x:
            p=(x&-x).bit_length()-1
            if p in piv: x^=piv[p][0]; c^=piv[p][1]
            else: piv[p]=(x,c); break
    return piv

def solve(columns,target):
    piv=span(columns); x=target; c=0
    while x:
        p=(x&-x).bit_length()-1
        if p not in piv: return None
        x^=piv[p][0]; c^=piv[p][1]
    return c

def nullspace_pivots(piv,n):
    result=[]
    for free in range(n):
        if free in piv: continue
        x=1<<free
        for p in sorted(piv,reverse=True):
            if (piv[p]&x).bit_count()&1: x^=1<<p
        result.append(x)
    return result

def nullspace_rows(rows,n):
    piv={}
    for x in rows:
        while x:
            p=(x&-x).bit_length()-1
            if p in piv: x^=piv[p]
            else: piv[p]=x; break
    return nullspace_pivots(piv,n)

def kernel_columns(columns):
    width=max((x.bit_length() for x in columns),default=0)
    return nullspace_rows([sum(((col>>i)&1)<<j for j,col in enumerate(columns))
                           for i in range(width)],len(columns))

def polynomial_value(poly,x): return sum((x&m)==m for m in poly)&1

def tensor_pairs(poly,n):
    pair=[[0]*n for _ in range(n)]
    for mask in poly:
        if mask.bit_count()!=3: continue
        a,b,c=bits(mask)
        for i,j,k in ((a,b,c),(a,c,b),(b,c,a)):
            pair[i][j]^=1<<k; pair[j][i]^=1<<k
    return pair

def tensor_value(pair,u,v,w):
    return xor_all((pair[i][j]&w).bit_count()&1 for i in bits(u) for j in bits(v))

def centroid(poly,n):
    pair=tensor_pairs(poly,n)
    radical=nullspace_rows([pair[i][j] for i in range(n) for j in range(i+1,n)],n)
    if radical: raise ValueError('third derivative has a radical')
    piv={}; trail=[]
    def add(row):
        while row:
            p=(row&-row).bit_length()-1
            if p in piv: row^=piv[p]
            else: piv[p]=row; return
    for k in range(n):
        for i in range(n):
            for j in range(i,n):
                add((pair[j][k]<<(n*i))^(pair[i][k]<<(n*j)))
        dimension=n*n-len(piv); trail.append(dimension)
        if dimension>n: continue
        basis=[unflat(x,n) for x in nullspace_pivots(piv,n*n)]
        failure=None
        for P in basis:
            for c in range(k+1,n):
                for a in range(n):
                    for b in range(a,n):
                        if ((P[a]&pair[b][c]).bit_count()^(P[b]&pair[a][c]).bit_count())&1:
                            failure=True; break
                    if failure: break
                if failure: break
            if failure: break
        if not failure: return basis,pair,trail
    return [unflat(x,n) for x in nullspace_pivots(piv,n*n)],pair,trail

def matrix_minpoly(A,n):
    powers=[]; P=[1<<i for i in range(n)]
    for j in range(n+1):
        vec=flat(P,n); coeff=solve(powers,vec)
        if coeff is not None: return coeff|(1<<j)
        powers.append(vec); P=compose(A,P)
    raise AssertionError('matrix has no minimal polynomial')

def prime_powers(n):
    out=[]; p=2
    while p*p<=n:
        if n%p==0:
            power=1
            while n%p==0: n//=p; power*=p
            out.append((p,power))
        p+=1
    if n>1: out.append((n,n))
    return out

def acquire_field(algebra,n):
    d=len(algebra); af=[flat(P,n) for P in algebra]
    frob=[solve(af,flat(compose(P,P),n)) for P in algebra]
    assert all(x is not None for x in frob)
    if len(span(frob))!=d: raise ValueError('nilpotent centroid: field-only implementation')
    if len(kernel_columns([x^(1<<i) for i,x in enumerate(frob)]))!=1:
        raise ValueError('product centroid: split components first')
    for A in algebra:
        h=matrix_minpoly(A,n)
        if h.bit_length()-1==d: break
    else:
        coordinate=0
        def frob_iter(x,count):
            for _ in range(count): x=linear_apply(frob,x)
            return x
        for prime,m in prime_powers(d):
            ker=kernel_columns([frob_iter(1<<j,m)^(1<<j) for j in range(d)])
            gamma=next(x for x in ker if frob_iter(x,m//prime)!=x)
            coordinate^=gamma
        A=unflat(linear_apply(af,coordinate),n); h=matrix_minpoly(A,n)
        assert h.bit_length()-1==d
    if n%d: raise AssertionError('nonintegral module dimension')
    columns=[]; module_basis=[]
    for i in range(n):
        v=1<<i
        if solve(columns,v) is not None: continue
        module_basis.append(v); orbit=[]; w=v
        for _ in range(d): orbit.append(w); w=linear_apply(A,w)
        columns.extend(orbit)
        assert len(span(columns))==len(columns)
    assert len(columns)==n
    return h,columns,module_basis


def monomial_value(exponent,values,h):
    ans=1
    for power,x in zip(exponent,values):
        if power: ans=gf_mul(ans,gf_pow(x,power,h),h)
    return ans

def field_polynomial_value(poly,values,h):
    return xor_all(gf_mul(c,monomial_value(e,values,h),h) for e,c in poly.items())

def field_poly_mul(a,b,h):
    out={}
    for e,c in a.items():
        for f,d in b.items():
            g=tuple(x+y for x,y in zip(e,f)); out[g]=out.get(g,0)^gf_mul(c,d,h)
    return {e:c for e,c in out.items() if c}

def field_poly_substitute(poly,columns,h):
    linears=[{tuple(int(j==k) for j in range(3)):columns[k][i] for k in range(3)
              if columns[k][i]} for i in range(3)]
    out={}
    for e,c in poly.items():
        product={(0,0,0):c}
        for i,power in enumerate(e):
            for _ in range(power): product=field_poly_mul(product,linears[i],h)
        for f,v in product.items(): out[f]=out.get(f,0)^v
    return {e:c for e,c in out.items() if c}

def trace_gram(h):
    d=h.bit_length()-1
    return [sum(gf_trace(gf_mul(1<<i,1<<j,h),h)<<i for i in range(d)) for j in range(d)]

def field_cubic_fit(poly,n,coordinate_columns,pair,h,quadratic_override=None):
    d=h.bit_length()-1
    if n!=3*d or d<3: raise ValueError('requires module dimension three and extension degree >=3')
    gram=trace_gram(h)
    cubic_trace=[tensor_value(pair,coordinate_columns[t],coordinate_columns[d],coordinate_columns[2*d]) for t in range(d)]
    lam=solve(gram,sum(x<<i for i,x in enumerate(cubic_trace)))
    assert lam not in (None,0)
    constant=polynomial_value(poly,0)
    values=[polynomial_value(poly,c)^constant for c in coordinate_columns]
    target=0; index={}; t=0
    for i in range(n):
        for j in range(i+1,n):
            index[i,j]=t
            val=polynomial_value(poly,coordinate_columns[i]^coordinate_columns[j])^constant^values[i]^values[j]
            target|=val<<t; t+=1
    if quadratic_override is not None: target=quadratic_override
    exponents=[]
    for i in range(3):
        for j in range(i+1,3):
            e=[0]*3; e[i]=e[j]=1; exponents.append(tuple(e))
    for i in range(3):
        e=[0]*3; e[i]=3; exponents.append(tuple(e))
        for j in range(3):
            if i!=j:
                e=[0]*3; e[i]=2; e[j]=1; exponents.append(tuple(e))
    candidates=[]; linear_parts=[]; labels=[]
    for e in exponents:
        support=[i for i in range(n) if e[i//d]]
        singles={}; cols=[0]*d; lins=[0]*d
        for i in support:
            point=[0]*3; point[i//d]=1<<(i%d)
            value=monomial_value(e,point,h); singles[i]=value
            trace_bits=linear_apply(gram,value)
            for c in bits(trace_bits): lins[c]^=1<<i
        for i,j in itertools.combinations(support,2):
            point=[0]*3; point[i//d]^=1<<(i%d); point[j//d]^=1<<(j%d)
            value=monomial_value(e,point,h)^singles[i]^singles[j]
            trace_bits=linear_apply(gram,value)
            for c in bits(trace_bits): cols[c]^=1<<index[i,j]
        candidates.extend(cols); linear_parts.extend(lins)
        labels.extend((e,1<<c) for c in range(d))
    combination=solve(candidates,target)
    if combination is None: raise ValueError('no ordinary field-degree-three trace lift')
    result={(1,1,1):lam}; linear=sum(x<<i for i,x in enumerate(values))
    for j in bits(combination):
        e,c=labels[j]; result[e]=result.get(e,0)^c; linear^=linear_parts[j]
    for i in range(3):
        coefficient=solve(gram,(linear>>(d*i))&((1<<d)-1))
        assert coefficient is not None
        if coefficient: result[tuple(int(j==i) for j in range(3))]=coefficient
    if constant: result[(0,0,0)]=next(1<<i for i in range(d) if gf_trace(1<<i,h))
    assert linear_apply(candidates,combination)==target
    return {e:c for e,c in result.items() if c},dict(quadratic_candidate_columns=len(candidates),
        quadratic_constraint_count=t,fit_rank=len(span(candidates)),raw_constant=constant)


def trim(poly):
    while poly and not poly[-1]: poly.pop()
    return poly

def uadd(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]^=x
    for i,x in enumerate(b): c[i]^=x
    return trim(c)

def umul(a,b,h):
    if not a or not b: return []
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]^=gf_mul(x,y,h)
    return trim(out)

def udivmod(a,b,h):
    a=a[:]; out=[0]*max(0,len(a)-len(b)+1); inv=gf_pow(b[-1],(1<<(h.bit_length()-1))-2,h)
    while len(a)>=len(b):
        k=len(a)-len(b); c=gf_mul(a[-1],inv,h); out[k]=c
        for j,v in enumerate(b): a[k+j]^=gf_mul(c,v,h)
        trim(a)
    return trim(out),a

def ugcd(a,b,h):
    while b: a,b=b,udivmod(a,b,h)[1]
    inv=gf_pow(a[-1],(1<<(h.bit_length()-1))-2,h)
    return [gf_mul(c,inv,h) for c in a]

def field_roots(g,h):
    d=h.bit_length()-1; x=[0,1]; check=x
    for _ in range(d): check=udivmod(umul(check,check,h),g,h)[1]
    if check!=x: raise ValueError('slice polynomial does not split over acquired field')
    factors=[g]
    for a in (1<<i for i in range(d)):
        power=[0,a]; tr=[]
        for _ in range(d):
            tr=uadd(tr,power); power=udivmod(umul(power,power,h),g,h)[1]
        new=[]
        for factor in factors:
            if len(factor)<=2: new.append(factor); continue
            divisor=ugcd(factor,tr,h)
            if 1<len(divisor)<len(factor):
                quotient,remainder=udivmod(factor,divisor,h); assert not remainder
                new.extend([divisor,quotient])
            else: new.append(factor)
        factors=new
        if all(len(f)==2 for f in factors): break
    assert len(factors)==3 and all(len(f)==2 for f in factors)
    return [gf_mul(f[0],gf_pow(f[1],(1<<d)-2,h),h) for f in factors]

def along_line(poly,u,v,h):
    out=[]
    for e,c in poly.items():
        term=[c]
        for i,p in enumerate(e):
            for _ in range(p): term=umul(term,[u[i],v[i]],h)
        out=uadd(out,term)
    return out

def gradient(poly,x,h):
    answer=[0]*3
    for e,c in poly.items():
        for i in range(3):
            if e[i]&1:
                f=list(e); f[i]-=1; answer[i]^=gf_mul(c,monomial_value(f,x,h),h)
    return answer


def inverse_matrix(rows,h):
    a=[list(row)+[int(i==j) for j in range(3)] for i,row in enumerate(rows)]
    q=1<<(h.bit_length()-1)
    for j in range(3):
        pivot=next((i for i in range(j,3) if a[i][j]),None)
        if pivot is None: raise ValueError('dependent recovered factor planes')
        a[j],a[pivot]=a[pivot],a[j]
        inv=gf_pow(a[j][j],q-2,h); a[j]=[gf_mul(x,inv,h) for x in a[j]]
        for i in range(3):
            if i!=j and a[i][j]:
                c=a[i][j]; a[i]=[x^gf_mul(c,y,h) for x,y in zip(a[i],a[j])]
    return [row[3:] for row in a]

def factor_cubic(poly,h):
    cubic={e:c for e,c in poly.items() if sum(e)==3}
    v=next(([1,t,gf_mul(t,t,h)] for t in range(7)
            if field_polynomial_value(cubic,[1,t,gf_mul(t,t,h)],h)),None)
    if v is None: raise ValueError('no certified factorization direction')
    for s in range(7):
        u=[1,s,gf_mul(s,s,h)]; g=along_line(cubic,u,v,h)
        derivative=[g[1] if len(g)>1 else 0,0,g[3] if len(g)>3 else 0]; trim(derivative)
        if len(g)==4 and len(ugcd(g,derivative,h))==1: break
    else: raise ValueError('no squarefree factorization slice')
    roots=field_roots(g,h)
    normals=[gradient(cubic,[x^gf_mul(r,y,h) for x,y in zip(u,v)],h) for r in roots]
    inverse=inverse_matrix(normals,h)
    columns=[[inverse[i][j] for i in range(3)] for j in range(3)]
    transformed=field_poly_substitute(poly,columns,h)
    if {e for e in transformed if sum(e)==3}!={(1,1,1)}:
        raise ValueError('homogeneous cubic is not three independent linear factors')
    return transformed,columns,dict(slice_base=u,slice_direction=v,roots=roots,normals=normals)


def count_balanced(poly,h):
    d=h.bit_length()-1; q=1<<d; lam=poly.get((1,1,1),0)
    if not lam: raise ValueError('missing nonzero cubic')
    inv=gf_pow(lam,q-2,h)
    axy=gf_mul(poly.get((1,1,0),0),inv,h)
    axz=gf_mul(poly.get((1,0,1),0),inv,h)
    ayz=poly.get((0,1,1),0)
    linear=[poly.get(tuple(int(j==i) for j in range(3)),0)^gf_pow(poly.get(tuple(2*int(j==i) for j in range(3)),0),1<<(d-1),h) for i in range(3)]
    dx=gf_mul(linear[0],inv,h)
    dy=linear[1]; dz=linear[2]
    a=dx^gf_mul(axy,axz,h); b=dy^gf_mul(axy,ayz,h); c=dz^gf_mul(axz,ayz,h)
    constant=poly.get((0,0,0),0)^gf_mul(dx,ayz,h)^gf_mul(dy,axz,h)^gf_mul(dz,axy,h)
    sign=(-1)**gf_trace(constant,h)
    if c==0:
        k=q*int(a==0)+q*int(b==0)-1; backend={'shortcut':'zero product fiber'}
    elif a==0 or b==0:
        k=q-1 if a==b==0 else -1; backend={'shortcut':'linear nonzero product fiber'}
    else:
        parameter=gf_mul(gf_mul(a,b,h),c,h)
        k,backend=kloosterman_dwork(parameter,h,use_hasse=True)
        backend['kloosterman_parameter']=parameter
    return sign*q*k,dict(reduced_linear=[a,b,c],constant_trace=gf_trace(constant,h),backend=backend)


def compile_raw(poly,n):
    if not isinstance(n,int) or n<=0 or any(not isinstance(x,int) or x<0 or x.bit_length()>n or x.bit_count()>3 for x in poly): raise ValueError('not a cubic ANF')
    start=time.perf_counter(); algebra,pair,trail=centroid(poly,n)
    h,columns,module_basis=acquire_field(algebra,n)
    fieldpoly,fit=field_cubic_fit(poly,n,columns,pair,h)
    balanced,field_columns,factor=factor_cubic(fieldpoly,h)
    signed,count=count_balanced(balanced,h)
    return dict(original_variables=n,raw_anf_terms=len(poly),raw_cubic_terms=sum(x.bit_count()==3 for x in poly),
        centroid_dimension=len(algebra),centroid_kernel_dimensions=trail,field_modulus=h,
        field_extension_degree=h.bit_length()-1,module_dimension=3,coordinate_columns=columns,
        field_polynomial=[{'exponents':list(e),'coefficient':c} for e,c in sorted(fieldpoly.items())],
        balanced_polynomial=[{'exponents':list(e),'coefficient':c} for e,c in sorted(balanced.items())],
        recovered_field_columns=field_columns,fit=fit,factorization=factor,
        count_certificate=count,signed_count=signed,zero_count=((1<<n)+signed)//2,
        seconds=time.perf_counter()-start,raw_polynomial=sorted(poly))


def extract_anf(evaluator,n,degree=3):
    values={0:evaluator(0)}; poly=set()
    if values[0]: poly.add(0)
    for weight in range(1,degree+1):
        for combination in itertools.combinations(range(n),weight):
            mask=sum(1<<i for i in combination); values[mask]=evaluator(mask)
            coefficient=0; sub=mask
            while True:
                coefficient^=values[sub]
                if not sub: break
                sub=(sub-1)&mask
            if coefficient: poly.add(mask)
    return poly

def random_invertible(n,rng):
    columns=[1<<i for i in range(n)]
    for _ in range(6*n):
        a,b=rng.sample(range(n),2); columns[a]^=columns[b]
    return columns

def fixture(h,seed):
    rng=random.Random(seed); d=h.bit_length()-1; n=3*d; q=1<<d
    planted={(1,1,1):rng.randrange(1,q)}
    for e in [(1,1,0),(1,0,1),(0,1,1),(1,0,0),(0,1,0),(0,0,1),(0,0,0)]: planted[e]=rng.randrange(q)
    columns=random_invertible(n,rng); offset=rng.randrange(1<<n)
    def raw_evaluator(x):
        y=linear_apply(columns,x)^offset; values=[(y>>(d*i))&(q-1) for i in range(3)]
        return gf_trace(field_polynomial_value(planted,values,h),h)
    raw=extract_anf(raw_evaluator,n)
    planted_count,planted_meta=count_balanced(planted,h)
    return raw,n,raw_evaluator,planted_count,dict(planted_modulus=h,planted_polynomial=
        [{'exponents':list(e),'coefficient':c} for e,c in sorted(planted.items())],
        planted_affine_columns=columns,planted_affine_offset=offset,planted_count=planted_count,
        planted_count_certificate=planted_meta)


def validation():
    cases=[]
    for h,seed in [(0b1011,3001),(0b10011,4001),(0b100101,5001),(0b1000011,6001)]:
        raw,n,evaluate,reference,metadata=fixture(h,seed)
        answer=compile_raw(raw,n); assert answer['signed_count']==reference
        checks=0
        if n<=15:
            actual=sum((-1)**polynomial_value(raw,x) for x in range(1<<n)); assert actual==reference
            fpoly={tuple(t['exponents']):t['coefficient'] for t in answer['field_polynomial']}
            d=answer['field_extension_degree']; q=1<<d
            for y in range(1<<n):
                x=linear_apply(answer['coordinate_columns'],y); fields=[(y>>(d*i))&(q-1) for i in range(3)]
                assert polynomial_value(raw,x)==gf_trace(field_polynomial_value(fpoly,fields,answer['field_modulus']),answer['field_modulus'])
                checks+=1
        answer.update(metadata,pointwise_identity_checks=checks); cases.append(answer)
        print(json.dumps({k:answer[k] for k in ['original_variables','centroid_dimension','signed_count','zero_count','seconds']}),flush=True)
    return dict(status='all exact assertions passed',cases=cases,
        pointwise_identity_checks=sum(c['pointwise_identity_checks'] for c in cases),
        backend='actual finite Dwork trace with exact algebraic acquisition',practical_speed_claim=False)


if __name__=='__main__':
    data=validation(); path=Path(__file__).with_name('field_descent_results.json')
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],cases=len(data['cases']),pointwise=data['pointwise_identity_checks'],results=str(path))))
