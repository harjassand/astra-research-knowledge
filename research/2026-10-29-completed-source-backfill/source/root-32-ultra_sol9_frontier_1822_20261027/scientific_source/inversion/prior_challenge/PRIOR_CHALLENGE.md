# Bounded primary-science challenge and frontier placement

Checked 28 October 2026. This challenge imports the accepted literal Hopf
strict-ROC theorem and support gaps. It neither re-audits the complete Hopf
proof nor establishes historical priority. The previously completed pulse
operation in inversion/ is unchanged.

The challenge acquired two consequential results. First, the accepted
polynomial and entire aligned family admit a smooth, coercive, objective,
stress-free, orientation-preserving stored-energy completion that retains
non-polyconvexity. That exact derivation has passed the independent whole
review in [physical_review/REVIEW.md](../../hopf/physical_review/REVIEW.md).
Second, an established theorem excludes the actual three-atom witness from
being a homogeneous bounded gradient Young measure. The latter application
has exact algebraic replay but has not received a separate independent
substantive review.

## The generic elastic phenotype is already prior science

Voss, Ghiba, Martin and Neff, [arXiv:2009.09690v1, Proposition 3.5](https://arxiv.org/html/2009.09690v1#S3.SS2),
submitted 21 September 2020, gives

    W0(A)=K-log K+log q+1/q,
    K=lambda_max/lambda_min, q=det A>0.

The proposition proves ROC, isotropy, compact connected sublevels and non-PC.
Its formula gives determinant blowup. Since t-log t>=1, W0-2>=0 with zero
set SO(2). Their non-PC proof applies the scalar minor-support criterion
at singular values (e^4,e^3), compared to (e,1). Thus objective nonnegative
ROC/non-PC energies with stress-free rotational wells and determinant blowup
were already available. The present completion must not be called the first
such model. This prior is nonpolynomial; its scaling includes log s and
s^{-2}, and is not made into the accepted homogeneous quartic by an invertible
linear matrix transport. [Journal DOI](https://doi.org/10.1017/prm.2021.9).

Earlier, Šilhavý's [2002 primary article, pp.325–328](https://www.mi.sanu.ac.rs/ysm/journal/_private/vol28_29/pdf_format/silhavy.pdf)
already gave a nonnegative O(n)-invariant ROC/non-PC function of linear
growth. For n=2, with singular values v1>=v2, it is v1 v2 when v1<=1 and
v1+v2-1 when v1>=1. Here O(n) invariance explicitly means BOTH left and
right actions. Its piecewise formula and growth differ from the current
positive homogeneous quartic. Positivity and objectivity alone are therefore
not defensible novelty boundaries.

## Objectivity is not the stronger rotational hypothesis in the cited results

For A in GL+(2), put C=A^T A and M=diag(1,-1). The main accepted polynomial is

    F(A)=(tr C)^2+(252/25)det C
                   +(99/25)sqrt(det C) tr(C M).

It is objective under left SO(2). A right rotation of A with M fixed changes
the last term. In a structural-tensor representation, simultaneous rotation
of C AND M expresses coordinate covariance; it does not establish material
isotropy with M fixed. Moreover, the displayed square root means F is not
a quadratic polynomial of the entries of C on GL+, although it is a quartic
polynomial of the entries of A on all real matrices.

This distinction is explicit in Schröder and Neff's [2003 primary article](https://www.uni-due.de/imperia/md/content/mathematik/ag_neff/invariant_formulation_of_hyperelastic_transverse_isotropy_based_on_polyconvex_free_energy_functions.pdf),
sections 2.3–2.4: objectivity is a left spatial rotation, while equation 2.7
imposes right material symmetry only for the prescribed symmetry group.
Their sufficient polyconvex invariant building blocks, including quartic
fiber stretch in equation 3.44, are a construction of PC models, not a
classification of all objective anisotropic ROC quartics. Substitution of
our sign-changing q tr(CM) coupling into those sufficient ansatzes is not
an acquired PC theorem.

Dacorogna and Koshigoe's [1993 primary article](https://www.numdam.org/article/AFST_1993_6_2_2_163_0.pdf)
uses hypothesis H on printed p.164: f(U A V)=f(A) for BOTH U,V in SO(2).
Their diagonal restriction criterion for PC, Theorem 2.1, therefore cannot
be invoked from left objectivity alone. The actual hypothesis was visually
checked in sources/DacorognaKoshigoe1993_p2.png. This complements the already
acquired stronger-symmetry boundaries in hopf/LITERATURE.md; it does not
claim a new symmetry theorem.

## The quartic method is established; the inspected examples do not identify this family

Bandeira and Pedregal's [2009 primary article](https://www.numdam.org/item/10.1016/j.anihpc.2008.08.002.pdf),
Theorem 1 and pp.1624–1625, already reduce quartic ROC parameter searches to
Hessian quotients and exchange the two quadratic polarization slots.
The whole 14-page article was read. Examples 1–5 are respectively the DM
T^2-cTq family, T^2-cq^2, T^2-c(tr A)^4, a nonhomogeneous trace family and
a rectangular-minor example. Example 2 covers the zero-coupling subfamily.
The nonzero qx aligned ROC/non-PC boundary was not supplied in those examples.
This is a bounded read-scope finding, not a priority certificate.

Gutiérrez's [2006 primary article](https://www.heldermann-verlag.de/jca/jca13/jca0514_b.pdf),
Corollary 4.2 and printed pp.58–59, provides a necessary QC test using three
compatible oscillation modes and derivatives through order four. Its extra
information depends on a cubic derivative. That derivative vanishes at the
origin for the present homogeneous quartic, so that particular application
does not settle QC. Translation to a nonzero base creates a cubic part and
could be informative; no such universal translated test or exclusion was
proved here. A zero cubic term at one base must not be reported as universal
vacuity of the theorem.

## A primary theorem rules out the actual three-atom route to QC failure

Müller's [1999 primary theorem](https://files-www.mis.mpg.de/mpi-typo3/preprints/1999/preprint1999_29.pdf),
Theorem 2 on printed p.3, says every bounded gradient Young measure supported
on diagonal 2x2 matrices is a laminate. The actual accepted increments span
Gamma=span{X1,X2}, with

    det(s X1+t X2)=(11s^2-5760t^2)/500.

This plane has two independent rank-one generators and an explicit invertible
left/right transformation to the diagonal plane. The exact transformation
is replayed in verify_completion.py. If the actual three-atom measure were
a homogeneous W^{1,infinity} gradient Young measure, this theorem would make
it a laminate, contradicting the accepted ROC energy's strict Jensen gap.
The full argument and boundedness scope are in
[JENSEN_COMPATIBILITY.md](JENSEN_COMPATIBILITY.md).

Thus the current finite minors witness is provably incompatible with that
gradient microstructure acquisition. A different compatible spatial
construction or a QC theorem would materially change the scientific scope;
neither has been acquired. Global QC remains UNKNOWN. The theorem does not
exclude arbitrary unbounded sequences with concentration.

## The 2026 objective non-QC construction is in a different dimension and degree

Conti, Dolzmann and Dondl's [22 October 2026 preprint](https://arxiv.org/html/2610.31886v1),
Theorem 1.1, claims a C-infinity objective ROC/non-QC function on 3x3 matrices.
Near SO(3) it is quartic in the Green strain, hence degree eight in the
deformation gradient. Its three-mode mechanism requires a third row,
e3 tensor (e1+e2), and does not give a planar 2x2 construction by deleting
that row. The stated global cutoff construction is not the present
homogeneous quartic. The source was read at the theorem, local construction,
compatible test and globalization; its claimed formal proof has not been
independently audited here. It is relevant new primary science, not evidence
that the planar QC question is settled.

## Retained scope after the challenge

The inspected sources did not supply an exact theorem or example subsuming
the positive homogeneous quartic in the even-Hopf sector with the accepted
nonzero coupling, its aligned infinite family and their explicit margins.
No world-priority conclusion follows. The source family and its coefficients
remain exact mathematical results whose historical novelty is UNKNOWN.
General ROC/non-PC separation, its scalar supports and three-point minors
interface, quartic polarization, positivity alone, and the broad elastic
phenotype are established prior science.

The [physical completion](PHYSICAL_DOMAIN.md) is an accepted exact derived
constitutive operation. It gives smooth strict ROC, quartic coercivity,
nonnegative stress-free wells, determinant blowup and non-PC on GL+(2), for
the main example and the entire accepted m>=197 family. Right normalization
gives the well SO(2), while moving the non-PC obstruction away from I. The
completed energies are materially anisotropic and cease to be homogeneous
quartics or even-Hopf energies. No material qualification, compatible QC
violation, minimizer-existence theorem or physical experiment is inferred.

All external acquisition was free, public and read-only. Sources, exact
replay inputs and outputs are retained locally. The bounded search used
objective/frame-indifferent/anisotropic quartic and hyperelastic terms and
followed the primary articles above. It is not a systematic literature
exhaustion. No purchased retrieval, paid compute, outreach, public write,
corpus integration or new agent was used.
