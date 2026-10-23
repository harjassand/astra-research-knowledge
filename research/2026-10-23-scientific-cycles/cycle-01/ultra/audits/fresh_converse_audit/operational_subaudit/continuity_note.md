# Finite-output entanglement-of-formation continuity

All logarithms and entropies in this note are natural. This is an independent support argument for the original entanglement-of-formation witness route. Every entropy-continuity step below takes place on finite-dimensional systems.

## Statement

Let rho and sigma be states on A tensor B, with dim A = dim B = d < infinity, and let

    (1/2) ||rho - sigma||_1 <= epsilon,       0 <= epsilon <= 1.

Set

    delta = sqrt(epsilon (2 - epsilon)),
    h(p) = -p log p - (1-p) log(1-p),
    g(delta) = (1+delta) h(delta/(1+delta))
             = (1+delta) log(1+delta) - delta log delta,

with the continuous endpoint convention 0 log 0 = 0. Then

    E_F(rho) <= E_F(sigma) + delta log d + g(delta).

The same argument in the opposite direction gives an absolute-value bound. No additivity of E_F is assumed or used.

For d = D^(N t), fixed finite N and D, and epsilon_t -> 0 as t -> infinity,

    E_F(rho_t) <= E_F(sigma_t) + o(t),

since the correction divided by t is

    N log D sqrt(epsilon_t(2-epsilon_t)) + g(delta_t)/t -> 0.

In particular, no quantitative convergence rate for epsilon_t is needed. Here t ranges over the protocol lengths for which the indicated finite dimensions are defined.

## Finite pure ensembles suffice

Put n = d^2. The pure states on A tensor B form a compact set, and pi -> S(Tr_B pi) is continuous and bounded on it. The graph

    { (pi, S(Tr_B pi)) : pi pure }

is therefore compact in a real affine space of dimension at most n^2: n^2-1 state coordinates and one cost coordinate. Its convex hull is compact. Any probability-measure ensemble, including a countable ensemble, has its state/cost barycenter in that convex hull. Caratheodory therefore replaces it by at most n^2+1 = d^4+1 pure states with exactly the same state and exactly the same average entropy.

Consequently the convex-roof minimum is attained by a finite ensemble. Alternatively one may use finite eta-optimal ensembles and take eta down to zero; this avoids needing attainment. The slightly loose d^4+1 cardinality is intentional and sufficient.

## Uhlmann and one fixed rank-one measurement

Choose a finite minimizing ensemble

    sigma = sum_j q_j |phi_j><phi_j|,
    E_F(sigma) = sum_j q_j S(Tr_B |phi_j><phi_j|).

Let C have dimension L >= max(number of ensemble terms, n), padding the ensemble with zero-weight terms, and define

    |Sigma>_ABC = sum_j sqrt(q_j) |phi_j>_AB |j>_C.

Using the root fidelity F(rho,sigma) = ||sqrt(rho) sqrt(sigma)||_1, finite-dimensional Uhlmann gives a purification |Rho> on the same ABC with

    |<Rho|Sigma>| = F(rho,sigma).

The ancilla padding ensures that both states admit purifications there. The half-trace distance of the pure purifications is

    sqrt(1-F(rho,sigma)^2) <= sqrt(epsilon(2-epsilon)) = delta,

because F(rho,sigma) >= 1-(1/2)||rho-sigma||_1 >= 1-epsilon.

Measure C in the displayed orthonormal basis and then trace out B. Denote the resulting finite-dimensional cq states on A X by tau and omega for |Rho> and |Sigma>, respectively. The basis measurement is rank one, so its nonzero conditional AB states are pure. Thus

    E_F(rho) <= H(A|X)_tau,
    E_F(sigma) = H(A|X)_omega,
    a := (1/2)||tau-omega||_1 <= delta.

The final inequality is trace-distance contraction. No claim about continuity on an infinite-dimensional ancilla is needed.

## A finite cq conditional-entropy bound

For every cq state zeta on A X,

    0 <= H(A|X)_zeta <= log d.

For cq states u,v and 0 <= p <= 1, write f(zeta)=H(A|X)_zeta. Adding a binary classical mixing label J proves

    (1-p)f(u)+p f(v)
        <= f((1-p)u+p v)
        <= (1-p)f(u)+p f(v)+h(p).

Indeed the difference from the weighted average is I(A:J|X), between zero and H(J|X) <= h(p). Equivalently, this follows by applying the usual entropy-of-mixture bounds in each classical block.

If a>0, write the Jordan decomposition

    tau - omega = a(P-Q),

where P and Q are normalized positive states. These states are cq in the same X basis: tau-omega is block diagonal in X, and taking its positive and negative spectral parts acts separately within each block. Define

    zeta = (tau+a Q)/(1+a) = (omega+a P)/(1+a),
    p = a/(1+a).

Use the lower mixing bound for the first representation and the upper mixing bound for the second. Multiplication by 1+a yields

    f(tau)-f(omega)
        <= a(f(P)-f(Q)) + (1+a)h(a/(1+a))
        <= a log d + g(a).

The case a=0 is immediate. The function a log d+g(a) is increasing for a>=0 (for a>0, g'(a)=log((1+a)/a)>0). Hence it is bounded by delta log d+g(delta). Combining with the purification construction proves the statement.

## Schmidt-number support bound with local infinite ancillas

The following is a separate structural fact. Starting with Phi_M and ancillary states prepared locally, an LOCC output on finite-dimensional A_out tensor B_out has Schmidt number at most M. In particular,

    E_F(output) <= log min(M,d)

when both output dimensions are d.

Local ancillas must not supply additional shared entanglement. They may be mixed, infinite dimensional, and correlated with systems on their own side; they can be purified locally for the argument. In a refinement into pure local operations, a branch has the form

    (K_A tensor K_B) |Phi_M>
      = (1/sqrt(M)) sum_{i=1}^M K_A|i> tensor K_B|i>,

so every nonzero branch vector has Schmidt rank at most M. Appending arbitrary local isometries preserves this bound across the full A-side/B-side cut.

Discarding arbitrary local environments does not change the conclusion. To see this directly, write the global pure branch as

    |Psi> = sum_{i=1}^M c_i |alpha_i>_(A_out E_A)
                              tensor |beta_i>_(B_out E_B).

Expanding E_A and E_B in orthonormal bases gives an output decomposition into vectors

    |v_ab> = sum_{i=1}^M c_i
        (I tensor <e_a|)|alpha_i> tensor (I tensor <f_b|)|beta_i>,

each of Schmidt rank at most M. This is a mathematical decomposition; the protocol need not actually measure or reveal its discarded environments. For finite outputs, only finite-dimensional environmental support is needed for each such finite-Schmidt-rank vector: the A-side span of all environment coefficients has dimension at most M dim A_out, and similarly on the B side. Thus arbitrary discarded local Hilbert spaces do not create a continuity or decomposition obstruction.

The normalized pure states of Schmidt rank at most M form a compact set in finite output dimensions. Its convex hull is compact and closed. Countable sums and probability-measure mixtures of branch outputs therefore remain in it, and Caratheodory reduces the final finite-dimensional state to a finite pure-state decomposition of rank at most M. Every term has entropy at most log min(M,d), proving the E_F bound without additivity.

This applies to finite-round LOCC with discrete normal instruments, measurable classical outcomes under the usual measurable-instrument formulation, and infinite-round protocols when their finite-dimensional output is an operational trace-norm limit of such local protocols (including almost-sure termination with vanishing uncompleted probability). For continuous outcomes, one should specify the usual outcome-space and posterior-state measurability assumptions; one should not infer an unrestricted pointwise bounded Kraus density for every infinite-dimensional instrument merely from normality. The final finite-dimensional barycenter and closedness argument itself needs no such density.

Closedness of the finite-output Schmidt-number set supplies the infinite-round limit step. On fixed finite output ports, convergence of all observable expectations already implies trace-norm convergence. The word "normal" by itself is not a substitute for specifying an LOCC construction or operational limiting notion; an arbitrary normal global quantum channel can create entanglement. A putative infinite-round definition that supplies no trace-norm approximating local outputs requires a separate argument. Conditioning on a probability-zero infinite transcript is also not a normalized operation without additional structure. No such extra definition is needed for the continuity theorem above.
