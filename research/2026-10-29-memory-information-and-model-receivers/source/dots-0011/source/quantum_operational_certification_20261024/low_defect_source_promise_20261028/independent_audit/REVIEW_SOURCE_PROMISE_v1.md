# Independent review: iid near-pure source tails and SWAP acquisition

28 October2026. **Accepted at the stated iid common-source, trusted-test and success-weighted scope**, with operational clarifications below. No change to the original governing source or exact-tail file is required. No source was experimentally acquired by this review.

## Independent representation argument

For a fixed set of t exceptional tensor positions, every vector in the term with the other k−t positions in the dominant vector is invariant under the subgroup permuting those latter positions. The central projector onto an S_k isotypic component commutes with this subgroup, so its image is still subgroup invariant. Iterated ordinary branching removes t Young-diagram boxes. A trivial S_(k−t) component can occur exactly when the row diagram(k−t) is contained in nu, namely nu_1>=k−t. Consequently no term with t<=j has support in defect>j. Positive mixture weights over exceptional positions give the stated Binomial(k,e) tail, and stochastic monotonicity gives the delta bound. Noncommuting exceptional states do not affect this invariant-subspace argument.

This is a virtual spectral decomposition, not eigenvector learning or eigenbasis access. The proof applies to positive integer k; empty tensor powers can be assigned the trivial convention separately. Zero impurity is handled by the pure term alone, without needing to choose an orthogonal normalized sigma in a one-dimensional space.

For the environmental application, take the tensor product of a SINGLE-COPY purification of rho_AB. Its single-copy environment spectrum equals that of rho_AB, and the preceding theorem applies to its k-copy environment state. A globally re-encoded purification of the whole block need not preserve this environmental tensor-factor/permutation action; it is not the object whose Schur weights were bounded. Choosing a product purification for analysis does not require physical environment access. Actual Alice/Bob label conditioning can increase the conditional bad weight. Only its weighted sum over branches is bounded by the unconditional tail. Further postselection must retain its probability weight.

## Purity implication and observable acquisition

Let r=lambda_max(rho), P=Tr(rho²). Independently, P<=r and P<=r²+(1−r)². If delta<1/2 and P>=(1−delta)²+delta², then P>1/2 and r>1/2. Monotonicity of r²+(1−r)² on that interval yields r>=1−delta, including equality. The premise is sufficient, not necessary for the spectral condition; it can reject states whose small remaining weight is spread over many eigenvalues.

For two independent copies, swap expectation is P, hence antisymmetric probability q=(1−P)/2. In the distributed implementation, one must multiply Alice's and Bob's signs FROM THE SAME TWO-COPY TRIAL, not multiply separately estimated mean signs. Their commuting local projective measurements give the product-observable expectation of global SWAP. The exact entangled test fixture has global purity41/50 and antisymmetric product-sign probability9/100, with local joint probabilities283/400,9/200,9/200,81/400. These test copies are consumed, so the extra local measurement disturbance is irrelevant to later independent source copies.

The operation needs two simultaneously retained copies, trusted local controlled operations/readout and classical sign communication. No assertion is made that those controls are available with negligible noise or cost. The standard Schur label transform is basis-independent, but neither that fact nor this tail proof supplies the separate low-defect decoder's efficient access circuit. Primary context for Schur-subspace measurement: Bacon–Chuang–Harrow, arXiv:quant-ph/0407082, https://arxiv.org/abs/quant-ph/0407082 . No novelty claim for Schur measurement or the SWAP identity is made.

## False acceptance, stationarity and honest success weighting

For0<delta<1/2, put q0=delta(1−delta). With fixed n and acceptance only at zero antisymmetric events, P_q(accept)=(1−q)^n. Thus q>q0 is falsely accepted with probability at most(1−q0)^n<=beta. At delta=0 this finite zero-event rule cannot certify exact purity for beta<1, because the required inequality is1<=beta. This is a limitation, not a loophole.

If the observed probability differs from actual q by at most a known bias radius c, use the positive null margin q0−c and require(1−(q0−c))^n<=beta; without q0>c the guard cannot work. Unknown or uncontrolled SWAP bias is not covered. Adaptive choices of delta,n, cutoffs or repeated attempts require their own confidence allocation; the displayed fixed-n test does not grant optional-stopping validity.

The statistical claim is frequentist. It is not P(source good|accepted)>=1−beta. For any fixed iid common source, let B be its fresh-block bad-sector probability and eta the certified binomial-tail target. If q<=q0, then B<=eta and independent fresh copies imply E[1_accept B]<=P(accept)eta. If q>q0, then E[1_accept B]<=beta. Therefore the uniform success-weighted bound E[1_accept B]<=P(accept)eta+beta is valid. A conditional bound after dividing by an unboundedly small acceptance probability does NOT follow. Any conversion of B into decoding risk still needs the separately proved code/recovery theorem.

Independence/stationarity of the test pairs and subsequent source block is an actual assumption. Neither the SWAP counts nor one-copy marginals certify it. A source with common marginal state but correlated copies can violate the binomial law.

## Independent exact checks and costs

check_source_tail_v1.py reproduces every numerator/denominator in exact_tails_v1.json. It also independently evaluates all five S4 sector weights using exact character sums for20 spectra across dimensions2,3,5,10, and checks all defect cutoffs. The two-copy pure-product counterexample |0>|1> has antisymmetric weight1/2 despite pure individual marginals; it is non-identically distributed, not a common iid source.

A stronger correlated same-marginal example is

    Omega=(1−2delta)|00><00|+2delta|psi_minus><psi_minus|.

For0<delta<=1/2 both marginals have largest eigenvalue1−delta, but antisymmetric weight2delta exceeds the iid Binomial(2,delta) tail2delta−delta². The checker verifies delta=1/10 exactly:1/5>19/100.

For beta=1/1000, the minimal zero-event counts for delta=1/20,1/100,1/200 are n=142,695,1386, consuming284,1390,2772 source copies respectively, before the protected block and local test resources. Boundary acceptance is only approximately.001; even at actual q=q0/2 it is approximately.032. This is a valid acquisition guard but not high throughput. POWERED_TEST_ADDENDUM_v1.md describes a standard separated-alternative count threshold with higher acceptance, explicitly as protocol design rather than performed acquisition.

## Scope received

The source-tail and sufficient acquisition implications are correct. They do not provide a global state/environment reconstruction, conditional success guarantee, arbitrary correlated-memory result, or implemented low-defect decoder. Fixed positive delta still requires j growing with k for this tail estimate to remain small; a k^O(j) implementation is not thereby polynomial. The useful fixed-j regime delta=O(1/k) carries real preparation and acquisition obligations.
