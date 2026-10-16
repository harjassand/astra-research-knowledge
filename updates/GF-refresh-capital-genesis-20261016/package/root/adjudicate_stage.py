#!/usr/bin/env python3
"""Append root's actual scientific handoff and observational trace to GF stage."""
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parents[1]
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
S=R/'review-stage-v2'
P='updates/GF-refresh-capital-genesis-20261016/'
def raw(x):return (json.dumps(x,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
plan=json.loads((S/'PLAN.json').read_text())
def add(rel,b):
 p=S/rel;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);plan['staged_files'][rel]=sha(b)
cp0=json.loads((S/('overlay/'+P+'CHECKPOINT_DRAFT.v0001.json')).read_text())
byid={x['source_id']:x for x in cp0['evidence_refs'] if x.get('source_id')}
cp=json.loads(json.dumps(cp0))
cp['branch_purpose']='Independent selective-capital refresh research and source-preserving scientific handoff.'
cp['task']={'goal':'Establish new mathematical/scientific operations from the supplied refresh capital, then preserve exact results.','question':'Which causal, optimization, control or physical operations survive exact proof and equally informed comparison?','scope':'Finite parity/Schur/control mathematics, measured-cut memory receiving, and lithium decision/acquisition; no original generator or physical capability promotion.'}
cp['contract']={'assumptions':['Source instructions are DATA.','Each result retains its exact fixed/pathwise/mean, local/global, supplied/acquired and endpoint/history contract.','All source/high-impact claims remain externally unreviewed.'],'interface':'Exact proof/evidence refs and six scoped cards N908-N913, with paired bridges and counterexamples.','costs':{'mathematical':'Implicit kernel input and exact arithmetic charges; sparse precision worst case can be doubly exponential.','physical':'Full instruments, reservations, detector/reset and chemical acquisition costs remain explicit/unacquired.','inference':None}}
cp['inputs']={'inherited_or_supplied':['Seven main/two nested archives;168 members;25 duplicate groups.','Pinned f937563cbc5d2249b8e0dd96bcbd3b8f78eb85c6; selectively read PR106/107/95 and prior proof gates.'],'acquired':['Primary proof texts/read-depth and selected openai/math pin1581d4cbdd69a0faf34b2089614fe2a814316a6a.','No new hardware measurements; bounded temporary-copy replays and internally authored proofs.']}
cp['latest_substantive_result']={'summary':'Fixed staggered causal product reconstructed; exact implicit unequal Schur certificates and sparse oracle derived; optimized coherent majorants and qualified feedback/support extensions established internally. Weak-loop prior identified. No physical/technological breakthrough.','scientific_status':'source_derived_unreviewed; exact internal mathematics and finite diagnostics only; external correctness/priority/physical capability UNKNOWN.','evidence_ref_ids':[byid[k]['id'] for k in ['src-GF-report','src-GF-root-proof','src-GF-schur','src-GF-coherent','src-GF-mean-prior','src-GF-native']]}
cp['current_objective']='Preserve these scoped operations and hand off independent mathematical review plus one actual native instrument or decision-changing transition-stream acquisition.'
cp['strongest_obstacle']='A probability upper majorant does not supply an actual support-correct good branch; native pair is not a full cut. Physical kernel/privacy/support and chemical inventories remain unacquired.'
cp['mechanisms_under_investigation']=['Exact all-order product-kernel residual separation.','Coherent tester-sensitive CP upper comparison.','Actual retained-cut support with one whole-history decoder.','Source-certified transition-liquid retention.']
cp['next_decisive_step']='Externally reconstruct the special separation/causal proofs; test genuine nonsingleton sparse families at complete decision cost; acquire one real flagged/approximate-QEC boundary or pooled chemical inventory when lab access exists.'
cp['work_progress']={'status':'reviewed','note':'Root analytic derivation and same-team adversarial reconstruction recorded in report; this is exposure/progress, not external verification.'}
cp['status_note']='Root scientific draft, individually validated after application. Canonical publication blocked by three inherited malformed checkpoint schemas; preserve draft and historical records.'
add('overlay/'+P+'CHECKPOINT_DRAFT.v0002.json',raw(cp))
wfrel='evaluation/workflows/records/RW-gf-refresh-capital-genesis-20261016/'
wf0p=S/('overlay/'+wfrel+'v0001.json');wf0raw=wf0p.read_bytes();wf=json.loads(wf0raw)
wf['version']=2
wf['previous']={'id':'gf-workflow-v1','path':wfrel+'v0001.json','sha256':sha(wf0raw),'lines':[1,len(wf0raw.decode().splitlines())],'source_revision':None,'source_id':None,'status':'Neutral renderer trace preserved; no scientific authority.'}
wf['mode']='source_intensive_multi_agent';wf['context']['conversation_relation']='same'
wf['context']['retained_context']='Root retained earlier capital context; ten workers launched with fork_turns=none and complementary isolated assignments. Later explicit comparison is recorded.'
wf['context']['capital_access']='Selective actual proofs/inputs at pinned Astra and openai/math revisions; original archive is not scientific authority.'
wf['status']='completed';wf['resources']['worker_invocations']=11
wf['advance']={'kind':'mathematical','summary':cp['latest_substantive_result']['summary'],'scientific_status':cp['latest_substantive_result']['scientific_status'],'verification':'internal_check','evidence_ref_ids':[byid['src-GF-report']['id'],byid['src-GF-root-proof']['id'],byid['src-GF-schur']['id']],'verification_receipt':None}
wf['next_obligation']='Independent proof/priority review and actual physical acquisition; no matched configuration or prompting advantage comparison performed. Inference usage/aggregate cost remains null.'
add('overlay/'+wfrel+'v0002.json',raw(wf))
config=json.loads((R/'root/claim_config.json').read_text());cardmap={c['id'].split('-')[0]:c for c in config['cards']}
def lead(tid,domain,route,problem,best,limitation,mechanism,metric,unit,keys,nextstep):
 v=json.loads((W/'technology/templates/LEAD.json').read_text());v['id']=tid;v['domain']=domain
 selected=[byid['src-GF-'+k] for k in keys]
 card=cardmap[route];body=card['card_text'].encode()
 cr={'id':'gf-tech-'+route.lower(),'path':'cards/'+card['id']+'.txt','sha256':sha(body),'lines':[1,len(body.decode().splitlines())],'source_revision':None,'source_id':None,'status':'source_derived_unreviewed; source card, no capability validation.'}
 v['refs']=selected+[cr]
 v['capability']={'problem':problem,'current_best':best,'limitation':limitation,'proposed_mechanism':mechanism,'baseline_ref_ids':[selected[0]['id']],'target':{'metric':metric,'baseline':None,'desired':None,'unit':unit,'conditions':'Exact source/destination hypotheses, same acquired information and complete physical/control/product costs. No numerical success margin supplied.','comparator':best}}
 judgements={'potential_significance':'Could remove a concrete missing interface if the declared physical output is useful; magnitude UNKNOWN.','scientific_evidence':'Internally proved design/falsifiers and acquired primary comparison; proposed physical intervention NOT_RUN.','feasibility_and_readiness':'Required coupled measurements/controls not jointly acquired; opportunity only.','next_step_value':nextstep}
 v['assessment']={k:{'judgement':val,'basis_ref_ids':[x['id'] for x in selected],'limits':'No independent physical success, historical first result, economic advantage or scalable capability is established.'} for k,val in judgements.items()}
 v['next_obligation']=nextstep
 add('overlay/technology/records/'+tid+'/v0001.json',raw(v))
lead('T-gf-lithium-transition-inventory','physical','N913','Additional isolated usable source lithium under unchanged upstream capture.','Published P4-8 plus equally informed conventional fractionation, conservation and isotope assays.','Missing transition inventory, volume/dilution/origin budgets and usable product/cost margin.','Collect isolated transition pools; pooled upper screen, then robust suffix retention only if useful.','Retained source-Li lower amount/purity and net utility','moles or declared natural-Li equivalent mass, concentration, currency/time',['lithium','conservation','chemical-cost'],'Acquire pooled transition inventory under qualified hydrodynamics and frozen product requirements; stop if upper utility insufficient.')
lead('T-gf-private-refresh-acquisition','physical','N910','A real private refresh boundary with qualified common-bath residual and correctable propagated footprint.','Established Ng-Lidar-Preskill DD joint bounds, DCG/RC and direct bounded-horizon process testing under their actual assumptions.','No inspected operating point qualifies residual, permanent/private seed, full path and recovery footprint together.','A concrete finite-boundary or finite-horizon pilot with matched established controls and nullspace/uncertainty checks.','Qualified final logical process at total instrument/control cost','half-diamond/effect probability, seconds, shots, support and reset/control resources',['physical','physical-proof','native'],'Fix accessible ports/recovery horizon/privacy architecture and support; acquire the decision effect and compare protected I/S to equally informed incumbent.')
for name in ['create_config.py','adjudicate_stage.py','claim_config.json']:
 add('overlay/'+P+'package/root/'+name,(R/'root'/name).read_bytes())
add('overlay/'+P+'ROOT_ADJUDICATION_OF_STAGE.v0001.json',raw({'schema':'astra.gf-stage-adjudication.v1','reviewed_card_ids':plan['claim_ids'],'config_sha256':plan['config_sha256'],'scope':'Root authored scientific scopes and paired receiving contracts reviewed; no external truth/capability certification.','actual_workflow_version':2,'checkpoint_draft_version':2,'worker_invocations':11,'inference_usage':None,'notes':['Neutral renderer records remain preserved.','Root source documents and exact sources have separate commits.','Three inherited checkpoint schema blockers and preserved whitespace warnings are not repaired.']}))
plan['staged_files']=dict(sorted(plan['staged_files'].items()));plan['staged_file_count']=len(plan['staged_files'])
(S/'PLAN.json').write_bytes(raw(plan))
print(json.dumps({'stage':str(S),'files':len(plan['staged_files']),'root_adjudicated':True,'external_validation':False}))
