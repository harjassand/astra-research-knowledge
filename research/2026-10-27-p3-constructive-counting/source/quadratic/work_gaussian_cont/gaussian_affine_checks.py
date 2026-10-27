#!/usr/bin/env python3
"""Exact finite Gaussian-interface and affine-compiler checks.

Counting is exhaustive. This validates identities/compilers, not a fast solver.
"""
import argparse
import itertools
import json
from pathlib import Path
import random


def bits(mask):
    while mask:
        low=mask&-mask
        yield low.bit_length()-1
        mask^=low


def xor(items):
    result=0
    for item in items:
        result^=item
    return result


def parity(x):
    return x.bit_count()&1


def basis_add(basis,x):
    while x:
        pivot=x.bit_length()-1
        if pivot not in basis:
            basis[pivot]=x
            return True
        x^=basis[pivot]
    return False


def binary_rank(rows):
    basis={}
    for row in rows:
        basis_add(basis,row)
    return len(basis)


def inverse(rows):
    n=len(rows)
    work=[row|((1<<i)<<n) for i,row in enumerate(rows)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if work[i]>>col&1)
        work[col],work[pivot]=work[pivot],work[col]
        for i in range(n):
            if i!=col and work[i]>>col&1:
                work[i]^=work[col]
    assert all(row&((1<<n)-1)==1<<i for i,row in enumerate(work))
    return [row>>n for row in work]


def odd_field_rank(matrix,p=3):
    a=[[x%p for x in row] for row in matrix]
    n=len(a)
    m=len(a[0]) if n else 0
    rank=0
    for col in range(m):
        pivot=next((i for i in range(rank,n) if a[i][col]),None)
        if pivot is None:
            continue
        a[rank],a[pivot]=a[pivot],a[rank]
        z=pow(a[rank][col],-1,p)
        a[rank]=[(x*z)%p for x in a[rank]]
        for i in range(n):
            if i!=rank and a[i][col]:
                f=a[i][col]
                a[i]=[(x-f*y)%p for x,y in zip(a[i],a[rank])]
        rank+=1
        if rank==n:
            break
    return rank


def kernel_checks(rng):
    fixtures=[]
    for a in range(1,5):
        for b in range(1,5):
            for _ in range(3):
                rows=[rng.randrange(1<<b) for _ in range(a)]
                rank=binary_rank(rows)
                matrix=[]
                for u in range(1<<a):
                    char=xor(rows[i] for i in bits(u))
                    matrix.append([1-2*parity(char&v) for v in range(1<<b)])
                actual=odd_field_rank(matrix)
                assert actual==1<<rank
                fixtures.append({"left":a,"right":b,"cross_rank":rank,"kernel_rank":actual})
    sampled=[]
    for n in (8,10,12,14,16):
        rows=[0]*n
        for i in range(n):
            for j in range(i):
                if rng.randrange(2):
                    rows[i]|=1<<j
                    rows[j]|=1<<i
        minimum=n
        examined=0
        witness=None
        for size in range((n+2)//3,n//2+1):
            for subset in itertools.combinations(range(n),size):
                mask=sum(1<<i for i in subset)
                other=((1<<n)-1)^mask
                rank=binary_rank([rows[i]&other for i in subset])
                if rank<minimum:
                    minimum=rank
                    witness=mask
                examined+=1
        sampled.append({"n":n,"adjacency_rows":rows,"balanced_cuts_examined":examined,
                        "minimum_cross_rank":minimum,"witness_mask":witness})
    return fixtures,sampled


def schur_checks(rng):
    results=[]
    for t in (2,4,6):
        # Explicit dense inverse I+J; inverse equals itself for even t.
        A=[((1<<t)-1)^(1<<i) for i in range(t)]
        inv=inverse(A)
        assert inv==A
        quartic=[(i,j) for j,row in enumerate(inv) for i in bits(row)]
        assert len(quartic)==t*(t-1)
        samples=list(range(1<<(4*t))) if t==2 else [rng.randrange(1<<(4*t)) for _ in range(24)]
        for x in samples:
            f=sum((((x>>i)&1)*((x>>(t+i))&1))<<i for i in range(t))
            g=sum((((x>>(2*t+i))&1)*((x>>(3*t+i))&1))<<i for i in range(t))
            zstar=sum(parity(row&f)<<j for j,row in enumerate(inv))
            expected=(1<<t)*(1-2*parity(g&zstar))
            total=0
            for y in range(1<<t):
                yA=xor(A[i] for i in bits(y))
                for z in range(1<<t):
                    exponent=parity(yA&z)^parity(y&f)^parity(z&g)
                    total+=1-2*exponent
            assert total==expected
        results.append({"t":t,"original_nonlinear_cubic_terms":2*t,
                        "induced_distinct_quartic_terms":len(quartic),
                        "x_assignments_checked":len(samples),
                        "internal_assignments_per_x":1<<(2*t)})
    return results


def direct_program(n,gates,targets,x):
    values=[x>>i&1 for i in range(n)]
    for gate in gates:
        op,args=gate
        if op=="xor":
            values.append(parity(sum(values[i]<<j for j,i in enumerate(args))))
        elif op=="not":
            values.append(1^values[args[0]])
        elif op=="and":
            values.append(values[args[0]]&values[args[1]])
        else:
            raise ValueError(op)
    return all(values[i]==b for i,b in targets)


def compile_program(n,gates,targets):
    forms=[(1<<i,0) for i in range(n)]
    nonlinear=[]
    for op,args in gates:
        if op=="xor":
            forms.append((xor(forms[j][0] for j in args),xor(forms[j][1] for j in args)))
        elif op=="not":
            mask,c=forms[args[0]]
            forms.append((mask,c^1))
        elif op=="and":
            nonlinear.append((forms[args[0]],forms[args[1]]))
            forms.append((1<<(n+len(nonlinear)-1),0))
    t=len(nonlinear)
    primal=n+3*t
    equations=[]
    for i,(a,b) in enumerate(nonlinear):
        u=n+t+2*i
        v=u+1
        equations.extend([(a[0]^(1<<u),a[1],0),
                          (b[0]^(1<<v),b[1],0),
                          (1<<(n+i),0,(1<<u)|(1<<v))])
    for index,target in targets:
        mask,c=forms[index]
        equations.append((mask,c^target,0))
    quadratic=set()
    cubic=set()
    def toggle(container,mask):
        if mask in container:
            container.remove(mask)
        else:
            container.add(mask)
    for j,(mask,c,nonlinear_mask) in enumerate(equations):
        multiplier=1<<(primal+j)
        for bit in bits(mask):
            toggle(quadratic,multiplier|(1<<bit))
        if c:
            toggle(quadratic,multiplier)
        if nonlinear_mask:
            toggle(cubic,multiplier|nonlinear_mask)
    return primal+len(equations),len(equations),quadratic,cubic


def program_checks(rng):
    results=[]
    for n in (1,2,3):
        for t in (1,2):
            for sample in range(2):
                gates=[]
                for stage in range(t):
                    for _ in range(8+4*sample):
                        available=n+len(gates)
                        if rng.randrange(5)==0:
                            gates.append(("not",[rng.randrange(available)]))
                        else:
                            gates.append(("xor",[rng.randrange(available) for _ in range(rng.randint(1,4))]))
                    available=n+len(gates)
                    gates.append(("and",[rng.randrange(available),rng.randrange(available)]))
                gates.append(("xor",[n+len(gates)-1,rng.randrange(n)]))
                targets=[(n+len(gates)-1,sample)]
                N,r,Q,P=compile_program(n,gates,targets)
                assert len(P)==t and all(mask.bit_count()<=2 for mask in Q)
                signed=sum(1-2*(sum((mask&x)==mask for mask in Q|P)&1)
                           for x in range(1<<N))
                assert signed%(1<<r)==0
                count=signed//(1<<r)
                direct=sum(direct_program(n,gates,targets,x) for x in range(1<<n))
                assert count==direct
                results.append({"inputs":n,"raw_states":len(gates),"and_gates":t,
                                "phase_variables":N,"multipliers":r,
                                "quadratic_monomials":len(Q),"cubic_monomials":len(P),
                                "signed_phase_sum":signed,"original_count":count,
                                "gates":gates,"targets":targets})
    return results


def sparse_dual_fixture(n,rows,offset,monomials,w):
    r=len(rows)
    rank=binary_rank(rows)
    cdim=r-rank
    basis={}
    short=[]
    for size in range(1,min(w,r)+1):
        for chosen in itertools.combinations(range(r),size):
            h=sum(1<<i for i in chosen)
            if xor(rows[i] for i in chosen)==0 and basis_add(basis,h):
                short.append(h)
    c0=len(short)
    long=[]
    # Exhaustive completion is only a finite checker; the theorem uses Gaussian elimination.
    for h in range(1,1<<r):
        if xor(rows[i] for i in bits(h))==0 and basis_add(basis,h):
            long.append(h)
    assert len(basis)==cdim
    def phase(y):
        return sum((mon&y)==mon for mon in monomials)&1
    numerator=0
    inner=[]
    for mu in range(1<<len(long)):
        remaining=xor(long[j] for j in bits(mu))
        z=0
        for y in range(1<<r):
            for lam in range(1<<c0):
                selected=remaining^xor(short[j] for j in bits(lam))
                exponent=phase(y)^parity(selected&(y^offset))
                z+=1-2*exponent
        inner.append(z)
        numerator+=z
    assert numerator%(1<<cdim)==0
    image_sum=numerator//(1<<cdim)
    original_sum=image_sum*(1<<(n-rank))
    true=0
    for x in range(1<<n):
        y=offset^sum(parity(row&x)<<i for i,row in enumerate(rows))
        true+=1-2*phase(y)
    assert original_sum==true
    return {"n":n,"readouts":r,"rank":rank,"codimension":cdim,
            "w":w,"short_dual_rank":c0,"remaining_characters_dimension":len(long),
            "short_rows":short,"short_rhs":[parity(h&offset) for h in short],
            "long_rows":long,"inner_signed_sums":inner,"original_signed_sum":true,
            "raw_rows":rows,"affine_offset":offset,"phase_monomials":monomials}


def sparse_dual_checks(rng):
    results=[sparse_dual_fixture(2,[3,2,3],4,[1|2,4],2)]
    for n in (3,4,5):
        for sample in range(4):
            base=[]
            while len(base)<n:
                row=rng.randrange(1,1<<n)
                if binary_rank(base+[row])>len(base):
                    base.append(row)
            rows=base+[base[0]^base[1]]
            rows.append(xor(base))
            r=len(rows)
            offset=rng.randrange(1<<r)
            monomials=sorted(set(sum(1<<i for i in rng.sample(range(r),rng.randint(1,min(3,r))))
                                 for _ in range(2*r)))
            results.append(sparse_dual_fixture(n,rows,offset,monomials,3))
    return results


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="gaussian_affine_results.json")
    args=parser.parse_args()
    rng=random.Random(202610272)
    kernel,graphs=kernel_checks(rng)
    schur=schur_checks(rng)
    programs=program_checks(rng)
    dual=sparse_dual_checks(rng)
    out={"status":"all exact assertions passed",
         "scope":"finite exact identities and compiler checks; exhaustive phase sums, no fast solver claim",
         "kernel_rank_fixtures":len(kernel),
         "balanced_graph_cut_checks":sum(x["balanced_cuts_examined"] for x in graphs),
         "schur_x_fixtures":sum(x["x_assignments_checked"] for x in schur),
         "program_compiler_fixtures":len(programs),
         "program_phase_assignments":sum(1<<x["phase_variables"] for x in programs),
         "sparse_dual_fixtures":len(dual),
         "discovered_odd_rhs_rows":sum(sum(x["short_rhs"]) for x in dual),
         "kernel_ranks":kernel,"sampled_graphs":graphs,"schur":schur,
         "programs":programs,"sparse_dual":dual}
    Path(args.output).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k not in
                     ("kernel_ranks","sampled_graphs","schur","programs","sparse_dual")},indent=2))


if __name__=="__main__":
    main()
