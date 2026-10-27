from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path('morrey_law_first_stress_20261026/cube_brownian_completion');O=P/'fully_corrective141_half_K48';r=json.loads((O/'ACTUAL_CORRECTIVE_ROOT.json').read_text());p=json.loads((O/'actual_primal_endpoint_proxy_receipt.json').read_text());ns=list(map(int,r['root_probability_numerators']));assert len(ns)==141 and sum(ns)==2**80 and sum(n>0 for n in ns)==30;assert sum(F(c['root_probability']) for c in r['components'])==1
for c in r['components']:
 assert F(c['root_probability'])==F(ns[c['catalog_index']],2**80);l=c['label'];path=Path(l['actual_received_law_identity_path']) if 'actual_received_law_identity_path' in l else Path('morrey_global_w1_receiver_20261025/intrinsic')/l.get('actual_policy',l.get('actual_indexed_law_manifest'));assert hashlib.sha256(path.read_bytes()).hexdigest()==l['sha256']
 if 'actual_witness_receipt' in l:assert hashlib.sha256(Path(l['actual_witness_receipt']).read_bytes()).hexdigest()==l['actual_witness_sha256']
assert F(p['actual_to_exact_proxy_W1_upper'])==sum(F(c['root_probability'])*F(c['actual_proxy_W1_upper']) for c in r['components']);out={'status':'INDEPENDENT_ROOT_PROXY_ARITHMETIC_PASS','root_count':30,'denominator':str(2**80),'orbit_rows':p['points'],'W1':p['actual_to_exact_proxy_W1_upper'],'nonmutating_replay':True,'scope':'Exact root and proxy only; full field not yet received'};(O/'independent_root_proxy_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',float(F(out['W1'])))
