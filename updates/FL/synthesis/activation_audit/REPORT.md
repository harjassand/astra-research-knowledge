# FL regenerative molecular activation: independent audit

**Disposition:** the constant-hazard work/product inequality is correct under the pasted source's explicit idealized assumptions. It is an elementary competing-risk and work-accounting identity, not a new physical law. A useful extension is a renewal ledger with outcome-specific returned work and a uniform hazard-ratio bound that survives adaptive switching. Exact countermodels show why the source's $E/(\eta a)$ floor is not universal once partial losses or product-state recovery are allowed.

The conditional 6.14-eV-per-CO comparison is 5.8751 kWh/kg CO at nominal $M_{CO}=28.010$ g/mol. This exceeds the ISPT report's modeled 3.2 kWh/kg electricity case (and its 3.3 kWh/kg table with the stated AC/DC allowance). It is not above every complete-plant comparison: Topsoe's separate vendor FAQ gives 6–8 kWh/Nm³ for total plant energy, and the activation floor falls inside that range under either explicit Nm³-to-mass convention checked here. The defensible result is **unqualified and worse than the named matched-condition model**, not a universal full-plant energy no-go.

## What was checked

The provisional file work/FL-sources/temporal_PASTED_SOURCE.txt is indeed the regenerative-activation report, as the supplemental intake manifest says. Its SHA-256 is 7dfff79bddb5175067e4b90549b52c0c50fa5c9e5d9c2cc92f4e1a2f3b87d6ce. It is prose only. I found no original activation executable, source code, or executable checker in its bytes or the FL activation intake. The Python script in work/FL-sources/global/ belongs to the separate global-compatibility stream and was not used for this audit. The only program executed for this lane is the independently written, standard-library checker in code/check_activation.py.

The derivation and assumptions are in proofs/activation_bound.md. The checker gives exact rational renewal and mixture countermodels, evaluates finite-time hazard and unloading formulae, solves the 99% unloading threshold with Decimal arithmetic, and reproduces the unit conversions. Its saved output is results/ACTIVATION_CHECKS.json. It passed. This is bounded arithmetic verification, not a proof assistant, kinetic simulation, or validation of a physical device.

## Independent results

For constant competing hazards, the probability of a desired event by hold time $t$ is $p=a(1-s)$, where $a=\lambda_r/(\lambda_r+\lambda_\ell)$ and $s=\exp[-(\lambda_r+\lambda_\ell)t]$. If the molecular excitation is $E$, source-to-excitation energy efficiency is $\eta$, the surviving fraction returns fraction $r$, and unrecovered control work is $h$ per addressed attempt, the expected work/product is

$$
w(t)=\frac{E/\eta-rEs+h}{a(1-s)}
=\frac{E}{\eta a}
+\frac{Es(1/\eta-r)+h}{a(1-s)}
\ge\frac{E}{\eta a}.
$$

All failed activation is treated as unrecoverable, no work is returned from products, and unloading acts only on survivors. A nonzero overhead is divided by product probability. With $r=1,\eta=1,h=0$, the bound is attained for every finite $t>0$. Otherwise the energy-only optimum is the limiting hold $t\to\infty$, absent time or throughput penalties. This model therefore does not select a finite reaction/unload delay from energy minimization alone. In the loss-free, zero-overhead case, $w/E=r+(1-r)/p$: for $p=10^{-6}$ and 99% recovery, $w/E=10000.99$ (so $w=10000.99E$ per product). This shows why recovery percentage alone is insufficient when productive events are rare. If both hazards scale as the same binary-collision density factor, $\lambda_r=nk_r$ and $\lambda_\ell=nk_\ell$, density raises throughput but leaves $a$ and the ideal energy/product floor unchanged; density-dependent state populations or additional reaction channels require a new model.

For an ideal rigid rotor subject to a torque bound, $t_d\ge L_0/U_{\max}$. If a constant catastrophic loss hazard $\lambda_\ell$ acts during unload and work extracted before a later event remains stored, maximum deceleration from the outset maximizes recovered work. It gives

$$
r_{\max}(z)=2\int_0^1(1-u)e^{-zu}\,du
=\frac{2(z-1+e^{-z})}{z^2},\qquad z=\lambda_\ell t_d.
$$

This credits work already extracted before a later loss; using whole-pulse survival $e^{-z}$ would undercount. The 99% return threshold is $z\le0.03022704459947$. This result assumes reaction is closed during unload and the only competing unload event erases the remaining recoverable energy. If product chemistry continues during unloading, both cause-specific hazards and event-conditioned energy returns must be modeled together. Rotational coherence loss alone is not an energy-loss measurement.

The strongest safe generalization is standard renewal accounting. If an attempt succeeds with probability $q$, a productive attempt costs net $c_r$, and a failed attempt costs net $c_\ell$, then resetting to the same state after each failure gives exactly

$$
w=c_r+\frac{1-q}{q}c_\ell.
$$

Branch costs must be net of work that is actually returned and reusable at the declared boundary. At $q=1/10,E=1$, exact examples are $10E$ when every failure costs $E$, $1.9E$ when failures return 90% of $E$, and $E$ when both success and failure branches return 90%. These refute a universal $E/a$ lower bound after partial loss or product recovery is allowed. They are accounting examples, not evidence that any such molecular work return occurs.

For adaptive controls, a uniform pointwise ratio $\lambda_\ell\ge\kappa\lambda_r$ over every permitted state and history implies $\Pr(\mathrm{loss})\ge\kappa\Pr(\mathrm{product})$ by the counting-process compensator. If a terminal event occurs almost surely, $q\le1/(1+\kappa)$. With uniform branch-cost floors, the repeated-attempt floor is $\epsilon_r+\kappa\epsilon_\ell$. If a legal action can change the reaction/loss ratio, no policy-independent floor follows from one nominal or averaged rate pair.

A finite heterogeneous-mixture countermodel shows why pooling cause-specific rates can fail. Types A/B with weights $1/10,9/10$ and rates $(100,0),(1,9)$ have true yield $19/100$. Pooling the unweighted rates predicts $109/190$. With unit cost per attempt, the respective work/product figures are $100/19$ and the fictitious pooled prediction $190/109$. The surviving risk set changes type composition over time; it has no single constant cause-specific hazard pair.

This adaptive scope agrees with current capital and does not replace it. N777 states that a finite-state controlled generator preserves eventual target probability under arbitrary predictable switching if every legal generator satisfies $L^u q=0$ for the acquired full-configuration committor and absorption completes. A shared clock factor cannot change the eventual branch probability. N777 also warns that finite-window conditional yield can change through censoring. N783 requires a joint full-state transition/reward/cost law and declared retention horizon for repeated rewards; endpoint counts alone do not certify reusable excitation. The local N777 and N783 status is source_derived_unreviewed, with review and capability gates open. This audit closes neither gate and supplies no physical generator or reward kernel.

## CO₂ comparison and boundary correction

The 2023 CO₂ optical-centrifuge article reports $J_{\max}=364$ and $E_{rot}=6.14$ eV at 380 Torr. It shows a broad rotational distribution and identifies $J=364$ at the tail end, so 6.14 eV is a detected high-state value, not the mean energy of the centrifuged population. It also reports that a centrifugal barrier prevents dissociation at those energies; the observations are state-resolved spectra and rotation-to-vibration transfer, not CO production. The authors find that the fastest rotors do not significantly participate in observed inelastic energy-transfer dynamics; moderate states are the main contributors. [Chen et al., *Nature Communications* 14, 3227 (2023)](https://www.nature.com/articles/s41467-023-38873-z)

Using the exact SI electron-volt and Avogadro constants from [NIST CODATA 2022](https://physics.nist.gov/cuu/pdf/wall_2022.pdf), and nominal CO molar mass 28.010 g/mol based on [CIAAW 2024 standard atomic weights](https://ciaaw.org/atomic-weights.htm),

$$
1\ \mathrm{eV/molecule}
=\frac{(1.602176634\times10^{-19}\ \mathrm{J/eV})
(6.02214076\times10^{23}\ \mathrm{molecule/mol})}
{(3.6\times10^6\ \mathrm{J/kWh})(0.028010\ \mathrm{kg/mol})}
=0.9568540\ \mathrm{kWh/kg\ CO}.
$$

Thus 6.14 eV per addressed CO is 5.87508 kWh/kg. This is a per-addressed-product calculation only. If fraction $f_{\rm addr}$ of feed is addressed and only addressed molecules can make counted CO, that fraction cancels from energy per product only when unaddressed-feed handling uses no extra work; it still controls feed-basis yield and throughput. No ensemble-average activation energy follows from $J_{\max}$.

The process comparisons have different evidence and boundaries:

- ISPT's 2023 public SOEC upscaling report models an Air Liquide CO case specified at at least 96 mol% CO and 13 barg. It assumes 5,000 Nm³/h design capacity, 50% single-pass conversion, thermoneutral operation, liquefied high-quality CO₂ feed, and available waste heat. The use-case electricity figure is 3.2 kWh/kg CO. Table 6 lists 2.7 stack DC + 0.2 feed heat + 0.1 air heat + 0.2 compression. Table 12 adds 0.1 kWh/kg for an explicit 97%-efficient AC/DC conversion and gives 3.3 kWh/kg. This is modeled system electricity, not an independently demonstrated full-scale operating plant. The study describes high-quality liquefied CO₂ feed as available and assumes excess heat; those are boundary conditions, and the listed CO electricity total does not charge upstream CO₂ capture or liquefaction. [ISPT, *Next Level Solid Oxide Electrolysis*, 2023 report](https://ispt.eu/media/2023-SOE-public-report_ISPT.pdf)
- A 2022 Topsoe presentation reports a **stack** demonstration: 14,000 h, 30,000 Nm³ (35.5 t) CO, 3.44 kWh/Nm³, and Faradaic efficiency $99\pm1$%. This is not a complete-plant energy result. Using only that presentation's implied 1.1833 kg/Nm³ conversion gives about 2.907 kWh/kg for the stack; this derived stack figure remains distinct from system electricity and from the FAQ's separate plant range. [Topsoe presentation hosted by DOE](https://www.energy.gov/documents/shared-learnings-achieving-high-volume-hte-manufacturing-poul-georg-haldor-topsoe)
- Topsoe's product FAQ separately gives 6–8 kWh/Nm³ for total eCOs-plant energy versus 3–3.5 kWh/Nm³ for the stack, with standard 99 vol% CO product. [Topsoe eCOs plant FAQ](https://www.topsoe.com/hubfs/CAMPAIGNS/eCOs/FAQ_eCOs.pdf) Mass conversion depends on the normal-volume convention. The presentation itself implies 1.1833 kg/Nm³ from 35.5 t/30,000 Nm³, giving 5.07–6.76 kWh/kg; an ideal 0 °C, 1 atm gas conversion gives 1.2497 kg/Nm³ and 4.80–6.40 kWh/kg. The activation floor lies inside both illustrative ranges. These different boundaries and output specifications do not form a matched plant-performance comparison.

The direct conclusion is that the ideal high-J one-CO cycle cannot beat the 3.2–3.3 kWh/kg ISPT **modeled electricity case**. It has no demonstrated CO-producing reaction, compatible recovery, or process-level loading efficiency, so it is not a credible advantage candidate. The source's broader wording that the route “fails the energy comparison” is supported against that model but is not an all-full-plant theorem: the Topsoe FAQ range overlaps 5.875 kWh/kg under the stated conversions. With real activation and process losses added, the route remains unqualified and has no established advantage; whether it is worse than every full-plant CO installation is unknown from the cited boundaries.

## Physical prior and scope

The reported SiO⁺ + H₂ super-rotor experiment observes about a threefold reaction-rate enhancement, but in an ion trap at estimated H₂ density $7(1)\times10^6$ cm$^{-3}$, with reaction rates $0.18(3)$ min$^{-1}$ versus $0.05(2)$ min$^{-1}$ for the unpumped ion distribution. It cannot be combined with dense neutral CO₂ processing as if it supplied a compatible reaction-rate pair. [Venkataramanababu et al., *Nature Communications* 14, 4446 (2023)](https://www.nature.com/articles/s41467-023-40135-x)

The August 2026 helium-droplet preprint studies accelerating and decelerating ultraslow optical centrifuges, but emphasizes strong rotor–bath dissipation, rapid thermalization, and progressive loss of molecular alignment. A change or decay in the field-alignment signal is not energy returned as reusable work. [MacPhail-Bartley et al., arXiv:2608.25161v1 (25 Aug 2026)](https://arxiv.org/abs/2608.25161)

Neither the mathematics nor literature review establishes measured $\eta,a,r,h$, a molecular unloading trajectory, a product recovery pathway, or industrial CO conversion. Priority for the proposed combined operation remains unknown. The source's narrower experiment—measure molecular state populations and net optical work, then demonstrate less supplied work at fixed stable product output—remains a discriminator to test, not a passed gate.

## Reproducibility and evidence tier

Run from the workspace root:

    python3 work/FL-activation-audit/code/check_activation.py work/FL-activation-audit/results/ACTIVATION_CHECKS.json

The script uses only Python's standard library. Its assertions passed. The output is arithmetic/integrity evidence for the scoped formulas and examples; it is not a numerical integration of chemistry or independent physical validation. The source copy, relevant N777/N783 text, read ledger, exact input pins, and file hashes are frozen in this directory. MANIFEST.json covers every owned file other than itself.
