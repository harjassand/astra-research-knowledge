# Adversarial delta audit: thermal transition certificate

Status: independently reconstructed analytic review of the copied certificate, not a formal proof or physical validation. The final audited target snapshot is SHA-256 `bc0c8c73a7ed62161c27842d6bfdcdc26c8b70f3e13be60a536896d293402dcb`. The certificate changed once during this audit: only its §8 comparator attribution paragraph changed, and both the original and current snapshots are preserved under `input/`. The audit used no files from `work/FK-root` other than the target note; root's numerical checker and result JSON were not read. The first frozen audit at `work/FK-anchor-audit/` was left untouched.

## Decision

I found no counterexample to the finite-resolution mean bound, the clipping inequality, the sector-weight example, or the compact-Euclidean signed-measure obstruction under their stated mathematical premises. The main contract is conditional and must stay that way. The adversarial corrections are about scope and definitions: energy-readout noise must be genuinely nondemolition at the level of each Kraus operator; total variation must use the probability-distance convention; an unbounded observable is a separate infinite-dimensional extension with trace/moment hypotheses; and local detailed balance does not certify canonical sector weights. None of these findings shows that the transition estimator is biased for its actual input state when the balance relation holds.

## 1. Finite-resolution, nondemolition readout

The deterministic resolution term is sound. For

\[
k(d)=\frac{2d\tanh(\beta d/2)}{d^2+\eta^2},\qquad d\ge0,
\]

direct differentiation gives

\[
k'(d)=\frac{2\tanh(\beta d/2)(\eta^2-d^2)}{(d^2+\eta^2)^2}
 +\frac{\beta d\,\mathrm{sech}^2(\beta d/2)}{d^2+\eta^2}.
\]

Writing \(x=\beta d/2\), the first term is bounded by
\(\beta d/(d^2+\eta^2)\), and the second by the same quantity, so
\(|k'|\le\beta/\eta\). Separately, the first term is at most
\(2/(d^2+\eta^2)\); \(x\operatorname{sech}^2x\le1/2\) bounds the second
by \(1/(d^2+\eta^2)\). Thus \(\mathrm{Lip}(k)\le
\min(\beta/\eta,3/\eta^2)\). At \(d=0\), the continuous derivative is zero.
The two recorded energies each within \(\zeta\) imply a magnitude-gap error
at most \(2\zeta\), hence the stated \(2a^2L\zeta\) output bias. The
computed output is already in \([0,B]\) for every finite nonnegative
reported gap; clipping also handles invalid/out-of-range records if those
are mapped to any value in \([0,B]\).

The no-minimum-level-spacing premise is mathematically consistent. If every
refined Kraus operator is a Borel function of \(H\), the instrument preserves
each exact energy sector. Starting from Gibbs, the state conditioned on an
initial record remains proportional to the identity in each degenerate
energy eigenspace. Applying \(A/a\) then gives the latent transition law
weighted by the first per-energy record kernel; the final energy-preserving
readout applies the second kernel. This gives the ideal \(q(n,m)\) coupled to
the two classical readouts, without resolving close eigenvalues. The two
per-record failure probabilities give a bad-pair probability at most
\(2\kappa\) by the union bound, whether or not readout errors are correlated
with each other. Since both folded outputs lie in \([0,B]\), that term is
\(2B\kappa\). The argument does not apply to arbitrary instruments merely
described as "approximately nondemolition": each refined Kraus operator
(not only the sum channel or POVM effect) must be a scalar function of
\(H\), and the record kernels must not induce outcome-dependent dynamics
outside the contract. Mere commutation \([K_j,H]=0\) is insufficient in
degenerate subspaces. An exact three-level check in
`checks/exact_delta_checks.py` exhibits \(H=\operatorname{diag}(0,0,1)\),
Gibbs populations \((2/5,2/5,1/5)\) at \(\beta=\log2\), and
energy-preserving Kraus operators \(K_0=\operatorname{diag}(1,0,1)\),
\(K_1=|0a\rangle\langle0b|\). They form a trace-preserving channel and
commute with \(H\), but reweight the ground eigenspace to \((4/5,0)\). For
\(A=|0a\rangle\langle1|+|1\rangle\langle0a|\), the upward/downward
transition ratio changes from \(1/2\) to \(1/4\), and the folded mean
changes from the canonical \(1/5\) to \(1/3\). This does not break the
certificate's stated function-of-\(H\) condition; it shows why that
condition must not be weakened to a generic energy-commuting instrument.

The robustness inequality follows by a triangle/coupling argument. With
probability one minus the bad-label event, the output error is at most
\(2a^2L\zeta\); on the bad event it is at most \(B\). A bounded output
changes expectation by at most \(B\delta\) under quantum trace distance
\(\delta=\tfrac12\|\rho-\tilde\rho\|_1\), and by at most \(B\gamma\)
under classical total variation distance. Adding these terms gives exactly
the displayed certificate. Independent (or otherwise explicitly
concentration-controlled) trials are still required for Hoeffding.

Two definition fixes should accompany the formula:

* Define classical TV as \(d_{TV}(P,Q)=\sup_E|P(E)-Q(E)|=\frac12\|P-Q\|_1\).
  If \(\gamma\) instead denotes the unhalved \(L^1\) difference, its
  contribution is \(B\gamma/2\), not \(B\gamma\). "Trace distance" usually
  already means the half-trace-norm convention.
* Say whether \(\gamma\) compares the full classical outcome channel after
  readout or only the transition instrument before the separately modelled
  readout kernels. If it already includes the readout, adding \(2\kappa\)
  is redundant but remains a valid looser bound. If it excludes readout,
  the triangle bound has the stated interpretation.

The resolution statement is not an implementation theorem. A coarse
function-of-\(H\) measurement may avoid any minimum-spacing requirement, but
its synthesis, Hamiltonian access, runtime, calibration, and Gibbs
preparation are not bounded here. At fixed \(\beta,a\) and small \(\eta\)
(in particular \(\beta\eta\le3\)), the stated Lipschitz constant takes the
branch \(L=\beta/\eta\); achieving resolution bias at most
\(\epsilon_{res}\) then requires
\(\zeta\le\epsilon_{res}\eta/(2a^2\beta)\). Thus the contract avoids a
minimum-eigenvalue-spacing promise but does not give uniform-in-\(\eta\)
precision or operation cost. A fixed common drift across trials would
also invalidate the independent-trial Hoeffding premise unless the bound is
proved conditionally for the realized device or a dependence-aware
concentration result is supplied.

## 2. Unbounded-observable clipping

The displayed inequality is correct as a quadratic-form argument. For a
Hermitian \(B\), write the regular response as

\[
Q(B,B)=\sum_{E_m>E_n}
 \frac{2d(p_n-p_m)}{d^2+\eta^2}|B_{nm}|^2.
\]

The coefficient is nonnegative. Since
\(2d/(d^2+\eta^2)\le2/d\) and
\((p_n-p_m)/d\le\beta(p_n+p_m)/2\),
\(Q(B,B)\le\beta\operatorname{Tr}(\rho B^2)\). Polarization and
Cauchy--Schwarz for this positive semidefinite form yield

\[
|Q(A,A)-Q(A_L,A_L)|
\le \sqrt{Q(A-A_L,A-A_L)Q(A+A_L,A+A_L)}.
\]

Spectral clipping gives \(A_L^2\le A^2\) and
\((A-A_L)^2\le A^4/L^2\) by scalar functional calculus. Thus
\(\|A_L\|_{\rho,2}\le\sqrt{M_2}\),
\(\|A-A_L\|_{\rho,2}\le\sqrt{M_4}/L\), and
\(\|A+A_L\|_{\rho,2}\le2\sqrt{M_2}\), proving
\(2\beta\sqrt{M_2M_4}/L\). The finite exact two-level fixture in
`checks/exact_delta_checks.py` checks a nonzero clipping error against this
bound.

This is not literally a corollary for an unbounded \(A\) of the
finite-dimensional §1 statement, where every operator is bounded. To use it
for an oscillator or other infinite-dimensional source, state the extension
premises explicitly: self-adjoint \(H\) bounded below with
\(Z=\operatorname{Tr}e^{-\beta H}<\infty\), self-adjoint \(A\) with the
needed spectral products defined and \(M_4<\infty\), and the regular Lehmann
response defined by the convergent positive form (or a proved limiting
construction). These conditions make the finite-temperature Gibbs operator
trace-class; nonnegative-sum monotone limits then support the coefficient
bound. For infinite-volume/continuum thermal states without a trace-class
Gibbs density, replace traces by a specified finite-volume or per-volume
form and prove bounds uniform in volume. Finite \(M_2,M_4\) at each volume
does not by itself give a uniform tail as volume grows. The note correctly
declines a thermodynamic-limit claim, but the source oscillator example
should be labelled as an application of this separate extension rather than
the finite-dimensional theorem itself.

Finally, the tail lemma does not supply the clipping operation. One must
implement a bounded filter for \(A_L\) with known scale (for example
\(a_L=L\)), acquire or certify \(M_2,M_4\), and pay the growing range and
trial cost. This is consistent with the note's stated caveat.

## 3. Sector weights and unusual sources

The two-block example is an exact counterexample to inferring canonical
sector mass from detailed balance on the observed transition graph. Take
\(\beta=\log2\), within-block gap \(1\), \(\eta=1\),
\(D=\log3/\log2\), \(c=1/2\), and source sector mass \(w=1/2\). The
canonical first-sector mass is \(w_*=3/4\), while the source's transition
rates have \(q(-1)/q(+1)=1/2=e^{-\beta}\). The exact folded mean is
\(5/24\) for the source and the canonical target is \(13/48\), a difference
of \(1/16\). The check computes these rational values directly.

The limitation is precise: local detailed balance across each observed
\(A\)-edge constrains ratios within connected components of the transition
graph, but leaves a normalization per disconnected component. A state
canonical within each component can therefore be stationary and pass every
edge-balance check while having the wrong canonical global component masses.
The theorem's exact Gibbs premise excludes this source. On such a source the
folded mean still estimates its source-weighted regular spectral sum when
the same edge-balance relation holds; what fails is identifying that number
with the *canonical Gibbs* target. If \(A\) and its known sector amplitudes
make raw success/failure frequencies informative about \(w\), those
frequencies can be used as extra information, as the certificate notes.
Thus this is not a counterexample to the estimator under its Gibbs contract
and not a claim that all transition data are uninformative.

This matches the relevant capital distinction: the N788 dossier requires an
actual loaded Gibbs histogram and leaves its acquisition open; the separate
fixed-charge/local-stationarity countermodel in
`PREPARATION_OBSTRUCTION.md` changes the ensemble by trapping a hidden bath
sector. Those capital claims are scoped access statements, not a new premise
for this estimator, and neither broadens the root certificate to arbitrary
stationary sources.

## 4. Compact Euclidean signed-measure obstruction

For fixed \(\beta>0\), if \(\mu\) is a finite signed (or complex) measure
on \([0,\beta]\), then

\[
F(z)=\int_0^\beta(e^{-\tau z}+e^{-(\beta-\tau)z})\,d\mu(\tau)
\]

is entire: compact support bounds the integrand and all derivatives on
compact subsets of the complex plane. A universal representation of the
Euclidean kernel target would imply, for all real \(d>0\),

\[
F(d)=(1-e^{-\beta d})\frac{2d}{d^2+\eta^2}.
\]

By analytic continuation, the meromorphic right side must have no
nonremovable poles. Its residues at \(z=i\eta\) and \(z=-i\eta\) are
\(1-e^{-i\beta\eta}\) and \(1-e^{i\beta\eta}\); both vanish exactly when
\(\beta\eta\in2\pi\mathbb Z\). Outside that Matsubara set this contradicts
entirety. At \(\eta=2\pi k/\beta\), the real signed measure
\(\cos(2\pi k\tau/\beta)\,d\tau\) does give the target; the exact
functional identity is checked in the script.

For a nonzero positive finite measure, the Euclidean kernel is uniformly
\(2/(\beta d)+O(1)\) as \(d\downarrow0\), so its integral diverges with
positive leading coefficient, whereas \(2d/(d^2+\eta^2)\to0\). Signed
measures can cancel the leading term, so the analytic-pole argument is the
decisive signed obstruction.

This no-go needs a single measure independent of \(d\), equality for every
positive gap, and bounded linear functionals on \(C([0,\beta])\) (equivalent
to finite regular measures by Riesz--Markov). It does not exclude finite
approximation on a restricted gap interval, nonlinear or data-dependent
rules, extra spectral information, or unbounded functionals that use
derivatives/noise-sensitive norms. It also does not say a nonlinear
estimator avoids the corresponding acquisition or stability costs.

## Scope and reproducibility

The exact script is independent of the root checker. It confirms the sector
weights and folded means, tests one finite clipping case, and verifies the
Matsubara Fourier identity. Those checks do not establish the universal
operator inequalities; their proofs are given above. No numerical scan is
used as proof of a global Lipschitz or infinite-dimensional statement.

The cited comparator papers in §8 of the target note were not opened during
this delta audit. In particular, the updated Sun/QPE attribution sentence is
recorded but not independently verified here. No historical-priority or
literature-completeness claim is made. The prior frozen audit remains
preserved and unmodified.
