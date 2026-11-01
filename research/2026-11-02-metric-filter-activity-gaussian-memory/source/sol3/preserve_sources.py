#!/usr/bin/env python3
"""Preserve the selective primary sources and exact source-bound review scope."""
from pathlib import Path
from urllib.request import urlopen
import hashlib,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
repo=Path('producer-workspace/repo')
a=repo/'research/2026-10-31-trajectory-warm-auxiliary-and-quantum-memory/source'
sel=[
('N1511 main',a/'dots-interacting/members/GRADED_SECTOR_FIRST_EVENT_RECEIVING.md','93731752d0d34c2fcfa1e7fb0b6812b88f90d301083d32ecd60525cee5b543c9','Complete source, including actual interfaces, scalar bridge, full first-event assembly and exclusions.'),
('N1511 whole review',a/'dots-interacting/members/GRADED_WHOLE_INDEPENDENT_REVIEW.md','38e6b2b67ed540ffa7b4679c51eb8b15ea85639e51d140b1e83597663f192820','Actual source-bound whole internal review PASS at constructive mathematical scope; accepted as received.'),
('N1511 uniform bound',a/'dots-interacting/members/UNIFORM_OCCUPATION_BOUND_CANDIDATE.md','136e1cf32b06eac6dbfba53f1e7c4a91783c607233779f2cf7ce55fa234509dd','Complete uniform normalized occupation argument; tilted-state warning retained.'),
('N1511 uniform review',a/'dots-interacting/members/UNIFORM_OCCUPATION_INDEPENDENT_REVIEW.md','0c00abbde78ca30c691761de0d7f6e204bfa03b2a19744d76b749dbfa676c573','Complete actual local review and its PASS/domain scope, binding source 136e1cf3. Its preserved bytes differ from the legacy receipt identifier a799f156 cited inside the older receiver; these are not conflated. The new metric theorem is independently derived here.'),
('Acquired scalar bridge',a/'dots-bosonic/members/THINNING_IMMIGRATION_DEATH_BRIDGE.md','beb4cfb5a5ae77b096d712d12c7ebdbce1ad2a73de16ffebd1fab65bd444a458','Complete source. Old header preserved; acquired through the actual whole N1511 receiving/review. Endpoint law, finite caps and stable arithmetic are reused, not claimed new.'),
('N1512 schedule',a/'dots-activity/members/NEAR_LINEAR_ACTIVITY_SCHEDULE_CANDIDATE.md','69e4c59079c426c0a047b21995c94f4afa420496c9df29011fd56c46324285bd','Complete final actual controlled-duration schedule and query-versus-gate qualification.'),
('N1512 review',a/'dots-activity/members/NEAR_LINEAR_SCHEDULE_INDEPENDENT_REVIEW.md','2bb21329fae284579e1fe60c700b609f0ab2e20e1019f8e82956a526a7ea72c6','Complete source-bound actual refinement review PASS; accepted at its unchanged common-loss scope.'),
('N1512 primary comparison',a/'dots-activity/members/PRIMARY_COMPARISON_AND_CONSEQUENCE.md','bf5147e9f7be36367b5e1cee0c02b648e6025e84e4f778d4dab6e60cd6b110e5','Complete comparison, dense acquired comparator, retained-memory limitations and unresolved high-order/history-aware alternatives.'),
('Linked N1516 input',repo/'research/2026-10-31-stable-experiments-pure-return-and-response/source/dots-pure-return/members/pure_return_source_20261031/PURE_RETURN_FULL_FINITE_BIT_RECEIVING.md','1a097458af52e4b89746b2f5e38e8ba4ea9f8a835db731daef39b8e9ea71e032','Inspected the exact Section 1 input, Section 2 identities and selected source assembly through Section 6, plus the linked arbitrary-input interface, only for exact-model comparison. No N1516 whole proof or coupled source is imported.')]
rows=[]
for label,src,want,scope in sel:
 data=src.read_bytes();got=hashlib.sha256(data).hexdigest();assert got==want,(src,got)
 dst=P/'sources/astra'/src.name;dst.parent.mkdir(exist_ok=True,parents=True);dst.write_bytes(data)
 rows.append({'label':label,'source_local':str(src),'preserved_local':str(dst),'sha256':got,'actual_read_and_use_scope':scope})
for ident,url,scope in [
 ('1205.3566v1','https://arxiv.org/html/1205.3566v1','Vladimirov-Petersen: CCR/Lure setup, Theorems 2-3 and characteristic risk-sensitive PDE. Prior exponential-Lyapunov methods credited; no priority claim.'),
 ('2112.08344v3','https://arxiv.org/html/2112.08344v3','Barthel-Zhang: quasi-free covariance and Liouvillian structure; the noncommuting driven joint system need not remain Gaussian.')]:
 dst=P/'sources'/f'{ident}.html'
 if not dst.exists():dst.write_bytes(urlopen(url,timeout=45).read())
 rows.append({'label':ident,'url':url,'preserved_local':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'actual_read_and_use_scope':scope})
(P/'source_receipts.json').write_text(json.dumps({'status':'Source provenance and accepted prior scope; not independent review or novelty validation of new stage-three science.','sources':rows,'packet_copies':[str(P/'sources/N1511.json'),str(P/'sources/N1512.json')],'preserved_prior_stage_receipts':str(P.parent/'stage2/source_receipts.json')},indent=2)+'\n')
# Verify the authored second-stage snapshot without modifying it.
f=Path('producer-workspace/astra-sol-round2-frozen-20261102')
checks=[]
for name in ['REPORT.md','COMPILER_PROOF.md','FINITE_BIT_DETAILS.md','PRIOR_COMPARISON.md','DILATION_FAILURE.md','README.md','source_receipts.json','loss_clock.py','generic_gaussian_checks.py','retained_process_check.py','reduction_comparator.py']:
 u=P.parent/'stage2'/name;v=f/name
 assert u.read_bytes()==v.read_bytes(),name
 checks.append({'file':str(u),'matches_frozen':True,'sha256':hashlib.sha256(u.read_bytes()).hexdigest()})
(P/'results/preserved_second_stage.json').write_text(json.dumps(checks,indent=2)+'\n')
print('11 selective primary/review sources preserved; 11 authored second-stage files match their frozen copies.')
