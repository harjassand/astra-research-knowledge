# Conditional closed-porosity certificate for conducting manufacturing powder

Status, 2026-10-12: a mathematically supported one-sided certificate and an ideal electrostatic acquisition identity have been reconstructed. A practical instrument, an industrial separation advantage, and originality have **not** been established. There are no experiments in this work. `model.py` supplies conditional numerical budgets and coefficient checks only.

The manufacturing bottleneck is closed gas volume inside metal feedstock, which exterior size sieves cannot directly distinguish. Feedstock pores can survive, move, coalesce, or seed larger defects during laser deposition, directly observed in [Pore evolution mechanisms during directed energy deposition additive manufacturing](https://www.nature.com/articles/s41467-024-45913-9), Nature Communications 2024. [Thermocapillary purification of molten powder droplets](https://www.sciencedirect.com/science/article/pii/S0032591024010568), Powder Technology 2025, is already a computationally proposed alternative, so pore-free feedstock is an active target. The candidate here is an electrical prequalification operation: accept a particle only when a conservative upper bound on its polarizability trace divided by mass is sufficiently close to the dense-sphere minimum. Its central feature is a one-sided guarantee rather than a shape-dependent inversion. Its value depends on acquiring that upper bound cheaply enough and retaining enough dense powder.

## 1. Closest demonstrated and disclosed competition

| Method | Primary evidence | Consequence for this candidate |
|---|---|---|
| Vacuum AC dielectrophoretic powder deflection | NASA/MIT report for the year ending September 1986, [NASA CR-183016](https://ntrs.nasa.gov/citations/19890004300), describes a constructed free-fall vacuum separator, designed for 20 Hz–20 kHz AC and up to 10 kV RMS, with the high-frequency voltage limited by transformer/capacitive effects. Its aim was material separation with approximately size-independent acceleration. [Report, pp. 5–8](https://ntrs.nasa.gov/api/citations/19890004300/downloads/19890004300.pdf) | Dry ballistic AC DEP and the size cancellation are established prior art. They cannot be claimed as the invention. This report does not establish 1% closed-void certification. |
| Hollow-powder air classification | [CN113499989A](https://patents.google.com/patent/CN113499989A/en), priority 2021, describes sieve size bins followed by airflow deflection to separate hollow and solid powder. | The application of density sorting to hollow AM powder is also prior art. A patent disclosure is not measured separation performance. |
| Electrostatic metal-powder classification | [Aluminum Powder Preparation for Additive Manufacturing Using Electrostatic Classification](https://www.mdpi.com/2079-6412/11/6/629), Coatings 2021, reports a narrower aluminum size distribution using a drum classifier. | Demonstrates relevant powder handling, but the reported endpoint is size distribution, not per-particle closed porosity. |
| Gas-phase polarizability/mass sorting | [Gas phase sorting of nanoparticles](https://arxiv.org/abs/0708.1936), Ulbricht et al., experimentally uses electric deflection of fullerenes. | Polarizability/mass sorting and patterned spatial readout are known. Moving from molecules to metal powder alone is insufficient novelty. |
| Spherical low-defect powder production | [Centrifugal granulation behavior in metallic powder fabrication by plasma rotating electrode process](https://www.nature.com/articles/s41598-020-75503-w), Scientific Reports 2020. | PREP already offers highly spherical powder with minimal internal pores; compare final retained yield and cost against purchasing or making better powder. No matched cost/porosity benchmark has been acquired here. |
| Thermocapillary pore removal | [Pore elimination mechanisms during 3D printing of metals](https://pmc.ncbi.nlm.nih.gov/articles/PMC6625989/), Nature Communications 2019, experimentally tracks pore motion and escape during laser processing. | Processing can already remove some pores. A feedstock certificate has to beat this route under matched part quality, material yield, and energy accounting. |

Electrodynamic balances already measure individual aerosol size and mass: [Davis and Ray, 1980](https://www.sciencedirect.com/science/article/pii/0021979780904786) measured suspended droplets using optical scattering and DC balance. [Mass, charge, and radius of droplets in a linear quadrupole electrodynamic balance](https://www.tandfonline.com/doi/full/10.1080/02786826.2018.1559921), 2019, is a newer primary example. These are close metrology, but do not supply the missing multi-million-particle-per-second acquisition for irregular metal powder. Direct internal-defect characterization is also established: [Defect and satellite characteristics of additive manufacturing metal powders](https://www.sciencedirect.com/science/article/pii/S0921883122000644), 2022, resolves dispersed individual particles by synchrotron tomography. A direct prior-art search for the complete trace-bound certificate remains incomplete. It is not defensible to call it a new patentable operation on the basis of this search.

## 2. Exact certificate and its admitted material class

Let Ω be the filled outer conducting domain of a single connected particle, volume V. Closed internal gas cavities occupy fraction φ of V. Initially admit smooth, bounded, simply connected filled domains and continuous metallic walls; this permits very general shapes without relying on a topology extension. The metal has uniform known density ρ, and all cavities are electrically screened. There are no appreciable nonmetal masses or density-changing inclusions in the ideal statement. Open pores, disconnected conducting grains, broken metallic skins, and unbounded composition variation are excluded.

The electrostatic exterior response of a connected conductor is unchanged when shielded cavities are filled with conductor. Its physical uniform-field dipole polarizability is α=ε₀M∞, a positive definite tensor. The endpoint inverse-trace Hashin–Shtrikman bound is

\[
 V\operatorname{Tr}(M_\infty^{-1})\le 1.
\]

The finite-contrast bound is stated in [Kang and Milton, Solutions to the conjectures of Pólya–Szegő and Eshelby](https://arxiv.org/abs/math/0609374), equations (1.3)–(1.4), with the right side tending to 1 as contrast tends to infinity. The sphere has M∞=3VI. A direct endpoint proof with broader connected-domain hypotheses appears as Theorem 4.2 in [Colbrook and Sadeghi, 2026 preprint](https://arxiv.org/html/2608.20466v1). The necessary imported fact is the inequality; equality classification is not needed for safety.

For positive eigenvalues, Cauchy–Schwarz gives

\[
9\le\operatorname{Tr}(M_\infty)\operatorname{Tr}(M_\infty^{-1})
\quad\Longrightarrow\quad
\operatorname{Tr}\alpha\ge9\epsilon_0V.
\]

Since m=ρ(1−φ)V,

\[
R:=\frac{\operatorname{Tr}\alpha}{m}\ge\frac{9\epsilon_0}{\rho(1-\phi)}.
\]

Thus an acquired **upper** bound R≤U certifies

\[
\boxed{\phi\le1-\frac{9\epsilon_0}{\rho U}.}
\]

In particular, R≤(1+δ)9ε₀/ρ implies φ≤δ/(1+δ). Arbitrary asphericity can cause false rejection, but cannot cause false acceptance under the admitted model. A result with a negative computed upper bound means the acquisition/material hypotheses are inconsistent and must be rejected, not silently clipped into evidence of a perfect particle.

For a conducting spheroid with depolarization factors Lᵢ, αᵢ=ε₀V/Lᵢ, so its normalized ratio is

\[
\frac{R}{9\epsilon_0/\rho}=\frac{\sum_iL_i^{-1}}{9(1-\phi)}.
\]

The runnable calculation gives a dense prolate with aspect ratio 1.19188 the same R as a spherical particle with 1% void. This falsifies porosity inversion from high R. It does not falsify the low-R certificate. Dense aspect ratios 1.1 and 1.2 have trace penalties approximately 0.294% and 1.091% respectively, showing the yield cost.

### Robust material statement

Let the electrically screened conducting core have filled volume Vc and void fraction φc. Suppose per-particle ancillary/nonmetal mass is at most ηmax of total mass, the average density of its conducting solid material is at most ρmax, and the measured response obeys

\[
\operatorname{Tr}\operatorname{Re}\alpha_{\rm meas}
\ge(1-\varepsilon_\alpha)\,9\epsilon_0V_c.
\]

This last condition is a calibrated physical lower bound, not automatically a consequence of a bulk conductivity datasheet. Then

\[
(1-\eta_{\max})m\le m_{\rm conductor}
\le\rho_{\max}(1-\phi_c)V_c
\]

and a true upper bound U on Tr Re αmeas/m gives

\[
\boxed{\phi_c\le1-
\frac{9\epsilon_0(1-\eta_{\max})(1-\varepsilon_\alpha)}{\rho_{\max}U}.}
\]

A bulk lot assay bounds a mean, not every particle; it cannot silently supply these per-particle bounds. A sphere with 2% void plus 2% inclusion volume of density 2ρ has exactly the nominal filled mass and the same exterior conductor polarizability. It defeats a nominal-ρ certificate. Density bounds, composition control, or rejecting uncertain particles are essential.

At strictly static positive dielectric contrast, an oxide coating around a conducting core should not lower polarizability relative to the bare core; its mass still weakens R. A spherical coated-core calculation gives a useful calibration example. With core/outer volume fraction f and relative coating permittivity εs,

\[
\frac{\alpha}{4\pi\epsilon_0 R^3}=
\frac{\epsilon_s(1+2f)-(1-f)}{\epsilon_s(1+2f)+2(1-f)}.
\]

This example is not a general dynamic, irregular-coating error bound. Oxide thickness, metallic continuity, magnetic forces, and frequency response must be admitted or measured. The dimensionless conductivity parameter σ/(ωε₀) is very large for bulk metals at MHz frequencies, but this does not settle coating, finite-electrode, or motion errors.

## 3. A source-free field geometry; scalar identity only

Define three harmonic potentials near a particle:

\[
\Phi_1=-E_0x-\tfrac g2(x^2-y^2),\qquad
\Phi_2=-E_0y-gxy,\qquad
\Phi_3=-E_0z-gxz.
\]

Each satisfies ∇²Φ=0. Their uniform vectors are e₁=E₀x̂, e₂=E₀ŷ, e₃=E₀ẑ, and their symmetric trace-free gradient matrices are

\[
G_1=g\operatorname{diag}(1,-1,0),\quad
G_2=g\begin{pmatrix}0&1&0\\1&0&0\\0&0&0\end{pmatrix},\quad
G_3=g\begin{pmatrix}0&0&1\\0&0&0\\1&0&0\end{pmatrix}.
\]

For a neutral point dipole at the origin, Fⱼ=Gⱼαeⱼ. Equal exposure gives

\[
\overline F_x=\frac{gE_0}{3}\operatorname{Tr}\alpha,\quad
\overline F_y=0,\quad
\overline F_z=\frac{gE_0}{3}\alpha_{xz}.
\]

The last force is real: this construction does **not** cancel arbitrary anisotropy in the full force vector. The useful identity is a scalar measurement along x. Source-free field constraints obstruct the stronger naive full-vector cancellation.

For the same point-dipole construction away from the origin,

\[
\begin{aligned}
\bar a_x&=\frac g{3m}[(E_0+gx)\operatorname{Tr}\alpha+gz\alpha_{xz}],\\
\bar a_y&=\frac{g^2y}{3m}(\alpha_{xx}+\alpha_{yy}),\\
\bar a_z&=\frac g{3m}[gz\alpha_{xx}+(E_0+gx)\alpha_{xz}].
\end{aligned}
\]

Positive semidefiniteness gives |αxz|≤Trα/2. When E₀+gx>|gz|/2, a conservatively bounded measured acceleration can produce

\[
\frac{\operatorname{Tr}\alpha}{m}
\le\frac{3(\widehat a_x+\varepsilon_a)}
{g(E_0+gx-|gz|/2)}.
\]

The position and field denominator require lower confidence bounds. This is only a point-dipole result; it cannot itself certify arbitrary finite particles. At z=15 μm and E₀/g=1 mm the position-independent conservative bound already loses about 0.756%, nearly the complete target budget.

## 4. Exact finite-body parity acquisition

The finite-size correction is not optional. In an affine applied field a gradient can induce a dipole even when the uniform field is zero. Its force is even in g and can have a shape-dependent sign along x. Natural power counting Rparticle/(E₀/g)=0.015 in the proposed example is larger than the 1% void signal. This is a warning scale, not a rigorous universal error bound.

There is an exact ideal way to remove it. Hold the particle's position, orientation, geometry, and net charge q fixed. Work in free space with a linear electrostatic response and exactly affine imposed field Eext(r)=e+Gr. The net self-force cancels. Integration of external force over the full surface charge gives exactly

\[
F=q e+G p,
\]

where p is the full laboratory dipole; no multipole truncation has occurred. Linear response at fixed q implies

\[
p=p_q+\alpha e+B:G
\]

with the position-induced term αGr included in B:G or written separately. In the four sign settings (e,G)=(se,tG), s,t∈{−1,+1}, therefore

\[
\boxed{F^{\rm odd,odd}:=\tfrac14\sum_{s,t}st\,F(se,tG)=G\alpha e.}
\]

The q e, Gpq, G(B:G), and position-dependent GαGr terms all have different parity. Combining the x component of this operation for the three field geometries gives

\[
\boxed{\tfrac13\sum_{j=1}^3(F_j^{\rm odd,odd})_x/m
=\frac{gE_0}{3}\frac{\operatorname{Tr}\alpha}{m}.}
\]

The energy formulation is equivalent: translation replaces e by e+Gr in

\[
W_0=-\tfrac12e^T\alpha e-e^T(B:G)-\tfrac12G:\Gamma:G
\]

plus fixed-charge terms. Differentiating and selecting odd/odd parity yields the same result.

The proof is conditional on a fixed configuration and imposed affine free-space field. Real electrode image forces, spatial cubic/higher harmonics, nonlinearity, magnetic forces, particle interactions, geometry changes, phase calibration errors, motion, and rotation require new error bounds. The finite coefficient example in `model.py` includes nonzero B:G, charge, and displacement and checks the identity; it is not a numerical solution of a conductor boundary problem or an experiment.

Crucially, st is a **signed data weight**. Equal unweighted exposure to the four sign settings cancels the desired E₀g term in the net impulse. Therefore this identity is a metrology primitive; it is not automatically a passive separator with the large uncompensated deflection. A claim that it automatically preserves the approximately 103 μm kick signal is false. Phase ordering can leave a nonzero displacement even with zero impulse, so this is not a claim that every displacement-based acquisition fails. It needs resolved force/trajectory records, a defensible joint fit, or another physical transducer, followed by active rejection.

### Positive-exposure obstruction, including mass-center tracking

There is an exact obstruction to replacing the signed operation by a universal positive-exposure ensemble of affine fields. Let every gradient Gⱼ be symmetric, choose weights wⱼ>0, and allow arbitrary correlated uniform fields eⱼ. Suppose the ensemble cancels the even-gradient nuisance in its x force for every admitted particle.

It is enough to consider a conducting spherical outer boundary of radius R with one closed spherical gas cavity of fixed volume fraction φ>0. Let u be the cavity center relative to the outer sphere center. Its exterior response is α₀I, independent of u. Its mass center is displaced by −φu/(1−φ) from the outer sphere center. Even when the instrument centers each known **mass center** at zero, the electrical sphere center is

\[
d=\frac{\phi}{1-\phi}u.
\]

As the cavity moves inside the sphere, d ranges over a nonempty ball. Its exact dipole and force are

\[
p=\alpha_0(e+Gd),\qquad F=\alpha_0G e+\alpha_0G^2d.
\]

Therefore cancellation of the nuisance for every cavity location requires x̂ᵀHd=0 for all d in that ball, where H=ΣⱼwⱼGⱼ². Hence x̂ᵀH=0 and

\[
0=\hat x^TH\hat x=\sum_jw_j\|G_j\hat x\|^2.
\]

Every Gⱼx̂ must vanish. Symmetry then makes every x row vanish, so (Gⱼαeⱼ)x=0 for every α,eⱼ. Thus no nonzero universal x trace signal remains. This proves an exact negative result for this positive-exposure architecture, even with known mass-center centering and within the admitted closed-pore material family. Taking a full isotropic ensemble of five symmetric trace-free gradients cannot evade the sum of squares.

The scope matters: this does not forbid adapting to an acquired electrical center, allowing a bounded residual, nonlinear fields, shape-specific calibration, signed trajectory measurements, or active force feedback. It does rule out claiming that a universally cancelling passive ensemble exists simply by averaging more harmonic quadratic fields.

### Random axis probing does not remove acquisition cost

For an isotropic independent random unit vector u, let e=E₀u and choose

\[
G/g=\begin{pmatrix}u_x&u_y&u_z\\u_y&-u_x/2&0\\u_z&0&-u_x/2\end{pmatrix}.
\]

This is symmetric and trace-free, with scalar cross force Fx=gE₀uᵀαu. Conditional on a tensor orientation that cannot react to the random draw, X=3uᵀαu/Trα is unbiased and

\[
\operatorname{Var}X=\frac65\left[
\frac{\operatorname{Tr}(\alpha^2)}{(\operatorname{Tr}\alpha)^2}-\frac13\right]
\le\frac45.
\]

For the naive independent sample mean, a worst-case 0.2% relative standard-error budget therefore corresponds to 200,000 probes per particle, before sensing noise or a confidence margin. This is an estimator budget, not a universal information lower bound; admitted near-isotropy or structured protocols may do better. Random codes can address orientation sampling bias only when their independence and response timing hold. They do not cancel the even-gradient nuisance proved above or acquire each force record for free.

## 5. Decisive physical budget

The exact values below are generated by `model.py`, using a 30 μm diameter aluminum sphere with nominal ρ=2700 kg/m³, E₀=10⁶ V/m and g=10⁹ V/m². Field amplitudes are RMS for a fast common AC carrier, or static amplitudes if force signs are explicitly resolved. Carrier averaging and slow sign modulation are distinct operations.

| Quantity | Conditional value | What it establishes |
|---|---:|---|
| Central three-field acceleration | 9.838 m/s² | Ordinary force scale only |
| 1 ms unipolar kick + 10 ms drift | 103.30 μm | Ideal point-dipole spatial readout baseline |
| Extra displacement for 1% void | 1.043 μm | Required differential resolution before error margins |
| Particle rate at 1 kg/h | 7.277 million/s | Actual acquisition burden |
| 5 m/s lanes at 0.5 mm longitudinal spacing | 728 lanes | Illustrative parallelization; not a demonstrated feeder |
| Twelve independent phase records/particle | 87.3 million records/s | A lower-level accounting example, not a complete sensor budget |
| Radius/field variation length | 0.015 | Point-dipole accuracy cannot be presumed below 1% |
| Epstein relaxation time at 0.1 Pa N₂, 300 K | Approximately 75.8 s | Gas drag is potentially manageable over 11 ms; accommodation and pumping still need calibration |

For a mechanical acceleration harmonic amplitude a at sign-modulation frequency fm, free displacement is a/(2πfm)². At fm=1 kHz the above acceleration gives only 249 nm, so a 1% coefficient is 2.49 nm. At fm=100 kHz it is 0.249 pm. These are not the much larger downstream displacement of an uncompensated kick. They are also not a universal lower bound on pulse-coded readout: a known waveform can encode accumulated position or velocity moments that a joint fit could exploit. Optical phase tracking or pulse fitting might improve acquisition, but no such instrument has been specified and validated here.

Rotation conflicts directly with long force acquisition. If a rigid body's angular speed is bounded by Ωrot, then ||α̇||≤2Ωrot||α||. A coarse equal-slot error bound is 2Ωrot h for frame duration h; at an assumed Ωrot=10⁵ rad/s, a 0.1% worst-case bound requires h≤5 ns. This assumed spin is a stress case, not measured feedstock spin. Nearly spherical admitted particles have smaller tensor anisotropy, and palindromic schedules can cancel some smooth drift, but neither supplies an uncharged arbitrary-rotation guarantee. Slowing, orienting, measuring, or rejecting fast-spinning particles is part of the acquisition cost.

At a 100 kHz carrier, q=10⁻¹³ C gives a residual ponderomotive/electric DEP scale q²/(mω²α)≈0.00177 for this particle. A charge bound or valid parity cancellation is required. Carrier AC by itself is not exact neutralization. At 1 MHz that illustrative scale is approximately 1.77×10⁻⁵. Finite-configuration four-sign cancellation removes charge parity terms; charge-driven movement between phases can reintroduce them.

For an illustrative 10 pF electrode load at 1 kV RMS, reactive power is ωCV²: 6.28 VA at 100 kHz and 1257 VA at 20 MHz. At Q=100, corresponding losses are 0.063 and 12.6 W. These are per specified load, not per actual lane: shared electrodes may reduce or increase total capacitance. Vacuum pumps, feeder locks, sensing, active rejection, electrode cleaning, and cooling are not included. An electrode layout and contamination-qualified high-voltage test are needed before an energy claim.

An example total error allocation of ηmax=0.1%, εα=0.1%, relative upper measurement error=0.2%, and ρmax/ρnominal=1.001 leaves normalized measured acceptance Rhat/(9ε₀/ρnominal)≤1.005065 for a 1% void target. A dense prolate then passes only up to aspect approximately 1.13290. Those are assumed error budgets, not measured capabilities or certified per-particle material bounds.

## 6. Falsifiable experiment and stop gates

First build a low-rate force instrument, not an industrial sorter. Admit one alloy and a stated oxide/composition window. Include dense spheres, dense smooth aspheres, deliberately closed-void particles spanning below and above 1%, asymmetric dense particles to expose B:G, charged particles, and measured spin states. Ground truth each retained test particle with registered sufficiently resolved X-ray tomography and, where needed, destructive sectioning; assess the uncertainty of the tomography and solid-density reference instead of calling it exact. Compare airflow density sorting, ordinary one-field DEP, shape/size imaging, and the trace/parity operation on the same frozen challenge set.

The first decisive gate is simultaneous acquisition of a conservative 0.2% upper error on R for admitted moving particles, including image fields, phase dynamics, position, charge, rotation, and oxide response. An asymmetric particle's raw even-gradient force should remain while the odd/odd estimate is invariant under changes of g at fixed E₀g and under charge reversal, within that error budget. Deliberately change field cubic contamination and electrode spacing to test the claimed boundary of the exact identity.

Stop the proposed 1% certificate if a ground-truthed above-threshold particle is accepted beyond the declared confidence/mismatch budget, if the needed material bounds cannot be acquired, or if the error interval is too broad to retain a useful dense-powder yield. Dense asphere rejection alone is expected and should be counted as yield loss. Passing a few spheres only verifies a special case.

Only after that gate, freeze the sensing and rejection operation and test throughput, energy, contamination, maintenance, and retained powder yield against matched commercial preparation. An illustrative industrial target is ≥1 kg/h, ≤1% per-particle closed-void upper bound for accepted material, and ≥90% retention of admitted dense powder. This target is proposed, not demonstrated. A false-accept rate below 10⁻⁶ with 95% one-sided confidence would require about 3.0 million independent representative above-threshold challenges if zero failures occur; an adversarial or distribution-shift guarantee requires more than a binomial calculation.

## 7. Originality and scope verdict

The best candidate contribution is the composition-aware one-sided trace certificate and the finite-body odd/odd acquisition identity. The imported polarization inequality, AC DEP, polarizability/mass sorting, electrostatic powder processing, and hollow-powder separation are known. The combination's originality has not been established, and the measurement mechanism may be an ordinary application of lock-in parity methods. Its practical acquisition burden currently prevents any claim of a transformative manufacturing capability.

Earlier branches were deliberately abandoned: membrane-based phase-change cooling and separate vapor paths have strong experimental precedents; selective gas extraction through a molten-metal-blocking membrane appears in [US2809107A](https://patents.google.com/patent/US2809107A/en), priority 1953. Phase-gated substrate acceleration was derived as a pore-clearing mechanism, but [Phase-controlled vibrational laser percussion drilling](https://www.extrica.com/article/14923) already synchronizes laser melting with workpiece acceleration, making the proposed rectification too close for a strong novelty claim. These are excluded routes, not evidence of a discovery.

The concrete result is a conditional mathematical certificate plus an exact ideal sensing identity, with a sharply exposed rotation/readout/throughput gate. It is not an experimentally verified separator, a validated porosity measurement, or an established new foundational technology.
