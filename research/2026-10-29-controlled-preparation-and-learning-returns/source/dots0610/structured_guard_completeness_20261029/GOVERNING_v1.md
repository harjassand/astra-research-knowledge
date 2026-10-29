# Structured-family completeness with model-free guarded soundness
2026-10-29. New synthesis and full-physical Bell-loss extension, awaiting independent review. Actual source/interface assumptions are retained; polynomial bounds have very large explicit constants.

## Two different guarantees
SOUNDNESS: the physical-permutation/matching guard gives a finite accepted-operation error bound for every current source at the declared private/trusted boundary, whether the learned frame/model is correct or not. The source may always force rejection.

COMPLETENESS: a stronger structured family gives an explicit probability of acceptance after polynomial acquisition, without selecting parameters using a known future source matrix. This family has (i) unknown fixed local SU2 frames, (ii) the same FULL JOINT collective algebra on data plus all source memory at each complete call, and (iii) a positive singular gap of the actual predictable occupation-average pair defects during acquisition. These conditions are supplied physical/identifiability promises, not inferred merely from small residuals or an accepted guard.

Fix B=2^h with h>=5, n=4h physical qubits per source call, and h inner logical qubits. Encode each logical qubit into a four-spin total-spin-zero block; the tensor product Q has dimension K=2^h=B and lies inside the FULL n-spin singlet space P. It is generally a very small proper subspace of P and need not be permutation invariant. The physical random-permutation code-orbit service is essential: encode Q, randomly permute physically, apply the learned local frames, call source, undo frames and permutation, then reset-decode Q. Its full joint CP good/bad split has the FULL-P coefficient C_n=(n+2)/(n-1)<=2, independent of d/K. The old fixed-Q transfer cannot be used to reach this conclusion.

## 1. Full physical Bell loss from the received frame-variance proof
Work in exact aligned coordinates. Let W=exp(-iH) be the learned-versus-true product-frame mismatch, H=(1/2)sum_i h_i.sigma_i, with short local logarithms ||h_i||<=pi and a common gauge in which the root mismatch vanishes. Let V embed the entire exact singlet P of dimension d, used only as a MATHEMATICAL Bell reference, not as an implemented d-level encoder.

The full joint source dilation obeys U|P=I_P tensor U0 and has no cross-sector blocks. For an arbitrary purified current bath |b>, compare the actual effective output
 (I_R tensor W†)U(W tensor I)|Phi_d,b>
with |Phi_d> tensor U0|b>. Their vector difference has squared norm at most4||Q_perp W P||F²/d. Projection onto the physical Bell subspace |Phi_d><Phi_d| tensor I_bath shows that the RAW physical Bell loss satisfies

 p_raw <=4||Q_perp W P||F²/d <=4 Tr(PH²)/d.

No code-return projection/reset has been performed in this derivation. It therefore avoids the old distinction between projected Bell overlap and reset-decoder fidelity. Duhamel gives ||Q_perp WP||F<=||HP||F. The already received exact singlet covariance gives

 Tr(PH²)/d = n/[4(n-1)] sum_i ||h_i-hbar||².

The existing proper-rotation rounding bound is ||Chat_i-C_i||F<=4sqrt6 e/gL. Since theta<=pi||R-I||F/(2sqrt2), every nonroot log satisfies ||h_i||²<=12pi²e²/gL². Consequently, uniformly over the current bath and the allowed complete joint source operation,

             p_raw <=12pi² n e²/gL².                         (1)

This is the required extension of the received v9 vector argument to the full physical Bell overlap. It uses the stronger full joint algebra promise, not a reduced current-channel fit. U0 may act on arbitrarily large retained memory; its dimension is absent from(1).

For any fixed current channel, the matching ensemble has E rho_M=P/d. Decomposing each projected Kraus operator into scalar plus traceless part gives matching pass probability=f_raw+sum of nonnegative variances. Thus matching failure q<=p_raw. The physical-permutation CP bad effect equals the raw full-P Bell-loss effect. By applying(1) to all bath states, both service bad probability and test failure probability are bounded by the same p0 on every actual conditional history, not just on an averaged iid channel.

## 2. Paid no-reset acquisition
Use the received common-bank16x9 product-Pauli estimator. All n sites are prepared and measured on each call. Current settings remain private, known, independent coins. Source memory need not reset. The new matrix-martingale radius is
 e_m=(31ell+sqrt((31ell)²+1800m ell))/m,
 ell=log[25(n-1)/delta].

Assume every star occupation-average defect at the fixed declared endpoint has a true one-dimensional kernel and second singular value at least g0>0, almost surely over allowed acquisition histories. A weaker probabilistic excitation promise adds its failure probability separately. The unknown kernel is the true relative frame. Individual instantaneous gaps alone do NOT imply the average gap; the occupation/excitation premise must be supplied at the stated object.

On the concentration event (probability>=1-delta), measured s2>=g0-e and the observed gL=s2-e>=g0-2e. Choose0<g0<=4 and
 e_target=g0/(500sqrt n),
 m=ceil[450500000 n ell/g0²].

Because e_target<=.004, the displayed m is sufficient for e_m<=e_target. Then gL>=g0/2, the earlier proper-rotation sign condition is satisfied, and(1) gives
 p_raw<=48pi²/250000<1/512=:p0.
The last strict comparison follows already from pi²<10. The candidate is produced from actual counters and known controls; no source/bath matrix or future noise realization enters the learner.

This m is O(n g0^-2 log(n/delta)) FULL n-qubit calls, with O(nm) local preparations/readouts and counter updates. Constants are enormous. For B=2048,n=44,g0=.35,delta=.05, the conservative bound is about1.6e12 calls. The existing1m numerical candidate can work far earlier, but that observation does not discharge this uniform completeness bound.

Known g0 is not needed to define a gap-adaptive variant: inspect declared geometrically growing banks, allocate delta_j with sum<=delta, and stop when the actual observed gL and radius satisfy12pi² n e_j²/gL²<=1/512 and the sign condition. Under a sustained occupation-gap lower bound, it eventually stops with logarithmic confidence-spending overhead. A physical implementation must still declare a finite maximum bank budget; if the required endpoint lies beyond it, return INCONCLUSIVE rather than claim termination. The present concrete finite m theorem assumes the supplied numerical g0 bound.

## 3. Outer correction and finite guard
Use the existing explicit CSS/GRS mechanism over GF(2^h)=GF(B), with B distinct evaluation points, to encode h(B-4t) logical qubits into B field symbols of h qubits each, correcting arbitrary errors on at most t symbols. Here

 t=floor(B/8), b=floor(B/32), J=B,
 s=1/(C_n+1), L=6B.

Each outer symbol uses ONE n=4h physical source call through the h four-spin blocks and orbit randomization; there is no h-fold source-call grouping. The actual outer encoder/total decoder and their endpoint control costs remain paid. Matching tests use n/2 Bell pairs on random matchings, not the whole Schur encoder.

The private service probability obeys s>=1/3; test probability1-s<=2/3. Stop and reject on test failure b+1; accept immediately after J=B services and execute the total outer decoder, INCLUDING when the Bth service is call L. Otherwise reject at the finite call cap L. Completion is checked before the cap abort. Reset leakage, private keys and decoder syndrome are treated exactly as in the governing orbit guard.

For ANY source, the accepted bad-fault probability is bounded by
 P[Bin(t+b+1,1/2)<=b].
For B>=32, t-b+1>=3B/32 and t+b+1<=3B/16. Hoeffding therefore gives

       epsilon_sound <= exp(-3B/128).                         (2)

This is the existing arbitrary-error guard after the new orbit mechanism, not a statement that errors are independent physical Pauli faults.

## 4. Structured-family acceptance
On the acquisition-good event, every actual conditional matching-test failure probability is at most p0=1/512 by(1). Thus the binary event 'this call is a test failure' has conditional probability at most(1-s)p0<=1/768. Adapted Bernoulli mgf domination, with no independence assumption on outcomes or bath, gives for the first L=6B calls

 P[test failures>b] <= exp[-(4log4-3)B/128].

Indeed the upper expected-count parameter is L/768=B/128; using exponential parameter log4 and threshold B/32 yields the stated exponent. Since b+1>B/32, the abort event is covered despite integer rounding.

The private role coins are independent. Fewer than B service coins by6B calls has probability at most exp(-B/4), since the mean is at least2B. Extend hypothetical private coins after early stopping if necessary; no source-state extension is used to claim actual output. Union bounds yield

 P[accept] >=1-delta-exp(-B/4)-exp[-(4log4-3)B/128].             (3)

This is a uniform structured-family lower bound, not a known-generator replay. It remains valid for arbitrary adaptive retained memory inside the supplied common full algebra. Controls/storage are still ideal or separately budgeted. When the right side is positive, a fixed initial-memory reduced accepted logical channel has normalized error at most epsilon_sound/P[accept], because the orbit theorem supplies the actual input-independent accepted trace effect. For correlated logical-memory inputs retain the governing accepted-map/filter formulation rather than assert an input-independent scalar success probability.

## 5. What is enabled and what is not
The construction gives model-free finite soundness plus polynomial structured-family completeness without environment reconstruction. Unlike a zero-test-failure rule, it tolerates Theta(B) observed failures; therefore learning need only drive raw failure below a constant, not below1/B. The simple block encoder and physical orbit avoid both a whole high-rate Schur encoder and an exponential d/K test coefficient.

With fixed g0 and fixed delta, n=4log2B and m=O(logB loglogB). The output size is at least hB/2; total source-call cap is m+6B. Its physical-exposure ratio is at least hB/[2n(m+6B)], tending to1/48 as B grows, before control/storage costs. The constants make this asymptotic statement remote from practical sizes. No total circuit-time, energy, threshold or hardware advantage is claimed.

If exponentially small training failure delta=exp(-cB) is demanded, m grows as O(B logB/g0²), and a SINGLE block's calibration-inclusive exposure ratio falls as1/logB unless calibration is amortized. Do not simultaneously claim exponential readiness confidence and constant single-block total rate for free. Soundness(2) itself does not depend on delta or model correctness. Fixed delta gives constant positive readiness probability with exponentially small accepted soundness error.

Resource-first compilation from the separate finite first-success theorem can avoid consuming an unknown payload before a resource is ready; it pays clean reference storage, terminal teleportation and finite retry error allocations. For local memory, that trusted storage may be as strong as storing the payload directly. For communication, it is an explicit assistance resource. Arbitrary source noise may always abort. A silent training source reveals no frame and can later change within an unknown compatible algebra, so no uniform gap-free future-yield guarantee is supplied.

## 6. Equally informed direct full-path alternative
Polynomial structured completeness is NOT uniquely enabled by the physical orbit. For the same h-block code Q, exact block covariance gives Tr(QH²)/K=(1/3)sum_blocks sum_i||h_i-hbar_block||². The physical vector argument then yields p_raw,Q<=16pi² n e²/gL². Full-path two-MUB tests (bare logical computational/Hadamard preparations and matching output tests THROUGH the same encoder/source/total decoder), with bare endpoint Pauli randomization, have dimension-free witness coefficient2. Choosing e_target=g0/(600sqrt n) and a slightly larger training constant gives the same displayed polynomial acquisition and guard acceptance/soundness bounds.

The matching/orbit construction's distinct contribution is a model-free proper-subcode transfer using matching-only tests with no d/K penalty; it is not necessary for every equally informed polynomial full-path alternative. Full-path tests pay the deployed encoder/decoder and can detect their faults, whereas matching-only tests bypass those endpoints and require separate trust/calibration/isolation. Conversely orbit service pays physical permutations. Both mechanisms have linear-in-n primitive work for fixed-size compiled blocks. No total-control or asymptotic advantage is established without a concrete equal-resource cost model. The independent derivation is in resource_first_audit_20261029/STRUCTURED_DIRECT_FULLPATH_COMPARATOR.md.

## Governing dependencies
- nonunital_collective_frame_acquisition_20261029/GOVERNING_v1.md and reviewed matrix-confidence extension for the actual common-bank estimator.
- unknown_collective_noise_encoder_20261029/TWIRLED_FRAME_VARIANCE_BOUND_v9.md and TWIRLED_VARIANCE_SCOPE_v10.md for exact singlet covariance/vector comparison. Section1 here is a separately reviewable full-physical-Bell extension.
- physical permutation/code-orbit good/bad theorem and its independent review, including proper-subcode support and retired-record boundary.
- existing explicit finite-field outer compiler/total decoder; source-call grouping is changed by using K=B in the simple h-block singlet code.
- Existing matrix concentration, Reed-Solomon/CSS codes and exchange/singlet encoding are established tools; no historical novelty or experimental implementation is asserted by this synthesis.
