# Independent challenge: the branching-tree lower construction

Reviewer: `/root/reachable_obstruction_challenge`.
Scientific date: 2026-10-22 Australia/Brisbane; execution date 2026-10-21 UTC.

Status: both complete contributor and principal sources accepted below, with exact bindings.
This is a focused challenge of the new tree mechanism and its inference
interface, not another review of the entire predecessor programme.

## Challenge scope and finding

The root proposed replacing a one-dimensional symmetric path by a rooted
D-ary tree. The question is whether the factor-two gap between the old path
lower and incoming killed-operator upper reflects a true symmetry constraint.
I independently reconstructed the actual per-vertex acceptances, global
transitions, lumpability, KL admission, timing event and quantifier order.
I found one necessary multiplicity correction in the initial task wording:
reverse local acceptance is **D n^-2 s**, not n^-2 s, where
s=(z/D)^eta. This follows from pi_child/pi_parent=n²/D. After multiplication
by Q(child,parent)=1/(D+1), the reverse mixture probability is f/n², where
f=beta D s/[2(D+1)]. It remains negligible, and this correction is required
for detailed balance. I sent it immediately to the root and constructor;
both explicitly adopted it before completing their proofs.

No obstruction to the corrected mechanism was found. In particular the
outward probability D/(D+1) is compatible with a **symmetric per-vertex Q**:
the inward probability uses one edge and the outward probability D edges.
The quotient matrix on levels is not symmetric in ordinary counting measure,
and must never be substituted into the native class as a new symmetric Q.
It is an exact lumping of the admitted full tree.

## Load-bearing obligations checked independently

1. **Admission and support.** At level i there are D^i vertices, each with
   q_x=b z^i/D^i and pi_x=p n^-2(m-i)/D^i. Summing per-level KL cancels
   multiplicity exactly and gives the old path's KL expression. For fixed
   D,b,v,M and m=O(loglog n), positivity and KL slack therefore hold uniformly
   while the number of vertices grows. The star and all vertices retain
   strictly positive probabilities. Q depends only on the declared tree,
   not on an observed target value; n,eta and the tree are fixed for each run.
2. **Acceptance branches.** Adjacent proposal ratio is z/D, adjacent target
   ratio n²/D, and forward acceptance is s because n²/(D s)>=1 eventually.
   Reverse acceptance is D s/n². The W_i are exactly the old level weights,
   W_m=n(log n)² and W_i=W_m(z/n²)^(m-i); all nonterminal levels eventually
   lie below the star and the leaf set lies above it. These assertions require
   D fixed before n tends to infinity; allowing arbitrary D_n without further
   estimates would be an unproved extension.
3. **All competing moves.** Independence MH can jump between different
   vertices at the same depth, so a bare path calculation copied per vertex
   would miss transitions. Their aggregate probabilities depend only on the
   level: all vertices in a level have the same W, q and pi. The partition
   into levels and the star is strongly lumpable for G and L and hence C.
   Within-level moves are actual quotient selfloops. Alternatively one can
   discard them in a labelled event, charging at most the positive-level
   q mass S_q; either route keeps them in the actual chain.
4. **Timing and retention.** In the level quotient, marked local forward
   mass is f at every transient level, while the accepted global star exit
   supplies a strictly positive lower exit bound. The sum of all other
   exits supplies the upper competing-exit bound. Conditioning the next
   level exit to be marked and occur within a deterministic window gives
   (f/e_i)[1-(1-e_i)^h], so the waiting penalty is relative to the small
   capture event. Upon arrival at the terminal level, exact escape from the
   entire leaf set is alpha(1-p)/(2W_m)+f/n²; same-level global moves stay
   inside it. Subtract the actual target mass p, not one leaf's mass.
5. **Order of limits.** Fix a strict desired exponent margin first. Then
   choose b below its entropy endpoint, a finite integer D, a finite v, and
   M. Only then let n tend to infinity. The effective competition parameter
   is a_bD=alpha(1-b)(D+1)/(beta D). Taking the infimum over fixed choices
   sends a_bD down to alpha exp(-K)/beta. No support-dependent norm constant
   or simultaneous unproved D_n limit is needed.
6. **Accuracy conversion.** For a policy eta(epsilon)~d epsilon log(1/epsilon),
   evaluate the lower at n=floor(exp(A/epsilon)), with eta fixed during that
   run. Then eta log n/loglog n tends to d A. If d A times the chosen tree
   exponent is below one, its risk is much larger than epsilon, yielding
   T_policy(epsilon)>n. This direct comparison uses within-run TV monotonicity
   only. The matching incoming upper can then give coefficient existence.
7. **Critical limitation.** The logarithmic risk exponent can be determined
   even at lambda=1/c_*, but this alone cannot determine a finite prefactor
   for (log n)R there. Likewise actual finite powers never establish the
   asymptotic theorem. The killed-norm witness alone was not a mixing lower;
   the new tree supplies actual q-start capture and retention.

## Independent exact finite calculation

`tree_lumping_exact_check.py` reconstructs a complete D=4, depth-2 tree plus
star, with 22 states. Parameters are b=3/5, z=1/64, p=1/64, the auxiliary
n label 16, eta=1/2 and alpha=beta=1/2. This is an algebraic check and not a
horizon-asymptotic specimen satisfying the special p=(log n)^-M choice.
All arithmetic is `fractions.Fraction`; needed square roots are verified as
perfect numerator and denominator squares.

The check verifies exact positivity, normalization, Q symmetry and
stochasticity, both original MH acceptance formulas, C stochasticity,
detailed balance, strong lumpability of every full row, detailed balance
of the quotient, marked forward and reverse mass, and leaf-set escape.
It propagates both the full and quotient laws for twelve ordinary steps,
verifies equality at every level at that final horizon, and verifies equal full and
quotient TV. No floating positivity or normalization tolerance is used.

The exact resulting values include s=1/16, f=1/80, reverse=f/256=1/20480,
and leaf-set escape=193/81920. An exact KL<1 certificate is also checked:
all nonterminal tree KL terms are negative; pi_star<197/200, q_star>39/100;
the finite exponential sum through degree six at 93/100 exceeds 197/78,
so log(pi_star/q_star)<93/100; and e>8/3 implies log(W_leaf)<5 since
W_leaf=320/3<(8/3)^5. Consequently

    D(pi||q) < (197/200)(93/100)+5/64 = 39767/40000 < 1.

This is an actual admitted finite example. Its exact calculation confirms
multiplicity and transition identities; its finite TV value does not prove
or numerically demonstrate a sharp asymptotic coefficient.

## Failures, costs and source status

The initial parent task wording missed D in reverse acceptance. This was a
real mathematical correction, not rounding or a relaxed test. No code run
failed. The first exact invocation checked transition/lumping algebra only;
a second added the exact KL admission certificate. Measured body wall/CPU
seconds were respectively 0.023068317/0.023065342 and
0.024186383/0.024187892. Interpreter startup, proof reading/writing, model
reasoning, tokens, money and full discovery cost are not included in those
numbers; unavailable totals remain unknown. One finite family and one fixed
horizon were used, with no parameter search or old campaign replay.

I read the incoming instrument proof, the relevant control proof transfer,
and the complete prior path-lower proof. This challenge does not certify
historical novelty, practical sampling speed, external acceptance or another
owner's science. Root owner acceptance and Max integration remain separate.

Final proof hashes and acceptance scope will be appended after the root and
constructor finish their source, without silently extending this review.

## Source-bound acceptance of the contributor's complete proof

At 2026-10-21T20:22:06Z I finished reading the complete final contributor
source `contributors/branching_capture.md`: 16,560 bytes, SHA256
`3049740974cc39c468738d7fbebd5d6bfb0cb685f2fffcbb5ba84ec28ce98b04`.
**Accepted within its declared finite class.** The file incorporates the
reverse-factor correction and charges same-level global moves in the full
vertex exit bound. Its marked event uses all D children, its retention is
on the complete leaf set, and its constants and errors justify the logarithmic
capture estimate uniformly in the growing support. The KL proof is unaffected
by branching because it sums exact level masses.

I checked the optimization and the policy/log-risk implications in Sections
6--7, including the capped case r_*>=1 and the order of fixed choices before
n tends to infinity. I found no remaining load-bearing defect. The illustrative
integer check is exact: 801^3=513,922,401 and 16*320^3=524,288,000, a positive
margin of 10,365,599. This confirms the declared lambda=3/2 separation; it
is not used as a substitute for the variational infimum argument.

The resulting source-bound acceptance covers the full new lower proof, the
matching policy coefficient conditional on the separately accepted incoming
upper, and the logarithmic risk exponent conditional on that same upper and
the inherited Q=I lower. It does not independently recertify the full incoming
upper or the older Q=I proof. A differently worded principal theorem requires
its own final-source reading; no claim about that not-yet-final document is
implied here.

The exact check now accepts `--output PATH` so a receiving replay can write
outside the preserved source directory. This final CLI-only edit adds no
scientific computation or altered assertion and was not counted as another
mathematical run. The default remains the adjacent JSON output.

## Source-bound acceptance of the principal theorem

At 2026-10-21T20:24:26Z I completed the distinct source-bound reading of
`BRANCHING_SHARPNESS.md`: 18,091 bytes, SHA256
`0aecfb4bc46390a1a859308a47dd7af64ebddd83a89e18587ba70b42fddf633f`.
**Accepted without a load-bearing repair.** This verdict binds these precise
bytes and is not inferred from the contributor proof's acceptance.

The principal uses the exact level quotient, whereas the contributor charges
same-level jumps as failed vertex exits. The principal's sharper E in (11)
is valid: the total proposal mass of the star and levels above i is exactly
`1-sum_{j=0}^i b z^j`, at most 1-b. All these global moves accept. Global moves
to a lower level j have accepted mass `b z^i n^-2(i-j)`, so their total is at
most b/(n²-1). Within-level jumps are genuine quotient holds, established
by strong lumpability, and must not be charged as additional level exits.
These facts account for every nonself quotient transition in E. The accepted
global star exit gives the claimed lower bound D_0.

Equations (12)--(14) are a valid actual marked-event bound: the geometric
waiting identity holds in the level chain, the successive conditional marks
need no waiting-time independence, and leaf-union retention retains all moves
within that union. Equation (15) controls the accumulated error, not merely
per-edge error: eta[(M+2)log L+log b]+m eta log D=o(1) for the fixed-parameter
regime. Extra competing-exit terms are O(n^-2), and m times that error is o(1).
The O(1) integer-depth rounding in (17) is justified by the bounded derivative
specified there. The finite-family positivity, KL slack and growing support
arguments are independent of support cardinality.

The infimum in (19) is taken over the standing positive b range established
in Section 3, namely 0<b<1-exp(-K). I suggested displaying that lower bound
explicitly for readability; it is already an assumption of the construction
and no mathematical repair is required. Fixed finite D,b,v are chosen for
any strict exponent margin before n tends to infinity. This suffices both
below c_*=1 and in the capped case r_0>=1; no optimizer at finite v is asserted
in the latter case.

I checked the principal's own two-state lower: G's nontrivial eigenvalue is
1-1/(nL²), so C's is exactly 1-alpha/(2nL²), and the q-start deficit is
(p_0-q_0) times that eigenvalue to the nth power. Its KL tends to k<K.
Consequently the eta-independent logarithmic exponent bound and K coefficient
are correct. For a direct accuracy lower when A<K, choose k in (A,K); the
same instance at n=floor(exp(A/epsilon)) has error/epsilon tending to k/A>1.
This supplies the K part of the policy lower without diagonal monotonicity.

For Theorem 1, the received finite upper applies eventually since eta_n tends
to zero. At R=n/(log n)^4 its base-log errors multiplied by eta_n are o(1),
justifying (20). The tree lower is only needed when lambda c_*<1, in which
case M>2 automatically makes the target leaf mass negligible after a strict
phi choice. At equality, the ordinary lower and limiting strict upper
exponents match at one; no prefactor is inferred. For Theorem 2, fixed A,d
lead to u/loglog n->Ad. The chosen strict tree exponent makes its actual
error/epsilon diverge. Within-instance TV monotonicity then yields the
mixing-time lower, matching the separately accepted incoming upper.

This review accepts the two stated theorems within the native finite positive
class, conditional on their named received upper dependency, which I did not
independently re-prove in this challenge. It does not claim a formal-kernel
proof, historical originality, finite-time speedup, numerical asymptotic
confirmation or external mathematical acceptance. The open critical prefactor
is appropriately left open. No further numerical runs were needed for this
principal-source review; the two exact-check costs above are the entire
executed calculation record of this challenge.

## Final source rebind after notation clarification

At 2026-10-21T20:25:03.254281+00:00, the principal explicitly wrote `0<b` in (19).
The final theorem is 18,093 bytes, SHA256
`119dfb8d0b8e77b3ce93fdef1f1450c01fc1d090a0f05c4dd7ae0ea7ada1d645`.
I verified byte-for-byte that this is the only change from the completely
reviewed main source: deleting that inserted `0<` reproduces its prior hash.
The acceptance above therefore applies to these final bytes without a new
scientific obligation or repeated review. This final binding supersedes the
previous principal-source digest; all substantive review findings stand.
