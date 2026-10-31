#!/usr/bin/env python3
"""Bind an exact raw-operator drift certificate to a complete external schedule.
The reused scalar model is a BOOKKEEPING ENVELOPE, not a physical equivalence.
"""
import argparse, hashlib, importlib.util, json
from pathlib import Path
import sympy as S
import acquire_operator_certificate as raw

HERE=Path(__file__).resolve().parent
LEGACY=HERE.parent/'local_energy_fault_admission_20261031'/'acquire_local_admission.py'
LEGACY_SHA='a7bc4e513cb4de03a3ef5c504bae75b7b464cb4985a9a683cd560f9d439136f8'
FORMAT='raw-operator-location-receiver-v1'

def legacy():
    if hashlib.sha256(LEGACY.read_bytes()).hexdigest()!=LEGACY_SHA:
        raise raw.InputError('frozen schedule component hash mismatch')
    spec=importlib.util.spec_from_file_location('_frozen_schedule_component',LEGACY)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def acquire(spec):
    raw.exactkeys(spec,['format','operator_spec','operator_certificate','schedule'])
    if type(spec['format']) is not str or spec['format']!=FORMAT:raise raw.InputError('receiver format')
    model=spec['operator_spec'];cert=spec['operator_certificate'];schedule=spec['schedule']
    if not raw.verify_certificate(model,cert):raise raw.InputError('raw drift certificate not verified')
    raw.exactkeys(schedule,['task','system_qubits','duration','locations'])
    raw.exactkeys(schedule['task'],['id','consumer_contract_sha256','amplitude_budget'])
    if not raw.strict_equal({k:schedule['task'][k] for k in ('id','consumer_contract_sha256')},model['task']):
        raise raw.InputError('external consumer task mismatch')
    dims,_,terms,_,_,norms=raw.parse(model)
    M=S.zeros(len(dims));aa=[S.Integer(0) for _ in dims]
    for term,allocation in zip(terms,cert['allocations']):
        e=term[0]
        for i,gi in enumerate(e):
            aa[gi]+=raw.rat(allocation['activation'][i])
            for j,gj in enumerate(e):M[gi,gj]+=raw.rat(allocation['M'][i][j])
    kappa=min([-sum(M[i,j] for j in range(len(dims))) for i in range(len(dims))]+
              [-sum(M[j,i] for j in range(len(dims))) for i in range(len(dims))])
    activation=max(aa)
    # The generic-charge proof receives only the row/column margin and
    # activation. Identity of its physical GKSL source is NEVER asserted.
    old=legacy()
    envelope={'format':old.VERSION,'task':schedule['task'],
              'source_model':{'mode':'explicit','sources':[{'loss_lower':raw.encq(kappa),'injection_upper':raw.encq(activation)} for _ in dims],'hopping':[]},
              'system_qubits':schedule['system_qubits'],'duration':schedule['duration'],'locations':schedule['locations'],
              'couplings':[{'source':c['cell'],'source_operator':'occupation','coefficient':raw.encq(norm),'pauli':c['system_pauli']}
                           for c,norm in zip(model['couplings'],norms)]}
    try:check=old.acquire(envelope)
    except old.InputError as e:raise raw.InputError(str(e)) from e
    return {'format':FORMAT,'external_input_sha256':raw.digest(spec),
            'operator_model_sha256':raw.digest(model),'operator_certificate_sha256':raw.digest(cert),
            'external_schedule_sha256':raw.digest(schedule),'frozen_schedule_component_sha256':LEGACY_SHA,
            'status':check['status'],'reason':check['reason'],
            'parameters':{'source_cells':len(dims),'source_dimensions':dims,'drift_gap':raw.encq(kappa),
                          'activation_upper':raw.encq(activation),
                          **{k:v for k,v in check['parameters'].items() if k in ('coupling_c_upper','source_support_g','location_duration_tau','control_epsilon_upper','requested_amplitude_budget')}},
            'certificate':check['certificate'],
            'schedule_resources':{k:v for k,v in check['resources'].items() if k in ('system_qubits','raw_coupling_terms','merged_nonzero_coupling_terms','coupling_location_assignments','locations','system_patch_entries','max_system_patch_size','idle_locations','intended_pauli_action_upper')},
            'comparators':check['comparators'],
            'scope':'Conditional known finite-operator model and complete schedule admission. Scalar envelope is not a physical source replacement. Hardware, consumer threshold and control evidence truth remain unverified.'}

def verify_certificate(external_spec,record):
    try:return type(record) is dict and raw.strict_equal(acquire(external_spec),record)
    except (raw.InputError,ValueError,TypeError,KeyError,IndexError,AttributeError,ZeroDivisionError):return False

def verify_admitted(external_spec,record):
    return verify_certificate(external_spec,record) and record['status']=='PASS'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--verify');p.add_argument('--output');args=p.parse_args()
    try:
        x=raw.load(Path(args.input).read_text())
        if args.verify:
            ok=verify_admitted(x,raw.load(Path(args.verify).read_text()));print(json.dumps({'admitted':ok}));return 0 if ok else 1
        out=acquire(x);txt=json.dumps(out,sort_keys=True,indent=2)+'\n'
        if args.output:Path(args.output).write_text(txt)
        else:print(txt,end='')
        return 0 if out['status']=='PASS' else 1
    except (raw.InputError,ValueError,OSError) as exc:
        print(json.dumps({'status':'REJECTED','reason':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
