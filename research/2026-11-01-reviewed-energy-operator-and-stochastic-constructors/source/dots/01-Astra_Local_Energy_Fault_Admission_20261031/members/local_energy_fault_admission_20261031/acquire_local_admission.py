#!/usr/bin/env python3
"""Known-model rational local fault-amplitude admission. No hardware validation.
External spec is mandatory for certificate verification. Python standard library only.
"""
from fractions import Fraction as F
from math import gcd
from collections import defaultdict
import argparse, hashlib, json, sys

VERSION='occupation-local-admission-v1'
PROOF_SHA='0b0bd7ffa77e9c90323be91d5dec929b5bbd66d0c059ad783357838bf5ba010e'
COROLLARY_SHA='403e142105400b6cdc5e0f4d7a5b8b62663e79dfd13aa36632206ae6ab7fa77f'
class InputError(ValueError): pass

def obj(x,keys,label):
    if type(x) is not dict or set(x)!=set(keys):
        raise InputError(label+': wrong object fields')
    return x

def integer(x,label,minimum=0):
    if type(x) is not int or x<minimum: raise InputError(label+': invalid integer')
    return x

def string(x,label):
    if type(x) is not str or not x: raise InputError(label+': empty/non-string')
    return x

def array(x,label):
    if type(x) is not list: raise InputError(label+': expected list')
    return x

def rat(x,label):
    if (type(x) is not list or len(x)!=2 or any(type(z) is not int for z in x)
        or x[1]<=0 or gcd(abs(x[0]),x[1])!=1):
        raise InputError(label+': expected canonical [integer, positive denominator]')
    return F(*x)

def pair(x):
    x=F(x);return [x.numerator,x.denominator]

def digest(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)

def sha(x,label):
    if type(x) is not str or len(x)!=64 or any(c not in '0123456789abcdef' for c in x):
        raise InputError(label+': invalid SHA-256')
    return x

def pauli(x,n,label):
    out=[];last=-1
    for z in array(x,label):
        if type(z) is not list or len(z)!=2: raise InputError(label+': malformed Pauli entry')
        q=integer(z[0],label+' index')
        if q>=n or q<=last or type(z[1]) is not str or z[1] not in ('X','Y','Z'):
            raise InputError(label+': Pauli support must be sorted, unique, in range, XYZ')
        out.append((q,z[1]));last=q
    if not out: raise InputError(label+': nonidentity Pauli required')
    return tuple(out)

def merged_paulis(terms,n,label,with_source=False,nsource=None):
    merged=defaultdict(F)
    for t in array(terms,label):
        keys=['coefficient','pauli']+(['source','source_operator'] if with_source else [])
        obj(t,keys,label+' term')
        coeff=rat(t['coefficient'],label+' coefficient');word=pauli(t['pauli'],n,label)
        if with_source:
            i=integer(t['source'],label+' source')
            if i>=nsource: raise InputError(label+': source out of range')
            if t['source_operator']!='occupation' or type(t['source_operator']) is not str:
                raise InputError(label+': only source occupation n_i is admitted')
            key=(i,word)
        else: key=word
        merged[key]+=coeff
    return {k:v for k,v in merged.items() if v}

def source_parameters(model):
    if type(model) is not dict: raise InputError('source_model: object required')
    mode=model.get('mode')
    if mode=='explicit':
        obj(model,['mode','sources','hopping'],'source_model')
        sources=array(model['sources'],'sources');n=len(sources)
        if not n: raise InputError('at least one source required')
        losses=[];injections=[]
        for s in sources:
            obj(s,['loss_lower','injection_upper'],'source')
            loss=rat(s['loss_lower'],'loss_lower');inj=rat(s['injection_upper'],'injection_upper')
            if loss<=0 or inj<0: raise InputError('loss must be positive; injection nonnegative')
            losses.append(loss);injections.append(inj)
        incident=[F(0)]*n;degrees=[0]*n;seen=set()
        edges=array(model['hopping'],'hopping')
        for e in edges:
            obj(e,['i','j','real','imag'],'edge')
            i=integer(e['i'],'edge i');j=integer(e['j'],'edge j')
            if not 0<=i<j<n or (i,j) in seen: raise InputError('unordered unique edge i<j required')
            seen.add((i,j))
            weight=abs(rat(e['real'],'hopping real'))+abs(rat(e['imag'],'hopping imag'))
            if weight:
                incident[i]+=weight;incident[j]+=weight;degrees[i]+=1;degrees[j]+=1
        return dict(n=n,loss=min(losses),injection=max(injections),
                    incident=max(incident),max_degree=max(degrees),edges=len(edges),
                    inspected_sources=n,inspected_edges=len(edges),
                    graph_acquisition='explicit local inspection')
    if mode=='uniform_open_chain':
        obj(model,['mode','n','loss_lower','injection_upper','hopping_real','hopping_imag'],'source_model')
        n=integer(model['n'],'source n',1)
        loss=rat(model['loss_lower'],'loss_lower');inj=rat(model['injection_upper'],'injection_upper')
        if loss<=0 or inj<0: raise InputError('loss must be positive; injection nonnegative')
        w=abs(rat(model['hopping_real'],'hopping real'))+abs(rat(model['hopping_imag'],'hopping imag'))
        degree=min(2,n-1) if w else 0
        return dict(n=n,loss=loss,injection=inj,incident=degree*w,max_degree=degree,
                    edges=n-1,inspected_sources=0,inspected_edges=0,
                    graph_acquisition='known uniform open-chain finite program; symbolic degree proof')
    raise InputError('unsupported source model; no arbitrary generator admission')

def acquire(spec):
    obj(spec,['format','task','source_model','system_qubits','duration','couplings','locations'],'spec')
    if spec['format']!=VERSION or type(spec['format']) is not str: raise InputError('unsupported format')
    task=obj(spec['task'],['id','consumer_contract_sha256','amplitude_budget'],'task')
    string(task['id'],'task id');sha(task['consumer_contract_sha256'],'consumer contract')
    budget=rat(task['amplitude_budget'],'consumer amplitude budget')
    if not 0<budget<1: raise InputError('consumer amplitude budget must lie strictly between zero and one')
    sp=source_parameters(spec['source_model']);nsource=sp['n']
    nsys=integer(spec['system_qubits'],'system_qubits',1)
    T=rat(spec['duration'],'duration')
    if T<=0: raise InputError('positive finite schedule duration required')
    rawlocs=array(spec['locations'],'locations')
    if not rawlocs: raise InputError('full nonempty gate/idle schedule required')
    locs=[];by_qubit=defaultdict(list);ids=set()
    for k,l in enumerate(rawlocs):
        obj(l,['id','start','end','patch','target','control_error'],'location')
        lid=string(l['id'],'location id')
        if lid in ids: raise InputError('duplicate location id')
        ids.add(lid)
        start=rat(l['start'],'start');end=rat(l['end'],'end')
        if not 0<=start<end<=T: raise InputError('location time outside schedule or zero duration')
        patch=array(l['patch'],'patch')
        if not patch or any(type(q) is not int or q<0 or q>=nsys for q in patch) or patch!=sorted(set(patch)):
            raise InputError('patch must be nonempty, sorted, unique and in range')
        target=l['target']
        if type(target) is not dict: raise InputError('target object required')
        if target.get('kind')=='idle':
            obj(target,['kind'],'idle target');target_action=F(0)
        elif target.get('kind')=='constant_pauli_hamiltonian':
            obj(target,['kind','terms'],'Hamiltonian target')
            tp=merged_paulis(target['terms'],nsys,'target')
            if any(not {q for q,axis in word}<=set(patch) for word in tp):
                raise InputError('intended target acts outside its patch')
            target_action=(end-start)*sum(map(abs,tp.values()),F(0))
        else: raise InputError('unsupported target; preparation/measurement need a separate acquired interface')
        ce=obj(l['control_error'],['integrated_hamiltonian_bound','evidence_sha256'],'control error')
        eps=rat(ce['integrated_hamiltonian_bound'],'control-error bound')
        if eps<0: raise InputError('negative control-error bound')
        sha(ce['evidence_sha256'],'control-error evidence')
        locs.append(dict(id=lid,start=start,end=end,patch=set(patch),eps=eps,
                         bysource=defaultdict(F),target_action=target_action))
        for q in patch: by_qubit[q].append(k)
    if len(by_qubit)!=nsys: raise InputError('missing system qubit idle/gate coverage')
    for q,indices in by_qubit.items():
        previous=F(0)
        for k in sorted(indices,key=lambda k:(locs[k]['start'],locs[k]['end'])):
            if locs[k]['start']!=previous: raise InputError('gate/idle schedule has a gap or overlapping patch')
            previous=locs[k]['end']
        if previous!=T: raise InputError('missing terminal idle/gate coverage')
    couplings=merged_paulis(spec['couplings'],nsys,'coupling',True,nsource)
    assignments=0
    for (source,word),coefficient in couplings.items():
        support={q for q,axis in word}
        touched=set()
        for q in support: touched.update(by_qubit[q])
        for k in touched:
            if not support<=locs[k]['patch']:
                raise InputError('always-on coupling straddles simultaneous location patches')
            locs[k]['bysource'][source]+=abs(coefficient);assignments+=1
    source_intervals=defaultdict(list)
    for k,l in enumerate(locs):
        for i in l['bysource']: source_intervals[i].append(k)
    for i,indices in source_intervals.items():
        previous=F(-1)
        for k in sorted(indices,key=lambda k:(locs[k]['start'],locs[k]['end'])):
            if locs[k]['start']<previous: raise InputError('one source controls overlapping active locations')
            previous=locs[k]['end']
    c=max((v for l in locs for v in l['bysource'].values()),default=F(0))
    g=max((len(l['bysource']) for l in locs),default=0)
    tau=max(l['end']-l['start'] for l in locs)
    eps=max(l['eps'] for l in locs)
    loss=sp['loss'];a=sp['injection'];beta=sp['incident']/loss;gamma=1-2*beta
    raw=max((l['end']-l['start'])*sum(l['bysource'].values(),F(0))+l['eps'] for l in locs)
    rec=dict(format=VERSION,proof_sha256=PROOF_SHA,resource_corollary_sha256=COROLLARY_SHA,
             external_spec_sha256=digest(spec),external_task_sha256=digest(task),
             status='NOT_ADMITTED',reason='',parameters=dict(loss_lower=pair(loss),injection_upper=pair(a),
               hopping_incident_l1_upper=pair(sp['incident']),beta_upper=pair(beta),gamma_lower=pair(gamma),
               coupling_c_upper=pair(c),source_support_g=g,location_duration_tau=pair(tau),
               control_epsilon_upper=pair(eps),requested_amplitude_budget=pair(budget)),
             certificate=dict(radius=None,exponential_upper=None,eta_upper=None,linear_eta_upper=None),
             resources=dict(source_qubits=nsource,system_qubits=nsys,source_edges=sp['edges'],
               source_max_degree=sp['max_degree'],graph_acquisition=sp['graph_acquisition'],
               explicitly_inspected_sources=sp['inspected_sources'],explicitly_inspected_edges=sp['inspected_edges'],
               raw_coupling_terms=len(spec['couplings']),merged_nonzero_coupling_terms=len(couplings),
               coupling_location_assignments=assignments,locations=len(locs),
               system_patch_entries=sum(len(l['patch']) for l in locs),
               max_system_patch_size=max(len(l['patch']) for l in locs),
               idle_locations=sum(x['target']['kind']=='idle' for x in rawlocs),
               intended_pauli_action_upper=pair(sum(l['target_action'] for l in locs))),
             comparators=dict(raw_integrated_hamiltonian_amplitude_upper=pair(raw),
               raw_bound_meets_requested_budget=raw<=budget,
               gaussian_correlation_admission='not acquired: no Gaussian/Wick or correlation-integral certificate supplied'),
             scope='Known-model structural/amplitude admission only; consumer threshold, control evidence, model-to-hardware validity and gates are not verified.')
    if c==0:
        rec['certificate']['eta_upper']=pair(eps)
        rec['certificate']['linear_eta_upper']=pair(eps)
        rec['status']='PASS' if eps<=budget else 'NOT_ADMITTED'
        rec['reason']='ordinary control-only Hamiltonian bound' if eps<=budget else 'control-only bound exceeds consumer budget'
        return rec
    if gamma<=0:
        rec['reason']='nonpositive loss-relative transport margin';return rec
    R0=gamma*loss/(8*c*g*(1+a*tau));R=min(R0,1/(2*eps)) if eps else R0
    rec['certificate']['radius']=pair(R)
    if R<2:
        rec['reason']='optimized contour radius below two';return rec
    expbound=F(17,8) if eps else F(9,7)
    eta=expbound/(R-1)
    linear=max(16*expbound*c*g*(1+a*tau)/(gamma*loss),4*expbound*eps)
    rec['certificate'].update(exponential_upper=pair(expbound),eta_upper=pair(eta),linear_eta_upper=pair(linear))
    assert eta<=linear
    rec['status']='PASS' if eta<=budget else 'NOT_ADMITTED'
    rec['reason']='conditional known-model local amplitude bound meets supplied budget' if eta<=budget else 'certified bound exceeds consumer budget'
    return rec

def verify_certificate(external_spec,certificate):
    """Recompute against caller-supplied task/model. True does NOT imply PASS."""
    try:
        if type(certificate) is not dict: return False
        return canonical(acquire(external_spec))==canonical(certificate)
    except (InputError,ValueError,TypeError,OverflowError,RecursionError): return False

def verify_admitted(external_spec,certificate):
    return verify_certificate(external_spec,certificate) and certificate.get('status')=='PASS'

def no_duplicates(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise InputError('duplicate JSON key')
        d[k]=v
    return d

def load(path):
    def bad_number(x): raise InputError('JSON floating/nonfinite numbers are not allowed')
    with open(path) as f:
        return json.load(f,object_pairs_hook=no_duplicates,parse_float=bad_number,parse_constant=bad_number)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('spec');ap.add_argument('--output');ap.add_argument('--verify')
    ap.add_argument('--require-admitted',action='store_true',help='exit nonzero unless the checked/generated record is admitted')
    args=ap.parse_args()
    try:
        spec=load(args.spec);exit_code=0
        if args.verify:
            cert=load(args.verify);ok=verify_certificate(spec,cert)
            result={'record_valid_for_external_spec':ok,'admitted':ok and cert.get('status')=='PASS'}
            if not ok or (args.require_admitted and not result['admitted']):exit_code=1
        else:
            result=acquire(spec)
            if args.require_admitted and result['status']!='PASS':exit_code=1
        data=json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+'\n'
        if args.output:
            with open(args.output,'w') as f:f.write(data)
        else:sys.stdout.write(data)
        return exit_code
    except (InputError,ValueError,TypeError,OverflowError,RecursionError) as e:
        print(json.dumps({'status':'REJECTED','reason':str(e)}));return 2
if __name__=='__main__': raise SystemExit(main())
