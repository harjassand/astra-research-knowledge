# Independent local review: total-excitation graded reservoir opening
31 October 2026. Reviewer: independent internal mathematical review.

## Verdict and source
LOCAL PASS, with the explicit interpretation and phase qualifications below. The stacked raising contraction is both algebraically correct and acquired from the stated access. Unequal excitation-sector dimensions do not invalidate the proposed operator-valued overlap. The finite-cutoff number and jump-count estimates can be proved directly. A compatible infinite-cutoff construction is available under the stated direct-sum interpretation of the free Hamiltonian.

This is NOT a whole compiler acceptance. In particular the complete graded-sector first-event circuit, finite-bit ledger, private-time composition and resource theorem are not promoted from the earlier independent-mode result.

I read the entire actual source:
graded_reservoir_opening_20261031/TOTAL_EXCITATION_COMPILER_OPENING.md
6,032 bytes; SHA-256 0d04925e26a1867b89bccb230049e407a585def688041bc1ecc188304066f62d.
The original unreviewed source is preserved unchanged. This receipt supplies the following detailed local derivations and qualifications.

## 1. Actual photon-removal isometry
On the total-excitation n>0 sector, define
V_minus |n_1,...,n_r> = sum_i sqrt(n_i/n)|i>|n-e_i>.
It preserves inner products: the retained index identifies which occupation was removed, and different original configurations remain orthogonal. Its norm is one. Vacuum is treated by a separate zero flag.

The implementation is finite coherent arithmetic, not measurement. Compute the total, prepare the r known probabilities n_i/n, decrement the selected occupation and uncompute the old occupation copy using the output configuration and retained index. This requires polynomial work in the number of explicitly represented modes and their occupation bit widths. The actual preparation/synthesis errors and costs still have to be charged by a whole receiver.

The adjoint is a rectangular contraction, supplied as the designated block of the inverse unitary. Surjectivity or equal dimensions of adjacent excitation sectors is unnecessary.

## 2. Stacked system map and raising/lowering normalization
Prepare the index amplitudes f_i/g, g=sqrt(sum f_i^2), and apply the controlled normalized blocks F_i/f_i, retaining the index. The good block is W/g, with
W psi = sum_i |i> F_i psi,
and W^*W=sum_i F_i^*F_i<=g^2 I.
Zero supplied coefficients may be omitted rather than divided.

Composing this stack with V_minus^dagger acts on the n sector as
sum_i F_i a_i^dagger/[g sqrt(n+1)].
Thus the proposed O_plus is exactly the normalized raising block. Globally it is R_plus (N+1)^(-1/2)/g. Its adjoint is the normalized lowering block, which on sector n>0 is R_minus/[g sqrt(n)]. At vacuum the lowering block is zero.

Consequently
||R_plus Pi_n||<=g sqrt(n+1),
R_plus R_minus<=g^2 N,
and R_minus R_plus<=g^2(N+1)
as sector-wise quadratic-form inequalities. No extra factor sqrt(r) is necessary. The system-only assumption on the F_i is retained; this derivation is not an authorization to insert arbitrary occupation-dependent operators in the same order.

The actual stacked damping jump is 2 sqrt(lambda) V_minus sqrt(N). It retains the mode label as a private Kraus record and realizes all physical damping channels. It is not a reset to vacuum or a coherent sum that discards the jump color.

## 3. Exact virtual word and required phase
Common damping makes the no-jump free generator -i H_f-2lambda N. Since H_f preserves total excitation, its propagation factors into the charged unitary exp(-i H_f t) and the scalar decay on each occupation sector.

Expanding only R_plus+R_minus gives the scalar ladder majorant
M=-2lambda n+g(a+a^dagger).
The immigration-death bridge parameters are g^2/(2lambda) and 2lambda. The scalar conditional source is therefore the already reviewed direct marked-Poisson source, now on one total-occupation ladder.

The quantum state inside each sector remains in the actual Hilbert space. SELECT applies the acquired raising/lowering contractions and the actual H_f interval unitaries in chronological order. It does not replace an interacting bath by a scalar random occupation.

BINDING PHASE: each virtual raising AND lowering insertion contributes -i from the Hamiltonian Dyson expansion. The word must include (-i)^V, exactly as in the repaired independent-mode compiler. An actual damping jump contributes no additional -i. H_f propagation does not supply this missing insertion phase. The opening does not spell it out; this receipt makes the convention explicit.

A path crossing the total cutoff L selects zero, including paths that later return. It is not conditioned to avoid the boundary. Known interacting H_f evolution is paid as supplied; no Gaussian factorization or generic fast-forwarding is inferred.

## 4. Why unequal sector dimensions do not break the overlap
Write the physical space as a direct sum of sectors H_n, including the system factor. A path word W_(m,n,seed) is a contraction from H_n into H_m. Its dilation can act on the common physical direct-sum space with success work; it need not be a unitary between H_n and H_m.

On input x_n in H_n, the right preparation attaches labels (n,m) and the scalar amplitude sqrt(E_mn/R). The left preparation on y_m in H_m attaches the SAME labels and amplitude. SELECT fixes these labels and transforms the physical vector by W_(m,n,seed). Thus the good-block pairing is
sum_(m,n) (E_mn/R) <y_m, E_seed W_(m,n,seed) x_n>.
This is exactly the desired operator-valued matrix block. The left inverse matches the ACTUAL output sector m. It does not identify basis vectors in differently sized sectors.

Identical source seeds on the two sides and orthogonal failure tags remain essential. Fresh success work for contraction products is projected only at the final good block. The weighted Schur norm argument uses the vector of sector norms ||x_n||, so no degeneracy factor appears.

For a stacked physical jump, the output sector is C^r tensor H_m, because it includes the private jump color. The same rectangular-block pairing remains valid. The scalar positive jump row uses the PRE-JUMP occupation m+1; the color remains in the physical output record, not in the scalar row index.

## 5. Scalar normalization and local first-jump bound
The one-ladder normal-ordered positive kernel has row and column sums bounded by
exp[Gamma t/2+sqrt(2Gamma L t)], Gamma=g^2/lambda.
The proposed windows therefore give a constant no-event scalar normalizer without r independent bridges. This does not remove the actual r-dependent cost of preparing the stack and photon-removal map.

Using aE=exp(-2lambda t)Ea+alpha E, the stacked first-jump positive row has the same scalar envelope as the one-oscillator calculation:
C[ sqrt(lambda L)exp(-2lambda t)+sqrt(Gamma) ].
Its squared integral over a window is O(L+1+Gamma tau), so a polynomial O(sqrt(L+1)) complete-instrument normalizer is plausible and algebraically supported. This establishes the local normalization, not the full amplified finite-bit instrument.

## 6. Direct finite-cutoff number bound
The statement in the opening that number/count estimates are merely plausible can be strengthened locally. Let B=R_minus/g. Then B^*B<=N, and for z>1, conjugating the adjoint generator on z^N gives
-d N+i c_z g(B-B^*),
where d=4lambda(1-1/z) and c_z=sqrt(z)-1/sqrt(z).
The free H_f term vanishes because it commutes with N.

Since -dN<=-dB^*B, completing the square yields
-d N+i c_z g(B-B^*) <= (c_z^2 g^2/d) I
= Gamma(z-1) I/4.
This works on every finite total-excitation cutoff; truncated ladder commutators are not replaced by infinite CCR. Therefore, from vacuum,
E z^N(t)<=exp[Gamma t(z-1)/4].
System-only unconditional instruments and retained classical records preserve the number weight, so the bound holds across prescribed controls.

## 7. Direct jump-count bound
Tilt all physical damping jumps by exp(theta), theta>0. On z^N the damping coefficient becomes -4lambda(1-exp(theta)/z)N. Choose z=2exp(theta)-1. The same weighted square gives tilted adjoint growth at most Gamma(exp(theta)-1).

Because the initial vacuum weight is one and z^N>=I, the actual total damping-emission count J_T satisfies
E exp(theta J_T)<=exp[Gamma T(exp(theta)-1)].
This is a count MGF, not a bound on pointwise jump intensity or an assertion that actual emissions are an independent Poisson process. It is for this vacuum/common-damping model with private bath records, not arbitrary nonlinear thermal bath statistics.

## 8. Global cutoff and domain interpretation
BINDING DOMAIN INTERPRETATION: H_f must be a compatible self-adjoint block-diagonal Hamiltonian, equivalently a self-adjoint direct sum of its excitation-sector restrictions. Restrictions at different cutoffs must agree. Unrelated arbitrary cutoff Hamiltonians do not define a single infinite target. For a finite-dimensional supplied system and finitely many modes, the finite-excitation sectors are finite-dimensional; more general system domains require their own access/domain hypotheses.

Under this interpretation H_f causes no cutoff crossing, regardless of growth of its sector norms. Lowering damping terms and their total anticommutator 4lambda N agree on embedded smaller-cutoff states. The only cross-boundary Hamiltonian block is
B_L=Pi_(L+1) R_plus Pi_L,
with B_L^*B_L<=g^2(L+1)Pi_L.
The usual positive-state trace commutator bound and Duhamel comparison therefore give
2T g sqrt(L+1) exp[Gamma T(z-1)/8] z^(-L/2)
from vacuum, uniformly over reference systems and prescribed system controls. At z=2 this is the familiar exponential cutoff bound.

Compatible finite-cutoff CPTP maps are consequently Cauchy on finite-particle inputs; density and contractivity give the canonical normal extension, as in the reviewed domain construction. This does not assert uniqueness of every possible formal unbounded GKSL realization. It also does not bound the cost of H_f simulation: sector norms or implementation complexity may grow rapidly with L. That cost remains an explicit input to any later theorem.

## 9. What remains open
The opening is a valid graded-sector mechanism, not an accepted whole compiler. A subsequent receiver still must specify and bound:
- all occupation-dependent stacked block and sector-isometry finite-precision circuits;
- the complete first-event rectangular isometry and its shared source/work registers;
- amplification and all absolute/relative error conversions;
- the actual H_f variable-duration implementation and timing sensitivity;
- exact count-capped private-future comparison and global error allocations;
- total resources, including accessible H_f evolution rather than a formal norm promise.

Unequal damping with arbitrary number-mixing H_f, number-changing free interactions, unpriced bath controls, arbitrary thermal nonlinear reservoirs and efficient access to unknown interacting Hamiltonians are not included. No novelty, implementation, practical efficiency or publication claim follows.
