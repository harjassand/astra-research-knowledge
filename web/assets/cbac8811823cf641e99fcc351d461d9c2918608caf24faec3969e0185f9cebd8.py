"""Checkpoint phase two without overwriting any phase-one artifact."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
root=Path(__file__).resolve().parents[4]
own=root/'work/cycle6/c08_s01'
out=root/'outputs/round6/c08_s01'
def record(relative):
    p=root/relative
    return {'path':relative,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
initial=record('work/cycle6/c08_s01/INITIAL.txt')
assert initial['sha256']=='04492258a38afabeed53d25b8e4530e9568a45186cab4295d13ec656176ca444'
paths=[
 'work/cycle6/c08_s01/reviews/CROSS_REVIEW.json',
 'work/cycle6/c08_s01/reviews/FIXED_ANISOTROPY_FULL_SEPARABILITY_AUDIT.txt',
 'work/cycle6/c08_s01/revisions/03_GROWING_ANISOTROPY_STOPPED_DIFFUSION.txt',
 'work/cycle6/c08_s01/revisions/04_BALANCED_CASIMIR_SHIFT.txt',
 'work/cycle6/c08_s01/reviews/check_claims.py',
 'work/cycle6/c08_s01/reviews/claim_checks.json',
 'work/cycle6/c08_s01/revisions/check_growing_diffusion.py',
 'work/cycle6/c08_s01/revisions/growing_diffusion_checks.json',
 'work/cycle6/c08_s01/reviews/check_fixed_qudit.py',
 'work/cycle6/c08_s01/reviews/fixed_qudit_checks.json',
 'work/cycle6/c08_s01/reviews/check_ball_absorption.py',
 'work/cycle6/c08_s01/reviews/ball_absorption_checks.json']
checkpaths=[p for p in paths if p.endswith('.json') and 'checks' in p]
fixtures=[json.loads((root/p).read_text()) for p in checkpaths]
assert all(f['status']=='PASS' for f in fixtures)
counts=[len(f['checks']) for f in fixtures]
now=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
result={
 'worker_id':'c08_s01','phase':'phase2','utc_time':now,
 'status':'COMPLETE_INTERNAL_INDEPENDENT_AUDIT_AND_STRONGER_DERIVATIONS; EXTERNAL_VALIDATION_AND_PRIORITY_UNKNOWN',
 'requested_model':'gpt-6.1-sol','requested_effort':'max','observed_model':'UNKNOWN',
 'initial_preserved':initial,
 'phase1_final_preserved':record('work/cycle6/c08_s01/FINAL.txt'),
 'cross_review':{'assigned':['c08_l01','c08_l04','c08_l07','c08_l10'],
   'frozen_baselines':['c08_s01','c08_s02','c08_s03'],
   'claims':13,'maximum_score':2,'acquired_gate_score3_or4':'NONE',
   'substantive_refutation':'c08_l07 Sasaki frame is nonorthogonal unless kappa=1; corrected work density nu(kappa^2+1)^2, equality only kappa1. General sl2 construction and revision03 survive.',
   'peer_repair_status':'Precise correction request sent; peer acceptance UNKNOWN at this checkpoint'},
 'strongest_audit':{
   'scope':'Full collective fundamental SU(d), known parameters; exact N-party full separability',
   'quantifiers':'Every fixed d>=2,alpha>0,bounded traceless Hermitian local field op norm<=B0; every N>=1; every real symmetric E with op norm<=delta_star',
   'state':'exp(Q_(alpha I+E)/N+F_B)/Tr exp(Q_(alpha I+E)/N+F_B)',
   'constants':{
      'beta':'2alpha(d-1)(d+3)+dB0',
      'H1':'2alpha(d-1)(d+1)/d+B0',
      'a':'8alpha d(d-1)', 'c0':'d log d+beta',
      'q':'H1+c0+log d+1+log max(2H1,1)',
      'L':'(a+sqrt(a^2+4a q))/2+1',
      'eta':'exp(-c0-L)', 'delta_star':'alpha eta^2/40'},
   'proof_chain':['Exact full tensor generator','Full-basis principal positivity','Known positive covariance margin on eta/2 neighborhood','Exact logdet drift/QV cancellation','Scalar martingale exit tail','Stopped Duhamel exp(hN) loss','Scalar Jensen trace normalization','Elementary full separable trace-norm ball','White mass (d eta)^N','2T<(eta/d)^N all-N absorption'],
   'repairs':['Earlier delta=alpha eta^2/10 certifies 3eta/4 neighborhood, not eta/2; use /40 for eta/2','HS1 and HS1/2 conventions must be scaled consistently','Exact full separability does not imply exact IID-product mixture'],
   'origin':'Root fixed-open-ball and root ball-absorption proposals; c04_s01/c04_s02 full generator/logdet reconstruction; c07_s02 qubit stopping precursor; c08_s01 independent full audit and explicit all-N constants',
   'status':'ANALYTIC_AUDIT_PASS_INTERNAL; no formal or external validation'},
 'other_delivered_derivations':[
   {'claim':'Localized coherent sandwich trace lemma removes global exp(hN), gives R^2/sqrtN->0 and B R^1.5/N^.75->0 with exp(-cN/R^2)',
    'status':'Complete internal derivation; superseded in growing-range strength by balanced shift, lemma remains useful',
    'origin':'c08_s01 on c07_s02/S01 construction'},
   {'claim':'Balanced Casimir shift keeps fixed qubit PSD ball; M=o(sqrtN), B=o(N^.75) give exp(-cN)',
    'status':'Complete internal derivation; shared independent post-exposure variant reported from c05_s03',
    'origin':'c08_s01 independent reconstruction plus c05_s03 parallel variant, c07_s02 baseline'},
   {'claim':'Unrestricted sandwich trace norm is exp(Theta(M sqrtN)); no uniform polynomial replacement possible',
    'status':'Exact rank-one spin-sector obstruction'},
   {'claim':'White peeling can produce fully separable non-IID remainder; two-qubit same-Z covariance=-4/225',
    'status':'Exact counterexample; boundary only, not a refutation of full separability'}],
 'cost':{'check_groups':counts,'exact_checks':sum(counts),
    'runtime_seconds':sum(f['runtime_seconds'] for f in fixtures),
    'dependencies':'Existing Python3, SymPy1.14.0; one local process per script; no solver/large matrix/hardware experiment',
    'largest_full_tensor_fixture':'d3 N2, dimension9; parity fixture d3 N3, dimension27 diagonal products',
    'sampler_compiler':'UNIMPLEMENTED; no finite-bit efficiency claim',
    'backend_tokens_energy_peak_memory':'UNKNOWN'},
 'priority':{'status':'UNKNOWN','sources':[
    {'url':'https://arxiv.org/abs/quant-ph/0302102','scope':'Known multipartite separable balls; elementary proof here is conservative'},
    {'url':'https://arxiv.org/html/2607.28536v1','scope':'Generic long-range high-temperature separability/preparation Theorems1/2 and existing Pauli parity Lemma8; no exclusion of prior special open-ball result'},
    {'url':'https://link.springer.com/article/10.1007/BF01053756','scope':'Publisher abstract only; full 1991 proof unavailable here'}]},
 'boundaries':['Known parameters and full SU(d) fundamental basis','Fully separable target, exact IID mixture UNKNOWN','Continuous law and ball existence, no efficient decomposition acquisition','No external reference/channel preservation','No hardware, energy or field-breaking conclusion','No causal comparison of origin models'],
 'artifacts':[record(p) for p in paths],
 'peer_files_changed':'NONE','peer_scripts_executed':'NONE','new_agents_created':0}
out.joinpath('PHASE2_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
summary='''C08_S01 PHASE2 FINAL -- cross-review plus independent stopped-diffusion audit
INITIAL, phase1 FINAL and all earlier outputs are preserved.

STRONGEST DELIVERED AUDIT
The full SU(d) tensor/principal/logdet/exit/Duhamel/Jensen proof survives
independent reconstruction. Root's fixed-anisotropy and ball-absorption
strengthening gives exact N-party FULL separability for every N>=1 in an
explicit fixed positive radius delta_star around the ferromagnetic isotropic
coupling alpha I/N, for every fixed d>=2,alpha>0 and bounded known traceless
local field. The complete all-N constants and derivation are in
 reviews/FIXED_ANISOTROPY_FULL_SEPARABILITY_AUDIT.txt.
Root's strengthening and c04/c07 source construction are explicitly credited.
Exact IID mixture, efficient sampler, formal/external validation, priority and
field-breaking significance remain UNKNOWN. /40 radius explicitly certifies
the eta/2 neighborhood; the earlier /10 radius certifies 3eta/4 instead.

CROSS-REVIEW
 reviews/CROSS_REVIEW.json assesses13 consequential claims from c08_l01,l04,
l07,l10 against all three frozen Sol INITIALs. Max contribution score2;
no score3/4 acquired gate. c08_l07 general-curvature Sasaki equality is false:
the alleged frame is not orthogonal unless kappa1 and actual work density is
nu(kappa^2+1)^2. Corrected formulas sent to the worker; acceptance UNKNOWN.
Its orthonormal sl2 family and fixed-flow/fixed-volume revision03 are retained.

OWN GROWING-ANISOTROPY DERIVATIONS
 revisions/03_GROWING_ANISOTROPY_STOPPED_DIFFUSION.txt proves a coherent
sandwich trace lemma, weighted tails and a stronger growing region. Revision04
then obtains the best qubit range M=o(sqrtN),B=o(N^.75),exp(-cN), by a balanced
Casimir shift and fixed PSD ball. A concurrent independent c05_s03 variant
was reported by c07_s02 and is credited; no exclusive-origin claim.
An exact global norm obstruction and an explicit fully-separable non-IID
white-remainder counterexample are also preserved.

EVIDENCE AND COST
120 own finite exact checks PASS across21 geometry,42 qubit,36 qudit and21
parity/white checks. Total observed script runtime about50.89seconds; existing
Python/SymPy1.14.0, bounded single-process algebra only. Fixtures detect
transcription/sign/normalization errors; all-N proofs are supplied separately.
No peer script ran or peer file changed. No new agent, model change, spend,
automation, commit or publication. Mathematical local coefficients are known;
Brownian/stopping/weight sampling and finite-bit acquisition remain unexecuted.

Priority is UNKNOWN. Separable balls and parity arguments have established
primary-source comparators; the 1991 full proof remains unavailable here.
No causal model comparison or breakthrough claim is made.
Complete structured metadata: outputs/round6/c08_s01/PHASE2_RESULT.json.
'''
own.joinpath('PHASE2_FINAL.txt').write_text(summary)
end={'worker_id':'c08_s01','phase':'phase2','utc_time':now,
     'status':result['status'],'initial_preserved':initial,
     'final':record('work/cycle6/c08_s01/PHASE2_FINAL.txt'),
     'result':record('outputs/round6/c08_s01/PHASE2_RESULT.json'),
     'peer_changes':'NONE','new_agents':0,'exact_checks':sum(counts)}
own.joinpath('PHASE2_END.json').write_text(json.dumps(end,indent=2)+'\n')
print(json.dumps({'status':'SAVED','utc':now,'initial_sha256':initial['sha256'],
                 'exact_checks':sum(counts),'script_seconds':result['cost']['runtime_seconds'],
                 'final':end['final'],'result':end['result']},indent=2))
