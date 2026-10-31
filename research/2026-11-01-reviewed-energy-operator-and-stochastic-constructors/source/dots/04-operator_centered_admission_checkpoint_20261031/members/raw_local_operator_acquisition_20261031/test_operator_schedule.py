import copy,json,time
from pathlib import Path
import acquire_operator_certificate as raw
import receive_operator_schedule as recv
from test_operator_certificate import qutrit,q

def fixture():
    model=qutrit(); model['requested_gap']=q(10**8)
    model['generator_terms'][0]['jumps'][0]['rate']=q(10**8)
    model['generator_terms'][0]['jumps'][1]['rate']=q(10**8)
    cert=raw.acquire(model)
    return {'format':recv.FORMAT,'operator_spec':model,'operator_certificate':cert,
        'schedule':{'task':dict(model['task'],amplitude_budget=[1,10**6]),'system_qubits':1,'duration':[1,1],
                    'locations':[{'id':'actual X gate','start':[0,1],'end':[1,1],'patch':[0],
                                  'target':{'kind':'constant_pauli_hamiltonian','terms':[{'coefficient':[1,1],'pauli':[[0,'X']]}]},
                                  'control_error':{'integrated_hamiltonian_bound':[0,1],'evidence_sha256':'b'*64}}]}}

def run():
    checks=[]
    def check(name,b):assert b,name;checks.append(name)
    spec=fixture();t=time.perf_counter();rec=recv.acquire(spec);elapsed=time.perf_counter()-t
    check('complete qutrit schedule PASS',rec['status']=='PASS')
    check('external task verified',recv.verify_admitted(spec,rec))
    check('no physical qubit mislabel',rec['parameters']['source_dimensions']==[3] and 'source_qubits' not in rec['schedule_resources'])
    check('actual gap reused',rec['parameters']['drift_gap']==[10**8,1])
    for name,fn in [('external budget',lambda x:x['schedule']['task'].__setitem__('amplitude_budget',[1,10**12])),
                    ('different model',lambda x:x['operator_spec']['couplings'][0].__setitem__('cell',1)),
                    ('different target',lambda x:x['schedule']['locations'][0].__setitem__('target',{'kind':'idle'}))]:
        z=copy.deepcopy(spec);fn(z);check(name+' invalidates saved admission',not recv.verify_admitted(z,rec))
    for name,fn in [('missing idle',lambda x:x['schedule'].__setitem__('system_qubits',2)),
                    ('task mismatch',lambda x:x['schedule']['task'].__setitem__('id','other')),
                    ('unverified control kind',lambda x:x['schedule']['locations'][0].__setitem__('target',{'kind':'reset'})),
                    ('bad raw certificate',lambda x:x['operator_certificate']['allocations'][0]['M'][0].__setitem__(0,[-10**20,1])),
                    ('schedule gap',lambda x:x['schedule']['locations'][0].__setitem__('start',[1,2]))]:
        z=copy.deepcopy(spec);fn(z)
        try:recv.acquire(z)
        except raw.InputError:ok=True
        else:ok=False
        check(name+' rejected',ok)
    # Same source coupled to two simultaneous disjoint system gates is rejected.
    z=copy.deepcopy(spec);c=copy.deepcopy(z['operator_spec']['couplings'][0]);c['id']='second';c['system_pauli']=[[1,'Z']]
    z['operator_spec']['couplings'].append(c);z['operator_certificate']=raw.acquire(z['operator_spec'])
    z['schedule']['system_qubits']=2;l=copy.deepcopy(z['schedule']['locations'][0]);l['id']='other';l['patch']=[1];l['target']={'kind':'idle'};z['schedule']['locations'].append(l)
    try:recv.acquire(z)
    except raw.InputError:ok=True
    else:ok=False
    check('same guard simultaneous fanout rejected',ok)
    z=copy.deepcopy(spec);z['schedule']['locations'][0]['control_error']['integrated_hamiltonian_bound']=[1,10]
    notadmitted=recv.acquire(z)
    check('large actual control residual NOT_ADMITTED',notadmitted['status']=='NOT_ADMITTED')
    check('truthful NOT_ADMITTED verifies but not admitted',recv.verify_certificate(z,notadmitted) and not recv.verify_admitted(z,notadmitted))
    for bad in (None,[],True,{}):check('invalid record '+repr(bad),not recv.verify_certificate(spec,bad))
    r=copy.deepcopy(rec);r['parameters']['source_cells']=True
    check('bool alias rejected',not recv.verify_certificate(spec,r))
    return checks,spec,rec,elapsed
if __name__=='__main__':
    checks,spec,rec,elapsed=run();here=Path(__file__).parent
    (here/'qutrit_complete_schedule_input.json').write_text(json.dumps(spec,sort_keys=True,indent=2)+'\n')
    (here/'qutrit_complete_schedule_certificate.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
    (here/'operator_schedule_checks.json').write_text(json.dumps({'checks':checks,'count':len(checks),'receiver_seconds':elapsed},indent=2)+'\n')
    print(len(checks),'checks passed; eta=',rec['certificate']['eta_upper'])
