# Astra XH2 — Fresh-source bootstrap closure and inherited pioneer escrow

27 Oct 2026 (AEST). This is analytical/computational work, not a reported biological experiment. All rates, seed costs, accuracy values, and reliabilities are synthetic model parameters. Earlier work on force-selected maturation, local-functional versus global-service credit, context, source mismatch, external helper rescue, lineage extinction and molecular memory remains governing.

## 1. New precise problem

The prior role/address mapping assumes an address is already present to direct the corresponding worker. A descendant starting with one intact founder and fresh feed has no inherited exterior material. Which founder-produced pioneer roles must be synthesized before role-mediated address recruitment can become self-sustaining? When can a provisional physical pioneer be withdrawn, and when can its corresponding **genetic instruction** be deleted?

Let V={0,...,K-1} denote role/address capabilities and let each role j have a family of alternative prerequisite sets P_j: any one all-available set is sufficient to generate j. A founding genotype can produce initially active roles S, possibly by manufacturing genetically encoded temporary extracellular seed structures. The dynamics is monotone during one startup episode: A_0=S and A_{t+1}=A_t ∪ {j: exists P in P_j with P ⊆ A_t}. Once formed, all roles are retained during this idealized closure test. This assumption is explicitly relaxed in the seed-loss race below.

### Bootstrap obstruction theorem

Call U⊆V nonempty **self-blocking** if, for every j in U, every allowed prerequisite P ∈ P_j has P∩U ≠ ∅. This includes the case in which role j has no allowed production rule. Then:

**Closure(S)=V if and only if S hits every self-blocking U.** It suffices to hit every inclusion-minimal such U.

Proof: If U is self-blocking and U∩S=∅, by induction no role in U can ever be made because creating the first role in U always requires a role in U already. Conversely, if Closure(S)≠V, let U=V\Closure(S). For each j∈U, no prerequisite set P can be contained in Closure(S), so every allowed P intersects U. This makes U a self-blocking set disjoint from S. QED.

This is closely related to standard bootstrap-percolation / target-set selection stopping-set reasoning. The theorem's distinctive role here is to certify a *source-closed developmental genotype*, not a new combinatorics result.

### Two exact 12-role constructions

A 12-role directed unary cycle has one minimal blocker (all 12 nodes), minimum pioneer set size one, and 12 choices of that seed. Four independent three-role clusters in which every role requires **both** partners have 12 inclusion-minimal two-role blockers (three per cluster), minimum pioneer seed size eight, and 3^4=81 minimum pioneer sets. A strongly connected dependency graph alone is insufficient to infer the minimal pioneer number: the *AND structure* matters.

All 2^12 possible pioneer sets were exhaustively enumerated for both cases. The seed-hitting equivalence was also checked for 60 random seven-role AND/OR hypergraphs with no violations.

### Rare spontaneous nucleation exponent

Suppose each of K roles independently nucleates as a spontaneous pioneer with probability p. Let m be the minimum feasible pioneer set size and N_m the number of feasible seed sets of that minimum size. Then the exact bootstrap probability is a reliability polynomial and obeys

    P_bootstrap(p) = N_m p^m + O(p^{m+1})   as p→0.

For the 12-role directed cycle, P=1-(1-p)^12 and m=1. For the four AND triads, P=(3p²-2p³)^4 and m=8. At p=.05 this gives about .4596 for the cycle versus 2.7628e-9 for the triads, despite the same number of total roles. The combinatorial order of the required founder origin is a potentially decisive constraint on autonomous regeneration.

## 2. Source-generated pioneer attempts: seed diversity versus reliability

Synthetic per-attempt seed functionality p=.95, four independent AND triads, 20 fresh reconstruction episodes, no common-cause failures. Let n_i be attempts invested in producing the pioneer structure of role i; then its activation probability is 1-(1-p)^n_i. Triad completion requires ≥2 of its three seeds to activate, because the third can develop when both partners exist. All per-role attempt allocations were optimized by exact dynamic programming over the four independent triads.

For fixed open-loop allocation: 12 attempts (one per type) give P_20=.558717; 16 attempts give .803081; 19 attempts give .932240; 20 attempts (per triad counts 2,2,1) give .979755; 24 attempts (2,2,2 each triad) give .998504. A 95% target for 20 episodes requires at least 20 precommitted pioneer attempts in this search space.

A different physical contract may help: a local pioneer receipt that can tell whether a new basal role has actually been made, before requesting the next source-built seed. If K=8 distinct basal pioneer roles are required, a source can retry failed attempts until each has been positively acknowledged, rather than making all 12 roles in advance.

Assume p=.95 physical success per attempt, a synthetic reader with true-positive β=.97, false-positive α=.03, and h independent readings required to be unanimously positive. Each disposable attempt is accepted as a correct receipt with probability a=p β^h, and falsely accepted with b=(1-p) α^h. Let A=a+b, t=a/A. Within a hard budget N attempts, exactly K=8 correct acknowledged basal roles are acquired with probability

    P_episode = P[Binomial(N,A)≥8] × t^8,

assuming the first eight accepted receipts correspond to eight distinct needed roles and the source knows which role to try next. This is a *stronger address-specific sensor* than an undifferentiated whole-material pass/fail report.

For h=2 and N=13, episode reliability=.99833629 and 20-episode reliability=.96724654. A source performs 8.94796 attempts on average before eight receipts or exhausting the cap, with 17.8959 binary readings. It is cheaper than 20 attempted seed structures only if each binary reading costs <(20-8.948)/17.896≈0.618 of the cost of a seed attempt (excluding fixed control costs). For h=3, N=14 gives P_20=.978630; h=1 can never give P_20≥.95 in this model, even with an unlimited attempt budget, due to false acceptance.

A 200,000-run independent Monte Carlo check of h=3,N=12 yielded 0.98574 ± .000265 versus exact 0.985382 for one episode (difference about 1.35 standard errors).

**Shared false-receipt episodes** defeat replication of readings. With h=2,N=13 and 0.3% per-attempt systematic all-positive events, the exact synthetic 20-episode reliability falls from .967247 to .942031; 0.5% yields .925591. More repetitions of the *same* corrupted physical state cannot fix that.

## 3. Pioneer survival: short-lived template no-go under uncompensated losses

After two successful pioneer seeds appear in an AND triad, suppose maturation of the third role is exponential at rate γ and each pioneer expires at rate λ. If any expiry before maturation irreversibly aborts startup, competing exponential clocks give

    P_triangular_maturation = γ/(γ+2λ).

Across 4 triads and 20 independent generation episodes, the strict uninterrupted reconstruction probability is [γ/(γ+2λ)]^80. To achieve ≥95% from *this loss mechanism alone* requires γ/λ≥3118.3162; with γ/λ=100, P=.20511, and with 4000 P=.96080. Direct exponential-race Monte Carlo (300,000 draws) agreed within sampling error.

This does NOT imply real pioneers need to mature thousands of times faster than they decay. It says that **a protocol that cannot renew an expired pioneer and cannot hold it until downstream completion** incurs a severe repeated-lifecycle penalty. Retries, spatial redundancy, continuous source manufacture, and a reversible held seed are candidate ways around it, with explicit resource charges.

### Two distinct escrow rules

Physical escrow: a temporary seed structure should not be released until downstream functional maturation has independently been certified. In a model with 80 fatal release opportunities and independent per-release premature-release probability f, ≥95% survival requires f≤1-.95^(1/80)=.0006409607. An ideal two-reading false-positive gate with α=.03 gives f=.0009 and only .93050 survival; an independent three-reading gate gives f=.000027 and .99784 survival. This analysis conditions on successful construction otherwise and cannot be interpreted as total system reliability.

**Genetic escrow is stronger.** In a fully assembled AND triad the temporary A pioneer can be withdrawn from the *material* after C forms, yet deleting the inherited ability to manufacture A may make its descendant unable to start from fresh feed. If founder now produces only pioneer B, then both A and C require a missing partner and the next episode stalls. Parent function can remain 100% while its ability to reproduce that function becomes 0%. A genetic pioneer instruction may be deleted only after demonstrating de novo closure with the altered source programme, not because the mature parent no longer physically needs that seed.

A selected deletion mutant can be favored under parent-only selection if its pioneer-biosynthesis cost is lower. With cost c=.1 to a complete source genotype, a deletion mutant initially at 1% and identical parent performance rises to ~84.9% after 60 idealized common-scaffold transfers. On a fresh-source transfer without old material, those mutants cannot bootstrap. In a source-closed functional selection with β=.97, α=.03, complete genotype expected reproductive weight (1-c)β=.873 and deletion genotype expected weight α=.03, restoring the correct selection direction. High external-rescue probability can reverse it again; the ideal threshold is s>((1-c)β−α)/(β−α)=.8968 for an independent helper rescue model.

## 4. Physical candidate and equally informed alternative

Prefer a founder-autogenic extracellular seed matrix to external prepatterned DNA strands. The 2026 Hammad et al. Advanced Materials DOI 10.1002/adma.74312 experimentally demonstrated *E. coli* secretion and self-assembly of genetically encoded curli-like beta-solenoid fibres, with modifiable displayed binding domains; this supports a way to manufacture basal structural material from genetic instructions. It does not demonstrate three mutually dependent addressed roles, seed receipts, role-specifying fate switches, or source-closed hereditary learning. The 2025 iDP2 bacterial surface display system (PNAS DOI 10.1073/pnas.2510167122) demonstrated sequence-dependent cellular condensation/segregation, not de novo fate conversion at site-specific matrices. The 2025 DNA-addressed microbial assembly DOI 10.1126/sciadv.ads8651 used DNA functionalization of cell surfaces rather than showing genotype-encoded automatic fabrication of every externally supplied DNA address. The 2026 Nature synthetic differentiation paper DOI 10.1038/s41586-026-10259-3 established founder-derived programmable fates, not a material vacancy-to-fate feedback writer. These components must not be conflated.

A concrete first testbed would be three distinguishable structural roles with pairwise prerequisites (a 3-node AND bootstrap trap): a complete founder synthesizes two independently functional pioneer surfaces from fresh feed; the third role matures at their mutual interface; temporary pioneers are removed only after a verified permanent structural contribution; clonal descendants must recreate the full system with **no inherited extracellular seed**. Compare directly to an equally informed external engineer supplying the two starter surfaces, and to a simpler single-role autogenic biofilm which trivially nucleates. The former is likely more efficient but fails the specified autonomous origin-of-structure goal; the latter is easier but does not demonstrate cooperative-bootstrap learning.

Remaining unsolved physical interfaces: (i) role-specific pioneers made by a single founder without externally preformed addresses, (ii) an independent functional receipt distinguishing correct structural maturation from occupancy/force-only decoys, (iii) source-linked inheritance of the complete pioneer repertoire, and (iv) final mechanical/hydraulic service independent of temporary support and unlinked helpers. No claim of integrated biological capability or novel pure mathematics.

Executable checks: `astra_xh2_bootstrap_seed_research.py`, plus `astra_xh2_bootstrap_seed_checks.json`, `astra_xh2_bootstrap_lifetime_checks.json`, and `astra_xh2_bootstrap_receipt_robustness.json`.

## 5. Fourth attack: can end-to-end experiments reveal the hidden bootstrap order?

For a common independent probability p of producing each candidate basal role, the network's true probability of completing from fresh feed is a polynomial R(p). If its minimum source pioneer cardinality is m and N_m minimal-cardinality seed sets exist, then R(p)=N_m p^m+O(p^(m+1)). Accordingly the logarithmic response to changing general founder nucleation rate is

    lim_{p→0} d log R(p)/d log p = m.

This suggests a **phenotype-only bootstrap-order assay**: titrate a common source seed opportunity, then infer the minimal number of jointly required basal origins from the low-probability slope. The test does not identify which roles are essential, and it requires that p controls those seed events independently and uniformly without changing downstream completion or the reporter. Correlated nucleation, independently changing growth, or changing outside helper availability invalidate the inference.

A decisive sampling obstruction exists. For the four-triad AND example R(p)=(3p²-2p³)^4 and the finite-p log slope is exactly 8-8p/(3-2p). At p=.05 the slope≈7.862, but R≈2.763e-9: approximately 3.62e10 independent whole-material constructions are needed even to obtain 100 expected passes. At p=.25, R≈.000596 and ~167,772 trials give 100 expected passes, but the apparent slope is only 7.2 rather than the true asymptotic order eight. At p=.5 the apparent slope is six. Thus, phenotype-only dilution could in principle estimate the *order of cooperative bootstrap*, but may be impractical exactly where high-order dependence is scientifically interesting. Local causal probes or source-labelled pioneers remain necessary for useful efficiency.
