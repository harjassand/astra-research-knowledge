# N722 composition audit — appended delta

**Scope.** Separate delta for the frozen FJ-nonlinear packet. The earlier report and manifest remain untouched. I reconstructed the FJ/N722 composition from pinned source and original N722 theorem/code, ran bounded copy-first checks, inspected primary FORS literature, and audited the sinh extension in the ideal-real model. No other FJ worker result was read.

## Finding and theorem composition

The composition works for a fixed finite list of points if the global FJ tube certificates hold and every N722 oracle call returns a fresh iid whole vector. It yields a Gaussian perturbation centered at the unique-in-tube PDE solution vector, with full-joint-law TV error. N722's sampler is already the positive Poisson factory from first-order rejection sampling (FORS); the application and cost accounting may be useful, but the Gaussian operation is not new.

For fixed x_i, FJ gives |Z_i|≤1 and E[h_i Z_i]=u(x_i)−v(x_i). At sigma>0, define one vector acquisition by

```
X = (h_i Z_i / sigma)_{i=1}^r
E[X] = ((u(x_i)−v(x_i))/sigma)_{i=1}^r
||X||_2 ≤ R = ||h||_2/sigma.
```

Coordinates within one vector need not be independent. Whole vectors across acquisitions must be iid with this fixed mean and known a.s. radius. The point list/radii must stay fixed; adaptive changes based on prior N722 outputs invalidate the stated oracle model without a new theorem.

N722 uses

```
m = ceil(64(1+R^2) log(64(1+R^2)/epsilon_g))
```

and returns Y within epsilon_g in TV of N(E[X],I_r). By affine invariance, v_vec+sigma Y is within epsilon_g in TV of N(u_vec,sigma^2 I_r). This is a finite-dimensional Gaussian perturbation around the local PDE solution, not a field-wide draw or physical/posterior uncertainty law, and not an estimate of u_vec to accuracy sigma·epsilon_g. TV to an unbounded Gaussian does not control its mean functional. Smaller sigma increases R^2=sum_i h_i^2/sigma^2 and acquisition cost.

## Expected work, including value-dependent costs

For coordinate i, FJ gives a.s. termination and expected node count ≤ Lambda_i/(lambda_i−Gamma_i(h_i)). Let C_X include setup, every coordinate tree, endpoints, coefficient work, and reading one full vector. If node i costs at most c_i, then

```
E[C_X] ≤ C_setup + sum_i c_i Lambda_i/(lambda_i−Gamma_i(h_i)).
```

Each N722 factor proposal uses J~Poisson(2) vectors and accepts with probability a≥exp(−2), so expected vectors per accepted factor are 2/a≤2e^2. Unit-cost expected source nodes are ≤2e^2 m sum_i Lambda_i/(lambda_i−Gamma_i(h_i)); insert c_i for weighted work and add one-time certificate/predictor costs. Factory arithmetic/output adds O(rm). These are expected-work bounds, not hard caps.

Tree cost may correlate with that proposal's acceptance. If C_j is cost of proposal j and T the first accepted proposal, {T≥j} depends only on earlier trials and is independent of the current trial pair (C_j,success_j). Thus

```
E[sum_{j≤T} C_j] = sum_{j≥1} P(T≥j) E[C_1] = E[C_1]/P(accept).
```

No within-trial cost/success independence is required, provided each complete fresh vector is acquired before the decision. The exact rational check uses success probability 1/10, success cost 100, failure cost 1; total expected cost is 109. Correlated/reused trees, adaptive points, or value-selected partial vectors can break the oracle law.

For equal radii h_i=h, R^2=r h^2/sigma^2; vector-call count grows with r, and a direct call evaluates about r point trees. Naive source-node work is quadratic in r up to logs, not a dimension-free field sampler. Averaging N722 outputs to estimate the center also does not evade mean-estimation cost: error epsilon takes order sigma^2/epsilon^2 outputs, each with vector-call count scaling as ||h||_2^2/sigma^2.

## N722 reconstruction and novelty limit

Original N722 specifies an iid bounded-vector oracle X with known radius R and unknown mean mu, and an ideal-real sampler close in full-law TV to N(mu,I_d). A factor proposal y~N(0,I_d/m) draws J~Poisson(2), obtains fresh X_j, and accepts with product_j (1+clip(<y,X_j>))/2. For w_hat(y)=E[clip(<y,X>)], the Poisson formula is

```
P(accept|y) = sum_{j≥0} exp(−2) 2^j/j! ((1+w_hat(y))/2)^j
            = exp(w_hat(y)−1).
```

The accepted density is proportional to q_m(y)exp(w_hat(y)), normalized and positive, with acceptance ≥exp(−2). Calls per factor solve Q=2+(1−a)Q, so Q=2/a≤2e^2 even though J and same-proposal acceptance are dependent. The unclipped tilt q_m(y)exp(<y,mu>) is N(mu/m,I_d/m). Projection-tail control gives per-factor TV ≤10 exp(−m/(8R^2)); product-TV plus summation contraction gives total TV ≤10m exp(−m/(8R^2))≤epsilon_g for the displayed m.

This is exactly the B=1 positive Poisson product factory in Chen, Chewi, Daskalakis, and Rakhlin, FORS Algorithm 1/Theorem 3.1. Their later primary stochastic-query Gaussian-tilt theorem also covers the capability: f(y)=−<mu,y>, gradient oracle −X, x_0=x_hat=0, ||X−mu||≤2R; step variance 1/m gives factors N(mu/m,I/m), whose m-fold sum is N(mu,I). N722 supplies explicit constants/projection-tail details, but not a new same-oracle operation. Sample-mean plug-in is not the right comparator.

Defensible application-level claim: the FJ certificate supplies an acquired iid bounded vector-gradient oracle whose mean is transported into a selected Gaussian-smoothed finite-dimensional law with TV and expected-work accounting. No acquisition-inclusive advantage or operation beyond FORS was established.

## Source compatibility and finite-bit limits

FJ requires a global residual bound, 0<lambda≤V≤Lambda, uniform absolute power-series control, enclosure R_residual+P(h)≤lambda h, and strict Gamma(h)<lambda. These yield a unique solution in the tube, bounded hZ, correct expectation, and finite expected tree work. They do not identify an arbitrary intended branch if the PDE has multiple global branches.

Each vector call pays for all requested trees and outputs. Prove R from source bounds rather than finitely observed outputs. Include predictor/certificate construction and verification, setup/burn-in, endpoint and coefficient costs in comparisons; finite residual grids/training loss do not establish global tube conditions.

The theorem is ideal-real. FJ needs exact endpoint/branch decisions; N722 needs exact Gaussian/uniform/Poisson/acceptance operations. Finite floating output has finite support and TV distance 1 from a continuous Gaussian. Copied N722 code uses float normals/dots/acceptance and allows 1e−12 norm overshoot; this does not certify a.s. radius. FJ prototype likewise allows 1e−12 probability-bound drift. A finite-bit claim needs a quantized target or rigorous interval/random-bit construction with explicit total arithmetic error.

## Bounded copy-first checks

Checks ran on copies under N722-delta-source-copy; pinned sources remain read-only.

- Exact Fraction replay of copied FJ verifier passed both supplied certificates. Constant predictor q=5425/12928, E[N]≤12928/7503; predictor B passed. h=1/20 fails enclosure; h=3/10 passes enclosure but fails strict work.
- Copied N722 diagnostic: 20 outputs per finite-support scalar oracle, epsilon=0.1, seed 20261014, all four source cases. It observed 5.46–5.59 acquisitions/factor. Symmetric-law quadrature was zero; other high-m values were near floating precision. Smoke evidence only, not an independent TV proof or exact sampler validation.
- N722_composition_checks.py checks exact Fraction radius scaling, quartic q/node constants, Poisson boundary cases, cost-correlated renewal, and sinh factorial-ratio bounds. JSON includes R=0 (zero-acquisition shortcut), reflection-symmetric X (exact centered Gaussian in ideal model), deterministic X=a (only projection clipping tail), and worst acceptance w_hat=−1.

## Sinh extension: degree selection and node-count cap

For V=kappa^2 cosh(v), source bounds are

```
sum_{m≥2}|c_m|h^m/V ≤ exp(h)−1−h
sum_{m≥2}m|c_m|h^(m−1)/V ≤ exp(h)−1.
```

If delta=sup_x|r(x)|/V(x)≤2h+1−exp(h), 0<h<log(2), probabilities are valid; offspring mean ≤1−g with g=lambda(2−exp(h))/Lambda>0, hence E[N]≤1/g.

For even m≥2, weights h^m/m! sum to cosh(h)−1; odd m≥3 sum to sinh(h)−h. Choose parity with masses

```
A_even = kappa^2 |sinh(v)| (cosh(h)−1)
A_odd  = kappa^2 cosh(v) (sinh(h)−h).
```

Then inverse-CDF sample within parity using w_m=h^m/m!, w_(m+2)/w_m=h^2/((m+1)(m+2)). Since h<log(2)<1, ratios are below 1/12 (even) and 1/20 (odd). The inversion terminates a.s. with bounded expected scans; conservative bounds are 144/121 and 400/361. Exact hyperbolic-function evaluation and certified finite-bit comparisons remain open.

There is an exponential node-count tail despite unbounded offspring degree. Let H_y(s)=E[s^K|Y=y], including the no-offspring mass. Factorial coefficients and bounded v on the compact torus make H_y(s) uniformly finite for finite s>0; the offspring gap gives sup_y H'_y(1)≤1−g. Hence some s0>1 has H_*=sup_y H_y(s0)<s0. With z=s0/H_*>1, tree recursion gives sup_x E[z^(T_n)]≤s0 and P(T>k)≤s0 z^(−k). Abort after k≥ceil(log(s0/delta_T)/log(z)) nodes and return a fixed bounded fallback; output-law error is at most delta_T. This caps node count, not endpoint time, bit operations, or degree-inversion work.

For finite degree K≤D with mean ≤1−g, depth-first queue increments K−1 lie in [−1,D−1] and drift at most −g. Conditional Hoeffding plus Chernoff gives

```
P(T>n) ≤ exp(4g/D^2 − 2g^2 n/D^2).
```

Thus cap n≥D^2(4g/D^2+log(1/delta_T))/(2g^2) makes fallback error ≤delta_T; quartic D=4 gives exp(g/4−g^2n/8). A composed N722+FJ cap must also cap outer rejection and Poisson counts. FORS Theorem 3.1 gives high-probability O(e^2(m+log(1/delta_o))) queries for m factors, B=1. With outer vector cap Q_max and per-coordinate tree errors delta_i, coupling budget is epsilon_g+delta_o+Q_max sum_i delta_i; worst endpoints Q_max sum_i n_i. Exact bit/transcendental work remains uncapped.

## Scoped uncentered separation

For the source independent-product uncentered quartic tree, let m(x)=E|W_x|. Conditioning on the first event and Tonelli for nonnegative descendant absolute values gives

```
m = R_1(|s| + 25m^4),   R_1 = (−d_x^2+1)^−1.
```

The periodic resolvent kernel is strictly positive and R_1 1=1. If m(x0)<infinity anywhere, positivity forces m^4 integrable and m finite a.e. Set w=ess inf m. Since s=26+10g≥16, m(x)≥16+25w^4, so w≥16+25w^4, impossible for w≥0. This gives infinite absolute expectation at every starting point for this specified representation only; it is not a lower bound against alternative trees, Newton/MLP, or deterministic solvers.

## Novelty comparators and limits

- Agarwal–Claisse (2020), §§2.2/3.3, Props. 3.4–3.5: branching and nonnegative supersolution criteria for absolute-q moment/integrability bounds. FJ's positive tangent/explicit expected-node certificate is at most a useful specialization pending historical comparison.
- Fan et al., ICLR 2026 SCaSML: defect PDE around a surrogate solved stochastically. Predictor-plus-Monte-Carlo correction is prior art; no matched cost comparison was done.
- Bossy et al., arXiv:1411.2304v3: branching Brownian representation/Monte Carlo for nonlinear sinh Poisson–Boltzmann. Problem geometry differs, but sinh branching itself is not new.
- Beck–Gonon–Jentzen (2024): MLP for semilinear elliptic PDEs with globally Lipschitz reaction. Quartic is not globally Lipschitz; tube-preserving extension, domain/norm/branch transfer, and cost comparison remain unproved. Supplied 1D Fourier baseline is much faster.
- N722/FORS covers the positive Poisson factory and stochastic Gaussian tilt. Plausible contribution is the acquired FJ bounded-gradient interface and application accounting, not the sampler.

## Read/access ledger

Pinned workspace: work/FJ_PIN.json (main ace0cfc4437fe91c20ccd24d69e0ee4bb335e871; checkout cb62d881a071c617b11d7dbc82a98921969389a). Original FJ source manifest: 21 files/223,218 bytes. No other FJ worker result was read.

| Source | Scope | SHA-256 |
|---|---|---|
| FJ research_note.md | Lines 13–102 theorem/tree/proof/concentration; 104–117 cost; 121–206 quartic/uncentered; 208–245 sinh; 247–253 prior art. | a843a6cdfc1f0b55b25dbe1dd1b24ba2b157f7f4c67e51e5fcbc28f080c721f0 |
| FJ nonlinear_query.py | Lines 44–66 floating certificate; 70–77 predictor/residual; 80–127 sampler/guard. | 829f370818ca2cf0de04b9930f09de5bd2cd1d3f35987a7a24dd55c894e861e4 |
| FJ verify_certificates.py | Lines 13–48 exact rational checks. | dfdbcad1f43ac71283e269c2e8f21ecc69a0346554ccc94edf6fadc5d17c706e |
| N722 THEOREM.md | Lines 7–149 interface/algorithm/proof/m; 151–178 FORS; 188–210 acquisition/precision; 212–241 evidence boundary. | f696de4d60c3313e7b0fd122941c6a57a887390e9d6e95d0727fe16ae66e7b9b |
| N722 gaussian_factory.py | Lines 36–124 factory; 141–240 diagnostics/scope. | 1a30f526a3fcec0a45c66d799c137856a302b12158c1635b11636f5d5a55a58c |
| Chen et al., FORS | arXiv:2602.01338v2, §3.1, Alg. 1/Thm. 3.1. | https://arxiv.org/html/2602.01338v2 |
| Chen et al., stochastic-query Gaussian tilts | arXiv:2602.14342v2, §§3.1–3.2/Thms. 3.1–3.2, §4.1. | https://arxiv.org/html/2602.14342v2 |
| Agarwal & Claisse | 2020, §§2.2/3.3, Props. 3.4–3.5. | https://eprints.gla.ac.uk/210343/7/210343.pdf |
| Fan et al. | Official ICLR 2026 SCaSML record. | https://proceedings.iclr.cc/paper_files/paper/2026/hash/cf8353a0efc3644454a5591a7cb55c17-Abstract-Conference.html |
| Beck, Gonon & Jentzen | 2024, Thm. 3.16 / Thm. 1.1 and eqs. (10)–(13). | https://link.springer.com/article/10.1007/s42985-024-00272-4 |
| Bossy et al. | arXiv:1411.2304v3, §§3.1–3.3. | https://arxiv.org/html/1411.2304v3 |

Delta-owned additions: this report, N722_composition_checks.py/.json, and N722-delta-source-copy/ (byte-identical source copies plus exact-certificate and bounded-diagnostic outputs). N722_DELTA_MANIFEST.json records hashes; frozen OWNED_MANIFEST.json is unchanged.

