# Conditional local-surgery extension to the simple one-body-reset compiler
2026-10-30. Candidate reduction with explicit inputs; not asserted independently audited.

Use the monomial gauge and commuting combined bad flags C_h from MONOTONE_COMPILER_FLAGS.md. Let V_ext=sum_A f_A include R identical unary tokens for each C_h, and W_ext=sum_A |A|f_A. Let D_h^bad be the actual nonnegative bad-source reset decrement. Required independently established inputs:

(A) Raw reset monotonicity, with strict bad charge:
L_phys V_ext<=-kappa sum_h Q_h(1-C_h)d_h-kappa sum_h D_h^bad,
d_h=(I-Phi_h^*)V_ext>=0,
D_h^bad>=c_bad C_h sum_{A containing ALL h tokens} f_A.
Here actual resets need not be classical arbitrarily; the tailored monomial gauge or root's pinching proof establishes the operator inequality. C_h=1 implies Q_h=1.

(B) No clean creation of flags; every raw physical reset adjoint preserves the joint syndrome/label diagonal algebra. On a buffered region with all C=0, the actual gauge generator agrees with the legal direct fresh-K model. H commutes every C.

(C) Geometric-blocker circuit credits commute EVERY C, and their data channels do likewise. Thus Z_h and T preserve mask blocks. At nu=0 the credit B_h is Q_h and sqrt(B_h)=Q_h; Z_h maps joint-diagonal observables to joint-diagonal observables. Uniformly in finite local dimension,
||sqrt(B_h(nu))-Q_h||<=C nu,
||Z_h(nu)-Z_h(0)||_cb<=C nu.
The square-root estimate follows from the explicit available 2x2 block (small eigenvalue O(nu^2)) and the diagonal blocked/dark blocks; generic square-root Holder continuity alone would give the wrong power.

## Local bad-support charge
For any fixed-radius support X and any positive animal f_A whose relevant support meets X, let Q_X=I-product_{j in buffered X}(1-C_j). Then
sum_{A meeting X} Q_X f_A <= C_X sum_{j in buffered X} D_j^bad,
after summing over a bounded-incidence family of X, with a uniform constant.
Proof: Q_X<=sum_j C_j. Complete each source A to a connected bounded patch joining A's intersection with X to all R j-tokens. The added size, local weight ratio, and preimage multiplicity are fixed constants. Its target contains every j-token and is paid by (A). Each j belongs to only boundedly many X. No extra |A| factor is introduced by this charge.
The same argument bounds any nearby hypothetical d_h Q_X by a constant times these D_j^bad, since d_h itself is a bounded sum of local animal differences.

## Diagonal bad terms and cross-mask terms
Expand the exact first-order generator
L_phys+t sum_h[L_phys,Z_h]
on V_ext, grouping each commutator into its fixed buffered local support X. On P_X=I-Q_X its clean block is the already audited legal geometric-blocker calculation (remote flags are spectators). The omitted bad diagonal blocks have local relative norm O(t kappa); the local charge above bounds their positive part by C t kappa sum D_j^bad. Choose t small to absorb into the raw bad-reset loss.

At nu=0, raw V_ext, L_phys V_ext and Z_h V_ext are joint diagonal. Hence the cross-mask blocks P_X[L_phys,Z_h]V_ext Q_X vanish at nu=0. The local square-root estimate in (C), bounded local generators, and H commutation with C give their relative norm O(kappa nu). For each animal, conjugate by f_A^{-1/2}; local orbit ratios are bounded because only a fixed number of syndrome/token factors are affected. Since P_X,Q_X commute f_A, the block Young inequality gives
±t(cross block)<=delta Q_X f_A+C_delta t^2 nu^2 P_X f_A.
The first term is paid by the bad-support charge. Summing the second over local supports costs C t^2nu^2 W_ext. Restore kappa throughout.

Missing clean service d_h Q_X is also bounded by D_bad and absorbed into its much stronger instantaneous kappa-rate loss. Thus the clean-range first-order estimate extends, conditionally on (A)-(C), to
(L_phys+t sum[L_phys,Z_h])V_ext
 <=-c t kappa nu^2 sum_h d_h-c' kappa sum_h D_h^bad,
up to terms already absorbed and the usual sparse-animal CN allowance.

## Extended weighted coverage
Flag-dense animals are charged directly to D_bad by completing one occupied flag's token bundle and bounded connection patch. Syndrome-dense animals use the original component-container proof. Extra occupied flag tokens in a completed component can only improve its weight ratio. Enlarge the fixed geometry/containers to include local token bundles; all sizes and incidence constants remain bounded. This should yield
W_ext<=C(sum_h d_h+sum_h D_h^bad)+C0N.
A full written coverage proof is still required; one must split on flag versus syndrome density rather than treating arbitrary flags as error components satisfying FGL confinement.

## Exact finite-depth remainder and noise
The same inverse-circuit local expansion yields a remainder O(kappa t^2) in local cb norm. The joint syndrome/flag local-orbit bound gives C kappa t^2 W_ext. Choose t sufficiently small relative to nu^2 times the actual coverage constant. Push through the positive unital T to obtain the desired physical drift for T(V_ext), conditional on the stated inputs. The Stinespring local-noise lemma then controls arbitrary continuous local Hamiltonian/Lindblad/shared-bath perturbations by epsilon C T(W_ext).

This reduction makes the remaining obligations explicit: prove raw bad-reset charge (A), the monomial-gauge identities (B), the uniform square-root/mask estimate (C), and extended coverage. It does not identify dirty resets with intended Phi_h, discard controller coherences, or assume an effective Poisson clock.
