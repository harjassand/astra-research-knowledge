# Growing real-time obstruction for fixed-band Euclidean reconstruction

Research date: 2026-11-04. Independent constructor for the parent research task.
Status: complete analytic argument at the explicit oracle scope below, plus finite numerical diagnostics. Not externally reviewed, formally verified, historically novel, or a civilisation-changing capability. The attempted general late-time capability failed its information gate.

## Consequence, backward step, and attempted operation

The selected consequence was predictive real-frequency/real-time many-body response from equilibrium imaginary-time calculations, without paying for generic coherent many-body dynamics. The essential missing operation is: given noisy Euclidean correlators, return a *usefully narrow, uniformly valid* interval for a declared dynamical functional at finite data-acquisition cost.

I constructed a linear minimax estimator with an explicit approximation/noise bound, and compared it with the strongest equally informed positive-measure moment program. These are established algorithmic ingredients, not new algorithms. The experiment deliberately grants the locations of every possible spectral atom. I then built a positive-spectrum adversary that defeats both operations, including arbitrary adaptive choices of imaginary time. It works at **growing real time** with **fixed bandwidth, fixed spectral support gap, fixed temporal smearing width, and fixed absolute target error**. It makes no fixed-time exponential-in-accuracy claim.

## Primary predecessors and Astra receipt

Astra checkout: `3e6f6fa576181275bb8ed28164e7cacd51055789`. Read `AGENTS.md`, `00_START_HERE.txt`, current N810 packet, and exact current source `updates/FK/synthesis/root/THERMAL_TRANSITION_CERTIFICATE.md`, especially Sections 1–4 and 7–8, plus `updates/FK/synthesis/anchor_prior/REPORT.md`, Section 6. These already contain the bounded transition observation and a Mutzel–Tilloy comparator. No archived source supplied a proof premise here.

[Lawrence, arXiv:2408.11766v1](https://arxiv.org/html/2408.11766v1), Sections III–V and Appendix A: positivity-constrained convex bounds are information complete; the paper treats smeared real-time response and conjectures exponential sample requirements at growing time for fixed Gaussian smearing. My result is a worst-case **specified-oracle** theorem with a different adversarial spectrum at each growing time. It does not settle a claim about a single fixed physical system under its full Monte Carlo observation law.

[Mutzel and Tilloy, arXiv:2606.09791v1](https://arxiv.org/html/2606.09791v1), Sections II–III: the finite-lattice positive spectral representation, confidence region, dual bounds, and piecewise-affine envelope hierarchy already provide rigorous functional intervals, conditional on their statistical/data assumptions. They are the governing continuum incumbent. I did not obtain or execute their full implementation.

[Kernel transformations and bounds for smeared spectral functions, arXiv:2606.19503v1](https://arxiv.org/html/2606.19503v1), Sections III.2–III.3: positivity-optimized bounds, box-error dual penalties, and continuum correction of numerical kernel violations are already present. The finite LP below is therefore a comparison/diagnostic, not an originality claim.

The binomial finite-difference identity and two-point statistical arguments are standard tools. The specific combined construction was derived independently here, but the limited search does not clear priority. Source content was inspected through the web tool; no downloaded source-byte archive or external-code reproduction is claimed.

## Exact input/output/cost contract

Set hbar=1. Fix a bandwidth `Omega>0` and Gaussian **temporal** smearing width `sigma>=0`. The unknown input is a positive probability spectral measure supported on the *fixed* band `[Omega/2,Omega]`:

    mu >= 0,  integral mu = 1.

A zero-temperature Euclidean ordinate is

    C_mu(tau) = integral exp(-tau*omega) mu(domega),  tau>=0.

The target is the sine response convolved in real time with a normalized Gaussian of standard deviation sigma:

    F_mu,sigma(T) = integral exp(-sigma^2*omega^2/2) sin(omega*T) mu(domega).

Indeed Gaussian convolution of `sin(omega*T)` multiplies it by the displayed damping factor. This is temporal smearing, not Gaussian smearing of a spectrum around a target frequency. This is the odd spectral commutator response extended to all real times, up to its overall sign. For the Gaussian convolution of the causal response restricted to t>=0, the single-input correction has magnitude at most Phi(-T/sigma), since the sine response is bounded by one. The pair separation is therefore at least G_n-2 Phi(-T_n/sigma), which has the same fixed positive lower limit at growing T_n. For sigma=0 and T_n>0 the definitions coincide.

Three separate data-access models are analyzed; they are not interchangeable:

1. A deterministic ordinate with arbitrary error bounded by eta. More queries need not reduce adversarial error.
2. An independent Gaussian ordinate `Y=C_mu(tau)+N(0,v)`, with a specified common `v>0` per raw query. Adaptive tau choices and private random seeds are allowed.
3. A Bernoulli acceptance bit of mean `C_mu(tau)`. Its variance is signal dependent. A second, explicitly *stronger* version grants exact removal of the known lowest response energy, so the acceptance mean is `exp(E_min*tau) C_mu(tau)`.

A query is charged as one raw observation; computation and imaginary-time evolution can only add costs. Models 2 and 3 are specified oracles, not inferred descriptions of all QMC estimators. Access to explicit Hamiltonian/observable structure, full sampled configurations, simultaneous correlated vector observations, derivatives, or extra instruments is not included unless separately stated.

## The positive pair at growing time

For every integer n>=1 define

    a = n+1/2,
    h = Omega/(2n+1/2),
    omega_j = h(a+j),  j=0,...,n,
    T_n = pi/h = pi(2n+1/2)/Omega.

The even and odd probability measures are

    mu_even = 2^(1-n) sum_(j even) binom(n,j) delta_(omega_j),
    mu_odd  = 2^(1-n) sum_(j odd)  binom(n,j) delta_(omega_j).

Both have mass one because the even and odd binomial sums equal `2^(n-1)`. The largest atom is exactly Omega. The smallest is `Omega*(n+1/2)/(2n+1/2)>Omega/2`. Thus the band and its positive lower endpoint are fixed as n grows; neither support width nor highest frequency grows. **The real-time center T_n grows linearly with n.**

At these times,

    sin(omega_j*T_n) = (-1)^(n+j).

Consequently the responses have opposite signs and their difference satisfies

    G_n := |F_even,sigma(T_n)-F_odd,sigma(T_n)|
         = 2 E_[J~Bin(n,1/2)] exp(-sigma^2*omega_J^2/2)
         >= 2 exp(-sigma^2*Omega^2/2).

The separation is fixed in n. For `sigma*Omega<=1`, any fixed absolute error `epsilon<exp(-1/2)` is less than half this universal separation. In particular epsilon=1/2 is allowed.

## All imaginary times are exponentially uninformative

Put `z=exp(-h*tau)`. The binomial theorem gives the exact identity

    C_even(tau)-C_odd(tau)
      = 2^(1-n) z^a (1-z)^n >= 0.

For all tau>=0 its maximum is

    Delta_n = 2^(1-n) [a/(a+n)]^a [n/(a+n)]^n,

attained at `z=a/(a+n)`, equivalently `tau_*=-log(a/(a+n))/h`. Differentiating `a log z+n log(1-z)` proves this is the global maximum; the endpoints give zero. Furthermore

    Delta_n <= 2^(1-3n),
    Delta_n ~ 2^(1/2-3n).

The elementary upper bound follows from `z^a(1-z)^n=z^(1/2)[z(1-z)]^n<=4^(-n)`.

For the deterministic error model, give the algorithm the common transcript

    y(tau) = [C_even(tau)+C_odd(tau)]/2.

At every queried time this is within `Delta_n/2` of both legal inputs. The argument holds for an arbitrary adaptive query policy, since it defines an answer at every tau. Thus at tolerance `eta>=Delta_n/2`, no uniformly valid returned interval can have width smaller than G_n on this transcript. Nonlinear reconstruction and optimal positivity inference cannot change this information fact.

## Exact sum rules and known atoms do not remove the ambiguity

The n-th finite-difference identity implies

    integral omega^k mu_even = integral omega^k mu_odd,
    k=0,...,n-1.

Grant all these moments exactly and grant the possible atom locations. The n-by-(n+1) moment matrix is Vandermonde and has rank n. Its nullspace is spanned by `((-1)^j binom(n,j))_j`. Relative to the midpoint weights `b_j=binom(n,j)/2^n`, every solution of the moment equalities is

    p_j(t)=b_j[1+t(-1)^j].

Nonnegativity is equivalent to `-1<=t<=1`, since both parities occur. The entire moment-consistent positive set is therefore precisely the segment joining the two adversaries. Both segment endpoints satisfy the common noisy Euclidean transcript above. The exact optimal response interval is the full endpoint interval even after these extra inputs. One additional *exact* nonzero-tau ordinate would determine t; the noise floor is essential.

This proof explicitly checks the finite-discretization concern: the exact moment constraints leave one free direction, rather than an invertible complete moment system. Moments through order n, instead, would determine the n+1 weights.

## Adaptive Gaussian query lower bound

Suppose an algorithm takes at most M queries. Include its private random seed in the transcript. Given a common history, the algorithm's next-time kernel is the same under both hypotheses; only the Gaussian response mean differs. The chain rule for relative entropy gives

    KL(P_even || P_odd)
      = E_even sum_(i=1)^M [C_even(tau_i)-C_odd(tau_i)]^2/(2v)
      <= M Delta_n^2/(2v).

Early stopping can be padded with unused observations, so the result covers a bounded adaptive stopping rule. It is not a theorem for an unbounded expected-query stopping rule without additional treatment.

Assume the estimator satisfies `Pr(|Fhat-F|<=epsilon)>=1-alpha` for both inputs, where `0<alpha<1/2` and `epsilon<G_n/2`. Thresholding at the midpoint of the two response values gives a binary test with each error at most alpha. Hence transcript total variation is at least `1-2alpha`. Pinsker and the preceding chain rule imply

    1-2alpha <= TV(P_even,P_odd)
              <= Delta_n sqrt(M)/(2 sqrt(v)),

and therefore

    M >= 4v(1-2alpha)^2/Delta_n^2
      >= v(1-2alpha)^2 64^n.

Equivalently, along the growing-time sequence T_n this is exponential in `Omega*T_n`, with exponent `3 log(2)/pi`. Sigma and Omega stay fixed, and the target absolute error can stay fixed. This is a worst-case theorem over spectra at increasing times, not exponential complexity at fixed time and not a theorem that every fixed physical system is difficult.

## Granting the known gap and signal-dependent acceptance noise

A cheap known energy shift must not be confused with free precision. To stress-test the barrier I grant a stronger oracle with mean

    Ctilde_mu(tau)=exp(E_min*tau) C_mu(tau),
    E_min=a*h.

The exact shifted difference is

    Ctilde_even-Ctilde_odd = 2^(1-n)(1-z)^n,
    sup_tau |difference| = Dtilde_n=2^(1-n).

If this shifted ordinate is supplied with independent fixed Gaussian variance v, the same proof gives

    M >= v(1-2alpha)^2 4^n.

This is a new oracle promise, not the variance obtained by multiplying old Gaussian observations by `exp(E_min*tau)`.

If each shifted query is instead a Bernoulli bit with that mean, maximal coupling of two Bernoulli laws disagrees with probability exactly their mean difference, at most Dtilde_n. Run the two adaptive algorithms with the same random seed and the same next time while their histories agree. A union bound gives `TV(P_even,P_odd)<=M Dtilde_n`. Thus the same fixed-error, two-hypothesis task requires

    M >= (1-2alpha) 2^(n-1).

This remains exponential in growing time, despite signal-dependent variance and the granted removal of the lowest response energy. It is weaker than the Gaussian lower bound because it is a different observation law. Without the shift, the same coupling gives `M>=(1-2alpha)/Delta_n`, of order `8^n`.

The exponent of the shifted Bernoulli bound is attainable on this *known pair*: at sufficiently large tau the even acceptance probability approaches `2^(1-n)`, while the odd probability approaches zero. Seeing a rare success distinguishes the pair using order `2^n` trials. Finite tau, filter realization, and preparation add costs; the lower bound did not charge them.

## Delta peaks are not necessary, but uniform regularity is an extra input

A smooth-density version uses `h=Omega/(2n+3/4)`, the same a=n+1/2 and parity weights, and convolves each measure with the same normalized C-infinity nonnegative bump supported in `(0,h/4)`. The resulting supports remain in `[Omega/2,Omega]` and all moments through n-1 still agree.

Their Euclidean difference is multiplied by a Laplace transform in [0,1], so the same Delta_n upper bound applies. At `T_n'=pi/h`, the sine factor is `(-1)^(n+j) cos(T_n' s)` with `0<s<h/4`; this cosine is at least `1/sqrt(2)`. The smeared response gap is therefore at least `sqrt(2) exp(-sigma^2 Omega^2/2)`. The proof extends to smooth spectral densities.

The derivatives of these bumps grow with n. No lower bound over a class with fixed, acquired uniform derivative norms, known linewidth, or other quantitative regularity follows. Such stronger input can exclude the adversaries and may make late-time response uniformly small.

## Implemented operation and strongest same-data alternative

For declared known atoms and `K_ij=exp(-tau_i omega_j)`, I constructed

    Fhat=c0+sum_i c_i y_i,
    E=r+eta sum_i |c_i|,
    |f_j-c0-sum_i c_i K_ij|<=r for every possible atom j.

Minimizing E is an LP. This is a uniform linear minimax approximation/noise estimator. Independently I solved the ordinary positive-measure LP

    minimize/maximize sum_j f_j p_j,
    p_j>=0, sum_j p_j=1, |Kp-y|<=eta,

with and without the exact n-1 additional moments. This implements the finite, strongly informed restriction of the Lawrence/Mutzel–Tilloy incumbent; it is not a continuum spectral certificate. At fixed data the positive-measure LP can be stronger than the symmetric linear minimax estimator. No new interval method is claimed.

Both methods received identical 61 Euclidean ordinates, atom locations, and error bounds. The transcript was the adversary midpoint, with `eta=Delta_n/2`. For unsmeared responses at n=2,4,6,8, both returned `[-1,1]`, which is exactly attained by the explicit pair. For sigma=Omega=1, the positivity intervals remained approximately `[-0.739,0.732]`, `[-0.7446,0.7450]`, `[-0.74765,0.74765]`, and `[-0.74937,0.74937]`. The pair nearly saturates these and exactly saturates the LP after adding the exact moments. The symmetric estimator was weaker at n>=4; at n=8 it returned approximately `[-0.7533,0.8104]` with noise amplification `sum|c_i|=129675`. This defeats the candidate operation, rather than comparing against a deliberately weak incumbent.

The LPs use floating-point HiGHS and tolerances; they are finite diagnostics, not rational/outward-rounded certificates. The exact pair, identities, and analytic lower bounds do not depend on these solver outputs. Default HiGHS dual tolerance initially reported a false unbounded status for a nonnegative-objective LP at small noise penalties; explicitly setting primal/dual tolerances to 1e-10 resolved it. This numerical issue is retained here rather than counted as scientific evidence.

## Numerical values and actual cost

At Omega=sigma=v=1, alpha=0.05 and a fixed target absolute error epsilon=1/2:

| n | growing time T_n | max Euclidean difference | actual response gap | raw Gaussian query lower bound | gap-shifted Bernoulli query lower bound |
|---:|---:|---:|---:|---:|---:|
| 4 | 26.704 | 3.504e-4 | 1.4887 | 2.639e7 | 7.2 |
| 10 | 64.403 | 1.325e-9 | 1.5008 | 1.845e18 | 460.8 |
| 20 | 127.235 | 1.230e-18 | 1.5052 | 2.140e36 | 4.719e5 |
| 40 | 252.898 | 1.066e-36 | 1.5074 | 2.853e72 | 4.948e11 |
| 80 | 504.226 | 8.010e-73 | 1.5085 | 5.049e144 | 5.440e23 |

The powers of time cannot be read as seconds without a physical Omega. Gaussian lower bounds scale linearly with the declared raw observation variance v. These are analytic oracle lower bounds, not measured QMC runtime.

Run `python3 construct_and_test.py` in this directory. The saved `results.json` records Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0; actual versions are authoritative in the JSON if this prose differs. The final run took about 0.174 seconds inside the script, with no external compute spend or acquired Monte Carlo configurations. It checked exact rational normalization and n moment identities for eight n values through 80, 32 transform identities at 220 decimal digits with relative tolerance 1e-100, eight finite LP comparisons, and 18 independently enumerated parity-circuit histograms through n=10. Exact symbolic reasoning establishes the universal statements; finite tests alone do not.

## Physical realization, stronger access, and failure of the mission

These are legal quantum spectral measures. In dimension n+2, use a ground state |g> of energy zero and excited states |j> of energy omega_j. Set

    |v_p>=sum_j sqrt(p_j)|j>,
    A_p=|v_p><g|+|g><v_p|.

Then A_p is Hermitian with norm one and the zero-temperature spectral measure of A_p is exactly the declared parity measure. This finite Hamiltonian has a fixed excitation gap above Omega/2. Its observable is not claimed to be geometrically local.

There is also an efficient circuit fixture on n data qubits and an ancilla. Let `H=a*h*n_ancilla+h sum_i n_i`. A circuit V_p prepares the uniform superposition of n-bit strings of parity p using n-1 Hadamards, n-1 parity CNOTs, and an optional X. The Hermitian unitary

    A_p=|1><0| tensor V_p + |0><1| tensor V_p^dagger

maps the simple ground state to the required excitation distribution. H is a sum of one-qubit terms, with norm Omega; its *response support* is above Omega/2, although other dark excitations have smaller energies. The histogram checks independently recover the binomial parity weights.

Direct occupation/energy sampling of this fixture reveals the parity with one ideal sample. Computing the full response from the explicit formulas is O(n) arithmetic. Thus no lower bound on ordinary algorithms supplied with explicit H and A, no general quantum advantage, and no many-body hardness follows. This distinction is central: exploiting structure can escape a scalar Euclidean information barrier.

For a genuinely unknown complicated system, the stronger operation is acquired ground/Gibbs preparation, a calibrated bounded observable/filter, and energy-transition readout or direct real-time measurement. Astra N810 already supplies a conditional transition-observation construction. For this target the spectral output f(omega) is bounded by one and has derivative at most `T+sigma^2 Omega` on the fixed band. An energy resolution zeta contributes at most `(T+sigma^2 Omega) zeta` bias; attaining fixed bias therefore needs resolution of order 1/T. Preparing the state, applying A, making nondemolition energy readout, and paying evolution time and repetitions are substantive additional resources. No cheap generic implementation was acquired here.

Other legitimate escapes are a physically earned sparse-spectrum/linewidth/regularity model, additional cross-observable data, or asking for a coarser functional that the incumbent already certifies. These alter the input/output contract. Merely changing reconstruction basis, using adaptive imaginary times, removing a known gap, or using the strongest positivity solver does not remove this adversary.

**Actual outcome:** a complete scoped growing-time information obstruction and a constructed-but-defeated response estimator, with a stronger incumbent comparison. The civilisation-changing response capability was not obtained. The missing substantive operation is still affordable non-Euclidean information or independently acquired structural restrictions. No external publication, repository mutation, person-directed message, ZIP, or denied-network retry was performed. There are no pending approvals or unresolved tool outcomes; novelty and independent mathematical review remain unestablished.
