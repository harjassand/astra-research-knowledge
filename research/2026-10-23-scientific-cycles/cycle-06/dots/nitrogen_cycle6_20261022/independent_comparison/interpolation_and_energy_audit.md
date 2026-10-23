# Follow-on audit: corrected-product interpolation and power inequality

This audit was requested after completion of the independent Fig. 7 transcription. It examines the parent's observed_operation/admission.py and digitized.json. The initial transcription remains independent: those parent files were not read until after independent_fig7_experiments.csv and the main challenge report had been completed. Parent digitized.json SHA-256 at inspection: d008bafa7822478e614774394ed024b6b3b0f5faa9c74cd71e50422392d3f63d.

## Corrected product basis is valid under the stated closure

Let x = x_NO + x_NO2, z = x_NO2, and n_in be total inlet moles of dry feed. With final gas consisting of N2, O2, NO, NO2 (and optionally unchanged inert gas), no leaks, no product storage, and no other changing species, net molecular stoichiometry gives

    n_out = n_in - n_NO2/2
          = n_in/(1 + z/2).

Each counted NO or NO2 molecule contains one nitrogen atom, so fixed-N count per inlet mole is

    h = x/(1 + z/2).

Since 0 <= z <= x, h is bounded by x/(1+x/2) <= h <= x. Therefore a plotted x envelope [l,u] maps to a conservative product envelope [l/(1+l/2),u]. This is an exact algebraic closure conditional on the restricted species and boundary, not an empirical proof that closure holds in the FTIR system. N2O4, N2O, other product nitrogen, leaks, moisture changes, and retained inventory would need their own accounting. The absence of separately reported NO2 means the bounds should remain worst-case rather than point corrections.

## The proposed interpolation theorem is correct, conditionally

Let q_B(P) and q_F(P) denote actual fixed-N output per inlet mole, not merely uncorrected concentration. Assume they are continuous and nondecreasing across the relevant reported-power interval and conform to the stipulated graphical product envelopes at the tested points. These are explicit assumptions about response curves, not established full measurement confidence bands.

At a tested separator P0, choose a target t in the strict interval

    max[U_B(P0), U_F(400)] < t < min[L_F(P0), L_B(700)].

Then q_F(400) < t < q_F(P0), and q_B(P0) < t < q_B(700). The intermediate-value theorem gives a forced setting PF strictly between 400 and P0 and a baseline setting PB strictly between P0 and 700 at which each reaches t. Nondecreasing response prevents the baseline from having an earlier solution below P0 and prevents the forced configuration from first reaching t only above P0. Plateaus can make a target's solution nonunique; defining the least required reported power on [400,700] avoids claiming uniqueness.

Using the parent's current digitized envelopes and the full product correction, the numerical target windows are:

- P0 = 500 W: 0.0111007752 < t < 0.0116347071 mol fixed N per mol inlet feed (1.11008–1.16347 per 100 inlet moles).
- P0 = 600 W: 0.0125271318 < t < 0.0128165629 mol fixed N per mol inlet feed (1.25271–1.28166 per 100 inlet moles).

These are not outlet-concentration percentages once the contraction correction has been applied. The 500 W result establishes a conditional strict ordering in reported power, not a measured matched-output operating point.

### No uniform positive watt saving follows

For every small positive epsilon, choose continuous nondecreasing piecewise-linear curves consistent with the neighboring measured bounds that cross t at PF=P0-epsilon and PB=P0+epsilon. The forced curve can rise steeply just before P0 while the baseline rises steeply just after P0; all four discrete point constraints can still be met. Then PB-PF=2 epsilon approaches zero.

Thus every individual admissible continuous curve pair has a strictly positive separation for a strict target, but the infimum over all admissible curve pairs is zero. Neither a 100 W measurement grid nor observed average slopes certifies a positive minimum watt saving. A bound on the local slopes, or additional direct response information, is needed for a quantitative lower saving. If known finite upper slope bounds MB and MF apply, a sufficient lower bound is (t-U_B(P0))/MB + (L_F(P0)-t)/MF. The paper does not provide such a certified slope bound.

## Same-power specific-energy inequality is exact

At the common reported P, let G = QF/QB > 0, EF = P/etaF + AF, and EB = P/etaB + AB, with positive total input and non-overlapping accounting of source and auxiliary loads. Then

    EF/QF < EB/QB
    iff EF < G EB
    iff AF - G AB < P (G/etaB - 1/etaF).

This is algebraically correct. A valid conservative lower G can be used as a sufficient admission threshold because EF-G EB decreases with G when EB>0. The visible-chart lower ratio is not itself a confidence-qualified lower G for real operation; calibration, power convention, closure, and stability remain separate assumptions.

Eta must have a defined boundary. It is a physical conversion efficiency only if the reported P is a calibrated physical output at that boundary. If P is merely an indicator or command, eta is an effective conversion factor and cannot be assumed equal between configurations or fixed at unity. Air already supplied at pressure cannot be charged twice, and the jet load is the incremental pressure-work/loss difference for the relevant stream, not evidence of an extra 10 SLM of total feed. Both compared cases total 20 SLM.

## Do not conflate same-P and matched-output inequalities

At the interpolated matched target, QF(PF)=QB(PB), so G=1, but PF differs from PB. The total-power condition becomes

    AF(PF) - AB(PB) < PB/etaB(PB) - PF/etaF(PF).

The same-P yield multiplier must not be reused as though it were measured at those unequal settings. Lower reported power at the matched target still does not establish lower total wall-plug power without the supply and auxiliary comparison.

## Verdict

The new bounded whole-apparatus positive evidence survives this challenge. The product-corrected conditional interpolation and exact same-P energy admission inequality are mathematically sound with the stated qualifications. The strongest defensible output is: measured improvement at common reported settings; a conditional lower-reported-power matched-output existence result; and an explicit, still-unfilled total-input admission inequality. It is not an isolated-mechanism identification, old-heater retrofit result, confidence-certified minimum gain, quantitative watt-saving certificate, or durability/reset qualification.
