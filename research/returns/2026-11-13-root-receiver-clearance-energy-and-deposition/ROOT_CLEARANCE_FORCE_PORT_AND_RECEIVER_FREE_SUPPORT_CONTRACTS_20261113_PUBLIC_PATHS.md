RECEIVER CLEARANCE AND OBSERVABLE ROUGH-SURFACE FORCE PORTS
13 November 2026 Brisbane / 12 November UTC

Scope
These are conditional mechanical, geometric, transport and service contracts. They do not supply a manufactured anchor, measured asperity capacity, a field sensor, a complete force-port geometry or an operational platform. The P3 available contained-reset return is preserved unchanged at P3_CONTAINED_RESET_AVAILABLE_RETURN_20261113.md,34590 UTF8 bytes,SHA256 49364a94cbf21af5b7eb787d6abf887fd18e68824d735512e2f783ffa1625e69. Its native final identity/prefix/bytes remain unknown; rendered equations/tables and nested activity have stated gaps; its linked report/code/archive were not collected. No producer code was executed.

1. Prepared-face clearance is a geometry and force-path contract
For the symmetric orthogonal-slot model with station half-spacing a and diametral clearance c, define the linearized rigid clearance set
P(c)={ (ux,uy,psi): |ux|+a|psi|<=c/2, |uy|+a|psi|<=c/2 }.
It has four pure-translation vertices (ux,uy)=(+/-c/2,+/-c/2),psi=0 and two pure-yaw vertices ux=uy=0,psi=+/-c/(2a). Arbitrary initial engagement followed by loaded reversal requires P-P=2P, not displacement relative to a chosen mathematical origin.

At a face corner (+/-b,+/-b), displacement is (ux-y psi,uy+x psi). Convexity and the six vertices give the exact rigid in-plane reversal diameter
D_clear=sqrt(2)*max(1,b/a)*c.
Yaw reversal is c/a. Two independent serial interfaces with this same geometry have Minkowski sum P(c1)+P(c2)=P(c1+c2). This statement assumes the declared common coordinate/anchor geometry; real guide rocking and individual moving-stem modes are not erased by it.

Using a=15.91mm,b=24.5mm from the proposed dimensions, clearance53/60/78/85um gives rigid-only corner reversal.115422/.130666/.169866/.185110mm. Corresponding yaw spans for60/85um are about.2161/.3061deg. These exclude elasticity, out-of-plane motion, carrier compliance, guide rocking and bearing pressure. They neither reproduce nor replace the producer's fuller.194/.248mm and.319/.410deg conservative screens. An upper bound above a requirement removes that certificate; it does not demonstrate an actual loading trajectory that fails.

The return's new receiver/stem dimensions can consume53um of clearance, and its active guide can add25um. Its stated7um receiver wear allowance is consequently a functional geometry limit, not a permissible5% loss of the whole housing. A stiffer assumed complete joint cannot repair an unconstructed guide or load path.

2. The issued energy boundary and a comparison-specific finance screen
The issued1kJ requirement was for the dedicated module, including its proof/unload duties; occupied robot energy was separately requested in the full service. The return's introduced714J/attempt with2% rejection is728.571J/potential accepted cycle. Its separate300W*64s/.98 robot allocation is19591.837J. The online total is20320.408J, but that does not by itself violate the separately defined1kJ module boundary. Both remain unmeasured budgets, with no accepted physical denominator. No retroactive boundary change follows.

Retaining the return's approximate favorable prepared comparator.512USD/service,30% reduction means.3584USD/service. Retaining its comparison-specific common service floor.302 leaves.0564 for unique hardware, renewal, handling and consumables. At100 services/year for ten years and8%, discounted services are671.00814. If ALL that headroom were assigned to unique initial hardware, its allowable present value would be37.84486USD. If the same unique cost had to recur at year5, the initial allowance would be22.51888USD. These are conditional arithmetic on this introduced comparator and floor, not a universal lower bound, a quote, or an unavailable decomposition of the producer's complete code.

3. A continuous-wrench contact-group construction
Introduce twelve groups at radius R=.032m and angles theta_i=2pi*i/12. The external reference is the convex simplex
Fn/100N + |Ft|/250N + |Mxy|/10Nm <=1, Fn>=0.
A separate conservative self-load envelope permits signed10N normal,10N shear and.25Nm in-plane bending simultaneously. These are introduced bounded loads, not an achieved body mass/center of gravity.

At group i define e_r=(cos theta,sin theta),e_t=(-sin theta,cos theta). For its body-side point-force port, let s be inward radial shear, t transverse shear and n tensile normal force. Introduce the convex local bounds
0<=s<=150N, |t|<=.5s, n<=.7s, n>=-100N.
The following is a required port law for a physical construction, not an empirical spine/adhesion law.

Set an opposed radial preload p=120N per live group. Assign the net tangential force equally among live groups. For normal force and bending, make A's columns (1,y_i,-x_i), and use n=A^T(AA^T)^(-1)(Fn,Mx,My). For all twelve groups, and after deactivating any one complete opposed pair, A has full row rank. Opposed symmetry balances the introduced preload and the net-shear moment. Exact paired balance is an assumption that hardware must bound; it is not furnished by a common actuator command.

For each linear contact inequality, the support of the reference simplex is the MAXIMUM of its normal, arbitrary-shear-direction and arbitrary-bending-direction supports, not their sum. The independent self-load supports are then added. For example n-.7s has worst value
-.7p + max(100/N, .7*250/N, 10*|c_M,i|)
       +10/N+.7*10/N+.25*|c_M,i|,
where c_M,i are the two bending coefficients from A^T(AA^T)^(-1). The side inequality uses sqrt(1+.5^2)*(250+10)/N. Thus the directional scope is continuous under these assumptions, not a finite-angle sweep.

For all twelve live groups the minimum normal-cone margin is29.1979N and the maximum conservative vector-force bound is175.0521N. After any one opposed pair is removed, ten groups remain; minimum normal-cone margin7.9906N, side-cone margin30.9311N, radial upper margin4N and compression margin24.6906N. The worst vector-force bound is196.3094N. Algebraic reconstruction of all three normal-wrench bases is checked in the owned executable.

If each live group had at least30 engaged tips with actual per-tip capacity8N and maximum-to-mean load-share factor gamma<=1.2, the triangle bound gives worst tip load7.85237N after paired removal, leaving only.14763N below8N. With24 rather than30 engaged tips that bound fails. Counting installed tips is not counting engaged tips; neither quantity supplies gamma, tip strength, asperity strength or observable readiness. Thirty-six installed tips per group could provide geometrical search capacity, but no hardware or sensing that establishes the minimum30 is supplied.

For the paired-removal case, the scalar preload interval allowed by the normal-cone, radial and tip-force bounds is approximately108.5848--123.6906N. A commanded120N is therefore not a robust result against arbitrary setting error or independent preload imbalance. The source of preload, its actual force distribution, passive retention and recovery must be built.

4. Physical organization and missing local operations
A12x8mm contact tile moving radially from42 to32mm has maximum swept corner radius48.1664mm. Using each tile's circumscribed radius, minimum conservative separation between adjacent tile boxes is2.1422mm. This only screens planar contact tiles. It supplies no rear carriage, local compliance, sensor, equalizer, tendon, latch, ring stiffness, dust seal, support tool or arm route.

Twelve120N preloads sum to1440N of local loading despite zero resultant in the symmetric model. If that force were maintained throughout10mm drag, mechanical work would be14.4J; this is a stated force-distance scenario, not a measured engagement energy. A twelve-node regular polygon reacting these forces would have segment hoop force231.822N in the ideal planar balance. Actual out-of-plane reactions, surface-normal couple and connection stiffness are additional.

An introduced.5mm round shank with.5mm loaded lever carrying8N has nominal cantilever bending stress325.95MPa. That is not a material yield, fatigue, sharp-tip contact or masonry fracture certificate. A sharp point can fracture its substrate well before a shank calculation is useful. Independent tip compliance and a retained hold may also conflict with the required fixture stiffness.

The local cone must be defined at an actual body force port with its real lever arm. Moving an unknown contact within a finite tile changes its moment. A known point-force port needs an actually built moment-isolating or otherwise qualified connection; a free mathematical spherical joint is not supplied. Individual contact moments, normal compression pads, surface damage, creep and loss of engaged asperities must be included in the measured port law. Global proof alone does not identify every local strength or preload.

One physical question is whether contact groups can search compliantly, share and locally qualify actual reactions, then retain a sufficiently stiff state without sliding loaded contacts on release. A known disabled pair in the algebra is not an observation algorithm. The controller must establish its own bounded state and safely transfer load before deactivation. Existing independent supports, captive preload release and positive keepers are useful concepts but not automatically compatible hardware.

5. Actual primary bindings and availability limits
IMAO's exact four-page maker file was read as text through its main tables and installation/operation description:
https://www.imao.com/files/en/pdf/qcwesa-e.pdf?utm_source=chatgpt.com
It describes a retracting wedge/ball mechanism; the1227 variant lists1000N clamping,2500N holding tied to a.1mm plate-gap criterion,190g and a separate receiver. It lists failure-level strengths rather than qualified working limits and recommends separate locating pins for higher accuracy. The first screenshot then timed out: the identity is HELD against further/recovered access. Its plotted curves were not visually read. The related-family30,000 unloaded cycles and Japanese price retain producer-only exposure; they were not read in this exact maker file. No2500N arbitrary-wrench/500-cycle qualification or delivered price follows.

DISTINCT Jiang et al., Modeling the Dynamics of Perching with Opposed-Grip Mechanisms:
https://bdml.stanford.edu/uploads/Main/PerchingPublications/ICRA_2014_Modeling_preprint.pdf
The actual read main text through line492 includes the opposed-truss/tendon/latch/rebound model, small120g reference and calculated.017J engagement absorption, roughly1cm microspine dragging requirement, and17/20 small perching trials on roofing shingle at declared velocities. This is not100N/250N/10Nm concrete/brick qualification. A requested page4 screenshot returned a reference without an observable bitmap; no curve values or unseen image contents are imported. Later text, videos, cited originals and other artifacts were not recovered. Parness2013 and Merriam2016 are distinct unavailable identities, not recovered through this2014 paper.

6. A different physical manufacturing operation, with its own missing bridge
A separate introduced diffusion-film calculation for localized copper deposition uses D=7e-10m2/s, Cu concentration1000mol/m3, film thickness20um,400um circular footprint and unity current use. It gives j=6753.97A/m2,.848729mA per footprint,.00100616g/h and994 such simultaneous footprints for1g/h. This is a geometry/transport budget, not a universal rate limit or a constructed printing array. The prescribed film, field localization, many independent feeds, high-current-use chemistry, preparation, functional finished part and complete renewal/cost remain unconstructed.

The DISTINCT Arshad et al.2022 FJECAM initial main exposure read the actual Prusa-based setup,400um plastic nozzle,350um copper wire,1M copper sulfate and dedicated z-stage. The first governing follow-up timed out and the identity is HELD. Its later measured deposition rate, roughness and results were not read or imported from abstract/search text. DISTINCT Babchuk2024/jese.2291 first PDF access failed; no governing preparation or rate was supplied. These access failures are not scientific evidence against electrodeposition manufacturing.

Owned artifacts
ROOT_RECEIVER_CLEARANCE_AND_ROUGH_SUPPORT_CONTRACTS_20261113.py
12400 bytes; SHA25637ed59eb2fa117878f56bd5eff72d4de41536bb38041c163712b7457db1e3c6a.
ROOT_RECEIVER_CLEARANCE_AND_ROUGH_SUPPORT_CONTRACTS_20261113.json
61702 bytes; SHA2566974eb4f3afdcd1722b72913df59f39fbf8c0806504f514630c5910b04fa2b63.
These are beside this note. No physical experiment, acquisition, installed instrument qualification, geometry-complete assembly, full service advantage or all-design obstruction is established.
