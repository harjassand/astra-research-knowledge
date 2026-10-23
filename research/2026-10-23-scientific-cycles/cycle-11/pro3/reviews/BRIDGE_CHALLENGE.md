# Independent challenge of the Cycle11 native transport bridge

Reviewer: `/root/cycle11_bridge_challenge`.
Scientific date: 23 October 2026 UTC.

## Verdict and exact principal source

**ACCEPT Theorems A-B and Corollary C, within their explicit finite exact-real
scope and the accepted predecessor interfaces. No mathematical proof repair
is required.** The new finite bridge applies to arbitrary native reciprocal
geometry. It supplies the missing all-class upper, so the stated phase law,
exact liminf and limit-nonexistence criterion concern the unrestricted supremum.
The wider antisymmetric-screen class is also justified by the actual inherited
hypotheses and an admitted subclass lower.

Reviewed final principal:

- `NATIVE_PATH_COMPOSITION_THEOREM.md`
- 25,456 bytes
- SHA256 `d9e5427b86305998a949f1497568fffb03903e2b51a927a3d417db2ab81dc911`

The principal was read in full. The reviewer requested one explicit domain
convention: proposal ratios/screens are defined on positive off-diagonal Q
edges, and absent edges have L_xy=0. The final source contains that standard
convention. This is a clarification preventing an apparent 0/0 formula, not
a repaired theorem or a change to the admitted class. The review also made
explicit that the control cost is Lipschitz only for positive progress
arguments; its actual jump at immediate completion is correctly preserved.

Reviewed new contribution:

- `contributors/HETEROGENEOUS_TRANSPORT.md`
- 12,429 bytes
- SHA256 `56d6b5656ec1179a588927bceb29fc460cb3fa42ea291f657f851e1f35f8f7a4`

Also read, for its distinct finite result and explicit nonclaims:

- `contributors/NATIVE_COMPOSITION.md`
- 12,279 bytes
- SHA256 `139cb8963d5734cc107bd49bdf7bfcc20cc86bfd8e146595d683ab056ee3b822`

The reviewer did not construct either of those contributions. The review read
Cycle10 principal Sections 1, 2 and 6 and the actual Cycle8 full-return interface,
Section 4, in the recovered original source. It did not rerun old fixtures or
infer an asymptotic theorem from finite matrices.

## 1. Tagged reversal is an exact identity with a paid defect

An off-diagonal native transition is split into local and global mixture tags.
All actual diagonal probability is retained in one hold tag with probability
C_xx. This is a decomposition of the original transition law: it does not
replace rejected moves by an off-diagonal accepted event or renormalize a row.
After removing only the off-diagonal acceptance factors, the reference matrix
has row sum

    C_xx + beta(1-Q_xx)/2 + alpha(1-q_x)/2 <= 3/2.

This is a ROW bound; the proof does not mistake a reverse column sum for a row
sum or claim the matrix is Markov. Each local reference edge has q-weighted
reverse ratio r_q=q_y Q_yx/(q_x Q_xy). The global proposal q has ratio one,
and the actual diagonal reverses unchanged. Hence any tagged path with signed
increment Z=-eta sum_local log(r_q) satisfies the displayed path identity.
Acceptance factors only decrease its actual forward weight.

Reversing a finite first-hit path gives a path starting in E. Removing its
interior and first-hit restrictions enlarges the sum of nonnegative reference
weights. Consequently all first-hit paths of length at most N with Z<U have
mass at most

    e exp(U/eta) sum_(j=1)^N (3/2)^j
       <= 3 e exp(U/eta) (3/2)^N.

Repeated vertices, cycles, merging and arbitrary native degrees are included
in this sum. No potential whose edge differences equal Z is assumed. In
particular a nonzero proposal circulation is not a loophole in the identity.
The price for retaining every native hold is explicit and cannot be dropped
for a long horizon without a separate scale argument.

## 2. The progress counter uses the actual constant killing probability

Inside A={W<h}, every independence proposal into B=A^c is accepted, because
W_y>=h>W_x. Its actual mixture probability is the constant

    g=alpha(1-b)/2=beta r_b/2.

All global exits are treated as killing in the progress counter, including a
global first hit of E. This is legitimate: a global edge contributes no signed
or positive-clipped progress, so a capture path with signed total at least U
and a final global edge must already have crossed the positive-progress
threshold before that exit. A final local edge can itself cross the threshold.
Thus every high-progress capture is contained in the stated counter event.

For a positive local increment x, the actual acceptance is at most
sigma(x)=exp[-(x-d)_+]. Negative increments can be clipped to zero for an upper
bound on reaching a progress threshold; this changes only the proof counter,
not the actual path probabilities. At a pre-threshold history use potential
V(z), where z is remaining positive-clipped progress. The accepted control
Bellman inequality gives

    sigma(x)[V(z-x)-V(z)] <= r_b V(z).

V is nonincreasing, so its positive local drift with the actual acceptance is
no larger than the drift with sigma. Summing with the actual Q row weights
gives local positive drift at most beta r_b V(z)/2=gV(z). Global killing
subtracts exactly gV(z), and all other transitions are either history-changing
holds or extra killing. The resulting stopped potential is a bounded
supermartingale.

This direct conditional argument avoids any hidden assumption that a held
native state or its next control stays unchanged. Internal global moves and
zero/negative local moves may reveal a new state and change subsequent action
choices. The inequality holds after every resulting history. Local exits
before reaching the threshold can be killed; assigning them their would-be
continuation potential only enlarges the upper bound. A positive local edge
that reaches the threshold, even on an exit, is assigned terminal value one.

Starting from q restricted to A therefore bounds the high-progress event by
b V_{d,r_b}(U). Adding the low-progress bound proves the new finite theorem.
No source mass is spent independently at each possible crossing count.

## 3. Interface with the original full chain

The actual Cycle8 Section 4 uses the first-B-hit submeasures nu_j and the
identity

    q C^n = sum_(j=0)^N nu_j C^(n-j) + residual,
    residual mass <= b rho^N.

Its union E of bad bounded-test states is a subset of B with q(E)<=ebar.
The earlier weighted-energy estimate bounds only the mass of first hits in E;
the new finite theorem can replace that estimate at this exact interface.
The factors C^(n-j) remain original full-chain kernels. Thus the replacement
retains every later return, rejection and global attempt. It does not turn
the absorbed proof counter into an algorithm or target oracle.

With e<=E_n=O(ell^6(L+1)/n), N=O(L), eta=Theta(L/ell), the proposed threshold

    U=eta[log(1/E_n)-N log(3/2)-3L-log 3]

is positive eventually and equals u-o(1). Its short-progress defect is at most
ell^-3 exactly. The entire factor (3/2)^N is paid; the reason its progress
cost vanishes is eta N=o(1), not a false stochasticity claim.

For positive U and U', M_{d,r}(U)=-log V is 1-Lipschitz in its argument:
each fixed-J cost has slope between zero and one, and a minimum preserves
this Lipschitz bound. Thus u-o(1) can replace u even near an integer phase.
Also M is monotone in r. On compact positive-r intervals, relevant minimizing
counts are O(U+1), which gives the stability bound O((U+1)|Delta log r|).
These facts permit the small finite KL cutoff deficit in r_b to be paid.
They do not themselves perform the principal's single-information-budget
MAX argument or claim the completed unrestricted phase theorem.

## 4. Distinct fixed-count operator note

The separate NATIVE_COMPOSITION note integrates local holds against a fixed
killing rate before conjugation. Reverse-Q Jensen and row concavity give its
stated exact operator bound; the fixed-J scalar optimization then retains the
integer crossing count. Its two explicit limitations are correct: summing
separate per-J bounds cannot be replaced by their maximum without another
argument, and native within-A global transitions cannot simply be deleted.
The tagged-path theorem supplies a different operation that avoids both
unproved replacements. The fixed-count note is useful capital, not a premise
silently substituted for the all-native bound.

## 5. Complete critical upper and the one-information-budget allocation

The principal's abstract Theorem B does not require a target or stationary
law: the only global-kernel hypotheses it uses are off-diagonal G_xy<=q_y
and equality on A to A^c. These are sufficient respectively for reference
path domination and the constant killing probability. The native IMH satisfies
both on A={W<hcut}. All ratios on present reciprocal edges are positive and
finite; absent local edges contribute zero.

I checked the complete finite full-chain certificate, not only the schematic
capture statement. The explicit E_n bounds the union of all N+1 bad test
sets. With N=O(loglog n) and eta=Theta(loglog n/log n), the chosen U_n is
u_n-o(1)>0, and the reverse-path defect is exactly at most (log n)^-3.
The anchored-smoothing, initial-hit and unhit terms are O((log n)^-2).
The reference row growth is paid in the definition of U_n before the limit.
The original full-chain return decomposition remains unchanged.

For U>0, the integer minimizer of M can be selected with
1<=J<=ceil(U/d): all larger counts have zero attenuation and strictly
larger cost than the ceiling. This proves the stated local-in-parameter
stability bound in log r as well as the positive-U Lipschitz bound. In
particular the finite cutoff deficit

    r_b >= r exp(-delta_h), delta_h=O(L/ell^2)

costs at most O(L delta_h)=o(1) in the exponent. Monotonicity and U_n=u_n-o(1)
therefore preserve the fixed-r crossing cost uniformly over native instances.
The already proved discrete control expansion then yields the phase-sensitive
capture upper, including integer phases and the tie between the two depths.

The proof correctly does not add a full K tail to a full transport term.
The three-cell inequality is applied to the same instance and gives
k+ell a<=K+o(1). On a subsequence with k tending to K, the information tail
loses its leading amplitude and b tends to b0. On a subsequence with k
bounded below K, the true killing ratio is bounded below by r1>r. The
principal's compact/tail argument correctly proves a fixed c1>c(d) with
h_r1(a)>=c1(d+a) for every a>=0. Its transport term is then o(1/ell),
leaving an information amplitude at most K-k_infty<=K. This argument does
not require a rate at which k tends to K.

The approximate-maximizer and convergent-phase subsequence argument proves
that the positive part of the proposed all-class upper error vanishes.
It does not assume that a finite native supremum is attained. The accepted
native lower holds at every sufficiently large horizon with a uniform phase
error, while the separate Q=I lower supplies K. Combining them by a MAX
proves the full assertion rather than spending two entropy budgets in one
instance.

## 6. Exact minimax oscillation and extended screen class

All circle phases occur along the stated integer-horizon subsequences because
the critical policy perturbation is o(1), and Psi is continuous on the circle.
For d>d_star its maximum gamma(1-d_star/d) is strictly positive. Thus the
liminf and limsup formulas follow from the pointwise asymptotic profile.
If b0 exp(-s)>K, the phase-zero value exceeds both K and the positive-penalty
phase value, so a limit does not exist. If b0 exp(-s)<=K, the maximum profile
is identically K. This is an exact necessary-and-sufficient criterion in
the stated strict regime, not a conclusion drawn from one oscillating family.

For Corollary C, antisymmetry of xi makes S_yx=1/S_xy. The exact factorized
Hastings identity proves pi_x L_xy=pi_y L_yx, including the actual diagonal.
Hence laziness, positive spectrum and Dirichlet domination by alpha G/2
remain available for the anchored smoothing. The new finite bridge uses only
the upper screen inequality. I checked the actual Cycle8 Section 3 as well:
its finite energy, local rejection subtraction and reverse-Q Jensen likewise
use only that upper bound, native row budgets and the stated reversibility.
Thus the two older branches extend under their real hypotheses; they are not
being assumed merely from an off-diagonal comparison.

The positive-mismatch native policy A_n=d, kappa_n=eta_n+1 has
xi_xy=log(Q_yx/Q_xy), bounded by d and target-independent. It provides the
accepted original-law lower within the wider class, without any new geometry
or suppressed native multiplicity. This completes the claimed wider sharp
law. It does not address nonreciprocal target errors, nonreversible target
kernels, within-run adaptations, concrete floating arithmetic or free screen
evaluation. No separate proposal-asymmetry bound is required by this wider
class's upper.

## 7. Diagnostic and comparator qualifications

I read the frozen new four-state diagnostic inputs, exact Fraction source,
result and resource receipt without rerunning them. It checks tagged path
identities, actual diagonal factors, first-hit path enumeration against a
separate recurrence, and high-progress final global hits whose threshold was
crossed earlier. It includes a nonzero circulation ratio and both increment
signs. The code's admission bound is K=24, not K=1, and it is not a critical
sequence or asymptotic proof. Those limits are stated. The existing admitted
32-state and failed-K=1 coalescence fixtures are not relabelled or rerun.

The preserved ordinary IMH comparison is compatible with the stronger theorem:
its minimax amplitude remains K, and on the same adverse native families its
error is O((log n)^-4) at the stated proportional horizons. The hybrid's
oscillating order-1/log n risk is a robustness result with an adverse ordinary
comparison. The generalized distortion formulation introduces no useful-sampler,
target-call or wall-time advantage. The principal's standard-Borel continuation
is explicitly an unproved next question, not an extension already accepted
by this review.

## 8. Scope and resources

This is an internal, source-bound mathematical review, not formal verification,
external acceptance, historical priority, an arithmetic implementation theorem,
or evidence of useful sampler performance. The finite lemma needs only its
stated one-sided screen bound; the original full-return application additionally
retains native target reversibility and the population KL contract. No target,
normalizer, proposal, reverse-probability, label or precision access is granted
for free by a proof counter.

No scientific computation, old fixture replay, graph materialization, or private
delivery was performed by this reviewer. Source reads, reasoning and local
review-file writes are observed. Inference/token, design and total discovery
costs are unknown. Current review work began with the observed UTC time
2026-10-23 04:29:32; wall-clock duration is not a discovery-cost estimate.
