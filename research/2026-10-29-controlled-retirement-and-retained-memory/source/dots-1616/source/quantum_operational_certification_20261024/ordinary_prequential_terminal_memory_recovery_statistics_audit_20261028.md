# Independent statistics audit: prequential terminal memory recovery

28 October 2026. Reviewer: `producer-workspace/audit_count_pilot_fresh`.

**PASS at the stated expected, one-shot, privately timed terminal-service scope.** Bound source: `ordinary_prequential_terminal_memory_recovery_20261028.md`, SHA-256 `20e59391aeab608e0fb76dbaee3fee6825d434991892a2c63fe5e57634316079`. This audit retains the source's actual conservative step size, projection tolerance and `d^5/epsilon^2` cap. A possible sharper Choi-radius rate is not included. No received source, author fixture, prior audit or prior receipt was edited. No source calls, random samples or acquisition simulations were performed.

## 1. Actual-record conditional gradient

Fix only an actual prior record h and its induced conditional source-memory density operator. A new input independent of that memory defines the current CPTP map E_h. Fresh private j,s and a uniformly sampled physical Pauli word W have the specified Born probabilities. Local Pauli readouts provide a real integer parity b, not a supplied matrix coefficient. The local measurement instrument and its retained record must be the actual one; full local outcomes and parity-coarsened outcomes may induce different occupation histories, although either supports the conditional calculation.

For each input state r_(j,s),

`E_(W,b)[d b W | h,j,s] = r_(j,s)`.

With the source's output-first normalized Choi convention, differentiation of the affine six-state mismatch risk gives

`grad p_h = -(d/12) sum_(j,s) s sigma_j tensor r_(j,s)^T`.

Averaging the actual record matrix `g=-(d^2/2)s b(sigma_j tensor W^T)` over j,s,W,b gives exactly this gradient. The transpose is essential, including for Pauli Y; it cannot be removed by appealing to a real-input convention. Also,

`g^2=(d^4/4) I_(2d)`, hence `||g||_F^2=d^5/2` and `||g||_op=d^2/2`.

The integer bound `G=d^2 2^ceil(w/2)` therefore satisfies the claimed inequalities. Fresh settings cannot be leaked so that the complete current source map depends on their classical value outside the specified quantum input. The public complete-port/role-sealing premises, rather than source reset, establish this condition.

The six-state average mismatch identity `p=(2/3)(1-F_e)` holds for every trace-preserving qubit channel, including nonunital channels. The conditional gradient calculation and this identity require neither identical channels at successive calls nor a classical model of the retained memory.

## 2. Rational feasible projection and objective debit

The normalized Choi feasible set consists of density operators with a fixed input marginal. Its Frobenius diameter is at most sqrt(2), its center is `I_(2d)/(2d)`, and the source's initial squared-distance bound of 1 is safe. Since `eta G=1/sqrt(N)<=1`, `||Y_t||_F<=2`.

The received local-CPTP addendum supplies only the known-center finite solve, rational TP/PSD repair and finite synthesis. Its iid state-acquisition argument is not imported. For the repaired normalized Choi matrix, the imported trace-norm estimate implies

`||Jphys-Ktilde/d||_F<=9 delta`.

Because Jphys is a density operator, `||Ktilde/d||_F<=1+9 delta`. The change in the new **squared-distance** objective is thus bounded by

`9 delta (6+9 delta) < 100 delta`, for `delta<=1/100`.

This supplies the needed extension from the old linear objective to the new quadratic projection problem. With `xi=1/(16N^2)` and `delta=xi/1024`, repair costs less than `100xi/1024`. Solver slack and the known-center perturbation leave ample remaining slack.

The prescribed Hermitian grid bounds are also sufficient. An entrywise rounded unnormalized Choi matrix changes in operator/Frobenius norm by at most `4d u`, and its output partial trace changes by at most `8d u`. Starting from residual delta/2 leaves both residuals below delta at `u<=delta/(64d)`. After division by d, the Frobenius change is at most 4u; a safe quadratic objective debit is 28u on the near-feasible ball. For example the explicit dyadic choice

`u=xi/(65536d)`

meets both stated mesh conditions and gives

`xi/8 + xi/4 + 100delta + 28u < xi`.

This example establishes an available finite mesh, not a change to the source algorithm. Its denominator is fixed by d,N. The rational repair then resets denominator growth, so iterative history does not require recursively growing entry lengths. The finite solver must deliver its certificates on every history under its declared implementation contract. An uncertified fallback is physical but cannot claim the projection guarantee. This review did not run an SDP solver or a compiled physical decoder.

## 3. Exact repaired-OGD constant and comparator

Let P be the exact Euclidean projection of Y onto K. Its variational inequality and objective gap imply `||Jnext-P||_F<=sqrt(xi)`. For any feasible fixed comparator J*,

`| ||Jnext-J*||_F^2 - ||P-J*||_F^2 |`

`<=||Jnext-P||_F (||Jnext-J*||_F+||P-J*||_F)`

`<=2sqrt(2)sqrt(xi)<3sqrt(xi)`.

This derivation avoids inserting an unnecessary extra xi term. Telescoping the resulting projection inequality gives exactly

`1/(2eta)+(eta/2)N G^2+3N sqrt(xi)/(2eta)=(11/8)G sqrt(N)`.

Thus the relaxed bound `2G sqrt(N)` is valid for every acquired gradient path. J_t is fixed before the current probe, while a comparison decoder D is fixed before the trajectory. Conditional unbiasedness then implies the expected mismatch-risk inequality. Minimization over a deterministic fixed D in the expected all-probe occupation objective is legitimate by compactness/continuity. It does not permit moving the infimum inside the random-history expectation, selecting a hindsight path minimizer, or changing the source's earlier occupation law.

## 4. Terminal transfer and scope of the expectation

The main independent receipt separately checks the complete-port causal transfer, arbitrary independent reference and common CP-memory oracle. That received proof is imported for those controls/algebra claims; this audit additionally checks its statistical use.

The full initial QR state is product with source memory and acquisition randomness. Given private T=t, the first t-1 actual operations have the all-probe law; the current frozen decoder is applied to the independently held payload through the same complete current port. No gradient is acquired from the payload. Therefore the actual averaged channel is

`Lambda=(1/N) sum_t sum_h p_t(h) D_(t,h) E_(t,h)`.

Linearity of Bell fidelity and the factor 3/2 converting mismatch risk to Bell loss yield

`1-F_e(Lambda)<=inf_D R_N(D)+3G/sqrt(N)`.

For the stated least power-of-four horizon, `3G/sqrt(N)<=epsilon/2` and

`N<144G^2/epsilon^2<=288d^5/epsilon^2`.

This is an expectation / averaged-channel guarantee, not a high-probability assertion conditioned on T or the transcript. No iid confidence event or optional-stopping concentration theorem is silently used. Holding a new datum until a private terminal slot is a real control/storage premise; ordinary training alone does not certify an arbitrary deterministic future slot. The optional averaged private Pauli twirl changes the actual service and does not give a key-conditioned guarantee.

The supplied CP-order family has a fixed decoder optimal at each actual history, as checked in the main independent receipt. This identifies the comparator but is not learned or inferred from the records. The generic expected fixed-comparator result does not require that structural family.

## 5. Finite resources and operational allowances

The cap N includes the one payload. The ideal uniformly chosen terminal slot gives mean calls `(N+1)/2`; an implementation that stops early on sampler exhaustion can only reduce this count, while a padded fallback preserves it. Neither convention changes the worst-case cap or risk debit.

Per potential probe: W uses 2w fair bits, s uses one, and axis rejection uses at most 2R bits. With `R=ceil(log2(2N/nu_rng))`, exhaustion probability is at most `N4^(-R)<=nu_rng`. The uniform terminal index uses exactly log2 N bits. Thus the stated finite random-bit cap holds, with two extra bits for the optional terminal twirl. Sampler exhaustion contributes at most its probability to bounded Bell loss; any stronger norm convention must allocate its corresponding norm factor within the same declared whole-process allowance.

All local output readouts and input preparations are actual physical operations. The ledger includes bounded-bit O(d^2) Choi storage, optional O(Nw) raw records, finite classical solves, up to N pre-call decoder compilations, their padded computation time, and storage of the isolated payload during that time. The terminal decoder's dense synthesis is paid; no arbitrary-CPTP black box is supplied. The worst-case N-update ledger conservatively covers the all-probe analysis and the at most N-1 actual pre-payload updates.

The remaining epsilon/2 is a single complete actual-versus-declared-ideal operational loss allowance. The ideal all-probe comparator is not automatically replaced by a separately perturbed actual-history comparator. Compiler, storage, role-sealing, sampler and measurement errors must fit that allowance. This is not a hardware threshold or a claim of equal numerical Bell and untwirled diamond losses.

## 6. Independent exact evidence and acceptance boundary

The separate source-disabled script `prequential_terminal_memory_statistics_check_20261028.py` uses exact rational/complex arithmetic, no RNG and no source actor. Its saved JSON records:

* 336 actual Born-event terms and 336 deterministic gradient norm identities across four channels, including nonunital and complex mixed-gauge examples in dimensions 2 and 4;
* exact conditional mean-gradient equality in all four examples, and detection of an incorrect omitted transpose in all four;
* twelve exact six-state / normalized-Choi / Bell-loss identities for physical decoders;
* four exact rational TP/strict-PSD repair cases;
* twenty-four finite horizon, step, mesh, objective, regret, source-cap and random-bit budget checks.

These are finite algebraic checks, not a sampled count pilot, a full OGD run, execution of the certified convex solver or hardware validation. The universal result rests on the arguments above. Main and received finite-repair manifest entries were reverified before binding.

No load-bearing issue remains within the stated premises. The accepted result is a conventional online convex decoder learner using ordinary single-copy integer records, arbitrary retained causal source memory, a known patch/fixed encoder, and one privately timed averaged terminal payload. There is no separation from an equally informed conventional learner, reusable future service guarantee, counterfactual-policy comparator or record-wise confidence certificate.
