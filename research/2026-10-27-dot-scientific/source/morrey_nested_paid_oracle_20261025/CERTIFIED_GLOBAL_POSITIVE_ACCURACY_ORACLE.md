# A certified global paid reward oracle at every positive accuracy

## Result and precise input model

For a boundary reward f supplied with a known Lipschitz constant L, a bound on |f|, and certified point-value evaluations to any requested accuracy, there is a terminating algorithm which, for every rational epsilon>0, returns:

- an ACTUAL complete paid law with a certified reward lower bound A;
- an ACTUAL verified rational polynomial null-concave boundary majorant P, giving the GLOBAL upper bound B=P(0);
- the certificate 0<=B-A<epsilon.

Termination has no claimed useful complexity or computable a priori scale bound. The result does not decide exact source membership, return a Morrey separator without an actual source gap, or promote an unverified polynomial to an upper bound. Arbitrary continuous f without a computable modulus/evaluation model is not an algorithmic input covered here. A known computable modulus can replace Lipschitz continuity with the corresponding boundary-net/integration modifications; only the Lipschitz case is detailed.

## 1. The actual source-specific value function

Let C be the weak closure of the boundary terminal laws of finite null trees rooted at0, with finite convex mixtures. Let

 V_f(x)=sup over finite boundary null trees rooted at x of integral f.

The independently audited ACTUAL_SOURCE_PRIMAL_DUAL_RECEIVING_THEOREM.md proves:

- V_f is bounded and null-concave;
- bounded separate concavity gives interior local Lipschitz continuity;
- every boundary-root E-supported law preserving mean and q is a point mass;
- compactness then gives uniform boundary concentration of all paid posteriors as the root approaches the boundary;
- consequently V_f is continuous on ALL of compact E, equals f on Sigma, and V_f(0)=sup_C integral f.

These are actual properties of this elliptope/source, not assumed regularity of a formal HJB equation.

## 2. Strict rational polynomial majorants are dense from above

Fix a target error epsilon>0. For lambda<1, V_f(lambda z) is defined and null-concave on the expanded body lambda^-1 E, which contains an open neighborhood of E. Convolution there with a sufficiently small compactly supported smooth nonnegative kernel preserves concavity along EVERY null direction. Uniform continuity of V_f implies that for lambda close enough to1 and a small enough kernel, the resulting smooth U satisfies

 |U-V_f|<=epsilon/8 on E.

This is an existence/density argument; the later enumeration does not pretend to know the required modulus of V_f or these smoothing parameters.

Put delta=epsilon/48 and

 Q(z)=U(z)-delta|z|^2+epsilon/4.

Since |z|^2<=3 on E,

 Q-f>=epsilon/16 on Sigma,
 D^2Q[d,d]<=-2delta |d|^2 for q(d)=0,
 Q(0)<=V_f(0)+3epsilon/8.

A smooth function defined on a neighborhood of E has polynomial approximations in the C2 norm on E: extend it smoothly with a cutoff to a surrounding cube, then use ordinary C2 polynomial approximation on that cube. Approximate the coefficients rationally. Choose a rational polynomial P with uniform value error<=epsilon/32 and Hessian operator error<=delta. It follows that

 P-f>=epsilon/32 on Sigma,
 D^2P[d,d]<=-delta |d|^2 for null d,
 V_f(0)<=P(0)<V_f(0)+epsilon.

The lower inequality follows by actual null-tree Jensen and closure. Thus there are STRICT rational polynomial upper certificates arbitrarily close to the unrestricted optimum. This does not assert that every numerical near-majorant is valid.

## 3. Finite verification and enumeration

Enumerate rational polynomials P, rational margins tau,sigma>0, integer phase-net sizes N, and evaluation precisions. Each tuple has a finite verification test.

**Null-Hessian test.** Exactly decide the compact semialgebraic statement

 for all z in[-1,1]^3 with F(z)>=0,
 for all d with |d|^2=1 and q(d)=0,
 d^T D^2P(z)d <= -tau.

The cube plus F>=0 is exactly E by the principal-minor PSD criterion. All coefficients are rational. Real-closed-field quantifier elimination is a finite exact decision algorithm for this test. Equivalently any independently rigorous successful compact interval/positivity certificate is acceptable; failure to find one is not evidence of invalidity. The existence theorem here uses the finite exact decision algorithm, not an assumed available efficient SOS solver.

**Boundary test.** The torus map Z(x,y)=(cos x,cos y,cos(x+y)) covers Sigma. A uniform N by N phase grid has boundary-image covering radius<10/N. A rational upper gradient bound G_P on the coefficient cube is computable from polynomial coefficients, for example G_P=sum_alpha |c_alpha|*|alpha|. At every grid image, evaluate P-f with certified error bounds. Accept only if every lower enclosure exceeds

 sigma+(G_P+L)*10/N.

Then P>=f+sigma on the WHOLE actual boundary. Cosines are evaluated with certified intervals, and the evaluation oracle for f includes its prescribed numerical error. Every strict majorant from Section2 passes such a boundary test at some finite N and precision.

The tuple enumeration is dovetailed, so a polynomial with no strict boundary gap does not block others. Keep the smallest P(0) among actually accepted certificates. The resulting verified upper values tend down to V_f(0).

## 4. Dovetail with genuinely paid lower laws

The nested dyadic-helper/Brownian-macro construction in NESTED_HELPERS_AND_UNIVERSAL_PAID_ORACLE.md provides finite complete paid families with optima increasing to V_f(0). Its deterministic Cesaro walk-on-spheres integration gives certified Brownian reward intervals. Exact rational occupation LP optimization, or an exact feasible policy with certified objective, supplies lower bounds whose running maximum tends up to V_f(0). A finite optimal LP can be solved by exact enumeration of rational basic feasible solutions if necessary; efficiency is not assumed.

Run these lower searches and the strict-polynomial upper enumeration together. Stop only when an actually verified upper B and an actually certified paid lower A satisfy B-A<epsilon. Both sequences converge to the same number by Sections1-3 and the paid-family density theorem, so this condition is reached in finite time for EVERY epsilon>0.

The returned Brownian macro is the true physical exit law. Finite sphere quadrature computes its reward only; it is not silently substituted as a paid law. Likewise the upper polynomial is actually checked before it enters B. The global guarantee comes from these two receiving interfaces, not from finite-control stagnation.

## 5. Limitations and next scientific use

This supplies a global positive-accuracy reward oracle in principle. It gives no finite decision at epsilon=0, no membership certificate for mu from a long run with no separator, and no general complexity estimate. No relation to a Hellinger update is asserted until the chosen reward is proved to approximate the required density-ratio gradient with appropriate error controls.

An actual strict inequality integral f dmu>B for a VERIFIED majorant would be a true source-separating gap; the previously audited smooth/global2x2 extension and periodic-gradient receiving theorem would then apply. Conversely an actual paid law beating a proposed witness is a constructive primal response. Neither conclusion may be inferred merely from the oracle's abstract existence. A concrete nontrivial global majorant and paid response for the new-helper tent reward are recorded separately.
