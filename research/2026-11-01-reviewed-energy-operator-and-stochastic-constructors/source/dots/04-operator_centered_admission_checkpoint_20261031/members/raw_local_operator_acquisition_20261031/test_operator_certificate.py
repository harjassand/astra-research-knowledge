import copy, json, time, signal, subprocess, tempfile, random
from unittest.mock import patch
from pathlib import Path
import sympy as S
import acquire_operator_certificate as a

def q(x):return a.encq(x)
def mat(x):return a.encmat(S.Matrix(x))
def term(id,e,H,jumps=()):
    return {'id':id,'support':e,'hamiltonian':mat(H),'jumps':[{'rate':q(r),'operator':mat(L)} for r,L in jumps]}
def coupling(id,i,B):return {'id':id,'cell':i,'system_pauli':[[i,'Z']],'source_matrix':mat(B)}
def base(dims):
    return {'format':a.FORMAT,'task':{'id':'known raw finite operator fixture','consumer_contract_sha256':'a'*64},
            'cells':dims,'couplings':[],'generator_terms':[],'requested_gap':q(1),'activation_cap':q(S.Rational(1,10)),
            'limits':{'max_cell_dimension':4,'max_term_support':2,'max_local_dimension':16},
            'search_budget':{'max_lp_seconds':10,'max_lp_constraints':10000,'max_lp_variables':10000}}
def qutrit(omega=10**20):
    s=base([3]);Q=S.diag(0,0,1);H=S.Matrix([[0,omega,0],[omega,0,0],[0,0,0]])
    L0=S.zeros(3);L0[0,2]=1;L1=S.zeros(3);L1[1,2]=1;J=S.zeros(3);J[2,0]=1
    s['couplings']=[coupling('charge',0,Q)]
    s['generator_terms']=[term('raw cell',[0],H,[(1,L0),(1,L1),(S.Rational(1,100),J)])]
    return s

def qubits():
    s=base([2,2]);N=S.diag(0,1);L=S.Matrix([[0,1],[0,0]])
    s['couplings']=[coupling('c0',0,N),coupling('c1',1,N)]
    s['generator_terms']=[term('loss0',[0],S.zeros(2),[(4,L)]),term('loss1',[1],S.zeros(2),[(4,L)]),
        term('injection0',[0],S.zeros(2),[(S.Rational(1,100),L.T)]),
        term('injection1',[1],S.zeros(2),[(S.Rational(1,100),L.T)]),
        term('hopping',[0,1],S.Rational(1,4)*(S.kronecker_product(L,L.T)+S.kronecker_product(L.T,L)))]
    return s

def run():
    checks=[]; fixtures={}
    def test(name,cond):
        assert cond,name;checks.append(name)
    for name,s in [('mixed_qutrit',qutrit()),('qubit_hopping',qubits())]:
        start=time.perf_counter();r=a.acquire(s);elapsed=time.perf_counter()-start
        print(name,r['status'],r.get('reason'),elapsed,flush=True)
        test(name+' admitted',r['status']=='CERTIFIED');test(name+' external verifies',a.verify_certificate(s,r))
        fixtures[name]=(s,r,elapsed)
    s,r,_=fixtures['mixed_qutrit']
    test('rank two transparent mixed sector',r['projectors'][0]['transparent_rank']==2)
    nohuge=qutrit(0); rr=a.acquire(nohuge)
    test('huge harmless Hamiltonian same allocations',a.strict_equal(rr['allocations'],r['allocations']))
    budgeted=copy.deepcopy(s);budgeted['search_budget']['max_lp_constraints']=1
    test('finite LP size refusal',a.acquire(budgeted)['reason']=='LP_SIZE_BUDGET')
    # An inactive source cannot create a loss certificate below the activation cap.
    fake=copy.deepcopy(s);fake['generator_terms'][0]['hamiltonian']=mat(S.zeros(3));fake['generator_terms'][0]['jumps']=[]
    test('fake loss UNKNOWN',a.acquire(fake)['status']=='UNKNOWN')
    # Full-rank bypass coupling has no common transparent sector.
    bypass=copy.deepcopy(s);bypass['couplings'].append(coupling('bypass',0,S.eye(3)))
    test('bypass not admitted',a.acquire(bypass)['reason']=='NO_COMMON_TRANSPARENT_SECTOR')
    # Source creation is a raw GENERATOR term; charge it, never omit it.
    create=base([2]);N=S.diag(0,1);L=S.Matrix([[0,1],[0,0]]);X=L+L.T
    create['couplings']=[coupling('charge',0,N)]
    create['generator_terms']=[term('loss',[0],S.zeros(2),[(10,L)]),term('drive',[0],X)]
    test('unbudgeted coherent source creation UNKNOWN',a.acquire(create)['status']=='UNKNOWN')
    create['activation_cap']=q(2);cr=a.acquire(create)
    test('budgeted coherent creation admitted',cr['status']=='CERTIFIED' and a.verify_certificate(create,cr))
    act=sum(a.rat(al['activation'][0]) for al in cr['allocations'])
    test('creation pays nonzero activation',act>=1)
    fixtures['charged_creation']=(create,cr,None)
    # No claimed geometry oracle: the coupling itself is non-diagonal.
    rotated=base([2]);B=S.Matrix([[1,-1],[-1,1]])/2
    rotated['couplings']=[coupling('rotated',0,B)]
    # L=|+><-| with rational entries.
    LR=S.Matrix([[1,-1],[1,-1]])/2
    rotated['generator_terms']=[term('loss',[0],S.zeros(2),[(4,LR)])]
    rot=a.acquire(rotated)
    test('rotated raw common kernel discovered',rot['projectors'][0]['transparent_rank']==1)
    test('rotated sufficient certificate',rot['status']=='CERTIFIED' and a.verify_certificate(rotated,rot))
    # PSD verifier handles singular matrices, rejects zero pivot with offdiagonal.
    for name,A,want in [('singular',S.diag(1,0),True),('zero',S.zeros(2),True),
                        ('bad zero pivot',S.Matrix([[0,1],[1,2]]),False),('negative',S.diag(1,-1),False),
                        ('rankone complex',S.Matrix([[1,S.I],[-S.I,1]]),True)]:
        test('PSD '+name,a.psd(A)==want)
    B=S.Matrix([[9,9+9*S.I,-6*S.I],[9-9*S.I,18,-6-6*S.I],[6*S.I,-6+6*S.I,4]])
    PP,QQ=a.charges([3],[[B]])
    test('reviewer complex common-kernel regression',S.trace(PP[0])==2 and a.normalized_matrix(B*PP[0])==S.zeros(3))
    rng=random.Random(7321)
    for k in range(30):
        d=1+k%5; rank=1+k%3
        X=S.Matrix(d,rank,lambda i,j:S.Rational(rng.randrange(-3,4),3)+S.I*S.Rational(rng.randrange(-3,4),5))
        A=(X*X.H).applyfunc(S.expand)
        test('reviewer complex Gram regression '+str(k),a.psd(A))
        test('reviewer negative Gram regression '+str(k),not a.psd(A-S.diag(A[0,0]+1,*([0]*(d-1)))))
    # Degree2 Bernstein must not mistake positive endpoint values for positivity.
    u=S.symbols('u',real=True)
    co=a.bernstein(S.Matrix([(u-S.Rational(1,2))**2-S.Rational(1,10)]),[u])
    test('interior-negative polynomial coefficient rejected',not all(a.psd(x) for x in co.values()))
    # External task and every scientific claim are bound.
    for name,fn in [('task',lambda x:x['task'].__setitem__('id','other')),
                    ('gap',lambda x:x.__setitem__('requested_gap',q(3))),
                    ('activation',lambda x:x.__setitem__('activation_cap',q(0))),
                    ('operator',lambda x:x['generator_terms'][0]['jumps'][0].__setitem__('rate',q(0)))]:
        z=copy.deepcopy(s);fn(z);test('external '+name+' mismatch',not a.verify_certificate(z,r))
    for name,fn in [('hash',lambda x:x.__setitem__('input_sha256','0'*64)),
                    ('rank bool',lambda x:x['projectors'][0].__setitem__('transparent_rank',True)),
                    ('rank float',lambda x:x['projectors'][0].__setitem__('transparent_rank',2.0)),
                    ('matrix',lambda x:x['allocations'][0]['M'][0].__setitem__(0,q(-100))),
                    ('activation',lambda x:x['allocations'][0]['activation'].__setitem__(0,q(0))),
                    ('extra',lambda x:x.__setitem__('extra',0)),
                    ('stats',lambda x:x['acquisition_counts'].__setitem__('lp_constraints',True))]:
        z=copy.deepcopy(r);fn(z);test('record '+name+' tamper',not a.verify_certificate(s,z))
    for bad in [None,[],1,True,{},'bad']:
        test('invalid record '+repr(bad),not a.verify_certificate(s,bad))
    for name,fn in [('bool dim',lambda x:x['cells'].__setitem__(0,True)),
                    ('negative rate',lambda x:x['generator_terms'][0]['jumps'][0].__setitem__('rate',q(-1))),
                    ('malformed matrix',lambda x:x['generator_terms'][0].__setitem__('hamiltonian',[])),
                    ('unsupported extra spectator',lambda x:x.__setitem__('spectator_norm','assume')),
                    ('bad gap',lambda x:x.__setitem__('requested_gap',q(0))),
                    ('noncanonical',lambda x:x.__setitem__('activation_cap',[2,20])),
                    ('coupling nonHermitian',lambda x:x['couplings'][0].__setitem__('source_matrix',mat(S.Matrix([[0,1,0],[0,0,0],[0,0,1]]))))]:
        z=copy.deepcopy(s);fn(z)
        try:a.acquire(z)
        except a.InputError: ok=True
        else:ok=False
        test('reject '+name,ok)
    try:a.load('{"x":1,"x":2}')
    except a.InputError:ok=True
    else:ok=False
    test('duplicate JSON rejected',ok)
    # Timer budgets are enforced and an existing caller timer is not replaced.
    with patch.object(a,'lpmin',side_effect=lambda *_: time.sleep(2)):
        try:a.budgeted_lp(S.Integer(0),[],1)
        except a.SearchLimit:ok=True
        else:ok=False
    test('LP timeout enforced',ok and signal.getitimer(signal.ITIMER_REAL)[0]==0)
    signal.setitimer(signal.ITIMER_REAL,10)
    try:
        try:a.budgeted_lp(S.Integer(0),[],1)
        except a.SearchLimit:ok=True
        else:ok=False
        test('existing timer preserved',ok and signal.getitimer(signal.ITIMER_REAL)[0]>0)
    finally:signal.setitimer(signal.ITIMER_REAL,0)
    # Executed CLI statuses, including UNKNOWN and independent verification.
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); ip=td/'input.json'; cp=td/'cert.json'
        ip.write_text(json.dumps(s)); cp.write_text(json.dumps(r))
        cli=[__import__('sys').executable,str(Path(a.__file__))]
        test('CLI acquire',subprocess.run(cli+[str(ip),'--output',str(td/'out.json')],capture_output=True).returncode==0)
        test('CLI verifies',subprocess.run(cli+[str(ip),'--verify',str(cp)],capture_output=True).returncode==0)
        wrong=copy.deepcopy(r);wrong['input_sha256']='0'*64;cp.write_text(json.dumps(wrong))
        test('CLI wrong certificate fails',subprocess.run(cli+[str(ip),'--verify',str(cp)],capture_output=True).returncode==1)
        ip.write_text(json.dumps(fake))
        test('CLI UNKNOWN nonzero',subprocess.run(cli+[str(ip)],capture_output=True).returncode==1)
        ip.write_text('{"format":1,"format":2}')
        test('CLI malformed nonzero',subprocess.run(cli+[str(ip)],capture_output=True).returncode==2)
    return checks,fixtures

if __name__=='__main__':
    checks,fixtures=run();root=Path(__file__).parent
    for name,(s,r,_) in fixtures.items():
        (root/(name+'_input.json')).write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
        (root/(name+'_certificate.json')).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    (root/'operator_certificate_checks.json').write_text(json.dumps({'checks':checks,'count':len(checks),
        'acquisition_seconds':{k:v[2] for k,v in fixtures.items()},'scope':'exact declared-model certificate tests; not hardware'},indent=2)+'\n')
    print(len(checks),'checks passed')
