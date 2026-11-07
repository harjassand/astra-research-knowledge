# A coherent READ decoder stays inside CFG's proved circuit core

Machinery researcher, 7 November 2026. This adds a safe implementation choice to the frozen [port closure](quantum_ports_closure.md), SHA256 d6d9ba449dc6dae53489cb53055a013ecc5650d65154e83cb65a675df2c36fdd. It leaves its closure, hypotheses, error formulas and polynomial resource conclusion unchanged. It replaces its conservative O(N^3) decoder implementation bound by **O(N^4)** for the entirely coherent implementation below. The encoder remains O(N^3), with waiting locations counted.

The reason is precision of the import. CFG Remark 28 discusses classical controls, but the detailed proof of Lemma 29, inherited by Lemma 40, explicitly factors the auxiliary channel for pure-state preparation, unitary gates and measurements. If an outer adaptive decoder's measurement histories control later gates, the auxiliary channels can be history-dependent. There is no need to rely on a stronger global factorization through such feedback: implement the promised decoder with pure ancilla preparations, quantum unitary gates, and final discarded work. This is exactly the circuit class proved in Lemma 40. No objection to the truth of CFG's intended adaptive extension is needed.

## Explicit reversible construction

Let M<=c_M N be the number of local hubs; every hub has a fixed finite list of candidate local Pauli corrections. The actual energy satisfies U<=c_U u_* N. Fix a deterministic ordering of hubs/candidates and choose

    K_N = ceil(c_U u_* N).

Use DATA, an O(N)-bit syndrome register, O(N^2) fresh history qubits, and constant-size reusable temporary registers.

1. Coherently extract the commuting stabilizer syndrome into initially zero qubits. The joint eigenprojector circuit is standard controlled-Pauli syndrome extraction, with no measurement. Bounded support/incidence gives O(N) nonidle elementary gates, or a larger polynomial bound without any scheduling improvement.
2. Unroll exactly K_N passes through all M hubs. A hub visit uses only the fixed bounded set of syndrome bits needed to evaluate its possible energy changes. Reversibly compute the label of the first candidate with strictly negative energy change, or label zero if none. Write this constant-size label into the visit's fresh history register and uncompute the temporary evaluation while the syndrome is unchanged.
3. Conditional on this stored quantum label, apply the corresponding physical Pauli to DATA and XOR its known syndrome change into the syndrome register. These are fixed finite-arity unitary gates; there is no measurement or classical feedback. Keep the label history so that the whole operation remains reversible.
4. Apply a fixed Clifford unencoder on DATA. Keep its m logical outputs and discard its other DATA outputs, syndrome, temporary and history registers. Final discard can be implemented by measurement with the result unused. There is no later gate conditioned on a discarded work outcome.

Each local truth table has fixed finite size, since it reads exactly the bounded local syndrome neighborhoods of the supplied energy/correction catalog. Its reversible circuit therefore has a fixed cost independent of N. Fixed finite-arity controlled Pauli gates and Boolean permutations can be expressed exactly over a gate palette containing Clifford and Toffoli (or Clifford+T with work). Such a fixed universal palette is within the computational-scheme construction. The whole ideal decoder is a specified finite circuit, with a CPTP extension to every physical input.

## Correctness on the complete promised module

On a promised syndrome the selected move strictly lowers integer U whenever a visit makes an update. If a full pass makes no update and U>0, the active-hub guarantee is contradicted: the syndrome did not change during that pass, so one of its active hubs would have been visited. Thus every full pass with nonzero U makes at least one update. At most K_N passes suffice to reach U=0. After reaching zero there is no strictly decreasing move and the remaining visits perform identity.

The radius/energy argument from Section 4 of the frozen report keeps the entire promised greedy path safe. Every accepted physical move acts as identity on the canonical logical factor up to a phase depending only on syndrome and the move label. The coherent syndrome extraction also acts as identity on that logical factor. Thus, on any superposition

    sum_sigma E_sigma Enc |psi_sigma> tensor |b_sigma>,

including arbitrary logical/gauge/bath/reference entanglement, the complete unitary before the Clifford unencoder has the form

    id_L tensor V_gauge.

The final unencoder and work discard implement the required logical partial trace. Its phases and stored histories belong to the auxiliary channel. The same statement holds for the enlarged common span containing the additional sparse input-interface errors because the distance inequalities in (P.5)--(P.6) identify their canonical logical factor before the first decoder gate. No actual correction history has to be guessed from a marginal channel.

## Paid bounds

There are O(N^2) hub visits, O(1) finite-arity unitary operations per visit, O(N^2) history qubits, and a sequential O(N^2)-gate Clifford unencoder. Hence ideal width and depth are both at most O(N^2). Counting every waiting qubit in every layer gives

    S_D = O(N^4).

This is deliberately conservative; it avoids using free classical computation to reduce the counted noisy width. The nonidle quantum work is smaller, but is not the complete circuit size used in the noise bound.

The unchanged complete bounds are

    epsilon_W,FT <= 2 S_E (cp)^l,
    epsilon_R,FT <= 2(N+S_D) (cp)^l.

For S_E=O(N^3), S_D=O(N^4), and desired bulk error exp(-c_F N), equation (P.12) still gives l=O(N). The full compiled location count, encoded-port size, workspace and duration remain polynomial. All other physical port costs, LS support tails, retained-bath SWAP bounds and endpoint limitations in the frozen report are unchanged.

This implementation also avoids needing noiseless OUTER syndrome-processing hardware. The imported computational fault-tolerance scheme retains whatever classical primitives it itself requires; CFG's cited scheme still assumes its own classical computations are noiseless. That assumption has not been removed.
