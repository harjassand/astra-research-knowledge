"""Isolated dependency tamper and API refusal-boundary checks."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util, json, shutil, sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'robustness_dilation_capacity_20261031'))
import receive_robustness as c
scratch=H/'dependency_tamper'
(scratch/'robustness_dilation_capacity_20261031').mkdir(parents=True,exist_ok=True)
(scratch/'dilation_partition_free_20261031').mkdir(exist_ok=True)
shutil.copyfile(H/'robustness_dilation_capacity_20261031/receive_robustness.py',scratch/'robustness_dilation_capacity_20261031/receive_robustness.py')
b=(H/'dilation_partition_free_20261031/receive_dilation.py').read_bytes()
(scratch/'dilation_partition_free_20261031/receive_dilation.py').write_bytes(b+b'\n# harmless-byte tampering must refuse before import\n')
spec=importlib.util.spec_from_file_location('tampered_receiver',scratch/'robustness_dilation_capacity_20261031/receive_robustness.py');m=importlib.util.module_from_spec(spec)
try:spec.loader.exec_module(m)
except RuntimeError as e:
 assert str(e)=='accepted dependency hash mismatch';tamper={'status':'REFUSED','exception':type(e).__name__,'reason':str(e)}
else:raise AssertionError('modified dependency admitted')
raw=c.fixture(1);rows=[]
for label,call in [('missing mandatory delta',lambda:c.certify(raw)),('unknown keyword',lambda:c.certify(raw,delta=F(1,500),unknown_keyword=True))]:
 try:call()
 except TypeError as e:rows.append({'case':label,'exception':'TypeError','reason':str(e),'scope':'Python API argument binding outside admitted callable signature; not Unknown and not false PASS'})
 else:raise AssertionError('wrong call accepted')
report={'status':'PASS','checks':3,'isolated_dependency_tamper':tamper,'api_signature_boundaries':rows,'note':'Only isolated scratch copies were changed. Frozen source and the clean replay tree are unmodified.'}
(H/'binding_boundary_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
