# Conserved-isotope product certificate

Newly authored, 16 October 2026. This is elementary conservation/partial identification applied to a proposed chemical measurement. It is not an experimentally calibrated model and carries no historical novelty claim.

## 1. Exact one-pool identified interval

Fix a complete control volume and a finite time horizon. Every lithium atom entering it is classified by origin as source-feed or nonfeed. Origin persists through exchange, dissolution, isotope fractionation, and reintercalation. Let i be 6Li or 7Li. Assume:

- Total source input of isotope i is a_i >= 0.
- Total nonfeed input of isotope i is bounded by b_i >= 0.
- A physically isolated deliverable product pool, after assay aliquots and any finishing/storage losses, contains z_i >= 0 atoms/moles of isotope i.
- No undeclared source, nuclear isotope conversion, or inaccessible initial store can supply that isotope.
- Unretained outputs/stores are unrestricted except for nonnegative inventories. Additional real constraints can only tighten the result.

Let f_i denote source-origin isotope i in the product. Necessarily

```
0 <= f_i <= a_i,
0 <= z_i - f_i <= b_i.
```

Therefore

```
l_i = max(0, z_i - b_i) <= f_i <= u_i = min(z_i, a_i).
```

If l_i > u_i, the inputs and observed pool are inconsistent with the declared budgets. Fail the premise; do not clip the contradiction into an apparent result.

Conversely, for any f_i in [l_i,u_i], put f_i source atoms and z_i-f_i nonfeed atoms in the product. Put all remaining source atoms and any remaining nonfeed atoms in unobserved allowed stores/outputs. All inventories are nonnegative. Thus the interval is sharp given exactly this one-pool, conservation-only information. If b_i is only an upper bound, choose a feasible actual nonfeed input at most b_i. The construction is an identifiability witness, not a proposed chemical mechanism.

The two isotope allocations are independent under these minimal premises, so total source lithium F=f_6+f_7 has the sharp interval

```
L = max(0,z_6-b_6) + max(0,z_7-b_7),
U = min(z_6,a_6) + min(z_7,a_7).
```

An interval in moles is converted to source-Li mass only with a declared isotopic convention. For comparison with natural-lithium production, use a declared natural-Li equivalent molar mass consistently. Do not compare raw enriched-isotope masses to natural-Li masses at the same nominal mg/L; match molar concentrations.

This certificate needs no fixed isotope ratio in product. In particular it remains valid under arbitrary isotope fractionation. The familiar two-endmember equality F=(z_6-p_old*z_total)/(p_feed-p_old) is not used: it requires an additional transport/fractionation model or a justified bounded relaxation.

## 2. Joint uncertainty and whole-run accounting

Let C be a simultaneous confidence/systematic-error region for all input and pool inventories, including actual volumes, gravimetric sampling, stock purities, blanks, mass discrimination, dilution, incomplete digestion, initial electrode content, and loss streams. The safest lower/upper source bounds are

```
L_C = inf_{theta in C and conservation feasible} L(theta),
U_C = sup_{theta in C and conservation feasible} U(theta).
```

The actual system belongs to these bounds whenever the declared coverage and physical budget premises hold. A set with no conservation-feasible point is an accounting/calibration failure. A best-fit point or per-channel standard deviation is not the simultaneous region.

For a simple simultaneous rectangular outer set, conservative bounds are

```
L_box = sum_i max(0, z_i_lower - b_i_upper),
U_box = sum_i min(z_i_upper, a_i_upper).
```

These are safe outer bounds, and need not be sharp. Retain correlations when they matter. A negative measurement lower bound is truncated at the physical nonnegative inventory boundary; missing input is not zero.

For multiple fractions j, compute z_i(A)=sum_{j in A} z_ij for the selected pool A. The **same global nonfeed budget b_i is charged once**. Charging b_i independently against every retained fraction throws away information; pretending each fraction has a fresh or zero background invents information.

A fuller finite linear program can allocate origin/isotope inventories across every measured output, feed remainder, electrode, membrane, and known loss stream. For each isotope, impose total input equals total terminal outputs plus terminal stores. Add measured intervals and actual capacity constraints. The source-origin product sum is a linear objective. This is standard conservation-based partial identification, not a new LP algorithm.

For recirculated feed, a_i counts the initial source stock and actual new additions, not repeated pump passes or repeated exposures. Over electrode life, residual source Li from earlier cycles remains source-origin, while replacement-electrode Li and new receiver/conditioning seed remain nonfeed. Count each physical input once.

## 3. Finite fraction-routing decision

There are m=15 ordered fractions and K=m+1=16 suffix policies. Suffix k retains k,...,15; policy16 retains nothing. The particular family is a controllable engineering choice. No optimality outside it is claimed.

Suppose the uncertainty set simultaneously covers every relevant fraction and budget. For each suffix A compute:

- L_A: source-origin Li lower bound.
- Total Li and all competing-cation bounds for actual chemical purity.
- V_A: actual isolated liquid volume.
- Separate Fe/P and other required impurity bounds.
- Complete collection, storage, purification, assay, and disposal costs.

For positive concentrations, one sufficient chemical-purity bound is

```
purity_lower = Li_total_lower / (Li_total_lower + nonLi_cations_upper).
```

If the denominator is zero, product qualification is unavailable rather than automatically perfect. Report source-Li yield separately from chemical purity so that receiver seed cannot manufacture new recovery. Source-Li concentration is bounded by L_A/V_A_upper. A fixed user/product contract supplies minimum concentration and purity, maximum contaminants/volume/cost, and a worthwhile source-Li or economic margin. None is inferred from the source papers.

Choose any suffix passing all robust constraints and a positive lower utility margin. Because the confidence event is simultaneous, data-dependent choice among the sixteen suffixes preserves that event. This statement certifies the measured batch, not future electrodes or unseen histories. Freeze the rule and validate its future behavior on independent full runs.

A pooled-screen no-go is immediate: any selected suffix is a subset of the whole collected wash, hence its source-Li amount is at most all-wash total Li. If the latter's valid upper bound lies below the minimum worthwhile amount, no suffix can meet that amount. The fine time series is unnecessary for that decision. Failure of a pooled purity test alone does not reject every suffix; a tail fraction could be purer.

## 4. Causal increment from downstream routing

Let the declared baseline send collected transition fractions to an explicit disposition, and let the candidate retain a qualified subset. Assume:

- upstream liquid/pressure/temperature histories and electrical controls are identical;
- the collector acts downstream of a one-way, equal-backpressure boundary;
- collected liquid cannot return or alter subsequent cell inputs;
- the added pool is physically retained to the declared product deadline.

Then the candidate and baseline have the same electrode/ordinary-receiver evolution. Additional isolated source Li is exactly the source Li in the extra retained pool. A positive L_A certifies a nonnegative output increment on this realized run. This is a deterministic causal-interface argument, not an inference from correlated product data. The first proposed test makes the boundary especially direct: both policies collect identical fractions, and only the keep/dispose action after sealing differs. An inline deployment needs the additional hydraulic qualification above.

If collection modifies backpressure, flow, a recirculating reservoir, or future wash feed, that premise is false. Use actual randomized arms and full-history measurements. A valve schematic alone is not a measured hydraulic guarantee.

Even under the premise, extra cost can exceed extra product value. Practical superiority requires a positive lower net value or the user's declared multiobjective improvement. The comparison must include an equally informed conventional fractionation operator. No software monopoly on the measured rule exists.

For a population/lifetime statement, the experimental unit is an independent electrode life or declared finite full history. ICP instrument repeats are assay precision measurements. Per-cycle observations on one electrode are dependent and cannot be treated as independent lives. Termination at a cycle cap before the physical endpoint does not establish lifetime yield.

## 5. No-go for the supplied electrical/endpoint data

Coulometry observes the charge-weighted sum of ionic/electronic fluxes. The equal-valence exchange direction

```
delta J_Li(t) = -h(t),
delta J_Na(t) = +h(t)
```

has zero cation charge increment. Thus an unmeasured Li-to-Na exchange can change species occupancy with no corresponding current. A calibrated voltage/state relation might add information, but the supplied traces do not establish an injective species-inventory observation map.

Endpoint species measurements add integrals, not intermediate histories. Two nonnegative exchange profiles with the same area, one concentrated early and one later before the first endpoint, have the same charge and endpoint species changes. They can differ during seconds-long rests. Choose the area small enough that all declared inventories retain nonnegative slack. Without acquired rate/response constraints, endpoint records do not identify the early profile. This is a data-identification obstruction, not evidence that either profile describes the actual LFPC electrode.

Released net receiver-Li increments also do not label origins. In a complete receiver accounting,

```
delta receiver Li =
  source Li arriving + nonfeed Li arriving
  - receiver Li leaving in samples/other streams/stores.
```

Unknown nonfeed/terminal/sample inventories prevent replacing this equality by delta receiver Li = source recovered Li. Quantitative closed inventory or a marker can remove the ambiguity.

Finally, finite ten-cycle observations allow different future degradation/recovery continuations. Better own-initial retention alone does not compare cumulative product, matched time/dose, replacement cost, or life endpoint. Figure4 electrical dose and Figure5 Li are separate runs. They cannot jointly fill this observation fiber.

These obstructions justify declining the broad rest/lifetime claim while proceeding with a direct, finite physical-output measurement. No theorem here supplies missing experimental data.

