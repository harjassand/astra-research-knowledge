# Independent 3D Toeplitz sign calibration by a suspension generator

Root derivation, 2026-11-03. This does not use the earlier eta expansion. Conventions: p=-i partial, D=sigma_1 p_x+sigma_2 p_y+sigma_3 p_z, positive spectral projection P_+(D), and W3(U)=integral tr(U^-1 dU)^3/(24 pi^2), orientation dx dy dz.

Choose a smooth projection E(y,z) over T² with first Chern number c=integral tr(E dE dE)/(2 pi i). Let U(x,y,z)=exp(ix) E+(1-E), with x period2pi and antiperiodic spin structure in x. This is a U(N) suspension generator; it need not itself have determinant1 to calibrate the strong 3D coefficient.

Direct differential-form calculation:
A_x=iE, and A_perp=(1-exp(-ix))E dE(1-E)+(exp(ix)-1)(1-E)dE E.
Thus tr(A³)=3i(2cos x-2) dx tr(E dE dE). Integrating x yields -12pi i tr(E dE dE), so W3(U)=c.

Replace the trivial connection by the connection preserving E and1-E, namely E d E+(1-E)d(1-E), interpreted as the induced direct-sum covariant derivative. This changes D only by a bounded zero-order term, hence leaves its odd K-homology/index pairing unchanged. In this connection U shifts p_x by+1 in the E block and does nothing in its complement.

For the E-block transverse Dirac operator D_perp=sigma_2 pi_y+sigma_3 pi_z, chirality is sigma_1. With pi=p+A and A=-i v†dv in a local E frame, the flux integral is2pi c. Its square is pi_y²+pi_z²+sigma_1 B. For positive flux the zero Landau modes have sigma_1=-1. Therefore n_+-n_-=-c (the same result follows from the 2D index theorem with these explicitly fixed conventions).

During D(t)=D+t sigma_1 E, t0→1, only those transverse zero modes cross zero. Antiperiodic p_x makes endpoints invertible. Higher transverse modes remain paired at ±sqrt((p_x+t)²+lambda²). Therefore spectral flow is -c.

The Toeplitz convention is Index(P_+ U P_+ +1-P_+)=-Sf(D→U†DU), calibrated already by the 1D Hardy shift: U=e^{ix} has shift index−1 and spectral flow+1. Hence the 3D Toeplitz index on this generator is +c=+W3(U). The weak 1D winding generators have zero pairing with D3 because their transverse untwisted chiral index is zero. This fixes the strong coefficient as+1 on T³.

Consequently, for the actual near Wilson branch D=+sigma.p,

 Index(P_+ U P_+ +1-P_+) = W3(U).

The audited quaternion convention U=[[z,w],[-w*,z*]] has W3(U)=-deg_S3(z,w)=-s. The filled-count bridge Q=N_-−dim/2=-Index therefore gives Q=+s for that existing face/root orientation. Taking the opposite boundary chirality D=-sigma.p flips the odd pairing and gives Q=-s, which cancels decoration charge+s.

This sign calibration is a root derivation to be independently reconciled. It does not change the proved Wilson-to-localizer inertia formula or assert a quantum rotor gap.
