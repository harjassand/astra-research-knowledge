#!/usr/bin/env python3
"""Exact finite-matrix, sound-incomplete product-weight certificate acquisition.

No experimental calibration, spectator norm oracle, or quantum gate execution.
Dependencies: SymPy exact rational linear algebra and its ordinary simplex LP.
"""
import argparse, hashlib, itertools, json, signal, threading
from pathlib import Path
import sympy as S
from sympy.solvers.simplex import lpmin, InfeasibleLPError, UnboundedLPError

FORMAT='raw-local-operator-certificate-v1'
class InputError(ValueError): pass
class SearchLimit(RuntimeError): pass

def exactkeys(x, keys):
    if type(x) is not dict or set(x)!=set(keys): raise InputError('wrong object keys')
def integer(x,lo=0):
    if type(x) is not int or x<lo: raise InputError('invalid integer')
    return x

def rat(x):
    if type(x) is not list or len(x)!=2: raise InputError('rational pair required')
    a,b=x
    if type(a) is not int or type(b) is not int or b<=0: raise InputError('invalid rational')
    y=S.Rational(a,b)
    if int(y.p)!=a or int(y.q)!=b: raise InputError('noncanonical rational')
    return y

def encq(x):
    x=S.Rational(x); return [int(x.p),int(x.q)]
def scalar(x):
    if type(x) is not list or len(x)!=2: raise InputError('complex pair required')
    return rat(x[0])+S.I*rat(x[1])
def normalized_scalar(x):
    z=S.expand_complex(x)
    re=S.cancel(S.re(z)); im=S.cancel(S.im(z))
    if re.is_Rational is not True or im.is_Rational is not True:
        raise InputError('non-rational matrix expression')
    return S.Rational(re)+S.I*S.Rational(im)
def normalized_matrix(A):return S.Matrix(A).applyfunc(normalized_scalar)
def encmat(A):
    A=normalized_matrix(A)
    return [[[encq(S.re(x)),encq(S.im(x))] for x in row] for row in A.tolist()]
def matrix(x,d):
    if type(x) is not list or len(x)!=d or any(type(r) is not list or len(r)!=d for r in x):
        raise InputError('wrong matrix shape')
    return S.Matrix([[scalar(v) for v in r] for r in x])
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(x): return hashlib.sha256(canonical(x).encode()).hexdigest()
def strict_equal(a,b):
    return type(a) is type(b) and (set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in a) if type(a) is dict else
        len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)

def load(text):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise InputError('duplicate JSON key')
            d[k]=v
        return d
    return json.loads(text,object_pairs_hook=pairs,parse_float=lambda _: (_ for _ in ()).throw(InputError('floats forbidden')),
                      parse_constant=lambda _: (_ for _ in ()).throw(InputError('nonfinite forbidden')))

def tensor(xs):
    out=S.ones(1,1)
    for x in xs: out=S.kronecker_product(out,x)
    return out

def parse(spec):
    exactkeys(spec,['format','task','cells','couplings','generator_terms','requested_gap','activation_cap','limits','search_budget'])
    if spec['format']!=FORMAT: raise InputError('wrong format')
    exactkeys(spec['task'],['id','consumer_contract_sha256'])
    if type(spec['task']['id']) is not str or not spec['task']['id']: raise InputError('task id')
    h=spec['task']['consumer_contract_sha256']
    if type(h) is not str or len(h)!=64 or any(c not in '0123456789abcdef' for c in h): raise InputError('contract hash')
    exactkeys(spec['limits'],['max_cell_dimension','max_term_support','max_local_dimension'])
    lim={k:integer(v,1) for k,v in spec['limits'].items()}
    exactkeys(spec['search_budget'],['max_lp_seconds','max_lp_constraints','max_lp_variables'])
    for v in spec['search_budget'].values(): integer(v,1)
    if spec['search_budget']['max_lp_seconds']>3600: raise InputError('LP time budget limit')
    # Explicit finite acquisition cap; refusal is not a physical no-go.
    if lim['max_cell_dimension']>8 or lim['max_term_support']>3 or lim['max_local_dimension']>64:
        raise InputError('implementation resource cap exceeded')
    if type(spec['cells']) is not list or not spec['cells']: raise InputError('nonempty cells')
    dims=[integer(d,2) for d in spec['cells']]
    if max(dims)>lim['max_cell_dimension']: raise InputError('cell dimension limit')
    gap=rat(spec['requested_gap']); cap=rat(spec['activation_cap'])
    if gap<=0 or cap<0: raise InputError('gap/cap sign')
    if type(spec['couplings']) is not list or type(spec['generator_terms']) is not list: raise InputError('term lists')
    Bs=[[] for _ in dims]; coupling_norms=[]
    seen=set()
    for c in spec['couplings']:
        exactkeys(c,['id','cell','system_pauli','source_matrix'])
        if type(c['id']) is not str or not c['id'] or c['id'] in seen: raise InputError('coupling id')
        seen.add(c['id']); i=integer(c['cell'])
        if i>=len(dims): raise InputError('coupling cell')
        p=c['system_pauli']
        if type(p) is not list or not p: raise InputError('nonidentity Pauli list')
        last=-1
        for item in p:
            if type(item) is not list or len(item)!=2: raise InputError('Pauli entry')
            q=integer(item[0]); ch=item[1]
            if q<=last or ch not in ('X','Y','Z') or type(ch) is not str: raise InputError('Pauli order/type')
            last=q
        B=matrix(c['source_matrix'],dims[i])
        if B!=B.H: raise InputError('coupling not Hermitian')
        Bs[i].append(B)
        coupling_norms.append(max(sum(abs(S.re(B[r,j]))+abs(S.im(B[r,j])) for j in range(dims[i])) for r in range(dims[i])))
    terms=[]; seen=set()
    for t in spec['generator_terms']:
        exactkeys(t,['id','support','hamiltonian','jumps'])
        if type(t['id']) is not str or not t['id'] or t['id'] in seen: raise InputError('generator id')
        seen.add(t['id']); e=t['support']
        if type(e) is not list or not e or any(type(i) is not int for i in e) or e!=sorted(set(e)) or e[0]<0 or e[-1]>=len(dims):
            raise InputError('support')
        d=S.prod(dims[i] for i in e)
        if len(e)>lim['max_term_support'] or d>lim['max_local_dimension']: raise InputError('local resource limit')
        H=matrix(t['hamiltonian'],int(d))
        if H!=H.H: raise InputError('Hamiltonian not Hermitian')
        if type(t['jumps']) is not list: raise InputError('jump list')
        js=[]
        for j in t['jumps']:
            exactkeys(j,['rate','operator']); rate=rat(j['rate'])
            if rate<0: raise InputError('negative jump rate')
            js.append((rate,matrix(j['operator'],int(d))))
        terms.append((e,H,js))
    return dims,Bs,terms,gap,cap,coupling_norms

def charges(dims,Bs):
    Ps=[]; Qs=[]
    for d,bs in zip(dims,Bs):
        stacked=S.Matrix.vstack(*bs) if bs else S.zeros(0,d)
        vs=stacked.nullspace()
        if not vs: P=S.zeros(d)
        else:
            X=S.Matrix.hstack(*vs); P=normalized_matrix(X*(X.H*X).inv()*X.H)
        Q=normalized_matrix(S.eye(d)-P)
        assert P==P.H and normalized_matrix(P*P)==P and normalized_matrix(Q*Q)==Q
        assert all(normalized_matrix(B*P)==S.zeros(d) and normalized_matrix(P*B)==S.zeros(d) for B in bs)
        Ps.append(P); Qs.append(Q)
    return Ps,Qs

def bernstein(A,us):
    """Exact conversion of degree <=2 in each variable on [0,1]^s."""
    out={k:S.zeros(A.rows) for k in itertools.product(range(3),repeat=len(us))}
    for i in range(A.rows):
        for j in range(A.cols):
            poly=S.Poly(S.expand(A[i,j]),*us)
            for power,coeff in poly.terms():
                if any(a>2 for a in power): raise AssertionError('degree exceeds 2')
                for k in out:
                    if all(a<=b for a,b in zip(power,k)):
                        f=S.prod(S.binomial(b,a)/S.binomial(2,a) for a,b in zip(power,k))
                        out[k][i,j]+=coeff*f
    return out

def local_coefficients(dims,Qs,term,M,act):
    e,H,js=term; us=S.symbols('u0:'+str(len(e)),real=True)
    Is=[S.eye(dims[i]) for i in e]; qs=[Qs[i] for i in e]
    V=tensor([I+u*Q for I,u,Q in zip(Is,us,qs)])
    G=S.I*(H*V-V*H)
    for rate,L in js:
        C=L.H*L; G+=rate*(L.H*V*L-(C*V+V*C)/2)
    F=-G
    for i in range(len(e)):
        deriv=tensor([qs[j] if j==i else Is[j]+us[j]*qs[j] for j in range(len(e))])
        F+=sum(M[i,j]*us[j] for j in range(len(e)))*deriv+act[i]*us[i]*V
    return bernstein(F,us)

def psd(A):
    """Exact Hermitian PSD check, with singular pivots handled explicitly."""
    A=normalized_matrix(A)
    if A!=A.H: return False
    while A.rows:
        if any(S.re(A[i,i])<0 for i in range(A.rows)): return False
        zero=[i for i in range(A.rows) if A[i,i]==0]
        if any(any(A[i,j]!=0 for j in range(A.rows)) for i in zero): return False
        keep=[i for i in range(A.rows) if A[i,i]!=0]
        if not keep: return True
        A=A.extract(keep,keep)
        if A.rows==1: return A[0,0]>0
        p=A[0,0]; v=A[1:,0]; A=normalized_matrix(A[1:,1:]-v*v.H/p)
    return True

def build_lp(dims,Qs,terms,gap,cap):
    constraints=[]; allocations=[]; total=S.zeros(len(dims)); a_total=[S.Integer(0) for _ in dims]
    slack_count=0; coeff_count=0
    for k,term in enumerate(terms):
        e=term[0]; m=len(e)
        M=S.Matrix(m,m,lambda i,j:S.Symbol(f'm{k}_{i}_{j}',real=True))
        a=[S.Symbol(f'a{k}_{i}',real=True) for i in range(m)]
        for i,gi in enumerate(e):
            constraints.append(a[i]>=0); a_total[gi]+=a[i]
            for j,gj in enumerate(e):
                total[gi,gj]+=M[i,j]
                if i!=j: constraints.append(M[i,j]>=0)
        coeffs=local_coefficients(dims,Qs,term,M,a); coeff_count+=len(coeffs)
        for key,A in coeffs.items():
            rows=[S.Integer(0) for _ in range(A.rows)]
            for i in range(A.rows):
                for j in range(i+1,A.rows):
                    for part in (S.re(A[i,j]).expand(complex=True),S.im(A[i,j]).expand(complex=True)):
                        if part==0: continue
                        w=S.Symbol(f'w{slack_count}',real=True); slack_count+=1
                        constraints += [w>=part,w>=-part]
                        rows[i]+=w; rows[j]+=w
            for i in range(A.rows):
                diag=S.expand_complex(A[i,i])
                if S.im(diag)!=0: raise AssertionError('nonreal diagonal')
                constraints.append(S.re(diag)>=rows[i])
        allocations.append((M,a))
    for i in range(len(dims)):
        constraints += [sum(total[i,j] for j in range(len(dims)))<=-gap,
                        sum(total[j,i] for j in range(len(dims)))<=-gap,a_total[i]<=cap]
    clean=[]
    for c in constraints:
        if c==S.false: return None
        if c!=S.true: clean.append(c)
    symbols=set().union(*(c.free_symbols for c in clean)) if clean else set()
    return sum(a_total),clean,allocations,{'bernstein_matrices':coeff_count,'lp_constraints':len(clean),'lp_variables':len(symbols),'absolute_value_slacks':slack_count}

def base_record(spec,dims,Ps,Qs,norms):
    return {'format':FORMAT,'input_sha256':digest(spec),'task':spec['task'],
            'projectors':[{'P':encmat(P),'Q':encmat(Q),'transparent_rank':int(S.trace(P))} for P,Q in zip(Ps,Qs)],
            'coupling_norm_upper':[encq(x) for x in norms],
            'scope':'finite supplied operators; drift certificate only; no hardware or circuit admission',
            'status':'UNKNOWN','allocations':[]}

def budgeted_lp(objective,constraints,seconds):
    # Ordinary exact solver, NOT a polynomial-time performance claim.
    # Never replace an existing process timer. This CLI runs on the main thread.
    if threading.current_thread() is not threading.main_thread():
        raise SearchLimit('main-thread timer required')
    if not hasattr(signal,'setitimer') or signal.getitimer(signal.ITIMER_REAL)[0]>0:
        raise SearchLimit('timer unavailable or already active')
    old=signal.getsignal(signal.SIGALRM)
    def stop(*_): raise SearchLimit('LP wall-clock budget reached')
    try:
        signal.signal(signal.SIGALRM,stop)
        signal.setitimer(signal.ITIMER_REAL,seconds)
        return lpmin(objective,constraints)
    except ValueError as exc:
        raise SearchLimit('main-thread timer unavailable') from exc
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        signal.signal(signal.SIGALRM,old)

def acquire(spec):
    dims,Bs,terms,gap,cap,norms=parse(spec); Ps,Qs=charges(dims,Bs)
    out=base_record(spec,dims,Ps,Qs,norms)
    if any(P==S.zeros(P.rows) for P in Ps):
        out['reason']='NO_COMMON_TRANSPARENT_SECTOR'; return out
    lp=build_lp(dims,Qs,terms,gap,cap)
    if lp is None:
        out['reason']='SUFFICIENT_CONE_INFEASIBLE'; return out
    objective,constraints,allocs,counts=lp; out['acquisition_counts']=counts
    budget=spec['search_budget']
    if counts['lp_constraints']>budget['max_lp_constraints'] or counts['lp_variables']>budget['max_lp_variables']:
        out['reason']='LP_SIZE_BUDGET'; return out
    try:
        _,sol=budgeted_lp(objective,constraints,budget['max_lp_seconds'])
    except SearchLimit:
        out['reason']='LP_TIME_OR_TIMER_BUDGET'; return out
    except InfeasibleLPError:
        out['reason']='SUFFICIENT_CONE_INFEASIBLE'; return out
    except UnboundedLPError:
        out['reason']='OPTIMIZER_UNBOUNDED'; return out
    except (ValueError,TypeError,ZeroDivisionError) as exc:
        out['reason']='OPTIMIZER_UNRESOLVED_'+type(exc).__name__; return out
    for M,a in allocs:
        vals={s:sol.get(s,S.Integer(0)) for s in set(M.free_symbols)|set().union(*(x.free_symbols for x in a))}
        out['allocations'].append({'M':[[encq(x) for x in row] for row in M.subs(vals).tolist()],
                                   'activation':[encq(x.subs(vals)) for x in a]})
    out['status']='CERTIFIED'; out['reason']='EXACT_LOCAL_PSD_AND_GLOBAL_MARGIN'
    if not verify_certificate(spec,out):
        out['status']='UNKNOWN';out['reason']='OPTIMIZER_PROPOSAL_FAILED_EXACT_CHECK';out['allocations']=[]
    return out

def verify_certificate(spec,record):
    """Verify a supplied successful certificate, independently of LP/search.

    Accepts valid PSD allocations beyond the finder's DD cone. It checks the
    external model and requested budgets, not experimental truth or a circuit.
    """
    try:
        dims,Bs,terms,gap,cap,norms=parse(spec); Ps,Qs=charges(dims,Bs)
        if type(record) is not dict or record.get('status')!='CERTIFIED': return False
        expected=base_record(spec,dims,Ps,Qs,norms)
        mandatory=set(expected)|{'reason'}
        if set(record) not in (mandatory,mandatory|{'acquisition_counts'}): return False
        for key in ('format','input_sha256','task','projectors','coupling_norm_upper','scope'):
            if not strict_equal(expected[key],record[key]): return False
        if record['reason']!='EXACT_LOCAL_PSD_AND_GLOBAL_MARGIN': return False
        if any(P==S.zeros(P.rows) for P in Ps): return False
        als=record['allocations']
        if type(als) is not list or len(als)!=len(terms): return False
        total=S.zeros(len(dims)); acts=[S.Integer(0) for _ in dims]
        for term,al in zip(terms,als):
            exactkeys(al,['M','activation']); e=term[0]; m=len(e)
            if type(al['M']) is not list or len(al['M'])!=m or any(type(r) is not list or len(r)!=m for r in al['M']): return False
            M=S.Matrix([[rat(x) for x in row] for row in al['M']])
            if type(al['activation']) is not list or len(al['activation'])!=m:return False
            a=[rat(x) for x in al['activation']]
            if any(x<0 for x in a) or any(M[i,j]<0 for i in range(m) for j in range(m) if i!=j): return False
            if not all(psd(A) for A in local_coefficients(dims,Qs,term,M,a).values()): return False
            for i,gi in enumerate(e):
                acts[gi]+=a[i]
                for j,gj in enumerate(e): total[gi,gj]+=M[i,j]
        if any(acts[i]>cap or sum(total[i,j] for j in range(len(dims)))>-gap or
               sum(total[j,i] for j in range(len(dims)))>-gap for i in range(len(dims))): return False
        # Search statistics are non-scientific metadata but their type/value is
        # still validated by reconstructing the exact finite LP description.
        if 'acquisition_counts' in record:
            lp=build_lp(dims,Qs,terms,gap,cap)
            if lp is None or not strict_equal(record['acquisition_counts'],lp[3]):return False
        return True
    except (InputError,ValueError,TypeError,KeyError,IndexError,AttributeError,ZeroDivisionError):return False

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--verify');p.add_argument('--output')
    args=p.parse_args()
    try:
        spec=load(Path(args.input).read_text())
        if args.verify:
            ok=verify_certificate(spec,load(Path(args.verify).read_text()));print(json.dumps({'verified':ok}));return 0 if ok else 1
        record=acquire(spec); text=json.dumps(record,sort_keys=True,indent=2)+'\n'
        if args.output:Path(args.output).write_text(text)
        else:print(text,end='')
        return 0 if record['status']=='CERTIFIED' else 1
    except (InputError,ValueError,OSError) as e:
        print(json.dumps({'status':'REJECTED','reason':str(e)}));return 2
if __name__=='__main__':raise SystemExit(main())
