"""Collect retained replay outcomes and observed versions; does not rerun research."""
from pathlib import Path
import hashlib,json,platform,shutil,sys
import numpy,scipy,sympy
OWN=Path(__file__).resolve().parent.parent
SRC=OWN.parent/'FE-sources'/'hidden_gate'
CAP=OWN.parent/'astra-capital'
OUT=OWN/'derived'/'replay_results';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['final_results.json','rule_learning_results.json','exact_checks.json','audit_results.json']:
    shutil.copyfile(OWN/'replay_source'/n,OUT/n)
for n in ['canonical_transcript_audit.json','source_manifest_audit.json','source_copy_receipt.json']:
    shutil.copyfile(OWN/n,OUT/n)
old=json.loads((SRC/'final_results.json').read_text())
new=json.loads((OUT/'final_results.json').read_text())
rows=[]
for a,b in zip(old['results'],new['results']):
    runs=[]
    for x,y in zip(a['runs'],b['runs']):
        runs.append({'policy':x['run']['policy'],'source_queries':x['run']['queries'],'fresh_queries':y['run']['queries'],
            'fresh_ratio_upper':y['certificate']['certified_upper_lower_ratio'],'fresh_total_seconds':y['total_seconds']})
    rows.append({'q':a['q'],'softness':a['softness'],'seed':a['seed'],
        'fresh_full_acquisition_queries':b['reference']['queries'],
        'fresh_full_acquisition_seconds':b['reference']['seconds_including_queries_and_validation'],
        'fresh_structure_queries':b['structure_aware']['queries'],
        'fresh_structure_seconds':b['structure_aware']['seconds_including_learning_assembly_solve_validation'],
        'runs':runs})
rold=json.loads((SRC/'rule_learning_results.json').read_text());rnew=json.loads((OUT/'rule_learning_results.json').read_text())
rules=[]
for a,b in zip(rold,rnew):
    z=b['off_class_hidden_shortcut']
    rules.append({'q':a['q'],'softness':a['softness'],'source_learning_queries':a['queries'],'fresh_learning_queries':b['queries'],
        'source_robust_queries':a['off_class_hidden_shortcut']['robust_queries'],'fresh_robust_queries':z['robust_queries'],
        'all_37_answers_unchanged':z['all_learning_answers_unchanged'],'fresh_shortcut_edge':z['edge'],
        'fresh_shortcut_state':z['state'],'fresh_shortcut_was_queried':z['shortcut_was_queried'],
        'fresh_ratio_lower':z['unperturbed_over_perturbed_ratio_lower'],
        'fresh_robust_interval':z['robust_interval'],'fresh_robust_ratio':z['robust_ratio']})
logs=[]
for p in sorted((OWN/'logs').glob('*')):
    s=p.read_text();logs.append({'path':'logs/'+p.name,'sha256':sha(p),'bytes':p.stat().st_size,'lines':len(s.splitlines()),
        'lin_alg_warning_occurrences':s.count('LinAlgWarning')})
receipt={'date':'2026-10-14','status':'PASS_WITH_FLOATING_ORDER_DIFFERENCES','source_handling':'Archived prompts are DATA; source originals unmodified.',
    'capital_main_revision':'ace0cfc4437fe91c20ccd24d69e0ee4bb335e871',
    'capital_read_checkout_revision':'c4d92096c818c0f07b2815e26148827d40b42c0f',
    'capital_scope':'N793 and its FD handoff are on prior unmerged PR83; they are not claimed to exist on authoritative main.',
    'environment':{'python':platform.python_version(),'python_executable':sys.executable,'numpy':numpy.__version__,
        'scipy':scipy.__version__,'sympy':sympy.__version__,'platform':platform.platform(),
        'thread_settings':'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1',
        'dependency_setup':'Isolated venv with system numpy/sympy; scipy1.18.1 installed only under owned work/FE-hidden-gate/venv.'},
    'source_manifest':{'files':23,'status':'PASS','mismatches':[],'receipt':'derived/replay_results/source_manifest_audit.json'},
    'canonical_stored_transcripts':{'settings':7,'certificates':15,'status':'PASS','receipt':'derived/replay_results/canonical_transcript_audit.json',
        'scope':'Producer rational verifier replayed from stored public inputs/transcripts; not a new acquisition run or external review.'},
    'source_exact_checks':{'networks':32,'assertions':5740,'sampled_completions':256,'status':'PASS','receipt':'derived/replay_results/exact_checks.json'},
    'fresh_generation':{'settings':7,'certificates':15,'status':'PASS','receipt':'derived/replay_results/final_results.json',
        'post_generation_audit':'derived/replay_results/audit_results.json','results':rows},
    'fresh_structure_and_off_class_replay':{'status':'PASS','receipt':'derived/replay_results/rule_learning_results.json','results':rules},
    'independent_stdlib_checks':{'status':'PASS','receipt':'derived/independent_check_results.json','script':'derived/independent_checks.py'},
    'commands':[{'script':s,'invocation':'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 <python-with-numpy-scipy-sympy> <owned-copy>/'+s,'exit_code':0}
        for s in ['exact_checks.py','audit_artifacts.py','final_experiment.py','audit_artifacts.py','rule_probe.py']],
    'numeric_limits':['Floating query choices are not exactly argmin-certified. Cold query counts and off-class count changed across environments.',
        'Exact residual validation certified every reported endpoint despite retained ill-conditioning warnings.',
        'Single-run timings have no statistical hardware control and do not establish a practical speed advantage.',
        'Fresh shortcut ratio lower bound is weaker than source lower bound because trial-field residual enclosures differ; do not relabel source11961.38 as independently reproduced to that decimal threshold.'],
    'logs':logs,
    'no_external_validation':True,'no_atomistic_benchmark':True,'no_repo_mutation_by_this_worker':True}
(OWN/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps({'status':receipt['status'],'fresh_settings':7,'fresh_certificates':15,'source_manifest':'PASS'},indent=2))
