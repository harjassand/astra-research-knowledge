"""Ordinary hidden-K canonical MDP comparator. Post-freeze, not yet reviewed.

Consumes the SAME received small coefficients. Exact LP output is only a proposal:
we independently check every sign, column sum, inverse and Bellman equation.
No source sampling or full microscopic operator is used by compile/plan.
"""
from pathlib import Path
import sys,time
import sympy as S
from sympy.solvers.simplex import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'resolvent_control_reuse_20261031'))
import control as C


def compile_model(cert,*,expected_certificate_sha256,expected_tolerance):
    ad=C.uniform_admission(cert,expected_certificate_sha256=expected_certificate_sha256,expected_tolerance=expected_tolerance)
    if ad['status']!='PASS_ALL_GOAL_LP_ADMISSION':return dict(status='UNKNOWN_INPUT_ADMISSION',admission=ad)
    r,m,gamma,eta,dh,B,h=C._coefficients(cert);t=gamma/(1-gamma)
    A=S.Matrix.hstack(*[(S.eye(r)-t*Ba).T for Ba in B]);nv=r*r+1;didx=nv-1
    # Morris LP(A), Section 3: maximize minimum column sum after a Z-form
    # transformation, with diagonal <=1. All X entries are free variables.
    rows=[];rhs=[]
    for a in range(m):
        for j in range(r):
            col=A[:,a*r+j]
            for i in range(r):
                row=[S.Integer(0)]*nv
                for k in range(r):row[i*r+k]=col[k]
                rows.append(row);rhs.append(int(i==j))
            row=[S.Integer(0)]*nv
            for i in range(r):
                for k in range(r):row[i*r+k]=-col[k]
            row[didx]=1;rows.append(row);rhs.append(0)
    row=[S.Integer(0)]*nv;row[didx]=-1;rows.append(row);rhs.append(0)
    row=[S.Integer(0)]*nv;row[didx]=1;rows.append(row);rhs.append(1)
    F=S.Matrix(rows);b=S.Matrix(rhs);objective=S.zeros(1,nv);objective[didx]=-1;start=time.perf_counter()
    try:val,x=linprog(objective,F,b,bounds=(None,None));x=S.Matrix(x)
    except Exception as ex:return dict(status='UNKNOWN_CANONICAL_BACKEND',exception=type(ex).__name__,message=str(ex),seconds=time.perf_counter()-start)
    # Optimality is NOT needed; any independently verified positive candidate works.
    if any(v>0 for v in F*x-b):return dict(status='UNKNOWN_INFEASIBLE_BACKEND_PROPOSAL')
    X=S.Matrix(r,r,list(x[:r*r]));d=x[didx];Y=X*A
    if not 0<d<=1 or X.det()==0:return dict(status='UNKNOWN_NO_POSITIVE_TRANSFORM')
    for a in range(m):
        for j in range(r):
            col=Y[:,a*r+j];assert d<=sum(col)<=col[j]<=1
            assert all(col[k]<=0 for k in range(r) if k!=j)
    beta=1-d;trans=[]
    for a in range(m):
        Q=S.zeros(r+1)
        for j in range(r):
            Q[:r,j]=Y[:,a*r+j];Q[r,j]=d-sum(Y[:,a*r+j])
        Q[r,r]=d
        if beta:
            P=(S.eye(r+1)-Q).T/beta
        else:
            assert Q==S.eye(r+1);P=S.eye(r+1)
        assert min(P)>=0 and P*S.ones(r+1,1)==S.ones(r+1,1);trans.append(P)
    entries=list(X)+list(Y)+[d]+[v for P in trans for v in P]
    return dict(status='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP',source_certificate_sha256=C.digest(cert),admission=ad,r=r,m=m,X=C.serial(X),canonical_gap=str(d),canonical_discount=str(beta),transitions=[C.serial(P) for P in trans],lp_variables=nv,lp_constraints=F.rows,lp_output_feasibility_exactly_checked=True,lp_optimality_not_needed_or_claimed=True,max_transform_entry_bits=max(max(abs(int(v.p)).bit_length(),int(v.q).bit_length()) for v in entries),seconds=time.perf_counter()-start,new_source_calls=0,scope='Ordinary hidden-K decision-equivalent computational MDP; NOT a block transition predictor. Same acquired confidence event. SymPy LP proposal may refuse; no polynomial worst-case runtime claim for executed simplex.')


def plan_model(cert,model,goals,*,expected_certificate_sha256,expected_model_sha256,expected_goal_sha256,expected_tolerance):
    if C.digest(model)!=expected_model_sha256 or C.digest(goals)!=expected_goal_sha256:raise ValueError('model/goal binding')
    if C.digest(cert)!=expected_certificate_sha256 or model['source_certificate_sha256']!=expected_certificate_sha256:raise ValueError('core binding')
    r,m,gamma,eta,dh,B,h=C._coefficients(cert);reward=C.matrix(goals)
    if reward.shape!=(m,r) or any(v<0 or v>1 for v in reward):raise ValueError('goal domain')
    if model['status']!='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP':return dict(status='UNKNOWN_MODEL')
    beta=C.rational(model['canonical_discount']);d=C.rational(model['canonical_gap']);X=C.matrix(model['X']);P=[C.matrix(p) for p in model['transitions']]
    assert 0<=beta<1 and beta==1-d and X.det()!=0 and len(P)==m and X.shape==(r,r)
    t=gamma/(1-gamma)
    for a in range(m):
        assert P[a].shape==(r+1,r+1) and min(P[a])>=0 and P[a]*S.ones(r+1,1)==S.ones(r+1,1)
        Q=(S.eye(r+1)-beta*P[a]).T;Y=X*(S.eye(r)-t*B[a]).T
        assert Q[:r,:r]==Y and Q[:r,r]==S.zeros(r,1) and Q[r,r]==d
        assert all(Q[r,j]==d-sum(Y[:,j]) for j in range(r))
    rewards=[S.Matrix(list(reward.row(a))+[S.Integer(0)]) for a in range(m)]
    # Ordinary exact policy iteration on the COMPILED stochastic MDP, retaining
    # ties. Actual iterations reported; no universal polynomial PI bound asserted.
    pi=[0]*(r+1);iterations=0;seen=set();start=time.perf_counter()
    while True:
        assert tuple(pi) not in seen;seen.add(tuple(pi));iterations+=1
        PP=S.Matrix(r+1,r+1,lambda i,j:P[pi[i]][i,j]);rr=S.Matrix([rewards[pi[i]][i] for i in range(r+1)])
        v=(S.eye(r+1)-beta*PP).inv()*rr;scores=[rewards[a]+beta*P[a]*v for a in range(m)]
        best=S.Matrix([max(x[i] for x in scores) for i in range(r+1)])
        if v==best:break
        for i in range(r+1):
            if best[i]>v[i]:pi[i]=max(range(m),key=lambda a:scores[a][i])
    assert v[r]==0;w=X.T*v[:r,0]
    original_scores=[reward.row(a).T+t*B[a]*w for a in range(m)]
    rho=max(abs(w[j]-max(ss[j] for ss in original_scores)) for j in range(r));assert rho==0
    assert all(original_scores[pi[j]][j]==w[j] for j in range(r))
    error=2*(rho+t*eta*C.norminf(w));tol=C.rational(expected_tolerance)
    return dict(status='PASS_POLICY_REGRET' if error<=tol else 'UNKNOWN_POLICY_REGRET',policy=pi[:r],w=[str(x) for x in w],canonical_value=[str(x) for x in v],rho=str(rho),regret_bound=str(error),policy_iteration_evaluations=iterations,seconds=time.perf_counter()-start,new_source_calls=0)
