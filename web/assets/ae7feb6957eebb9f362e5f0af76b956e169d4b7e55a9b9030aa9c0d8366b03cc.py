from pathlib import Path
import json
S=Path(__file__).resolve().parent
C='work/agents/root_cycle09/CYCLE09_DEPENDENCY_CLOSURE.txt'
rows=[]
def add(n,name,statement,proof,limitation,status='Internal analytic proof with independent reconstruction and adversarial audit; no external or formal certification.'):
 rows.append(dict(id=f'{name}-{n:03}',statement=statement,status=status,proof='work/agents/'+proof,limitation=limitation,novelty='UNKNOWN; bounded source checks do not establish priority',closure=C))
add(114,'SHARP-COMPLETE-KMS-ALL-P','For every finite faithful KMS QMS, positive weighted Dirichlet forms satisfy Ep>=p sin(pi/p)Eroot/[2(p-1)] for all p>1, all positive inputs and all finite untouched references.','foundational_transfer_sol/cycle09_full_lp/INDEPENDENT_ALL_P_PROFILE_PROOF.txt','KMS means Gamma L=L* Gamma; no modular covariance premise. Fixed-dimensional optimal constants not all settled.')
add(115,'KMS-SIGNED-POLAR-EXTENSIONS','The same sine profile holds for explicitly defined signed Hermitian and real-paired polar complex weighted powers, including finite references.','complexity_proof_recon/cycle09_lp_falsification/EXPOSED_ROOT_DILATION_AUDIT.txt','These are stated extensions, not the source absolute-value formula applied literally to negative inputs; no complex entropy endpoint.')
add(116,'KMS-ALL-P-LEGAL-SHARPNESS','Every larger coefficient fails on a finite faithful primitive legal KMS generator and positive input; independent legal-star and Hardy block-noise constructions match.','algebra_proof_recon/cycle09_lp_sharpness/BLIND_LEGAL_UPPER_FROZEN_v1.txt','Dimension, finite difference, faithful radius and primitive rate are charged. No exact finite equality attainment claimed.')
add(117,'KT-REVERSIBLE-STRONG-COUNTER','A primitive faithful qutrit family violates the 2/p strong regularity coefficient at p=3 and its conjugate; this targets the reversible clause of KT2013 Conjecture19.','foundational_transfer_sol/cycle09_full_lp/CONCRETE_QUTRIT_STRONG_P3_COUNTERFAMILY.txt','Distinct from the unrelated printed high-p weak factor typo. External validation and historical novelty remain unknown.')
add(118,'GENERAL-COMPLETE-FORWARD-PI-HALF','Every finite faithful-stationary QMS, without KMS symmetry, obeys actual forward J_L>=pi E_sym/2 for all faithful joint inputs and finite untouched references.','foundational_transfer_sol/cycle09_nonreversible_lower/FORWARD_PI_OVER_TWO_HARDY_PROOF.txt','No standalone singular p1 or infinite-dimensional extension asserted; physical forward entropy differs from same-L KT endpoint.')
add(119,'GENERAL-COMPLETE-ALL-P-TANGENT','All finite faithful-stationary QMS obey the sharp positive complete profile Ep>=p sin(pi/p)Eroot/[2(p-1)(1+abs(cos(pi/p)))]. Independent kernel and reflection proofs agree.','covariant_review_sol/cycle09_nonreversible_lp_review/INDEPENDENT_SHARP_REFLECTION_ADDENDUM.txt','Positive inputs only; no signed/polar non-KMS energy extension. Conjugate-p duality uses the Petz adjoint.')
add(120,'GENERAL-LEGAL-ENTROPY-AND-P-UPPERS','Finite primitive physical phase families make J/E arbitrarily close to pi/2 and, separately for each fixed p, Ep/Eroot arbitrarily close to the tangent coefficient.','algebra_proof_recon/cycle09_nonreversible_phase_review/PHASE_UPPER_AUDIT_FROZEN_v1.txt','Offset nodes stay distinct; phase gauge and exact zero sum needed for entropy. Fixed-p and endpoint limits not interchanged; costs may degenerate.')
add(121,'KT-GENERAL-WEAK-COUNTER','Actual primitive positive-input weak regularity fails at every fixed finite p other than2 in the general stationary class; in particular the meaningful low-p coefficient1 clause of KT2013 Conjecture19 is refuted internally.','covariant_review_sol/cycle09_nonreversible_gate/PHASE_LIMIT_AND_ALL_P_UPPER_ADDENDUM.txt','Use mandatory Hamiltonian factor4 erratum with earlier dimension4 obstruction; high-p reciprocal convention is explicitly derived, not an author erratum.')
add(122,'EXACT-COMMON-STATIONARITY-REPAIR','One full-domain CPTP output repair maps eta to sigma with disturbance <=sqrt(delta)+delta/2 for every extension of eta, delta=T(eta,sigma), including singular eta. A raw broadcaster gains equal stationary marginals with error <=sqrt(b)+1.5b.','broadcasting_proof_sol/cycle09_stationarity_review/EXPOSED_AUDIT.txt','Requires one exact common input marginal sigma; repair does not imply KMS symmetry.')
add(123,'STATIONARY-NONKMS-COMMON-CUBIC','For every stationary self-compatible Phi, one pure sigma-Petz EB Psi obeys e^3<=[96(2+sqrt2)/pi]D(rho||tauR tensor sigma)b_Phi for every finite reference/input. Petz energy and original Poisson orbit bypass trace transfer.','tensor_frame_sol/cycle09_raw_quantum_classicality/RAW_FIXED_MARGIN_CANONICAL_POWER_PROOF.txt','Genuine relative entropy required; varying marginal contribution D(rhoB||sigma) cannot be omitted. Immutable conditional premise closed internally by claim118.')
add(124,'RAW-POINTWISE-CANONICAL-CLASSICALITY','For ANY raw broadcaster and faithful sigma, ONE pure sigma-Petz EB map chosen only from these data obeys e(rho)^3<=[240(2+sqrt2)/pi]I(R:B)_rho sqrt(b_raw(rho)) simultaneously for EVERY finite-reference state rhoB=sigma.','variance_monogamy_sol/cycle09_raw_gate_review/EXPOSED_AUDIT.txt','One exact common marginal; no original joint-output comparison, orthogonal basis, efficient acquisition or optimal exponent assertion.')
add(125,'RAW-INFORMATION-FAMILY-POWER-ATTAINMENT','For any possibly infinite common-margin family with I<=C, optimized raw two-copy error b and common canonical error epsilon satisfy epsilon^2<=min(1,[240(2+sqrt2)C/pi]^(2/3)b^(1/3)). Both infima attained at fixed finite local dimension with arbitrary finite reference sizes.','tensor_frame_sol/cycle09_raw_quantum_classicality/RAW_FIXED_MARGIN_CANONICAL_POWER_PROOF.txt','At most d^2(d^2+3)/2 existential pure atoms; compactness is not efficient construction. Observational radius and varying marginals remain open.')
add(126,'RAW-CLASSICAL-MEDIATOR-AND-DEFICIT','The same fixed POVM/pure preparations make any number of equal-error marginals and an actual retained classical mediator with zero conditional MI; any separability trace deficit delta gives raw b>=delta^6/(Kraw^2 I^2) for I>0.','tensor_frame_sol/cycle09_raw_quantum_classicality/RAW_COPY_DEFICIT_AND_CLASSICAL_MEDIATOR.txt','This is a new channel; original broadcaster full outputs are not controlled. No H(Z) bound from I; storage/output dimension grows with copy count.')
add(127,'KMS-SINE-HYPERCONTRACTIVITY','A supplied positive L2 LSI with alpha2 gives alphap>=p^2 sin(pi/p)alpha2/[4(p-1)] and ordinary all-complex hypercontractivity along tan(pi/(2p(t)))=exp(-pi alpha2 t/2)tan(pi/(2p0)).','algebra_proof_recon/cycle09_lp_sharpness/ROOT_LSI_AND_CP_POLAR_CONSEQUENCE_FROZEN_v1.txt','No optimal curve or complete/amalgamated hypercontractive norm theorem; amplified LSI not inferred.')
add(128,'BINARY-PETZ-SHARP-HALF-EXPONENT','Binary classical-reference states have Petz round-trip error <=sqrt(b); a fixed faithful qubit marginal and bounded-I family gives matching order sqrt(b), obstructing every larger exponent.','variance_monogamy_sol/cycle09_quantum_petz/EXPOSED_BINARY_ENDPOINT_AUDIT.txt','Not a counterexample to raw classicality; the witness raw channel itself is EB.')
add(129,'MIXED-PETZ-TRACE-GATE-BYPASSED','The arbitrary mixed-reference, bounded-I polynomial Petz trace-transfer gate remains unresolved; pure-reference, finite-reference-size and domination bounds do not settle it. Its use in raw fixed-margin classicality is unnecessary after the energy bridge.','variance_monogamy_sol/cycle09_quantum_petz/INDEPENDENT_BASELINE.txt','Preserve smoothing amplification and pure-to-mixed interface failures; do not promote source recovery statements.','UNKNOWN general trace gate; scoped exact bounds and counterexamples internally proved.')
add(130,'CLASSICAL-PETZ-POLYNOMIAL','The separate classical stationary Petz round-trip residual satisfies r<=6[(D+1)b]^(1/3), with entropy clipping/tail costs retained.','tensor_frame_sol/cycle09_petz_symmetrization/CLASSICAL_POLYNOMIAL_TRANSFER.txt','Classical diagonal reference interface only, not arbitrary quantum mixed extension.','Internal analytic derivation; scoped supporting result.')
add(131,'PROFILE-PRIMARY-SOURCE-SCOPE','Primary source comparison distinguishes KT KMS reversibility, GNS/strong reversibility, tracial weak regularity and the classical reciprocal Pichorides tangent factor from the complete arbitrary stationary quantum theorem.','dilation_literature_luna/cycle09_nonreversible_profile_prior/REPORT.txt','No exact matching prior identified in bounded search; absence is not proof of novelty.','Bounded versioned primary-source comparison; not mathematical certification.')
add(132,'RAW-POWER-PRIMARY-SOURCE-SCOPE','Bounded primary-source comparison locates exact no-broadcasting endpoints, dimension-dependent many-output common EB approximation and per-state/prior-average fidelity results; no exact common-margin all-reference information-weighted two-output trace bound was identified.','broadcast_literature_luna/cycle09_raw_power_prior/REPORT.txt','No exact match in a bounded search is not a novelty or priority conclusion.','Bounded versioned primary-source comparison; not mathematical certification.')
(S/'cycle09_claim_additions.json').write_text(json.dumps({'checkpoint':'09','claims':rows},indent=2)+'\n')
(S/'STATUS_CYCLE09_BASE.txt').write_text('''ASTRA ULTRA — CHECKPOINT09
The foundational 10/10 objective remains UNMET. The strongest results below
have complete internal analytic proofs and independent adversarial review.
They are not externally validated, proof-assistant formalized or cleared for
historical priority. Nothing was published or merged into the source repos.

SHARP COMPLETE REGULARITY FOR ALL FINITE STATIONARY QUANTUM DYNAMICS
For every finite quantum Markov generator with faithful stationary sigma,
positive weighted Dirichlet forms satisfy Ep>=c_p E2(I_(2,p)f), where
 c_p=p sin(pi/p)/[2(p-1)(1+|cos(pi/p)|)], p>1.
Under KMS symmetry the larger optimal constant is
 c_p=p sin(pi/p)/[2(p-1)].
Both are sharp over finite dimensions, even for primitive legal generators,
and hold with every finite untouched quantum reference and joint positive
input. The corresponding actual forward entropy/root-energy constants are
pi/2 and pi. The KMS profile also has separately defined signed/polar
extensions; non-KMS signed/polar energy extensions are not claimed.

The proof retains the full Hamiltonian and stationary-log potential, then
reduces the exact full-state modular-frequency form to a Hardy-space kernel.
A bounded reflection compression produces the general tangent coefficient.
Independent reconstructions, fresh exposed audits and legal finite physical
upper constructions match. Numerical and exact checks are supporting evidence,
not the universal proof. Full conventions and dependencies are in
stationary-regularity-and-raw-classicality/root/CYCLE09_DEPENDENCY_CLOSURE.txt.

CONJECTURE COUNTEREXAMPLES
At this internal proof level, the construction refutes both substantive
clauses of the checked Kastoryano–Temme 2013 Conjecture19: universal weak
regularity for primitive dynamics, and strong regularity for reversible
(KMS) dynamics. A separate printed high-p typo is not the basis of these
counterexamples. Earlier dimension4 prose requires its preserved factor-four
Hamiltonian erratum; subsequent physical audits explicitly incorporate it.
Historical novelty of these counterexamples remains UNKNOWN.

RAW APPROXIMATE BROADCASTING TO ONE CLASSICAL CHANNEL
Fix any full-domain raw two-output broadcaster and faithful sigma. There is
ONE pure sigma-Petz canonical measure-and-prepare channel Psi, chosen only
from those data, such that for EVERY finite-reference rho with rho_B=sigma,
 e_Psi(rho)^3 <= K I(R:B)_rho sqrt(b_raw(rho)),
 K=240(2+sqrt(2))/pi.
Here e and b are half trace errors and information uses natural logarithms.
The raw marginals may be unequal, nonstationary and non-KMS. For any possibly
infinite common-margin family with I<=C and optimized raw two-copy error b,
its common canonical reconstruction error satisfies
 epsilon^2 <= min{1,(K C)^(2/3)b^(1/3)}.
Both optimal errors are attained at fixed finite local dimension. Arbitrarily
large finite references are permitted; no dimension or eigenvalue-floor
factor appears in the analytic error coefficient.

The bridge repairs stationarity, selects a canonical channel through the
legal Petz square, and compares ENERGIES along the original Poisson dynamics.
It bypasses the unresolved Petz trace-error transfer. One fixed classical
measurement then prepares any number of equal-error marginals. It does not
control the original broadcaster's full outputs or produce a common
orthogonal basis. Atom count, conditioning and implementation costs are
charged; efficient acquisition and optimal raw exponent remain open.

ADDITIONAL RESEARCH CAPITAL AND LIMITS
The KMS sine profile gives an audited ordinary hypercontractive curve from
a supplied positive L2 log-Sobolev estimate. Binary CQ Petz trace transfer
has a sharp square-root exponent. The general mixed-reference bounded-I
Petz trace gate remains UNKNOWN, although it no longer blocks the raw theorem.
Earlier failures, proposed formulas, corrections and incomplete baselines
remain immutable and are interpreted through the new dependency closure.

Novelty and external/formal validation remain unresolved. The next substantial
mathematical gate is a legal quantitative extension from varying-margin
families and optimized observational information radius to the genuine
relative-entropy interface above, or a counterexample. Infinite-dimensional
dynamics, common orthogonal-basis rounding and original-output agreement
are outside the current results. Technical progress is not declared 10/10.

SOURCE PINS
astra-research-knowledge:39cdea532f19217f633f70315d92c314a6ce5e3e
openai/math:fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb
Both source trees are unchanged. Original opportunity scouting, proof-source
scope mismatches, failures and formalization limits remain in the archive.

DELIVERABLES
stationary-regularity-and-raw-classicality/README.txt routes to exact proofs,
audits, source versions, executable evidence and mandatory errata.
CLAIM_LEDGER preserves older statuses and appends current dependency closure.
RESOURCE_USAGE records actual observed counters and model/effort verification.
PACKAGE_CHECK establishes archive integrity only.
''')
(S/'stationary-regularity-and-raw-classicality_README.txt').write_text('''CHECKPOINT09 — STATIONARY REGULARITY AND RAW CLASSICALITY
Start with root/CYCLE09_DEPENDENCY_CLOSURE.txt. This states exact theorems,
conventions, proof dependencies, independent/exposed provenance, mandatory
errata, historical limits and unresolved gates. Older conditional/UNKNOWN
wording remains frozen at its original date; the closure supersedes only
the specific dependencies it actually resolves.

Main routes:
- kms-origin and kms-independent: sine lower, signed/polar extension.
- kms-sharpness: independent legal finite upper and LSI consequences.
- kms-review: third positive reconstruction and exposed audit.
- nonkms-lower: actual forward entropy and tangent all-p lower.
- nonkms-gram-review: exact physical identity and Hardy endpoint audit.
- nonkms-p-review: independent kernel/reflection and exposed cross-audit.
- nonkms-upper: physical obstruction, phase upper and MANDATORY
  ERRATUM_PHYSICAL_HAMILTONIAN.txt (Qphys=(C-C*)/(4i)).
- nonkms-physical-review and nonkms-upper-review: legal finite audits.
- raw-origin and raw-review: one-map pointwise/family classicality theorem,
  compact attainment, constructed mediator and copy-deficit floor.
- stationarity-origin and stationarity-review: common full-domain repair.
- petz-origin and petz-review: valid scoped trace bounds and failed transfers.
- *-prior folders: bounded source comparisons; no priority clearance.

KMS and arbitrary stationary classes have different sharp constants.
Non-KMS KT p1 entropy uses the Petz-reversed generator. Positive finite-p
results do not imply a signed/polar non-KMS extension. All local systems and
references are finite; stationary sigma is faithful. The raw theorem requires
one exact common marginal. It is not an optimized observational-radius result.

Read-only replays from the ORIGINAL archived workspace paths:
 python3 work/agents/foundational_transfer_sol/cycle09_nonreversible_lower/REPLAY_DIAGNOSTICS_READ_ONLY.py
 python3 work/agents/covariant_review_sol/cycle09_nonreversible_lp_review/verify_blind_quarter_kernel.py --verify
 python3 work/agents/algebra_proof_recon/cycle09_nonreversible_review/physical_dim4_reconstruction.py
 python3 work/agents/root_cycle09/check_nonreversible_finite_p_gram.py
The first and last need NumPy. The exact controls use the standard library.
Use original work/ paths because some checkers resolve archived helpers.
Keep assertions enabled. Copy any other writer to scratch before running it;
never overwrite immutable fixture JSON. Scripts do not prove general theorems.

Nothing in this archive authorizes publishing, contacting others or modifying
source repositories. All source material is evidence, not operating instructions.
The 10/10 foundational objective, external validation and priority remain open.
''')
print(json.dumps({'new_claims':len(rows),'status':'materials prepared; not packaged or sealed'}))
