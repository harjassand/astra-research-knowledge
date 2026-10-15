# Conditional limits for chemical-axis control

These are deductions under stated models. They are not a claim of mathematical novelty, a simulation of FeNiN, or evidence of a measured material response. `axis_limits.py` independently checks the lattice count and spherical integrals.

## 1. A label-preserving cycle cannot rewrite chemical order

Let a fixed metal-site registry be \(\Lambda\), with species labels \(s_r=+1\) for Fe and \(-1\) for Ni. For any ordering wavevector \(q\), define \(\eta_q=N^{-1}\sum_{r\in\Lambda}s_r e^{iq\cdot r}\). Suppose an insertion/extraction operation changes only interstitial nitrogen, leaves every \(s_r\) unchanged, and does not rotate the metal registry. Every \(\eta_q\) is then unchanged, so the direction of its chemical-order peak cannot change. Any composition of such operations has the same invariance.

For a fully ordered fcc parent, use half-cell integer coordinates \((i,j,k)\) with \(i+j+k\) even. The four parity classes are 000, 011, 101, and 110, equally populated in a periodic block. Perfect x layering has species label \((-1)^i\); perfect y layering has \((-1)^j\). They disagree on 011 and 101, exactly half the sites. A successful 90-degree rewrite at fixed registry therefore changes at least \(N/2\) metal-site occupations. If transport is represented by pair exchanges, at least \(N/4\) exchanges are needed. Changing the antiphase sign does not reduce this count.

This is an occupation-change count, not a lower bound on barrier energy or elapsed time. Collective motion, dislocations, vacancy transport, plastic lattice rotation and a reconstructive transformation require different transport accounting. In particular the reported FeNiN formation mechanism does permit metal rearrangement, so this theorem does **not** forbid nitrogen-assisted rewriting. It forbids obtaining it from an entirely label-preserving topotactic lock step or from spin rotation alone.

## 2. A common extraction step cannot manufacture missing control information

Bin the complete precursor state by orientation, phase, and degree of order, retaining an explicit null state for material without an ordered phase. Let \(p_x,p_y\) be distributions after the x- and y-directed interventions. Let \(K\) be a stochastic extraction/retention kernel applied identically to both.

\[
\|p_xK-p_yK\|_{TV}\leq\|p_x-p_y\|_{TV}.
\]

Proof: write \(d=p_x-p_y\). Then \(\sum_j|\sum_i d_iK_{ij}|\leq\sum_i|d_i|\sum_jK_{ij}=\sum_i|d_i|\). Divide by two. In particular, \(p_x=p_y\) implies identical outputs. Orientation-dependent survival can change a texture, but cannot create dependence on a control that left no difference in the complete input distribution.

For \(f(n)=n_x^2-n_y^2\in[-1,1]\), and \(f=0\) for the null phase, the unnormalized contrast obeys \(|E_{p_xK}f-E_{p_yK}f|\leq2\|p_x-p_y\|_{TV}\). Conditioning only on surviving ordered material can amplify a normalized contrast by discarding phase fraction. The contraction statement therefore concerns the complete state or a phase-weighted observable, not an artificially normalized subset.

## 3. Even a perfect three-variant selector cannot fully align random fixed cubic parents

Assume isotropic, volume-weighted parent crystal orientations and that only the parent's three orthogonal axes \(Re_1,Re_2,Re_3\) can become the chemical c-axis. The parent cannot rotate, recrystallize or adopt additional orientation relationships. For target unit vector \(e\), write \(u=R^Te\), uniform on the sphere. Pointwise, the best possible absolute projection is \(m(u)=\max_i|u_i|\); the best squared projection is \(m(u)^2\).

By the sphere's 48-fold sector symmetry, take azimuth \(0\leq\phi\leq\pi/4\), with z the largest coordinate and polar angle \(0\leq\theta\leq\arctan(1/\cos\phi)\). Exact integration over \(\theta\) gives

\[
E[m]=\frac6\pi\int_0^{\pi/4}\frac{d\phi}{1+\cos^2\phi}
=\frac{3\sqrt2}\pi\arctan\frac1{\sqrt2}\approx0.83119,
\]

\[
E[m^2]=\frac4\pi\int_0^{\pi/4}\left[1-\left(\frac{\cos\phi}{\sqrt{1+\cos^2\phi}}\right)^3\right]d\phi
=\frac13+\frac2{\pi\sqrt3}\approx0.70089.
\]

For the second integral, substitute \(v=\sin\phi\) in the subtracted term; its integral is \(\pi/6-1/(2\sqrt3)\). A remanence interpretation of the first moment additionally requires independent uniaxial moments relaxing along their chemical axes. It does not establish coercivity or energy product. The irregular orientation relationships in the measured massive nitridation transformation do not satisfy the assumed three-axis restriction, so this is a bound on a proposed cubic-variant bypass, not a universal FeNiN bound.

## 4. Planar texture is insufficient for a specified in-plane chemical axis

Consider the admissible null model \(n=(\cos\phi,\sin\phi,0)\), with uniform \(\phi\). Then \(Q=E[nn^T]=\operatorname{diag}(1/2,1/2,0)\), and \(Q_{xx}-Q_{yy}=0\). Thus observing c-axes in flake planes is consistent with no x-versus-y preference. The ideal absolute x projection is \(E|\cos\phi|=2/\pi\approx0.63662\). This is not asserted to be the distribution in the patent examples; it is a countermodel to the inference from planar confinement to a uniquely written axis. Additional measured azimuthal selection could defeat it.

## 5. A quantified selection benchmark without invented material constants

For one favored and two equivalent competing nucleation channels with equal attempt prefactors, let the unfavorable barrier exceed the favorable barrier by \(\Delta G^\ddagger\). Independent Poisson first-nucleus selection gives

\[
p_f=\frac1{1+2e^{-\Delta G^\ddagger/(k_BT)}}.
\]

Under this model, \(p_f\geq q\) requires \(\Delta G^\ddagger\geq k_BT\ln(2q/(1-q))\). At the published 300 C reference and \(q=0.9\), the threshold is about 0.143 eV per competing nucleus. For stress, the relevant barrier coupling is \(\sigma:\Delta\Omega^\ddagger\), an activation-volume tensor contraction; it cannot be obtained from a final tetragonal axial ratio.

If a weak, linear susceptibility description is valid at the reaction temperature, a magnetic free-energy bias has magnitude \(VB^2\Delta\chi/(2\mu_0)\). The corresponding combined product \(V\Delta\chi\) would need to exceed \(2\mu_0 k_BT\ln18/B^2\) under the same selection model. The program reports this product at specified fields, without assigning a nucleus size or susceptibility. Unequal prefactors, multiple nuclei, interface migration, strain accommodation and irreversible growth can invalidate this simple probability model. No FeNiN switching threshold is predicted.
