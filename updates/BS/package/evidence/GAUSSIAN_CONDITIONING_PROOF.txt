# Bounded-energy Gaussian heralding retains the general matching barrier

Date: 2026-10-10, Australia/Brisbane. Source-derived programme continuation; new internally proved reduction with independent model audit and exact finite checks. **Historic objective not achieved. Historical novelty and external proof certification are UNKNOWN.**

## The precise result

The following two algorithmic capabilities are polynomially equivalent:

1. An FPRAS for the number of perfect matchings of arbitrary unweighted simple graphs, including exact detection of zero.
2. An adjustable-accuracy classical sampler for a particular family of pure, undisplaced, entrywise-nonnegative Gaussian pair kernels, conditioned on exactly one photon in every graph mode, leaving just **two** unheralded modes. The sampler must run in time polynomial in its exact rational input length and inverse requested total-variation error, uniformly over every nonzero herald.

Every kernel in this restricted family has operator norm below 1/2 and total unconditioned mean photon number below 5/12. After calibration, each of the two possible conditional outcomes has probability bounded below by a universal constant. Thus neither large energy, proximity to instability, a large output space, nor a rare *remaining output* accounts for the matching barrier. It resides in exact conditioning on an exponentially rare event.

This is a barrier-equivalence theorem. It is not an impossibility result for general matching, a new matching FPRAS, or a demonstrated useful conditional sampler. In particular, the pinned OpenAI source claims a general matching FPRAS; that source's global correctness remains unaudited here and its prescribed constants are impractical.

## Construction and proof

Let G have even order m and Z(G)>0 perfect matchings. Select an edge uv. Add leaves a,b, attached only to u,v respectively. Put weight t=1/(4m) on each original edge and lambda=2^(-j)/4 on both pendant edges. The symmetric matrix B of those weights defines the physical pure Gaussian state proportional to exp(a-dagger B a-dagger/2)|0>. Initially j=0; only O(log m) successive halvings are needed.

Herald H requires one photon at each original vertex. Each leaf has at most one photon because its sole neighbour has one. Even parity therefore leaves exactly outcomes 00 and 11. Their amplitudes, before common normalization, are

    A00 = t^(m/2) Z(G),
    A11 = lambda^2 t^((m-2)/2) Z(G-u-v).

Consequently, with p_uv=Z(G-u-v)/Z(G) and R=lambda^2/t,

    q_uv = P(11 | H) = R^2 p_uv^2 / (1 + R^2 p_uv^2).

The p_uv are the uniform-perfect-matching edge marginals at u, summing to one. At j=0, R=m/4; hence some incident edge has q>=1/17. Estimating every incident q to additive 1/128 and choosing the largest gives true q>1/32. Halve lambda while the estimated q exceeds 1/2. One halving divides the odds by 16. At the first stop,

    1/32 < q <= 65/128.

The complete constants and adaptive union bound are proved in `REDUCTION_AUDIT.md`. For original order n, coarse estimates use sampler TV tolerance 1/256 and O(log(n/delta)) samples. Refine each selected calibrated probability with tolerance epsilon/(512n) and O(n^2 epsilon^-2 log(n/delta)) samples. Since

    d log(p_uv)/dq = 1/[2q(1-q)],

the refined marginal has log error at most epsilon/(4n). Remove u,v and repeat. The identity Z(G)=Z(G-u-v)/p_uv telescopes; at most n/2 steps give total log-count error at most epsilon/8 with probability at least 1-delta. Initial and residual matching-existence tests guard every nonzero-conditioning premise, including on failed statistical runs.

For the converse, use a matching FPRAS on G and G-u-v with relative error alpha=eta/64 and failure probability eta/16 each; exact matching existence handles zero. Let their rational estimates be Zhat,Zminorhat and set

    qhat = R^2 Zminorhat^2 / (Zhat^2 + R^2 Zminorhat^2).

On the good event the log-ratio error is at most 4alpha. Because dq/dlog(p)=2q(1-q)<=1/2, the Bernoulli probability error is at most 2alpha. The two failure events add at most eta/8. Round qhat down to b=ceil(log2(4/eta)) dyadic bits and use exactly b unbiased bits; the extra error is below eta/4. Total TV is below 13eta/32, with bounded polynomial runtime rather than an uncharged random-bit rejection tail. Malformed counter outputs on failure events produce a safe default. This converse depends on no general Gaussian-sampling or Schur-complement theorem.

## Physical and computational costs

Every row sum is at most (m-1)/(4m)+1/4<1/2. Also ||B||_F^2<5/16, so

    E[Nphotons] = tr[B^2(I-B^2)^(-1)] < 5/12.

The two conditional output probabilities can nevertheless require an exponentially rare experiment. The exact herald probability is

    P(H) = sqrt(det(I-B^2)) t^m Z(G)^2 (1+R^2p_uv^2).

Using Z(G)<=(m-1)!!<=m^(m/2) gives P(H)<=(1+m^2/16)4^-m, and after calibration the sharper P(H)<=(128/63)4^-m. Literal rejection thus costs at least (63/128)4^m preparations per accepted calibrated herald. An unconditional approximate simulator also needs its approximation error controlled relative to this mass before conditioning; its ordinary additive-TV guarantee does not supply the oracle.

The abstract reduction uses O(n^2 log(n/delta)+n^3 epsilon^-2 log(n/delta)) conditional samples. State descriptions take O(n^2 log n) bits; only rational matrix construction, ordinary polynomial matching-existence tests, polynomial-bit arithmetic, and one rounded square root occur outside the sampler. Its finest TV request is Theta(epsilon/n). Total runtime multiplies sample count by the cost of that conditional sampler. That cost is the unresolved capability, not a free primitive.

`oracle_reduction.py` implements the reduction with explicit sampler and existence callbacks, exact integer error schedules, guarded conditional calls, and a sample-budget stop. It does **not** implement the missing sampler. Its deliberately loose certified constants already request about 7.3e8 samples for n=2, epsilon=.1, delta=.01; these are proof constants, not a practical proposal. The exact-frequency control tests only emulate batch means and never claim to have generated these samples.

The equally weighted subclass B=cA, c=1/[2(m+1)], also gives the implication with norm<1/2 and mean energy<1/3, at greater polynomial accuracy cost. See the independent audit. It shows that two adjustable classes of edge weights are useful for reducing the overhead but unnecessary for the barrier itself.

## Pinned research capital and comparators

- Astra revision `8aed7fd74eb14622ed5a0a3635a799374296e32a`. Retrieval followed `00_START_HERE.txt` -> `agent/topics/quantum.tsv` -> current review cards N417/N419 and lemma routes LA146/LA149/LA152. Original note `web/pages/d-7dfec258730b6dfb.html` was decoded; exact SHA256 `31082ce32e8cdb9cb6069c871ed7913f40f3c17710126cc81c9cda76e9024ecd`. Its supplied conditional sampler has exponential exact matching DP; polynomial-herald extension imports general matching FPRAS. Current status remains source-derived/unreviewed.
- OpenAI Math revision `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, family 113, original `preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/build/main.tex`. `MATCHING_AUDIT.md` reconstructs targeted energy, quadrangulation and capacity arguments without finding a local flaw. No full proof or Lean dependency build was completed. Its prescribed replica count already exceeds 10^1892 per tier at the source's n=2,K=0 profile. This is a practical obstruction for that construction, not a refutation of its asymptotic guarantee.
- Hamilton et al., [Gaussian Boson Sampling](https://arxiv.org/abs/1612.01199), supplies the standard hafnian photon-probability framework. Brádler et al., [Gaussian boson sampling for perfect matchings of arbitrary graphs](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.98.032310), already connects graph matching counts with Gaussian amplitudes and analyzes graph encodings. Neither broad connection is new here.
- Anand et al., [Simulating Gaussian boson sampling on graphs in polynomial time](https://arxiv.org/abs/2511.16558), [current author manuscript](https://homepages.inf.ed.ac.uk/hguo/papers/BS-simulation.pdf), Theorem 1.1, already gives a polynomial sampler for a variable-subset squared-matching law on all graphs through the doubled graph G-square-K2. It does not provide arbitrary rare unit-herald conditioning. This stronger comparator supersedes treating dense-graph-only GBS methods as the relevant frontier.

The exact two-leaf bounded-energy equivalence was not found by the targeted primary-source search. That limited search does not establish novelty or priority. Classical self-reducibility and Gaussian hafnian identities supply the main ingredients.

## Evidence and scope

`verify_reduction.py` passes 194 graph instances, including exhaustive graphs of orders two and four, with 575 selected edge pairs and 5,175 direct repeated-mode Fock-pattern checks. It verifies physical norm/energy bounds, both amplitudes, support, balanced calibration, and exact telescoping on 157 positive instances. The independently written `reduction_audit_check.py` passes 138 graph instances, 20,784 repeated-hafnian support identities and 5,999 weighted-odds checks. `ORACLE_CONTROL_CHECKS.json` records exact-frequency test-double results, not sampled performance. Matching-source finite checks and their much narrower scope are recorded separately in `MATCHING_AUDIT.md`.

No physical experiment, useful-size conditional-sampling implementation, new efficient general matching algorithm, independent human/external certification, or historical breakthrough has been achieved.

## Cross-branch handoff and next gate

Primitive Genesis: the mathematically exact interface is efficient *conditioning* on a simple product count event, not efficient unconditioned evolution or low-energy state description. Theoretical Pro: an efficient general matching mechanism and this restricted conditional Gaussian capability stand or fall together algorithmically; the equivalence can be reviewed independently of the imported FPRAS. Natural-Sciences Pro: small unconditioned mean energy does not measure acquisition cost after an extensive herald; any physical protocol must charge event probability and stability under calibration error.

**The single consequential obstacle is a proved, executable direct conditioning mechanism whose total cost avoids both exponentially rare herald rejection and impractical general-matching overhead.** The current result identifies this obstacle precisely; it does not remove it.
