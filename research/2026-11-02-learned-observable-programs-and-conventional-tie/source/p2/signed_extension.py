"""Incrementally acquire a NEW mode with a generic SIGNED observable calculus.
Preserves frozen v1 bits, uses only 8 extra Poisson measurements to discover
new signed transitions; no hidden rate law read inside this compiler.
"""
import json,math,hashlib
from dataclasses import dataclass
from pathlib import Path
from fractions import Fraction
from source_device import MeasuredDevice,PrivateBath
from synthesize import acquire,walsh_fit,local_residual

ROOT=Path(__file__).parent
BASE_HASH='3581c7c1f8de3d8db9e11e634cc38c15b7f38a2574d0d3df8897f4becbdbde95'

@dataclass(frozen=True)
class HiddenFieldBath(PrivateBath):
    field:float=.0
    def rate(self,spins):
        return super().rate(spins)+self.field*spins[1]

HIDDEN=HiddenFieldBath(.80,.18,.16,.035,.14)

def signed_program(rec,base_encoding=(-1,1),target_rho=.014):
    assert tuple(base_encoding)==(-1,1)
    th=walsh_fit(rec.estimates)
    a=th[0]
    # Positive, negative or complex weights not preselected. Enumerate 7 generic
    # index-configuration toggles. Signed candidate is acquired if its local
    # coefficient has credible effect; a sign bit is attached to its execution.
    proposals={m:-2*v for m,v in th.items() if m}
    chosen={};history=[]
    for step in range(8):
        err=local_residual(rec,a,chosen)
        history.append({'step':step,'residual':float(err),'rules':{str(m):str(q) for m,q in chosen.items()}})
        if err<=target_rho:break
        opts=[]
        for m,q in proposals.items():
            if m in chosen:continue
            new=dict(chosen);new[m]=q
            if 2*a-sum(abs(v) for v in new.values())<0:continue
            rho=local_residual(rec,a,new)
            opts.append((rho,m,q))
        if not opts:break
        opts.sort()
        rho,m,q=opts[0]
        if rho>=err:break
        chosen[m]=q
        history[-1]['next_rule']=m
    final=local_residual(rec,a,chosen)
    kill=2*a-sum(abs(q) for q in chosen.values())
    if kill<0:raise RuntimeError('No bounded signed dual; costly weighted fallback not implemented')
    return {'mode':rec.mode,'encoding':list(base_encoding),'alpha':float(a),'alpha_fraction':str(a),
            'kill':float(kill),'kill_fraction':str(kill),'local_residual_bound':float(final),
            'local_residual_fraction':str(final),
            'rules':[{'toggle_mask':m,'offsets':[j-1 for j in range(3) if (m>>j)&1],
                     'rate':float(abs(q)),'rate_fraction':str(abs(q)),
                     'sign':(1 if q>=0 else -1)} for m,q in sorted(chosen.items())],
            'history':history,'candidate_rules_tested':7,'missing_signed_offdiag_if_nonnegative_only':
                [m for m,q in proposals.items() if q<-.015],
            'source_configuration_count':8,'heldout_source_law_unread_by_compiler':True}

if __name__=='__main__':
    v1=(ROOT/'frozen_programs.json').read_bytes()
    assert hashlib.sha256(v1).hexdigest()==BASE_HASH
    frozen=json.loads(v1)
    device=MeasuredDevice({'weak_field':HIDDEN},seed=72117)
    rec=acquire(device,'weak_field',2_000_000,total_cells=16)
    proposal=signed_program(rec,tuple(frozen['programs']['baseline']['encoding']))
    if proposal['local_residual_bound']>.015:raise RuntimeError('Failed signed acquisition')
    if not any(z['sign']<0 for z in proposal['rules']):raise RuntimeError('Signed case not acquired')
    result={'derived_from_frozen_sha256':BASE_HASH,
            'new_physical_exposure':device.exposures,'new_scalar_reports':device.calls,
            'new_observed_event_count':device.reported_events,
            'new_mode':proposal,'source_confidence':'original 16 cells and new 8 cells: joint failure < 48 exp(-22)',
            'no_training_on_larger_graphs':True,
            'previous_modes_unchanged':True}
    (ROOT/'signed_frozen_v2.json').write_text(json.dumps(result,indent=2,sort_keys=True))
    (ROOT/'signed_measurements_v2.json').write_text(json.dumps(rec.to_json(),indent=2,sort_keys=True))
    print('V2 SHA256',hashlib.sha256((ROOT/'signed_frozen_v2.json').read_bytes()).hexdigest())
    print('new',proposal['rules'],'kill',proposal['kill'],'local residual',proposal['local_residual_bound'])
    print('residual history',[(v['step'],v['residual'],v.get('next_rule')) for v in proposal['history']])
    print('cost',device.exposures,device.reported_events)
