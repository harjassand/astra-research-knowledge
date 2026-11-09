# Assumptions and dependencies

## Original density

For F=[[a,b],[c,d]], set u=a²+c², v=b²+d² and j=ad−bc. For r>0,

    J_r(F)=alpha(u+v−2j)²+beta u²+j²+r u j,
    alpha=3r/[8(r+2)], beta=r(r−1)/6.

Equivalently let k=(2r+1)/3>1/3, B=(3k−1)/[8(k+1)] and F0=(5k+1)/[2(k+1)]. Then

    J_r(F)=B[k²u²+v²+2uv+4k u j−4v j]+F0 j².

No normal penalty, corrected density or restricted-gradient replacement is used.

## Original theorem

For each fixed r>0 and affine mean F, there is a positive radius delta(F,r). For periodic Lipschitz vector fields, or admissible zero-boundary Lipschitz tests, the Jensen gap is nonnegative when ||Dphi||∞<=delta(F,r).

At A=[[0,k],[1,0]], the proof gives the stronger gap Qbar/2+c_k M/2, where

    Q(X)=((3k+1)b+2kc)²/4+[(3k−1)(k+1)/4]d²,
    Qbar=int Q(Dphi), M=int|Dphi|⁴,
    c_k=(3k−1)min(k²,1)/[4(5k+1)]>0.

The test field is compatible: X=Dphi. Replacing it by a determinant-balanced matrix law is not permitted. The original gradient, not its Hodge projection, is bounded in L∞.

The radius is a positive formula in declared finite periodic Calderon-Zygmund, Hilbert-transform and mixed-interpolation constants. Those constants were not numerically evaluated. They depend on r and fixed coordinates; no limit-uniform assertion is made as r→0.

## Proof dependency map

- Literal polynomial algebra -> corrected quadratic/cubic and quartic coercivity: proofs/LOCAL_QC_DEGENERATE_CONTACT.md §§1–2.
- Standard finite-p Fourier multipliers and complex interpolation -> mixed L6/L2 to L3 estimate: same proof §3; independently reconstructed in reviews/INDEPENDENT_REVIEW.md §3.
- Periodic Hodge projection in p=2,3,6 -> normal/tangent estimates: proof §§4–5.
- Young absorption and admissible extension/mollification -> fixed-contact theorem: proof §6.
- Exact right-A symmetry plus explicit acoustic determinant 9r⁴t⁴ -> all affine means: review §§6–7. The review reconstructs this step independently, so the theorem does not require trusting the older symbolic code.
- Original rank-one convexity/source conventions are documented in sources/ORIGINAL_ASTRA_PROOF.txt. Its broader claims are not automatically adopted.

## Abstract Type-II implication

The complete unconditional analytic contract is an exact Taylor decomposition after a determinant null-Lagrangian subtraction, Q>=nu[c²+(d−lambda a)²], lambda!=0, a cubic that restricts to kappa a³ on c=0,d=lambda a, and partial_b²C=0.

The first lemma assumes F(X)>=c|X|⁴. The subsequent contact-line lemma instead needs only F(e12)>0 at the specified nonzero contact. It constructs F(X)>=c|X|⁴−C|Y|⁴ and pays the transverse debit using compatibility and small original-gradient supremum.

The concrete polynomial

    G=3(u+v−2j)²+(35/24)u²+j²−(5/2)ju

has G(I)=−1/24 and G(e12)=3. At mean I, direct expansion gives Q=(d−3a/2)²+(5/12)c² and the required cubic. This application uses no whole-cone exhaustion assumption.

## Conditional wider consequence

N806 supplies the claim that every non-polyconvex member of the left-SO(2) rank-one-convex homogeneous quartic cone has positive rank-one values and only Type-I/Type-II nonzero contacts. The implication from those hypotheses to small-gradient stability is checked here. The entire classification is not independently reconstructed here, so wider nonzero-mean coverage remains conditional.

There is no general origin theorem in this consequence. For a homogeneous quartic, weak quasiconvexity at zero is already the arbitrary-amplitude zero-mean inequality by scaling.

## No computation dependency

These are analytic proofs. The package requires no scientific software, stored floating matrix, optimizer, empirical gate or symbolic receipt. verify_manifest.py is solely a standard-library hash check.
