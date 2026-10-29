# A fixed controller on the admitted nominal stabilizer family

29 October 2026. This instantiates the nominal-operation hypotheses of
PROOF.md; it does not supply its unproved classical persistence event.
The accepted earlier nominal Gibbs encoder/decoder and distance/admissible
syndrome relations are reused at their actual scope, not re-audited.

Let H0=sum_a(I-S_a)/2. For a single-site seed Pauli P, let Pi_omega be
the mutually orthogonal projectors onto the energy-change values omega
of applying P. They are functions of the at most D incident checks,
sum_omega Pi_omega=I, and are supported inside a fixed neighborhood of
at most 1+D*w qubits. The nominal thermal seed generator is

    L_P=sum_omega gamma(omega) D_{P Pi_omega},
    gamma(omega)=1/(1+exp(beta omega)).                    (1)

Define instead a local Poisson attempt channel

    Q_P(rho)=sum_omega [gamma(omega) P Pi_omega rho Pi_omega P
                    +(1-gamma(omega)) Pi_omega rho Pi_omega]. (2)

It measures omega, flips P with the specified probability and discards
the outcome. The coin is independent of the quantum state before the
syndrome-based decision, and its choice can be included in the fixed
nominal schedule in the proof. The attempted channel is trace preserving
and has rate one. Direct expansion gives the exact identity

    Q_P-id = L_P+sum_omega(1-gamma(omega))D_{Pi_omega}.     (3)

The auxiliary coin need not be a continuous random oracle: partition the
unit interval at the finitely many values gamma(omega). Only a constant
finite set of coin symbols is required; at the admitted rational
temperature their probabilities are rational. Equivalently these
probabilities are already coefficients of the fixed local channel (2).
No externally generated event clock or sampled coin stream is supplied
to the mathematical controller.

Thus the change from the admitted controller consists ONLY of additional
bounded-local syndrome dephasing. On a syndrome-diagonal state its Pauli
transition rates are exactly (1). On a nominal Gibbs state the added
terms vanish. They also annihilate every corrected logical observable
which commutes with the checks. The nominal Gibbs encoder, same Pauli
module and same decoder therefore remain the declared input/receiver.
Unknown energy-changing errors do not make their perturbed Gibbs state
stationary; no such statement is used.

Sum (2) over the 3n single-site Pauli seeds, retain the check Hamiltonian
if desired, and add Gamma(M_a-id) per check as in PROOF(1). Every
nominal operation now has an independent, state-independent Poisson
attempt clock built into its Lindblad representation. There is no stored
clock phase to repair, and no fresh control record that has to be retained
outside the system. The actual time-independent controller is selected
from H0, beta, the local check list, a warranted error support/norm budget
and a fixed finite Gamma before the unknown error maps are chosen.

An extra small depolarizing ballast per error-catalogue block admits all
bounded local Markov-generator errors as exact CPTP events by the frozen
c_autonomous_restoring_history/PROOF.md. No unknown H or Lindblad jump
coefficient needs to be learned or supplied to the controller. The
resulting event rate costs and local dimension factors remain paid; they
can be very conservative. Unknown perturbations of the nominal read/
correction apparatus itself can be included at that generator-norm
level, provided the full support/error promise is warranted.

The full controller is bounded-local and constant-rate per site at fixed
D,w,q. Its ideal primitive maps can be written from finite Pauli-check
tables without a spectral oracle. At the admitted rational temperature
beta=4log(B0), the integer energy differences make gamma(omega) rational.
This does not make a native apparatus free: implementing the multi-qubit
check-projector jumps/dephasing and warranting the Markovian local-error
budget are separate physical obligations. This work does not duplicate
the other worker's microscopic reservoir-realization problem.

The earlier accepted syndrome-only nominal initializer remains an ideal
polynomial/expected-polynomial computation contract at its stated
accuracy and runtime scope. No noisy-preparation threshold is inherited
merely by writing (2). The decoder remains an ideal final Pauli decoder;
its actual implementation and its noise are still charged separately.

### What is actually improved

Finite Gamma supplies an exact, all-orders destruction of local syndrome
coherence histories, with the paid multipoint waiting bound in PROOF(8).
It does not replace the unknown errors by an exact population Markov
chain. On correctable coherence components, only an offline classical
Pauli history is obtained. Consequently the remaining dynamical gate
for THIS controller is a classical, support-wise uniform persistence
bound under rare arbitrary Pauli events. That is a more specific problem
than the original coupled coherent/clock-history question, but is not
already proved by the stationary thermal analysis.
