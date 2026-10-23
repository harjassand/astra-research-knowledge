# Cold jets do not forbid heat recovery; they do not certify its grade

## Result
There is a constructive conditional heat certificate, without assuming a whole-flow 3500 K or 800 K temperature: bound the unrecovered loss before the downstream exchanger and subtract the enthalpy needed to bring the entire product flow to the desired delivery temperature. The remainder is an ideal available duty above that temperature. The measured NOx and reported power alone do not supply that loss bound. They permit both a substantial downstream-heat completion and a zero-useful-downstream-heat completion of the same inventory balance. Neither completion is asserted to reproduce the device's kinetics or geometry.

This is not the old 2700 K / 1.407 MJ/kg contract. The actual operation remains 10 SLM primary plus 10 SLM cold jets, compared with ordinary 20 SLM. The published 3500-to-800 K feature is a local CFD field, not a mass-flow calorimeter. Section 2 says direct temperatures were not measured at this operating condition; Section 3.4 normalizes the modeled heat source to imposed power. That normalization is not an experimental absorbed-RF or wall-plug measurement.

## 1. Whole-apparatus chemical and thermal ledger
Choose a declared accounting endpoint: dry N2/O2/NO/NO2 (plus unchanged inert), 298.15 K, common pressure, with no material storage, leakage, other product or exported mechanical work. This is an accounting endpoint, not a claim that the measured reactor reaches it. Let F be original inlet mol/s, x outlet NO+NO2 mole fraction, and z outlet NO2 mole fraction. Atom balance gives

    Fout = F/(1+z/2),   Ndot = Fx/(1+z/2),   0 <= z <= x.
    Hchem = F[(x-z) h_f(NO) + z h_f(NO2)]/(1+z/2).

At 298.15 K, h_f(NO)=90.29 and h_f(NO2)=33.10 kJ/mol. Therefore

    F x 33.10/(1+x/2) <= Hchem [kW] <= F x 90.29.

The bounds vary composition and consequent molar contraction together, rather than multiplying concentration by an uncorrected product stream. With the explicit volume convention 22.414 L/mol, 20 SLM is F=0.01487166 mol/s. At digitized forced-flow centers, Hchem ranges are 4.84–13.26 W at 400 W and 7.94–21.83 W at 700 W. These are endpoint/speciation bounds at graphical centers, not measurement confidence intervals. The accompanying CSV evaluates all eight measured-center conditions.

Let Wa be actually absorbed RF; let L be all unrecovered energy escaping before the nominated downstream sensible-heat recovery surface; and Hs be its arriving sensible enthalpy above that endpoint. With cold feeds at the accounting temperature and negligible kinetic-energy transport,

    Wa = Hchem + L + Hs.

More generally add measured feed sensible/kinetic inputs and any other energy crossing this control volume. If the full apparatus and outlet finally cool to the accounting endpoint, total eventual heat rejection is R=Wa-Hchem. Under the explicit hypothesis Wa=P_reported, forced-center R is 386.74–395.16 W at 400 W and 678.17–692.06 W at 700 W. Roughly 97–99% of this assumed absorbed power ultimately exits as heat. This is a large heat-disposal requirement, not a heat-export guarantee. Product formation enthalpy is not product chemical exergy, nor is either a fertilizer value or capture-process energy.

The electrical boundary is separate: E_wall=Wa/eta_abs+auxiliaries, with an experimentally established conversion convention required. Generator losses E_wall-Wa are not plasma exhaust heat. If collected, they need their own temperature and recovery ledger for BOTH designs. Compression/drying and jet pressure costs must likewise be counted once at the common input boundary.

## 2. A load-bearing favorable certificate, not an assumed outlet temperature
For prescribed delivery threshold Td>T0, let S(Td) be the sensible enthalpy rate of the entire fixed-composition outlet if it were at Td. For any nonuniform outlet, the ideal heat removable while each parcel is above Td is

    Q_available(>Td) = integral [h(T)-h(Td)]_+ dN
                     >= max(0, Hs-S(Td)).

The inequality follows from [a-b]_+ >= a-b; it does not require a uniform outlet or a hot-core mass fraction. If L<=Lmax is established, then

    Q_available(>Td) >= max(0, Wa-Hchem-Lmax-S(Td)).       (certificate)

This is a thermodynamic availability statement for composition-preserving sensible cooling with a suitable heat exchanger; actual finite-area duty is lower, and strict finite driving force needs a hotter gas cutoff than the receiving load temperature. It does not assume preserved NOx kinetics through an added exchanger.

For a deliberately conservative numerical screen at Td=500 K, all four molecular species have cp<50 J/(mol K) over 298.15–500 K in NIST Shomate data; unchanged argon also satisfies that bound. Hence S(500)<=F*50*(500-298.15)=150.09 W, without assuming a 79/21 feed composition. Under Wa=P, the forced 400 W center has

    Q_available(>500 K) >= max(0,236.65 W-Lmax),

using the worst-speciation Hchem=13.26 W. At 700 W it is >=max(0,528.08 W-Lmax). These are conservative sufficient certificates, not observed exports. A zero-prior-loss thermodynamic completion has substantial available downstream heat even with both feeds, including the jets, still cold. Conversely an unbounded L can consume all R before the recovery surface, leaving no positive useful downstream heat. Thus the evidence cannot decide which completion applies. One need not invent a wall temperature, kinetics, or a whole-flow core temperature to prove this non-identification.

The certificate identifies a concrete falsifiable contract: e.g. at the conditional 400 W point, a verified pre-exchanger loss bound below 236.65 W would guarantee positive ideal sensible duty above 500 K in the stated species/endpoint class. An outlet calorimetric Hs measurement can replace Wa and L altogether. Actual absorbed power and graphical/speciation bounds must replace the illustrative center assumptions before certification.

## 3. Entropy prevents treating every thermal watt as an electrical watt
For the complete steady apparatus at common environmental T0 and pressure, including all inlet physical exergy, the exergy balance is

    W_input + B_feed = Delta B_product + sum Q_k(1-T0/T_k)
                      + W_export + T0 S_generated.

Chemical mixing contributions belong in Delta B_product; Hchem cannot be substituted for it. For a frozen-composition sensible parcel, available work is integral cp(T)[1-T0/T]dT. Cooling or mixing can conserve enthalpy while destroying this physical exergy. The 10 SLM cold jets are not a work-producing refrigerator or an external sink that removes heat: their internal mixing conserves combined enthalpy and produces entropy. With no thermal measurement, all residual heat can in principle reach an external boundary arbitrarily close to T0 and carry arbitrarily little useful exergy. Therefore NOx, throughput and indicated RF power give no strictly positive measured heat-grade or thermal-work guarantee.

## 4. Cold-feed inventory and the strongest ordinary comparator
Do not route recovered heat into the quench 10 SLM and still call those jets unchanged. Heating and then recooling that share to restore its original state gives no net feed-preheat credit and creates an additional rejection duty. External-load heat recovery downstream is the clean constructive option that leaves both inlet streams unchanged, subject to unchanged backpressure and product state.

If primary-feed recuperation is allowed as a NEW operating condition, only 10 SLM is available in the forced design. For a uniform exhaust at Th and a passive exchanger,

    Qrec,F <= min(Hs,F, F/2 * [h_feed(Th)-h_feed(T0)]).

For a finite minimum approach DeltaT, the necessary two-end bound is instead

    Qrec,F <= min[Hhot(Th)-Hhot(T0+DeltaT),
                  Hprimary(Th-DeltaT)-Hprimary(T0)],

with nonnegative feasible terms and stream-specific sensible-enthalpy rates. This minimum is not generally an exact maximum when heat capacities differ with temperature: an interior pinch can be tighter. A precise countercurrent thermodynamic maximum is the supremum of Q for which, at every cumulative hot-side duty q in [0,Q],

    Hhot^-1(Hhot(Th)-q)
      - Hprimary^-1(Hprimary(T0)+Q-q) >= DeltaT.

Here Th is a required measured or otherwise established hot-inlet state, not the CFD core temperature; chemistry must remain fixed for these enthalpy functions. Product stability and actual exchanger losses can further restrict the duty.

The ordinary 20 SLM design gets the corresponding full-F sink and the SAME external heat-export options. With equal species heat capacities and a common exhaust temperature, forced feed recuperation is capped near half the exhaust sensible duty, while ordinary recuperation can approach the full duty. This half bound is a conditional matched-stream limit, not a universal bound for nonuniform exhaust or auxiliary heat pumps. Preheating primary feed changes the demonstrated plasma operation; its yield cannot be inherited from the cold-feed measurements.

There is a sharper retirement result if BOTH feed-port states must stay unchanged: their enthalpy inflow is unchanged, so internal feed preheat cannot give a positive net feed-enthalpy credit. An upstream exchanger followed by cooling back to the original port state must reject the same added enthalpy, unless that energy leaves as work or is used at another explicitly included sink. Returning all thermal inventories to their original state rules out a transient storage loophole. Thus the specific “free recuperation retrofit, unchanged cold feeds, unchanged observed yield, reduced RF” inference is retired by the first law. Heat-to-work assistance to compression, external heat coproduction, or staged recovery is NOT retired; each is a distinct grade/auxiliary/output contract, available equally to ordinary flow.

At exactly matched product amount AND speciation, pressure, thermal endpoint and feed throughput, Hchem is common, so R_B-R_F=Wa,B-Wa,F. More input generates more residual heat, not a free comparator handicap. If ideal recovery were credited watt-for-watt, common-boundary net input E-Q collapses to the common product enthalpy (when all non-product input is captured). A fair useful-energy comparison instead specifies the same external load and grade, assigns the same justified credit lambda, and evaluates (E_F-lambda Q_F)/N_F against (E_B-lambda Q_B)/N_B. A heat advantage cannot be assigned only to forced flow; neither the same-power yield gain nor the conditional matched-product power ordering establishes that comparison.

## Sources
- Vashisth et al., Chemical Engineering Journal 543 (2026), 178575: https://doi.org/10.1016/j.cej.2026.178575. Actual local source: cycle7_received/owner_cycle6/nitrogen_cycle6_20261022/electrodeless_evidence/2026_forced_intrinsic.txt, Sections 2 and 3.4; original comparison caveats: observed_operation/PROOF_AND_BOUNDARY.md in the same archive.
- Digitized centers: electrodeless_evidence/digitized_experiments.csv in that archive. No new curve or trajectory fit used.
- NIST thermochemistry and Shomate data: https://webbook.nist.gov/cgi/cbook.cgi?ID=C10102439&Mask=1 ; https://webbook.nist.gov/cgi/cbook.cgi?ID=C10102440&Mask=1 ; https://webbook.nist.gov/cgi/cbook.cgi?ID=C7727379&Mask=1 ; https://webbook.nist.gov/cgi/cbook.cgi?ID=C7782447&Mask=1 . Retrieved 2026-10-22.
