# Actual longitudinal barrier gate: projection failure and repaired return

Working correction, 31 October 2026. Only new measurement-branch files
were written. The physical Hamiltonian is exactly the root's real
two-electron longitudinal finite-grid model: fixed strong double-well
confinement, transverse-Gaussian-averaged Coulomb, and a Gaussian barrier
control of width .20. The dimensionless mass remains d/a_B*=2.842462961.
No old ideal four-charge-state pulse was substituted for this model.

## 1. The previous small projected fit fails

The old40-dimensional space used low eigenspaces at barrier heights0 and
204. Its fitted height217.739275457, rise4, hold27.019376832 gave an
apparent isometry error .000848. Direct root propagation instead found
error about .873 and leakage about .766.

A new120-dimensional space uses24 actual low eigenvectors at each of
0,100,180,217.739275457,230. It predicts error .872669 and leakage .765545
for the old pulse. Its full-grid Galerkin residual integral is .01510,
so it also exposes the old projection failure without the expensive
full-cycle direct propagator. A40-dimensional optimizer residual was
not a physical gate error.

## 2. A repaired pulse in the same real potential

The new space found the following useful candidate:

\[
 b=203.7579951119,\quad T_{rise}=T_{fall}=4,
 \quad T_{hold}=19.7175608151.
\]

The barrier envelope uses the same quintic10u^3-15u^4+6u^5 on both
ramps. Total duration is27.7175608151 hbar d/K. Maximum barrier slew is
about95.51156 in the corresponding energy/time units. These finite
controls retain the fixed base potential and the full longitudinal
Coulomb interaction.

A200-dimensional independent space, with40 vectors per sampled height,
predicts error .00132295 at the nearby original fitted hold19.7179077024.
Its conservative Galerkin defect integral remains .0108122. This loose
bound is not an obstruction: the direct finite-grid calculation below
determines the actual error much more sharply.

The direct check integrates the up-ramp on the complete112^2 spatial grid
with no Galerkin projection. It then uses true eigenvectors of the actual
active Hamiltonian and exact real-Hamiltonian transpose reciprocity for
the down-ramp. The48-mode active projection leaves up-state tail norm
3.80e-8; its eigen residual is about4e-12. The numerical full-grid return
has isometry error .0013222134 and code-band leakage .0013181434.

This is a useful finite-model quarter gate. It is not a device error
certificate. In particular, the leaked longitudinal orbital component
must not be assumed detectable by a single-band charge meter.

## 3. A posteriori Galerkin and time-propagation defects

For a real orthonormal Galerkin basis B, with
H(t)=H_0-b(t)W, the residual of its reduced solution is

\[
 R(t)\psi_r(t)=
 [H_0B-Bh_r-b(t)(WB-Bw_r)]\psi_r(t).
\]

The full finite-grid error is at most its integrated operator norm plus
the initial projection defect. `refined_gate.py` QR-compresses the full
grid residual operators before evaluation; it does not estimate them
from differences between optimizer outputs. Sampled Simpson integrals
are ordinary quadrature evaluations, not interval enclosures.

For the actual full-grid up-ramp, `audited_ramp.py` constructs the exact
Schroedinger defect of the DOP853 dense interpolation on every step.
The interpolation has degree7; the quintic Hamiltonian makes the defect
degree at most12. Its squared Frobenius norm is a real polynomial of
degree at most24, so13-point Gauss-Legendre integrates it exactly in exact
arithmetic. Cauchy-Schwarz on each step gives

\[
 \delta_{up}\le\sum_k\sqrt{h_k
   \int_{t_k}^{t_{k+1}}\|\dot\psi_h+iH\psi_h\|_F^2dt}.
\]

The floating evaluation gives

\[
 \delta_{up}\le .000209062703.
\]

The inequality and polynomial quadrature identity are mathematical
statements; the displayed number lacks certified rounding enclosures.
It is conservative relative to the observed gate error.

## 4. Linear propagation of that defect through a reciprocal gate

A naive bound on the returned overlap introduces an unnecessary square
root of delta_up. A unitary-extension argument avoids it.

For isometries Phi,Psi, define the block reflection

\[
 W(\Phi)=
 \begin{pmatrix}I-\Phi\Phi^\dagger&\Phi\\
                 \Phi^\dagger&0\end{pmatrix}.
\]

It is unitary. Since
||Phi Phi^dagger-Psi Psi^dagger||<=||Phi-Psi||, the product
W(Phi)W(Psi) maps (Psi v,0) to (Phi v,0) and differs from identity
by at most2||Phi-Psi||. Extending the true up-ramp by identity and
applying this comparison yields an up-unitary with prescribed approximate
code image within2delta. Its two appearances in the forward-transpose
return cost at most4delta. This dilation is proof-only; no physical
ancilla, negative time, inverse bath or extra controller is supplied.

Let Y be the numerical up-state, V the real active spectral basis,
C=V^T Y, and Cbar=C(C^dagger C)^(-1/2). With tau=||Y-VC|| and
e_iso=||Y^dagger Y-I||, put q=e_iso+tau^2. Then

\[
 \|Y-VCbar\|\le\tau+
 {q\over1+\sqrt{1-q}}.
\]

The scalar overlap used for the comparison gate is
Cbar^T exp(-i Lambda T_hold) Cbar. For the real normalized active
eigenvectors, direct Duhamel costs at most
T_hold ||H V-V Lambda|| on that state; no whole-space hold inverse is
assumed. Thus

\[
 \epsilon_{grid}\le\epsilon_{spectral,normalized}
 +4\left[\delta_{up}+\tau+
 {q\over1+\sqrt{1-q}}\right]
 +T_{hold}\|HV-V\Lambda\|.
\]

The measured up-isometry defect is3.63e-15, tail norm3.80e-8, and the
polar-normalization distance bound2.53e-15. Including those terms gives
the floating defect-based finite-grid estimate

\[
 \boxed{\epsilon_{grid}\lesssim .00215862.}
\]

The approximately .001322 observed error and .002159 sufficient estimate
are different quantities. Spatial discretization, frozen transverse
motion, source/controller corrections and interval rounding remain
outside both numbers. The spectral vectors and numerical initial code
are treated as orthonormal in the mathematical identity; their ordinary
floating normalization errors are at the numerical precision scale,
not interval certified.

## 5. Resources and remaining scope

This repaired pulse supplies a finite local rotation within the actual
interacting longitudinal model used by the root. It requires an acquired
real barrier height, finite ramp and hold timing; the numerical fit is
not an experimental acquisition procedure. It keeps source and bath
inverse operations absent. Actual electrode fluctuations, transverse
excitation, interrail transfer, reservoir loading, detector capture,
readout and retained-source interactions are not simulated here and
retain their separate cost/error terms. No threshold or complete
microscopic resource cycle is inferred from this local gate.

Two copies supply the corresponding logical X flip, with coherent
duration55.43512163 and a sufficient initial-code isometry estimate
twice the single-gate estimate, about .00431724. This telescoping bound
does not assume the actual intermediate state has returned perfectly;
the comparison gate preserves the code and the actual propagator is
unitary. It remains a bound in the same closed longitudinal model.

Files: refined_gate.py/results, refined_gate_200dim_check.json,
sparse_reciprocal.py/results/checkpoint, audited_ramp.py/results. The
old failure and its actual direct-grid correction remain in the root's
records. An already-running higher-barrier candidate check was also
preserved as sparse_reciprocal_229_results.json, but no further search
or physical claim was developed from it after the root's stop request.
