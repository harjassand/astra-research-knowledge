# S1–S3: spatial stochastic safety, facet-compatible transport, and an unequal-diffusion obstruction

Date: 2026-10-21 (Australia/Brisbane). NEW ADDITIVE RESEARCH only. Original N33 and its existing reviews/status are unchanged. This record has analytic arguments and independently checked exact rational constants; no external peer review, Lean replay, historical novelty clearance, simulation, experimental verification or real-time hardware claim.

## Baseline and attribution

Original N33 manuscript: \`web/pages/d-326696af15b5e02b.html\`; original plaintext SHA256 \`bbecea61cd373a787920bb4484494114b7d616d5f20ee096cae3831487707e9c\`, per N33 dossier. Exact load-bearing original lines: endotactic essential-edge definition 66–86; active-slope essential-source drift 396–518; positive compact affine plateau / measurable trajectories / scale absorption 519–737; finite-compartment scalar mixing 858–918; controlled stochastic polytope-exit martingale 1159–1310. OpenAI family149 fixed-affine construction pinned at \`adc7f1241b42e322a6451854ab7e4b4c146bf78a\`. Independent later registered comparator to deterministic permanence: Michael Mislan, \`mmislan/palomar-endotactic-permanence\`, pinned \`c72c945264565397ecc3eee779e6bd5f3f3a061d\`, 9 October 2026. Its six-reaction three-species model, *not originated in this note*, is in \`paper/main.tex\` §6. Qualitative exponential exit techniques are established in chemical large deviations (Agazzi–Dembo–Eckmann 2018, DOI 10.1214/17-AAP1344). Reaction–diffusion master equations are conventional (see PMC3825834). Unequal-diffusion invariant-region antecedents include Plum (1988), DOI 10.1016/0022-0396(88)90119-2, and Antonín Slavík (2017), DOI 10.1016/j.jde.2017.08.019. The present claims are a concrete mathematical combination with specified new interfaces and constants, not the invention of any of these methods.

## Model — six molecular reactions per compartment

For each of n arbitrary finite compartments z and integer volume V>=100, define count Z_z=(A_z,B_z,C_z) and concentration X_z=Z_z/V. Each site uses actual integer-complex channels:
C→A+C, 2A+C→A+C, A+B→A+2B, A+3B→A+2B, B+C→B+2C, B+3C→B+2C.
Each channel has predictable rate k_{z,r}(t,past)∈[1/2,2], and density-dependent molecular intensity V k_{z,r} phi^V_{y_r}(X_z) with standard falling factorials (zero if insufficient molecules). Start all site counts at (V,V,V). Let Q=[2/5,5/2]^3 and tau be the first jump with any X_z outside Q.

For each chemical species s separately, allow predictable particle migration w→z at rate m^s_{zw}(t,past) Z_{w,s}, with nonnegative m^s and *specieswise balance*
sum_{w != z} m^s_{zw} = sum_{w != z} m^s_{wz} = d_z^s <= 1/4.
The directed graphs may differ completely across s and change arbitrarily over time; connectivity, lower migration-rate bounds and dwell times are NOT required. Balance guarantees the physically mass-conserving transport mean field is sum_w m^s_{zw}(X_{w,s}-X_{z,s}); merely bounding directed in/out separately without balance is not an allowed substitution.

## Theorem S1: stochastic spatial safety (derived this investigation)

For any n>=1, integer V>=100, finite T>=0, and all such predictable rate and transport controls,

P(tau<=T) <= 6 n exp(-V/20) + (2205/44) n V T exp(-V/480).

Constants do not depend on n, rates, control strategy, number of graph edges, species mobility topology or switching schedule. For n=100,V=30000,T=exp(V/960), risk RHS=4.030645587585597e-6; log10(T)=13.571702559476618, in SYNTHETIC NONDIMENSIONAL units. If n(V)<=exp(sigma V), T(V)<=exp(rho V), and sigma+rho<1/480, the bound vanishes as V grows. This is not an infinite-graph process claim or actual device timescale.

### Detailed finite-volume proof

Set L=2/5, U=5/2, collar ell=1/40, L+=17/40, U-=99/40, theta=1/12, E=12/11. Scalar Taylor-series comparison gives exp(theta)<=1/(1-theta)=E. For site z and species s=u, the scaled favorable **chemical** birth and death rates are:
A: (b,d)=(k1 c, k2 c*u*(u-1/V));
B: (b,d)=(k3 a*b, k4 a*b*(u-1/V)*(u-2/V)), u=b;
C: (b,d)=(k5 b*c, k6 b*c*(u-1/V)*(u-2/V)), u=c.
Write q=c for A, q=a*b for B and q=b*c for C, so chemical birth is k_plus q. Globally q>=L^2 and for A q>=L. Chemical death <=2 q u^2. In an upper collar, A death >=(1/2)q*u*(u-1/V), while B/C death >=(1/2)q*(u-1/V)*(u-2/V). Since the upper collar has u>=U-, V>=100, all displayed factors are positive.

Balanced migration at site z has scaled birth influx b_D=sum_w m^s_{zw} X_{w,s} and scaled death outflux d_D=d^s_z u. For x inside Q^n, lower collar u∈[L,L+] gives b_D>=d_z L and d_D<=d_z L+. Using q>=L^2 and d_z<=1/4, the exact worst-case margin is
(b_chem+b_D)-E(d_chem+d_D) >= L^2(1/2 -2 E(L+)^2) -(1/4)(E L+ - L)
= 57/55000 >0.

In the upper collar u∈[U-,U], the migration favors death by >= d_z U-, while influx birth <=d_z U. For A, q=c>=L:
(d_chem+d_D)-E(b_chem+b_D)
>= L[(1/2) U- (U- -1/100) -2E] -(1/4)(E U-U-)
= 125127/440000 >0.
For B and C, q includes the coordinate u itself so q>=L U-:
(d_chem+d_D)-E(b_chem+b_D)
>= (L U-)[(1/2)(U- -1/100)(U- -2/100)-2E] -(1/4)(E U-U-)
= 67976607/88000000 >0.
All are exact rational inequalities for every permitted population and control, not point samples.

For each species/site and each of its two coordinate face gaps g=x_{z,s}-L and g=U-x_{z,s}, define Phi=exp(-theta V g). Its generator divided by V Phi equals
b_in(e^{-theta}-1)+d_out(e^{theta}-1)
=(e^{theta}-1)(d_out-b_in/e^{theta}),
where b_in and d_out refer to movements favorable/adverse to the gap (reverse physical birth/death for an upper gap). All three rational margins prove that the generator is <=0 whenever g<=ell.

Off the collar and before exit, Phi<=exp(-theta V ell)=exp(-V/480). Chemical jump intensities affecting a site/species, per V, are bounded by
Lambda_A=2(U+U^3)=145/4 and Lambda_B=Lambda_C=2(U^2+U^4)=725/8.
Incoming + outgoing species migration is <=2*(1/4)*U=5/4, hence every such face has affected-jump scaled hazard <=Lambda_loc=735/8. Discard favorable jumps and bound outward jump multiplier by exp(theta)-1 <=E-1=1/11:
L_t Phi <= V (735/8)(1/11) exp(-V/480)
outside its collar (inside it L_t Phi<=0). Sum the six facets per site across n sites:
L_t Phi_total <= (2205/44)n V exp(-V/480).

Initially all sites have concentration 1, lower gap=3/5, upper gap=3/2, so Phi_total(0)<=6n exp(-V/20). At the first exit a face gap becomes negative, so Phi_total(tau)>=1. Before exit the total jump intensity is uniformly bounded, and the single jump overshoot bounds Phi_total at tau by at most 6n exp(theta); thus stopped counting-process compensation applies without a Markov assumption or global unstopped nonexplosion. At time T,
P(tau<=T)<=E Phi_total(T∧tau)<= Phi_total(0)+(2205/44)n V T exp(-V/480).
This proves S1. A direct Monte Carlo procedure would need exponentially many expected events at the displayed horizon; this is an analytic risk bound.

## Theorem S2: abstract full-span N33 spatial-stochastic transfer (conditional)

Assume a finite *integer-complex* endotactic mass-action network has S=R^d (full reaction span) and fixed positive rate box. N33's already-constructed finite-affine ceiling gives a compact convex **full-dimensional** polytope Q={x:a_i·x+b_i>=0} wholly in the positive orthant with rational c in int(Q). Every proper facet i comes from a nonzero active slope a_i, and N33's weighted essential-source lemma gives uniform strict chemical inward drift a_i·f(x,k)>=delta_h>0 on that facet for all box-valued rates. Finite compactness thickens every facet to a uniform strict positive collar.

For n sites, use the same integer-complex molecular reactions at each site and balanced predictable migration of individual molecules. **Normal compatibility:** for each proper facet i, all species with (a_i)_s !=0 share the same ordered migration coefficient m^{(i)}_{zw}; other species may migrate differently. Let its balanced row/column sum be <=D_i independent of n. Then
a_i·migration_drift_at_z =sum_w m^{(i)}_{zw}[g_i(x_w)-g_i(x_z)] >=-D_i g_i(x_z)
while x_w∈Q. Decrease collar width until this leakage is smaller than half its reaction margin. The falling-factorial chemical drift differs from the deterministic polynomial by O(1/V) uniformly on Q, with no transport factorial error. For large enough V, strictly positive collar drifts survive. Finite jump size J_i, local variance/activity bound B_i and local total hazard Lambda_i all remain independent of n. The original N33 controlled jump-exit exponential-martingale proof, applied to the product polytope, yields constants a,b,C,V0>0 independent of n with
P(tau_{Q^n}<=exp(aV))<= C n V exp(-bV)
from lattice-compatible rational interior starting states.
No efficient synthesis of Q, mesh-uniform PDE theorem, stationary law or physical benefit follows. Full-span is needed for this automatic *per-local-facet* argument; neutral stoichiometric directions can obstruct strict reaction restoration. For axis-aligned box Q, each normal is a coordinate axis, so normal compatibility is automatic for entirely different migration processes across species; this is why S1 is stronger than the original N33 identical-species-mixing statement in its special model.

Finite bounded-degree graphs also tolerate small **unequal-species deviations** from common migration even at oblique facets: if each deviation has absolute row budget <=epsilon, its adverse face drift is at most epsilon*sum_s|a_{i,s}|(U_s-L_s). Below the chemical inward margin, a smaller collar and large enough V restore the stochastic argument. No mesh-independent epsilon is implied because a refined physical lattice can have row sums growing like inverse mesh size squared.

## Proposition S3: sharp unconditional unequal-diffusion geometry and falsifier

For any full-dimensional compact convex polytope Q in R^d, Q×Q is invariant for *every* two-site diffusion-only dynamics x'_z=D(x_w-x_z), x'_w=D(x_z-x_w) with arbitrary independently selected nonnegative diagonal species mobility D **iff Q is an axis-aligned box**. Proof: on the relative interior of any facet with outward normal a, choose a tangent vector v (a·v=0); both x±epsilon*v remain on that facet for small epsilon. Taking neighboring site at either point, facet invariance forces a·D v=0 for every tangent v and every diagonal D. Applying coordinate projections D shows a has at most one nonzero coordinate. Thus each facet is coordinate aligned and bounded convex Q is a product of intervals. Conversely coordinate interval maxima/minima are preserved by each scalar species diffusion independently. This is elementary and has established invariant-region antecedents, not a historically novel theorem.

Concrete two-species falsifier: Q={1/4<=x1,x2<=2, x1+x2<=3/2}, at site z take x_z=(1,1/2), at site w take x_w=(1/2,1). With mobilities D1=1,D2=2, both begin on Q's oblique facet, but d_t(x_z1+x_z2)=-1/2+1=+1/2, so site z instantly leaves Q. Arbitrarily weak differences in diffusivity can break universal oblique-facet invariance for sufficiently high spatial curvature in a PDE, a known obstruction. This does not refute N33's single-compartment theorem or the finite-graph small-mismatch transfer.

## Reproduction, limits, continuation

Exact standard-library \`verify_spatial_safety.py\` checks all reaction stoichiometry, rational face inequalities, exp(theta) rational majorant, per-site hazard and example. \`spatial_reproduction.json\` is the saved result. It does not independently check the martingale proof or historical novelty. Chemical rates and fixture are synthetic; physical actuation to sustain lower-bounded rates and model nondimensional time are unvalidated. The n-compartment result is a mathematical conditional guarantee for a reaction-diffusion master equation, not experimental stochastic permanence.

Next decisive steps: independent review/formalization of S1/S2; acquire actual high-dimensional N33 polytope and finite positive collars with explicit bit/runtime accounting (N50 only conditional general acquisition); identify measured realistic chemical/biological integer-complex model and mobility/rate budgets; test mesh-refinement cost and physical per-cell molecule count. Do not close original G-PERMANENCE-GLOBAL-COMPOSITION or promote N33/N54/N173; this record is additive.