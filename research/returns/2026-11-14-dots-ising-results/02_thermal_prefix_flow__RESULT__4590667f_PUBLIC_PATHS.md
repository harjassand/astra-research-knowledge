# Compact thermal growth flow: an explicit fiber result, not yet a current-moment theorem

## Result
For a fixed compact contour/interior fiber satisfying the conditions below, a bit-preserving native-spin flow carries its FULL thermal source normalizer to the actual majority target. Its paid mean resistance has only a constant activation factor exp(4theta), not a volume-scale all-plus entropy factor. An auxiliary soft growth capacity obeys

 C_growth >= Z_D/[kappa_D^-1+2n exp(4theta)].

This is a source-fiber capacity result. It does NOT establish the desired second moment under actual current, global residence, contour-family coverage, or polynomial acquisition of Z_D. The exact remaining defects are stated in Sections5–7.

## 1. Fully specified fixed fiber
Assume theta>=4, R>=80, phi=theta/R, and L>=8R. Fix a filled, nonwinding compact domain D whose bounding rectangle embeds in a torus chart and |D|>5R^2. Fix every spin inside D. Require its physical outer boundary endpoints to be plus and its total interior magnetization M_D>0. A dense low-hole interior can satisfy this, but no Gibbs law for that interior is assumed.

Fix an exterior minus collar sufficient to separate the retained plus component under the source's augmented connectivity. Outside, allow the full conditional thermal ensemble Omega_D in which every companion plus component has an embedded filled domain of area<=R^2. For the Peierls involution, explicitly require these filled companion domains to be disjoint from every frozen pin. This is automatic only after the relevant nesting/collar separation is established; it is not silently inferred from a vague 'outside component' label.

DO NOT additionally impose global M<0 in Omega_D. A filled-domain spin flip can increase plus volume when the domain contains many holes and need not preserve that constraint. Source configurations already in B are allowed and stop immediately. Let Z_D=sum_{Omega_D}w and mu_D=w/Z_D.

The fiber is a rigorous envelope/class, not a claim that all remaining actual M5 entries have exactly this support. The fixed interior and fixed collar are source restrictions; they are not assumed to be maintained by the actual native process during a physical time interval.

## 2. A non-asymptotic companion-gas moment bound
Allow arbitrary inhomogeneous fields between0 and3phi on all free sites. Flipping the ENTIRE filled domain V of a specified companion contour, including its holes, preserves the fiber constraints because V is disjoint from pins, area<=R^2, and all newly formed components remain inside V. Its weight ratio is at most

 exp[-2theta P+6phi min(P^2/16,R^2)].

Use the retained source's rooted physical-contour count 8(2P+3)^2 4^P. For P<=R the exponent is at most-(13theta/8)P. For P>R, V<=RP/4 gives exponent at most-(theta/2)P. Thus, at theta>=4,R>=80, the probability that any free site is plus is bounded by

 rho <=8 sum_{P>=4}(2P+3)^2(1/160)^P
       +8 sum_{P>=80}(2P+3)^2(11/20)^P
     <1.490053e-6 <1/500000.

The two geometric-series bounds were evaluated exactly as rational numbers; density.json records the result. No FKG property of the constrained fiber is assumed.

Set a=1-2/500000=.999996. Tilting the source by exp(t N_F^+) for any deterministic free-site subset F and0<=t<=4phi changes its fields by t/2, so they remain<=3phi. The density estimate gives

 E_muD exp(4phi N_F^+) <=exp(4phi rho |F|).

Fixed-minus collar sites contribute zero plus count. This is where the complete thermal entropy, including diffuse companions, is paid.

## 3. Bit-preserving shell and its geometric cost
Choose a deterministic geometry-only ordering of sites outside D. First use a two-neighbor bootstrap ordering to fill D's bounding rectangle geometrically; then grow the shorter rectangle side, one complete strip at a time, eventually covering the torus. Let F_k be the first k outside sites. The transformed configuration is x^(k)=x XOR F_k. Interior and original contour spins are never changed; source thermal bits outside are FLIPPED, not erased or replaced by plus spins.

For a physical edge from D into F_k, the ORIGINAL spins are plus/minus by the source contour/collar definition. Its contribution to the resistance exponent is negative. All other crossing products are at most1. Therefore

 E_muD[w(x)/w(x XOR F)]
 <=exp[2theta(P(D union F)-P(D))-2phi a |F|].

This identity includes arbitrary thermal exterior companions through the field-tilt bound. The relevant area is the actual deterministic shell |F|, not occupied plus area or a falsely solid source.

During bootstrap-to-bounding-box filling, perimeter never increases, so the right side is at most1. Thereafter the long rectangle side exceeds sqrt(5)R>2R/a. The first site of an added strip increases perimeter by at most2; subsequent sites do not increase it, and a completed strip strictly lowers the displayed exponent. Torus identifications can only reduce perimeter. Consequently every prefix moment is at most exp(4theta).

The process is an analytical native-edge path, not a claim of high-probability execution under frozen pins. It may flip source plus defects to minus. Nevertheless the original boundary witness is untouched, so the path remains in its stable witness sector. If the initial state is outside B, flipping all outside-D spins gives final magnetization M_D-M_outside>0 because M_D>0 and initial M_D+M_outside<0. Thus the path reaches the ACTUAL target and is stopped at its first B visit.

## 4. Injectivity, actual clocks and exact finite test
Join an auxiliary source vertex to every x in Omega_D with conductance kappa_D w(x), and send mass w(x)/Z_D along the preceding path.

For this ONE FIXED D and its deterministic ordering, a physical edge identifies its flipped site and hence its unique prefix position. There are at most two source preimages, recovered by XOR from the two orientations. Opposite-direction traffic cancels: (u-v)^2<=u^2+v^2. First-target stopping only removes paths.

Native heatbath resistance is exactly1/g(z,z^i)=1/w(z)+1/w(z^i). Summing the prefix moment bound gives physical flow energy<=2n exp(4theta)/Z_D. Source edges contribute1/(kappa_D Z_D), including any source states already in B. Thomson gives the stated capacity bound.

For a fixed D, decoding a candidate source, checking companion-domain constraints and replaying first-B stopping require polynomial work in n. This does not make the normalization Z_D acquired.

check.py executes the entire exact rational flow in a4x4 diagnostic with sixteen thermal source states and four free thermal bits. It verifies every non-target divergence, at most two edge preimages, and the native-energy upper bound. It uses e^(2theta)=e^(2phi)=2 and does not satisfy the large-R geometry hypotheses; it checks the flow algebra, not the asymptotic moment estimate.

## 5. Contour-family multiplicity is NOT solved
The at-most-two preimage assertion holds only when D is fixed. After the exterior collar is flipped, the old contour may merge with the growing thermal phase, so D is generally not decoded from the intermediate physical configuration. Different D fibers may then contribute to the same edge. An exponential contour count cannot be omitted.

Keeping the whole minus collar as an explicit marker would preserve D's identity, but removes the favorable old-interface cancellation: newly creating the exterior plus phase then pays another O(theta P(D)) interface cost. A small hidden label cannot simply be treated as a physical state variable. No claim of a label-free full-family flow is made.

## 6. Why this does not yet bound actual current second moments
Write a reweighted source as mu_D(x) b(x). The SAME path calculation bounds its energy by

 (1/Z_D) sum_k E_muD[b(x)^2(r_k(x)+r_{k+1}(x))],
 r_k=w(x)/w(x XOR F_k).

The proved thermal moment controls E r_k, NOT E[b^2 r_k]. Actual incoming current generally has a nonconstant density b involving the unknown voltage gradient. No independence, negative correlation, or stochastic monotonicity for this constrained fiber has been established that permits replacing E[b^2 r] by E[b^2] E[r]. Such a substitution would be invalid in general.

Similarly, a low unit-flow energy bounds a source-averaged potential, not automatically its second moment or its reflected remaining time. Converting this auxiliary capacity theorem into Phi(p^2) or Phi(t_M^2) remains a substantive operator/transport problem.

## 7. Current-source join and acquisition still required
One must establish actual boundary-fiber coverage (including the post-entry domain, not merely a large predecessor), retain nesting/winding distinctions, pay every D label, and either acquire Z_D or cancel it in a valid current-normalized inequality. The full M<0 restriction cannot be reinserted into the field-tilt proof without a separate argument. Source-feed states in B are part of this auxiliary capacity construction, not an alteration of the original physical task.

The result improves the compact construction from a single low-energy path to an entropy-paid thermal FIBER flow, with explicit constants. It does not solve actual-current growth or residence. It is an application of Thomson, Peierls and bit-preserving flow machinery already present in the program, rather than a new physical primitive or a claimed North Star breakthrough.
