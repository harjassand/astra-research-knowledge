# Independent adversarial review

Date: 2026-11-05. Scope: the corrected nearest-neighbor proper-parent argument
in `PROOF_CANDIDATE.md`, including the revised contiguous-core moment estimate.

## Verdict

After correcting the Gram-matrix transpose error described below, I found no
remaining algebraic gap in the stated convergence argument for the unrestricted
Rai Eq. (17) hierarchy, under its explicit proper injective-MPS parent
assumptions. I independently derived the full-subspace ideal stitching identity,
the energetic boundary bound, and the unnormalized quotient comparison. These
give the claimed model-dependent O(sqrt(log n / n)) comparison to the n-site
periodic gap.

This is an independently reviewed proof argument, not a machine-checked formal
proof, peer-reviewed publication, or guarantee of novelty. The claim is not
general one-dimensional gap decidability, not a practical SDP runtime result,
and not a proof that arbitrary weak MPS parents satisfy the assumptions.

## Exact assumptions and gap definition

The argument needs a nonzero, positive, nearest-neighbor interaction h; a
primitive canonical MPS tensor with a faithful transfer fixed point; and
equality of the sufficiently long open-chain ground spaces with the MPS
boundary spaces. The uniform positive open-chain gap used throughout is a
standard proper-parent result, not a consequence of merely having an injective
infinite-chain ground state. The finite periodic ground state is unique for
sufficiently large lengths in this class.

The conclusion establishes the existence of the **periodic finite-size gap
limit** and convergence of the specified SDP bounds to that limit. It does not
separately identify this limit with an infinite-volume GNS gap. Such an
identification would need its own theorem or citation before changing the
meaning of “bulk gap.” Extra open-chain zero modes, as in weak-parent/PVBS-type
examples, lie outside the asserted proper-parent hypothesis.

## Verified steps

1. **Energy-moment identities.** Full local translation invariance makes all
   translated h_i, h_i^2 and anticommutator moments agree. With a=Tr rho h_i^2,
   b_r=Tr rho {h_i,h_(i+r)}, one has 0<=a<=M, b_1>=-2a, and b_r>=0 for r>=2.
   Thus Tr rho H_open^2 <= (n-1)v+2M. For the contiguous untouched core of m_c
   bonds, the sharper direct estimate is

       Tr mu H_c^2 <= m_c v + 2M.

   Indeed the difference from m_c v is a sum of nonnegative distant-pair
   terms and possibly the coefficient-one term b_1. No unjustified operator
   inequality H_c^2<=H_open^2 is used.

2. **Ground-mass removal.** If P projects onto ker H_open and Q=I-P, then
   h_i=Qh_iQ and h_i h_j=Qh_i h_jQ. Consequently Q rho Q preserves all moments
   used in the proof, even with ground/excited coherences. Its trace is at most
   (n-1)/g. The projected operator need not remain LTI, and the proof correctly
   does not assume that it does.

3. **Duality and normalization.** The strictly positive dual witness
   I/Tr h_1 supplies Slater feasibility. The stated delta=-M primal witness is
   valid: (h_1+h_2)^2+(M h_1-h_1^2) is positive and differs from g_3(-M) by
   h_2^2-h_1^2. Larger levels add positive disjoint terms. Near minimizers are
   sufficient; no dual optimizer is needed. The repair channel is trace
   preserving on the unnormalized mu. Hence its central energy remains m_c,
   rather than being silently rescaled to a normalized-state expectation.

4. **The corrected Gram limit.** For the explicit convention

       Gamma_L |a,b> = sum_word (A_word)[a,b] |word>,

   the Gram entries are E^L(|d><b|)[c,a]. With E unital and E*(sigma)=sigma,
   they converge to delta[a,c] sigma[b,d]. The limit is I tensor sigma, not
   I tensor sigma transpose. Positivity of sigma and primitivity give uniform
   bounds on all inverse square roots and pseudoinverses for long buffers.

5. **Full-subspace stitching.** Let R be the correctly defined right factor
   of the Gram limit. On a spanning pair of extended end-block code vectors,
   ideal decoding and joined encoding produce the exact physical coefficient

       (A_t A_r A_l A_s)[d,c] sqrt(R)[b',b] X[a,c,d,b,reference].

   The free indices a,b' go to the environment. This identity holds for every
   reference coefficient X, not just for one MPS state. The joined physical
   order is right buffer followed by left buffer, with neither buffer reversed.
   It proves that all boundary terms annihilate the ideal repaired image.

6. **CPTP completion and the correct good projector.** The decoder's reset
   branch is a genuine trace-and-prepare channel with the reference system
   preserved. It vanishes on the required code. The good projectors must cover
   ell+1 sites at each end, including the untouched inner neighbor, although
   the channel acts only on the ell-site buffers. Using only ell-site good
   projectors would not justify vanishing of the two buffer/core seams.

7. **No hidden buffer-length norm factor.** Every actual or ideal encoded
   output is in the joined S_(2ell). All internal joined-buffer interactions,
   including the periodic seam, therefore annihilate it. H_b acts on these
   outputs through only two core seams. This gives ||Phi*(H_b^2)||<=4M^2 and
   a compressed good-subspace bound O(theta^(2ell)), despite the unrestricted
   norm of H_b growing with ell. Positive-block domination then gives
   Tr Phi(mu) H_b^2 = O(ell)+O(n theta^(2ell)).

8. **Quotient and limit.** The exact finite spectral inequality
   H_per^2>=Delta_n H_per applies to any positive unnormalized repaired
   operator with positive energy; it need not be orthogonal to the ground
   state. The denominator is at least m_c. Choosing ell proportional to log n
   yields gamma_n>=Delta_n-o(1). Together with gamma_n<=Delta_N for all large
   N>=2n, this forces the periodic gap limit and hierarchy convergence. One
   can even avoid using monotonicity in this last step: every gamma_n is at
   most liminf Delta_N, while the comparison bounds limsup Delta_n by the same
   quantity.

## Error actually found and independent finite-matrix evidence

The initial numerical comparison used I tensor sigma transpose. For the supplied
generic complex tensor, an independent transfer reshuffling gives, at L=100,

- correct limit error: about 4.25e-14;
- transposed limit error: about 0.2706132722.

Thus the original claimed exponential comparison was false under its own
conventions. The ideal seam-annihilation test did not expose the mistake because
the ideal coefficient cancellation works for any positive product metric. The
metric error has now been corrected; the actual polar channel was unchanged.

`../mps_gap_independent_audit_20261105/check_stitching.py` imports none of the
proposer's test implementation. It independently builds the block maps and
channel by explicit matrix operations, retaining a complete reference basis.
For AKLT and the supplied generic complex tensor, buffers ell=2,3 give:

- actual isometry defects below 1.3e-14;
- full-good-subspace ideal seam residuals below 3.2e-15;
- compressed repaired H_b^2 norms agreeing with the reported values;
- direct agreement between transfer reshuffling and explicit block Grams.

The matrices' SHA256 and all results are saved in `stitching_results.json` in
that independent audit directory. These are sanity checks, not substitutes for
the algebraic proof above.

## Separately checked projected-Y extension

The Appendix D projected-Y restriction is not the same primal problem and must
not be conflated with unrestricted Eq. (17). Nevertheless its dual condition

    Q_(n-1) [Tr_1 rho - Tr_n rho] Q_(n-1) = 0

already supplies every energy-moment identity needed here: each contained
h_i, h_i^2 and {h_i,h_j} annihilates the open ground space on both sides, so it
is an allowed projected test observable. The same trace-removal and repair
argument therefore applies. Strict dual feasibility remains true, and the
delta=-M primal coboundary h_1^2 tensor I is itself an allowed projected Y.

There is an important printed indexing distinction. Literal Appendix D
Eq. (112)/(117) uses j<1+n-k, hence j<=n-2 when k=2, whereas Eq. (17) uses
j<=n-1. Under the literal Appendix D convention, take sigma=Tr_last rho on
L=n-1 sites. Its objective is exactly the natural g_L objective, and its
contained energy moments have the required translation identities. The result
is then gamma_cert,n>=Delta_(n-1)-o(1), not a same-level equality. Valid
large-periodic-system lower bounds give convergence to the same limit. This
extension is valid for sufficiently large n (in particular n>=4); it should be
written separately with the indexing convention explicit.

This does not establish an efficient numerical algorithm or identify finite-
level optima of the two variants. It is an extension of the convergence argument.

## Prior-art and significance limits

- [Rai et al., 2411.03680v3](https://arxiv.org/html/2411.03680v3) supplies the
  hierarchy and explicitly leaves general completeness/tight convergence open.
  The construction and basic SDP principle are theirs.
- [Rao, 2510.08427v2](https://arxiv.org/html/2510.08427v2) proves convergence of
  a different hierarchy for a fixed finite qubit system. It does not by itself
  establish this thermodynamic-limit assertion.
- [Rozman, Molnar and Schuch, 2607.19078v1](https://arxiv.org/html/2607.19078v1)
  provides directly relevant proper/weak-parent distinctions and improved
  martingale bounds. Existence of a proper MPS parent gap and exponential Gram
  convergence are established ingredients, not new conclusions of this work.

No claim that the broad Rai completeness question is solved is justified. No
novelty guarantee follows from this targeted literature screen. The reviewed
result is a conditional, restricted-class convergence proof; no new optimized
SDP value, improved physical gap estimate, or practical high-consequence
capability has been demonstrated by this audit.
