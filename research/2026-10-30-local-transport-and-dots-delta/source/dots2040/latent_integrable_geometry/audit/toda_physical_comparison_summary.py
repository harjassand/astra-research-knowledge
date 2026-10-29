"""Join completed full-bridge and independent physical ODE receipts."""
from pathlib import Path
import json,hashlib
import mpmath as mp
mp.mp.dps=70
P=Path(__file__).parent
base=json.loads((P/'toda_full_physical_bridge.json').read_text())
fine=json.loads((P/'toda_full_physical_refinement.json').read_text())
ode=json.loads((P/'toda_direct_ode_reference.json').read_text())
assert len(base['records'])==len(fine['records'])==11
assert all(r['admitted'] and r['below_budget'] for d in [base,fine] for r in d['records'])
assert base['fixed_curve']==fine['fixed_curve']
assert base['source_sha256']==hashlib.sha256((P/'toda_full_physical_bridge.py').read_bytes()).hexdigest()
assert fine['source_sha256']==hashlib.sha256((P/'toda_full_physical_refinement.py').read_bytes()).hexdigest()
records=[]
for k,t in [(9,'16'),(10,'32')]:
 ref=ode['records'][-1]['states'][t];other=ode['records'][0]['states'][t]
 b=base['records'][k];f=fine['records'][k]
 be=max(abs(float(a)-z) for a,z in zip(b['physical_state'],ref));fe=max(abs(float(a)-z) for a,z in zip(f['physical_state'],ref))
 records.append(dict(time=int(t),baseline_max_physical_error=be,refined_max_physical_error=fe,physical_error_reduction=be/fe,
  ode_reference_step_halving_difference=max(abs(a-z) for a,z in zip(other,ref)),baseline_direct_abel_error=b['direct_abel_error'],refined_direct_abel_error=f['direct_abel_error'],
  direct_error_reduction=float(b['direct_abel_error'])/float(f['direct_abel_error'])))
def invariant_residuals(data):
 residual=[]
 for rec in data['records']:
  a1,a2,a3,b1,b2,b3=map(mp.mpf,rec['physical_state'])
  residual.extend([abs(b1+b2+b3),abs(a1*a2*a3-6),abs(b1*b2+b1*b3+b2*b3-a1*a1-a2*a2-a3*a3+15),abs(-b1*b2*b3+a1*a1*b3+a2*a2*b1+a3*a3*b2-8)])
 return mp.nstr(max(residual),30)
out=dict(reconstructed_spectral_coefficient_max_residual=dict(baseline=invariant_residuals(base),refinement=invariant_residuals(fine)),scope='Noncertified end-to-end physical coordinate checks and precision refinement; original fixed curve and physical state throughout.',
 baseline=dict(qbits=256,epsbits=44),refinement=dict(qbits=288,epsbits=52),expected_perturbation_reduction=256,records=records)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
