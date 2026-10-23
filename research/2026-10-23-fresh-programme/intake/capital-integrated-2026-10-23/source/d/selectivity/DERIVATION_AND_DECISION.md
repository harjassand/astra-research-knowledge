# A two-fugacity return path, rather than a single-pressure separator

ASTRA-FRESH-20261023, branch D. First substantive calculation, 23 October2026. ACTIVE; no admitted plant or civilisation-level breakthrough.

## Origin and named operation

System: real-ore iron production in lithium carbonate, with lithium-bearing silicate gangue. The earlier concurrent investigation proposed a segregated hot gangue carbonator but lacked a selective Fe/Li return operation. That proposal, the2025 ore measurements and the Inoue2010 silicate data are pre-existing material. The fresh calculation tests a previously uncomputed Fe-versus-Si chemical-potential discriminator using Rakshit2011 measured ferrite free energies and compatible JANAF formation tables.

## Acquired numerical interface and limits

At1000K (726.85°C), pure lithium carbonate is above the JANAF993.15K melting transition, and the ferrite fit is inside its stated569–1021K range. This is not the2025 apparatus's750°C operating point.

Rakshit etal., JSSC184(2011)1186–1194, DOI10.1016/j.jssc.2011.03.033, report measured standard formation Gibbs fit for solid LiFeO2: -708+.1656T kJ/mol, with quoted±3kJ/mol. The indexed primary abstract/first page was acquired; complete PDF retrieval failed503/timeout. No claim to have inspected its whole experimental record, uncertainty convention or exact pressure-standard reconciliation is made.

JANAF at1000K supplies ΔfG°: Fe2O3(cr) -561.866, Li2CO3(l) -933.471, CO2(g) -395.886kJ/mol. Use C-078 combined-phase table: the C-077 liquid-only1000K HTML/TXT row is malformed and lacks signs. The separate signed C-078 row, not a silent repair, governs. Search-rendered whole-PDF tables also contained corrupt fields and were rejected. These are formation Gibbs energies at T, not Hf(298)-T*S mixed with an uncorrected elemental reference.

## Two reaction affinities

F: Fe2O3 + Li2CO3(l) -> 2LiFeO2 + CO2, central ΔG°=+14.651kJ/mol at1000K.

S: Li2Si2O5 + CO2 -> 2SiO2 + Li2CO3(l), Inoue Eqs20+21 central ΔG°=+22.800kJ/mol at1000K in its pressure convention.

Using nominal JANAFbar and converting the source's silicate pressure fromatm:
- To retain/produce the ferrite at unit activities, fCO2<about.1717bar.
- To complete disilicate carbonation at unit activities, fCO2>about15.727bar.

There is NO unit-activity equilibrium pressure window accomplishing both in the same compartment. Varying ONLY CO2 pressure cannot reverse their affinity ordering. The supplied ferrite±3kJ/mol, applied twice, gives an Fe pressure range.0834–.3533bar; this is not a complete confidence interval or all-source uncertainty budget. It does not close the nominal gap.

For actual activities the relevant necessary window condition is

(a_Fe2O3*a_Li2Si2O5)/(a_LiFeO2^2*a_SiO2^2) > about91.60.

The common carbonate activity cancels. With all other activities one, ferrite activity below about.1045 could reopen a window; at20bar the corresponding threshold is about.09265. Activities are relative to the specified reference phases, NOT mass fractions. No dissolved-ferrite activity coefficient or mixed-ore phase closure has been acquired, so the calculation does NOT exclude an actual melt window.

The equivalent exchange reaction 2LiFeO2+2SiO2 -> Fe2O3+Li2Si2O5 has a favorable nominal affinity of about37.56kJ/mol after the stated pressure-reference conversion. That eliminates the common CO2/carbonate pair and exposes why pressure alone is not a selective reagent under the pure-phase reference.

## Constructive consequence: direct ferrite-forming return

The same calculation also prevents an overly strong intermediate requirement. A recovered carbonate stream need NOT first be decomposed to pure Li2O to re-enter the Fe cycle. At sufficiently low CO2 fugacity, it can react DIRECTLY with Fe2O3 to form LiFeO2 and release CO2, according to F. Therefore a pure-Li2O basicity/decomposition screen alone cannot prove the return path unavailable or assign its gross decomposition heat as an unavoidable extra input.

A candidate two-zone operation is:
1. Preconcentrate actual separable gangue without losing Fe-bearing liquor; this material operation remains unacquired.
2. Carbonate the silicate-rich fraction at high CO2 fugacity and recover carbonate from the silica-rich phase under admitted hot phase/separation conditions.
3. Return carbonate to a lower-CO2 ferrite-forming feed zone WITH Fe2O3, using the directly coupled reaction rather than an unqualified pure-oxide calciner.
4. Recover the released CO2, restore both gas circuits and working inventories, and feed the regenerated ferrite into the electrolysis cycle. Pay gas separation/compression, heat integration, leakage, entrained Fe/Li and product recovery.

The nominal pure-phase fugacity ratio must exceed91.60 at1000K. A low CO2 partial pressure is not necessarily a vacuum, but dilution does not make separation or gas reset free. The high-temperature chemical-potential separation RT ln(91.60)≈37.56kJ per CO2 equivalent is NOT automatically wall-plug work or additional net heat. Isothermal compression at a colder reference temperature, gas purity, reversible heat transfer and reaction enthalpies belong in a closed balance before ranking this against the ordinary route.

The earlier worker's .04896kWh/kg pure-carbonate-decomposition gross screen is retained as a scenario in its original record, not carried forward as a necessary cost of this direct ferrite pathway. No favorable substitute cost is invented here.

## Empirical discriminator and next attack

Needed observation: the Fe-bearing melt's activity/phase boundary as CO2 fugacity changes, together with hot Si/Fe/Li partition and kinetic residence time. A coupled measured saturation curve can distinguish a genuine selective window from a reference-phase illusion. Low-temperature ferrite carbonation studies show strong preparation/structural-rate dependence; their200–500°C rates are not transplanted into this molten bath.

Next: obtain compatible existing ferrite/iron solubility or equilibrium measurements under controlled CO2, and reconcile the full thermochemical reference. Then test the complete two-zone reaction/inventory balance against ordinary preconcentration and ferrite-forming feed, without a speculative trajectory or new hardware. No request for another branch's allocation is made.

Primary routes: https://doi.org/10.1016/j.jssc.2011.03.033 ; https://janaf.nist.gov/tables/Fe-030.html ; https://janaf.nist.gov/tables/C-078.html ; https://janaf.nist.gov/tables/C-095.html ; https://doi.org/10.2355/isijinternational.50.1532 .
