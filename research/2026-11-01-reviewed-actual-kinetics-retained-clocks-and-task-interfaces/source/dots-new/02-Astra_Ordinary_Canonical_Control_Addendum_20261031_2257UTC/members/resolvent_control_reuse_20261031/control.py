#!/usr/bin/env python3
"""Exact scientific prototype. No source sampling is performed by this module.

receive_counts checks fixed-design endpoint statistics; authentic iid/source/
freshness provenance is external. plan consumes a previously received certificate
with an externally retained digest. Full replay costs are not erased.
"""
from fractions import Fraction
from math import isqrt
import hashlib,json,time
import sympy as S
from sympy.solvers.simplex import linprog


def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,str,Fraction,S.Rational)):raise TypeError('exact rational required')
    z=S.Rational(x)
    if not z.is_Rational:raise TypeError('exact rational required')
    return z

def integer(x,lo=0):
    if type(x) is not int or x<lo:raise TypeError('integer domain')
    return x

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def serial(M):return [[str(v) for v in M.row(i)] for i in range(M.rows)]
def matrix(x):
    if isinstance(x,S.MatrixBase):return x.applyfunc(rational)
    return S.Matrix([[rational(v) for v in row] for row in x])
def norminf(v):return max([abs(x) for x in v]+[S.Integer(0)])
def row_l1(M):return max([sum(abs(x) for x in M.row(i)) for i in range(M.rows)]+[S.Integer(0)])

def partitions(parts,n):
    integer(n,1)
    if not isinstance(parts,list) or not parts:raise TypeError('partition')
    if any(not isinstance(p,list) or not p for p in parts):raise TypeError('partition')
    flat=[integer(i) for p in parts for i in p]
    if sorted(flat)!=list(range(n)):raise ValueError('partition does not cover states exactly')
    Z=S.zeros(n,len(parts));W=S.zeros(len(parts),n);which=[None]*n
    for g,p in enumerate(parts):
        for i in p:Z[i,g]=1;W[g,i]=S.Rational(1,len(p));which[i]=g
    return Z,W,which

def ceil_log2(x):
    x=rational(x);k=0
    if x<=0:raise ValueError('log domain')
    while S.Integer(2)**k<x:k+=1
    return k

def sqrt_up(x,bits=64):
    x=rational(x);integer(bits,1)
    if x<0:raise ValueError('sqrt domain')
    D=1<<bits;q=(int(x.p)*D*D)//int(x.q);v=isqrt(q)
    if S.Rational(v*v,D*D)<x:v+=1
    return S.Rational(v,D)

def exact_effects(actions,parts,gamma):
    """Analysis/fixture routine with exact matrices, NOT statistical acquisition."""
    gamma=rational(gamma)
    if not 0<gamma<1:raise ValueError('discount')
    mats=[matrix(A) for A in actions];n=mats[0].rows
    if any(A.shape!=(n,n) or min(A)<0 or A*S.ones(n,1)!=S.ones(n,1) for A in mats):raise ValueError('stochastic matrix')
    Z,W,_=partitions(parts,n);H=(1-gamma)*(S.eye(n)-gamma*mats[0]).inv()*Z
    C=[(A-mats[0])*H for A in mats];B=[W*A for A in C]
    return {'H':H,'C':C,'B':B,'R':W*H,'h':S.ones(1,len(parts))*W*H/len(parts),'Z':Z,'W':W,'eta':max(row_l1(Ca-Z*Ba) for Ca,Ba in zip(C,B))}

def exact_refinement(actions,native_features,gamma):
    """Exact-input reference algorithm, not row-sample learning or a fast oracle."""
    n=len(native_features);groups={}
    for i,row in enumerate(native_features):groups.setdefault(tuple(rational(x) for x in row),[]).append(i)
    parts=list(groups.values());rounds=[]
    while True:
        E=exact_effects(actions,parts,gamma);new=[]
        for p in parts:
            groups={}
            for i in p:groups.setdefault(tuple(v for C in E['C'] for v in C.row(i)),[]).append(i)
            new.extend(groups.values())
        rounds.append({'rank_before':len(parts),'rank_after':len(new),'exact_dense_resolvent_solves':1,'state_dimension':n})
        if new==parts:return {'parts':parts,'rounds':rounds,'effects':E}
        parts=new

def statistical_refinement(parts,empirical_effects,epsilon):
    """Connected components; never assumes all noisy chains are tight clusters."""
    n=empirical_effects[0].rows;partitions(parts,n);eps=rational(epsilon)
    if eps<0:raise ValueError('radius')
    ans=[];comparisons=0
    for p in parts:
        parent={i:i for i in p}
        def find(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        for ii,i in enumerate(p):
            for j in p[ii+1:]:
                d=max(sum(abs(x) for x in (E.row(i)-E.row(j))) for E in empirical_effects);comparisons+=1
                if d<=4*eps:parent[find(j)]=find(i)
        groups={}
        for i in p:groups.setdefault(find(i),[]).append(i)
        ans.extend(groups.values())
    return {'parts':ans,'pair_comparisons':comparisons}

def receive_counts(record,*,expected_design):
    """Typed fixed-design receiver. It does not authenticate observation provenance."""
    if not isinstance(record,dict) or digest(record.get('design'))!=digest(expected_design):raise ValueError('external design mismatch')
    d=expected_design
    if set(d)!={'n','m','gamma','parts','N','cap','delta','root_bits','source_id'}:raise ValueError('design keys')
    n=integer(d['n'],1);m=integer(d['m'],1);N=integer(d['N'],1);cap=integer(d['cap']);bits=integer(d['root_bits'],1)
    gamma=rational(d['gamma']);delta=rational(d['delta'])
    if not 0<gamma<1 or not 0<delta<1 or not isinstance(d['source_id'],str) or not d['source_id']:raise ValueError('design domain')
    Z,W,which=partitions(d['parts'],n);r=Z.cols
    rows=record.get('counts')
    if not isinstance(rows,list) or len(rows)!=m:raise ValueError('action count')
    P=[]
    for a in rows:
        if not isinstance(a,list) or len(a)!=n:raise ValueError('state count')
        for row in a:
            if not isinstance(row,list) or len(row)!=r:raise ValueError('block count')
            if sum(integer(v) for v in row)!=N:raise ValueError('fixed sample total')
        P.append(S.Matrix(a)/N)
    log=ceil_log2(S.Integer(2)**r*n*m/delta)
    stat=sqrt_up(S.Rational(2*log,N),bits);bias=2*gamma**(cap+1);eps=stat+bias
    E=[Pa-P[0] for Pa in P];B=[W*Ea for Ea in E]
    measured=max(row_l1(Ea-Z*Ba) for Ea,Ba in zip(E,B));eta=measured+2*eps
    u=S.ones(1,r)/r;h=(1-gamma)*u+gamma*u*W*P[0]
    cert={'kind':'RECEIVED_FIXED_DESIGN_RESOLVENT_EFFECT_CERTIFICATE','design_sha256':digest(d),'record_sha256':digest(record),'n':n,'m':m,'r':r,'gamma':str(gamma),'partition_sha256':digest(d['parts']),'Bhat':[serial(Ba) for Ba in B],'hhat':serial(h)[0],'epsilon':str(eps),'statistical_radius':str(stat),'truncation_bias':str(bias),'eta_hat':str(measured),'eta':str(eta),'delta_h':str(gamma*eps),'confidence_failure':str(delta),'log_upper':log,'source_episodes':n*m*N,'source_call_cap':n*m*N*(cap+1),'expected_source_calls':str(n*m*N*(1+gamma*(1-gamma**cap)/(1-gamma))),'count_entries':n*m*r,'nominal_partition_bits':n*max(1,(r-1).bit_length()),'scope':'Uniform conditional confidence only under authentic fixed-design fresh iid endpoint protocol. No closure equality or physical provenance authenticated.'}
    return cert

def _coefficients(cert):
    r=integer(cert['r'],1);m=integer(cert['m'],1);gamma=rational(cert['gamma']);eta=rational(cert['eta']);dh=rational(cert['delta_h'])
    if not 0<gamma<1 or eta<0 or dh<0:raise ValueError('certificate domain')
    B=[matrix(A) for A in cert['Bhat']];h=S.Matrix([[rational(x) for x in cert['hhat']]])
    if len(B)!=m or any(A.shape!=(r,r) or A*S.ones(r,1)!=S.zeros(r,1) for A in B) or B[0]!=S.zeros(r):raise ValueError('effect shape/conservation')
    if h.shape!=(1,r) or min(h)<0 or sum(h)!=1:raise ValueError('objective law')
    return r,m,gamma,eta,dh,B,h

def candidate_bound(cert,goal,y,*,expected_certificate_sha256,expected_goal_sha256,expected_tolerance):
    if digest(cert)!=expected_certificate_sha256 or digest(goal)!=expected_goal_sha256:raise ValueError('certificate/task binding')
    r,m,gamma,eta,dh,B,h=_coefficients(cert);g=S.Matrix([rational(x) for x in goal]);v=S.Matrix([rational(x) for x in y]);tol=rational(expected_tolerance)
    if len(g)!=r or len(v)!=r or not all(0<=x<=1 for x in g) or tol<0:raise ValueError('goal/candidate domain')
    t=gamma/(1-gamma);w=g+v;scores=[A*w for A in B];policy=[max(range(m),key=lambda a:scores[a][j]) for j in range(r)]
    rho=max(abs(v[j]-t*scores[policy[j]][j]) for j in range(r));error=2*(rho+t*eta*norminf(w))
    return {'status':'PASS_POLICY_REGRET' if error<=tol else 'UNKNOWN_POLICY_REGRET','policy':policy,'rho':str(rho),'weight_supnorm':str(norminf(w)),'normalized_pointwise_regret_bound':str(error),'requested_tolerance':str(tol),'per_candidate_scalar_products':m*r*r,'scope':'Against optimal microscopic/history control in the stated stationary fully observed discounted model, on the received confidence event. Deployment map/sensing is separately paid.'}

def robust_plan(cert,goal,*,expected_certificate_sha256,expected_goal_sha256,expected_tolerance):
    if digest(cert)!=expected_certificate_sha256 or digest(goal)!=expected_goal_sha256:raise ValueError('certificate/task binding')
    r,m,gamma,eta,dh,B,h=_coefficients(cert);g=S.Matrix([rational(x) for x in goal]);tol=rational(expected_tolerance)
    if len(g)!=r or not all(0<=x<=1 for x in g) or tol<0:raise ValueError('goal domain')
    t=gamma/(1-gamma);q=t*eta
    if q>=1:return {'status':'UNKNOWN_ROBUST_MARGIN','q':str(q)}
    c=2*q/(1-gamma)/(1-q);Y=t+c;M=1+Y;slack=q*M
    A=[];b=[]
    for Ba in B:
        for j in range(r):
            row=[t*Ba[j,k]-int(j==k) for k in range(r)]
            A.append(row);b.append(-slack-t*(Ba*g)[j])
    for j in range(r):
        A.append([int(j==k) for k in range(r)]);b.append(Y)
        A.append([-int(j==k) for k in range(r)]);b.append(S.Integer(0))
    A=S.Matrix(A);b=S.Matrix(b);start=time.perf_counter()
    try:
        objective,y=linprog(h,A,b,bounds=(None,None));y=S.Matrix(y)
        negdual,lam=linprog(b.T,S.zeros(1,A.rows),S.zeros(1,1),A_eq=A.T,b_eq=-h.T);lam=S.Matrix(lam)
    except Exception as ex:return {'status':'UNKNOWN_LP_BACKEND','exception_type':type(ex).__name__,'message':str(ex),'seconds':time.perf_counter()-start}
    # Exact primal/dual receiving, independent of the backend's optimality claim.
    if not all(x<=0 for x in A*y-b) or min(lam)<0 or A.T*lam!=-h.T or (h*y)[0]!=-(b.T*lam)[0]:raise ArithmeticError('LP certificate failed')
    out=candidate_bound(cert,goal,list(y),expected_certificate_sha256=expected_certificate_sha256,expected_goal_sha256=expected_goal_sha256,expected_tolerance=tol)
    prior=2*r*(c+dh*Y)/(1-gamma)+2*(r+1)*slack
    entries=list(A)+list(b)+list(h)+list(y)+list(lam)
    out.update({'y':[str(x) for x in y],'dual':[str(x) for x in lam],'objective':str(objective),'robust_shift':str(c),'box_upper':str(Y),'robust_slack':str(slack),'a_priori_exact_closure_bound':str(prior),'lp_variables':r,'lp_constraints':A.rows,'exact_primal_dual_verified':True,'max_lp_entry_numerator_or_denominator_bits':max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in entries),'backend':'SymPy rational simplex; no polynomial worst-case claim for this implementation','seconds':time.perf_counter()-start})
    return out

def uniform_admission(cert,*,expected_certificate_sha256,expected_tolerance):
    """All-goal admission on the ALREADY RECEIVED conditional confidence event."""
    if digest(cert)!=expected_certificate_sha256:raise ValueError('certificate binding')
    r,m,gamma,eta,dh,B,h=_coefficients(cert);tol=rational(expected_tolerance)
    if tol<0:raise ValueError('tolerance')
    if min(h)<=0:raise ValueError('strictly positive acquired objective required')
    t=gamma/(1-gamma);q=t*eta;kappa=(1-gamma)/(1+gamma);d=kappa-q
    out={'q':str(q),'kappa':str(kappa),'d':str(d),'requested_tolerance':str(tol),'scope':'Uniform over all bounded action-dependent final-block-compatible reward tables in [0,1], conditional on the received actual-source error event; no exact closure promise.'}
    if d<=0:return dict(out,status='UNKNOWN_NO_INVERSE_MARGIN')
    margin=(1-gamma)/r-(q+dh)/d;error=2*q/d
    return dict(out,status='PASS_ALL_GOAL_LP_ADMISSION' if margin>0 and error<=tol else 'UNKNOWN_ALL_GOAL_LP_ADMISSION',objective_margin=str(margin),normalized_pointwise_regret_bound=str(error),weight_bound=str(1/d))

def margin_plan(cert,goal,*,expected_certificate_sha256,expected_goal_sha256,expected_tolerance):
    """Sharper nominal LP with acquired dual-objective positivity margin."""
    if digest(goal)!=expected_goal_sha256:raise ValueError('goal binding')
    admission=uniform_admission(cert,expected_certificate_sha256=expected_certificate_sha256,expected_tolerance=expected_tolerance)
    if admission['status']!='PASS_ALL_GOAL_LP_ADMISSION':return admission
    r,m,gamma,eta,dh,B,h=_coefficients(cert);g=S.Matrix([rational(x) for x in goal]);tol=rational(expected_tolerance)
    if len(g)!=r or not all(0<=x<=1 for x in g):raise ValueError('goal domain')
    t=gamma/(1-gamma);bound=rational(admission['weight_bound']);A=[];b=[]
    for Ba in B:
        for j in range(r):A.append([t*Ba[j,k]-int(j==k) for k in range(r)]);b.append(-t*(Ba*g)[j])
    A=S.Matrix(A);b=S.Matrix(b);start=time.perf_counter()
    try:
        objective,y=linprog(h,A,b,bounds=(None,None));y=S.Matrix(y)
        _,lam=linprog(b.T,S.zeros(1,A.rows),S.zeros(1,1),A_eq=A.T,b_eq=-h.T);lam=S.Matrix(lam)
    except Exception as ex:return {'status':'UNKNOWN_LP_BACKEND','exception_type':type(ex).__name__,'message':str(ex),'seconds':time.perf_counter()-start}
    if not all(v<=0 for v in A*y-b) or min(lam)<0 or A.T*lam!=-h.T or (h*y)[0]!=-(b.T*lam)[0]:raise ArithmeticError('LP certificate failed')
    grouped=[sum(lam[a*r+j] for a in range(m)) for j in range(r)]
    posterior=candidate_bound(cert,goal,list(y),expected_certificate_sha256=expected_certificate_sha256,expected_goal_sha256=expected_goal_sha256,expected_tolerance=tol)
    # Keep the posterior check even though the source-event theorem gives rho=0.
    if rational(posterior['rho'])!=0 or min(grouped)<=0:posterior['status']='UNKNOWN_NOMINAL_ROOT_JOIN'
    entries=list(A)+list(b)+list(h)+list(y)+list(lam)
    posterior.update({'admission':admission,'y':[str(x) for x in y],'dual':[str(x) for x in lam],'dual_group_weights':[str(x) for x in grouped],'objective':str(objective),'lp_variables':r,'lp_constraints':A.rows,'exact_primal_dual_verified':True,'max_lp_entry_numerator_or_denominator_bits':max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in entries),'seconds':time.perf_counter()-start,'backend':'SymPy rational simplex; exact primal/dual checks; no polynomial worst-case claim for this backend'})
    return posterior

def receive_refinement_attempts(records,*,expected_native_features,expected_n,expected_m,expected_gamma,expected_source_id,expected_schedules,expected_confidence_total,expected_tolerance):
    """Receive an actual paid refinement trace, not an advised useful partition.

    Full count receiving is performed for every supplied attempt. Any successful
    trace must stop at its last record, so later paid records cannot be hidden.
    Each schedule/partition is fixed before the corresponding fresh batch under
    the external protocol. All retained paths remain separate available data.
    """
    n=integer(expected_n,1);m=integer(expected_m,1);gamma=rational(expected_gamma);budget=rational(expected_confidence_total)
    if len(expected_native_features)!=n or not 0<budget<1 or len(records)!=len(expected_schedules) or not records:raise ValueError('attempt interface')
    groups={}
    for i,row in enumerate(expected_native_features):groups.setdefault(tuple(rational(x) for x in row),[]).append(i)
    parts=list(groups.values());trace=[];total_delta=S.Integer(0);episodes=0;cap_calls=0;cert=None
    for j,(record,schedule) in enumerate(zip(records,expected_schedules)):
        if set(schedule)!={'N','cap','delta','root_bits'}:raise ValueError('schedule keys')
        design={'n':n,'m':m,'gamma':str(gamma),'parts':parts,'source_id':expected_source_id,**schedule}
        cert=receive_counts(record,expected_design=design);total_delta+=rational(cert['confidence_failure'])
        if total_delta>budget:raise ValueError('confidence budget exceeded')
        episodes+=cert['source_episodes'];cap_calls+=cert['source_call_cap']
        adm=uniform_admission(cert,expected_certificate_sha256=digest(cert),expected_tolerance=expected_tolerance)
        before=parts;after=parts
        if adm['status']=='PASS_ALL_GOAL_LP_ADMISSION':
            if j!=len(records)-1:raise ValueError('supplied paid records after declared acquisition stop')
        else:
            P=[S.Matrix(a)/design['N'] for a in record['counts']];effects=[Pa-P[0] for Pa in P]
            after=statistical_refinement(parts,effects,rational(cert['epsilon']))['parts']
        trace.append({'attempt':j,'rank_before':len(before),'rank_after':len(after),'design_sha256':digest(design),'certificate_sha256':digest(cert),'admission':adm});parts=after
    return {'status':'PASS_REUSABLE_CONTROL_ACQUISITION' if trace[-1]['admission']['status']=='PASS_ALL_GOAL_LP_ADMISSION' else 'UNKNOWN_REUSABLE_CONTROL_ACQUISITION','certificate':cert,'next_partition_proposal':parts,'trace':trace,'total_failure_budget':str(total_delta),'total_source_episodes':episodes,'total_source_call_cap':cap_calls,'native_features_sha256':digest(expected_native_features),'scope':'Receives all supplied endpoint batches and acquired refinements. Fresh iid fixed-N/source provenance remains external. No exact closure assertion.'}

def margin_plan_action_rewards(cert,action_goals,*,expected_certificate_sha256,expected_goal_sha256,expected_tolerance):
    """Primary LP for all bounded action-dependent acquired-block reward tables."""
    if digest(action_goals)!=expected_goal_sha256:raise ValueError('goal binding')
    admission=uniform_admission(cert,expected_certificate_sha256=expected_certificate_sha256,expected_tolerance=expected_tolerance)
    if admission['status']!='PASS_ALL_GOAL_LP_ADMISSION':return admission
    r,m,gamma,eta,dh,B,h=_coefficients(cert);goals=matrix(action_goals);tol=rational(expected_tolerance)
    if goals.shape!=(m,r) or not all(0<=x<=1 for x in goals):raise ValueError('action reward table')
    t=gamma/(1-gamma);A=S.Matrix([[t*B[a][j,k]-int(j==k) for k in range(r)] for a in range(m) for j in range(r)]);b=S.Matrix([-goals[a,j] for a in range(m) for j in range(r)])
    start=time.perf_counter()
    try:
        objective,w=linprog(h,A,b,bounds=(None,None));w=S.Matrix(w)
        _,lam=linprog(b.T,S.zeros(1,A.rows),S.zeros(1,1),A_eq=A.T,b_eq=-h.T);lam=S.Matrix(lam)
    except Exception as ex:return {'status':'UNKNOWN_LP_BACKEND','exception_type':type(ex).__name__,'message':str(ex),'seconds':time.perf_counter()-start}
    if not all(v<=0 for v in A*w-b) or min(lam)<0 or A.T*lam!=-h.T or (h*w)[0]!=-(b.T*lam)[0]:raise ArithmeticError('LP certificate failed')
    grouped=[sum(lam[a*r+j] for a in range(m)) for j in range(r)]
    scores=[goals.row(a).T+t*B[a]*w for a in range(m)];policy=[max(range(m),key=lambda a:scores[a][j]) for j in range(r)]
    rho=max(abs(w[j]-scores[policy[j]][j]) for j in range(r));error=2*(rho+t*eta*norminf(w))
    status='PASS_POLICY_REGRET' if error<=tol else 'UNKNOWN_POLICY_REGRET'
    if rho!=0 or min(grouped)<=0:status='UNKNOWN_NOMINAL_ROOT_JOIN'
    entries=list(A)+list(b)+list(h)+list(w)+list(lam)
    return {'status':status,'admission':admission,'policy':policy,'w':[str(x) for x in w],'rho':str(rho),'weight_supnorm':str(norminf(w)),'normalized_pointwise_regret_bound':str(error),'requested_tolerance':str(tol),'objective':str(objective),'dual':[str(x) for x in lam],'dual_group_weights':[str(x) for x in grouped],'exact_primal_dual_verified':True,'lp_variables':r,'lp_constraints':m*r,'max_lp_entry_numerator_or_denominator_bits':max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in entries),'seconds':time.perf_counter()-start,'scope':'Action-dependent rewards in [0,1], constant within final acquired blocks, same source/gamma/action set and received confidence event. No arbitrary microscopic reward extension.'}
