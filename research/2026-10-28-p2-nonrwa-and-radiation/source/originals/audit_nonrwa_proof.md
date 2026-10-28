# Independent audit of the positive-spring, non-RWA embedded pair

27 October 2026. The infinite-Fock sector-gap argument, exact fourth-order functional, large-W expansion, and the strengthened own-rail positivity theorem for every W>8 pass this independent audit. The sign conclusion is for the fourth-order coefficient and hence sufficiently small nonzero coupling at each fixed W; it is not an arbitrary-finite-g theorem.

## Stable positive local Hamiltonian

The declared spring matrix has diagonal W squared, nearest leg entries -W, and rung entries -4W. It is assembled from positive leg springs W, rung springs 4W, and ground springs W squared minus 6W, with an extra W at each endpoint for its missing leg. Its exact bath-frequency bands are

\[
A_l=[\sqrt{W^2-6W},\sqrt{W^2-2W}],\qquad
A_h=[\sqrt{W^2+2W},\sqrt{W^2+6W}].
\]

Quantizing the specified coordinate interaction gives parity-mode couplings `(t+s) sqrt(W/omega)` and `(t-s) sqrt(W/omega)`, with the spin transition signs used in the root code. This was checked independently by diagonalizing the real-coordinate matrix and applying physical L/R spin flips.

After omitting the infinite additive zero-point constant, H0=W(nL+nR)+dGamma(omega). The bath has mass m=sqrt(W squared minus 6W)>0. Endpoint field form factors and their inverse-frequency weighted norms are finite. The interaction is infinitesimally H0-bounded. Thus H(g) is self-adjoint on D(H0), semibounded, and an analytic family for small g. No photon cutoff enters this operator argument.

## Exact symmetry-sector gap and global embedding

Excitation parity Pi=(-1)^(nL+nR+Nph) and simultaneous memory/rail exchange S are conserved without making a rotating-wave approximation. The bare pair has (Pi,S)=(+,+).

At g=0, its allowed two-photon continua use two lower or two upper photons, while mixed-band photons have S=-. A one-spin-plus-one-photon state in the pair sector uses the symmetric spin with a lower photon or the antisymmetric spin with an upper photon. These spectra avoid 2W. For W>8, four photons cost at least 4m>2W; three photons plus one spin cost at least W+3m>2W; two photons plus the spin pair are still higher.

The bare pair is therefore a simple isolated eigenvalue in its invariant sector, with a sufficient free gap

\[
\delta_0=\min\{\sqrt{W^2+2W}-W,\;4\sqrt{W^2-6W}-2W\}>0.
\]

The omitted distances are larger when W>8. Analytic isolated-eigenvalue perturbation in that sector gives the exact pair branch for sufficiently small |g|. The ground and two one-spin branches likewise persist in their own symmetry sectors.

The mixed-band sum A_l+A_h contains 2W strictly. At small g, two opposite-parity photon packets translated far from the endpoint, acting on the dressed ground state, produce Weyl sequences at Eg+A_l+A_h in sector (Pi,S)=(+,-). Endpoint interaction errors vanish as the packets escape. The massive finite-field model supplies the boson-number regularity required for these Weyl sequences; it can also be established by a finite-particle graph-core approximation and diagonal limit. Since Ep-Eg=2W+O(g squared), the pair remains inside that opposite-sector essential spectrum for small g. It is thus globally embedded and exactly protected by symmetry.

This bath is massive. It has a continuum at the pair transition energy but does not retain arbitrarily low-frequency modes of the earlier model.

## Exact fourth-order functional

For positive-frequency parity measures eta_plus and eta_minus, separated from the spin frequency epsilon and satisfying the needed integrability, put delta=eta_plus-eta_minus and C(w)=1/(epsilon squared minus w squared). Define

\[
G=\int wC(w)d\delta(w),\quad H=\int C(w)^2d\delta(w),\quad
J=\iint\frac{C(w)C(v)}{w+v}\,d\delta(w)d\delta(v).
\]

The connected energy is Ep+Eg-Eplus-Eminus. Its second-order term cancels, and its fourth-order coefficient is

\[
\boxed{\chi_4=8\epsilon^2GH-4\epsilon^2J.}
\]

This was independently derived from fourth-order paths, including normalization subtraction, zero-photon middle states, and two-photon middle states. The symmetrized same-parity kernel is

\[
\mathcal K(x,y)=4\epsilon^2C(x)C(y)
\left[xC(y)+yC(x)-\frac1{x+y}\right],
\]

while the cross-parity coefficient is -2 times this kernel, giving the quadratic form in delta. The appendix below records the path identity, and `audit_kernel_identity.py` proves the rational identities exactly with rational arithmetic and polynomial interpolation. This is an exact algebra certificate, not a float fit.

## Own-rail exact identity and positivity for every W>8

Set s=0, epsilon=W, u in [1,3], rho(u)=(2/pi)sqrt(1-(u-2) squared), and a=integral rho(u)/u du=4-2sqrt(3). The frequencies are omega_l,h=sqrt(W squared minus/plus 2Wu), with measures eta_l,h=t squared rho W/omega_l,h. The signed measure z=delta C is positive on both bands. Direct algebra gives

\[
G=t^2a,\qquad
H=t^2\int\frac{\rho(u)}{u(\omega_l+\omega_h)\omega_l\omega_h}\,du.
\]

Let A=1+y squared and

\[
F_W(y)=\int_1^3\frac{\rho(u)}u\frac{A}{A^2-4u^2/W^2}\,du.
\]

All following y integrals are over [0,infinity). The identity

\[
\frac1{\omega\nu(\omega+\nu)}=
\frac2\pi\int_0^\infty\frac{d\xi}{(\omega^2+\xi^2)(\nu^2+\xi^2)}
\]

yields

\[
H=\frac{2t^2}{\pi W^3}\int_0^\infty\frac{F_W(y)}A\,dy,
\qquad J=\frac{2t^4}{\pi W^3}\int_0^\infty F_W(y)^2\,dy.
\]

Completing the square, using integral A to minus two dy=pi/4, proves exactly

\[
\boxed{\chi_4(W)=\frac{2t^4a^2}{W}
-\frac{8t^4}{\pi W}\int_0^\infty
\left[F_W(y)-\frac aA\right]^2dy.}
\]

The remainder integrand is positive and

\[
0\le F_W(y)-\frac aA
=\frac4{W^2}\int_1^3\frac{\rho(u)u}{A(A^2-4u^2/W^2)}du
\le\frac8{W^2-36}A^{-3}.
\]

The inequality uses integral rho(u)u du=2 and A>=1. Since integral A to minus six dy=63pi/512, the claimed bound follows:

\[
\boxed{\chi_4(W)\ge\frac{t^4}{W}
\left[2a^2-\frac{63}{(W^2-36)^2}\right]>0
\quad\text{for every }W>8,\ t\ne0.}
\]

At W=8 the bracket already exceeds 0.49, so there is no hidden borderline sign issue. Combined with the symmetry-sector existence theorem, this proves an interacting exact embedded pair for every fixed W>8 and sufficiently small nonzero g, using only own-rail ports. No extrapolation from floating data is needed.

The same exact identity gives

\[
\chi_4(W)=\frac{2a^2t^4}{W}-\frac{63t^4}{W^5}+O(W^{-7}).
\]

The first correction has coefficient 63 because the leading square is 64 A to minus six divided by W to the fourth. The RWA-only coefficient for this spring bath is 4a t to the fourth divided by W cubed plus O(W to minus five). Thus counter-rotating contributions dominate the deliberately cancelled own-rail interaction at large W. The old exactly reflected RWA bath and this physical spring bath are distinct Hamiltonians.

## Numerical scope and physical qualifications

`audit_nonrwa.py` uses the real-coordinate matrix, physical L/R spins, and all photon states needed for fourth-order perturbation. Two photons suffice for fourth order since a four-vertex path returning to vacuum cannot have more than two photons at its middle. It reproduces the root coefficients independently. At W=12 and 16 sites per rail the calibrated coefficient is 0.601916105149639. For own-rail ports at W=400, W chi_4 is 1.21948833035 versus the asymptotic 1.21948833553 for the chosen t.

The infinite-Fock theorem comes from the operator argument, and positivity from the analytic bound. A truncated finite-g diagonalization does not provide a continuum finite-time error certificate. No explicit g radius has been bounded here.

The positive local spring bath is established for the declared oscillator model. Exact two-level memories and their transverse coordinate couplings remain assumed components. This is not yet a full Maxwell/gauge-derived device model. External radiation, extra device modes, noise, finite-time loading, pulse errors, calibration, and the costs of large W remain open. The result supplies an ideal interacting embedded eigenstate; practical advantage over an ordinary accessible band-gap comparator has not been established.

## Appendix: independent path-algebra certificate

Put d_x=1/(epsilon-x), s_x=1/(epsilon+x), r=x+y. For two photons in the same parity channel, the normalization, zero-photon-middle, and two-photon-middle contributions to the connected symmetrized kernel are respectively

\[
N_s=\tfrac12(d_xs_y^2+d_ys_x^2-s_xd_y^2-s_yd_x^2),
\qquad Z_s=(d_xd_y-s_xs_y)/(2\epsilon),
\]

\[
T_s=\tfrac12\left[(d_x+d_y)^2\left(\frac1{2\epsilon-r}-\frac1r\right)
-(s_x+s_y)^2\left(\frac1r+\frac1{2\epsilon+r}\right)
+\frac{(d_x-s_x+d_y-s_y)^2}{r}\right].
\]

Their sum equals K(x,y). For opposite parity the contributions are

\[
N_c=s_xs_y^2+s_ys_x^2-d_xd_y^2-d_yd_x^2,
\qquad Z_c=-(d_xd_y-s_xs_y)/\epsilon,
\]

\[
T_c=4\epsilon^2(C(x)^2+C(y)^2)/r.
\]

Their sum is -2K. Both identities are certified by `audit_kernel_identity.py`. Multiplying by

\[
D=\epsilon r(2\epsilon-r)(2\epsilon+r)
(\epsilon-x)^2(\epsilon+x)^2(\epsilon-y)^2(\epsilon+y)^2
\]

produces homogeneous numerator polynomials of total degree 9, because D has degree 12 and the kernels degree -3. Homogeneity sets epsilon=1. Exact vanishing at a 10-by-10 Cartesian grid of distinct x,y points where D is nonzero proves that each polynomial is identically zero. The executable uses only exact rational arithmetic.

## Appendix: independent large-carrier expansion

Let p=(t+s) squared, q=(t-s) squared, b=4/sqrt(3)-2. Dispersion and oscillator-normalization corrections to the RWA interaction yield

\[
ab(p^2-q^2)+\frac{b}{2W}(p-q)^2+O(W^{-2}).
\]

A Schrieffer-Wolff elimination of the counter-rotating vertices supplies

\[
\frac1{2W}\left[-b(p-q)^2+a^2(p+q)^2\right]+O(W^{-2}).
\]

For example, the order-g-squared coefficient in the expectation of its effective operator is -b(p squared+q squared)+2a squared p q for the dressed pair, -b p q-a squared p squared for the symmetric single branch, and -b p q-a squared q squared for the antisymmetric branch. Their connected difference is the displayed bracket. The two b terms cancel between the RWA dispersion correction and the counter-rotating correction. This independently recovers

\[
\chi_4(W)=ab(p^2-q^2)+\frac{a^2}{2W}(p+q)^2+O(W^{-2}).
\]
