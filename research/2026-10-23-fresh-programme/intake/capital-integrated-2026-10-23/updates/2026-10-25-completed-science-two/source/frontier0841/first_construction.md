# Independent first construction: oxygen-conditioned hydraulic redistribution

25 October 2026. This note precedes the primary-literature comparison. It records an original working construction, not a claim of novelty or demonstrated biological recovery.

## Opportunity comparison

Three barriers were considered briefly:

1. **Whole-organ vitrification.** Consequence: banking intact organs and perhaps complex neural tissue. The main interacting barriers are cryoprotectant transport/toxicity, ice, thermal gradients, and mechanical fracture. A new viable-path framework could help, but the present candidate mechanisms too readily assume an unbuilt intracellular transport interface and overlap the programme's active thermal investigations.
2. **Selective low-energy recovery from dilute mixed resources.** Consequence: closed resource cycles. Coupled binding/transport ratchets are plausible, but a decisive construction would need verified binding thermodynamics and a complete regeneration cycle; an abstract separation proposal would not suffice.
3. **Reopening and sustaining oxygen delivery after severe ischemia.** Consequence: recovering organs and tissues that conventional circulation cannot rescue, and extending the reversible window of complex biological function. A concrete obstruction is flow heterogeneity: open shunts can consume a perfusion pressure/flow budget while high-resistance territories remain hypoxic. Local oxygen extraction supplies a physical signal of mismatch, but current pumps mainly control aggregate inlet conditions.

Commitment: investigate item 3 at constructive depth. The ambition is recoverable complex function, not merely an improved average oxygen number.

## Candidate mechanism

Use an oxygen-carrying perfusate with a **reversible increase of viscosity in the oxygenated state**. A well supplied branch retains oxygen along its length and remains relatively resistive. A heavily extracting branch spends more of its length in the low-viscosity state. Under a shared pressure or flow constraint this can create passive hydraulic negative feedback.

This is opposite in sign to deoxygenation-induced aggregation and cannot simply be assumed to be a property of ordinary blood. An invented interface would be needed. One specific candidate is an oxygen-ligation-dependent soluble protein/polymer association: oxy-state recognition domains on an oxygen carrier form weak reversible contacts; deoxy-state conversion destroys those contacts. Assemblies must remain nanoscale and non-obstructing, dissociate on the transit timescale, have bounded viscosity, and preserve oxygen release. These requirements are part of the invention, not free inputs.

## Minimal coupled model

For a branch of length L and radius r, with Newtonian local viscosity mu(c),

    Delta p = (8 / (pi r^4)) q integral_0^L mu(c(x)) dx.

Let c be carried oxygen per perfusate volume, including bound oxygen at local equilibrium. Before oxygen limitation, distributed extraction is approximately uniform:

    q dc/dx = -M/L,
    c(x) = c_a - (M/q)(x/L).

If mu increases with c, lowering q lowers the branch's mean viscosity. The geometry-to-flow map may therefore be less heterogeneous than the usual q proportional to r^4 law. This is an analyzable physical feedback, not a controller which reads the whole organ.

Use an ideal two-state rheology first:

    mu(c) = mu_lo + (mu_hi - mu_lo) 1[c > c_*],
    z = (c_a-c_*) / c_a,
    e = M/(q c_a).

For 0 <= e <= 1 (oxygen-supported uptake), the high-viscosity length fraction is min(1,z/e), so

    mu_bar = mu_lo + (mu_hi-mu_lo) min(1, z q c_a/M).

After the switch is reached, branch pressure is a positive linear-plus-quadratic function of q:

    Delta p = R_lo q + R_lo (gamma-1) (z c_a/M) q^2,
    gamma = mu_hi/mu_lo.

The differential logarithmic response d log(q)/d log(Delta p/R_lo) interpolates from 1 to 1/2. Thus the most naive distributed switch gives at most square-root compression in its active regime, not arbitrary equalization. Its dynamic range, inlet high-viscosity segment, and oxygen-carrying capacity must be retained.

## Equally serious alternative

Conventional pressure/flow control plus low-viscosity perfusate and oncotic management may already give greater endangered-territory oxygen delivery for a fixed pressure budget. The adaptive fluid increases viscosity somewhere; under fixed inlet pressure and identical low-viscosity baseline it may never improve absolute branch flow. Any gain may exist only under a finite total-flow budget or a pressure/edema constraint on high-flow paths. This dominance possibility is the first calculation to resolve.

## Discriminating tasks

- Prove the fixed-pressure comparison before claiming rescue.
- Solve branch networks at matched oxygen capacity, total-flow/pump-power/pressure budgets, and peak hydraulic burden.
- Include oxygen-limited uptake, transit delay, bounded rheological response, and a distribution of branch geometry/demand.
- Compare against informed alternatives: uniform low viscosity, conventional viscosity/pressure optimization, direct branch resistance control where anatomically accessible, and established machine-perfusion restoration protocols.
- Read current primary work on ischemic no-reflow, recovery perfusion, and oxygen-dependent materials; retire novelty or effectiveness claims if covered or defeated.
- Preserve a stronger physical explanation even if this first material construction fails.

Scientific state: construction formed; its biological applicability, material feasibility, novelty, and practical advantage are UNKNOWN.
