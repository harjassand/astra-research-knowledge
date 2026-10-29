# Independent review: compressed mixed-encoder physical recovery

2026-10-29. Reviewer `producer-workspace/review_history_program_bounds`.

**ACCEPT the mathematical recovery theorem, with both frozen corrections and the finite rational schedule, conditional on the separately received reference-joint compression/fixed-d compiler interface.** The result is a physical, always-outputting approximate decoder in the specified coherent-training/late-payload model. It is not a classical-training-only learner, a small-budget implementation, an arbitrary-noise theorem, or a novelty/advantage determination.

Two initial defects were repaired additively: the inverse-conditioning floor over all accepted estimates was too large by a factor2, and squaring the competitor lower bound required `delta<=1`. Neither changes the intended target schedule or the central gap-free recovery argument. Original source bytes were preserved; the receipt binds the corrections as part of acceptance.

## 1. The shared latent frame and reference interface

The promise is a fixed memoryless channel `N(rho)=V(rho tensor sigma)V†`, with logical dimension k, junk dimension at most r, and known output carrier dimension `D>=d=kr`. Zero junk eigenvalues are allowed. Padding the junk state with zeros and extending the isometry to d columns are mathematical constructions; they do not give the controller an arbitrary-junk input port or the unknown V as a gate.

The independently accepted compression receipt pins Yoshida–Soeda–Murao `2110.00258v4`, Lemma4/Eqs22–23. Its identity is equality of CPTP maps on all joint d-dimensional inputs, not an identity restricted to identical product states. Tensoring it with the identity on every training reference and payload reference is therefore valid.

Before compression, the ideal input is N independent logical Bell-pair training inputs and one independent later payload, each supplied with the same fresh junk sigma. Apply the compression **once, jointly to all N+1 encoded outputs**. The resulting state has the exact decomposition

`integral [J_U^tensorN tensor (id_reference tensor A_U)(rho)] dU`,

up to a known register reorder, with `A_U(x)=U(x tensor sigma)U†` and one common latent U. The controller receives neither U nor new query access to A_U. This ensemble is only a proof representation of the physical joint state. It is nevertheless legitimate to apply any subsequent fixed measurement/feedforward channel to it by linearity.

For a tomography record z, conditional on U the training copies are IID and independent of the payload/reference. Its likelihood `p(z|U)` is therefore independent of the unknown payload state. The complete decoded channel is

`M(rho)=integral sum_z p(z|U) R_z(A_U(rho)) dU`.

This is the expression needed for the final channel-norm bound. Conditioning on z changes the posterior distribution of U, so neither an independent-U model for different records nor an unconditional state law after observing z may be substituted. Instead the proof bounds each good `(U,z)` pair, then averages with its actual weight. A Hoeffding failure bound uniform in U implies total bad weight at most beta. This controls the fully averaged physical channel; it does not assert that every observed z certifies a good decoder.

The reference-joint property is load-bearing. My independent n=2 test compresses `D=3` to `d=2` with a four-dimensional external reference and agrees with the collective24-element qubit Clifford2-design twirl to about1.25e-16. Separate per-output compression differs in trace distance by about.320 in the same fixture. A training-Bell measurement gives a posterior payload entanglement fidelity1/2 under the shared frame, versus1/4 for independent frames. A `D=5,d=4` mixed-junk reference test also agrees with the two-copy Schur channel. These diagnostics support the exact interface; they are not a large-N compiler execution.

## 2. Tomography, affine repair and the physical fallback

Let `h=kd`. There are h diagonal projector settings and two real/imaginary settings for each of the `h(h-1)/2` unordered off-diagonal pairs, hence h² settings and `N=h²m` copies. Each scalar estimate is unbiased with outcome interval length1. For the imaginary part, choose the two-level observable `i|i><j|-i|j><i|`, with its sign fixed accordingly, and divide the outcome mean by2. Hoeffding and a union bound yield the stated failure probability `2h² exp(-2me²)`.

On the good event, diagonal errors have magnitude at most e and real/imaginary off-diagonal errors separately at most e. Thus complex entry magnitudes are at most sqrt(2)e and `||A-J_U||op<=2he`. For Hermitian X, `||Tr_output X||op<=d||X||op`. The affine correction tensor `I_d/d` consequently costs at most another `||A-J_U||op`, proving

`||B-J_U||op<=a=4he`.

B has exactly the normalized trace-preserving marginal `I_k/k` and trace1. Since `B>=-a I`, the ridge

`C=(B+2a I_h)/(1+2ha)`

is positive with `C>=a I_h/(1+2ha)` on the good event. Its normalized Choi marginal is exactly `I_k/k`; it defines a CPTP channel, not merely a positive state. The trace-norm bound follows explicitly from

`C-J=[B-J+2a I-2ha J]/(1+2ha)`:

the first numerator term has norm at most ha, and the latter two together at most4ha. Thus `||C-J||1<=5ha`, and the normalized-Choi channel inequality gives `halfdiamond(Ahat,A_U)<= (k/2)||C-J||1<=10kh²e=delta`.

For completeness, that Choi-to-diamond factor k follows by expressing a normalized pure input/reference state as a filtered maximally entangled vector with filter operator norm squared at most k, then applying trace-norm submultiplicativity. It holds for the channel difference and arbitrary reference inputs; no average-input fidelity is silently substituted for diamond distance.

On a bad statistical record, the affine/ridge formula need not be positive. The finite rational addendum correctly requires exact Hermitian positivity of `C-a I/[2(1+2ha)]`, exact marginal verification, and a completely depolarizing CPTP replacement when the test fails. Its strict-positive test rejects the threshold boundary. Every good record passes with a proven factor2 margin. Thus all physical branches are defined, and statistical failures cannot create a non-CP “decoder” or an undefined inverse.

The floor correction is necessary. A range-respecting rational raw diagonal estimate can pass the strict weaker test while its S minimum is only3/4 of the originally claimed stronger floor. An explicit h=8 fixture gives `lambda_min(S)=3/232`, above the valid uniform bound1/116 but below the incorrect1/58. This is included in the independent exact certification tests. The corrected all-accepted bound is

`S>=k a I_d/[2(1+2ha)]`.

The stronger bound without2 remains valid on the good event. The fallback has `S=I_d/d` and is also uniformly conditioned.

## 3. A physical Petz map, with no original-channel adjoint

The learned matrix C is an explicit small classical description. One convenient Kraus construction is to take `Q=C^(1/2)` and set `K_l=sqrt(k) unvec(Q_column_l)`. This avoids choosing an unstable eigenbasis and gives the same learned channel. All these matrices are computed from the observed counts and public rational constants.

Set `S=Ahat(I_k/k)`. The proposed recovery Kraus matrices are `L_l=K_l† S^(-1/2)/sqrt(k)`. Directly,

`sum_l L_l†L_l = S^(-1/2) [sum_l K_l K_l†/k] S^(-1/2) = I_d`.

The map is therefore CPTP on the entire small output register, not only on the true encoder's unknown support. In particular, zero eigenvalues of sigma do not require a pseudoinverse of sigma. The ridge supplies a faithful learned S. The adjoints are of learned finite matrices; there is no query to `N†`, no inverse-V oracle, and no accessible environment or purification.

The explicit all-accepted condition bound simplifies when `e=delta/(10kh²)` to

`||S^(-1/2)||op² <= 5h/delta + 4d`.

It is independent of every nonzero eigenvalue of sigma. The finite schedule also ensures an accepted C floor. Matrix roots/inverse roots can therefore be approximated with rigorous precision. Construct a Stinespring isometry from the ideal learned Kraus list, complete it to a known unitary, and compile that unitary. This yields an actually physical implemented channel. Merely rounding Kraus entries and ignoring the resulting trace-preservation error would not suffice; the addendum explicitly avoids that mistake.

## 4. Barnum–Knill and the final error chain

Primary source directly inspected: [Barnum–Knill, quant-ph/0004088v2,18January2026](https://arxiv.org/html/quant-ph/0004088v2), Eq12 and Theorem3/Eq13. Its reversal construction is precisely the learned Petz map above. The single-state ensemble `{I_k/k}` automatically satisfies its commuting-ensemble condition; no extension to a noncommuting ensemble is being assumed. Rectangular input/output Kraus matrices pose no difficulty; equivalently one can embed the logical input as a code subspace and apply the same theorem.

For each latent U there exists a mathematical CPTP competitor `R_U(X)=Tr_junk(U† X U)` satisfying `R_U A_U=id_k`. It is used only as a witness, not executed. Contractivity of the good-event model error implies its entanglement fidelity on Ahat is at least `1-delta`. For `0<=delta<=1`, the cited theorem gives learned Petz fidelity on Ahat at least `(1-delta)^2>=1-2delta`. Applying that same physical Petz channel to A_U instead changes the entanglement-fidelity test probability by at most delta. Thus the actual fidelity is at least `1-3delta`.

The fidelity-range correction is required: if delta exceeds1, squaring a negative lower bound is invalid. The valid all-range expression is `max(0,1-delta)^2`; the intended target schedule is inside `[0,1]` and is unaffected. The original small-budget simulation uses a separate clipped actual distance estimate and is not a demonstration that the formal confidence delta is small.

For a pure ideal Choi target, the actual normalized-Choi trace distance is at most `sqrt(1-F_e)`, hence the decoded half-diamond error for each good `(U,z)` is at most `k sqrt(3delta)`. Every bad branch is still CPTP and has half-diamond error at most1. Averaging the true latent/data mixture therefore gives `k sqrt(3delta)+beta`. A full joint implementation error gamma adds by the channel triangle inequality, proving exactly the claimed

`halfdiamond(M_implemented,id_k) <= k sqrt(3delta)+beta+gamma`.

Gamma must be a compositional reference-safe channel bound for the implemented joint controls, including any approximate preparation, measurement, compression and branch-conditioned recovery synthesis that are not treated as exact. Matrix residuals alone do not certify it. The discontinuity of the classical acceptance decision causes no problem if the finite rational ideal decision is implemented exactly and quantum implementation errors are bounded against that fixed complete processor.

## 5. Finite resources and material limitations

For rational `0<epsilon<=1`, the choices `delta=epsilon²/(12k²)`, `beta=epsilon/4`, `gamma=epsilon/4` sum to the claimed epsilon bound. The original natural-log query formula is algebraically correct. The finite addendum gives a fully rational conservative alternative: choose integer L with `2^L>=2h²/beta`, and `m=ceil[L/(2e²)]`. Then `2h² exp(-2me²)<=2h² 2^-L<=beta`. This avoids an unverified logarithm/square-root oracle and leaves all count matrices, a, B and C rational complex.

Training uses exactly `N=h²m` forward CPTP calls, plus one encoder use for the payload. The statistical query bound is polynomial in k,r,1/epsilon and independent of D and the smallest nonzero junk eigenvalue. It is exceptionally conservative: the rational schedule at k=2,r=2,epsilon=.01 uses193273528320000000000 training calls. The small-model sampled fixtures are not executions of this certified end-to-end schedule.

The control conclusion depends on the separate `multiplicity_compression_compiler_review_20261029/REVIEW_RECEIPT.json`. It receives the corrected reference-joint compression and a finite compiler with polynomial dependence on N and log D **for fixed d=kr**, including explicitly paid GT enumeration. It does not prove a uniform polynomial-in-r gate bound. I did not reaccept its primary compiler beyond that scoped interface.

The training outputs must remain coherent until the later payload arrives. All N+1 output carriers are processed jointly; training references are retained, and the compressed payload remains protected while tomography, exact feasibility checks and recovery compilation are performed. At least N log D training storage qubits, plus references and work, are paid. This is not an offline classical learned decoder ready before an unrelated later payload, and it is not a theorem for causal source memory, drift or a changed junk state. Ordinary forward quantum-channel access must permit entangled Choi inputs.

The learned small Petz matrix belongs to this batch's shared latent frame. It is not reusable directly on later original-D outputs. A new payload requires a new jointly compressed training batch, or a separately proved simultaneous multi-payload extension; no such reuse theorem is included here.

## 6. Reproduction and acceptance boundary

Independent evidence in `independent_checks.py` includes:

- exact rational CP/TP repair, all-principal-minor checks, strict threshold/fallback tests, and an explicit counterexample to the uncorrected conditioning floor;
-26 physical learned-Petz cases at k=2,3 and r=1,2,3, including exact zero and10^-18 junk eigenvalues, with a square-root-column Kraus construction different from the author's;
- direct TP, Barnum–Knill competitor, model-to-actual fidelity and arbitrary entangled-input checks;
- reference-joint two-copy compression tests, a shared-frame versus independent-frame counterexample, and explicit training-measurement posterior-U verification;
- exact symbolic sample/conditioning identities and three log-free rational controller schedules.

The author script was replayed separately from the immutable source snapshot and its JSON reproduced. The independent worst TP residual was about8.98e-12 in the ill-conditioned floating fixtures; these are diagnostics of the exact algebra, not error certificates for a device. No SDP, unknown adjoint oracle, native large-D compression or hardware run was used.

Accepted scope is the corrected physical recovery theorem in this exact mixed-isometry, memoryless, coherent-training model, with the stated classical/quantum controls and error budgets. The rank lower bound and exact mixed-exterior decoder are separate packets and are not part of this receipt. Historical priority, optimal query/rank dependence, approximate-noise extensions, practical performance, fault tolerance, a classical-memory comparison, and any exclusive quantum advantage remain unproved here.
