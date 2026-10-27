# Internal audit of the finite joint-budget global optimum

27 October 2026. Decision: **PASS at the exact declared mathematical scope.** No substantive gap or counterexample was found in JOINT_PROOF.md, the exact nested-root construction, the five-root all-frequency certificate, the positive-star realization, or the graph-wide dual comparison. This is a concrete finite joint-budget optimum, beyond the earlier strict-improvement result. It does not solve the arbitrary-resource joint-budget family.

This is an exposed internal mathematical audit: the helper authored the general Descartes lemma and earlier compliance root proof, then independently reconstructed the new joint construction and its equations. It is not a blind comparison, external audit, historical novelty clearance, fabrication validation or practical-device evidence.

## Preserved source and rerun

The reviewed files were copied unchanged into the helper-owned `joint_audit/` directory before execution, preserving the local import of certify.py. Hashes are:

* JOINT_PROOF.md: 9853f57d536b20b4de670c1a6f07f66ef93b2ab0accf8684a2691dd7ca276be7
* joint_certify.py: 38382286092f9ad0178408bf025522c40d3dbba6f7f84fe47747d1ae11b263fa
* certify.py: b40b5ec048c673d7fb60bdb1c4b50695d9104c1e28e01f0ce71290bc2ff20dca

The owned copy of joint_certify.py executed successfully, with every assertion passing. It generated `joint_audit/JOINT_CERTIFICATE.md`, SHA256 8f151013d3305cfbf077bb894a6aedf6794067c0e4363931614f83cc40e51802. The underlying dyadic arithmetic and full Bose-tail enclosures were already inspected substantively in AUDIT.md and rerun for this certificate.

## 1. Exact resource algebra and graph-wide cap

I reconstructed the endpoint product, trace and inverse endpoint sum. With A=4-delta, B=2H/(H+delta), and the displayed t,

A+delta=4,
B(H+delta)/H=2,
1/B+(A-B)/(Bt)-delta/[H(H+delta)]=21/40.

Thus the original physical backbone/total masses are exactly one/two and the original CM compliance is exactly 1/20. These are identities in the exact parameters, not approximate numerical checks. The candidate's q(z) has leading coefficient one and constant numerator d=Bt(H+delta)/4=tH/2. Consequently its reciprocal has backbone mass one and total mass tH/d=2. The displayed residue formulas are the correct partial-fraction formulas and their positivity is enclosed over the complete root box.

For every graph, frozen F gives kappa_inc=(E-16)/8. Since all internal edges have positive stiffness, kappa_inc<=kappa_total<=1001/50, yielding E<=4404/25. The candidate is a star, so its total and incident sums coincide. Therefore the spectral E relaxation is tight for the exact candidate; no uncharged nonincident spring is required for realization.

## 2. Existence of the kappa-exact branch

The code's kprime and hprime are the correct partial derivatives of the rational kappa(delta,H). I independently simplified the formulas as a cross-check. Write

G=2H+4delta-delta H-delta²,
D=H²-19H delta-20delta²+40delta.

Then

t=20(H+delta)G/D,
kappa=t(4-delta-B)/4+delta(H-4+delta)/4.

Differentiating these expressions independently and enclosing them on the entire broad box delta in [0.00577,0.00578], H in [73.33846366923165,73.33846366923166], gives

kappa_delta in [3.469987822257281386019773,
                3.470173732144808523090216],
kappa_H in [0.000969175668561602976180,
            0.000979656040246269741538].

Both are strictly positive, independently corroborating the parent's derivative functions. The rational denominator remains away from zero there.

The uniform lower/upper-delta boundary signs therefore guarantee exactly one kappa=1001/50 root in the broad delta interval for each H in the whole bracket. The implicit function theorem makes delta(H) differentiable; delta'(H)=-kappa_H/kappa_delta<0. Exact rational bisection at the two H endpoints encloses their roots, and monotonicity makes those endpoint enclosures a valid uniform branch enclosure. The 220 bisection steps use exact Fraction comparisons, not floating signs.

## 3. Fifth endpoint equation and exact object

The four-edge divided differences are the coefficients of the negative cubic interpolant of w³g(w) in w². Expanding Newton's interpolation formula yields exactly the implemented b,a,lambda,nu expressions, including all signs. The endpoint distinctness and positive denominators are enclosed on the whole parameter box, so the fit and fifth residual are continuous along the exact kappa branch.

The owned rerun encloses the fifth-edge residual strictly negatively at the lower H endpoint and strictly positively at the upper H endpoint, despite their small magnitude. All interval widths are propagated outward at 256 binary fractional bits. IVT therefore gives an exact interior Hhat and deltahat=delta(Hhat), with both budgets exact and all five dual roots exact. It is correct to define the design by these equations and isolating brackets; representative decimal masses alone would not enforce an exactly binding cap.

## 4. Complete five-root sign certificate

I reconstructed the entire function

Q(w)=w³+nu sinh²(w)/w²+lambda sinh²(w)
      +a w²sinh²(w)+b w⁴sinh²(w).

Its even coefficient is exactly

q_n=nu d_(n+1)+lambda d_n+a d_(n-1)+b d_(n-2),

with d_j=2^(2j-1)/(2j)! for j>=1 and zero for j<=0. The code encloses every nonzero coefficient through n=17 on the complete root box, with signs

(- through n=5), (+ for n=6..8), (- for n=9..12), (+ for n=13..17).

The odd cubic coefficient is positive and lies between q_1 w² and q_2 w⁴. It inserts two additional sign changes into the even sequence, for exactly five changes in total.

The normalized coefficient formula for n>=18 is also correct:

q_n/d_(n-2)=b+4a/U_n+16lambda/V_n+64nu/Z_n.

The interval coefficient signs are nu<0, lambda>0, a<0, b>0. The displayed strictly positive lower bound drops only the positive lambda term. Increasing n increases U_n and Z_n, so the two retained negative terms become less negative. This certifies the complete infinite tail, not merely a finite truncation. There is no remaining high-frequency range or series coefficient whose sign is assumed.

The self-contained analytic Descartes lemma therefore gives at most five positive roots counting multiplicities. The five distinct exact endpoints exhaust the bound, so every root is simple and no other positive root exists. Negative sign near zero follows from nu<0; positive sign at infinity follows from b>0. Alternation proves that the strict negative set is precisely the three candidate pass bands.

This is a rigorous point-specific sign certificate. It does not depend on, or assert, a universal five-root theorem for all joint resource vectors.

## 5. Global optimum and uniqueness

For an arbitrary admitted finite graph, the complete indicator satisfies 0<=chi<=1. The established negative set gives

I=integral R(chi-chi*)>=0.

Trace and logarithmic moments cancel exactly. The constraints give DeltaW>=0 and DeltaE<=0 because the candidate saturates both bounds. Consequently

J-J*=I-nu DeltaW-(b/4)DeltaE>=0.

The coefficient b/4 is correct because E=integral 4w³ chi. All difference integrals converge as in the earlier proof. No assumption that a general relaxed indicator is physically realizable enters the lower bound, and the candidate's positive star supplies actual attainment.

Equality forces I=0 and therefore chi=chi* almost everywhere, since R is nonzero except at five isolated frequencies. Thus the active spectrum/response is unique. The high band's start and width uniquely recover H and delta, proving uniqueness of the nested root within the isolating box. This need not imply unique physical topology in the presence of isospectral or dark-mode representations, as the parent correctly states.

## 6. Numerical scope and remaining obligations

The successful exact rerun certifies positive finite masses/springs, both exact budgets at the IVT-defined object, every pass band, all-frequency root signs, and a strictly smaller full Bose integral than the strongest legal one-pendant k=20. The gain is enclosed between 1.88249677872143150e-7 and 1.88249691405121882e-7 in the declared J normalization. The candidate's spring sum is exactly 20.02 at the root; its enclosing-box spring interval straddles that value because the box includes parameters off the kappa-exact branch. The proof handles this distinction correctly.

The two-branch construction globally attains the optimum at this one exact joint-budget point. A single active pendant cannot match its strictly smaller objective, so two active side resonances are necessary for improvement and sufficient here. The earlier unbounded-stiffness escape mechanism is excluded at this point by an actual finite optimum, not merely by choosing one finite approximation.

The full arbitrary-resource joint frontier, numerical conditioning/manufacturing tolerance near a binding resource boundary, small-mass connector costs, individual displacement/strain, vector elasticity, finite contacts, anharmonicity, fabrication, historical priority and measured device benefit remain unestablished. Those limits are material and are retained in the parent's proof.
