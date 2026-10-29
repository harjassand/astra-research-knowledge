# Independent admission of the exact Gaussian Gibbs sampler

29 October 2026. Whole-read of root's `CKG_ADMISSION.md`, plus literal primary
formula reconstruction. **ACCEPTED at its explicit algorithmic/model scope.**

The primary is Chen--Kastoryano--Gilyen,
[arXiv:2311.09207v2](https://arxiv.org/html/2311.09207v2), Theorem I.1,
Corollary II.2, Corollary III.1 and its Appendix A derivation. The exact PDF
was acquired, text-extracted, and the printed kernel page 26 visually read.
PDF SHA256: `f631f5530824866e2dd2640abcc950cad680e27d8d58e71489a37dd7a2b43841`.
Its construction and Hamiltonian-simulation algorithm are established prior.

## 1. Direct spectral normalization check

Write Delta=beta(nu1-nu2), S=beta(nu1+nu2). Directly integrating the Gaussian
Fourier jumps and transition weight gives the transition coefficient

    alpha = (1/sqrt(2)) exp[-Delta²/8-(S+2)²/16].             (C1)

The exact detailed-balance correction for (A_nu2)†A_nu1 is
(i/2)tanh(Delta/4) alpha. This can be derived by solving the scalar
left/right Gibbs multiplication equation, rather than relying on an informal
claim of local detailed balance.

For the literal primary kernels used by root, ordinary (unnormalized)
Fourier integration gives

    integral b1(t)e^(-i Delta t)dt
       = (i pi/sqrt(2)) tanh(Delta/4) exp(-Delta²/8),
    integral b2(s)e^(-i S s)ds
       = (1/(2pi)) exp[-(S+2)²/16].                         (C2)

Indeed, the transform of sech(2pi t) is (1/2)sech(Delta/4), and that of
-sin(t)e^(-2t²) is
i sqrt(pi/2)e^[-(Delta²+1)/8]sinh(Delta/4). Their product with
2sqrt(pi)e^(1/8) proves the first identity; the second is one Gaussian
integral. Multiplying (C2) yields exactly (i/2)tanh(Delta/4) alpha in (C1).
The factors and clock signs in root's admitted B therefore agree with the
stationary spectral correction.

The printed paper separately asserts ||b2||_1<1/8, although its literal
b2=pi^(-3/2)e^(-4t²-2it) has norm 1/(2pi). This isolated printed sharp-norm
assertion is not used here or by root. The required coarse bound <1 and the
spectral identities above are valid. No failure of stationarity is inferred.

## 2. Integrated jump budget and clock normalization

Let a_beta=||f||_1/sqrt(2pi). Elementary Gaussian integration gives

    a_beta²=beta/sqrt(2pi),  integral gamma=sqrt(2pi)/beta.

For a norm-one seed A, both the exact and patch jumps have norm <=a_beta,
so integral gamma||Ahat||²<=1. This is a bound on the integrated OPERATOR
norm, not an invalid application of scalar Parseval after taking a norm.

Use one Hermitian site Pauli per primary instance; its adjoint closure and
normalization hold separately. Sum all 3n instances at rate one each. Their
stationary Gibbs states coincide, so the sum is exactly stationary. The
overall generator strength and simulation clock acquire the visible 3n
factor. Optional -i[H_g,·] also fixes rho_beta but must be counted in the
logical generator defect. No mixing-time conclusion follows.

## 3. Jump and coherent tails with an explicit LR input

Supply the actual patch-evolution estimate

    ||A(t)-A_R(t)|| <= min(2,C0 exp[-mu(R-v|t|)]).

Splitting at |t|=R/(2v), the jump difference is uniformly at most a_beta d_R,

    d_R=C0 e^(-mu R/2)+2e^[-R²/(4v²beta²)].

Applying (R6) to WHOLE frequency jumps and integrating gamma proves the
root tail 4d_R+2d_R². If every patch algebra has bad probability <=p_R,
the patch dissipator contributes <=3sqrt(p_R) per seed.

For the coherent correction, direct convolution and Gaussian integration
give ||b1||_1<3, ||b2||_1<1. Also

    integral_(|t|>T)|b1(t)|dt <= C1 e^(-pi T),
    C1=8sqrt(2) exp[(1+pi²)/8],
    integral_(|s|>T)|b2(s)|ds <= e^(-4T²).

For the first inequality, integrate the convolution with weight e^(pi|t|).
The weighted sech norm is <=4/pi; the weighted Gaussian-sine norm is
<=sqrt(2pi)e^(pi²/8). For the second inequality, the exact norm-weighted
tail is erfc(2T)/(2pi), which is at most the stated bound.

The two actual Heisenberg clocks in the double integral are beta(s-t) and
-beta(s+t). On the rectangle |s|,|t|<=R/(4v beta), both lie inside the
short LR time range. The product difference costs <=2C0 e^(-mu R/2);
outside the rectangle it is <=2. Splitting the tail by a union bound proves

    ||B_A-B_AR|| <= r_B(R)
     =6C0 e^(-mu R/2)+2C1 e^[-pi R/(4v beta)]
                         +6e^[-R²/(4v²beta²)].              (C3)

The patch B_AR is Hermitian by the same kernel-conjugation/change-of-variable
identity as the exact B_A and has the whole patch support. Its local
commutator costs <=6sqrt(p_R); its omitted tail costs <=2r_B.

Combining these facts independently recovers root's bound

    ||L_phys*(O_alpha)||_rho
      <= h_alpha +3n[9sqrt(p_R)+2r_B+4d_R+2d_R²],           (C4)

with h_alpha only when the optional H_g drift is present. Every finite beta,
LR constant, radius, patch probability, and site count is visible.

## 4. What a growing-support static bound would supply

This is a conditional consequence, not an admission of A's static proof.
Suppose for volume n and size parameter L that all radius-R patches obey

    p_R <= A_n exp[-a L+b c(1+R)^D],

with A_n polynomial, a,b,c>0 and bounded patch density. Choose any fixed
eta>0 small enough that b c(2eta)^D<a/2 and R=eta L^(1/D)>=1. Then
p_R<=A_n exp(-aL/2), whereas the coherent-tail term in (C3) is at most a
fixed prefactor times exp[-c' L^(1/D)] for fixed beta and LR constants.
Thus (C4) and (R1)--(R3) yield a stretched-exponential conditional memory
window if h_alpha and the twirl error are paid at the compatible scale.
The coherent kernel, not just Gaussian Fourier-jump decay, controls this
particular generic-radius estimate.

This does not infer a uniform growing-support p_R from a single-site bound.
It also does not infer microscopic thermal dynamics, efficient preparation
of the ancilla tau, or that a fixed-radius implemented approximation remains
stationary. A physically approximated generator needs a separate accumulated
error budget over the actual storage time.
