# A finite-bit coherent oracle for integrated telegraph paths

**Status:** Constructive mathematical candidate, not yet independently reviewed or implemented. This note proves the source-oracle construction proposed below; acceptance of the complete quantum simulation theorem additionally requires its Hamiltonian-simulation and controlled-process receiving arguments.

**Date:** 31 October 2026.

## 1. Task, output, and scope

Let a sign process xi(t) start with an independent uniform sign and flip at rate lambda > 0. On a fixed interval [0,T], define

    W(t) = v integral_0^t xi(s) ds,       v = sqrt(gamma lambda).

The parameters lambda, T, and gamma are supplied with finite rational descriptions; square roots are evaluated with certified precision. A fixed initial sign is also allowed. The system and its reference initially have no correlation with this private source.

Given path error epsilon_W > 0 and failure allowance delta in (0,1/10), the independent-word version of the construction supplies one globally consistent finite-bit path W_tilde. It admits a coupling to the exact integrated telegraph path such that

    P[ sup_{0<=t<=T} |W(t)-W_tilde(t)| > epsilon_W ] <= delta.

Queries return fixed-point approximations at finitely encoded times. This is a uniform-value coupling, not total-variation approximation of a continuous path by finitely many outputs.

The source can be evaluated reversibly in time polynomial in the input bit length, log(2+lambda T), log(2+vT), log(2+1/epsilon_W), log(1/delta), and the time-query precision. A finite-query quantum consumer can replace the independent word table by a polynomial-size, limited-independence seed without changing its averaged visible output. The seed and all source work remain private. The claim is not an unlimited reusable random-path service.

All arithmetic, rejection caps, field construction, source calls, and uncomputation are charged. No arrival list of length proportional to lambda T is generated.

## 2. Exact continuous source representation

Put mu = lambda T and draw N from Poisson(mu). Conditional on N, the N+1 chronological spacings, divided by T, have distribution

    Dirichlet(1,...,1).

This follows from the constant joint density of the ordered N uniform event times. Relative to the initial sign, spacing indices 0,2,4,... have positive sign and indices 1,3,5,... have negative sign. Their counts are

    k_plus = ceil((N+1)/2),       k_minus = floor((N+1)/2).

The total positive mass V has distribution Beta(k_plus,k_minus). Conditional on V, the normalized positive spacing vector and normalized negative spacing vector are independent Dirichlet vectors with unit parameters; they are independent of V. These statements follow by representing all spacings as independent Gamma(1,1) variables divided by their sum, grouping the two colors, and changing variables to each group sum and normalized vector.

A Dirichlet vector with k unit parameters admits a balanced binary construction. A node containing k leaves assigns the fraction

    Beta(k_left,k_right)

to its left child, independently of all descendant splits. A zero count makes the split deterministic; no Beta distribution with zero shape is invoked. The same Gamma-sum change of variables proves this recursion.

For N=0 the only spacing has length T and no Beta draw is required. The final sign is exactly initial_sign times (-1)^N. The representation is exact before numerical discretization; no diffusion approximation is involved.

## 3. Poisson sampling without generating arrivals

Choose an outward rational or integer bound

    Nmax >= ceil(2 mu + 2 log(100/delta)) + 2.

Since E[2^N] = exp(mu), Markov's inequality gives P(N>Nmax) <= delta/100. Sampling Poisson(mu) conditioned on 0<=N<=Nmax changes its law in total variation by at most that amount.

### 3.1 A uniform rejection envelope for mu >= 1

Let m=floor(mu), d=ceil(sqrt(m)), a=m-d, and b=m+d. Here a>=0. Normalize the target weights by their mode:

    f(n) = mu^(n-m) m! / n!,       f(m)=1.

For n outside the retained nonnegative range set the target to zero. Use the proposal envelope

    g(n) = (a/mu)^(a-n),       n<a;
           1,                 a<=n<=b;
           (mu/(b+1))^(n-b),   n>b.

If a=0, the left tail has zero weight. Otherwise it may be extended to negative integers, which are rejected. The adjacent Poisson ratios prove f<=g: to the left the backwards ratio is at most a/mu, and to the right the forward ratio is at most mu/(b+1). The central region is bounded by the modal weight 1.

The envelope mass is

    Z = 2d+1 + r_left/(1-r_left) + r_right/(1-r_right)
      <= 8 sqrt(m).

For j=0,...,floor(sqrt(m)/2),

    f(m+j) >= product_{l=1}^j m/(m+l)
            >= exp[-j(j+1)/(2m)] >= exp(-1).

There are at least sqrt(m)/2 such terms. Consequently the target mass is at least sqrt(m)/(2e), and the acceptance probability exceeds 1/64. These terms lie below Nmax, so truncation does not remove this lower-bound interval. A conservative common bound of 1/128 is sufficient below.

The proposal is a mixture of a uniform central integer and two geometric tails. A geometric tail is sampled by inverse-CDF binary search with an overflow symbol beyond the retained range. Overflow and negative proposals are rejected. This takes logarithmically many comparisons, not a linear scan.

### 3.2 The case mu < 1

Use target f(n)=mu^n/n!, n>=0, and envelope g(n)=2 times 2^(-n). The envelope mass is 4, and f<=g because max_n 2^n/n! = 2. The untruncated acceptance probability is at least 1/4; the same retained range leaves a constant lower bound.

### 3.3 Capping

Every rejection sampler executes a fixed number R of proposals and selects its first accepted proposal. If none is accepted, it returns a designated default and a private failure flag. A lower acceptance bound 1/128 gives cap failure at most exp(-R/128). Taking R=O(log(Nmax/delta)) makes the union of all conceptual sampler-cap failures small. Fixed caps give a deterministic circuit and query budget.

## 4. Large-shape Gamma and Beta sampling

Generating Gamma(k,1) by summing k exponentials would invalidate the complexity claim. The following elementary log-concave envelope avoids that operation.

For integer k>=2, put m=k-1 and choose the exact dyadic number

    d = 2^( floor(floor(log2(m))/2) - 1 ).

Then sqrt(m)/4 < d <= sqrt(m)/2. Set a=m-d and b=m+d. Normalize the target density at its mode:

    f(x)=exp[m log(x/m)-x+m],       x>0.

Its logarithm is concave. Use

    g(x)=exp[(d/(m-d))(x-a)],       x<a;
         1,                       a<=x<=b;
         exp[-(d/(m+d))(x-b)],     x>b.

Negative proposals are rejected. Concavity and f(a),f(b)<=1 prove domination. All slopes and mixture weights are rational. The envelope area is

    Z = (m-d)/d + 2d + (m+d)/d
      = 2m/d+2d <= 9 sqrt(m).

For x=m(1+u) in the central interval, |u|<=1/(2sqrt(m))<=1/2. The elementary bound log(1+u)-u >= -u^2 gives log f(x)>=-1/4. Hence

    acceptance >= 2d exp(-1/4)/(9sqrt(m))
               >= exp(-1/4)/18 > 1/32.

The proposal mixture consists of a uniform central interval and two exponential tails. It requires logarithms of uniforms, not a number of operations proportional to k. Gamma(1,1) is simply -log(U).

Two independent Gamma(k,1), Gamma(l,1) outputs G,H give Beta(k,l)=G/(G+H). All shapes used by the spacing trees are positive integers at most Nmax+1. The deterministic zero-count cases are treated separately.

## 5. Certified arithmetic and an explicit conservative budget

This section makes the finite-bit claim quantitative in bit length. Large auxiliary numbers below determine precision and probability bounds; no algorithm loops that many times.

Let Dsam be a deterministic upper bound on the number of Gamma samplers in the entire conceptual tree, with Dsam<=8(Nmax+2). Increase it by a fixed constant for the count and sign source. Choose

    R >= ceil(128 log(100 Dsam/delta)).

Let H be a power of two at least

    256, Nmax+2, Dsam, R, 1/delta, 1/eta,

where eta is the desired error in every Beta split. Use

    tau = H^(-6),       X = 100 H^2,
    b = ceil(500 log2(H)) + O(input bit length).

Uniform random words are interpreted as b-bit midpoints. Elementary functions are computed by certified interval arithmetic with a comparable number of guard bits. Constants can be enlarged without changing any complexity claim.

### 5.1 Gamma cutoffs and proposal coupling

For integer k>=1, Gamma(k,1) stochastically dominates Exp(1), so

    P(G<tau) <= tau.

Also E exp(G/2)=2^k. Since k<=Nmax+1<=H, the cutoff X gives an upper-tail probability far smaller than H^(-6). Across at most H conceptual Gamma draws, their total accepted-tail loss is O(H^(-5)), much smaller than delta. Restricting acceptance to [tau,X] preserves a uniform constant acceptance probability, conservatively 1/128.

For coupling analysis, exclude uniforms outside [H^(-6),1-H^(-6)]. There are at most a constant times Dsam R, bounded conservatively by 16H^2, conceptual uniform draws. Their total excluded probability is at most 32H^(-4), again much smaller than delta.

On that compact uniform interval, each proposal inverse transform has derivative bounded by O(H^7). On [tau,X], the acceptance threshold f/g has derivative bounded by O(H^7): its logarithmic derivative is m/x-1 minus one of the envelope slopes, and 0<=f/g<=1. At the explicit cutoff boundaries, the proposal density is bounded by 1, so a boundary strip of width z has probability O(z). Mixture-boundary errors are similarly controlled by uniform interval lengths.

Thus b-bit midpoint coupling and certified elementary arithmetic make the proposal-location and acceptance-threshold errors much smaller than H^(-40). Acceptance comparisons use a fresh independent uniform, so threshold errors have probability at most their interval width. The finite union over at most 16H^2 decisions remains negligible relative to delta.

Coupled accepted Gamma values are within an error much smaller than eta tau. Their exact and approximate denominators in the Beta ratio are bounded below by a fixed multiple of tau. The quotient is therefore stable; rounding it to a dyadic number in [0,1] gives split error at most eta. Complementary child masses are formed as v and 1-v, never rounded independently.

### 5.2 Poisson comparisons

A b-bit central uniform integer differs from its exact counterpart only near one of O(Nmax) rounding boundaries. Geometric inverse-CDF comparisons can also be coupled by excluding neighborhoods of all O(Nmax) retained thresholds; this conservative union is adequate because it costs only O(log Nmax) precision bits. Overflow is a single rejected outcome, not a long loop.

The Poisson acceptance ratio is evaluated through

    log f(n) = (n-m) log(mu) + log(m!) - log(n!).

For the envelope, add or subtract the corresponding linear multiple of log(r_left) or log(r_right). Ratios are clamped to [0,1]. A sufficiently negative certified log ratio may be replaced by zero with its explicit absolute error. The small-mu case uses the same arithmetic; the input bit length pays for a very small positive mu.

### 5.3 No hidden factorial work

To approximate log(n!)=log Gamma(n+1), shift its argument upward to at least 16B with at most O(B) recurrence steps, then use O(B) Stirling/Bernoulli terms. For positive real arguments, the remainder is bounded by the first neglected term. The standard bound on Bernoulli numbers makes the remainder exponentially small in B at the shifted argument. Bernoulli rationals are generated by a finite rational recurrence with polynomial bit complexity.

Computing large log-factorial values and then subtracting them requires guard precision; this is paid with B+O(log Nmax) absolute working precision. The values themselves have only O(log Nmax+B) binary digits at that precision. No factorial product of length n is taken. Logarithms use range reduction and a geometrically convergent atanh series; exponentials are evaluated on a bounded relevant log range, with negligible tails cut off explicitly.

Consequently the arithmetic costs are polynomial in input length, log Nmax, log(1/delta), and log(1/eta). The displayed H is not a runtime bound: loops run for R, logarithmic search depth, or polynomially many precision steps, never for H or Nmax.

The independent continuous and finite-word samplers can therefore be coupled so that N agrees and all tree splits are within eta, except with total probability at most delta after allocating the constant error budgets. This coupling is uniform in the count N and hence remains valid after averaging over it.

## 6. Two valid lazy representations

### 6.1 Original separate-color trees: O(log^2 Nmax) nodes

Construct independent balanced trees for the positive and negative groups, together with the root occupation split V. Each prefix of one color is evaluated using O(log Nmax) nodes. The first j chronological spacings contain ceil(j/2) positive leaves and floor(j/2) negative leaves. Binary search on the sum of the two corresponding prefixes locates the queried interval with O(log^2 Nmax) node evaluations.

At that interval, add the elapsed part if it has positive sign. Then

    W_tilde(t) = initial_sign times v times (2 positive_elapsed - t).

This construction remains valid; its extra logarithm is not necessary.

### 6.2 Reviewer optimization: one chronological parity tree

The following improvement was proposed during independent review.

Use a balanced tree on chronological spacing indices 0,...,N. Each node stores two masses: its positive and negative total occupation, and the known number of leaves of each parity. The root masses are V and 1-V.

When a chronological node is split into consecutive left and right index ranges, divide its positive mass according to

    Beta(number of positive leaves on left,
         number of positive leaves on right),

and independently divide its negative mass using the analogous negative counts. If one count is zero, that mass is assigned deterministically. These splits have the exact conditional law by the same Dirichlet neutrality argument as before. Positive and negative splits use distinct random addresses.

For a query, first normalize its time to u=t/T. Compare the remaining normalized time with the left child's TOTAL mass. If the query lies on the right, subtract that total mass and add the left child's SIGNED mass to the accumulated normalized signed integral. Otherwise descend left. At the leaf, add its known sign times the remaining normalized elapsed time. Multiply the result by T, the initial sign, and v to obtain W_tilde(t).

There are at most two nontrivial Beta draws per visited node and one descent of depth O(log Nmax). Therefore the optimized query evaluates O(log Nmax) nodes. It does not generate the siblings' entire subtrees.

This is an optimization of the source representation, not a claim of generic novelty for lazy trees. The earlier separate-color implementation and its bound are retained as a correct alternative.

## 7. Uniform path error without minimum spacings

Every rounded split lies in [0,1], and complementary child fractions sum exactly to one. Thus either tree produces one genuine, globally consistent nonnegative spacing vector.

If every split differs from its exact counterpart by at most eta, a depth-D probability tree has leaf-mass l1 error at most 2D eta. This follows inductively: at a split, the additional l1 error is at most twice the parent mass times eta; parent masses sum to one at a depth. Include the occupation root as one more level. The chronological parity tree has the same bound by applying this argument to each color's normalized tree and then their root masses. Therefore

    d := sum_j |s_j - s_tilde_j| <= 2(D+1) eta.

Here spacings are normalized to total one. Corresponding chronological endpoints differ in time by at most T d, and their signed cumulative integrals differ by at most T d.

Map each exact spacing interval linearly onto its rounded counterpart. This gives a continuous nondecreasing surjection, possibly collapsing intervals of rounded length zero. At corresponding interpolated points the time and signed-integral discrepancies remain at most T d. For an arbitrary rounded time t, choose any preimage u. Since the exact integrated sign is 1-Lipschitz,

    |S_tilde(t)-S(t)|
      <= |S_tilde(t)-S(u)| + |S(u)-S(t)|
      <= 2 T d.

Consequently

    sup_t |W_tilde(t)-W(t)|
      <= 4 v T (D+1) eta.

Take eta smaller than epsilon_W divided by this coefficient, with fixed slack for approximating v and rounding the returned value. Products of dyadic split fractions and all prefix sums are computed exactly with O(Db) bits. Time comparisons are exact on these rational quantities. At a repeated rounded endpoint choose a consistent endpoint convention; zero intervals contribute zero duration and signed integral.

This proof needs no anti-concentration of queried times, no minimum spacing, and no accumulation proportional to the number of switches. It also covers query times precisely at a true or rounded switch.

## 8. Coherent implementation and finite independent seeds

### 8.1 Finite random-table circuit

Assign an address to each tree node, color, Gamma factor, rejection proposal, and uniform role. Root occupation draws have their own addresses. The address space has size O(Nmax R), but is never generated or stored. Shapes and left/right counts are computed from N and the node's interval endpoints.

The capped samplers are deterministic functions of finite random words. Standard reversible computation implements them with polynomial gate and workspace cost. Compute every capped proposal, select the first accepted one, and uncompute private intermediate arithmetic as needed. Defaults on failure still define valid splits in [0,1], so even a failed source instance defines a valid rounded path.

Sample N and the initial sign using independent private randomness, charging their capped time, random bits, and approximation error. Conditional on N, use a separate random table for the tree. This simplifies the independence proof. Alternatively, count their table calls in the same global budget.

For L coherent path queries, the optimized tree requires a deterministic abstract table-query budget

    Q = poly(L, R, log Nmax),

including all required source computation and uncomputation. The original separate-color version uses one additional logarithmic factor. Arithmetic bit costs are additional polynomial factors, not oracle calls.

### 8.2 Exact bounded-query replacement

Choose a binary field F_(2^w), with w at least the random-word length, the address length, and log2(2Q). Inject all addresses into the field. A uniformly random polynomial of degree at most 2Q-1, evaluated at an address and projected to the required output bits, is a 2Q-wise independent word table.

The seed uses 2Qw bits. Horner evaluation takes O(Q) field operations per abstract table query; elementary field arithmetic is polynomial in w. A conservative total additional gate bound is O(Q^2 poly(w)). This is an information-theoretic construction, not an uncharged cryptographic PRNG.

The field representation itself is constructible with capped randomized polynomial preprocessing. A uniformly random monic binary polynomial of degree w is irreducible with probability at least 1/(2w), apart from finitely many small degrees handled directly. Test irreducibility exactly using Frobenius powers and polynomial gcds. O(w log(1/delta)) candidates make setup failure at most delta. The classical setup cost and failure are charged; only a verified field polynomial is used.

For a Q-query quantum circuit, amplitudes have degree at most Q in table-entry indicators. Output density-matrix entries have degree at most 2Q. Every such monomial involves at most 2Q distinct addresses, so its expectation is exactly the same for the independent table and the polynomial family. This proves equality of the averaged visible output states, including arbitrary retained references and controller records. Adaptive or coherent addresses and deferred measurements are included.

The proof has a crucial order:

1. Prove the full-tree coupling and uniform path error for the independent finite table.
2. Apply the consuming circuit to that table.
3. Replace its table by 2Q-wise independence, using exact equality of the consuming circuit's averaged output.

There is no claim that the entire polynomial-seed path has the exact law, or that the all-node good event remains probable under limited independence. The seed and private work are traced out and inaccessible to the controller. Unlimited subsequent source queries are outside the theorem.

## 9. Receiving boundary and ordinary alternatives

For the physical Hamiltonian H(t)=H0+v xi(t) A, the exact noise interaction frame is

    R(t)=exp[-i A W(t)],
    H_I(t)=R(t)^dagger H0 R(t).

Its Hamiltonian norm is ||H0||, independent of lambda. This source oracle is intended to feed a high-precision time-dependent Hamiltonian simulator in that frame, with controller operations handled using the same private path.

This note does not by itself prove the full simulator's complexity or diamond error. The receiving proof must pay for conjugations, time discretization, all source queries, Hamiltonian encodings, retained-controller operations, and source/private-work tracing. No bath redraw at control boundaries is allowed. No generic noncommuting-multimode or quantum-bath extension is asserted.

Uniformly fast log-concave and Poisson rejection, lazy stochastic paths, reversible arithmetic, and bounded-query independence are established machinery. The proposed scientific capability is their complete, precision-accounted join for the integrated telegraph source and its quantum consumer. Neither priority nor practical advantage follows from this construction.

## 10. Sources and provenance

- NIST Digital Library of Mathematical Functions, Section 5.11(ii): positive-real Stirling remainders are bounded by the first neglected term. https://dlmf.nist.gov/5.11
- Luc Devroye, Non-Uniform Random Variate Generation, primary author-hosted book: log-concave rejection is established machinery. https://luc.devroye.org/rnbookindex.html
- Wolfgang Hormann, The transformed rejection method for generating Poisson random variables (1993), primary institutional record. https://ie.bogazici.edu.tr/content/transformed-rejection-method-generating-poisson-random-variables
- Andraz Jelincic, James Foster, Patrick Kidger, Single-seed generation of Brownian paths and integrals for adaptive and high order SDE solvers: a strong ordinary lazy-path comparator, not a telegraph finite-bit quantum-oracle theorem assumed here. https://arxiv.org/abs/2405.06464
- Mark Zhandry, How to Construct Quantum Random Functions: the bounded-query independence principle is established; the indicator-polynomial proof used here is supplied in Section 8. https://collaborate.princeton.edu/en/publications/how-to-construct-quantum-random-functions/
- Astra N710, finite-seed classical correlated-noise simulation, read at revision 93f9f92a6dcdf33d3f13b5ea11c0447c2b5f67a6. Its fixed-amplitude versus fixed-diffusion-strength distinction motivated this task. Its compiler remains source-reported and unreviewed, and is not a proof premise of the source construction above. https://github.com/harjassand/astra-research-knowledge/blob/93f9f92a6dcdf33d3f13b5ea11c0447c2b5f67a6/updates/EB/package/cray_correlated_noise/ORIGINAL_PASTED_SOURCE.txt

No source sampler, quantum circuit, or numerical verification was executed for this note. Independent review and the whole receiving theorem remain necessary.
