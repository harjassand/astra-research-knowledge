# A deliberately high-oracle retained-memory source
2026-10-29. New family, not a retuned replacement for the preceding negative fixture. Parameters fixed in HIGH_ORACLE_PLAN_v1.json before simulation.

Memory has dimension4 and projectors Pi_0=|0><0| tensor I, Pi_1=|1><1| tensor I. Fix a noncommuting unitary U and A_m=Pi_m U. Then sum A_m^dagger A_m=I and A_0^dagger A_1=0. On two data qubits choose P_0=I and P_1=Z tensor Z. Pure flags are
 |phi_m>=sqrt((1+c)/2)|0>+(-1)^m sqrt((1-c)/2)|1>, c=1/5.

The source isometry before its final coupling is sum_m P_m tensor |phi_m> tensor A_m. Its cross terms vanish in V^dagger V because A_0^dagger A_1=0. Append the actual output unitary C=exp(-i kappa Z_flag tensor Q_memory), where Q=I tensor X commutes with both Pi_m, and kappa=1/100. This remains an isometry. Memory is retained between calls without reset.

Because C preserves the orthogonal memory ranges Pi_m, tracing memory removes cross-label terms. At every actual history, the fresh-input channel is Pauli+flag with unnormalized flag operators sigma_m=Tr_memory[C(|phi_m><phi_m| tensor A_m rho A_m^dagger)C^dagger]. These operators can vary with the conditional quantum memory state, and the flag is correlated with within-block memory. Measuring the flag can steer that memory; different shadow/evaluation instruments genuinely induce different future occupations. No classical Markov replacement is made.

Without C, the fixed X-basis flag measurement, followed by the corresponding P_m correction, succeeds conditionally on EITHER label with probability h=(1+sqrt(1-c^2))/2. Hence it has Bell fidelity h for every prior and every source memory state. For any joint flag-memory state, the half-trace distance between C rho C^dagger and rho is at most ||C-I||op=2 sin(kappa/2)<=kappa. Any measurement success probability therefore changes by at most kappa. The SAME fixed receiver consequently achieves
 F_e >= (1+sqrt(1-1/25))/2-1/100 > .97989
at EVERY conditional history, independent of the source-memory state or actual earlier instruments. This is an informed benchmark; its flag frame is not supplied to the learner. The full-CPTP oracle is at least this large because the source is Pauli+flag. Nothing claims the learner already reaches the benchmark or that this source family is generic unknown noise.

Rank-two branch memory can retain coherence and is rotated by U between calls. Noncommuting conditional-state diagnostics, if reported, demonstrate only the stated simulator mechanism, not an acquired proof that classical hidden-state models cannot reproduce its records.
