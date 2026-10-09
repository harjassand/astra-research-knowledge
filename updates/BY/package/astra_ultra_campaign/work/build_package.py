#!/usr/bin/env python3
"""Assemble immutable research evidence, without changing either source repository."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'outputs/astra_ultra_campaign'
PKG.mkdir(parents=True, exist_ok=True)
PINS = {'astra': '8aed7fd74eb14622ed5a0a3635a799374296e32a',
        'openai-math': 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb'}
MAINHASH = 'cfdbb6a0ca85861788d39c8843ce7533a641633c4cabab8070ac09b9d41d170d'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(rel, content):
    path = PKG / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def data(rel, obj):
    write(rel, json.dumps(obj, indent=2) + '\n')


def copy(source, dest=None):
    source = ROOT / source
    dest = PKG / (dest or source.relative_to(ROOT))
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(ROOT/'work/sources'/repo), *args])


assert sha(ROOT/'outputs/amplifier_proof_candidate.tex') == MAINHASH
copy('outputs/amplifier_proof_candidate.tex', 'amplifier_proof_candidate.tex')
copy('work/campaign_result.txt', 'campaign_result.txt')
shutil.copy2(ROOT/'work/campaign_result.txt', ROOT/'outputs/campaign_result.txt')
copy('work/verify_core.py', 'verify_core.py')
copy('work/reproduce_package.py', 'reproduce.py')
copy('work/build_package.py', 'work/build_package.py')
for rel in ['work/worker_brief.txt', 'work/source_pins.json', 'work/coordinator_fock_closure.txt', 'work/amplifier_core.tex']:
    copy(rel)
for p in (ROOT/'work/freezes').glob('*.tex'):
    copy(p.relative_to(ROOT))

excluded = []
for p in sorted((ROOT/'work/reports').rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to(ROOT)
    if '__pycache__' in p.parts:
        continue
    if p.suffix == '.pdf' or p.name in ['isotropic_independent_sets_prior.txt', 'direct-finiteness.txt']:
        excluded.append({'original_path': str(rel), 'sha256': sha(p), 'bytes': p.stat().st_size,
                         'reason': 'Third-party paper capture; source URL retained in investigator report. Not authored campaign work.'})
        continue
    assert p.suffix in ['.txt', '.py', '.json', '.tex'], str(rel)
    copy(rel)

source_entries = []
for repo, rev in PINS.items():
    assert git(repo, 'rev-parse', 'HEAD').decode().strip() == rev
    assert not git(repo, 'status', '--porcelain').decode().strip()
    paths = git(repo, 'ls-tree', '-r', '--name-only', rev).decode().splitlines()
    if repo == 'openai-math':
        selected = [p for p in paths if p in ['LICENSE', 'README.md', 'CONTENTS.md', 'lean/LICENSE', 'lean/docs/273.md']
                    or p.startswith('preprints/The-entropy-photon-number-inequality-September-24-2026/') and p.endswith(('.tex','.md'))]
        audit = json.loads((ROOT/'work/reports/sol4_adversarial/import_audit.json').read_text())
        selected += [m['path'] for m in audit['modules'].values()]
    else:
        selected = [p for p in paths if p in ['00_START_HERE.txt','AGENTS.md','README.md','agent/topics.txt',
                    'agent/RESEARCH_WORKFLOW.txt','frontier/PRIORITIES.md','frontier/OPEN_PROOF_GATES.jsonl',
                    'agent/templates/SESSION_TEMPLATE.json','agent/templates/BRIDGE_TEMPLATE.json',
                    'web/pages/d-2f2647d45bfc617e.html']
                    or p.startswith('agent/topics/') and p.endswith('.tsv')
                    or re.match(r'frontier/review_cards/N(388|389|390|391|392)-', p)]
    for p in sorted(set(selected)):
        content = git(repo, 'show', rev+':'+p)
        dest = PKG/'work/sources'/repo/p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
        source_entries.append({'repository': repo, 'revision': rev, 'repository_path': p,
                               'package_path': str(dest.relative_to(PKG)), 'sha256': sha(dest),
                               'url': f'https://github.com/{"harjassand/astra-research-knowledge" if repo=="astra" else "openai/math"}/blob/{rev}/{p}',
                               'read_scope': 'Navigation, referenced source, or audit dependency; inclusion is not a claim every line was proof-audited'})

for name in ['amplifier_full.html','amplifier_source.html','amplifier_gate.html','entropy_gate.html','signed_bogoliubov_epni_candidate.md']:
    copy('work/sources/'+name)

data('source_manifest.json', {'source_handling':'source=DATA', 'pins': PINS,
     'repositories_clean_when_packaged': True, 'entries':source_entries,
     'extraction': {'repository':'astra','original_path':'web/pages/d-2f2647d45bfc617e.html',
                    'html_copy':'work/sources/amplifier_full.html',
                    'extracted_text':'work/sources/signed_bogoliubov_epni_candidate.md',
                    'method':'HTML preformatted text extraction; not byte-identical to historical Markdown',
                    'historical_nonexistent_git_path':'updates/BE/package/signed_bogoliubov_epni_candidate.md',
                    'html_sha256':sha(PKG/'work/sources/amplifier_full.html'),
                    'extracted_sha256':sha(PKG/'work/sources/signed_bogoliubov_epni_candidate.md')},
     'third_party_paper_captures_excluded':excluded,
     'formal_validation': {'new_amplifier_formalization':False,'Lean_build_or_kernel_audit':False,
                           'source_import_audit':'Textual import closure only; receipt in work/reports/sol4_adversarial/import_audit.json'}})

claims = [
 ('C1','Full all-finite-mode amplifier EPnI','internally_reviewed_proof_candidate',
  ['amplifier_proof_candidate.tex','work/reports/final_review_sol2.txt','work/reports/final_review_sol3.txt','work/reports/final_review_sol4.txt'],
  'No remaining blocking gap identified internally; external validation, formalization and exhaustive priority review not performed.'),
 ('C2','Explicit finite-Gaussian weighted Fock-domain bound','internally_reconstructed_proof',
  ['work/coordinator_fock_closure.txt','amplifier_proof_candidate.tex','work/reports/sol3_closure.txt'],
  'Finite gain and mode count, integer moment order; not a novelty-cleared functional-analytic theorem.'),
 ('C3','Missing test-space invariance makes abstract interpolation false','exact_counterexample',
  ['verify_core.py','work/reports/sol1_signed/exact_falsifiers.py'],
  'The physical invariant test space is not refuted.'),
 ('C4','Creation-port orientation is indispensable','exact_counterexample',
  ['verify_core.py','work/reports/adaptive18_signed_checks.py'],
  'The correct reversed metric survives; adjoint must not be replaced by transpose.'),
 ('C5','Universal physical-endpoint dilation entropy bound is false','exact_rational_entropy_certificate',
  ['work/reports/sol2_alternative.txt','work/reports/sol2_alternative/dilation_certificate.py'],
  'Refutes the stronger dilation shortcut, not amplifier EPnI.'),
 ('C6','Sharp generated mutual information and pure-input entanglement minima','conditional_on_C1',
  ['work/reports/sol5_consequences.txt'],
  'Derived if C1 is correct; equality uniqueness is not claimed.'),
 ('C7','Regularized Holevo upper bound with a non-Gaussian environment','conditional_on_C1',
  ['work/reports/sol5_consequences.txt'],
  'Memoryless centered environment and energy constraint; not an exact general capacity formula.'),
 ('C8','2064 one-mode physical-amplifier cases found no counterexample','floating_diagnostic',
  ['work/reports/sol5_consequences/search_results.json','work/reports/sol5_consequences/verification.json'],
  'No interval-certified arithmetic or universal conclusion; four near-equality ambiguous cases retained.'),
 ('C9','p-spin plateau expectation inequality','unresolved',
  ['work/reports/adaptive24_plateau.txt'],
  'Pointwise positivity is false; the calculated expectation was positive. Universal gate remains open.'),
 ('C10','Symplectic-span independent-set counting','specialist_candidate_not_novelty_cleared',
  ['work/reports/16_integer_computation.txt'],
  'Parameter-dependent exact algorithm; no general #P breakthrough.'),
 ('C11','2D power-to-dissipation observable certificate','internally_reconstructed_known_mechanism',
  ['work/reports/adaptive34_positive.txt'],
  'Known energy balance; no experiment or demonstrated novel practical advantage.'),
]
data('claim_ledger.json', {'primary_objective_status':'NOT_ESTABLISHED',
     'main_manuscript_sha256':MAINHASH, 'external_validation':False,
     'historic_significance_established':False,
     'claims':[{'id':i,'claim':c,'status':s,'evidence':e,'limits':l} for i,c,s,e,l in claims]})

data('review_resolutions.json', {
 'proof_final_sha256': MAINHASH,
 'proof_reviews':['work/reports/final_review_sol2.txt','work/reports/final_review_sol3.txt','work/reports/final_review_sol4.txt'],
 'proof_issues_closed':['Source multiplier-invariance hypothesis','Elementary-factor graph domains before composition',
                        'Centered dual representing-vector norm','Distinct y_0 and y_A parameters',
                        'Half-integer scope for weighted-channel estimate','Discarded operators cut off in own number basis'],
 'report_consistency_review':'work/reports/final_report_consistency.txt',
 'report_precision_edit_applied':'Section 2 specifies finite-energy one-mode environment, signal photons per use, and nats per use.',
 'report_sha256_after_edit':sha(PKG/'campaign_result.txt'),
 'external_review':False})
data('compilation_receipt.json', {
 'manuscript':'amplifier_proof_candidate.tex','sha256':MAINHASH,
 'tool':'mcp__codex_app__compile_latex_document','status':'success',
 'message':'The current source compiled successfully with the desktop editor compiler.',
 'date':'2026-10-10','scope':'Compilation only, not proof verification','standalone_pdf_exported':False})

breadth = sorted((PKG/'work/reports').glob('[0-9][0-9]_*.txt'))
assert len(breadth) == 36
adaptive = sorted((PKG/'work/reports').glob('adaptive*.txt'))
depth = sorted((PKG/'work/reports').glob('sol[1-5]_*.txt'))
assert len(adaptive)==5 and len(depth)==5
catalogue_allowed = {21,22,23,24,26,30,32}
def report_entry(p):
    return {'report':str(p.relative_to(PKG)), 'sha256':sha(p), 'status':'completed'}
data('agent_manifest.json', {
 'breadth': [{**report_entry(p),'worker':p.stem,'model':'gpt-6-luna','reasoning_effort':'max',
              'initial_catalogue_access_permitted':int(p.name[:2]) in catalogue_allowed,
              'portfolio':('applied' if int(p.name[:2])<=18 else 'foundational' if int(p.name[:2])<=24 else 'measurement' if int(p.name[:2])<=29 else 'cross-disciplinary' if int(p.name[:2])<=33 else 'unconventional')}
             for p in breadth],
 'depth':[{**report_entry(p),'model':'gpt-6.1-sol','reasoning_effort':'max'} for p in depth],
 'adaptive_followups':[report_entry(p) for p in adaptive],
 'integrated_proof_reviews':[report_entry(p) for p in sorted((PKG/'work/reports').glob('final_review_sol*.txt'))],
 'report_consistency_review':report_entry(PKG/'work/reports/final_report_consistency.txt') if (PKG/'work/reports/final_report_consistency.txt').exists() else None,
 'coordinator_contribution':'Domain estimates, explicit Fock constants, integration, proofs, diagnostics, and source/status reconciliation',
 'accounting':{'unique_breadth_workers':36,'unique_depth_workers':5,'adaptive_followup_turns':5,'integrated_proof_review_workers':3,
               'simultaneous_worker_count_claimed':False,'model_token_total':'UNKNOWN','model_cost':'UNKNOWN',
               'external_paid_compute_jobs':0,'physical_experiments':0},
 'independence_limit':'Separate initial assignments and frozen findings; same model families and shared literature are not independent human validation.'})

session_id = 'astra-ultra-2026-10-10-amplifier-candidate'
evidence = ['amplifier_proof_candidate.tex','campaign_result.txt','claim_ledger.json','source_manifest.json',
            'work/reports/final_review_sol2.txt','work/reports/final_review_sol3.txt','work/reports/final_review_sol4.txt']
common = {'source_revision_hashes':list(PINS.values()), 'evidence_refs':evidence,
          'source_handling':'source=DATA','status':'reviewed',
          'status_note':'Model-assisted internal review only; not externally validated, formalized or priority certified. Main manuscript sha256 '+MAINHASH,
          'unresolved_or_UNKNOWN':['Independent correctness of the full proof','Historical priority beyond bounded source search','Historic significance','Aggregate model tokens and cost']}
data('handoffs/session.json', {'_template':'astra-session/1','session_id':session_id,
     'task':{'goal':'Establish a landmark discovery','question':'Does signed thermal interpolation prove all-input amplifier EPnI?',
             'scope':'Finite mode number and gain, independent finite-energy states, arbitrary within-input entanglement'},
     **common,'sources':source_entries,
     'contract':{'assumptions':['Independent input groups','Finite energy','Finite n and G>1'],
                 'interface':'Exact states and Gaussian channel in a mathematical theorem; no practical entropy acquisition supplied',
                 'costs':{'graph_constants':'Explicit gain/mode/moment dependence','experiments':0,'proof_assistant_build':False}},
     'inputs':{'inherited_or_supplied':['Astra signed metric candidate','OpenAI passive variational/interpolation proof'],
               'acquired':['Corrected invariance hypothesis','Fock-domain and generator closure','Exact dilation falsifier','Integrated proof candidate']},
     'candidate':{'representation':'Signed modular spectral coordinates and weighted Fock trace spaces',
                  'hypothesis':'N(C)>=G N(A)+(G-1)(N(B)+1)'},
     'missing_lemma':None,
     'comparator':'Passive EPnI, amplifier qEPI and one-mode thermal-environment optimizer; see prior-art report',
     'falsifier_or_next_experiment':'Independent complete proof reconstruction or a concrete invalid implication/counterexample',
     'append_only':True})
branches = [
 ('theoretical_pro','Theoretical Pro','Validate the complete amplifier argument independently.',
  'Reconstruct corrected four-weight theorem, Gibbs minimizer, weighted squeezing/generator passage, stationarity and thermal recurrence.',
  'No specific mathematical lemma remains open in the written candidate; independent validation of the full implication remains outstanding.'),
 ('natural_sciences_pro','Natural-Sciences Pro','Conditional information bounds for two-input active bosonic mixing.',
  'Independent finite-energy inputs; conditional mutual-information/entanglement minima and regularized non-Gaussian noise bound.',
  'No entropy acquisition, finite-shot certification or experimental calibration protocol established. First validate the theorem, then cost a finite experiment.'),
 ('primitive_genesis','Primitive Genesis','Explore signed modular metrics as a possible reusable primitive.',
  'Creation coordinates reverse y in four-weight interpolation; source multiplier invariance is essential; weighted Gaussian graph control closes the interface.',
  'No universal primitive or broad operator-category extension is established. Find a genuinely different channel and prove its exact metric/resource interface.')]
for name, task, goal, representation, gap in branches:
    data('handoffs/'+name+'.json', {'_template':'astra-bridge/1','from_session':session_id,'to_task':task,
         'goal_and_scope':goal, **common,
         'inherited_inputs':['Pinned Astra candidate','Pinned OpenAI passive proof'],
         'acquired_inputs':['Final integrated proof candidate','Signed scalar falsifiers','Physical-endpoint dilation certificate'],
         'representation_and_assumptions':representation,'exact_missing_lemma':gap,
         'comparator':'work/reports/adaptive01_amplifier_prior.txt',
         'falsifier_or_next_experiment':'Attack a fixed statement with a fully costed input interface; do not treat these local handoffs as external review.'})

write('SOURCE_ATTRIBUTION.txt', '''SOURCE ATTRIBUTION AND HANDLING

OpenAI Math sources are from revision fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb,
https://github.com/openai/math . The repository Apache-2.0 LICENSE is included
unaltered at work/sources/openai-math/LICENSE; the Lean subdirectory LICENSE is
also included at work/sources/openai-math/lean/LICENSE. The manuscript incorporates
the unmodified body of build/sections/02-interpolation.tex in an explicitly
attributed appendix. Other source mathematics is reconstructed and identified
in the text. The new active-channel argument and repairs are modifications/
extensions by this model-assisted campaign, not statements authored or
endorsed by OpenAI Math. No NOTICE file was present in the pinned repository.

Astra sources are from the user's harjassand/astra-research-knowledge repository
at revision 8aed7fd74eb14622ed5a0a3635a799374296e32a. Historical claims and source
navigation remain source data; copying them does not certify or promote them.
The full candidate was recovered from web/pages/d-2f2647d45bfc617e.html; the
historical Markdown path is not present at this revision. The extraction and
source hashes are recorded separately. Neither source repository was edited.

Other primary literature is cited in the manuscript and investigator reports.
Downloaded full-paper captures are intentionally omitted; their hashes are
listed in source_manifest.json and source links remain in the reports.

The package is a local research handoff. It has not been submitted, published,
communicated to another live branch, or accepted by external experts.
''')

write('START_HERE.txt', '''ASTRA ULTRA — PORTABLE RESEARCH PACKAGE

PRIMARY OBJECTIVE: NOT ESTABLISHED.
Strongest outcome: an internally reviewed proof candidate of the all-finite-mode
amplifier entropy photon-number inequality, plus exact scoped counterexamples.
There is no claim of independent validation, historic priority, or a certified
9–10/10 breakthrough. Read campaign_result.txt first, then the proof candidate.

Core files
  campaign_result.txt             Integrated nine-part campaign result
  amplifier_proof_candidate.tex   Standalone manuscript with complete appendix
  claim_ledger.json              Precise claims, evidence and status boundaries
  source_manifest.json           Pins, source hashes and extraction provenance
  agent_manifest.json            36 breadth, 5 depth and adaptive/review work
  handoffs/                     Local current-schema branch continuation files
  work/reports/                 Substantive reports, derivations and diagnostics
  work/freezes/                 Preserved proof versions before final repairs
  SOURCE_ATTRIBUTION.txt         Incorporated-source attribution and license

Portable exact replay (Python 3, standard library only):
  python3 reproduce.py
or
  python3 reproduce.py --output my_receipt.json
No network, Git checkout, source directory, external package or proof assistant
is needed for this replay. The scripts are copied to a temporary directory so
that historical receipts stay unchanged. These checks certify their stated
finite/exact assertions, not the universal amplifier theorem.

Other scripts are optional research diagnostics. Their imports identify their
dependencies (NumPy/SciPy/SymPy/mpmath where used). Existing numerical receipts
are included. The source-import audit requires a full pinned openai/math Git
checkout at work/sources/openai-math; the delivered source snapshot is not a
Git checkout. No Lean/kernel replay was performed. Source builds and numerical
searches are not part of the portable exact replay.
work/build_package.py is preserved as assembly provenance and expects the
original workspace and pinned Git clones; it is not the portable replay entry.

The standalone .tex compiles in the Codex built-in LaTeX editor and uses standard
article, geometry, AMS, mathtools and hyperref packages. Compilation is document
integrity evidence, not proof certification. Historical worker reports retain
their own earlier conditional scopes; the final ledger and final_review_sol*
reports record the integrated state. Their original outputs/ manuscript path
corresponds to amplifier_proof_candidate.tex at this package root.

MANIFEST.sha256 covers every delivered file except itself. Package validation
checks file hashes and exact replay in an extraction with sources omitted.
The next decisive gate is independent source-complete review of the fixed
candidate, especially its interpolation and infinite-dimensional passage.
''')
print(json.dumps({'package':str(PKG),'breadth_reports':len(breadth),'depth_reports':len(depth),
                  'adaptive_reports':len(adaptive),'source_files':len(source_entries),
                  'main_sha256':MAINHASH}, indent=2))
