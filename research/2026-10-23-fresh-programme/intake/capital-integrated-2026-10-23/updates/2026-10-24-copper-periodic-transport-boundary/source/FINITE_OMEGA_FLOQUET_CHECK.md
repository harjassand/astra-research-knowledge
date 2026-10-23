# Finite-\(\Omega\) Floquet cross-check of the reduced boundary model

**Scope.** This is an independent numerical check of the reduced, supported-diffusion boundary equations supplied for this checkpoint. It is not the Pastor–Rubio CuSO\(_4\)-only experiment, a CuSO\(_4\) physical validation, or the full ionic/moving-domain model in [SOURCE_MATCH_AND_MODEL.md](SOURCE_MATCH_AND_MODEL.md). The mean domain is frozen; the dilute linear diffusion base and prescribed sinusoidal surface concentration are taken as given. Mean-boundary motion, Stefan/advection corrections, ion migration, reaction/transport parameter inference, and physical mechanism claims are outside this check.

## Equations integrated

Use the specified fixture \(D=L=1,\ c_0=r_0=0.5,\ k=1,\ \omega=10,\ b=0\), \(C_\infty=c_0+r_0L/D=1\), and
\[
Z=\frac{\tanh(L\sqrt{i\omega/D})}{D\sqrt{i\omega/D}}
 =0.219781958174-0.229758380603i,
\quad T=2\pi/\omega.
\]
For each \(\varepsilon\), evaluate
\[
r(t)=r_0+\varepsilon\cos(\omega t),\quad
C_s(t)=c_0-\varepsilon\Re(Ze^{i\omega t}),\quad
A(t)=r(t)/C_s(t),\quad C(t)=A(t)r(t)/D,
\]
and \(S(t)=C(t)-\dot C_s(t)\). The requested perturbation equations are
\[
w_t=D(w_{xx}-k^2w),\quad w(L,t)=0,\quad
D w_x(0,t)=A(t)w(0,t)+S(t)h,
\]
\[
\dot h=\Omega[A(t)w(0,t)+C(t)h].
\]
Writing \(v=w/h\) and \(g=\dot h/h\) gives the finite-\(\Omega\) periodic problem
\[
v_t=D(v_{xx}-k^2v)-g v,\quad
D v_x(0,t)=A(t)v(0,t)+S(t),\quad v(L,t)=0,
\qquad g=\Omega[A(t)v(0,t)+C(t)].
\]
After \(v\) reaches its attracting periodic orbit, its cycle-average \(\bar g\) is the Floquet exponent of \(h\). This includes the within-cycle height feedback through \(-gv\); it is not the leading-\(\Omega\), height-fixed calculation.

The checker [floquet_screen.py](floquet_screen.py) uses centered second differences for interior nodes and classical RK4 over complete periods. It eliminates the interface value from a third-order one-sided derivative condition,
\[
D\frac{-11v_0+18v_1-9v_2+2v_3}{6\Delta x}=A v_0+S,
\quad
v_0=\frac{18v_1-9v_2+2v_3-6\Delta x S/D}{11+6\Delta x A/D},
\]
then evolves the interior \(v_i\). This boundary stencil avoids the first-order boundary-adjacent defect that arose with a lower-order derivative formula. The code reports the paired difference \(\Delta\lambda=\bar g_\varepsilon-\bar g_0\) and coefficient
\[
\mathcal C_{\Omega,\varepsilon}=\frac{\Delta\lambda}{\Omega\varepsilon^2}.
\]
The DC comparator has the same \(r_0\), period, and modeled total charge as the pulsed case.

## Results

The raw finite-grid coefficients are below. The number of RK4 steps per period was increased approximately as \(N^2\), where \(N=L/\Delta x\); each result uses eight periods to remove the initial transient.

| Cells \(N\) | \(\mathcal C\), \(\Omega=10^{-3}\) | \(\mathcal C\), \(\Omega=10^{-4}\) |
|---:|---:|---:|
| 12 | -0.00406148 | -0.00409271 |
| 16 | -0.00494208 | -0.00497329 |
| 24 | -0.00548814 | -0.00551935 |
| 32 | -0.00564477 | -0.00567597 |
| 48 | -0.00573593 | -0.00576713 |
| 64 | -0.00576129 | -0.00579249 |
| 80 | -0.00577126 | -0.00580246 |

Thus the finite-\(\Omega\) pulse correction stays negative on every mesh tested. At \(N=80\), \(\varepsilon=0.05\), the paired shifts are \(-1.44281457\times10^{-8}\) at \(\Omega=10^{-3}\) and \(-1.45061461\times10^{-9}\) at \(\Omega=10^{-4}\). The underlying DC exponent is still positive; this small pulse correction lowers the growth rate, rather than stabilizing the mode outright.

The requested leading-\(\Omega\) value is \(-0.00581944646574\). Spatial convergence is not complete at raw \(N=80\). A simple local linear extrapolation in \(1/N^2\) using \(N=64,80\) gives \(-0.00578899\) for \(\Omega=10^{-3}\) and \(-0.00582019\) for \(\Omega=10^{-4}\). Including \(N=48\) in a three-point least-squares fit gives \(-0.00579182\) and \(-0.00582302\), respectively. The few-\(10^{-6}\) fit spread is a realistic numerical limitation here; the small-\(\Omega\) estimates approach the supplied leading coefficient, but this finite-grid check is not a new derivation of that coefficient.

Checks beyond the spatial sequence:

- At \(N=48,\Omega=10^{-3},\varepsilon=0.05\), increasing from 16,384 to 32,768 RK4 steps per period changes \(\mathcal C\) from \(-0.005735927826353\) to \(-0.005735927821366\) (about \(5.0\times10^{-12}\)).
- At \(N=48\), replacing \(\varepsilon=0.05\) with \(0.025\) changes \(\mathcal C\) by \(3.6\times10^{-7}\) at either \(\Omega\), consistent with small higher-order pulse-amplitude effects.
- At \(N=48,\Omega=10^{-3}\), the coefficient for 6, 8, and 10 periods is \(-0.00573562838,-0.00573592783,-0.00573592832\); 8-to-10 cycle change is below \(5\times10^{-10}\).

## Boundary of the result

This verifies the sign of the pulse-induced Floquet correction and its approach toward the given leading-\(\Omega\) coefficient for this reduced fixture. It does not validate a copper bath, identify a morphology mechanism, or close the physical moving-domain gate. In particular, the prescribed periodic \(C_s(t)\) and local flux are assumed; the unsupported 0.5 M CuSO\(_4\) source has neither a measured local flux nor the dilute supporting-electrolyte conditions needed to import this check. For that source, the coupled binary-ion/BV eigenproblem and calibrated current/area accounting remain unresolved as stated in [SOURCE_MATCH_AND_MODEL.md](SOURCE_MATCH_AND_MODEL.md).
