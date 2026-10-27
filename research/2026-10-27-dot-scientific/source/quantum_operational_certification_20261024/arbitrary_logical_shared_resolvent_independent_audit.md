# Independent audit: arbitrary logical success state, shared-resolvent value proof

**PASS**, 2026-10-26. Governing manuscript: `arbitrary_logical_success_reset_flag_value_theorem.md`, Sections 1–7. Independently checked the parent's candidate for

E(rho)=p V(rho tensor sigma)V*+q Tr(rho)P_f,

where sigma is an arbitrary finite-dimensional logical density, not necessarily flat. This is not an extension by the false unequal-weight Schmidt concavity argument.

## 1. Actual three determinant ratios

Assume p,q>0, diagonalize sigma, and restrict to its positive support (zero logical eigenvalues contribute no success output). Let G have the inside-flag coefficient columns g_j in physical/reference-qutrit coordinates; sum_j ||g_j||^2<=1. Set b=q/p and

K(t)=G diag(sigma_j/(t+sigma_j)) G*, T=TrK, z=t/b.

Compare with an orthogonal reset flag in a fixed padded output of the same dimension. The baseline deficit is exactly zero: the reversible sigma encoder has zero deficit by cancellation of its logical entropy, reset has zero deficit, and orthogonal reference blocks add homogeneously.

For the input, the success eigenvalues are p sigma_j on maximally entangled code vectors. Compressing their resolvent correction to the three-dimensional flag subspace gives conjugate(K)/3, not K itself in an arbitrary complex frame. Its determinant is the same as K's. The matrix determinant lemma, relative to the orthogonal-flag baseline, gives det(I-beta K) after s=pt, where beta=1/[3(3z+1)].

For the reference, the success eigenvalues are p sigma_j/3, each threefold. The rank-one flag determinant ratio after s=pt/3 is 1-gamma T, with gamma=3/(z+3).

For the unscaled output, the success eigenvalues are 2p sigma_j/3 on each antisymmetric block; the reset flag has weight 2q/3. The actual compressed antisymmetric projector sum is (TI-K)/2. After s=2pt/3 its determinant ratio is det(I-alpha(TI-K)), alpha=1/[2(z+1)]. This retains the output factor two and the correct complex orientation.

At equal traces, f(X)-f(Y) is minus the integral of the corresponding log-determinant ratio. Combining the input/reference/output signs and Jacobians therefore gives EXACTLY

Delta=(p/3) integral_0^infinity F(K(t),t/b) dt,
F=2 sum_i log(1-alpha(T-k_i))-3 sum_i log(1-beta k_i)-log(1-gamma T).

The plus output log sign and all coefficients 2,-3,-1 are correct.

## 2. Convergence and positive series remainder

For t>0, 0<=T(t)<=1/(1+t)<1 since sigma_j<=1 and the projected flag has norm <=1. All logarithm arguments are strictly positive. At t down to zero, the only potentially singular logarithm is the reference term, bounded in magnitude by log(1+1/t); this is integrable. At infinity, K=O(1/t) while alpha,beta,gamma=O(1/t), so every displayed logarithm is O(1/t^2). The exact entropy/log-determinant integral is therefore received even when the original reference rank drops at full flag overlap.

Expanding at each t>0, the linear term is h(z)T, with

h(z)=gamma+3beta-4alpha=4z(z-1)/[(z+3)(3z+1)(z+1)].

For n>=2, the coefficient times n is

gamma^n T^n+3 beta^n sum_i k_i^n-2 alpha^n sum_i(T-k_i)^n.

Since each T-k_i<=T and their sum is 2T, sum_i(T-k_i)^n<=2T^n. Also gamma>=2alpha for z>=0. Therefore the coefficient is nonnegative: gamma^n T^n-4alpha^n T^n>=0 for n>=2, with the additional positive beta term retained. Thus R=F-hT>=0 pointwise. This does NOT assert F>=0 pointwise. The convergent pointwise series is sufficient; no unjustified exchange of conditionally signed terms is needed. Both F and hT are integrable, so R is integrable as well.

## 3. The signed linear integral is nonnegative, strictly so on supported overlap

The finite signed measure dmu(t)=h(t/b)dt/t is negative on (0,b), positive on (b,infinity), and has total mass zero. Explicitly

h(z)/z=2/(z+1)-1/(z+3)-1/(z+1/3),

whose combined logarithmic antiderivative has equal zero limits at zero and infinity. The measure is absolutely integrable; its partial-fraction terms are not integrated separately as divergent integrals.

For every sigma_j>0, m_j(t)=t sigma_j/(t+sigma_j) is bounded and strictly increasing. Therefore

integral h(t/b) sigma_j/(t+sigma_j) dt
=integral [m_j(t)-m_j(b)] dmu(t)>0.

The integrand on the right is nonnegative on both sign regions and positive on sets of positive measure. Expanding T as sum_j ||g_j||^2 sigma_j/(t+sigma_j) proves integral hT>=0, strictly positive if any supported flag column is nonzero. Combining with R>=0 proves the whole class nonnegative and strict whenever p,q>0 and the flag overlaps the ACTUAL positive success support.

At p=0 or q=0 the channel is exactly reset or a reversible encoder. If the flag has zero overlap on sigma's support, it is an orthogonally heralded generalized-erasure channel and Delta=0. A component in an unused zero-eigenvalue logical direction must count as outside the success support, not as a strict-overlap case. These are the complete equality cases furnished by this argument.

## Scope and reproducibility

This proof covers arbitrary finite logical sigma for the reversible-success-plus-reset family. The value portion does not prove arbitrary two-Kraus/shared-reset positivity or unrestricted WH3. Its quantitative operational completion is independently received below. It uses actual common-resolvent matrices, not hidden access to logical labels, false pointwise F positivity, or unequal-weight Schmidt concavity.

`arbitrary_logical_shared_resolvent_independent_check.py` compared the exact physical Choi deficit with the proposed integral for 24 complex sources, logical ranks 1,2,3,5, including spectrum [.999,.001] and full supported flag overlap. All pass, with maximum entropy-integral discrepancy 8.7e-14. The remainder and integrated linear contribution were checked as corroboration; the sign proof above is analytic.

## Quantitative follow-on: independently received filtered-flag construction

The parent's further quantitative construction also **PASSES**, and its saved governing Sections 6–7 have now been read and received. It proves a dimension-independent same-p/sigma generalized-erasure approximation; no conditioning or logical-rank hypothesis is introduced.

For one positive logical eigenvalue sigma set x=sigma/b. Subtracting the signed measure's zero mean gives the exact linear integral

L(sigma,b)=b x^2/(1+x) integral_0^infinity 4(z-1)^2/[(z+3)(3z+1)(z+1)(z+x)] dz.

On z in [2,3], the numerator is >=4, the first three denominator factors multiply to <=240, and z+x<=3(1+x). Hence L>=b x^2/[180(1+x)^2]. Define r_j=p sigma_j/(q+p sigma_j) and e^2=sum_j ||g_j||^2 r_j^2. The exact integral proof therefore gives Delta>=q e^2/540, since the nonlinear remainder is nonnegative.

Form the actual reference vector h=f_out+sum_j [q/(q+p sigma_j)]g_j tensor |j>. Its distance from the unit flag f is exactly e. If ||h||<1/2, then e>1/2; simply move the flag outside the original success code. This costs <=2q<=4qe and preserves p,sigma.

If ||h||>=1/2, normalize it to h_hat. The reset projector change costs <=2qe: the distance from f to span(h) is no greater than ||f-h||=e. Rotate the success isometry away from h_hat by polar projection, completing the sole deficient direction in a fixed outside coordinate if necessary. The change D=V-W has rank one, D=|d><u| with u a unit domain vector, and ||d||^2<=2theta_h. The resulting W is an isometry and h_hat is an orthogonal failure flag, so the final comparison is a genuine generalized-erasure channel with unchanged p and sigma.

The key rank-uniform norm bound uses the ACTUAL input dimension three. For a pure qutrit input with a three-dimensional ancilla, let X=P_psi tensor sigma. The operator (I_anc tensor D)X has rank at most three. Its Hilbert-Schmidt squared norm is

||d||^2 <u|(rho_phys tensor sigma^2)|u>
<=2theta_h <u|(I tensor sigma^2)|u>
=2 sum_j sigma_j^2 ||(V*h_hat)_j||^2.

Here rho_phys<=I and no logical ancilla is incorrectly treated as an accessible classical record. Trace norm is at most sqrt(3) times this Hilbert-Schmidt norm. Expanding the difference of the two isometric success maps gives twice that trace norm, with success weight p. The filtered coefficients satisfy

sum_j sigma_j^2 ||(V*h_hat)_j||^2=q^2 e^2/[p^2||h||^2].

Thus success-map diamond cost is <=2sqrt(6)qe/||h||<=4sqrt(6)qe. Adding reset cost gives <=(2+4sqrt(6))qe. The small-h case is also bounded by that constant. Since qe<=sqrt(540Delta) (q<=1), total distance is <275sqrt(Delta), and the proposed loose constant280 is safe. The universal distance two gives its cap. Zero p or q cases are exact and treated before division.

A fixed output padding to dimension 3 rank(sigma)+1 suffices after restricting sigma to its positive support. Flag components in unused zero-sigma directions are part of f_out. The theta_h=1 polar completion is therefore genuinely available, and all final maps are TP on the same padded output. The filter is a comparison construction, not a claimed physical attenuation of an unknown flag. Applying the FINAL code/flag instrument to the original channel receives the corresponding heralded error, with the usual explicit success-probability division for normalized successful states.

`arbitrary_logical_filtered_flag_independent_check.py` passed 48 complex cases of logical ranks1,2,4,7, including14 small-h cases and34 filtered-polar cases. It checked the exact filtering norm, isometry and orthogonal-flag properties, reset angle bound, and the changed ancilla operator rank (at most3). This corroborates the analytical rank argument; no sampled-state premise is used in the theorem.


## Final written capability receipt

Read the entire saved `arbitrary_logical_success_reset_flag_value_theorem.md`, Sections 1–7. **Whole value, exact-zero classification, and the actual same-p/sigma operational bound min(2,280sqrt(Delta)) all PASS.** There is no residual mathematical blocker.

The additional closed scalar resource in Section 5 also checks: J(x)=integral h(z)/(z+x) dz. Expanding h(z)/z into the three stated partial fractions and cancelling their common divergent logarithm gives exactly

3 log(x/3)/(x-3)+(1/3)log(3x)/(x-1/3)-2log(x)/(x-1).

The apparent singularities at x=1/3,1,3 are continuous divided differences, and strict positivity follows from the already-received signed-measure argument. The retained quadratic resource coefficient is correct: (p/3)*(3/2)=p/2. It is not double counted in the filtered-flag payment, which only uses the linear resource.

The governing quantitative proof uses the correct telescoping identity for D=W-V, the actual pure-input-plus-mixed-sigma state, and the rank-at-most-three changed operator. Its explicit rational constant check is valid: (2+4sqrt6)sqrt540<(59/5)(93/4)=5487/20<275<280. All support, normalization, polar-completion, and original-channel instrument conventions agree with this audit.

The final theorem is dimension- and spectrum-independent, including arbitrarily small positive logical eigenvalues; zero eigenvalues are removed before identifying the success support. The comparison is a generalized-erasure channel with the SAME p and SAME sigma. Fixed output padding to at least3rank(sigma)+1 supplies the sole possible missing orthogonal direction. The adaptive flag filter and proof path are comparison constructions, not claimed physical preprocessing. Applying the final code/flag decoder to the original channel is deterministic; normalized success error still requires p>zeta and is bounded statewise by2zeta/p. The existing flat two-mode lower bound establishes sharpness of the one-half exponent within this broader class.

The precise remaining frontier is nonreversible successful operations or input-dependent/nonscalar reset effects, including arbitrary K0,K1/shared-reset channels, and unrestricted WH3. The false unequal-weight Schmidt or sigma concavity routes remain false; this theorem bypasses them rather than repairing them.
