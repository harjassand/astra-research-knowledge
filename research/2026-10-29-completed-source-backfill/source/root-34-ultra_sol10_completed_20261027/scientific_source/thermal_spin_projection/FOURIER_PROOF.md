# Full transfer-spin extraction and paid angular error

The history rotation acts as R^tensor(k) on k Cartesian event labels.
Spin2 covariance of G_alpha=iS_alpha implies that J_beta commutes with it.
Only integer SO(3) spins occur; the equivalent SU(2) central action is trivial.
For even p>=2 the compact self-adjoint decomposition is

    J_beta=direct_sum_s I_(2s+1) tensor B_s,
    m_s=Tr B_s^p>=0, sum_s(2s+1)m_s=f_p(0)<infinity.

The twisted cycle identity gives

    f_p(phi)=Tr(U_phi J_beta^p)=Z_p(beta,phi)/5^p
             =sum_s chi_s(phi)m_s,
    chi_s(phi)=sum_(a=-s)^s exp(i a phi).

Absolute uniform convergence follows from |chi_s|<=2s+1. Therefore

    A_m=(1/2pi)integral f_p(phi)exp(-im phi)dphi
        =sum_(s>=|m|)m_s,
    m_s=A_s-A_(s+1).

These are SOURCE transfer spins, not physical total-spin sectors of the
small cycle. They are unbounded even for a six-site physical trace.

The literal physical seam is SzSz+exp(i phi)S+S-/2+exp(-i phi)S-S+/2.
An incoming/outgoing convention may replace phi by-phi, but inverse rotations
are conjugate in SO(3), so their traces are equal. Odd closure is derived
separately in ODD_PROOF.md; positivity here explicitly uses even p.

Write H(phi)=D+exp(i phi)E+exp(-i phi)E*, with ||E||=3. Then

    Re H(phi+iy)=H(phi)+(cosh y-1)(exp(i phi)E+exp(-i phi)E*).

The perturbation norm is at most6(cosh y-1). For Hermitian A,B,
|Tr exp(A+iB)|<=||exp(A+iB)||_1<=Tr exp A: apply Schatten Holder with
exponentm to the m factors of(exp(A/m)exp(iB/m))^m and pass to the Lie limit.
Hermitian eigenvalue monotonicity and f_p(phi)<=f_p(0) consequently give

    |f_p(phi+iy)|<=f_p(0) exp[6 beta(cosh y-1)].

This continuation uses the finite physical trace, not a bounded complex
history rotation. There is only a seam cost, no p-extensive energy prefactor.
Cauchy displacement implies A_m<=f_p(0)exp[6 beta(cosh y-1)-|m|y].

For N equally spaced angles and N>2s+1 the EXACT alias identity is

    mhat_s=m_s+sum_(l>=1)[m_(lN+s)-m_(lN-s-1)].

It is not positive-only aliasing. With C=f_p(0)exp[6 beta(cosh y-1)],

    mhat_s-C exp[-(N+s)y]/(1-exp[-Ny]) <=m_s
      <=mhat_s+C exp[-(N-s-1)y]/(1-exp[-Ny]).

For beta3,s1, independent Fraction arithmetic verifies errors relative to
f_p(0) of[-2e-11,+5e-10] forN32,y5/4, and[-2e-35,+6e-33] forN64,y2.
These scalar alias constants do not certify the physical trace samples.
Sample errors epsilon_k add N^-1 sum epsilon_k|cos(s phi_k)-cos((s+1)phi_k)|,
at most2max epsilon_k when trigonometric weights are exact.

The direct new physical constructor stores exact integer/sqrt6 sparse
parts D0,D1,E0,E1. All15625 states are included at each angle. Exact spin
inversion component checks justify positive-M multiplicity2. The largest
block has1751 states. The64-grid reads33 unique angles using proven phi->-phi
symmetry; the32-grid is its nested subset. Low Hamiltonian moments0--6 match
the old exact I/P source: a k-event closed word has winding degree floor(k/6),
so these moments are constant plus a cosine. Relative errors at powers2--6
are below1.53e-14; this is a construction check, not trace-exp validation.

At beta3, the numerical64-grid gives m_1,6=1.2685901800596822e33, radius
329018.4288883472. The current scalar lower322705.8515 gives ratio1.0195614.
The complete A5 triplet complement is the FULL A5 moment minus m1:
1.7369138705202685e30, only.13672966% of its mass. Its radius/theta is.33974745.
No high-spin tail is dropped. The complete split loop count is427.51 and
fails. The32/64 moments agree to3.28e-14 relative; this is not a certified
sample error estimate. No large certified angular grid was launched.

Rotations act as U_spin1 tensor I inside its multiplicity space. Further
rotational refinement cannot split those internal modes. This restriction
does not exclude better scalar references, time-frequency projection, higher
moments, other thermal methods, or the spin-two gap.
