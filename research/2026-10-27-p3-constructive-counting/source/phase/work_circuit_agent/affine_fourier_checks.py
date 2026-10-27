#!/usr/bin/env python3
"""Exact finite checks for counting fixed-width CNF on an affine subspace.

This program DOES NOT implement the governing paper's subexponential SAT counter.
Every Fourier coefficient is evaluated by explicitly labeled exhaustive summation.
The execution validates the reduction and the disjoint affine recursion only.
All integer arithmetic is exact. Standard library only.
"""
from itertools import product
from pathlib import Path
import json, math, random


def rref(n, equations):
    rows={}
    for mask,rhs in equations:
        mask &= (1<<n)-1
        rhs &= 1
        for p in sorted(rows):
            if mask>>p&1:
                mask ^= rows[p][0]
                rhs ^= rows[p][1]
        if not mask:
            if rhs:return None
            continue
        p=(mask&-mask).bit_length()-1
        for q,(a,b) in list(rows.items()):
            if a>>p&1: rows[q]=(a^mask,b^rhs)
        rows[p]=(mask,rhs)
    return [rows[p] for p in sorted(rows)]


def affine_parameterization(n, reduced):
    pivots=[(a&-a).bit_length()-1 for a,b in reduced]
    free=[i for i in range(n) if i not in pivots]
    fpos={v:i for i,v in enumerate(free)}
    forms=[None]*n
    for v in free:forms[v]=(1<<fpos[v],0)
    for a,b in reduced:
        p=(a&-a).bit_length()-1
        mask=sum(1<<fpos[v] for v in free if a>>v&1)
        forms[p]=(mask,b)
    return forms,free


def satisfied(x, clauses):
    return all(any(((x>>(abs(lit)-1))&1) ^ int(lit<0) for lit in c) for c in clauses)


def direct_count(n, clauses, equations):
    return sum(satisfied(x,clauses) and all(((x&a).bit_count()&1)==b for a,b in equations)
               for x in range(1<<n))


def signed_count_by_exhaustive_summation(n,clauses,character):
    return sum((-1 if (x&character).bit_count()&1 else 1)
               for x in range(1<<n) if satisfied(x,clauses))


def fourier_projection_check(n,clauses,equations):
    reduced=rref(n,equations)
    if reduced is None:return 0,0,0
    rank=len(reduced)
    accumulator=0
    negatives=0
    for selector in range(1<<rank):
        character,sign=0,0
        for i,(row,rhs) in enumerate(reduced):
            if selector>>i&1:
                character ^= row
                sign ^= rhs
        coefficient=signed_count_by_exhaustive_summation(n,clauses,character)
        negatives+=coefficient<0
        accumulator+=(-coefficient if sign else coefficient)
        assert abs(accumulator).bit_length()<=n+rank+1
    assert accumulator%(1<<rank)==0
    result=accumulator//(1<<rank)
    assert 0<=result<=1<<(n-rank)
    return result,1<<rank,negatives


def affine_branch_count(n,clauses,equations):
    stats={'nodes':0,'leaves':0,'max_depth':0,'branch_widths':{}}
    def visit(current,depth=0):
        stats['nodes']+=1
        stats['max_depth']=max(stats['max_depth'],depth)
        reduced=rref(n,current)
        if reduced is None:return 0
        d=n-len(reduced)
        forms,free=affine_parameterization(n,reduced)
        for clause in clauses:
            local=[]
            for lit in clause:
                a,b=forms[abs(lit)-1]
                local.append((a,b^int(lit<0)))
            # If all literals cannot be zero together, this clause is tautological here.
            zeros=rref(d,local)
            if zeros is None:continue
            if len(zeros)==0:return 0
            # Choose independent coefficient vectors of original literals.
            independent=[]
            basis=[]
            for lit,(a,b) in zip(clause,local):
                extended=rref(d,basis+[(a,0)])
                if len(extended)>len(basis):
                    independent.append(lit)
                    basis=extended
            j=len(independent)
            assert j==len(zeros) and 1<=j<=len(clause)
            stats['branch_widths'][j]=stats['branch_widths'].get(j,0)+1
            result=0
            prefix=[]
            for index,lit in enumerate(independent):
                v=abs(lit)-1
                zero=int(lit<0)
                branch=reduced+prefix+[(1<<v,zero^1)]
                child=rref(n,branch)
                assert child is not None and len(child)==len(reduced)+index+1
                result+=visit(child,depth+1)
                prefix.append((1<<v,zero))
            return result
        stats['leaves']+=1
        return 1<<d
    return visit(equations),stats


def random_instance(n,rank,k,rng):
    planted=rng.randrange(1<<n)
    rows=[]
    for j in range(rank):
        row=(1<<j)
        for v in range(rank,n):
            if rng.randrange(2):row^=1<<v
        rows.append(row)
    if rank>1:
        for _ in range(4*rank):
            i,j=rng.sample(range(rank),2)
            rows[i]^=rows[j]
    equations=[(a,(a&planted).bit_count()&1) for a in rows]
    if rows:
        a=rows[0]^rows[-1]
        equations.append((a,(a&planted).bit_count()&1))
    clauses=[]
    for _ in range(2*n+1):
        vs=rng.sample(range(n),min(k,n))
        c=[(v+1)*(1 if rng.randrange(2) else -1) for v in vs]
        if not satisfied(planted,[c]):c[0]*=-1
        clauses.append(c)
    return clauses,equations


def compile_xor_program(n, rows):
    # Each record is XOR of two previously available original/gate coordinates.
    gates=[]
    outputs=[]
    for mask in rows:
        support=[v for v in range(n) if mask>>v&1]
        if not support:outputs.append(None);continue
        acc=support[0]
        for v in support[1:]:
            gates.append((acc,v))
            acc=n+len(gates)-1
        outputs.append(acc)
    return gates,outputs


def recover_affine_program_forms(n,gates,outputs):
    forms=[1<<i for i in range(n)]
    for a,b in gates:forms.append(forms[a]^forms[b])
    return [0 if out is None else forms[out] for out in outputs]


def gamma(k):
    lo,hi=1.0,2.0
    for _ in range(80):
        mid=(lo+hi)/2
        if sum(mid**(-i) for i in range(1,k+1))>1:lo=mid
        else:hi=mid
    return (lo+hi)/2


def main():
    rng=random.Random(107727)
    records=[]
    negative_coefficients=0
    for n in range(2,11):
        for rank in range(n+1):
            k=2+(n+rank)%2
            clauses,equations=random_instance(n,rank,k,rng)
            direct=direct_count(n,clauses,equations)
            projected,terms,neg=fourier_projection_check(n,clauses,equations)
            recursive,stats=affine_branch_count(n,clauses,equations)
            assert direct==projected==recursive
            negative_coefficients+=neg
            records.append({'n':n,'rank':rank,'k':k,'count':direct,
                            'fourier_terms':terms,'affine_recursion':stats})
    # An inconsistent duplicate constraint is recognized before projection.
    inconsistent=[(3,0),(3,1)]
    assert direct_count(4,[],inconsistent)==0
    assert fourier_projection_check(4,[],inconsistent)[0]==0
    assert affine_branch_count(4,[],inconsistent)[0]==0
    # Dense affine program family n=2r, r rows [I_r | J_r-I_r].
    n,rank=14,7
    right=((1<<rank)-1)<<rank
    rows=[(1<<i)|(right^(1<<(rank+i))) for i in range(rank)]
    gates,outputs=compile_xor_program(n,rows)
    assert len(gates)==rank*(rank-1)
    recovered=recover_affine_program_forms(n,gates,outputs)
    assert recovered==rows
    planted=rng.randrange(1<<n)
    equations=[(a,(a&planted).bit_count()&1) for a in rows]
    clauses,_=random_instance(n,rank,3,rng)
    direct=direct_count(n,clauses,equations)
    projected,terms,neg=fourier_projection_check(n,clauses,equations)
    recursive,stats=affine_branch_count(n,clauses,equations)
    assert direct==projected==recursive
    dense={'n':n,'rank':rank,'naive_XOR_internal_states':len(gates),
           'total_original_plus_XOR_states':n+len(gates),
           'family_internal_state_formula':'n*(n-2)/4 for even n',
           'matrix_recovered_from_program_exactly':True,
           'count':direct,'fourier_terms':terms,'affine_recursion':stats,
           'clauses':clauses,'linear_equations':equations,'xor_gates':gates,'outputs':outputs}
    exponents=[]
    for k in (2,3,4,5,8):
        g=gamma(k);alpha=math.log2(g);beta=alpha/(1+alpha)
        exponents.append({'k':k,'gamma_k':g,'alpha_k':alpha,
                          'hybrid_exponent_beta_k':beta,'hybrid_base':2**beta})
    result={'finite_fixtures_passed':len(records)+2,
            'negative_Fourier_coefficients_observed':negative_coefficients+neg,
            'subexponential_counter_implemented':False,
            'fourier_coefficients_evaluated_by':'exact exhaustive summation',
            'fixtures':records,'dense_XOR_program':dense,'exponents':exponents}
    Path(__file__).with_name('affine_fourier_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'finite_fixtures_passed':result['finite_fixtures_passed'],
                      'negative_Fourier_coefficients_observed':result['negative_Fourier_coefficients_observed'],
                      'dense_XOR_program':{k:v for k,v in dense.items() if k not in ('clauses','linear_equations','xor_gates','outputs')},
                      'exponents':exponents,
                      'subexponential_counter_implemented':False},indent=2))

if __name__=='__main__':main()
