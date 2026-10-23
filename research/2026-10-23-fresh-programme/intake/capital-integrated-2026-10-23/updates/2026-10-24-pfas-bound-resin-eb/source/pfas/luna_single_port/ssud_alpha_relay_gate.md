# PFOS α-hydrodefluorination → SsuD relay: balanced, unvalidated, reject as lead

**Decision.** The proposed relay is chemically balanceable, but it is not presently a demonstrated PFOS pathway or a better treatment operation. The necessary enzyme substrate is a *specific positional isomer* that the available PFOS H/F-exchange evidence does not identify, and there is no evidence that SsuD accepts its perfluoroalkyl tail. This kills it as an active lead; it does not prove the chemistry impossible. No experiment was run.

## The exact substrate gate

Write PFOS as \(\mathrm{CF_3(CF_2)_7SO_3^-}\). The SsuD-active motif characterized in ordinary alkane-1-sulfonates is \(\mathrm{RCH_2SO_3^-}\), with α-hydrogens at the carbon attached to sulfonate. Native PFOS has \(\mathrm{R-CF_2-SO_3^-}\) there instead. For the proposed α-CF₂→CH₂ gateway, both fluorines on that one carbon must be replaced with hydrogen, giving the particular geminal product

\[
\mathrm{CF_3(CF_2)_6CH_2SO_3^-}
 = \mathrm{C_7F_{15}CH_2SO_3^-}
 = \mathrm{C_8H_2F_{15}SO_3^-}.
\]

With \(R=\mathrm{C_7F_{15}}\), that formation step balances as

\[
\mathrm{C_8F_{17}SO_3^- + 2H^+ + 4e^-}
\longrightarrow
\mathrm{RCH_2SO_3^- + 2F^-}.
\]

The two-H molecular formula alone does not establish the needed structure: the same \(\mathrm{C_8H_2F_{15}SO_3^-}\) formula includes positional isomers where one or both H atoms are away from the sulfonate-adjacent carbon, which do not present a \(\mathrm{CH_2-SO_3^-}\) motif. Here \(n\) counts H/F exchanges from PFOS, so the balanced series is \(\mathrm{C_8F_{17-n}H_nSO_3^-}\) (\(n=1\): \(\mathrm{C_8F_{16}HSO_3^-}\); \(n=17\): \(\mathrm{C_8H_{17}SO_3^-}\)). The 2026 plasmon-enhanced PFAS study reports those endpoint examples and states that substitution can occur at multiple carbon sites. Its n=2 mass class therefore does not establish this geminal α-H isomer. An α-CHF sulfonate would retain one α-H and is another possible but untested SsuD substrate; it is a different hypothesis from the proposed α-CF₂→CH₂ relay. The paper's MS/MS assignment supports a family of hydrofluorosulfonates; it does not show SsuD turnover on any PFOS-derived intermediate.

## Conditional reaction and cofactor ledger

The primary SsuD isotope-effect study used 1-octanesulfonate and found a primary kinetic isotope effect of \(3.0\pm0.2\) after replacing its C1 hydrogens with deuterium. This supports α-proton abstraction as a kinetically important step. The study is evidence for the ordinary alkane-1-sulfonate chemistry, not for acceptance of \(\mathrm{C_7F_{15}CH_2SO_3^-}\). The perfluoroalkyl-tail substrate, its binding, and its turnover are unreported.

Using common aqueous ionic forms, the conditional SsuD step and SsuE flavin-recycling step are:

\[
\begin{aligned}
\mathrm{RCH_2SO_3^- + FMNH_2 + O_2}
&\longrightarrow
\mathrm{RCHO + SO_3^{2-} + FMN + H_2O + H^+},\\
\mathrm{FMN + NADPH + H^+}
&\longrightarrow
\mathrm{FMNH_2 + NADP^+}.
\end{aligned}
\]

Adding these gives

\[
\mathrm{RCH_2SO_3^- + O_2 + NADPH}
\longrightarrow
\mathrm{RCHO + SO_3^{2-} + H_2O + NADP^+}.
\]

This is one NADPH equivalent per SsuD substrate if SsuE supplies the reduced flavin. E. coli SsuE is [NADPH-dependent](https://www.ncbi.nlm.nih.gov/gene/945947). The equations use common aqueous ionic forms. They also make clear that the immediate sulfur product is **sulfite**, not sulfate. If sulfate is the mineralization endpoint, a separate oxidation is required, for example \(\mathrm{SO_3^{2-}+\tfrac12 O_2\to SO_4^{2-}}\), and sulfate must be measured against background.

An aldehyde-dehydrogenase-type oxidation would balance as

\[
\mathrm{RCHO + H_2O + NADP^+}
\longrightarrow
\mathrm{RCOO^- + NADPH + 2H^+}.
\]

For \(R=\mathrm{C_7F_{15}}\), \(\mathrm{RCOO^-}\) is perfluorooctanoate (PFOA), not mineralized carbon. This aldehyde-oxidation step is also an assumption: acceptance of \(\mathrm{C_7F_{15}CHO}\) by a chosen aldehyde dehydrogenase is not established here. The displayed cofactor cancellation requires an NADP⁺-dependent aldehyde oxidation; with an NAD⁺-dependent enzyme, include an explicit transhydrogenase or other cofactor-regeneration balance. If the steps couple ideally through a compatible NADP pair, the NADP(H) pair cancels and the three chemical steps sum to

\[
\mathrm{C_8F_{17}SO_3^- + 4e^- + O_2}
\longrightarrow
\mathrm{C_8F_{15}O_2^- + SO_3^{2-} + 2F^-}.
\]

Carbon, fluorine, sulfur, oxygen, hydrogen, and charge balance in this conditional equation. It describes removal of two fluorines as fluoride, transfer of the PFOS carbon into PFOA, and reduction of sulfonate sulfur to sulfite. It does **not** describe complete defluorination or carbon mineralization. The same 2026 plasmon-enhanced PFAS study reports the PFOS H/F-exchange series through \(\mathrm{C_8H_{17}SO_3^-}\), a fully hydrodefluorinated product that retains sulfonate. Thus C–S cleavage/sulfate is a separate sulfur-fate claim, not a prerequisite for counting all 17 fluorines as removed from the parent.

## Comparison and stop condition

The incumbent comparison is unfavorable. Guan et al.'s Pd–TiO₂ photo-electrochemical reduction (PER) already reports about 90% PFOS desulfonation; following PER with boron-doped-diamond electrooxidation brings measured defluorination to about 100% under their reported condition. That system starts from PFOS and does not require a regioselectively prepared α-CH₂ sulfonate or a two-enzyme relay. The relay would need to show a matched whole-process benefit (energy, reagents/cofactors, time, waste streams, and closed F/S inventories), not merely produce PFOA or sulfate. The 2026 plasmon-enhanced study is a second direct reductive comparator: it reports near-stoichiometric fluoride evolution for PFOS in its tested system, further weakening the case that an enzyme relay solves the main defluorination bottleneck. Neither comparator implies field-ready performance in dilute complex water; they do set a demanding bench comparator.

The relay stays **not established** until both necessary links are shown: (1) a quantitatively important, site-confirmed \(\mathrm{C_7F_{15}CH_2SO_3^-}\) fraction is formed from PFOS under the proposed upstream treatment; (2) SsuD/SsuE measurably consumes that substrate and releases the corresponding fluorinated aldehyde plus sulfite. The subsequent aldehyde-to-PFOA step and its value over direct PER→BDD remain separate gates. No novelty, efficacy, catalyst turnover, or cost claim follows from stoichiometric feasibility.

## Sources

Two new primary sources used for this gate:

1. Robbins & Ellis (2014), [Steady-state kinetic isotope effects support a complex role of Arg226 in the proposed desulfonation mechanism of alkanesulfonate monooxygenase](https://doi.org/10.1021/bi401234e), *Biochemistry* 53, 161–168. Primary SsuD mechanistic evidence; the C1-deuterated substrate was octanesulfonate.
2. Özce et al. (2026), [Plasmon-enhanced reductive defluorination of PFAS in water under ambient conditions](https://doi.org/10.1038/s44221-026-00690-1), *Nature Water* 4, 1166–1176. Primary PFOS hydrodefluorination evidence; observed nH product families and fluoride evolution, without demonstrating SsuD substrate acceptance.

Existing direct process comparator already documented in [`pfos_capture_cleavage_candidate.md`](pfos_capture_cleavage_candidate.md): Guan et al. (2026), [Photo-electrochemical reduction of PFAS in complex water matrices](https://doi.org/10.1038/s41467-026-71263-9), including PER→BDD. This is a comparator, not a third new enzyme-relay source.
