# Astra Chemical Invention — chemical self-silencing versus product-thiol feedback
26 October 2026. Analytical/computational construction; **no new physical experiments**. Governing programme: fault-tolerant molecular writing, preserving competent parents after failed reaction and avoiding irreversible incorrect chemistry. Executable source: `astra_product_sulfur_state_20261026.py`.

## 1. Mechanistic correction and stronger reaction comparator

Previous distributed NCL-like writer consumed the unique free amino terminus through an S-to-N acyl shift but **regenerated the acceptor cysteine thiol**. An N-acylated, rooted product is thus unavailable for another native-amide commitment via the same nitrogen, but is not generally chemically inert: it can form reversible S-acyl species and disulfides, and may present S-acyl cargo to other sites. The previously derived quadratic *unfinished-unfinished* disulfide burden omitted **completed-unfinished and completed-completed** sulfur reactions. This is distinct from the earlier reactor-ageing problem with discarded donor waste: product-derived thiols cannot simply be washed away.

Primary sources confirming this chemistry:
- Overview of NCL/free final Cys thiol and subsequent maleimide labeling: https://pmc.ncbi.nlm.nih.gov/articles/PMC8228110/ ; NCL speciation: https://doi.org/10.1039/D0CC01604G .
- **Li, Wang & Gao (2020), Angew. Chem. Int. Ed.**, DOI 10.1002/anie.202000837, https://pmc.ncbi.nlm.nih.gov/articles/PMC8041485/ : a 6-acyloxy-2-formylphenylboronic-acid reagent (e.g., KL42) rapidly forms a *reversible* thiazolidino-boronate (TzB) with a free cysteine-like 1,2-aminothiol, followed by slower *intramolecular acyl transfer*, yielding a *stable N-acyl thiazolidine*. That commits **both** amine and thiol in the new heterocycle; the final product retains the aryl-thiazolidine structure and is **not** an unmodified/native simple amide. Authors report ~5,000 M^-1 s^-1 precursor chemistry for a tested reagent; acyl-product apparent half-time ~0.3 h at pH 6 in their model reaction; ~80% product after 1 h for one model peptide at 2 μM KL42; enzymatic/phage labeling on separate targets. None demonstrates PNA/DNA-coded 256-way writing, traceless reagent-DNA removal or arbitrary cargo.
- **Cyclopropenone (CPO)** is another tested 1,2-aminothiol-consuming, thiol-silencing alternative forming a stable 1,4-thiazepan-5-one, in aqueous pH ~7 and with diverse conjugatable cargo; it has documented high chemoselectivity in proteins (2022 JACS, DOI 10.1021/jacs.2c02185). Its actual off-template association, early-step reversibility and compatibility with DNA-programmed multi-reagent mixtures are unacquired. https://pubs.acs.org/doi/10.1021/jacs.2c02185
- A **reversible** 2-formylphenylboronic-acid (2-FPBA) NCys mask followed by separately selective internal Cys maleimide modification and triggered demasking was demonstrated (2016 Chemical Science DOI 10.1039/C6SC01520D), but this is not error-free large-array cleanup.

## 2. Exact donor/product-sulfur kinetic theorem

At instruction `j` assume one competent unfinished site, and `j` correctly N-acylated but free-thiol completed sites. The current acyl donor is transiently `F` (free) or `S` (captured on a completed site's sulfur). From F, intended amide at k, permanent wrong bond w, harmless reagent loss λ, or transient S-acyl diversion across `j` completed sites at total rate j*b. From S, equivalent free reagent is restored at r, permanent incorrect inter-site transacylation at x, or harmless donor loss at h. A wrong event at x is a **hypothesized net transfer to another reactive site**, not a second N-acylation on the completed product. It may be absent or suppressed in particular real reagents.

Transient generator and final exits:

Q = [[-(k+w+λ+j*b), j*b], [r, -(r+x+h)]].

The 3-column exit matrix (correct, wrong, reagent loss):
B = [[k,w,λ],[0,x,h]].

Solving (-Q)^(-1) B from F yields probabilities proportional to:

`correct = k`, `wrong = w+j*b*x/(r+x+h)`, `reagent loss = λ+j*b*h/(r+x+h)`.

When reagent loss is truly harmless, new equivalent donors are replenished, and the root returns to an identical state, the probability that the eventually permanent outcome at stage j is correct is **exactly**

P_j = 1/[1 + ρ0 + s*j], with ρ0 = w/k, s=b*x/[k*(r+x+h)].

Therefore the exact correct L-stage probability is

P_L = product_{j=0}^{L-1}(1+ρ0+s*j)^(-1),
log P_L = -L ρ0 - s L(L-1)/2 + higher-order terms when small.

The potentially quadratic error exponent is due to **retained correct products** acting as chemical side-reactants, and survives perfect removal of spent donors. It does not apply if x=0 or completed-site sulfur is inaccessible/silenced.

Even if x=h=0 so every excursion returns harmlessly, the expected total number of S-acyl detours before L intended incorporations is exactly `(b/k)L(L-1)/2` (with w=λ=0 or equivalent harmless replacement); its resource burden is quadratic. Example b/k=0.01, L=1000 -> 4995 off-target sulfur captures. Counts do not directly establish permanent wrong products.

This formula is verified against the independently assembled two-state CTMC for j=0,1,4,25,100,999, a gamma/product identity where numerically conditioned, and a separate Gillespie-style event sampler using larger error probabilities. Large-argument `gammaln` subtraction is ill-conditioned; the authoritative implementation sums `-log1p` directly.

For illustrative R: k=.02/s, w=4e-8/s, b=2e-5/s PER completed site, r=1/s, x=2e-4/s, h=.01/s, λ=.005/s, L=1000 gives 90.40% correct by the ideal renewal limit. Completely eliminating post-product SH participation raises the *same model* to 99.80%; 1% residual SH leaves 99.70%. THESE ARE NOT MEASUREMENTS.

### Chemical route crossover

Consider a direct self-silencing reaction with a *worse intrinsic* wrong/correct hazard ratio ρ_cap, compared with a NCL route with initial ratio ρ0 but j-dependent product-thiol penalty `s*j`.

P_NCL = Π_j(1+ρ0+s*j)^(-1), P_cap=(1+ρ_cap)^(-L).

The capped route wins precisely when `log(1+ρ_cap) < (1/L)sum_j log(1+ρ0+s*j)`. In a small-ratio limit it wins once `ρ_cap-ρ0 < s(L-1)/2`.

With intentionally hypothetical ρ0=2e-6, s=2e-7 and ρ_cap=5e-5, the first integer L at which cap wins is **482**, notwithstanding its 25x greater initial incorrect hazard. At L=1000: NCL 90.31%, self-silencing comparator 95.12%. At L=100: NCL 99.881%, comparator 99.501%. Thus scalable chemical synthesis can favor a mechanism whose *product* is chemically inert, despite modestly worse single-operation selectivity. The comparison ignores the alternative product's steric/DNA-guide footprint and other rates.

## 3. Reversible masking cannot be treated as perfect selective capping

An alternative way to silence completed N-acyl-Cys sulfur while preserving unfinished 1,2-aminothiol is:

(1) Remove thioester donors/auxiliary thiols; (2) reversibly mask **unfinished** cysteine using non-acylating 2-FPBA to form TzB; (3) apply a thiol-specific irreversible reagent (such as a suitably chosen maleimide) to cap **completed** N-acyl-Cys sulfurs; (4) clear capping reagent, then unmask the unfinished site with an appropriate trigger (e.g. benzylhydroxylamine) before more thioester donors are introduced.

2016 experiments support selective NCys-versus-internal-Cys masking and separate labeling; they do not establish the chemistry on dense DNA-rooted scaffolds or per-step survival near 1-1e-5. Hydroxylamine/methoxyamine can attack thioesters, requiring reagent separation.

Exact cap-period CTMC: unfinished site `U` (unmasked) -> `H` (TzB protected) at rate a, back H->U at rate b, and irreversibly damaged by thiol-capper U->D at rate c_U. Assume initial equilibrium distribution [b/(a+b), a/(a+b)] and 2-FPBA present during cap. Then:

Q = [[-a-c_U,a],[b,-b]],
S_U(t) = [b/(a+b), a/(a+b)] exp(Q*t) [1,1]^T.

A completed-site free-S product is successfully capped with probability `1-exp(-c_P*t)`. The probability of both desired events for a separated unfinished/completed pair is `(1-exp(-c_P*t))*S_U(t)` under independent site evolution.

For illustrative a=2/s, c_U=c_P=.1/s, 99.9995% capping needs t>=122.06 s. To keep per-treatment unfinished-site irreversible cap loss below 5e-6 requires **b<=8.60e-7/s**, corresponding to a >13.46-day mean protected lifetime absent externally induced release. This is *not* a measured FPBA off-rate. At b=.001/s the unfinished-site survival at that t falls to 99.42%; demanding 1,000 independent protected-pair operations then yields only about 0.298% correctly processed pairs. Leakage matters because any temporary opening exposes thiol to irreversible trapping; a high average protection fraction is insufficient. A chemically triggered, very stable reversible mask might satisfy the condition, but this is not established.

## 4. Challenge to direct self-silencing acylation: wrong donor can bind chemically before DNA checks

The KL42-like 6-acyloxy-FPBA reagent is **itself chemically reactive toward accessible NCys**. DNA barcode mismatch alone does not prevent a wrong reagent forming a *covalent* TzB on the wrong site. Once the ring is covalently formed, mere DNA dissociation may not undo it; slow intramolecular transfer can commit wrong cargo later.

Model correct and wrong TzB capture rates α_C and α_W, reversible precursor disassembly r_C,r_W, chemical acyl commitment c_C,c_W. Effective right and wrong irreversible rates are

A=α_C c_C/(c_C+r_C), B=α_W c_W/(c_W+r_W).

With harmless precursor reversal, eventual right/wrong ratio B/A is exact under exponential renewal. **If r_C=r_W and c_C=c_W, DNA dissociation by itself provides no extra chemical proofreading.** Physical coupling to chemical reversal or prevention of off-template precursor formation is required.

Highly conditional target example anchored to one published association-rate order of magnitude: 255 wrong donors, each at 1 nM, k2=5000 M^-1s^-1 => aggregate wrong NCys capture α_W=0.001275/s if all equally accessible. Assume correct DNA-assisted capture α_C=0.1/s, a correct precursor commitment probability 0.5, and take product half-time 0.3 h at pH 6 as approximate commitment c=ln(2)/1080s=0.000642/s (the paper's observed half-time includes reaction environment). For full-chain 1000-step 99% correct fidelity, B/A <= .99^(-1/1000)-1 ~1.005e-5. Then wrong precursor must commit less than 3.941e-4 of encounters, requiring **wrong precursor reversal >=1.628/s**, over 2,500 times the assumed correct precursor reversal. Under these optimistic assumptions, mean single-site time ~1578 s. At correct capture 0.01/s, required wrong reversal ~16.28/s; at 1/s ~0.162/s.

A stronger special case: if correct and wrong precursors have **identical** commitment/reversal behavior, then in this example each incorrect donor must be at most 7.88e-13 M (~0.79 pM) when α_C=0.1/s, or correct association must exceed 126.86/s when all wrong species are present at 1 nM. This is a **conditional incompatibility** between unrestrained bulk cysteine chemistry and high-fidelity simultaneous 256-species writing, not a claim about sterically shielded or chemically caged substrates.

All unmeasured capture/accessibility/reversal rates in this calculation are *model assumptions*. The reported isolated 5000 M^-1s^-1 capture rate does not establish that all 255 DNA-linked analogues have that rate when excluded by scaffold geometry. Crucially, absence of DNA duplex formation is not proof of absence of off-template covalent 1,2-aminothiol capture.

## 5. Physical priority, equally informed alternatives, and falsifiable discriminators

Three distinct approaches survive:

(A) **Direct self-silencing 1,2-aminothiol conjugation** (6-acyloxy-FPBA / stable N-acyl TzB; or CPO/1,4-thiazepan-5-one): most experimentally grounded dual-handle commitment, but final chemistry includes bulky heterocycle, substrate identity can be wrong, persistent DNA-guide attachment on the reagent could poison the scaffold, and an arbitrary 256-cargo DNA-addressed implementation is not acquired.

(B) **Classic NCL + state-dependent completed-site thiol silencing**: may retain native amide cargo, but requires extremely reliable unfinished-site shielding through thiol capping, compatible selective unmasking after donor clearance, and no irreversible thiol-transfer damage before cleanup.

(C) **Staged protected NHS-PNA amidation** (Joshi et al. 2025 DOI 10.1021/jacs.5c00708): direct evidence for reversible amino-terminal protection, no product-S sink, and easier experiments on sequential growth; still suffers off-template wrong amides, waste poisoning, persistent stalls, and lack of independent address-by-address progress.

The smallest meaningful chemical discrimination uses at least two scaffold-bound, independently addressable free 1,2-aminothiols, one covalently completed N-acyl-Cys product, plus a second donor carrying a chemically distinct cargo. Compare donor capture with/without DNA matching, separate stable amide and transient sulfur adducts, test whether a wrong TzB chemically disassembles on DNA unbinding, and determine whether a completed product's residual sulfur (NCL) or heterocyclic footprint (self-silenced alternative) blocks next-site writing. For the masking route, compare protected-but-unreacted cysteine competence after thiol capping versus uncapped product SH. Use mass AND site-specific chemical structure, not only fluorescence and total mass.

**New conditional principle:** the chemical state after successful writing is as important as selectivity during writing. A genuinely self-silencing product may remove an accumulating, nonwashable competing-reaction population. The result remains analytical/chemical-precedent grounded and is **not a demonstrated multi-instruction molecular writer**.
