# From the complete overcount to actual cut-energy edges

Status: constructive acquisition interface, with an exact small native-network identity check. Large-R backward walk sampling/core sampling has NOT been implemented or run. Its cost is explicitly controlled by the acquired overcount/lower-capacity ratio, which is not yet proved polynomial uniformly in R.

## 1. Same global trial, no canonical-count substitution

Keep the actual M_s indicator potential and original soft-source network of RESULT.md. Let T be the mathematical truncated overcount tuple normalizer, using the chosen rational tilt separately at each physical perimeter. A contour label consists of a physical root, a closed nonbacktracking word, and its deterministic chosen tilt. If its positive filled area is V and its physical perimeter P, define

 b_gamma=exp(-2theta P+2phi Vp) r_P^[2(V-Vp)],
 Vp=min(floor(s²R²),floor(P²/16)).

The same expression assigns a positive weight to all overcount words, even invalid or negatively oriented ones. The tuple law includes1<=j<=8 ordered labels and totalP>=S0, and weights product b_gamma. Its exact normalizer is T, not the numerical upper receipt. Positive finite DP acquires T and samples this law to specified precision: samplej/totalperimeter by the tuple convolution, backsample perimeters, choose roots, and backsample each weighted closed walk by its endpoint/direction recurrence. The min-tilt choice is simply a fixed chosen tilt at eachP; it need not equal the unknown exact optimum.

This is a finite positive algorithm. Recomputing conditional path tables or using checkpoints keeps memory polynomial; all rational local moments and subsequent exponential perimeter factors can be enclosed to arbitrary relative precision. The already executed64-bit upper receipt is NOT by itself a high-accuracy sampler implementation.

## 2. Auxiliary proposal core, without changing the source

Choose r'>=r with C_(r') subset M_s, r'<=R and r'<L/4. This is an AUXILIARY proposal distribution, not a replacement for the original source A=C_r. The authorized core primitive supplies its TV sampler and relative normalizer Z_(r').

The exact same filled-domain flip comparison proves

 mu_M(C_(r')^c) <= u'=6n(4exp(-a_s))^(2r')/[1-4exp(-a_s)],
 a_s=theta(2-s/2).

The original normalizer comparison still gives Z_M/ZA<=1/(1-u4). No assumption about an actual entrance law is made. This law will be used only through an exact change of variables for trial ENERGY.

## 3. One rejection attempt

1. Draw an overcount tuple with weight product b/T.
2. Draw y from the auxiliary core law w(y)/Z_(r').
3. Draw one of the n physical gate sites uniformly.
4. Reject unless the words lift under the ORIGINAL fixed diagonal resolution to valid, disjoint, embedded filled contours, each with area within the cut. Form x by flipping every spin inside those domains.
5. Recompute the actual augmented components of x. Require x in M_s\B, the gate spin minus, and its native birth to leave M_s. Require that the tuple is EXACTLY the old affected outer-domain tuple of that gate, using a deterministic canonical positive root for each contour and deterministic ordering. This canonical check pays all root/order/invalid-word multiplicity by rejection rather than ignoring it.
6. Accept with probability

 c_i(x) * w(x)/(w(y) product b_gamma).

The ratio is <=1. Indeed the full-domain flip bound gives w(x)/w(y)<=product exp(-2theta P+2phi V), including all thermal interior bits. Since2log r_P<=2phi and V<=Vp, each corresponding factor is <=b_gamma. Native c_i<=1.

Each valid structural cut edge with inverse image y in C_(r') has exactly ONE accepted canonical label/gate representation. Hence its probability per attempt is exactly

 g(x,x^i) / [n T Z_(r')].

Accepted edges therefore have the ACTUAL conductance-weighted law of this retained part of the original global trial. This is not a pure-shape law, a canonical-k law, or a claim that source currents are Gibbs-distributed.

## 4. Missing energy is paid, not declared absent

Let W_aux be retained structural edge energy. Missing structural edges with inverse image outside C_(r') have total energy at most

 n T Z_M u'.

To see this, fix an overcount tuple and gate, perform the injective full-domain change of variables, bound the exact weight ratio by product b, and sum the omitted y under the SAME mu_M. Then sum tuple/gate bounds. No independent-source assumption is involved.

Add the previously bounded P>Mper structural tail, target crossings within M_s, and source-to-target overlap. Let the resulting complete omitted energy bound be DeltaW. If an acquired original capacity lower is C>=ell ZA and DeltaW<=delta ell ZA, then

 W_aux>=C-DeltaW>=(1-delta)ell ZA,
 TV(actual full trial energy law, retained law)<=DeltaW/W<=delta.

The full global energy upper U satisfies n T Z_(r')<=U ZA. Consequently acceptance probability is at least(1-delta)ell/U. This explicitly charges the overcount rejection. It is polynomial only WHEN U/ell is polynomial; no such uniform assertion is smuggled into the sampler.

Approximate per-attempt sampling/acceptance error eta_attempt produces accepted-law error at most2 eta_attempt/p_lower when eta_attempt<=p_lower/2. Thus choose all errors with the rejection amplification paid, cap attempts using p_lower and a charged failure probability, and return the explicit error contract. Since log(1/p_lower) is O(R) for the current certificates, required arithmetic/core-TV precision remains polynomial even when the number of attempts is not.

Acceptance-frequency estimation acquires W_aux=nT Z_(r')p. Together with DeltaW it gives a controlled full trial-energy normalizer. The retained energy proposal then interfaces with the source's conditional coupled estimator, but its separate actual physical decision-time certificate remains required.

## 5. Concrete finite scale and honest significance

At R200, original r5 and epsilon1/100, use U=exp(-6202) and the conservative original-clock bulk-free lower ell=exp(-6449). Taking auxiliary r'=64 changes NO source edge or source definition and satisfies its geometry conditions. The same contour comparison gives u'<exp(-302) by elementary rational exponential inequalities, so omitted inverse-image energy relative to C is <exp(-55). The certified perimeter tail contributes <exp(-354) relative to ell; target/source terms are far smaller. Thus delta=1/1000 is conservatively available.

The resulting rejection cost upper is2exp(247). This is enormous; expressing it as at most n^17 at THIS one n is not a uniform polynomial theorem or a practical algorithm. Stronger lower certificates can improve this cost, but the ratio must always be paid. This construction's gain is that the global proposal interface no longer requires an unavailable fixed-magnetization or closed-critical-Gibbs oracle: it is explicitly reduced to acquired positive walk DPs, an already-authorized auxiliary core sampler, native acceptance and a quantified overcount ratio.

## 6. Small exact native check

energy_proposal_identity_check.py uses the actual3x3 periodic heatbath graph with rational e^(2theta)=4,e^(2phi)=2 and the fixed-diagonal singleton-component cut. It enumerates its thermal configurations and all structural birth edges. For every edge it constructs the unique canonical affected singleton tuple, its exact inverse-flip image, and verifies both the full Gibbs weight ratio and the accepted-edge identity. This is a genuine native conductance/change-of-variables test, not an implementation of the large contour sampler or a test of its asymptotic quality.
