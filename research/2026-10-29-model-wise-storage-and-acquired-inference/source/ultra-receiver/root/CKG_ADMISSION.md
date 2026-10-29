# A nonempty exactly stationary quasilocal model class

29 October2026. Root source acquisition and derived receiver bounds. This
does not admit a microscopic Davies bath or a fixed finite-range truncation.
The static Peierls estimate and decoder-good bounds for the chosen support
radius remain separate active inputs.

## 1. The precise ordinary source

Chen--Kastoryano--Gilyen, arXiv:2311.09207v2, TheoremI.1 and Equations7--12,
80--82, acquired directly from the primary paper:
https://arxiv.org/html/2311.09207v2

Use its Gaussian version, not its separately approximated Metropolis weights.
For one Hermitian unitary one-site Pauli A and beta>0 put

    f(t)=exp(-t^2/beta^2)/sqrt(beta*sqrt(pi/2)),
    Ahat(omega)=(1/sqrt(2pi)) integral f(t)exp(-i omega t) A(t)dt,
    gamma(omega)=exp[-(beta omega+1)^2/2],
    A(t)=exp(iH_g t) A exp(-iH_g t).

The source gives a Hermitian coherent correction B_A with the double-time
kernel b1,b2 of its Eq11. The resulting

    L_A(rho)=-i[B_A,rho]+integral gamma(omega) D_Ahat(omega)(rho)domega

is EXACTLY stationary at rho_beta=e^(-beta H_g)/Z. Each one-seed instance
satisfies the source's normalization6. Sum these instances for the3n site
Paulis, and optionally add -i[H_g,rho], which also fixes rho_beta. This gives
a genuinely nontrivial exactly stationary generator at constant per-site
update rate. Its total local strength is O(n). This avoids mistaking the
source's globally normalized one-update clock for a physical parallel clock.
No uniqueness or rapid-mixing hypothesis is needed by the root receiver.

The source coherent correction is retained. Omitting B_A generally forfeits
exact stationarity for a noncommuting H_g. The algorithmic sampler is an
established operation; neither it nor detailed balance is claimed invented.

## 2. Integrated jump strength has no hidden dimension/frequency factor

Let a_beta=||f||_1/sqrt(2pi). The exact elementary integrals are

    a_beta^2=beta/sqrt(2pi),
    integral gamma(omega)domega=sqrt(2pi)/beta.

Thus ||Ahat(omega)||<=a_beta and

    integral gamma(omega)||Ahat(omega)||^2 domega <=1.            (1)

This directly pays the frequency-integrated operator-norm-square budget
needed for coherent-jump estimate(4) of PROOF.md. Operator Parseval alone
would not justify exchanging operator norm with the frequency integral.

## 3. Input Lieb--Robinson contract and local patch approximations

Supply finite-range, bounded-strength, bounded-incidence H_g and explicit
ordinary Lieb--Robinson constants C0,mu,v>0 such that the one-site evolution
and its radius-R Hamiltonian-patch version obey

    ||A(t)-A_R(t)||<=C0 exp[-mu(R-v|t|)]

inside the light cone estimate, together with the trivial bound2. These are
standard finite-range locality inputs, independent of n, not an assumed
property of Davies spectral projectors. In the RX/RZ application geometric
ball volume is O((1+R)^3) by bounded density and range.

Split the Fourier time integral at |t|=R/(2v). The local-patch Fourier jump
Ahat_R has the SAME radius-R support for every omega, and

    ||Ahat(omega)-Ahat_R(omega)||<=a_beta d_R,
    d_R=C0 exp(-mu R/2)+2 exp[-R^2/(4v^2 beta^2)].                (2)

Here the Gaussian tail ratio is erfc(R/(2v beta))<=exp[-R^2/(4v^2 beta^2)].
The estimate is uniform in frequency. With L_omega=sqrt(gamma)Ahat(omega),
the WHOLE-jump truncation bound of PROOF.md and (1)--(2) give

    integral ||D_Lomega*(O)-D_Lomega,R*(O)|| domega
       <=4 d_R+2 d_R^2,        ||O||<=1.                         (3)

The local part costs at most3 sqrt(p_R), where p_R is the actual uniform
decoder-bad probability for ALL operators on the radius-R support. No
independent-jump decomposition of a coherent Fourier jump is used.

## 4. The coherent correction has a paid tail as well

The primary kernels are

    b1=2 sqrt(pi) exp(1/8) [sech(2pi t) * (-sin t)exp(-2t^2)],
    b2=pi^(-3/2)exp(-4t^2-2it).

Direct coarse integration bounds suffice here: ||b1||_1<3 and ||b2||_1<1,
so ||B_A||<3. We do not need a sharp printed kernel normalization. Also

    integral_(|t|>T)|b1(t)|dt <=C1 exp(-pi T),
    C1=8 sqrt(2) exp[(1+pi^2)/8],
    integral_(|t|>T)|b2(t)|dt <=exp(-4T^2).

The first follows by weighting the convolution with exp(pi|t|): the weighted
sech norm is at most4/pi, and the other weighted norm is at most
sqrt(2pi)exp(pi^2/8). The second is the elementary Gaussian tail bound.

Rewrite Eq11's two evolved factors at times beta(s-t) and -beta(s+t).
For |s|,|t|<=T=R/(4v beta), both times are at mostR/(2v). Replacing both by
the same local Hamiltonian patch gives a Hermitian radius-R B_A,R, norm<3,
with

    ||B_A-B_A,R||<=r_B(R),
    r_B(R)=6C0 exp(-mu R/2)
       +2C1 exp[-pi R/(4v beta)]
       +6 exp[-R^2/(4v^2 beta^2)].                               (4)

This pays the coherent correction without granting it strict finite range.

## 5. What this actually admits

Let h_alpha=||[H_g,O_alpha]||_(rho_beta) as in PROOF.md, and suppose the
decoder-good projector for every radius-R patch has probability at least
1-p_R under the ACTUAL perturbed Gibbs state. Equations(1)--(4) give

    ||L_phys*(O_alpha)||_rho
       <=h_alpha+3n[9sqrt(p_R)+2r_B(R)+4d_R+2d_R^2].             (5)

The h_alpha term is only for the optional physical H_g drift. It is absent
if that drift is not included. The logical-twirl cost still uses H_g itself.
Thus the exactly stationary quasilocal model is nonempty and its integrated
strength/tails have explicit volume-independent constants before the visible
3n prefactor. Its support radius must be selected jointly with the ACTUAL
decoder-stability/Peierls estimate. No growing-support estimate was proved
merely by saying that the original source allowed O(1)-support jumps.

For long-time storage the generator remains the exact quasilocal one;
truncation above is a proof bound. Replacing it physically by fixed-radius
jumps changes stationarity and the model. Implementing the exact spectral
filters/coherent correction or proving robustness to their fixed local
errors is a further operation. These formulas do not turn an algorithmic
Gibbs sampler into an acquired passive hardware bath, and a slow memory
phase does not provide rapid thermal initialization.
