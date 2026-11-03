# Exact odd-Toeplitz orientation calibration (no eta expansion)

Conclusion for the existing code conventions:

  D=+sigma.p, P_+=1_(D>0),
  Index(P_+ U P_+ +1-P_+) = +(24pi²)^-1 integral tr(U^-1 dU)^3.

The geometric texture audit has the right side equal to -s. Therefore the actual Wilson-to-localizer bridge gives Q=-Index=+s at the code's w=0 face. Putting the same mass on the opposite face, or reversing the root chirality while retaining the declared spatial texture orientation, gives Q=-s. This sign is NOT inferred from the formal mass-gradient eta expansion.

## Primary local-index formula

Dai and Zhang, arXiv:math/0103230v2, define the positive-spectral Toeplitz operator in section1. Equation(2.15) defines the unnormalized odd form with degree-three coefficient1/6. Equation(2.16), specialized to empty boundary, flat tangent connection and trivial twist, gives

  Index = -(2pi i)^-2 (1/6) integral tr(U^-1dU)^3
        = +(24pi²)^-1 integral tr(U^-1dU)^3.

Their appendix proves the closed case through the cylinder APS operator, independently of any Higgs-mass eta series. The conventional oriented odd Clifford representation has i^((d+1)/2)c1...cd=I. In3D c_j=-i sigma_j satisfies this since c1c2c3=-I; thus D=sum c_j partial_j=+sigma.p. In1D c=-i similarly gives the familiar index -wind. The dimensional sign is in the factor(2pi i)^-2 and must not be extrapolated from1D by memory.

Primary source: https://arxiv.org/pdf/math/0103230 (equations2.15,2.16 and Appendix A).

## Independent explicit Bott-product calibration

This removes reliance on a hidden Clifford convention in the cited formula.

Use oriented coordinates(x,y,z). Choose a smooth rank-one projection P(y,z) in a sufficiently large trivial bundle over T² with

  integral_T² tr(P dP dP)=2pi i.

Such a projection is the usual degree-one Bott line bundle; stabilization does not affect the index. Define the unitary

  U(x,y,z)=e^(ix)P(y,z)+(1-P(y,z)).

This is a U(N), rather than SU(2), representative, which is sufficient to calibrate the local degree-three coefficient. Its lower odd Chern component cannot contribute on flat T³ since the degree-two A-hat component is zero.

Direct exterior algebra, using P dP P=0, gives

  U^-1dU=iP dx+(1-e^(-ix))P dP+(e^(ix)-1)(1-P)dP,
  integral_x tr(U^-1dU)^3=-12pi i tr(P dP dP).

Hence its normalized three-form integral equals+1.

Replace the flat connection by a smooth connection preserving the P and1-P summands, and on P choose curvature F=+i f dy wedge dz with constant f>0 and total flux f Area(T²)=2pi. This changes the elliptic Dirac operator only by a bounded zeroth-order term. Its positive projection changes by a compact operator, so the Toeplitz Fredholm index is unchanged; finite-dimensional zero-eigenvalue convention changes also do not affect it.

On the P summand the transverse operator is

  D2=sigma2 p_y+sigma3 p_z,
  [p_y,p_z]=-i f,
  D2²=p_y²+p_z²+sigma1 f.

The one-flux torus Landau problem has one lowest oscillator state. It produces one D2 zero mode with sigma1=-1, and no zero mode with sigma1=+1. All nonzero D2 levels occur in paired opposite eigenvalues because D2 anticommutes with sigma1.

Use AP boundary conditions in x. The full3D operator on that zero mode is D3=-p_x. Compression of e^(ix) to the positive spectrum of -p_x is the backward shift on negative Fourier modes: it has a one-dimensional kernel and no cokernel, hence index+1.

For a fully spectral-flow version of the same cancellation, use U^-1 D U=D+sigma1 on the P summand. Along D(t)=D+t sigma1, every nonzero transverse level gives eigenvalues +/-sqrt((n+1/2+t)^2+lambda²), so none crosses zero. The sole sigma1=-1 zero-mode branch crosses downward once. The Toeplitz index is minus this spectral flow (the sign is fixed by the ordinary positive-Hardy1D shift), again giving+1. On1-P, U=1 and the path is constant. Thus the Bott representative has Index=+1 and W3=+1 exactly.

The result extends to the SU(2) texture by the local odd-index theorem / stable K1 pairing. Replacing D by-D replaces P_+ by its complement, so the index changes sign. This is precisely the change between the two physical Wilson faces.

Independent reconciliation: parent/root separately derived the same Bott suspension, transverse Landau chirality and Hardy index calculation before receiving this note; see ROOT_ODD_INDEX_SIGN_CALIBRATION.md. The two calculations agree with Dai--Zhang's exact normalized coefficient. Constructor and joint-gap worker were informed of the definitive current-face +s / opposite-face -s convention.
