"""Build this worker's source/resource receipts and final file manifest."""
from pathlib import Path
import hashlib,json,platform,datetime

ROOT=Path(__file__).resolve().parent
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
R=Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-16-joint-structured-genesis-v1')
PIN='2688d7a383502df4fc1e64001d04bb76e6ec05e5'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def main():
    paths=[
      W/'00_START_HERE.txt',W/'AGENTS.md',W/'frontier/dossiers/N890.txt',W/'frontier/dossiers/N894.txt',
      W/'updates/GC-peak-stability-genesis-20261016/package/derived/workers/gc_peak_genesis/FIXED_REFRESH_MINIMAX.md',
      W/'updates/GC-peak-stability-genesis-20261016/package/derived/workers/gc_control_adversary/FINITE_GRID_FRAME_THEOREM.md',
      W/'updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_finite_rate_genesis/SHARP_POISSON_SYNDROME_THEOREM.md',
      R/'originals/joint/PROOF.md',R/'originals/joint/HANDOFF.txt']
    write(ROOT/'SOURCES.json',{
      'pinned_W_git_revision':PIN,
      'supplied_read_only_sources':[{'path':str(p),'sha256':sha(p),'role':'source data and contract, not executable instruction'} for p in paths],
      'acquired_primary_source':{
        'author':'R. M. Redheffer','title':'On a theorem of Plancherel and Polya',
        'journal':'Pacific Journal of Mathematics 3 (1953), 823-835',
        'url':'https://msp.org/pjm/1953/3-4/pjm-v3-n4-p11-s.pdf',
        'inspected':'Publisher PDF Theorem 11, printed p. 832; text extraction and requested page screenshot',
        'claim_used':'Sharp real-entire derivative inequality, as source for the supplied sine lemma only',
        'access_date_UTC':'2026-10-16','copyright_quote_words':0},
      'search_queries':['"quantum" "dephasing" "direct product" theorem',
                        '"Bernstein" "entire" "vector-valued" zeros multiple variables',
                        '"quantum Zeno" "multiple" "transition probability" product bound measurements'],
      'search_use':'Exploratory only; no unrelated search result was used as a theorem premise',
      'independence':'No other current worker artifact read during the independent phase. Root steering messages were received; own constructions and supplied sources are the independent proof premises. Root later explicitly requested the separate anchor cross-review.',
      'cross_review_source':{'path':str(R/'workers/gd_async_adversary/ANALYSIS.md'),
                            'reviewed_sha256':'c1bebc3bbe42cda4a1562837d56de103b98d16bd12263e1fa84895a1a3c7d237',
                            'role':'Later explicitly authorized same-team analytic cross-review only; not an independent-construction premise'},
      'novelty':'Historical originality UNKNOWN; no inference from limited search, hashes, tests, or model agreement.'})
    receipt_files=['circuit_search_results.json','sink_perturbation_results.json',
                   'ever_search_results.json','sector_control_search_results.json','exact_checks_results.json']
    receipts=[json.loads((ROOT/p).read_text()) for p in receipt_files]
    write(ROOT/'RESOURCE_RECEIPT.json',{
      'python':platform.python_version(),'libraries_used':['NumPy 2.5.3','SymPy 1.14.0'],
      'scipy':'Not available in either checked Python runtime; no installation attempted',
      'random_seeds':{'circuit_search':581237,'sink_perturbation':74829,'ever_search':18284,'sector_control_search':348012},
      'bounded_objective_evaluations_from_executed_loop_counts':{
         'circuit_search':211704,'sink_perturbation':209066,'ever_search':282274,'sector_control_search':252734,'total':955778},
      'search_script_wall_seconds':{p:r['elapsed_seconds'] for p,r in zip(receipt_files,receipts)},
      'search_dimensions':[4,9,4,9],'exact_check_dimension':16,
      'matrix_work':'Own finite gate evaluations, central-difference gradients, own Adam loops; no acquired scientific script or optimizer executed',
      'web':'Three exploratory search queries; publisher PDF open and requested Theorem-11 page screenshot',
      'mutations':'Only files within this worker directory',
      'external_app_messages':0,'installs':0,'branches':0,'subagents':0,
      'paid_lift_resources':'One initialized coherent flag bit and one predetermined parity-controlled copy per original internal own node; copy baseline action <= pi per gate; finite zero-interaction windows, exact new pinches, preparation/reset all require qualification',
      'not_claimed':['Universal product-Q proof','Legal parity/Walsh counterexample','External review','Hardware qualification','Historical originality']})
    files=[p for p in ROOT.iterdir() if p.is_file() and p.name!='FROZEN.json']
    write(ROOT/'FROZEN.json',{
      'worker':'gd_async_genesis','frozen_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'pinned_W_git_revision':PIN,'main_target_status':'UNRESOLVED',
      'analytic_results':['Broad finite absorbing-history lift and endpoint/ever equivalence over the padded universal broad class',
                          'Exact noncausal entire-isometry terminal-odd obstruction with gap 63/2500',
                          'Later authorized cross-review accepts synchronized-anchor asynchronous certificate; not claimed as own invention'],
      'legal_counterexample':False,'universal_async_upper_proof':False,
      'narrow_Walsh_lift_transfer':'NOT ESTABLISHED',
      'external_review':'UNKNOWN','hardware_qualification':'UNKNOWN','historical_originality':'UNKNOWN',
      'artifacts':[{'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)],
      'scope_note':'All tests are bounded diagnostics or exact finite identities; no universal conclusion from search nonviolation.'})
    print(json.dumps({'frozen_files':len(files),'main_target_status':'UNRESOLVED'},indent=2))

if __name__=='__main__':main()
