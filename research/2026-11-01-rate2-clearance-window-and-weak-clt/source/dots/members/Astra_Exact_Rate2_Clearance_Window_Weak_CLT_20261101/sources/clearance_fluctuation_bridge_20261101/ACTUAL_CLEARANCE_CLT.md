# Actual rate-2 clearance-time CLT: growing stopped-clock bridge

**Author theorem, pending independent review.** This is a weak-convergence result for the actual twelve-channel chain, not a finite-N distributional error bound or a moment-convergence theorem. It does not change any rate, initial state, target, or accepted source. No stationary fast-fiber law is assumed.

## Result and the precise remaining limitations

Let the actual count chain have the twelve reactions in the accepted task-observable corrector, with coefficient **2** on CD→AE and falling-factorial A(A−1) rates on each 2A source. Start at `(A,B,C,D,E)=(0,N,1,1,0)`, put `T=N^(1/5)`, and define

    tau = inf{t: A+B+C+D+E <= 15(N+2)/16}.

Let `(l,e)` solve `l'=1+3l²e, e'=2l²`, starting from `(0,0)`, with blow-up time `s_*`. Let `b(l,e)` be its deterministic remaining time to blow-up. Then

    (tau - s_* T)/sqrt(T)  ==>  Normal(0, Sigma²),
    Sigma² = integral_0^{s_*} b_l(l(s),e(s))²(1+3l(s)²e(s)) ds
           = integral_0^infinity b_l(l,e(l))² dl.                 (1)

The integral is finite and strictly positive. This bridge identifies the previously deterministic candidate as the limiting **weak-fluctuation parameter of the actual clearance law**. It does NOT establish `Var(tau)/T -> Sigma²`, convergence of means, uniform integrability, a finite-N CDF bound, a finite-noise diffusion formula, or a practical finite-N evaluator. Those are separate statements.

The accepted scalar enclosure for `s_*` and separately reviewed acquisition of the integral may be attached as numerical evaluations of (1). Their numerical certification is not part of this proof. In particular this source does not independently accept the variance solver.

### What is new in this bridge

A genuinely growing cutoff `L approximately T^(3/2)` replaces an invalid fixed-K truncation. Between a fixed `KT` and this cutoff, weighted **full-generator** residuals are summable, and the full corrected-martingale bracket is bounded by `C/(T K^4)`. The omitted-channel event is paid only as an admission failure, at cost `O(T^(-1/4))`; no omitted term is removed from the generator or bracket. The remaining actual all-channel amplification and physical removal take `O(T^(1/4))+5=o(sqrt(T))`. Ordinary martingale characteristic functions are a component, not a novelty claim.

## 1. Received inputs and conventions

The exact source hashes are recorded in `SOURCE_BINDINGS.json`. The proof receives:

1. The accepted full-chain C² corrector `TASK_OBSERVABLE_CORRECTOR.md` and its independent review: all twelve jumps, exact drift, segment residual and actual corrected bracket.
2. The accepted fixed-level induction entrance and actual clearance continuation in `rate2_induction_clock_20261101`, including its source-bound review. For each fixed `K>=10^40`, the actual first `L>=KT` entrance is admissible for the dyadic stages with probability tending to one; its time is `<3T`; no omitted reaction has occurred on the received good event. Its compact path residuals also give the fixed-compact LLN, as detailed below.
3. The accepted full-chain dyadic stage lemma, its receiving conventions, and the continuation's explicitly received occupation clock. At a stage of scale `m`, write `w=sqrt(Nm)`. Before its common stop,

       m/2 <= L <= 2m,   w/2 <= E <= 2w,   A<=m/16,
       B<=2N,   int A dt <= 10^4 w/N,
       duration <= 16w/m².                                 (2)

   Its complete good event excludes all auxiliary exits and supplies the next actual entrance at `2m`. Its conditional failure probability is at most `16 exp(-m/(3*10^12))`. Every stage is the same continuing process and reference N. Band exit is adverse here, including a simultaneous band/L exit.
4. The accepted deterministic remaining clock and conditional cone derivative bounds, including their independent receipts.
5. The accepted actual macro/interior continuation. Its existence constants `c(delta/4)>0` and `n0(delta/4)<infinity`, with `delta=10^-100`, are sufficient asymptotically. Their numerical acquisition is NOT silently claimed.

All martingales below are stopped *before applying* any probabilistic inequality. Additional occupation, count, jump/tube and omitted-mark exits are genuine admission failures. Bounds are not martingale assertions conditioned on future good histories. Stopping jumps and all one-jump targets are included.

## 2. Clock smoothness, including the initial boundary

The received inverse-flow construction proves smoothness of b at `l>0,e>0`, the PDE

    (1+3l²e)b_l + 2l² b_e = -1,                            (3)

and `|b_l|<=1` on the quadrant. It also proves the cone bounds. A short local extension fills the initial-boundary regularity needed here: for any nonnegative initial point choose a positive forward time h, shorter than its blow-up time, at which its deterministic flow has both coordinates strictly positive. This holds even at the origin because `l'>=1` and then `e'>0`. On a neighborhood of that initial point the flow at h exists smoothly and remains in the positive interior. Define there

    b_ext(z)=h+b(flow_h(z)).

On nonnegative starting points this agrees with the remaining time by the flow property. These extensions agree locally wherever needed, and give bounded C² norms on every fixed compact union of physical jump segments. Thus no singular inverse expression is evaluated at `l=0`. In particular `b_l(0,0)=-1` by (3), so the variance in (1) is positive.

For later use, in the cone `l>=g e²`, direct inverse-flow integration also gives

    b(l,e) <= integral_e^infinity (2g²v^4)^(-1) dv
           = 1/(6g² e³).                                 (4)

## 3. A fixed-compact actual martingale CLT and its covariance

Fix K, with `K>=10^40`, throughout this section. Let `t_K` be the first actual `L>=KT`. Use the accepted `E` ceiling, time ceiling `3T`, count stop `I>8T`, and first omitted-mark stop, where

    omitted = {A→0, the three 2A exits, AC→2A, AD→2A}.

These are not deleted channels: stop the FULL chain at their first mark. Before that stop, `Z=C-D=0` and `n-N=2+I`. Impose also the actual compact occupation budget

    int A dt <= h_K/T²,  h_K=100(K+1)².                   (5)

The accepted full-chain A-clock estimate gives its failure probability `exp(-c_K T³)` for sufficiently large T; its hypotheses hold with count width `10T`. The first omitted-mark probability before the other compact stops is `O_K(T^-1)`, since its exact intensity is

    q_rem=A+3A(A-1)+A(C+D) <= (1+5L)A.                    (6)

Count failure is bounded by the original `Poisson(4T+5)` tail above `8T`, which tends to zero exponentially. The received fixed-level theorem pays all other compact exits and earns the stage entrance with probability tending to one. Denote the resulting compact stopped time by `sigma_K`; on its good event it equals `t_K`. If a compact failure occurs, freeze all later construction.

Put `z=(L/T,E/T³)`, `h=AE`, and

    q(x)=b(z)+h b_l(z)/(NT).

The exact full-chain identity gives

    q(X_t)-q(X_0) = -t/T + integral_0^t R_b(X_u)du + M_b(t), (7)

at the common stop. Compact source formulas, with (5), `Z=0` before the stop and `|n-N|<=10T`, give

    int |R_b| dt <= C_K/T,
    <M_b> <= C_K/T,  max|Delta M_b|<=C_K/T.               (8)

Constants may depend on K but not N. One-jump endpoints of an omitted mark are covered by the compact enlargement.

### 3.1 Actual fast-source averaging, not an equilibrium substitution

The source's exact h identity is

    Gh=-Nh+3EL²+r_h.

On the SAME stopped compact domain, its literal residual and bracket bounds give

    int |r_h|dt=O_K(T^4),
    int q_hh dt=O_K(T^9),  sup h=O_K(T^4).

Consequently, uniformly in stopped physical times `t<=3T`,

    (1/T)int_0^t h du - (1/T)int_0^t 3EL²/N du
      = (h(0)-h(t)+M_h(t))/(NT) + (1/(NT))int_0^t r_h du
      -> 0 in probability.                               (9)

The deterministic terms are `O_K(T^-2)` and the squared maximal martingale term is `O_K(T^-3)`. Hence, in scaled time,

    (1/T)int_0^{sT} h du - int_0^s 3l_N(v)²e_N(v)dv ->0.  (10)

All integrals are stopped consistently. The primitive convergence also permits multiplication by any uniformly convergent continuous compact path weight: approximate the limiting weight by step functions and use positivity and tight total mass of `h dt/T`.

### 3.2 Fixed-compact law of large numbers used for the bracket

The accepted finite-level proof supplies, at its common stop, uniformly vanishing residuals in

    l_N=s+3e_N²/4+o_p(1),
    e_N=2int_0^s l_N²dv+o_p(1),

and its scalar time-shift sandwich. Equivalently, the full corrector with `f=l` and the E counter, together with (9), gives the same compact integral equations. On a fixed enlarged compact the drift is Lipschitz. Stopped Gronwall followed by the strictly positive crossing speed `l'>=1` yields

    sigma_K/T -> s_K,
    (l_N,e_N) -> (l,e) uniformly up to the stopped crossing,
    z(sigma_K) -> (K,e(s_K)),                             (11)

in probability, with deterministic paths frozen at their crossing. A proof may first work on a compact `L<(K+1)T` through a deterministic time just after `s_K` and before `s_(K+1)`; transversality then proves the stopping assertion. No Gronwall estimate is used as K grows, or beyond the deterministic blow-up.

### 3.3 The actual reaction covariance

For each actual reaction, write `u=Delta L, v=Delta E, w_r=Delta h`. The exact corrected jump is

    Delta q = Delta b + w_r b_l/(NT) + h' Delta b_l/(NT).

On the fixed compact, let `kappa_r=Delta q-b_l u/T`. The exact source sums imply

    int sum_r lambda_r kappa_r² dt = O_K(T^-3),
    int sum_r lambda_r (b_l u/T)² dt = O_K(T^-1).          (12)

Indeed the E part costs `int q_EE/T^6=O(T^-3)`; the fast correction costs `int q_hh/(N²T²)=O(T^-3)`; second-order b increments cost `int q_LL/T^4+int q_EE/T^12=O(T^-3)`; the product terms cost still less. Cauchy–Schwarz controls all cross terms. This retains, in particular, the nonzero AB/CD corrected marks.

The exact L-rate sum is

    q_LL=1+h+A+(3/2)A(A-1)+A(C+D)/4.

The integrated last three terms are `O_K(T^-1)`, using (5) and `A<=O_K(T)`. From (9)–(12),

    T<M_b>_(sigma_K)
      - (1/T)int_0^(sigma_K) b_l(z)²(1+h)dt ->0,
    T<M_b>_(sigma_K) -> Sigma_K²
       :=int_0^(s_K) b_l(l(s),e(s))²(1+3l(s)²e(s))ds.     (13)

This derives the coefficient `1+3l²e` from actual reaction intensities. It is not inserted as a diffusion premise. Similarly the scaled E martingale has variance bound

    T int q_EE/T^6 = O_K(T^-2) ->0,

and its covariance with the corrected l martingale vanishes by Cauchy–Schwarz. Thus the finite-compact leading noise has rank one in the l direction. The fast-source correction does not add a hidden leading covariance.

### 3.4 Elementary martingale CLT component

For completeness: if a scalar stopped martingale Y has jumps bounded by `j_N->0`, predictable bracket bounded by a fixed v, and terminal bracket converging in probability to `v0`, then `Y_terminal ==> Normal(0,v0)`. Apply the compensated jump formula to

    exp(i theta Y_t + theta²<Y>_t/2).

Its residual drift has absolute integrated expectation bounded by

    exp(theta² v/2) |theta|³ j_N v/6,

using `|exp(ix)-1-ix+x²/2|<=|x|³/6`. Thus its terminal expectation tends to one. Boundedness of the bracket and its convergence to `v0` then give characteristic-function convergence to `exp(-theta²v0/2)`. Localization at the stated budgets justifies all expectations. This argument is ordinary probability, not a new theorem.

Apply it with `Y=sqrt(T) M_b` and (8),(13). Therefore

    sqrt(T) M_b(sigma_K) ==> Normal(0,Sigma_K²).           (14)

## 4. A growing cutoff, and a paid small probability of omitted marks

For each fixed K and sufficiently large T, choose the least integer J with

    m_J=2^J KT >= T^(3/2).

Then `T^(3/2)<=m_J<2T^(3/2)`, while every active stage `j<J` has

    m_j=Tr_j,  K<=r_j<T^(1/2),  w_j=T³ sqrt(r_j).         (15)

Use the actual dyadic stages from `t_K` to this entrance, retaining all their stops, and stop additionally at the first omitted mark or `I>8T`. The original immigration clock is evaluated over `[0,4T+5]`. On no omitted mark, before every such stop,

    Z=0, n-N=2+I, |n-N|<=10T.                            (16)

The full generator still includes every omitted channel; (16) is merely a state constraint before an adverse first mark. Its terminal jump is included in the corrector.

From (2),(6), the actual omitted compensator in one admitted stage is at most

    11 m_j int A dt <= 110000 T^-1 r_j^(3/2).

The increasing geometric sum over `j<J` is less than

    400000 T^(-1/4).                                     (17)

Including the compact phase adds `C_K/T`. For the full chain stopped at its first omitted mark and all other budgets, the stopped count has expectation equal to its compensator expectation; hence its probability of a mark is at most this deterministic budget. This is a paid actual counting-process bound, not conditioning on no marks, and not a coupling claim after a failure.

All stage/tube/budget failures retain their original union bound, at most `32 exp(-KT/(3*10^12))`. Simultaneous adverse exits are failures. Added stopping can only reduce the probability of the original bad exit before stopping. The original Poisson upper-count event is intersected only after conditional stage estimates; no future arrival event is used to condition them.

## 5. Whole-segment cone admission and explicit tail envelopes

At an active stage let `m=Tr`, `w=sqrt(Nm)=T³sqrt(r)`. Bounds (2) and every actual one-jump increment imply, for m and w at least 100, on EVERY connecting segment,

    l>=r/3,   sqrt(r)/3<=e<=3sqrt(r),  l>=e²/32.          (18)

The last assertion follows from `l>=r/3` and `e²<=9r`. Thus the received cone theorem applies with `g=1/32`, using the minimum segment e, not just the pre-jump value. Convexity also verifies the cone from endpoints. The five segment derivative bounds are

    |b_l|<=D r^-5/2,  |b_e|<=D r^-2,
    |b_ll|<=D r^-7/2, |b_le|<=D r^-3, |b_ee|<=D r^-5/2,  (19)

where the literal common ceiling `D=10^14` suffices. The largest received constant after the factor `3^5` is less than `2.88*10^13`; exact rational checks accompany this source.

Let U,W,V_E,V_L be the integrated rate sums `q_LL, sum lambda|uv|, q_EE, sum lambda|u|`. From (2), with `H=int A<=10^4w/N`, `int A²<=mH`, and `Z=0`, one obtains the uniform numerical envelopes

    U,W,V_L <= C0 m,  V_E<=C0 w,
    int q_hh dt <= C0 w³,   h+=(A+1)(E+1)<=3mw,
    int H_h dt <= C0[N/m+m²+m²w/N+w+mw],                 (20)

with `C0=10^7`. Here H_h is exactly the absolute h-residual envelope in the accepted corrector. In its count term (16) is used, not the much larger fixed band `delta N`. For example `int h<=2wH=20000m`; the term `int h(|n-N|+E+4L+2)` is at most a constant times `m(T+w)<=2mw`. The q_hh bound includes `E² AB`: `int AB<=2NH=20000w`, making its charge `O(w³)`, not zero.

Substitute (19),(20) into the accepted **full** residual and bracket formulas. Elementary algebra gives the following generous literal ceilings for each common stopped stage:

    int |R_b|dt <= 10^23[T^-1 r^-5/2 + T^-2 r^-1],
    int q_q dt <= 10^40/(T r^4),
    max|Delta q| <= 10^16/(T r^(5/2)),
    |q-b| at any one-jump target <= 10^16 T^-2 r^-1.      (21)

These constants are deliberately huge and are existence-proof bounds, not practical claims. The monomial ledger and exact checks in `TAIL_ENVELOPES.md` / `check_tail_envelopes.py` expose every contribution. Crucially the first bound is `O(T^-1)`, not a fixed `O(K^-3/2)` timing loss.

Summing the decreasing geometric series from `r=K` gives

    int_tail |R_b|dt <= C[T^-1 K^-5/2+T^-2 K^-1],
    <M_b(tail)> <= C/(T K^4).                            (22)

All constants in (22) are independent of K,N. Brackets/residuals hold on the stopped process itself. There is no post-selection martingale theorem.

## 6. Actual boundary, the remaining clock, and physical removal

On the joint good event, let `t_J` be the actual entrance at `m_J`; the global stopped clock time `sigma_N` equals `t_J`. There has been no A death, hence no clearance, before this time. From the accepted entrance, `E>=sqrt(Nm_J)` and `l>=e²/32`. Equations (4),(21) give

    sqrt(T)|q(X_(t_J))|
       <= C sqrt(T)(m_J/T)^(-3/2)+o(1)
       <= C T^(-1/4)+o(1) ->0.                           (23)

Now continue the ORIGINAL full-chain stages from this actual entrance to the first macro level `delta N`, and then use the received actual interior removal. The accepted proof pays the lower mass-band exit with its actual death-clock budget, upper exit with the original immigration clock, and all subsequent stage/interior failures. Its time remaining after `t_J` is at most

    32sqrt(N)/m_J^(3/2) +5 <=32 T^(1/4)+5=o(sqrt(T)).    (24)

The lower band is not miscalled clearance: the received death-clock argument removes that adverse exit before the genuine macro-positive entry. At that entry the actual B,C,D,E fractions satisfy the accepted interior hypotheses; `n>=n0(delta/4)` eventually, and the five-unit removal really hits `15(N+2)/16`. No retained-chain estimate is used in this last phase.

Each of the following error probabilities tends to zero for fixed K: the fixed-level entrance errors; compact A-budget and original count errors; (17) plus `C_K/T`; dyadic stage failures; the received Poisson lower-band error with constant clock `40000sqrt(delta)` and threshold `ceil(delta N)`; and `exp[-c(delta/4)(1-delta)N]` for interior removal. Thus

    (tau-t_J)/sqrt(T) ->0 in probability                 (25)

on events of probability tending to one. Outside these events no timing or moment bound is asserted. A weak limit tolerates this vanishing probability; a moment theorem cannot.

Since `q(X_0)=b(1/T,0)` and `|b_l|<=1`,

    sqrt(T)|q(X_0)-s_*|<=T^-1/2.

Combine the exact identity (7), compact residual (8), tail residual (22), terminal clock (23), and actual continuation (24). For every fixed K,

    (tau-s_*T)/sqrt(T) - sqrt(T)M_b(sigma_N) ->0
       in probability.                                  (26)

This is the step a fixed-K LLN/window alone does not supply.

## 7. Removing fixed K in the noise, not in the deterministic duration

After a failed compact entrance freeze the tail martingale at zero; after an admitted entrance use the adapted stage stops described above. Its bracket bound (22) gives, by the martingale isometry,

    E|sqrt(T)[M_b(sigma_N)-M_b(sigma_K)]|² <= C/K^4.       (27)

This is an L² bound on the **stopped martingale difference**, not on the clearance time or failed histories. It is uniform for all sufficiently large N at fixed K. For any bounded 1-Lipschitz test function, the two martingales' expectations therefore differ by at most `sqrt(C)/K²`.

At fixed K, (14) gives the compact normal limit. The received deterministic variance-tail estimate gives `Sigma_K²->Sigma²`; equivalently the orbit bounds yield a tail `O(K^-4)`. Let N tend to infinity first, and then K to infinity in the bounded-Lipschitz comparison. Equations (26),(27) prove (1).

This order of limits does **not** discard the fixed deterministic duration `T/K^(3/2)`. That entire segment is transported by the actual corrected clock before taking limits. Only its centered martingale remainder is made small as K grows. The physical duration is discarded only after the separately justified growing cutoff, where (24) is genuinely `o(sqrt(T))`.

## 8. Moment, error-rate, and numerical gates remain closed

The failure probability (17) is only `O(T^-1/4)`. Neither that nor the earlier `O_K(T^-1)` omission price allows multiplying an unrestricted slow fallback duration by its probability and declaring it negligible. The received all-start recurrence/fallback could be consumed only with an explicit conditional return-time and moment cost on these bad histories. No such cost is supplied here.

Accordingly, this result earns a nondegenerate weak Gaussian clearance law and identifies its parameter, but earns no mean/variance convergence or UI. Ordinary CLT reasoning supplies no finite-N Kolmogorov rate. Any finite-N distribution kernel also needs quantitative compact approximation/characteristic-function control, admission error evaluation and numerical acquisition of the interior constants. No hardware, chemistry operation, publication, outreach, Morrey work, or external source is involved.
