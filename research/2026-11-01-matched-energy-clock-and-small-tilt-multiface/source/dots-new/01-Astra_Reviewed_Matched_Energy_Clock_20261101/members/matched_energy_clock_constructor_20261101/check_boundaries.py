"""Paid original-task refusals; not mocked scientific recomputation."""
from receive_matched_clock import *
import copy
original=json.loads(Path('matched_certificate.json').read_text());task=external_from_record(original);rows=[]
for name,raw,overrides in [('coarse_new_price',p.old.fixture(),{'Nt':128,'Ny':64}),('larger_actual_angular_coupling',p.old.fixture(512,F(200)),{})]:
 args=dict(task);args.update(overrides);start=time.perf_counter()
 try:
  c=certify(raw,**args);status='PASS';reason=None
 except Unknown as e:status='UNKNOWN';reason=str(e)
 assert status=='UNKNOWN',name
 rows.append({'name':name,'actual_raw_sha256':base.canonical_hash(raw),'task_overrides':overrides,'status':status,'reason':reason,'seconds':time.perf_counter()-start,'all_unmodified_task_values_from_certificate':True})
 Path('boundary_checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows[-1],flush=True)
