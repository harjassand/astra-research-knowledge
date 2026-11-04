---
title: "Alpha-to-ion heat conversion: a damping–bandwidth obstruction"
date: "4 November 2026"
geometry: margin=0.85in
fontsize: 10pt
---

# Outcome and scope

The attempted capability is useful transfer of fusion-alpha energy into fuel ions,
with sufficient power, accessible geometry and a better total energy balance than
existing alpha-channeling approaches. That capability has **not** been constructed.
The work below supplies an exact theorem for a reduced kinetic model, an exact
finite-Hermite energy identity, and numerical tests of one homogeneous linear
conversion stage. It does not establish a new instability, a reactor operating
point, a nonlinear extraction fraction, historical novelty or experimental success.

Microscopic thermal memory was set aside after the preserved two-body mediator
failed its composed logical-degeneracy test. Existing higher-dimensional passive
models and active fault tolerance remain stronger references than that failed
construction. This is a change of physical operation, not an extension of it.

The ingredient is [Qin and Fisch, arXiv:2609.07732v1](https://arxiv.org/html/2609.07732v1),
Sections II and VI–IX: a minority-ion cyclotron pole can destabilize a thermal ion
Bernstein mode. Its example transfers energy into coherent proton motion; the
authors explicitly leave irreversible heating and practical thresholds open.
Our question is whether adding a conserving relaxation channel closes that gap
without losing the source instability to Doppler broadening.

# Exact damping–bandwidth theorem for the reduced equation

Use frequencies relative to the energetic-ion harmonic. Let \(g,d,K>0\), with
\(g\) a coupling frequency, \(d\) the damping rate of the positive-energy thermal
mode, \(K\) the Gaussian parallel Doppler width, and \(\Delta\in\mathbb R\) a
freely adjustable detuning. Consider precisely

\[
 \delta-\Delta+i d-\frac{g^2}{K}Z(\delta/K)=0,                 \tag{1}
\]

where, for \(\operatorname{Im}z\ge0\),

\[
 Z(z)=i\int_0^\infty e^{-t^2/4+i zt}\,dt.
\]

This is a local normal form, not the full dielectric. It retains one positive
residue, a constant thermal slope/damping, and a Gaussian parallel source. In
particular it omits the source's parallel-gradient numerator and other poles.

**Theorem.** Some real detuning permits a root with positive growth if and only if

\[
 K<K_{\rm crit}:=\frac{\sqrt\pi g^2}{d}.                    \tag{2}
\]

The greatest possible growth over all real detunings is attained at \(\Delta=0\)
and is the unique positive solution of

\[
 \gamma+d=\frac{\sqrt\pi g^2}{K}
           \operatorname{erfcx}(\gamma/K).                  \tag{3}
\]

**Proof.** Write \(\delta=x+i\gamma\), \(\gamma>0\). The integral gives

\[
 \operatorname{Im}Z(x/K+i\gamma/K)
 =\int_0^\infty e^{-t^2/4-\gamma t/K}\cos(xt/K)\,dt
 \le\sqrt\pi\operatorname{erfcx}(\gamma/K)<\sqrt\pi.
\]

Taking the imaginary part of (1) proves necessity of (2). At zero detuning,
\(\delta=i\gamma\) solves the real part identically. The right side of (3)
strictly decreases with \(\gamma\), while the left side increases. At zero
growth their ordering is favorable exactly under (2); at infinite growth it is
unfavorable. Continuity therefore gives a unique positive root. The preceding
cosine bound shows that any root at any detuning has growth no larger than it.
Equality requires \(x=0\), which in (1) requires \(\Delta=0\). This proves the
claimed optimum and excludes an improvement from mere frequency retuning. At
equality in (2) the centered root is marginal, not growing. \(\square\)

In the cold-source limit, (3) becomes

\[
 \gamma(\gamma+d)=g^2,\qquad
 \gamma=\frac{2g^2}{d+\sqrt{d^2+4g^2}}.                    \tag{4}
\]

For a strongly damped conversion stage, \(d\gg g\), growth is approximately
\(g^2/d\), and the allowed Doppler width is only \(\sqrt\pi g^2/d\).
Efficient relaxation can therefore narrow the source's allowed frequency spread.
This conclusion is an exact statement about (1). It is not a stability theorem
for every alpha distribution, every plasma branch, or every geometry.

# A conserving model separates stored wave energy from heat

Let \(f_1/f_0\) have normalized three-dimensional probabilists' Hermite coefficients
\(a_{n_xn_yn_z}\), with Maxwellian \(f_0\) of variance
\(\sigma_p^2=T_p/m_p\). Frequencies below are in units of \(\Omega_p\).
The linearized Dougherty model is

\[
 C=-\nu N+\nu\Pi_{1}+2\nu|u_E\rangle\langle u_E|,
 \quad u_E=(|200\rangle+|020\rangle+|002\rangle)/\sqrt3,     \tag{5}
\]

where \(N\) is total Hermite degree and \(\Pi_1\) projects onto the three degree-one
momenta. Thus density, all three momenta and total three-dimensional energy are
null modes; every remaining eigenvalue is nonpositive. The model and its Hermite
structure are established; see [Anderson and O'Neil, *Eigenfunctions and Eigenvalues
of the Dougherty Collision Operator*](https://nnp.ucsd.edu/pdf_files/Dougherty_operator.pdf),
Sections I–II. Its constant drag/diffusion coefficients do not reproduce the full
velocity dependence of Coulomb collisions. We have not calibrated \(\nu\) to a
measured or full Landau collision operator.

Use the field convention \(\exp(i\mathbf k\cdot\mathbf x-i\omega t)\), and normalize
\(q_p\phi/T_p=1\). The finite Galerkin response obeys

\[
 (A-C-iwI)a=b,\quad
 b=-i\frac{\sigma_p}{\Omega_p}(k_\perp|100\rangle+k_\parallel|001\rangle),
\]

where streaming plus gyromotion \(A\) is anti-Hermitian. Define

\[
 P=\frac{\omega_{pp}^2}{k^2\sigma_p^2},\quad
 \chi_p=-P a_{000},\quad \gamma=\operatorname{Im}w>0.
\]

Multiplying the response equation by \(a^\dagger\), taking its real part, and
using its density row gives the **exact finite-matrix identity**

\[
 \frac{\operatorname{Re}[-iw\chi_p]}{\gamma}
   =P\|a\|^2-\frac{P}{\gamma}a^\dagger Ca.                 \tag{6}
\]

The first term is reversible fluctuation free energy; the second is nonnegative
quadratic entropy production. In the specified relaxation model it is the
irreversible conversion of fluctuation free energy into background heat.
First-order conservation of total energy in (5) is consistent with this
second-order relaxation. It does not justify equating all coherent proton power
with heat. Nor does (6) certify nonlinear heating in a real device.

For \(k_\parallel=0\), the full 3D operator leaves \(n_z\in\{0,2\}\) invariant; both
are retained. At finite parallel wavenumber, extra \(n_z\) values are included and
their cutoff is checked. An initial 2D trial was replaced by the full 3D model;
only the latter supports the physical numbers below.

# Specified full-dielectric test

The reference uses \(B=0.05\) T, \(n_p=10^{17}\,\mathrm m^{-3}\),
\(n_\alpha/n_p=0.02\), \(T_p=5\) eV, \(T_e=10\) eV, alpha mass \(4m_p\), and
mean alpha energy 24 keV. These are a cold laboratory-scale reference, not a
proton–boron fusion plasma. At finite \(k_\parallel\), electrons and alphas have
their full collisionless kinetic susceptibilities; protons use (5).

For independently normalized gyrotropic distributions, the kinetic integral is

\[
 \chi_s=\frac{\omega_{ps}^2}{k^2}
 \sum_n\int d^3v\frac{J_n^2(k_\perp v_\perp/\Omega_s)}
 {\omega-k_\parallel v_\parallel-n\Omega_s}
 \left(\frac{n\Omega_s}{v_\perp}\partial_{v_\perp}f_s
              +k_\parallel\partial_{v_\parallel}f_s\right). \tag{7}
\]

Integrating its Gaussian parallel factor gives \(Z\) and its derivative.
Large-argument upper-half-plane expansions avoid cancellation. Cold-ring
responses are averaged over an explicitly normalized perpendicular speed
distribution, a Gaussian in \(u=v/v_0\) of width 0.1, truncated at six standard
deviations and rescaled to keep the stated mean energy. This is an imposed test
population, not an acquired fusion birth or loss-cone distribution. With parallel
temperature \(T_{\alpha\parallel}\), mean perpendicular energy is
\(24000-T_{\alpha\parallel}/2\) eV, so total energy is unchanged.

## Benchmark and perpendicular-width correction

At \(k_\perp=251.74\,\mathrm m^{-1}\), the source's cold benchmark is reproduced:

\[
 w=1.49837407794+0.00133377037i,
\]

with proton, alpha and electron powers in units \(2\gamma W_E\) equal to
11843.15987, −11848.43978 and 4.2799083. Including the growing field closes the
balance. Here \(W_E=\epsilon_0|E|^2/4\).

The actual thermal-only crossing at \(w=1.5\) is
\(k_*=250.147719979\,\mathrm m^{-1}\), \(b_p=1.306503224\).
For the mass/response conventions just stated, the *cold* third-alpha residue
there is negative, −0.07217383435 in dimensionless \(w^2\) coordinates. The
positive-residue theorem therefore does not certify that nominal cold crossing.
The source's Section VIII already says this crossing needs revalidation; this
discrepancy does not refute the conditional root-pole theorem.

Finite perpendicular width changes the sign favorably in this example. At the
same crossing, widths 0.02, 0.1 and 0.2 give residues 0.0006146618, 0.0006671396 and
0.0008915813; corresponding collisionless growth rates are approximately
0.0001606113, 0.0001673271 and 0.0001934365. Broadening need not destroy the
perpendicular drive because it averages an oscillatory Bessel derivative.

Harmonic truncation 190 versus 450 and radial quadrature 160, 320 and 640 were
compared. Width 0.1 is converged for the reported quantities. An initial
width-0.4 residue was aliased; its value was withdrawn. The converged width-0.4
residue is −0.03979934, with no validated growing continuation branch found.
Failure to find one is not a global stability proof.

## Relaxation helps heat conversion while suppressing growth

For width 0.1, \(k_\parallel=0\) and \(k_\perp=k_*\), numerical solutions of the full
dielectric give:

| model collision rate \(\nu/\Omega_p\) | growth \(\gamma/\Omega_p\) | irreversible proton heat / alpha power loss |
|---:|---:|---:|
| 0 | 0.0001673271 | 0 |
| 0.000001 | 0.0001653220 | 0.02382 |
| 0.00001 | 0.0001483660 | 0.21379 |
| 0.0001 | 0.0000603649 | 0.86985 |
| 0.001 | 0.0000069280 | 0.998286 |
| 0.003 | 0.0000023135 | 0.999809 |

These are *fractions of the infinitesimal eigenmode's instantaneous alpha power
loss*. They are not fractions of all alpha birth energy recovered, and they do
not determine absolute power without amplitude and saturation. Rate 0.001 was
chosen as a model stress test, not supplied as a calibrated physical service.

The extracted local parameters are \(g=0.0001673270\Omega_p\) and
\(d=0.004034533\Omega_p\), giving \(K_{\rm crit}=1.230025\times10^{-5}\Omega_p\)
and cold growth \(6.927778\times10^{-6}\Omega_p\). This closely describes the full
numerical branch. Agreement is an asymptotic/numerical check; it does not promote
the exact theorem about (1) into a full-dielectric theorem.

## Direct marginal solve and retuning

For \(\nu/\Omega_p=0.001\), solve both real and imaginary dielectric equations on
the real-frequency axis rather than treating failed unstable-root searches as
stability. At fixed \(k_\perp=k_*\), the results are:

| \(T_{\alpha\parallel}\), eV | marginal \(k_\parallel\), \(\mathrm m^{-1}\) | \(\pi/k_\parallel\), m |
|---:|---:|---:|
| 1 | 0.00880865 | 356.65 |
| 10 | 0.00269373 | 1166.26 |
| 100 | 0.0008539486 | 3678.90 |
| 1000 | 0.000277841 | 11307.15 |

For 100 eV, Hermite total orders 20, 24 and 28 with parallel cutoffs 3, 4 and 5
give marginal wavenumbers 0.000853948701, 0.000853948616 and 0.000853948615.
Marginal residuals are below \(1.1\times10^{-10}\). Tracking the same branch at
0.8 and 1.2 times this wavenumber gives respectively positive growth
\(2.0807632\times10^{-6}\Omega_p\) and negative growth
\(-2.2682245\times10^{-6}\Omega_p\).

Retuning \(k_\perp\) to place the marginal wave exactly at the alpha harmonic
gives \(k_\perp=250.144493933\,\mathrm m^{-1}\) and
\(k_\parallel=0.000853982666\,\mathrm m^{-1}\). Thus this resonance retuning does
not remove the small bandwidth. It is not an optimization over every mode,
distribution, collision rate or geometry. The parallel-gradient source term is
included in these numerical tests, which is why the reduced theorem is not an
exact identity for the full calculation.

For a uniform column with Dirichlet potential at both ends, the smallest nonzero
parallel wavenumber is \(\pi/L\). This one stage therefore requires roughly
3.7 km at 100 eV. Periodic/closed-field/flute geometries can admit exactly
\(k_\parallel=0\); the length inference does not apply to them. We have not
acquired a finite-device eigenmode or proved a no-go theorem for alpha channeling.

# Same-resource comparator and unclosed capability gates

At identical \(f_0,k,\omega,\phi,\nu\), an externally maintained wave has precisely
the same linear proton response \(a\) and heat production as this self-excited
field. Equation (6) gives, without dividing by growth,

\[
 Q_p=-2\Omega_p W_E\,P\,a^\dagger C a.
\]

Thus the constructed relaxation operator supplies no new heating advantage at a
fixed field. A practical advantage would have to come from affordable alpha
extraction and reduced external drive after all losses and source preparation
are charged. Neither absolute extraction power nor such a total-cost advantage
has been demonstrated.

The stronger established architecture couples spatial extraction with energy
diffusion and selective ion damping. [Fisch and Herrmann's 1999 tutorial](https://w3.pppl.gov/~fisch/web/1999c.pdf),
Section 2, explains why the energy/position paths, wave competition with slowing
down, and multiple-wave spectrum matter for a full birth distribution. The
present homogeneous ring stage has not beaten that architecture with equal
wave/control resources. No completed reactor-level comparison is claimed.

The decisive missing operations are an earned energetic-ion distribution and
its replenishment cost; a finite-device mode that survives parallel/field
inhomogeneity and escape; a calibrated conserving multispecies collision model;
nonlinear extraction, saturation and ash removal; and a full equal-resource
energy balance including electron heating, radiation, drive and confinement.
Adding a positive growth rate or a high instantaneous heat fraction does not
supply these operations. The source's own single-wave plateau warning is also
not an acquired many-wave recovery scheme.

# Evidence and limitations ledger

Private working directory: `scratch/astra-alpha-transfer-20261104` under
`/workspace`. Numerical receipts are `DISPERSION_RESULTS.json`,
`WIDTH_RESULTS.json`, `QUADRATURE_CHECK.json`, `PARALLEL_GATE.json`,
`MARGINAL_RESULTS.json` and `NORMAL_FORM_RESULTS.json`. Source code and logs remain
private; this proof archive contains no Python. Computation used Python 3.12.14,
NumPy 2.3.5 and SciPy 1.17.0 on the provided CPU environment, with no external
compute purchase. The repository ingredient checkout is
`3e6f6fa576181275bb8ed28164e7cacd51055789`.

The finite-Hermite null space, anti-Hermitian streaming/gyromotion, identity (6),
full field/species power balance, quadrature and selected marginal convergence
were checked. Near-pole cancellation made an absolute power-balance tolerance
inappropriate; it was replaced by a relative tolerance, with the dielectric
residual retained. Numerical solves are floating-point diagnostics, not interval
certificates or a global root census. The only exact stability statement here is
the explicit reduced-model theorem (1)–(3).

The current Astra N1639 packet was consulted as a warning about missing RF-to-
heat accounting. Its reduced zonal-flow primitive is a different mechanism and
supplies no theorem used here. Current packet access did not supply a gyrokinetic
heat advantage or the missing energetic-ion kernel. No held archive was fetched.

Access limits: two OSTI primary endpoints returned HTTP 502 during this pass;
their full text was not acquired. An APS search result for the 2022 proton–boron
power-balance paper required authorization; no alternate full-text route was
used. These are literature-comparison limits, not physical evidence against any
method. Other cited primary sources were read through the web tool. This record
preserves a substantial scoped obstruction and adverse numerical tests; the
civilisation-changing objective remains open.
