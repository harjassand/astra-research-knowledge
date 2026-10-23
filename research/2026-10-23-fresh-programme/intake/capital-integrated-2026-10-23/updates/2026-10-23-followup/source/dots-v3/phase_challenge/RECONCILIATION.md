# Pressure exclusion: conditional arithmetic survives; physical exclusion does not
23 October2026,08:43UTC. Supersedes any reading of v1/v2 as an empirically robust exclusion. No input was tuned to preserve or overturn a conclusion.

## Governing cycle and conventions
Forward F: Fe2O3 + Li2CO3 -> 2 alpha-LiFeO2 + CO2.
A: Li2CO3 -> Li2O + CO2.
B: Li2O + Fe2O3 -> 2 alpha-LiFeO2.
A+B=F; cycle.py verifies stoichiometry and exact decimal Hess closure. One reaction mole makes TWO LiFeO2 formula moles. Do not confuse these denominators.
S: Li2Si2O5+CO2 ->2SiO2+Li2CO3.
F+S: Fe2O3+Li2Si2O5 ->2alpha-LiFeO2+2SiO2.
Its Gibbs energy is POSITIVE37.560443kJ/reaction mole in the original1000K calculation. The reversed exchange has negative Gibbs energy; v1 called the reverse's positive affinity37.56. No sign change is made here.

At1000K JANAF C-078 uses LIQUID carbonate. At800K it uses crystalline carbonate. The silicate reaction uses Inoue's fusion correction only above carbonate melting. JANAF standard pressure is1bar, while the inherited Inoue pressure convention is nominallyatm; the conversion adds0.109443kJ at1000K,0.087555at800K. That cannot explain a tens-of-kJ discrepancy.

## Source data retained, not averaged
Rakshit2011 DOI10.1016/j.jssc.2011.03.033 Eq32: alpha-LiFeO2 formation G=-708+.1656T kJ/formula mole,569–1021K, quoted±3. Eq33 reproduces Kawamura's older EMF fit -752+.187T,673–873K. The paper itself acknowledges20–30kJ disagreement. Indexed primary pp1192–1193 were recovered, including Tables4/6; direct PDF download still503. No complete-PDF reading claimed.
Wang/Navrotsky2005 DOI10.1016/j.jssc.2005.01.028 Table5: alpha-phase Hf298=-749.8±1.8kJ/mol; absolute S298=75.3±.8J/mol/K is tabulated from older calorimetry. Numeric table extracted from indexed primary; complete PDF download503.

At800K both G fits are supported: -575.52 versus -602.40kJ/mol. The same solid-carbonate cycle gives F=+53.076 versus-.684kJ/reaction mole, and reference CO2 thresholds .0003424 versus1.1083bar. Difference26.88kJ/formula mole is larger than adding quoted fit boxes3+3.4. These boxes are NOT established confidence intervals or a full uncertainty budget. The old-fit pressure-gap box at800K crosses zero if the quoted coefficient limits are treated as independent bounds; covariance is unavailable. NONE of that extrapolates the old fit to1000K or turns800K into a molten-carbonate process.

## Independent calorimetric-anchor cycle at1000K
A source-supported alternative can be constructed without extrapolating Kawamura's G fit. Use the same alpha-phase thermal increment from Rakshit Table6 but anchor it to Wang/Navrotsky's independently measured Hf298 and the measured absolute entropy. This is a declared thermochemical reconstruction, not a preferred fitted truth.

Table6 lists Hf298=-719kJ/mol, S298=75.8J/mol/K, H1000-H298=78.095kJ/mol and S1000=205.1J/mol/K. Its thermal increment
I=integral Cp dT - T integral Cp/T dT =78.095-1000*(205.1-75.8)/1000=-51.205kJ/mol.
Define Gstar relative to zero elemental enthalpies at298.15K, NOT formation G atT:
Gstar_ferrite=Hf298-T*S298+I.
This gives -846.005 with the Table6 anchor and -876.305 with the calorimetric anchor. Difference -30.300 follows from deltaH-T*deltaS; it was NOT chosen to open a window.

Use all other species in the SAME Gstar convention: JANAF Hf298 minus T times its tabulated free-energy function gives hematite -977.863, liquid carbonate -1371.339 and CO2 -629.423kJ/mol. The resulting F is +27.769 for the Table6 anchor and -32.831 for the calorimetric anchor. Adding S and pressure conversion gives +50.678443 versus -9.921557kJ/reaction mole. The latter nominal pure-phase reconstruction has a15.7269–51.8659bar window. It is NOT a measured molten-ore operating window.

This also exposes a separate within-source seam: Rakshit Eq32 gives F+14.651 at1000K, whereas Table6 on a common elemental reference gives+27.769. Table6's formation-G column -536.0 differs from Eq32 -542.4; a further small elemental-reference difference appears when combining FactSage-derived values with JANAF. The common-Gstar cycle removes that elemental convention, not the larger source inconsistency. No table is silently repaired or favored.

## Phase and uncertainty reconciliation limits
All numerical ferrite anchors above are labelled alpha-LiFeO2, not LiFe5O8, Li0.5Fe2.5O4 or an arbitrarily rescaled formula. Gamma/beta/alpha polymorphism exists; replacing an alpha enthalpy by gamma's lower value without its entropy/transition terms is rejected. LiFe5O8 can alter the stable phase assemblage and is not eliminated by the two-phase reference. A solid reference activity is not a dissolved-melt concentration or activity coefficient.

Rakshit measured Cp only to861K and extrapolated its thermodynamic table to1000K. The reconstructed alternative therefore inherits that thermal-shape assumption. Its quoted anchor-only worst-case half-width is2.6kJ/formula mole at1000K, but unknown Cp/transition/systematic errors and the source/table seams remain. The nominal open-window margin is9.921557kJ/reaction mole; uncharged changes can erase it. Do not report a confidence-certified window, nor select the alternative because it is favorable.

Kato2005 DOI10.2109/jcersj.113.684 was downloaded, rendered and read. TG reversal near530C and CO2 release at600–700C challenge the original simple reference, but do not calibrate its equilibrium G: finite-rate, partial-conversion curves, additive effects, an unidentified initial XRD peak and no shown post-reaction quantitative phase closure remain. Figure2 labels1C/min while methods say5C/min. The plots are not reversible equilibrium measurements. We do not fit a thermodynamic correction to them.

## Decision
The original algebraic exclusion remains TRUE ONLY FOR ITS FROZEN INPUTS. A robust physical pressure exclusion is WITHDRAWN/NOT_ESTABLISHED. A calorimetric source-anchored reconstruction changes the nominal sign without extrapolating the older EMF fit. This is sufficient to reject promoting one dataset into a physical impossibility claim, but insufficient to admit the proposed return operation. The priority is reconciliation of primary heat/entropy, Cp/phase and chemical-potential measurements, plus actual mixed-ore activities. No new trajectory is justified by selecting a favorable dataset.

The solubility/inventory work continues separately in fractionation/. It rejects temperature swing alone as a preconcentrator of the nominal dilute gangue, retains30.93kg Si-associated Li/t original-feed Fe as a conditional orthosilicate throughput, and counts Fe entrainment/phase losses. Existing computational work remains intact and its speedup claim remains withdrawn.
