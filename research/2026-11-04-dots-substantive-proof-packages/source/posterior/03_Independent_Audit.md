# Independent posterior-reduction audit

Date: 2026-11-04. Scope: POSTERIOR_OBSTRUCTION.md and POSTERIOR_GENERALIZATION.md, including the clarification that original unit interactions are deleted before degree reduction. This is a mathematical proof audit, not implementation verification or a priority search.

## Verdict

Both reductions are justified. A uniform sampler, polynomial in encoded source size and inverse TV tolerance, for arbitrary observed original edge bits in the accepted zero-field cubic tensor networks would imply an FPRAS for #BIS. Output of original edge bits alone suffices. This is a conditional complexity implication, not an impossibility theorem, a novelty claim, or evidence of practical computational advantage.

## Cubic posterior construction

- For an n-vertex cubic target, the doubled subdivided source has 2n core vertices, 6n ports, and 12n edges. Every degree is three. The 3n cross-copy edges form a matching covering the ports. Simplicity is preserved.
- For incident parameters a_1,a_2,a_3>1, the raw tensor is the invertible three-leg image of the diagonal tensor with entries T_000=T_111=1. Its hyperdeterminant is product_i (a_i^2-1)^2>0. Column normalization gives the same coefficient product_i(a_i+1) to both latent states. Every edge Gram matrix is symmetric with equal diagonal entries, so all unconditional fields are exactly zero and every interaction is ferromagnetic.
- Fixing a cross-copy edge bit contributes separate unary endpoint factors. Their activity is a for observation 1 and 1/a for observation 0. Thus the chosen port fields are correct, and conditioning separates the two copies exactly.
- On the alignment event, each copy's core law is exactly the target with the selected middle interactions. For each unaligned assignment, the relative strong-edge penalty is at most B^-1, the field ratio at most P, and the middle-edge ratio at most Q. Summing gives Z_bad/Z_aligned <= 2^(3n)PQ/B. The chosen R implies this is at most delta. Products and logarithms of rational weights have additive encoding length, so the large numerical couplings do not invalidate polynomial bit size.
- Rational approximation of a=beta+sqrt(beta^2-1), with a>1 maintained, realizes the requested interactions to an allocated total log-weight error. Source size, construction time, and raw-entry bit lengths are polynomial in input length and logarithmic inverse accuracy.

## Posterior fields and original-only output

Deleting observed interactions leaves spin-zero vertex weight
c_v(0) product_observed B_v,e(b_e,0) / product_unobserved r_v,e
and spin-one weight c_v(1) product_observed B_v,e(b_e,1). Their ratio is exactly the stated residual activity. Residual interactions remain ferromagnetic; the componentwise field test is the correct sufficient certificate. Likelihood constants must be retained for evidence-probability estimation.

For a complete original assignment x, the reverse conditional is
q(s|x) = product_v normalized[c_v(s_v) product_e B_v,e(x_e,s_v)].
It is a product of positive local probabilities. Completing the evidence bits and applying this kernel converts an original-only posterior sample to the desired joint law, with TV error contracting under the kernel. The constructed factors and these probabilities are rational with polynomial bit length; capped approximate coins can receive a separate error budget. No hidden-spin oracle is assumed.

## Generalization and counting

The path-splitting comparison is valid even for opposing fields because all activity weights remain on fixed representatives. Its unaligned mass bound, partition factor B^h, and polynomial encoding estimate are correct. The degree-deficit parity argument and separate K4-minus-edge gadgets produce a simple cubic graph, including when two deficits belong to one old vertex. Unit gadget edges give the claimed independent-spin factor; replacing them by 1+tau causes only the bounded global weight perturbation stated in the proof.

Pinning a spin to 0 changes a neighbor activity by division by beta; pinning it to 1 multiplies it by beta. Scalar constants may be discarded for sampling. Each original edge contributes at most once, so encoding lengths remain polynomial throughout the self-reduction. At each adaptive stage, uniform sampling guarantees and fresh randomness support Hoeffding bounds and a conditional union bound. Selecting a probability bounded below by 1/3 makes additive estimates into relative estimates. The identity Z=w(s*)/product_i p_i is exact for the selected assignment.

The current text incorporates two routine conventions that make the algorithm fully specified: estimate the two selection probabilities as complementary empirical frequencies, and clip the fresh denominator estimate below at 1/4 or return a flagged failure. For a<=1/12, the successful-event fresh estimate is at least 1/3, so clipping changes no successful run.

Goldberg and Jerrum's Theorem 1 explicitly gives the general varying-field Ising/#BIS approximation equivalence. Their rational-input convention and partition normalization are compatible with this reduction up to known efficiently approximable positive factors. Source: [The Complexity of Ferromagnetic Ising with Local Fields](https://www.cs.ox.ac.uk/people/leslieann.goldberg/papers/ising.pdf), Sections 1.1–1.3 and Theorem 1.

## Main-proof repair check

The current PROOF.md, SHA256 07daa9482f4a569b801e59c5f6e73ff03e8bfc478bf20f51df541b46402c8705, incorporates all three repairs requested in PROOF_AUDIT.md:

1. Section 6 explicitly divides by product_e(2t_e) when recovering the pre-subdivision partition function.
2. Section 7 separately rationalizes subdivision couplings, preserves the lower interaction margin, allocates their perturbation error, and approximates reciprocal normalizations using the unrounded identity.
3. Section 7 distinguishes expected-time exact rational coins from capped rejection, bounds aggregate cap probability by gamma, and charges fallback/error appropriately. The quantitative implementation discussion repeats this distinction.

No missing repair identified. This check does not repeat the full main-proof audit.

## Reviewed posterior version identifiers

- POSTERIOR_OBSTRUCTION.md SHA256: 0d8fd698010510db3df180dfdbaf34f0dcb6ca6643a0f31c60c491b86059e328.
- POSTERIOR_GENERALIZATION.md SHA256: b8489d313d2fff574eae27c636666509df548bcbaf43824078d20998f3daba70.

The audit includes the final probability-estimation conventions and updated status lines in these versions. Later substantive revisions require another check.
