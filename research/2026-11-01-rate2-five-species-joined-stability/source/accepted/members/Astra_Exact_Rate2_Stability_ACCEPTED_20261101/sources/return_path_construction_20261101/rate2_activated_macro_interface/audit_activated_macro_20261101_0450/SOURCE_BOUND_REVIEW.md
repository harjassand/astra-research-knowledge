# Source-bound review: activated M to macro M and positive fractions

**Verdict: the conditional mathematical interface is received with the two explicit statement addenda below. The frozen source is not accepted as a literally unqualified section-1 summary.** No channel, drift, stopping, or concentration estimate requires a change of numerical constant.

Reviewed source: `../ACTIVATED_TO_MACRO_AND_POSITIVE_FRACTIONS.md`, SHA256 `e527fafdfe790fa753b4584fca338bf9e4aa37179643a1f1596e39b140cb99a0`. The review is independent ordinary mathematical reasoning; the separate exact finite checks are supplementary only. No source file was edited and no external retrieval was used.

## 1. Exactly received result and mandatory addenda

Let the count chain have all twelve channels in the frozen source, with falling-factorial propensities and coefficient two only on CD->AE. Fix reference N>=10^40, r=10^-3, delta=10^-12 and integer 8<=k<=delta N. Start in 3N/4<S<=2N, R>=4rN, M>=k. Then, by physical time 256N/k, the actual chain reaches M>=delta N or a main mass stop, apart from probability at most

`8 exp(-k/3)+exp(-rN/100)`.

Here S<=3N/4 is the removal output; S>2N is an adverse output, not removal. Lower-M stage exits and resource loss are failures already charged in the displayed bound. They are not extra successful outputs. Actual states continue between analysis stages, without independent attempts or resetting the process.

**Addendum A (initial macro entry).** The overshoot assertion `M in [delta N,delta N+1]` applies only when macro M is first crossed from below. If the allowed initial state already has M>=delta N, macro entry is time zero and no upper bound delta N+1 follows. For example, A=E=N/2 and B=C=D=0, for even integer N, satisfies all entrance assumptions but has initial M=N/2. The positivity argument needs only M>=delta N, so this correction has no downstream cost.

**Addendum B (positivity range and exponential prefactor).** Define, exactly as in the source,

`eta=delta^4/(1000*3^40)`, `rho=eta exp(-100)/4`,

`N_pos=28 exp(100)/eta`, `kappa=rho^2/[2(32+rho/3)]`.

The paid actual window established by equation (8) requires **N>=N_pos**, in addition to the macro range N>=10^40. At a macro state with 3N/4<S<=2N and M>=delta N, after a further physical 1/N, all five actual coordinates are >=eta N/2 except on probability at most **10 exp(-kappa N)** (or its minimum with one). The section-1 prefactor-free shorthand `exp(-c_delta N)` follows explicitly by taking c_delta=kappa/2 and imposing also **N>=2 log(10)/kappa**. The base N>=10^40 alone is not the hypothesis of the displayed concentration proof, and N_pos alone does not absorb its prefactor ten. The source's later acknowledgement of an enlarged positivity threshold must not be lost in consumption.

If endpoint S<=2N, the five lower bounds imply B,C,D,E>= (eta/4) S. This endpoint upper bound is conditional in the frozen source, not an automatic consequence of concentration. A prior hit S<=3N/4 can instead be received as removal. No initial activation, global arbitrary-state entry, interior removal theorem, recurrence, or stationary moment is received here.

## 2. All-channel and nonlinear-corner audit

Write m=min(C,D), so M=A+m. Every M mark is -1,0,1. The following table gives `(Delta M, Delta J)` for C<D, C=D, C>D respectively, where J=R+2A+4M. It is valid whenever the channel is enabled, including gap-one crossings into a tie.

| Channel | C<D | C=D | C>D |
|---|---|---|---|
| 0->A | (1,6) | (1,6) | (1,6) |
| A->0 | (-1,-6) | (-1,-6) | (-1,-6) |
| 2A->AC | (0,-1) | (-1,-5) | (-1,-5) |
| AC->2A | (0,1) | (0,1) | (1,5) |
| 2A->AD | (-1,-5) | (-1,-5) | (0,-1) |
| AD->2A | (1,5) | (0,1) | (0,1) |
| 2A->AE | (-1,-5) | (-1,-5) | (-1,-5) |
| AE->2A | (1,5) | (1,5) | (1,5) |
| AE->CD | (0,-1) | (0,-1) | (0,-1) |
| CD->AE | (0,1) | (0,1) | (0,1) |
| CD->AB | (0,0) | (0,0) | (0,0) |
| AB->CD | (0,0) | (0,0) | (0,0) |

For theta=.01, grouping the two AE outgoing channels gives
`AE [exp(-5theta)+exp(theta)-2]<=-3theta AE`.
The remaining groups give immigration <=-3theta, death <=7theta A, the three 2A exits <=18theta A(A-1), both arm returns <=-theta A(C+D)/2, and CD->AE <=-theta CD. AB<->CD is exactly J-neutral. Thus equation (2), including its relaxation to -AR/2, follows for every integer state. The elementary exponential bounds used there hold by their displayed Taylor inequalities (and e^x<=1+x+x^2 for 0<=x<=.06).

On R>=2rN, M<delta N, one has A<=delta N and 7+18delta N<=rN/2<=R/4. Consequently Q=exp(-J/100) has nonpositive generator. At the first non-prioritized R<=2rN exit, J<=2rN+6delta N<=3rN. Initially J>=4rN. Nonnegative stopped supermartingale reasoning therefore gives the single global bound exp(-rN/100), without charging each stage separately. Macro/mass priorities exclude all terminal states where the small-M bound would not apply.

The exact positive-M rate is `1+AE+A max(C,D)` off a tie and `1+AE` at a tie; this dominates `1+A(R-2M)` in both cases. The exact negative rate is `A+3A(A-1)` at a tie and `A+2A(A-1)` otherwise, hence <=3A^2. Positive M marks always have Delta A=1; negative marks always have Delta A=-1.

In the continuing macro region and every one-jump target, clipping in h_N is inactive and h_N>=.99. A positive M jump contributes `-h_N/2-1/(8N)<=-.49` after division by 2^-M. A negative one contributes `h_N+1/(2N)<=1.01`. The zero-M pair CD->AB and coefficient-two CD->AE supplies exactly -3CD/(4N). Every positive zero-M phase expense is one of AB->CD, AE->CD, or at most one 2A arm exit; their total rate is <=AB+AE+A(A-1). The other zero-M changes are nonpositive.

This gives, before relaxation,

`LV_N/2^-M <=-.49-.49 AR+.98 AM+3.03 A^2+[A(B+E)+A(A-1)-3CD]/(4N)`.

Using B+E<=2N and A,M<=delta N gives exactly equation (4). Its displayed constant comparison subtracts another .24 AR, leaving at most `-.49-AR/4-3CD/(4N)`. Since R>=A, N>=1 and `(A+m)^2<=2(A^2+m^2)<=2(A^2+CD)`, this is <=-M^2/(8N), and h_N<=1 proves equation (5). No C-D balance, averaged A fiber, deleted channel, or unpriced startup is used.

## 3. Stage exits, clocks, and counting

In a stage at integer j with entrance j<=M<min(2j,delta N), the lower boundary is floor(j/2). On continuation M>j/2, so the decay rate is j^2/(32N). All source and exit targets use the same V_N; the one-jump maximum A<=delta N+1 keeps the h_N lower bound valid at exit. Initial V_N<=2^-j, whereas a lower exit has V_N>=(99/100)2^-floor(j/2). Stopped optional expectation gives `(100/99)2^-j/2<=2exp(-j/3)`.

For no exit by T_j=128N/j, V_N>=(99/100)2^-2j and the integrating factor yields `(100/99)exp(j log2-4j)<=2exp(-3j)`. Thus `4exp(-j/3)` safely bounds the union of a non-prioritized lower exit and a stage timeout. Resource exits are charged only by the global Q estimate. Main mass stops have first priority, macro second, resource next, lower boundary last; these priorities preserve all terminal lower bounds used above.

At j_i=2^i k there are finitely many relevant stages, at most `1+ceil(log_2(delta N/k))`; skipped stages only shorten the construction. Deadlines sum to <=256N/k. For k>=8,
`sum_i exp(-2^i k/3)<=exp(-k/3)/(1-exp(-k/3))<=2exp(-k/3)`.
Conditional estimates at actual stopping-time entrances and a union bound therefore give equation (1). This is stronger than introducing a polynomial event-count loss; neither independence nor a fresh process is assumed. The supplied hypothesis M>=k is essential and has not been manufactured by this audit.

## 4. Deterministic positivity and paid actual noise

The displayed polynomial F is the exact quadratic field obtained from the twelve channels. It conserves mass, preserves nonnegativity, and on mass in [3/4,2] satisfies all five displayed differential inequalities. For instance, the negative coefficient in a' is at worst a(3a+b)<=6a, and that in c' is at worst c(a+3d)<=6c. The d and e inequalities are analogous.

If a(0)>=delta/2, then a(t)>=delta exp(-6)/2 on [0,1]. Integrating its squared lower bound over [0,1/2] and retaining the maximal decay through time 1 gives c,d,e>=beta=delta^2 exp(-18)/8 for t in [1/2,1]. Integrating c d into b over [1/2,1] gives b(1)>=delta^4 exp(-38)/128. The other coordinates also exceed eta. If min(c(0),d(0))>=delta/2, retain c,d>=delta exp(-6)/2 and integrate c d into a,b,e; this gives exactly the three bounds displayed in section 5. Replacing e by the strict upper bound 3 verifies that every listed margin exceeds eta. These cases exhaust M/N>=delta, including arbitrary already-macro initial M.

For the actual window set Y(u)=X(u/N)/N. Before the first actual S>3N, total physical intensity is
`1+A+3A(A-1)+A(C+D)+2AE+3CD+AB <=3S^2+S+1<=32N^2`.
Every coordinate jump has size <=1/N in Y; over u<=1 its martingale has predictable squared-jump compensator <=32/N. Direct expansion of A(A-1) and immigration/death gives the exact drift correction
`(a/N)(2,0,-1,-1,-1)+(1/N^2)(1,0,0,0,0)`,
whose infinity norm is <=7/N before this stop. Jacobian row envelopes (54,12,42,42,30) on [0,3]^5 are <=100, proving the chosen Lipschitz bound.

Two-sided stopped Freedman for each of five coordinates and a finite union bound give probability <=10exp(-kappa N) that any martingale exceeds rho in absolute value. If N>=N_pos, then 7/N<=rho; Gronwall, applied up to the stopping time and including its terminal jump, bounds the coordinate error by `2rho exp(100)=eta/2`. At a hypothetical 3N exit, this would imply actual total/N <=2+5eta/2<3, contradicting the exit. Consequently the stop is not hidden inside the conclusion: the same estimate holds throughout the full physical 1/N window. At its end, positivity >=eta N/2 follows. Strong Markov application at the actual macro time is legitimate because these estimates are uniform over the received macro entrance set.

## 5. Integrability and limitations

Only immigration changes S upward, at constant rate one; all internal channels conserve S and A-death lowers S by one. Therefore S(t)<=S(0)+I(t), where I is a rate-one Poisson process. Finite-horizon mass localization bounds every channel intensity on a finite set and proves nonexplosion. Dynkin/integrating-factor arguments can be localized there; positivity/Fatou gives the nonnegative-supermartingale bounds on removal of localization. No finiteness of an unbounded hitting time was assumed before proving the relevant estimates.

The two addenda above must travel with this receipt. In particular, neither the adverse upper mass stop nor a seed/activation prerequisite becomes successful removal, and an endpoint S<=2N must be independently retained if the epsilon=eta/4 relative-mass receiver is used. This receipt makes no claim about global initial entry, composition with another theorem, recurrent return, tail, stationary moment, hardware, or publication.
