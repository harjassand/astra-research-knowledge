from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import importlib.util,json,shutil,subprocess,sys,hashlib
H=Path(__file__).resolve().parent;S=H/'replay/retained_state_renewal_clock_20261101';spec=importlib.util.spec_from_file_location('c',S/'receive_clock.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);checks=0;details=[]
def ok(v,s):
 global checks
 assert v,s
 checks+=1;details.append(s)
old=json.loads((H/'independent_production_replays.json').read_text());new=json.loads((S/'results.json').read_text())
for a,b in zip(old,new):ok(a['name']==b['name'] and c.base.same(c.proof_record(a['certificate']),c.proof_record(b['certificate'])),'independent literal production matches regenerated author full proof record')
small=json.loads((H/'independent_small_certificate.json').read_text());task=c.external_from_record(small);scaled=c.certify(c.fixture(64,mobility=F(1,3)),**{**task,'beta':F(9)})
for key in ['global_spectral_error_upper','record_TV_error_upper','continuous_jitter_failure_upper','comparison_flip_probability','event']:
 ok(c.base.same(small[key],scaled[key]),'beta9 mu1/3 exact dimensionless equality '+key)
for key in ['physical_grid_spacing','physical_horizon','jump_time_tolerance']:ok(F(scaled[key])==9*F(small[key]),'beta/mobility exact physical time scaling '+key)
ok(F(scaled['reference_flip_rate'])*9==F(small['reference_flip_rate']),'beta/mobility exact inverse-rate scaling')
raw=c.fixture(128,mobility=F(64),diagonal=True);raw['energy_terms'][127]['coefficient']='1/7';raw['mobility_program']['entries'][-1]='32/11'
task2=dict(n=1,x=F(1),event_lower=0,event_upper=1,path_error=F(99,100),query_absolute_width=F(1),quad_relative=F(1,16),full_ratio=F(100),beta=F(2,3),kappa=F(7,3))
z=c.certify(raw,**task2);aq=z['mean_engine_certificate']['acquisition'];ok(aq['pure_coefficient_min']=='1/7' and aq['mobility_floor']=='32/11','nonfirst-axis minimum coercivity and mobility actually scanned')
ok(c.verify(raw,z,**task2)['status']=='PASS','nonunit beta/kappa irrational-root case actually received')
(H/'nonunit_case.json').write_text(json.dumps({'raw':raw,'task':z['task'],'certificate':z},indent=2)+'\n')
modules=['retained_state_renewal_clock_20261101/receive_clock.py','well_redistribution_mfpt_20261031/receive_mfpt.py','constant_spd_mfpt_20261031/receive_mfpt.py','autonomous_radial_mfpt_20261031/receive_mfpt.py','radial_kinetic_service_20261031/receive_kinetic.py']
for i,target in enumerate(modules[1:]):
 root=H/'dependency_tamper'/str(i)
 for name in modules:
  p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((H/'replay'/name).read_bytes())
 p=root/target;p.write_bytes(p.read_bytes()+b'\n# intentional isolated audit corruption\n')
 result=subprocess.run([sys.executable,'-c',"import importlib.util; s=importlib.util.spec_from_file_location('c',r'"+str(root/modules[0])+"');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)"],text=True,capture_output=True)
 (root/'stderr.txt').write_text(result.stderr);ok(result.returncode!=0 and 'hash mismatch' in result.stderr,'runtime inherited source hash refuses corrupted dependency '+target)
# Preserve actual malformed-tree v1 limitation. This is NOT counted as Unknown.
bad={};o=bad
for i in range(1100):o['deep']={};o=o['deep']
try:c.verify(c.fixture(64),bad,**task)
except RecursionError as e:(H/'v1_deep_tree_failure.json').write_text(json.dumps({'status':'UNCHECKED_DEPTH_API_LIMITATION','actual_exception':'RecursionError','depth':1100,'reason':str(e),'no_false_PASS':True},indent=2)+'\n')
else:raise AssertionError('expected v1 edge not reproduced')
report={'status':'PASS','checks':checks,'details':details,'nonunit_TV':float(F(z['record_TV_error_upper'])),'v1_deep_tree':'actual RecursionError preserved separately, not an UNKNOWN success'};(H/'additional_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
