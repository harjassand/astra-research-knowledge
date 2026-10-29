"""Problem-to-premise evaluation at a committed source cut, not science audit."""
from pathlib import Path
import sys,json,hashlib,time
SRC=Path(__file__).resolve().parent;R=SRC.parents[2]
if len(sys.argv)!=2:raise SystemExit('usage: replay.py OUTPUT_DIRECTORY')
H=Path(sys.argv[1]);H.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R))
from knowledge.mcp_adapter import ResearchAdapter
a=ResearchAdapter(R,method='agent');cases=json.loads((SRC/'FROZEN_RESEARCH_USE_PROBLEMS.json').read_bytes())
def full(identifier):
 pages=[]
 while identifier:
  p=a.fetch(identifier);pages.append(p);identifier=p['metadata']['next_id']
 raw=''.join(p['text']for p in pages).encode();assert hashlib.sha256(raw).hexdigest()==pages[0]['metadata']['payload_sha256']
 return json.loads(raw),len(pages)
ids=[i for i in a.library.records if any(i.startswith(f'{k}{n}-')for n in range(1337,1348)for k in ['N','U'])]
ids+=[i for i in a.library.records if any(i.startswith(f'{k}{n}-')for n in [1296]for k in ['N','U'])]
budgets=[]
for ident in sorted(set(ids)):
 packet=a.library.packet([ident]);capsule,np=full(a.handle('current',ident))
 budgets.append(dict(id=ident,packet_bytes=len(json.dumps(packet,ensure_ascii=False).encode()),capsule_pages=np))
(H/'DEFAULT_PACKETS_AND_CAPSULES.json').write_text(json.dumps(dict(records=len(budgets),checks=budgets),indent=2)+'\n')
out=dict(scope=cases['scope'],revision=a.revision,input_version=a.version,cases=[],exposed_prior_context=cases['exposed_diagnostics'])
for c in cases['cases']:
 row=dict(c,methods={})
 for method in ['lexical','content','structured']:
  t=time.monotonic();hits=a.library.search(c['query'],method=method,limit=5)['results'];found=[x['id']for x in hits]
  row['methods'][method]=dict(ids=found,first_expected_rank=next((i+1 for i,k in enumerate(found)if any(k.startswith(e)for e in c['expected'])),None),seconds_observed=round(time.monotonic()-t,3))
 t=time.monotonic();s=a.search(c['query']);hits=s['results'][:5];found=[x['metadata']['record_id']for x in hits]
 row['methods']['agent']=dict(ids=found,first_expected_rank=next((i+1 for i,k in enumerate(found)if any(k.startswith(e)for e in c['expected'])),None),seconds_observed=round(time.monotonic()-t,3),method=s['metadata']['method'],fallback=s['metadata']['fallback'])
 assert s['metadata']['method']=='agent'and s['metadata']['fallback']is None
 target=c.get('target');rank=row['methods']['agent']['first_expected_rank']
 if target and rank:
  p,np=full(hits[rank-1]['id']);route=[p['id']]
  if p['id']!=target and p.get('parents'):p,np=full(a.handle('current',p['parents'][0]));route.append(p['id'])
  if p['id']!=target:
   direct=next((x for x in p.get('related_units',[])if x['id']==target),None)
   if direct:p,np=full(direct['fetch_id']);route.append(p['id'])
   else:
    # Actual correction card IDs are navigation, never a scientific transfer.
    for notice in p.get('notices',[]):
     n=notice.get('notice',notice)
     for card in n.get('card_ids',[]):
      parent,npp=full(a.handle('current',a.library.resolve(card)['id']))
      direct=next((x for x in parent.get('related_units',[])if x['id']==target),None)
      if direct:p,np=full(direct['fetch_id']);route.extend([parent['id'],p['id']]);break
     if p['id']==target:break
  sources=[]
  if p['id']==target:
   for ref in p['evidence']:
    src,ns=full(ref['fetch_id']);sources.append(dict(source=src['source'],text=src['text'],pages=ns))
  row['usable_premise']=dict(id=p['id'],exact_unit_reached=p['id']==target,route=route,statement=p['statement'],contract=p['contract'],notices=p['notices'],review_overlays=p.get('review_overlays',[]),sources=sources,pages=np)
 else:
  packets=[]
  for hit in hits[:3]:
   p,np=full(hit['id']);packets.append(dict(id=p['id'],statement=p['statement'],contract=p['contract'],notices=p['notices'],pages=np))
  row['unsupported_or_missed_use_inspection']=dict(scope='Scope inspection is not proof of whole-corpus absence. Search candidates do not certify the requested device, output contract, performance or composition.',packets=packets)
 out['cases'].append(row);(H/'FRESH_RESEARCH_USE_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(c['id'],{m:x['first_expected_rank']for m,x in row['methods'].items()},flush=True)
positive=[x for x in out['cases']if x['kind']=='positive']
out['summary']=dict(positive_denominator=len(positive),top5={m:sum(x['methods'][m]['first_expected_rank']is not None for x in positive)for m in ['lexical','content','structured','agent']},actual_unit_to_source_routes=sum(x.get('usable_premise',{}).get('exact_unit_reached',False)for x in positive),remaining_agent_misses=[x['id']for x in positive if x['methods']['agent']['first_expected_rank']is None],nonpositive_case_kinds=[x['kind']for x in out['cases']if x['kind']!='positive'],coverage='Closing received2040/2041cut: local transport and measurement suppliers, constrained mobility, conditional free-energy counting, raw-field chart obstructions, repaired periodic Toda, ideal correlated clock stalls, unreviewed recovery proposal and open noisy-data architecture. Eligible mechanism denominatorUNKNOWN; broad field or global superiority unmeasured.')
(H/'FRESH_RESEARCH_USE_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out['summary']),flush=True)

# Exposed regressions from the supplied audit; never counted as fresh problems.
exposed=[]
for query,target in [
 ('Compare quantum measurements by relative entropy for every pair of input states and any untouched auxiliary quantum system.','U675-complete-order-and-reference-cutoff'),
 ('ordered-word inverse-Jordan compiler','U675-ordered-word-compiler')]:
 response=a.library.search(query,method='agent',limit=5)
 row=dict(query=query,target=target,initial_ids=[x['id']for x in response['results']],source_routes=[])
 if any(x['id'].startswith(('N675-','U675-'))for x in response['results']):
  packet,np=full(a.handle('current',target));row['packet']=packet
  for ref in packet['evidence']:
   source,nsp=full(ref['fetch_id']);row['source_routes'].append(source)
 exposed.append(row)
unsupported=[]
for left,right in [
 ('U1330-positive-prefix-empirical-teacher-with-absorbing-support-escape','U1334-one-joint-program-to-consistent-controlled-reflections'),
 ('U1332-affine-gram-and-reference-balance-information-window','U1335-invariant-heldout-property-not-old-frame-decoder')]:
 b=a.library.bridge(left,right);assert b['state']=='NO SUPPORTED CONNECTION';unsupported.append(b)
inspection=a.library.search('a reverse information factor for supplied quantum preparations',method='agent',limit=5,
 object_text='classical labels mapped to supplied finite density matrices',operation='qualify a universal information-retention guarantee',
 available=['estimated state matrices with a confidence interval'],unavailable=['exact supports and kernel projectors'])
assert all(x['premise_check']['compatibility']=='NOT ESTABLISHED'for x in inspection['results'])
(H/'INTERFACE_AND_ASSUMPTION_RESULTS.json').write_text(json.dumps(dict(input_version=a.version,unsupported_connections=unsupported,premise_inspection=inspection,exposed_audit_regressions=exposed,
 scope='No scientific reproof or producer execution. Exposed queries remain exposed. Shared vocabulary and semantic conditions do not establish an interface or discharge a premise.'),ensure_ascii=False,indent=2)+'\n')
print('Exposed audit, unsupported-transfer and supplied-premise inspection retained.',flush=True)

# The prior miss motivated a general outlink projection, not query/score tuning.
prior=json.loads((SRC/'EXPOSED_CAUSAL_PRIOR_CASE.json').read_bytes())
response=a.search(prior['query']);target=prior['target'];routes=[];direct=[]
for hit in response['results'][:5]:
 if hit['metadata']['record_id']==target:direct.append(hit['id'])
 for route in hit['metadata'].get('current_scope_navigation',{}).get('routes',[]):
  if route['id']!=target:continue
  capsule,np=full(route['fetch_id']);assert capsule['content_version']==route['content_version']
  sources=[]
  for ref in capsule['evidence']:
   src,nsp=full(ref['fetch_id']);sources.append(src)
  routes.append(dict(candidate=hit['metadata']['record_id'],route=route,target_capsule=capsule,capsule_pages=np,sources=sources))
(H/'EXPOSED_CAUSAL_CURRENT_SCOPE_NAVIGATION.json').write_text(json.dumps(dict(query=prior['query'],target=target,revision=a.revision,input_version=a.version,first_menu_ids=[x['metadata']['record_id']for x in response['results'][:5]],direct_target_hits=direct,explicit_routes=routes,metadata_ablation=dict(scope='Remove only current_scope_navigation from this same observed menu; IDs, ranking, scores, source candidates and text stay identical. This is a projection ablation, not a new scientific or independent ranking baseline.',direct_current_scope_routes=0),scope='P01is exposed prior context. The generic helper exposes only already authored supported notice targets and exact current content versions; no query aliases, weights, model or ranking change. A navigation route is not a compatible transfer or inherited acceptance.'),ensure_ascii=False,indent=2)+'\n')
print('Exposed P01direct hits',len(direct),'explicit current-scope routes',len(routes),flush=True)
