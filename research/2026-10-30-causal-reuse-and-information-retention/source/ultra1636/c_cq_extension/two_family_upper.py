"""One numerical proposal for the SAME0,+ two-family CQ upper operation.

This is NOT an exact entropy characterization or a quantum-reference
sampling experiment. Its own stronger free domain is retained explicitly.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,resource
START=time.perf_counter()
import sympy as sp
import numpy as np
import cvxpy as cp
IMPORT_SECONDS=time.perf_counter()-START
ROOT=Path(__file__).resolve().parent


def encode(M):return [[str(x) for x in row] for row in M.tolist()]


def source():
    t0=sp.diag(1,0);t1=sp.ones(2)/2;taus=[t0,t1]
    # Column vectorization on HS(out): L_tau=I tensor tau,
    # R_tau=tau^T tensor I. All actual tau entries are rational/real.
    W=[sp.kronecker_product(sp.eye(2),t) for t in taus]
    W += [sp.kronecker_product(t.T,sp.eye(2)) for t in taus]
    e,f=9,3;A0=sp.zeros(e)
    for i in range(4):A0[i,i]=sp.Rational(1,4)
    A0[4:8,4:8]=sum(W,sp.zeros(4))/4;A0[8,8]=1
    A=[A0];B0=sp.diag(sp.Rational(1,2),sp.Rational(1,2),0);B=[]
    # Independent effects E0L,E1L,E0R; E1R=I/4-sum X_j.
    labels=[0,1,0,1]
    for j in range(3):
        M=sp.zeros(e);M[j,j]=1;M[3,3]=-1;M[4:8,4:8]=W[j]-W[3];A.append(M)
        T=sp.zeros(f);T[labels[j],labels[j]]+=1;T[labels[3],labels[3]]-=1;B.append(T)
    delta=sp.Matrix([t0[i,j]-t1[i,j] for j in range(2) for i in range(2)])
    for skew in (False,True):
        M=sp.zeros(e);M[4:8,8]=delta;M[8,4:8]=(-delta.T if skew else delta.T);A.append(M)
        T=sp.zeros(f);T[0,2]=1;T[1,2]=-1
        T[2,0]=-1 if skew else 1;T[2,1]=1 if skew else -1;B.append(T)
    assert all(sp.trace(M)==0 for M in A[1:]) and sp.trace(A0)==4
    return A,[B0]+B


def main():
    tick=time.perf_counter();A,B=source();e,f=9,3;d=e*f
    C=cp.Variable((d,d),symmetric=True);c=cp.Variable()
    def phi(M):
        return sum(float(M[a,b])*C[a*f:(a+1)*f,b*f:(b+1)*f]
                   for a in range(e) for b in range(e) if M[a,b])
    eq=[]
    for j in range(1,len(A)):
        P=phi(A[j]);T=np.array(B[j],dtype=float)
        for p in range(f):
            for q in range(p+(j==5),f):eq.append(P[p,q]==T[p,q])
    R=cp.diag(cp.hstack([.5,.5,c]))-phi(A[0])
    constraints=[C>>0,R>>0,c>=0,c<=4]+eq
    prob=cp.Problem(cp.Minimize(c),constraints)
    compile_seconds=time.perf_counter()-tick;tick=time.perf_counter()
    prob.solve(solver='CLARABEL',tol_gap_abs=2e-10,tol_feas=2e-10,tol_gap_rel=2e-10,max_iter=250)
    solve_seconds=time.perf_counter()-tick
    if C.value is None:raise RuntimeError('NO_PROPOSAL '+str(prob.status))
    result={'scope':'two-unrestricted-effect-family SUFFICIENT upper; physical necessity NOT_PROVED',
        'same_prepared_pair':{'tau0':[['1','0'],['0','0']],'tau1':[['1/2','1/2'],['1/2','1/2']]},
        'source_pencil':[encode(M) for M in A],'target_constant_without_c':encode(B[0]),
        'target_nonconstant':[encode(M) for M in B[1:]],'source_order':e,'target_order':f,'Choi_order':d,
        'status':prob.status,'c_proposal':float(c.value),'C_proposal':C.value.tolist(),'R_proposal':R.value.tolist(),
        'dual_equalities':[float(q.dual_value) for q in eq],
        'dual_C':constraints[0].dual_value.tolist(),'dual_R':constraints[1].dual_value.tolist(),
        'costs':{'imports_seconds':IMPORT_SECONDS,'compile_seconds':compile_seconds,
            'solve_seconds':solve_seconds,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        'numerical_status_is_not_a_certificate':True}
    (ROOT/'TWO_FAMILY_PROPOSAL.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':prob.status,'c_proposal':float(c.value),'costs':result['costs']},indent=2))


if __name__=='__main__':main()
