# Independent audit: uniform actual removal block, exact rate-2 tree

**PASS. All previously pending component-receipt blockers are now resolved at
exact hashes, with the activated-interface qualifications retained. No change
to the frozen composition or its constants is needed.**

Reviewed 2026-11-01 by `review_interior_removal_theorem`. Target:
`../UNIFORM_ACTUAL_REMOVAL_BLOCK.md`, SHA-256
`a0e09b39c50c28365a1ed5a0fe04c71b003b9c5556ffe9b94202441f9ee4cb21`.
This is an ordinary proof audit, not acceptance by numerical experiments.

For the exact twelve-channel rate-2 count chain, this review receives: for every
initial state of total N above the stated finite N_*, at the deterministic time
`d_N=1+10^8 sqrt(N)`,

    P_x[S(d_N)>15N/16] <= 32 exp[-sqrt(N)/10^6].

The proof is uniform over all initial compositions, including boundary states.
The separate accepted sampled consumer can consequently be applied as detailed
in `CONSUMER_APPLICATION.md`. No original source was edited; no new source was
retrieved. This is not a practical numerical threshold or efficiency claim.

## 1. Exact dependencies received, not silently widened

The checker binds the composition and each source/receipt by SHA-256. In
particular:

- Initial growth `90a80f12...` is received through receipt `a1eb22f7...`.
  Its original B-rich claim is not itself an arbitrary-state entrance theorem.
- Activation `c1d2ed08...` is received through `1d26eae5...`. Its U generator,
  bracket, lower-seed excursions, and conditional charging bounds are used.
  Its time-zero activated output is not presumed to contain a seed.
- Activated macro `e527fafd...` is received through `bf220ba3...`, with the two
  mandatory addenda also recorded in receiving note `4f98b41a...`.
  The overshoot upper bound holds only for first crossing from below; the
  composition needs only `M>=delta N`, so already-macro states cause no gap.
  The positivity window requires `N>=28 exp(100)/eta` and costs exactly
  `10exp(-c_win N)`. Both are kept; no prefactor is silently absorbed.
- Interior removal `a8e0bd38...` is received through the earlier independent
  ordinary review `25513463...`. Its actual entry size n and epsilon-dependent
  threshold are rechecked below. Its deterministic global-attraction supplier
  remains the explicitly received ordinary supplier, not stochastic mixing.
- The sampled consumer is the final repaired source `a4d41076...`, not an
  earlier draft. Its receipt remains a conditional theorem; this audit earns
  its previously missing network block premise, rather than assuming it.

Full paths and hashes appear in `EXACT_CHECK_RESULTS.json`. The source-bound
macro receipt is qualified, but those qualifications are fully satisfied here;
there is no outstanding conditional proof gap after receiving it.

## 2. New global seed extension is valid

Keep the original N fixed and put
`m=floor(sqrt(N)/20000)`, `k=floor(m/2)`, with `N>=10^40`.
For the same globally defined cutoff potential G_N, consider every state with
`M<m` and `S>3N/4`. Integer M and one-step M marks imply A<=m both before and
at every one-jump target. The source bound `1<=h<=101/100` therefore applies
without changing its target function.

In the core `R<=48(M+1)`,

    B=S-A-R>3N/4-49m-48>=N/2.

Thus the original core calculation, including its AB capture reserve, applies.
Outside that core, its calculation is genuinely B-free: a largest satellite
has an actual positive-M return group of rate at least `A max(C,D,E)`, at
least four times the negative-M rate; immigration supplies the constant
reserve; the entire positive zero-M cutoff expense is bounded by
`(A^2+1)/100`. AB->CD preserves M, decreases A and increases R, so decreases
h and is nonadverse for every B, not only for B-rich states. Its omission in
this upper bound is legitimate. Both regions therefore give

    LG_N/2^(-M)<=-12/25,

which implies `LG_N<=-G_N/4` since `h<=101/100`.
The parameter `N>=10^8(m+1)^2` holds throughout the stated range.

Stop at seed M>=m, lower mass S<=3N/4, or adverse upper mass S>2N, with mass
priority. Every terminal M is at most m if the phase began below m: all M
marks are at most one. Consequently G_N>=2^-m throughout the stopped path,
including each mass-stop target. Localized integrating-factor expectation,
Fatou, and the positive terminal bound give

    P(seed/main stop exceeds 8m)<=(101/100)e^-m.

There is no added B-exit ambiguity and no assumed finiteness of an unbounded
hitting time before deriving the bound. If initially M>=m, this wait is skipped.
In particular even a state already activated at time zero is first seeded
unless it already has M>=m; the earlier interface gap has been closed.

## 3. Activation preserves an actually acquired seed

After a seed phase that has not hit a mass boundary, M>=m. Direct macro states
skip charging. Already activated states skip charging but retain M>=m>=k.
Otherwise the phase starts with R<B/100 and continues from the actual state.

The accepted exact U drift and squared-mark identities give the actual
exponential charging inequality on this region. Adding a macro stop can only
shorten this stopped construction. Every lower-seed excursion begins at an
actual crossing m->m-1, uses the same global G_N on k<M<m, and has conditional
lower-hit probability at most `(202/100)2^(-m/2)`. Before the global adverse
upper stop, total intensity is at most `32N^2`; hence the expected number of
these crossings in T0=10^12 is at most `32N^2 T0`. Summing conditional bounds
at the actual crossing times requires no independent attempts. The accepted
constant calculation bounds their union by `exp(-m/4)`.

On survival past that lower boundary, integer M>k implies M>m/2. The U
integrating factor thus gives charging timeout probability at most `exp(-N)`.
The combined post-seed failure bound is therefore the displayed
`exp(-m/4)+exp(-N)`, still with the upper mass stop adverse. A simultaneous
activation and lower-seed mark lands at M=k, not below it, because marks have
size one. It is a valid activated output for the next component.

At a continuing activated, nonmacro output,

    R>=(S-A)/101>(3/4-delta)N/101>=4rN.

Also `3N/4<S<=2N`, `M>=k`, and `8<=k<=delta N`. Thus every required entrance
condition of the qualified activated-macro receipt is earned, not guessed.

## 4. Macro entry, positivity, and actual interior size

Conditional on each activated stopping-time state just obtained, the qualified
macro receiver reaches M>=delta N or a main mass stop by 256N/k, with error

    8exp(-k/3)+exp(-N/100000).

The resource-retention event is paid once, not at each stage. Lower-M/resource
exits are charged failures; an upper mass stop is adverse, never service.
All stage restarts are analysis clocks on the continuing actual state. The
source receipt explicitly verifies all competing channels and min-coordinate
ties. Direct macro states need no dyadic construction and require no overshoot
upper bound.

At macro entry, Section 5's actual full-chain window applies because N_* keeps
`N>=28exp(100)/eta`. Its stopped concentration bound excludes its own 3N exit
on a good path and keeps the factor ten. No deterministic ODE positivity
argument is mistaken for a probability estimate. Its good endpoint has all
five counts at least eta N/2. Any earlier lower mass hit can instead be treated
as removal; a 2N upper crossing remains adverse throughout.

At a continuing endpoint let n be the *actual* total. Then
`3N/4<n<=2N`, and each of B,C,D,E is at least `(eta/4)n`.
The threshold `N>=4n0(eta/4)/3` ensures `n>=n0(eta/4)`.
The independently received interior theorem is therefore applicable at this
actual stopping-time entrance, with its own reference total n, by strong
Markov. Its conditional error is at most

    exp[-(3/4)c(eta/4)N].

On success, after five more physical units the actual total is at most 7n/8.
There is no replacement of n by N inside that theorem and no use of a fresh
independent immigration process. Random entrance times are stopping times;
the fixed subsequent increments 1/N and five preserve that property.

## 5. Deterministic physical budget and one original immigration charge

The floor bounds `m>=sqrt(N)/40000` and `k>=m/4>=sqrt(N)/160000` imply
`256N/k<=40960000 sqrt(N)`. The maximum successful analysis time is

    8m+10^12+256N/k+1/N+5 < 1+10^8 sqrt(N)=d_N.

Skipped stages only shorten it. Deadline failure sets are charged; on those
sets the original process still continues to d_N, without asserting service.
There is no random terminal-time substitution in the final claim.

Let I be the single actual immigration counter from the original time zero
through d_N. Nonexplosion and `S(t)<=N+I(t)` hold pathwise. For N>=10^40,
`d_N<=N/256`. Chernoff at log 2 with log 2>=2/3 gives

    P[I(d_N)>N/64] <= exp[-N/256].

On its complement G_imm, no upper S>2N exit can occur in any phase. This one
event pays all such adverse exits simultaneously. No local probability bound
was conditioned on this future event: bounds were first applied conditionally
on actual past-measurable entrances, and G_imm is intersected afterward.

A lower mass hit at any successful construction time leaves, at d_N,

    S(d_N)<=3N/4+N/64=49N/64<15N/16.

Otherwise the successful interior entrance total satisfies `n<=65N/64` on
G_imm, and all unused post-service time is paid by the same count:

    S(d_N)<=7n/8+N/64<=463N/512<15N/16.

The conservative reuse of the whole N/64 immigration allowance in both terms
only weakens the bound. It does not assert independence or forget past arrivals.
These alternatives close the random-time-to-deterministic-time interface.

## 6. Finite threshold and full error union

All fixed quantities eta, c_win and c(epsilon) are positive and finite;
`n0(epsilon)` is finite by its received ordinary proof. Thus the maximum defining
N_* is finite. Its two squared thresholds imply respectively

    c_win N >= sqrt(N)/10^6,
    (3/4)c(epsilon)N >= sqrt(N)/10^6.

All integer/floor, activation, dyadic, and immigration requirements follow
already from N>=10^40. No extra prefactor-free concentration threshold is needed,
because the exact prefactor ten is carried into the final union bound.

The seed, charging, macro, window, interior, and immigration errors have
prefactors totaling

    101/100 +1+1+8+1+10+1+1 = 2401/100 < 32.

Their exponents all dominate sqrt(N)/10^6: the weakest displayed mesoscopic
one is k/3>=sqrt(N)/480000. Hence the union proves exactly the claimed (H).
All conditional probabilities were bounded uniformly at actual states before
summing. Neither stochastic independence nor a killed/modified generator is
used at any join.

## 7. Evidence, blocker ledger, and scope

`independent_checks.py` independently checks 30 source-hash/algebraic/rational
conditions. Its monotonicity certificates expand relevant polynomials in
`sqrt(N)-10^20` with nonnegative coefficients and positive constant terms,
rather than checking a single numerical N. It additionally checks the actual
G_N drift at 560 exact rational fixtures, including B-poor outer states, and
2,238 enabled jumps in constructive communication fixtures. These finite tests
support but do not replace the uniform ordinary proof above.

`REVIEW_RECEIPT.json` explicitly records all formerly pending items and their
resolution. There are **no open mathematical blockers for this exact block**.
The conclusion is for this five-species rate-2 tree, not arbitrary connected
binary networks. The threshold is an existence recipe in received component
constants, not an efficient algorithm or a useful numerical size claim. The
accepted consumer application is separate below; no novelty, publication,
hardware action, external state change, or paused Morrey work is asserted.
