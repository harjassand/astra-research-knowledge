# Audit of the nearest-cell, multiple-link range bound

This checks the proposed extension from one rank-one intercell link to a
finite scalar cell with positive intracell springs and arbitrary positive
springs from a cell to its nearest neighbor. Let the cell masses be `m_j`,
`M=sum_j m_j`, and let the total stiffness of cross-cell links counted once
per cell be `K_aff=sum_e kappa_e>0`. For Bloch phase `q`, a cross edge
`e=(j,k)` contributes `kappa_e |x_j-e^(iq)x_k|^2` to the mass-normalized
quadratic form. Write `s=sin^2(q/2)` and
`Omega^2=4K_aff/M`.

## Mode-shape inequality and constants

Take a lowest normalized Bloch eigenvector at `q`, with
`sum_j m_j |x_j|^2=1` and eigenfrequency `omega(q)<=a`, where
`a=max_q sqrt(lambda_min D(q))`. Decompose it into cell center of mass and
internal deviations:

`X=sum_j m_j x_j/M`, `y_j=x_j-X`, `sum_j m_j y_j=0`.

Let `E_q` collect the cross-edge differences weighted by `sqrt(kappa_e)`,
and define

`W(y)=K_aff^(-1) sum_(e=(j,k)) kappa_e(|y_j|^2+|y_k|^2)`,
`F_q=||y||_M^2+M W(y)`.

The cross-edge part of the normalized mode energy cannot exceed total energy,
so `||E_q x||_kappa<=omega(q)<=a`. Also,

`||E_q(X 1)||_kappa=|1-e^(iq)|sqrt(K_aff)|X|=2sqrt(s K_aff)|X|`,
`||E_q y||_kappa^2<=2 sum_e kappa_e(|y_j|^2+|y_k|^2)=2K_aff W(y)`.

For `|q|>=pi/2`, `s>=1/2`; the triangle inequality therefore gives

`sqrt(M)|X| <= sqrt(2) a/Omega + sqrt(M W(y))`.

Since `||x||_M=1`,

`1 <= sqrt(M)|X|+||y||_M <= sqrt(2)a/Omega+sqrt(2F_q)`.

Thus if `a<=Omega/(2sqrt(2))`, then `F_q>=1/8` throughout this half-zone.
The constants in the proposed shape estimate check.

## Gibbs average and range cap

In a periodic ring, form the translation-invariant per-cell quadratic
observable whose Bloch-mode coefficient is `F_q`. Its thermal expectation is
the normalized sum over `q` and bands of `F_q` times the normal-coordinate
variance. For a quantum harmonic mode,

`Var(Q_omega)=hbar/(2omega)coth(hbar omega/(2k_B T)) >= k_B T/omega^2`.

The lowest mode at every `|q|>=pi/2` has `F_q>=1/8` and `omega(q)<=a`; that
zone has asymptotic density `1/2`. Hence in the thermodynamic limit

`F_variance >= k_B T/(16 a^2)`

whenever `a<=Omega/(2sqrt(2))`. At finite ring size, the factor is the exact
fraction of sampled wave numbers in the selected half-zone and converges to
`1/2`; the q=0 translation is absent from this bound.

If each internal relative displacement `r_j=x_j-x_b` has centered RMS at most
`d`, then `y_b=-sum_(j!=b)m_j r_j/M`, so `rms(y_b)<=d`, and
`y_j=y_b+r_j` gives `rms(y_j)<=2d`. Therefore
`E||y||_M^2<=4Md^2`; every endpoint in every cross edge has variance at most
`4d^2`, so `E W<=8d^2`. This gives
`F_variance<=12Md^2`. Combining the two cases proves

`a >= min(Omega/(2sqrt(2)), sqrt(k_B T/(192 M d^2)))`.

No node-count or graph-degree constant enters. Retuning internal masses,
intracell springs, and cross-link placement at each temperature does not
affect this bound if `M,d,K_aff` are held fixed and the stated positive,
nearest-cell scalar model remains in force.

## Conductance implication and channel caveat

The lowest eigenvalue is continuous, equals zero at `q=0`, and reaches
`a^2`. Its range therefore contains `[0,a^2]`. For regular interior
frequencies, a Bloch crossing and its time-reversed partner give a right-moving
channel. Critical frequencies, band edges, or a flat-band value can have zero
group velocity; these exceptional values do not affect the Landauer integral.
Thus the precise transport statement is an almost-everywhere channel
coverage, sufficient for

`J >= integral_0^a g_theta(omega) d omega`.

At fixed `M,d` and fixed positive `K_aff`, for sufficiently small `T` the
second branch of the minimum yields
`a/theta >= hbar/(sqrt(192 M)d sqrt(k_B T))`, where
`theta=k_B T/hbar`. Therefore the missing part of the single-channel quantum
integral is at most
`theta integral_(a/theta)^infinity g_1(x)dx`, which is a polynomial factor
times `exp[-c/sqrt(T)]`. The lower-channel conclusion is uniform over cell
topology and retuning under these fixed-resource hypotheses; total
conductance may of course exceed one quantum because additional channels can
carry heat.

One quantifier matters: the phrase “fixed `M,d`” alone is insufficient if
`K_aff` may also vanish with temperature. For example, take two equal masses
per cell, a fixed positive intracell spring `k0`, and a single backbone
cross-cell spring `K_aff(T)=T^4` in fixed units. The internal relative
zero-point variance remains finite, so a fixed sufficiently large `d` caps
it. But `Omega=O(T^2)`, the acoustic bandwidth is `O(T^2)`, and the optical
band width is `O(T^4)` around a nonzero frequency; at `theta=O(T)`, the
normalized conductance tends to zero rather than one quantum. This does not
contradict the displayed bound: its first term also tends to zero. A uniform
low-temperature quantum-channel conclusion requires fixed `K_aff>0`, or at
least a uniform lower bound on it, in addition to fixed `M,d`.

The result is for positive reciprocal scalar springs and nearest-cell range.
It does not cover nonreciprocal/gyroscopic couplings, negative or active
elements, longer-range links, or a continuum of channels.

## Full-quantum covariance strengthening

For the arbitrary finite-shift theorem, the Gibbs coefficient is not merely
bounded below by its classical part. The full coefficient

`c_T(omega)=hbar/(2 omega) coth(omega/(2 theta))`,
`theta=k_B T/hbar`,

is strictly decreasing for `omega>0`: differentiating its dimensionless
factor gives a negative multiple of
`coth(x)+x csch^2(x)`, where `x=omega/(2 theta)`. Thus on the set of
normalized measure at least `1/3`, where `F>=1/12` and `omega_min(q)<=a`,
positivity of all other mode contributions gives

`V_F >= c_T(a)/36`.

The already audited range cap is `V_F<=12 M d^2`, so, in the branch
`a<=Omega_aff/4`,

`c_T(a)<=432 M d^2`,
`a tanh(a/(2 theta)) >= hbar/(864 M d^2)`.

Since `tanh<=1`, this implies `a>=hbar/(864 M d^2)` in that branch; in the
other branch `a>Omega_aff/4`. Hence

`a>=min(Omega_aff/4, hbar/(864 M d^2))`.

With fixed positive `K_aff`, `M`, and finite `d`, this gives a positive
temperature-independent cutoff. The normalized deficit below one channel is
then bounded by the Bose tail at `a/(2 theta)`, hence by a polynomial in
`1/T` times `exp(-c/T)` for some resource-dependent `c>0`. The nearest-cell
constants similarly sharpen to
`min(Omega/(2 sqrt(2)), hbar/(384 M d^2))`: there `F>=1/8` on half the zone,
so `V_F>=c_T(a)/16`, while the cap is still `12 M d^2`. For the separate
self-coordinate-rail estimate in the theorem, its mass-relative observable
has `F>=1/4` on half the zone and cap `4 M d^2`, giving the stated
`hbar/(64 M d^2)` term.

These strengthenings require the stated `d` to cap the **total centered
Gibbs variance**, including zero-point motion. If `d` instead bounds only
thermal excess above the ground-state covariance, replacing `k_B T/omega^2`
by the full `c_T(omega)` in the lower bound is not justified; the earlier
thermal-only bounds remain the applicable ones. A uniform cutoff also
requires fixed positive `K_aff` (or a uniform lower bound), as the earlier
vanishing-`K_aff(T)` example shows.

### Correction: excess-only quantum variance

The preceding caveat's sentence suggesting that the earlier thermal-only
`k_B T/omega^2` lower bounds remain applicable under an excess-only quantum
variance cap was incorrect. The quantum thermal-excess coefficient

`c_ex(omega)=hbar/[omega (exp(omega/theta)-1)]`

is no larger than `k_B T/omega^2`; it cannot supply that classical lower
bound. If the excess-only variance is separately capped by `12 M d^2`, the
finite-shift mode estimate instead gives

`V_ex>=c_ex(a)/36`,
`a (exp(a/theta)-1)>=hbar/(432 M d^2)`.

This temperature-dependent inequality does not imply a positive
temperature-independent cutoff. The classical Gibbs model supports the older
thermal bound; the full quantum Gibbs model supports the zero-point
strengthening above. An excess-only quantum cap lies outside those two
conclusions unless handled with its own inequality.
