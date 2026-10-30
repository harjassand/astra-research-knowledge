# Exact signed level reduction with almost-contractive good maps
30 October 2026. Root receiving lemma, not an application of Gács probability estimates to quantum noise. The physical decomposition premises below remain substantive.

## 1. A real chronological block decomposition
Let a parent gadget contain m actual chronological channels T_1,...,T_m on a system with an arbitrary retained memory/bath/reference. Each T_i is CPTP, so its diamond norm is1. Assume EXACT linear decompositions T_i=G_i+B_i with ||B_i||_diamond<=epsilon and therefore ||G_i||<=1+epsilon. B_i need not be positive; G_i need not be trace preserving. Do not obtain these maps by assigning classical fault records to signed perturbations.

Define the parent's bad map as the sum of the EXACT expanded words with at least r marked B factors, in their original order. This is a channel-space definition; no event-probability domination is used. Triangle inequality/submultiplicativity gives

 ||B_parent|| <= sum_(k=r)^m binom(m,k) epsilon^k (1+epsilon)^(m-k)
              <= binom(m,r) epsilon^r (1+2epsilon)^(m-r).

For the second inequality use binom(m,k)<=binom(m,r)binom(m-r,k-r). It is an upper bound that overcounts words; no inclusion-exclusion coefficient is dropped. In particular for r=2,

 epsilon_parent <= m² epsilon² exp(2m epsilon).            (1)

One can instead use known malignant r-tuples if the exact word classification/cover is proved. An unproved classical witness union cannot be substituted for this definition.

If every word with fewer than r bad children has the SAME required logical/output identity, the parent good sum has that identity by linearity, including retained syndrome/bath coefficients. The small bad norm then supplies the usual trace-preservation factor2 logical error bound. Correctness must cover the entire child interface, not merely each reduced DATA marginal.

## 2. Growing block sizes do not automatically destroy the threshold
Suppose level k has m_k<=exp(a+b k^p), for fixed a,b,p, and r=2. There exists epsilon_0>0 and c>0 for which repeated (1) gives epsilon_k<=exp(-c 2^k).

Proof without an asymptotic gap: choose c so

 exp(a+b k^p-c 2^(k-1))<=1/2 for every integer k>=1.

This is possible because the finite supremum of (a+b k^p+log2)/2^(k-1) exists. Let

 S=sum_(j>=1) 2^(-j)[2a+2b j^p+1]<infinity,

and choose -log epsilon_0>=c+S. Inductively, if epsilon_(k-1)<=exp(-c 2^(k-1)), then m_k epsilon_(k-1)<=1/2 and

 -log epsilon_k >= 2[-log epsilon_(k-1)] -2a-2b k^p-1.

Divide by2^k and telescope. The partial sum is at most S, so the resulting lower bound is at least c2^k, closing the induction. All base-level resource constants are paid in epsilon_0; no numerical useful threshold is asserted.

Thus the extra good-map norm factor1+epsilon is not itself an obstruction for hierarchy block sizes exp(poly(k)). This is ordinary analytic fault-path/level-reduction reasoning, not a new probability theorem.

## 3. What this does NOT prove for asynchronous reliable classical media
The actual source needs a physical decomposition into these chronological children, or an equally strong mixed-cavity multilinear factorization with the same norm bound. Spatially overlapping colonies sharing service intervals cannot be declared independent chronological channels. Adaptive boundaries, deleted intervals, retained classical commands and native partial transactions must belong to the real receiving interface. A scalar bad-island probability does not establish ||B_i|| or an exact T_i=G_i+B_i meeting semantic correctness.

A coarse norm bound on all globally excluded trajectories also does not give the required local B_i for each parent. The map classification must match the actual Gács damage certificates and exact Boolean coefficients, or a separate deterministic good-region theorem. The lemma is useful only if that bridge is supplied.

It does show why replacing the good map by a CPTP domination is unnecessary: the exact difference from the physical channel gives1+epsilon, and the resulting finite amplification can be explicitly absorbed in a genuine hierarchical construction.
