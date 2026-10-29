# Supplier comparison: reciprocal line, chiral memory, and trusted current control

30 October 2026. Companion to `RECIPROCAL_WAVE_COUNTER.md`. This records the actual ordinary alternative and its limits, including failed constructions that changed the choice.

## 1. What the reciprocal supplier really grants

Order storage variables as `(x,q)` and energy-normalized momentum variables as `(v,p)`, retaining the native inertia tau separately. The conservative interconnection is the local matrix

\[
C_N=\begin{pmatrix}B&0\\ g_N I&-aB^*\end{pmatrix}.
\]

Storage flows are `C_N(v,p)` and the corresponding momentum forces are `-C_N^*(x,q)`. This is an explicit power-conserving reciprocal multiport relation: every force term has its transpose flow term. A local electrical transformer/junction or mechanical linkage must actually realize the relevant ratios. The dissipative native ports see v; the auxiliary pair dampers see `B^*p`, so their equal/opposite forces and matched noise are imposed by the connection, rather than by subtracting independently measured random numbers.

The selected native current is v, and the force input f acts in its actual momentum equation with work `f^T v`. A device with only noninvasive labels and a reversible native operation does not automatically offer this continuous reciprocal load port. Conversely, when this port is supplied, an ordinary passive network may attach the auxiliary storage and line without knowing each R numerically.

The declared model retains native inertia and has bounded local matrices. It provides finite response and an integrable high-frequency current spectrum. It does not certify an exact hard band limit, perfect reactive elements, an actual mechanical design, or a fabricated netlist. In particular, a real transformer may have a low-frequency cutoff; its static ideal ratio cannot be assumed valid on arbitrarily long N^2 horizons. Component compliance, parasitic modes, ratio accuracy and initialization all remain in the supplier budget.

## 2. Why the reciprocal line changes the mathematical selection

For chiral first-order memory with symbol proportional to ik, the feedback correction at a density mode k scales like `kappa/k`; preserving nonflat heat required a restrictive tap window in the candidate root construction. The reciprocal q,p line instead has load

\[
Z_{\rm aux}(\lambda,k)
=\kappa\frac{\lambda+\gamma\ell}
{\lambda^2+\gamma\ell\lambda+a^2\ell},\qquad \ell\sim k^2.
\]

At a diffusive density pole `lambda=O(ell)`, this is O(kappa), uniformly for bounded conservative gamma. It therefore retains the density response for every `kappa_N -> 0`; current suppression separately requires `kappa_N N^2 -> infinity`. The complete proof controls all other modes through the exact slow projection and energy contraction. It does not merely insert the slow root into a formal dispersion relation.

This permits slowly weakening taps such as `kappa_N=1/log(N+1)` at fixed local conservative loss and finite response. Neither chirality nor repeated externally clocked swaps are needed for the homogeneous Gaussian task. The main proof also gives the nonflat density path law and the zero-harmonic-current Gaussian action, not only an equilibrium CLT.

This is an ordinary passive comparison. It does not make the basic field operation novel. The larger research question is what topology-conditioned transport law this kind of local apparatus can realize under the actual native kinetic interface.

## 3. Loss channels are physically different

The positive auxiliary bath is

\[
-B\Gamma B^*p\,dt+\sqrt2 B\sqrt\Gamma\,dV.
\]

It can have fixed bounded coefficients. Each local pair exchanges momentum and preserves its sum. This is an actual structural conservation law, as with a pair viscous interaction; it is not the same as independent damping to a stationary substrate.

Independent grounded p damping produces a different long-wave impedance and a slow density rate `a^2 ell^2/(kappa gamma)`. It controls current while damaging nonflat relaxation. A supplier using such loss needs `kappa gamma_N N^2 -> 0` in addition to `kappa N^2 -> infinity`; fixed positive loss does not qualify. Calling an arbitrary lossy transmission line conservative would therefore remove a load-bearing condition.

A leak from q to an independent reservoir is worse in a different way: it changes the exact native-current counter itself. Its noise and cumulative transport must be counted. Neither finite response nor passivity alone guarantees the desired low-frequency topology.

## 4. Gain error and the output it actually controls

Suppose the actual reciprocal native taps are `g_i=g(1+h_i)`, while auxiliary transport still preserves the unweighted sum q. Then the exact counter controls the weighted current `sum_i(1+h_i)J_i`, not the requested unweighted total.

Let `bar h=N^(-1)sum h_i` and solve `B^*phi=h-bar h 1`. Exact native continuity gives

\[
(1+\bar h)J_{\rm tot}(t)
=g^{-1}\sum_i[q_i(t)-q_i(0)]
-\langle\phi,x(t)-x(0)\rangle.                              \tag{1}
\]

At the canonical Gaussian law, with the actual reciprocal taps preserving that law, the variance is bounded by a constant times

\[
\frac{N/\kappa+\|\phi\|^2}{(1+\bar h)^2}.                    \tag{2}
\]

Thus common gain error only changes a scale. Spatially coherent error can change the macroscopic rare-current objective: a fixed smooth error profile has `||phi||^2` of order N^3, leaving an ordinary speed-N tail. Uniform worst-case relative errors tending to zero are sufficient to remove that floor, but a fixed error radius is not an exact asymptotic zero-current certificate. The actual low-wave-number/cohomology error is the relevant quantity, not only a single scalar calibration number.

A charge-conserving hardware representation can instead use actual displacement-unit storage z with `dz=dJ-div(auxiliary flux)` exactly, while local stiffnesses vary. Then total native current is an endpoint for the actual physical z regardless of the numerical stiffness. After energy normalization, both the native and auxiliary couplings change together. That is a different, structurally matched port and may be preferable to independently calibrated taps. The homogeneous normalized theorem does not silently grant this matching to an arbitrary fabricated array.

## 5. Stronger additive-current control is a different supplier

If a trusted additional port can add an arbitrary common current `u(t)1` directly to every native branch, then `B1=0` makes the entire density path unchanged, even for heterogeneous kinetics. Feedback can then act only on circulation. This is stronger than a reciprocal force port: a force is multiplied by the unknown mobility, whereas a prescribed additive current is not.

With finite propagation time, a common command could be buffered and applied synchronously after a delay of order N. A stable circulation feedback with gain of order 1/N would then have a time scale much shorter than N^2 while remaining slower than the communication delay by an appropriate constant factor. This is an ordinary control opportunity **if** the additive sources, a trusted cumulative-current record, the common command timing and their noise budgets are supplied. It is not a completed apparatus or a free fallback at the passive port.

In particular, integrating noisy instantaneous current measurements creates a random-walk counting error. Fixed low-frequency sensor noise can restore an ordinary circulation tail even when the measured feedback variable is well controlled. Likewise imperfectly synchronized branch injections need not be divergence-free. These errors cannot be discarded because the controller is conventional. The passive wave counter avoids this sensing record by storing the actual current through its reciprocal dynamics, at its own topology and loss conditions.

For unknown heterogeneous native mobility D, the passive force route implements the weighted projection `D-D11^TD/(1^TD1)`. The algebraic `PDP` route preserves density but requires a different current-shaping operation. An actual trusted additive-current supplier could defeat a broader novelty claim; it is not supplied by equilibrium or reciprocity alone.

The conditioned-history wording must also be precise. The positive line result imposes zero harmonic integrated current at **every macroscopic time**, equivalently `int j(t,x)dx=0` almost everywhere in a finite-action history. Conditioning only the terminal integrated current, or a long-time average current to its typical value zero, is a different ensemble and can retain substantial intermediate circulation. No generic equivalence with that weaker conditioning is claimed.

## 6. Earlier independent attempts retained

The first inertial attempt used a fixed-strength counter tap. It did remove frozen local memory and restore an N^2 two-field relaxation, but its density receiver generally contained two damped long-wave modes rather than ordinary heat. Allowing the tap to weaken, and controlling the visible slow projection rather than discarding the auxiliary mode by name, produced the current positive result.

A local static cut is an even simpler ordinary way to eliminate a winding channel while leaving diffusive relaxation on a connected path. It changes the periodic boundary task and does not preserve the ring's heat/current receiver; it cannot be used as a same-task comparison without declaring that change.

A two-rail sequence of finite local swaps can transport memory ballistically, but introduces actual clock, gate-noise and routing premises. The reciprocal autonomous line renders that route unnecessary for the present homogeneous Gaussian target. No perfect memory-swap primitive was imported into the final theorem.

## 7. Primary predecessor record

* Freitas, Delvenne and Esposito, *Stochastic and Quantum Thermodynamics of Driven RLC Networks*, PRX 10, 031005 (2020), [arXiv:1906.11233](https://arxiv.org/abs/1906.11233). The actual paper was read, including the charge/flux network equations, conservative versus dissipative blocks, physical time reversal, Johnson--Nyquist sources and the need for high-frequency regularization when computing heat. These are direct predecessors for the supplier mathematics.
* Nyquist, *Thermal Agitation of Electric Charge in Conductors*, Phys. Rev. 32, 110 (1928), [DOI 10.1103/PhysRev.32.110](https://doi.org/10.1103/PhysRev.32.110). Its thermal-noise/impedance principle is the conventional basis of the passive spectrum bound. The current calculation is not a new fluctuation-dissipation theorem.
* Lelièvre, Rousset and Stoltz, *Langevin dynamics with constraints and computation of free energy differences*, [arXiv:1006.4914](https://arxiv.org/abs/1006.4914). The actual introductory constrained dynamics, mass-metric projector (1.7), and projected fluctuation-dissipation pair (1.16) were read. They are direct predecessors for metric-dependent constraints and matched noise. A prescribed global algebraic constraint is not itself a supplied local finite-response wave apparatus.
* Chetrite and Touchette, *Nonequilibrium Markov processes conditioned on large deviations*, [arXiv:1405.5157](https://arxiv.org/abs/1405.5157), Ann. Henri Poincaré 16, 2005 (2015). The actual conditioning definitions, bridge distinction and driven diffusion formula (116) were inspected. They preclude a broad claim to inventing physical/dynamical representatives of conditioned path ensembles. Their standard driven diffusion retains its original microscopic noise while changing drift; the whole-time harmonic constraint and local apparatus supplied here are separately stated objectives.
* Viola and DiVincenzo, *Hall Effect Gyrators and Circulators*, PRX 4, 021019 (2014), [arXiv:1312.5190](https://arxiv.org/abs/1312.5190), was located as an actual nonreciprocal supplier comparison. The accessible abstract reports finite-frequency device proposals and losses; the full PDF fetch failed in this session. No component guarantee or detailed theorem is borrowed from it. The final construction does not need a gyrator.
* The saved round-eight `PRIMARY_CONSTRUCTION_COMPARISON.md` retains dipole-conserving, paired-current, current-gauge, common-clock and tight-coupling predecessors. The new reciprocal phase-space supplier does not erase those comparisons or turn the harmonic Gaussian calculation into an exclusion result.

Priority for a new LC principle is not claimed. This is a useful ordinary architecture and a precise resource comparison; the broader nonlinear/topological capability remains root's separate constructive question.
