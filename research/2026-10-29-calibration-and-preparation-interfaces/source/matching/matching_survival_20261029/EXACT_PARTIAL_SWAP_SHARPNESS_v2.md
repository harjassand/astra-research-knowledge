# Exact full-code sharpness, replacing the small-angle-only argument

2026-10-29. Author construction supplied by root; algebra independently checked
by derive_matching_survival_bound. This strengthens Section 4 of
PROOF_MATCHING_SURVIVAL_v1.md without changing its theorem or assumptions.

Let S=S_12 be the ordinary physical SWAP of qubits 1 and 2, and let
U_t=exp(i t S)=cos(t)I+i sin(t)S. This unitary commutes with collective SU(2),
so it preserves the entire singlet sector. Let n>=4 be even.

In a uniform perfect matching, edge {1,2} occurs with probability 1/(n-1).
On that event <M|S|M>=-1. Otherwise qubits 1 and 2 belong to independent
singlets; their reduced state is I_4/4, giving <M|S|M>=Tr(S)/4=1/2.
Therefore

    q = [3(n-2)/(4(n-1))] sin²(t).

The average matching state is P/d, so

    a = Tr(P S)/d = (n-4)/(2(n-1)).

The full-code entanglement fidelity of this leakage-free unitary is
|cos(t)+i a sin(t)|². Hence

    1-F_e = (1-a²) sin²(t)
          = [3(n²-4)/(4(n-1)²)] sin²(t),
    (1-F_e)/q = (n+2)/(n-1)

whenever sin(t) is nonzero. The multiplicative coefficient in the full-code
theorem is thus attained exactly by a physical two-qubit partial SWAP, not
merely approached by an infinitesimal or densely synthesized code operation.
For n=4, d=2 and t=pi/2, the code unitary is traceless: F_e=0 and q=1/2.
The test coefficient 2 is necessary even for a unitary noise operation.

This does not establish sharpness of the extra d/K factor for a proper
subcode, or any worst-case diamond claim without its separate hypotheses.
