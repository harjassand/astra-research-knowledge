# S12 — A conductive load-path certificate for sacrificial release

**Status (15 October 2026):** Original conditional mathematical design and a physically specified, unbuilt MEMS experiment. No device was fabricated or tested here. No release yield, advantage, or new physical effect has been measured. Novelty **UNKNOWN**. The exact benefit over the strongest equally informed incumbent is also **UNKNOWN**.

## Proposed operation and why the substrate matters

Manufacture an array of flexure-supported micromechanical shutters or resonator islands. The permanent flexures hold each island after fabrication. During handling, extra narrow **copper braces** temporarily tie the island to a separate frame bus, protecting the compliant element. Each brace is both an unwanted mechanical constraint and an electrical path from the island electrode to that bus. The permanent sense lead runs along a protected flexure and is electrically isolated from the brace bus. Copper is removed by a qualified selective wet etch; after a rinse and dry, measure island-to-bus conductance and a calibrated service-mode displacement. The target is a specified force–displacement response of the released island, not total identification of the etching chemistry or microscopic defect map.

This uses an unusual coupling manufactured into the object: every *temporary load path* is intended to be an *electrical path*. Under a material contract, the amount of extra mechanical stiffness that can remain is upper-bounded by the electrical conductance of the actual braces. The etch rate, front shape, diffusion geometry, and particular sequence of brace removals can remain hidden. The substrate turns an unknown interior state into a measured task bound; it does not make arbitrary hidden states harmless.

The proposed stack is an insulating substrate, a patterned permanent suspended element/flexures with a protected electrode, exposed copper brace **necks**, and an etch-protected isolated frame bus. Only the necks should be exposed to the release bath; loss of the bus or its contacts before loss of the necks would create a false endpoint. This is a **fabrication proposal**, not a demonstrated stack. Selective copper release in MEMS and a flexure-motion endpoint are experimentally established in the cited Ni–Fe work, but that paper did not build this particular parallel-brace device or validate the electromechanical bound below. Wet processing requires a rinse/dry protocol that does not cause stiction or corrosion. The first demonstration should use large enough structures that individual braces and motion can be independently inspected before attempting dense arrays.

## Exact mathematical mechanism (original derivation)

Take one intended small-displacement service coordinate \(q\). Let the permanent device's service-mode stiffness be \(K_0\). Brace \(i\) has axial displacement \(\alpha_iq\), length \(L_i\), and possibly uneven remaining cross-section \(A_i(x)>0\). On a linear axial branch, with local Young modulus \(E_i(x)>0\) and electrical conductivity \(\sigma_i(x)>0\), its stiffness and dry electrical conductance are

\[
k_i=\left[\int_0^{L_i}\frac{dx}{E_i(x)A_i(x)}\right]^{-1},\qquad
g_i=\left[\int_0^{L_i}\frac{dx}{\sigma_i(x)A_i(x)}\right]^{-1}.
\]

Suppose the qualified material state envelope establishes \(E_i(x)/\sigma_i(x)\le M\) at every point of each residual brace. Then

\[
\int\frac{dx}{E_iA_i}
=\int\frac{\sigma_i}{E_i}\frac{dx}{\sigma_iA_i}
\ge \frac{1}{M}\int\frac{dx}{\sigma_iA_i},
\quad\text{so}\quad k_i\le M g_i.
\]

With braces in electrical parallel between the island and brace bus, \(G=\sum_i g_i\). The added stiffness is therefore

\[
\Delta K=\sum_i\alpha_i^2 k_i
\le M\sum_i\alpha_i^2g_i
\le M\alpha_{\max}^2G.\tag{1}
\]

This survives an unknown nonuniform etch profile: the whole profile enters only through the measured \(G\) and the acquired upper bound \(M\). For uniform rods the result is equality when \(E/\sigma=M\). At an actual physical break, both mechanical and electronic contribution must vanish for the coupling to continue to hold. A false electrical break at a mechanically intact interface invalidates it.

Choose an allowable service stiffness \(K_{\mathrm{lim}}\) and establish an upper bound \(K_0^{+}\) for the permanent flexures, including fabrication scatter. If the dry conductance's conservative upper confidence/uncertainty endpoint \(G^{+}\) satisfies

\[
K_0^{+}+M\alpha_{\max}^2G^{+}\le K_{\mathrm{lim}},\tag{2}
\]

then the axial-brace model certifies adequate service compliance without imaging the hidden brace residues. This is a **task threshold**, stronger than the vague instruction to etch until an open-circuit reading. It also permits a small amount of harmless residual copper. If the goal instead requires literal absence of all copper, equation (2) is insufficient.

As copper is physically removed, each edge's conductance falls when its geometry shrinks with fixed conductivity, so the parallel \(G\) falls monotonically. This is the simple form of Rayleigh monotonicity. It justifies pulse/check/continue control without a kinetic model *inside the qualified envelope*. In a real bath, deposition, contact chemistry, ionic shunts, and changes in conductivity can break the observed monotonicity; a monotonic trace is a check, not proof of the envelope.

**Electrical readout detail.** A two-terminal measurement includes series lead and contact resistance. If it is naively used as \(G\), it can understate brace conductance and falsely certify (2). Use Kelvin taps at the island and brace-bus boundaries where possible, and qualify an upper bound on all remaining contact contributions. If only total resistance \(R_{\rm tot}\) is available and the series contribution is known to lie below \(R_s^{+}\), a safe brace-conductance upper bound is \(G^{+}\le 1/(R_{\rm tot}^{-}-R_s^{+})\) only when the denominator is positive and no hidden series interface lies inside the brace path. An ionic wet shunt would usually make the apparent conductance too high, but electrode polarization and contact effects can go either way. Dry measurements or a demonstrated de-embedding procedure are necessary.

## Explicit hidden-state counterexample and substantive redesign

World A has all copper braces severed. World B retains one mechanically intact brace of stiffness \(k=1\) in normalized units, while a thin insulating oxide at its island contact or a broken sense metallization makes its measured conductance \(g=0\). Both worlds return the same open-circuit endpoint and can have the same prior conductance trajectory if the contact degrades at the apparent release time. Yet their service stiffness differs by one unit. Equivalently, an insulating polymer residue can mechanically bridge island and frame after the conductive copper has dissolved. In this world \(E/\sigma\) is unbounded on a load-bearing path, so the hypothesis of (1) fails. The patent cited below independently describes a related problem: mechanically anchoring sacrificial residues can remain after electrical shorts have disappeared.

The redesign has **two independent witnesses**. First, manufacture the *actual* temporary braces as the conductance network, rather than relying on a neighboring release coupon whose local etch may differ. Place no uninstrumented temporary support outside that pattern. Second, after electrical acceptance, apply a predeclared force/field sweep through the intended service mode and measure displacement, hysteresis, and return on the *same device*. The direct motion check is the final functional certificate for the tested force, frequency, temperature, and time envelope. It catches the insulating mechanical bridge even when (2) appears to pass. A viscoelastic bridge that yields during one short sweep and recovers later remains a counterexample to an extrapolated lifetime guarantee; extend the test envelope or retain that risk. The conductance bound's possible benefit is earlier/cheaper determination of when to attempt the functional check, and a quantitative limit on residual brace stiffness. No superiority is claimed until measured against the comparators below.

## Strongest equally informed comparison

The incumbent is not blind fixed-time etching. Give it the same substrate layout, bath, process history, electrical pads, optical access, calibration coupons, and final motion assay. It can use (a) the same actual-device electrical reading, (b) a same-wafer electrical test structure, (c) optical backside or pointer motion monitoring where geometry allows, and (d) direct force–displacement acceptance. Existing electrical sacrificial-layer test structures and direct motion endpoint checks are real prior methods. With the same acquired \(M\) and pads, the incumbent can use inequality (1) too. There is no information-theoretic or demonstrated full-resource advantage over this comparator.

The specific distinction to test is whether putting **all removable service load paths in parallel between two isolated electrodes** reduces missed tethering or unnecessary etch compared with a witness coupon or endpoint-by-time, at acceptable added fabrication/readout cost. A comparator with the same actual-device sensing may tie. A direct functional assay may make the electrical bound redundant. The experiment must report that possibility rather than compare only to an intentionally weak fixed-time recipe.

## Acquisition, preparation, control, reliability, and scale

The operation has to acquire, not assume: (i) the as-built map that all temporary load paths are in the sensed brace network; (ii) conservative \(M\) over partial etch, oxidation, cracks, and contacts; (iii) \(K_0^{+}\) and geometry factors \(\alpha_i\); (iv) bath selectivity for the exact device stack and maximum safe exposure; (v) meter noise floor, leakage, lead/contact resistance, and dry-state reproducibility; and (vi) force/displacement assay calibration. Same-stack destructive coupons with deliberately thinned braces are a practical way to challenge the \(E/\sigma\) bound, but a finite sample only qualifies a stated manufacturing envelope. The final motion test is indispensable if that envelope is not comprehensive.

Fabrication costs include extra brace lithography/patterning, an electrically isolated bus, protected permanent sense trace, test pads, and per-device or multiplexed readout. Process costs include copper etchant, bath preparation and refresh, rinse, critical-point or equivalent anti-stiction dry where required, waste handling, process time, and any extra etch/check cycles. Measurement costs include a low-leakage conductance meter, force or magnetic/electrostatic drive, optical displacement readout, calibration coupons, and rejected devices. The tested copper chemistry's reagent amounts and minutes are literature data, not measurements for this proposed stack. Anodic etching adds electrical work, counterelectrode/control hardware, and a precipitation/passivation hazard; it is an optional comparator, not free acceleration.

For \(N\) devices, measuring each island separately costs at least \(N\) endpoint decisions and usually \(N\) motion checks; multiplexers add leakage and switching time. A wafer-summed conductance can certify a sum only under the same material contract and a much tighter aggregate noise floor. If each device has probability at most \(p\) of an unqualified hidden bypass, the chance of at least one such bypass is at most \(Np\) by a union bound; no value of \(p\) has been measured. Processing yield and lifetime cannot be inferred from one accepted device.

## Primary-source inspection and prior-art boundary

1. [Selby and Shannon, *Anodic Sacrificial Layer Etch (ASLE) for Large Area and Blind Cavity Release of Metallic Structures* (Hilton Head 1998)](https://transducer-research-foundation.org/technical_digests/HiltonHead_1998/hh1998_0252.pdf). **Inspected:** abstract, Cu/Ni experimental stack and comparison, results discussing etch-front rates, Cu precipitation, passivation and bubble limits. They experimentally anodically etched copper sacrificial layers under nickel and compared standard etching. They did not establish this report's coupled load-path certificate. Their observed precipitate/clogging directly limits any assumption of simple monotone processing.
2. [*Test structure to monitor the release step in a micromachining process*, US 7,932,727](https://patents.justia.com/patent/7932727). **Inspected:** background and detailed figures 1–9. It uses electrical shorts through residual conductive sacrificial layers to monitor MEMS release and explicitly notes a case where residues mechanically immobilize a structure without an electrical short. This is close prior art for electrical endpoint sensing and a direct warning against equating open circuit with mechanical release. Patent claims/novelty were not exhaustively assessed.
3. [*Integration of Electrodeposited Ni-Fe in MEMS with Low-Temperature Deposition and Etch Processes* (Micromachines 2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5503316/). **Inspected:** Cu etch development, pointer-arm release test, compositions, results, and final cantilever motion verification. It experimentally found Ni–Fe attack and Cu redeposition with an initial persulfate bath, then reports a bath with persulfate, NaOH, and citric acid that released its 300 nm Cu/4 μm undercut pointer structures in 3–5 minutes, with no visible attack under its stated tests. Its pointer motion is an existing functional release witness, and its exact bath performance cannot be transferred to the proposed braces without new tests.
4. [Rondé, Walton, and Terry, *Manipulating Etch Selectivities in XeF₂ Vapour Etching* (JMEMS 2021)](https://eprints.gla.ac.uk/226998/). **Inspected:** author repository abstract and linked data description. It reports that normally resistant neighboring materials can etch much faster in proximity to sacrificial silicon; the associated [primary dataset](https://datashare.ed.ac.uk/items/0c4d195f-61b5-4a34-8fb5-663b45e257bb) describes a severe polysilicon/SiN selectivity example. This argues against casually replacing the wet copper step by nominally selective dry Si etch. No dry-stack substitution is claimed here.

## Decisive experiment and claim boundary

Fabricate a small lot of actual two-electrode copper-braced flexure devices alongside destructive same-stack coupons. Deliberately include randomized blinded cases: clean Cu braces; partly etched Cu; electrically failed but mechanically intact contacts; and insulating mechanical bypasses. Qualify a conservative \(M\) or record its failure, then run an etch/measure/stop protocol with a predeclared conductance threshold and a service-mode force/displacement requirement. Independently image and/or section selected devices after acceptance. Compare false accepts, over-etch damage, yield, wall time, chemical/energy use, and assay cost against (i) optimized fixed-time plus final motion test, (ii) an electrical same-wafer witness coupon plus final motion test, and (iii) actual-device direct motion endpoint control. Keep all methods equally informed about the fabricated design and calibration data.

**Pass condition:** every accepted device in the blinded lot meets the predeclared mechanical response over the registered test envelope; the electromechanical bound conservatively predicts the residual stiffness on the challenge coupons; and the method beats at least one serious comparator on an acquisition-inclusive manufacturing measure without losing reliability. **Kill conditions:** a false electrical acceptance from an intact hidden load path, an unbounded \(E/\sigma\) state within intended use, significant damage/stiction before threshold, or no measured gain over direct functional acceptance. The operation currently establishes only a conditional design theorem and a falsifiable fabrication experiment. It is not a demonstrated new manufacturing capability.
