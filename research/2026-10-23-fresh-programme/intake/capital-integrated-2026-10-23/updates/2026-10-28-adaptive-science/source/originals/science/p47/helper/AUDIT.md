# Internal mathematical audit of the parent's construction

27 October 2026. Decision: **PASS at the stated scalar harmonic ballistic scope.** No substantive gap or counterexample was found in the general optimum/infimum theorem, its positive approximation sequence, or the supplied numerical certificates.

This is an exposed internal audit: the helper authored the all-frequency root lemma before reviewing the parent's construction. I independently reconstructed the parent's compactness, KKT, dual comparison, high-band trace-fill algebra and finite-star formulas. This is not a blind comparison, external acceptance, historical novelty clearance, a physical-device audit or a practical-advantage claim.

## Examined artifacts

The preserved audit snapshot is `audited_parent_PROOF.md` (copied from the authorised parent's PROOF.md), SHA256

bc20a3144eece9bbdbc45aef8ed2b7adf361595a0dfc600a10b2b6e4709a9abc.

The certificate source was copied unchanged into the helper-owned `audit_certify.py`, SHA256

c9f7e371dff7d8844e728ad4df002a459336ec3c6dede292568cef98059e9c71.

The copied script was executed only in the helper's directory, where its generated `CERTIFICATE.md` records a successful rerun of every assertion. The parent source and active checkout were not executed or modified by this audit.

## 1. Compactness and existence

The interior below-rigid feasible point exists for every positive cap: hold A=A0 and choose sufficiently large finite r. The supplied asymptotic strict saving is algebraic in r^-2; the compensating optical heat is exponentially small. The cap is then satisfied because (A0-B)/r² tends to zero.

I checked each possible degeneration of the feasible two-band family. If r tends to zero, feasibility gives A-B<=dmax r² and hence A tends to B; since p<=r, both p,r tend to zero and s tends to sqrt(B), so the full objective tends to the rigid value. If r tends to infinity, uniformly in B<=A<=A0,

p²=B/[1+(s²-r²)/r²] tends to B,
0<=s-r<=(A0)/(2r),

so the acoustic contribution tends to the rigid value and the optical contribution tends to zero. If A tends to B while r remains in a positive compact interval, the endpoint formulas are continuous even at the discriminant-zero point r=sqrt(B). At A=B the occupied intervals merge or the upper one cancels, leaving exactly the rigid interval. A strictly below-rigid sublevel therefore avoids every excluded boundary and is compact. Its continuous objective attains a genuine two-band minimum with A>B and r>0.

## 2. KKT multipliers and the nu=0 corner

The interpolation matrix for lambda,a,nu is nonsingular: after multiplication of the endpoint equations by w³ it has columns w²,w⁴,1 at three distinct positive squared endpoints. The endpoint variation identity is exactly

dj+(a/2)dA+nu dW=0,

because dL=0 and R vanishes at every moving endpoint.

For the inequalities A-A0<=0 and Wmin-W<=0, standard minimization KKT conditions read

dj+eta dA-zeta dW=0, eta,zeta>=0.

Thus eta=a/2 and zeta=-nu, giving precisely a>=0 and nu<=0. The constraint qualification is satisfied: partial W/partial r=(A-B)/(B r³)>0, so the A and W gradients are linearly independent wherever both constraints bind. Complementary slackness yields the stated products. There is no overlooked A=B or r=0 constraint at the attained sublevel minimum.

When nu<0, the helper root lemma applies for a>0 with any lambda. At a=0, lambda<=0 would leave at most two coefficient sign changes in the entire Q series, contradicting the three prescribed positive roots. Hence lambda>0. When nu=0, multiplication by w reduces the dual exactly to frozen F's two-moment form w g+lambda+a w². F's root argument forces lambda<0<a and supplies the same global occupied-band sign. Thus the uncharged-compliance corner and a=nu=0 exclusion are handled correctly.

## 3. Global dual comparison and uniqueness

The compliance normalization agrees with frozen C/A:

W=-ms² C_CM/(2M)=-d/(2B).

The pointwise inequality I=integral R(chi-chi*)>=0 is valid because 0<=chi<=1 and chi* occupies exactly the strict negative set of R. The apparent inverse powers cause no divergence in the difference: every finite connected spectrum equals one on a nonzero acoustic interval at zero and has finite upper support.

The comparison

J-j*=I-(a/2)(T-A*)-nu(W-W*)

has the correct signs after complementary slackness, both when the trace cap is active and when a=0, and both when the compliance cap is active and when nu=0. Equality forces I=0 and therefore equality of indicators almost everywhere; the three isolated roots do not create a further equality class. Strict two-band spectra with this common indicator have the same p,r,s, and hence the same A,r. If A*<A0, an original finite network cannot attain equality because its exact trace is A0. Dark modes cannot hide the missing trace: the active determinant ratio still has the exact rank-one trace S/m from frozen F.

## 4. Positive high-band fill sequence

I independently solved the three moment equations. Appending the squared high band [H,H+delta] adds trace delta, multiplies the endpoint product by (H+delta)/H, and changes the inverse endpoint sum by -delta/[H(H+delta)]. Consequently the parent's definitions

B_H=B H/(H+delta),
t_H=(A*-B_H)/{B_H[Q-1/B_H+delta/(H(H+delta))]}

are exactly correct. Their denominator tends to d*>0 and t_H tends to r*². For large H, A*>B_H>0 and the low endpoints remain bounded while the high band moves upward, so the strict interlacing needed by the positive inverse theorem holds. Trace, logarithmic product and inverse endpoint sum are all exact, giving the original backbone mass, total mass and legal physical compliance. This is a positive finite two-branch star, rather than an assumed realizability oracle.

The full objective converges to j*: low endpoint continuity handles the first two bands and the high contribution is bounded by its width times g(sqrt(H)). Its spring cost is correctly charged: E=2H delta+O(1), giving total star spring sum S delta H/A0²+O(1). Thus the missing compactness is genuinely purchased by diverging stiffness. For A*<A0 the best legal pendant has an attained minimum strictly above j*, so members of the convergent finite sequence eventually beat it. This justifies the theorem's finite strict-improvement consequence.

## 5. Certificate arithmetic and special cases

I inspected and reran the entire copied certificate. The following components were reconstructed rather than inferred from a PASS label:

* Dyadic addition, multiplication, reciprocal and square root operations round outward. The reciprocal formula works for both positive and negative intervals; zero is excluded explicitly. Integer square roots supply valid lower and upper bounds.
* The positive exponential series lower bound is its finite partial sum. The first omitted term times 1/[1-x/(N+2)] bounds the positive tail because all later term ratios are smaller; the code verifies that denominator is positive.
* The Machin formula's atan sums use an even truncation length. Their partial sums are lower bounds and the next positive term bounds the alternating remainder. Interval subtraction propagates the signs correctly.
* For theta=1/2, the full Bose tail is exactly sum_(n>=1) exp(-2nx)(2x²+2x/n+1/n²). The omitted coefficients decrease with n, so the implemented positive geometric bound encloses every omitted term. Acoustic integrals use the enclosed full integral pi²/6; no high-frequency band is omitted.
* The three-endpoint divided differences produce the coefficients of the negative interpolant of w³g(w) in w², with the displayed signs lambda,a,nu.
* The severe-cap a=0 sign bracket uses exact interval signs at the two rational endpoints and encloses lambda>0,nu<0,A<4 across the whole bracket. Continuity and IVT therefore give an exact certified dual root; uniqueness follows from the analytic global certificate, not a presumed optimizer's behavior.
* The finite example's response expands as q(z)=(z²+c z+d)/[z(z+t)(z+H)]. Its reciprocal has branch poles sigma_1,2 and residues rho_1,2 exactly as stated. The certificate proves both residues positive, and the exact identity tH/d=2 gives total side mass one. The exact endpoint sum identity yields C_CM=1/20.

All numerical assertions passed, including the target dual signs, the severe-cap limiting certificate, strict positive finite branch parts, exact resource equalities, all-band finite objective and its strict improvement over the optimized legal pendant. The preserved output contains the enclosures; the parent additionally owns independent matrix reconstruction.

## Scope and remaining obligations

The audit establishes the declared mathematical construction and its certified instances, conditional on the supplied scalar rank-one model and frozen F/C/A spectral identities. Those foundations were read at their full governing scope; this audit did not repeat every earlier inverse-network review from scratch. The all-frequency lemma was authored by this helper, so its integration audit is exposed.

No theorem for a joint internal-spring cap has been established here. The diverging-stiffness sequence and the finite example's roughly 69.65 spring sum make that a substantive next resource question. Physical CM compliance remains an aggregate static response; individual displacement, connector mass, strain, finite modulus, contacts, vector modes, anharmonicity, fabrication, historical priority and measured advantage remain outside this PASS.
