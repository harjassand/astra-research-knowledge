"""Build Cycle06 deliverables only after a zero-pending final inventory."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2]; A=R/'work/agents'; S=R/'work/state'; O=R/'outputs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
gate=json.loads((S/'CYCLE06_READY.json').read_text())
assert gate['pending_worker_reports']==0 and gate['unclassified_artifacts']==0
packets={
 'kms-regularity':{
  'canonical-origin':'variance_monogamy_sol/cycle06_kms_entropy',
  'independent-origin-and-review':'tensor_frame_sol/cycle06_kms_endpoint',
  'hostile-audit':'algebra_proof_recon/cycle06_kms_c4_audit',
  'primary-prior':'dilation_literature_luna/cycle06_kms_counterexample_priority',
  'earlier-primary-status':'dilation_literature_luna/cycle06_kms_regularities',
  'weak-endpoint-independent':'complexity_proof_recon/cycle06_weak_regular',
  'weak-endpoint-audit':'variance_monogamy_sol/cycle06_weak_endpoint_review',
  'weak-endpoint-prior':'dilation_literature_luna/cycle06_weak_endpoint_prior',
  'general-operator-gate':'covariant_review_sol/cycle06_global_weak_bridge',
  'operator-tools-audit':'algebra_proof_recon/cycle06_operator_tools_audit',
  'general-endpoint-attack':'complexity_proof_recon/cycle06_general_endpoint_attack',
  'report-preservation-repair':'complexity_proof_recon/cycle06_preservation_repair',
  'root':'root_cycle06',
 },
 'canonical-energy':{
  'origin':'covariant_review_sol/cycle06_scalar_gate',
  'independent-and-review':'broadcasting_proof_sol/cycle06_scalar_blind',
  'orbit-integral-audit':'broadcasting_proof_sol/cycle06_orbit_integral_audit',
  'gns-reference-corollary':'broadcasting_proof_sol/cycle06_gns_reference_corollary',
 },
 'recoverable-records':{
  'origin':'foundational_transfer_sol/cycle06_record_transfer',
  'independent-and-review':'spin1_anisotropic_sol/cycle06_double_markov_review',
  'markov-prior':'broadcast_literature_luna/cycle06_markov_intersection_prior',
  'record-prior':'broadcast_literature_luna/cycle06_record_prior',
  'classical-basis-gate':'broadcasting_blind_review/cycle06_cq_stability',
 },
}
readmes={
'kms-regularity':'''KMS ENTROPY REGULARITY: EXACT COUNTEREXAMPLES AND REFERENCE SYMMETRY
Cycle06. Natural logarithms; ordinary trace. These are internal research
results, not externally reviewed or proof-assistant certified mathematics.
Historical priority remains UNKNOWN. Nothing was published or merged.

MAIN RESULT
The strong clause of Kastoryano--Temme Conjecture19 (arXiv1207.3261v2 and
the checked 2013 journal version) fails. Its reversibility convention is
KMS symmetry, Gamma G=G*Gamma, Gamma(X)=sqrt(sigma)Xsqrt(sigma).
Its p=1 strong inequality is J>=4E, where for positive Heisenberg generator L,
 J=Tr[L_*(rho)(logrho-logsigma)],
 E=Tr[sqrt(rho) Gamma^(1/2)L Gamma^(-1/2)(sqrt(rho))].
The weak p=1 requirement J>=2E is proved here for ALL qubit KMS generators;
higher dimensions and arbitrary quantum reference extensions remain open.

SIMPLE SOURCE-DERIVED WITNESS
V=[[0,1],[2,0]], sigma=diag(1,4)/5,
L(X)={V*V,X}/2-V*XV, rho=[[1/4,-2/5],[-2/5,3/4]].
This is a primitive KMS, non-GNS qubit generator. Exact algebra gives
 E=(10-sqrt11)/(4(10+sqrt11)),
 J=log2/2 + 7/(20sqrt89) log[(10+sqrt89)/(10-sqrt89)],
and J-4E<-3/125. The generator is in Liu--Wan--Wu2609.13726v1;
the endpoint failure is reconstructed here, not asserted by those authors.
See root/LWW_SOURCE_ENDPOINT_DERIVATION.txt and its exact rational replay.

INDEPENDENTLY CONSTRUCTED STRONGER-SCOPE WITNESS
canonical-origin/BASELINE_STRONG_C4.txt gives a different primitive qubit
Poisson generator from an explicit pure canonical EB channel. It has an
actual two-output broadcaster and a positive transformed channel spectrum.
At rho=[[24/425,1/1700],[1/1700,401/425]], exact arithmetic proves
J-4E<-7*10^-8. The witness survives strict positivity and all channel
quantifiers. hostile-audit/AUDIT_FROZEN_v1.txt reconstructs legality and
the source convention and gives a separate rational fixed-state certificate.
An additional independent original witness is preserved in
independent-origin-and-review/STRONG_ENDPOINT_COUNTEREXAMPLE.txt.

STRUCTURAL CONSEQUENCE
Within finite KMS quantum Markov generators, the constant4 endpoint holds
for EVERY faithful qubit PRODUCT REFERENCE STATE tau and every faithful
joint rho precisely when the generator is modular covariant, equivalently
GNS symmetric. In fact ONE fixed faithful tau, even I/2, suffices if ALL joint
states are tested: J,E are independent of tau. The separate reference-scope
erratum supersedes an earlier overrestrictive warning. An additional physical
marginal constraint is not silently covered. The proof turns any modular-frequency
mixing into a commutant-to-coherence coupling with a two-level reference.
A Hessian with a zero commutant block cannot be positive with that coupling.
Every nonmodular generator therefore gives a strict violation after such
an extension; small reference replacement makes it primitive if needed.
Only the added replacement is GNS in this construction; the total is KMS
and generally non-GNS. Read the explicit primitive-scope clarification.
The exact final review and dependency status is recorded in
root/CYCLE06_DEPENDENCY_CLOSURE.txt.

GLOBAL QUBIT POSITIVE THEOREM
weak-endpoint-independent/INDEPENDENT_BASELINE.txt proves J>=2E for EVERY
KMS-symmetric qubit quantum Markov generator and every faithful qubit state,
without primitivity or modular covariance. A fresh exposed analytic audit
and separate channel, singular-state and classical-reference closures are
in weak-endpoint-audit/. This supersedes the earlier merely local Hessian
scope, while preserving that frozen result. Every stationary KMS qubit
channel is covered by Poissonization, even with negative weighted spectrum.

The proof reconstructs all finite KMS generators using Hermitian noises
and a Lyapunov equation. Exact qubit algebra reduces the nonlinear endpoint
to a concave scalar quadratic and a hyperbolic kernel inequality. The scalar
inequality has a separate blind elementary proof. The stronger full PSD
kernel has a Hardy-space Gram proof, independently audited after exposure.
Arbitrary quantum reference extensions and system dimension>=3 remain open.
The exact general-dimensional quadratic operator and failed stronger lifts
are preserved in general-operator-gate/ and general-endpoint-attack/.

WHAT REMAINS OPEN
The constant4 counterexamples do not refute constant2. The successful qubit
proof does not establish higher-dimensional or completely amplified weak
regularity, all p regularity, or an optimal constant.
The source's earlier special amplified near-stationary family has J/E>=4;
this remains a valid scoped failed route, not a global assertion about its
generator. Both the failed route and the successful far-state witness are
preserved. The stronger fidelity-square shortcut also fails separately.

VERIFICATION AND NOVELTY
The counterexample has analytic proofs, exact interval certificates and a
fresh hostile audit. The classification has independently reconstructed
necessity and separately checked sufficiency with exact scope. Primary
versions, hashes, source status and failures are retained. A bounded search
found no checked prior statement of the classification converse; this is
not a novelty certificate. The foundational10/10 objective remains unmet.
Copy scripts to scratch before replay: some write adjacent result files.
MANIFEST.json records copied bytes, not mathematical truth.
''',
'canonical-energy':'''TRACE DISTURBANCE FROM THE CORRECT CANONICAL KMS ROOT ENERGY
Cycle06. All trace distances are HALF trace norm. Internal proof status
and exact review closure are in the sibling kms-regularity/root packet.

Fix finite faithful sigma and a pure decomposition sigma=sum p_i pi_i.
Let Psi(X)=sum p_i Tr[sigma^-1/2 pi_i sigma^-1/2 X]pi_i be the corresponding
physical canonical EB channel, and T=Gamma^-1/2 Psi Gamma^1/2.
For every density rho, including singular inputs, define
 E=Tr[sqrt(rho)(I-T)sqrt(rho)], e=T_trace(rho,Psi rho).
Then e^2<=(1+1/sqrt2)E. Arbitrary overcomplete ensembles are covered;
finite-dimensional pure measure ensembles have exact finite representations.

A distinct block-column proof gives, for every quantum reference R,
 e_R^2<=(2+sqrt2)E_R,
 E_R=Tr[sqrt(rho_RB)(id_R tensor (I-T))sqrt(rho_RB)].
The reference may be any separable normal system; B remains finite and
sigma faithful. There is no reference-dimension or spectral-floor factor.
The map id_R tensor Psi is NOT treated as a global pure EB map. The proof
uses an explicit block-column commutator lemma instead of scalar purity.

The mechanism is an exact frame representation and a split of energy into
two nonnegative terms, followed by Hilbert--Schmidt commutator bounds. It
does not use the false nontracial operator Jensen shortcut or the false
stronger fidelity-square bound. Those failures remain preserved.

This closes the trace-distance-versus-root-energy gate. It does not prove
that genuine entropy production dominates that energy for general KMS
generators. In particular, universal constant4 has just been refuted. The
weaker constant2 bridge is now proved for qubits, while the unrestricted
raw broadcaster/optimized radius power theorem remains a separate obligation.

INTEGRATED DISTURBANCE CONSEQUENCES
For ONE fixed comparator Psi, if e(rho)^2<=A J(rho) for every state along
a stationary channel's Poisson orbit, entropy integration and the exact
Lipschitz cone give e^3<=6 A D(rho||sigma) b, b=T_trace(rho,Phi rho).
Together with the prior compatible-channel C4 energy construction this gives
e^3<=(6+3sqrt2)D b in the tracial case, and
e^3<=12(1+1/sqrt2)D b for arbitrary faithful KMS self-compatible QUBIT Phi.
The first bound extends to every GNS/modular-covariant stationary compatible
channel with arbitrary faithful sigma, using the unaveraged comparator.
For an arbitrary separable normal quantum reference it gives
e_R^3<=(12+6sqrt2)D(rho_RB||tau_R tensor sigma)b_R.
When rho_B=sigma and tau_R=rho_R on support, the entropy term is I(R:B).
There is no reference-dimension factor. The compression-plus-flag proof
passes from finite to normal references and retains the SAME comparator.
In each case Psi is the same sigma-dependent canonical EB comparator for
all input states. The nonmodular qubit consequence is closed by the global
qubit theorem; the earlier audit's conditional wording is historical.
These statements preserve the stationary common-channel interface. They
are not claims about arbitrary raw broadcasters or optimized state-family
radii. Quantum-reference powers are proved in the GNS case; the nonmodular
qubit power is scalar only. No unrestricted nontracial
power law, optimal constant, historical priority or formal certification
is asserted by this packet. Earlier frozen Cycle05 files calling this gate
open are historical; this packet and final closure record the new results.
''',
'recoverable-records':'''TWO RECOVERABLE RECORDS AND SEPARABLE RECONSTRUCTION
Cycle06. HALF trace norm, natural logarithms, normal channels.

Fix kappa_BC and actual recovery channels R_B:B->BC and R_C:C->BC,
each mapping its kappa marginal exactly to kappa. Set
D=Tr_C R_C:C->B and C_B=(id_B tensor D)R_B:B->B tensor B.
This is an actual broadcaster, whose two residuals on tau_AB are at most
eta_B and eta_B+eta_C, where eta_j=T(tau_ABC,R_j tau_Aj).
The previous local reconstruction theorem selects ONE kappa_B-preserving
EB Lambda_B from these fixed data. Then F=R_B Lambda_B is EB from B to BC,
preserves kappa, and simultaneously for every finite-information extension
 T(tau_ABC,(id_A tensor F)tau_AB)
 <=min{1,eta_B+g(I(A:B),min(1,eta_B+eta_C))},
 g(I,b)=min{1,6sqrt((I+1)/ln(1/b))} for 0<b<1, with exact zero endpoint.
The output has exactly the original A and BC marginals and is separable
across A:BC. Its BC preparations may themselves be entangled.

Universal recoveries chosen only from kappa give
eta_B<=r_B=sqrt(1-exp(-delta_B)), eta_C<=r_C=sqrt(1-exp(-delta_C)),
delta_B=I(A:C|B), delta_C=I(A:B|C).
The same F therefore satisfies the displayed bound with r_B,r_C. The
finite and separable normal versions have independent reconstruction and
exposed review. The normal CMI gate is explicitly closed using versioned
Shirokov and universal relative-entropy recovery statements. At both CMIs
zero, the SAME selected map reconstructs exactly even at infinite I.
At positive deficits with infinite I, only the trivial bound1 is claimed.

STRONGER TARGETS AND FAILED SHORTCUTS
If one CMI is exactly zero in finite dimensions, a separate HJPW-block
argument removes the I cap and gives separable error<=sqrt(other_CMI/2),
preserving A and BC. This does not extend automatically to two small CMIs.
Balanced antisymmetric states have both deficits tending to ln2 and relative
entropy of entanglement growing logarithmically. They refute a universal
linear relative-entropy shortcut, not a small-deficit trace modulus.
An information-free two-small-CMI trace theorem remains UNKNOWN.

Hayashi--Zhao2601.09995v1 states a stronger exact double-Markov
structure with a common locally readable projective label. This is a checked
prior-source statement, not an imported proof premise or externally certified
preprint theorem. Our approximate
separable/EB conclusion does not establish approximate shared projective
labels or closeness to a CQ basis. The independent CQ branch proves exact
gate reductions but supplies no valid basis-rounding theorem or counterexample;
in particular, a product-basis gap does not control arbitrary entangled bases.

DEPENDENCIES AND STATUS
This packet depends on the internally proved local theorem in the older
quantum-reference-classicality packet. Primary recovery interfaces are
pinned, and normal completion, map quantifiers and exact marginals are
audited. It is not an external/formal proof or a novelty certificate.
All origin freezes, later closures and failed arguments are retained.
''',
}
for name,parts in packets.items():
 dest=O/name; assert not dest.exists(),f'New packet already exists: {dest}'
 dest.mkdir(); rows=[]
 for label,rel in parts.items():
  source=A/rel; assert source.is_dir(),source
  for p in sorted(source.rglob('*')):
   if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc':continue
   q=dest/label/p.relative_to(source);q.parent.mkdir(parents=True,exist_ok=True)
   shutil.copyfile(p,q);rows.append({'path':str(q.relative_to(dest)),'source':str(p.relative_to(R)),'sha256':sha(q),'bytes':q.stat().st_size})
 (dest/'README.txt').write_text(readmes[name])
 save(dest/'MANIFEST.json',{'scope':'Frozen source copies; integrity only, not proof certification.',
      'copied_frozen_files':rows,'all_packet_files':[{'path':str(p.relative_to(dest)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file() and p!=dest/'MANIFEST.json']})

base=json.loads((R/'work/checkpoints/checkpoint05/CLAIM_LEDGER.json').read_text())
def add(key,statement,proof,status='internal proof; see final dependency closure for review scope',**kwargs):
 n=len(base['claims'])+1
 base['claims'].append(dict(id=f'{key}-{n:03d}',statement=statement,status=status,
  proof='work/agents/'+proof,novelty='UNKNOWN; no external validation or historical priority clearance',**kwargs))
add('KMS-STRONG-COUNTEREXAMPLE','An explicit primitive KMS canonical-EB qubit Poisson generator with positive transformed channel spectrum and an actual joint broadcaster violates J>=4E, hence the strong clause of KT1207.3261v2 Conj19.','variance_monogamy_sol/cycle06_kms_entropy/BASELINE_STRONG_C4.txt',evidence=['work/agents/algebra_proof_recon/cycle06_kms_c4_audit/AUDIT_FROZEN_v1.txt','work/agents/root_cycle06/KMS_C4_FIXED_STATE_CERTIFICATE.txt'])
add('INDEPENDENT-C4-FAILURE','A second independently constructed primitive qubit canonical-EB channel violates the same strong endpoint with an analytic fixed-state certificate.','tensor_frame_sol/cycle06_kms_endpoint/STRONG_ENDPOINT_COUNTEREXAMPLE.txt')
add('SOURCE-HIDDEN-C4-FAILURE','The LWW2609.13726v1 generator evaluated at rho=[[1/4,-2/5],[-2/5,3/4]] has exact J-4E<-3/125. This is an internally reconstructed consequence, not the source authors stated theorem.','root_cycle06/LWW_SOURCE_ENDPOINT_DERIVATION.txt',evidence=['work/agents/dilation_literature_luna/cycle06_kms_counterexample_priority/REPORT.txt'])
add('REFERENCE-C4-CLASSIFICATION','For finite KMS generators, J>=4E on all faithful joint states with a fixed faithful qubit product reference iff modular covariance iff GNS symmetry; arbitrary finite faithful references then follow.','variance_monogamy_sol/cycle06_kms_entropy/COMPLETE_C4_CLASSIFICATION_ADDENDUM.txt',closure='work/agents/root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt',erratum='work/agents/root_cycle06/CLASSIFICATION_REFERENCE_SCOPE_ERRATUM.txt',limitation='J,E are independent of the chosen untouched reference, so even I/2 suffices; a separately fixed physical marginal is a different constrained test domain.')
add('CANONICAL-SCALAR-ENERGY','For every pure sigma-Petz canonical EB channel, scalar halftrace error squared <=(1+1/sqrt2) times physical weighted root energy, with no dimension or spectral-floor factor.','covariant_review_sol/cycle06_scalar_gate/SCALAR_THEOREM_BLIND.txt',closure='work/agents/root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt')
add('CANONICAL-REFERENCE-ENERGY','For finite faithful system sigma and any separable normal reference, id tensor canonical EB error squared <=(2+sqrt2) times physical weighted root energy.','covariant_review_sol/cycle06_scalar_gate/COMPLETE_EXTENSION_INDEPENDENT.txt',closure='work/agents/root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt')
add('RECOVERABLE-RECORDS','One fixed-kappa normal EB channel B->BC reconstructs every finite-I extension with error <=rB+g(I,min(1,rB+rC)), exact A/BC marginals; same-map exact double-zero endpoint even at infinite I.','foundational_transfer_sol/cycle06_record_transfer/INDEPENDENT_BASELINE.txt',closure='work/agents/spin1_anisotropic_sol/cycle06_double_markov_review/NORMAL_CMI_CLOSURE.txt',dependency='NORMAL-LOCAL-REFERENCE-042')
add('ONE-EXACT-MARKOV','In finite dimensions, one zero CMI and other deficit delta imply separable approximation with exact A/BC marginals and error <=sqrt(delta/2), without an I cap.','foundational_transfer_sol/cycle06_record_transfer/STRONGER_GATE_AND_FALSIFIERS.txt')
add('TWO-MARKOV-ER-OBSTRUCTION','Balanced wedge states have bounded two-CMI sum but logarithmically growing relative entropy of entanglement; no universal linear ER<=K(deltaB+deltaC). This does not refute small-deficit trace stability.','foundational_transfer_sol/cycle06_record_transfer/STRONGER_GATE_AND_FALSIFIERS.txt')
add('QUBIT-WEAK-HESSIAN','Every KMS qubit CPTP map or generator satisfies the constant2 entropy/root inequality to second order at its faithful stationary state. This is local, not nonlinear/global or completely amplified.','variance_monogamy_sol/cycle06_kms_entropy/QUBIT_C2_HESSIAN_THEOREM.txt',status='internal proof with root algebraic audit; no separate fresh theorem-first reconstruction')
add('CQ-GATE-OPEN','At bounded mutual information, optimal broadcasting and optimal EB errors vanish equivalently; whether this forces distance to a CQ basis to vanish is UNKNOWN. Product-basis gaps do not control arbitrary bases.','root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt',status='exact reductions plus unresolved theorem; no valid counterexample')
add('WEAK-ENDPOINT-OPEN','Genuine KMS J>=2E in dimensions>=3 and for arbitrary quantum-reference amplifications remains UNKNOWN. The scalar qubit case is closed by the later global theorem.','root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt',status='unresolved general gate; qubit case proved internally')
add('INFO-FREE-RECORDS-OPEN','Removing the mutual-information cap when both CMIs are merely small remains UNKNOWN; one-sided Markov and antisymmetric controls do not settle the target.','foundational_transfer_sol/cycle06_record_transfer/STRONGER_GATE_AND_FALSIFIERS.txt',status='unresolved gate')
add('FALSE-SCALAR-SHORTCUTS','Exact legal canonical channels refute both the stronger fidelity-square sufficient inequality and the blind branch comparison g>=f. Neither refutes the proved trace-energy bounds.','covariant_review_sol/cycle06_scalar_gate/FAILED_ROUTES_BLIND.txt',evidence=['work/agents/broadcasting_proof_sol/cycle06_scalar_blind/BLIND_BASELINE.txt'],status='exact scoped counterexamples; no main-target counterclaim')
add('GLOBAL-QUBIT-WEAK-ENDPOINT','Every finite KMS-symmetric qubit QMS generator obeys J>=2E at all faithful states, without modular covariance or primitivity. Poissonization covers every stationary KMS qubit channel; separate singular and arbitrary classical-reference closures hold. Quantum references and dimension>=3 are not proved.','complexity_proof_recon/cycle06_weak_regular/INDEPENDENT_BASELINE.txt',evidence=['work/agents/variance_monogamy_sol/cycle06_weak_endpoint_review/EXPOSED_GLOBAL_QUBIT_AUDIT.txt','work/agents/variance_monogamy_sol/cycle06_weak_endpoint_review/GLOBAL_QUBIT_CHANNEL_SINGULAR_CLOSURES.txt','work/agents/root_cycle06/GLOBAL_QUBIT_ROOT_AUDIT.txt'])
add('HYPERBOLIC-PSD-KERNEL','K(x,y)=[x sinh(y)+y sinh(x)-4sinh(x/2)sinh(y/2)]/[2cosh((x-y)/2)] is a PSD kernel on all real x,y. Hardy-space Gram proof; separate blind elementary proof of its two-point determinant inequality.','complexity_proof_recon/cycle06_weak_regular/HARDY_KERNEL_PROOF.txt',evidence=['work/agents/variance_monogamy_sol/cycle06_weak_endpoint_review/BLIND_SCALAR_BASELINE.txt','work/agents/variance_monogamy_sol/cycle06_weak_endpoint_review/EXPOSED_HARDY_PSD_KERNEL_AUDIT.txt'])
add('ALL-KMS-LYAPUNOV-REDUCTION','Every finite KMS generator has a sum of Hermitian-noise Lyapunov representations. The general weak endpoint is equivalent to the explicit noncommutative quadratic operator M>=0; representation and reduction are proved, positivity is UNKNOWN.','covariant_review_sol/cycle06_global_weak_bridge/BLIND_BASELINE.txt',evidence=['work/agents/complexity_proof_recon/cycle06_weak_regular/INDEPENDENT_BASELINE.txt'])
add('INTEGRATED-DISTURBANCE','If one fixed comparator obeys e(rho)^2<=A J(rho) along every stationary-channel Poisson orbit, then e^3<=6 A D(rho||sigma)b, including zero and singular endpoints.','root_cycle06/INTEGRATED_DISTURBANCE_POWER_LEMMA.txt',evidence=['work/agents/broadcasting_proof_sol/cycle06_orbit_integral_audit/AUDIT_AND_CLOSED_COROLLARY.txt'])
add('NONMODULAR-QUBIT-POWER','Every stationary KMS self-compatible qubit channel admits one pure canonical EB comparator with e^3<=12(1+1/sqrt2) D(rho||sigma)b for all states. Uses global qubit J>=2E, canonical scalar trace-energy gate and prior C4 energy ordering.','root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt',limitation='Common-channel stationary interface; not arbitrary raw broadcasters, optimized family radii, or arbitrary quantum references.')
add('SHARPER-TRACIAL-POWER','For the same pure canonical C4 comparator in the stationary tracial compatible-channel setting, e^3<=(6+3sqrt2)D(rho||sigma)b.','broadcasting_proof_sol/cycle06_orbit_integral_audit/AUDIT_AND_CLOSED_COROLLARY.txt')
add('FAILED-CP-GENERATOR-LIFT','The proposed stronger assertion that minus the entropy quadratic operator M generates a CP semigroup fails exactly already for commuting dimension3. This does not refute M>=0 or J>=2E.','covariant_review_sol/cycle06_global_weak_bridge/BLIND_BASELINE.txt',status='exact counterexample to a sufficient route only')
add('OPERATOR-HARDY-KERNEL','For bounded selfadjoint operator arguments on a common space, the Hardy compression gives a PSD block kernel satisfying the exact ordered hyperbolic Sylvester identity. This does not identify the entropy operator M with a positive kernel congruence.','covariant_review_sol/cycle06_global_weak_bridge/OPERATOR_KERNEL_LIFT_EXPOSED.txt',closure='work/agents/root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt')
add('POSITIVE-SPECTRAL-POTENTIAL','For all finite faithful sigma,rho, the exact spectral Hardy potential R_K is PSD and W=z+2s-4q+4R_K. Spectral completeness cancels a required residual; the remaining entropy cross terms can be negative separately.','covariant_review_sol/cycle06_global_weak_bridge/R_K_POTENTIAL_PROOF.txt',evidence=['work/agents/variance_monogamy_sol/cycle06_weak_endpoint_review/GENERAL_DIMENSIONAL_KERNEL_IDENTITY_ADDENDUM.txt'])
add('OPERATOR-CONVEX-POTENTIAL','f(t)=(t-1)log(t)-2(sqrt(t)-1)^2 is operator convex by an explicit positive resolvent integral. Replacing physical noncommuting Q,D by sqrt(P),log(P) is not justified, so the general entropy bridge is not inferred.','covariant_review_sol/cycle06_global_weak_bridge/OPERATOR_CONVEX_POTENTIAL.txt',closure='work/agents/root_cycle06/CYCLE06_DEPENDENCY_CLOSURE.txt')
add('GNS-REFERENCE-POWER','Every stationary GNS self-compatible finite channel has one unaveraged pure canonical EB comparator with e^3<=(6+3sqrt2)Db. For arbitrary separable normal quantum reference, e_R^3<=(12+6sqrt2)D(rho_RB||tau_R tensor sigma)b_R; when rho_B=sigma and tau_R=rho_R, D=I(R:B).','broadcasting_proof_sol/cycle06_gns_reference_corollary/GNS_REFERENCE_COROLLARY.txt',limitation='GNS/modular covariance of Phi remains essential to this proof. The comparator need not be modular averaged. Not a raw unrestricted broadcaster theorem.')
base['checkpoint']='06'
base['scope_note']='New closure supersedes earlier open statuses only at stated interfaces; all historical claim bytes preserved in checkpoints. No foundational10/10, external validation, priority, or formal proof is claimed.'
save(S/'CLAIM_LEDGER.json',base);save(O/'CLAIM_LEDGER.json',base)
print(json.dumps({'new_packets':list(packets),'claims':len(base['claims'])}))
