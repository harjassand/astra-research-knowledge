# Fixed-temperature obstruction at growing real time and fixed transition bandwidth

Date: 2026-11-04. Separate extension; the original zero-temperature proof, script, and receipt remain unchanged.

Status: root proposed the normalized finite-beta construction; the independent constructor audited the algebra, sharpened the uniform bound by a factor of two, checked the physical realization and its costs, and executed the diagnostics below. The analytic argument is complete at its specified-oracle scope. No formal verification, external review, locality theorem, full-Hamiltonian complexity lower bound, or novelty claim follows.

## Fixed parameters and growing-time family

Fix beta>0, Omega>0, sigma>=0, and 0<alpha<1/2 independently of n. Use exactly the original parity probability weights p_even,p_odd on

    a=n+1/2, h=Omega/(2n+1/2), omega_j=h(a+j), j=0,...,n,
    T_n=pi/h=pi(2n+1/2)/Omega,
    p_even,j=2^(1-n) binom(n,j) 1_(j even),
    p_odd,j =2^(1-n) binom(n,j) 1_(j odd).

Their response-transition support stays in the fixed band [Omega/2,Omega]. The center T_n grows linearly with n; beta and the Gaussian temporal smearing width sigma stay fixed. The underlying spectrum/Hamiltonian may change with n and parity.

Define the ordinary Laplace transform, normalization, and thermal Euclidean correlator by

    C_p(t)=sum_j p_j exp(-t omega_j),
    W_p=1+C_p(beta),
    C_p^beta(tau)=[C_p(tau)+C_p(beta-tau)]/W_p, 0<=tau<=beta.

The output is the Gaussian-temporally-smeared odd commutator response, up to an overall sign convention:

    F_p^beta(T)=sum_j p_j [1-exp(-beta omega_j)]
                    exp(-sigma^2 omega_j^2/2) sin(omega_j T)/W_p.

The fixed-beta query oracle returns either this scalar Euclidean mean plus independent Gaussian noise of specified variance v>0, or a Bernoulli bit with mean C_p^beta(tau). These are two distinct observation laws. Adaptive tau choices and private random seeds are permitted, with at most M queries. A deterministic absolute-error version is also valid. Full sampled configurations, simultaneous vector observations with exploitable noise correlations, exact partition functions, explicit H/A descriptions, other observables, and temperature changes are outside this oracle contract.

## Normalization and a genuine Gibbs realization

For every positive p_j, form a two-level block with energies

    E_j,lower=-log(p_j)/beta + E_shift,
    E_j,upper=E_j,lower+omega_j,
    A_j=Pauli X.

Omit zero-weight blocks. The common shift is arbitrary. The partition function is `Z=exp(-beta E_shift) W_p`, so the canonical lower and upper probabilities are exactly `p_j/W_p` and `p_j exp(-beta omega_j)/W_p`. A is a direct sum of Pauli X matrices, hence is Hermitian, unitary, and has norm one.

Direct evaluation of `Tr[exp(-(beta-tau)H) A exp(-tau H) A]/Z` gives precisely C_p^beta(tau). The imaginary part of the thermal real-time correlator gives the stated sine response. This is a finite-temperature Gibbs system, rather than a probability measure asserted to have an unspecified thermal interpretation.

The compressed block realization uses O(n) levels, but its total Hamiltonian energy spread grows as O(n/beta). A common shift does not remove that spread. Thus fixed *transition* bandwidth must not be described as fixed total Hamiltonian bandwidth for this compressed realization. If equal Hilbert-space dimensions are desired, split one nonzero p_j into several identical-gap blocks with positive subweights; this preserves both formulas.

A second realization below keeps the total Hamiltonian norm bounded using n qubits. It has exponentially many levels, as an n-qubit space ordinarily does; it does not require exponentially many qubits.

## Response gap at fixed beta and fixed smearing

At T_n, `sin(omega_j T_n)=(-1)^(n+j)`. Each parity response therefore has one sign and the other parity has the opposite sign. Put `g_min=exp(-sigma^2 Omega^2/2)`. For either p,

    |F_p^beta(T_n)|
      >= g_min [1-C_p(beta)]/[1+C_p(beta)]
      >= g_min tanh(beta Omega/4),

because every omega_j>Omega/2 and hence `C_p(beta)<=exp(-beta Omega/2)`. Thus

    G_n^beta:=|F_even^beta(T_n)-F_odd^beta(T_n)|
      >= 2 tanh(beta Omega/4) exp(-sigma^2 Omega^2/2)>0.

This lower bound is independent of n. Any fixed target error

    epsilon < tanh(beta Omega/4) exp(-sigma^2 Omega^2/2)

is less than half the universal pair separation. For beta=Omega=sigma=1, epsilon=0.1 is an admissible illustrative choice. An error of 1/2 from the zero-temperature example cannot be carried over to these thermal parameters.

For a Gaussian convolution of the causal response restricted to t>=0, the single-input correction is at most Phi(-T_n/sigma), since the unsmeared response is bounded in magnitude by one. The separation is at least the displayed bound minus `2 Phi(-T_n/sigma)` and retains the same positive lower limit at growing time. For sigma=0 and T_n>0 the causal and odd-continuation values coincide.

## Sharpened all-tau normalized difference bound

The original exact binomial identity is

    delta C(t):=C_even(t)-C_odd(t)
      =2^(1-n) exp(-a h t) [1-exp(-h t)]^n >=0.

Define

    d_n=2^(1-n) (h beta)^n
       =2 [beta Omega/(4n+1)]^n.

For every tau in [0,beta], positivity and `1-exp(-x)<=x` give

    delta A:=delta C(tau)+delta C(beta-tau)
      <=2^(1-n) h^n [tau^n+(beta-tau)^n]
      <=d_n,

where the last inequality holds for every integer n>=1. Also `delta W=delta C(beta)<=d_n`.

To control the normalization, write the exact identity

    C_even^beta(tau)-C_odd^beta(tau)
      =[delta A-C_odd^beta(tau) delta W]/W_even.

For each omega and 0<=tau<=beta,

    exp(-tau omega)+exp(-(beta-tau)omega) <=1+exp(-beta omega),

since `(1-exp(-tau omega))(1-exp(-(beta-tau)omega))>=0`. Therefore `0<=C_odd^beta<=1`. Both nonnegative terms in the numerator identity lie in [0,d_n], and W_even>=1. It follows that

    sup_(0<=tau<=beta) |C_even^beta(tau)-C_odd^beta(tau)| <=d_n.

Root's initially proposed `epsilon_n=2 d_n=4[beta Omega/(4n+1)]^n` is valid. The subtraction of two nonnegative bounded terms improves it to d_n. This argument does not assume the normalized difference has one sign; it need not have the zero-temperature sign.

For small n or very large beta the expression d_n may exceed one, yielding a trivial valid bound. One may replace it with min(1,d_n). The claimed superexponential asymptotic is at fixed beta*Omega as n grows, where d_n tends to zero.

## Adaptive oracle lower bounds

For deterministic ordinate errors of size at least d_n/2, the transcript

    y(tau)=[C_even^beta(tau)+C_odd^beta(tau)]/2

is compatible with both thermal systems at every query. Any uniformly valid output interval on this transcript must span the full thermal response pair.

For independent Gaussian noise of variance v per scalar query, the same adaptive chain-rule argument as in the original proof gives

    KL(P_even||P_odd)<=M d_n^2/(2v).

If the output achieves absolute error epsilon<G_n^beta/2 with probability at least 1-alpha for each input, midpoint thresholding gives a binary test with both errors at most alpha. Pinsker yields

    M >=4v(1-2alpha)^2/d_n^2
      =v(1-2alpha)^2 [(4n+1)/(beta Omega)]^(2n).

For a Bernoulli-bit oracle of mean C_p^beta(tau), each conditional query can be maximally coupled with disagreement probability at most d_n. Couple the algorithms with the same seed while their histories agree. Then `TV(P_even,P_odd)<=M d_n`, giving

    M >=(1-2alpha)/d_n
      =[(1-2alpha)/2] [(4n+1)/(beta Omega)]^n.

Both bounds are superexponential in n at fixed beta, Omega, sigma, alpha, and fixed admissible epsilon. Since T_n is linear in n, their logarithms grow respectively as `2n log n+O(n)` and `n log n+O(n)`, or as a constant times `T_n log T_n` to leading order. These are growing-time worst-case bounds, not fixed-time precision theorems and not statements about the actual raw observation law or computational runtime of arbitrary QMC algorithms.

The Bernoulli statement permits signal-dependent variance, including deterministic means at tau=0,beta. It does not convert a Gaussian mean estimator into a Bernoulli instrument. The bounded fixed-beta correlator makes the specified bit oracle mathematically well-defined. Full block/energy labels contain more information than its single bit.

## Bounded-norm n-qubit realization with local A

Use n-1 data bits x and one ancilla b. Let `n_i=(I-Z_i)/2`, `n_b=(I-Z_b)/2`, and set

    q_p(x)=[1-(-1)^p product_(i=1)^(n-1) Z_i]/2,
    H_p=n_b h [a+sum_(i=1)^(n-1) n_i+q_p(x)],
    A=X_b.

Here p=0 is even and p=1 is odd, and a=n+1/2 is the scalar defined earlier. The empty product at n=1 is one, so q_p=p and the construction is a single valid two-level system.

Every ancilla-zero basis state has energy zero. Its paired ancilla-one state has energy `h(a+j)`, where `j=sum_i x_i+q_p(x)` has parity p. The map appends the unique nth bit that makes the n-bit string have parity p. Consequently each allowed j occurs exactly binom(n,j) times. There are `2^(n-1)` two-level blocks and dimension `2^n`, with the same dimension for either parity. The partition function is `2^(n-1) W_p`; aggregating equal-gap blocks reproduces the stated normalized thermal correlator and response.

The Hamiltonian is diagonal, nonnegative, and has norm at most Omega; its gap above its degenerate ground manifold is greater than Omega/2. A is the same one-qubit Pauli operator under both hypotheses. Expansion of H gives star two-body number terms and one term acting on all n qubits. No fixed-body, geometric locality, or laboratory implementation is claimed. Root supplied this compact Hamiltonian expression after the independent constructor identified the equivalent degeneracy realization.

This bounded-norm realization removes an otherwise unnecessary growing-total-energy assumption. It does not make the oracle theorem a full-Hamiltonian complexity result: the explicit sign of the parity term reveals p immediately, and the model is diagonal and classically simple.

## Exact original moments and the optimal positive-measure incumbent

Define thermal block weights and kernels

    nu_p,j=p_j[1+exp(-beta omega_j)]/W_p,
    k_j(tau)=[exp(-tau omega_j)+exp(-(beta-tau)omega_j)]
                 /[1+exp(-beta omega_j)],
    f_j=tanh(beta omega_j/2) exp(-sigma^2 omega_j^2/2) sin(omega_j T_n).

Then nu_p is a probability measure, `C_p^beta=K nu_p`, and `F_p^beta=f dot nu_p`. Thus the ordinary optimal finite positive-measure LP applies directly; no special reconstruction method is needed. The original p moments through n-1 still agree, but moments of nu generally do not, and are not silently granted.

If the shared original-p moments m_k are additionally supplied, they translate into the linear homogeneous constraints

    sum_j nu_j (omega_j^k-m_k)/[1+exp(-beta omega_j)]=0,
    k=1,...,n-1.

Normalization of nu provides the remaining constraint. The map `nu_j=p_j(1+r_j)/(1+sum p r)` is a positive projective transformation. It maps the original p moment segment onto the segment between nu_even and nu_odd. Both endpoints remain compatible with the midpoint correlator at tolerance d_n/2, so the exact endpoint response ambiguity persists even with these granted moments and known atom locations. Exact W_p, in contrast, differs between hypotheses and is outside the oracle contract.

Nine finite LP comparisons implemented this strongest same-data restriction with 65 thermal ordinates, known atoms, and the exact original-p moment constraints. Each returned the explicit pair interval to floating tolerance. These are diagnostics, not rational or outward-rounded certificates. The analytic pair remains sufficient against any valid continuum positivity method because both inputs are physically admissible.

## Adversarial checks and actual cost

`check_fixed_temperature.py` and `thermal_results.json` are separate from the original files. The run used 500-decimal-digit mpmath arithmetic, Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0. It checked:

- 40 parameter cases: n in {1,2,4,8,10,20,40,80}, beta in {0.01,0.1,1,10,100}, with Omega=sigma=1.
- 5,160 fixed-beta imaginary-time grid points against the *analytic* all-tau d_n bound; sampled maxima are not advertised as certified maxima.
- 400 explicit canonical trace evaluations from the compressed block energies, plus the thermal response and partition normalization in every case.
- 24 independently enumerated n-qubit Hamiltonian/degeneracy cases, n=1,...,12 and both parities, including the empty-product special case n=1.
- Nine optimal finite positive-measure LP comparisons with the transformed original-p moment constraints.

All passed. The initial automatic near-equality tolerance at the full 500-digit machine precision was too strict for a repeated-power arithmetic identity; setting an explicit relative tolerance of 1e-480 resolved this numerical check. No analytic bound or conclusion changed. Trace comparisons used absolute tolerance 1e-430. No Monte Carlo configurations or physical measurements were acquired. The final script run took 10.577 seconds, with no external compute spend.

At beta=Omega=sigma=v=1, alpha=0.05, and admissible fixed target error epsilon=0.1:

| n | growing T_n | d_n, valid uniform difference bound | actual response separation | Gaussian query lower bound using d_n | Bernoulli query lower bound using d_n |
|---:|---:|---:|---:|---:|---:|
| 4 | 26.704 | 2.395e-5 | 0.53357 | 5.650e9 | 3.758e4 |
| 10 | 64.403 | 1.490e-16 | 0.53774 | 1.459e32 | 6.040e15 |
| 20 | 127.235 | 1.353e-38 | 0.53932 | 1.770e76 | 6.651e37 |
| 40 | 252.898 | 1.067e-88 | 0.54015 | 2.848e176 | 8.438e87 |
| 80 | 504.226 | 6.034e-201 | 0.54057 | 8.898e400 | 1.491e200 |

For n=40 the sampled maximum normalized difference was 3.300e-89, below d_n. Only the analytic d_n was spent in the displayed query lower bounds. No grid-derived strengthening is claimed.

## Scope and substantive outcome

The fixed-temperature extension is valid, with the tighter d_n constant. In a bounded-norm n-qubit realization it has fixed beta, fixed transition band and gap, fixed smearing width, and a fixed nonzero thermal response ambiguity at growing time. The scalar fixed-beta Euclidean oracle requires superexponentially many queries under either stated observation law.

The inputs are different systems at successive n and parity. H includes an n-body term; no local many-body hardness follows. Full H/A access, transition energy labels, other observables, exactly known partition functions, stronger noise models, or changing beta can escape the stated information boundary. The fixture admits cheap direct structural calculation. Generic preparation, energy resolution, coherent evolution, and measurement costs remain separate paid operations. This strengthens the scoped proof-only failure of the Euclidean route; it supplies no new response capability or reactor/materials claim.

The original source comparisons and novelty limitations remain in `../PROOF_AND_OUTCOME.md`; the fixed-beta kernel is also checked directly from the Gibbs trace here, so no new external source is required as a premise. Original proof/script/results bytes were preserved. No external publication, ZIP, repository mutation, person-directed message, approval request, or denied-source retry occurred.
