# Independent audit: pendant-pair conditional Gaussian reduction

Frozen audit date: 2026-10-10. Auditor: `physical_reduction_critic`.

**Conclusion.** The reduction is correct, subject to an explicit, adjustable-accuracy conditional-sampling assumption. Its strongest version uses independently weighted pendant edges and adaptive calibration. A polynomial-time classical sampler for the specified conditional two-mode photon distributions, with arbitrary total-variation error eta and cost polynomial in input size and 1/eta, implies an FPRAS for counting perfect matchings in arbitrary simple graphs. The converse also holds for this explicit graph-encoded family, as checked in Section 8. This is a polynomial equivalence, not an implementation of either side and not a counting breakthrough. The literal physical preparation has exponentially small heralding probability. No flaw was found in the algebra, physicality, or polynomial accuracy reduction. No novelty conclusion is established.

## 1. Exact state and support

Let G be a simple graph on an even number m >= 2 of vertices and suppose Z(G) > 0, where Z denotes the number of perfect matchings. Choose an edge uv. Add a leaf a adjacent to u and a leaf b adjacent to v. In a real symmetric Gaussian pair matrix B, give every original graph edge weight t > 0 and both pendant edges weight lambda > 0, with all other entries zero. Require ||B||_2 < 1.

The normalized pure, undisplaced Gaussian state has Fock probabilities

    P(s) = sqrt(det(I - B B^T)) |haf(B_s)|^2 / product_i(s_i!).

Herald event H: every original mode is measured by exact photon-number resolution to contain exactly one photon. Each leaf photon must pair with its sole neighbor. Since that neighbor has only one photon, leaf occupation is at most one. Since m is even and the state has even total parity, the only supported leaf outcomes are 00 and 11.

Their unnormalized amplitudes are

    amp00 = t^(m/2) Z(G),
    amp11 = lambda^2 t^((m-2)/2) Z(G-u-v).

No factorial is missing: all supported occupations are zero or one. Thus, with p_uv = Z(G-u-v)/Z(G),

    r = (lambda^2/t) p_uv,
    q = P(11 | H) = r^2/(1+r^2),
    p_uv = (t/lambda^2) sqrt(q/(1-q)).

Here p_uv is exactly the uniform-perfect-matching probability that uv is occupied. For each vertex u, sum_{v adjacent to u} p_uv = 1, so some incident edge has p_uv >= 1/(m-1). The condition uv in E(G) is essential to this interpretation and to p_uv <= 1.

The exact physical herald probability is

    h = sqrt(det(I-BB^T)) t^m Z(G)^2 (1+r^2).

These formulas remain mathematically meaningful when Z(G-u-v)=0, in which case q=0. The ratio formula requires Z(G)>0. A polynomial-time perfect-matching existence test supplies the initial zero case.

## 2. Weighted, calibrated construction

Set t = 1/(4m), initially lambda = 1/4. Every row sum of B is at most (m-1)/(4m)+1/4 < 1/2, so ||B||_2 < 1/2. Halving lambda preserves this. Also

    ||B||_F^2 <= m(m-1)/(16m^2) + 4/16 < 5/16,
    E[total photons] = tr[BB^T(I-BB^T)^(-1)] < 5/12.

Thus the states are physical, have constant spectral margin, bounded mean photon number, no displacement, rational pair matrices, and only two unheralded modes. Low unconditioned energy does not make the heralded distribution easy to acquire.

At the initial lambda, r = mp_uv/4. A heavy incident edge therefore has q >= 1/17. Estimate q for every edge at one chosen vertex, each with total additive error at most 1/128, and choose the largest estimate. Its true q obeys

    q >= 1/17 - 2/128 = 47/1088 > 1/32.

For this chosen edge, estimate q with the same accuracy and halve lambda while the estimate exceeds 1/2. Halving lambda divides r^2, the odds q/(1-q), by 16. At the first stopping value:

- The stopping estimate implies q <= 65/128.
- If no halving occurred, edge selection gives q > 1/32.
- If a halving occurred, the preceding q was > 63/128; hence the current q is > 63/1103 > 1/32.

Consequently the selected, calibrated instance satisfies

    1/32 < q <= 65/128.

There are at most ceil(log_2 m) halvings: initially r^2 <= m^2/16, and after that many halvings it is <= 1/(16m^2), which forces a stopping estimate. All weights still require only O(log m) bits. An implementation should impose this deterministic cap and fail safely if a bad sampling event prevents a stop.

## 3. Fully polynomial accuracy and failure budget

Let n be the original graph order, 0 < epsilon <= 1, and 0 < delta < 1. The assumed classical conditional sampler takes the exact rational description B, the specified H, and a requested eta > 0; its sample law has TV distance at most eta from the exact conditional distribution, and its running time is polynomial in input length and 1/eta. Fresh independent invocations are used.

There are fewer than T = 3n^2 probability-estimation calls, including all edge searches, calibration tests, and refinements. This bound is deliberately loose. Conditional on any prior history, the usual concentration guarantee applies to the next fixed instance, so a union bound remains valid for adaptive selection.

For every coarse search/calibration estimate use eta_0 = 1/256, and

    M_0 = ceil(32768 log(2T/delta))

samples. Let the estimated q be the frequency of exactly outcome 11, counting every other output as zero. TV controls its bias by eta_0. Hoeffding bounds sampling error by 1/256 except with probability delta/T. Therefore total additive error is at most 1/128 as required above. Invalid-output mass in an approximate sampler causes no additional problem: the event estimate is still covered by TV.

For the final estimate on each calibrated instance use

    eta_1 = epsilon/(512n),
    M_1 = ceil(131072 n^2 epsilon^(-2) log(2T/delta)).

Except with probability delta/T, the total additive q error is at most epsilon/(256n). True and estimated q, and the segment joining them, lie inside [1/64,3/4]. On this interval,

    |d log p / dq| = 1/[2q(1-q)] <= 2048/63 < 64.

Hence

    |log(phat/p)| <= epsilon/(4n).

Delete the endpoints of the selected edge and continue. The exact identity

    Z(G) = Z(G-u-v)/p_uv

telescopes to Z(G) = product_i p_i^(-1), with Z(empty)=1. There are at most n/2 steps, so the estimate obeys

    |log(Zhat/Z)| <= epsilon/8.

For 0 < epsilon <= 1, this is strictly stronger than the FPRAS requirement (1-epsilon)Z <= Zhat <= (1+epsilon)Z. All estimation calls simultaneously satisfy their guarantees with probability at least 1-delta.

**Zero-event guard.** Test whether the current residual graph has a perfect matching before making conditional-oracle requests. On the good event, selected q>1/32 already ensures that the next residual graph has one. On a bad sampling event, this explicit guard prevents an undefined request conditioned on a zero-probability event; return an arbitrary failure value instead. Initial Z=0 is detected exactly. Likewise guard qhat=0 or qhat>=1 in refinement and terminate safely on these failure cases.

**Arithmetic.** Accumulate the exact rational estimate of Z^2,

    R = product_i [(lambda_i^2/t_i)^2 (1-qhat_i)/qhat_i],

then approximate sqrt(R) with polynomially many bit operations. Empirical frequencies are rational, selected parameters have O(log n) bits, there are O(n) factors, and log Z = O(n log n). Reserve, for example, another epsilon/8 in relative error for square-root rounding. Computing an exact real square root is unnecessary. Matrix B is the exact rational input representation; an interface requiring optical gates or a different covariance convention needs an explicit polynomial-bit conversion, rather than an assertion that ideal hardware realizes exact rational amplitudes.

Total conditional samples are

    O(n^2 log(n/delta) + n^3 epsilon^(-2) log(n/delta)).

There are polynomially many matching-existence checks, state-description operations, and rational arithmetic operations. The coarsest requested TV accuracy is constant; the finest is Theta(epsilon/n). Thus total runtime is polynomial provided the assumed conditional sampler has the stated uniform running-time guarantee. A fixed, nonadjustable TV accuracy alone does not yield an arbitrary-epsilon FPRAS.

## 4. Equal-weight special case originally proposed

Set t=lambda=c=1/[2(m+1)]. Then

    q = c^2 p_uv^2/(1+c^2 p_uv^2).

The state satisfies ||B||_2<1/2, ||B||_F^2<1/4, and mean total photon number <1/3. A heavy edge has q >= a, for the uniform lower bound a = 1/[8(n+1)^4]. Therefore inverse-polynomial-accuracy conditional sampling still suffices, without weighted calibration.

A valid two-stage budget is:

- Selection: eta=a/16 and M=ceil((256/a) log(8n^2/delta)) samples per incident edge. Use threshold 3a/4: a heavy true q>=a has sampled-law mean >=15a/16, while every low true q<=a/2 has mean <=9a/16. Multiplicative Chernoff tails separate these cases. Choosing the largest frequency obtains true q>a/2 with high probability. Do not justify this step using a uniform additive-a bound for all edges, since large-q variance would need more samples; threshold separation is the relevant proof.
- Refinement: rho=epsilon/(4n), eta=a*rho/64, and M=ceil((1024/(a*rho^2)) log(8n/delta)). Since q>a/2, sampler bias is <=rho*q/32. Multiplicative Chernoff yields |qhat/q-1|<=rho with ample slack. Here q<=1/37, so |log(phat/p)|<rho. Telescoping again gives log-count error <=epsilon/8.

This gives O(n^6 log(n/delta) + n^7 epsilon^(-2) log(n/delta)) conditional samples. It confirms the original reduction; the weighted variant improves only its oracle reduction overhead.

## 5. Physical acquisition cost is not removed

For the weighted construction, Z(G) <= (m-1)!! <= m^(m/2), the determinant prefactor is at most one, and r^2 <= m^2/16. Therefore

    h <= (1+m^2/16) 4^(-m).

After calibration the sharper bound is

    h <= (128/63) 4^(-m).

Consequently rejection sampling requires exponentially many independent preparations per accepted herald, already on the first m=n stage. The equal-weight construction similarly has

    h <= (1+c^2) 2^(-m).

An unconditional approximate sampler also does not automatically furnish the required oracle: conditioning on an event of probability h can amplify TV error by a factor of order 1/h. The reduction is a hardness/implication result for direct conditional sampling, not a claim that physical postselection is free.

An independent concrete obstruction is G=k disjoint edges, with both attachment vertices on one edge. Under equal-weight encoding, the augmented graph is P4 disjoint union (k-1)K2. Every untouched two-mode squeezed component contributes P(1,1)=c^2(1-c^2)<=1/4, so h<=4^(-(k-1)) for every allowed c. Factorization can of course solve this easy graph class classically; the example diagnoses literal physical acquisition, not the computational hardness of that class.

## 6. Prior art and status

- Hamilton et al., *Gaussian Boson Sampling* (2017), https://arxiv.org/abs/1612.01199: the hafnian Fock-probability framework.
- Bradler et al., *Gaussian Boson Sampling for Perfect Matchings of Arbitrary Graphs* (2018), https://arxiv.org/abs/1712.06729, especially Sections II.C-D: graph encoding, squared-hafnian counts, spectral rescaling, and exponentially small all-ones probabilities.
- Stefankovic, Vigoda, and Wilmes, *On Counting Perfect Matchings in General Graphs* (2017/2018), https://arxiv.org/abs/1712.07504: a primary source documenting the general-graph FPRAS barrier and failure of a natural JSV extension. This source alone does not establish the latest 2026 status.
- Anand et al., *Simulating Gaussian Boson Sampling on Graphs in Polynomial Time*, current manuscript accessed 2026-10-10, https://homepages.inf.ed.ac.uk/hguo/papers/BS-simulation.pdf, Theorem 1.1: polynomial approximate sampling of variable vertex subsets with squared-perfect-matching weights through a doubled-graph construction. Its stated variable-subset sampler is not an oracle for arbitrary rare-event heralding. No contradiction follows.

Targeted primary-source search by an independent literature subagent did not identify the exact two-pendant-leaf theorem. That limited search is not evidence of novelty. The individual algebraic ingredients are standard. Agreement between model agents and the finite checks below are internal evidence only, not external proof certification.

## 7. Reproducible diagnostic

Run `python3 work/foundational_bridge/reduction_audit_check.py` from the workspace. It exhaustively checks all simple graphs through four vertices and 60 seeded graphs each at six and eight vertices, whenever a perfect matching exists. Repeated-mode hafnian recursion verifies leaf support for occupations 0 through 3, the two surviving amplitudes, marginal normalization, and weighted odds. Output is saved in `reduction_finite_check.txt`. These finite checks do not replace the argument above and do not test a conditional-sampling implementation.

**Single remaining obstacle exposed by this audit:** construct the stipulated uniformly efficient direct conditional sampler, or a comparably strong acquisition mechanism, without performing exponentially costly herald rejection or hiding perfect-matching counting inside its implementation.

## 8. Checked converse: a perfect-matching FPRAS supplies this family of samplers

This converse concerns exactly the family above, described by G, the chosen edge uv, and the rational weights t and lambda. In the weighted construction t=1/(4m) and lambda=2^(-j)/4 with 0<=j<=ceil(log_2 m)+2; input lengths are polynomial. It does not assert a sampler for arbitrary conditioned Gaussian states.

Assume an FPRAS for perfect-matching counts on general graphs. Given a requested 0<eta<1, first use a polynomial-time matching algorithm to test Z=Z(G) and Zm=Z(G-u-v) for zero. The conditional-sampling promise requires Z>0. If Zm=0, output 00 exactly. If Z=0, then Zm=0 as well because uv is an edge, and the herald has probability zero: report that the request lies outside the promise rather than sampling a nonexistent conditional distribution.

For positive counts, independently obtain rational estimates Zhat, Zmhat, each with relative error alpha=eta/64 and failure probability at most eta/16. Standard repetition and median amplification supplies the requested failure probability with logarithmic overhead if the FPRAS originally has fixed success probability. Let

    R = lambda^2/t,
    phat = Zmhat/Zhat,
    qhat = R^2 Zmhat^2 / (Zhat^2 + R^2 Zmhat^2).

Guard nonpositive or malformed count estimates, and any zero denominator, by setting qhat=0. On the good event these guards never apply. Since alpha<=1/2,

    |log(phat/p)| <= log((1+alpha)/(1-alpha)) <= 4alpha.

For q(p)=R^2 p^2/(1+R^2 p^2),

    dq/d(log p) = 2q(1-q) <= 1/2.

The mean-value theorem therefore gives |qhat-q|<=2alpha=eta/32, uniformly in p and R. By a union bound the bad-estimate event has probability at most eta/8. If a Bernoulli(qhat) draw were exact, averaging over the randomized count estimates would produce TV error at most eta/32+eta/8=5eta/32.

**Strict runtime detail.** Exact rational Bernoulli sampling from unbiased bits is easy in expected polynomial time but generally has an unbounded rejection tail. For a worst-case polynomial bound, take b=ceil(log_2(4/eta)) and qtilde=floor(2^b qhat)/2^b. Draw a uniform b-bit integer and output 11 exactly when it is below 2^b qtilde; otherwise output 00. This adds less than eta/4 TV, for total error less than 13eta/32<eta. All arithmetic uses polynomially many bits, and the count-FPRAS precision cost is polynomial in 1/eta.

Thus, under the standard uniform accuracy conventions, the existence of an FPRAS for general-graph perfect-matching counts is equivalent to the existence of a fully polynomial approximate sampler for this specific two-output, pendant-pair heralded Gaussian family. Both directions are constructive reductions. The equivalence identifies a complexity boundary; it does not remove the counting or physical-acquisition obstacle.
