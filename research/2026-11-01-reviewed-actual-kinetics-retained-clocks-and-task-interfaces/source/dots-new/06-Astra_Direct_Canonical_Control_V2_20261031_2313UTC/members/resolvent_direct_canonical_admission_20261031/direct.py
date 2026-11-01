"""Direct acquired canonical stability certificate. Separate unreviewed extension.

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


def effect_coefficients(cert):
    """Only the actually needed already received action-effect core; no h field."""
    r=C.integer(cert['r'],1);m=C.integer(cert['m'],1);gamma=C.rational(cert['gamma']);eta=C.rational(cert['eta']);B=[C.matrix(x) for x in cert['Bhat']]
    if not 0<gamma<1 or eta<0 or len(B)!=m or any(A.shape!=(r,r) or A*S.ones(r,1)!=S.zeros(r,1) for A in B) or B[0]!=S.zeros(r):raise ValueError('effect domain/conservation')
    return r,m,gamma,eta,None,B,None


def direct_admission(X,d,t,eta,tol):
    cap=max(X[i,i] for i in range(X.rows))/d;error=2*t*eta*cap
    return dict(status='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION' if error<=tol else 'UNKNOWN_ALL_GOAL_DIRECT_CANONICAL_ADMISSION',weight_bound=str(cap),normalized_pointwise_regret_bound=str(error),requested_tolerance=str(tol),source_objective_accuracy_required=False)


def compile_model(cert,*,expected_certificate_sha256,expected_tolerance):
    if C.digest(cert)!=expected_certificate_sha256:raise ValueError('core binding')
    tol=C.rational(expected_tolerance)
    if tol<0:raise ValueError('tolerance')
    r,m,gamma,eta,dh,B,h=effect_coefficients(cert);t=gamma/(1-gamma)
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
    # Baseline columns force every feasible X entry into [-1,1] when d>=0.
    # Translate X=U-1, U>=0, avoiding the backend's faulty free-variable path.
    shift=S.Matrix([1]*(r*r)+[0])
    try:val,u=linprog(objective,F,b+F*shift);x=S.Matrix(u)-shift
    except Exception as ex:return dict(status='UNKNOWN_CANONICAL_BACKEND',exception=type(ex).__name__,message=str(ex),seconds=time.perf_counter()-start)
    # Optimality is NOT needed; any independently verified positive candidate works.
    if any(v>0 for v in F*x-b):return dict(status='UNKNOWN_INFEASIBLE_BACKEND_PROPOSAL')
    X=S.Matrix(r,r,list(x[:r*r]));d=x[didx];Y=X*A
    if not 0<d<=1 or X.det()==0:return dict(status='UNKNOWN_NO_POSITIVE_TRANSFORM', proposed_X=C.serial(X), proposed_gap=str(d), proposed_objective=str(val))
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
    return dict(status='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP',source_certificate_sha256=C.digest(cert),admission=direct_admission(X,d,t,eta,tol),r=r,m=m,X=C.serial(X),canonical_gap=str(d),canonical_discount=str(beta),transitions=[C.serial(P) for P in trans],lp_variables=nv,lp_constraints=F.rows,lp_output_feasibility_exactly_checked=True,lp_optimality_not_needed_or_claimed=True,max_transform_entry_bits=max(max(abs(int(v.p)).bit_length(),int(v.q).bit_length()) for v in entries),seconds=time.perf_counter()-start,new_source_calls=0,scope='Direct canonical witness; no source hhat/delta_h or former kappa/objective-margin test used. Conditional on already received effect-error event. Not predictive block dynamics; no worst-case simplex bound.')


def plan_model(cert,model,goals,*,expected_certificate_sha256,expected_model_sha256,expected_goal_sha256,expected_tolerance):
    if C.digest(model)!=expected_model_sha256 or C.digest(goals)!=expected_goal_sha256:raise ValueError('model/goal binding')
    if C.digest(cert)!=expected_certificate_sha256 or model.get('source_certificate_sha256')!=expected_certificate_sha256:raise ValueError('core binding')
    r,m,gamma,eta,dh,B,h=effect_coefficients(cert);reward=C.matrix(goals)
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
    pi=[0]*(r+1);iterations=0;seen=set();entry_bits=0;start=time.perf_counter()
    while True:
        assert tuple(pi) not in seen;seen.add(tuple(pi));iterations+=1
        PP=S.Matrix(r+1,r+1,lambda i,j:P[pi[i]][i,j]);rr=S.Matrix([rewards[pi[i]][i] for i in range(r+1)])
        v=(S.eye(r+1)-beta*PP).inv()*rr;entry_bits=max(entry_bits,max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in v));scores=[rewards[a]+beta*P[a]*v for a in range(m)]
        best=S.Matrix([max(x[i] for x in scores) for i in range(r+1)])
        if v==best:break
        for i in range(r+1):
            if best[i]>v[i]:pi[i]=max(range(m),key=lambda a:scores[a][i])
    assert v[r]==0;w=X.T*v[:r,0]
    cap=max(X[i,i] for i in range(r))/d
    assert min(w)>=0 and max(w)<=cap
    original_scores=[reward.row(a).T+t*B[a]*w for a in range(m)]
    rho=max(abs(w[j]-max(ss[j] for ss in original_scores)) for j in range(r));assert rho==0
    assert all(original_scores[pi[j]][j]==w[j] for j in range(r))
    error=2*(rho+t*eta*C.norminf(w));tol=C.rational(expected_tolerance)
    if tol<0:raise ValueError('tolerance')
    return dict(status='PASS_POLICY_REGRET' if error<=tol else 'UNKNOWN_POLICY_REGRET',policy=pi[:r],w=[str(x) for x in w],canonical_value=[str(x) for x in v],rho=str(rho),regret_bound=str(error),policy_iteration_evaluations=iterations,max_evaluated_value_entry_bits=entry_bits,seconds=time.perf_counter()-start,new_source_calls=0)


def plan_small_lp(cert,model,goals,*,expected_certificate_sha256,expected_model_sha256,expected_goal_sha256,expected_tolerance):
    """Ordinary r-variable LP with an objective acquired from X, not source h."""
    if C.digest(cert)!=expected_certificate_sha256 or C.digest(model)!=expected_model_sha256 or C.digest(goals)!=expected_goal_sha256:raise ValueError('binding')
    if model.get('source_certificate_sha256')!=expected_certificate_sha256 or model.get('status')!='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP':raise ValueError('model')
    r,m,gamma,eta,_,B,_=effect_coefficients(cert);t=gamma/(1-gamma);gg=C.matrix(goals);tol=C.rational(expected_tolerance)
    if gg.shape!=(m,r) or min(gg)<0 or max(gg)>1 or tol<0:raise ValueError('task')
    X=C.matrix(model['X']);d=C.rational(model['canonical_gap'])
    if X.shape!=(r,r) or not 0<d<=1 or X.det()==0:raise ValueError('witness')
    for a in range(m):
        Y=X*(S.eye(r)-t*B[a]).T
        for j in range(r):
            if not d<=sum(Y[:,j])<=Y[j,j]<=1 or any(Y[i,j]>0 for i in range(r) if i!=j):raise ValueError('canonical witness inequality')
    hc=(X.inv()*S.ones(r,1)).T
    assert min(hc)>0
    A=S.Matrix.vstack(*[t*Ba-S.eye(r) for Ba in B]);bb=-S.Matrix([gg[a,j] for a in range(m) for j in range(r)]);start=time.perf_counter()
    try:
        _,w=linprog(hc,A,bb);w=S.Matrix(w) # baseline guarantees w>=0
        _,lam=linprog(bb.T,S.zeros(1,A.rows),S.zeros(1,1),A_eq=A.T,b_eq=-hc.T);lam=S.Matrix(lam)
    except Exception as ex:return dict(status='UNKNOWN_LP_BACKEND',exception=type(ex).__name__,seconds=time.perf_counter()-start)
    if any(x>0 for x in A*w-bb) or min(lam)<0 or A.T*lam!=-hc.T or (hc*w)[0]!=-(bb.T*lam)[0]:return dict(status='UNKNOWN_BAD_LP_PROPOSAL')
    scores=[gg.row(a).T+t*B[a]*w for a in range(m)];pi=[max(range(m),key=lambda a:scores[a][j]) for j in range(r)];rho=max(abs(w[j]-scores[pi[j]][j]) for j in range(r));cap=max(X[i,i] for i in range(r))/d
    assert rho==0 and min(w)>=0 and max(w)<=cap
    err=2*(rho+t*eta*max(w));return dict(status='PASS_POLICY_REGRET' if err<=tol else 'UNKNOWN_POLICY_REGRET',w=[str(x) for x in w],policy=pi,rho=str(rho),regret_bound=str(err),constructed_objective=[str(x) for x in hc],primal_dual_verified=True,lp_variables=r,lp_constraints=m*r,seconds=time.perf_counter()-start,new_source_calls=0)


def verify_uniform(cert,model,*,expected_certificate_sha256,expected_model_sha256,expected_tolerance):
    """Exact caller-bound receiving of the direct all-goal witness; no source calls."""
    if C.digest(cert)!=expected_certificate_sha256 or C.digest(model)!=expected_model_sha256 or model.get('source_certificate_sha256')!=expected_certificate_sha256:raise ValueError('binding')
    r,m,gamma,eta,_,B,_=effect_coefficients(cert);tol=C.rational(expected_tolerance);t=gamma/(1-gamma)
    if tol<0 or model.get('status')!='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP' or C.integer(model['r'])!=r or C.integer(model['m'])!=m:raise ValueError('scope')
    X=C.matrix(model['X']);d=C.rational(model['canonical_gap']);beta=C.rational(model['canonical_discount']);PP=[C.matrix(x) for x in model['transitions']]
    if X.shape!=(r,r) or not 0<d<=1 or beta!=1-d or X.det()==0 or len(PP)!=m:raise ValueError('witness')
    for a in range(m):
        Y=X*(S.eye(r)-t*B[a]).T;P=PP[a]
        if P.shape!=(r+1,r+1) or min(P)<0 or P*S.ones(r+1,1)!=S.ones(r+1,1):raise ValueError('stochastic kernel')
        Q=(S.eye(r+1)-beta*P).T
        if Q[:r,:r]!=Y or Q[:r,r]!=S.zeros(r,1) or Q[r,r]!=d or any(Q[r,j]!=d-sum(Y[:,j]) for j in range(r)):raise ValueError('transform join')
        for j in range(r):
            if not d<=sum(Y[:,j])<=Y[j,j]<=1 or any(Y[i,j]>0 for i in range(r) if i!=j):raise ValueError('witness sign')
    if C.rational(model['admission']['requested_tolerance'])!=tol:raise ValueError('requested tolerance')
    expected=direct_admission(X,d,t,eta,tol)
    if C.digest(expected)!=C.digest(model['admission']):raise ValueError('claimed uniform bound')
    return expected


def receive_refinement_attempts(records,*,expected_native_features,expected_n,expected_m,expected_gamma,expected_source_id,expected_schedules,expected_confidence_total,expected_tolerance):
    """Same full observation receiver/refinement protocol, direct canonical stop.

    All supplied attempts are paid; source provenance, fixed-N freshness and
    nonanticipation are external protocol premises, not manufactured by hashes.
    """
    n=C.integer(expected_n,1);m=C.integer(expected_m,1);gamma=C.rational(expected_gamma);budget=C.rational(expected_confidence_total)
    if len(expected_native_features)!=n or not 0<budget<1 or len(records)!=len(expected_schedules) or not records:raise ValueError('attempt interface')
    groups={}
    for i,row in enumerate(expected_native_features):groups.setdefault(tuple(C.rational(x) for x in row),[]).append(i)
    parts=list(groups.values());trace=[];total_delta=S.Integer(0);episodes=0;cap_calls=0;cert=None;model=None;final_pass=False
    for j,(record,schedule) in enumerate(zip(records,expected_schedules)):
        if set(schedule)!={'N','cap','delta','root_bits'}:raise ValueError('schedule keys')
        design={'n':n,'m':m,'gamma':str(gamma),'parts':parts,'source_id':expected_source_id,**schedule}
        cert=C.receive_counts(record,expected_design=design);total_delta+=C.rational(cert['confidence_failure'])
        if total_delta>budget:raise ValueError('confidence budget exceeded')
        episodes+=cert['source_episodes'];cap_calls+=cert['source_call_cap'];model=compile_model(cert,expected_certificate_sha256=C.digest(cert),expected_tolerance=expected_tolerance)
        adm=verify_uniform(cert,model,expected_certificate_sha256=C.digest(cert),expected_model_sha256=C.digest(model),expected_tolerance=expected_tolerance) if model['status']=='PASS_EXACT_CANONICAL_COMPUTATIONAL_MDP' else model
        final_pass=adm['status']=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION';before=parts;after=parts
        if final_pass:
            if j!=len(records)-1:raise ValueError('supplied paid records after declared acquisition stop')
        else:
            P=[S.Matrix(a)/design['N'] for a in record['counts']];effects=[Pa-P[0] for Pa in P];after=C.statistical_refinement(parts,effects,C.rational(cert['epsilon']))['parts']
        trace.append({'attempt':j,'rank_before':len(before),'rank_after':len(after),'design_sha256':C.digest(design),'certificate_sha256':C.digest(cert),'compiled_model':model,'admission':adm});parts=after
    return {'status':'PASS_REUSABLE_DIRECT_CANONICAL_ACQUISITION' if final_pass else 'UNKNOWN_REUSABLE_DIRECT_CANONICAL_ACQUISITION','certificate':cert,'model':model,'next_partition_proposal':parts,'trace':trace,'total_failure_budget':str(total_delta),'total_source_episodes':episodes,'total_source_call_cap':cap_calls,'native_features_sha256':C.digest(expected_native_features),'scope':'Receives all supplied endpoint batches, failed compiles and refinements. Fresh iid fixed-N/source provenance remains external; source objective h is unused by admission.'}
