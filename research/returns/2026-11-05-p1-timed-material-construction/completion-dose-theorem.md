# Competitor-free completion dose within a specified planar model

The [supplied return](P1_REACTIVE_INTERFACE_CONSTRUCTION_20261105_RETURN.txt) contains the analytic argument. This is a completed deduction within ordinary compound-growth physics, not an acquired universal constitutive law or a demonstrated manufacturing recipe.

## Exact statement and indispensable assumptions

Maintain a reservoir of A and a finite total areal B inventory `N_B`. Ordered line compounds have B fractions `0<a=c_1<b=c_2<...<c_n<1`; the desired final compound is `c_1`, with atomic molar volume `V_1` and final thickness `L=V_1 N_B/a`.

Assume quasistationary planar diffusion, local interface equilibrium, already available product phases and the stated admissible topology. After elemental B exhausts, outer phases can disappear successively, but the nearest competitor `c_2` remains adjacent to the target until the last competing phase disappears. The target's integrated diffusivity `D_1(t)` must be known under its **actual neighboring phases**. It cannot be imported unchanged across different boundary chemical potentials without justification.

Define the dose `H(t)=integral_0^t D_1(s) ds`. In the ideal initially zero-product-thickness limit,

\[
\frac{a(b-a)}{2b}L^2
\le H(t_{complete})\le
\frac{a(1-a)}2L^2.
\]

No competing compound's transport coefficient occurs in this interval. Those coefficients may vary with time/history along admissible trajectories. The number and molar volumes of additional compounds also disappear; the target law, target volume, total inventory and nearest competing composition remain inputs.

The theorem does not discover which phases form or justify its topology. The source reports a positive measured initial-layer variant, avoiding a claim that zero-thickness continuum growth predicts nucleation. Its full formula belongs to the original report rather than being reconstructed here.

## The weighted amount eliminating competing fluxes

For physical layer widths `h_i`, write `ell_i=(V_1/V_i)h_i` and `d_i=(V_1/V_i)^2D_i`. Standard interface balances take the form `ell_dot=C(d_i/ell_i)`, with tridiagonal entries

\[
C_{ii}=\frac1{c_i-c_{i-1}}+\frac1{c_{i+1}-c_i},\quad
C_{i,i+1}=-\frac1{c_{i+1}-c_i},\quad c_0=0,c_{n+1}=1.
\]

Its inverse is `G_ij=min(c_i,c_j)[1-max(c_i,c_j)]`. The weighted amount

\[
Z=(G\ell)_1=a\sum_i(1-c_i)\ell_i
\]

satisfies `Z_dot=D_1/h_1`, hence `dH=h_1 dZ`. All competing fluxes cancel. When an allowed outer layer disappears its contribution is zero, preserving continuity of `Z` through the interface removal.

Finite inventory and nonnegative amounts give

\[
\max\!\left(0,
\frac{bZ-a^2(1-b)L}{a(b-a)}\right)
\le h_1\le\frac{Z}{a(1-a)}.
\]

At completion `Z_f=a(1-a)L`. Integrating these thickness envelopes against `dZ` proves the dose interval. The upper envelope is a stopping certificate inside the model: an incomplete state cannot accumulate more dose than it permits. No fitted clock is introduced.

## Consequence and limits

Detailed phase trajectories generally need the separate transport laws, but a bounded complete-conversion question can need fewer inputs. Additional B-rich phases do not themselves widen the interval; its upper/lower ratio is `b(1-a)/(b-a)`, large when the nearest competitor approaches the target composition.

For Cu3Sn/Cu6Sn5, `a=1/4`, `b=5/11`, so `(9/160)L^2<=H_complete<=(3/32)L^2`, ratio `5/3`. A hypothetical one-front 10 micrometre final target at `D_1=1.85e-17 m^2/s` gives 84.46–140.77 hours. No such film was prepared here.

Numerical cases with multiple compounds, time-varying rates and explicit layer disappearance supplement the analytic proof; they are not new empirical observations. Existing Wagner/Stefan growth, finite-layer disappearance and related quadratic diffusion identities are credited. The source did not find this particular competitor-free interval in its examined references, but does not establish exhaustive priority, optimality or improved experimental accuracy.

Changing the target's nearest neighbor, permitting other topology, blocked contact, nucleation or unmodeled resistance changes the hypotheses. The bound does not manufacture the missing target coefficient or a mechanical-quality law.
