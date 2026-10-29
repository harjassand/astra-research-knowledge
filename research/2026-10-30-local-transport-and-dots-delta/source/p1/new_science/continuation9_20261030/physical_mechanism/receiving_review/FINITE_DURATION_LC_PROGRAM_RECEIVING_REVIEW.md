# Receiving review: the finite-duration local LC program

30 October 2026. Reviewer: the existing physical-mechanism role. This is an actual-file mathematical and physical-interface review; it is not a priority, apparatus, acquisition, or numerical-precision acceptance.

## Reviewed input and decision

Reviewed source: `record_geometry/FINITE_DURATION_LC_PROGRAM.md`.

SHA256: `49acbebb439b5eaa2305ee273239101316261d4875be45015f188f8a744b8cf2`.

An exact 23,374-byte snapshot is preserved as `FINITE_DURATION_LC_PROGRAM_REVIEWED_49acbebb439b.md`, alongside `FINITE_DURATION_REVIEW_INPUT.json`. Both source and snapshot were hashed during this review and agree. The accompanying `check_finite_pulse_lc.py` was read, but no new fixture was created and the existing checker was not rerun: the issues below are analytic and the source already records its executed population checks.

**Decision: accept the stated homogeneous, Gaussian, explicitly gated finite-duration supplier and its density/native-current path receiver.** I found no mathematical correction required. The conclusion requires the complete operation and conditional initialization specified in the source. It does not establish a white-noise-free implementation of an arbitrary pre-existing hidden resistor, a finite-amplitude apparatus, or robustness to unmodeled port leakage or schedule error.

For a concrete joint topology, the proof works in

\[
C([0,T],H^{-s})\times C([0,T],H^{-s}),\qquad s>3/2,
\]

for density and integrated native current respectively. A stronger topology is unnecessary for the asserted action. The source calls the current topology a weak Sobolev path topology; the displayed choice makes the receiving scope explicit.

## 1. The Schur cell coefficient is correct

Put \(\gamma=g/\sqrt\tau\), \(\theta=\gamma h\), and freeze the slow coordinates \((x,p)\) to their order-zero values. With \(F_q=-a\beta p\), \(F_u=-\beta x/\sqrt\tau\), the forced rotation is

\[
q'=\gamma u+F_q,\qquad u'=-\gamma q+F_u.
\]

Write \(A=q(0)-F_u/\gamma\). Since \(u(0)=0\), periodicity of the retained fast coordinate gives

\[
(1-\cos\theta)A=(F_q/\gamma)\sin\theta,
\quad
A=(F_q/\gamma)\cot(\theta/2).
\]

It follows exactly that \(u(h)=-2F_q/\gamma\). Integrating the two differential equations then gives

\[
\int_0^h u\,dt=-F_qh/\gamma,
\qquad
\int_0^h q\,dt=F_uh/\gamma+2F_q/\gamma^2.
\]

Thus the order-\(\beta^2\) slow increment is precisely

\[
M_g=\begin{pmatrix}0&ah/g\\-ah/g&-2a^2\tau/g^2\end{pmatrix}.
\]

This calculation includes the periodic fast-coordinate response. Replacing that response with a freshly zeroed q would give a different coefficient. The two eigenvalues of \(M_g\) are \(-D_\pm(g)\) as stated, and \(D_-(g)\to h^2/(2\tau)\). Dividing by the full physical period \(h+b\) is essential and correctly produces the stated diffusivity. The bath duration is not omitted.

## 2. The singular-looking remainder has a uniform regime

The argument does not require a uniform spectral gap at \(g=0\). For fixed h,a,tau, the matrix exponential and its beta derivatives are bounded on a compact small-beta, small-g set. The stated parity of the blocks follows by changing the signs of x,p when beta changes sign. In the indicated eigenvalue disk, the q resolvent is bounded by \(C/g^2\), because its order-zero gap is \(1-\cos\theta\asymp g^2\).

After eliminating q and dividing by \(\beta^2\), the remainder is bounded by \(C\beta^2/g^6\). The potentially largest contribution is the change of the q resolvent when \(\lambda-1=O(\beta^2/g^2)\); multiplication by the two off-diagonal beta factors gives the quoted power. The two eigenvalues of \(M_g\) are separated by order \(g^{-2}\), with a uniformly conditioned eigenbasis whose columns approach the coordinate axes. Dependence of the remainder on lambda is harmless under \(|\beta|\le c g^8\). A two-root perturbation or Rouché argument therefore isolates the real density eigenvalue; the published \(O(\beta^4g^{-12})\) bound is looser than needed.

Back substitution bounds q by \(C|\beta|/g^2\), while the slow-vector change is bounded by \(C\beta^2/g^4\). These imply the stated, deliberately weaker eigenvector estimate. Momentum reversal gives the left eigenvector \(\Theta w/(w^*\Theta w)\), with denominator bounded away from zero. Because C is a contraction, the left and right small residuals multiply to bound every omitted power uniformly in n. No decay estimate for the remaining auxiliary eigenvalues is silently used.

For each fixed continuum Fourier label, \(\beta=O(N^{-1})\) and \(g_N^2=1/\log(N+1)\). Thus the required beta-versus-g condition eventually holds, every inverse power of g is dominated by N, and the eigenvalue error multiplied by \(N^2\) vanishes. The conclusion is a fixed-macroscopic-mode receiver, not a uniform approximation of every microscopic Fourier mode.

## 3. Initialization and covariance are correctly distinguished

The retained chain obeys \(S_{n+1}=CS_n+f\xi_n\), with independent Gaussian \(\xi_n\) and \(CC^*+ff^*=I\). Its stationary covariance is I. Conditioning only the initial visible x subtracts the rank-one initial-x covariance contribution and gives source equation (23). Conditioning all initial retained coordinates gives equation (24). The latter has the same limit because both density eigenvectors approach the x coordinate and C remains a contraction.

Conditioning a finite-dimensional Gaussian on a specified deterministic value is a legitimate covariance calculation even though the corresponding singleton has zero equilibrium probability. It is not a physical preparation claim. The actual initializer is separately and explicitly supplied. Independent thermal q,p,v, or the declared zero q,p initializer with a fresh velocity draw, are material hypotheses. An arbitrary microscopic calibration record would not leave those laws unchanged.

The mean and covariance limits determine finite-dimensional laws here because the entire deterministic-schedule process is Gaussian. The source correctly declines to transfer this conclusion to a Poisson-reset process, whose multi-time distribution is a Gaussian mixture.

## 4. The path and rare-event step closes the covariance-only gap

At cycle starts, the left density eigen-observable has increment variance proportional to \(1-\lambda_s^r\). The residual observable has variance bounded by its squared norm. This gives the source's vanishing-floor modulus bound. It is not a finite-N Kolmogorov estimate, but it is sufficient for the speed-N exponential modulus: a density increment of fixed size corresponds to a centered fluctuation increment of order \(\sqrt N\), while the polynomial number of time pairs contributes only \(O(\log N)/N\) to the normalized log probability. The floor tends to zero before the time-mesh limit.

Within a transport segment, the fixed Fourier density changes by beta times a bounded-norm four-coordinate linear map. The supremum is controlled by a finite Gaussian coordinate norm; the bath leaves x fixed. This supplies the missing interpolation estimate without a hidden microscopic grid or a white-noise approximation.

The high-mode argument also works. The total energy norm of each Fourier block is preserved during transport, and the body covariance is bounded by I after conditioning. Weighted Gaussian norm tails therefore control the entire segment from its starting coordinates. Discrete Fourier alias weights obey the claimed bounds for s greater than one half. At fixed cutoff K the expected empirical tail norm tends to zero; the largest tail covariance eigenvalue is at most \(C K^{-2s}/N\). A union over order \(N^2\) segments preserves the speed-N bound. The deterministic mean tail is controlled by the energy bound.

Together these facts give exponential tightness and exponentially good finite-mode/time-grid approximation. The finite-dimensional normalized log moment-generating functions converge exactly because their covariance matrices converge. The resulting quadratic projective rate is the Cameron--Martin image of the heat equation with zero initial fluctuation. It includes all finite-energy weak controlled solutions, not only smooth histories. No inference from a fixed total-variation error or from typical trajectories enters this step.

## 5. All native displacement is counted, and the current constraint is a path constraint

During transport, \(d\sum q=g\,dJ_{\rm tot}\). During the isolated bath, both quantities are fixed. Consequently the exact counter is valid for the actual gated current. Integrating the velocity state through the closed bath port would be wrong; the source explicitly excludes that operation.

The zero Fourier mode of q and u undergoes a bounded rotation in every transport stage. Under either stated initializer its centered covariance is bounded by the equilibrium covariance, and its mean harmonic current is zero. A Gaussian bound followed by a union over the physical stages gives the displayed \(\exp[-c\epsilon^2g^2N^3]\) estimate. With the chosen g, this is superexponential at speed N. It controls the complete macroscopic time interval, not just the final endpoint.

For nonzero resolved modes, exact continuity determines the integrated current. The discrete inverse multiplier is uniformly bounded by \(C/|m|\). In the joint topology specified above, high-mode exponential approximation and fixed-mode multiplier convergence suffice, including alias replicas. The constant current mode is removed by the superexponential estimate. The rate is therefore the ordinary constant-mobility quadratic action restricted to zero instantaneous harmonic current. Contracting over that current leaves precisely the ordinary heat density action, since the density gradient has zero spatial average. This statement would fail for a general heterogeneous current metric, and the source correctly does not claim it.

## 6. Physical supplier and two interpretation details

The result earns a genuinely different noise interface, at substantial supplied cost: order \(N^3\) fresh scalar Gaussian reservoir preparations over a diffusive horizon, deterministic local rotations, isolation, synchronized phase, and retirement or paid rethermalization of used coordinates. It has bounded local coefficients and finite-duration operations. It does not have a hard amplitude cap, an exact hard frequency cutoff, or a general unknown-kinetics implementation. The source says so explicitly.

The smooth-envelope sentence is valid with its literal Hamiltonian interpretation: a common envelope c(t) scales the entire transport generator, h is its integrated duration, and the measured native current in that segment is **c(t)v(t)**. One cannot keep \(dJ=vdt\) while scaling \(dx=Bvdt\) to \(dx=c(t)Bvdt\). This is an interpretation detail of the optional envelope replacement, not a defect of the fully specified piecewise program.

The old-record premise must apply to the complete actual conditional initializer and future independent reservoir laws. Exposing the new reservoir coordinates, retired velocities, or an apparatus microstate does not automatically preserve a conditional version of the stated action. Likewise a fixed probability of calibration failure or saturation cannot be discarded at speed N. These boundaries are correctly retained.

## Final scope

Accepted: an exact declared finite-duration Gaussian program; its low-wave-number heat receiver including the full elapsed time; Gaussian density-path LDP; and whole-path elimination of harmonic native current in the same joint action.

Not supplied by this acceptance: an apparatus, a free isolation capability, a hidden-rate-blind implementation from the predecessor reversible operation menu alone, robustness to fixed unmodeled faults, or novelty of LC dynamics, Gaussian refreshing, or Hamiltonian splitting. The new receiver is supported by the exact cell analysis and path estimates rather than by those generic precedents.
