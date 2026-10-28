# Finite physical traces from untrusted eigenpair proposals

This is a root-authored construction, not an independent scientific audit.
It uses standard polar decomposition, Weyl eigenvalue perturbation and
outward Taylor bounds. Its purpose is a reusable physical-input interface;
it is not a claim of a new validation theorem or a spin-two gap.

## Certificate

Let H be the intended Hermitian physical block, H0 a Gaussian dyadic
Hermitian matrix, and ||H-H0||<=eta. An eigensolver proposes any Gaussian
dyadic square V and real dyadic diagonal Lambda. Calculate exactly

    E=V*V-I, R=H0 V-V Lambda.

Supply bounds ||E||<=epsilon<=1/2 and ||R||<=r. The exact Gram condition
implies V is invertible, and U=V(V*V)^(-1/2) is unitary. On this interval

    ||(V*V)^(-1/2)-I||<=epsilon, ||V||<=1+epsilon<=3/2.

Consequently ||U-V||<=3epsilon/2 and

    ||H-U Lambda U*|| <= eta+r+3epsilon(||H0||+||Lambda||)/2 = delta.

Weyl's theorem orders every physical eigenvalue within delta of the ordered
diagonal proposals. For beta>=0 this gives

    exp(-beta delta) sum_i exp(-beta Lambda_i)
      <= Tr exp(-beta H)
      <= exp(beta delta) sum_i exp(-beta Lambda_i).

The eigensolver needs no trusted error model. A poor proposal produces a
large bound, or fails the Gram precondition, rather than invalidating the
inequality. All eigenvalues are included; there is no Ritz completeness
assumption. Hermitian Gram and H0 norms are bounded by row sums of
|Re entry|+|Im entry|. The residual norm is bounded by the maximum of its
row and column sums (which bounds sqrt(||R||1 ||R||infinity)).

## Actual physical demonstration

`certify.py` builds the four-site periodic spin-two Heisenberg Hamiltonian
with closing XY phase (3+4i)/5, an exact unit complex number. Diagonal bond
entries are m_i m_j. Each directed hop has coefficient

    sqrt[(6-m_i(m_i+step))(6-m_j(m_j-step))]/2,

which is an integer or sqrt(6). The closing hop receives the phase or its
conjugate. Every magnetization sector -8 through 8 is included explicitly,
625 states in total. No negative-sector symmetry is assumed.

An integer square root gives rational lower/upper bounds for sqrt(6) with
width 2^-80. Every real and imaginary entry is enclosed before rounding
H0 to denominator 2^40; exact maximum absolute row error supplies eta.
V and Lambda are rounded to denominator 2^40 as well.

Gram and residual products use arbitrary-precision Python integers. The
proposal arrays are promoted before multiplying, so no finite integer
overflow or floating-point GEMM arithmetic contract enters the certificate.
Integer column-square and absolute-row magnitudes are retained in the
output. Scalar exponentials use rational
degree-28 Taylor bounds after reduction to [0,1/2], an explicit geometric
tail, and outward 96-bit fixed-point squaring/reciprocation.

The saved exact rational output encloses Z_4(3,phase) between approximately
5.245258884157928e25 and 5.245259023776998e25, relative width at most
2.661814662e-8. Maximum eigenvalue displacement bound is approximately
4.460257271e-9. These decimals are display-only; the JSON rational endpoints
are the certificate. The final demonstration took about 1.21 seconds of
elapsed time, including exact physical controls Tr H=0 and Tr H²=30000.
The latter independently equals n*5^n*s²(s+1)²/3 for n=4,s=2. Every sqrt(6)
coefficient in that trace cancels exactly. No measured peak memory or
full-cycle research cost is invented.

This is one four-site physical trace, not a later connected thermal input.
The first lower-precision int64 trial had relative width5.3943e-5; the
arbitrary-precision construction improves it by about2027-fold at the
charged small-model cost. No general speed advantage is claimed. Dense
Python-integer Gram products may be expensive at six sites; their larger
cost is not measured or assumed negligible. No expensive angular grid is
justified by the negative spin-list preview. A positive new mechanism can
justify further acquisition.

## Angular acquisition interface and prior

For an even transfer power p, f_p(phi)=Z_p(phi,beta)/5^p has the spin-character
expansion sum_s chi_s(phi) m_s, m_s>=0. If A_j are its Fourier coefficients,
m_s=A_s-A_(s+1). On an N-point angular grid the exact alias is

    mhat_s=m_s+sum_(l>=1) [m_(lN+s)-m_(lN-s-1)].

The thermal worker supplies a seam-only strip bound
|f_p(phi+iy)| <= f_p(0) exp(6 beta(cosh(y)-1)) and explicit rational alias
constants separately. Those alias constants do not enclose numerical trace
errors. Combining them with this physical residual interface would enclose
both errors if that acquisition becomes useful.

Exponential convergence of analytic periodic trapezoidal quadrature is
established numerical analysis, not credited to this programme:
[Trefethen and Weideman (2014)](https://people.maths.ox.ac.uk/trefethen/publication/PDF/2014_149.pdf).
Exact integer products using floating-point GEMM under explicit mantissa
bounds are also established, for example
[FFLAS-FFPACK](https://linalg.org/linbox/fflas-ffpack/) and
[FLINT's exact GEMM documentation](https://fredrikj.net/fdoc/html/algorithms/linear-algebra/gemm.html).
This demonstrator uses integer products instead, so no Apple Accelerate
implementation assumption is needed.
