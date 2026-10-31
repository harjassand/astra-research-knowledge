import copy,json,sys,time,subprocess,tempfile
from pathlib import Path
import sympy as S
import acquire_centered_certificate as cc
import receive_centered_schedule as recv
raw=cc.raw
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'raw_local_operator_acquisition_20261031'))
from test_operator_certificate import base,term,coupling,q,mat


def centered(model):
    return {'format':cc.FORMAT,'operator_model':model,'candidate_budget':{'max_subset_size':2,'max_subsets_per_cell':16,'max_joint_candidates':16,'max_lp_attempts':16}}


def lossy(lam=10**12,bias=False,guarded=False):
    s=base([2]);L=S.Matrix([[0,1],[0,0]]);X=L+L.T;N=S.diag(0,1)
    s['requested_gap']=q(lam);s['activation_cap']=q(S.Rational(1,100))
    B=N if guarded else X
    if bias:B+=S.diag(1,0)
    s['couplings']=[coupling('actual unwanted coefficient',0,B)]
    s['generator_terms']=[term('actual loss',[0],S.zeros(2),[(lam,L)])]
    return centered(s)


def scheduled(spec,cert):
    return {'format':recv.FORMAT,'centered_spec':spec,'centered_certificate':cert,
       'schedule':{'task':dict(spec['operator_model']['task'],amplitude_budget=[1,10000]),'system_qubits':1,'duration':[1,1],
           'locations':[{'id':'gate','start':[0,1],'end':[1,1],'patch':[0],
               'target':{'kind':'constant_pauli_hamiltonian','terms':[{'coefficient':[1,1],'pauli':[[0,'X']]}]},
               'control_error':{'integrated_hamiltonian_bound':[0,1],'evidence_sha256':'b'*64}}]},
       'arithmetic_budget':{'max_radius_doublings':1000,'max_exponential_power':10000}}


def run():
    checks=[];saved={}
    def ck(name,x):assert x,name;checks.append(name)
    t=time.perf_counter();spec=lossy();cert=cc.acquire(spec);elapsed=time.perf_counter()-t
    ck('source-derived X charge admits',cert['status']=='CERTIFIED' and cc.verify_certificate(spec,cert))
    ck('ground acquired from actual loss',cert['projectors'][0]['P']==mat(S.diag(1,0)))
    ck('coupling does not annihilate ground',raw.parse(spec['operator_model'])[1][0][0]*S.diag(1,0)!=S.zeros(2))
    sch=scheduled(spec,cert);out=recv.acquire(sch)
    ck('full centered schedule admits',out['status']=='PASS' and recv.verify_admitted(sch,out))
    ck('guarded bound not misused',out['guarded_alternative']['conditional_status']=='NOT_APPLICABLE')
    ck('exact consumer budget',raw.rat(out['certificate']['eta_upper'])<=S.Rational(1,10000))
    saved['x_loss']=(spec,cert);saved['x_complete_schedule']=(sch,out)
    ck('nonzero ground compression refused',cc.acquire(lossy(bias=True))['status']=='UNKNOWN')
    # Same actual jump subset may suggest the ground, but omitted creation is NOT free.
    omitted=copy.deepcopy(spec);L=S.Matrix([[0,1],[0,0]])
    omitted['operator_model']['generator_terms'].append(term('actual excitation',[0],S.zeros(2),[(100,L.T)]))
    ck('all creating jumps included in drift',cc.acquire(omitted)['status']=='UNKNOWN')
    omitted['operator_model']['activation_cap']=q(100)
    charged=cc.acquire(omitted)
    ck('creating jump paid can certify',charged['status']=='CERTIFIED' and cc.verify_certificate(omitted,charged))
    parsed,M,aa,_,_=cc.verified_parameters(omitted,charged)
    ck('activation actually charged',max(aa)>=100)
    saved['paid_activation']=(omitted,charged)
    # A two-jump intersection is necessary: neither single kernel is centered.
    mm=base([3]); mm['requested_gap']=q(1000);mm['activation_cap']=q(0)
    J1=S.zeros(3);J1[0,1]=1;J2=S.zeros(3);J2[0,2]=1
    BB=S.Matrix([[0,1,0],[1,0,0],[0,0,1]])
    mm['couplings']=[coupling('centered qutrit',0,BB)]
    mm['generator_terms']=[term('both actual losses',[0],S.zeros(3),[(1000,J1),(1000,J2)])]
    pair=centered(mm);pc=cc.acquire(pair)
    ck('two-jump intersection acquired',pc['status']=='CERTIFIED' and len(pc['proposals'][0])==2 and cc.verify_certificate(pair,pc))
    narrow=copy.deepcopy(pair);narrow['candidate_budget']['max_subset_size']=1
    ck('subset size limitation UNKNOWN',cc.acquire(narrow)['status']=='UNKNOWN')
    narrow=copy.deepcopy(pair);narrow['candidate_budget']['max_subsets_per_cell']=3
    ck('actual subset count paid',cc.acquire(narrow)['status']=='UNKNOWN')
    saved['two_jump_qutrit']=(pair,pc)
    # Zero-rate favorable proposal cannot create a fake ground certificate.
    zero=copy.deepcopy(spec);zero['operator_model']['generator_terms'][0]['jumps'][0]['rate']=q(0)
    ck('zero-rate loss is not a proposal',cc.acquire(zero)['status']=='UNKNOWN')
    # Rate cannot be changed after the source-derived proof by merely editing digest.
    tam=copy.deepcopy(spec);tam['operator_model']['generator_terms'][0]['jumps'][0]['rate']=q(1)
    bad=copy.deepcopy(cert);bad['external_input_sha256']=raw.digest(tam)
    ck('rehashed fake loss rejected',not cc.verify_certificate(tam,bad))
    # Empty subset is first; budget1 stops before actual loss proposal.
    small=copy.deepcopy(spec);small['candidate_budget']['max_subsets_per_cell']=1
    ck('subset budget UNKNOWN',cc.acquire(small)['status']=='UNKNOWN')
    # Phase/rotation of the actual source jump can be acquired exactly.
    rot=copy.deepcopy(spec);U=S.Matrix([[1,S.I],[S.I,1]]) # U/sqrt2 is unitary; rational conjugation below.
    B=raw.parse(spec['operator_model'])[1][0][0]
    rot['operator_model']['couplings'][0]['source_matrix']=mat(U*B*U.H/2)
    rot['operator_model']['generator_terms'][0]['jumps'][0]['operator']=mat(U*L*U.H/2)
    rc=cc.acquire(rot)
    ck('complex rotated source charge',rc['status']=='CERTIFIED' and cc.verify_certificate(rot,rc))
    # One-cell proposals are deliberately incomplete: a purely multi-cell jump
    # does not get silently collapsed into a favorable one-cell operator.
    multi=centered(base([2,2]));multi['operator_model']['couplings']=[coupling('c0',0,S.Matrix([[0,1],[1,0]]))]
    multi['operator_model']['generator_terms']=[term('joint loss',[0,1],S.zeros(4),[(10,S.kronecker_product(L,L))])]
    ck('no unprovided local jump candidate',cc.acquire(multi)['status']=='UNKNOWN')
    # The guarded option stays available when its stronger premise holds.
    gs=lossy(guarded=True);gc=cc.acquire(gs);go=recv.acquire(scheduled(gs,gc))
    ck('guarded alternate applicable',go['guarded_alternative']['conditional_status']=='PASS')
    ck('guarded alternate cheaper',raw.rat(go['guarded_alternative']['conditional_eta_upper'])<raw.rat(go['certificate']['eta_upper']))
    saved['guarded_comparison']=(scheduled(gs,gc),go)
    # Full schedule and external consumer binding.
    for name,fn in [('missing idle',lambda z:z['schedule'].__setitem__('system_qubits',2)),
                    ('task changed',lambda z:z['schedule']['task'].__setitem__('id','other')),
                    ('unknown reset',lambda z:z['schedule']['locations'][0].__setitem__('target',{'kind':'reset'})),
                    ('gap',lambda z:z['schedule']['locations'][0].__setitem__('end',[1,2]))]:
        z=copy.deepcopy(sch);fn(z)
        try:recv.acquire(z)
        except raw.InputError:ok=True
        else:ok=False
        ck('schedule '+name+' rejected',ok)
    for name,fn in [('catalog bool',lambda z:z['selected_catalog_indices'].__setitem__(0,False)),
                    ('candidate position',lambda z:z.__setitem__('candidate_position',False)),
                    ('proposal',lambda z:z['proposals'][0][0].__setitem__(1,1)),
                    ('activation forged',lambda z:z['allocations'][0]['activation'].__setitem__(0,[-1,1])),
                    ('extra',lambda z:z.__setitem__('free_spectator',True))]:
        z=copy.deepcopy(cert);fn(z);ck('certificate '+name+' rejected',not cc.verify_certificate(spec,z))
    for z in (None,[],{},True):ck('bad certificate '+repr(z),not cc.verify_certificate(spec,z))
    for name,fn in [('radius budget',lambda z:z['arithmetic_budget'].__setitem__('max_radius_doublings',1)),
                    ('exponential budget',lambda z:z['arithmetic_budget'].__setitem__('max_exponential_power',1)),
                    ('control cost',lambda z:z['schedule']['locations'][0]['control_error'].__setitem__('integrated_hamiltonian_bound',[1,2]))]:
        z=copy.deepcopy(sch);fn(z);r=recv.acquire(z)
        ck(name+' NOT_ADMITTED',r['status']=='NOT_ADMITTED' and recv.verify_certificate(z,r) and not recv.verify_admitted(z,r))
    # Fixed diffusion: c grows sqrt(lambda), so the eta certificate cannot be
    # made to vanish just by raising lambda. This is a scope/calculation check.
    vals=[]
    for lam in (10**6,10**8):
        d=lossy(lam);d['operator_model']['couplings'][0]['source_matrix']=mat(S.sqrt(lam)*S.Matrix([[0,1],[1,0]])/100)
        r=cc.acquire(d);rr=recv.acquire(scheduled(d,r));vals.append(raw.rat(rr['certificate']['eta_upper']))
    ck('fixed diffusion bound does not vanish with loss',vals[1]>vals[0]/2)
    # Aggregate all terms at one source/location, not one c per summand.
    agg=copy.deepcopy(spec);co=copy.deepcopy(agg['operator_model']['couplings'][0]);co['id']='second term';co['system_pauli']=[[0,'X']]
    agg['operator_model']['couplings'].append(co);ac=cc.acquire(agg);ar=recv.acquire(scheduled(agg,ac))
    ck('all simultaneous terms aggregated',ar['parameters']['c']==[2,1])
    fan=scheduled(agg,ac);fan['centered_spec']['operator_model']['couplings'][1]['system_pauli']=[[1,'X']]
    fan['centered_certificate']=cc.acquire(fan['centered_spec']);fan['schedule']['system_qubits']=2
    lo=copy.deepcopy(fan['schedule']['locations'][0]);lo['id']='other';lo['patch']=[1];lo['target']={'kind':'idle'};fan['schedule']['locations'].append(lo)
    try:recv.acquire(fan)
    except raw.InputError:ok=True
    else:ok=False
    ck('same source simultaneous fanout rejected',ok)
    # A valid but badly conditioned M is charged via D/kappa, not just its gap.
    mm=base([2,2]);scale=10**12;mm['requested_gap']=q(scale);mm['activation_cap']=q(0)
    mm['couplings']=[coupling('c0',0,L+L.T),coupling('c1',1,L+L.T)]
    mm['generator_terms']=[term('proposal0',[0],S.zeros(2),[(scale,L)]),term('proposal1',[1],S.zeros(2),[(scale,L)]),
       term('joint declared losses',[0,1],S.zeros(4),[(101*scale,S.kronecker_product(L,S.eye(2))),(101*scale,S.kronecker_product(S.eye(2),L))])]
    ms=centered(mm);mc=cc.acquire(ms)
    mc['allocations']=[{'M':[[q(-scale)]],'activation':[q(0)]},{'M':[[q(-scale)]],'activation':[q(0)]},
       {'M':[[q(-100*scale),q(100*scale)],[q(100*scale),q(-100*scale)]],'activation':[q(0),q(0)]}]
    ck('conditioned drift certificate exact',cc.verify_certificate(ms,mc))
    ss=scheduled(ms,mc);ss['schedule']['system_qubits']=2
    lo=copy.deepcopy(ss['schedule']['locations'][0]);lo['id']='other';lo['patch']=[1];lo['target']={'kind':'idle'};ss['schedule']['locations'].append(lo)
    mr=recv.acquire(ss)
    ck('diagonal to gap explicitly paid',mr['parameters']['D']==[101*scale,1] and mr['parameters']['kappa']==[scale,1] and raw.rat(mr['certificate']['C0'])>100)
    ck('bad conditioning can defeat admission',mr['status']=='NOT_ADMITTED')
    # Execute both CLI contracts, rather than infer their exit statuses.
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);ip=td/'in.json';op=td/'out.json'
        ip.write_text(json.dumps(spec));cmd=[sys.executable,str(Path(cc.__file__))]
        ck('source CLI acquires',subprocess.run(cmd+[str(ip),'--output',str(op)],capture_output=True).returncode==0)
        ck('source CLI verifies',subprocess.run(cmd+[str(ip),'--verify',str(op)],capture_output=True).returncode==0)
        ip.write_text(json.dumps(lossy(bias=True)))
        ck('source CLI UNKNOWN nonzero',subprocess.run(cmd+[str(ip)],capture_output=True).returncode==1)
        ip.write_text(json.dumps(sch));cmd=[sys.executable,str(Path(recv.__file__))]
        ck('receiver CLI acquires',subprocess.run(cmd+[str(ip),'--output',str(op)],capture_output=True).returncode==0)
        ck('receiver CLI verifies',subprocess.run(cmd+[str(ip),'--verify',str(op)],capture_output=True).returncode==0)
        ip.write_text('{"format":1,"format":2}')
        ck('receiver CLI malformed nonzero',subprocess.run(cmd+[str(ip)],capture_output=True).returncode==2)
    # All aliases in recorded integer leaves must be rejected without optimizer.
    def leaves(x,p=()):
        if type(x) is dict:
            for k,v in x.items():yield from leaves(v,p+(k,))
        elif type(x) is list:
            for k,v in enumerate(x):yield from leaves(v,p+(k,))
        elif type(x) is int:yield p,x
    for path,v in leaves(cert):
        for rep in (bool(v),float(v)):
            z=copy.deepcopy(cert);at=z
            for k in path[:-1]:at=at[k]
            at[path[-1]]=rep
            ck('strict alias '+str(path)+str(type(rep)),not cc.verify_certificate(spec,z))
    return checks,saved,elapsed

if __name__=='__main__':
    checks,saved,elapsed=run();here=Path(__file__).parent
    for name,(inp,out) in saved.items():
        (here/(name+'_input.json')).write_text(json.dumps(inp,sort_keys=True,indent=2)+'\n')
        (here/(name+'_certificate.json')).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    (here/'centered_acquisition_checks.json').write_text(json.dumps({'checks':checks,'count':len(checks),'first_acquisition_seconds':elapsed},indent=2)+'\n')
    print(len(checks),'checks passed')
