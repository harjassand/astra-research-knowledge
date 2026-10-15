#!/usr/bin/env python3
"""Read-only PR92 draft validation and inherited failure preservation audit."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-pr92-audit-20261015');O=Path(__file__).resolve().parent
sys.path.insert(0,str(R));s=importlib.util.spec_from_file_location('pr92_checkpoint_readonly',R/'state/publish_checkpoint.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
p=R/'updates/FT-foundational-capability-20261015/CHECKPOINT_RECORD.json';d=json.loads(p.read_text());m.validate_record(d,R)
passed=[];failed=[]
for f in sorted((R/'state/checkpoints').rglob('*.json')):
 try:m.validate_record(json.loads(f.read_text()),R);passed.append(str(f.relative_to(R)))
 except (ValueError,KeyError,TypeError) as e:
  relative=str(f.relative_to(R));raw=f.read_bytes();old=subprocess.check_output(['git','-C',str(R),'show','b7cada92d2eb304578be5ed974f1e44b10a89928:'+relative]);assert old==raw
  failed.append({'path':relative,'error':str(e),'sha256':hashlib.sha256(raw).hexdigest(),'base_bytes_unchanged':True})
assert len(passed)==165 and len(failed)==3 and all(x['error']=='unsupported checkpoint schema' for x in failed)
receipt={'schema':'astra.late-pr92-checkpoint-audit.v1','status':'PASS_SCOPED_DRAFT_AND_FAILURE_PRESERVATION','draft_path':str(p.relative_to(R)),'draft_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'draft_individual_validation':'PASS','draft_schema':d.get('schema'),'draft_evidence_refs':len(d['evidence_refs']),'draft_base_revision':d['base_revision'],'draft_branch_id':d['branch_id'],'draft_checkpoint_id':d['checkpoint_id'],'published_into_state_tree':(R/'state/checkpoints'/d['branch_id']/(d['checkpoint_id']+'.json')).exists(),'existing_checkpoint_records_validated':len(passed),'inherited_validation_failures':failed,'observed_global_validation':{'command':['python3','-B','state/publish_checkpoint.py','validate','--immutable-base','b7cada92d2eb304578be5ed974f1e44b10a89928'],'exit_code':1,'stderr':'ERROR: unsupported checkpoint schema\n','status':'FAIL_INHERITED_SCHEMA_PRESERVED'},'reporting_correction':'Initial ad-hoc individual validation completed but its reporter then incorrectly queried schema_version; it has been rechecked using actual schema field. No checkpoint or source byte was changed.','scope':'An individually valid unpublished draft and unchanged inherited global failures only; no shared state publication or scientific validation.'}
assert not receipt['published_into_state_tree'];(O/'CHECKPOINT_AUDIT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
