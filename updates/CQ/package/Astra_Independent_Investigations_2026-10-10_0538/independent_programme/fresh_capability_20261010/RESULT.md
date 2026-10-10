# Fresh computational capability screen — 10 October 2026

## Outcome

**No transformative invention established.** Two plausible, consequential targets
were screened. Local scientific-simulation reuse collided directly with prior
work. Guaranteed deep-transformer reuse after a small input edit reached a
concrete mechanism test, but the proposed inexpensive certificate became
useless after one layer. The natural correlated repair exposed uncharged dense
mixed products. These findings close these particular proposals; they do not
prove the capabilities impossible.

No deployed-model improvement, general attention lower bound, novel verifier,
or performance speedup is claimed. No external compute, publication, repository
push, third-party contact, or user-computer operation was used.

## Capability selection

The initial screen considered these missing practical abilities:

1. **Make a local physical-design change and obtain a reliable updated simulation
   immediately.** Boundary-response reuse and local residual certificates offer
   a credible route, with consequences for repeated engineering design. However,
   localized reduced-model training, certified error control, enrichment, and
   reuse after geometry changes already appear explicitly in ArbiLoMod. A
   cache-free Dirichlet/Neumann variant still rests on classical Schur/Rayleigh
   machinery. There was no new mechanism worth prototyping.
2. **Edit a small part of a long model input and preserve the actual output
   decision without recomputing the entire deep network.** Reusing fixed-query
   attention is elementary, but evolving queries create a genuine next-layer
   problem. A cheap, rigorous gate could make approximate reuse dependable. This
   target was selected for a construction and falsification test.
3. **Reuse compressed scientific/measurement data for unforeseen precise future
   queries.** Fixed summaries can discard precisely the signal a later query
   needs. No credible mechanism was identified that both avoids that loss and
   charges acquisition/storage honestly; this was not developed.
4. **Rapidly repair a trained nonlinear model after data changes.** The apparent
   local update depends on a dense inverse training Hessian and can fail when
   the optimization branch changes. No new method for obtaining that response
   from native training data was found; this was not developed.

This was a consequence-first screen, not a claim that all four are globally
unsolved or that familiar methods were newly invented.

## 1. The easy first-layer identity

Write an attention row as y = N/Z, with N = sum_j exp(s_j) v_j and
Z = sum_j exp(s_j). If only a set E of keys and values changes and the query
stays fixed, then

N_new = N_old - sum_E exp(s_old,j) v_old,j
                + sum_E exp(s_new,j) v_new,j,

Z_new = Z_old - sum_E exp(s_old,j) + sum_E exp(s_new,j).

For k edited tokens and n unchanged queries this costs O(n k (d+d_v)),
assuming the old outputs, normalizers and queries are available. This is an
algebraic reuse identity, not a new invention. Its floating-point check against
full attention had maximum discrepancy 4.45e-16.

**Important boundary:** every affected hidden row feeds the next layer. Its
query generally changes, including rows whose original input was unchanged.
The identity by itself does not yield a deep-transformer edit algorithm.

## 2. A proposed cheap certificate, stated exactly

For one original row let p_j be its attention weights, v_j its values, and
 y = sum_j p_j v_j. Partition keys into B groups G. Cache

P_G = sum_(j in G) p_j,
C_G = sum_(j in G) p_j ||v_j-y||.

Suppose score perturbations obey |delta s_j| <= b_G and value perturbations
obey ||delta v_j|| <= e_G within group G. Then

||y_new-y|| <=
 [sum_G ((exp(b_G)-1) C_G + exp(b_G) P_G e_G)]
 / [sum_G exp(-b_G) P_G].

**Proof.** Divide the new numerator and denominator by the old normalizer. The
new denominator is z = sum_j p_j exp(delta s_j), at least the displayed lower
bound. Subtract y, use sum_j p_j(v_j-y)=0, and write the numerator difference as
sum_j p_j [(exp(delta s_j)-1)(v_j-y)
          + exp(delta s_j) delta v_j]. Triangle inequality gives the result.

For the tested normalized residual block

x_new,i = x_i + alpha · Attention(sphere(X))_i W_O,
sphere(x) = sqrt(d) x/||x||,

an input ball of radius r_i around a nonzero x_i induces a normalized-vector
radius, for t = r_i/||x_i|| < 1,

rho_i = sqrt(d) sqrt(2 - 2 sqrt(1-t^2)).

Use 2 sqrt(d) when t >= 1. This follows from the maximum angle arcsin(t) between
x_i and any vector in its input ball. The implementation uses a rationalized
form for numerical stability.

With q_i the original query, and operator norms of W_Q,W_K,W_V,

b_iG = (||q_i|| ||W_K|| max_G rho
        + ||W_Q|| rho_i max_G ||k_j||
        + ||W_Q|| ||W_K|| rho_i max_G rho) / sqrt(d),
e_G = ||W_V|| max_G rho.

The next hidden-state radius is bounded by r_i + alpha ||W_O|| times the
attention bound. We cap the latter at 2 sqrt(d)||W_V||, since both attention
outputs are convex combinations of normalized projected values. No contractive
layer assumption is made.

### Honest costs

The original full forward and summary construction cost O(n^2 d) per layer.
The proposed additional cache is O(nB), plus ordinary O(nd) state. Once the
summaries and weight norms exist, radius propagation costs O(nB+nd); it needs no
new all-pairs scores. B=n eliminates grouping loss but uses quadratic storage
and time. The experiment constructs summaries as needed for convenience and
does not benchmark online speed. Its full changed forward is ground truth
only. Floating-point containment checks are not directed-rounding certificates;
the displayed real-arithmetic derivation is the mathematical guarantee.

### Test and rejection

`test_attention_edit_gate.py` uses seeds 7, 19, 41; n=192; d=24; 12 layers;
alpha in {0.1, 0.5, 1}; one input edit of norm 0.5; and B in {1,8,32,192}.
There are no trained weights, natural-language data, MLPs, positional encodings,
or causal masks. It is a deliberately cheap mechanism gate, not an LLM test.

All tested mathematical bounds contained the true changes numerically. At the
last token, actual 12-layer changes were 0.000834 to 0.091581. The corresponding
B=n bounds were 36.009 to 392.389. Even with one group per token, no run certified
radius <0.125 beyond layer 1. Radius <0.125 would preserve an original 0.25
margin between two logits with unit-norm readout rows. The true final changes
would satisfy that tolerance in all nine cases; the proposed certificate did
not establish it.

**Decision:** independent per-token balls lose essential correlations far too
quickly here. Increasing the number of groups does not fix the primary failure.
This falsifies the selected certificate as a plausible end-to-end mechanism;
it does not falsify every possible data-dependent or correlated certificate.

## 3. Why the obvious correlated repair is not free

Give the next layer a rank-one hidden-state variation a u^T, such as the
output of a value-only edit in the preceding attention layer. Let

u_Q = u W_Q, u_K = u W_K, u_V = u W_V,
t = K u_Q, z = Q u_K,
P = softmax(Q K^T/sqrt(d)), O = P V.

The exact directional output derivative is

D O = (P a) u_V^T
 + diag(a) [P diag(t) V - diag(P t) O] / sqrt(d)
 + diag(z) [P diag(a) V - diag(P a) O] / sqrt(d).

The expression retains correlation, but **P a and P diag(a) V depend on the
edited source** and are absent from the usual cached O=P V. If
 a = P_previous[:,j], retaining these for every possible source j requires
cross-layer matrices P P_previous and P diag(V[:,r]) P_previous. Straight
materialization has O(n^2) or O(n^2 d_v) storage and additional construction
cost. Computing these products on demand by the obvious method reinstates
dense attention work. Precomputing the query-side tensor also has O(n d d_v)
storage, not just O(nd). None of those costs can be treated as an oracle.

Five random tests with n=40,d=12 verify the displayed mixed-product identity to
6.25e-17 and agree with central finite differences to 5.06e-11. Rank-one hidden
variations gave rank-two score derivatives and rank-39 probability derivatives.

An exact structural warning is also easy: for any invertible positive
row-stochastic P, a rank-one score change 1 e_1^T has derivative

D P = diag(P[:,1]) (1 e_1^T - P),

whose nullspace is precisely span{1}; hence its rank is n-1. Such P arise in
dimension two from positive Vandermonde attention weights. This warns against
assuming that a low-rank score change remains low-rank through softmax.

**This is not a runtime lower bound.** The easy first-layer identity itself can
process a high-rank probability change cheaply. The unresolved issue is a
native, inexpensive representation of the new mixed products, with a useful
multi-layer error bound. No such representation was constructed in this pass.

## 4. A nonzero-margin summary collision

For m>=0 let n=m+1, keys k_j=j, old weights p_j=binomial(n,j)/2^n, and
values v_j=(-1)^j, j=0,...,n. Compare this cache with the same keys and weights
and opposite values. Their value-weighted moments through degree m are all
zero, by the finite-difference identity

sum_j (-1)^j binomial(n,j) j^r = 0 for r<n.

After a query change that multiplies each weight by exp(t j), the outputs are
opposites, with first output (-tanh(t/2))^n. For m=5,t=4 this magnitude exceeds
0.8. Adding the same fixed output bias 0.25 gives a strictly positive original
classification score for both caches and opposite new decisions. The baseline
is realizable either by log-binomial score biases, or by binomial multiplicities
of equal-weight tokens.

This only rules out fixed low-order moment summaries without additional range
or margin restrictions. It is not an arbitrary-sketch lower bound. The example
charges its score-range change n t = 24; making the query displacement tiny by
rescaling keys merely moves the cost into key norms.

## Stopping decision

The intended capability remains valuable. But this pass found neither a novel
cheap certificate nor a native correlated update mechanism that could justify
an exceptional capability claim. Continuing by tuning group sizes, assuming
small global Lipschitz constants, changing the network architecture, or building
a general robustness verifier would not satisfy this investigation's goal.
The route is closed at this scope, with reproducible evidence preserved.
