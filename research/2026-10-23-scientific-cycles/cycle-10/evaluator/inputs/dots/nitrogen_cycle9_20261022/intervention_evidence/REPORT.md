# Cycle 9: bounded recovery of the measured batch intervention

22 October 2026. **Result: no admissible paired intervention response recovered.** The 10 kW batch paper remains an abstract-level lead, not a matched captured-nitrogen/whole-system-energy result. A newly identified publisher-registered corrigendum makes verification of the full record more important; its existence does not establish that any numerical result is wrong.

## Exact identity and new correction

Original: Cesar M. Moreira, Pratap Pullammanappallil and Bruce Welt, *Batch-wise nitrogen fixation from atmospheric air for on-farm fertilizer production using a 10 kW microwave induction-coupled plasma (MICP) torch*, Cleaner Engineering and Technology 33 (August 2026), 101277. DOI: https://doi.org/10.1016/j.clet.2026.101277 . PII S2666790826001369.

Crossref publisher-deposited metadata identifies a correction by the same authors: *Corrigendum to: [original title]*, Cleaner Engineering and Technology 34 (October 2026), 101291. DOI: https://doi.org/10.1016/j.clet.2026.101291 . PII S2666790826001503. Its update-to entry explicitly points to the original DOI, type erratum, dated 1 October 2026. The record was created 21 August 2026. This is stronger evidence than an index title alone. **The correction's substance was not retrieved: do not infer whether it concerns authorship, methods, numbers or anything else.** Full publisher-route retrieval was not attempted, consistent with the inherited access restriction.

## What remains available and what remains missing

The indexed original abstract reports 60 L initial water, torch durations of 30/60/90/300 min, an oxygen-depletion limitation below 6%, and continuing acid formation after shutdown. It reports its best schedule as 60 min torch-on plus 30 min recirculation/replenishment, maximum 0.162 M and 6.82 MJ/mol. These are the same abstract claims already recorded in Cycle 8, not new primary tables or a newly recovered measured response. The indexed data-availability statement says data are available on request; no request was made.

Missing from the material retrieved:
- Paired run-level liquid nitrogen amounts, nitrate/nitrite distinction and assay methodology, uncertainties and replicates.
- Reference versus intervention cumulative energy, torch-energy versus electrical-input boundary, recirculation/compression/cooling and replenishment energy.
- Total elapsed run duration and number of cycles underlying the maximum concentration, including sampling and final absorption.
- Matched initial gas and liquid inventories, final holdup, purge/vent accounting, and reset procedure.
- Operating pressure, oxygen makeup composition/amount, replenishment protocol and its simultaneous changes to gas inventory.

Do not multiply nominal 60 L by maximum concentration and combine it with a single 60-minute torch period to invent a paired energy response. The abstract does not establish that these quantities belong to that single cycle or that final liquid volume equals initial charge. Likewise, after-shutdown acid formation can reflect transfer of previously formed gas-phase nitrogen rather than new fixation, and a schedule that includes oxygen replenishment does not isolate recirculation/capture as its cause. These are interpretation limits, not newly measured findings.

## Finite retrieval record

Started by reading nitrogen_cycle8_20261022/capture_evidence/REPORT.md. Searches covered exact title, exact DOI and PII, title plus PDF/preprint/repository, Moreira/Pullammanappallil/Welt author combinations, UF and ESPOL institutional domains, the public author Academia profile, and exact correction identifiers. Relevant source locations:

- https://api.crossref.org/works/10.1016/j.clet.2026.101277 : downloaded original publisher-deposited metadata; archived as crossref_original.json. It supplies only Elsevier text-mining links, not an institutional manuscript. These links were not followed.
- https://api.crossref.org/works?query.title=Corrigendum%20Batch-wise%20nitrogen%20fixation%20atmospheric%20air%20on-farm%20fertilizer%20production&rows=3 : successful primary bibliographic correction search; archived as crossref_correction_search.json.
- https://api.openalex.org/works/https://doi.org/10.1016/j.clet.2026.101277 : archived as openalex.json. It reports any_repository_has_fulltext=false; its only full-text location is the excluded ScienceDirect publisher PDF. A DOAJ metadata location has no PDF. This is an index's current coverage, not proof that no author copy exists.
- https://www.researchgate.net/publication/410610645_Batch-wise_nitrogen_fixation_from_atmospheric_air_for_on-farm_fertilizer_production_using_a_10kW_microwave_induction-coupled_plasma_MICP_torch : search result explicitly says no full-text available and offers author request, which was not used.
- https://espol.academia.edu/CesarMoreira : title appeared in search index, but the opened profile snapshot did not expose this paper or a full-text manuscript. No sign-in, account or download request pursued.
- https://i-research.espol.edu.ec/ods/7 : institutional search index lists the exact corrigendum. Opening returns JavaScript shell, not article text. Crossref independently confirms the bibliographic correction link.
- https://orcid.org/0000-0002-2014-7953 : author record corroborates original title/authors/DOI, not measured tables.

An initial local metadata-fetch script lacked the requests package; it made no network request. The same read-only public metadata retrieval succeeded using Python's standard urllib. No software install was needed.

**Stopping condition reached:** exact-title/DOI/author and institutional/public-copy checks plus public metadata-location checks yield no legitimate accessible independent full primary text or detailed tables. The prior ScienceDirect 403 was not retried, nor was a publisher API/PDF/proxy route used to bypass it. No hardware, outreach, purchases, credit use, author requests or new Max computation occurred. This is a bounded retrieval negative, not a claim that the paper lacks the required data. No quantitative capture benefit or compatible target operation is admitted from this lead.
