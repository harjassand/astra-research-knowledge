"""Independent parser/enumerator of the actual serialized one-shot network.

No worker generator or transition routine is imported. Actual prepared z=1
is retained. Full reachable count states are used, not trajectory sampling.
"""
from pathlib import Path
from collections import Counter,deque
import hashlib,json,sys,time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[3]
sys.path.insert(0,str(WORKSPACE/'work/sol6_openings_20261027/positive_current_operation/vendor'))
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

SOURCE=ROOT.parents[1]/'finite_copy_bridge/GENERATED_ACTION_CRN.json'
raw=SOURCE.read_bytes();network=json.loads(raw)
names=network['species'];index={n:i for i,n in enumerate(names)}
rules=[(Counter(r['reactants']),Counter(r['products']),r) for r in network['reactions']]
volume=network['spec']['volume']
yes,no=index['ACTION_YES'],index['ACTION_NO']


def solve(a,b,endpoint):
    initial=[0]*len(names)
    for name,count in network['prepared_context'].items():initial[index[name]]=count
    initial[index['P']]+=a;initial[index['N']]+=b
    states=[tuple(initial)];where={states[0]:0};queue=deque([states[0]])
    edges=[]
    while queue:
        state=queue.popleft();es=[]
        if state[yes]+state[no]:
            assert state[yes]+state[no]==1
            edges.append(es);continue
        for reactants,products,r in rules:
            if any(state[index[n]]<count for n,count in reactants.items()):continue
            if 'rate_interval' in r:rate=r['rate_interval'][endpoint]
            else:rate=r['rate_lower_bound']
            order=sum(reactants.values());prop=rate/volume**(order-1)
            target=list(state)
            for name,count in reactants.items():
                for k in range(count):prop*=state[index[name]]-k
                target[index[name]]-=count
            for name,count in products.items():target[index[name]]+=count
            target=tuple(target)
            if target not in where:where[target]=len(states);states.append(target);queue.append(target)
            es.append((where[target],prop))
        assert es
        edges.append(es)
    transient=[i for i,s in enumerate(states) if not(s[yes]+s[no])]
    ix={old:new for new,old in enumerate(transient)}
    rows=[];cols=[];vals=[];wrong=np.zeros(len(ix));right=np.zeros(len(ix))
    truth=a>b
    for old in transient:
        i=ix[old];total=0
        for to,rate in edges[old]:
            total+=rate
            if to in ix:rows.append(i);cols.append(ix[to]);vals.append(-rate)
            else:
                correct=bool(states[to][yes])==truth
                (right if correct else wrong)[i]+=rate
        rows.append(i);cols.append(i);vals.append(total)
    killed=csr_matrix((vals,(rows,cols)),shape=(len(ix),len(ix)))
    fail=spsolve(killed,wrong);success=spsolve(killed,right)
    mean=spsolve(killed,np.ones(len(ix)))
    assert np.max(abs(fail+success-1))<1e-10
    assert -1e-12<fail[ix[0]]<network['spec']['epsilon_total']
    h=network['spec']['clock_stages'];rate=network['spec']['clock_rate_interval'][endpoint]
    n=a+b+network['prepared_context']['z']
    expected=h/rate+volume/n
    assert abs(mean[ix[0]]/expected-1)<1e-10
    return {'A':a,'B':b,'prepared_z':network['prepared_context']['z'],
      'rate_endpoint':endpoint,'full_reachable_states':len(states),'transient_states':len(ix),
      'wrong_action_probability':float(fail[ix[0]]),'absorption_completeness_error':float(np.max(abs(fail+success-1))),
      'mean_action_time':float(mean[ix[0]]),'independent_clock_plus_collision_mean':float(expected),
      'linear_system_max_residual':float(np.max(abs(killed@mean-1)))}


start=time.monotonic()
records=[solve(a,b,end) for a,b in [(3,2),(2,3),(2,2),(0,0)] for end in (0,1)]
out={'status':'ACTUAL_SERIALIZED_CRN_PREPARED_CONTEXT_REPLAY_PASS',
 'network_sha256':hashlib.sha256(raw).hexdigest(),'records':records,
 'seconds':time.monotonic()-start,
 'scope':'Exact reachable-state enumeration with floating sparse backward-equation solves for eight declared inputs/rate endpoints. Not an independent proof of every bounded input/rate assignment or physical chemistry.'}
(ROOT/'REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
