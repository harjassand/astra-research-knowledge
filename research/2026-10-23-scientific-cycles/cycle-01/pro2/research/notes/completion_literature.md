# Primary-literature boundary for common-operator spectral inference

Scientific contributor: `/root/completion_literature`, 21 October 2026.
Scope: primary-source check for the root's prescribed-action completion construction;
no numerical matrix experiment, complete competing programme, or new subagent.

## Conclusion

The interval of self-adjoint norm-bounded extensions is classical Krein extension
theory. The proposed finite-dimensional endpoint formulas are its elementary
Schur-complement/energy-space realization. The scientific contribution must be
stated as the resulting explicit executable certificate and the actual information
boundary on the saved data, if those are established. Neither existence of the
extension interval nor its Loewner extremality is a new general theorem here.

The cleanest directly applicable primary theorem inspected is Theorem 2.2 of
Tarcsay and Sebestyén (2024), with Lemma 2.1 providing the compatibility criterion.
It avoids requiring a dense domain and applies to real as well as complex spaces.

## Closest meaningful theorem

**Tarcsay, Zsigmond; Sebestyén, Zoltán.** “Reduction of positive self-adjoint
extensions.” *Opuscula Mathematica* 44(3) (2024), 425–438.
DOI: <https://doi.org/10.7494/OpMath.2024.44.3.425>.
Full primary text: <https://www.opuscula.agh.edu.pl/vol44/3/art/opuscula_math_4422.pdf>.

Lemma 2.1 identifies the extendibility condition for a partial positive symmetric
operator as `||Ch||² <= <Ch,h>`. Theorem 2.2 states that its positive contractive
extensions form the operator interval `[C_m, I-(I-C)_m]`, with `C_m=J_C J_C*`
from the energy-space factorization. The proof also verifies that *every* operator
between these endpoints has the prescribed action. Thus the statement is stronger
than merely bounding extensions already known to exist. Consult pages 427–429,
particularly equations (2.2)–(2.3). The root must establish a separate quantitative
rounding/input bridge for any numerical realization; the theorem supplies none.

**Sebestyén, Zoltán; Tarcsay, Zsigmond.** “Extensions of positive symmetric
operators and Krein's uniqueness criteria.” arXiv:2209.00318v1 (2022), later
*Linear and Multilinear Algebra*, DOI 10.1080/03081087.2023.2196610.
Primary preprint: <https://arxiv.org/html/2209.00318v1>.

Section 7 develops bounded extensions and shorted operators. Theorem 7.6 explicitly
writes the norm-preserving self-adjoint endpoints as `(I+S)_N-I` and
`I-(I-S)_N`, and identifies all extensions with their interval. The introduction
and bibliography attribute the underlying extension theory to Krein's 1947 work.
This preprint has visible typographical errors in the proof: its displayed
ordering after (7.4) reverses the endpoints, and the prose after (7.9) prints
inequality of endpoints in a uniqueness statement. These do not supply grounds
to claim new theory; use the 2024 theorem and the direct finite-dimensional proof.

A further relevant primary paper is Baidiuk and Hassi, “Completion, extension,
factorization, and lifting of operators with a negative index,” arXiv:1403.5133.
Its abstract explicitly generalizes Krein's interval of contractive self-adjoint
extensions and Shmul'yan's positive block-completion result. Full-text retrieval
through the web tool failed, so **no detailed theorem from this paper is used**.

## Exact mapping to the proposed finite-dimensional object

This section is our own algebraic mapping, not a quotation or an extra literature
claim. Let `X` have full column rank, let `G=X^T X`, `T=X^T Y`, and let `L<U`.
The prescribed action on `D=range(X)` is `A_0 Xc=Yc`. Symmetry on this domain is
exactly `T=T^T`. Normalize its desired spectral interval by

    C(Xc) = (Y-LX)c/(U-L).

The compatibility inequality in the cited theorem becomes

    (Y-LX)^T(Y-LX) <= (U-L)(T-LG),

or equivalently

    Y^T Y - (L+U)T + LU G <= 0.

Together with `T=T^T` and full rank of `X`, this is a necessary and sufficient
condition for a common symmetric completion with `L I<=B<=U I` and `BX=Y`.
The inequality includes positivity of the normalized partial action. Mere
positivity and norm at most one of a partially defined operator would not, by
themselves, be the correct positive-contractive extension premise.

When `H_L=T-LG` is positive definite, the energy form on the coordinate space is
`c^T H_L c`. Its inclusion map into the ambient space sends `c` to `(Y-LX)c`.
Consequently the minimal positive extension of `A_0-LI` is

    (Y-LX) H_L^(-1) (Y-LX)^T.

The same calculation applied to `UI-A_0` gives the other endpoint. This yields
exactly the root's proposals

    B_L = L I + (Y-LX)(T-LG)^(-1)(Y-LX)^T,
    B_U = U I - (UX-Y)(UG-T)^(-1)(UX-Y)^T.

Positive definiteness of both compressed endpoint matrices is an explicit
hypothesis of these inverse formulas. The full extension theorem also covers
boundary cases, but an implementation cannot silently invert a singular Gram
matrix. A pseudoinverse implementation must justify the associated range
conditions and exact rank decision. Strong ill-conditioning of the combined
stored bases is a separate numerical obligation even if each probe basis is
well conditioned in isolation.

The consequent monotonicity of *unweighted eigenvalue counts* under Loewner order
uses the ordinary finite-dimensional min-max principle. It does not transfer to
an arbitrary fixed-vector spectral CDF. Calling the resulting count interval
exact requires exhibiting both feasible endpoints and actually verifying their
count/inertia, including inclusive threshold treatment. No underlying spectral
subspace is to be replaced by the individual small-J node range.

## Information and randomized-query boundary

**Sun, Xiaoming; Woodruff, David P.; Yang, Guang; Zhang, Jialin.** “Querying a
Matrix Through Matrix-Vector Products.” ICALP 2019, LIPIcs 132, article 94.
DOI: <https://doi.org/10.4230/LIPIcs.ICALP.2019.94>.
Primary full text:
<https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.94/LIPIcs.ICALP.2019.94.pdf>.

This paper defines an oracle model allowing randomized adaptive matrix-vector
queries. Its real-matrix rank lower bound is proved using distributions of oracle
matrices, followed by Yao's principle; see Section 3.1 and Theorem 8. That result
concerns its rank problem and hypotheses, not this bounded self-adjoint CDF class.
It is a methodological comparator, not a transferable numerical lower bound.

The following scope distinction is elementary logic. Two completions built
*after seeing a realized random query block* establish ambiguity of its
consistency class. They can rule out a narrower deterministic interval that must
cover every operator consistent with those observations. They do not alone
contradict a repeated-run stochastic guarantee for each fixed input matrix.
The constructed competing matrices may depend on the observed random probes.
The statement `for every seed there exists a bad compatible matrix` does not
imply `there exists a fixed matrix with substantial failure probability over
seeds`. A randomized lower bound needs the latter quantifiers, or a suitable
input-distribution argument. This distinction remains even if all count endpoints
are computed exactly.

Also, the owner already possesses all coefficients of the finite model. An
oracle-transcript obstruction is a statement about deliberately retained
information, not impossibility of solving that known matrix or a lower bound
on algorithms allowed to inspect its entries. Input conversion allowances and
all representation/checking costs remain part of a practical operation.

## Retrieval and observed resources

Six web-tool batches were used. Their returned orchestration wall durations were
approximately 2.5, 4.3, 2.9, 2.4, 3.1, and 3.3 seconds, totaling about 18.5 seconds.
The batches contained two routine searches, one verification search, and follow-up
opens/finds. This is observed tool latency, not research or model-compute cost.
No numerical experiment or optimization was performed by this contributor.
No full external paper was copied into this archive.

Failed full-text routes: arXiv PDF1602.02546; HTML1403.5133; PDF1403.5133; and
PDF1403.5133v1 all returned DisabledError in web retrieval. Their abstracts were
read but are not silently substituted for theorem verification. The two relevant
primary full texts cited above and the ICALP primary PDF were successfully read.
Analytical reading, message writing, source preparation, inference tokens,
energy and monetary cost are unmetered. Do not add this note's source-check latency
to any enclosing measured wall clock as an independent non-overlapping total.

Web refs available to root, which must open a source itself before final citation:
`turn43view3` (2024 theorem), `turn43view0` (2022 preprint), `turn45view0`
(ICALP full paper); additional precise finds `turn45view2`, `turn48view1`.
