# Independent mathematical review of the continuum-packet channel theorem

Date: 28 October 2026. Reviewer: successor physical-mechanism contributor, separate from the root theorem producer. The reviewer did not author the root theorem or its continuum-kick program.

Reviewed source: `../theory/CONTINUUM_PACKET_CHANNEL_THEOREM.md`, 10,034 bytes, SHA-256 `63d64c94ef4965e22c504360f3e04a5fdb5df1342998fa300947c1683dc16c8d`.

**Decision: accepted at the stated mathematical scope.** This is a proof-text review. It does not independently replay or certify the root's interval benchmark program, the P2 physical circuit, or the literature's priority claims.

## Precision correction made during review

An earlier draft called the generator “integrable bounded self-adjoint.” The reviewer requested clarification because continuum Weyl families are strongly continuous but generally not continuous in operator norm. The final source explicitly requires a strongly measurable generator with an integrable norm bound and uses strong vector integrals. It does not claim Bochner integrability into the operator-norm topology. This correction supports the unitary propagator and variation-of-constants proof without changing the error constants. The amended paragraph was reread before hashing the final source above.

## Checks supporting acceptance

1. **Weyl signs and source matrix elements.** With inner products conjugate-linear first, `W(beta)|alpha>=exp(i Im<alpha,beta>)|alpha+beta>` has the correct phase. The displayed coherent Weyl kernel and displaced `|0>,|1>` matrix elements are consistent with that convention. The latter restrict the input polynomial, not the output Fock space.

2. **Full-output operator residual.** On the finite-dimensional declared input code, variation of constants yields equation (1), including the initial defect and every internal discontinuity. Taking the operator norm retains arbitrary reference entanglement. A scalar average over input columns would not suffice; the theorem explicitly uses the largest eigenvalue of the complete `R†R` matrix.

3. **Polar repair.** If the raw map is within epsilon<1 of the exact isometry, its singular values lie in `[1-epsilon,1+epsilon]`. The positive inverse square root exists, and the polar isometry differs from the raw map by at most epsilon. Triangle inequality gives at most 2epsilon in isometry norm and hence the stated full-output half-diamond bound. The repair is a mathematical CPTP approximation, not a measurement success probability.

4. **Exterior directions.** Evaluating `H²` after projection would underestimate the residual. Equations (1)–(2) correctly require the actual generated packet directions and the full-space Gram kernel. There is no implicit bath photon cutoff. The source can also remain infinite dimensional, but only when its stated actions and overlaps are evaluable and enclosed; the theorem makes no automatic claim of that capability for every source Hamiltonian.

5. **Ultraviolet regularity.** Finite phase mass makes `f_t` strongly continuous by dominated convergence. It need not give a derivative when the second frequency moment diverges. Equation (3) follows from `|exp(ix)-1|<=min(|x|,2)` split at Omega. Fixed packets with absolutely continuous source coefficient maps avoid differentiating `f_t`. The inherited baseline source explicitly records its ideal-line infinite second moment, so this issue is grounded rather than hypothetical.

6. **Compression.** For the stated input isometry, `D=V†(I-P)V` is positive, and `delta²=||D||<1` ensures the compressed normalization exists. The identity `V†V_tilde=sqrt(I-D)` gives exactly `||V-V_tilde||²=2(1-sqrt(1-delta²))`. This is an amplitude-scale correction. For bath-span projection, `G_A-C†G_B^+C` is the correct discarded Gram form. Ill-conditioned numerical pseudoinverses still need independent enclosure, as stated.

7. **Detector instrument.** Positive kernel domination on every finite list gives bounded positive forms on the quotient/completed visited one-particle space. The passive dilation then permits noncommuting input effects while retaining commuting physical output-port projectors. Equations (5)–(7), including matrix index orientation and inclusion-exclusion, agree with the separately reviewed detector interface. Efficiency, collection and unobserved loss are genuine extra data; scalar source phase density alone is insufficient.

8. **Rare events and dependence.** Equation (8) follows by applying the contraction `F^(1/2)` to the vector difference, then using the triangle and reverse-triangle inequalities. It remains valid for an unnormalized approximate map. The wrong-record marginal bounds are the correct Frechet bounds for the event “empty port clicks and occupied port does not.” The product requires independence and is not justified by the marginals alone.

## Limits retained

The theorem is conditional on bounded interaction-picture dynamics, evaluable/enclosed kernels and source actions, an actual small residual or other proved isometry error, and a specified detector transfer. It proves neither efficient packet growth nor uniform algorithmic completion. Its code-input channel statement does not become an unrestricted full-source diamond theorem. Thermal input states, finite duration replacements of ideal kicks, actual P2 circuit controls and additional loss mechanisms must be supplied separately.

The continuum-kick receipt and program were read for orientation, but are being reviewed independently by another contributor. This review does not claim an independent numerical replay of them.

## Producer self-check of the separate low-pump coefficient

The reviewer also rechecked their own result in `LOW_WORK_MULTIPLIER_CHALLENGE.md`. This subsection is explicitly a **producer self-check**, not an independent review of that result.

The positive free bath spectrum and the odd-source selection rule place the entire first-vertex vector above source energy `h f_a`. The vacuum norm is exactly `(1-exp(-2x_a))(1-exp(-2v))/4<=1/4`, including all odd bath multiplicities for every finite phase variance v. The Fourier bound for `sin^4(pi t/T)` is uniform for `nu T>2`; applying it to both pump harmonics at `Delta=f_a-f_p` gives the stated coefficient bound.

A separate scalar reconstruction within this self-check uses Machin's formula and rational alternating arctangent sums to certify `pi>3.14159`. The resulting squared-norm upper rational is

`102400000000 / 969837594664580591623921`,

which is strictly below `1.056e-13`. `ROOT_THEOREM_REVIEW_RECEIPT.json` preserves the rational pi enclosure and hashes. No all-orders or physical dark-count bound follows, and none is claimed.
