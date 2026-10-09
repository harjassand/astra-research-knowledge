"""Build readable Cycle05 packets only after the coordinator's ready gate."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2]; A=R/'work/agents'; S=R/'work/state'; O=R/'outputs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
gate=json.loads((S/'CYCLE05_READY.json').read_text())
assert gate['pending_worker_reports']==0 and gate['unclassified_artifacts']==0
packets={
 'quantum-reference-classicality':{
  'weighted-origin':'covariant_obstruction_sol/cycle05_weighted_dirichlet',
  'weighted-independent':'tensor_frame_sol/cycle05_weighted_blind',
  'local-proof':'foundational_transfer_sol/cycle05_local_broadcast',
  'local-independent':'spin1_anisotropic_sol/cycle05_local_blind',
  'normal-extension':'broadcasting_blind_review/cycle05_normal_local_extension',
  'local-obstruction':'broadcasting_blind_review/cycle05_antisymmetric_blind',
  'root':'root_cycle05',
  'local-prior':'broadcast_literature_luna/cycle05_local_broadcast_prior',
  'weighted-prior':'broadcast_literature_luna/cycle05_weighted_prior',
 },
 'power-law-boundaries':{
  'entropy-origin':'variance_monogamy_sol/cycle05_tracial_power',
  'entropy-independent':'spin1_anisotropic_sol/cycle05_power_blind',
  'nonreversible':'variance_monogamy_sol/cycle05_bistochastic_power',
  'observational-and-failures':'broadcasting_proof_sol/cycle05_power_upper',
  'modular-and-review':'covariant_review_sol/cycle05_nontracial_entropy',
  'lower-origin':'quadratic_dilation_sol/cycle05_power_lower',
  'lower-independent':'algebra_proof_recon/cycle05_power_lower_review',
  'power-prior':'dilation_literature_luna/cycle05_power_prior',
  'dirichlet-prior':'dilation_literature_luna/cycle05_dirichlet_prior',
 }
}
readmes={
'quantum-reference-classicality':'''ROBUST LOCAL RECONSTRUCTION WITH AN UNTOUCHED QUANTUM REFERENCE
Cycle05. All trace errors are HALF trace norm; logs are natural.

STRONGEST DEFENSIBLE RESULT
For a fixed normal state sigma_B on a separable Hilbert space and an actual
normal CPTP broadcaster C:B->B tensor B, there is ONE full-domain normal EB
map Lambda_B preserving sigma_B, chosen only from C and sigma_B. For EVERY
separable quantum reference A and normal rho_AB with rho_B=sigma_B and
finite I=I(A:B), it satisfies
 e=T((id_A tensor Lambda_B)rho_AB,rho_AB)
 <=min{1,6sqrt[(I+1)/ln(1/b)]},
 b=max_j T((id_A tensor C_j)rho_AB,rho_AB), 0<b<1.
The SAME map fixes all b=0 extensions exactly, even at infinite I. Use1
at b=1. No dimension, spectral floor, Hamiltonian, or finite entropy of
sigma is required. Infinite-dimensional EB uses the trace-norm-closed
convex hull of normal product states; finite/countable outcomes are not
asserted for the limiting channel.

START HERE
 root/LOCAL_DEPENDENCY_CLOSURE.txt gives the final exact status and hashes.
 local-proof/NONTRACIAL_Q_ORBIT_CONDITIONAL_PROOF.txt is the short finite
 proof. Its historical conditional title is resolved by the separate
 local-proof/DEPENDENCY_CLOSURE.txt and final local-independent audit.
 normal-extension/THEOREM_FIRST_BASELINE.txt proves the normal extension;
 root/NORMAL_LOCAL_ROOT_AUDIT.txt and root closure discharge its finite premise.
 weighted-origin/WEIGHTED_C4_PROOF.txt and weighted-independent/BLIND_BASELINE.txt
 independently establish the new physical KMS comparator, with mutual audits.

MECHANISM AND VERIFICATION
An explicit gentle local marginal repair makes the raw channel stationary.
A broadcast-tree covariance/Schur argument gives one physical canonical EB
map in the correct weighted metric. A quadratic-energy orbit compares the
original nearly stationary state with a separately capped substate, paying
smoothing only once. Normal extension uses trace-norm compact weighted Choi
states with both marginals fixed, followed by a full-domain normal CP/TP/EB
construction. No nontracial entropy-square-root regularity is assumed.
Status: complete internal proofs, independent reconstruction of the weighted
theorem, fresh exposed local audit, root normal-extension audit, and finite
exact/numerical diagnostics with their narrower scopes. Not formal-kernel
or external certification. Primary imports and versions are pinned in files.

BOUNDARIES AND CONTROLS
The conclusion is measure-and-prepare recoverability in JOINT trace norm.
It is not closeness to a classical-on-B basis, entropic-discord continuity,
uniform channel/diamond approximation, or efficient classical acquisition.
A classical mediator can have large outcome entropy/alphabet even when its
mutual information with A is bounded. The selected channel is supplied by
an existence proof; all acquisition/representation costs remain explicit.
The unflagged antisymmetric ladder has b<=1/L, e>=1/2, I~L ln2/2, yet its
conditional state family has capacity<=2/L and replacement error<=1/L.
The shared-vacuum extension has bounded I, b<=1/L^2 and e>=1/(2L), excluding
any proposed e^2<=K(I+1)b^alpha with alpha>1. It does not exclude continuity.
The complete flagged conditional family has capacity>=ln2; do not transfer
the unflagged vanishing-capacity statement to that different family.
The standard antisymmetric state itself is highly extendible but has actual
local broadcasting optimum1/4 and EB error1/2: mere extensions do not meet
the channel-generated broadcasting premise.

General nontracial power rates and historical novelty remain UNKNOWN.
The foundational10/10 objective remains OPEN. No publication or canonical
repository merge occurred. Source versions and failures are preserved.
Scripts may write adjacent JSON: replay a scratch copy with assertions on.
MANIFEST.json certifies copied bytes and integrity, not mathematical truth.
''',
'power-law-boundaries':'''POWER RATES, EXACT LOWER FAMILIES, AND FAILED NONTRACIAL TRANSFERS
Cycle05. HALF trace errors, natural logarithms. Internal mathematical results;
no external/formal validation or historical priority clearance.

POSITIVE RATES HAVE DIFFERENT HYPOTHESES
1. Reversible bistochastic Phi and any fixed bistochastic CP Psi with
I-Psi<=C(I-Phi) satisfy e^3<=(27C/8)D(rho||I/d)b for the SAME Psi at allrho.
The independently discovered orbit average improves the first27C/4 freeze.
C4 gives e^2<=3(D+1)b^(2/3). Negative eigenvalues and singular states allowed.
2. Every raw bistochastic compatible marginal, without reversibility, has
ONE fixed C4-derived EB map with e^3<=54Db and e^2<=8(D+1)b^(2/3).
Untouched-reference budget is I(A:B)+D(rho_B||I/d_B), equal to I for tracialB.
3. With an arbitrary actual local broadcaster but fixed tracial B marginal,
gentle repair gives e^3<=54I min{1,b+sqrt(2b-b^2)}. Its proof is in the
sibling quantum-reference-classicality/local-proof packet.
4. A distinct spectral clipping argument gives e^2<=256(R0+1)b^(1/2) for
bistochastic marginal, where R0=sup Dobs(rho||I/d). R0 cannot be silently
replaced by the optimized convex-hull radius R(E).
5. For nontracial stationary, modular-covariant KMS-reversible Phi, an
ordered modular comparator satisfies e^3<=(27C/4)D(rho||sigma)b. When only
Phi is modular, averaging a canonical C4 comparator over the compact
modular group supplies ONE such comparator. General KMS alone is not enough
for the proof. The root exposed branch audit is in the sibling packet/root.

EXACT LOWER BOUND AND A REAL CORRECTION
lower-origin/VACUUM_FLAG_POWER_OBSTRUCTION.txt constructs finite algebraic
families with bounded nonzero R, optimal b2=Theta(K^-2), and
e=Theta(log K/K^2). Thus e^2<=K0(R+1)b2^alpha is impossible for EVERY alpha>=2,
including the endpoint. Full-domain broadcasters, arbitrary mixed/flag-changing
EB channels, finite designs, true convex minimax radius, and faithful noise
are handled. lower-independent/ preserves a stronger independent EB lower.
Read lower-origin/ERRATUM.txt: the ancillary summary's exact R=wR_K formula
belongs to the UNPERTURBED family. Faithful states have a separate exact
formula proved in lower-independent/FAITHFUL_RADIUS_AND_CAPACITY_EXTENSION.txt.
Its bounded-R asymptotics and the power obstruction are unchanged.

The optimized nonuniform division theorem uses delta=b_div=w max p_j,
not unrestricted optimal b2. It proves e<=3delta ln[12(R+1)/delta] and rules
out that restricted class as a small-exponent counterexample source.
Label-independent catalysts are exactly neutral. Coherent-flag versions
of the existing splitter dephase the flags and fail the promised error.

FAILED FORMULAS ARE NOT FAILED TARGETS
Exact faithful examples refute ordinary likelihood root-energy substitution,
a KMS bilinear-log entropy expression, and nontracial operator Jensen.
Those quantities are not the correct Qrho energy or genuine relative-entropy
dissipation. The canonical scalar Qrho trace comparison is still unresolved.
An orientation erratum preserves Heisenberg versus Schrodinger stationarity.
A separate three-state rare-event example has tiny SUPPLIED broadcaster
residual but constant relative-entropy DPI loss; its OPTIMAL b=e=0.
It refutes an entropy-continuity reduction, not the actual power target.

The unrestricted state-family power target remains UNKNOWN for alpha in(0,2).
The local-reference bounded-I lower family separately excludes alpha>1.
No matching optimal rate, general nontracial power theorem, or foundational
10/10 result is claimed. Read every theorem's supplied-channel and reference
conditions. Independent agreement and exact small replays are scoped evidence.
Scripts may write adjacent evidence; copy to scratch before replaying.
'''
}
for name,parts in packets.items():
 dest=O/name;dest.mkdir(exist_ok=True);rows=[]
 for label,rel in parts.items():
  source=A/rel;assert source.is_dir(),source
  for p in sorted(source.rglob('*')):
   if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc':continue
   q=dest/label/p.relative_to(source);q.parent.mkdir(parents=True,exist_ok=True)
   shutil.copyfile(p,q);rows.append({'path':str(q.relative_to(dest)),'source':str(p.relative_to(R)),'sha256':sha(q),'bytes':q.stat().st_size})
 (dest/'README.txt').write_text(readmes[name])
 save(dest/'MANIFEST.json',{'scope':'Frozen source copies; integrity only, not theorem certification.','copied_frozen_files':rows,'all_packet_files':[{'path':str(p.relative_to(dest)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file() and p!=dest/'MANIFEST.json']})

base=json.loads((R/'work/checkpoints/checkpoint04/CLAIM_LEDGER.json').read_text())
def add(n,key,statement,proof,status='internal proof with independent or root exposed audit',**kwargs):
 base['claims'].append(dict(id=f'{key}-{n:03d}',statement=statement,status=status,proof='work/agents/'+proof,novelty='UNKNOWN; no historical priority or external validation',**kwargs))
add(40,'WEIGHTED-C4','Every faithful sigma-stationary self-compatible KMS-reversible channel has ONE finite pure sigma-Petz canonical EB comparator K>=(2H^2-I)+ and I-K<=4(I-H), no dimension or spectral-floor constant.','covariant_obstruction_sol/cycle05_weighted_dirichlet/WEIGHTED_C4_PROOF.txt',evidence=['work/agents/tensor_frame_sol/cycle05_weighted_blind/BLIND_BASELINE.txt','work/agents/tensor_frame_sol/cycle05_weighted_blind/POST_EXPOSURE_AUDIT.txt'])
add(41,'LOCAL-QUANTUM-REFERENCE','For fixed finite sigma_B and actual local broadcaster, ONE sigma_B-preserving full-domain EB map works for all A/rho_AB with rho_B=sigma_B, with joint e<=min(1,6sqrt((I(A:B)+1)/ln(1/b))), exact same-map zero endpoint.','foundational_transfer_sol/cycle05_local_broadcast/NONTRACIAL_Q_ORBIT_CONDITIONAL_PROOF.txt',closure='work/agents/root_cycle05/LOCAL_DEPENDENCY_CLOSURE.txt',evidence=['work/agents/spin1_anisotropic_sol/cycle05_local_blind/EXPOSED_LOCAL_Q_ORBIT_AUDIT.txt'],limitation='No CQ-basis, entropic-discord, diamond, or efficient-acquisition conclusion.')
add(42,'NORMAL-LOCAL-REFERENCE','The same local theorem and constant6 hold for normal channels on separable infinite dimensions, finite mutual information, without a Hamiltonian or sigma-entropy assumption. Exact b0 extends even to infinite I.','broadcasting_blind_review/cycle05_normal_local_extension/THEOREM_FIRST_BASELINE.txt',closure='work/agents/root_cycle05/LOCAL_DEPENDENCY_CLOSURE.txt',evidence=['work/agents/root_cycle05/NORMAL_LOCAL_ROOT_AUDIT.txt'],limitation='EB is trace-norm-closed separable output; exact finite/countable outcomes not asserted.')
add(43,'GENTLE-MARGINAL-REPAIR','Any nu,sigma admit one full-domain CPTP R with Rnu=sigma and disturbance<=sqrt(2delta-delta^2) on EVERY extension ofnu, delta=T(nu,sigma); singular cases included.','root_cycle05/GENTLE_MARGINAL_REPAIR.txt',evidence=['work/agents/foundational_transfer_sol/cycle05_local_broadcast/NONCOMMUTING_MARGINAL_REPAIR_AUDIT.txt'])
add(44,'REVERSIBLE-POWER','Bistochastic reversible Phi and fixed physical ordered Psi give e^3<=27C Db/8; C4 gives e^2<=3(D+1)b^(2/3). Same comparator and exact endpoints.','spin1_anisotropic_sol/cycle05_power_blind/BLIND_POWER_THEOREM.txt',evidence=['work/agents/variance_monogamy_sol/cycle05_tracial_power/ORBIT_AVERAGING_ADDENDUM.txt','work/agents/spin1_anisotropic_sol/cycle05_power_blind/EXPOSED_POWER_AUDIT.txt'])
add(45,'BISTOCHASTIC-POWER','Raw bistochastic compatible marginal, without reversibility, admits fixed EB e^3<=54Db and e^2<=8(D+1)b^(2/3); reference budget I+D(rho_B||tau_B).','variance_monogamy_sol/cycle05_bistochastic_power/BISTOCHASTIC_RAW_POWER_PROOF.txt',evidence=['work/agents/variance_monogamy_sol/cycle05_bistochastic_power/LOCAL_REFERENCE_POWER_PROOF.txt'])
add(46,'TRACIAL-LOCAL-POWER','Arbitrary actual local broadcaster with fixed tracial B marginal admits same-map e^3<=54I min(1,b+sqrt(2b-b^2)).','foundational_transfer_sol/cycle05_local_broadcast/TRACIAL_POWER_ORBIT_PROOF.txt')
add(47,'TRACIAL-OBS-POWER','For bistochastic marginal and R0=sup Dobs(rho||I/d), one common EB has e^2<=256(R0+1)b^(1/2); not optimized R(E).','broadcasting_proof_sol/cycle05_power_upper/TRACIAL_POWER_PROOF.txt',evidence=['work/agents/root_cycle05/POWER_BRANCH_ROOT_AUDIT.txt'])
add(48,'MODULAR-POWER','Modular-covariant KMS-reversible stationary Phi has an ordered averaged canonical EB comparator with e^3<=27C D(rho||sigma)b/4; C4 supplies C=4 for compatiblePhi.','covariant_review_sol/cycle05_nontracial_entropy/MODULAR_COVARIANT_POWER_BRIDGE.txt',evidence=['work/agents/root_cycle05/POWER_BRANCH_ROOT_AUDIT.txt'],limitation='Modular covariance is essential to this proof; original unaveraged comparator is not covered automatically.')
add(49,'BOUNDED-R-POWER-OBSTRUCTION','Finite faithful families with bounded nonzero R have optimal b2=Theta(K^-2), e=Theta(logK/K^2), refuting every exponentalpha>=2 including2.','quadratic_dilation_sol/cycle05_power_lower/VACUUM_FLAG_POWER_OBSTRUCTION.txt',evidence=['work/agents/algebra_proof_recon/cycle05_power_lower_review/EXPOSED_AUDIT_FROZEN_v1.txt','work/agents/algebra_proof_recon/cycle05_power_lower_review/FAITHFUL_RADIUS_AND_CAPACITY_EXTENSION.txt'],erratum='work/agents/quadratic_dilation_sol/cycle05_power_lower/ERRATUM.txt')
add(50,'DIVISION-CLASS-OBSTRUCTION','Optimal flag-lowering division error delta=w maxp_j obeys e<=3delta ln(12(R+1)/delta); this class cannot refute small power exponents.','quadratic_dilation_sol/cycle05_power_lower/NONUNIFORM_DIVISION_RADIUS_OBSTACLE.txt',limitation='delta=b_div, not unrestricted optimalb2; genuine cloning/coherence remains a separate gate.')
add(51,'LOCAL-ANTISYMMETRIC-OBSTRUCTION','Shared-vacuum antisymmetric ladder has boundedI, suppliedb<=1/L^2 and e>=1/(2L), excluding local e^2<=K(I+1)b^alpha for allalpha>1. Unflagged ladder separates vanishing conditional capacity from persistent jointEB error.','broadcasting_blind_review/cycle05_antisymmetric_blind/FLAG_EXTENSION_THEOREM_FIRST_AUDIT.txt',evidence=['work/agents/root_cycle05/ANTISYMMETRIC_LOCAL_LADDER.txt','work/agents/broadcasting_blind_review/cycle05_antisymmetric_blind/EXPOSED_AUDIT.txt'],limitation='Does not refute continuity. Complete flagged conditional family has capacity>=ln2.')
add(52,'NONTRACIAL-FORM-FAILURES','Exact canonical examples refute ordinary likelihood-root substitution, KMS bilinear-log entropy, and nontracial operator Jensen; not the correct Qrho scalar or genuine entropy-production power gate.','covariant_review_sol/cycle05_nontracial_entropy/EXACT_CANONICAL_JENSEN_FAILURE.txt',status='exact scoped counterexamples, with independent exposed component audit',evidence=['work/agents/broadcasting_proof_sol/cycle05_power_upper/PURE_CANONICAL_ENTROPY_OBSTRUCTION.txt'],erratum='work/agents/broadcasting_proof_sol/cycle05_power_upper/ERRATUM.txt')
add(53,'GENERAL-POWER-GATE','Unrestricted optimized-R family power law remains unknown foralpha in(0,2); arbitrary-marginal local power remains unknown below thealpha>1 obstruction.','root_cycle05/INTERFACES.txt',status='UNKNOWN; logarithmic existence is proved, general power not established',next_gate='Control actual nonclassical trace loss in nontracial geometry, without false log/root or entropy-continuity substitutions.')
add(54,'RARE-ENTROPY-DEFICIT','A three-state classical supplied broadcaster has residual2^-n and boundedDobs but true relative-entropy DPI loss>=ln2; its optimalb=e=0.','broadcasting_proof_sol/cycle05_power_upper/RARE_ENTROPY_DEFICIT_OBSTRUCTION.txt',status='scoped exact counterexample to a proof reduction; root audit',evidence=['work/agents/root_cycle05/RARE_ENTROPY_ROOT_AUDIT.txt'],limitation='Not a counterexample to broadcasting-to-EB or any optimal power law.')
base.update(objective_achieved=False,external_validation=False,formal_kernel_replay=False,checkpoint='05',current_lead='LOCAL-QUANTUM-REFERENCE-041 and NORMAL-LOCAL-REFERENCE-042',historical_entries_note='Prior claims retain original scopes and unresolved statements; later entries and closure files supersede earlier research gates, not immutable proof bytes.')
assert len(base['claims'])==54
save(S/'CLAIM_LEDGER.json',base);save(O/'CLAIM_LEDGER.json',base)
print(json.dumps({'packets':list(packets),'claim_count':len(base['claims'])}))
