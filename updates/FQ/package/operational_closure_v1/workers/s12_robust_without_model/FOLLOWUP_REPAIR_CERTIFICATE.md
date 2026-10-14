# S12 follow-up — what dry conductance can certify about a repaired metallic strut

**Status, 15 October 2026:** Exact conditional derivation and counterexamples. No strut was fabricated, plated, measured, or mechanically tested here. The result concerns **small-signal axial stiffness**, not tensile strength, toughness, fatigue life, or repair novelty.

## Direct answer

**Yes, under a one-dimensional shared-path model:** for a straight axial strut with any unknown positive cross-section \(A(x)\), if every load-bearing and electronically conducting segment has local \(E(x)/\sigma(x)\ge m>0\), the bulk axial stiffness obeys \(k_b\ge m g_b\). The shape and local plating thickness need not be reconstructed. **No, for an arbitrary three-dimensional conductive repair or arbitrary contacts:** a conductive path can bend, slip, run around the load path, or terminate in an electrically good but mechanically unbonded interface. Dry terminal conductance alone cannot rule those out. A wet electrochemical current is still further from a structural certificate because electrolyte can provide an ionic path.

## Exact one-dimensional proof and cross-section scope

For a uniform axial force and Ohmic current along a continuous straight strut of length \(L\), let \(B(x)=E(x)A(x)\) be its local axial rigidity and \(S(x)=\sigma(x)A(x)\) its local electronic line conductivity. With ideal end contacts,

\[
C_b:=k_b^{-1}=\int_0^L\frac{dx}{B(x)},\qquad
R_b:=g_b^{-1}=\int_0^L\frac{dx}{S(x)}.
\]

If \(B(x)\ge m S(x)\) almost everywhere, then \(C_b\le R_b/m\), hence

\[
\boxed{k_b\ge m g_b.}\tag{1}
\]

For a single metal whose current-carrying section is exactly the strain-carrying section, \(B/S=E/\sigma\); arbitrary changes in the unknown positive \(A(x)\) cancel. For a **bonded, co-strained composite deposit**, \(B=\sum_j E_jA_j\) and \(S=\sum_j\sigma_jA_j\); the same conclusion holds if every included constituent has \(E_j/\sigma_j\ge m\). This includes unknown local thickening only when every electrically counted deposit actually shares axial load. A conductive coating that slips on the parent metal contributes to \(S\) but not to \(B\), so the premise fails.

The word “arbitrary” above means arbitrary **axial cross-section profile within the 1D model**. It does not cover a winding 3D filament. For a slender U- or S-shaped wire, terminal separation in the service direction can be taken up mainly by bending. Electrical conductance scales as \(\sigma A/L\), while bending stiffness scales as \(EI/L^3\); their ratio is of order \((E/\sigma)(I/(AL^2))\), arbitrarily smaller than \(E/\sigma\) for a thin wire. A manufactured straight guide or post-repair imaging/assay must exclude such bypass geometry before using (1).

## Both contacts: exact sufficient condition and a usable weaker bound

Let the two terminal interfaces have **electrical series resistances** \(r_L,r_R\ge0\) and **axial mechanical series compliances** \(c_L,c_R\ge0\) on the service branch. Let \(r_{\rm lead}\ge0\) be lead resistance. Suppose there is no parallel electrical leakage or second structural load path. Then the measured dry two-terminal conductance and joined stiffness are

\[
G=\frac{1}{R_b+r_L+r_R+r_{\rm lead}},\qquad
k=\frac{1}{C_b+c_L+c_R}.
\]

A **sufficient aggregate condition on both contacts** is

\[
\boxed{c_L+c_R\le (r_L+r_R)/m.}\tag{2}
\]

The stronger, individually checkable conditions \(c_L\le r_L/m\) and \(c_R\le r_R/m\) also suffice. Combining (1) and (2) gives \(C_b+c_L+c_R\le(R_b+r_L+r_R)/m\le 1/(mG)\), and therefore

\[
\boxed{k\ge mG.}\tag{3}
\]

Condition (2) is not a law of metal contacts. If the bulk achieves only the lower material ratio \(E/\sigma=m\), it is the exact worst-case aggregate condition for (3) when lead resistance is ignored. Extra *electrical* series resistance by itself only lowers \(G\), making a lower stiffness bound more conservative; uncontrolled *mechanical* contact compliance destroys the inference. A bonded contact could have very low electrical resistance and nonzero compliance, so (2) may be too strong to certify in practice.

A more usable interface contract is an independently measured upper bound \(c_L+c_R\le c^{+}\). It yields, without knowing the individual electrical contact resistances,

\[
\boxed{k\ge\left[\frac{1}{mG}+c^{+}\right]^{-1}
=\frac{mG}{1+mGc^{+}}.}\tag{4}
\]

With conservative lower endpoints \(m^{-},G^{-}\), a target \(k\ge k_{\rm req}\) is certified if

\[
\frac{1}{m^{-}G^{-}}+c^{+}\le \frac{1}{k_{\rm req}}.
\tag{5}
\]

The contact-compliance bound must hold for **both ends**, in the actual load direction and over the stated force, time, and temperature envelope. If it is unavailable, no positive lower bound on joined stiffness follows from \(G\), however large the conductance becomes. Four-wire sensing can remove conservative lead resistance but cannot establish mechanical bonding. If an upper bound \(g_{\rm leak}^{+}\) on nonstructural dry shunt conductance is acquired, replace \(G^{-}\) by \(\max\{0,G_{\rm measured}^{-}-g_{\rm leak}^{+}\}\) only after verifying the parallel-circuit decomposition. An unbounded shunt leaves no useful certificate.

## Exact falsifiers: contacts, liquid, and strength

1. **Good electrical contact, failed mechanical contact.** In normalized units take \(R_b=C_b=m=1\), \(r_L=r_R=0\), \(c_L=1,c_R=0\). Then \(G=1\) but \(k=1/2<mG=1\). More sharply, a plated metal filament merely touching one pad can carry a dry low-bias current under compression while the joint has zero tensile stiffness after it separates. Both cases satisfy the bulk material condition and fail only at the interface. A high conductance endpoint would falsely accept the tensile repair.
2. **Wet ionic shunt.** With no metallic bridge at all, let electrolyte between electrodes have ionic conductance \(G_{\rm ion}>0\). A wet two-terminal current reports \(G_{\rm wet}=G_{\rm ion}\), while axial strut stiffness is zero. Faradaic current and polarization make the relation to metallic conductance still less direct. Measure the electronic low-bias response after rinsing/drying, or validate an independent decomposition; electrochemical plating current is not the \(G\) in (3)–(5). Dry metallic redeposition outside the load path is another possible shunt.
3. **High stiffness, arbitrarily low strength even with perfect contacts.** Set \(L=1\), \(E=\sigma=m=1\), and \(A(x)=1\) except for a notch of length \(\delta^2\) and area \(\delta^2\). Then \(R_b=C_b=2-\delta^2\), so \(G=k=(2-\delta^2)^{-1}\to1/2\). If local yield stress is bounded by \(Y\), the tensile force capacity at the notch is at most \(Y\delta^2\to0\). Thus even an exactly valid stiffness-conductance certificate says nothing about required proof load under unrestricted fine geometry. A minimum bottleneck length/shape bound, a lower yield or interface-strength bound, and a failure test are additional acquisitions.

## Implication for the proposed repair operation

Bounded geometry that retains the intended routing, electrochemical initiation at a gap, and subsequent chemical thickening are a plausible **process contract**, but they do not establish the assumptions above. The first electronic bridge can be a narrow dendrite, a weakly attached film, or a shunt. Later deposition can raise \(G\) while leaving an oxide-bearing weak interface or a short fine notch. Qualify the actual deposit's \(E/\sigma\) lower envelope, two interface compliances, electronic path exclusivity, and axial geometry before treating a dry \(G\) threshold as a stiffness certificate. Even if all pass, use a direct proof-load and displacement assay for a strength-bearing repair. A destructive shear/tensile sample from the same lot helps characterize the process but cannot replace a task-specific proof test when hidden device-to-device defects matter.

The strongest equally informed comparator already grows metal at fractures, controls deposited volume/geometry, and directly assays mechanical strength. The [2023 electrochemical-healing paper](https://psl.design.upenn.edu/wp-content/uploads/2023/03/Advanced-Materials-2023-Hsain-Electrochemical-Healing-of-Fractured-Metals.pdf) uses passivation to localize deposition, a geometric/mechanical model, pulsed plus potentiostatic plating, tensile tests, complex printed structures, and cost scaling. A [2022 electrodeposited Cu butt-joint study](https://www.jstage.jst.go.jp/article/matertrans/63/6/63_MT-MC2022009/_html/-char/ja) found very low strength at its early partial-fill stage and a later fully filled joint with about 240 MPa shear strength, while observing oxide-bearing fracture interfaces. [US 4,994,154](https://patents.justia.com/patent/4994154) already describes one electrochemical step to establish electrical continuity and a second to thicken the copper bridge. These are direct prior-art barriers to a novelty claim for initiation-plus-thickening or mere conductance feedback. No evidence here shows the proposed certificate beats direct force acceptance after charging bath preparation, coating, rinse/dry, calibration, electrical measurement, proof loading, failed repairs, and lifetime validation.

**Decisive test:** on geometry-controlled struts, deliberately vary interfacial oxide/adhesion and introduce subresolution notches while matching dry terminal \(G\). Blind-predict small-signal axial stiffness using (4), then measure both stiffness and tensile proof-load survival. Include a disconnected strut immersed in plating bath and a nonstructural metallic shunt. If the contact/geometry-validated bound survives but strength at a fixed \(G\) varies, retain the scoped stiffness result and require the direct force assay. If even stiffness violates (4), the claimed material/contact interface was not acquired. No novelty or operational advantage is established by the current derivation.
