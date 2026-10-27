# Strict trace-invariant monotonicity of the filtered-seed log kernel

Root construction, 26 October 2026. Submitted for independent audit. This concerns F at fixed second and third elementary symmetric invariants, not generic matrix monotonicity.

Write T=Tr X, E=e2(X), P=det X for X>0. The acquired kernel is

F=-3 log(1+T/3+E/9+P/27)-log(1+T)
  +2 log(1+T+(T^2+E)/4+(TE-P)/8).

Let A=27+9T+3E+P and B=8+8T+2T^2+2E+TE-P. Both denominators are positive for actual positive X. Clearing the positive denominator A B(1+T) from F_T gives

N_T=P^2+(ET+3E+6T^2+52T+62)P
    +3TE^2-(6T+30)E+36T^2+72T.

The P terms are nonnegative. Put N0 for the last four terms. Feasibility gives 0<E<=T^2/3.

For 0<T<=1,
N0 >= 3TE^2+26T^2-2T^3+72T >0.

For T>=1, exactly,
N0=3T(E-1-5/T)^2 + 3(T-1)(12T^2+35T+25)/T.
This is strictly positive for T>1. At T=1 the square is also strictly positive since E<=1/3, not6. Hence F_T>0 throughout the actual positive spectral domain.

## Fixed-spectrum orientation consequence

Let A_reset>0 have distinct eigenvalues a_i and let H>0 have fixed distinct spectrum. In the A_reset eigenbasis, the acquired orientation invariants are m_i=H_ii (sum fixed) and ell=Tr(A_reset adj H). At fixed ell, the integrand's E(t) and P(t) are fixed while

T(t)=sum_i m_i/(a_i+t).

Thus the unconstrained m scores may be represented by

d_i=integral_0^infinity F_T(t)/(a_i+t) dt,

and if a_i<a_j then d_i>d_j. The integrals and differences converge for fixed faithful reset; the infinity integrand is O(t^-2).

The separately derived interior-unistochastic stationary equations require ell-score c=0 and d_1=d_2=d_3 when both spectra are simple. Strict score ordering therefore excludes such an interior stationary point for the VALUE at fixed spectra, regardless of whether c changes sign. This does not settle real/orthostochastic boundary minima, repeated spectra, or the anchored gap whose unfiltered baseline changes with the generalized reset spectrum. It is not a physical pinching or processing operation.
