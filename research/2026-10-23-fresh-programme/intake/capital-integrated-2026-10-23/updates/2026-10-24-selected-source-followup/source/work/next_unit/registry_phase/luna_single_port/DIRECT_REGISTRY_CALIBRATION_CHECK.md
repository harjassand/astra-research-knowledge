# Direct registry calibration: slip-robust TV bound

24 October 2026. Bounded check of the proposed pointwise calibration for the
periodic-registry energy. No source, fixture, or spectral-band claim.

Let `V(w)=V0(1-cos(2 pi w/d))`, `q(w)=sqrt(2 S V(w))`, and
`m_c=4 sqrt(V0/S)/pi`. The mean of `q` over one registry period is
`S m_c`. Hence there is a bounded `d`-periodic primitive `R` satisfying
`R'(w)=q(w)-S m_c`. For `|m|<=m_c`, direct expansion gives the exact
pointwise identity

```text
S/2 (w_x-m)^2+V(w) - S m^2/2 - (m/m_c)R'(w)w_x
 = S/2 [w_x-(m/m_c)q(w)/S]^2
   +(1-m^2/m_c^2)V(w) >= 0.
```

The factors and sign check: the square's cross term is
`-(m/m_c)q(w)w_x`; the two remaining multiples of `V` combine to
`(1-m^2/m_c^2)V` because `q^2=2SV`.

## Apply it to composition-dependent mismatch

Assume `a<0`, `a+S alpha^2>0`, and the strict condition
`|alpha|sqrt(-2a/b)<m_c`. Choose a smooth cutoff `chi(phi)` equal to one on
`|phi|<=sqrt(-2a/b)`, supported in
`|alpha phi|<m_c`, and with `0<=chi<=1`. Then for every `phi`,

```text
f(phi)+chi(phi) S alpha^2 phi^2/2 >= 0,
f(phi)=a phi^2/2+b phi^4/4.
```

Since the mismatch density `E_m=S/2(w_x-alpha phi)^2+V(w)` is nonnegative,
`E_m>=chi E_m`. On the support of `chi`, apply the identity with
`m=alpha phi(x)` and integrate. Define
`B(phi,w)=chi(phi) alpha phi R(w)/m_c`. The calibrated cross term is
`B_w w_x`; periodicity gives `integral B_w w_x = -integral B_phi phi_x`
because `integral d_x B=0`. Therefore the full energy obeys

```text
F[phi,w] >= kappa/2 integral |phi_x|^2 dx
             - C integral |phi_x| dx,
C = sup_{phi,w} |B_phi(phi,w)| < infinity.
```

Finiteness follows because `chi` has compact support in `phi`, and `R` is
bounded and periodic. This estimate is independent of slip count and of the
absolute displacement level. It uses only `phi,w` in the periodic `H^1`
energy class, so the chain rule and boundary cancellation hold at that
regularity. The imposed zero winding `w(L)=w(0)` ensures periodic boundary
data; more generally the same cancellation holds for an integer registry
winding because `R` is `d`-periodic. Non-periodic endpoint phases would add
the explicit boundary term `B(L)-B(0)`.

If `F/L<=-q0<0`, then
`C TV(phi)/L >= q0 + kappa/(2L) integral |phi_x|^2`, so
`TV(phi)/L>=q0/C` (and `C=0` would make such a sublevel impossible). Thus a
fixed negative energy-density gap forces a nonzero composition total-
variation density. For any fixed-parameter deterministic gradient flow with
`F_dot<=0`, the same inequality applies at every later time after crossing
that sublevel. This is a slip-robust macroscopic-coarsening obstruction for
this exact registry functional; it is not the earlier Fourier-band bound,
does not select a wavelength or morphology, and is not uniform as the strict
amplitude margin or negative energy-density gap tends to zero.

## Finite-spacing check and representation boundary

For a periodic chain of spacing `h`, set `Delta_i=w_i-w_(i-1)`,
`m_i=alpha phi_i`, and
`E_i=S/(2h)(Delta_i-h m_i)^2+hV(w_i)`. The function `R' = q-S m_c` is
Lipschitz with constant `Lq` (even though `q` has cusps at registry minima),
so expansion at `w_i` gives
`|R(w_i)-R(w_(i-1))-R'(w_i)Delta_i| <= Lq Delta_i^2/2`. Consequently,

```text
E_i - h S m_i^2/2 - (m_i/m_c) DeltaR_i
 >= [S-h(|m_i|/m_c)Lq] Delta_i^2/(2h)
    + hV(w_i) - (|m_i|/m_c)q(w_i)|Delta_i|.
```

Writing `t=|m_i|/m_c`, completion of the quadratic in `|Delta_i|` makes the
right side nonnegative when `t^2 + nu_h t <= 1`, where `nu_h=hLq/S`.
Thus the admissible local ratio is
`t<=r_h=(sqrt(nu_h^2+4)-nu_h)/2`. A cutoff equal to one on the negative-
`f` interval and supported in `|alpha phi|<m_c r_h` yields the same bound
after discrete summation by parts: with
`a(phi)=chi(phi)alpha phi/m_c`,
`sum_i a(phi_i)DeltaR_i = sum_i [a(phi_i)-a(phi_(i+1))]R(w_i)`, whose magnitude
is at most `||R||_infinity Lip(a) sum_i |phi_(i+1)-phi_i|`. The discrete
composition term is nonnegative under the same `a+S alpha^2>0` premise.
Therefore a negative energy density `F_h/(nh)<=-q0` forces a nonzero
discrete total-variation density, with this finite-`h` calibration, for all
later times of any fixed-parameter finite-dimensional dynamics that conserve
the composition mean and satisfy `dF_h/dt<=0`.

This is an exact statement about the displayed continuous-valued lattice
functional and its stipulated passive dynamics. It does not identify an alloy
Hamiltonian/free energy, establish that `phi_i` is a continuous local
composition rather than a binary occupation, or derive physical hopping,
registry-slip, or thermal transition rates. A physical application would
first need a justified coarse-grained state map and parameterization at the
actual lattice scale. The deterministic sublevel bound is not a finite-
temperature pathwise result or a claim about experimentally realized
microphase separation.
