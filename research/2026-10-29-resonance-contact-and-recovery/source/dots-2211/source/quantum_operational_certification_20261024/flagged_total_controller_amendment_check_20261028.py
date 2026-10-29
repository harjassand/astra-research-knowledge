from pathlib import Path
import json,hashlib,importlib.util
D=Path(__file__).parent
# Independently reconstructed simulator, run without its output-writing tail.
ind={'__file__':str(D/'flagged_five_qubit_independent_check_20261028.py')};f=D/'flagged_five_qubit_independent_check_20261028.py';exec(compile(f.read_text().split("author=D/")[0],str(f),'exec'),ind)
sp=importlib.util.spec_from_file_location('completed',D/'flagged_five_qubit_storage_check_20261028.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
from itertools import product
missing=0;branches=1
for k in range(4):
 for sy in product((0,1),repeat=4):
  if sy not in a.FLAGCOR[k]:missing+=1
  for sb,fb in [(0,1),(1,0),(1,1)]:
   cor=a.FLAGCOR[k].get(sy,a.W1COR[sy]) if fb else a.W1COR[sy]
   assert cor is not None and a.weight(cor)<=3;branches+=1
assert missing==32 and branches==193
saved=json.loads((D/'flagged_controller_precompletion_20261028/flagged_five_qubit_storage_check_20261028.json').read_text())
current=json.loads((D/'flagged_five_qubit_storage_check_20261028.json').read_text())
assert saved['all_fault_results']==current['all_fault_results']
assert saved['fault_free_input_tests']==current['fault_free_input_tests']
for e in a.W1:assert a.canon(a.run(e)[0])==0
_,_,faults,_=a.run()
for fault in faults:
 out,rec,tr,n=a.run(fault=fault);assert a.canon(out) in a.CORRECTABLE
assert len(faults)==len(ind['results'])==1528
files=['flagged_five_qubit_storage_check_20261028.py','flagged_five_qubit_storage_check_20261028.json','flagged_five_qubit_storage_round_20261028.md',Path(__file__).name]
out={'status':'PASS_TOTAL_CONTROLLER_COMPLETION','all_syntactic_terminal_records':193,'previously_missing_flag_syndrome_pairs':32,'unchanged_clean_single_fault_cases':1528,'unchanged_faultfree_input_cases':16,'potential_locations':751,'TP_scope':'Every measurement record receives a unitary correction or identity; bounded complete local instruments imply CPTP. No extra robustness inferred.','sha256':{f:hashlib.sha256((D/f).read_bytes()).hexdigest() for f in files}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
