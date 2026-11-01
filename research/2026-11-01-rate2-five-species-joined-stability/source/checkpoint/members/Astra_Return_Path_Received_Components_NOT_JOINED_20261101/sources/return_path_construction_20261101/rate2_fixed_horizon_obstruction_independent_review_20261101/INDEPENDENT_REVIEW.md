# Independent receipt: rate-2 fixed-horizon obstruction transfer

**PASS for the fixed-horizon death/MGF statements and the bounded-comparability
Foster obstruction. One harmless Dynkin-display clarification is recorded below.**
Reviewed 2026-11-01 by `review_interior_removal_theorem`.

Frozen target: `../rate2_fixed_horizon_obstruction/RATE2_FIXED_HORIZON_ADDENDUM.md`,
SHA-256 `415edfdf0829c1a95935bc200547d286a639f11e60f6366383be6548fa2d4232`.
I also read and hash-checked the original all-unit root proof
`0f6a4405e9566b070100322606f004ea1f58dda08fd7ea46d03cec1da8d3e478`
and its independent receipt
`4321f9200831c54d5b33f5e430fad8ede9759b5d7392ccd18115fa46ef020590`.
No source was edited or newly retrieved.

## Exact transfer and stopped probability argument

The actual all-channel generator, with falling-factorial propensities and
coefficient two on `CD -> AE`, has

    LA = 1-A-3A(A-1)+A(C+D)+3CD-AB,
    q_bad = A+3A(A-1)+A(C+D+2E).

Thus the rate-1 proof's `+2CD` becomes `+3CD`; the bad intensity is unchanged.
In the retained process, direct jump inspection gives

    A+C=A+D=1+I,        B=N-I+A-E,

and E counts the retained `CD -> AE` events, now at intensity `2CD`.
Stopping that count at immigration number `m+1` bounds its intensity by
`2(1+m)^2`, so the corresponding tail is bounded by
`P[Poisson(2T(1+m)^2)>ell]`. This is stopped counting-process domination,
not conditioning intensity on the future event `I(T)<=m`.

Outside the two counter tails, monotonicity of I and E ensures these bounds
at every time up to T. In particular, with `K=3+2m+ell`,

    A+C+D+E = 2+2I-A+E <= K-1 < K,
    B >= N-m-ell > N-K > N/2.

The full-generator bounds in the addendum hold on this region. Exact
nonnegative decompositions make their directions transparent:

    [1+3K^2-(N/2-K)A] - LA
      = 3(K^2-CD)+A(B-N/2)+A(K-C-D)+A+3A(A-1),

    (1+5K)A-q_bad
      = A[3(K-A)+2(K-C-D-E)+(C+D)+3].

Here `A(A-1)>=0` because A is an integer count. Stop at time T, the first
bad mark, or region exit, whichever comes first. The terminal A is nonnegative
and `A(0)=0`, so stopped Dynkin gives the stated upper bound on the stopped
integral of A. The first bad-event compensator is bounded by `(1+5K)` times
that integral. An earlier region exit before any bad mark is covered by the
dominant counter tails because the paths coincide until that first mark.
This proves equation (1), including bad events whose jump itself exits the
region. The unit immigration process gives nonexplosion and finite polynomial
moments on every bounded physical interval, justifying localization.

For each fixed T, choose m to make the first tail small, then ell for the
second, and only then increase N. The last term vanishes. This proves that
the probability of any bad mark, and hence of an actual A death, tends to zero.
It makes no claim about unrestricted expected A occupation.

## Uniform integrability and exact fixed-T exponential-count limit

Let `U_N=r^[S(T)-(N+2)]` and `I_N=I(T)`. The exact total identity gives

    0 < U_N = r^(I_N-D_A(T)) <= r^I_N,
    sup_N E[U_N^2] <= exp[T(r^2-1)] < infinity.

This provides uniform integrability. More directly,

    0 <= E[r^I_N]-E[U_N]
      <= E[r^I_N 1_{D_A(T)>0}]
      <= exp[T(r^2-1)/2] P[D_A(T)>0]^(1/2) -> 0.

Neither step assumes independence of immigration and deaths. Since the
immigration MGF is `exp[T(r-1)]`, equation (3) follows for every fixed T and r>1.

## Foster contradiction and the display clarification

For a finite function W uniformly bounded above by `C r^S`, all localized
expectations needed here are legitimate. Indeed actual rates are bounded by a
quadratic in S and each reaction changes S by at most one, so absolute
generator terms are bounded by a constant times `(1+S^2)r^(S+1)`.
The domination `S(t)<=S(0)+I(t)` makes this integrable on every finite interval.
Alternatively, nonnegative localized integrating-factor Dynkin and Fatou
suffice for the desired upper bound.

**Clarification:** the addendum allows merely finite K0, without saying K0>=0.
The exact inequality is

    E W(X(T)) <= exp(-zeta T) W(x)
                +(K0/zeta)(1-exp(-zeta T)).

Its displayed weaker `+K0/zeta` form is valid after replacing K0, without loss,
by `max(K0,0)`. This harmless convention or the exact formula above repairs the
display for negative K0; it does not change the theorem or the limit argument.

Using the lower comparability bound, dividing by `r^(N+2)`, and taking N to
infinity yields

    c exp[T(r-1)] <= C exp(-zeta T).

All the K0 terms vanish. Choosing any fixed
`T>log(C/c)/(r-1+zeta)` contradicts the inequality. Thus the actual rate-2 chain
has no geometric Foster function uniformly comparable to `r^S` for any r>1.

## Scope and saved evidence

This is an independent ordinary-proof acceptance, not a simulation conclusion.
The accompanying `independent_exact_checks.py` reconstructs the all-channel
generator and checks the retained invariants, stopped-region decompositions,
total-count identity, and all three source hashes: **13/13 checks PASS**.
`independent_exact_results.json` records the run; `REVIEW_RECEIPT.json` records
this decision and file hashes.

No rate-1 product-Poisson law, detailed balance, positive recurrence, or stationary
moment statement was transferred to rate two. This receipt also does not supply
boundary entrance, a quantitative growing time horizon, an absolute-occupation
limit, or global recurrence. No publication, hardware action, new source access,
external state change, or paused Morrey work was performed.
