from pathlib import Path
import json,hashlib
r=Path('producer-workspace/quartic_value_polynomial_20261029');a=Path(__file__).parent
assert 'ordinary24-start' not in (r/'README.md').read_text()
files={}
for n,h in json.loads((r/'AUTHOR_FREEZE.json').read_text()).items():
 p=r/n;assert hashlib.sha256(p.read_bytes()).hexdigest()==h,n;files[str(p)]=h
for p in [r/'AUTHOR_FREEZE.json',a/'INDEPENDENT_REVIEW.md',a/'check_value_certificate.py',a/'value_checks.json',a/'provenance_checks.json',a/'replay/direct_identity.json',a/'replay/deterministic_exact_verification.json',Path('producer-workspace/REVIEW_RECEIPT.json')]:files[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
receipt={'date':'2026-10-29','status':'accepted_exact_one_instance_normalized_value_polynomial_and_global_certificate','reviewer':'producer-workspace/derive_matching_survival_bound','proofs':['exact GMP homogeneous quotient identity','443 good-prime deterministic height uniqueness'],'checks':['all28 real roots','exact unit candidate and original objective bound','accepted source provenance'],'exclusions':['generic implementation or practical runtime','cold-start benchmark','hardware or unknown-noise advantage'],'files':files}
(a/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(hashlib.sha256((a/'REVIEW_RECEIPT.json').read_bytes()).hexdigest())
