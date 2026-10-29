# Receiving review: prepared correlations and a fresh force response

Existing record-geometry role. Actual reviewed root source:
`../PREPARED_CORRELATIONS_AND_CAUSAL_RESPONSE.md`.

SHA-256: `4d7a596bcbecb717ff7b33c5b1fd35449aa166584603d9b0cf4c9017f24a5974`.

Exact snapshot: `PREPARED_CORRELATIONS_AND_CAUSAL_RESPONSE_REVIEWED_4d7a596bcbec.md`.

The companion two-ring file was read to reconstruct the target, at SHA-256
`42b5d5537a2f357a05a8b1ff55d292414e23c84d50d99bf50d3527073afc3ce2`.
This review does not replace the physical-mechanism role's independent review of that full application.

## Disposition

**The finite-range response estimate and the two-ring step-response consequence are correct at the fixed physical carrier geometry.** No correction to the factorial estimate or the target current is needed. The phrase “for any architecture obeying (1), the distance is order N” needs its intended geometric quantifier made explicit: all architecture links have uniformly bounded physical range on the same ring/ladder carrier, and the source/output gains are uniformly bounded in N. Bounded degree on an arbitrary newly chosen graph does not itself imply that distance. The source's final paragraph already recognizes changed carrier geometry as an alternative resource.

The result concerns startup response to a fresh input and does not prove a frequency-domain minimax bound. I retain that restriction.

## 1. The input and output supports must include the actual ports

For an input supported on a physical set S, let `S_plus` contain the state coordinates in the support of `G P_S`. For an output on T, let `T_plus` contain the state coordinates in the support of `H* P_T`. The relevant d is the graph distance between these expanded supports, with every actual controller link included. This is the literal interpretation of the root text's instruction to absorb the fixed support radii of G and H.

The direct map also needs `P_T D_0 P_S=0`. Its supplied locality ensures this for the separated quarter-ring intervals at sufficiently large N. A local source force accompanied by an uncounted remote feedthrough is outside the stated class.

Use a fixed physical norm in which `||M||<=Lambda`, and uniform bounds on `||G||` and `||H||`. These are the coefficients and port gains that enter the estimate. Large gain hidden in a size-dependent change of state units cannot be omitted from G or H.

For positive separation, take `n=ceil(d/R)>=1`. A product of j range-R matrices can connect at most distance jR. Thus the asserted vanishing for j<n is correct, including the equality case when d/R is an integer. The projections in equation (2) act on the expanded state supports, rather than on an input index and an output index of unrelated spaces.

## 2. The factorial and Duhamel bounds are valid

The norm-convergent exponential series gives

\[
\|P_{T_+}e^{tM}P_{S_+}\|
\le\sum_{j=n}^{\infty}\frac{(\Lambda t)^j}{j!}.
\]

For `Lambda t<=n/2`, successive terms from j=n onward have ratio at most
`n/[2(n+1)]<1/2`. The series is at most twice its first term. The elementary inequality `n!>=(n/e)^n` then gives exactly equation (3). The operator norm already bounds the sum of all routes; there is no missing multiplicity or volume factor.

Let the two force alternatives be zero and `f_0 1_(t>=0)`, with the same initial mean and additive-bath mean law. Their mean difference obeys

\[
\Delta\mathbb E v_T(t)
=P_T H\int_0^t e^{(t-u)M}Gf_0\,du.
\]

The direct term vanishes at T. Integration of the exponential-tail bound actually gives the slightly stronger estimate

\[
\|\Delta\mathbb E v_T(t)\|
\le \frac{2\|H\|\|G\|}{n+1}
t\left(\frac{e\Lambda t}{n}\right)^n\|f_0\|.
\]

Dropping `1/(n+1)` gives the printed equation (4). Nothing requires normality, diagonalizability, dissipation, a spectral gap, reversibility, or a Gaussian bath. The global bounded-generator assumption is the actual ingredient.

The displayed expectations presume their first moments exist. Equivalently, with an unchanged complete joint preparation/future-bath law, the deterministic difference may be defined under a common-source coupling even before a moment is taken. This is a mathematical comparison, not physical copying. The stated result only needs the mean response; it does not infer independence of complete output laws from prepared correlations.

Arbitrary initial covariance, including long-range covariance and nonzero prepared means, cancels from the response difference. A controller could be preprogrammed to emit a particular absolute current at a known time, but that output occurs under both force alternatives. It cannot replace the response difference required here. If the input choice is correlated with a preparation record, the conditional initial experiment changes; the source correctly excludes that substitution and requires retaining the record.

## 3. Reconstruction of the ideal step response

Take N divisible by four for the exact printed fractions, and let S contain N/4 consecutive bonds on ring 1. Let the actual newly selected step be one on S and zero elsewhere. The mathematical ideal is the overdamped native law with the global constraint that the two spatially averaged currents agree. Its constraint force is a scalar multiplier of the signed harmonic direction.

Writing the multiplier as ell(t), the mean native equations may be written

\[
r_1j_1=-B_N^*x_1+f_1+\ell\,1_N,
\qquad
r_2j_2=-B_N^*x_2-\ell\,1_N.
\]

Spatial averaging and `average j_1=average j_2=I` give

\[
r_1 I=\tfrac14+\ell,
\qquad r_2 I=-\ell,
\qquad I=\frac1{4(r_1+r_2)}=c_0.
\]

On ring 2, `j_2=-(1/r_2)B_N^*x_2+c_0 1_N`, so its density obeys the homogeneous heat equation. With zero initial density mean, it stays zero. Therefore `j_(2,i)(t)=c_0` for every bond and every t>0. The nonuniform density response induced on ring 1 does not change this conclusion, because a periodic gradient has zero spatial average.

For quarter-ring T, the output norm is `c_0 sqrt(N/4)` and the source norm is `sqrt(N/4)`, exactly as stated. If N is not divisible by four, take a block of `floor(N/4)` bonds; the corresponding constant is `floor(N/4)/[N(r_1+r_2)]` and tends to c_0. The exact-quarter subsequence already proves the claimed order of the obstruction.

The ideal in this comparison is an instantaneous constrained overdamped law. The proof does not assert that the positive finite-inertia wave apparatus has that microscopic startup response. In particular, evaluating at a time proportional to N removes any suggestion that the obstruction is only the ordinary order-one native inertial startup.

## 4. Geometry is a resource premise, not a consequence of bounded degree

On the fixed ring/ladder carrier, choose T on ring 2 opposite S. Every controller link must have uniformly bounded range in this physical cyclic coordinate. After the O(1) source/output support enlargement, their separation is at least `c N-O(1)`. Thus n is of order N.

For `t<=n/(4e Lambda)`, equation (4), divided by the source norm, is at most

\[
2\|H\|\|G\|t\,4^{-n}=O(N4^{-n}).
\]

Consequently the error relative to the ideal response norm is at least

\[
1-\frac{2\|H\|\|G\|t}{c_0}\,4^{-n},
\]

which tends to one. This is the explicit startup-response lower bound. It also holds uniformly on the indicated early time interval.

On an arbitrary bounded-degree graph, the separate statement `d=Theta(N)` is false. For example, adding a matching between opposite ring-1 and ring-2 positions keeps degree bounded while bringing the selected source and receiver a bounded graph distance apart. Such a matching is a long physical link on the original carrier. It is excluded by a fixed physical-range premise, or must be charged as a changed carrier geometry. It is not excluded by bounded degree alone.

The proof of (2)-(4) is valid on either graph, using its actual d. Only the order-N specialization needs the fixed-geometry sentence. The root text already lists remote actuation, nonlocal native coupling, faster coefficients, and changed geometry as alternative resources; the receiving qualification makes that list part of the theorem's quantifiers.

The positive signed-ladder model fits this comparison class: its incidence maps have bounded range and norm, the native resistance and inertia are uniformly bounded as stipulated, and its local source and output maps have size-independent norm. Its weak tap does not introduce a faster coefficient. A controller with additional nonlocal native memory is not covered merely because its visible marginal dynamics looks local.

## 5. What the bound does and does not establish

The result separates a supplied covariance from the response to an independent new force. It proves an early-time suppression with a small analytic tail, not a hard light cone. The forcing test is causal and has broad frequency support. It therefore does not prove an optimal bandwidth-versus-error relation, a universal frequency-domain lower bound, or optimality of the selected wave architecture. The root text makes precisely these exclusions.

A narrow frequency band can require a different input class and a different comparison norm. Prepared correlations can be important for fluctuations, sampling, and initial records even though they disappear from this linear mean-response calculation. Neither observation weakens the proved step-response resource distinction.

The credited primary predecessor is appropriate. I read Raz and Sims, *Lieb-Robinson bounds for classical anharmonic lattice systems*, [arXiv:0902.0025](https://arxiv.org/pdf/0902.0025), especially the introduction and Theorem 1: it establishes volume- and initial-condition-independent locality estimates for classical harmonic oscillators and suitable extensions. The present finite-matrix tail is proved directly rather than imported through a nonlinear theorem. No priority claim for propagation bounds is warranted or made.

## Receiving status

Accepted at the fixed ring/ladder carrier, uniform bounded-port interface, with finite means where means are printed. The only requested root clarification is the explicit geometry/gain quantifier. No extra numerical test is needed. Original bytes and this actual review are preserved separately; no root file has been edited by this reviewer.

## Actual clarification receipt

I subsequently read `../CAUSAL_RESPONSE_INTERFACE_CLARIFICATION.md`, SHA-256
`1d43dfd576af8a898b5405f4401ce2789f6ed5a6203a96de9c3634a16c040052`.
Its exact snapshot is `CAUSAL_RESPONSE_INTERFACE_CLARIFICATION_REVIEWED_1d43dfd576af.md`.

The addendum explicitly fixes the physical ring/ladder metric, uniformly bounded physical link range and port gains, includes every permitted controller link in the actual distance, and distinguishes the response difference from a preprogrammed absolute output. It also retains the startup-step scope and declines a frequency-domain minimax claim. **Accepted: the original proof together with this exact addendum closes the requested interface clarification.** No further mathematical correction or numerical check is required.
