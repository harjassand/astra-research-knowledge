#!/usr/bin/env python3
"""Complete-schedule centered-creation receiver with exact radius arithmetic.
A scalar envelope is used only to reuse frozen schedule SUPPORT checks.
"""
import argparse, hashlib, importlib.util, json
from pathlib import Path
import sympy as S
import acquire_centered_certificate as cc
raw=cc.raw
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'local_energy_fault_admission_20261031'/'acquire_local_admission.py'
OLD_SHA='a7bc4e513cb4de03a3ef5c504bae75b7b464cb4985a9a683cd560f9d439136f8'
FORMAT='centered-creation-location-receiver-v1'


def old_checker():
    if hashlib.sha256(OLD.read_bytes()).hexdigest()!=OLD_SHA:raise raw.InputError('frozen schedule hash')
    sp=importlib.util.spec_from_file_location('_schedule_support_component',OLD)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m


def acquire(spec):
    raw.exactkeys(spec,['format','centered_spec','centered_certificate','schedule','arithmetic_budget'])
    if type(spec['format']) is not str or spec['format']!=FORMAT:raise raw.InputError('receiver format')
    parsed,M,aa,Ps,Qs=cc.verified_parameters(spec['centered_spec'],spec['centered_certificate'])
    dims,Bs,terms,_,_,norms=parsed
    raw.exactkeys(spec['arithmetic_budget'],['max_radius_doublings','max_exponential_power'])
    for v in spec['arithmetic_budget'].values():raw.integer(v,1)
    if spec['arithmetic_budget']['max_radius_doublings']>100000 or spec['arithmetic_budget']['max_exponential_power']>100000:
        raise raw.InputError('arithmetic implementation limit')
    schedule=spec['schedule'];raw.exactkeys(schedule,['task','system_qubits','duration','locations'])
    raw.exactkeys(schedule['task'],['id','consumer_contract_sha256','amplitude_budget'])
    model=spec['centered_spec']['operator_model']
    if not raw.strict_equal({k:schedule['task'][k] for k in ('id','consumer_contract_sha256')},model['task']):
        raise raw.InputError('external consumer mismatch')
    kappa=min([-sum(M[i,j] for j in range(len(dims))) for i in range(len(dims))]+[-sum(M[j,i] for j in range(len(dims))) for i in range(len(dims))])
    D=max(-M[i,i] for i in range(len(dims)));a=max(aa);old=old_checker()
    envelope={'format':old.VERSION,'task':schedule['task'],'system_qubits':schedule['system_qubits'],
        'duration':schedule['duration'],'locations':schedule['locations'],
        'source_model':{'mode':'explicit','sources':[{'loss_lower':raw.encq(kappa),'injection_upper':raw.encq(a)} for _ in dims],'hopping':[]},
        'couplings':[{'source':x['cell'],'source_operator':'occupation','coefficient':raw.encq(norm),'pauli':x['system_pauli']} for x,norm in zip(model['couplings'],norms)]}
    try:sch=old.acquire(envelope)
    except old.InputError as e:raise raw.InputError(str(e)) from e
    par=sch['parameters'];c=raw.rat(par['coupling_c_upper']);g=par['source_support_g'];tau=raw.rat(par['location_duration_tau'])
    eps=raw.rat(par['control_epsilon_upper']);budget=raw.rat(par['requested_amplitude_budget'])
    annihilating=all(raw.normalized_matrix(B*P)==S.zeros(P.rows) for bs,P in zip(Bs,Ps) for B in bs)
    out={'format':FORMAT,'external_input_sha256':raw.digest(spec),'centered_model_sha256':raw.digest(spec['centered_spec']),
         'centered_certificate_sha256':raw.digest(spec['centered_certificate']),'external_schedule_sha256':raw.digest(schedule),
         'raw_component_sha256':cc.RAW_SHA,'schedule_component_sha256':OLD_SHA,
         'status':'NOT_ADMITTED','reason':'','parameters':{'source_cells':len(dims),'source_dimensions':dims,
         'kappa':raw.encq(kappa),'D':raw.encq(D),'activation':raw.encq(a),'c':raw.encq(c),'g':g,'tau':raw.encq(tau),
         'epsilon_ctl':raw.encq(eps),'consumer_amplitude_budget':raw.encq(budget)},
         'certificate':{'radius':None,'C0':None,'a_eff':None,'exponent':None,'exponential_power':None,'exponential_upper':None,'eta_upper':None},
         'schedule_resources':{k:v for k,v in sch['resources'].items() if k in ('system_qubits','locations','system_patch_entries','max_system_patch_size','idle_locations','intended_pauli_action_upper','coupling_location_assignments')},
         'guarded_alternative':{'annihilating_on_selected_charges':annihilating,
                               'conditional_eta_upper':sch['certificate']['eta_upper'] if annihilating else None,
                               'conditional_status':sch['status'] if annihilating else 'NOT_APPLICABLE'},
         'scope':'Centered-creation known-model conditional amplitude admission, not physical calibration/gate execution. The scalar envelope is support bookkeeping only; its guarded error bound is NOT used for centered couplings.'}
    if c==0:
        out['certificate']['eta_upper']=raw.encq(eps);out['status']='PASS' if eps<=budget else 'NOT_ADMITTED';out['reason']='ordinary control-only bound';return out
    kp=3*kappa/4;F=D-kappa/4;aeff=a+4*c*c/kappa
    C0=g*(1+F/kp)+aeff*g*(1/kp+F*tau/kp)
    out['certificate'].update(C0=raw.encq(C0),a_eff=raw.encq(aeff))
    def allowed(R):return 16*c*R<=kappa and 72*R*R*c*c*g*tau<=kappa and (eps==0 or 2*R*eps<=1)
    R=S.Integer(2)
    if not allowed(R):out['reason']='no admitted power-of-two radius at least two';return out
    doublings=0
    while allowed(2*R):
        if doublings>=spec['arithmetic_budget']['max_radius_doublings']:
            out['reason']='radius arithmetic budget exhausted';return out
        R*=2;doublings+=1
    x=C0/2+18*R*R*c*c*g*tau/kappa+R*eps
    m=int(S.ceiling(8*x))
    out['certificate'].update(radius=raw.encq(R),exponent=raw.encq(x),exponential_power=m)
    if m>spec['arithmetic_budget']['max_exponential_power']:
        out['reason']='exponential rational-size budget exhausted';return out
    E=S.Rational(8,7)**m;eta=E/(R-1)
    out['certificate'].update(exponential_upper=raw.encq(E),eta_upper=raw.encq(eta))
    out['status']='PASS' if eta<=budget else 'NOT_ADMITTED'
    out['reason']='centered clamped bound meets supplied budget' if eta<=budget else 'centered clamped bound exceeds supplied budget'
    return out


def verify_certificate(external_spec,record):
    try:return type(record) is dict and raw.strict_equal(acquire(external_spec),record)
    except (raw.InputError,ValueError,TypeError,KeyError,IndexError,AttributeError,ZeroDivisionError):return False


def verify_admitted(external_spec,record):return verify_certificate(external_spec,record) and record['status']=='PASS'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--verify');p.add_argument('--output');args=p.parse_args()
    try:
        spec=raw.load(Path(args.input).read_text())
        if args.verify:
            ok=verify_admitted(spec,raw.load(Path(args.verify).read_text()));print(json.dumps({'admitted':ok}));return 0 if ok else 1
        out=acquire(spec);txt=json.dumps(out,sort_keys=True,indent=2)+'\n'
        if args.output:Path(args.output).write_text(txt)
        else:print(txt,end='')
        return 0 if out['status']=='PASS' else 1
    except (raw.InputError,ValueError,OSError) as e:
        print(json.dumps({'status':'REJECTED','reason':str(e)}));return 2
if __name__=='__main__':raise SystemExit(main())
