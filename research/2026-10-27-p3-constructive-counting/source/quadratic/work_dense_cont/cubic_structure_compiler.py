#!/usr/bin/env python3
"""Exact cubic radical/centroid compiler and hidden-forest counter over F2.

The linear-algebra structure machinery is established prior art. The code
executes representation discovery, Gaussian elimination, and exact sums.
It does not claim a generic subexponential dense-cubic algorithm.
"""
import itertools
import json
import random
from pathlib import Path


def indices(mask):
    while mask:
        bit=mask&-mask
        yield bit.bit_length()-1
        mask^=bit


def xor_all(values):
    out=0
    for v in values: out^=v
    return out


def rref(rows,n):
    basis={}
    for row in rows:
        while row & ((1<<n)-1):
            p=(row&-row).bit_length()-1
            if p in basis: row^=basis[p]
            else:
                basis[p]=row
                break
        else:
            if row: return None
    for p in sorted(basis,reverse=True):
        for j in list(basis):
            if j<p and basis[j]>>p&1: basis[j]^=basis[p]
    return basis


def nullspace(rows,n):
    basis=rref(rows,n)
    assert basis is not None
    free=[i for i in range(n) if i not in basis]
    return [(1<<f)|sum((1<<p) for p,row in basis.items() if row>>f&1)
            for f in free]


def affine_solve(rows,n):
    basis=rref(rows,n)
    if basis is None: return None
    particular=sum(1<<p for p,row in basis.items() if row>>n&1)
    kernel=[(1<<f)|sum(1<<p for p,row in basis.items() if row>>f&1)
            for f in range(n) if f not in basis]
    return particular,kernel


def affine_inconsistency_witness(rows,n):
    """Return equation indices whose XOR is the impossible equation 0=1."""
    basis={}
    linear_mask=(1<<n)-1
    for i,original in enumerate(rows):
        row=original; combination=1<<i
        while row&linear_mask:
            p=(row&-row).bit_length()-1
            if p in basis:
                old,used=basis[p]
                row^=old;combination^=used
            else:
                basis[p]=(row,combination)
                break
        else:
            if row:
                assert row==1<<n
                witness=list(indices(combination))
                assert xor_all(rows[j] for j in witness)==1<<n
                return witness
    return None


def independent(values):
    basis={}; keep=[]
    for value in values:
        x=value
        while x:
            p=(x&-x).bit_length()-1
            if p in basis: x^=basis[p]
            else:
                basis[p]=x;keep.append(value);break
    return keep


def apply(cols,x): return xor_all(cols[i] for i in indices(x))
def compose(a,b): return [apply(a,x) for x in b]
def mat_xor(a,b): return [x^y for x,y in zip(a,b)]
def flat(cols,n): return sum(x<<(n*i) for i,x in enumerate(cols))
def unflat(x,n): return [(x>>(n*i))&((1<<n)-1) for i in range(n)]


def poly_mul(a,b):
    out=set()
    for x in a:
        for y in b:
            z=x|y
            if z in out: out.remove(z)
            else: out.add(z)
    return out


def substitute(poly,n,cols,offset=0):
    linear=[{1<<j for j,c in enumerate(cols) if c>>i&1}
            ^({0} if offset>>i&1 else set()) for i in range(n)]
    out=set()
    for term in poly:
        product={0}
        for i in indices(term): product=poly_mul(product,linear[i])
        out.symmetric_difference_update(product)
    return out


def phase(poly,x): return -1 if sum((x&s)==s for s in poly)&1 else 1
def brute(poly,n): return sum(phase(poly,x) for x in range(1<<n))


def tensor_pairs(poly,n):
    pair=[[0]*n for _ in range(n)]
    for mask in poly:
        if mask.bit_count()!=3: continue
        a,b,c=indices(mask)
        for i,j,k in ((a,b,c),(a,c,b),(b,c,a)):
            pair[i][j]^=1<<k
            pair[j][i]^=1<<k
    return pair


def radical(poly,n):
    pair=tensor_pairs(poly,n)
    return nullspace((pair[i][j] for i in range(n) for j in range(i+1,n)),n)


def radical_step(poly,n,rad,certificate=None):
    original_rad=len(rad)
    complete=independent(rad+[1<<i for i in range(n)])
    assert len(complete)==n and complete[:len(rad)]==rad
    cols=complete[len(rad):]+rad
    d=n-len(rad)
    p=substitute(poly,n,cols)
    assert all(s.bit_count()!=3 or s<(1<<d) for s in p)
    active=set(range(d,n)); pairs=0;pair_updates=[]
    while True:
        term=next((s for s in p if s.bit_count()==2 and all(i in active for i in indices(s))),None)
        if term is None: break
        i,j=indices(term)
        bi,bj=1<<i,1<<j
        a={s^bi for s in p if s&bi and not s&bj}
        b={s^bj for s in p if s&bj and not s&bi}
        c={s for s in p if not s&(bi|bj)}
        assert all(s.bit_count()<=1 for s in a|b)
        p=c^poly_mul(a,b)
        pair_updates.append(dict(variables=[i,j],affine_A=sorted(a),
                                 affine_B=sorted(b),output_polynomial=sorted(p)))
        active.remove(i);active.remove(j);pairs+=1
    equations=[]
    for i in sorted(active):
        a={s^(1<<i) for s in p if s>>i&1}
        assert all(s==0 or (s.bit_count()==1 and s<(1<<d)) for s in a)
        equations.append(xor_all(s for s in a if s) | ((1<<d) if 0 in a else 0))
    p={s for s in p if all(i not in active for i in indices(s))}
    metadata=dict(input_variables=n,input_polynomial=sorted(poly),
                  third_tensor_rank=d,radical_dimension=original_rad,
                  radical_basis=list(rad),complement_columns=cols[:d],
                  coordinate_columns=cols,gaussian_pairs=pairs,
                  gaussian_pair_updates=pair_updates,
                  remaining_radical_variables=sorted(active),
                  linear_equations=equations,
                  pre_affine_polynomial=sorted(p),
                  factor_exponent=pairs+len(active))
    result=affine_solve(equations,d)
    if result is None:
        metadata['inconsistent_equation_subset']=affine_inconsistency_witness(equations,d)
        assert metadata['inconsistent_equation_subset'] is not None
        if certificate is not None: certificate.update(metadata)
        return None
    offset,kernel=result
    reduced=substitute(p,d,kernel,offset)
    metadata.update(linear_constraint_rank=d-len(kernel),
                    affine_offset=offset,affine_kernel_columns=kernel,
                    output_variables=len(kernel),output_polynomial=sorted(reduced))
    if certificate is not None: certificate.update(metadata)
    return reduced,len(kernel),pairs+len(active),metadata


def eliminate_radical(poly,n,zero_certificate=None):
    factor=0; rounds=[]
    while n:
        rad=radical(poly,n)
        if not rad: break
        record={}
        step=radical_step(poly,n,rad,record)
        if step is None:
            if zero_certificate is not None:
                zero_certificate.update(prior_factor_exponent=factor,
                                        prior_rounds=rounds,failed_round=record)
            return None
        poly,n,power,record=step
        factor+=power;rounds.append(record)
    return poly,n,factor,rounds


def centroid_blocks(poly,n):
    if n==0: return [],dict(centroid_dimension=0,idempotent_dimension=0)
    assert not radical(poly,n)
    pair=tensor_pairs(poly,n)
    equations=[]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                equations.append((pair[j][k]<<(n*i))^(pair[i][k]<<(n*j)))
                equations.append((pair[j][k]<<(n*i))^(pair[i][j]<<(n*k)))
    center=nullspace(equations,n*n)
    matrices=[unflat(x,n) for x in center]
    for a in matrices:
        for b in matrices:
            assert compose(a,b)==compose(b,a)
    frob=[flat(mat_xor(compose(a,a),a),n) for a in matrices]
    constraints=[0]*(n*n)
    for j,col in enumerate(frob):
        for i in indices(col): constraints[i]^=1<<j
    idem_coeffs=nullspace(constraints,len(center))
    idempotents=[unflat(xor_all(center[i] for i in indices(c)),n) for c in idem_coeffs]
    projectors=[[1<<i for i in range(n)]]
    for e in idempotents:
        assert compose(e,e)==e
        new=[]
        for p in projectors:
            pe=compose(p,e)
            other=mat_xor(p,pe)
            if any(pe): new.append(pe)
            if any(other): new.append(other)
        projectors=new
    blocks=[independent(p) for p in projectors]
    assert sum(map(len,blocks))==n
    assert len(blocks)==len(idem_coeffs)
    return blocks,dict(centroid_dimension=len(center),idempotent_dimension=len(idem_coeffs))


def forest_sum(poly,n,block_sizes):
    groups=[]; cursor=0
    for size in block_sizes:
        groups.append(list(range(cursor,cursor+size)));cursor+=size
    location={v:(i,j) for i,g in enumerate(groups) for j,v in enumerate(g)}
    local=[set() for _ in groups];edges={};constant=int(0 in poly)
    for term in poly-{0}:
        touched={location[v][0] for v in indices(term)}
        if len(touched)==1:
            i=next(iter(touched))
            local[i].add(sum(1<<location[v][1] for v in indices(term)))
        else:
            assert term.bit_count()==2 and len(touched)==2
            i,j=sorted(touched)
            edge=edges.setdefault((i,j),[])
            vertices=list(indices(term))
            first=next(v for v in vertices if location[v][0]==i)
            second=next(v for v in vertices if location[v][0]==j)
            edge.append((location[first][1],location[second][1]))
    adjacent=[[] for _ in groups]
    for i,j in edges: adjacent[i].append(j);adjacent[j].append(i)
    visited=set(); total=(-1)**constant
    def interaction(i,xi,j,xj):
        if i>j: i,j,xi,xj=j,i,xj,xi
        return (-1)**(sum(((xi>>u)&1)*((xj>>v)&1) for u,v in edges[(i,j)])&1)
    def visit(i,parent):
        if i in visited: raise ValueError('quadratic coupling graph has a cycle')
        visited.add(i)
        weights=[phase(local[i],x) for x in range(1<<block_sizes[i])]
        for child in adjacent[i]:
            if child==parent: continue
            child_weights=visit(child,i)
            for x in range(len(weights)):
                weights[x]*=sum(w*interaction(i,x,child,y) for y,w in enumerate(child_weights))
        return weights
    for i in range(len(groups)):
        if i not in visited: total*=sum(visit(i,-1))
    return total,len(edges)


def compile_and_count(poly,n):
    zero_certificate={}
    reduction=eliminate_radical(poly,n,zero_certificate)
    if reduction is None:
        return dict(count=0,balanced_by_linear_constraint=True,
                    zero_certificate=zero_certificate)
    p,ncore,power,rounds=reduction
    blocks,meta=centroid_blocks(p,ncore)
    cols=[v for block in blocks for v in block]
    transformed=substitute(p,ncore,cols)
    sizes=list(map(len,blocks))
    forest=True
    try:
        value,edges=forest_sum(transformed,ncore,sizes)
    except ValueError:
        forest=False;edges=None;value=brute(transformed,ncore)
    return dict(count=(1<<power)*value,core_variables=ncore,
                factor_exponent=power,radical_rounds=rounds,
                block_sizes=sizes,quadratic_coupling_forest=forest,
                quadratic_coupling_edges=edges,**meta)


def random_invertible(n,rng):
    cols=[1<<i for i in range(n)]
    if n>1:
        for _ in range(12*n):
            i,j=rng.sample(range(n),2)
            cols[i]^=cols[j]
    assert len(independent(cols))==n
    return cols


def validate():
    rng=random.Random(20261102)
    records=[]
    for n in range(3,10):
        for trial in range(4):
            universe=[sum(1<<i for i in subset) for d in range(4)
                      for subset in itertools.combinations(range(n),d)]
            p={s for s in universe if rng.randrange(3)==0}
            out=compile_and_count(p,n)
            assert out['count']==brute(p,n)
            records.append(dict(family='random cubic',n=n,trial=trial,**out))
    for n in (6,9,12):
        for chain in (False,True):
            base={7<<(3*i) for i in range(n//3)}
            if chain:
                base.update((1<<(3*i+2))|(1<<(3*i+3)) for i in range(n//3-1))
            p=substitute(base,n,random_invertible(n,rng))
            out=compile_and_count(p,n)
            expected=brute(base,n)
            assert out['count']==expected==brute(p,n) and out['block_sizes']==[3]*(n//3)
            assert out['quadratic_coupling_forest']
            assert out['quadratic_coupling_edges']==(n//3-1 if chain else 0)
            records.append(dict(family='hidden cubic block chain' if chain else 'hidden independent blocks',
                                n=n,canonical_cubic_terms=sum(s.bit_count()==3 for s in p),**out))
    for n in (8,10,12):
        base={7}
        for i in range(3,n-1,2): base.add((1<<i)|(1<<(i+1)))
        base.add((1<<0)|(1<<3))
        p=substitute(base,n,random_invertible(n,rng))
        out=compile_and_count(p,n)
        assert out['count']==brute(base,n)==brute(p,n)
        assert out.get('core_variables',0)<=3
        records.append(dict(family='hidden cubic core plus quadratic directions',n=n,
                            canonical_cubic_terms=sum(s.bit_count()==3 for s in p),**out))
    return dict(status='all assertions passed',fixtures=len(records),records=records,
                scope='Exact structure compiler; no generic dense-cubic subexponential claim')


if __name__=='__main__':
    result=validate()
    Path(__file__).with_name('cubic_structure_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
