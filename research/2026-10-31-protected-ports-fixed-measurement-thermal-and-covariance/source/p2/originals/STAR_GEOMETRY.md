# Full-charge electrostatic locality for the S3 STAR interface

Working derivation, 30 October 2026. This extends the direct-refocusing investigation in this directory without changing earlier work. It supplies an electrostatic interface and incident-interaction bounds. It does not establish an orbital/source/noise device regime or an arbitrary-gauge active logical gate.

## 1. The useful structural distinction

A symmetric STAR protects its logical multiplicity exactly from an invariant charge apparatus. An equilateral layout does not make its charge density immune to arbitrary external fields. A neighboring leaked charge can couple to an outer-site standard charge mode, and that mode can act nontrivially on the low-energy logical doublet.

The strongest opening found here is different: remove the gapless transverse electrostatic mode by screening on both sides of the charge layer, and provide the desired interaction through an explicit symmetric circuit mode. The unwanted direct interaction then has an exponentially summable, **full-Fock** incident norm. Its bound does not require the other blocks to be in the code, the gauge to be cold, or even the local operation to preserve particle number. The intended circuit mode is a separate retained resource, with a mandatory capacitance term and a finite-energy qualification when symmetry is imperfect.

The screened interaction is not a switchable density edge. It remains present throughout the source, gate, return, sensing, routing and renewal operations; the bound multiplies their full duration.

## 2. Exact S3 decomposition of the actual capacitance matrix

Site 0 is the center. The three outer sites have positions

\[
 r_i=a u_i,\quad u_i=(\cos(2\pi(i-1)/3),\sin(2\pi(i-1)/3)),\quad i=1,2,3.
\]

Every site is one orbital with two spin modes. On the full local Fock space, n_i has spectrum {0,1,2}; no fixed particle number is imposed on a leaked neighbor. For two modules, let

\[
 H_{AB}=n_A^T V_{AB}n_B,\qquad
 (V_{AB})_{ij}=v(|R_{AB}+r_{Bj}-r_{Ai}|).
\]

Identical extended orbital charge profiles replace each entry by its corresponding convolution. The symmetry assertions remain exact when the profiles and dielectric boundaries respect the site permutations.

On density vectors the independent outer-site averages are

\[
 T=\operatorname{diag}(1,J_3/3),\qquad F=I-T.
\]

The independently S3-invariant term is n_A^T(TVT)n_B. It is a polynomial in n_c and N_o on each side. Schur's lemma makes every such operator I_L tensor a gauge operator on the spin-zero standard isotypic sector. This is true on one valid module even when the other module, the other gauges, and the retained memory are arbitrary. It is the appropriate strong harmless term during an exactly invariant idle or gauge operation.

The remaining coefficient matrix is

\[
 W=V-TVT=FV+TVF.
\]

This includes standard-invariant and invariant-standard terms, as well as the standard-standard interaction. Keeping only FVF misses charge-dependent logical fields.

### Baseline voltages are an operation

Write x_i=n_i-1. Then

\[
 n_A^TWn_B=x_A^TWx_B+x_A^TW1+1^TWx_B,
\]

because 1^TW1=0. The last two terms are known static, generally asymmetric one-body voltages. Removing them requires actual compensation or a geometry that cancels their full lattice sum. The code reports both centered and uncompensated norms. A square lattice does not automatically supply the cancellation.

The exact centered full-space norm is

\[
 \|x_A^TWx_B\|=\max_{x,y\in\{-1,0,1\}^4}|x^TWy|
 =\max_{x,y\in\{-1,1\}^4}|x^TWy|.
\]

The second equality follows by maximizing a bilinear function over each cube in turn. It reduces the occupation calculation to 16 by 16 vertices. The uncompensated norm uses n_i in {0,2} at those vertices. Spin multiplicities do not alter a diagonal density norm.

## 3. Why a dipole survives

The two outer standard charge modes carry an in-plane dipole. The standard representation E satisfies E tensor E containing E, so symmetry alone does not force their projection into an E logical doublet to vanish. The executable Hubbard check confirms that it does not vanish at nonzero central detuning.

A neighboring particle-number change produces a monopole field. Its leading coupling to the valid module's standard dipole is proportional to a times the gradient of v. With one ground plane this is order Kh^2 a/R^4. It is not automatically quadrupolar.

If the neighbor is guaranteed to keep total N=4, an invariant center-versus-uniform-outer charge redistribution has zero monopole and zero dipole; its variable field starts at quadrupole order. That restricted improvement cannot be used for arbitrary particle-loss and particle-gain leakage. Nor does zero mean dipole establish zero dipole operator or no transition into a different gauge/irrep sector.

## 4. A general STAR gradient bound

Let G(r) bound the magnitude of the radial kernel gradient for distances at least r. If the module centers are R apart, R>2a, then

\[
 \sum_{ij}|W_{ij}|\le16\sqrt3\,a\,G(R-2a).
\]

To prove it, one outer-row averaging difference is bounded by the mean of the three corresponding potential differences. The two nonzero chord lengths are both sqrt(3)a, so a row difference is at most 2sqrt(3)aG/3. There are three outer rows and four columns. This gives 8sqrt(3)aG for FV. The nonnegative doubly stochastic projection T contracts the entrywise l1 norm, giving the same contribution for TVF. The centered density norm is at most the coefficient l1 norm. The uncompensated density norm is at most four times it.

For charge profiles supported within radius ell of their site centers, replace R-2a by R-2a-2ell. This follows by integrating the same pointwise finite-difference inequality. A Gaussian is not compactly supported; the compact-support statement must not be applied to a Gaussian merely by naming its width.

### A full-gate repair when the active drive breaks S3

An asymmetric hopping drive can mix S3 irreps. During such a gate, TVT need not remain logically harmless. If a valid block keeps N=4 throughout, subtract only the exactly harmless monopole term nu N_A N_B, where nu=(1^TV1)/16. Set P=J_4/4. The remaining matrix is V-PVP, and the same argument gives

\[
 \|x_A^T(V-PVP)x_B\|\le12(1+\sqrt3)aG(R-2a).
\]

The sum of all ordered site-pair distances within one STAR is 6(1+sqrt(3))a; each averaging half contributes this amount times G. This bound is only 1.183 times the S3-specific bound. It applies during number-preserving active gates without extending the idle subsystem theorem beyond its hypotheses.

Section 6 gives an even cleaner bound that makes no subtraction and covers changing local particle numbers as well.

## 5. One ground plane has a summable but algebraic tail

For a layer a height h above a grounded plane,

\[
 v_1(r)=K\left({1\over r}-{1\over\sqrt{r^2+4h^2}}\right),\qquad
 |v_1'(r)|\le {6Kh^2\over r^4},\quad K={e^2\over4\pi\epsilon}.
\]

On a square lattice with spacing d>2a, each max-norm shell m has 8m modules and center distance at least dm. Thus the centered full-charge S3 residual obeys

\[
 \kappa_{S3,1}\le{768\sqrt3 Kh^2a\,\zeta(3)\over(d-2a)^4}.
\]

There is no system-size divergence. However, its action remains kappa times the full exposure duration. The earlier direct-refocusing calculation shows why geometry dilution alone can make a directly capacitive gate unusably slow: it suppresses the desired edge too.

## 6. Two-sided screening supplies exponential full-state locality

Place the layer at z=0 between grounded planes z=+h and z=-h. The electrostatic Green kernel is

\[
 v_2(r)={2K\over h}\sum_{m=0}^{\infty}K_0(q_mr),\qquad
 q_m={(2m+1)\pi\over2h}.
\]

Equivalently, its in-plane Fourier transform is (2pi K/k)tanh(kh). Separation of variables gives the displayed positive K0 expansion. Poisson summation of the alternating image lattice gives the same coefficient. The free-space small-r limit is K/r and fixes the normalization. The code independently checks the alternating-image partial sums against their elementary alternating-series tail bounds.

Let

\[
 G_2(r)={2K\over h}\sum_{m\ge0}q_m K_1(q_mr),\qquad q_0={\pi\over2h}.
\]

The positive integral representations of K0 and K1 imply, for s>=r,

\[
 v_2(s)\le e^{-q_0(s-r)}v_2(r),\qquad
 G_2(s)\le e^{-q_0(s-r)}G_2(r).
\]

Consequently the centered S3 residual satisfies the all-shell bound

\[
 \boxed{\kappa_{S3,2}\le
 {128\sqrt3 aG_2(d-2a-2\ell)\over(1-e^{-q_0d})^2}.}
\]

The monopole-only subtraction replaces 128sqrt(3) by 96(1+sqrt(3)). Uncompensated one-body voltages can be retained by multiplying those gradient bounds by four.

### Stronger bound with no harmless-part subtraction

Every V_ij is nonnegative. Therefore, on the entire local Fock spaces,

\[
 \|H_{AB}\|=4\sum_{i,j}V_{ij}
 \le64v_2(R-2a-2\ell).
\]

All sites doubly occupied attain the equality in the first expression. Summing shells gives

\[
 \boxed{\kappa_{\rm all}\le
 {512v_2(d-2a-2\ell)\over(1-e^{-q_0d})^2}.}
\]

This is the safest full-operation bound. It does not rely on either module being valid, a symmetry-preserving active control, cold gauges, baseline compensation, or fixed module particle number. It includes all incident neighbors, including those already leaked or interacting with source/renewal apparatus. In a tightly screened geometry this unprojected bound can be numerically stronger than the gradient bound, because a displacement a is not small compared with the screening length.

The unprojected bound also has a useful extension beyond site-density Hubbard interactions. Suppose every active module contains at most N_max electrons, all confined to a physical region of radius R_mod. The first-quantized interaction is the positive multiplication operator sum over its N_A N_B electron pairs of v_2(|r_e-r_f|). Every pair separation is at least R_AB-2R_mod, so

\[
 \|H_{AB}\|\le N_{\max}^2v_2(R_{AB}-2R_{\rm mod}),\qquad
 \kappa_{\rm all}\le{8N_{\max}^2v_2(d-2R_{\rm mod})\over(1-e^{-q_0d})^2}.
\]

This remains true with arbitrary internal orbitals, spin states, coherent tunneling paths and internal charge leakage. It does not require each orbital to retain compact support around its individual site during a control pulse. Taking N_max=8 and R_mod=a+ell recovers the displayed one-orbital bound. The source/transfer interaction region must be included if it extends outside the module. An infinite reservoir, unbounded particle accumulation or uncontrolled wavefunction tails are not covered by naming a finite module: a real allowed-domain or energy-constrained source bound is then necessary.

For an operation of full duration T_full,

\[
 \eta_{\rm direct}\le\kappa_{\rm all}T_{\rm full}/\hbar.
\]

An arbitrary retained history or strong invariant source conjugates these bounded interactions but does not change their norms. This supplies an incident Hamiltonian-strength bound, rather than merely a low-energy matrix element. Translating it into a many-location accuracy theorem still uses the stated local Hamiltonian/fault model and the supplied correction and leakage-reduction operations.

### Finite-shell computations

The executable code computes exact finite occupation maxima for shells through M, then adds the analytic remaining-shell bound

\[
 128\sqrt3 aG_2(d(M+1)-2a)
 \left[{M+1\over1-q}+{q\over(1-q)^2}\right],\quad q=e^{-q_0d},
\]

for the centered S3 residual. The analytic formula for kappa_all does not need a finite-shell numerical maximization. Numerical evaluations use ordinary floating point; no directed-rounding enclosure is claimed.

## 7. A real symmetric voltage port with nonvanishing local coupling

The upper boundary contains a circular electrode patch of radius b centered over a STAR. Its voltage V is supplied by an explicit circuit port; the rest of the upper boundary and the lower boundary are grounded. In the quasi-static model, the potential at the midplane is V alpha(r), with

\[
 \alpha(r)=b\int_0^\infty
 {J_1(kb)J_0(kr)\over2\cosh(kh)}\,dk.
\]

This follows from the Fourier solution of Laplace's equation with top boundary data and zero lower boundary data. A circular patch is more symmetric than S3: all outer lever arms equal alpha(a), and the center lever arm is alpha(0). The charge coupling is

\[
 eV[\alpha(0)n_c+\alpha(a)N_o].
\]

On fixed N=4, the nonconstant part is eV[alpha(0)-alpha(a)]n_c. On arbitrary particle-number sectors it remains S3 invariant. The physical voltage port therefore preserves the exact subsystem theorem, and its local contrast is independent of the module spacing d.

One can increase d to reduce direct cross-talk without suppressing this local lever arm. The guided circuit, however, still has a mode capacitance, propagation delay, loss, mode crowding and loading cost. A single resonator shared by indefinitely many modules cannot be assumed to retain its zero-point voltage as its total capacitance grows. Regional fixed-degree buses, their switches and routing operations, or an explicit scaling circuit model are needed for a scalable claim.

### The capacitance counterterm is mandatory

For one circuit conductor, let alpha be its unit-voltage weighting potential and C its electrostatic capacitance. With all conductors grounded, the internal charges induce Q_D=-integral rho alpha on the patch. For a free conductor charge Q, the actual voltage is (Q-Q_D)/C. The field-energy decomposition is

\[
 H_{\rm electrostatic}=H_{\rm Dirichlet}
 +{[Q-Q_D(n)]^2\over2C}.
\]

The grounded Green energy and the harmonic boundary field are orthogonal in the electrostatic energy integral. This proves the expression without assuming an arbitrary independently tunable charge-resonator interaction. A conductor network replaces the square by one half (Q-Q_D)^T C^{-1}(Q-Q_D).

Expansion supplies both a linear charge-circuit coupling and the Q_D^2/(2C) term. Their strengths are linked. The latter includes cross-module interactions and local charging corrections. For the symmetric patch, every Q_D is a function of n_c and N_o, so all these terms are exactly identity on idle logical factors. During an asymmetric active gate their effect must be included in the actual gate Hamiltonian. A resonantly driven longitudinal protocol may control the resulting phase; dropping the capacitance term is not a physical-interface derivation.

## 8. Finite screening penetration retains a structural gap

An ideal plane is not the only mathematical boundary with exponential locality. Consider the local passive Robin boundary condition

\[
 \phi+\lambda\partial_n\phi=0\quad\text{at }z=\pm h,\qquad0\le\lambda<\infty.
\]

For a dielectric surface with local capacitance density C_s to a grounded reservoir, lambda=epsilon/C_s is the corresponding electrostatic length. It also approximates finite penetration into a thick screening medium in the appropriate long-wavelength regime. It is a physical boundary model to justify, not a blanket replacement for every thin metallic film.

The even transverse modes have q_n in (n pi/h,(n+1/2)pi/h] determined by

\[
 q_n\tan(q_nh)=1/\lambda.
\]

Writing L_n=h+sin(2q_nh)/(2q_n), the midplane kernel is

\[
 v_\lambda(r)=2K\sum_{n\ge0}{K_0(q_nr)\over L_n}.
\]

Every finite nonnegative lambda has q_0>0. The same full-Fock incident theorem holds with this kernel and q_0. Thus a finite screening penetration changes the exponential length continuously; it does not introduce an arbitrarily assigned small residual.

The driven-patch solution changes to

\[
 \alpha_\lambda(r)=b\int_0^\infty
 {J_1(kb)J_0(kr)\over2[\cosh(kh)+\lambda k\sinh(kh)]}\,dk.
\]

The source lever arm and shielding length are therefore computed in the same boundary model. The Neumann limit lambda=infinity is different: q_0 closes. A gapless electrostatic escape channel, an unmodeled opening or feed, or a thin-screen response with a different low-wave-number law requires a new Green-function bound. Ideal-plane formulas cannot be extrapolated to those cases.

## 9. Charging energy and source changes come from the same model

For a normalized in-plane Gaussian charge density with Fourier transform exp(-ell^2 k^2/4),

\[
 U_{\rm on}=K\int_0^\infty e^{-\ell^2k^2/2}\tanh(kh)\,dk.
\]

For ell much smaller than h this is

\[
 U_{\rm on}=K\sqrt{\pi/2}/\ell-K\ln2/h+O(K\ell^2/h^3).
\]

The leading image correction is finite. Bringing screens from infinity to h of order a need not suppress a local charging energy whose orbital radius is much smaller than a. Also

\[
 0\le\partial_h U_{\rm on}\le K\ln2/h^2,
\]

since the density form factor is at most one. A common h perturbation changes the charging scale and source timing; differences across the three outer orbitals also break S3 and cannot be absorbed into a harmless common U.

For an arbitrary nonnegative normalized charge density supported within radius ell, the unscreened pair separation is at most 2ell, while the image correction is at most K ln2/h. Hence

\[
 U_{\rm on}\ge {K\over2\ell}-{K\ln2\over h}.
\]

This conservative lower bound is independent of the detailed radial profile. Identical profiles on the four sites give a common U and the exact symmetric mutual coefficients V_c, V_o, bounded above by v_2(a-2ell) and v_2(sqrt(3)a-2ell).

At fixed N=4, relative to charge pattern 1111, the five possible charging excitation energies are

| Charge type | Excitation energy |
|---|---|
| Center doublon, one outer hole | U_c+epsilon+V_c-2V_o |
| Center hole, one outer doublon | U_o-epsilon-3V_c+2V_o |
| Outer doublon and outer hole | U_o-V_o |
| Center and one outer both doubled | U_c+U_o+epsilon+V_c-3V_o |
| Two outer doublons, center empty | 2U_o-epsilon-3V_c+V_o |

Their minimum is the zero-hopping charge gap Delta. This exposes how a source detuning or a resonator voltage can close the relevant gap. A quantum oscillator with unbounded voltage amplitude cannot simply be placed into a fixed detuning box.

### A conditional low-energy charge-leg bound

For equal center-to-outer hopping t, the N=4 hopping operator has norm v=2sqrt(3)|t|. The coupling from the singly occupied spin-zero doublet to the charge-excited subspace has norm w=sqrt(6)|t|. If Delta>v, the isolated low-energy E doublet projector P obeys

\[
 \|(I-P_{1111})P\|\le{r\over\sqrt{1+r^2}},\qquad
 r={w\over\Delta-v}.
\]

The block eigenvalue equation proves it: the excited block is at least Delta-v, while the two low eigenvalues are nonpositive relative to the singly occupied energy. The off-diagonal block maps the reference doublet with norm w. Moreover,

\[
 \|(n_i-1)P\|\le\|(I-P_{1111})P\|.
\]

This bounds leakage-transition amplitudes as well as the projected logical density. It is stronger than a P n_i P calculation, but it is **not** uniform on arbitrary gauge histories in the full standard isotypic sector. A symmetric source can excite the gauge while preserving the logical factor. Once it does, the low-energy charge-leg bound cannot be reused without a supplied gauge-renewal or energy-confinement argument.

## 10. Numerical electrostatic regions, with their precise scope

The runnable fixture takes a=K=1, h=.5, Gaussian ell=.2 for the onsite estimate, and a circular source patch b=.5. It gives

\[
 U=4.944573063,\quad V_c=0.1181650523,\quad V_o=0.00911805055,
\]

\[
 \alpha_c=0.254648200,\quad\alpha_o=0.0305059462,
 \quad\alpha_c-\alpha_o=0.224142254.
\]

The intersite fixture uses point charges. It is a transparent comparison model, not a self-consistent wavefunction/tunneling calculation.

| d/a | Centered S3 row kappa/U, finite shells plus analytic tail | Action for UT_full/hbar=10^5 |
|---|---:|---:|
| 6 | 2.06612e-6 | 0.206612 |
| 7 | 8.23893e-8 | 0.00823893 |
| 8 | 3.32250e-9 | 0.000332250 |
| 9 | 1.35117e-10 | 0.0000135117 |
| 10 | 5.53104e-12 | 0.000000553104 |

For d=10a, the unprojected all-shell bound of section 6 gives action 1.25317e-4 in the point model. Replacing the minimum separation by d-2a-.4a gives 4.51639e-4 for charge profiles with support radius .2a. This latter support statement is separate from the Gaussian estimate.

A completely compatible, conservative **electrostatic** region uses h=.5a, d=10a and identical profiles supported within ell=.1a. It supplies

\[
 U\ge3.61370564K/a,\quad V_c\le0.246459321K/a,
 \quad V_o\le0.0181271322K/a.
\]

For |epsilon|<=.4U the charging gap obeys Delta>=.395396U. The patch contrast is at least .206448, and the full unprojected direct-interaction action is at most 3.25468e-4 for UT_full/hbar<=10^5. The patch contrast bound uses radial monotonicity of the slab Poisson kernel and places the center charge at radius ell and the nearest outer charge at a-ell.

This region does not supply a hopping amplitude or operation duration. A compact orbital, its tunnel barrier, its excited orbital gap, the resonator, the fresh-electron source and the meter must give a common physical realization. In particular, assuming both a very narrow orbital and t/U=.1 without deriving the barrier physics would recreate the missing bridge. The mathematical consequence is that **once a finite operation time is actually supplied**, shielding distance need grow only logarithmically in that time or the requested direct-coupling tolerance, while the local circuit lever arm stays finite. Holding and source noise remain charged for the full time.

## 11. Finite symmetry error and the unbounded-source obstruction

A lateral displacement delta s of the nominally centered source patch gives outer coefficients

\[
 \delta\alpha_i=-\alpha'(a)\,u_i\cdot\delta s+O(|\delta s|^2).
\]

The first-order average is zero. For three equilateral directions, sum_i |u_i dot delta s|<=2|delta s|. The exact density norm for a zero-sum voltage pattern is its l1 coefficient norm, so

\[
 \|E_{\rm asym}\|\le2e|V_{\rm zpf}|\,|\alpha'(a)|\,|\delta s|\,\|X\|+O(|\delta s|^2).
\]

In the fixture alpha'(a)=-.1065092713/a. Relative to e V_zpf[alpha_c-alpha_o], the first-order full-Fock coefficient is .950372 |delta s|/a times the quadrature norm.

For a truly arbitrary initial oscillator state, ||X|| is unbounded. No nonzero symmetry error then has a finite uniform operator-norm tolerance. Exact S3 supports arbitrary retained bus histories; finite departures need an actual energy/quadrature domain, preparation/renewal/monitoring, or an energy-constrained error theorem. The bounded local electronic Fock space is why the direct Coulomb theorem is fully state uniform. It does not automatically qualify an unbounded voltage source.

Electrode dissipation is another independent source. Static screening does not imply noiseless metallic boundaries. Johnson noise and the conductor's dynamic Green function must enter the source/holding model. A local Robin electrostatic model establishes a spatial Green-function gap, not a bound on its dissipative spectrum.

## 12. Prior machinery and implication

Two-metal-gate exponential screening is established electrostatics. Koulakov and Shklovskii explicitly use the exponentially screened two-gate interaction in their Wigner-island analysis: [arXiv:cond-mat/9707204](https://arxiv.org/abs/cond-mat/9707204). The K0 kernel, normalization, finite-support bounds and full-occupation incident laws above are derived here.

Symmetric central electrical coupling is also established machinery. Friesen and collaborators' charge-quadrupole construction couples the center gate to a resonator while preserving outer reflection symmetry, and distinguishes dipolar leakage from protected logical behavior: [arXiv:1605.01797](https://arxiv.org/abs/1605.01797). The present role is to combine an independently invariant S3 source with a full-leakage, full-duration direct-interaction bound. It does not claim priority for symmetric gates, resonator coupling or metallic shielding.

The source-noise qualification follows the known electromagnetic fluctuation issue. Premakumar, Vavilov and Joynt derive geometry- and conductivity-dependent evanescent-wave Johnson noise and discuss the limits of local response: [arXiv:1705.01165](https://arxiv.org/abs/1705.01165). No numerical Johnson-noise floor is inferred here without specifying the materials, temperature, frequency range and finite orbital averaging.

The new organising statement is: **a positive transverse electrostatic gap can give a size-independent full-leakage interaction budget, while an explicitly supplied symmetry-preserving circuit port retains a finite local source lever arm.** It removes the need to posit a small inactive Coulomb edge. It does not supply a complete source, a universal arbitrary-gauge active gate, or a complete physical advantage.

## Executable work

Run `python p2_physical_bridge/coulomb_leakage/star_geometry.py` from the workspace root. It writes `star_geometry_results.json`, checks the exact occupation-cube reduction, verifies the image/Bessel normalization, computes finite-shell sums and analytic tails, evaluates patch lever arms and Robin screening modes, and checks the low-energy charge-leg distinction using the root STAR representation. Earlier files are read only.
