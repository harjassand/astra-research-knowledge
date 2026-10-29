# Joint restrictions and literal finite-precision access

30 October 2026. This strengthens/simplifies the proposed compiler's access
implementation. It replaces the normalized-child cache in the engineering
prototype and the support-cutoff construction in RESOURCE_QUALIFICATION §4.
The existing execution is preserved; this note does not claim a second run.

## 1. Do not divide a teacher child

For a selected positive-Q prefix h_i, store at the next cut's feature f_j the
JOINT restriction

    V_(i,o)(f_j) = Q(o f_j | h_i).

For the uniform row the value is O^(-L), where L is the parent's remaining
length. Each V_(i,o) is a subprobability density on child futures, bounded by1.
Its mass is the separately stored q_i(o). Its value is a product of next-token
probabilities starting at h_i. It never requires a query at h_i o.

Given parent coefficients alpha and the ACTUALLY OUTPUT token probability pi_o,
the reference array is

    w_o(f_j) = sum_i alpha_i V_(i,o)(f_j) / pi_o.

This is exactly the restriction of the virtual full signed parent density,
divided by pi_o. Coefficients are bounded by C/a. The asymmetric gradient lemma
uses only 0<=V_i<=1, integral V_i<=1 and a bounded coefficient box; it therefore
holds unchanged. No child is sampled, placed into the importance mixture, or
required to approximate a target conditional law. If q_i(o)=0 its entire joint
restriction is zero. No zero-probability conditional oracle is needed.

## 2. A full-future probability at finite precision

At a positive-Q prefix h the product for a fixed continuation f has factors in
[0,1]. Request each next-token factor to absolute accuracy eps/(8T). Track an
outward interval for the partial product. Before querying an extension, either
its partial product has certified positive lower endpoint, or its upper endpoint
is at most eps/2. In the latter case return0: the final product is at most eps/2.
If neither condition holds, refine the current factor. A value that stays
unresolved within the requested factor precision forces the partial product to
be at most eps/2 after adjusting the constants. Thus the algorithm does not need
to decide whether an arbitrary tiny probability is exactly zero.

A more literal fixed-budget implementation uses next-token intervals of width
eps/(16T) from the start: if an extension's lower endpoint is nonpositive, its
upper probability is at most eps/(8T), so STOP rather than query it. Its final
product is then at most eps/(8T). Otherwise the extension is certified positive.
Products of all non-stopped factors have error at most the sum of widths. All
teacher queries are at known positive-Q prefixes. Every sampled raw basis prefix
is positive-Q because P(h)>0 and D(P||Q)<infinity. This is a consequence of the
supplied promise, not a test by the learner.

Both V_(i,o) and the fresh full-row densities can therefore be cached to arbitrary
absolute eps using polynomially many queries and O(log(T/eps)) probability bits.
This is a VALUE-ORACLE result. Its service cost must be charged at that precision.
It is NOT a polynomial conditional-SAMPLE-only simulation: estimating an
exponentially small absolute tolerance from draws can take exponentially many.

## 3. Robust cache, constraints and the real transition

Let eps be a uniform absolute error bound for every cached row density, joint
restriction and token probability. Normalize the token rows as rational
probability vectors with l1 error<=2O eps. Put E_m=2S C O eps. Then the actual
computed marginals mhat have sum1 and satisfy |mhat_o-m_o|<=E_m. The actual token
rule uses max(mhat_o,b), normalized. Its denominator is at most

    1+v+O b+O E_m,

since the true signed token marginals have negative mass at most v. If the
displayed excess is<=1, every actual pi_o>=b/2=a. Moreover the TRUE virtual
reference normalization satisfies

    integral max(z(o,.)/pi_o,delta_child)
       <=1+v+O b+O E_m+E_m/a+v/a+theta_floor.

This is the only place token-row rounding changes the transition normalization
proof. The exact chain-rule inequality holds for ANY actual positive pi, hence
has no additional approximation term. There is no sequence of inferred teacher
conditional-error divisions.

For mixture floor mu_min=1/(S O^L), the true feature ratios R_i/mu are at most S.
Store rational approximations rhat_i and define muhat=sum_i rhat_i/S EXACTLY.
For eps<=mu_min/4 the ratio error is at most 4S eps/mu_min per row. Thus all
coefficient-state feature values differ from their true values by at most
4S^2 C eps/mu_min. Impose the rational constraint zhat/muhat>=2tau. The true
padded proxy is>=3tau at good features and the true values of all feasible
states are>=tau when the last error is<=tau/2. The uniform coefficient vector
is strictly feasible with ratio exactly1. Sum alpha=1 is imposed exactly, so
the virtual full signed density has mass exactly1 regardless of rounding.

At child features the raw reference value has error at most S C eps/a.
Clipping and log are Lipschitz with constants1 and1/delta_min. The empirical
gradient discrepancy is bounded by a polynomial in S,C,1/a,1/mu_min,
1/delta_min,B times eps. Choose eps so that this bound, O E_m+E_m/a, and all
ratio errors use at most tau/100 each. For example a sufficiently conservative
single value is

    eps = [tau a delta_min mu_min /
           (10^6 (S+1)(C+1)(O+1)(T+1)(B+1))]^4.

One may replace B by the explicit rational integer upper bound A*ceil(log2 x)
times2, avoiding a transcendental request in the accuracy rule. Finite interval
evaluation/LP certificates pay the same remaining tolerance. The bit length is
polynomial in T,log O,log(1/tau),log D,log N,log M. The tiny VALUE of eps is not
a polynomial-in-1/eps query-count claim: the primitive supplies requested
probability BITS, whose actual service cost is explicitly multiplied in.

Geometry has its own preliminary tolerance. With
mu_geo_min=1/((N+1)O^L), request density error at most
theta_geo*mu_geo_min/[1000(N+1)]. This changes the ratio columns by at most
theta_geo/100, fitting inside the robust-SVD constants in FRESH_SPANNERS. Its
bit length is again polynomial. It is not omitted from the value-oracle bill.

## 4. Sampling features and output tokens

Conditional Q-sampling is already an input primitive. If instead it is implemented
from next-token probability queries, draw a persistent uniform and compare it
with the categorical cumulative sums using successively refined intervals. An
exact chosen token has positive Q probability almost surely, so every subsequent
conditional call is valid. Here b bits means the cumulative probabilities have
width O(2^-b): request b+ceil(log2 O)+3 bits for EACH token probability before
summing. The probability that a comparison remains unresolved at that cumulative
precision is at most 2O*2^-b. Across a prescribed polynomial number of calls,
truncate at a known polynomial bit budget and count any unresolved outcome as
a declared compilation failure. A union bound fits this inside delta/10.
This avoids silently sampling an impossible prefix by rounding a zero upward.

The returned finite model uses rational token probabilities and no Q reference.
They can be sampled with expected polynomial fair-bit work, or with a finite bit
budget and separately allocated TV error. The teaching oracle's own numerical
complexity and the full-trajectory source's acquisition cost are inputs, not free
physical measurement capabilities.

## 5. Status

These are mathematical access/perturbation statements for the general proposed
compiler. The finite engineering run used normalized child arrays, floating SVD
and CLARABEL, with a full-support teacher, and hence did not exercise support-zero
or formal interval branches. Its output is not a verified implementation of the
formal astronomical resource schedule. The proof still awaits independent whole
challenge; no practical advantage or installed-library worst-case complexity is
claimed.
