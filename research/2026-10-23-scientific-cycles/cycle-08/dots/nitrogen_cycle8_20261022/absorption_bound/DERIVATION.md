# Regeneration-counted water capture: a serial-stage bound and its recycle limitation

## Result first

The proposed immediate-absorption construction is a rigorous infimum of cumulative gas-reaction volume for serial, once-through ideal PFR/absorber stages, when every regenerated NO molecule is returned locally to the same forward-moving gas. It remains valid under arbitrary NO2/N2O4 partition and exact gas-flow contraction. It is NOT proved for arbitrary recycle networks, selective phase transport, or mixed-product capture. An ideal separated-regeneration recycle construction below actually beats that serial bound, so a universal version is false unless those operations are expressly excluded.

Nothing here qualifies actual absorption kinetics, interfacial area, liquid inventory, cooling, pressure drop, corrosion, or total train energy. The compared volumes are gas oxidation reaction volumes, not installed plant volumes. Infinite staging is a limiting construction, not a hardware recommendation.

## Input and chemical scope

Use the pinned input.json of nitrogen_cycle7_20261022/oxidation_operation, not old replay: 298 K, 1 bar, 20 declared SLM with 22.414 L/mol; all counted inlet NOx assigned to NO; a=0.010635658914728683 ordinary or 0.012198142414860683 split, b=0.21-a/2. Initial total molar flow is F0. The original source interface has event rate r=k[NO]^2[O2] and NO sink 2r, k=3.95e-38 cm6 molecule^-2 s^-1. The numerical check uses k=0.014325140836635082 m6 mol^-2 s^-1 and c=P/(RT)=40.35985068547854 mol/m3.

This deliberately restricted capture chemistry uses the NET reaction 3NO2+H2O -> 2HNO3+NO, including equivalent oxidized-N in N2O4. It is not an elementary absorption law. EPA AP-42 describes this regeneration and the need to reoxidize generated NO in nitric-acid manufacture; it does not establish the perfect absorption or selective recycle idealizations here. Primary-source cross-check: https://www.epa.gov/system/files/documents/2024-04/ap42_2nded_withsupps1_4_march1975.pdf and https://gaftp.epa.gov/ap42/ch08/s08/final/c08s08_1995.pdf.

No extra oxygen feed, alkali, peroxide, ozone, nitrate/nitrite product substitution, gas loss, water-vapor dilution, selective carrier removal, or dissolved-N inventory credit is admitted to the serial proof. Comparing such alternatives is legitimate, but requires their own product, reagent, resource and reset boundary. No claim of superiority to those routes follows from this restricted result.

## State and exact contraction

Normalize flow amounts by F0. At a cross-section let e be cumulative NO oxidation extent, s cumulative absorbed oxidized-N extent, and d gas N2O4 molar flow/F0. For serial local regeneration,

nNO = a-e+s/3; nO2=b-e/2; nNO2+2nN2O4=e-s;
0<=s<=e; 0<=d<=(e-s)/2;
t=Ft/F0=1-e/2-2s/3-d.

The stable acid-N capture per feed is 2s/3; the captured fraction of inlet fixed N is Y=2s/(3a). Regenerated NO totals s/3, and must not be counted as new captured product. Terminal complete absorption has s=e, hence e=1.5aY, NO=a(1-Y), O2=b-.75aY, and t=1-1.75aY.

For each mole captured as HNO3, oxidation turnover is 1.5 mol NO, regeneration is 0.5 mol NO, net oxygen consumption is 0.75 mol O2, and net stoichiometric water consumption is 0.5 mol H2O. Excess solvent is separate. These are steady net balances, not startup charges or proof of liquid purity.

## Pointwise rate bound, including dimerization

Fix e up to E*=1.5aY*, with Y*<1 and b>.75aY*. The ideal local-immediate-absorption state has s=e,d=0:

n*=a-2e/3 > 0; o*=b-e/2 > 0; t*=1-7e/6.

For any admissible delayed absorption and dimer partition:

nNO<=n*;
t >= 1-e-s/6 >= 1-7e/6=t*.

The first inequality for t follows by setting d to its largest possible value. Thus nNO/t <= n*/t* and nO2/t <= o*/t*. Both reactant concentrations, and therefore k[NO]^2[O2], are simultaneously maximized by immediate absorption. Dimerization cannot defeat the bound: even complete residual dimerization contracts the gas less than immediate capture plus local regeneration.

Along a gas PFR, de/dV=2kc^3 nNO^2 nO2/(F0 t^3). Absorbers are assigned zero gas-reaction volume. Therefore any serial staged train reaching capture Y* must pass cumulative oxidation E* and obey

Vgas >= F0/(2kc^3) integral(0 to E*) (1-7e/6)^3 / [(a-2e/3)^2(b-e/2)] de.

If it oxidizes farther while leaving some NO2 uncaptured, the additional volume cannot weaken this bound. A positive-rate limitation applies only up to E*. The equivalent immediate-path differential equation is

dY/dV=(4/3)kc^3 a(1-Y)^2(b-.75aY)/[F0(1-1.75aY)^3].

This proves the parent's proposed coefficient, including the event-rate factor of two. At Y=1 the volume diverges in this model; exact 100% capture is not reached in finite gas-reaction volume.

## Finite-stage approach to the infimum

Partition E* into N equal oxidation increments delta. In each stage hold s=e_previous while oxidizing by delta, then instantly absorb all oxidized N and locally return its NO. Choose delta<a(1-Y*), which ensures NO remains positive throughout every stage. Monomer-only reaction volumes are obtained from the exact same PFR law with t=1-e/2-2e_previous/3. Allowing dimers can only lower those stage volumes without crossing the proved lower bound.

On the compact target interval with NO and O2 bounded away from zero, integrands and first derivatives are bounded. The stair-step absorption history differs from s=e by at most delta, so the summed reaction volume differs from the immediate-absorption integral by O(delta). This proves attainability as an infimum by finite serial trains; it does not assume physical instantaneous mass transfer. Finite stage count can be important near a stringent residual-NO target.

## Numerical checks and matched endpoint

The check script uses independent SciPy quadrature with u=1/(1-Y) for the limiting path. These are numerical checks, NOT certified rational enclosures or physical uncertainty bounds. The prior source's +/-0.2 log10 k sensitivity multiplies volumes by 10^(-.2) to 10^(.2); it is not a universal experimental enclosure. Common k uncertainty must stay common across configurations.

At 99% captured inlet N:
- Ordinary immediate serial infimum: 530.13 L; outlet NO 108.35 ppm.
- Split immediate serial infimum: 463.01 L; outlet NO 124.61 ppm.

At matched 100 ppm NO AFTER complete terminal NO2/N2O4 capture:
- Y=(a-epsilon)/[a(1-1.75epsilon)].
- Ordinary Y=0.9907710526; serial infimum 574.84 L.
- Split Y=0.9919756262; serial infimum 578.08 L.
- 256/1024/4096 monomer-only finite stages: ordinary 657.60/591.18/578.71 L; split 678.91/597.19/582.57 L.

A mere 100 ppm NO measurement without terminal oxidized-N capture DOES NOT imply this capture target. A dry oxidation section can lower NO while exporting almost all fixed N as NO2/N2O4. This is an internal modeling endpoint, not an emission or exposure standard.

## Counterexample to extending the serial bound over arbitrary regeneration routing

Suppose an ideal separator absorbs all oxidized N after one PFR and a separate liquid regeneration operation recovers the resulting NO as a pure stream, which is returned to the PFR inlet. Assign zero reaction volume to these ideal phase-transfer operations, only for this mathematical stress test. No unconverted tail NO is recycled. At prescribed final capture Y, set E=1.5aY and g=E/3=.5aY. The regenerated-NO recycle is F0*g; the PFR feed is fresh gas plus that recycle.

Inside this PFR, at oxidation extent e:

nNO=a+g-e; nO2=b-e/2; t=1+g-e/2-d, 0<=d<=e/2.

For the monomer path d=0, admissible only within the relaxed arbitrary-partition class (not a demonstrated NO2/N2O4 equilibrium trajectory),

Vrecycle=F0/(2kc^3) integral(0 to E) (1+g-e/2)^3/[(a+g-e)^2(b-e/2)] de.

After all E oxidized-N is removed, acid production is 2E/3=aY and the separately collected regeneration flow E/3=g exactly closes its own recycle. Final discharged gas NO=a(1-Y), oxygen=b-.75aY, total=1-1.75aY: the same net product and tail as the serial limiting path. No extra nitrogen source has been introduced.

At the matched complete-capture 100 ppm endpoint this model gives 402.88 L ordinary and 407.90 L split, below the respective 574.84/578.08 L serial bounds. Hence stoichiometry alone cannot establish that local immediate absorption is globally volume-optimal once regenerated NO may be relocated upstream. Dimerization could reduce the counterexample volumes further, not invalidate the mathematical counterexample.

This is NOT evidence that a real water absorber produces an isolated pure-NO stream for free. It requires selective removal/transport before NO release or equivalent NO recovery; its viability, mass-transfer rate, liquid chemistry, finite inventory, recycle pressure and separation/stripping energy are unqualified. If the admitted operation is only an inline equilibrium gas/water contactor, the counterexample may not be an admissible operation. The correct conclusion is a rigorous serial/local-return bound, plus an explicit missing constraint for a claimed all-trains bound. Ordinary controls must receive the same admissible recycle/separation options as DOTS.

## Resource, liquid-inventory and reset closure

1. Every trial must use stable outlet product plus change in full gas and liquid fixed-N inventory. Absorbed NO2, HNO2, dissolved NO and nitrate/nitrite cannot all be labeled captured HNO3. A rising inventory can make a short run appear to suppress NO without achieving a steady product rate.
2. Gas inventory is the integral of c times volume, with actual species composition. Liquid holdup, residence and solubility require a separate state model. A separate regeneration loop adds startup filling and shutdown release; its steady g relation does not eliminate that inventory.
3. At steady isothermal operation net heat release is fixed by all inlet/outlet species and their actual solution states. Use HNO3(aq) at the chosen acid concentration and water excess, not a gas-only NO2 endpoint or arbitrary pure-acid enthalpy. Include cooling from plasma, reaction/absorption and dilution heat, sensible streams, pump/compressor work and any heat recuperation consistently. No finite cooling area is established here.
4. All models impose 1 bar and 298 K. Real staged contactors and recycle need pressure-drop, blower/pump and temperature constraints. The perfect zero-volume stages have no demonstrated hydraulic realization. Compression is not a free way to replace gas-reaction volume, and the inherited ambient k cannot certify a high-pressure extrapolation.
5. Count startup/off-spec gas, filling, shutdown/flush, product recovery, liquid regeneration, remaining inventory and complete reset. A bound on gas volume is not a bound on whole-cycle energy, installed size or delivered-fertilizer SEC.
6. A strong conventional comparison can combine PFR oxidation, staged/countercurrent capture, allowed regeneration recycle and separately costed alternative liquid chemistry. It must share the same end product, fraction captured, tail-gas criterion, original feed, thermal/hydraulic constraints, operating window and reset state. This note does not establish a whole-train winner.

## Path/source-binding correction

The original numerical script is preserved as check_bound_original_cwd_v1.py. The current check_bound.py differs only in input path/source binding: it reads an unchanged copy at inputs/input.json relative to its own __file__, and rejects any mismatch with the original SHA256 75de794a26ecaac2e8c4c938249bea1af08fa4fa7e563407962e9ecb58f10a34. It invokes no previous-cycle program. The monomer trajectories used as finite-stage or recycle examples are admissible only in the relaxed arbitrary NO2/N2O4 partition model, not established equilibrium paths.
