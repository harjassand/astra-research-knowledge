"""Exact rational dual upper bound for TWO parallel flat-source queries.

Numerics propose twelve invariant coefficients. Rational rounding plus an exact
positive shift is accepted only after all six representation-block LDL proofs
and the two input-normalization inequalities pass in exact arithmetic.
This is not a quantum/source/Haar run or an asymptotic query lower bound.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import time
import numpy as np
import sympy as sp
import cvxpy as cp
from covariant_inverse import perms,compose,invert,cycles


def reps3():
    pp=perms(3);out=[]
    out.append(('trivial', [sp.ones(1) for _ in pp],sp.ones(1)))
    matrices=[]
    for p in pp:
        cols=[]
        for j in range(2):
            v=[0,0,0];v[p[j]]+=1;v[p[2]]-=1;cols.append(sp.Matrix(v[:2]))
        matrices.append(sp.Matrix.hstack(*cols))
    out.append(('standard',matrices,sp.Matrix([[2,1],[1,2]])))
    out.append(('sign',[sp.Matrix([[(-1)**(3-cycles(p))]]) for p in pp],sp.ones(1)))
    for _,matrices,g in out:
        for p,m in zip(pp,matrices):assert m.T*g*m==g
        for i,p in enumerate(pp):
            for j,q in enumerate(pp):assert matrices[pp.index(compose(p,q))]==matrices[i]*matrices[j]
    return out


def ldl_positive(a):
    assert a==a.T
    n=a.rows;L=sp.eye(n);d=[]
    for j in range(n):
        pivot=a[j,j]-sum(L[j,h]**2*d[h] for h in range(j))
        if pivot<=0:return None
        d.append(pivot)
        for i in range(j+1,n):
            L[i,j]=(a[i,j]-sum(L[i,h]*L[j,h]*d[h] for h in range(j)))/pivot
    assert L*sp.diag(*d)*L.T==a
    return d


def main():
    start=time.perf_counter();k=2;r=2;D=4;pp=perms(3);aa=perms(2)
    gram=sp.Matrix([[D**cycles(compose(invert(p),q)) for q in pp] for p in pp]);gi=gram.inv()
    omega={(i,j):gi[j,i]*sp.Rational(r)**(cycles(p)-3)/k**2 for i,p in enumerate(pp) for j in range(len(pp))}
    representations=reps3();designs=[]
    for nameA,ra,ga in representations:
        if nameA=='sign':continue # third exterior power of the two-dimensional logical space is zero
        for nameB,rb,gb in representations:
            metric=sp.kronecker_product(ga,gb);d=metric.rows
            const=sp.zeros(d)
            for i in range(6):
                for j in range(6):const+=omega[i,j]*(metric*sp.kronecker_product(ra[i],rb[j]))
            columns=[]
            for a in aa:
                embedded=(0,a[0]+1,a[1]+1);i=pp.index(embedded)
                for j in range(6):columns.append(metric*sp.kronecker_product(ra[i],rb[j]))
            assert const==const.T
            designs.append((nameA,nameB,const,columns))
    y=cp.Variable((2,6));lam=cp.Variable();yv=cp.reshape(y,(12,),order='C');constraints=[]
    iv=[pp.index(invert(p)) for p in pp];constraints.append(y==y[:,iv])
    for _,_,const,cols in designs:
        design=np.column_stack([np.array(v,dtype=float).reshape(-1) for v in cols]);d=const.rows
        block=cp.reshape(design@yv,(d,d),order='C')-np.array(const,dtype=float)
        constraints.append((block+block.T)/2>>0)
    for sign in (1,-1):constraints.append(lam>=sum(D**cycles(p)*(y[0,i]+sign*y[1,i]) for i,p in enumerate(pp)))
    prob=cp.Problem(cp.Minimize(lam),constraints)
    proposal=prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10,max_iter=300)
    B=40;den=1<<B
    rounded=[[F(round(float(y.value[i,j])*den),den) for j in range(6)] for i in range(2)]
    for i in range(2):
        for j in range(6):
            other=iv[j]
            if j<=other:
                common=(rounded[i][j]+rounded[i][other])/2
                rounded[i][j]=rounded[i][other]=common
    records=None
    for exponent in range(45,-1,-1):
        shift=F(1,1<<exponent);candidate=[row[:] for row in rounded]
        candidate[0][pp.index(tuple(range(3)))]+=shift
        records=[]
        for nameA,nameB,const,cols in designs:
            z=-const
            for value,col in zip(sum(candidate,[]),cols):z+=sp.Rational(value.numerator,value.denominator)*col
            assert z==z.T
            diagonal=ldl_positive(z)
            if diagonal is None:records=None;break
            records.append({'logical_irrep':nameA,'physical_irrep':nameB,
                            'metric_dual_block':[[str(v) for v in row] for row in z.tolist()],
                            'exact_LDL_positive_pivots':list(map(str,diagonal))})
        if records is not None:break
    assert records is not None
    normalization=[sum(F(D**cycles(p))*(candidate[0][i]+s*candidate[1][i]) for i,p in enumerate(pp)) for s in (1,-1)]
    upper=max(normalization)
    strict_target=F(55716029295809,123760695281664)
    assert upper<F(11,25) and strict_target>upper
    result={'status':'EXACT_RATIONAL_PARALLEL_DUAL_CERTIFICATE',
            'scope':'all deterministic two-parallel-query strategies including entangled source inputs; full-rank flat k2 r2 D4 family',
            'k':k,'r':r,'D':D,'source_queries_in_strategy':2,
            'numerical_proposal':float(proposal),'numerical_solver_status':prob.status,
            'rounding_bits':B,'exact_identity_shift':str(shift),
            'parallel_Bell_fidelity_upper':str(upper),'parallel_Bell_fidelity_upper_decimal':float(upper),
            'dual_coefficients':[[str(v) for v in row] for row in candidate],
            'input_symmetry_sector_values':list(map(str,normalization)),
            'positive_blocks':records,
            'candidate_adaptive_lower_requires_its_separate_exact_CPTP_proof':str(strict_target),
            'comparison_gap_if_that_proof_holds':str(strict_target-upper),
            'source_quantum_Haar_executions':0,'seconds':time.perf_counter()-start}
    path=Path(__file__).with_name('PARALLEL_DUAL_CERTIFICATE.json');path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','parallel_Bell_fidelity_upper','parallel_Bell_fidelity_upper_decimal','exact_identity_shift','numerical_proposal','seconds']},indent=2))


if __name__=='__main__':main()
