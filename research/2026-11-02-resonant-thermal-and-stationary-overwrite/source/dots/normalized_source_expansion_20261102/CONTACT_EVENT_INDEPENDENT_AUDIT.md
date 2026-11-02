# Independent audit of contact-source / connected-event resummation

2026-11-02. This audits root's proposed exact two-level gas after the independent forest investigation. The construction is stronger and simpler than the generic hyperforest route: enlarge source components until singleton contact neighborhoods are disjoint, then promote nonsingleton native clusters to independent event species.

## 1. Exact source regrouping

For each elementary perturbation label λ retain the earned owned-clock set R_λ: all explicit clock matrix-unit sites and all checks meeting its dressed data support. Also retain its original data/bath supports. Define T_λ=N_1(R_λ) in the native clock interaction graph. Form USED-label components using intersections of the T_λ and intersections of original data/bath supports. Compatibility MUST forbid exactly these same intersections.

This is a deterministic coarsening of the earned source partition, hence a bijection of full histories remains valid. It merges components but never splits an independently closed component. More directly, disjoint enlarged marks imply disjoint affected-check sets and data/bath supports, so the original independent syndrome-closure argument applies verbatim. Ordered insertion times and repeated uses retain the original simplex / factorial measure.

For distinct compatible sources, T_Γ are disjoint. Native source–source signs are trivial because adjacent owned clock columns would force contact intersection. A background singleton rod on clock x can affect at most ONE source: any source it sees has x in T_Γ. This includes both deletion on R_Γ and interaction with its complete histories on neighboring columns.

## 2. Exact singleton resummation

In the original native logarithm split off all singleton clusters. For a source Γ let B_Γ(r)=0 on its owned columns and otherwise be its exact source–rod factor. Since a singleton sees at most one compatible source,

`product_Γ B_Γ(r)-1 = sum_Γ [B_Γ(r)-1]`.

Thus the singleton response exponent factors EXACTLY into separate source activities. No estimate or independence assumption is needed.

Positive ordinary nonwinding singleton activity contributes the exact owned-column factor exp(-λ_x), λ_x its finite-β intensity. On unowned clocks its response has modulus <=1, since Re(B-1)<=0. Positive wrap singleton responses likewise have modulus <=1. Signed winding singleton responses have modulus at most exp(2βJ0) per contact column (the sharper owned-column factor is exp(βJ0)).

The absolute un-tilted full-source transfer bound is K exp(βM0) per owned clock. Combining with exp(-λ_x) gives K exp[β(J0+δ_β)] per owned clock. Hence a safe source envelope is

`K^|R_Γ| exp{β(J0+δ_β)|R_Γ| + 2βJ0|T_Γ|}`

before dictionary, bath and insertion factors. It includes every thermal level and never-vacuum path. There is no exp(βJ0K) self-pressure cost.

## 3. Independent connected-event species

For every original native connected cluster E with n(E)>=2, retain its full trajectory labels and complex Ursell measure φ(E). Set event–event pair factor to 1 and source–event pair factor

`h(Γ,E)=product_{r in E} B_Γ(r)`.

This is in {0,+1,-1} in the audited sign model. The grand partition sum of these independent complex events is the exponential of their total modified intensity. Dividing by the event-only partition function yields exactly

`exp{ integral φ(E)[product_Γ h(Γ,E)-1] }`.

That is the required nonsingleton response of the original native logarithm. Event overlap is NOT forbidden: these are connected-cluster terms in a logarithm, not disjoint physical trajectory components. Artificially adding event hard cores would destroy the identity.

Finite-volume absolute integrability follows from native KP. Thermodynamic ratios are taken through uniform local bounds, not by pretending the extensive event partition exponent is finite in infinite volume.

At event charge γ n(E), the local absolute native event intensity is bounded by

`ell_γ <= exp(γ){β[exp(a0_γ)M0(b_γ)-M0] + exp(a0_γ)W(b_γ)}`,

with native activities inflated by exp(γ), and any separate spatial weights included. The M0 subtraction is INSIDE the exp(γ) factor. It is O_γ(β x_γ J0) plus the wrap bound. This avoids the otherwise false expression exp(a0_γ) exp(γ)M0(b_γ)-M0. A fixed γ suffices; there is no need for the hyperedge method's γ of order D.

## 4. Syndrome dependence: a necessary correction to the old consumer

After singleton resummation a source activity is generally NOT a single syndrome character. Signed winding singleton responses exponentiate local s_x-dependent terms. It is a scalar analytic FUNCTION of syndrome, with a uniform absolute envelope.

Its dependence footprint is contained in:
- the original stabilizer filling footprint of its closed V data word;
- its owned native clock flux labels, already inside T_Γ;
- the contact set T_Γ from singleton dressing.

The original polynomial anchor-counting argument extends to this union. No expansion into exponentially many Fourier characters is required. For any source whose footprint meets a flipped check, use

`|z_Γ(s)-z_Γ(s')| <= 2 z_Γ^majorant`.

Event measures remain native cluster measures and have syndrome dependence only through their constituent winding rods. Their dependence footprint can conservatively be overcounted by all constituent clock labels; the local event row bound then controls marking.

Source–event pair factors, contact hard cores, and their Mayer coefficients are syndrome independent once trajectories are fixed. Therefore a mixed cluster can change only if a source footprint or an event flux footprint meets the flipped set. This proves the required locality bookkeeping once mixed KP is imposed; monomial source structure is unnecessary.

## 5. O(v), bath-volume uniformity, and exceptions

Rescale perturbation coefficients by η=v/v0. A concrete source with k insertion events gains exactly η^k; all singleton dressing and event measures are independent of those coefficients. Since k>=m>=1, every source-containing mixed cluster gains at least η. Apply the convergent reference-majorant bounds before summing. This gives O(v) local influence rather than differentiating an operator logarithm.

Bath-only sources remain in the scalar gas at all sizes. For memory-touching sources retain only m<d/b_D in that gas; ALL larger ones are exceptional, including accidentally scalar words. Enlarging the contact component graph does not invalidate |D_Γ|<=b_D m, so the same conservative cutoff remains valid.

For an exceptional source the logical word has norm one. Its singleton dressing remains scalar; its event pair factors remain scalar. Consequently the standard pinned scalar-gas ratio bound applies if the mixed KP inequalities also hold for excluded sources as test roots with charge A m. This test-root fact must be explicitly stated, not inferred from scalar zero-freeness alone. Compatible exceptional logical words commute because their underlying data supports are disjoint; absolute matrix-product norm bounds in any case suffice for the remainder majorant.

Bath-volume independence follows because event interactions require a native contact column, and exceptional source animals are anchored at native data OR clock labels. Pure bath animals arbitrarily far away cancel in normalized scalar ratios. Connected bath extensions are counted with the same enlarged bounded-degree label-animal constant, never with total bath volume.

## Verdict

The exact two-level resummation passes this independent audit, subject to the already earned dictionary and the stated exact contact-compatibility convention. The remaining quantitative work is ordinary two-species KP bookkeeping and physical incidence/resource accounting, not an unproved generic connected-source cumulant theorem. The local-influence consumer must use bounded scalar source functions rather than its old claim that every dressed source is one monomial.

## 6. Explicit consumer inequalities after the audited KP choice

Use A, γ, q_norm and Q from `TWO_LEVEL_CONTACT_GAS_AUDIT.md`, retaining a spare positive per-label weight α. For a fixed syndrome check g define

`S_g = integral_(small sources Γ: g in F_Γ) |z'_{Γ,0}| exp[A m(Γ)]`,

where F_Γ is the enlarged dependence footprint above. Polynomial filling/anchor counting and the spare α imply `S_* = sup_g S_g < infinity`, independent of bath and memory volume. This is an actual source-measure integral, not a count of Fourier coefficients.

Let Ξ(s)=log Z_small(s)-log Z_native(s), after common product-bath factors cancel. Every term in Ξ contains at least one source. At perturbation ratio η=v/v0<=1, each such term is bounded by η times its reference-majorant counterpart. For two syndromes differing on T, mark every changing source activity or changing event activity in the telescoping product. Rooted mixed KP gives

`|Ξ(s)-Ξ(s')| <= 2 η |T| [S_* + P_γ]`.

Using all events with a rod on g to bound changing events only overcounts. The free-energy influence is therefore at most `2η(S_*+P_γ)/β` per flipped check. The same inequality applies to real logarithms through Re Ξ; positivity of the truncated signed scalar gas is not assumed.

For exceptional memory-touching source roots, the identical source KP bound holds for every size m: its proof used only contact cardinality <=b_full m, not m<d/b_D. Thus pinning any finite exceptional family costs at most `exp(A sum m)` relative to the scalar background. With q_norm evaluated at the actual perturbation and label-animal counting,

`R_n <= C n sum_(m>=d/b_D) C_contact^m q_norm^m exp(A m)`.

At a strict admitted point this is `<=C' n lambda^(d/b_D)` for lambda<1. The matrix remainder obeys `r_n<=exp(R_n)-1`. The anchors are native data/clock perturbation labels; connected bath extensions are inside the animal count, not an extra bath-volume prefactor.

For actual positive syndrome Gibbs traces W(s) and the scalar truncated Z_small(s), the usual logical multiplicity d_L gives

`|W(s)/(d_L Z_small(s))-1|<=r_n`.

Consequently `d_L|Z_small(s)|(1-r_n)<=W(s)<=d_L|Z_small(s)|(1+r_n)`. For r_n<=1/2 the two-syndrome logarithmic correction is <=4r_n. This is a multiplicative witness-ratio correction; it is not an additive failure-probability floor and uses no operator-log expansion.
