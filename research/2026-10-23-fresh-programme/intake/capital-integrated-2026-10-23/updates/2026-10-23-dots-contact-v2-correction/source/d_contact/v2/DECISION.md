# Inventive attack: separately contacted, inventory-matched hematite subpellets
23 October2026. This is a concrete proposed intervention and a tested discriminating prediction, not an observed performance gain.

## One governing operation
Retain the ordinary Fayaz2023 Ni36/Fe64-anode, beaker/air operation: hematite of the same batch,10MNaOH,353K, cathode at−1.4V versus its Ag/AgCl reference. Retain identical preparation temperature, grain structure, porosity, feed iron, electrolyte composition and product definition. Do NOT introduce the dilute goethite/silicate chemistry. The controlled change is macroscopic current-contact spacing and pellet shape. A successful intervention must improve independently recovered metallic iron, not just normalized crystalline metal fraction or current. Original-feed recovery additionally requires all missing/retained iron to be accounted for.

## Mechanism and countermechanisms
Hypothesis H_R: charge access and propagation away from the collector dominate useful reduction time. Shortening the longest lateral path helps even without chemical additives.
Alternative H_Z: pore-electrolyte access across pellet thickness dominates. A thicker compact pellet can be worse despite shorter lateral paths.
Alternative H_D: local dissolved iron transport and/or nucleation is dominant; the controlling length may be the crystallite/pore scale, not pellet radius. Reducing bulk radius then provides little gain. Dissolved intermediates and a visibly advancing front are not mutually exclusive.
Alternative H_H: increased wetted collector/product area mostly increases hydrogen or other side currents. Higher total current alone cannot distinguish it from H_R.

Compatible governing observation: Fayaz2023 reports reduction starting at the central collector and progressing outward in the actual80C pellet; this supports spatial access as a candidate but does not identify the dominant resistance. Its current decay does not by itself measure local front velocity. No fit to that decay is used to assign a free speed.

Primary mechanism challenges, not numerical transplants:
- Lopes et al.2019 DOI10.1016/j.electacta.2019.135060 tested Al-containing ceramics at90C,10MNaOH with different collector exposure and porosity. Electrolyte access/contact mattered; some configurations disintegrated, losing solids. Their feed/anode/potential differ, so their efficiency is not assigned here.
- Shekhar et al.2025 DOI10.1021/acsnano.5c10559 correlated microscopy and ring-disk measurements: nanoporous hematite followed dissolution/redeposition; dense material showed reactive fracture with metal formation. A front appearance cannot exclude short-range solution mediation. The author's accessible upload contains the final2025 article under an older2024 preprint page title. Its exact kinetic rates are not copied into the80C bulk-pellet model.
Sources: https://www.researchgate.net/publication/336450429_Electrochemical_reduction_of_hematite-based_ceramics_in_alkaline_medium_Challenges_in_electrode_design ; https://www.researchgate.net/publication/385926995_Understanding_the_mechanism_for_the_low-temperature_reduction_of_Fe2O3_to_Fe_in_alkaline_electrolytes

## Concrete construction, including what is not free
Replace a radius10mm,thickness2mm disk by four equal disks inside the SAME circular projected envelope. Geometrical packing gives radius ratio k=1/(1+sqrt(2))=.41421356. Preserving porous oxide volume requires height ratio H=1/(4k²)=1.45710678: new radius4.14214mm,thickness2.91421mm. The extra0.91421mm depth is a real changed geometric constraint, not hidden as the same cell envelope volume.
Each disk has its own through-thickness collector. Preserve total active collector volume by radius scaling1/sqrt(4H)=k. For an explicitly CHOSEN, not source-reported, original pin radius.25mm, each new pin radius is.103553mm. CORRECTED: ideal parallel axial resistance increases by H²=2.12316017 at fixed total pin volume. Each pin resistance scales as H/k², and four equal branches give H/(4k²)=H². Independently, R=rho*length²/total_volume gives the same factor. External headers, contacts, insulation, mounting, handling and mechanical failure add further costs. The v1 statement that resistance was unchanged was wrong. No material supplier has qualified this construction. Bare pin area increases by1/k=2.41421; masking exposed leads does not eliminate hydrogen on newly formed iron.

The electrode is a changed design, not smaller particles with free extra preparation. Retain the strong ordinary controls: ordinary thinner pellet, conventional mesh/foil contact, and well-stirred suspension where applicable. Mesh/foil contacts already exist in primary literature. This is not a historical novelty claim. A comparator may use the same material, envelope, preparation and contact budget.

## Actual computational test and load-bearing result
No unmeasured kinetic coefficient is fitted. Two explicit scaling hypotheses are tested:
1. constant-speed radial front: T_R proportional to radius;
2. diffusion-like radial front: T_R proportional to radius².
Axial pore-transport time is tested as T_Z proportional to height². Under a declared additive-times approximation, let alpha be the ORIGINAL fraction of time attributable to the radial mechanism. Then
T_new/T_old = alpha*k^p +(1-alpha)*H².
This is a model-class discriminator, not a measured constitutive law. H²=2.12316017.
For p=1, subdivision is faster only if alpha>0.65722368.
For p=2, it is faster only if alpha>0.57551111.
Thus the initial idea that shorter contacts necessarily help is rejected. An axial-dominated admissible case predicts a2.123x slowdown at identical material inventory. The construction must earn its radial-dominance premise.

For the favorable purely radial limit, assume parasitic current is a sum of a term proportional to converted oxide volume and a term proportional to wetted pin area. The pin fraction f is UNKNOWN. Accounting gives H2/side-charge ratio k^p*[(1-f)+f/k]. At p=1,f=1 it equals1: faster completion yields NO charge saving because the extra collector exposure exactly consumes the time saving. At p=1,f=0 it is.4142. With the source-conditioned baseline efficiency.80523, resulting total charge ratios for the SAME metal are1 and.88591, respectively. Neither endpoint is a prediction for real hardware; they bracket only that declared side-current model.

A further failure is power demand: those favorable time ratios require roughly2.14–2.41x mean current for p=1, or4.89–5.16x for p=2. Do not advertise the speed ratio at the original power/supply limit. Higher full-cell voltage, OH transport, hydrogen, loss of contact or anode loading can erase it. No voltage-response law was fitted to restore a gain.

## Independent checks and rejected shortcut
geometry.py evaluates distance-arrival statistics on deterministic polar grids at600,1200,2400resolution; exact center and ring moments supply independent checks. subdivision.py verifies oxide-volume and pin-inventory identities. The first tested shortcut placed four contacts in an unchanged single disk. It reduced ideal maximum travel distance toR/sqrt(2), but increased integrated already-converted volume exposure from1/3 to about.34717 in a constant-speed model. Faster completion can therefore INCREASE hydrogen exposure even before extra pin area. This nontrivial failed direction motivates independent subpellets rather than merely adding contacts. The ring-contact alternative has favorable ideal distances but needs thin extended metal and much larger wetted area; it is not admitted as a free electrode.

## Discriminating prediction and decision rule
For the proposed subpellets, compare spatially resolved conversion histories at fixed actual local cathode potential, including core-to-face versus center-to-rim lag, with absolute metallic output, integrated hydrogen and dissolved/escaped Fe. H_R predicts the onset/lag changes with contact spacing; H_Z predicts thickness penalties; H_D predicts dependence on local pore/particle morphology and detectable dissolved flux rather than just bulk spacing; H_H predicts extra charge/gas without commensurate metal.
A ring collector detecting Fe(II) proves a solution pathway exists but its collection efficiency and competing re-deposition must be calibrated before assigning the pathway's fraction. Blank collector subtraction must use matched exposed area and surface state; newly formed Fe differs from the original collector. Quenched phase fractions alone do not yield absolute recovery. Paired charge and full-cell voltage determine energy; no reference-electrode-energy substitute.

Decision: the concrete contact intervention has decision-changing predictions, but NOT a robust demonstrated advantage over ordinary Ni/Fe. Proceed with an existing-data test of radial versus axial/contact dominance only if compatible spatial/time observations exist. Do not launch a kinetic trajectory with arbitrary alpha, or promote the favorable radial limit. The tested negative cases are retained. This is a mechanism construction, not another headline audit. The other research assignment and all frozen evidence remain intact.

## Correction receipt,09:56UTC
The v1ZIP remains unchanged. Its claim of unchanged ideal pin resistance was a construction error, caught in the parent physical cross-check. The corrected script explicitly tests both the parallel-circuit expression and fixed-volume length-squared law. Geometric packing, travel-distance, exposure and time-fraction thresholds are unaffected. No practical gain was admitted in v1; the corrected electrical penalty further restricts the candidate.
