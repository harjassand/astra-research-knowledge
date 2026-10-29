**I completed a principle linking protection density, quantum reconnection and purification flow—even when the encoding and recovery mechanism are allowed to change.** It provides a way to assess a protected computing resource without committing to one syndrome circuit, receiver or reset schedule.

The proofs, constructions, executable checks and actual internal reviews are preserved in :chatgpt-content-reference{index="3"}[README.md](producer-workspace/README.md).

## 1. Mixed information consumes protection capacity

Consider an encoder carrying a logical space of dimension \(K\) into \(n\ge3\) nodes of dimension \(d\), with exact recovery after losing any one node. The completed theorem gives

\[
\boxed{
S(J)+\frac{n}{n-2}\log_2K
\le \sum_i S(A_i)
\le n\log_2d,
}
\]

where \(J\) is the normalized Choi state of the encoder.

This quantifies how much mixed preparation or gauge information the protected encoding can contain. At the packing limit \(K=d^{n-2}\), it forces \(S(J)=0\): **the encoder must be an isometry**, even if its implementation was allowed to discard an environment or prepare mixed gauges.

The coefficient is attained by a construction: append independent mixed gauge factors inside every node of a supplied saturated code. Distinct exact implementations were independently checked. These examples also disprove a tempting stronger claim based on gauge **rank**.

There is a useful uniform channel consequence:

\[
\min_{W\ \mathrm{isometry}}
\frac12\|\mathcal N-\operatorname{Ad}_W\|_\diamond
=1-p_{\max}(J).
\]

A crucial review correction is retained: when a preparation record selects the decoder, these formulas apply **to each normalized record branch**. Applying them to the unconditioned mixture requires common decoders that work without that label.

The proof uses established entropic Singleton machinery and common-decoder reductions. The contribution here is the derived entropy identity, its matching construction and the operational bridge; historical priority for these derived results has not been exhaustively established. :chatgpt-content-reference{index="0"}

Full derivation: :chatgpt-content-reference{index="4"}[CHANNEL_ENCODER_RIGIDITY.md](producer-workspace/CHANNEL_ENCODER_RIGIDITY.md).

## 2. This closes a repeated-operation argument

I then connected rigidity to the actual-record machinery.

Exact record-controlled recovery forces each nonzero checkpoint branch to have an input-independent probability and a normalized encoder channel. At maximum packing, rigidity makes that branch isometric. Its code/reference state therefore factors from the old apparatus, and every newly lost node has the independent state \(I_d/d\).

For \(N\) fresh, complete, nonreturning losses, the resulting retirement bound is

\[
\boxed{
S(F)\ge N\log_2d-\bigl[S(M_N)-S(M_0)\bigr].
}
\]

Here \(M_N\) includes all returning quantum memory and remaining supplies; \(F\) includes genuine retirement and the purifiers required for actual classical records.

**The conditions matter.** The proof includes all initial mixed resources and their purifiers, permits subsequent pure input ports, and retains internally generated gauge purifications. The record must be classical jointly against the inaccessible systems and returning memory—not merely diagonal in its own marginal. Those are explicit interface premises.

Separately, if a replacement protocol can attain Schmidt number at most \(M\) across its defined replacement/helper cut, its error from a saturated, exactly protected target is at least

\[
\max(0,1-M/d).
\]

Thus exact restoration needs \(M\ge d\). Direct entangling interactions, shared entanglement and quantum messages are valid ways to supply that connection, with their actual costs counted. This is **not automatically an additive contact count or bitrate**.

Below maximum packing, the retained rotating-spare construction genuinely changes what can be done. It can leave the newest replacement disconnected while using an older spare, paying for that spare’s later coherent access.

The combined, independently reviewed result is in :chatgpt-content-reference{index="5"}[PROTECTION_FLOW_COROLLARY.md](producer-workspace/PROTECTION_FLOW_COROLLARY.md).

## 3. The constructive side survives strong conventional comparisons

The work also produced usable recovery and supply constructions.

Optimized conventional recovery can emit the restored data directly, improving our generic two-pass complete-error bound from \(2a\) to \(a\). Its remote delivery, control embedding and work-state conditions remain attached.

For biased fixed repair resources, I constructed a deterministic causal factory using preparation, coherent compression, transmission and expansion. It requires no rare postselection or hypothetical repeated starts. This builds on conventional entanglement dilution and explicit conditional state preparation. :chatgpt-content-reference{index="1"}

Its finite costs prevent an inflated advantage claim. For one million pairs with spectrum \((4/5,1/5)\) and total **source-comparison allowance** \(10^{-3}\), an 8,192-pair block uses about **0.775 transmitted qubits per pair**, but double buffering requires **32,768 pair-bank qubits**, before arithmetic and message work. Preparation time, holding noise and link service remain additional obligations. Direct coupling or uncompressed delivery may win. Saturated codes have flat node spectra, so this compression offers no saving there.

Construction and certificates: :chatgpt-content-reference{index="6"}[CAUSAL_PAIR_FACTORY.md](producer-workspace/CAUSAL_PAIR_FACTORY.md).

**What this enables:** we can now distinguish economies obtained through extra protection space, quantum connections, returning memory and retirement streams while allowing the architecture itself to change. That is a stronger design instrument than optimizing a fixed recovery circuit.

The main remaining scientific boundary is approximate future protection under a real service and noise interface. The present results establish neither a device threshold nor a reset-energy advantage. All substantive corrections and useful failures are preserved; the final integrity check passed **132 receipt pins and 463 unchanged predecessor files**.