# Exact independent receipt: unweighted source-time storage

Reviewed original source: now preserved as `../HISTORY_SOURCE_STORAGE_V1_221a66ea.md`, SHA-256 `221a66ea00b3bcfa8179def2e43cbe0310b0705090aa23e8f4c9cb413a0cac50`.

Reviewed repaired source: `../UNWEIGHTED_SOURCE_STORAGE.md`, SHA-256 `13af680297269e41d9b02e6cc09a43e9b65781493391484002841bf712643700`. The full diff was inspected: it changes the initial-state qualification and replaces the asymptotic paragraph with explicit storage-dependent bounds and the required scaling hypothesis.

**PASS for the repaired exact stopped-domain generator, bracket, Freedman, same-stop count and qualified scaling statements.** The original unqualified asymptotic sentence required repair: the exact receiver does not imply `W(X0)+d=Theta(nu N)` merely from `Emax=Theta(nu N)` and `d=o(N)`. The accepted repaired hash states the missing condition explicitly. The counterexamples below are retained as historical scope checks, not outstanding defects. No domain admission or physical clearance is accepted.

The ordinary theorem is for a fixed finite initial state in the displayed domain and deterministic positive parameters/budget. Alternatively use a deterministic initial storage ceiling, or formulate the result conditionally on the initial sigma algebra with an explicitly conditional martingale theorem, as the repair now specifies. With an upper ceiling `W_0<=wbar`, replacing `W_0` by `wbar` in the budget/radius supplies a uniform bound. A random initial storage must not silently become a deterministic unconditional Freedman threshold.

## 1. Literal full-channel calculation

Independently enter the twelve rates, in the source's order:

`1, A, A(A-1), AC, A(A-1), AD, A(A-1), AE, AE, 2CD, CD, AB`.

The corresponding `A-2E` marks are exactly

`+1,-1,-1,+1,-1,+1,-3,+3,+1,-1,+1,-1`.

In particular `CD->AE` has coefficient two, the three `2A` rates use the falling factorial without a factor `1/2`, and no channel is discarded. Summing rate times mark and rate times squared mark gives exactly

`GW=1+4A-5A²+A(C+D-B+4E)-CD`,
`q_W=1+A+11A(A-1)+A(C+D)+10AE+3CD+AB`.

Let `K=B/2-C-D-4E>=0`. The drift comparison has the exact nonnegative remainder

`[1-AB/2-CD]-GW = 5A(A-1)+A+AK >=0`,

where integrality of `A>=0` is essential to `A(A-1)>=0`. For the bracket ceiling,

`[1+15AB+3CD]-q_W`
` = A[11(B-A)+K+6(B/8-E)+7B/4+10] >=0`.

All bracket slack terms are nonnegative on the source domain. Finally

`[1+30(AB/2+CD)]-[1+15AB+3CD]=27CD>=0`.

These are direct polynomial certificates, not numerical testing alone.

## 2. Terminal storage and actual stopping

Inside the domain, `E<=Emax` gives `W=A+2(Emax+1-E)>=2`. Every enabled one-step exit has nonnegative counts and `E<=Emax+1`, so its globally evaluated `W>=0`, including exits through other domain faces. The shift by `Emax+1`, not just `Emax`, is important for an upward `E` exit. All marks have magnitude at most three.

Write `h=AB/2+CD`, `Q_t=integral_0^t h ds`, and stop at `sigma=min(domain exit,d,Q hitting Qbar)`. The budget compensator is continuous, so `Q_sigma<=Qbar` without jump overshoot. The actual stopped Dynkin martingale has

`<M>_d=integral_0^sigma q_W ds<=d+30Qbar`.

On a budget hit before the adverse domain exit and by `d`, `Q_sigma=Qbar`, `W_sigma>=0`, and

`M_sigma=W_sigma-W_0-integral_0^sigma GW ds`
`        >=Qbar-W_0-sigma>=Qbar-W_0-d=x`.

For deterministic `x>0`, one-sided bounded-jump Freedman with `j=3` therefore gives exactly

`P(budget hit by d before domain exit)`
` <= exp{-x²/[2(d+30Qbar+x)]}`.

No conditioning on a later favorable event, independent count replacement, or target reachability is used. A simultaneous adverse domain exit is charged as domain failure as the source prescribes. The pre-exit inequalities are valid in the compensator integral; isolated terminal states do not acquire positive Lebesgue duration.

## 3. Same-stop occupation and counters

At this same stop,

`integral A ds <= 2Qbar/(cN)`, `integral CD ds<=Qbar`.

These bounds hold for the actual stopped paths, including terminal failure exits, because the inequalities hold before the stop and `Q_sigma<=Qbar`. No future occupancy is licensed.

If `D_sigma` is the true-death count, its compensator is `Lambda_sigma=integral_0^sigma A ds<=a=2Qbar/(cN)`. The counting-process exponential supermartingale gives, for deterministic `k>a>0`,

`P(D_sigma>=k)<=exp[-k log(k/a)+k-a]`.

The `a=0` case has no deaths almost surely. Integer event thresholds must be rounded to the actual event. There is no assertion that `D_sigma` is an independent Poisson variable.

Total population satisfies `P_t=P_0+I_t-D_t` because all ten internal channels conserve particle number. Hence an actual lower total-population exit `P_sigma<=m<P_0` requires `D_sigma>=P_0-m`; this supplies the stated receiving mechanism at the same stop. It does not establish any desired threshold probability without specifying its parameters.

Immigration has the known unit-rate Poisson law over deterministic horizon `d`, and `I_sigma<=I_d` pathwise. Its deterministic-horizon tail can be union-bounded with the death event. Independence between stopped counts or conditional favorable histories is neither needed nor asserted.

## 4. Scaling defect and explicit repairs

The following repair is included in the accepted repaired hash. This section retains the exact reasoning and counterexamples to the original implication.

Put `S=W_0+d`. For the source choice `Qbar=2S`, the exact conclusions are

`integral A ds<=4S/(cN)`, `integral CD ds<=2S`,
`P(budget exit)<=exp{-S²/[2(d+61S)]}<=exp(-S/124)`,

using `0<=d<=S`. Thus both advertised scales follow with fixed `c>0` if **`S=Theta(nu N)` is supplied separately**. Only `S=O(nu N)` is needed for the occupation scale; only `S=Omega(nu N)` is needed for this exponential-tail deduction.

Two admitted examples expose the missing assumptions, even if one additionally imposes initial total population `N`:

1. Choose small `nu<=1/17`, `E_0=Emax=nu N`, `C_0=D_0=0`, `A_0=B_0=(1-nu)N/2`, `d=1`, on integer-compatible sizes. With fixed `c=1/4`, all domain inequalities hold. But `S` is order `N`; the delivered occupation ceiling is order one, not uniformly `O(nu)` as `nu` decreases.
2. Choose `E_0=Emax=nu N`, `A_0=C_0=D_0=0`, `B_0=(1-nu)N`, `d=1`, with `nu<=1/9` and fixed `c=1/2`. Then `W_0=2`, `S=3`, `Qbar=6`, and the displayed budget bound is `exp(-9/368)`, independent of `nu N`. It is not an exponentially small bound in `nu N` when that product grows.

These are scope counterexamples to the asymptotic inference, not to the exact generator or stopped-probability formulas. A sufficient repair is to state the exact `S` bounds and explicitly add `S=Theta(nu N)` for the simultaneous asymptotic conclusions. Another option is a separately declared deterministic `Qbar=Theta(nu N)` with a comparably large gap above `W_0+d`, provided its initial-state ceiling is acquired.

## Non-acceptances

No acquisition of the `B` floor, `A` cap, `E` ceiling, cone, domain-exit failure probabilities or final removal time is included. No weighted `O(T^-2)` source budget, numerical complexity gain, actual clearance, or stochastic CLT follows from this storage component. Sources were not edited by this reviewer. The first independent-check invocation correctly rejected a hash mismatch when the parent concurrently repaired the source; after verifying the preserved original and complete diff, both versions were bound and the checks rerun.
