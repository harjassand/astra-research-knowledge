# Exact hard-core clock intertwiner (root construction, independently checked)
Date: 2026-10-29. This closes the overlapping-pending-update objection in DERIVATION.md **at the many-body Hamiltonian level**. It does not yet close the two-body/noisy compiler.

Let G be the bounded-degree conflict graph of fixed-size update boxes: edges mean overlapping data support. For each x, Φ_x(ρ)=Σ_s K_xsρK_xs† is CPTP, V_x=Σ_s K_xs⊗|s>_x<0|, Q_x=I−P0_x. Set

H_phys=Σ_x g_x(V_x+V_x†) Π_{y~x}P0_y,
L_xs=√κ_x I⊗|0>_x<s|.

For an independent set S of G define W_S|ψ>=(Π_{x∈S}V_x)(|ψ>⊗|0...0>). Its factors have disjoint data support and distinct ancillas. Therefore W_S†W_S=I; different S have orthogonal ancilla occupation patterns. Let

W: |ψ>⊗|S> ↦ W_S|ψ>.

This is an isometry from data × independent-set clocks into the full physical Hilbert space.

Define b_x|S>=|S\{x}> if x∈S, zero otherwise, and H_c=Σ_x g_x(b_x+b_x†), where addition by b_x† is allowed only if the resulting set is independent. Then the following are exact operator identities:

H_phys W = W(I⊗H_c),
L_xs W = W(K_xs⊗√κ_x b_x).

Proof of first identity: if a neighboring clock is excited, the physical term vanishes. Otherwise V_x adds x when x is absent; V_x† removes x when present, since V_x†V_x=I on the ready sector. All other active boxes are disjoint from x, so their V_y commute through. Proof of second: the jump annihilates sets not containing x; on sets containing x it contracts |s> in V_x to K_xs, which commutes with every remaining V_y.

Moreover Σ_s (K_xs†K_xs)⊗κ_x b_x†b_x = I⊗κ_x n_x. Thus the encoded no-jump generator is data-trivial, I⊗(H_c−iΣκ_x n_x/2). Conditional on emission times and locations, the clock evolution is independent of the data and each emission applies precisely Φ_x. Conditional on resolved Kraus labels, it applies K_xs as an instrument. The post-emission clock vector is b_x times its previous vector, independent of the label s. This remains true for mixed or reference-entangled data.

The reduced clock master equation itself closes:

L_clock(c)=−i[H_c,c]+Σ_x κ_x D[b_x](c).

The clock need not be a classical Markov independent-set process; coherent amplitudes remain. Therefore its local progress and multi-box tail estimates still require proof. The isolated-node law reduces to the exact three-phase waiting distribution in DERIVATION.md.

## Local decoding / retained memory
There is a constant-depth local unitary extension of W. Embed each abstract binary clock |0>,|1> into ready state |0> and one selected excited state |1> of its physical ancilla. For each box choose a unitary U_x that:
1. is identity on data⊗|0>,
2. preserves the excited-ancilla sector,
3. maps |ψ>⊗|1> to Σ_s K_xs|ψ>⊗|s>.
Such an extension exists because the right side is an isometry into data⊗excited and is orthogonal to the ready sector. Color G using at most D+1 colors and apply U_x color by color. On an independent-set input, every active U_x acts on disjoint data supports, while inactive U_x is identity. The product U therefore restricts to W, independent of color order.

This implies that conjugating a physical local error by U expands its support by only a fixed neighborhood, independent of N and runtime. It does **not** automatically prove a fault-path threshold: errors can leave the legal independent-set/encoded-excited subspace, producing clock leakage, and the effective data schedule is random/coherent. Still, the encoding does not hide a nonlocal decoding requirement. Local observables can be decoded by a constant-size circuit; global decoding has constant depth (with gates of fixed support).

## Limitations
- The blockade projectors and V_x are many-body, although bounded range/arity/norm for fixed update rules. No claim of two-body completion.
- Upward thermal reset jumps generally leave the encoded subspace and must be treated as real noise, not ignored.
- A physical data readout without decoding is not automatically the abstract logical data marginal; pending V_x dress it. One may apply the above decoding, or stop the drives and allow pending clocks to emit, but these are distinct readout protocols with their own noise/authorization assumptions.
- Sparse excited clocks induced by noise may temporarily violate the independent-set constraint. Decay repairs occupation but can corrupt local data; a local cluster bound is still required.

## Verification
hardcore_test.py tests conflict path x−y−z, with x and z acting on different data qubits via nonunitary amplitude-damping maps (different bases), and y acting by a CNOT on both. All ancillas are qutrits. The independent set {x,z} checks simultaneous disjoint updates; y checks true conflicts. Isometry and Hamiltonian intertwining residuals are below 9e−16; all jump intertwining residuals vanish numerically. This is a verification example, not a substitute for the algebraic proof.
