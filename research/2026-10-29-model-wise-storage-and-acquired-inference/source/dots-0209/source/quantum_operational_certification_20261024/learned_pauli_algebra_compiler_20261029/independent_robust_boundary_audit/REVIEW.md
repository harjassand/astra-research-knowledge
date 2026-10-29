# Independent review: robust Clifford discovery boundary
2026-10-29 UTC. Reviewer: review_robust_algebra_boundary.

## Decision and immutable scope
**Accepted as a conditional reduction at the specified output and query interface.** No unconditional complexity lower bound, novelty of the LPN/subspace reduction, or hardness of unrestricted quantum encoding/recovery is established. The large-gap dependency construction later in the same source note is outside this receipt's scope.

Reviewed source snapshot hashes are in `check_exact.json`. No author source was modified. The completed substantive review applies to the first section of ROBUST_SELECTION_BOUNDARY_v1.md at the recorded hash, with the clarifications below.

## Explicit theorem and interfaces
Fix d>=0, n=d+1 and 0<eta<1/2. The ordinary LPN sampling oracle draws x uniformly in F2^d, e independently Bernoulli(eta), and returns z=(x,s·x+e). Define a=(s,1), S=ker a, and the CPTP channel

  N(rho)=sum_z p(z) Z_z rho Z_z,
  p(z)=2^-n [1+(1-2eta)(-1)^(a·z)].

Positivity and normalization follow directly (the two parity classes have per-point weights (1-eta)/2^(n-1), eta/2^(n-1)). A learner may make ordinary memoryless uses of N on arbitrary states, entangled references, and inputs chosen adaptively using previous observations. Its successful classical output is an explicit efficiently evaluable Clifford encoder U on n qubits and k>=1 logical qubits. The operative encoder and receiver are specifically

  E(rho)=U[(I_G/2^(n-k)) tensor rho]U†,
  R(sigma)=Tr_G[U† sigma U].

The requested fidelity is entanglement fidelity of R N E relative to identity on k qubits and the maximally mixed logical input, equivalently the maximally entangled logical-reference test. The description must expose the Clifford circuit or binary symplectic frame in polynomial size. The theorem does not cover arbitrary independent decoder, nonlinear conditional recovery, hidden quantum programme, or an encoder without accessible classical frame.

For a Pauli error, U†Z_z U is a product P_G tensor P_L up to phase. Tracing G gives precisely the logical Pauli channel P_L rho P_L†. Its entanglement fidelity is |Tr(P_L)|²/4^k: one for identity logical label, zero otherwise. Thus Fe=p(A), where A is the all-Z intersection with the pulled-back gauge-only Pauli space T. T is a nondegenerate symplectic space of dimension 2(n-k). Since all-Z labels commute, A is isotropic inside T, so dim A<=n-k<=n-1. This dimension bound is essential; mere dimension 2(n-k) would not suffice.

For any linear A in F2^n,

  p(A)=|A|/2^n [1+(1-2eta) 1_{a in A-perp}].

If dim A<=n-2, this is at most (1-eta)/2<=1/2. If dim A=n-1 but A!=S, character cancellation gives exactly 1/2. Hence Fe>1/2 forces A=S and then k=1. A basis for S can be compiled to Z on n-1 gauge qubits, attaining Fe=1-eta. Given successful learner output, solve the binary linear equations expressing vanishing logical coordinates of U†Z_z U. This computes A, whose annihilator is {0,a}; extracting its nonzero vector returns s. All classical postprocessing is polynomial in the explicit frame size and n. Success probability is exactly inherited from the learner's genuine fidelity guarantee; no fidelity-estimation oracle is assumed.

## Channel-query reduction
A solver with classical LPN samples simulates each channel use by drawing a fresh z and physically applying the known Pauli Z_z. On any joint state rho_AR, averaging gives (N tensor id_R)(rho_AR) exactly. Conditioning on earlier outcomes and induction over the learner's adaptive circuit proves equality of the entire interaction distribution. Sampling records stay private to the simulator; no environment or error-label leakage to the learner is supplied. Each simulated use costs one LPN sample and at most n single-qubit Z operations. Therefore a polynomial-time quantum learner with the above success guarantee gives a polynomial-time **quantum algorithm for classical-sample LPN**. A classical learner directly consuming labels gives a classical LPN algorithm. These are distinct conditional implications.

Controlled coherent access to a Stinespring unitary, its inverse, coherent quantum examples, and an error-label register are not ordinary channel access and are not supplied by this simulation. Hardware-noisy controls are also not covered: the simulation and the emitted ideal Clifford circuit use the customary ideal quantum-computation model.

## Offsets and limiting cases
- s=0 causes no degeneracy: a=(0,...,0,1) remains nonzero and is extracted normally. d=0 is trivial rather than hard.
- eta=0 remains algebraically valid but parity learning is easy; eta=1/2 is uniform and no such proper code has Fe>1/2. The strict threshold is indispensable: every other hyperplane has Fe=1/2.
- eta>0 gives full Z-label support; S is a high-mass approximate error algebra, not exact support.
- A known fixed output Pauli correction changes the correctable label set to an affine intersection q+A or to the empty set. Character averaging gives mass |A|/2^n [1+(1-2eta)(-1)^(a·q) 1_{a in A-perp}]. Mass>1/2 therefore forces A=S and q in S for this homogeneous source. This verifies the source note's shift extension; the emitted shift must be explicit.
- A different source with unknown affine label offset y=s·x+b+e is NOT the displayed homogeneous model. Its high-mass set is the coset a·z=b. An unshifted linear code cannot meet the threshold for b=1. With explicit affine correction, the direction still reveals s and any correctable coset representative reveals b. Do not silently claim the homogeneous code guarantee for offset sources.
- The result neither proves quantum LPN hardness nor resolves quantum capacity, optimal unrestricted recovery, or the physical fault-tolerance cost of discovering the frame.

## Primary-source comparison
Aidao Chen, Anindya De, Aravindan Vijayaraghavan, *Learning a mixture of two subspaces over finite fields*, ALT2021, PMLR132:481–504.
Primary publication: https://proceedings.mlr.press/v132/chen21a.html
Primary PDF: https://proceedings.mlr.press/v132/chen21a/chen21a.pdf
Read on2026-10-29: Section6, Proposition20 and its proof, PDF pages18–19 (zero-based17–18). This gives the same LPN mixture with weights 2eta and 1-2eta for the full space and a codimension-one subspace, transferring subspace recovery to parity recovery. Theorem2 addresses sufficiently separated dimensions with a polynomial-feature method. The prior paper receives full credit for the nested-subspace LPN core. The scoped addition here is the gauge-isotropy/fidelity implication from an emitted physical Clifford frame plus the ordinary-channel-query simulation, not a new LPN hardness principle or a claimed practical quantum advantage.

## Reproducible checks
Run `python independent_robust_boundary_audit/check_exact.py` from the compiler folder (or run by absolute path). It enumerates every binary linear subspace for n=1,2,3,4 (counts2,5,16,67), all source secrets, four rational noise values including endpoints, and every affine translate of each proper subspace. All35,848 exact threshold checks pass. It also constructs28 actual compiler frames for n<=3, verifies their corrected Z intersection and extracted secret, and computes logical entanglement fidelity directly from gauge-block Kraus operators of dense conjugated physical errors. Maximum deviation from 1-eta is2.220446049250313e-16. These finite tests support, but do not replace, the proof above. They do not constitute an empirical hardness experiment.
