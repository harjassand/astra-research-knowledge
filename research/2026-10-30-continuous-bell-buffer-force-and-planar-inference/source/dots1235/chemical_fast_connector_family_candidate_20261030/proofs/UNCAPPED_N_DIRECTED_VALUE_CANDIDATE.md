# Uncapped N-directed actual value: pointwise section and weighted repair
Status: NEW PERSONAL DERIVATION, unreviewed. Depends on the strict-power clearing theorem and the finite reset-walk estimate in N_DIRECTED_RESET_WALK_V2.md. The pointwise section below replaces the latter file's more delicate post-clearing-law section. No general weakly reversible recurrence claim.

## 0. Contract and exact scalar geometry
Composition species X_1=A,...,X_k, k>=2. Fast graph: finite strongly connected homogeneous degree-m composition complexes containing all pure mX_i, with a common catalyst qB. Integers q>m>=2. Connector0->A+B->mA+qB->0, all constants fixed positive. Put h=q-m and

    H(0)=0;
    H(B)=a(m-1)+v if B-1=a(q-1)+v-1, 1<=v<=q-1;
    r=N-H(B).

Only immigration can raise r, by h at positive B divisible by q-1. Only clearing can lower it, by h at B>=2q-1 congruent1 modulo q-1. All other jumps preserve r. In particular B=q->0 clearing is neutral. Also H(B)=[(m-1)/(q-1)]B+O(1).

Fix a strict clearing exponent epsilon>0 from the independently proved accessibility theorem. Write p(r)=r^{-(m-1+epsilon)}, beta(r)=p(r)^(1/m). Choose rational alpha>0 with alpha h<epsilon and alpha<1, and let phi(r)=Gamma(r+1)^alpha for large positive integer r. Every fixed polynomial enlargement of phi has the same fixed-shift exponents.

## 1. Nonexplosion is earned independently
For V_1=1+N+B, fast reactions have zero drift. Connector drift is bounded above by

    C+C AB-c(A)_m(B)_q.

If B<q it is O(1+N); if A<m it is O(1+B). When A>=m,B>=q, falling factorials dominate fixed positive multiples of A^m,B^q, and Young's inequality bounds C AB-c'A^mB^q above by a constant because q>m. Thus LV_1<=C V_1 globally. Finite sublevels and stopped localization rule out explosion. This argument does not use recurrence or a stationary distribution.

## 2. Fast processing and reset kernels
The strict clearing mean gives, before the next competing birth,

    P(immigration before clearing)<=Cp(r)B^-q,
    P(activation before clearing)<=C r^{-(m-2+epsilon)}B^(1-q),

uniformly over all hidden compositions with r large, since N=r+H(B)>=r. Clearing output obeys the actual compensator bound

    E[(1+A_after)^-m; clearing before birth]<=Cp(r).

A fast processing segment stops at B=q (if newly entered), B<q, a downward r exit, or the first immigration. Additional activations preserve B modulo q-1. At most q-1 clearings without immigration yield a low phase, the section, or a downward exit. Additional activations have uniformly o(1) probability per clearing stage, so the expected number of stages is bounded. Immigration is a bad branch of mass at most Cp(r). Every low output is an actual clearing reset. Activation from b=1 lands directly on the section S and terminates repair. For a segment started by low-phase activation at b>=2, no-immigration/no-downward low output has phase at most b-1, and its normalized joint output law has inverse-moment bound Cp(r): direct first clearing gives a low return with probability1-o(1).

The reset-walk lemma gives, from a fresh low-phase reset at b, upward/bad escape before reaching the section or a downward exit bounded by

    C p(r)^{min(q-b,m)/m}.

At B=0, compulsory immigration followed by this walk gives the stronger Cp(r), because q-1>=m. From arbitrary low-phase input no inverse-moment premise is imposed: before its first fast entry B only increases, so r can increase by at most h, and the mean time is bounded by a constant (immigration supplies a fixed positive rate).

### Final-clearing disintegration (conditioning control)
At EVERY fast-stage entrance, let K_D be the subprobability kernel for clearing before either birth. Its mass is at least1/2 for large r, and K_D[(1+A_after)^-m]<=Cp(r). Therefore the stronger relative inequality K_D[f]<=2Cp(r) K_D[1] holds. The terminal low phase or downward-exit classification is determined by the pre-clearing B, not by A_after. Decomposing any fast episode by its final clearing-stage input and then normalizing preserves this relative bound, even when a particular final phase is rare. This is an actual kernel disintegration; it never conditions on the newly observed A and asserts a false pointwise moment bound.

## 3. Weighted repair to the pointwise section S={B=q}
Stop also at r<=r0, with terminal value zero. For an arbitrary fast state B>=q, repair to S proceeds through the fast processing and fresh low-phase kernels above. A downward branch has weight ratio O(r^-alpha h). A fresh low-phase upward branch has probability O(beta(r)), with weight ratio O(r^alpha h). A fast bad-immigration branch has probability O(p(r)), with that same maximal ratio. All three weighted nonterminal factors tend to zero because alpha h<epsilon< (m-1+epsilon)/m.

A repair round composes one fast processing segment, when needed, WITH the ensuing fresh low-phase walk up to section/up/down/bad stopping. The neutral fast-to-low transition is inside that round; it must not be miscounted as a small-probability continuation. Only downward exits and bad active states feed another round (a low upward wrap lands directly in S). Equivalently, the two-type fast/low kernel has a unit fast-to-low entry but small reverse/other continuation entries, and its two-step continuation norm is small.

This is a positive-kernel Neumann construction, not an assumption that repair already has finite mean. Iterating killed repair rounds gives:

(a) From every fast input, expected terminal phi at S is <=C phi(r), and expected running phi-cost during repair is <=C phi(r), uniformly in the unbounded hidden fiber.

(b) From a fresh low-phase reset, the same bounds hold. From a FRESH clearing-reset law at B=0 specifically (not an arbitrary observed B=0 composition),

    E phi(r_S) <=[1+C p(r)r^(alpha h)]phi(r),              (R0)

because a path reaching S at the same level contributes exactly phi(r), a downward branch followed by repair costs at most C phi(r-h)<=phi(r) for large r, and all upward/bad branches together have mass Cp(r).

(c) From a fast state B=2q-1, every first clearing without immigration is downward, regardless of intervening activations. Therefore

    E phi(r_S)<=C phi(r-h)+Cp(r)phi(r+h)=o(phi(r)).         (R1)

(d) From any arbitrary low-phase state, the initial uncorrected approach costs at most C r^(alpha h)phi(r), after which (a) applies or S has already been reached.

The same statements hold for weight Psi(r)=(1+r)^(m-1)phi(r), and for the corresponding running-cost bounds, since fixed polynomial factors do not alter the small weighted-branch exponents. To make the Neumann estimate formal, take supremum normalized repair values over all r>=r0 and all relevant input states, first with a finite number of repair rounds. The continuation coefficient is at most C[r0^-alpha h+beta(r0)r0^(alpha h)+p(r0)r0^(alpha h)] after increasing r0; choose it below1/2 and pass monotonically to the limit. At r near the threshold use terminal zero; no claim of an invariant domain is made.

## 4. Pointwise section-return drift, with no observed-A moment assumption
Start from ANY state on S, B=q. Here N=r+m, so all large-r states are active. Wait for the first clearing/immigration/activation, allowing all actual fast reactions meanwhile. Let P_D,P_I,P_T be the three probabilities. Then P_I<=Cp(r), P_D=1-o(1), and

    P_T>=c r^{-(m-1)}P_D>=c' r^{-(m-1)}.                  (5)

The first inequality is pointwise competing-hazard comparison: lambda_T>=c r^{-(m-1)}lambda_D when clearing is enabled; elsewhere lambda_D=0. No stationary average is used.

- Clearing-first lands at B=0 with the actual inverse-moment reset law. Apply (R0).
- Activation-first lands at B=2q-1 with unchanged r. Apply (R1).
- Immigration-first lands at B=q+1 with unchanged r. Apply uniform fast repair bound (a).

Consequently the actual return kernel to S (killed at r<=r0) satisfies, pointwise for EVERY incoming composition,

    E phi(r_next) <=[1-c r^{-(m-1)}+C p(r)r^(alpha h)]phi(r)
                  <=[1-c' r^{-(m-1)}]phi(r).              (6)

The same estimate holds for Psi. Expected running phi-cost per section-return cycle is <=C phi(r), including real time spent in the fast subsystem and all repair rounds. The section state includes the full composition; only the reset kernels INSIDE a cycle are averaged. Thus there is no false assertion of a moment bound after observing A.

## 5. Construct the actual global N-directed stopped value
For Psi, (6) gives E Psi(r_next)<=Psi(r)-c phi(r). Telescoping the actual embedded section-return chain bounds expected total phi-cost until threshold by C Psi(r). Initial repair from arbitrary states costs at most C r^(alpha h)Psi(r). Therefore

    W_r(x)=E_x integral_0^T phi(r(X_t))dt,
    T=inf{t:r(X_t)<=r0},

is finite for all r>r0 and satisfies

    W_r(x)<=C(1+r)^(m-1+alpha h)phi(r),
    L W_r=-phi(r) when r>r0.

Set W_r=0 below threshold. First-jump dynamic programming earns the generator equality. No globally supplied Lyapunov barrier, rapid mixing, or finite expected physical return time was assumed. Normlike coercivity of W_r alone is NOT claimed because its threshold is noncompact.

Only immigration can jump from the exterior into r>r0, its rate is constant, and the target r belongs to a fixed finite band. The uniform hidden-fiber upper bound therefore gives

    (L W_r)^+<=C on r<=r0.                               (7)

A first-holding lower bound is W_r>=phi(r)/[C(1+N+B)^(m+q)] inside the domain. This is useful only in conjunction with a complementary residual.

## Review obligations
The crucial dependencies to challenge are the joint reset-walk lemma (not products of unconditional marginals), the weighted repair estimates (R0)-(R1), and the actual section-return stopping construction. This file is a candidate, not a declaration that those checks are complete. If any of them fails, the N-directed value and global closure must remain open.
