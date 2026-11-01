from pathlib import Path
from fractions import Fraction as F
import sys,json,subprocess
root=Path(__file__).resolve().parent;p=root/'robust_well_kinetics_20261031';sys.path.insert(0,str(p))
import receive_robust as c
raw=json.loads((p/'small_raw_fixture.json').read_text());cert=json.loads((p/'small_certificate.json').read_text())
r=c.verify(raw,cert,defect=F(1,1000),quad_relative=F(1,20),full_ratio=F(2),ks_error=F(3,4),query_absolute_width=F(1),times=[F(0),F(1000),F(10000)])
s=subprocess.run([sys.executable,'-B','PREVIOUS_CAPABILITY_REPLAY.py'],cwd=root,capture_output=True,text=True,check=True);old=json.loads(s.stdout)
assert r['status']=='PASS'and old['unchanged_actual_model']['status']=='PASS'
print(json.dumps({'current_literal_uncertain_family_receiver':r['status'],'current_scope':r['scope'],'predecessor':old,'physical_membership':'not authenticated'},sort_keys=True))
