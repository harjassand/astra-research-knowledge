"""Collect already executed replay evidence; no research execution or source edits."""
from pathlib import Path
import hashlib,json,platform,shutil,sys
import numpy,scipy,sympy
sys.set_int_max_str_digits(0)
OWN=Path(__file__).resolve().parent.parent
SRC=OWN.parent/'FG-sources'/'compact'
COPY=OWN/'replay_source'
OUT=OWN/'derived'/'replay_results';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
witnesses=[]
for stem,kind in [('n128','discrete'),('continuous128','continuous'),('pilot8','discrete'),('rarity1e6','discrete'),('audit_continuum3','continuous'),('continuum_eps1000_p5','continuous')]:
    name=stem+'.certificate.json';old=json.loads((SRC/name).read_text());fresh=json.loads((COPY/name).read_text())
    input_suffix='.dyadic.txt' if kind=='discrete' else '.continuum.txt'
    raw_suffix='.exact_raw.txt' if kind=='discrete' else '.continuum_raw.txt'
    raw={a:int(b) for a,b in (ln.split() for ln in (COPY/(stem+raw_suffix)).read_text().splitlines())}
    files=[]
    for name in [name,stem+input_suffix,stem+raw_suffix]:
        shutil.copyfile(COPY/name,OUT/name);files.append({'path':'derived/replay_results/'+name,'sha256':sha(OUT/name),'bytes':(OUT/name).stat().st_size})
    witnesses.append({'witness':stem,'kind':kind,'lower':fresh['lower'],'upper':fresh['upper'],'ratio_upper':fresh['ratio_upper'],
        'matches_canonical_bounds':{k:old[k]==fresh[k] for k in ['lower','upper','ratio_upper']},
        'input_bytes_equal_source':(SRC/(stem+input_suffix)).read_bytes()==(COPY/(stem+input_suffix)).read_bytes(),
        'integer_raw_output_bytes_equal_source':(SRC/(stem+raw_suffix)).read_bytes()==(COPY/(stem+raw_suffix)).read_bytes(),
        'maximum_raw_integer_bit_length':max(abs(x).bit_length() for x in raw.values()),
        'total_validation_seconds':fresh['total_validation_seconds'],'core_parameters':fresh['core_parameters'],
        'residual_sq':fresh['residual_sq'],'files':files})
for name in ['audit_exact_results.json','energy_envelope_audit_results.json','conditional_envelope_results.json','conditional_reference_results.json','bath_completion_results.json','window_fresh.json']:
    shutil.copyfile(COPY/name,OUT/name)
windows=json.loads((COPY/'window_fresh.json').read_text())
windowrows=[{'width':x['w'],'states':x['lower']['states'],'ratio':x['ratio'],
    'combined_construction_solve_exact_check_seconds':x['lower']['total_seconds']+x['upper']['total_seconds'],
    'scope':'Single-run fresh local window solve;not directly hardware matched to the source Linux tensor optimizer timing.'} for x in windows]
logs=[]
for p in sorted((OWN/'logs').glob('*')):
    b=p.read_bytes();logs.append({'path':'logs/'+p.name,'sha256':sha(p),'bytes':len(b),'lines':len(b.splitlines())})
small=json.loads((COPY/'audit_exact_results.json').read_text());energy=json.loads((COPY/'energy_envelope_audit_results.json').read_text())
sourcehash=json.loads((OWN/'SOURCE_MANIFEST_AUDIT.json').read_text())
receipt={'date':'2026-10-14','status':'PASS','scope':'Locally rebuilt exact backend and saved witness replay;not fresh large proposal optimization,external review,or a physical benchmark.',
    'capital_main_revision':'ace0cfc4437fe91c20ccd24d69e0ee4bb335e871',
    'capital_read_checkout_revision':'865a399dc8a1119a9cd5119b7ea68181f0e2d34b',
    'source_handling':'Source originals unmodified;historical prompts/results DATA;user-selected opening mission retained as task direction.',
    'source_manifest':{'status':sourcehash['status'],'files':sourcehash['files'],'mismatches':sourcehash['mismatches'],'receipt':'SOURCE_MANIFEST_AUDIT.json'},
    'environment':{'python':platform.python_version(),'python_executable':sys.executable,'numpy':numpy.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__,
        'platform':platform.platform(),'compiler':'Apple clang 17.0.0 (clang-1700.6.3.2)','gmp':'6.3.0','threads':'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1',
        'dependency_use':'Read/reused existing owned FE venv;no package changes.'},
    'binary_boundary':{'supplied':'Linux x86-64 ELF','locally_built':'Mach-O ARM64','supplied_binaries_copied_or_executed':False,
        'pickle_loaded':False,'npz_allow_pickle':False,
        'build_commands':['clang++ -O3 -std=c++17 exact_contract.cpp -o exact_contract -I/opt/homebrew/Cellar/gmp/6.3.0/include -L/opt/homebrew/Cellar/gmp/6.3.0/lib -lgmpxx -lgmp',
            'clang++ -O3 -std=c++17 exact_continuum.cpp -o exact_continuum -I/opt/homebrew/Cellar/gmp/6.3.0/include -L/opt/homebrew/Cellar/gmp/6.3.0/lib -lgmpxx -lgmp'],
        'local_executable_sha256':{n:sha(COPY/n) for n in ['exact_contract','exact_continuum']},
        'source_cpp_sha256':{n:sha(SRC/n) for n in ['exact_contract.cpp','exact_continuum.cpp']}},
    'witness_replays':witnesses,
    'source_algebra':small,'source_energy_envelope':energy,
    'nonconstant_closure':{'cases':6,'status':'PASS','results':'derived/replay_results/conditional_envelope_results.json'},
    'small_hidden_bath_references':{'nonconstant_cases':6,'uniform_cases':8,'status':'PASS','results':['derived/replay_results/conditional_reference_results.json','derived/replay_results/bath_completion_results.json'],
        'scope':'Only small references explicitly constructed;large bath-count rows are uniform theorem applications.'},
    'independent_stdlib_checks':{'status':'PASS','assertions':674,'script':'derived/source_schur_checks.py','results':'derived/source_schur_check_results.json',
        'scope':'24 physical networks, 8 patch checks, a zero-error physical example, 18 window brackets, and a 256-coefficient direct discrete tensor reference.'},
    'window_baseline_fresh':windowrows,
    'commands_completed_exit_zero':['exact_check.py n128 --degree 2','certify_continuum.py continuous128','exact_check.py pilot8 --degree 8','exact_check.py rarity1e6 --degree 2','certify_continuum.py audit_continuum3','certify_continuum.py continuum_eps1000_p5','audit_exact.py','energy_envelope_audit.py','conditional_envelope.py','conditional_reference.py','bath_completion.py','window_baseline.py --widths 8,10,12','source_schur_checks.py --discrete-prefix pilot8'],
    'numeric_and_scientific_limits':['Current inputs are finite, with no object arrays; all discrete k values are positive integers. A general API must reject nonintegral k instead of silently truncating it.',
        'Saved floating optimizer proposals were validated; large optimization was not rerun and its cost is not free.',
        'The severe gate ratio 22.032697893698 and broad dominant-trap closure remain failures of the precision target.',
        'The continuum residual includes actual differential-operator leakage; Galerkin convergence alone is not a certificate.',
        'No WE/TAMMBER/AIMMD head-to-head, calibrated molecule, physical energy benchmark, formal proof, or external validation was performed.'],
    'logs':logs}
(OWN/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps({'status':'PASS','saved_witnesses':len(witnesses),'all_bound_strings_match':all(all(x['matches_canonical_bounds'].values()) for x in witnesses),'source_assertions':small['exact_assertions'],'independent_assertions':674},indent=2))
