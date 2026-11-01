"""No-gap capped action-response frontend. Scientific typed API, not provenance authentication.

Every simulated intermediate label is retained. All claimed iid/independent source
and nonanticipating-bank premises are external. Exact probability matrices are not
read by Bank or receive. See PROOF.md for confidence and prior scope.
"""
from pathlib import Path
from copy import deepcopy
import sys,json,time
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'resolvent_control_reuse_20261031'))
import control as C
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'resolvent_direct_canonical_admission_20261031'))
import direct as D


def design(*,source_id,n,m,gamma,parts,i,j,delta_total,root_bits=48):
    n=C.integer(n,1);m=C.integer(m,2);i=C.integer(i,1);j=C.integer(j);bits=C.integer(root_bits,1)
    if not isinstance(source_id,str) or not source_id:raise ValueError('source id')
    gamma=C.rational(gamma);delta=C.rational(delta_total)
    if not 0<gamma<1 or not 0<delta<1:raise ValueError('discount/confidence')
    C.partitions(parts,n)
    return dict(source_id=source_id,n=n,m=m,gamma=str(gamma),parts=deepcopy(parts),i=i,j=j,N=2**i,K=2**j-1,delta_total=str(delta),delta=str(delta/S.Integer(2)**(i+j+1)),root_bits=bits)


def validate_design(d):
    expected=design(**{k:d[k] for k in ('source_id','n','m','gamma','parts','i','j','delta_total','root_bits')})
    # Strict integer validation before equality (bool == int is not a binding).
    C.integer(d['N'],2);C.integer(d['K']);C.rational(d['delta'])
    if C.digest(d)!=C.digest(expected):raise ValueError('noncanonical or changed grid design')
    return expected


class Bank:
    """Ordinary source.step(i,a) interface. Source internals never inspected.

    Actual random implementation must make independent draws. A seeded fixture is
    a reproducibility device, not a proof of authentic iid physical observations.
    """
    def __init__(self,source,*,source_id,n,m):
        self.source=source;self.source_id=source_id;self.n=C.integer(n,1);self.m=C.integer(m,2)
        self.rows={(i,a):[] for i in range(n) for a in range(1,m)}
        self.calls=0;self.attempts=[]
    def _step(self,i,a):
        y=self.source.step(i,a);C.integer(y)
        if y>=self.n:raise ValueError('source label')
        self.calls+=1;return y
    def ensure(self,N,K):
        C.integer(N,2);C.integer(K)
        before=self.calls;start=time.perf_counter()
        for (i,a),trials in self.rows.items():
            while len(trials)<N:trials.append(dict(x=[self._step(i,a)],y=[self._step(i,0)]))
            for tr in trials[:N]:
                while len(tr['x'])<=K and tr['x'][-1]!=tr['y'][-1]:
                    tr['x'].append(self._step(tr['x'][-1],0));tr['y'].append(self._step(tr['y'][-1],0))
        self.attempts.append(dict(N=N,K=K,new_source_calls=self.calls-before,cumulative_source_calls=self.calls,seconds=time.perf_counter()-start))
    def record(self,d):
        d=validate_design(d)
        if (d['source_id'],d['n'],d['m'])!=(self.source_id,self.n,self.m):raise ValueError('bank/source binding')
        rows=[dict(state=i,action=a,trials=deepcopy(trials)) for (i,a),trials in self.rows.items()]
        return dict(kind='retained_paired_path_bank_v1',design=d,rows=rows,source_calls=self.calls,attempts=deepcopy(self.attempts))


def tail_upper(k,N,F,delta,bits):
    C.integer(k);C.integer(N,2);C.integer(F,1);delta=C.rational(delta);C.integer(bits,1)
    if k>N or not 0<delta<1:raise ValueError('tail domain')
    ell=C.ceil_log2(S.Rational(2*F)/delta);b=S.Rational(ell,N);h=S.Rational(k,N)
    p=min(S.Integer(1),b if k==0 else h+b+C.sqrt_up(2*h*b+b*b,bits))
    return p,ell


def radii(samples,k,gamma,K,F,delta,bits):
    N=len(samples);C.integer(N,2);r=len(samples[0]);gamma=C.rational(gamma);delta=C.rational(delta)
    if r<1 or any(len(x)!=r or sum(x)!=0 for x in samples):raise ValueError('prefix conservation')
    L=gamma*(1-gamma**K)/(1-gamma);dh=delta/3
    if any(abs(v)>L for x in samples for v in x):raise ValueError('prefix range')
    means=[sum(x[j] for x in samples)/N for j in range(r)]
    variances=[sum((x[j]-means[j])**2 for x in samples)/(N-1) for j in range(r)]
    lh=C.ceil_log2(S.Integer(2)**(r+1)*F/dh);le=C.ceil_log2(S.Integer(4)*F*r/dh)
    eh=C.sqrt_up(8*L*L*lh/N,bits)
    ee=sum(C.sqrt_up(2*v*le/N,bits)+14*L*le/(3*(N-1)) for v in variances)
    pu,lt=tail_upper(k,N,F,dh,bits);tail=2*gamma**(K+1)*pu/(1-gamma)
    return means,dict(hoeffding=str(eh),empirical_bernstein=str(ee),prefix=str(min(eh,ee)),tail=str(tail),total=str(min(eh,ee)+tail),nonmeetings=k,p_upper=str(pu),sample_variance=[str(v) for v in variances],log_upper_bounds=[lh,le,lt],range_halfwidth=str(L))


def receive(record,*,expected_design):
    """Replay labels/counts and externally bind full task/statistical design.

    Does not authenticate source origin, independence, correct action execution or
    predeclaration. Larger retained paths are accepted for an earlier grid prefix.
    """
    d=validate_design(expected_design)
    if record.get('kind')!='retained_paired_path_bank_v1' or C.digest(record['design'])!=C.digest(d):raise ValueError('design binding')
    n,m,N,K=d['n'],d['m'],d['N'],d['K'];gamma=C.rational(d['gamma']);delta=C.rational(d['delta']);bits=d['root_bits']
    Z,W,which=C.partitions(d['parts'],n);r=Z.cols;F=n*(m-1)
    if len(record['rows'])!=F:raise ValueError('all row/action pairs required')
    rows={};calls=labels=trials_total=0
    for row in record['rows']:
        i=C.integer(row['state']);a=C.integer(row['action'],1);key=(i,a)
        if i>=n or a>=m or key in rows or not isinstance(row['trials'],list) or len(row['trials'])<N:raise ValueError('row coverage')
        rows[key]=row['trials']
        for tr in row['trials']:
            x,y=tr['x'],tr['y']
            if not isinstance(x,list) or not isinstance(y,list) or not x or len(x)!=len(y):raise ValueError('path pair')
            for u in x+y:
                C.integer(u)
                if u>=n:raise ValueError('path label')
            if any(xx==yy for xx,yy in zip(x[:-1],y[:-1])):raise ValueError('continued after microscopic meeting')
            calls+=2*len(x);labels+=len(x)+len(y);trials_total+=1
    C.integer(record['source_calls'])
    if record['source_calls']!=calls:raise ValueError('call ledger')
    # Cost records are replayable ledger metadata, not evidence of the protocol.
    cumulative=0
    for at in record['attempts']:
        C.integer(at['N'],2);C.integer(at['K']);C.integer(at['new_source_calls']);C.integer(at['cumulative_source_calls'])
        cumulative+=at['new_source_calls']
        if cumulative!=at['cumulative_source_calls']:raise ValueError('attempt ledger')
    if cumulative!=calls:raise ValueError('attempt totals')
    U=[S.zeros(n,r) for _ in range(m)];bounds=[];prefix_terms=0
    for i in range(n):
        for a in range(1,m):
            samples=[];k=0
            for tr in rows[i,a][:N]:
                x,y=tr['x'],tr['y'];met=x[-1]==y[-1]
                if len(x)<=K and not met:raise ValueError('path censored before requested cap')
                tau=len(x)-1 if met else None
                if tau is None or tau>K:k+=1
                v=[S.Integer(0)]*r
                for s in range(min(K,len(x)-1 if met else len(x))):
                    power=gamma**(s+1);v[which[x[s]]]+=power;v[which[y[s]]]-=power;prefix_terms+=1
                samples.append(v)
            mean,bb=radii(samples,k,gamma,K,F,delta,bits);U[a][i,:]=S.Matrix([mean]);bounds.append(dict(state=i,action=a,**bb))
    BU=[W*A for A in U];measured=max(C.row_l1(A-Z*B) for A,B in zip(U,BU));error=max(C.rational(x['total']) for x in bounds);etaU=measured+error;t=gamma/(1-gamma)
    core=dict(kind='received_scaled_action_response_core_v1',r=r,m=m,gamma=str(gamma),eta=str(etaU/t),Bhat=[C.serial(B/t) for B in BU],partition_sha256=C.digest(d['parts']),source_id=d['source_id'],design_sha256=C.digest(d),bank_sha256=C.digest(record),scope='Conditional on authentic independent nonanticipating paired-path bank and source/partition binding; no hhat needed.')
    return dict(status='PASS_RESPONSE_CONFIDENCE_ARITHMETIC',core=core,empirical_scaled_rows=[C.serial(A) for A in U],eta_U=str(etaU),measured_discrepancy=str(measured),row_radii=bounds,retained_source_calls=calls,selected_trials=F*N,retained_trials=trials_total,retained_microscopic_labels=labels,named_row_preparation_requests=calls,minimum_initial_pair_preparations=2*trials_total,prefix_terms_replayed=prefix_terms,partition_lookup_entries=n,statistical_failure_budget=str(delta),scope='Response radius only, not small-regret admission; provenance and predeclaration remain external.')


def initial_partition(native_features):
    """Task feature equality, not a promised useful operator basis."""
    if not isinstance(native_features,list) or not native_features:raise ValueError('native task features')
    groups={};width=len(native_features[0])
    if width<1:raise ValueError('feature width')
    for i,row in enumerate(native_features):
        if len(row)!=width:raise ValueError('feature width')
        groups.setdefault(tuple(C.rational(v) for v in row),[]).append(i)
    return list(groups.values())


def refine_received(record,*,expected_design):
    """Scaled counterpart of the accepted response refinement.

    A NEW partition must use a fresh independent prefix bank. This function makes
    no claim that a failed finite-precision split proves absence of structure.
    """
    rec=receive(record,expected_design=expected_design)
    e=max(C.rational(x['total']) for x in rec['row_radii'])
    answer=C.statistical_refinement(expected_design['parts'],[C.matrix(A) for A in rec['empirical_scaled_rows']],e)
    return dict(**answer,uniform_row_error=str(e),retained_source_calls=rec['retained_source_calls'],requires_fresh_prefix_validation_for_changed_partition=True)


def retained_search(source,*,source_id,n,m,gamma,parts,delta_total,D_max,tolerance,root_bits=48):
    """Finite specified planner. Pays all failed sample/LP attempts, no teacher."""
    C.integer(D_max,1);tol=C.rational(tolerance)
    if tol<0:raise ValueError('tolerance')
    bank=Bank(source,source_id=source_id,n=n,m=m);attempts=[]
    for diagonal in range(1,D_max+1):
        for i in range(1,diagonal+1):
            j=diagonal-i;d=design(source_id=source_id,n=n,m=m,gamma=gamma,parts=parts,i=i,j=j,delta_total=delta_total,root_bits=root_bits)
            bank.ensure(d['N'],d['K']);record=bank.record(d);start=time.perf_counter();rec=receive(record,expected_design=d)
            core=rec['core'];model=D.compile_model(core,expected_certificate_sha256=C.digest(core),expected_tolerance=tol)
            attempts.append(dict(design=d,eta_U=rec['eta_U'],source_calls=bank.calls,model=model,receiving_and_compilation_seconds=time.perf_counter()-start))
            if model.get('admission',{}).get('status')=='PASS_ALL_GOAL_DIRECT_CANONICAL_ADMISSION':
                return dict(status='PASS_SEARCH',attempts=attempts,record=record,received=rec,model=model,source_calls=bank.calls)
    return dict(status='UNKNOWN_SEARCH_BUDGET',attempts=attempts,record=record,received=rec,model=model,source_calls=bank.calls)
