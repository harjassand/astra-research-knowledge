# Unknown gains: two concrete barriers under first local motion

The full unknown-gain question is **not resolved in this tranche**. What is
established is a uniform unknown-coefficient primitive, a sharp obstruction
to composing that primitive into a calibrated gate, and an admitted moving
bath that defeats the straightforward higher-degree replacement. These
results identify a substantive remaining control problem rather than
silently importing the predecessor's stronger regularity assumptions.

The supplied supplement corrects the attribution: earlier Astra already
contains native sign-group projection, order raising and odd-chirality
polynomial compensation. Those are retained as predecessors. The results
here concern their transfer to arbitrary time dependence with **only** the
first local-motion bound.

## The surviving positive primitive

Let `c=g_A g_B g_C in [1,8]` and `F=Z_1X_2`. The first-tranche ten-segment
cycle remains uniformly valid if its native strengths are reduced to
`+/-1/2`. The unknown normalized gains then lie in `[1/2,1]`; the same norm
and Lipschitz bounds apply. Its clean cubic term is `-i c d^3 F/2`.

For every prescribed coefficient `alpha`, one can therefore implement

\[
R_c(\alpha)=e^{-i\alpha cF}
\]

to arbitrary finite averaged-channel accuracy without calibration. For
positive `alpha`, choose `Nd^3=2alpha`. The explicit joint-channel bound,
including a free bath unitary, is

\[
\text{error}\le25000\alpha d,
\quad T=20\alpha d^{-2},
\quad\text{native segments}=20\alpha d^{-3},\quad 10d\le1.
\]

Flipping the C convention handles negative `alpha`. Uniform finite timing
precision follows from the same common-duration and event-time estimates
as the first tranche. This supplies a real uncertain logical rotation,
not a gate with a gain-independent angle.

## Arbitrary mixtures of these completed rotations have a sharp error floor

Any private randomized program built exclusively from the completed
`R_c(alpha)` operations reduces, for each realized schedule, to
`exp(-icAF)` for a real random coefficient `A` independent of the gain.
No length, duration or discrete-support restriction is imposed in this
statement. Bath unitaries may depend on the schedule; final bath discard
removes them on arbitrary correlated inputs.

At the two allowed gain points `c=1` and `c=2`, its coherence multipliers
are `m_1=E Z` and `m_2=E Z^2`, where `Z=exp(-2iA)`. The desired multiplier
is `-i` at both points. Positivity of the three-by-three moment Toeplitz
matrix gives the exact minimax obstruction

\[
\max\{|m_1+i|,|m_2+i|\}
\ge\frac{\sqrt3-1}{2}\approx0.3660254.
\]

These absolute differences are the corresponding diamond distances.
The bound is sharp for this two-point comparison: a mixture supported on
`A=pi/2` and `A=pi/6` attains it. If physical synthesis contributes total
uniform error `delta`, any proposed target guarantee `epsilon` must obey
`epsilon+delta >= (sqrt(3)-1)/2`.

Thus arbitrarily accurate, arbitrarily long composition or randomization
of the earned commuting logical primitive cannot compensate the gains.
Native interactions inside uncompleted macros are outside this theorem.

## The higher-degree native bridge also encounters real noise

The predecessor compensates unknown chirality using higher odd powers,
implemented by flat higher-degree native Lie words. A generic replacement
of its high-order bath jets by the first-tranche random-sign argument does
not work.

Consider any **fixed** finite pulse shape with zero handle areas and with
zero-drift unitary `I+O(tau^5)` for each whole-word parity-sign choice.
Repeat it with fresh parity signs. Assume A is used nontrivially. I construct
a bath using only `H_M(t)=eta_k h(t/tau) Z_M`, with `|h|<=1/2` and zero mean
within each cycle. It is fixed independently of all private signs and initial
data, and satisfies the required commutator bound. The independent `eta_k`
are an adversarial proof distribution over predetermined trajectories.

The combined averaged cycle channel has the expansion

\[
\Psi_\tau=\mathrm{Id}+\tau^4\left[
a_A^2(\operatorname{Ad}_{X_1Y_M}-\mathrm{Id})
+a_B^2(\operatorname{Ad}_{X_2X_M}-\mathrm{Id})\right]+O(\tau^5),
\qquad a_A>0.
\]

This is channel noise, not a removable bath unitary. Its coefficient is
obtained from the publicly known control profile; the bath never reacts to
the current private signs. A fifth-order channel remainder has the explicit
bound `(3ell)^5 tau^5/120`, where `ell` is the fixed normalized word duration.

The two admissible inputs
`rho_+/-=(I_D +/- Z_1Z_2)/4 tensor I_M/2` start with trace-norm distance two.
The displayed dissipator contracts their difference. For a prefix of `m`
cycles, every purported full-program target guarantee must satisfy

\[
\epsilon\ge1-(1-2S\tau^4)^m-mK_5\tau^5,
\quad S=a_A^2+a_B^2>0,
\quad K_5=(3\ell)^5/120.
\]

Later controls and final memory discard cannot restore the lost joint
distinguishability. Choosing
`m=ceil(log(1/tau)/(2S tau^4))` shows that whenever
`N >> tau^-4 log(1/tau)`, worst-bath error is at least `1-o(1)` against
any data unitary. Some fixed admitted trajectory attains the adversarial
lower bound by convexity.

A degree-`k>4` primitive repeated with `N beta tau^k=theta!=0` falls in
this failing regime. The successful cubic primitive finishes earlier,
with `N=O(tau^-3)`, so there is no conflict with the first tranche.

The fixed-shape assumption matters. This does not exclude every changing,
epsilon-dependent native program, every form of private waveform
randomization, or every nonperturbative mechanism.

## Exact predecessor instance and checks

The inherited raw word `ad_a^2[c,[a,b]]` has 46 segments and frozen leading
term `-16i tau^5 F`. Exact Gaussian-integer series arithmetic checks its
vanishing lower coefficients for all four parity choices. A rational
piecewise-constant bath profile gives

\[
a_A=188/11,\qquad a_B=-128/77,\qquad S=1748240/5929.
\]

The complete moving-bath series through degree four is checked exactly,
not just fitted from samples. Its surviving channel dissipator has rates
`35344/121` and `16384/5929` on the two Paulis above.

Finite output diagnostics use `16N tau^5=pi/4`. At `N=100,000`, at least
one of the two displayed inputs has trace-norm target error at least
approximately `0.999896`; at `N=10,000,000`, the lower witness is about
`0.999999977`. The same finite witnesses also occur for one deterministic
periodic bath profile, with `eta_k=+1` throughout. These floating-point
checks illustrate the analytic failure; matrix-power rounding is not
treated as a certified enclosure.

The exact and numerical outputs are in [CHECKS.txt](CHECKS.txt). The
complete proofs and all scope assumptions are in
[DERIVATION.md](DERIVATION.md). Runnable files are
[macro_moment_barrier.py](macro_moment_barrier.py),
[high_order_barrier.py](high_order_barrier.py), and
[numerical_high_order.py](numerical_high_order.py); the exact Pauli helper
is [pauli_series.py](pauli_series.py).

The remaining frontier is precise: construct a uniform unknown-gain target
using native resources beyond the commuting completed library, while
avoiding the fixed higher-degree weak-word noise mechanism; or prove an
all-policy obstruction. Neither has been established here. No calibration,
meter, stronger local regularity, independent audit, hardware capability or
practical advantage is claimed.

Sources used: the frozen `CONTROL_TASK.md`; this arm's preserved first
tranche and checkpoint; `predecessor_supplement/uniform_gate_THEORY.md`,
especially the pure-control powers, flat extraction and polynomial
compensation in Sections 4-9; `LOCAL_REGULARITY.md` for the finite-jet
hypotheses; and `original_native_THEORY.md` for the earlier sign-projection
and order-raising context. The 46-segment degree-five word is inherited,
not a new synthesis claimed by this continuation.
