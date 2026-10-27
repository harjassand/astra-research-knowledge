# Gaussian shift reuse: rigidity, precision cost, and the needed weaker contract

27 October 2026. This rejects an overstrong reuse contract, not the general Gaussian-mean target. Earlier results and frozen sources are preserved.

## 1. Gaussian location-channel rigidity

Let K be a positive Markov kernel from R^p to R^q. Suppose that for every theta, applying K to N(theta,I_p) gives N(m(theta),Sigma), with the SAME finite covariance Sigma for all theta. Then

    m(theta)=b+A theta,       A A^T <= Sigma.

Conversely every such affine family is realized by Y=b+A W+E with independent Gaussian E of covariance Sigma-A A^T.

Proof. At theta=0 both W and Y have Gaussian marginals, so Cauchy-Schwarz proves finiteness of their joint moment-generating function for every real tilt. Gaussian change of measure gives

    C(theta,t)=log E exp(theta.W+t.Y)
              =|theta|^2/2+t.m(theta)+t^T Sigma t/2.

This is smooth and convex. Its theta-Hessian is I+sum_j t_j Hess m_j(theta). Positivity for every t of either sign forces every Hess m_j to vanish. The full Hessian then has blocks [[I,A^T],[A,Sigma]], and positivity gives the covariance inequality. Smoothness of m follows from the finite joint MGF, so it is not an extra assumption.

This theorem applies to positive kernels, not signed density expansions. Gaussian-transition rigidity is established mathematical territory; no historical novelty claim is made. Holevo's paper cited below studies Gaussian-preserving transition operators. This narrower fixed-input-covariance theorem is proved here in full.

## 2. Consequence for exact seed-shift contracts

Suppose a scalar-center routine Q(x;z), z in R^M, obeys the pathwise identity

    Q(x+Delta;z+v Delta/r)=Q(x;z)

for a fixed nonzero v, r>0, and every x,z,Delta. It may use arbitrary additional independent randomness. Decomposing standard Gaussian Z into its component along v and the orthogonal component shows that Q(x;Z) is the image of a Gaussian location family with effective input noise eta=r/|v| under one fixed positive kernel. Indeed Q(x;Z)=Q(0;Z-v x/r).

Therefore Q(x;Z) cannot have exact law N(m(x),sigma^2) for every x unless m is affine. The legal source g(t)=cos t at physical radius r=1 has m(x)=exp(-1/2)cos x and fails this condition.

This does not contradict R16. That compiler is approximate and its shift budget grows with accuracy. It also does not give a lower bound for the original target at a single center. It rejects an exact nonlinear Gaussian-readable channel that would have made cached center reuse automatic.

## 3. Full-law quantitative obstruction from bounded tests

Fix a source g. Let a positive kernel map N(x,eta^2) to P_x, and suppose

    sup_x TV(P_x,N(a cos(kx),sigma^2)) <= epsilon.

For every integer n>=1 and real t,

    2 epsilon >= exp(-sigma^2 t^2/2)|J_n(a t)|
                 -exp(-eta^2 n^2 k^2/2).                 (1)

Here J_n is the ordinary Bessel function; a negative right side is vacuous. The kernel may use unlimited computation, auxiliary randomness, and evaluations of the fixed g. The only restriction is that the unknown x enters through the supplied noisy cloud. Consequently the inequality also applies when unlimited fixed-source queries are allowed: those queries do not add another observation of x.

Proof. The conditional characteristic function psi_t(w)=E[exp(i t Y)|W=w] satisfies |psi_t|<=1. Thus the actual output characteristic function is f_t=P_eta psi_t. For a frequency lambda, let c_T(f)=(2T)^(-1) integral_{-T}^T f(x)exp(-i lambda x)dx. Changing variables inside the Gaussian convolution gives

    c_T(P_eta psi_t)=exp(-eta^2 lambda^2/2)c_T(psi_t)+o(1).

The error tends to zero because shifting the averaging interval by eta Z changes its normalized integral by at most |eta Z|/T. Hence limsup |c_T(f_t)|<=exp(-eta^2 lambda^2/2), whether or not psi_t or the kernel is periodic. Uniform TV bounds the difference of characteristic functions by 2epsilon. The target function exp(-sigma^2 t^2/2)exp(i a t cos(kx)) has Fourier coefficient of magnitude exp(-sigma^2 t^2/2)|J_n(a t)| at lambda=nk. Comparing coefficients proves (1).

This is a bounded-test full-law inequality. No tail assumption on P_x, moment test, or fitted residual is used. For every eta>0 the right side is positive at some fixed small nonzero at and sufficiently large n, because the relevant Bessel coefficient decays factorially while the Gaussian frequency attenuation decays as exp(-c n^2).

For the general legal source g(x)=L cos(kx)/k at physical radius r, the target center is a cos(kx), where a=(L/k)exp(-r^2 k^2/2). Thus (1) applies directly to the original scalar source family, and the effective cloud precision must still be charged when this family occurs inside a larger conservative source.

## 4. Exact numerical witnesses

Use g(x)=cos x, physical radius 1, sigma=t=k=1, a=exp(-1/2), and D=1/eta. The alternating Bessel series yields

    J_n(a) >= (a/2)^n/n! * (1-a^2/[4(n+1)])
            >= exp(-n/2)/(2^n n!) * (1-1/[4(n+1)]).

Hence

    epsilon >= (1/2){ exp(-(n+1)/2)/(2^n n!)
                      *(1-1/[4(n+1)])
                      -exp(-n^2/(2D^2)) }.             (2)

The companion script verifies positive rational lower bounds with directed rounding of exponential series. It does not call an oracle or infer TV from experimental moments. The source is used as an obstruction to a uniform kernel, not as a known-mean sampler fixture.

| D | n | Certified positive uniform TV floor, approximately |
|---:|---:|---:|
| 1 | 5 | 4.34925247462077024e-6 |
| 2 | 30 | 2.53776926985974467e-49 |
| 3 | 85 | 9.43710315741599125e-174 |
| 4 | 172 | 9.04023694552065601e-402 |

The exact rational interval endpoints are in shift_rigidity_exact_bounds.csv. Directed-rounding precision is 468, 968, 2344, and 4784 integer bits respectively. Every arithmetic comparison in the certification is rational. Decimal values above only display those exact inequalities.

These tiny floors are not useful query lower bounds. They establish that a fixed finite center-noise scale or seed-shift budget is a genuine accuracy resource, even for a smooth legal source. No lower bound on original g-query count follows from D alone. The desired general target at one supplied center has not been refuted.

## 5. Primary-research context

A. S. Holevo, *On a Characterization of Gaussian Transition Operators*, Theory of Probability and Its Applications 61(4), 712-718 (2017), DOI 10.1137/S0040585X97T988435. The publisher abstract explicitly describes Gaussian Markov-operator characterization and was retrieved. The proof above is self-contained; no historical novelty is claimed.

https://epubs.siam.org/doi/10.1137/S0040585X97T988435
