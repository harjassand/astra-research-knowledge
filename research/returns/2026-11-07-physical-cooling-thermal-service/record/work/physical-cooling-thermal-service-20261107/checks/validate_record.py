from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[3];b=root/'work/physical-cooling-thermal-service-20261107';out=root/'outputs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
prior=[]
for x in json.loads((b/'sources/INITIAL_SOURCE_PINS.json').read_text()):
 if 'original' in x:prior.append({'file':x['original'],'preserved':sha(root/x['original'])==x['sha256']==sha(b/'sources'/x['name'])})
expected={'initial/principal.md':'63131909bd94159166d364e9bcbd5c5480e4cf7eb99564878c04827920a5789e','initial/constructor.md':'12075ea25306425ae494831807d83ecddc739c8970d261bc4166810c2eade69d','initial/auditor.md':'2eb5a79c28069e3031c483d5655c835e5546de7e187ad695dcf292e9bdec02ca','machinery/initial/machinery.md':'832e5ad10fe9373e3a7547aa3c0956ffa3ebdd516d207a038cedf451a383ca35'}
initial=[{'file':f,'unchanged':sha(b/f)==h} for f,h in expected.items()]
p=out/'PHYSICAL_COOLING_THERMAL_SERVICE_RESEARCH_DOSSIER.md';links=[]
for t in re.findall(r'\]\(([^)]+)\)',p.read_text()):
 if '://' not in t and not t.startswith('#'):links.append({'target':t,'exists':(p.parent/t.split('#')[0]).exists()})
checks=[]
for f in sorted(b.rglob('*.json')):
 if 'sources' not in f.parts and ('check' in f.name.lower() or 'validation' in f.name.lower()):
  json.loads(f.read_text());checks.append({'file':str(f.relative_to(root)),'json_valid':True,'sha256':sha(f)})
assert all(x['preserved'] for x in prior)
assert all(x['unchanged'] for x in initial)
assert all(x['exists'] for x in links),links
r={'date':'2026-11-07','scope':'Artifact consistency and finite diagnostics; not mathematical proof, experiment or priority','dossier':{'sha256':sha(p),'bytes':p.stat().st_size,'words':len(p.read_text().split())},'prior_preservation':prior,'frozen_initials':initial,'local_links':links,'finite_check_records':checks}
review_paths=['challenges/FINAL_MATHEMATICAL_REVIEW.md','challenges/FINAL_CONSTRUCTION_REVIEW.md','machinery/challenges/FINAL_SOURCE_AND_NOVELTY_REVIEW.md']
r['reviews']=[{'file':f,'sha256':sha(b/f),'mentions_final_dossier_hash':r['dossier']['sha256'] in (b/f).read_text()} for f in review_paths]
assert all(x['mentions_final_dossier_hash'] for x in r['reviews'])
ledger=json.loads((out/'PHYSICAL_COOLING_THERMAL_SERVICE_THEOREM_LEDGER.json').read_text())
assert ledger['dossier_sha256']==r['dossier']['sha256']
r['ledger_claims']=len(ledger['claims'])
(out/'PHYSICAL_COOLING_THERMAL_SERVICE_VALIDATION.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'dossier':r['dossier'],'prior_files':len(prior),'initials':len(initial),'links':len(links),'finite_records':len(checks)},indent=2))
