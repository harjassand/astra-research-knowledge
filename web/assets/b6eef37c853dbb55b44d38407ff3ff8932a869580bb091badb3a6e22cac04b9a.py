#!/usr/bin/env python3
"""Gap-free, finite-bit rational PSD-root columns for the spin compiler.

Uses guarded symmetric Newton iteration, then independently checks PSD and
an exact rational squared-residual bound. No eigenvector/eigenvalue oracle.
"""
import argparse
from fractions import Fraction as F
import importlib.util
import itertools
import json
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('arithmetic',HERE/'certified_two_spin.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
fa,fs,fm,fd=base.fa,base.fs,base.fm,base.fd


def eye(x): return [[F(x if i==j else 0) for j in range(3)] for i in range(3)]
def add(A,B): return [[fa(a,b) for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def sub(A,B): return [[fs(a,b) for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def scale(A,c): return [[fm(a,c) for a in row] for row in A]
def mm(A,B):
    return [[sum((fm(A[i][t],B[t][j]) for t in range(3)),F(0))
             for j in range(3)] for i in range(3)]
def det(A):
    n=len(A)
    if n==1: return A[0][0]
    total=F(0)
    for p in itertools.permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=F((-1)**inversions)
        for i in range(n): term=fm(term,A[i][p[i]])
        total=fa(total,term)
    return total
def principal_minors(A):
    out=[]
    for size in range(1,4):
        for indices in itertools.combinations(range(3),size):
            block=[[A[i][j] for j in indices] for i in indices]
            out.append({'indices':indices,'determinant':det(block)})
    return out
def psd(A):
    assert all(A[i][j]==A[j][i] for i in range(3) for j in range(3))
    mins=principal_minors(A)
    return all(m['determinant']>=0 for m in mins),mins
def inverse(A):
    determinant=det(A)
    if determinant==0: raise ArithmeticError('Rational Newton iterate singular')
    adj=[]
    for i in range(3):
        row=[]
        for j in range(3):
            block=[[A[r][c] for c in range(3) if c!=i] for r in range(3) if r!=j]
            row.append(fd(F((-1)**(i+j))*det(block),determinant))
        adj.append(row)
    base.ledger.add('three_by_three_rational_inverses')
    return adj
def rownorm(A): return max(sum(map(abs,row),F(0)) for row in A)
def nearest_dyadic(x,P):
    z=fm(x,F(1<<P))
    # floor(z+1/2), exact and valid for signed values as well.
    rounded=fa(z,F(1,2))
    n=rounded.numerator//rounded.denominator
    base.ledger.add('nearest_dyadic_entry_roundings')
    return F(n,1<<P)


def root(C,ell):
    assert 2<=ell<=32
    good,minors=psd(C)
    if not good:
        return {'status':'REFUTED_PSD_INPUT','principal_minors':
                [{'indices':m['indices'],'determinant':str(m['determinant'])} for m in minors]}
    rho=rownorm(C)
    assert rho<=2 # explicit configured bounded domain, not a hidden scale assumption
    q=F(1,1<<ell)
    alpha=q*q/64
    D=add(C,eye(alpha))
    gamma=F(1)
    while gamma*gamma<rho+alpha: gamma*=2
    w=q*q/(64*(gamma+1))
    k=0
    while gamma/F(1<<k)>w: k+=1
    lipschitz=1+4*(rho+alpha)/alpha
    # Approximate iterates stay in the sqrt(alpha)/4 neighborhood of exact ones.
    # A nearest-entry rounding has operator error <=3/(2*2^P).
    rounding_budget=min(w,q/8)/(16*k*lipschitz**k)
    P=1
    while F(3,2*(1<<P))>rounding_budget: P+=1
    X=eye(gamma)
    history=[]
    for step in range(k):
        inv=inverse(X)
        exact=add(scale(X,F(1,2)),scale(add(mm(D,inv),mm(inv,D)),F(1,4)))
        # Symmetric exact map, symmetric rounding by using only the upper triangle.
        for i in range(3):
            for j in range(i,3):
                value=nearest_dyadic(exact[i][j],P)
                X[i][j]=X[j][i]=value
        good_x,xmins=psd(X)
        if not good_x: raise ArithmeticError('Guard invariant failed: non-PSD iterate')
        # This inverse bound is verified with rational PSD tests, rather than assumed.
        lower=q/16
        good_lower,_=psd(sub(X,eye(lower)))
        if not good_lower: raise ArithmeticError('Guard invariant failed: known inverse floor')
        residual=sub(mm(X,X),C)
        history.append({'step':step+1,'residual_row_norm':str(rownorm(residual))})
    residual=sub(mm(X,X),C)
    delta=rownorm(residual)
    # For Hermitian residual, operator norm <= maximum absolute row sum.
    # X>=0 plus ||X^2-C||<=q^2 implies ||X-sqrt(C)||<=q, gap-free.
    good_final,xmins=psd(X)
    assert good_final and delta<=q*q
    commutator=sub(mm(X,C),mm(C,X))
    return {'status':'CERTIFIED_GAP_FREE_PSD_ROOT_COLUMNS','input_C':[[str(x) for x in row] for row in C],
            'target_root_operator_error':str(q),'regularization':str(alpha),
            'initial_scalar':str(gamma),'newton_steps':k,'working_dyadic_bits':P,
            'per_matrix_update_operator_rounding_budget':str(rounding_budget),
            'conservative_step_lipschitz':str(lipschitz),
            'certified_root_matrix':[[str(x) for x in row] for row in X],
            'root_columns':[[str(X[i][j]) for i in range(3)] for j in range(3)],
            'root_entry_enclosures':[[{'lo':str(X[i][j]-q),'hi':str(X[i][j]+q)}
                                       for j in range(3)] for i in range(3)],
            'squared_residual_matrix':[[str(x) for x in row] for row in residual],
            'squared_residual_operator_upper':str(delta),
            'commutator_operator_upper':str(rownorm(commutator)),
            'input_principal_minors':[{'indices':m['indices'],'determinant':str(m['determinant'])} for m in minors],
            'output_principal_minors':[{'indices':m['indices'],'determinant':str(m['determinant'])} for m in xmins],
            'iteration_residuals':history,
            'limits':['Configured rational symmetric 3x3 PSD input with row norm <=2',
                      'Component, not a complete normal/filter/importance sampler',
                      'No eigenaxis gap, numerical eigenvalue or exact-real oracle']}


FIXTURES={
 'rank2':[[F(1,4),F(1,4),F(0)],
          [F(1,4),F(13,36),F(1,9)],
          [F(0),F(1,9),F(1,9)]],
 'rank1':[[F(1,9)]*3 for _ in range(3)],
 'zero':eye(0),
 'tiny':[[F(1,4),F(1,4),F(0)],
         [F(1,4),F(1,4)+F(1,1<<80),F(0)],
         [F(0),F(0),F(1,1<<100)]],
 'negative':[[F(1),F(0),F(0)],[F(0),F(-1,1<<80),F(0)],[F(0),F(0),F(0)]]}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--fixture',choices=FIXTURES,default='rank2')
    ap.add_argument('--error-bits',type=int,default=12)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    base.ledger=base.Ledger()
    start,cpu=time.perf_counter(),time.process_time()
    data=root(FIXTURES[args.fixture],args.error_bits)
    data.update({'worker_id':'c07_s03','fixture':args.fixture,
        'costs':{**base.ledger.snapshot(),'wall_seconds':time.perf_counter()-start,
                 'cpu_seconds':time.process_time()-cpu,
                 'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}})
    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'output':str(out),'status':data['status'],
        'working_bits':data.get('working_dyadic_bits'),'steps':data.get('newton_steps'),
        'squared_residual_upper':data.get('squared_residual_operator_upper'),
        'wall_seconds':data['costs']['wall_seconds']}))


if __name__=='__main__': main()
