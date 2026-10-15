# Physical model challenge: layer-resolved electrochemical control

**Disposition.** Tong et al.'s twisted-bilayer graphene (tBLG) experiment is a strong, independent counterexample to a one-knob transport model: at fixed total carrier density, the signed field and layer-resolved charge determine which layer reacts. It demonstrates an accessible, actively controlled operating regime and supports selective co-design. It does not falsify the supplied conditional passive-support theorem, establish that strain is irrelevant, or demonstrate a battery or civilization-scale advantage.

## Model limitation and experimentally demonstrated operation

A scalar description with one carrier density, one field magnitude, and one shared structural response cannot represent the following operation: hold total density fixed, reverse the perpendicular field, reverse proton flow, and select the other layer for hydrogenation while preserving a conductive layer. The minimal state must retain layer charges, layer reaction states, and signed field/proton direction. A useful bookkeeping state is

\[
x=(n_t,n_b,h_t,h_b,\operatorname{sgn}E,\text{proton-flow direction}),\qquad
u=(V_t+V_b,V_t-V_b),\qquad n_{\rm tot}=n_t+n_b.
\]

The gate sum primarily sets total charge and the gate difference sets the perpendicular field; the paper's Methods also includes quantum-capacitance corrections. Under field-induced polarization, the individual layer densities can move differently at fixed total density. Equal total density and equal field magnitude therefore need not mean equal reaction state if the field sign is reversed.

Tong et al. used a suspended tBLG device over a 10-µm aperture, with proton-conducting HTFSI/PEG electrolyte and PdHₓ gate electrodes. At fixed gate sum Vₜ+Vᵦ = 1 V, corresponding to n ≈ 5×10¹³ cm⁻²—below the ≈1×10¹⁴ cm⁻² monolayer hydrogenation threshold—the field drove proton transport and hydrogenated only the layer facing incoming protons. The other layer remained conductive. Reversing field polarity at fixed n reversed proton flow and selected the opposite layer. The single-layer insulating state persisted for more than 24 hours under fixed gates; lowering |E| below about 0.5 V nm⁻¹ at fixed n restored conductivity and removed the Raman D band. Selective cycling exceeded 1,000 cycles with electronic on/off ratio >10⁴ and cycle-to-cycle variation <6%.

The measurements and the mechanism should be kept distinct. Figure 1 simultaneously records top- and bottom-layer in-plane conductance and out-of-plane proton current under opposite field polarities (the electronic source-drain biases are 2 mV). Raman D-band appearance supports hydrogenation. The layer-resolved carrier-density imbalance is the authors' electrostatic/analytical explanation, not a direct layer-charge measurement. The paper's E–n map and analytical model explain the transition boundaries by one layer reaching the hydrogenation threshold; these are not transferable coefficients for another interface.

## Same-device simultaneous performance and strongest comparator

The 2026 paper's Fig. 3 configures three logic modes in one tBLG device using the same square-wave gate inputs (−1.2 V and +2.4 V). The parallel electronic outputs implement layer-specific NOT gates, a tunnelling NOR, or a total-current NAND; the out-of-plane proton current supplies an XOR output in each mode. The main text gives an electronic on/off ratio of 10⁴ and a proton-current XOR ratio of 10². The Methods section instead says 10⁴ for the proton XOR, an internal discrepancy; use the conservative main-text value unless the figure or source data resolve it. This is a demonstrated same-device, same-input, configurable electronic/protonic operation—not a proposed Astra device.

The strongest comparator is Tong et al.'s 2024 double-gated monolayer graphene experiment, which established independent control of field and density before the tBLG layer-selection result. With a single gate, proton transport drive and doping were coupled: around Vₜ ≈ 1.4 V, graphene conductivity fell by four orders of magnitude and a Raman D band appeared. With two gates, fixing the gate sum at 0.7 V while varying the difference drove strong proton current without hydrogenation; fixing the difference at zero while varying the sum suppressed proton flow but hydrogenated graphene. At n ≈ 10¹⁴ cm⁻², electron-doped graphene was about 30 times more proton-conductive than hole-doped graphene at the same density in the low-field regime, and at E > 0.5 V nm⁻¹ the current approached the electrolyte-limited current, with doping-dependent attenuation.

The tBLG paper reports proton currents about 100 times lower than monolayer graphene at the same E. This is a cross-paper comparator, not a simultaneous matched-device head-to-head. The authors attribute the penalty to proton access being limited to AA regions (about 30% of area) and higher barriers: calculated 1.4 eV for the first layer and 1.7 eV for the second. The AB-stacked bilayer control is proton-impermeable and lacks layer-selective transitions. Thus tBLG buys layer selection and parallel logic, while losing substantially on proton flux; the evidence does not show that it improves net energy per useful proton or a practical membrane/battery metric.

## A discriminating next measurement, not a claimed discovery

The article demonstrates opposite layer selection under opposite field signs and separately demonstrates a low-field erase route. It does not establish whether reversing polarity directly swaps a prepared one-layer-hydrogenated state, first erases it, or transiently hydrogenates both. Test this by preparing each selected state at fixed n ≈ 5×10¹³ cm⁻², reversing signed E without an intervening erase step, and time-resolving both layer conductances, proton-current direction, Raman response, and gate charge. The outcomes distinguish direct layer-to-layer switching from sequential erase/re-hydrogenation or a doubly reacted transient. Acquire switching delay, transition probabilities, transferred charge, and flux under the same operating sequence before proposing quantitative control or transfer. The published opposite-polarity comparison already establishes layer selectivity; the proposed experiment only resolves the transition path.

## Scope for co-design

This evidence expands the intervention set beyond a fixed passive mechanical boundary: active electrostatic control plus an internal layer degree of freedom can separate transport from reaction and select where reaction occurs. That supports the possibility of useful/harmful process co-design, but it does not refute a conditional result about mechanical support under specified coefficients. Nor does it provide those coefficients or transfer the effect to hBN defects, Li-metal interfaces, or other battery geometries. A separate 2026 double-gated Li⁺ study reports independent density/rate control in a micron-scale interfacial channel, but it is not a through-plane hBN/Cu battery test and is not needed to establish the graphene result.

## Primary sources

- J. Tong et al., [“Layer-selective hydrogenation and proton transport in twisted bilayer graphene,” Nature Communications 17, 4873 (2026)](https://doi.org/10.1038/s41467-026-71147-y). See Figs. 1–3 and Methods; source data are linked at [Zenodo record 18783917](https://zenodo.org/records/18783917), not downloaded for this note.
- J. Tong et al., [“Control of proton transport and hydrogenation in double-gated graphene,” Nature 630, 619–624 (2024)](https://doi.org/10.1038/s41586-024-07435-8). See Figs. 1–3 and Extended Data Fig. 9; replication data at [Zenodo record 10944915](https://zenodo.org/records/10944915).
