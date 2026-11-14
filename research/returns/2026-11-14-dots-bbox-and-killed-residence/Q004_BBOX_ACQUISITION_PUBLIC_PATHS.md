# Actual new-bbox energy acquisition and estimator interface

This explicitly changes membership and sector weights from the old area-cut proposal. It does NOT substitute the old accepted-edge law. Executed implementation below is a small complete native network; large-R weighted-walk backsampling is specified but not implemented here.

## 1. New proposal measure
Use H795, area cap floor(H²/4), perimeter threshold2H−4, and the same finite perimeter1900 magnetic-walk overcount, with the deterministic chosen rational tilt r_P at each P. For a word with signed area V, define its positive envelope
 b_gamma=exp(−8P+.04 Vp)*r_P^[2(V−Vp)], Vp=min(floor(H²/4),floor(P²/16)).
For every VALID contour of area≤Vp, exp(−8P+.04V)≤b_gamma by2log r_P≤.04. Invalid/self-intersecting words remain nonnegative proposal mass and are rejected.

Let a_1=exp(−15.96), a_j=1 for j2..8. Sample ordered rooted tuple with weight
 a_j*(3S/j!)*product_gamma(b_gamma/P_gamma), totalS≥2H−4,
normalized by its EXACT positive sum Q_bbox. The numerical upper certificate bounds this sum but is not itself an exact sampler. Acquire the exact sum/conditional probabilities to prescribed precision using positive convolution and weighted closed-walk DP, with root choice and backward walk sampling. All errors must be paid as below. The exponential weights may use interval-based lazy decisions.

Draw auxiliary y from the original model's acquired C_16 Gibbs sampler, leaving original source C_5 and kappa unchanged. Draw one of3S contour boundary marks. Decode the gate i. Reject unless all words describe disjoint valid filled domains, the new bbox area/span/topology requirements hold, x obtained by whole-domain flips belongs to M_H outside B, i is minus, its birth leaves M_H, and the tuple equals the actual affected old outermost domains. Among repeated boundary marks of this gate retain the first in this ordered rooted representation. Require a_1 only after verifying genuine j1 geometry; no approximate classification is allowed.

Accept with probability
 rate_i(x)/a_j * w(x)/(w(y)*product b_gamma).

The probability≤1: for j1 the new bbox lemma gives rate≤a1; for j≥2 rate≤1; whole-domain weight ratios are bounded by product b, including thermal interior bits.

There are j!*product P_gamma valid root/order representations of a physical edge. Their summed accepted probability is exactly
 g(x,x^i)/(Q_bbox*Z_aux).
Thus accepted edges have the actual NEW bbox trial's retained conductance-weighted law, not a shape distribution or the old area-cut law. This identity does not require that all configurations are four-corner droplets.

## 2. Full support via explicit omitted-energy error
Included: all short structural bbox exits with inverse image in C_16, including every merger and winding sector satisfying the exact validator. Excluded but bounded: inverse images outside C_16, perimeter tails, target overrides inside M_H, and original reservoir-to-target overlap.

The same bbox-preserving flip comparison gives
 u_16=6n*(4exp(−4.025))^32/(1−4exp(−4.025)).
Its log is approximately−67.81717. Missing inverse-image energy≤Q_bbox*Z_MH*u_16. Combined with Wupper/C lower ratio exp(19.511321), this is at most about exp(−48.30585) relative to C. Retain the archived complete perimeter tail, majority tilt and source-overlap bounds unchanged. These are much smaller at this tuple. For a conservative implementation one can allocate delta=10^−6, subject to reproducing the scalar omitted-mass inequalities with directed arithmetic.

Then W_aux≥(1−delta)C and the full-versus-retained energy laws differ in TV by at most delta. Rejection success≥(1−delta)*exp(−19.511321). The resulting upper guarantee is roughly298million attempts per accepted edge. This is vastly improved from older certificates but NOT practical, and each attempt also has weighted-walk/core/combinatorial costs.

Per-attempt approximation eta yields accepted-law error≤2eta/p_lower (when eta≤p_lower/2). Choose eta accordingly and cap attempts at ceil(log(1/failure)/p_lower), charging noncompletion probability. Do not treat a 64-bit upper-only DP receipt as an adequate sampler or ignore rejection amplification. The auxiliary core's implementation cost remains an explicit dependency.

## 3. Coupled estimator, with physical time still paid
Let v be the original soft committor. For this globally admissible f, Dirichlet pairing gives C=D(v,f). For oriented indicator-cut native edges x→x^i, the energy-law expectation of v(x)−v(x^i), together with the reservoir boundary contribution, equals C/W_bbox.

Under an established attractive native coupling with downward-closed source and upward target, simulate ordered initial states with common heatbath updates and common original reservoir opportunities until their source/target outcomes resolve. The outcome difference is a0/1 variable with expectation v(x)−v(x^i). Thus a full-law energy-edge draw plus this coupling gives a Bernoulli mean C/W_bbox, potentially enabling relative sampling cost proportional to W_bbox/C rather than its square.

This does NOT make the experiment fast. Native coupled absorption may itself require metastable physical time. Without a certified accelerated but exact decision procedure or a valid finite-time truncation/tail bound, this is only an estimator interface. Independent uncoupled endpoints give a signed variable and may have substantially worse variance. Omitted-energy and sampling errors must be allocated relative to C/W, not merely as an unrelated constant TV tolerance. For the stated omitted-energy bound, its contribution relative to C is already controlled.

## 4. Actually executed native toy acquisition
`bbox_sampler_toy.py` implements the entire proposal/rejection loop on a3x3torus with fixed-diagonal augmentation and bboxH2 (singleton augmented components), rational exp(2theta)=4,exp(2phi)=2. It includes root/order multiplicity, all boundary marks, deterministic duplicate-mark rejection, original native rates and the j1 rate envelope1/8. The exact auxiliary law has22 states; every one of126 structural cut edges satisfies the rational accepted-density identity.

20,000 actual seeded attempts gave3,706 accepted edges (0.1853) versus exact success probability0.1864090248. Accepted sectors j1,j2,j3 all occurred (3607,96,3). No target boundary can lie inside this singleton cut on this toy; target/long-contour exceptions for R200 remain handled analytically above. This experiment establishes finite native-law implementation consistency, not R200 runtime or general algorithmic tractability.

## 5. Executed omission budget
`check_omissions.py/json` now supplies exact rational elementary comparisons, combined with the inherited directed tail receipt: auxiliary inverse-image omission/C<10^-18; full long-contour omission/C<exp(−470)<10^-18; target plus source overlap/C<exp(−19000)<10^-18. Thus total omitted energy/C<3*10^-18 at auxiliaryr16, conditional on the same geometric/lower-bound interfaces. This supersedes the provisional omission-budget statement above; it does not include numerical errors of an unimplemented R200 sampler.
