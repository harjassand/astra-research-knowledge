#!/usr/bin/env python3
"""Independent physical-kernel Gaussian audit; no profiles or Hall branching."""
from pathlib import Path
import sys,json,itertools,random,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))
from cyclic_quadratic_primary_counter import cyclic_quadratic_primary_gap
from matrix_kloosterman import Field,kernel,rref
from validate_nonsplit_quadratic import subspaces

def xor(values):
    value=0
    for x in values:value^=x
    return value

def bits(x):
    while x:
        y=x&-x;yield y.bit_length()-1;x^=y

def packed_gaussian(rows,linear,constant=0):
    rows=list(rows);active=(1<<len(rows))-1;pairs=0;sign=constant
    while True:
        pivot=next(((i,(rows[i]&active&-(rows[i]&active)).bit_length()-1)
                    for i in bits(active) if rows[i]&active),None)
        if pivot is None:
            if linear&active:return 0
            return (-1 if sign else 1)*(1<<(pairs+active.bit_count()))
        i,j=pivot;qi=(linear>>i)&1;qj=(linear>>j)&1
        sign^=qi&qj;pairs+=1;active^=(1<<i)|(1<<j)
        u=rows[i]&active;v=rows[j]&active
        linear^=(v if qi else 0)^(u if qj else 0)^(u&v)
        for k in bits(active):
            rows[k]=(rows[k]&active)^(v if u>>k&1 else 0)^(u if v>>k&1 else 0)

def quadratic_value(x,rows,linear,constant=0):
    value=constant^((linear&x).bit_count()&1);remaining=x
    for i in bits(x):
        remaining^=1<<i;value^=(rows[i]&remaining).bit_count()&1
    return value

def audit_gaussian():
    rng=random.Random(892164);cases=0;assignments=0
    for n in range(8):
        for _ in range(20):
            rows=[0]*n
            for i in range(n):
                for j in range(i):
                    if rng.randrange(2):rows[i]^=1<<j;rows[j]^=1<<i
            linear=rng.getrandbits(n);constant=rng.randrange(2)
            expected=sum(1-2*quadratic_value(x,rows,linear,constant) for x in range(1<<n))
            assert packed_gaussian(rows,linear,constant)==expected
            cases+=1;assignments+=1<<n
    return dict(quadratics=cases,literal_assignments=assignments)

def block_primary(exponent,f):
    """Block Jordan operator over the quadratic field, not the companion f^e."""
    t=2*exponent;D=[[0]*t for _ in range(t)]
    for j in range(exponent):
        D[2*j][2*j+1]=f[0];D[2*j+1][2*j]=1;D[2*j+1][2*j+1]=f[1]
        if j+1<exponent:D[2*j][2*j+2]=1;D[2*j+1][2*j+3]=1
    return D

def matrix(packed,t,F):
    return [[(packed>>(F.a*(i*t+j)))&(F.q-1) for j in range(t)] for i in range(t)]

def physical_value(x,D,F,beta,eta,phi):
    t=len(D);X=matrix(x,t,F);tr=xor(X[i][i] for i in range(t))
    square=[[xor(F.mul(X[i][k],X[k][j]) for k in range(t)) for j in range(t)] for i in range(t)]
    marked=xor(F.mul(D[i][j],square[j][i]) for i in range(t) for j in range(t))
    lin=xor(F.mul(D[i][j],X[j][i]) for i in range(t) for j in range(t))
    e2=xor(F.mul(X[i][i],X[j][j])^F.mul(X[i][j],X[j][i]) for i in range(t) for j in range(i+1,t))
    return F.trace(F.mul(beta,e2)^marked^F.mul(eta,lin))^xor(int(tr&m==m) for m in phi)

def physical_quadratic(D,F,beta,eta,phi):
    n=F.a*len(D)**2;value=lambda x:physical_value(x,D,F,beta,eta,phi)
    constant=value(0);linear=sum((value(1<<i)^constant)<<i for i in range(n));rows=[0]*n
    for i in range(n):
        for j in range(i):
            b=value((1<<i)|(1<<j))^constant^((linear>>i)&1)^((linear>>j)&1)
            if b:rows[i]^=1<<j;rows[j]^=1<<i
    return rows,linear,constant

def annihilator_basis(K,t,F):
    rows=kernel(K,F,t);basis=[]
    for i in range(t):
        for r in rows:
            for bit in range(F.a):
                basis.append(sum(F.mul(1<<bit,c)<<(F.a*(i*t+j)) for j,c in enumerate(r)))
    return basis

def restricted_gaussian(basis,rows,linear,constant):
    polars=[xor(rows[i] for i in bits(x)) for x in basis]
    B=[sum(((x&v).bit_count()&1)<<j for j,v in enumerate(basis)) for x in polars]
    l=sum(quadratic_value(v,rows,linear,0)<<i for i,v in enumerate(basis))
    return packed_gaussian(B,l,constant)

def complete_kernel_oracle(exponent,h,f,parameters):
    begun=time.perf_counter();F=Field(h);q=F.q;t=2*exponent;D=block_primary(exponent,f)
    sources=[physical_quadratic(D,F,beta,eta,phi) for beta,eta,phi in parameters]
    moments=[[0]*(t+1) for _ in sources];counts=[0]*(t+1)
    for K in subspaces(t,F):
        k=len(K);counts[k]+=1;basis=annihilator_basis(K,t,F)
        for i,source in enumerate(sources):moments[i][k]+=restricted_gaussian(basis,*source)
    onto=[1]
    for k in range(t):onto.append(onto[-1]*(q**t-q**k))
    results=[]
    for (beta,eta,phi),row in zip(parameters,moments):
        expected=q**(t*t)*sum(a*b for a,b in zip(onto,row))
        actual,meta=cyclic_quadratic_primary_gap(exponent,h,f,beta,phi,eta)
        assert actual==expected,(exponent,h,beta,eta,phi,actual,expected)
        results.append(dict(beta=beta,eta=eta,phi=sorted(phi),gap=actual,
            original_bits=3*F.a*t*t,kernel_signed_moments=row))
    out=dict(exponent=exponent,h=h,irreducible=f,physical_operator=D,
        actual_subspaces=sum(counts),subspaces_by_dimension=counts,
        quadratic_kernel_evaluations=sum(counts)*len(sources),cases=results,
        seconds=time.perf_counter()-begun)
    print('independent physical kernels',exponent,h,sum(counts),len(results),out['seconds'],flush=True)
    return out

def literal_square_oracle():
    begun=time.perf_counter();F=Field(3);t=4;D=block_primary(2,[1,1,1])
    parameters=[(beta,eta,{1} if alpha else set()) for beta,eta,alpha in itertools.product(range(2),repeat=3)]
    sources=[physical_quadratic(D,F,*p) for p in parameters];totals=[0]*len(parameters)
    for x in range(1<<(t*t)):
        r=len(rref(matrix(x,t,F),F,t)[1]);weight=1<<(t*(t-r))
        for i,source in enumerate(sources):totals[i]+=(1-2*quadratic_value(x,*source))*weight
    rows=[]
    for (beta,eta,phi),expected in zip(parameters,totals):
        expected<<=t*t;actual,_=cyclic_quadratic_primary_gap(2,3,[1,1,1],beta,phi,eta)
        assert actual==expected
        rows.append(dict(beta=beta,eta=eta,phi=sorted(phi),gap=actual))
    return dict(exponent=2,literal_X=1<<(t*t),cases=rows,seconds=time.perf_counter()-begun)

if __name__=='__main__':
    begun=time.perf_counter();gaussian=audit_gaussian();literal=literal_square_oracle()
    binary=[(beta,eta,{1} if alpha else set()) for beta,eta,alpha in itertools.product(range(2),repeat=3)]
    kernels=[complete_kernel_oracle(3,3,[1,1,1],binary),
        complete_kernel_oracle(2,7,[2,1,1],[(1,2,{3}),(3,2,{0,1,3}),(2,1,{0,2,3}),(0,3,{3})])]
    result=dict(gaussian=gaussian,literal=literal,kernels=kernels,
        actual_subspaces=sum(x['actual_subspaces'] for x in kernels),
        quadratic_kernel_evaluations=sum(x['quadratic_kernel_evaluations'] for x in kernels),
        seconds=time.perf_counter()-begun)
    path=Path(__file__).with_name('cyclic_quadratic_primary_independent_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n');print('saved',path,result['seconds'],flush=True)
