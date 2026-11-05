# Fully reversible positive deviation: an exact two-cycle example

This is a synthetic counterexample to the proposition that instantaneous thermal equilibration always maximizes turnover. It is not a model fit to the cobalt/calixarene catalyst and is not a newly discovered microscopic mechanism. The six-state stationary problem, its thermal projection and the full-cycle response identity are independently verified with exact rational arithmetic in `projection_two_cycle_witness.py` and its results JSON.

## States, rates, thermodynamics

The states are `(A,0),(A,1),(B,0),(B,1),(C,0),(C,1)`. All state free energies are zero. Each thermal gate pair has rate gamma in both directions. Set `a=(A,1)`, `b=(B,0)`, `c=(B,1)`, `d=(C,0)`, `e=(C,1)`; `(A,0)` is a thermal leaf attached to a.

There are four reversible chemical channels. Each listed forward direction produces one counted chemical product and each reverse direction consumes one. The forward/reverse ratio is R on every channel, so there is exactly one chemical affinity `A=log R` and total stationary entropy production is `sigma=A J`:

| Forward channel | Forward rate | Reverse rate |
|---|---:|---:|
| a to d | u | u/R |
| e to a | v | v/R |
| d to b | w | w/R |
| c to d | z | z/R |

All rates are positive, all reactions are reversible and all work is included. The two productive cycles are `d,e,a,d` and `d,b,c,d`; each has one thermal transition and two forward product events. The rate unit is arbitrary until a physical timescale is supplied.

Write

\[
D_A=u\gamma+uv+v\gamma/R,\qquad
D_B=wz/R+w\gamma/R+\gamma z.
\]

With `p_d=x`, direct stationarity gives

\[
{p_a\over x}={v\gamma+(u/R)(\gamma+v)\over D_A},\quad
{p_e\over x}={\gamma(u+v/R)+uv/R^2\over D_A},
\]

\[
{p_b\over x}={w(z+\gamma)+\gamma z/R\over D_B},\quad
{p_c\over x}={\gamma w+(w/R+\gamma)z/R\over D_B}.
\]

The leaf has probability `p_a`, so `x=1/[1+2 p_a/x+p_e/x+p_b/x+p_c/x]`. The two net cycle currents and target current are

\[
I_A={\gamma x uv(1-R^{-2})\over D_A},\quad
I_B={\gamma x wz(1-R^{-2})\over D_B},\qquad J=2(I_A+I_B).
\]

The thermal projection equals the limit gamma to infinity with the chemical rates held fixed. Define

\[
A_\infty={v+u/R\over u+v/R},\quad
B_\infty={w+z/R\over w/R+z},\quad
x_\infty={1\over2(1+A_\infty+B_\infty)}.
\]

Then `I_A,infinity=x_infinity uv(1-R^-2)/(u+v/R)` and `I_B,infinity=x_infinity wz(1-R^-2)/(w/R+z)`.

For gamma=1, R=100, u=0.1, v=1000, w=10 and z=100, exact evaluation gives

\[
J={61105\over87342}=0.699606145955,\qquad
J_{th}={60330\over303697}=0.198651945854,
\]

\[
G={3711481037\over1053868572}=3.52176840226.
\]

## Mechanism and resource limits

The thermal projection spends 98.8914% of its time in chemical configuration A, whereas the finite-rate process spends 63.6706% there. The faster B cycle consequently increases from 0.0498852 to 0.318003 cycles per unit time, while the slower A cycle falls from 0.0494407 to 0.0318003. Thermal equilibration at C feeds a slow, strongly populated branch; finite bath relaxation limits that traffic and permits more progress through B. This is ordinary correlated cycle selection and kinetic trapping under chemical drive. There is no energy-free pump or entropy-free kinetic memory.

The example has zero gate free-energy splitting, bath lifetime one rate unit, chemical rates ranging from 0.001 to 1000 and chemical affinity log(100) per counted event. It does not use the reported 0.126 eV mode energy. Rescaling the bath rate to 1/(41 ns) scales every displayed chemical rate and J by 2.439e7/s; J then becomes approximately 1.706e7/s. The observed slow per-site turnover cannot be combined with the relative gain by changing only the units. These are indispensable resource conditions, not omitted implementation details.

The root bound holds, but its maximum-based gain limit is 4515.77 for this example. A constructive positive gain therefore does not demonstrate a sharp or predictive positive-gain bound.

## A topology limitation that the example evades

For a finite fully reversible **single ring**, with all fixed state energies and affinities, multiply any undirected edge's forward and reverse rate by lambda. The stationary cycle current has numerator lambda N and denominator `D0+lambda D1` with positive D0,D1, by the directed matrix-tree formula. Hence the magnitude of its current increases monotonically with lambda. For a family of bath edges scaled together, every spanning tree omits exactly one ring edge; the denominator has only powers lambda^m and lambda^(m-1), and the same monotonicity follows. A pendant tree contributes positive occupancy storage and preserves the corresponding one-edge monotonicity when its own rates are not changed.

Consequently a simple unicyclic catalytic model cannot obtain positive turnover gain over the same-architecture infinite-bath-rate projection merely by slowing its thermal gate. More than one independent chemical cycle, alternative branches, additional affinities, or changes to the chemical architecture are needed to evade that statement. The present graph has two independent cycles. This is a structural restriction on simplified explanations, not a universal exclusion for multi-site catalysts and not a novelty claim about unicyclic rate theory.

## Nonvacuity separate from sharpness

The independent exact rational examples in `projection_exact_witnesses_results.json` include a different six-state process with actual gain 1.01986877632, kappa=0.226255343767 and the rigorous maximum-based upper gain 1.60205835604. Thus the theorem can exclude a gain of 3.3 when its microscopic inputs are known. The threefold example above instead has a large coefficient and a loose bound. The distinction is crucial: the theorem is a computable conditional certificate, not a claim that all physically plausible catalysts have a small coefficient.
