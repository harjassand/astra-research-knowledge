"""Freeze authored source metadata and integrity receipts, not scientific truth."""
from pathlib import Path
import datetime, hashlib, json, subprocess

B=Path(__file__).resolve().parent
R=B.parents[1]
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
PIN='9dbe934e5475f415c2d160a6c0715534aafa546b'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()

def info(path):
 data=path.read_bytes()
 return {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'lines':data.count(b'\n')}

source_inputs=[
 ('originals/stability/PROOF_NOTE.md','complete analytic note'),
 ('originals/stability/certificate.json','data format/context; no producer execution'),
 ('originals/shared_bath/pr104_bath_audit/PEAK_RATE_CERTIFICATE_ADDENDUM.md','complete analytic proof'),
 ('originals/kinetic/schlogl_first_slab_packet/README.md','complete scope and certificate table'),
 ('originals/kinetic/schlogl_first_slab_packet/references/incumbent/AUDIT.md','complete primary-incumbent audit'),
 ('originals/kinetic/schlogl_first_slab_packet/verification/REPORT.md','decisive residual/localization/goal limits, substantial report; no verifier replay'),
 ('originals/catalysis/REPORT.md','complete received causal/recovery/source-reconciliation report'),
 ('originals/catalysis/EQUAL_DUTY_TEST.md','complete received equal-duty test note'),
]
input_receipts=[]
for p,depth in source_inputs:
 x=info(R/p);x['reading_depth']=depth;input_receipts.append(x)
for p in sorted((R/'originals').glob('*.zip')):
 x=info(p);x['reading_depth']='archive bytes hashed; extracted supplied documents read separately';input_receipts.append(x)
(B/'receipts'/'INPUT_HASH_RECEIPT.json').write_text(json.dumps(input_receipts,indent=2)+'\n')

capital=[
 ('AGENTS.md','complete'),('00_START_HERE.txt','complete'),
 ('frontier/dossiers/N888.txt','scope, notices, gates and exact proof pointers'),
 ('frontier/dossiers/N890.txt','scope, notices, gates and exact proof pointers'),
 ('frontier/dossiers/N893.txt','complete dossier'),
 ('frontier/dossiers/N887.txt','scope and exact proof pointers; received independent catalysis proof read separately'),
 ('frontier/dossiers/N880.txt','task-relevant context and gate definitions'),
 ('updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_parametric_stress_genesis/ALL_R_THEOREM_PROOF.txt','lines 1-129: exact residual, rational certificate logic, stress pairing, all-r separated theorem'),
 ('updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_sharp_invention/MIXED_SOURCE_CONTINUATION.md','complete'),
 ('updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_primary_math_prior/REPORT.md','complete comparison report, used as navigation not external proof substitute'),
 ('updates/GA-conformal-causal-genesis-20261016/package/derived/workers/ga_primary_math_prior/SEPARATED_SUBCLASS_PRIOR_ADDENDUM.md','complete'),
 ('updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_finite_rate_genesis/COST_AND_INCUMBENT.md','complete'),
 ('updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_finite_rate_genesis/SHARP_POISSON_SYNDROME_THEOREM.md','lines 1-115: assumptions, latent dilation, selected-event proof, kernel averaging'),
 ('updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_kinetic_genesis/PROOFS.txt','lines 1-160: exact model, quotient comparison, finite-deadline argument'),
 ('updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_primary_prior/REPORT.md','complete comparison context'),
]
capital_receipts=[]
for p,depth in capital:
 x=info(W/p);x.update(revision=PIN,relative_path=p,reading_depth=depth);capital_receipts.append(x)
(B/'receipts'/'CAPITAL_READ_RECEIPT.json').write_text(json.dumps(capital_receipts,indent=2)+'\n')

primary=[
 {'id':'OW2013','url':'https://web.mit.edu/wangj/www/pap/ObizhaevaWang13.pdf','local':'obizhaeva_wang_2013.pdf','type':'author-hosted final journal PDF','reading_depth':'Proposition 3/Eq31 and Appendix A3-A7; complete verification argument A15-A26. Rendered/viewed PDF pages 28-30; statement also inspected.','supports':'older exact unconstrained exponential optimizer; no lower-density constrained theorem imported'},
 {'id':'AS2013v4','url':'https://arxiv.org/pdf/1201.2756v4','local':'alfonsi_schied_v4.pdf','type':'primary author preprint v4','reading_depth':'Eq2, Lemma1, Theorem2, Example1, full Lemma7 proof Eq54-59; relevant pages rendered/viewed 7,19,20. Full later Volterra derivation not audited.','supports':'capacitary measure energy convention and complete-square verification mechanism'},
 {'id':'HKL2019v2','url':'https://arxiv.org/pdf/1708.07849v2','local':'harris_kirchheim_lin_v2.pdf','type':'primary author preprint v2','reading_depth':'Theorem2.4 and complete three-part proof PDF pages3-5, with rendered statement and conclusion pages3/5 viewed; appendix not newly fully audited.','supports':'exact triangular-support hypothesis; qualitative one-profile comparison'},
 {'id':'VS2017','url':'https://www.researchgate.net/publication/318233496_An_adaptive_solution_to_the_chemical_master_equation_using_tensors','type':'author-uploaded primary full text, read via web extraction','reading_depth':'Eqs21-30 and their recurrence/propagated residual proof; web extraction lines2181-2446 explicitly inspected','byte_download_status':'403; no local full text claimed','supports':'full physical l1 recurrence residual bound, distinct from FSP leakage/reduced solver norm'},
 {'id':'BBW2020v2','url':'https://arxiv.org/pdf/1910.12562v2','local':'backenkohler_bortolussi_wolf_v2.pdf','type':'primary author preprint v2','reading_depth':'Sections4-5.5 complete martingale, occupation/exit, objective, moment constraints; numerical-accuracy limitation inspected. Eq18 PDFpage10 and Eq23 PDFpage13 visually checked.','supports':'direct reachability/first-hit output bounds as primary precedent','source_correction':'Eq23 terminal y2 sign conflicts with Eq18; correct m=k=0 equation y10+y20=1'},
 {'id':'OAI082','url':'https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/An-L3-bound-for-the-dyadic-triangular-Hilbert-form-October-5-2026/build/sections','locals':['openai_082_02-matrix.tex','openai_082_03-trace.tex'],'type':'pinned primary source files','reading_depth':'both complete files and proof chain: supported Hessian/order/midpoint and mixed trace inequality','supports':'possible cancellation-preserving Gram mechanism only; no receiving representation constructed; no theorem transfer or Lean replay'},
]
for x in primary:
 if 'local' in x:x['acquired_file']=info(B/'acquired_excluded_from_publication'/x['local'])
 if 'locals' in x:x['acquired_files']=[info(B/'acquired_excluded_from_publication'/p) for p in x['locals']]

sources={
 'schema':'gc-primary-prior-sources-v1','frozen_utc':now,
 'capital_pin':PIN,'openai_math_pin':'1581d4cbdd69a0faf34b2089614fe2a814316a6a',
 'pr95_head':'b83009076c11422c1777cfa8049f6bb12cf1e47e',
 'primary_sources':primary,
 'receipts':['receipts/INPUT_HASH_RECEIPT.json','receipts/CAPITAL_READ_RECEIPT.json','receipts/PR95_OBJECT_RECEIPT.json','receipts/PR95_CHANGED_PATHS.json','receipts/ACQUISITION_INITIAL.json','receipts/ACQUISITION_ADDITIONAL.json','receipts/ACQUISITION_GOAL.json','receipts/ACQUISITION_OPENAI_SELECTED.json'],
 'failed_acquisition_scope':{
  'jahnke_initial':'HTTP404, no full text admitted',
  'jahnke_alternate':'HTML redirect saved; relabeled acquired_excluded_from_publication/jahnke_reduced_2011_alt.failed_html',
  'kaust_tau_leap':'HTML response, not PDF; relabeled acquired_excluded_from_publication/mora_tempone_vilanova_2016.failed_html; no proof premise',
  'vo_sidje':'byte acquisition403; primary full text read through web tool',
  'holtorf_barton':'publisher HTML acquired as lead, not admitted as a read proof premise'
 },
 'memory_use':'PR95 navigation only; status and actual scientific objects freshly verified',
 'publication_rule':'Do not publish acquired_excluded_from_publication. Author report/source metadata/receipts and independently authored acquisition/interface scripts only. No author program executed.',
 'limits':['bounded primary proof comparison, no historical absence conclusion','no external review or formal replay','no target-specific successful state/output certificate','no hardware validation or advantage'],
}
(B/'SOURCES.json').write_text(json.dumps(sources,indent=2)+'\n')

snap={'utc':now,'capital_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=W).decode().strip(),'capital_status_short':subprocess.check_output(['git','status','--short'],cwd=W).decode(),'method':'read-only status snapshot; worker wrote only its report directory'}
(B/'receipts'/'CHECKOUT_SNAPSHOT.json').write_text(json.dumps(snap,indent=2)+'\n')
assert snap['capital_head']==PIN

authored=[]
for p in sorted(B.rglob('*')):
 if p.is_file() and 'acquired_excluded_from_publication' not in p.parts and p.name not in {'PUBLIC_AUTHORED_MANIFEST.json','FROZEN.json'}:
  x=info(p);x['path']=str(p.relative_to(B));authored.append(x)
manifest={'scope':'authored files only; hashes certify integrity, not scientific correctness','utc':now,'files':authored,'excluded':'acquired_excluded_from_publication/**'}
(B/'PUBLIC_AUTHORED_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
frozen={'status':'FROZEN_SCOPE_COMPARISON','utc':now,'capital_pin':PIN,'report_sha256':info(B/'REPORT.md')['sha256'],'sources_sha256':info(B/'SOURCES.json')['sha256'],'authored_manifest_sha256':info(B/'PUBLIC_AUTHORED_MANIFEST.json')['sha256'],'input_and_checkout_edits':False,'acquired_code_executed':False,'external_messages':False,'state_solve_or_experiment':False,'historical_priority':'UNKNOWN','target_probability':'NOT_ESTABLISHED','primary_conclusions':['uncapped exponential optimizer is exact prior mathematics','lower-density active-cap specialization has UNKNOWN precise priority','tube is local uniform-in-sI,g continuity consequence of strict separated reserve','direct goal-output certificates are legitimate classical matched alternatives','BBW Eq23 terminal sign requires correction from Eq18','no PR95 or OpenAI proof closes a receiving gate']}
(B/'FROZEN.json').write_text(json.dumps(frozen,indent=2)+'\n')
print(json.dumps({'status':frozen['status'],'authored_files':len(authored),'report_bytes':info(B/'REPORT.md')['bytes'],'capital_clean':not bool(snap['capital_status_short'])}))
