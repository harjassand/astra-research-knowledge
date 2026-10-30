# A finite-duration interacting-carrier port

**Status.** Constructive supplier theorem at an explicitly supplied local mechanical-operation interface. It is not an apparatus demonstration, a passive projection of the old conductor, or a claim that unknown kinetics alone supply the additional port. The protected task counts the true displacement of all carriers in the composite conductor. The unbiased reference contains the same added lanes, carriers and thermal operations. This file is separate from the bounded-rate independent-walker supplier.

## 1. Physical state and operations

An auxiliary circular lane has circumference (N) and contains (R) unit-charge, unit-mass carriers. Write their unwrapped positions as (X_l), velocities as (V_l), and attached neutral internal coordinates as (Y_l), (1\leq l\leq R). Actual charge displacement is

\[
J(t)=\sum_l[X_l(t)-X_l(0)],\qquad P(t)=\sum_lV_l(t).
\tag{1}
\]

Every part of the particle motion below contributes to (1). There is no subtraction of native motion from the measured physical current.

The relative interaction can be unknown. A concrete sufficient interface is a smooth, periodic, finite-range, translation-invariant potential (U(X;h)), with a frozen unknown microscopic parameter (h), satisfying

\[
\sum_l\partial_{X_l}U(X;h)=0.
\tag{2}
\]

Assume the resulting finite-dimensional dynamics is globally well posed. The center-of-mass statements only need the actual force-conservation identity (2), even for more general hidden relative dynamics. The invariant-law statement below is asserted only for the displayed conservative model. External substrate drag or hidden forces that fail (2) are outside this supplier.

Fix (g,b>0), independent of (N), and put

\[
h_*=\frac{\pi}{2g},\quad p_*=h_*+b,\quad
\beta=\frac2g+b.
\tag{3}
\]

One period consists of two actual local operations. A common force (F_k) acts on every carrier and is kept constant throughout the period.

**Transport, duration (h_*).** Supply the energy-conserving local coupling

\[
\dot X_l=V_l,\qquad
\dot V_l=-\partial_lU-gY_l+F_k,\qquad
\dot Y_l=gV_l.
\tag{4}
\]

**Bath, duration (b).** Disconnect only the \(V_l\)--(Y_l) coupling. The actual particle dynamics and the same force continue:

\[
\dot X_l=V_l,\qquad \dot V_l=-\partial_lU+F_k.
\tag{5}
\]

Meanwhile each (Y_l) is quarter-rotated with a freshly prepared neutral coordinate \(\xi_{l,k}\sim N(0,1)\):

\[
\dot Y_l=\Omega\xi_{l,k},\quad
\dot\xi_{l,k}=-\Omega Y_l,\qquad
\Omega=\frac{\pi}{2b}.
\tag{6}
\]

Thus \(Y_l\) at the next period is the freshly prepared input \(\xi_{l,k}\); the old \(Y_l\) is carried into the retired coordinate with a sign. This is a finite-duration exchange, not an instantaneous reset or a white-force Langevin equation. Gaussian preparation, retirement, switching, synchronization and control are paid operations. The equation specifies a bounded-frequency response, not a hard amplitude bound; the Gaussian variables have unbounded support. Discontinuous switching of the coupling is an ideal part of this interface. A hardware pulse envelope must implement the stated period map, or its actual error must be included.

The auxiliary lane is mechanically and electrically isolated from the old conductor except for the declared sensing and externally supplied force. Its coupling to the old conductor is through classical feedback. Each added charge and oscillator is an actual extra component. A finite-range interaction does not require one separate full circular track per carrier; an independent-track implementation is a different, more expensive supplier.

## 2. Preparation and conditional independence

At every bath exchange, the incoming \(\xi_{l,k}\) are independent standard Gaussians, independent of all earlier physical and controller records and of the other lane's incoming coordinates. Their values are not read to select the next force. The controller sees physical current records and any older data allowed by the specified interface. Since (5) is disconnected from (Y,\xi), the next fresh \(Y\) has not influenced particle motion before the next force is selected.

Consequently, with \(Y_k=\sum_lY_l(kp_*)\),

\[
Y_k\sim N(0,R)
\tag{7}
\]

independently of the information used to choose (F_k), including the actual particle momentum \(P_k\), if that momentum is observed. This is the precise filtration required below. Exposing future bath seeds or using their preparation readout to select (F_k) would change it. An old retained record is allowed only when these same conditional initial/future statements remain true.

For \(F=0\), (4) preserves both volume and
\(U+\sum_l(V_l^2+Y_l^2)/2\). The particle Hamiltonian motion in (5) and the rotation (6) preserve the corresponding extended Gibbs law. Hence the full unbiased period kernel leaves

\[
\pi_h(dX)\prod_l\varphi(dV_l)\varphi(dY_l),\qquad
\pi_h(dX)\propto e^{-U(X;h)}dX
\tag{8}
\]

invariant. This does not claim that the unknown positional Gibbs law can be prepared, or that a given initial state converges to it.

The current identity needs no equilibration of relative positions. It is sufficient to start with arbitrary positions and hidden \(h\), a fresh \(Y_0\), and a supplied aggregate initial-momentum tail. Independent standard-Gaussian initial \(V_l\) supply \(P_0\sim N(0,R)\). Their preparation is charged. More general initial velocities are allowed with the explicitly corresponding endpoint bound.

## 3. Exact physical current cell

Summing (4) removes every unknown relative force:

\[
\dot P=-gY+RF_k,\quad \dot Y=gP,\quad \dot J=P.
\tag{9}
\]

At the end of the transport stage,

\[
P_h=-Y_k+\frac{RF_k}{g},\qquad
J_T=\frac{P_k-Y_k}{g}+\frac{RF_k}{g^2}.
\tag{10}
\]

During the bath the particles continue to move, and their full additional displacement is

\[
J_B=bP_h+\frac{RF_kb^2}{2},\qquad
P_{k+1}=P_h+RF_kb.
\tag{11}
\]

Combining (10)--(11) gives the two exact cell identities

\[
\boxed{P_{k+1}=-Y_k+RF_k(1/g+b)},
\tag{12}
\]

\[
\boxed{\Delta J_k+\frac{\Delta P_k}{g}
=-\beta Y_k+\frac{R\beta^2}{2}F_k.}
\tag{13}
\]

Equation (13) is an analytic martingale correction to the true current (1); it does not redefine the physical observable. All applications must bound its momentum endpoint. The corrected current has mobility and noise per unit physical time

\[
\mu=\frac{\beta^2}{2p_*},\qquad
E[\Delta J_k+\Delta P_k/g\mid\mathcal F_k]
=\mu Rp_*F_k,
\quad
\operatorname{Var}(\Delta J_k+\Delta P_k/g\mid\mathcal F_k)
=2\mu Rp_*.
\tag{14}
\]

These formulas retain the full unknown \(U\). They follow from force conservation, not from a dilute approximation or a learned rate.

## 4. Endpoint and within-period control

For any adapted forces \(|F_k|\leq a\), (12) implies

\[
|P_k|\leq |Y_{k-1}|+Ra(1/g+b),\qquad k\geq1.
\tag{15}
\]

The explicit sinusoidal transport solution and linear bath solution also give a constant \(C=C(g,b)\) such that

\[
\sup_{0\leq t\leq Kp_*}|P(t)|
\leq C\left(|P_0|+\max_{0\leq k<K}|Y_k|+Ra\right),
\tag{16}
\]

and the same right side, multiplied by another fixed constant, bounds the largest true displacement inside any single period. Under the Gaussian initial-momentum preparation,

\[
\Pr\{\sup_{t\leq Kp_*}|P(t)|>x\}
\leq C(K+1)\exp\left[-\frac{(x-CRa)_+^2}{CR}\right].
\tag{17}
\]

The feedback-controlled momentum need not have an unconditional Gaussian law. Bound (17) is obtained from the pathwise formula and a Gaussian maximum bound. A later controller record can correlate the current momentum and all earlier forces; that does not invalidate (15)--(17).

## 5. Two lanes and a dilute physical port

Take one such lane on each of two old conductors. Use opposite forces

\[
F_{1,k}=-a_Nu_k,\qquad F_{2,k}=a_Nu_k,
\qquad |u_k|\leq1.
\tag{18}
\]

Their corrected current difference has per-period drift

\[
-\nu_Nu_k,\qquad \nu_N=R_N\beta^2a_N,
\tag{19}
\]

and independent centered Gaussian innovation of variance \(2R_N\beta^2\). Their corrected current sum has zero control drift and the same innovation variance. The actual current sum differs only by the displayed momentum endpoints.

Over a physical observation interval of length \(TN^2\), if

\[
R_N/N\longrightarrow0,
\tag{20}
\]

the total empirical charge-density contribution on either ring is deterministically at most \(R_N/N\). This statement is valid at every time, with no assumption that the added carriers remain spatially uniform. Moreover the centered auxiliary sum, divided by \(N^2\), is superexponentially negligible at speed \(N\): for each \(\epsilon>0\),

\[
\limsup_{N\to\infty}\frac1N\log
\Pr\{\sup_{t\leq TN^2}|J_1(t)+J_2(t)|>\epsilon N^2\}
=-\infty,
\tag{21}
\]

provided \(R_Na_N=o(N^2)\). The Gaussian-martingale contribution has exponent of order \(N^2/R_N\); (17) controls the endpoint and intra-period terms. A bounded external force of order \(1/N\) applied to the added carriers contributes only \(O(R_NN)\) mean displacement on this horizon and is also negligible after division by \(N^2\).

For delayed feedback, the useful simultaneous regime is

\[
a_N\to0,\qquad R_Na_N\to\infty,
\qquad R_N/N\to0,
\qquad (R_Na_N)D_N=o(N^2),
\tag{22}
\]

where \(D_N\) is the maximum age of an implemented measurement in periods. An \(O(N)\) local communication delay is compatible with (22). For instance \(R_N=\lceil N^{2/3}\rceil\), \(a_N=N^{-1/3}\) is admissible. The delayed queue theorem is supplied separately; this file does not infer the whole physical path law from the endpoint identity alone.

## 6. Force work and preparation ledger

The actual force work in period \(k\) is **\(F_k\Delta J_k\)**. It is not \(F_k(\Delta J_k+\Delta P_k/g)\). Summing (13),

\[
\sum_{k=0}^{K-1}F_k\Delta J_k
=\sum_{k=0}^{K-1}\left[-\beta F_kY_k
 +\frac{R\beta^2}{2}F_k^2\right]
-\frac1g\sum_{k=0}^{K-1}F_k(P_{k+1}-P_k).
\tag{23}
\]

The first sum has expected value \((R\beta^2/2)\sum E F_k^2\), by the fresh-seed interface. The second is a real boundary/switching correlation term and must be retained. Its exact summation-by-parts form is

\[
\sum_{k=0}^{K-1}F_k(P_{k+1}-P_k)
=F_{K-1}P_K-F_0P_0
-\sum_{k=1}^{K-1}(F_k-F_{k-1})P_k.
\tag{24}
\]

For a force held over communication blocks, (24) involves only the block changes, not a change every microscopic step. No low-work conclusion is asserted without bounding those actual correlations. The mean-work optimization belongs to the separate feedback-governor comparison.

The operation uses \(R\) fresh standard-Gaussian coordinates each period, hence \(O(RN^2)\) input preparations over the diffusive horizon on each lane. It also requires their retirement, \(R\) local coupling units, initial aggregate momentum preparation, synchronized schedules, local current pickup, counter storage, communication and force actuation. Reusing the retired coordinates without a warranted preparation law changes (7). A bath at temperature one supplies the mathematical equilibrium distribution only if its actual preparation interface warrants that claim. No efficiency or practical speed advantage is established.

## 7. Predecessors and scope

Current-error feedback and freezing of long-time charge fluctuations already occur in Tobias Brandes, *Feedback Control of Quantum Transport*, Physical Review Letters **105**, 060602 (2010), [primary preprint](https://arxiv.org/pdf/1005.0018). Finite-window electronic feedback and strong shot-noise suppression were experimentally implemented by Wagner et al., *Strong suppression of shot noise in a feedback-controlled single-electron transistor*, Nature Nanotechnology **12**, 218--222 (2017), [primary preprint](https://arxiv.org/pdf/1602.05466). They are direct predecessors of the control objective, not evidence for this particular interacting mechanical supplier.

Thermal replacement operations have a long molecular-dynamics history; Andersen, *Molecular dynamics simulations at constant pressure and/or temperature*, Journal of Chemical Physics **72**, 2384 (1980), DOI [10.1063/1.439486](https://doi.org/10.1063/1.439486), is a conventional comparator. Here the exchange is explicitly spread over a finite physical interval while the carrier displacement continues to be counted.

The constructive content is the exact finite-period current/noise interface (12)--(14), retaining force-conserving unknown interactions, and its honest attachment to a dilute added **physical** port. The port is stronger than changing the metric of the original bath. It supplies actual additional charges, forces, local thermal coordinates and preparations. Any whole-path consequence must use the composite conductor as both the reference and the controlled physical task.
