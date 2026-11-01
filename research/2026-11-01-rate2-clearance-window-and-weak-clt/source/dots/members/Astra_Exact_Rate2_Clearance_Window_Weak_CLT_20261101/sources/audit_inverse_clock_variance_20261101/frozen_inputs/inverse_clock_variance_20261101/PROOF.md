# Rigorous acquisition of a deterministic candidate clock variance

**Author calculation, pending independent review. Not an actual-chain CLT or
an exact finite-noise diffusion variance. The previously accepted `s_*` freeze
is unchanged.**

## Result and useful cost

For the orbit from `(l,e)=(0,0)` of

    dl/ds=1+3l²e,  de/ds=2l²,  l=s+3e²/4,

put `J(e)=exp[-∫_e^∞ l(v)^(-3) dv]`. The deterministic functional

    Sigma²=∫_0^∞ (1−J(e))² dl(e)

has the rigorous outward-rounded enclosure

    0.5677211094 <= Sigma² <= 0.5687113183.

The exact certificate width is less than `0.000990208879`, meeting the requested
absolute width `10^-3`. It took about ten seconds on this local executor:
8,106 inverse-coordinate intervals, 16,212 order-five validated Taylor
half-steps, and 1,024 startup rectangles. There is no precision refinement
beyond the requested target. Thus this particular **ordinary scalar
acquisition is cheap enough to be a useful component**; this is not an
end-to-end finite-N complexity or simulation benchmark.

All proof arithmetic is rational or the existing 120-bit directed-dyadic
integer arithmetic. Exponential bounds below use finite rational series and
an explicit remainder. JSON stores exact fractions and outward decimal
strings; the elapsed runtime is integer nanoseconds and is not proof evidence.

## 1. Reused, explicitly bound scalar construction

`validated_variance.py` imports the frozen `validated_clock.py` read-only.
The existing forward polynomial startup and nonexpansive inverse Taylor
method are used without modification. The initial inverse pair is
`a>=e(1/2)`, `s(a)` enclosed by the existing startup. Integration runs from `a`
to `E=8` with mesh at most `2^-10`; each interval is split into two validated
Taylor steps so its midpoint state is available. All inverse state errors,
Taylor remainders, and arithmetic rounding are therefore enclosed by the
already proved scalar construction. The terminal inverse state width is
less than `5.04*10^-16`.

The deterministic functional and its macroscopic tail are from the qualified
root source `boundary_clearance_kernel_root_20261101/REMAINING_CLOCK_OBSERVABLE.md`.
Hashes of both sources and the scalar freeze/receipt are in `SOURCE_BINDINGS.json`.
No stochastic hypothesis is imported through these deterministic sources.

## 2. Backward acquisition of J, including its infinite tail

Write `L(e)=s(e)+3e²/4` and `V=L'=1/(2L²)+3e/2`. Then

    L''=3/2−V/L³,
    H=L^(-3),
    H''=12V²/L^5+3V/L^7−(9/2)/L^4.

On an interval `[a,b]`, `L` is increasing, so an interval-certified lower
endpoint `L_min>0` gives

    V <= 1/(2L_min²)+3b/2 =: V_max,
    |H''| <= 12V_max²/L_min^5+3V_max/L_min^7+(9/2)/L_min^4 =: M.

The midpoint quadrature enclosure is consequently

    ∫_a^b H(e)de ∈ (b−a)[H((a+b)/2)] + [−M,M](b−a)³/24.

Every quantity is evaluated outward. Intersecting a lower bound with zero is
safe because `H` is positive. The interval states at the midpoint contain the
same actual orbit: the proof never treats separately rounded states as an
uncorrelated orbit.

For the infinite tail, suppose the certified inverse time at `E` is `[L_s,H_s]`.
By the proved time tail, throughout `e>=E`,

    L_s <= s(e) <= U_s:=H_s+8/(27E³).

The exact elementary inequalities, valid for `x>=0`, are

    1−3x <= (1+x)^(-3) <= 1−3x+6x².

For example, multiply by `(1+x)^3`; the differences are respectively
`6x²+8x³+3x⁴` and `10x³+15x⁴+6x⁵`, both nonnegative. Substituting
`x=4s/(3e²)` and integrating gives

    H_tail >= 64/(135E^5)−256U_s/(189E^7),
    H_tail <= 64/(135E^5)−256L_s/(189E^7)
                            +2048L_s²/(729E^9).

The code checks these bounds are positive and ordered. Add the finite midpoint
pieces backward to this tail interval and evaluate `exp(−H)` to enclose every
node value of `J`. Monotonicity of the exponential automatically handles the
endpoint order.

### Finite rational exponential algorithm

For an interval `z>=0`, divide outward by powers of two until its upper endpoint
is at most `1/8`. Sum the first 18 positive Taylor terms of `exp(z)`. If `t_19`
is the next term, the remaining tail is at most

    t_19 / [1−z/20],

because every successive ratio is at most `z/20`. Add the interval from zero
to that upper bound, then repeatedly square to undo scaling. Reciprocation
encloses `exp(−z)`. All denominators are positive. This is a rational interval
construction, not an appeal to a floating-point exponential.

## 3. Verified origin startup for the singular sensitivity

Let `s0=1/2`, and let `P` be the same degree-78 exact forward polynomial, with
nonnegative coefficients and residual

    R(s)=2s²+3sP²+(9/8)P⁴−P',
    0<=R(s)<=R0(s/s0)².

The last inequality holds because the residual coefficients below degree 78
vanish and all remaining coefficients are nonnegative. On the existing
rectangle `0<=s<=1/2`, `0<=e<=1/4`, the forward derivative in `e` is bounded
by `L0=105/128`. Define the *cubic* barrier

    delta3=R0/[s0²(3−L0*s0)],  U(s)=P(s)+delta3*s³.

The code checks `U(s0)<1/4`. Since

    U'−f(s,U) >= delta3*s²(3−L0*s0)−R(s) >=0,

comparison proves `P<=e<=U` on the whole startup interval. This is a fresh
justified variant of the startup, not an assumption about a singular inverse
initial value. Coefficient positivity and an exact check also give

    (2/3)s³ <= e(s) <= C*s³,  C=84/125.

Now use `de/ds=2l²` to rewrite

    d(log J)/ds=2/l,
    2/l=2/s−k(s),
    k(s)= (3/2)(e(s)/s³)² s^4
                     / [1+(3/4)(e(s)/s³)² s^5].

Thus, for every `0<s<=s0`,

    J(s)=J(s0)(s/s0)² exp[∫_s^s0 k(u)du],

where the factor is regular and explicitly bounded. In particular,

    K_minus*s^4 <= k(s) <= K_plus*s^4,
    K_minus=(2/3)/[1+(3/4)C²*s0^5],
    K_plus=(3/2)C².

Integrating these powers yields rational bounds for the regular exponential
factor at each startup node. Their limit proves `J(0)=0`; the code uses that
exact endpoint rather than dividing by zero.

The inverse solver begins at `a>=e(s0)`, not exactly `e(s0)`. Since `l>=s0`
on the intervening segment and `e(s0)>=P(s0)`,

    0<=∫_e(s0)^a l^(-3)de <= 8[a−P(s0)].

Using `exp(−z)>=1−z` and the computed interval for `J(a)` gives a rigorous
`J(s0)` enclosure. The extra variance over this tiny joining segment is at
most its `l`-length, charged explicitly as `gap_variance_upper`.

At each of 1,025 equally spaced forward nodes, the polynomial and cubic barrier
are evaluated by directed interval arithmetic, using their sparse powers
`s^(3+5k)`. This prevents cancellation or subtraction of unverified approximate
node values when forming level increments.

## 4. Variance quadrature uses monotonicity, not an unproved smooth error model

`J` increases from zero to one, while `l` increases. Hence `q²=(1−J)²` decreases.
For consecutive true level values `l_i,l_(i+1)`,

    q_(i+1)² (l_(i+1)−l_i)
      <= ∫_l_i^l_(i+1) q² dl
      <= q_i² (l_(i+1)−l_i).

If level intervals are `[L_i,H_i]`, their nonnegative increment is enclosed by

    [max(0,L_(i+1)−H_i), H_(i+1)−L_i].

Use the lower endpoint of `q_(i+1)` for the lower rectangle and the upper
endpoint of `q_i` for the upper rectangle, with outward products. These
inequalities remain valid regardless of dependency between adjacent interval
values. They pay all rectangle error and all uncertainty in the `J` and `l`
node values. Sum separately over the startup and inverse meshes.

For the terminal variance tail, `1−J <= ∫_e^∞ l^(-3) <= 64/(135e^5)` and
`dl/de <= 8/(9e^4)+3e/2`. Therefore the root source's explicit bound is

    0 <= V_tail <= (4096/18225)[(8/117)E^(-13)+(3/16)E^(-8)].

At `E=8`, this is less than `2.512*10^-9`. The tail is added, not discarded.

The interval-width ledger is:

| Paid contribution | Upper bound on width |
|---|---:|
| Forward startup, including regular sensitivity bounds | `0.000235684126` |
| Inverse region, including state/J/rectangle errors | `0.000754522242` |
| Final variance tail | `0.000000002512` |
| Startup joining segment | less than `10^-26` |
| Final directed rounding of tail/join charge | less than `2^-120` |

The certificate records exact values, including the final rounding excess.
Their sum equals the total rational enclosure width.

## 5. Meaning and limitations

This is a finite deterministic integral, evaluated by ordinary validated ODE,
quadrature, rational exponential bounds, and analytic tails. No new numerical
principle or superiority to established validated solvers is asserted.

The coefficient is a **candidate** clock-fluctuation variance for a separately
justified linearized Gaussian limit with the specified noise covariance.
Neither a finite-N count-chain CLT nor that covariance nor terminal-tail
passage has been proved by this calculation. It is not an exact finite-noise
Ito variance, not a measured SSA variance, and not a finite-N CDF solver.
A stochastic boundary/continuation/clock-martingale bridge must still earn
those connections. The present result only establishes that acquiring this
particular scalar target is inexpensive once the deterministic orbit is known.
