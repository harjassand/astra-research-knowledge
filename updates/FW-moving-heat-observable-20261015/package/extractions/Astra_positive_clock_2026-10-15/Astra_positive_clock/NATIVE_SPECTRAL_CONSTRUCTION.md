# A natively acquired multistate rare clock

Date: 2026-10-15. Source revision: `0c789ca775808e23e57138b56a393ad1e58cb15c`.

## Result and status

This is a new proof candidate extending Astra N592's compressed first-passage construction from supplied two-state probabilities/rates to explicitly supplied rational finite reversible generators. The substantive addition is a native, degeneracy-safe positive spectral acquisition algorithm and its precision accounting. N592 itself explicitly anticipated a finite-component extension, so the generalization idea is not newly discovered here. Neither historical priority nor independent correctness review is established. The included floating-point experiments do not implement the certified finite-bit algorithm.

The construction addresses exponentially large joint-state spaces and potentially astronomically long first-passage times, while retaining arbitrary internal finite reversible dynamics in each independent module. It does not acquire a physically correct generator, certify independence, handle arbitrary preparations, return paths, or solve interacting kinetics.

## Exact contract

Input: n rational row-generators Q_i of dimensions d_i, a designated state a_i in each, and rational 0<epsilon,delta<1/2. Validate off-diagonal nonnegativity, zero row sums, irreducibility, and detailed balance against the exactly computed rational stationary vector pi_i. Let B be total binary input length, d=sum d_i, and L<=sum(d_i-1) the number of positive *visible* local decay modes, counted separately between modules. Modules with d_i=1 can be removed.

The joint chain is the independent product, starts in the stationary product distribution, and H is first passage to the single joint state a. Its atom at zero is q=product pi_i(a_i), exactly rational.

Claim candidate: a finite-random-bit algorithm returns a nonnegative rational Hhat with a coupling satisfying P(|Hhat-H|>epsilon H)<=delta. Expected bit cost is polynomial in B,d,epsilon^-1,log(delta^-1). There is no polynomial dependence on q^-1, inverse spectral gaps, inverse nonzero residues, or rate ratios beyond their encoded bit lengths. The exponent and implementation constants have not been optimized. No unquantized continuous-TV guarantee is claimed.

## 1. Acquire the positive local spectral laws without eigenvectors

For each module compute, over Q[s],

  R_i(s) = [(sI-Q_i)^-1]_(a_i,a_i)
         = det[(sI-Q_i) with row/column a_i removed] / det(sI-Q_i).

Cancel the numerator/denominator polynomial gcd exactly, writing R_i=A_i/B_i. All coefficients have polynomial bit length: fraction-free determinant computation and polynomial gcd suffice. There is no need to factor over algebraic number fields.

Reversibility makes -Q_i similar to a real symmetric positive-semidefinite matrix. Therefore

  R_i(s)=sum_b w_ib/(s+lambda_ib),
  lambda_i0=0, w_i0=pi_i(a_i), lambda_ib>0, w_ib>0, sum_b w_ib=1.

A repeated eigenvalue produces one spectral projector coefficient, hence one simple pole; an eigenmode invisible at a_i cancels. Thus the *reduced* B_i is squarefree. For each root alpha=-lambda of B_i,

  w=A_i(alpha)/B_i'(alpha).

The residue has this sign; no extra minus sign is inserted. This is an exact resolvent identity, not an assumption that a numerically computed eigenvector has a positive squared coordinate.

To order all modes, form the squarefree part of product_i B_i. Its degree is at most d and height is polynomial in B,d. Isolate its real roots by certified rational intervals. Polynomial gcds identify shared roots, and module index breaks rate ties. This avoids an exponentially large compositum of local algebraic fields. Individual roots and residue evaluations remain attached to their own rational polynomial.

### Tiny weights and gaps are acquired, not assumed

Standard integer-polynomial root-separation bounds imply every nonzero rate and every separation of distinct union roots is at least 2^-poly(B,d), while all rates are at most 2^poly(B,d). For residues, clear denominators and use

  Res_s(B_i(s), u B_i'(s)-A_i(s)).

This is a nonzero polynomial in u of polynomial degree/height; its constant term is nonzero because gcd(A_i,B_i)=1. Each visible residue is a nonzero root. The reciprocal Cauchy root bound gives w>=2^-poly(B,d). Certified interval evaluation can therefore produce relative eta approximations to all nonzero rates/residues with polynomial(B,d,log(eta^-1)) bits/work. Exact cancellations are handled before this step; no numerical cutoff silently deletes tiny modes. Root isolation and sign/comparison costs are standard polynomial algebraic-number operations, not supplied oracles. Emiris–Mourrain–Tsigaridas provide a primary reference for isolation, multiplicity, and comparison complexity.

Keep the zero weight exactly pi_i(a_i); approximate positive weights rationally and renormalize to 1-pi_i(a_i), preserving positivity and relative error up to a constant factor.

## 2. Positive renewal law and native strata

Let independent local spectral random variables Z_i take lambda_ib with probability w_ib. Then the target return probability is

  P_a(X_t=a)=product_i sum_b w_ib exp(-lambda_ib t)=E exp(-Lambda t),
  Lambda=sum_i Z_i, P(Lambda=0)=q.

Stationary renewal gives

  E exp(-sH)=q/[q+s E(1/(s+Lambda);Lambda>0)].

This is classical Brown/Fill–Lyzinski territory. Equivalently H is a geometric sum of exponential increments whose random rate is Lambda conditioned positive. Simulating the geometric number costs (1-q)/q expected marks and is not the proposed algorithm.

Totally order all positive pairs (i,b) by (lambda_ib,i), grouping equal modes within a module. A nonzero spectral tuple has one maximal pair u=(i,b). Its stratum weight is

  W_u=w_ib product_(j!=i) F_j(u),
  F_j(u)=sum_{c:(lambda_jc,j)<(lambda_ib,i)} w_jc,

where zero is always included. Its own module is fixed to b; every other module independently takes its spectral categorical law truncated below u. All F_j are positive because they include pi_j(a_j). Thus stratum sampling is explicit and requires no rejection on a rare event. Stratum weights sum to 1-q.

Write a_u=lambda_ib. Conditional rate Lambda_u lies in [a_u,n a_u], even with enormously disparate rates. For V_u|Lambda_u~Exp(Lambda_u), mu_u=E V_u satisfies mu_u a_u>=1/n. A sharper acquired value is kappa_u=E Lambda_u/a_u<=n, but the uniform n bound avoids an additional precision obligation.

Draw E~Exp(1), W=E/q; conditional on W use independent counts C_u~Poisson(W_u W) and marks V_uj. The sum has exactly H's law. This ordinary Cox representation is not new.

## 3. Compression and proof

Let h=epsilon/(2+epsilon) and set M=R=ceil[6n h^-2 log(4L/delta)]. For each intensity r_u=W_u W:

- r_u<R: draw its small Poisson count and sum the marks.
- r_u>=R: draw M marks and return r_u times their sample mean.

Conditional on Lambda_u>=a_u,

  E exp(theta V_u)-1-theta mu_u
  <= theta^2 mu_u/(a_u-|theta|), |theta|<a_u.

Consequently both the compound Poisson sum of mean r_u mu_u and an M-mark mean have multiplicative h deviation at most 2 exp[-h^2 min(r_u,M)/(6n)]. Couple small strata identically. Union bound both large-stratum deviations, then use 2h/(1-h)=epsilon. This reconstructs N592's concentration proof under the *acquired* categorical stratum law.

The ideal expected marks are at most LR=O(L n epsilon^-2 log(L/delta)). Each mark requires n-1 finite categorical draws and one exponential. Precomputed truncated categorical tables occupy O(Ld) entries. Thus arithmetic work is O(L n^2 epsilon^-2 log(L/delta) log(d_max+1)) with binary-search categorical draws, plus acquisition and table construction. This is an upper bound, not a practical performance prediction. Input-reading and local dense algebra can dominate.

## 4. Finite-bit closure, including acquisition error

A conservative implementation follows the N592 bounded-count specification, with h=epsilon/64, ell=ceil(log_2(2^16 L/delta)), R=M=ceil(6n h^-2 ell), K=12R+ell+1, and J=1+L(M+K). J bounds all exposed mark/exponential draws. Since R>=ell, J<=16LR.

Set eta=min(epsilon/4096,delta/(4096LR)). Acquire positive local rates and normalized weights to relative error at most eta/(64n); keep q exact. Products of n local CDF/weight factors then perturb every W_u by at most eta/16, with no q^-1 factor. Truncation/renormalization changes each local categorical law by at most eta/(16n) in TV. Coupling every module choice in every exposed mark fails with probability at most J eta/16<delta/4096. Rates summed from coupled choices retain the same relative error, regardless of their numerical ratio.

Generate bounded-bit exponential approximations with relative error <=eta/16 off an endpoint event of probability <=delta/64, using the explicit midpoint-uniform/log-series procedure in N592. Form Wtilde=Etilde/q. Relative intensity error remains <eta/4.

Branch on approximated intensity at 2R: a large branch has true intensity at least R; a small branch has true intensity at most 4R. Compute small Poisson probabilities up to K with the N592 finite rational table and total rounding/tail probability <=delta/(256L). Its work is polynomial because mean<=2R. Couple small true/approximate counts by one Poisson process: mismatch probability is bounded by the endpoint difference, totaling at most LR eta<delta/4096. Thus no tiny spectral-weight error is multiplied by a huge physical count in the large branches.

For each large branch, concentration uses *true* marks and intensity. The approximated M exposed marks are coupled to these, whereas the enormous exact Poisson count remains a proof variable. h=epsilon/64 leaves ample slack for the relative intensity, rate, and exponential errors. All finite sums preserve relative error. Union of the displayed budgets plus the concentration budget is less than delta; the relative output error is below epsilon. All rational products/sums have polynomial bit length in B,d,J,log(eta^-1). Exact rational categorical sampling has fewer than two expected power-of-two rejection attempts. This yields an expected polynomial bit bound, not a worst-case exact-real guarantee.

This is a detailed proof candidate; a separate implementation must verify interval constants and tables. The delivered experiments use floating point and do not certify this finite-bit algorithm.

## 5. Metrics and preparation limitation

The stationary reversible killed-chain survival law is a positive exponential mixture, so t f_H(t)<=1/e. Therefore the relative coupling implies Kolmogorov distance <=delta-log(1-epsilon)/e. Finite-bin TV additionally charges bin boundaries, as in N592. Continuous TV remains inappropriate for finite rational outputs.

For arbitrary initial law alpha, renewal has numerator integral P_alpha(X_t=a) exp(-st)dt, which is not q/s. Its spectral coefficients need not be positive. The above algorithm cannot silently replace an experimentally prepared molecular state with stationarity. Our synthetic two-module example has stationary CDF(100)=0.250931, but both modules prepared in the slow state gives CDF(100)=0.000003727. Stationary initialization is a consequential input assumption.

## 6. Strong comparators and experimental results

The most relevant scalable comparator is Horvath–Paolieri–Vicario's product-component ODE closure, not only the full joint matrix. It supports more general starts/targets and nonreversible components; this construction supports a narrower contract with a tunable coupling guarantee. Also compare an exactly mean-matched exponential whenever a computable Brown error certificate permits it, direct geometric sampling when q is moderate, and exact phase-type/lumped solutions when the model has small aggregate dimension. No practical superiority over these has been established.

`results.json`:
- Exact rational gcd cancellation handles a repeated complete-graph mode and an invisible path mode. Both yield (s+1)/(s(s+3)) with zero residue 1/3.
- A rational nonsymmetric reversible three-state input yields rates (47±sqrt(537))/4, residues 5/22±103sqrt(537)/11814 (opposite sign ordering by rate), and exact stationary residue 6/11. `exact_spectral_certificate.json` supplies exact expressions and 30-decimal rational root-isolating intervals.
- A heterogeneous 27-state joint generator and the product spectral resolvent agree within 5.9e-16 at four Laplace points. This is floating-point consistency only.
- A rare four-module example q~1e-12 used mean 14,796 exposed marks versus ~1e12 for naive geometric expansion. This is a comparison to that primitive only; the model has only 81 joint states, and its law is close to exponential, so it is not evidence that compression is needed.

`comparison.json`:
- Two three-state modules: pi=(.1,.4,.5), conductances c01=.4,c12=1e-5. Exact stationary CDF(100)=0.250931; the stationary HPV Eq.(6) closure gives 0.999668. 10,000 clock samples give 0.2515.
- Exact mean is ~62,514; mean-matched exponential CDF(100)~0.001598. A single exponential fails in the opposite direction.
- This is a decisive mathematical counterexample to those approximations, but only a nine-state system. Direct Brown costs 99 expected marks; no scalable advantage follows.

`nonexponential.json` tests rare, slow-module scaling with forty fast two-state modules plus a three-state module. q=9.094947e-14 and the Brown exponential diagnostic D=0.717775. At s=1/mean, the exact Laplace transform is 0.621979, versus 0.5 for a mean-matched exponential. One hundred compressed draws used ~1,124,666 exposed marks each and 51.84 seconds total in this environment; empirical transform 0.574028 has Monte Carlo SE 0.037096, so this is only a small-sample consistency check. Identical fast modules permit a 123-state lumped comparator, which is explicitly retained. This test demonstrates simultaneously rare/nonexponential behavior, not superiority to lumping.

## 7. Scientific acquisition and stopping gate

A natural use is stationary synchronization of independent multistate reversible conformational/kinetic modules. The exact input must come from supplied generator models or a separate data-calibration effort. The acquisition contract starts at rational Q_i, not raw trajectories. Markov adequacy, detailed balance, independence, coarse-graining error, and preparation stationarity require experimental/model validation. No real dataset was acquired here and no physical claim follows from these synthetic calculations.

The next decisive gate is a heterogeneous, non-lumpable, independently justified kinetic family with rare target and a failed certified exponential shortcut. Compare total acquisition plus repeated-query time against the product ODE, exact/structured phase-type solvers, and a calibrated approximation budget. Until then, the deliverable is a general computational theorem candidate, not a civilization-scale capability or scientific discovery.

## Sources and exact routes

Astra 00_START_HERE.txt and frontier/dossiers/N592.txt were read at the pinned revision. Decisive proof files:
- updates/CK/package/distinct_capability_20261010/02_main_construction.md, lines 1–162, hash 4cb1eaf1a082a643cf77ec1196da3730eb6f5af0655800ed7128fb5d823083cc.
- updates/CK/package/distinct_capability_20261010/03_finite_bit_specification.md, lines 1–111, hash e283d579bc7e90e5f5a472e52da001690e2f56a75e4c2dff5dc47e5f7ddedcf1.

Primary external comparators:
- Fill–Lyzinski, Hitting times and interlacing eigenvalues: https://www.ams.jhu.edu/~fill/papers/intertwinings.pdf
- Horvath–Paolieri–Vicario, Approximation of First Passage Time Distributions of Compositions of Independent Markov Chains (2025), particularly Eq.(6): https://qed.usc.edu/paolieri/papers/2025_epew_first_passage_replicated_components.pdf
- Emiris–Mourrain–Tsigaridas, Real Algebraic Numbers: Complexity Analysis and Experimentation: https://who.paris.inria.fr/Elias.Tsigaridas/b2hd-emt-lncs-2006.html
- Sagraloff, On the Complexity of Real Root Isolation: https://arxiv.org/abs/1011.0344

No canonical repository edits, publication, spending, outreach, or acquisition of a scientific dataset occurred.
