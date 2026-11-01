# Explicit ideal readout: no minimum-weight oracle

## Source radius checked

Leverrier–Zémor, *Decoding quantum Tanner codes*, arXiv:2208.05537v3, Theorem 13 (printed p20): the sequential decoder with parameter epsilon corrects every sector error of weight strictly below

D_seq(epsilon) = 2^(-11) min(epsilon^3/16, kappa_rob)
                (1-epsilon) delta^2 kappa_rob^2 n/Delta.

Primary inspected directly: https://arxiv.org/pdf/2208.05537 . The algorithm returns a correction differing from the error by a stabilizer, not merely a matching syndrome. It runs in linear time for fixed local-code parameters. Use the smaller radius of the two CSS sectors. In particular epsilon=1/2 gives

D_seq = 2^(-12) min(1/128,kappa_rob) delta^2 kappa_rob^2 n/Delta.

This finite-radius prior theorem is the only decoder guarantee imported here.

## Readout construction and condition

Let R be the radius used in the enlarged-system low component. Require additionally

R < (4/5) D_seq.

The low-component analysis uses representatives E_s with enlarged Pauli weight r_s<R/4, modulo the protected subsystem's gauge. These representatives are analytical labels; the implementation does NOT compute them.

The actual ideal consumer is:
1. Apply U†, the fixed two-layer controlled-X/controlled-Z frame removal on the 5n-qubit enlarged system (2n controlled gates, reverse of the encoding-frame order).
2. Measure the original code's stabilizer syndrome on the n data qubits.
3. Run the source's actual sequential Tanner decoder independently for the X and Z components and apply its Pauli correction.
4. Discard the four auxiliary witness qubits per data qubit. If bare logical output is required, use an ordinary ideal stabilizer unencoding circuit, computable and implementable with polynomial overhead.

Because U acts in disjoint five-qubit blocks, U†E_sU is a Pauli whose DATA support is at most 5r_s<5R/4<D_seq (a conservative bound). Each CSS component is no larger than this total data support. Both source decoders therefore return a correction equivalent to that component modulo original stabilizers. No canonical minimum-weight enlarged representative or global minimum-energy decoder is executed.

## Coherent errors and gauge do not invalidate the consumer

Write the ideal enlarged ground-space isometry as U(V_code tensor V_aux), where auxiliary repetition-pair logicals are gauge. For every E_s in the admitted family, conjugation separates its Pauli into data and auxiliary factors. The fixed syndrome-based data recovery corrects its data factor on every original logical state, including states entangled with a reference. In a Stinespring implementation of recovery, its action on each such error is identity on the protected logical subsystem tensor an operator on gauge plus syndrome/environment.

By linearity, this same recovery corrects the linear span of the admitted E_s with arbitrary gauge operators. Cross terms between distinct data syndromes are transferred to the discarded syndrome register; equal-syndrome errors differ by stabilizers on the protected code. Consequently coherent superpositions, coherent witness states, and protected-logical/gauge correlations produced by an admitted error channel require no stochastic-Pauli replacement or assumption of classical witnesses.

This establishes an explicit IDEAL terminal consumer for the low component. The parent's leakage estimate can be composed with this CPTP map by contractivity. It does not add a reliable online classical processor to storage: the computation occurs once, at requested final readout.

## Qualification / scope closure

Ideal readout is not a demonstration of reliable finite-duration noisy readout at nonzero physical noise. Gate errors during U†, measurement noise, classical decoder hardware faults, new data faults during decoding, and noisy final unencoding remain outside this ideal consumer unless separately bounded. Initial encoded-state preparation is likewise not free. The early cost audit remains unchanged: no useful finite physical realization or practical threshold was established. The sufficient proof constants do NOT prove a physical noise floor or impossibility.

## Rate convention clarification

At each vertex/type the ideal controller can be written as ONE fixed CPTP channel Phi_v with Kraus operators T_l Pi_l, for local joint-syndrome patterns l, including identity moves when no improvement is selected. Sum_l Pi_l=I, and L_v=kappa(Phi_v-id). Thus kappa is the total attempt rate per vertex/type, not a rate per table entry. Predicates need only the commuting joint-syndrome information, not an unnecessary measurement of the gauge frame. Hardware imperfections must be bounded as aggregate local channel/generator errors; assigning a small error separately to exponentially many truth-table branches does not produce a free aggregate guarantee. Total physical noise budgeting uses N_ext=5n and the actual Pauli-expansion/incidence factors.
