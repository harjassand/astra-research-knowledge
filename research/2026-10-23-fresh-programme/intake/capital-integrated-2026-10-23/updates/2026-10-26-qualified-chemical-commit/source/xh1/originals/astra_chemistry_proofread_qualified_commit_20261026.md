# Astra Chemical Invention — Precommit Proofreading With Covalent-Qualified Advancement

Analytical/computational investigation, 26 October 2026. Not an experimental chemical apparatus, novel proof of kinetic proofreading, or demonstration of a civilisation-changing capability. Sources and executable checks below.

## Problem and change of approach

An anchored, positionally registered DNA/PNA synthesis should let each molecule advance through chemically correct products at its own rate. On failed coupling, retain the same competent rooted parent. A DNA motor moving, NHS hydrolysis, transient donor docking, or donor activation do **not** imply that a correct amide has formed. Wrong stable amides may persist; nominal full mass does not imply sequence connectivity. For a programme of L steps, fidelity and correct-product yield both matter.

The experimentally closest established system is Joshi, Romanens, Winssinger 2025 (DOI 10.1021/jacs.5c00708): s-NHS-activated, azide-masked PNA4 primer extension, two sequential cycles with wash/PMe3, a 256-PNA4 mixture, two-minute reaction half-time under a studied condition. The paper directly reports terminal single mismatches with near-ambiguous 1:1 MALDI peak intensities, downstream preferential extension of the matched parent with 6:1 observed product ratio, and a repeatedly unreactive bead-bound fraction. The 6:1 MALDI product ratio is **not** a measured dissociation ratio, general forward rate ratio, or per-step true/false readout sensitivity. The 256 mix supports primer extension, not proof of one-pot general thousand-step fault-tolerant manufacture.

The 2024 Mukherjee/Sengar/Cabello-Garcia/Ouldridge paper (DOI 10.1021/jacs.3c14673) experimentally demonstrates DNA fuel-consuming, nonenzymatic kinetic proofreading during **DNA dimerization**. Kinetic proofreading itself dates at least to Hopfield's 1974 theory. The 2026 Mitra/Mukherjee/Jurinovic/Ouldridge work (DOI 10.1021/jacs.6c03709) experimentally demonstrates DNA-strand associative-toehold catalysis and explicitly discusses covalent joins as a possible alternative way to make an associative toehold; it does not show amide-qualified advancement. The experimental integration and control of wrong organic bonds remains open.

## Result 1: Post-reaction filtering does not rescue stable wrong amides

One chemical attempt yields correct irreversible PNA amide p, wrong irreversible amide w, parent death d, harmless failed parent f=1-p-w-d. If a failed parent can retry indefinitely, false advancement on failures is h, correctly joined product is eventually accepted with probability A_C, wrong joined product with A_W, the absorbing-stage probabilities are exactly

    G = p*A_C/(p+w+d+f*h)
    B = (w*A_W+f*h)/(p+w+d+f*h)
    D = 1-G-B.

Per programme of length L, fraction of original roots yielding an entirely correct product is G^L; purity conditional on a full-length output is [G/(G+B)]^L; fraction yielding any full-length output is (G+B)^L. They must not be conflated.

For a correct reader that passes per attempt r_C and irreversibly rejects/culls per attempt c_C (otherwise harmless retry), its eventual accept is A_C=r_C/(r_C+c_C). Analogously A_W=r_W/(r_W+c_W). If wrong products are endlessly retested and *never* culled (c_W=0), then A_W=1 for any positive r_W: even arbitrarily slow incorrect readers eventually accept. A single-read filter can improve conditional purity but generally sacrifices high full-chain yield by culling correct products too.

Even with A_C=1, A_W=0, h=d=0, correct-root manufacturing yield is upper bounded by [p/(p+w)]^L. E.g., p=.6,w=.003,L=1000 gives **0.682%** maximum full-correct yield from starting roots. For 99% full-chain yield in this model requires w/p <= (.99)^(-1/1000)-1 = 1.0050e-5. Thus robust pre-bond wrong-product prevention, or a real error-excision/repair chemistry, is necessary for long products.

Verified in `astra_chemistry_checkpoint_limits_20261026.py` with exact absorbing probabilities and simulated repeated reads. Numerical reader comparison: with p=.6,w=.003, per-read correct pass .8, wrong false pass .008, repeated unlimited reads with no rejection still give only .682% entirely correct 1000-step product; one-shot pass/cull can produce high conditional purity but destroys practical full-length yield. These numbers are hypothetical.

## Result 2: Precommit fuel-consuming kinetic proofreading

Suppose correct and wrong donors arrive at rates λ_C, λ_W. The donor must survive n equal-rate forward checkpoint/chemical-commitment transitions, each at k, competing with donor dissociation u_C or u_W. Crucially, every dissociation resets the whole current checkpoint, without damaging the chemically competent parent. There is no chemistry before the nth transition, and that last transition *is* the irreversible bond. Per arrival, the probability of chemical commitment is q_i=[k/(k+u_i)]^n. After arbitrary retries, wrong/right product odds are exactly

    Odds_wrong/correct = (λ_W/λ_C) * [(k+u_C)/(k+u_W)]^n.

The independent renewal time is (mean wait for donor + mean duration of one bound trial)/(probability a trial commits); complete derivation and exact CTMC verification in `astra_chemical_proofreading_memory_20261026.py`.

Purely illustrative case λ_C=λ_W=.05/s, k=.15/s, u_C=.05/s,u_W=.5/s: n=10 gives correct fraction .999992394 per bond, 99.2423% over 1000 independent steps, mean 725.82 s per bond, and unmeasured lifetime requirements. n=12 gives 99.9280% over 1000 and 21.765 minutes per bond. No inference that Joshi's PNA fourmers have these rate ratios, or that DNA circuits progress at k=.15/s on those bound donors.

## Result 3: Checkpoint-memory bypass

Extend the CTMC: if bound donor departs at checkpoint stage j, gate retains that progressed stage with probability m, and resets to 0 with 1-m; a new *different* donor can then bind the already progressed controller. Exact solution of the 3n-state generator shows this bypass destroys exponential selectivity. In the n=10 hypothetical example, m=.001 lowers 1000-step correctness to .93875, m=.01 lowers it to .56782. Maintaining ≥.99 requires m <= 4.3983e-5 when there are no other failures. Explicit stochastic simulations agree with the generator.

A gate not reset by ligand departure is therefore not equivalent to ligand-conditioned proofreading. Necessary physical interlock: checkpoint progress is jointly owned by **the particular donor–parent complex**, or it is destroyed/invalidated on separation. Simply presenting a persistent fuel-advanced DNA state next to a growing chain is insufficient. A donor carrying its authorization away and later using it on another root is a related cross-program bypass.

## Result 4: Premature chemistry defeats arbitrary proofreading

Suppose each of the n-1 intermediate bound states has irreversible premature amide-coupling hazard ell, even though the intended last step has normal k. Off-rate u_i competes with checkpoint progression k and leak ell. Exact probability of a committed bond from one docking is

    q_i(n) = [ell/(u_i+ell)]*(1-(k/(k+u_i+ell))^(n-1))
            + (k/(k+u_i+ell))^(n-1)*k/(k+u_i).

For any ell>0, as n→infinity,

    q_wrong/q_right -> (u_C+ell)/(u_W+ell),

assuming equal arrival rates. **Infinite proof checks eventually lose their benefit** because the desired proof-completed pathway vanishes while premature chemistry survives. There is generally a finite optimum n. This calculation matches the independent absorbing-chain generator in `astra_chemical_commitment_leak_20261026.py`.

For the illustrative n=10 system, the maximum ell for ≥99% correct 1000-step output is ~6.883e-8 /s when m=d=0. At ell=1e-6 /s, correct full-chain yield is ~95.78%; at 1e-5 /s it is ~69.65%. Those numbers are specifications within the hypothetical model, not measured premature-amide rates. **Already activated NHS PNA cannot be assumed compatible with delayed authorization without measuring or physically blocking amide chemistry in all intermediate states.**

## Result 5: Joint wrong chemistry, memory and chain death

The exact expanded CTMC contains: unbound gate state U_j, correct bound donor B_C,j, wrong bound donor B_W,j, target bond, wrong bond, root death. It allows checkpoint-memory m, premature bond ell in earlier states, root death d in all transient states, and background unbound wrong reaction hazard bg. Full matrix verified against each specialized model in `astra_joint_chemical_gate_20261026.py`.

With the same hypothetical base parameters, n=10, m=1e-5, ell=1e-8 /s, d=1e-9 /s gives 99.080% full-correct root yield over 1000 steps (no background bg). Optimizing n from 1 to 25 selects n=12 with 99.679% under those values. If root death rises to 1e-8 /s, the best among tested n gives ~98.697%; if memory or premature chemistry worsens, the optimum shifts and long product yield declines. Checkpoint count is therefore a multi-error optimization, not a scalar fidelity improvement.

## Result 6: A latent-chemistry alternative and its new risk

Manicardi/Cadoni/Madder 2020 (DOI 10.1039/D0SC04875E) experimentally demonstrated template-guided visible-light PNA ligation using a stable, pro-reactive furan that is oxidized to an activated keto-enal through localized sensitizer-produced singlet oxygen. The paper reports PBS pH7.4, 25 C and 5 µM solution PNA probes in the explored conditions, template-dependent ligation against mismatch/scrambled controls, and surface-format operation. Depending on amine/hydrazine nucleophile, products include pyrrolidinones/pyridazinium species. **These are not ordinary NHS-PNA amides or an established 256-PNA fourmer repeated-growth system.** It demonstrates a latent bond precursor under near-neutral conditions and is a serious alternative to continuously activated NHS donor chemistry if a DNA checkpoint can control the activator proximity. The experimental chemical network must still be shown to regenerate a suitable masked new terminus and remain stable over repeated stages. Existing use of photooxidation can damage nucleophilic handles under some conditions.

Photoactivation itself must not be mistaken for bond formation. A newly activated but still unjoined donor can depart, diffuse, and react elsewhere. If final-stage activated bound donor undergoes correct coupling hazard k_b, dissociates at u, and is quenched while bound at q_B, followed by free wrong reaction beta competing with quench q_F and removal mu, the unconditional wrong-reaction probability per activated donor is exactly

    P_wrong_after_activation = [u/(k_b+u+q_B)] * [beta/(beta+q_F+mu)]

in a simple exponential competing-hazards model. With illustrative k_b=.1/s,u=.3/s,q_B=0, achieving under 1.005e-5 per-stage error from this pathway requires beta/(beta+q_F+mu) < 1.34e-5, i.e. q_F+mu > 7.46e4 beta. This is *not* an experimentally measured furan-oxidation condition. A competent parent must not be attacked by a departing activated donor, and waste must not poison DNA recognition.

## Selected architecture and strongest equally informed comparator

Selected research mechanism, **not acquired experimentally**:

1. Keep a permanently rooted competent polymer end and an adjacent registered DNA position. Use the actual PNA amide system as low-risk chemical baseline, with external feed–wash–deprotect cycles and failed-parent retry.
2. If attempting prebond proofreading, employ an initially *noncommittal* donor and fuel-driven, DNA-based recognition steps whose state resets on donor departure. Couple organic chemistry only after qualification, not while the NHS donor is already active.
3. Prefer a ligand-tethered local latent bond activation chemistry to a persistent permissive gate. Compare the published pro-reactive furan/PNA system; it has different stable products, possible photooxidative side reactions, and no established serial protected-chain growth.
4. After successful bonding, distinguish actual covalent continuity from temporary contact by disrupting reversible template docking and removing unjoined material. A retained distal sidecar could reconstruct an associative toehold with the rooted product and allow fuel-mediated instruction advance. This borrows the topology principle discussed in Mitra et al. 2026 but **requires experimental organic-bond integration**. A stable wrong covalent product may still pass a continuity-only read, so position/sequence discrimination must be separate.
5. New amino group must remain masked until the previous site is closed and the next position is available; avoid double incorporation and global premature unmasking.

The strongest comparator is **plain staged azide-masked NHS PNA** with ordinary DNA templating, existing surface washing and PMe3 deprotection. This already avoids a separate motor that guesses whether chemistry happened; a failed parent remains at its old chemical terminus, and an incorporated donor is azide masked. The comparator has major unresolved long-term fidelity, permanent stalled populations, off-site stable products, and positional registration constraints, but far fewer new physical interfaces. An enhanced DNA proofreader must produce higher correct-product yield and/or broader chemicals *at comparable costs*, not merely a favorable DNA fluorescent signal.

## First decisive discriminators (not lab work performed)

- Contrast correct and terminal-mismatch PNA with missing donor, hydrolyzed donor, already linked product, and matched noncovalently bound donor. Identify *site-specific covalent bond* and chemical terminal competence rather than just toehold fluorescence or mass of full product.
- Check chemically premature bond formation in every pre-commit DNA controller state, not just final fluorescence. If ell cannot be suppressed, reject the prebond gating architecture.
- Dissociate donor deliberately after partial checkpoint progression; determine whether subsequent wrong donors can use the retained DNA state. If m too large under the intended kinetics, reject the gate.
- During photoactivation, separately assay oxidized-but-not-yet-coupled donor and its off-target acylation/ligation, comparing active donor chemical quench and scavenging with a simple wash.
- Check 2 programmes in one bath with deliberate wrong-site and cross-program donors and mixed templates; verify the covalent identity of rooted outputs. Small single-step tests must not be extrapolated as 1000-step success.
- For a 99% correct 1000-step programme with independent per-stage error hazard and zero errors observed, demonstrating an error probability below about 1e-5 at 95% confidence would demand ~300,000 independent informative stage-level trials (binomial model), absent mechanistic rate-based inference. MALDI peak intensity ratios alone do not supply this confidence.

## References

1. Joshi, Romanens & Winssinger (2025), *Sequencing of d/l-DNA and XNA by Templated-Synthesis*, JACS, DOI 10.1021/jacs.5c00708.
2. Mukherjee, Sengar, Cabello-Garcia & Ouldridge (2024), *Kinetic Proofreading Can Enhance Specificity in a Nonenzymatic DNA Strand Displacement Network*, JACS, DOI 10.1021/jacs.3c14673.
3. Mitra, Mukherjee, Jurinovic & Ouldridge (2026), *Fuel-Driven Catalytic Molecular Templating*, JACS, DOI 10.1021/jacs.6c03709.
4. Manicardi, Cadoni & Madder (2020), *Visible-light triggered templated ligation on surface using furan-modified PNAs*, Chemical Science, DOI 10.1039/D0SC04875E.
5. Hopfield (1974), *Kinetic proofreading: a new mechanism for reducing errors in biosynthetic processes requiring high specificity*, PNAS, DOI 10.1073/pnas.71.10.4135.
6. McKee et al. (2011), *Peptidomimetic bond formation by DNA-templated acyl transfer*, Org Biomol Chem DOI 10.1039/C0OB00753F (separate mild thioester route).

## Executable verification

- `astra_chemistry_checkpoint_limits_20261026.py`
- `astra_chemical_proofreading_memory_20261026.py`
- `astra_chemical_commitment_leak_20261026.py`
- `astra_joint_chemical_gate_20261026.py`
- `astra_photoactivation_escape_20261026.py`

All five scripts executed and their stated numerical/assertion checks passed. None contains empirical rate fitting or establishes experimental novelty of the proposed integration.

## Further result 7: Information-theoretic no-go for connectivity-only organic bond receipts

Correctly rooted organic bond C and wrong-site stable bond W may carry the same DNA sidecar signals. For all available controller observations O with distributions P_C and P_W, a randomized acceptance test δ(O)∈[0,1] satisfies

    E[δ|C]-E[δ|W] <= TV(P_C, P_W).

This follows from the variational characterization of total-variation distance. If P_C=P_W, no postbond controller can distinguish C from W, regardless of fuel expenditure, logic depth, or amplification, **unless it accesses additional chemistry-sensitive information**.

A reader admitting correct product with probability alpha and stable wrong with beta produces per-stage admitted correct fraction p alpha/(p alpha+w beta). At L stages, full correct conditional fraction [1+(w/p)(beta/alpha)]^-L. To make it at least F, necessity is

    beta/alpha <= (p/w)*(F^(-1/L)-1).

With p=.6, w=.003, F=.99, L=1000 and alpha=.99, the ratio must be ≤.00201007727, beta ≤ .00198997650, and thus TV≥alpha-beta=.988010024. This is a deliberately stringent hypothetical requirement, not a measured Joshi wrong-site acceptance curve. Continuity-only toehold reconstruction cannot certify bond SITE if wrong and right products have the same DNA observable law. This is the true pre-vs-post chemical identification obstacle.

## Further result 8: Physical clearance and registration jointly constrain reliable receipts

Suppose unjoined PNA donor disappears with exponential hazard u and correct rooted register is irreversibly lost with v (0<v<u). A one-time presence test after wash t admits correct with alpha=e^-vt and admits unjoined with beta=e^-ut. To reach a required false/true ratio ε, t >= ln(1/ε)/(u-v). To retain at least F of correct roots across L such washes, require v*t <= -ln(F)/L. These can coexist only when

    v <= u*(-ln F/L)/(ln(1/ε)-ln F/L).

If ε=.002010077, F=.99,L=1000,u=.3/s, this requires v <=4.8556e-7 /s and t≈20.70 s at the boundary. This tests *unjoined donor* vs rooted product, not wrong stable rooted product: for that latter comparison wash signatures may be identical and inequality is not useful. Conditions: no rebinding, independent exponential loss, no additional chemistry error. Actual multivalent bound PNA or hydrolyzed donor can violate the u assumption. Exact calculations independently checked by `astra_chemical_receipt_identifiability_20261026.py`.

## Primary chemistry cross-check (2020 latent PNA)

Manicardi/Cadoni/Madder, Chemical Science 2020 DOI 10.1039/D0SC04875E, report visible-light singlet-oxygen conversion of furan-bearing PNA into reactive keto-enal, leading to template-dependent ligation. Crucial result: mismatched/scrambled 7mer PNA under the activated regime produced **oxidized furan probe** but no stable ligation band, while matched generated ligation. This is exactly an experimental demonstration that activation is NOT equivalent to successful organic bond formation; reactive oxidized donor remains a distinct possible failure/waste state. This compound must be analyzed for mobility, stability, and offsite reaction, rather than treating fluorescence or light-triggered oxidation as a bond receipt. Authors used USDS-PAGE partly because even HPLC could mistake very stable PNA duplex for covalent ligation.

## Resolved design boundary

The strongest presently credible design stays a **staged masked NHS-PNA reference architecture** until the chemically independent improvements (DNA prebond proofreading + donor-state self-reset + latent bond activation + safe activated-donor clearance + sequence-resolving covalent receipt) are acquired. Prebond proof can prevent stable wrong amides; a postbond DNA receipt can reject unjoined donors and permit instruction motion; neither replaces the other. The latent 2020 furan chemistry is a separate chemistry family with different stable products and uncertain protected-chain serial-growth compatibility, so cannot be directly substituted for Joshi's NHS-PNA donor. The equal-information comparison is actual yields of fully correct multi-stage molecules from an initially equal number of roots, measured chemical bond site and terminal competence, not individual DNA circuit fluorescence.

### Combined 99% budget (clarification)

Two separately allocated 99% guarantees (product purity, root-registration retention) multiply to only 98.01%, not 99%. To target a total of 99% from these two independent mechanisms alone, give each a sqrt(.99)=.9949874 budget across 1000 instructions. For p=.6, w=.003 this demands false/true receipt ratio eps=.001005036, and, with unjoined PNA u=.3/s and pure single-exponential donor/registration wash, the joint boundary is wash 23.0091 sec and v<=2.1840e-7/s; the two factors then combine to 0.99. This remains inapplicable to wrong covalently rooted products and must not be read as a measured achievable registration-lifetime specification. Extra hazards would require additional budget.
