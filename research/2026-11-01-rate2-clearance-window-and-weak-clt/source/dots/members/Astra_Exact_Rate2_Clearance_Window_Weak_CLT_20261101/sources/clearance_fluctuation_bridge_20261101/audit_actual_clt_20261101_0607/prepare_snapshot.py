from pathlib import Path
import hashlib,json,shutil
here=Path(__file__).resolve().parent;root=here.parents[1];author=here.parent
entries=[]
def copy(p,category):
 data=p.read_bytes(); rel=str(p.relative_to(root)); out=here/'snapshot'/rel
 out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 entries.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'category':category})
assert hashlib.sha256((author/'AUTHOR_FREEZE.json').read_bytes()).hexdigest()=='fd48100bccba41d7df3cc777fe96a717f74746bf0c52354aec0cba8dda11a022'
copy(author/'AUTHOR_FREEZE.json','author_manifest')
for item in json.loads((author/'AUTHOR_FREEZE.json').read_text())['files']:
 p=author/item['path'];data=p.read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'];copy(p,'author_payload')
for item in json.loads((author/'SOURCE_BINDINGS.json').read_text())['files']:
 p=root/item['path'];data=p.read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'];copy(p,'author_dependency')
extras=[
'return_path_construction_20261101/rate2_paid_interior_removal_independent_review_20261101/REVIEW_RECEIPT.json',
'return_path_construction_20261101/rate2_paid_interior_removal_independent_review_20261101/INDEPENDENT_REVIEW.md',
'inverse_clearance_clock_20261101/SCALAR_FREEZE.json',
'inverse_clearance_clock_20261101/PROOF.md',
'inverse_clearance_clock_20261101/CERTIFICATE_FINE.json',
'audit_inverse_clock_certificate_20261101/RECEIPT.md',
'audit_inverse_clock_certificate_20261101/RECEIPT_BINDINGS.json',
'audit_inverse_clock_certificate_20261101/FINAL_VERIFICATION.json',
'inverse_clock_variance_20261101/VARIANCE_FREEZE.json',
'inverse_clock_variance_20261101/PROOF.md',
'inverse_clock_variance_20261101/VARIANCE_CERTIFICATE.json',
'audit_inverse_clock_variance_20261101/RECEIPT.md',
'audit_inverse_clock_variance_20261101/RECEIPT_BINDINGS.json',
'audit_inverse_clock_variance_20261101/FINAL_VERIFICATION.json']
for rel in extras:copy(root/rel,'separate_receipt_or_parameter')
(here/'SOURCE_READBACK.json').write_text(json.dumps({'status':'PASS','files':entries},indent=2)+'\n')
replay=here/'author_replay';replay.mkdir()
shutil.copy2(author/'check_tail_envelopes.py',replay/'check_tail_envelopes.py')
print(json.dumps({'snapshot_files':len(entries),'author_bindings':23,'separate_bindings':len(extras)},indent=2))
