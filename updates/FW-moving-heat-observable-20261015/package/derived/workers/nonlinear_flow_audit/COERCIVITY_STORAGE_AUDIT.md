# Interior Jensen constant and existing G storage-budget audit

15 October 2026. Separate continuation; old frozen source and audit files
are preserved. Internal analytic review, not external validation.

Root corollary reviewed at SHA-256
`2d7d329d73d47a87e9193b3448c89e1dc053608d57bdf1436c3b6c4ec01f1ac6`.
Root storage arithmetic receipt SHA-256
`f695e91a21d6e62fb047104bb744c7d1e6fb795ceacd29c0cf212679de18dd9e`.
Moving-kernel continuation report SHA-256
`d8ed5b008359599d8952bd7b45e40ccd4e65a6ac02bfdc2bd077c902fc9956b3`.

**Verdict:** the constant 4nu/1875, the earlier G value 3/1250, its exact
factor 6000 improvement, uniformity over the original alpha=3 interval
family, and substitution into N866's same-G gradient/horizon inequalities
are correct. The root preserves the fixed Heat18 diffusion and receiving
hypotheses. No boundary coercivity, practical solver, optimal constant, or
storage value computation is inferred.

## 1. Positive H remainder gives the exact Bregman factor

Under the negative-delta two-LMI hypotheses, the universal QC theorem gives

    F=lambda J_rho+mu j^2+nu H, lambda>0, mu,nu>=0,
    nu=alpha-delta^2/[8(2beta+delta)].

The first two terms are QC. With C A=(a-d,b+c), H(A)=|C A|^4. For vectors
x,h in R2, direct expansion gives

    |x+h|^4-|x|^4-4|x|^2 x.h-|h|^4/3
      =6(x.h+|h|^2/3)^2+2(x1 h2-x2 h1)^2>=0.

The factor 1/3 is sharp for this vector Bregman inequality: equality holds
at x=-h/3. Applied at x=C B,h=C Dphi, its integrated linear term is zero
for zero-boundary or periodic phi. Thus F's affine Jensen gap is at least
(nu/3) integral|C Dphi|^4.

## 2. Primary complex-valued transform theorem checked directly

The inspected primary source is Bañuelos–Janakiraman,
[Lp-bounds for the Beurling-Ahlfors transform, Theorem 1.1](https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf).
Its complex-valued estimate is sqrt(2(p^2-p)) for 2<=p<infinity; at p=4
this is sqrt(24). The separate real-valued bound is not used here.
The PDF was opened live, downloaded from the author's Purdue site, rendered,
and page 2 inspected visually. Saved source SHA-256:
`430876e18a0941fdfbdf30d33dc73dd876cccd39c2d38cc735610fcc45363a66`.
Source receipt and rendered theorem page are in this auditor's `sources/`.
No conjectural sharp transform norm is assumed.

For f=phi1+i phi2 with standard half-normalized Wirtinger derivatives,

    2 barpartial f=(a-d)+i(b+c)=C Dphi,
    |Dphi|^2=2(|partial f|^2+|barpartial f|^2),
    partial f=B(barpartial f).

Minkowski in L2 and the complex transform bound imply

    ||Dphi||_4^2
      <=2(||partial f||_4^2+||barpartial f||_4^2)
      <=2(24+1)||barpartial f||_4^2
       =(25/2)||C Dphi||_4^2.

Squaring gives integral|Dphi|^4<=(625/4)integral|C Dphi|^4. Therefore

    integral[F(B+Dphi)-F(B)]
      >= (4nu/1875) integral|Dphi|^4.

All factors are accounted for: 1/3 is the Bregman constant, 24 is the
squared complex L4 transform bound, 25/2 includes the half-derivative
normalization, and 625/4 is its square.

## 3. Domain, trace and parameter quantifiers

For bounded Lipschitz W0^(1,4) data, zero extension and compact smooth
approximation transfer both the elliptic estimate and the quartic Jensen
inequality. The same constant works on periodic rectangles: apply the
whole-plane gradient estimate to a periodic extension times chi(x/N),
divide both fourth-power integrals by N^2, and let N tend to infinity.
The cutoff derivative terms vanish, while the common integral chi^4
factor cancels. This is independent of the fixed cell dimensions.

A finite strip with periodic transverse direction and zero end profiles
can be glued periodically in the longitudinal direction because the traces
match at zero. The W1,4 periodic estimate therefore has the same constant,
independent of strip width. Arbitrary nonzero end profiles are not covered
by that gluing statement; N866 uses appended zero-end loops exactly where
coercivity is applied. Normalized circle measure multiplies both sides by
the same factor and does not change the constant.

At nu=0 the displayed argument gives zero. Sharp J_r cannot lose a positive
multiple of H and remain ROC, but that does not refute every possible
pure-fourth Jensen gap. The positive gap here is an interior consequence of
the explicit H remainder, not of reduced-Gram positive pivots alone.

## 4. Exact earlier G and source-family improvement

For the unchanged Heat18 quartic

    G=3H+(35/24)u^2+j^2-(5/2)u j,
    G=J_(-5/2)+(9/8)H.

Hence nu=9/8 and 4nu/1875=3/1250. Relative to 1/2500000 this is exactly
6000. For alpha=3 and every r in [-21/8,-5/2], alpha_*(r)<=15/8, so
nu(r)>=9/8. The same 3/1250 bound is therefore uniform over that original
compact family. This is not a uniform claim over all r<-2 and not a
claim that the new coercivity constant is optimal.

## 5. N866 receives the stronger constant without changing its operator

Read the current N866 dossier and the exact receiving proofs:

* `storage_horizon/FINITE_HORIZON_STORAGE.md`, whose coercivity step gives
  ||D Phi||_4^4<=(2M+eta)/gamma for eta-near-minimizers;
* `storage_spatial/THEOREM.md`, whose compact parameter construction uses
  R^4=(2M+1)/gamma and the fixed global Heat18 operator
  diag(4897/5000,5103/5000).

The new result concerns the identical G, identical affine adjusted energy,
identical zero-end trace contract and an all-background coercivity constant.
Its derivation uses a separate QC decomposition; it does not replace or
alter G's existing global Heat18 monotonicity. Thus gamma=3/1250 may replace
the old lower bound wherever those receiving proofs use coercivity. Growth
constants, endpoint entry budgets, effective data, mean resets, the fixed
diffusion and remaining costs retain their original contracts.

For U=(cos y,sin y), the unit entry xU has normalized fourth-power gradient
integral 1+2/3+1/5=28/15, so M=120(28/15)=224. Exactly,

    R^4=(2M+1)/(3/1250)=561250/3<21^4,
    E_*=2M/(3/1250)=560000/3.

The source B=0 horizon estimate is 6960 E_*(N-1)^(-3/4). For N=10^17 and
epsilon=1/1000, its validity is checked without irrational approximation by

    (6960 E_*/epsilon)^4 <= (N-1)^3.

The independent `check_continuation_corollaries.py` reconstructs the Bregman
and complex-gradient identities and verifies all the rational constants,
M, R^4, E_* and this horizon inequality. Its saved receipt is
`continuation_corollaries_receipt.json`.

This validates improved sufficient gradient/horizon budgets. It does not
reoptimize the spatial cutoff, precision, Fourier grid or global search, and
does not execute an objective evaluation or storage enclosure. For a
different negative-delta quartic, its own receiving heat/growth/input
interfaces would still have to be supplied; QC plus coercivity alone does
not silently provide G's particular Heat18 operator.
