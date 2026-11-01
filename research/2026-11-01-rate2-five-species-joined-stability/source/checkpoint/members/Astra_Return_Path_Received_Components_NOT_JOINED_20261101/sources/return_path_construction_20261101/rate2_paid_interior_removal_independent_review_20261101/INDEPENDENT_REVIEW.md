# Independent review: paid interior removal for the actual rate-2 chain

**Decision: PASS for the stated interior-only theorem. No theorem repair required.**

Reviewed 2026-11-01 by the independent `review_interior_removal_theorem` reviewer.
The frozen target is `../rate2_paid_interior_removal/PAID_INTERIOR_REMOVAL.md`,
SHA-256 `a8e0bd383b053021f72e8197986581c87878046cdeaa7570536e44f5cf71a1cf`.
The hash was independently checked. This review does not edit the author component.

For each fixed `0 < epsilon <= 1/4`, the proof establishes finite
`n0(epsilon)` and positive `c(epsilon)` such that, uniformly over actual initial
states with total `n >= n0` and `B,C,D,E >= epsilon n` (including `A=0`),

    P[S(5) <= 7n/8] >= 1 - exp(-c(epsilon)n).

Acceptance uses the already-received ordinary deterministic single-linkage
complex-balanced global-attraction theorem, exactly as scoped in
`../rate2_dyadic_continuation/DETERMINISTIC_SOURCE_RECEIPT.md`. I inspected that
receipt, not a newly retrieved paper. No new external source was accessed.
The argument below is a mathematical review; the accompanying exact symbolic
checker is support, not a replacement for the proof.

## 1. Deterministic supplier hypotheses and entry from A=0

Reconstructing the actual reaction vectors gives precisely the displayed
homogeneous field `F`. In the competitor, reducing `2A -> AC` and `2A -> AD`
by `1-s` and adding `2A -> CD` at `1-s` changes the field by zero, because

    -(AC-2A) -(AD-2A) +(CD-2A) = 0.

Here `s=(sqrt(7)-1)/2`, so `s^2+s=3/2` and `0<s<1`.
At `q=(2/9)(1,s^2,s,s,2-s)`, direct incoming/outgoing flux balances hold
at each of the six complexes. Their common directed graph is strongly connected.
The three vectors `AC-2A`, `AD-2A`, `AE-2A`, together with `AB-CD`, are
independent in the sum-zero hyperplane. Thus the positive compatibility class
at mass one is the whole positive simplex. The imported deterministic theorem
is applied only to this internal competitor, not to the two-linkage open chain.

The claimed differential inequalities hold on the simplex. For additional
ordinary certificates, the following residuals are nonnegative:

    F_a + 3a - 3cd = a(2b+4c+4d+3e),
    F_b + b        = cd+b(b+c+d+e),
    F_c + 3c       = a^2+ae+ab+c(2a+3b+3c+3e),
    F_d + 3d       = a^2+ae+ab+d(2a+3b+3d+3e),
    F_e + 2e       = a^2+2cd+2e(b+c+d+e).

Consequently `c(t)d(t) >= epsilon^2 exp(-6t)` and variation of constants
in `a'+3a >= 3cd` gives the author's bound

    a(t) >= a(0)exp(-3t)+epsilon^2(exp(-3t)-exp(-6t)).

Together with the other four bounds, this places `phi_1(K_epsilon)` in the
strictly positive simplex with the stated positive uniform lower bound.
Its compactness follows from continuous dependence. In particular `A=0`
at time zero is not smuggled into the positive-only attraction supplier.

## 2. Uniform finite entrance is supplied by an ordinary finite-cover argument

Let `L=phi_1(K_epsilon)`. At each `x in L`, attraction supplies a finite
relative time `T_x` at which `H(phi_(T_x)(x))<h/8`. Continuity gives a
neighborhood of `x` whose images at that same time have entropy `<h/4`.
A finite subcover of `L` exists. Entropy is nonincreasing, so at
`T=max_j T_(x_j)` every point of `L` has entropy `<h/4`.

Thus an integer not smaller than `1+T` satisfies the entrance requirement
for `K_epsilon`; the shift by the first unit of positive entry is included.
The least qualifying integer in the author definition is therefore finite.
The proof does not assume that pointwise attraction by itself is uniform:
compactness, continuity, and the Lyapunov monotonicity are all used.
No numerical upper bound for this entrance time has been established or is
needed for the existence theorem. A terminating validated search may return
any certified larger integer; computing the exact least integer is unnecessary.

## 3. Normalized entropy dissipation and the explicit local contraction

For positive composition, complex balance cancels the linear terms in

    D = sum_edges k q^y [u_y log(u_y/u_z)-u_y+u_z],
    u_y = p^y/q^y,

and each bracket is at least `(sqrt(u_y)-sqrt(u_z))^2`.
On `H<=h`, Pinsker places all species ratios `r_i=p_i/q_i` in `[1/2,3/2]`.
For `i=C,D,E`, the selected edge `2A -> Ai` contributes at least

    (s q_A^2 / 12)(r_A-r_i)^2,

using `r_A/(sqrt(r_A)+sqrt(r_i))^2 >= 1/12`. The two different edges
`2A -> CD -> AB` have flux coefficients at least `(1-s)q_A^2` because
`s^2-(1-s)=1/2`. The two-square inequality then gives at least

    ((1-s)q_A^2/24)(r_A-r_B)^2.

No selected edge is counted twice. Since `2s>=1-s`, their sum is at least
`kappa sum_(i!=A)(r_i-r_A)^2`, with `kappa=(1-s)/486`.
Taylor's bound for `r log r-r+1`, followed by weighted variance minimization,
gives

    H <= sum_i q_i(r_i-1)^2
      <= sum_i q_i(r_i-r_A)^2
      <= sum_(i!=A)(r_i-r_A)^2.

This proves `D>=kappa H` without a numerical spectral assertion.
For mass `m`, homogeneity gives the normalized equation `p'=mF(p)`.
With `m>=3/4` and `Delta=2/kappa`, the endpoint entropy is at most
`h exp(-3/2)<h/4`; the last strict inequality also follows from the first four
positive terms of the series for `exp(3/2)`, whose sum is `67/16>4`.

The normalization perturbation bound is valid: if both masses are at least
`3/4`, then `||z/m_z-w/m_w||_1 <= (40/3)||z-w||_infinity`.
The chosen `alpha` bounds this by `2q_*/15` and bounds the entropy error by
`2h/15`. For example, the deterministic coordinate lower bound `3q_*/4`
minus `2q_*/15` is `37q_*/60>q_*/2`; hence the entire normalized line segment
lies where the asserted entropy-gradient bound holds. This validates both
the whole-window entropy bound `17h/15<2h` and the endpoint reset
`23h/60<h/2`. At the entrance endpoint only, the same argument applies;
no entropy-gradient bound is required on the initially possibly boundary path.

## 4. Exact actual generator and stopped finite-window concentration

The actual falling-factorial count drift is

    F(X) + (2A+1, 0, -A, -A, -A).

It includes the three `A(A-1)` corrections and both port channels. For
`Z(u)=X(u/n)/n`, division by `n^2` yields exactly author equation (10).
Before the upper stop `S>=2n`, the drift error has infinity norm at most `5/n`.
All actual coordinate jumps, unlike the added competitor edge, are at most one.
The intensity bound `27n^2` therefore gives coordinate bracket at most
`27R/n` in a stopped fast window of length `R`. Applying the two-sided
bounded-jump exponential martingale bound, followed by a five-coordinate
union, gives exactly

    10 exp(-n r^2/(54R+2r/3)).

Both the upper stop and the lower removal stop can be included, together with
the stopping jump. On the interval up to that jump, compare the actual path
with the *unstopped* deterministic path at the same elapsed time. Both paths
are in `[0,2]^5`, where a valid infinity-norm Lipschitz bound is `40`
(the exact maximal row sums are in fact `28,8,24,24,16`). Gronwall yields
the author's equation (12). Its choices of `r_R` and `n_R` allot `alpha/2`
each to the martingale and generator-error terms, proving the claimed
uniform exponential window bound.

A good path starting at mass at most `9/8` cannot hit the upper threshold
before the lower success: at that putative hit the total difference from the
constant deterministic mass would be at least `7/8`, whereas tracking bounds
it by `5alpha <= 1/20`. This is an ordinary stopped argument, not an
assumption that the actual chain stayed bounded. Nonexplosion also follows
independently from `S(t)<=n+I(t)` and bounded rates on each finite state set.

## 5. O(n) windows, future-event conditioning, and all stopping cases

The initial tracking window has fast length `tau_epsilon`; its physical
endpoint `t0=tau_epsilon/n` is at most one. On a good first window, unless
removal has already occurred, the entropy at `t0` is below `h/2`.
Thereafter each full fast window of length `Delta` resets it below `h/2`.
The possible shorter final window only needs the whole-window bound; it
need not provide another reset. The number of these windows is at most
`5n/Delta+1 <= 5n+1`, since the explicit `Delta` exceeds one.

The conditional estimates can be formalized by defining a local bad event
only when its start is before the removal stop and is in the allowed
mass/entropy region. This start event is measurable in the past. Conditional
on it, the stopped bound above is uniform. One then unions the local bad
events *without conditioning on future immigration*. Intersecting afterward
with `G_I={I(5)<=n/8}` supplies all the needed upper bounds at window starts.
Induction supplies their entropy bounds. This justifies the stated cost

    10 exp(-c_tau n)+(50n+10)exp(-c_Delta n).

If the lower stopping time is at or before five, it is already a removal
success. Otherwise every time in `[t0,5]` has total exceeding `3n/4` and
entropy below `2h`. Pinsker then gives normalized A at least `1/6`, hence
`A(t)>=n/8` and the actual death compensator is at least `n/2`.
There is no long physical-time Gronwall estimate and no stochastic mixing
or equilibrium-distribution assumption.

## 6. Death and immigration accounting proves the exact time-five claim

On `sigma>5` and `G_I`, the count identity gives `D(5)<3n/8`.
Write the actual death count as `Y_D(Lambda_D(5))`. On the good-window event
`Lambda_D(5)>=n/2`, pathwise monotonicity implies

    Y_D(n/2) <= Y_D(Lambda_D(5)) = D(5) < 3n/8.

No independence between the compensator and its driving clock is asserted.
The Poisson lower-tail bound with mean `n/2` and relative deficit `1/4`
is `exp(-n/64)`. The immigration bound is also valid for `n>=512`:
using Chernoff parameter one and `e<3`,

    P[Poisson(5)>n/8] <= exp(5(e-1)-n/8)
                       <= exp(10-n/8) <= exp(-n/64).

If `sigma<=5`, then subsequent net total increase is at most subsequent
immigration, so on `G_I`, `S(5)<=3n/4+n/8=7n/8`, regardless of later
composition. These two cases exhaust the desired failure event.
Thus its probability is at most `100(n+1)exp(-c0 n)` with the stated positive
`c0`. The author's absorption threshold is finite; beyond `2/c0`, the function
`c0 n/2-log(100(n+1))` is increasing. This yields the final theorem with
`c=c0/2` and a finite uniform `n0(epsilon)`.

## 7. Review boundaries and saved support

No counterexample or necessary repair was found. The dependence on epsilon
enters only through the uniform deterministic entrance and its fixed-window
concentration constants. All constants may be fantastically poor, which does
not invalidate the stated sufficiently-large-n existence assertion.

This receipt does **not** acquire boundary/mesoscopic entrance into
`B,C,D,E>=epsilon S`; it does not validate the neighboring dyadic lemma,
compose its error budgets, or prove recurrence, stationary moments, or an
operationally useful entrance time. The global-attraction supplier remains an
explicit imported ordinary theorem rather than a reproof here.

Saved alongside this receipt:

- `independent_exact_audit.py`: a separately reconstructed exact reaction,
  balance, drift, boundary-inequality, and rational-margin audit;
- `independent_exact_results.json`: all 27 assertions PASS;
- `REVIEW_RECEIPT.json`: machine-readable decision and hashes.

No publication, hardware action, external state change, or paused Morrey work
was performed. No blocked or stopped source was accessed.
