# Coherent loading audit and a weaker post-loading admission theorem

2026-11-01. Decision: **PASS of the exact coherent overwrite and additive error accounting. Positive restricted admission theorem below; constant-density faulty local loading remains OPEN.** This is a proof audit, not a fault-tolerant loading construction.

## 1. Coherent decoded Pauli and SWAP

For a fixed Pauli decoder R_s, the decoded Pauli is Q_mu=L_mu sum_s f_mu(s)P_s, with f_mu the appropriate commutation sign. Bare logical Paulis commute with all syndrome projectors. Coherent syndrome extraction, reversible sign computation, externally controlled sign phase and externally controlled bare logical therefore implement controlled Q_mu exactly. Because neither the phase nor bare logical changes the syndrome, uncomputation restores EVERY workspace qubit, including on coherent superpositions and on states entangled with the bath. Nothing measures or dephases the syndrome.

Controlled Q_X gives CNOT from input to decoded logical. Controlled Q_Z is symmetric controlled-Z between those qubits; conjugation by Hadamard on the supplied physical qubit gives CNOT from decoded logical to input. The usual three-CNOT circuit therefore swaps the input and decoded logical subsystem and acts as identity on the gauge and bath.

For an initially independent input-reference state xi_IR and an arbitrary equilibrium rho_LGB (including all L-G-B coherences), tracing out the old logical output after SWAP gives exactly xi_LR tensor Tr_L rho_LGB. This is true without equilibrium being logically factorized and without access to B. The independence of the incoming input-reference from the old memory-bath system must be explicit.

These are finite circuit identities. They do not bound reversible decoder complexity, geometric routing, coherent depth, storage exposure during gates, reset resources or error propagation through the circuit.

## 2. Additive initial error

If the actual loaded joint MBR state differs from the target by delta in trace norm, subsequent common storage and decoding contract this difference. Delta is added ONCE to the ideal terminal bound, not multiplied by the storage time. This holds reference-safely. An approximation to the initial full memory-bath background contributes its joint trace distance only once as well. Local-observable agreement is not an adequate substitute absent a further argument.

## 3. Elementary second-moment admission: no stationarity of the loaded state

Use the notation of the exact thermal theorem. Let rho be its actual finite-volume Gibbs state, sigma=rho_bar its logical Pauli twirl, P the bad projector, p=Tr(P rho), delta=||sigma-rho||_1, and U_t=exp(-itH). Set

    a = p + delta/2.

Stationarity of rho, unitary invariance of trace distance and the equal-trace effect bound imply

    Tr(P U_t sigma U_t†) <= a                       (all t).

Let omega_MBR be ANY loaded state, possibly correlated between logical, gauge, bath and reference. Its incoming target is xi_LR. Assume only:

    ||Dec(omega_MBR)-xi_LR||_1 <= e0,
    K(omega_MB | sigma) := Tr[omega_MB sigma^(-1) omega_MB] <= K0.

The second hypothesis is on the SYSTEM marginal only. At finite beta and finite bath volume sigma is full rank. The same K is conserved when omega and sigma are jointly conjugated by U_t. Hilbert–Schmidt Cauchy–Schwarz gives, for any positive state w and positive definite s,

    Tr(P w) = Tr[(P s^(1/2))(s^(-1/2) w)]
             <= sqrt(Tr(P s)) sqrt(Tr[w s^(-1) w]).

Consequently

    Tr(P omega_MB(t)) <= sqrt(a K0)                (all t).

The exact thermal theorem's two-sided support of i[H,Q_mu] and bound ||i[H,Q_mu]||<=2vn apply to every state, not only thermal states. Reference trace-norm duality and the Pauli expansion therefore give

    ||Dec(omega_MBR(T))-xi_LR||_1
       <= e0 + 6vn T sqrt(a K0).                 (* )

No product logical/background assumption, post-loading stationarity, reference-dimension bound or bath mixing assumption enters this argument. For a channel guarantee, e0 and K0 must hold uniformly over all input-reference states (K only depends on their output system marginals).

The reference sigma, rather than rho, is useful: the EXACT ideal encoded marginal E(xi_L)=xi_L tensor tau_GB obeys E(xi_L)<=2sigma and hence K(E(xi_L)|sigma)<=2. Indeed w<=C s implies w s^(-1) w<=Cw and K<=C. Thus ideal loading satisfies this new admission automatically; direct divergence to rho need not have an equally simple uniform bound.

If a_n<=poly(n) exp(-c_a n^eta) and log K0<=kappa n^eta with kappa<c_a, (*) permits stretched-exponential times with exponent coefficient below (c_a-kappa)/2. In particular log K0=o(n^eta) suffices. Constants and K0 must be uniform in bath volume for an infinite-bath conclusion; one uses finite-volume inequalities and reduced-memory limits, not an infinite inverse density operator.

This weighted second-moment condition is weaker than max-relative-entropy/operator domination. It is also not global trace closeness: a state can have trace distance bounded away from zero while K remains a fixed constant, for example a fixed bounded local modification of a product thermal state. The inequality is a sufficient admission condition, not a characterization of all usable loaded states.

## 4. Smooth admission and max domination variants

If omega_MBR is within epsilon of a witness state omega'_MBR satisfying the moment admission and initial decoded error e0', then terminal error is at most

    epsilon + e0' + 6vn T sqrt(a K0').

The smoothing is in JOINT reference-safe trace norm and is charged only once. This accommodates a fixed acceptable probability of catastrophic loading failures without forcing its contribution to multiply T.

Alternatively, if omega_MB<=C sigma then direct operator order gives p_bad(t)<=Ca and terminal error <=e0+6vnT Ca. This is stronger than the second-moment result when domination is available. Domination relative to rho yields p_bad(t)<=Cp instead. Neither route requires omega itself to be stationary.

## 5. Why constant-density local faults do not automatically pass

Consider a product thermal reference on N independent bits with excitation probability r in (0,1). Independent local faults change that probability to s != r, with s-r fixed however small. Then the post-noise state is again product and

    K = [s^2/r + (1-s)^2/(1-r)]^N
      = [1+(s-r)^2/(r(1-r))]^N.

Thus log K=Theta(N). Its trace distance from the reference tends to 2, as the two empirical excitation densities concentrate around distinct means. This is a finite-depth constant-density local channel, so locality and short duration alone do not imply small trace distance or the sub-stretched-exponential moment budget. The example can be implemented by independent bit-flip noise whenever r is not 1/2.

Likewise an empirical-density event can be exponentially rare in the reference and typical after such noise. This is a sharp limitation of transferring an ARBITRARY rare-event estimate from locality alone. It is NOT a counterexample for the specific decoder-bad projector, and it is NOT a no-go for a threshold proof exploiting that projector's witness geometry.

Ordinary relative entropy only gives, by binary coarse-graining,

    D(w||rho) >= q log(1/p) - log 2,
    q=Tr(Pw), p=Tr(P rho).

Thus even a constant relative-entropy budget only gives q=O(1/log(1/p)), generally too weak for exponential-time derivative control. Nonzero fixed initial trace error can instead be charged additively via the common-channel argument; these are distinct proof mechanisms and must not be conflated.

## 6. The remaining constructive target

A constant-density faulty coherent loading theorem would need an additional structure-sensitive argument. Options include proving uniform small bad population for the subsequent exact dynamics from a specific local-stochastic loading class, constructing a physically supplied fault process that preserves a suitable thermal reference while maintaining logical correctness, or obtaining smooth sub-stretched-exponential moment/ domination budgets after a correction/recovery stage. None follows from finite circuit existence or input-qubit fault tolerance alone.

The moment theorem supplies a precise weaker, reference-safe and nonstationary admission gate. It does not certify generic extensive local noise through the coherent decoder/SWAP circuit. No external source or contact was used for these direct algebraic derivations.
