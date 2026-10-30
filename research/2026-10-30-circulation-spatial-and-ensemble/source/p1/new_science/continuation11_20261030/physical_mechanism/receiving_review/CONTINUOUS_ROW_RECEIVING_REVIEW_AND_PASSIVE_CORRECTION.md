# Actual receiving review: loaded continuous rows and passive recording

30 October 2026. Existing physical-mechanism role. No new fixture or worker.

## Exact input and verdict

CONTINUOUS_ROW_RECEIVER_AND_LOADED_SCOPE.md was read in full.

SHA256: 06b57066f45b59966388534eab9853dc409c8a22f9368b6ea28693dea9d690fb.

Its exact snapshot and CONTINUOUS_ROW_REVIEWED_INPUT.json are preserved in
this directory. The separate four-coordinate metered carrier remains its
own dependency; this receipt does not reopen that cell's review.

**Accepted for the stated continuous fixed-row family.** Source cancellation,
the loaded kinetic-moment extension, and the native source-work/probe-heat
formulas are correct. The needed direct source estimate in the actual
metered filtration is derived below. Marginal likelihood transfer alone
does not establish its second-moment scaling.

## 1. Binding correction to the original passive proof

The preserved PASSIVE_FINITE_RESPONSE_DISPLACEMENT_RECORDER.md remains at
SHA256 83b0a3aff1d2ae35b4960eef68718b754575e76e86c3c1e2610048fe9eedef04.
Equation (19) contains the typography error “Cq,d”. The intended product is

\[
 \log E e^{q\mathcal A_T}
 \le C_0'd+C q d\,g^4T_N,\qquad qg^4T_N\le c.
 \tag{C1}
\]

No derivation, range or conclusion changes. This note corrects the pinned
file without changing its bytes.

Its final measure-identification paragraph is valid. Under the actual
passive native law, exponential integrability makes the reverse Girsanov
exponential a true martingale. That change restores the original native
drift, diffusion and initial law. Weak uniqueness of the original native
equation identifies the transformed marginal with the reference. Taking
the reciprocal gives the forward likelihood. No separate uniqueness claim
for a hypothetical Volterra apparatus is needed.

## 2. Source cancellation and raw current

Independent row-translation symmetry gives
\(\sum_\ell\partial_{y\ell}U_N=0\). With
\(S_y=\sum_\ell V_{y\ell}\) and actual displacement \(A_y\),

\[
 dS_y=(-\gamma_yS_y+F_y)ds+\sqrt{2\gamma_yN}\,d\beta_y,
 \qquad dA_y=S_y\,ds.
\]

Root's integrated identity has the correct sign and normalization:

\[
 A_y(s)+{S_y(s)-S_y(0)\over\gamma_y}
 =\int_0^s{F_y(u/N^2)\over\gamma_y}\,du
                    +\sqrt{2N/\gamma_y}\,\beta_y(s).
 \tag{R1}
\]

The raw instantaneous drift \(S_y\) is not uniformly bounded. The displayed
analytic endpoint correction is essential. After division by \(N^2\) on
time \(N^2t\), the corrected current has bounded drift and bracket
\(2/(\gamma_yN)\). Its continuous martingale has no bounded-jump cutoff.
Smooth convolution and the specified nonlinear target then have bounded
drift, including the \(O(1/N)\) Itô term, and vector bracket \(O(1/N)\).

Under canonical initialization the centered row sum has variance N and
its loaded mean is \(O(1)\). Uniform OU stability gives the stated full-time
tail exponent \(N^3/K_N^2\) for its normalized maximum-row endpoint
correction. A warm path ceiling adds \(C_0N^2\) once. The actual controller
does not measure or subtract \(S_y/\gamma_y\).

## 3. A direct proof of the loaded kinetic moments

The center/relative argument in root's Section 3 is valid. An equivalent
pathwise shift gives a particularly direct proof, including on circles.
Start with an unforced canonical solution of the actual metered system.
For each row solve the deterministic per-particle means

\[
 \dot v_y=-\gamma_yv_y-g y_y+F_y(s/N^2)/N,\quad
 \dot y_y=g v_y-p_y,\quad
 \dot p_y=y_y-a_yp_y,
 \qquad \dot c_y=v_y,
 \tag{R2}
\]

from zero. Shift every native position in row y by \(c_y(s)\), and add
\(v_y,y_y,p_y\) to its velocity, extension and pointer velocity. The actual
symmetry implies \(\nabla U_N(X+\{c_y{\bf1}\}_y)=\nabla U_N(X)\), so these
shifted paths solve the loaded equations exactly with the same Brownian
sources. The unmetered case omits the probe coordinates.

At \(g=0\), the mean matrix is the stable native friction plus stable probe
oscillator. Uniform small-perturbation stability gives
\[
 |v_y|\le C/N,\qquad |y_y|+|p_y|\le Cg/N
\]
for the bounded prescribed load. Thus at every time the loaded native
velocity field has covariance \(I_{N^2}\) and deterministic mean m with
\[
 |m|^2=\sum_yN|v_y|^2\le C.
 \tag{R3}
\]

This does not make nonlinear relative position histories Gaussian. It uses
their unforced canonical law and the independent Gaussian velocity factors.
The allowed cross-row relative interactions do not obstruct the shift.
For small \(\lambda\),
\[
 \log E e^{\lambda|V(s)|^2}
       \le C\lambda N^2+C\lambda.
 \tag{R4}
\]

A warm native initializer contributes its density ceiling relative to the
same prescribed-load experiment started canonically. It does not make the
actual warm relative law canonical. Jensen in time now supplies the exact
kinetic-moment premise of the passive likelihood argument under both laws:
\[
 \log E_0L_N^p,\quad\log E_gL_N^{-p}
 \le C_0'N^2+Cp^2H_N^2,\qquad p\le cN/H_N.
 \tag{R5}
\]

The observation residual subtracts the actual prescribed load as a proof
operation. The instrument does not identify the nonlinear native force.
Fresh conditional Gaussian probes remain essential. Recorder row means
are \(O(g)\), so their normalized count-error bias is \(O(N^{-2})\).
The joint precision and separate cap tails therefore survive the load.

## 4. Direct actual-filtration source and work moments

The subsequent message from root correctly identifies a needed distinction:
Hölder transfer proves a rare-law/tracking comparison, not the required
second-moment scaling. The continuous row family supplies a direct repair.

Let \(R_y=\sum_\ell Y_{y\ell}\), \(P_y^\Sigma=\sum_\ell P^{ptr}_{y\ell}\).
In the actual metered experiment,
\[
 \begin{aligned}
 dS_y&=(-\gamma_yS_y-gR_y+F_y)ds
                                +\sqrt{2\gamma_yN}\,d\beta_y,\\
 dR_y&=(gS_y-P_y^\Sigma)ds,\\
 dP_y^\Sigma&=(R_y-a_yP_y^\Sigma)ds
                                +\sqrt{2a_yN}\,d\omega_y.
 \end{aligned}
 \tag{R6}
\]

The row matrix is
\[
 A_g=\begin{pmatrix}-\gamma_y&-g&0\\g&0&-1\\0&1&-a_y\end{pmatrix}.
\]
It is uniformly stable for small g. Its unforced covariance is \(NI_3\):
the drift's symmetric part and the actual bath covariance cancel exactly.

Put \(D_y=\gamma_y+a_yg^2\) and
\(C_y=S_y+gP_y^\Sigma-a_ygR_y\). Direct substitution gives
\[
 dC_y=-D_yS_y\,ds+F_y\,ds
             +\sqrt{2\gamma_yN}\,d\beta_y
             +g\sqrt{2a_yN}\,d\omega_y.
\]
Therefore
\[
 \boxed{
 A_y(s)+{C_y(s)-C_y(0)\over D_y}
 =\int_0^s{F_y(u/N^2)\over D_y}\,du
                       +\sqrt{2N/D_y}\,\widetilde\beta_y(s).}
 \tag{R7}
\]

The Brownian motion is the normalized combination of the two actual
sources, not a new apparatus input. Equivalently
\[
 k=-A_g^{-T}e_1=D_y^{-1}(1,-a_yg,g)^T.
\]
This verifies the matrix corrector proposed in root's latest message.

Crucially, (R7) remains a martingale decomposition in the full causal
native/probe/controller filtration: the displayed bath increments are
fresh there. It does not condition them on future successful readings.
Thus it directly supplies bounded corrected drift, \(O(1/N)\) normalized
Brownian bracket and ordinary second moments. Its corrector has \(O(N)\)
row variance and bounded mean under canonical initialization with the
prescribed load. It is super-volume negligible after normalization, as
in (R1). Unknown coefficients remain analytic proof parameters.

Under that same canonical loaded law, normalized native intrinsic pointer error
has second moment \(O((NH_N)^{-1})+O(N^{-4})\) per row. Stable deterministic
convolution can therefore bound its contribution to the executed governor's
second moments, in addition to its joint error and cap tails. A bounded
deterministic final-reader bias belongs to the separate \(O(1/K_N)\)
allowance. No second moment is obtained by postselecting a successful
future event or by appealing only to an LDP.

An arbitrary warm ceiling of order \(e^{C_0N^2}\) does not by itself retain
the same per-row moment scaling. Its rare-law transfer survives, while
actual work needs its initial moment/transient budget or the stated
canonical initialization. The direct repair should therefore accompany
the work claim with that distinction.

## 5. Actual source work and probe excess heat

For a constant load, steady aggregate means are
\[
 \overline S_y=F_y/D_y,\quad
 \overline P_y^\Sigma=gF_y/D_y,\quad
 \overline R_y=a_ygF_y/D_y.
\]
Source work rate is \(F_y\overline S_y/N\); probe excess heat rate is
\(a_y(\overline P_y^\Sigma)^2/N\). Hence on time \(N^2T\),
\[
 EW_{\rm native}=TN\sum_y{F_y^2\over D_y}+O(1),
\qquad
 EQ_{\rm probe}^{excess}
   =TNg^2\sum_y{a_yF_y^2\over D_y^2}+O(1).
 \tag{R8}
\]

These are root's formulas and give \(O(N^2)\) and \(O(H_N)\). Native and
probe excess dissipation sum exactly to source work:
\[
 {\gamma_y\over N}\overline S_y^2+
 {a_yg^2\over N}\overline S_y^2
 ={F_y\over N}\overline S_y.
\]
The centered canonical initial mean transient costs \(O(1/N)\) source work
per row, hence \(O(1)\) in total. Uniform center stability also bounds the
probe-heat transient within the stated \(O(1)\). Unknown nonlinear relative
interactions remain unforced and canonical and do not alter these terms.
Warm initial states can carry additional excess energy, as root states.
These expressions do not price complete readout or apparatus operation.

## 6. Scope and receiving conclusion

Common within-row coefficients, actual row-translation symmetry and fixed
row attribution are load-bearing. Arbitrary particlewise friction/damping
or arbitrary cross-row forces do not supply the same decomposition. A
particle changing Eulerian row needs another attribution mechanism.

The three-step composition in root's Section 4 keeps the correct
likelihood scope: extend the native marginal only by independent auxiliary
primitive sources, then compare actual and ideal governors on the same
native path and primitives. The full native probe-noise record does not
inherit the small marginal likelihood cost. Its final-reader and metered
carrier estimates remain explicit dependencies.

A native good path LDP must still be warranted. The source symmetry does
not derive one for every unknown potential. The actual root input correctly
keeps that receiving boundary, the continuous-material versus exclusion
distinction, and the final reader/export costs.

**Conclusion:** the loaded moment bridge and heat formulas are accepted.
Equation (R7) directly repairs actual-filtration source/work estimates under
the stated canonical initialization and prescribed load. Native-marginal
likelihood transfer is reserved for identifying the unchanged rare-law
rate. The original passive proof remains pinned with correction (C1).
