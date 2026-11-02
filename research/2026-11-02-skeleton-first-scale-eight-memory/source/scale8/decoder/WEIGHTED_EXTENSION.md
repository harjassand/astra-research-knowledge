# Weighted-charge extension for auxiliary-check inflation

The same proof works with a fixed finite set of check types and positive weights w_t bounded above and below independently of scale. Replace syndrome Hamming mass by W(s)=sum w_type(x) over occupied checks. Assume each complete component macrostep satisfies

  W(output_C) <= rho W(input_C),  0<rho<1.

The connected shape and correction supports must be O(W(input_C)). The comparison fault changes O(1) weighted mass. Ancestor closure then gives W(U_i)<=rho^i W(U_0), with total trace mass O(W(U_0)/(1-rho)). Distinct occupied Gibbs leaf count is at least W(U_0)/(2 w_max)-O(1), so connected-animal entropy still yields exp[-c W(U_0)] for sufficiently small q.

The resulting fixed-qubit instability bound is

  P <= B exp[-c min{rho^{-h}, d/S_h}],
  S_h = sum_{i<h}(K rho)^i.

For K rho>1 and enough depth h≈log_K d, this gives exponent

  alpha = log(1/rho)/log K.

For K rho=1, the bound is exp[-c d/log d]; for K rho<1, it is exponential in d at sufficient depth.

This does not justify assigning ad hoc favorable weights to an inflationary rule. A reusable way to certify a possible weighting is a finite nonnegative type-transfer majorant A with weighted output <= w^T A x for every allowed component input type-count vector x. A positive vector satisfying w^T A <= rho w^T with rho<1 proves the needed contraction. For an unrestricted exact transfer matrix, existence is governed by spectral radius <1. If admissibility excludes some type vectors, the inequalities need only hold on the rigorously identified admissible cone, which can be weaker. Crucially, a coarse 1→2 auxiliary rule may still be harmless in a longer macrostep if the return pathway contracts enough; a cycle with net noncontracting charge cannot be fixed merely by changing positive type weights.

For the actual ell=8 auxiliary-face issue, this is a proposed verification method, not evidence that the required admissible cone or contracting weights exist.
