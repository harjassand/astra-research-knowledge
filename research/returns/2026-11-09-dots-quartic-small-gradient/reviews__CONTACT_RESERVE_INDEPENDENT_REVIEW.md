# Independent narrow review: contact-line reserve

9 November 2026. Hand-derived analytic check, with no numerical or symbolic execution. This is an additional source-bound review, not a change to the two earlier dispositions.

## Binding and result

Governing addendum: `quartic_orbit_cone_20261109/CONTACT_LINE_RESERVE.md`, SHA256 `8af64aa5f0232270d62c1a5a218d868fb3124b74de4c412c41f2fc85513c8a1d`.

**The extra reserve implication passes.** Given the already checked Type-II quadratic/cubic normal-form hypotheses, positivity F(e12)>0 suffices for the fixed nonzero-mean small-gradient inequality. Global pointwise positivity is unnecessary. The displayed c, transverse debit, D1/D2, and absorption are valid. Type I is also valid under its stated assumptions.

The broad conclusion for every nonzero mean of the full left-SO(2) rank-one-convex quartic cone is still conditional on the two cited N806 classification facts. They are not independently proved by this narrow review. The abstract normal-form implication and the concrete contact below do not require that whole-class exhaustion theorem. The origin remains explicitly unpaid in the broad conclusion.

## 1. Positive-ray reserve

In canonical coordinates, X=b e12+Y is an orthogonal decomposition. Homogeneity of degree four handles b of either sign: for b nonzero, F(X)=b^4 F(e12+Y/b). If |Y|<=eta|b|, continuity or a coefficient-sum estimate gives F(X)>=(f0/2)b^4. Since eta<=1, |X|^4=(b^2+|Y|^2)^2<=4b^4, so c=f0/8 is safe. If b=0 inside the cone then X=0, already covered.

Outside the cone, b^2<eta^(-2)|Y|^2 and therefore |X|^4<=(1+eta^(-2))^2|Y|^4. Combining this with |F(X)|<=K|X|^4 gives exactly

    F(X)>=c|X|^4-(K+c)(1+eta^(-2))^2|Y|^4.

For an explicit algebraic choice of eta, group the polynomial F(b e12+Y)-f0 b^4 by positive degree in Y and bound every monomial by its absolute coefficient times eta b^4 when eta<=1. A sufficiently small positive eta from that finite sum works. No positivity optimization is hidden. As before, an evaluated numerical radius is not supplied.

## 2. Compatible gradients pay the debit

The cubic tangent estimate in the frozen generic lemma did not use a quartic positivity assumption. Multiplying its integral |a|^3 bound by the ORIGINAL gradient bound epsilon gives the source's (A), not an unjustified infinity bound on a Hodge-projected component.

The identities d=lambda a+r and |Y|^4=(a^2+c^2+d^2)^2 give

    |Y|^4<=3[(1+8|lambda|^4)|a|^4+|c|^4+8|r|^4].

Here (x+y)^4<=8(x^4+y^4) and the three-term square estimate are sufficient. For normal components, |c|<=epsilon and |r|<=(1+|lambda|)epsilon, while their summed L2 energy is at most Qbar/nu_*. Hence the stated

    D1=12(1+8|lambda|^4)A1^3,
    D2=12(1+8|lambda|^4)A2^3
       +3[1+8(1+|lambda|)^2]/nu_*

are valid, conservatively. The debit has size at most

    D1 epsilon^(3/2)M^(1/4)Qbar^(3/4)+D2 epsilon^2 Qbar.

These are one extra factor epsilon smaller than the already controlled cubic terms. For epsilon<=1, replacing C1,C2 by C1+C_Y D1,C2+C_Y D2 and using the previous radius formula proves the claimed Qbar/2+cM/2 reserve. All zero-energy cases are included without division.

For Type I, the transverse projection of the original X has pointwise norm at most epsilon. Therefore integral |Y|^4<=epsilon^2 Qbar/nu_* and the quadratic energy directly absorbs both the cubic and quartic transverse losses. No differential estimate beyond the stated Type-I cubic structure is needed.

## 3. An explicit contact outside the globally positive subclass

N806 Section 6 gives

    G=3(u+v-2j)^2+(35/24)u^2+j^2-(5/2)ju,
    u=a^2+c^2, v=b^2+d^2, j=ad-bc.

Direct substitution yields G(I)=-1/24 and G(e12)=3. Thus this example is genuinely excluded by a global positive pointwise reserve. Its contact admits the new one-ray reserve.

I independently expanded the literal polynomial at I. With r=d-(3/2)a and determinant multiplier mu=-1/2, its Taylor quadratic and cubic are

    Q=r^2+(5/12)c^2,
    C=-(5/12)a^3+(1/2)a^2r-(5/12)ac^2+2ar^2
       -2bcr-(5/2)c^2r.

For clarity, the quadratic BEFORE subtracting mu det X is

    (9/4)a^2+d^2-(7/2)ad+(5/12)c^2+(1/2)bc.

Subtracting mu det X adds one half of ad-bc and produces the stated Q. The cubic restricts on c=r=0 to -(5/12)a^3 and contains at most one b. All normal-form hypotheses and F(e12)>0 are therefore checked directly for this specific contact, independently of whether the complete N806 rank-one-convexity classification is accepted. The new implication proves its small-gradient inequality at mean I. This does not prove anything about its arbitrary-amplitude Jensen inequality or its zero mean.

The original N806 result already handled perturbations close to the contact line in relative L2/L4 geometry, for unrestricted coefficients on a plane of means. This additional implication instead permits every compatible perturbation with sufficiently small ORIGINAL gradient supremum at the fixed contact. Neither statement subsumes the other's unrestricted quantifiers.

## 4. Limits and attribution

For a homogeneous quartic, small-gradient Jensen at zero implies the unrestricted zero-mean inequality by scaling any fixed test into the permitted radius. It cannot be obtained here by silently importing the nonzero-mean result or by letting the mean tend to zero without a uniform relative estimate. The source explicitly retains this limitation.

The primary prior/terminology comparison and the conditional classification status are those in `TYPE_II_INDEPENDENT_REVIEW.md`. The contact geometry, ray positivity, Hodge correction and earlier mixed interpolation come from N806. The reserve construction itself is an elementary cone/Young estimate. The earned increment is the use of the new small-gradient tangent bound to pay the entire quartic transverse debit. No priority claim, global quasiconvexity theorem, numerical radius or practical result is justified.
