# A cooperative two-A fast-connector recurrence construction

1 November 2026. Solo mathematical construction and review. **No independent
audit, external novelty clearance, physical validation or mission success is
claimed.** This file depends on the detailed local derivation in
`COOPERATIVE_LOCAL_PROOF.md`, not on inheriting the accepted one-A theorem.

## Statement

Take the finite fixed graph and fixed positive rates in the local proof. Put
q=m+1, m>=3. Attach the same qB catalyst to every fast composition complex,
and add the directed connector cycle

    0 -> A+B -> mA+qB -> 0,

with arbitrary fixed positive rates k_I,k_T,k_D. The composition graph is
strongly connected, contains mA and every 2A+(m-2)X_i, every complex contains
at least 2A, and every latter source has an A-increasing edge.

The construction below yields nonexplosion from every integer state, positive
recurrence of each communicating class, and every exponential invariant moment
of S=N+B. Constants are not uniform in dimension, graph, degree or rates.
This is a restricted structural family, not general weakly reversible recurrence.
The extension to minimum A>=3 or arbitrary connector geometry is NOT proved.

## 1. Nonexplosion is independent of the stopping constructions

Fast jumps conserve S. The connector gives

    L(1+S) <= C + C AB - c(A)_m(B)_q <= C'(1+S).

If A<m or B<q, AB is at most a constant times S. On the complementary
quadrant, fixed falling-factorial lower bounds show that the negative product
dominates AB outside a bounded A/B region. Finite-sublevel stopped Dynkin
and Gronwall therefore exclude finite-time escape. Each finite set has bounded
total rate, so the full process is nonexplosive. Large hidden pools cause no
problem in this argument because their fast jumps conserve S.

## 2. Exact geometry and the two inactive faces

Let nu=m-1 and a=nu/m<1. Set H(0)=0. For B=um+v with 1<=v<=m, put

    H(B)=u(m-1)+v,       r=N-H(B).

Then 0<=H(B)-aB<=1. Activation is r-neutral; immigration raises r by one
only at positive B divisible by m; clearing lowers r by one only at
B>=2q-1 congruent to 1 modulo m. All other r changes are zero. In particular
N>=r and, at B=q, N=r+m. From B=2q-1 the first clearing before immigration
is down-r, regardless of intervening activations. These identities use actual
count shifts, including the special neutral clearing q->0.

Let I indicate that a composition source is enabled, independently of B.
Fast jumps preserve I; adding A cannot turn it off. Strong connectivity gives
an enabled path from any enabled source to mA. Set

    K=(m-1)+(d-1)(m-3).

For N>K, inactivity is exactly A=0 or A=1. Indeed A>=m enables mA, and
2<=A<m with every X_i<m-2 has N<=K. The two unbounded inactive faces are
never called a finite head. From A=0 one immigration gives A=1; from A=1 the
next immigration gives A=2 and activity, or activation gives A=m and activity.
Thus at most two actual events seed activity for large N. Their total mean
physical waiting time is bounded, and r can increase by at most two. We pay
these events whenever needed; no population reset is postulated.

Use the **active** section Q={B=q,I=1}. An inactive state with B=q is seeded,
not silently admitted as an active local input.

## 3. A finite-degree high-phase processor with carried weights

Start at a fully specified active input with B>=q and large r. Run actual fast
stages until a section return, a low phase B<q, a down-r clearing, an immigration
in a high phase, or an inactive clearing output. The last two are bad branches
and will be physically continued. Stop on a section entrance before processing
another stage there. When studying departure from Q, process its first event
separately, as in Section 6.

Without immigration, activation preserves B modulo m, and every clearing lowers
that residue by one. At most m clearings precede one of these stops. There may
be arbitrarily many extra activations. At a stage entrance the local proof gives

    K_D g_j <= M_j g_j,
    K_T g_j(A+nu) <= C p(r) g_j,
    T_stage <= C g_m/(B)_q,
    p(r)=r^(-(m-2)).                                  (14)

These are positive-kernel row inequalities before the output is observed.
For a word with ell extra activations and at most m clearings its weighted
operator norm is at most M_j^m[Cp(r)]^ell. There are at most C(1+ell)^m
placements. The positive series converges for large r. Therefore every terminal
low-output subkernel satisfies a carried bound C_j g_j(input). The total bad
probability is at most C g_m(input): use the stage time envelope for immigration
and 1_{A_after<2}<=2^m g_m(A_after) for inactive outputs.

Unweighted activation probability is uniformly o(1), by the actual occupation
bound in the local proof. The analogous unweighted word series bounds the
expected stage count and physical duration uniformly. It also gives total bad
mass O(p(r)), using the uniform time bound and the actual inactive-output mass.
No finite B cap or hidden N cap is present.

Every selected final clearing output has conditional inverse m-moment O(p(r))
when the selection uses its pre-clearing phase. Disintegrate by the FINAL stage
entrance, use K_D g_m<=Cp(r)K_D1 there, then integrate. This remains true for
a rare down exit or low phase. General selection on the observed A is treated
as an unnormalized positive subkernel, never given an independent fresh law.
There is one useful proved exception: discarding A<=c can only DECREASE a
conditional inverse-power moment, since g_m decreases with A. Thus the explicit
upward threshold filters A>=2 and A>A_* used below preserve the relative bound.
No other output-dependent conditioning is inferred to do so.

For activation from low phase b>=2, a nonbad low output has phase c<=b-1.
For b=1 activation reaches Q immediately. This special case is retained.

## 4. The new carried low-phase escape bound

For 1<=b<=m, let E_b(A) be the probability, from the actual observed low state,
of up-r escape or a bad processor branch before Q or a safe down exit.
The state includes all hidden counts. We also allow stopping as bad when a low
output has A<=A_*; its physical continuation will be paid by the priming step
in Section 5. This can only increase the escape probability to be bounded.

At low b, immigration probability is at most c/(1+A). It raises A by one.
Activation adds nu A, then its processor has carried output bounds (14), low
phase at most b-1, and bad probability <=C g_m(A). Consequently a supersolution
has the form

    h_b(A)=C_b g_(m+1-b)(A).                         (15)

Here is a noncircular choice of constants. First choose positive shape constants
d_b, with d_b>=4c d_(b+1), and d_m large enough to pay the boundary b=m+1
whose escape value is one. In an activation branch the next exponent is at
least m+2-b, so its ratio to (15) is at most a fixed multiple of 1/(1+A).
The immigration term uses at most one quarter of (15). Choose A_* sufficiently
large to make all the activation ratios at most one quarter. The processor bad
term is C g_m; it can be paid by enlarging a COMMON multiplier M of all d_b.
Choose that same multiplier large enough that M d_b g_(m+1-b)>=1 on A<=A_*.
It changes no neighboring ratios, so it does not undo the choice of A_*.

Finite-horizon positive-kernel iteration now proves E_b<=h_b; no prior exit
integrability is needed for this inequality. For b=1 the activation branch
is zero because it hits Q directly. The construction retains observed A until
the actual kernel integrates it, rather than substituting a worst uniform reset.

At a genuine first clearing output at B=0, the compulsory immigration to B=1
preserves r and raises A. Thus (15) gives the essential first-law bound

    P(up/bad from that output law)
      <= C K_D g_m(A_after) <= C T_actual.             (16)

T_actual is the time at the preceding section stage, not the worst-case time
of a later reset. This is the bridge that the coarse Holder reset expansion
did not provide. By the local theorem T_actual/U_actual<=C/log r.

## 5. Physical repair and actual running cost

Later fresh low laws only need the weaker uniform inverse moment Cp(r).
An ell-immigration run has row mass <=C_ell p(r)^(min(ell,m)/m), by the actual
race probabilities and Holder. Index kernels BEFORE sampling reset output.
If m consecutive run transitions contain no immigration, their low phases
strictly decrease to absorption. A surviving m-step kernel therefore has row
mass O(p(r)^(1/m)). Its positive geometric series bounds expected run count.
The total fresh-low up/bad mass is O(p(r)^(1/m)). The A<=A_* bad stop has
mass O(p(r)) and only shortens this walk. Low holding times have the constant
immigration floor; together with Section 3 this bounds round duration uniformly.

After any observed bad low state, at most q actual low jumps enter a high phase
or Q. Their mean time is bounded and r rises by a bounded amount. After a
high inactive output, the at-most-two-event seeding in Section 2 does the same.
Every bad state is continued from its actual counts and physical clock.

Fix theta>=log 8, increasing it later if a larger invariant moment is wanted.
Let phi(r)=exp(theta r) above a large r_0. A repair round includes its active
processor TOGETHER WITH the ensuing fresh low walk. A unit-mass neutral
fast-to-low transition stays inside the round. Safe down continuations cost
the exact ratio exp(-theta); all bad continuations have mass epsilon(r)->0
and a bounded upward overshoot, whose weight cost is a fixed C_theta.
Inactive down outputs are counted in the rare bad joint kernel; their seeding
is not assumed to preserve a pointwise down margin.

Truncate after n rounds. The largest normalized expected terminal phi-weight
has the inequality

    M_n <= 1 + [exp(-theta)+C_theta sup_(r>r0)epsilon(r)] M_(n-1).

Choose r_0 so the bracket is <=1/2. Positive monotone iteration gives terminal
weight <=2phi(r), uniformly in the fully observed active input and admissible
fresh low law. The identical iteration for the physical running integral has
a finite C_theta in place of 1; its value is <=C_theta phi(r). It also bounds
the expected number of rounds, and hence earns termination in real time.
An arbitrary initial low or inactive input pays the bounded priming/seeding
overshoot once. These bounds hold as well for a polynomial times phi, after
enlarging r_0; its fixed-shift ratios are bounded and tend to their exponential
ratios. No noncompact target has been assumed recurrent.

## 6. Section contraction uses time versus occupation

At an active section state N=r+m, write T,U for the ACTUAL first-stage physical
time and occupation. Its activation probability is exactly k_T q U.

If clearing is first, its output has B=0 at the same r. Safe same-level return
contributes exactly phi(r). Safe down continuations have terminal bound
2phi(r-1)<=phi(r). The remaining branch mass is bounded by (16), and physical
repair pays only a fixed C_theta factor. Thus its total contribution is at most

    P_D phi(r) + C_theta T phi(r).

If activation is first it enters B=2q-1. Before an immigration its first clearing
is down-r, even after extra activations. Uniform bad immigration/inactive-output
mass is o(1). Its repaired terminal weight is at most

    [2exp(-theta)+o(1) C_theta]phi(r) <= phi(r)/2.

An immigration first has probability k_I T and a bounded repair weight. Therefore

    E phi(r_next) <= [1-cU+C_theta T]phi(r)
                      <= [1-c' r^(-(m-1))]phi(r).      (17)

The last line uses the LOGARITHMIC ratio T/U->0 and the local opportunity lower
bound U>=cN^(-(m-1)). It assumes neither a strict-power clearing estimate nor
an independent reset. Section inputs are fully observed active states.

Repeat this branch proof for Psi(r)=(1+r)^(m-1)phi(r). Same-level returns still
have coefficient EXACTLY one; down ratios remain favorable, and only rare bad
branches pay bounded upward ratios. Thus

    E Psi(r_next) <= Psi(r)-c phi(r).                  (18)

Appending a generic O(1/r) multiplicative error to (17) would be invalid, since
its negative drift may be only order r^(-(m-1)); the branch proof avoids it.
Each actual section cycle has expected physical phi-cost <=C_theta phi(r).
Telescoping (18), using positive stopped iteration, constructs the finite value

    W_r(x)=E_x integral_0^{tau_(r<=r0)} phi(r_s) ds
           <= C_theta (1+r)^(m-1)phi(r),
    L W_r=-phi(r) on r>r_0.                           (19)

The initial repair is included. Define W_r=0 below threshold. Only constant-rate
immigration enters its positive domain from outside, into a fixed residual band;
the bound uniform in hidden coordinates gives bounded positive exterior leakage.

## 7. The complementary uncapped activity-credit trace

Set Z=B-N-I. Its nonzero jumps are +1 for active activation; -1 for immigration
turning activity on; and -1 for clearing whose target remains active. Inactive
activation and clearing to an inactive target are neutral. These are exact
identities, including A=0 and A=1.

All active finite-N classes can reach mA and clear by an enabled complex path.
The large-N local estimates, combined with these finitely many active classes,
give normalized time and A-occupation bounded uniformly over ALL active N.
Restoring B, at Z=z large, B>=z and

    P(high immigration first)<=CB^-q,
    P(active activation first)<=CB^(1-q),
    E(first connector time)<=CB^-q.                  (20)

For sufficiently large N, clearing's inactive-output probability is at most
1/4 uniformly. An active large-N input therefore has a down-Z clearing with
probability at least 1/2 before a birth, for large z. For a large inactive input,
A=0 first waits for its actual immigration to A=1. From A=1, immigration gives
a down-Z activation of the source, or activation seeds an active input. Applying
the preceding clearing stage gives a down probability bounded below and a
bounded physical block mean. Neutral inactive outputs may restart a block.

The remaining bounded-N head is treated by actual prescribed paths. Clear from
active states; if the target is inactive with A>=1, activate then clear. A neutral
pair lowers N by one, so a bounded number of such pairs reaches a down exit or
inactive A=0. At most m immigrations then activate mA. The first is compulsory;
each of the at most m-1 competitive ones has probability at least c/z in this
bounded head. Failures stop the block, and neutral failures restart at the SAME Z.
Only active activation can exit up. Equation (20), over the bounded number of
stages, consequently gives uniformly over the whole hidden composition,

    P(block down)>=c z^(-(m-1)),
    P(block up)<=C z^(-m),
    E(block physical duration)<=C.

Conditional renewal (not independent blocks) implies

    P(first Z exit up)<=C/z,
    E(first Z exit time)<=C z^(m-1).                 (21)

Global nonexplosion was proved first, so the neutral excursions used here are
legitimate. Fixed-shift exponential ratios in (21) contract both exp(theta Z)
and (1+Z)^(m-1)exp(theta Z) for large Z. Positive iteration, paying the excursion
time in (21), gives the actual stopped value

    W_Z<=C_theta(1+Z)^(m-1)exp(theta Z),
    L W_Z=-exp(theta Z) on Z>z_0.                    (22)

It vanishes below threshold. Only active activation enters the positive domain
from outside, into a fixed Z band. Its exterior leakage is at most CAB on that
INFINITE strip, not on a fictitious finite boundary.

## 8. Global gluing and invariant moments

For either stopped value the first actual holding interval gives a lower bound
exp(theta residual)/[C(1+S)^(m+q)] above its threshold. Since

    (1+a)(B-N)+2(N-aB)=(1-a)(N+B),

we have max(r,Z)>=S/(4m-1)-C. Thus V=1+W_r+W_Z is normlike for any fixed
theta>0. If Z is on its leakage strip at large S, r is a linear fraction of S,
so its negative exponential absorbs CAB. If r is below threshold, Z is a linear
fraction of S and absorbs W_r's bounded leakage. Where both are high both drifts
are negative; both residuals bounded above force bounded S.

Given any lambda>0, choose theta sufficiently large, for example larger than
(4m-1)(lambda+1) and log 8, then choose its residual thresholds as above. We obtain

    LV <= -exp(lambda S)+b_lambda 1_(F_lambda)

for a finite F_lambda. The nonexplosive countable-state Foster argument proves
positive recurrence of every closed class. All communicating classes are closed:
any enabled reaction x=z+y -> z+y' has an enabled return along a reaction-graph
path y'->...->y with the same nonnegative residual z. The full graph is strongly
connected through mA+qB.

For a finite-mean regenerative return cycle sigma in a positive recurrent class,
localized Dynkin, nonnegativity of V and monotone/Fatou passage give

    E integral_0^sigma exp(lambda S_t)dt
         <= V(X_0)+b_lambda E sigma < infinity.

The regenerative occupation identity yields the class invariant exponential
moment. No prior invariant integrability of V was used.

## Boundary of the result

The new inputs are the two-A logarithmic occupation argument and a carried
inverse-power committor bound; ordinary stopped Green identities, positive-kernel
iteration and Foster localization remain standard tools. The pure-source theorem
is already accepted Astra work, and the one-A theorem already repairs its own
siphon. This construction does not rebrand either one as new. A failure of the
minimum-three-A ratio is not a failure of recurrence for that family.

Current status: a fully written SOLO CANDIDATE PROOF with numerical implementation
controls for its local bridge. A separate independent whole-proof review has
NOT been performed. External novelty and a consequential broader capability
remain UNKNOWN/NOT_ACHIEVED.
