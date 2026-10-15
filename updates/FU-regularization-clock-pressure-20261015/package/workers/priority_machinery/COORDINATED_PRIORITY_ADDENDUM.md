# Exact priority comparison after the coordinated extensions

Date: 2026-10-15. This addendum follows the parent's explicit coordination of the arbitrary-domain, noncompact, and critical-endpoint proofs. Earlier independent findings are preserved in `PRIMARY_COMPARISON.md`. Status: internal source comparison and mathematical reconstruction. External correctness and historical priority of the full theorems remain UNKNOWN.

## The theorem contracts being compared

| Candidate | Exact added contract | What the inspected predecessors actually supply |
|---|---|---|
| Compact cone criterion, already in PR94 | Arbitrary finite-order compact Banach-cone distribution; positivity in cone interior at every real tilt iff a scalar all-exponential positive regularizer exists; smooth radial strictly log-concave choice; arbitrary Hilbert-space dimension for B(H) | KV2001 supplies all-exponential scalar positive convolution in its endpoint-sign class. Mattner1999/Ruzsa-Szekely supplies scalar positive convolution with ordinary moments. The acquired Weyl literature supplies the operator distribution and support, not this equivalence. Diamond-Essen1978 original remains unread. |
| Arbitrary open convex D | Interior positivity exactly on a chosen D containing zero iff regularizer with moments containing D exists; smooth strictly log-concave choice with full moment domain *equal* to D, all boundary moments infinite, gradient diffeomorphism onto D, and arbitrary relative cone error | General convex barriers and Legendre duality are established machinery. Borwein-Vanderwerff2001 Section4 contains an arbitrary-open-convex-domain barrier. The acquired scalar quotient theorem does not specify arbitrary exact moment domains or margin-controlled gradient jets. |
| Noncompact class W | e^(a sqrt(1+|y|²))T tempered for every a>0; distribution order may depend on a; global Laplace-interior criterion with no eventual-sign assumption; smooth radial strictly log-concave all-exponential noise | Noncompact sign repair and all-exponential multipliers already occur in KV2001 Theorem1 under initial/eventual sign hypotheses. Mattner applies broadly with ordinary moments. W does not become a first noncompact theorem. |
| Universal bounded quantum endpoint | One smooth radial strictly log-concave kernel, scale depending only on m,R, works for every tuple with ||A(u)||<=R|u|, every H; leading 1/(2R) attained; largest iterated-log coefficient beta=1 under the stated envelope; offset necessary bound but optimum unresolved | The supplied explicit Pauli noise plus Vervaat1972 already has the leading and beta=1 tail shape for that tuple, and Gaussian postconvolution makes it smooth. Canonical Husimi has a universal Gaussian for the canonical representation, a different input class. Neither acquired result supplies the arbitrary-tuple common-kernel endpoint or universal sharp obstruction. |

No row is a clearance of novelty: a stated non-implication is about the actual acquired theorem, and the unread ancestors remain consequential.

## What Mattner's actual geometric-series operation implies

The original Section2.5 of [Mattner1999](https://ems.press/content/serial-article-files/25848?nt=1), printed615–617, was visually read. It explicitly works in the all-ordinary-moment characteristic-function quotient setting and credits Ruzsa-Szekely. The directly written signed-measure proof in [Pomatto-Strack-Tamuz, AppendixA Lemma1](https://arxiv.org/pdf/1807.06927), PDF15–17, makes the following moment-domain consequence transparent.

For a scalar signed measure mu of mass one having all exponential variation moments, their construction has

\[
\nu=G_{\sqrt2a}*(1-c)\sum_{k\ge0}c^k\pi^{*k},\quad
0<c<1,\quad
\pi={|G_a*(\mu-\delta_0)|\over\|G_a*(\mu-\delta_0)\|}.
\]

The displayed domination of pi by a Gaussian convolved with |mu|+delta shows that pi has every exponential moment. Tonelli therefore gives the *exact* moment domain

\[
\mathcal D(\nu)=\{g:c\,m_\pi(g)<1\},\qquad
m_\nu(g)=e^{a^2g^2}{1-c\over1-cm_\pi(g)}
\quad(g\in\mathcal D(\nu)).
\tag{1}
\]

This contains an open neighborhood of zero by continuity and c<1. Thus the known machinery already produces a scalar sign-repair noise with some exponential-moment neighborhood for compact signed measures, and also for noncompact signed measures with all exponential variation moments. It would understate the predecessor to say it provides no exponential moments at all.

However, when pi is nondegenerate, its mgf is unbounded in at least one real direction, so (1) is not all of R. At c m_pi=1 the positive series diverges. Making c arbitrarily small does not remove that finite boundary for a fixed nontrivial construction. This is a specific obstruction to the actual geometric-series construction, even on a Laplace-positive subclass; it is not an impossibility theorem for every use of old ideas. The exact arbitrary D and all-real-domain results need a further operation.

For the compact-distribution Fourier version, a compactly supported nonzero smooth characteristic numerator cannot itself have an entire all-exponential extension. The frequency cutoff step therefore also cannot be silently carried through an all-exponential contract.

## The precise operation added by the D proof

The coordinated proof constructs a dual barrier U on D whose Hessian can exceed an arbitrary continuous inverse margin, passes to V0=U*, and obtains

\[
0<D^2V_0(x)\le\eta w(\nabla V_0(x))I.
\]

A fixed compact primal mollifier controls every required higher derivative. A Gronwall estimate transports w over the fixed support neighborhood, and the global Hessian bound makes mollification a bounded perturbation. The latter preserves both exact moment finiteness and divergence at every boundary point. This supplies the finite-order distribution error estimate at the required local tilt, rather than treating an arbitrary barrier as sufficient.

[Borwein-Vanderwerff2001](https://journalofconvexanalysis.com/articles/jca08030/jca08030.pdf?v=2), Theorem4.1 and proof in Section4, was acquired and read at PDF9–10. It is a genuine predecessor for arbitrary-domain convex barrier existence. It does not, in that theorem, give the tolerance-dependent higher jets, convolution positivity, or the combined exact-domain regularizer. The new proof appropriately gives its own polar-integral/barrier and Legendre arguments. The local example p(x)=exp(x-e^x), with Gamma moment domain (-1,infinity), is the classical logarithm of an exponential variable; that example is not a novelty claim.

## The precise operation added by the W proof

The global convex remainder F_x(y)>=0 gives e^(-F_x)<=1. Translation estimates for its derivatives are polynomial in |y|, with a small factor delta(x). Multiplication by e^(g dot y) followed by a stronger weighted seminorm e^(-k|y|), k>|g|, absorbs those polynomials globally. A diagonal choice of slow slope handles arbitrary weighted orders and inverse margins. This is how support is removed; no uncharged truncation or uniform finite distribution order is assumed.

The negative-atom example in the coordinated proof has all exponential variation moments and L_sigma(g)>=1 while negative atoms occur at every positive integer. It lies outside KV's eventual-sign assumptions. Conversely, KV Theorem1 already covers some noncompact scalar tails, so support alone is not a distinguishing claim. The finite-domain signed-tail obstruction in that proof is properly scoped: it forbids all-exponential output noise when input moments diverge beyond an endpoint, and does not refute the W theorem.

## Endpoint attribution and the valid width transfer

The now-coordinated endpoint proof uses a two-denominator sandwiched Duhamel estimate. Analytic Taylor summation preserves those denominators; a compact-distribution seminorm alone lost them. This supports the achieved endpoint internally, while its beta=1 upper obstruction uses tilted positive moment matrices and the moment addendum handles arbitrary weakly normalized noise. I read that proof and addendum completely. No formal or external verification is inferred.

The [original Dickman comparison](DICKMAN_ENDPOINT_PRIOR_ART.md) materially narrows the tail claim: Vervaat1972 Theorem4.7.7 and Lemma4.7.9 identify the exact supplied perpetuity and imply its r(log r+loglog r) density tail. The saved short Gaussian-postconvolution proof removes its spherical singularity while keeping the expansion. The universal strict-log-concavity/common-tuple theorem and sharp upper obstruction therefore deserve separate names and citations from the classical tail shape.

I transferred the coordinated endpoint to maximal directional spectral width

\[
\Delta(A)=\sup_{|u|=1}\operatorname{diam}\sigma A(u)\le D.
\]

The noise can be common even with unbounded scalar offsets; its coefficient is 1/D and beta=1 is attainable. The proof recenters coordinates for a compact box cutoff and recenters the *fixed base operator* inside each sandwiched exponential derivative. No derivative of a spectral midpoint is taken. This avoids a sqrt(m) loss. The full proof and explicit sufficient scale are in [SPECTRAL_WIDTH_ENDPOINT_TRANSFER.md](SPECTRAL_WIDTH_ENDPOINT_TRANSFER.md). This is an internally established geometric strengthening, not an external-priority result or a low-cost implementation.

## Unresolved priority gates

- Diamond-Essen1978, original full theorem text: publisher and API access failures persist. Scalar transform criteria, arbitrary-domain or tail conclusions, and possible broader distribution formulations remain unread.
- Anderson1969/1970, original Weyl-functional-calculus fulltexts: abstracts are insufficient to establish or exclude positive regularization.
- Kamynin-Ostrovskii1982, *Zero sets of entire Hermitian-positive functions*, DOI [10.1007/BF00973491](https://doi.org/10.1007/BF00973491): explicitly connected by KV2001 to its zero-free multiplier discussion. The Russian MathNet download returned403; the apparent English PDF endpoint returned200 HTML, not a PDF. Original theorem comparison remains open. A zero-set theorem by itself cannot be treated as positive probability-convolution factorization; an entire quotient need not be a characteristic function.
- Ruzsa1983 original *Convolution quotients of nonnegative functions*, DOI [10.1007/BF01352002](https://doi.org/10.1007/BF01352002): publisher abstract was acquired, original PDF not acquired. The abstract's locally compact abelian L1 sign-repair operation is not a moment-domain statement.
- Werner1984 original operator-convolution paper, DOI [10.1063/1.526310](https://doi.org/10.1063/1.526310), was located but not acquired. The accessible Luef-Skrettingland fulltext supplies the projective-representation operation and its normalization, not arbitrary-tuple scalar noise.

The selective OpenAI/math Crouzeix inspection is unchanged: its positive boundary dilation represents holomorphic powers after similarity. The mixed self-adjoint exponential/scalar-convolution bridge needed here is absent from the inspected theorem. No connection was forced from the shared word “positive.”
