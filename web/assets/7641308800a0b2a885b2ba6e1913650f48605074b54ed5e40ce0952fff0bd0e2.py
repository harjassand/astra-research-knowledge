"""Build the readable Cycle04 checkpoint after worker freezes; no source writes."""
from pathlib import Path
import hashlib, json, shutil

R=Path(__file__).resolve().parents[2]
S=R/'work/state'
O=R/'outputs'
A=R/'work/agents'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,indent=2)+'\n')

packets={
 'effective-broadcasting-compiler':{
  'proof':'broadcasting_proof_sol/cycle04_effective',
  'independent-review':'spin1_anisotropic_sol/cycle04_effective_blind',
  'prior-comparison':'dilation_literature_luna/cycle04_effective_prior',
 },
 'classicality-extensions':{
  'radius-rate-and-obstruction':'quadratic_dilation_sol/cycle04_tradeoff',
  'independent-radius':'variance_monogamy_sol/cycle04_observational_blind',
  'exposed-radius-and-pointwise':'variance_monogamy_sol/cycle04_exposed_audit',
  'independent-infinite':'covariant_review_sol/cycle04_infinite_blind',
  'infinite-review':'covariant_review_sol/cycle04_infinite_exposed',
  'infinite-radius':'covariant_review_sol/cycle04_observational_addendum',
  'hard-family-review':'algebra_proof_recon/cycle04_hard_family_audit',
  'statistical-prior':'broadcast_literature_luna/cycle04_statistical_prior',
  'attainment-prior':'broadcast_literature_luna/cycle04_eb_attainment_prior',
 },
 'memory-obstructions':{
  'balanced-subsets':'foundational_transfer_sol/cycle04_transfers',
  'independent-orthogonality':'complexity_proof_recon/cycle04_memory_blind',
  'exposed-review':'complexity_proof_recon/cycle04_memory_exposed',
 }
}
root_files={
 'effective-broadcasting-compiler':['TREE_SAMPLING_AND_STABILITY.txt','EFFECTIVE_COMPILER_ROOT_AUDIT.txt','EFFECTIVE_FINAL_NOTES.txt'],
 'classicality-extensions':['INFINITE_DIMENSIONAL_EXTENSION.txt','INFINITE_FREEZE.json','PRIMARY_PROVENANCE.json','NORMAL_EB_OPTIMIZER_ROOT_AUDIT.txt','EXTENSIONS_DEPENDENCY_CLOSURE.txt'],
}
readmes={
 'effective-broadcasting-compiler':'''CERTIFIED CLASSICAL COMPILATION OF A COMMON EB COMPARATOR — CYCLE04

Strongest effective result: from explicit valid Gaussian-rational Choi data
for a two-output broadcaster with common bistochastic HS-selfadjoint Phi,
and rational delta>0, an exact classical Las Vegas algorithm returns ONE
pure canonical entanglement-breaking channel Psi satisfying
  I-Psi <= 4(I-Phi)+delta I
on the FULL Hermitian space. It uses at most ceil(64d²/delta²)+d outcomes.
Expected bit runtime is polynomial in d,1/delta and the full input bitlength.
Every return is exact-PSD-certified; success probability is at least1/2
per uniform fallback batch. No physical quantum calls are used to compile.

Start with proof/THEOREM_AND_PROOF.txt and proof/COSTS_AND_STABILITY.txt.
independent-review/ separates the frozen blind finite-comparator derivation
from the exposed audit of the stronger complete compiler. root/ records
the coordinator's contribution and exposed audit. The optional exact
scalar depth improvement is in proof/SCALAR_DEPTH_CERTIFICATE.txt.

Status: complete internal proof candidate and exposed adversarial PASS,
with independent finite diagnostics. The main general algorithm is proved,
not implemented or benchmarked as a generic compiler. A small exact example
returns42 outcomes and passes705 assertions. Neither finite replay nor
agreement establishes external validation, formal proof or priority.

Replay with Python>=3.10 and SymPy:
  python3 proof/verify_effective_exact.py
Its default leaves frozen evidence unchanged. Other diagnostic scripts
may write adjacent JSON: copy those to scratch before running.

Costs include dense d^6 Choi input, rational precision, randomness,
measurement and state-preparation synthesis. The large worst-case
polynomial is in d, NOT log d, and is not a practical-device claim.
The ideal returned channel is exactly canonical/unital/selfadjoint.
Finite gate implementation stays EB but only approximates those identities.
No black-box acquisition, delta0 compiler or capacity-only end-to-end
compiler is established. Priority and the foundational 10/10 goal remain open.

MANIFEST.json hashes the copied files; hash checks prove integrity only.
Original provenance paths inside files refer to the full research archive.
''',
 'classicality-extensions':'''COMMON CLASSICAL RECONSTRUCTION — CYCLE04 EXTENSIONS

All errors are half trace distance and logarithms are natural. One physical
full-domain entanglement-breaking map serves the entire stated family.
These are internal mathematical results with independent checks, not
external or formal certification. Historical novelty remains UNKNOWN.

1. Broader complexity hypothesis. With observational divergence
  Dobs(rho||sigma)=sup_effect p ln(p/q),
define R as the minimum worst-state divergence over sigma in closed conv(E).
For broadcast infimum error b, common EB error satisfies
  e <= min(1,400 sqrt((R+1)/ln(1/b)), 0<b<1,
with exact e=0 at b=0. The convex-hull center restriction is essential.
This extends the bounded-Holevo-capacity sufficient class strictly; R need
not be pointwise <=C, though R<=C+ln2. Two distinct exact separations are
preserved. Begin radius-rate-and-obstruction/OBSERVATIONAL_RADIUS_PROOF.txt,
independent-radius/BLIND_BASELINE_PROOF.txt and the exposed audit.

2. Stronger fixed-map tracial result. For ANY joint B, put sigma=I/d and
Phi=(B1+B2)/2. ONE EB Psi, chosen from B and sigma before rho, satisfies
for EVERY rho
  T(Psi rho,rho) <= min(1,500[D(rho||sigma)+1]/ln(1/b_rho)),
where b_rho=max(T(Phi rho,rho),T(Phi sigma,sigma)). The zero endpoint fixes
rho exactly; use 1 at b_rho=1. The reference residual cannot be dropped.
Start exposed-radius-and-pointwise/FIXED_PSI_POINTWISE_COROLLARY.txt.
When sigma is a tracial Holevo center in closed conv(E), this yields
e<=min(1,500(C+1)/ln(1/b)). No arbitrary nontracial linear-log rate follows.

3. Infinite-dimensional extension. On separable Hilbert space, normal
families of finite Holevo capacity OR finite convex observational radius
satisfy the same respective400sqrt modulus. Physical finite compression
and uniform tails prove the transfer; no nonnormal limiting map is used.
The frozen infinite-radius proof originally awaited the finite audit;
root/EXTENSIONS_DEPENDENCY_CLOSURE.txt records that it has now passed.

4. Separate optimizer theorem. For arbitrary normal input families and
normal target states, the minimax trace-error infimum over ONE normal EB
channel is attained. A weak-star trace-loss limit and fixed preparation
completion prove it. General optimizers may need continuous outcomes.
Finite-outcome maps give arbitrary slack for the compact families above;
an exact finite-outcome optimum is not automatic. Read
independent-infinite/NORMAL_EB_OPTIMIZER_LEMMA.txt and the separate root audit.

5. Negative and unresolved endpoints. The reconstructed finite faithful
copy ladder has b=Theta(1/L), persistent EB error and
C=Theta(2^L ln L/L); it does NOT prove sharpness of the new upper rates.
Its exact formulas and fresh exposed audit are retained. Unrestricted
dimension-free classicality, capacity-only small memory, generic efficient
acquisition, matching lower rates and foundational breakthrough are not
established. Finite diagnostics are narrower than the analytic proofs.

The earlier C4, compatible smoother, centralization and Petz proof chain
remains in ../bounded-capacity-classicality and ../universal-broadcasting-proof
and the complete research archive. Each imported premise retains its actual
internal verification status. No canonical merge or publication occurred.
Scripts may write adjacent evidence: replay a scratch copy with assertions
enabled. The package manifest certifies copies, not mathematical validity.
''',
 'memory-obstructions':'''CLASSICAL SIMULATION AND ITS MEMORY LIMIT — CYCLE04

Positive transfer: one common EB approximation of error epsilon on all
original reachable states of a supplied full-domain quantum instrument
gives ONE fixed classical edge-emitting HMM whose length-n law is within
n*epsilon in total variation, for every n. The reverse hybrid only uses
original-prefix states; reset states may leave the promised family.
This does not imply small latent alphabet, efficient acquisition or an
infinite-path total-variation guarantee. Ordinary bounded-loss decisions
also transfer. Constrained classical response benchmarks require admission
of the reconstructed Born-rule responses; see exposed-review/EXPOSED_AUDIT.txt.

Two distinct exact counterexamples rule out capacity-only memory bounds.
Balanced subsets: stationary period-three commuting process, capacity ln4,
exact broadcasting, exact edge-emitting minimum N+2 states and memory
entropy ln3+(lnN)/3. Fixed-error cardinality and entropy lower bounds are
also proved. Its output alphabet includes binom(N,N/2) subsets.
Strict Moore convention instead has minimum2N+1 and entropy
ln3+(2/3)lnN; the conventions must not be conflated.

Independent finite-field orthogonality: N=2^m-1 output symbols, capacity
ln[(2^m-1)/(2^(m-1)-1)]<ln4, exact broadcasting, exact minimum N HMM states.
Memory entropy is >=ln(Nd/B_m), with d=2^(m-1)-1 and
B_m=(2^floor(m/2)-1)(2^ceil(m/2)-1). Its transition matrix satisfies
T²=(1-beta)Pi+beta I, beta<=2/9, so it mixes uniformly. Even two-output
TV error<=.01 forces entropy >=(m/2-4)ln2 and states>=sqrt(N+1)/16.
The exact Wyner common-information value is proved separately; it is not
identified with the minimum full HMM memory entropy.

Both constructions charge physical dimension, alphabet and description
costs. Neither demonstrates quantum memory advantage: the quantum memory
also grows. They refute the proposed deduction from bounded capacity and
exact broadcasting to small classical generative memory.

Start balanced-subsets/TRANSFER_PROOFS.txt,
independent-orthogonality/INDEPENDENT_BASELINE.txt and
exposed-review/EXPOSED_AUDIT.txt. Independent baselines preceded exposure;
cross-audits and exact/numerical diagnostics are explicitly distinguished.
No formal proof, external validation, historical priority or 10/10 claim.
Scripts may write JSON; copy to scratch before replay. The full archive
preserves original relative paths needed by checks.py's input-hash checks.
'''
}
for packet, folders in packets.items():
 out=O/packet;out.mkdir(exist_ok=True)
 rows=[]
 for target,source in folders.items():
  src=A/source
  assert src.is_dir(),src
  for p in sorted(src.rglob('*')):
   if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc':continue
   q=out/target/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True)
   shutil.copyfile(p,q)
   rows.append({'path':str(q.relative_to(out)),'source':str(p.relative_to(R)),'sha256':sha(p)})
 for name in root_files.get(packet,[]):
  p=A/'root_cycle04'/name;assert p.exists(),p
  q=out/'root'/name;q.parent.mkdir(exist_ok=True);shutil.copyfile(p,q)
  rows.append({'path':str(q.relative_to(out)),'source':str(p.relative_to(R)),'sha256':sha(p)})
 (out/'README.txt').write_text(readmes[packet])
 manifest={'scope':'Integrity and frozen-copy provenance only; proof status in README and claim ledger.','copied_frozen_files':rows}
 manifest['all_packet_files']=[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts]
 save(out/'MANIFEST.json',manifest)

# Rebuild from the preserved prior ledger, never duplicate appended claims.
ledger=json.loads((R/'work/checkpoints/checkpoint03/CLAIM_LEDGER.json').read_text())
new=[]
def claim(id,statement,status,proof,evidence,limits,dependencies=None):
 new.append({'id':id,'statement':statement,'status':status,'proof':proof,'evidence':evidence,
             'limits':limits,'dependencies':dependencies or [],'novelty':'UNKNOWN; bounded primary comparison is not priority clearance',
             'external_validation':False,'formal_kernel_replay':False,'foundational_endpoint':'Useful internal advance; no10/10 resolution established.'})
claim('BCAST-EFFECTIVE-030','Explicit rational Choi data of a bistochastic HS-selfadjoint self-compatible marginal admits a classical Las Vegas expected-polynomial compiler for ONE pure canonical EB Psi with I-Psi<=4(I-Phi)+delta I on the full Hermitian space and at most ceil(64d²/delta²)+d outcomes.',
 'Complete internal constructive proof; blind finite-core reconstruction, exposed full-compiler audit and coordinator replay PASS',
 'work/agents/broadcasting_proof_sol/cycle04_effective/THEOREM_AND_PROOF.txt',[
 'work/agents/broadcasting_proof_sol/cycle04_effective/COSTS_AND_STABILITY.txt','work/agents/broadcasting_proof_sol/cycle04_effective/SCALAR_DEPTH_CERTIFICATE.txt',
 'work/agents/spin1_anisotropic_sol/cycle04_effective_blind/EXPOSED_RECONSTRUCTION_AUDIT.txt','work/agents/root_cycle04/EFFECTIVE_COMPILER_ROOT_AUDIT.txt','work/agents/root_cycle04/EFFECTIVE_FINAL_NOTES.txt','work/root_replays/cycle04/effective/EXACT_REPLAY_FINAL.json'],
 ['Polynomial in d,1/delta and full entry/accuracy bitlength, not log d.','Generic compiler proved, not implemented or benchmarked; exact finite replay only.','No physical black-box acquisition or exact delta0 compiler.','Approximate gate realization stays EB; exact canonical structure belongs to ideal rational channel.'])
claim('BCAST-OBSERVATIONAL-031','With finite convex-hull observational-divergence radius R, common EB error e<=min(1,400sqrt((R+1)/ln(1/b)) for arbitrary finite-dimensional families and b in(0,1), with exact zero endpoint; bounded R strictly extends the uniform bounded-Holevo class.',
 'Independent theorem-first derivation and exposed audit PASS',
 'work/agents/quadratic_dilation_sol/cycle04_tradeoff/OBSERVATIONAL_RADIUS_PROOF.txt',[
 'work/agents/variance_monogamy_sol/cycle04_observational_blind/BLIND_BASELINE_PROOF.txt','work/agents/variance_monogamy_sol/cycle04_observational_blind/RADIUS_CAPACITY_SEPARATION.txt','work/agents/variance_monogamy_sol/cycle04_exposed_audit/OBSERVATIONAL_RADIUS_EXPOSED_AUDIT.txt'],
 ['Center must lie in closed convex hull.','R<=C+ln2; R<=C is false in general.','Separation concept has prior literature; exact theorem priority unknown.'],['BCAST-CAPACITY-027 mechanism chain','BCAST-UNIVERSAL-022'])
claim('BCAST-TRACIAL-RATE-032','For a family with tracial Holevo center, e<=min(1,500(C+1)/ln(1/b)) and exact zero endpoint.',
 'Internal scalar smoother proof and fresh exposed adversarial audit PASS',
 'work/agents/quadratic_dilation_sol/cycle04_tradeoff/TRACIAL_CENTER_RATE_PROOF.txt',[
 'work/agents/variance_monogamy_sol/cycle04_exposed_audit/TRACIAL_CENTER_RATE_EXPOSED_AUDIT.txt','work/root_replays/cycle04/exposed_radius/EXPOSED_REPLAY_RESULT.json'],
 ['No arbitrary nontracial linear-log rate.','Existential approximation statement does not charge center or minimizer acquisition.'],['BCAST-UNIVERSAL-022','Frozen compatible-smoother and tracial Petz lemmas'])
claim('BCAST-POINTWISE-033','For each joint B and fixed sigma=I/d, ONE EB Psi works for EVERY rho with T(Psi rho,rho)<=min(1,500(D(rho||sigma)+1)/ln(1/b_rho)), b_rho=max(T(Phi rho,rho),T(Phi sigma,sigma)), Phi=(B1+B2)/2; same-map exact zero endpoint.',
 'Post-exposure strengthening with explicit fixed Petz construction; coordinator exposed audit PASS',
 'work/agents/variance_monogamy_sol/cycle04_exposed_audit/FIXED_PSI_POINTWISE_COROLLARY.txt',[
 'work/agents/root_cycle04/EXTENSIONS_DEPENDENCY_CLOSURE.txt','work/root_replays/cycle04/exposed_radius/EXPOSED_REPLAY_RESULT.json'],
 ['Reference residual is load-bearing.','No arbitrary capacity replacement or nontracial version.','Not a blind independent theorem; attribution preserved.'],['BCAST-TRACIAL-RATE-032','BCAST-UNIVERSAL-022'])
claim('BCAST-INFINITE-034','For normal families on separable Hilbert space with finite Holevo capacity C or finite convex observational radius R, the corresponding400sqrt modulus holds with normal full-domain EB maps; finite-outcome approximants achieve arbitrary slack.',
 'Independent finite-capacity reconstruction and exposed review PASS; independently proved radius reduction now has its finite dependency internally closed',
 'work/agents/root_cycle04/INFINITE_DIMENSIONAL_EXTENSION.txt',[
 'work/agents/covariant_review_sol/cycle04_infinite_blind/BLIND_BASELINE.txt','work/agents/covariant_review_sol/cycle04_infinite_exposed/POST_EXPOSURE_AUDIT.txt','work/agents/covariant_review_sol/cycle04_observational_addendum/CONDITIONAL_ADDENDUM.txt','work/agents/root_cycle04/EXTENSIONS_DEPENDENCY_CLOSURE.txt'],
 ['Normal separable-Hilbert-space interface.','Exact finite-outcome optimum need not exist.','No effective finite-rank bound from capacity or radius alone.'],['BCAST-CAPACITY-027','BCAST-OBSERVATIONAL-031','NORMAL-EB-ATTAINMENT-035 for broad optimum'])
claim('NORMAL-EB-ATTAINMENT-035','For arbitrary normal input families and prescribed normal target states on separable Hilbert spaces, minimax worst half-trace error over ONE normal CPTP EB channel is attained.',
 'Complete independent analytic lemma; coordinator exposed audit PASS',
 'work/agents/covariant_review_sol/cycle04_infinite_blind/NORMAL_EB_OPTIMIZER_LEMMA.txt',[
 'work/agents/root_cycle04/NORMAL_EB_OPTIMIZER_ROOT_AUDIT.txt','work/agents/broadcast_literature_luna/cycle04_eb_attainment_prior/REPORT.txt'],
 ['General optimizer may require continuous outcomes.','Weak-star trace-loss compactification and a fixed completion are essential.','No finite/countable optimal-outcome or efficient acquisition claim.'])
claim('MEMORY-OBSTRUCTION-036','Bounded reachable Holevo capacity and exact broadcasting do not bound classical HMM state count or Shannon memory; two exact stationary commuting constructions establish this, including a uniformly mixing N-output orthogonality family and fixed-error lower bounds.',
 'Two distinct frozen derivations, cross-exposed audits and coordinator finite replays PASS',
 'work/agents/foundational_transfer_sol/cycle04_transfers/TRANSFER_PROOFS.txt',[
 'work/agents/complexity_proof_recon/cycle04_memory_blind/INDEPENDENT_BASELINE.txt','work/agents/complexity_proof_recon/cycle04_memory_exposed/EXPOSED_AUDIT.txt','work/agents/complexity_proof_recon/cycle04_memory_exposed/ORTHOGONALITY_ADDENDUM.txt','work/agents/foundational_transfer_sol/cycle04_transfers/ORTHOGONALITY_EXPOSED_AUDIT.txt','work/root_replays/cycle04/memory/checks.json'],
 ['Balanced exact minima use edge-emitting convention; strict Moore minima differ.','Output alphabet and quantum memory grow and are charged.','No quantum memory advantage or fixed-alphabet obstruction claimed.','Wyner common information is not automatically minimum full HMM memory entropy.'])
claim('DECISION-HMM-TRANSFER-037','One common EB approximation of original reachable states within epsilon gives one fixed supplied-instrument classical HMM with length-n total-variation error<=n epsilon, and simulates all ordinary bounded-loss decisions within epsilon.',
 'Internal full proof and fresh exposed audit PASS with explicit benchmark-response qualification',
 'work/agents/foundational_transfer_sol/cycle04_transfers/TRANSFER_PROOFS.txt',[
 'work/agents/complexity_proof_recon/cycle04_memory_exposed/EXPOSED_AUDIT.txt','work/agents/complexity_proof_recon/cycle04_memory_exposed/COUNTERS_AND_FAILURES.txt'],
 ['Full-domain instrument supplied; reverse hybrid uses original-prefix states.','No small memory or efficient acquisition.','Constrained benchmark A2 must admit reconstructed Born-rule decoder responses.','No ancillary/diamond converse or infinite-path TV bound.'],['Any separately established common EB error premise'])
claim('BCAST-RANK-TWO-038','For every unital self-compatible channel, C2 variance inequality holds for Gram rank<=2; one common canonical comparator exists on each fixed <=2-dimensional Hermitian span, without HS-selfadjointness or invariance.',
 'Theorem-only independent derivation and coordinator exposed audit PASS; exact scoped C2 exclusions replayed',
 'work/agents/tensor_frame_sol/cycle04_sharp/RANK_TWO_VARIANCE_THEOREM.txt',[
 'work/agents/root_cycle04/SHARP_FRAME_ROOT_AUDIT.txt','work/agents/tensor_frame_sol/cycle04_sharp/SEVEN_RAY_FINITE_CONE_EXCLUSION.txt','work/agents/tensor_frame_sol/cycle04_sharp/MUB_RANK_FIVE_EXACT_EXCLUSION.txt','work/agents/tensor_frame_sol/cycle04_sharp/GLOBAL_GATE_AND_FAILED_TRANSFERS.txt'],
 ['Arbitrary-rank global C2 remains UNKNOWN.','Separate scalar roofs and rank-two support inequalities do not aggregate.','Rank-five qutrit dual bound27/4 closes that candidate only.'])
claim('HARD-FAMILY-CAPACITY-039','The finite copy ladder has exact capacity C=(1/L)sum_j ln binom(2^j+d-1,2^j); its faithful perturbation has a separate exact entropy formula. Both have b=Theta(1/L), EB error approaching1 and C=Theta(2^L ln L/L) at d=L2^(L-1).',
 'Internal analytic reconstruction, exact small-object replay and fresh exposed all-channel proof audit PASS',
 'work/agents/quadratic_dilation_sol/cycle04_tradeoff/HARD_FAMILY_AND_CAPACITY_PROOF.txt',[
 'work/agents/algebra_proof_recon/cycle04_hard_family_audit/AUDIT_FROZEN_v1.txt','work/agents/quadratic_dilation_sol/cycle04_tradeoff/FAILED_ROUTES_AND_SCOPE.txt','work/root_replays/cycle04/tradeoff/EXACT_REPLAY_RESULTS.json'],
 ['Known ladder mechanism; no novelty claimed for it.','Does not establish sharpness of logarithmic upper rate.','Balanced-prior accessible information is not maximum-prior accessible capacity.'])
ledger['claims']+=new
ledger['checkpoint']='04'
ledger['objective_achieved']=False
ledger['cycle04_scope']='New mechanism escalation, not corpus coverage. No canonical merge or publication.'
save(S/'CLAIM_LEDGER.json',ledger)
print(json.dumps({'new_claims':len(new),'total_claims':len(ledger['claims']),'packets':list(packets)},indent=2))
