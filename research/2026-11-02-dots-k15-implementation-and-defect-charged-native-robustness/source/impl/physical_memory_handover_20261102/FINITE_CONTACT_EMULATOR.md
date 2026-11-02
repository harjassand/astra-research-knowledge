# A fixed-scale finite-duration contact emulator

The private local transaction proof need not regard a target unitary channel as an exactly instantaneous physical contact. This note supplies a finite-duration replacement in a declared time-independent finite-range Markov model. It does not solve protected recursive scheduling or native-Gibbs preparation.

## Quantum gate and timer

For a fixed-support target U=exp(-i H tau), use a q-stage classical clock with forward transitions j -> j+1 at rate gamma=q/tau. While 0<=j<q, the local payload Hamiltonian H is on; in the terminal clock state it is off. The Hamiltonian and jump operators are time independent on payload plus clock. Ideal forward clock jumps do not inspect or alter the payload, so their arrival time T is Gamma(q,q/tau), independent of its quantum/reference state.

Averaging over completion times implements Phi(X)=E[exp(-iHT) X exp(iHT)]. A first-moment bound is 2||H|| tau/sqrt(q), but the root supplied the sharper centered estimate. Put L=-i[H,.] and Delta=T-tau. Since E Delta=0, Taylor's integral formula cancels the first-order term, and for every real s,

    ||L^2 exp(s L)||diamond <= 4 ||H||^2.

Consequently

    ||Phi-Ad_U||diamond
       <= 2 ||H||^2 E Delta^2
       = 2 ||H||^2 tau^2/q.

This uses only the second moment, not an exponential-moment assumption. It is valid for the independent ideal timer; clock/contact faults correlated with the payload cannot be assigned the same mean-zero cancellation. The q-state clock, finite rate q/tau, bounded Hamiltonian norm, completion record, and energy/entropy flux are physical resources, not zero-cost precision.

This is a mathematical contact emulator, not a claim that its classical clock is intrinsically perfect. Clock initialization errors, erroneous transitions, faulty completion flags, imperfect H, and reset errors are local perturbations of the enlarged-system generator. They must remain in the same fixed-time-box fault budget as payload noise. A local repair word may restore an invalid timer, with bounded local damage charged to the initiating fault. The resulting channel is only approximately the requested gate, even in the ideal clock model, and its timing approximation is part of the error allowance.

## Fixed rate cap and continuing exposure

If the available clock transition rate is capped at Gamma, do not increase q at fixed tau for free. Write U=exp(-iK), where a=||K|| is fixed, set tau=q/Gamma, and implement H=K/tau. The ideal timing error is at most 2a^2/q. A per-tick channel error epsilon_tick contributes O(q epsilon_tick), not O(epsilon_tick), while a local enlarged-module Markov fault-strength budget epsilon_total(q) contributes O(epsilon_total(q) q/Gamma). Thus

    error <= 2a^2/q + C q epsilon_tick
                 + C epsilon_total(q) q/Gamma + epsilon_contact.

If the combined coefficient B=C(epsilon_tick+epsilon_total/Gamma) can genuinely be treated as fixed over the chosen timer family, optimizing A/q+Bq gives q of order sqrt(A/B) and error O(sqrt(A B)). But the clock volume itself may increase epsilon_total(q); that dependence must not be hidden in this optimization.

The conservative existence statement fixes a finite q first to make the ideal timing error small, charges its finite dimension, rate cap, number of transitions and heat, and then requires every actual hardware fault contribution to lie below the remaining fixed threshold. This gives an open sufficiently-low fixed-noise operating region, not arbitrarily accurate gates at fixed physical noise by q->infinity. All constants are independent of total memory size.

## Finite-purity reset

A reset contact can similarly run local thermal relaxation for a finite guarded duration. If its reset-channel diamond convergence bound to the replacement channel with state rho_th is A exp(-kappa t), averaging over an independent q-stage timer of mean tau bounds the residual by

    A E exp(-kappa T) = A (1+kappa tau/q)^(-q).

The target reset state differs from the desired pure workspace state by its fixed thermal impurity, which is another charged preparation error. Choose fixed tau,q and a fixed finite gap/temperature to put both contributions below a fixed threshold. There is no perfect pure ancilla operation. A physical biased timer also has backward transitions and imperfect reinitialization; finite affinity/pumping may suppress, but not delete, those errors. Its reset work and dissipation are charged on every cycle.

## Locality and composition limits

The timer and payload occupy a fixed-size neighborhood. Controlled H and clock jumps have fixed support and finite range; strictly two-body elementary hardware requires an additional constant-size compilation with its own faults and duration. No higher-level logical acquire, commit, or timer is thereby made microscopic. A whole growing circuit cannot share this one timer while its payload remains unprotected: the shared-stall and macrorestart objections still apply.

At fixed scale this removes the need for exact timing or noiseless instantaneous release. At growing scale the missing operation is still a recursively protected causal executor, or a different clock-free correction architecture. The same-resource active comparator gets the identical timers, thermal reset supply, Hamiltonian controls, local dimension, and energy throughput.
