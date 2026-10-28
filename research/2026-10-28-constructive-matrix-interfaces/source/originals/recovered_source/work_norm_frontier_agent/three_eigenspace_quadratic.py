#!/usr/bin/env python3
"""Raw three-eigenvalue square-source counting through the finite D4 quiver.

Kernel orbits are manufactured as sums of eleven fixed indecomposables;
their multiplicities follow from a fixed Hom table and exact automorphism
group orders. No kernel decomposition is supplied to the raw compiler.
"""
from functools import lru_cache
import time
from nonsplit_quadratic_orbits import (quadratic_anf,quadratic_anf_sum,
    acquire_square_source_parameters,algebra_scalar_embedding,polynomial_value,
    hidden_groups,AcquiredMatrixAlgebra,acquire_center,identity,inverse,bits,
    linear_apply,solve,Field,choose,gl_order)
from matrix_kloosterman import factor_polynomial

def xor(values):
    result=0
    for value in values:result^=value
    return result

def d4_types():
    """(name, vertex dimensions [center,three leaves], three row maps)."""
    out=[]
    for i in range(3):
        dims=[0,0,0,0];dims[i+1]=1
        out.append((f'outer_{i}',tuple(dims),tuple([()] if j==i else [] for j in range(3))))
    for mask in range(1,8):
        dims=(1,)+tuple(int(mask>>i&1) for i in range(3))
        out.append((f'support_{mask}',dims,tuple([(1,)] if mask>>i&1 else [] for i in range(3))))
    out.append(('three_lines',(2,1,1,1),([(1,0)],[(0,1)],[(1,1)])))
    return tuple(out)

TYPES=d4_types()

def binary_rank(rows):
    pivots={}
    for v in rows:
        while v:
            bit=v.bit_length()-1
            if bit not in pivots:pivots[bit]=v;break
            v^=pivots[bit]
    return len(pivots)

@lru_cache(None)
def hom_dimension(source,target):
    """Solve the fixed commuting-square system over the prime field."""
    _,sd,sa=TYPES[source];_,td,ta=TYPES[target]
    offsets=[];variables=0
    for s,t in zip(sd,td):offsets.append(variables);variables+=s*t
    equations=[]
    for i in range(3):
        for row in range(td[i+1]):
            for col in range(sd[0]):
                equation=0
                for k in range(sd[i+1]):
                    if sa[i][k][col]:equation^=1<<(offsets[i+1]+row*sd[i+1]+k)
                for k in range(td[0]):
                    if ta[i][row][k]:equation^=1<<(offsets[0]+k*sd[0]+col)
                equations.append(equation)
    return variables-binary_rank(equations)

HOM=tuple(tuple(hom_dimension(i,j) for j in range(11)) for i in range(11))
if any(HOM[i][i]!=1 for i in range(11)):raise AssertionError('D4 brick endomorphism check')

def d4_multiplicities(ranks):
    """Enumerate eight active multiplicities; three outer simples are forced."""
    active=list(range(3,11));parts=[0]*11
    def visit(index,remaining):
        if index==len(active):
            parts[:3]=remaining
            yield tuple(parts)
            return
        number=active[index];dims=TYPES[number][1][1:]
        maximum=min(remaining[i] for i in range(3) if dims[i])
        for count in range(maximum+1):
            parts[number]=count
            yield from visit(index+1,tuple(remaining[i]-count*dims[i] for i in range(3)))
    yield from visit(0,tuple(ranks))

def d4_orbit_multiplicity(ranks,parts,q):
    end_dimension=sum(parts[i]*parts[j]*HOM[i][j] for i in range(11) for j in range(11))
    radical_dimension=end_dimension-sum(m*m for m in parts)
    if radical_dimension<0:raise AssertionError('negative endomorphism radical dimension')
    aut=q**radical_dimension
    for multiplicity in parts:aut*=gl_order(multiplicity,q)
    numerator=1
    for dimension in ranks:numerator*=gl_order(dimension,q)
    value,remainder=divmod(numerator,aut)
    if remainder:raise AssertionError('D4 stabilizer does not divide ambient group order')
    return value

def canonical_column_map(ranks,parts):
    """Columns of matrices annihilating the canonical D4 kernel."""
    t=sum(ranks);offsets=[0,ranks[0],ranks[0]+ranks[1]];used=[0]*3
    column_masks=[None]*t;free=0;kernel=0
    for number in range(3,11):
        for _ in range(parts[number]):
            if number==10:
                columns=[]
                for leaf in range(3):
                    columns.append(offsets[leaf]+used[leaf]);used[leaf]+=1
                for col in columns:column_masks[col]=1<<free
                free+=1;kernel+=2
            else:
                mask=number-2;columns=[]
                for leaf in range(3):
                    if mask>>leaf&1:columns.append(offsets[leaf]+used[leaf]);used[leaf]+=1
                total=0
                for col in columns[:-1]:column_masks[col]=1<<free;total^=1<<free;free+=1
                column_masks[columns[-1]]=total;kernel+=1
    for leaf in range(3):
        if ranks[leaf]-used[leaf]!=parts[leaf]:raise AssertionError('outer-simple multiplicity')
        while used[leaf]<ranks[leaf]:
            col=offsets[leaf]+used[leaf];used[leaf]+=1;column_masks[col]=1<<free;free+=1
    if free+kernel!=t or any(v is None for v in column_masks):raise AssertionError('canonical kernel rank')
    return column_masks,free,kernel

def restrict_column_relations(poly,t,a,column_masks,free_columns):
    mapping=[]
    for row in range(t):
        for mask in column_masks:
            for bit in range(a):
                mapping.append(sum(1<<(a*(row*free_columns+col)+bit) for col in bits(mask)))
    out=set()
    for monomial in poly:
        image={0}
        for bit in bits(monomial):
            new=set()
            for old in image:
                for target in bits(mapping[bit]):
                    product=old|(1<<target)
                    if product in new:new.remove(product)
                    else:new.add(product)
            image=new
        out.symmetric_difference_update(image)
    return out,a*t*free_columns

def diagonal_source_value(packed,ranks,eigenvalues,F,beta,phi):
    t=sum(ranks);labels=sum(([value]*size for value,size in zip(eigenvalues,ranks)),[])
    X=[[(packed>>(F.a*(i*t+j)))&(F.q-1) for j in range(t)] for i in range(t)]
    trace=xor(X[i][i] for i in range(t));value=0
    for i in range(t):
        value^=F.mul(labels[i],F.mul(X[i][i],X[i][i]))
        for j in range(i+1,t):
            value^=F.mul(beta,F.mul(X[i][i],X[j][j]))
            value^=F.mul(beta^labels[i]^labels[j],F.mul(X[i][j],X[j][i]))
    return F.trace(value)^polynomial_value(phi,trace)

def three_eigenspace_gap(ranks,field_h,eigenvalues,beta,phi):
    ranks=tuple(ranks);eigenvalues=tuple(eigenvalues);phi=set(phi);F=Field(field_h);q=F.q
    if len(ranks)!=3 or any(type(r) is not int or r<0 for r in ranks) or not sum(ranks):
        raise ValueError('three nonnegative dimensions with positive sum required')
    if len(eigenvalues)!=3 or any(not 0<=v<q for v in eigenvalues) or not 0<=beta<q:
        raise ValueError('invalid field coefficients')
    if any(type(m) is not int or m<0 or m.bit_length()>F.a or m.bit_count()>2 for m in phi):
        raise ValueError('trace source must be a Boolean quadratic')
    t=sum(ranks);d=F.a*t*t
    native=quadratic_anf(lambda x:diagonal_source_value(x,ranks,eigenvalues,F,beta,phi),d)
    counts=[0]*(t+1);moments=[0]*(t+1);onto=[1];layers=[]
    for k in range(t):onto.append(onto[-1]*(q**t-q**k))
    for parts in d4_multiplicities(ranks):
        multiplicity=d4_orbit_multiplicity(ranks,parts,q)
        column_map,free,k=canonical_column_map(ranks,parts)
        restricted,dimension=restrict_column_relations(native,t,F.a,column_map,free)
        value=quadratic_anf_sum(restricted,dimension)
        counts[k]+=multiplicity;moments[k]+=multiplicity*value
        layers.append(dict(indecomposable_multiplicities=parts,kernel_dimension=k,
            multiplicity=multiplicity,restricted_bits=dimension,quadratic_sum=value))
    if counts!=[choose(t,k,q) for k in range(t+1)]:raise AssertionError('D4 orbits do not exhaust Grassmannians')
    gap=q**(t*t)*sum(onto[k]*moments[k] for k in range(t+1))
    return gap,dict(route='three eigenspaces, manufactured D4 kernel orbit sum',
        matrix_size=t,field_degree=F.a,field_modulus=field_h,eigenspace_dimensions=ranks,
        eigenvalues=eigenvalues,beta=beta,trace_quadratic_anf=sorted(phi),
        kernel_moments=moments,kernel_orbit_layers=layers,hom_table=HOM,
        uniform_polynomial_time=True,enumerated_subspaces=0,enumerated_field_elements=0,
        enumerated_original_assignments=0)

def acquire_three_eigenspaces(D,algebra):
    """Certify and acquire the three eigenspaces from an intrinsic operator."""
    F=algebra.F;a=algebra.a
    scalar_columns,scalar_element=algebra_scalar_embedding(algebra)
    powers=[algebra.one];columns=[];minimal=None
    for degree in range(1,4):
        columns.extend(algebra.mul(scalar_element(1<<i),powers[-1]) for i in range(a))
        powers.append(algebra.mul(powers[-1],D))
        solution=solve(columns,powers[-1])
        if solution is not None:
            minimal=[(solution>>(a*i))&(F.q-1) for i in range(degree)]+[1]
            break
    if minimal is None or len(minimal)!=4:raise ValueError('source operator does not have degree-three minimal polynomial')
    factors=factor_polynomial(minimal,F)
    if len(factors)!=3 or any(len(g)!=2 or multiplicity!=1 for g,multiplicity in factors):
        raise ValueError('source operator does not have three distinct split eigenvalues')
    eigenvalues=sorted(g[0] for g,multiplicity in factors);projectors=[];ranks=[]
    for value in eigenvalues:
        projector=algebra.one;denominator=1
        for other in eigenvalues:
            if other!=value:
                projector=algebra.mul(projector,D^scalar_element(other))
                denominator=F.mul(denominator,value^other)
        projector=algebra.mul(scalar_element(F.inv(denominator)),projector)
        if algebra.mul(projector,projector)!=projector:raise AssertionError('acquired eigenspace projector')
        projectors.append(projector);ranks.append(algebra.reduced_rank(projector))
    if xor(projectors)!=algebra.one or sum(ranks)!=algebra.t or min(ranks)<=0:
        raise AssertionError('acquired projectors do not resolve the whole matrix space')
    if any(algebra.mul(x,y) for i,x in enumerate(projectors) for j,y in enumerate(projectors) if i!=j):
        raise AssertionError('acquired eigenspace projectors are not orthogonal')
    if xor(algebra.mul(scalar_element(value),P) for value,P in zip(eigenvalues,projectors))!=D:
        raise AssertionError('source operator reconstruction')
    return ranks,eigenvalues,dict(acquired_minimal_polynomial=minimal,
        acquired_eigenvalues=eigenvalues,acquired_projectors=projectors,eigenspace_dimensions=ranks)

def count_acquired_three_eigenspace_source(algebra,beta,D,phi):
    ranks,eigenvalues,evidence=acquire_three_eigenspaces(D,algebra)
    gap,backend=three_eigenspace_gap(ranks,algebra.h,eigenvalues,beta,phi)
    backend.update(evidence)
    backend.update(operator_class='three split eigenspaces')
    return gap,backend

def fit_three_eigenspace_source(poly,algebra):
    beta,D,phi,evidence=acquire_square_source_parameters(poly,algebra)
    ranks,eigenvalues,spectral=acquire_three_eigenspaces(D,algebra)
    evidence.update(spectral)
    return ranks,eigenvalues,beta,phi,evidence

def compile_raw_three_eigenspace_quadratic(poly,n):
    begun=time.perf_counter();poly=set(poly)
    if type(n) is not int or n<=0 or any(type(m) is not int or m<0 or m.bit_length()>n or m.bit_count()>3 for m in poly):
        raise ValueError('raw cubic Boolean ANF required')
    grouped,slices,group_map,stats=hidden_groups(poly,n)
    algebra=AcquiredMatrixAlgebra(slices);d=algebra.d
    centered,offset=acquire_center(grouped,slices,d,allow_within=True)
    lower=[m for m in centered if 0<m.bit_count()<=2]
    groups={i//d for m in lower for i in bits(m)}
    if len(groups)!=1:raise ValueError('nonconstant source must occupy one acquired group')
    group=next(iter(groups));local={m>>(group*d) for m in lower}
    if 0 in centered:local.add(0)
    back=inverse([identity(d),algebra.Y,algebra.Z][group])
    source=quadratic_anf(lambda x:polynomial_value(local,linear_apply(back,x)),d)
    ranks,eigenvalues,beta,phi,evidence=fit_three_eigenspace_source(source,algebra)
    gap,backend=three_eigenspace_gap(ranks,algebra.h,eigenvalues,beta,phi)
    if abs(gap)>1<<n or gap%2:raise AssertionError('invalid original-domain count')
    stats.update(algebra.stats);stats.update(evidence)
    stats.update(backend=backend,raw_monomials=len(poly),affine_offset=offset,
        quadratic_group=group,supplied_unit_or_eigenspaces=False,seconds=time.perf_counter()-begun)
    return dict(original_bits=n,zeros=((1<<n)+gap)//2,ones=((1<<n)-gap)//2,gap=gap,stats=stats)
