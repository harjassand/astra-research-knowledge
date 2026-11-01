# Response-exact positive rational baths: construction and boundaries

Status: independently derived candidate primitive, not audited externally, no novelty/advantage claim. Single-worker derivation. Source/cost comparison is in REPORT.md. Units hbar=omega_c=1, and Fourier convention C(t)=(2pi)^-1 int S(w) exp(-iwt)dw.

## Consequential operation and actual target

A bounded Hermitian system coupling operator Q, arbitrary finite-dimensional controlled H_S(t), factorized initial system/bath state, zero-mean stationary Gaussian continuum. We seek the complete reduced channel on every input (including a reference) up to T. No RWA, weak-coupling limit or spectral gap is assumed. The model proved here is the zero-temperature Ohmic continuum

    S_*(w) = alpha (|w|+w)/(1+w^2)^2, alpha>0.

It corresponds to J(w)=alpha w/[pi(1+w^2)^2] on w>0. It is genuinely gapless; its positive-frequency spectrum has a nonanalytic edge at 0. Its imaginary correlation is exactly

    Im C_*(t)=-(alpha/4) t exp(-t), t>=0.

Its symmetrized fluctuations have a long tail. A finite rational spectrum cannot equal S_* globally; it can approximate it with a quantified excess of classical noise.

## Failure A: independently damped positive modes

For C_L(t)=sum_j v_j exp[-(gamma_j+i Omega_j)t], v_j>0, gamma_j>0, the two-sided spectrum is a positive sum of Lorentzians. At every real w it is strictly positive. In particular S_L(0)=sum_j 2v_j gamma_j/(gamma_j^2+Omega_j^2)>0. The target S_*(0)=0 and S_*(w)=0 for w<0. In a commuting dephasing experiment, the integrated real influence has asymptotic slope S_L(0)/2>0, whereas the Ohmic target grows logarithmically. Positive weights cannot cancel this slope. This does not forbid a finite-horizon approximation with T-dependent parameters, nor prove a lower bound against coupled modes.

At any finite beta>0, a nonzero rational spectrum cannot satisfy S(-w)=exp(-beta w)S(w) on an open frequency interval: its rational ratio would equal a nonrational exponential by analytic continuation. Exact finite-mode global KMS is therefore the wrong target. At beta=infinity, a nonzero rational spectrum cannot vanish on a whole negative half-line. Exact balance at finitely many frequencies remains possible.

## Positive mechanism B: interference and a rational upper envelope

Choose any positive nodes a_1,...,a_n (repetition allowed). Define

    P(x)=product_k (a_k+x), Qp(x)=P(-x), z(x)=Qp(x)/P(x),
    D(x)=[P(x)^2-P(-x)^2]/x,
    r_n(x)=[P(x)^2+P(-x)^2]/D(x).

The removable value at x=0 is r_n(0)=1/[2 sum_k a_k^-1]. For x>0, |z(x)|<1, and

    r_n(x)=x (1+z(x)^2)/(1-z(x)^2) >= x.

r_n is even, with no real pole; hence r_n(x)>=|x| on the real line. The spectrum

    S_n(w)=alpha [r_n(w)+w]/(1+w^2)^2

is nonnegative and rational. This is not a signed probability representation. Three useful facts are exact:

1. Response: S_n(w)-S_n(-w)=2alpha w/(1+w^2)^2=S_*(w)-S_*(-w). The free bath commutator and causal dissipative response are identical at every time.
2. Excess: S_n-S_*=alpha [r_n-|w|]/(1+w^2)^2 is even and nonnegative. It is exactly the spectrum of an independent real classical stationary Gaussian process. Thus the simulator is the target bath plus a controlled classical Hamiltonian noise, at the level of all Gaussian influence functionals, not only a dephasing fixture.
3. Thermal interpolation: at any node a_k, r_n(a_k)=a_k; S_n(-a_k)=0 and S_n(a_k)=S_*(a_k). A weak-coupling transition placed at that frequency sees the exact zero-temperature upward/downward rate. This does NOT establish exact strong-coupling steady states or finite-time channel equality.

Adding any extra positive node multiplies z(x)^2 by a number in [0,1] for x>0. It therefore monotonically reduces the excess spectrum while adding an exact negative-frequency zero. Selected known transition frequencies can be inserted without refitting or degrading the proved error. Acquiring all Bohr frequencies of a large many-body system would itself be an additional paid task.

This rational construction is related to classical product rational approximations of |x| (Newman/Zolotarev type). Its application-specific content is the joint exact-response/excess-noise/thermal-node contract; historical priority is unestablished.

## Explicit two-mode physical realization (n=1)

For one arbitrary a>0, r_1(w)=(w^2+a^2)/(2a), so

    S_1(w)=alpha (w+a)^2/[2a(1+w^2)^2].

Let two vacuum oscillator annihilators b=(b1,b2)^T obey linear drift

    A=[[0,1],[-1,-2]], ell=(0,2)^T,
    A+A^dagger=-ell ell^dagger,
    H=(i/2)(A-A^dagger)=[[0,i],[-i,0]],
    c=sqrt[alpha/(2a)] (-ia,1)/2.

Use the genuine Lindblad generator

    dot rho=-i[H_S+ b^dagger H b + Q(c b + b^dagger c^dagger),rho]
            +D[ell^dagger b](rho),
    D[L](rho)=L rho L^dagger -{L^dagger L,rho}/2.

The free vacuum correlation is

    C_1(t)=c exp(At)c^dagger
          =alpha/(8a) exp(-t)[(1+a^2)+(a^2-1-2ia)t].

Its spectrum is S_1, its imaginary part is exactly -(alpha/4)t exp(-t), and its negative-frequency noise vanishes at -a. The auxiliary one-particle H has eigenvalues +/-1: it is a driven/synthetic CPTP simulator, not an equilibrium positive-energy material reservoir. A rotating-frame implementation and ancilla resets consume resources. CPTP alone is not a claim of passive thermodynamic equilibrium.

## Constructive finite network for all n

For y>0, let theta(y)=sum_k arctan(y/a_k). theta is strictly increasing from 0 to n*pi/2. There is one simple positive s_j solving theta(s_j)=j*pi/2 for j=1,...,n-1. Direct factorization gives

    D(w)=4(sum a_k) product_{j=1}^{n-1}(w^2+s_j^2).

The stable strictly proper spectral factor is

    h_n(s)=sqrt[alpha/(2 sum a_k)] product_k(s-i a_k)
           /[(s+1)^2 product_j(s+s_j)],
    S_n(w)=|h_n(-iw)|^2.

It has McMillan degree <=n+1. Form any controllable state-space realization (A0,b0,c0) of h_n with A0 Hurwitz. Its controllability Gramian W>0 solves

    A0 W+W A0^dagger+b0 b0^dagger=0.

If W=L L^dagger, set A=L^-1 A0 L, ell=L^-1 b0, c=c0 L. Then A+A^dagger=-ell ell^dagger, so A=-iH-ell ell^dagger/2 with H Hermitian. The vacuum oscillator network with jump ell^dagger b and coupling c realizes S_n and is CPTP. This uses standard passive linear quantum realization machinery; existence is proved here, a uniformly well-conditioned high-n synthesis is not yet established.

## Explicit convergence, with no fitted decomposition supplied

Use endpoints delta=2^-L and Lambda=2^L, L>=1. In each dyadic bin [2^j,2^(j+1)], j=-L,...,L-1, put m positive nodes (for exact arithmetic one can use a_{j,k}=2^j(1+k/m), k=0,...,m-1), then add the endpoint Lambda. Total n=2Lm+1. For each x in [delta,Lambda], a full neighboring bin has m nodes in [x/2,2x]. Thus |z(x)|^2<=3^-2m=:q, and

    0<=r_n(x)-x<=2x q/(1-q).

For x<=delta, the endpoint a=delta and the one-factor estimate yield r_n(x)<=delta. For x>=Lambda, the endpoint a=Lambda gives r_n(x)<=(x^2+Lambda^2)/(2Lambda)<=x^2/Lambda. Since int_0^infinity x/(1+x^2)^2 dx=1/2,

    int_0^infinity (r_n(x)-x)/(1+x^2)^2 dx
       <=delta^2 + Lambda^-2 + q/(1-q).

The variance of the excess classical process is consequently

    sigma_n^2 = (2pi)^-1 int_real (S_n-S_*)dw
       <=alpha/pi [2*4^-L + 3^-2m/(1-3^-2m)].

As an implementation, the integrand and product formula are explicitly computable from the nodes; no bath simulator, feasibility oracle, or fitted correlation is an input. All a nodes can be rational.

## Finite-bit synthesis is earned for a reciprocal dyadic variant

For an explicit bit-complexity choice, repeat each dyadic node 2^j, j=-L,...,L, an odd number m of times. Then n=m(2L+1) is odd, all nodes are rational, and the same approximation proof applies: every x in [delta,Lambda] has m repeated nodes within a factor two. This variant is used for the conservative complete-memory cost table.

Let U=sum a_k=sum a_k^-1=m(2^(L+1)-2^-L). The positive poles s_j obey

    s_min>=pi/(2U), s_max<=2U/pi,
    |s_j-s_k|>=pi/(2U) for j!=k,
    |s_j-1|>=pi/(4U).

The first three follow from theta'<=U and theta(y)>=n*pi/2-U/y. The last follows from reciprocal symmetry theta(1)=n*pi/4 with n odd. Hence the roots and the double UV pole at1 have explicitly controlled separation; no arbitrarily close accidental pole collision is hidden.

Use the state-space basis t exp(-t), exp(-t), exp(-s_j t). Its Gramian entries are the elementary positive Cauchy/confluent-Cauchy entries

    W00=W01=W10=1/4, W11=1/2,
    W0j=(1+s_j)^-2, W1j=(1+s_j)^-1,
    Wij=(s_i+s_j)^-1 for simple poles.

The determinant is the continuous double-node limit of the Cauchy determinant

    det[(p_i+p_j)^-1] = product_{i<j}(p_i-p_j)^2/product_{i,j}(p_i+p_j).

Dividing by the squared double-node separation before taking the limit removes precisely that factor. With M=n+1, R=max(1,2U/pi), d=min(1,pi/(4U)), this yields the sufficient lower bound

    det W >=d^[M(M-1)-2]/(2R)^[M^2].

Also tr W<=M/[2min(1,pi/(2U))]. Therefore

    log cond W <= M log(tr W) -log(det W)
                 =O(M^2 log[2+U]+M log[2+M]).

The partial-fraction residues are finite products/divisions whose factors have the same explicit separation bound. Computing the poles by interval bisection, the residues, the Gramian Cholesky factor and the transformed coefficients thus needs a polynomial number of arithmetic operations and a polynomial number of guard bits in L,m and the requested coefficient precision. This is an existence-level finite-bit acquisition argument, not an optimized stable implementation; the small executable realizations use high-precision arithmetic and directly report their condition numbers.

The physical coefficients themselves are also bounded. The single-jump realization has Gamma=ell ell^dagger/2 of rank one and

    tr Gamma=2+sum_j s_j=:R_sum,
    ||ell||^2=2R_sum,
    ||H||<=||H||_F<=R_sum.

The final inequality follows by taking the real trace of A^2: all A eigenvalues are -1,-1,-s_j, so tr H^2=(tr Gamma)^2-[2+sum s_j^2]. In particular R_sum<=2+(2U/pi)H_{n-1}, polynomial in the charged range Lambda and m. Meanwhile ||c||^2=C_n(0)=alpha/(2pi)+sigma_n^2 is bounded. Increasing precision does not conceal exponentially large physical coupling amplitudes, although the fastest auxiliary rates do grow polynomially with T/epsilon.

## Complete-channel error, including arbitrary noncommuting Q and controls

By Gaussian influence equivalence, the S_n bath is equivalent to the S_* bath plus the independent real Gaussian xi_n(t) with variance sigma_n^2. Conditional on xi, the full target dilation differs by the bounded perturbation Q xi(t). For any system/reference input and common bath dilation, Duhamel and unitary invariance imply

    ||U_xi(T)-U_0(T)|| <= ||Q|| int_0^T |xi(t)|dt.

Tracing, averaging, and using E|xi(t)|=sqrt(2/pi)sigma_n gives

    ||Phi_n(T)-Phi_*(T)||_diamond
      <=min{2, 2||Q||T sqrt(2/pi) sigma_n}.

The same estimate holds for each t<=T and under identical arbitrary bounded piecewise continuous system controls (and a reference). Thus n=O(log^2[1+||Q||T sqrt(alpha)/epsilon]) suffices for error epsilon in the continuum reduced channel. This conservative bound avoids an assumed system/bath mixing gap. It does not assert fast-forwarding: implementing time T still costs evolution and resets.

## Full operation costs and unearned parts

Given explicit alpha, cutoff, Q, H_S, T and epsilon, choose L,m from the bound. The spectrum and s_j roots are acquired by known arithmetic and monotone scalar bisections. The n+1 oscillator-mode count is polylogarithmic, while the total covariance c c^dagger=alpha/(2pi)+sigma_n^2 stays bounded. The fastest and slowest auxiliary decay rates can vary polynomially with T/epsilon. Matrix coefficient precision, Gramian conditioning, gate/evolution cost, oscillator occupation cutoff, state-preparation and dissipation/reset resources must all be charged.

A stronger, derived occupation theorem closes an important part of the full operation. Let N=sum b_j^dagger b_j, a=||Q||||c||, lambda=a^2 T^2. For arbitrary number-preserving quadratic auxiliary H, vacuum initial modes, and any passive linear damping, define M_k(t)=E[(N)_k]. The free Hamiltonian commutes with (N)_k, damping only decreases its expectation, and the bounded system drive gives

    dM_k/dt <=2 k a sqrt(M_{k-1} M_k),  M_0=1.

Indeed, the lowering operator B=c b obeys B^dagger (N)_{k-1} B <=||c||^2 (N)_k, and weighted Cauchy-Schwarz gives the inequality. Induction after dividing by 2 sqrt(M_k), or a regularized argument at zero, yields

    M_k(t)<=(a t)^(2k),
    E exp(sN(t))<=exp[(a t)^2(e^s-1)], s>=0.

Hence P(N>=K)<=lambda^K/K! and the usual optimized Poisson Chernoff tail also applies. This bounds moments of the actual quantum process, not only Gaussian free modes or a commuting fixture.

For a total-occupation cutoff N<=K, retain the complete number-preserving auxiliary Hamiltonian and the exact lowering jumps inside this space, and omit only the Hamiltonian transition K<->K+1. To compare, extend the truncated Hamiltonian to the full Fock space by removing only this boundary edge and keep the original passive jumps. Starting in vacuum, its low sector is invariant and equals the finite simulator. The difference from the full generator is only the bounded boundary Hamiltonian Delta V. Its square satisfies

    (Delta V)^2 <=a^2 (K+1)(Pi_K+Pi_{K+1}).

Duhamel for the two contractive Lindblad propagators, applied to the actual full process, therefore gives the complete-channel bound

    ||Phi_n-Phi_{n,K}||_diamond
       <=min{2,2 a T sqrt(K+1) sqrt(lambda^K/K!)}.

One can justify the vacuum infinite-Fock process without assuming an arbitrary unbounded GKSL extension: first prove the moment and Duhamel bounds for two finite total-occupation cutoffs L>K. The K-bound is uniform in L, so the embedded controlled joint channels form a trace-norm Cauchy sequence on vacuum inputs, uniformly with references and controls. Their normal CPTP limit is the canonical process meant here.

The calculation extends with an untouched reference and the same bounded system controls. One can take K=O(lambda+log[(1+aT)/epsilon]) with enlarged absolute constants. A direct sufficient K is obtained by increasing an integer until the displayed explicit bound is <=epsilon. The M=n+1 modes can each be binary encoded up to K, using M ceil(log2(K+1)) qubits; implementing the total-number boundary requires arithmetic, not a basis of binomial(K+M,M) individually enumerated states. Thus an ideal digital simulator has polylogarithmic bath-register width in T/epsilon for this explicit bath family, while gate/depth/evolution time and parameter synthesis are additional real costs.

This occupation theorem is a derived proof, not an acquired independent audit. It must be checked carefully against earlier bosonic cutoffs before claiming novelty. The canonical full-Fock domain is obtained by that finite-cutoff limit; no independent mathematical review or physical implementation has been made.

The finite generator can be represented directly on binary occupation registers: number-preserving hopping has at most M^2 elementary terms, linear creation/lowering at most M, and the total-number condition is reversible arithmetic. There is no table of the joint Fock basis. On N<=K,

    ||H_aux||<=K R_sum,
    ||V||<=2||Q||||c||sqrt(K+1),
    ||L||^2<=2R_sum K.

These are the actual large norms a generic sparse Lindblad simulator may pay, in addition to H_S access and observable acquisition. This supplies a polynomial-cost completion under actual implementable system operators; it does not imply a useful exponent or beat the strongest coupled-mode method.

Rounding is also a paid error. Round H to a Hermitian matrix and round ell,c as vectors, and then construct the Lindblad generator from those rounded objects. Complete positivity is exact for that rounded finite generator. If their errors are delta_H,delta_ell,delta_c, then on the cutoff space

    ||Delta H_total||<=K delta_H+2||Q||sqrt(K+1)delta_c,
    ||Delta L||<=sqrt(K)delta_ell,
    ||Delta generator||_diamond
       <=2||Delta H_total||+2(||L||+||L'||)||Delta L||.

Duhamel multiplies this by T. Choosing polynomially small coefficient errors from this formula assigns, for example, epsilon/6 to parameter synthesis and epsilon/6 to digital evolution, with the other two thirds assigned to continuum and Fock errors. This requires logarithmic output precision and the already charged Gramian guard bits. The free-bath response and thermal zeros are exact identities of the ideal mathematical hierarchy; a finite-bit implementation approximates them within its paid total-channel budget.

The analytic model spectrum is an explicit acquired input. For an unknown measured bath, finite noisy spectroscopy does not grant this exact spectrum; spectral identification costs and model uncertainty are unearned. Exact global finite-temperature KMS is excluded for a finite rational spectrum. Non-Gaussian bath cumulants are not controlled.
