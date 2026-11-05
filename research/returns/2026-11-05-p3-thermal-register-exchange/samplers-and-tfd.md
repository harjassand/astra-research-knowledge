# Actual-check sampler obstructions and constructive TFD alternatives

The [integrated register result](README.md) retains the accepted history compiler as an efficient source-conditional loader. This page maps the newly supplied comparisons and alternative operations, rather than treating failed hypotheses as universal hardness.

## Extensive physical obstruction

For fixed allowed odd refinement `ell>=5`, at sufficiently large even depth, the actual BDL physical Z-check matroid has a minor

\[
\bigoplus_{i=1}^{r_N}F_7^*,\qquad r_N\ge a_\ell N>0.
\]

Both the physical relation space and dual syndrome space need `Omega(N)` added dimensions in any regular cover on the same coordinates. The [proof](package/sampler_route/sampler_obstruction.md) constructs the physical RX/Lawrence bridge, exact two-square Fano quotient, subdivision transport and disjoint packing. The auxiliary `[I|A^T]` matrix is an intermediate; its identity columns are not silently installed as Hamiltonian checks. See the [physical-bridge audit](package/decoding_route/matroid_bridge_audit.md), [exact certificate](package/sampler_route/two_square_fano.json) and [subdivision receipt](package/decoding_route/matroid_subdivision_audit.json).

The regular-matroid route needs regularity; the named Code Swendsen-Wang sufficient guarantees need logarithmic graphic/cographic cover defect. These conditions fail. Even granting a regular cover with defect `q`, positive zero-preferred weights give target-sector probability at least `2^(-q)`, and proposal TV error `delta` yields conditioned error at most `2^q delta`. Thus a logarithmic-defect rejection shortcut would be real, with abort/accuracy costs; the extensive obstruction rules out that small-defect route.

Large defect alone does not prove exponentially small acceptance for every weighted cover. Neither actual CSW slow mixing nor hardness of all Gibbs preparation follows. [P1's independent actual-check proof](../2026-11-05-p1-burst-constructive-exchange/physical-check-comparison.md) has its own refinement/depth scope.

## Complete relation-code decoding fails for the specified interface

The full recent QD-HDQI comparison concerns recovery of the relation code of indexed Hamiltonian Pauli terms, not physical-error decoding of the protected memory code. The actual BDL relation code contains `L=Omega(N)` disjoint bounded-weight nonzero relations. With `H=sum J_i(I-S_i)/2`, channel overlaps are `t_i=tanh(beta J_i/2)`. Granting a genie for complementary coordinates leaves independent unbiased bits on disjoint pure-state blocks, so even collective measurements obey

\[
P_{succ}\le\left[\frac{1+\sqrt{1-t_*^{2w_\ell}}}{2}\right]^L
\le\exp(-L t_*^{2w_\ell}/4),\quad
t_*=\tanh(\beta J_{min}/2)>0.
\]

At fixed positive inverse temperature this specified complete-decoding operation has exponential cost; amplitude amplification still leaves exponential scaling. The USD/rejection implementation has its own bound `(1-t_*^w_ell)^L`. The [completed independent audit](package/decoding_route/qd_hdqi_obstruction_audit.md) also separates the paper's sign-averaged normalization theorem from BDL's fixed frustration-free sign sector. This is a failed premise of that route, not a general Gibbs-sampling impossibility.

## Coherent history preparation and central-sector bypass

The [full decoding/TFD note](package/decoding_route/central_quotient_and_recent_decoding.md) preserves the relative-decoding paper's matched coefficients, Pauli algebra/relation data, canonical source TFD and certified radius/temperature requirements. The constructed short relations must be absorbed by a high-relative-distance BDL source; they are not claimed to generate every relation, so all possible relative sources are not excluded.

The accepted polymer compiler is made coherent along a controlled activity-scaling path. Quantum-walk filtering and a reversible history-to-syndrome map, logical Bell pair and conjugate encoders prepare the canonical TFD

\[
|TFD_H\rangle=\sum_s\sqrt{\pi(s)}2^{-k/2}
\sum_j|v_{s,j}\rangle|\overline{v_{s,j}}\rangle.
\]

Cutoff mass is chosen `O(epsilon^2)` because pure-state truncation costs its square root. Enumeration, reversible arithmetic, filtering, precision and both physical copies count. This coherent preparation is distinct from the classical-syndrome holding theorem.

Under compatible source/target Pauli algebras, missing target relations are `q=dim K_B-dim K_A` independent central source Paulis. Project the physical half of the canonical source TFD to their required sector, apply the corresponding Clifford identification on both halves and remove fixed registers. Conditional output is the exact target TFD, with

\[
p_\beta=\frac{Tr(Pe^{-\beta H_A})}{Tr(e^{-\beta H_A})}.
\]

Repeat-until-success costs `1/p_beta`; coherent reflections give the usual square-root improvement when supplied. Source error and trial caps are charged. For positive commuting homogeneous frustration-free constraints, Fourier positivity gives `p_beta>=2^(-q)`.

A constructed local noncommuting two-dimensional layout comes from a one-dimensional source restricted by one global central parity. A local sector flip changes two bounded terms, giving `p_+>=(1+exp(4 beta J_0))^(-1)`. The established canonical one-dimensional TFD preparer then supplies the target at each fixed finite temperature with polynomial size/precision cost. This bypasses a decoding-radius temperature restriction for that family. Its thermodynamics remains a restricted one-dimensional source; it is not a generic two-dimensional Gibbs sampler or a new passive-memory theorem.

The [finite central-quotient receipt](package/decoding_route/central_quotient_verification.json), [script hashes and executions](package/verification_receipt.json), proofs and primary-source conditions are retained unchanged. Capital did not execute the verifiers.
