# Covalent isotope fractionation: screening record

Status: proposed operation; not experimentally validated; historical novelty unresolved.
No civilisation-scale advantage has been established.

## Proposed operation

Electrochemically load a mixed H/D population on supported graphene. Apply a
partial oxidative stripping pulse to preferentially remove H. Retain the
remaining D-rich covalent inventory, then separately test recovery into a product
fraction. The stripping experiment must first work in a mixed-isotope electrode;
pure-H and pure-D voltammograms are not a substitute.

## Exact physical question

Can an electrode with a *measured* initial surface D atom fraction 0.10 reach a
surface D atom fraction at least 0.95 while retaining at least half of its initial
D, at room temperature, with a resolved isotope mass balance? A separate
collection experiment must demonstrate that this enriched inventory becomes an
enriched recovered product rather than being diluted by carrier hydrogen.

The numerical values above define a proposed go/no-go experiment. They are not
reported measurements and are not sufficient by themselves for commercial value.

## Screening relation

For a stripping-only interval, let k_H(t) = -d log N_H/dt and similarly k_D.
If both inventories decrease without readsorption/exchange and k_H <= r_max k_D
throughout, then:

    log(odds_enrichment) <= (r_max - 1) * [-log(D_recovery)].

At constant hazard ratio r > 1, equality gives:

    D_recovery = odds_enrichment ** (-1/(r - 1)).

This is elementary kinetics applied to the proposal, not a novel theorem.
A time-varying waveform cannot evade a genuinely uniform measured hazard-ratio
bound. Replenishment, isotope exchange, and heterogeneous initial loading require
their own accounting and must not be silently folded into this model.

## Files

- screening.py: standard-library numerical checks; run `python screening.py`.
- results.json: output from executing that script.

No raw experimental workbook was reanalysed. Zenodo identified a Figure 2.xlsx
dataset, but its binary download did not succeed in this session. The paper and
its preprint figure were inspected; the script uses the approximate operating
coverage reported in the paper, not digitised voltammograms.

## Evidence and comparator sources

1. Soong et al., Mechanism of the electrochemical hydrogenation of graphene,
   Nature Communications 16, 10741 (2025).
   https://doi.org/10.1038/s41467-025-65771-3
   Figure 2 shows separate-isotope oxidative responses. This does not establish
   mixed-isotope stripping selectivity. Reported operating coverage ~1e14 cm^-2.
   Approximate coverage is not a proved maximum storage capacity.
   Preprint with figures: https://arxiv.org/abs/2510.19505
   Public raw-data record: https://zenodo.org/records/17209896

2. Wen et al., Leveraging the kinetic isotope effect by compact H-bond motifs
   for electrochemical hydrogen isotope separation, PNAS (2026).
   https://doi.org/10.1073/pnas.2533803123
   Distinguish pure-isotope KIE, instantaneous gas/liquid separation factor,
   and accumulated liquid enrichment. They are not interchangeable.

3. Lozada-Hidalgo et al., Scalable and efficient separation of hydrogen isotopes
   using graphene-based electrochemical pumping (2017).
   https://arxiv.org/abs/1702.07562
   Prior art for membrane-based graphene isotope separation. The manuscript's
   industrial-scale outputs/energy statements are projections, not plant results.

4. Li et al., Large Transport Gap Modulation in Graphene via Electric Field
   Controlled Reversible Hydrogenation, preprint of Nature Electronics study.
   https://arxiv.org/abs/2008.09749
   Electronic switching endurance is not separator endurance.

## Unclosed obligations

Mixed-isotope hazards; loading composition and yield; absolute covalent inventory;
gas/solution side reactions; potential/reference and temperature calibration;
carrier-hydrogen dilution; product collection; net energy of the complete cycle;
accessible electrode area; scale-dependent transport; chemical and mechanical
endurance; throughput; cost; and a complete priority search.

No favourable values have been supplied for these quantities. No repository
write, experiment, fitted physical simulation, or validation is implied.

## Scope of the collector calculation

The 24.3 pL carrier-H limit is a single-cycle product-fraction calculation for
1 cm^2 at the stated coverage. It does not rule out accumulation over many
cycles into a fixed collector, isotope exchange that removes carrier H, a
separate gas collector, or another collection design. Each alternative requires
its own measured isotope balance, full-cycle time, energy and yield. It must not
be represented as already demonstrated by the source experiment.
