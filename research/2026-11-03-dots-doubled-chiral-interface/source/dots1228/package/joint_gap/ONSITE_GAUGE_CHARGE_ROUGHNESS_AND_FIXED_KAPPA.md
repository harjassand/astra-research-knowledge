# Actual onsite gauge-charge roughness and the fixed-kappa boundary

2026-11-03. This is a physical-capacity audit, not a retraction of the proved finite-volume cutoff/device theorems.

## 1. The jump is present in the actual state, not inferred from floor notation

For the shared-rotor doubled base, the canonical ground has decoration scalar axial charge2S(phi), with declared K_1=K_2'=Σ n_pair having vacuum charge zero. Static compensation makes the two-copy free axial charge −2S(phi), up to the already fixed orientation/background convention. The sign is immaterial below; its change is nonzero.

The corrected disentangler maps input rotors u,theta to output phi_alpha=u_alpha+v_alpha theta, with a scalar cochain phase and a fermionic rotation acting ONLY on decorations. Therefore its inverse acting on the ground evaluates the free Gaussian factor at this output phi. Neither its scalar phase nor its decoration rotations can mix eigenspaces of the free axial number operator of a selected base.

There is an explicit actual cochain wall in cubic_move.npz: only phi_0 changes, from0.2174046792882161 to0.21742467928821613. S changes0 to−1. At the midpoint, exactly edge(0,1) changes its rounding integer, from1 to0. The next closest unrelated rounding wall is at distance0.00010478051542450739, so this is an isolated wall and persists on an open neighborhood of spectator coordinates. This is a positive-measure event, not an isolated fine-tuned configuration.

For the concrete anomaly-free stack v=(2,1), varying theta_0 moves this base's phi_0 across the wall. The second base generically has no wall at the same theta value because its independent u coordinates are unconstrained. Anomaly cancellation cancels the global cocycle, not these independent local wall events.

Across this wall the free axial eigenvalue of one doubled base changes by2. Consequently the two normalized one-sided full state vectors are orthogonal, even after D†. Their jump norm is sqrt(2). Canonical grading and the inverse-conjugate second decoration retain, rather than cancel, this free-charge difference. Even if one chose to inspect only a weighted total free charge, simultaneous cancellations of independent-base walls occur only on exceptional sets; the separate base free-charge sectors already prove orthogonality.

Thus a positive-measure collection of charged theta slices has a genuine nonzero vector jump. The on-sited canonical ground is not in the quadratic-form domain of J_theta,j². Its local gauge charge is J_theta,j plus bounded finite-fermion onsite charges and fixed offsets. Adding a bounded operator cannot repair failure to belong to the derivative form domain. The corresponding local gauge-charge second moment diverges.

## 2. Cutoff growth and what is proved quantitatively

For a period-one Hilbert-valued slice f(theta) that is piecewise C¹ with finitely many jumps Delta_a at distinct t_a,

 2pi i n f_hat(n)=sum_a Delta_a exp(−2pi i n t_a)+o(1).

The remainder tends to zero by the vector-valued Riemann–Lebesgue lemma applied to the integrable smooth derivative. Cesaro averaging removes cross terms at distinct jump locations. Therefore

 lim_(N→infinity) (1/N) sum_(0<|n|<=N) n²||f_hat(n)||²
    = (1/(2pi²)) sum_a ||Delta_a||².

The uniform slice-BV bound provides domination, so this identity integrates over spectator coordinates. A cutoff on the charged theta coordinate alone has kinetic expectation growing linearly with N, with strictly positive coefficient from the verified wall event. This is stronger than just saying the uncut variance is infinite.

For a simultaneous rectangular cutoff on every rotor, the above coefficient cannot simply be copied: the spectator cutoffs act on moving jump surfaces. Nevertheless the actual walls are rational affine hyperplanes with integer normal, including a nonzero theta component and a unit matter-rotor component. An integer unimodular coordinate change makes one such wall t=constant. A nonzero tangential Fourier coefficient of its jump field exists. Fixing that tangential frequency and letting the normal frequency grow gives a linear-in-N lower bound along an oblique sequence of modes contained in the original rectangular box. Other nonparallel walls contribute continuously after tangential integration; parallel-wall contributions have distinct locations and vanish in the same Cesaro cross terms. This proves positive linear lower growth for a fixed finite volume under the stated piecewise-smooth finite-wall structure. It does not supply a volume-uniform lower coefficient without further local quantitative bookkeeping. None of the earlier upper-tail bounds proves a bounded charge variance.

## 3. Consequence for electric energy

On a physical Gauss-law state, Q_j=sum_(incident links) sigma_e E_e. If z links meet j, Cauchy–Schwarz gives the quadratic-form inequality

 <Q_j²> <= z sum_(e incident j)<E_e²>.

Any gauge dressing preserving the canonical state's local charge distribution therefore has infinite electric energy when the electric Hamiltonian has a positive E² coefficient. A dressing that filters high charges can evade the conclusion only by changing that matter distribution; it is a new state/regulator whose fidelity, phase and dynamics must be earned. A finite momentum cutoff has finite charge capacity, but its canonical-ground electric cost increases with the cutoff. This rules out silently taking the uncut canonical state as a finite-electric-energy gauge vacuum.

Finite variance is necessary, not sufficient, for a finite thermodynamic Coulomb energy: infrared charge correlations and neutrality also matter. The present argument is an ultraviolet/local obstruction and does not settle that additional infrared problem.

## 4. Fixed kappa: what is positive and what remains missing

For any fixed finite volume, H_kappa=H_parent+kappa ΣJ², in the already onsite symmetry frame, is a legitimate positive closed-form Hamiltonian for kappa>0. It has finite thermal trace and finite charge variance. It respects the actual onsite gaugeable symmetry. The earlier Fourier trial theorem preserves the desired ground/gap when kappa is allowed to shrink with volume and accuracy.

At FIXED kappa, a zero-momentum rotor product trial and bounded local interaction density C give E0(H_kappa)<=CV. Positivity then implies

 (1/V) sum_j <J_j²>_ground <= C/kappa.

Thus fixed kappa does acquire a volume-independent average charge-capacity density. For a translation-invariant finite device/state this yields a per-site bound. It does not establish the old phase, a uniform interface gap, suitable infrared charge correlations, or a gauged continuum limit.

The one-site rank-one example is encouraging but insufficient. For H=I−|f><f|+kappa J², the unique eigenvalue E0<1 satisfies

 1=sum_n |f_hat(n)|²/(1+kappa n²−E0).

With a nonzero piecewise-smooth jump, E0 is of order sqrt(kappa), and rank-one interlacing gives gap>=1−E0. The regularized eigenvector is proportional to f_hat(n)/(1+kappa n²−E0), so it has finite J² expectation, typically of order kappa^(−1/2). This pays a local smoothing without a local gap collapse.

No valid extension of that interlacing argument to the ACTUAL interacting Gaussian-controlled, symmetry-averaged quasilocal parent has yet been proved. Its reset terms are not independent rank-one terms in physical gauge-charge coordinates. Ordinary bounded perturbation stability is inapplicable because kappa ΣJ² is unbounded and the old ground is not even in its form domain. Conjugating the kinetic operator into the product frame does not remove the issue; it creates the correlated discontinuous boundary conditions that must be analyzed.

Potential routes are a local boundary-layer/form estimate relative to an explicitly regularized product parent, or a new symmetric smooth/finite-capacity parent with a uniform gap proof. Local filtering can smooth a vector while preserving global symmetry, but without controlled inverse bounds and local parent stability it is not such a proof. A globally small finite-volume energy estimate, or an energy-density upper bound, also does not imply a thermodynamic spectral gap.

## Verdict
The actual charged canonical ground has an ultraviolet gauge-charge-capacity divergence, despite its bounded parent gap. Existing finite-volume finite-auxiliary and far-response results remain valid. Fixed-coupling admission to finite-electric-energy gauge physics needs an additional uniform-gapped regularization theorem. Fixed kappa solves finite capacity but has not yet been shown to retain the desired interacting interface phase. This is a specific open physical implementation gate, not a generic no-go for finite-error gauge regulators.
