# Static-resolvent route to a continuous negative-work witness

## Claim boundary

This is a narrower possible route than proving the whole fixed-amplitude,
fixed-slow-frequency metastable cycle. It can establish negative control
work for a sequence of finite barriers if a static Poisson-resolvent limit
is proved. It does **not** establish the original `A=0.3`, slow angular
frequency `0.01` diffusion cycle, its full-cycle fuel convergence, useful power,
or a hardware realization. The amplitude and physical frequency chosen
for the finite-barrier existence argument may depend on `H` and may shrink
as `H` grows.

## Exact one-dimensional stationary and Poisson formulas

Write the zero-control tilted potential on the lift as
`psi_H(x)=V_H(x)+w(x)`, with `psi_H(x+3)=psi_H(x)-3F`. The diffusion
generator on densities at a static field `h` is
\[
L_h^*u=u''+\partial_x[(\psi_H'-h f')u].
\]
Its normalized stationary density on the circle is
\[
\rho_{H,h}(x)=Z_{H,h}^{-1}e^{-\psi_H(x)+h f(x)}
  \int_x^{x+3}e^{\psi_H(y)-h f(y)}dy,
\]
where `Z` is the integral over one period. This identity follows directly
by solving the constant-current stationary ODE; it does not assume detailed
balance. At `h=0`, let `rho=rho_{H,0}` and `r=partial_h rho_{H,h}|_0`. The
derivative is explicit:
\[
 r(x)=\rho(x)[a(x)-\langle a\rangle_\rho],\quad
 a(x)=f(x)-\frac{\int_x^{x+3}f(y)e^{\psi_H(y)}dy}
                         {\int_x^{x+3}e^{\psi_H(y)}dy}.
\]
The centering term is the derivative of the normalization, so `int r=0`.

Let `z_H` be the unique zero-mass periodic solution of
\[
L_0^*z_H=r.
\]
With the signed current `j_z=-z_H'-psi_H'z_H`, the second-order equation
reduces exactly to
\[
j_z'(x)=-r(x),\qquad z_H'(x)+\psi_H'(x)z_H(x)=-j_z(x).
\]
Thus
\[
j_z(x)=c-\int_0^x r(s)ds,\qquad
z_H(x)=e^{-\psi_H(x)}\left[C-\int_0^x e^{\psi_H(y)}j_z(y)dy\right].
\]
The two constants are fixed by `z_H(3)=z_H(0)` and `int_0^3 z_H=0`.
The finite-barrier friction is
\[
\zeta_H=-\int_0^3 f(x)z_H(x)dx.
\]
This gives a direct quadrature/linear-system route for checking any chosen
finite `H`; it avoids fitting a time-periodic trajectory. Sign convention:
`W_ctrl,on=-int hdot <f>dt`, so `zeta_H<0` means the controller receives
work in linear response.

## Exact limiting-chain sign

For the rates in `PERIODIC_METASTABILITY_GATE.md`, set `f=(1,0,0)` and
write `Q_0=Q(0)`, `Q_1=partial_h Q(h)|_0`. The zero-control stationary
column, its field derivative, and the Poisson vector satisfy
\[
Q_0\pi=0,\quad \mathbf1^T\pi=1,\qquad
Q_0r_Q=-Q_1\pi,\quad\mathbf1^Tr_Q=0,\qquad
Q_0z_Q=r_Q,\quad\mathbf1^Tz_Q=0.
\]
In probability-column convention the exact matrices are
\[
Q_0=\begin{pmatrix}
-26/25&4/25&1/1000\\
1&-161/1000&1/300\\
1/25&1/1000&-13/3000
\end{pmatrix},\qquad
Q_1=\begin{pmatrix}
13/25&2/25&1/2000\\
-1/2&-2/25&0\\
-1/50&0&-1/2000
\end{pmatrix}.
\]
Exact rational elimination gives
\[
\pi=\frac{(2083,13400,22320)^T}{37803},\qquad
\zeta_Q=-f^Tz_Q=-\frac{29239948720000}{54023012580627}
\simeq -0.5412498734009076<0.
\]
This is a strict finite-dimensional sign, not a numerical inference. It
comes from the driven stationary circulation; equilibrium passivity does
not apply because the constant-force cycle affinity is nonzero.
`chain_friction_exact.py` reproduces these equations and asserts all exact
residuals, normalizations, and the strict sign using only Python's
`Fraction` arithmetic.

There is also an exact static current check from the same quadrature. The
unnormalized stationary density `U_1` has flux `-1`, so the normalized
circle probability current is `j_H=-1/N_H`, `N_H=int U_1`. The well/saddle
Laplace sum gives `kappa_H*N_H -> 37803/61`, hence
`j_H/kappa_H -> -61/37803`; mean unwrapped displacement velocity is
`3*j_H`, so `(3*j_H)/kappa_H -> -61/12601`. This is the nonzero base
chemical circulation, with sign consistent with `F<0` and positive signed
force work `F*Delta X`.

## What asymptotic lemma would be enough

The needed static metastable statement is a zero-frequency resolvent
limit, not the stronger time-periodic path theorem. Let `C_H` map a
zero-mass density perturbation to its three well masses, and let `f_well`
be `(1,0,0)`. The target is
\[
C_H r_H\to r_Q,\qquad
\kappa_H C_H(L_0^*)^{-1}r_H\to Q_0^{-1}r_Q=z_Q,
\]
with enough control on the part orthogonal to well masses that
\[
\kappa_H\int_0^3 f(x)(L_0^*)^{-1}r_H(x)dx
\longrightarrow f_{well}^Tz_Q.
\]
Equivalently, `kappa_H*zeta_H -> zeta_Q < 0`. Frozen Eyring–Kramers
rates and convergence of stationary well masses suggest this limit but do
not prove the inverse-operator statement: the inverse is amplified by the
small slow eigenvalues, and the nonreversible operator need not be normal.
The explicit density and Poisson quadratures above make a Laplace/resistance
proof plausible in one dimension. A proof must bound the intrawell and
transition-region pieces after multiplication by `kappa_H`, not just the
three well masses.

If this limit is established, `zeta_H<0` for every sufficiently large but
finite `H`. At each such fixed `H`, the uniformly elliptic diffusion on the
compact circle has a unique periodic density for a periodic field. Its
small-amplitude, low-frequency expansion is
\[
W_{ctrl,on}(A,\Omega)
=\pi A^2\Omega\,\zeta_H
+O_H(A^3\Omega+A^2\Omega^2),
\]
for `h(t)=A cos(\Omega t)` as `A,Omega -> 0`. To see the sign, write
`rho(t)=rho_{h(t)}+hdot z_{h(t)}+O_H(\Omega^2 A)`, where
`L_h^*z_h=partial_h rho_h`; the quasistatic term is the exact closed
integral `-int <f>_{rho_h} dh=0`, while the leading lag term is
`int zeta_H(h) hdot^2 dt`. Since
`int_0^{2pi/Omega} hdot^2dt=pi A^2 Omega`, a negative `zeta_H(0)` yields
strictly negative work after choosing positive `A` and `Omega` small enough
at that fixed `H`.

The remainder constants are allowed to depend on `H`. Consequently this
argument does not support a common amplitude, the specified `A=0.3`, or
`Omega=0.01*kappa_H`; it only gives a finite-parameter witness after the
resolvent limit and then a diagonal choice of sufficiently small positive
amplitude/frequency. Since `|zeta_H|` scales like `1/kappa_H`, choosing
`Omega_H << kappa_H` gives vanishing output power, not an efficiency or
practicality result. In that low-amplitude, quasistatic regime the base
circulation makes the signed affinity work per cycle scale like
`kappa_H/Omega_H`, whereas control output scales like
`A_H^2*Omega_H/kappa_H`; their ratio tends to zero when
`Omega_H/kappa_H -> 0`. This static-current observation does not give
full-cycle fuel convergence for the originally selected driven waveform.

## Independent numerical chain check

`chain_reference.py` integrates the exact tilted triangle with RK4 and
the one-period fixed point. Halving the slow-time step from `0.04` to
`0.02` leaves the displayed control work unchanged to about `1.1e-16`:
`W_ctrl,on=-0.0007462686944465` for the *different* fixed choice
`A=0.3`, `Omega_slow=0.01`. It gives periodic start law approximately
`(0.07002353,0.33340768,0.59656878)` and net unwrapped chain displacement
`-3.0386858797339`; the signed force work `F*E[Delta X]` is `+3.0997338839971`
under the convention that this is work delivered by the constant force to
the particle. The one-period Markov kernel has TV Dobrushin coefficient
about `0.00132632`. These are numerical chain values only. They do not
validate the same fixed waveform in the diffusion.
