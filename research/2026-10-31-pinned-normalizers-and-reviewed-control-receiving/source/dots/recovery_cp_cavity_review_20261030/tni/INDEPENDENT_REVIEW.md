# Independent review: CP/TNI cavity extension beside a native bank
30 October 2026. Frozen source in sources/ROOT_TNI_CAVITY_RECEIVING.md, SHA256 c82c4e3d3dc5e78bbace64a5ad98d1be4123d2b5c017704f9b5b5903b2938372. Earlier core and approximate-gate cavity receipts retain their own scope.

## Verdict

**PASS for the CP/TNI, not-necessarily-centered local-perturbation extension of the finite scheduled cavity theorem.** Its conditional native-killed application is sound with the explicit logical-factorization and common-source-domain requirements below. The accompanying TRACE_FACTOR_COMPLETION.md supplies a precise factor-two normalization result under those requirements.

This does not independently prove the native bank's logical factorization, its full-versus-killed boundary estimate, or a complete concurrent hybrid architecture. A processor-independent cut is necessary here but does not by itself imply native logical identity.

## 1. Positivity and contraction survive the TNI replacement

For any selected processor block R, the short-step map Tr_R exp(hK) E_R is CP/TNI, is the identity at h=0, and has derivative Tr_R K E_R. In the finite bounded model its repeated-product limit is a CP/TNI semigroup. Tensoring the identity on R and restoring the independent intended CPTP generators on R gives

 K^R=P_R K+sum_(j in R)L_id,j.

This is CP/TNI. Trace preservation of the intended gates is sufficient for the same identity as in the core proof, including nonunital gates. Convex combinations of these generators remain CP/TNI. A CP/TNI map has complete trace norm at most one, since its adjoint maps I to an operator between0 and I. Equality to one was never required in the Duhamel/partition estimate.

## 2. Individual centering is unnecessary for the fault bound

The locality argument uses P_j M_e=M_e when M_e acts as identity on processor block j. That identity holds whether or not M_e annihilates trace. Bath-only terms, including a strong bath-only loss generator, are also killed by P_j-I. The derivative norm bound, support cutoff |A|<=q, ordered set-partition argument and rooted incidence recursion are therefore unchanged.

The normalized partial-trace projections still have diamond norm at most one. Individual compressed perturbations may be non-CP and noncentered; only the whole generator/interpolated propagators need positivity. Möbius inversion and its supported linear fault classes use no trace normalization. E_empty is the ideal processor channel tensored with a TNI bath map, not a TP bath map.

The approximate-gate extension also survives: selected isolated G_j slots can be replaced by CPTP target U_j, while all intervening complementary maps are CP/TNI contractions. Fixed Delta_j insertions retain their norm cost once per slot. Hence the same product_(j in S)(x+delta_j) bound applies. No normalized conditional trajectory is introduced.

## 3. The concrete killed compression must retain all losses

For a fixed bath-only projection P, the actual complete-loss generator on its corner is

 K_P(X)=P L(P X P)P,

with X restricted to range P. It is CP/TNI: the repeated product of the CP/TNI short-step compressions X->P exp(hL)(P X P)P has this derivative and converges to its propagator. Outgoing gains are removed while the original loss terms remain. Returning that lost trace by hand would be a different nonlinear or re-prepared process and is not covered.

Pre- and post-compression are complete contractions. Thus the compressed local term has norm no greater than the original term. Because P acts only on the retained bath relative to processor S, it cannot enlarge that term's processor support. It may drastically change its bath action and lose trace annihilation, exactly as allowed by the extension.

Processor intended gates commute with P and remain their original intended gates on the corner. With no nominal processor-DATA gate in the waiting phase, the nominal native generator is bath-only. An isometric native module chart preserves norms and processor locality.

If the cut moves in time, its actual transport terms and CP/TNI propagator must be included; the fixed formula alone does not prove such a moving-cut construction. The source's waiting-phase application uses its actual native cut rather than claiming that arbitrary moving cuts work.

## 4. Native logical identity is an imported, separate hypothesis

The statement that the killed dynamics is identity on the native logical subsystem must come from the actual native correctable-span/forest theorem and its valid radius/domain. It is NOT implied by CP/TNI, a bath-only cut, or processor locality. For example a native logical Z Hamiltonian stays inside a bath-only cut but acts nontrivially on that logical subsystem.

Once the WHOLE killed generator has the factorization I_native tensor K_aux, processor partial-trace cavities and intended processor gates preserve it. Every cavity propagator and hence every E_F has native logical identity. The processor good-fault-class theorem must separately give its intended logical operation on the prescribed encoded/correctable input modules. Their common factorization then gives the combined ideal logical operation with arbitrary auxiliary coefficients. It is not obtained by treating a live noisy logical subsystem as an inert reference in an unrelated marginal theorem.

All native energy/BUSY and full-versus-killed estimates must be uniform on the SAME admitted processor/native logical source chart and retained references. A source assigning auxiliary states as a function of an unknown logical input does not define the claimed channel. A product source or an explicit common positive auxiliary source channel supplies the required domain; separate state-dependent estimates do not.

## 5. Native trace loss is paid, not normalized away

The source correctly does not identify the killed channel's effect with I. The companion completion makes its safe budget exact: if full decoded F is CPTP, ||F-K||<=epsilon, the killed bad map has norm<=b, and K-B=U_logic tensor A_aux on a common input chart, extract a CPTP A_+ from F using one fixed logical input and trace out the logical output. Complete contractivity gives

 ||F-U_logic tensor A_+||_diamond<=2(epsilon+b).

This positive auxiliary-factor repair uses the actual full channel, pays native loss through epsilon, and never conditions on survival. Its product probe must remain inside the declared source domain. Without that domain/norm premise, retain the source's original restricted-state estimate rather than promoting it to a full diamond bound.

## 6. Executable checks and limits

check_tni_cavities.py first constructs a literal bath-output Lindblad jump and compresses to its bath-zero corner. The resulting processor term is the noncentered loss -{P1,rho}/2; the compression residual is exactly zero. It then uses four processor space-time locations, non-CP individual perturbation summands, this state-dependent loss, and a strong bath-only scalar loss rate0.7.

At three perturbation rates all cavities are CP/TNI within numerical tolerance. Their largest effect eigenvalue is below0.247, so the test is genuinely trace-decreasing. Möbius reconstruction and inclusive cancellation residuals are below5e-18. The valid Hermiticity-preserving diamond dual upper bounds on all inclusive maps are below0.01644 of the stated bounds. These tests corroborate the algebra and complete-loss convention; they are not a validation of any native code family.

Accepted scope: finite bounded fixed-schedule CP/TNI cavity algebra with local noncentered HP perturbations, approximate target gates, and the conditional common-chart native/processor receiving and normalization lemma.

Not supplied: the native logical theorem or its warm source, a full hybrid resource construction, native logical measurement, physical feedforward, unknown raw-input encoding, adaptive/autonomous command scheduling, infinite unbounded extensions, practical advantage, or historical novelty. No external state was changed.
