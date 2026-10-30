# Binding metered-cell and loaded-receiver clarifications

30 October 2026. Preserve the actual reviewed inputs unchanged:

* `METERED_FINITE_CELL_AND_SPATIAL_ERROR.md`, SHA256
  `dc141155fe9933e9a7c2cd475ec01aa7d2f02ac251ebcd6188fd61a0d391a655`.
* `CONTINUOUS_ROW_RECEIVER_AND_LOADED_SCOPE.md`, SHA256
  `06b57066f45b59966388534eab9853dc409c8a22f9368b6ea28693dea9d690fb`.

## 1. Aggregate normalization in the FDT proof

The metered-cell note's final asymptotic sentence in Section 3 omitted the
aggregate particle number N. The correct statements in its notation are

\[
 \operatorname{Var}_0 A_m=Nm\|\sigma_g\|²+O(N),\qquad
 {d\over dF}E_FA_m=Nm\mu_g+O(N).
\]

Equivalently its sentence applies to a one-carrier normalization. The exact
cell, current corrector, energy argument and final ||sigma_g||²=2mu_g are
unchanged. The actual record-geometry review identified this correction.

## 2. Tracking precision and mean work have different moment premises

Joint error tending to zero with super-volume failure suffices for tracking
and the LDP. To retain O(N²+NK_N) carrier-force work, deterministic timestamp,
evaluator and command bias must be O(1/K_N), or its actual second-moment
contribution must be priced separately. Intrinsic pointer errors have
second moment O(1/(NH_N)); H_N>=K_N supplies the earlier fluctuation order.
A generic o(1) deterministic bias alone does not give the quoted work bound.

The complete held force retains the full-block-old filtration, including
readout/evaluation error. A reader or delivery process correlated with the
intervening thermal innovations needs a separate work argument. Successful
decoding or later postselection does not retroactively supply this
filtration. Within-block actuator noise is not hidden in a held force.

## 3. Likelihood transfer is not a second-moment work proof

Two-sided native-marginal Holder comparison transfers the native LDP and
super-volume events. It does not by itself transfer the O(1/(NK_N)) source
moments needed for the governor. The continuous row family supplies them
directly. Under actual passive measurement let z_y=(sum V,sum Y,sum P_ptr).
With the same prescribed uniform native load as in the receiving note,

\[
 dz_y=A_yz_y ds+e_1F_y(s/N²)ds+\sqrt N D_y dW_y,\quad
 A_y=\begin{pmatrix}-\gamma_y&-g_N&0\\g_N&0&-1\\0&1&-a_y\end{pmatrix},
 \quad D_yD_y^T=\operatorname{diag}(2\gamma_y,0,2a_y).
\]

Internal native forces cancel by independent row translation invariance.
This matrix is uniformly stable on the positive compact parameter class
for small g_N. Its unforced stationary covariance is N I_3. With
k_y=-A_y^(-T)e_1, true native displacement therefore obeys

\[
 dA_y+k_y^Tdz_y=(k_y)_1F_y(s/N²)ds+\sqrt N k_y^TD_y dW_y.
\]

All coefficients are bounded and (k_y)_1=1/(gamma_y+a_y g_N²). Normalized
current has bounded drift, Brownian bracket O(1/N), and a stable Gaussian
endpoint corrector. This identity holds in the **full physical
source/probe/controller filtration**, with its actual independent future
sources. A marginal filter is not substituted into that filtration.
Nonlinear smoothing uses the same analytic endpoint comparison as before.

Under exact canonical native and independent Gaussian probe initialization,
with the prescribed bounded row load, these direct bounds provide the
joint tracking and second moments. The passive native-marginal theorem is
then used only to identify the rate with the unmetered material. The new
continuous receiver's stated loaded carrier-work bound has this canonical
initial scope. A broader warm native start retains its stated rare-law
comparison but requires its actual initial kinetic/transient work term;
that cost is not obtained by Holder or set to zero. The earlier isolated-
source work theorem retains its own accepted initialization scope.

## 4. Records and laws being compared

The passive follower preserves the native marginal rate at speed N², and
its coarse pointer error is negligible there. It changes finite-system
native trajectories. Its complete microscopic probe-bath record does not
have the small marginal likelihood cost. The original isolated-source
theorem still supplies exact native path preservation at its declared
noninvasive interface. Neither result is substituted for the other.

Final pointer reading, its forces, common-mode noise, gain calibration,
unwrapped range/slip control, synchronization and message integrity remain
actual suppliers. A new mechanical coordinate is not a completed external
reader. The full preparation, thermal capacity, switching and apparatus-
energy ledger remains binding.
