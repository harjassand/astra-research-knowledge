"""Exact tests for declared-model acquisition; no experimental or threshold validation."""
import copy, hashlib, json, math, tempfile, subprocess, sys
from fractions import Fraction as F
from pathlib import Path
import acquire_local_admission as m

HERE=Path(__file__).parent
checks=[]
def check(name,condition):
    assert condition,name;checks.append(name)
def hashtext(t): return hashlib.sha256(t.encode()).hexdigest()
CONTROL=hashtext('Fixture mathematical model: Delta(t)=0 exactly. Not a hardware calibration.')
CONSUMER=hashtext('Fixture requested amplitude budget only; no numerical FT threshold claimed.')
def loc(i,q,start=0,end=1):
    return {'id':f'location-{i}','start':[start,1],'end':[end,1],'patch':[q],
            'target':{'kind':'constant_pauli_hamiltonian','terms':[
                {'coefficient':[1,3],'pauli':[[q,'X']]}]},
            'control_error':{'integrated_hamiltonian_bound':[0,1],'evidence_sha256':CONTROL}}
def term(source,q,coefficient=(1,1),axis='Z'):
    return {'source':source,'source_operator':'occupation','coefficient':list(coefficient),'pauli':[[q,axis]]}
def fixture():
    return {'format':m.VERSION,'task':{'id':'explicit-four-source-two-gate-fixture',
             'consumer_contract_sha256':CONSUMER,'amplitude_budget':[1,10000]},
            'source_model':{'mode':'explicit','sources':[
                {'loss_lower':[1000000,1],'injection_upper':[1,5]} for _ in range(4)],
                'hopping':[{'i':i,'j':i+1,'real':[50000,1],'imag':[0,1]} for i in range(3)]},
            'system_qubits':2,'duration':[1,1],'couplings':[term(0,0),term(1,1)],
            'locations':[loc(0,0),loc(1,1)]}
def million():
    s=fixture();s['task']['id']='known-million-source-open-chain-program'
    s['task']['amplitude_budget']=[1,1000000]
    s['source_model']={'mode':'uniform_open_chain','n':1000000,
        'loss_lower':[1000000000,1],'injection_upper':[1,1],
        'hopping_real':[100000000,1],'hopping_imag':[0,1]}
    s['system_qubits']=1;s['couplings']=[term(500000,0)];s['locations']=[loc(0,0)]
    return s

def rejects(name,change,base=None):
    s=copy.deepcopy(fixture() if base is None else base)
    change(s)
    try: m.acquire(s)
    except m.InputError: check(name,True);return
    raise AssertionError(name+' accepted')

def main():
    s=fixture();r=m.acquire(s)
    check('explicit pass',r['status']=='PASS')
    check('explicit acquisition counts',r['resources']['explicitly_inspected_edges']==3)
    check('exact beta',r['parameters']['beta_upper']==[1,10])
    check('exact c',r['parameters']['coupling_c_upper']==[1,1])
    check('raw bound misses requested budget',not r['comparators']['raw_bound_meets_requested_budget'])
    check('external verifier',m.verify_admitted(s,r))
    for field,new in [('status','NOT_ADMITTED'),('external_spec_sha256','0'*64),('proof_sha256','0'*64)]:
        bad=copy.deepcopy(r);bad[field]=new
        check('reject certificate tamper '+field,not m.verify_certificate(s,bad))
    for new in [True,1.0]:
        bad=copy.deepcopy(r);bad['parameters']['source_support_g']=new
        check('strict certificate g '+repr(new),not m.verify_certificate(s,bad))
    bad=copy.deepcopy(r);bad['extra']='ignored?'
    check('reject extra certificate field',not m.verify_certificate(s,bad))
    changed=copy.deepcopy(s);changed['task']['id']='different consumer task'
    check('external task change',not m.verify_certificate(changed,r))
    changed=copy.deepcopy(s);changed['task']['amplitude_budget']=[1,1000]
    check('external budget change',not m.verify_certificate(changed,r))
    changed=copy.deepcopy(s);changed['locations'][0]['target']['terms'][0]['coefficient']=[2,3]
    check('external intended target change',not m.verify_certificate(changed,r))
    changed=copy.deepcopy(s);changed['locations'][0]['control_error']['evidence_sha256']='0'*64
    check('external control evidence change',not m.verify_certificate(changed,r))
    for bad in [None,[],True,1,'x',{'bad':1}]:
        check('invalid verifier object '+repr(bad),not m.verify_certificate(s,bad))
    for bad in [None,[],True,1,'x',{'bad':1}]:
        check('invalid external spec '+repr(bad),not m.verify_certificate(bad,r))
    rejects('noncanonical rational',lambda x:x['duration'].__setitem__(slice(None),[2,2]))
    rejects('boolean rational numerator',lambda x:x['duration'].__setitem__(0,True))
    rejects('float rational numerator',lambda x:x['duration'].__setitem__(0,1.0))
    rejects('zero denominator',lambda x:x['duration'].__setitem__(1,0))
    rejects('negative denominator',lambda x:x['duration'].__setitem__(1,-1))
    rejects('zero loss',lambda x:x['source_model']['sources'][0].__setitem__('loss_lower',[0,1]))
    rejects('negative injection',lambda x:x['source_model']['sources'][0].__setitem__('injection_upper',[-1,1]))
    rejects('duplicate hopping edge',lambda x:x['source_model']['hopping'].append(copy.deepcopy(x['source_model']['hopping'][0])))
    rejects('hopping self edge',lambda x:x['source_model']['hopping'][0].__setitem__('j',0))
    rejects('out of range hopping',lambda x:x['source_model']['hopping'][0].__setitem__('j',4))
    rejects('boolean source index',lambda x:x['couplings'][0].__setitem__('source',False))
    rejects('source index out of range',lambda x:x['couplings'][0].__setitem__('source',4))
    rejects('source creating X',lambda x:x['couplings'][0].__setitem__('source_operator','X'))
    rejects('source raising',lambda x:x['couplings'][0].__setitem__('source_operator','raise'))
    rejects('unsupported global generator',lambda x:x['source_model'].__setitem__('generator','magic'))
    rejects('empty Pauli support',lambda x:x['couplings'][0].__setitem__('pauli',[]))
    rejects('identity-axis syntax',lambda x:x['couplings'][0]['pauli'][0].__setitem__(1,'I'))
    rejects('duplicate Pauli index',lambda x:x['couplings'][0]['pauli'].append([0,'X']))
    rejects('Pauli index out of range',lambda x:x['couplings'][0]['pauli'][0].__setitem__(0,2))
    rejects('missing idle exposure',lambda x:x['locations'].pop())
    rejects('initial gap',lambda x:x['locations'][0].__setitem__('start',[1,2]))
    rejects('terminal gap',lambda x:x['locations'][0].__setitem__('end',[1,2]))
    rejects('zero location duration',lambda x:x['locations'][0].__setitem__('end',[0,1]))
    rejects('overlapping gate patches',lambda x:x['locations'].append(dict(copy.deepcopy(x['locations'][0]),id='overlap')))
    rejects('duplicate location id',lambda x:x['locations'][1].__setitem__('id','location-0'))
    rejects('target outside patch',lambda x:x['locations'][0]['target']['terms'][0].__setitem__('pauli',[[1,'Z']]))
    rejects('source fanout in simultaneous patches',lambda x:x['couplings'][1].__setitem__('source',0))
    rejects('coupling straddles simultaneous gates',lambda x:x['couplings'][0].__setitem__('pauli',[[0,'X'],[1,'Z']]))
    rejects('negative control budget',lambda x:x['locations'][0]['control_error'].__setitem__('integrated_hamiltonian_bound',[-1,1]))
    rejects('unacquired preparation',lambda x:x['locations'][0].__setitem__('target',{'kind':'perfect_reset'}))
    rejects('bad evidence hash',lambda x:x['locations'][0]['control_error'].__setitem__('evidence_sha256','fake'))
    rejects('budget zero',lambda x:x['task'].__setitem__('amplitude_budget',[0,1]))
    # Exact cancellation is recognized before fanout/acquired norms.
    z=fixture();z['couplings'] +=[term(0,1),term(0,1,(-1,1))]
    rz=m.acquire(z);check('exact cancellation avoids false fanout',rz['status']=='PASS' and rz['parameters']['coupling_c_upper']==[1,1])
    z=fixture();z['couplings'] +=[term(0,0,(2,1)),term(0,0,(-1,1))]
    check('merged Pauli coefficient norm',m.acquire(z)['parameters']['coupling_c_upper']==[2,1])
    z=fixture();z['source_model']['hopping'][0]['imag']=[30000,1]
    check('complex hopping rational L1 bound',m.acquire(z)['parameters']['beta_upper']==[13,100])
    z=fixture();z['source_model']['sources'][0]['loss_lower']=[500000,1]
    check('actual loss minimum',m.acquire(z)['parameters']['beta_upper']==[1,5])
    z=fixture();z['source_model']['hopping'][1]['real']=[500000,1]
    rz=m.acquire(z);check('valid strong transport not admitted',rz['status']=='NOT_ADMITTED')
    check('valid NOT_ADMITTED verifies but is not admitted',m.verify_certificate(z,rz) and not m.verify_admitted(z,rz))
    z=fixture();z['locations'][0]['control_error']['integrated_hamiltonian_bound']=[1,2]
    check('control radius rejection',m.acquire(z)['reason']=='optimized contour radius below two')
    z=fixture();z['task']['amplitude_budget']=[1,10**12]
    check('consumer budget failure',m.acquire(z)['reason']=='certified bound exceeds consumer budget')
    z=fixture();z['couplings']=[]
    check('zero-coupling zero-control exact',m.acquire(z)['certificate']['eta_upper']==[0,1])
    z['locations'][0]['control_error']['integrated_hamiltonian_bound']=[1,100000]
    check('ordinary control-only branch',m.acquire(z)['certificate']['eta_upper']==[1,100000])
    z=fixture();z['locations'][0]['control_error']['integrated_hamiltonian_bound']=[1,1000000]
    rz=m.acquire(z);check('nonzero control combined exponent',rz['certificate']['exponential_upper']==[17,8])
    # Sequential reuse of a source is admitted, unlike simultaneous fanout.
    z=fixture();z['system_qubits']=1;z['duration']=[2,1];z['couplings']=[term(0,0)]
    z['locations']=[loc(0,0,0,1),loc(1,0,1,2)]
    check('sequential source reuse',m.acquire(z)['status']=='PASS')
    # Joint gate permits multiple terms at one actual location.
    z=fixture();z['locations']=[loc(0,0)];z['locations'][0]['patch']=[0,1]
    z['couplings']=[term(0,0),term(0,1)]
    check('same-source joint patch normalization',m.acquire(z)['parameters']['coupling_c_upper']==[2,1])
    # Symbolic finite program, not a hidden n-entry source table.
    z=million();rz=m.acquire(z)
    check('million source program pass',rz['status']=='PASS')
    check('million source graph actual count',rz['resources']['source_edges']==999999)
    check('million source symbolic acquisition explicit',rz['resources']['explicitly_inspected_edges']==0)
    check('million source constant certificate size',len(m.canonical(rz))<5000)
    for n,degree in [(1,0),(2,1),(3,2),(1000000,2)]:
        z=million();z['source_model']['n']=n;z['couplings'][0]['source']=0
        check('chain degree '+str(n),m.acquire(z)['resources']['source_max_degree']==degree)
    # Elementary rational certificates for both exponential constants.
    for x,up in [(F(1,4),F(9,7)),(F(3,4),F(17,8))]:
        partial=sum((x**j/F(math.factorial(j)) for j in range(9)),F(0))
        tail=x**9/F(math.factorial(9))/(1-x/10)
        check('rational exp certificate '+str(x),partial+tail<up)
    with tempfile.TemporaryDirectory() as td:
        for i,text in enumerate(['{"x":1,"x":2}','{"x":1.0}','{"x":NaN}','{"x":Infinity}']):
            p=Path(td)/str(i);p.write_text(text)
            try:m.load(p)
            except m.InputError:check('strict JSON '+str(i),True)
            else:raise AssertionError('bad JSON accepted')
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);sp=td/'spec.json';cp=td/'cert.json'
        sp.write_text(json.dumps(fixture()));cp.write_text(json.dumps(m.acquire(fixture())))
        cmd=[sys.executable,str(HERE/'acquire_local_admission.py'),str(sp),'--verify',str(cp)]
        check('CLI valid admitted',subprocess.run(cmd+['--require-admitted'],capture_output=True).returncode==0)
        cp.write_text(json.dumps({'bad':'record'}))
        check('CLI invalid record exits nonzero',subprocess.run(cmd,capture_output=True).returncode==1)
        z=fixture();z['task']['amplitude_budget']=[1,10**12]
        sp.write_text(json.dumps(z));cp.write_text(json.dumps(m.acquire(z)))
        check('CLI truthful nonadmitted verification',subprocess.run(cmd,capture_output=True).returncode==0)
        check('CLI requires actual admission',subprocess.run(cmd+['--require-admitted'],capture_output=True).returncode==1)
        check('CLI generation admission exit',subprocess.run([sys.executable,str(HERE/'acquire_local_admission.py'),str(sp),'--require-admitted'],capture_output=True).returncode==1)
        sp.write_text('{"duration":1.0}')
        check('CLI malformed input rejection',subprocess.run(cmd,capture_output=True).returncode==2)
    return checks

if __name__=='__main__':
    names=main();print(json.dumps({'passed':len(names),'checks':names},indent=2))
    (HERE/'local_admission_test_results.json').write_text(json.dumps({'passed':len(names),'checks':names},indent=2)+'\n')
    for name,spec in [('explicit_fixture',fixture()),('million_source_fixture',million())]:
        (HERE/(name+'_input.json')).write_text(json.dumps(spec,sort_keys=True,indent=2)+'\n')
        (HERE/(name+'_certificate.json')).write_text(json.dumps(m.acquire(spec),sort_keys=True,indent=2)+'\n')
