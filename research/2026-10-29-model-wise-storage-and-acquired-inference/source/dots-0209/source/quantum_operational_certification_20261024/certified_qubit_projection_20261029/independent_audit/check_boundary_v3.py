from pathlib import Path
from fractions import Fraction as F
import json,runpy,hashlib
P=Path(__file__).resolve().parents[1]
ns=runpy.run_path(str(Path(__file__).with_name('check_exact_v1.py')))
a=json.loads((P/'boundary_certificates_v3.json').read_text());assert len(a)==2
for c in a:assert ns['validate'](c)<=F(c['xi'])==F(1,10**12)
result={'status':'PASS_TWO_PREVIOUS_FAILURES','exact_gaps':[c['gap'] for c in a],'scope':'v3 candidate correction accepted; moderate-K Dykstra failure remains inherited from v2. No generic convergence claim. Float zero is not necessarily exact zero.','hashes':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['certified_projection_v3.py','boundary_certificates_v3.json','certified_projection_v2.py']}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print('v3 boundaries PASS')
