# Exact barriers at the intermediate-state concentration gate

9 October 2026. Two rigorous obstruction mechanisms for proposed shortcuts. Neither is a counterexample to finite exact EB length for arbitrary PPT words. They explain what the remaining proof must control after exponential approximation and the faithful-trajectory theorem.

## 1. An absorbing flag can make any word concentrate arbitrarily rapidly

Let Phi_1,...,Phi_n be arbitrary PPT CPTP maps on M_r, and fix 0<epsilon<1. Enlarge the system to C^r direct-sum C|f>. On block inputs define

 Phi_hat_i([[X,z],[z*,t]])
   = [[epsilon Phi_i(X),0],
      [0,(1-epsilon)tr(X)+t]].                          (1)

This is CPTP. It is the sum of the embedded PPT signal map epsilon Phi_i, the EB map that measures the signal block and prepares the flag with weight 1-epsilon, and the EB map preserving the flag population. Hence it is PPT. All signal/flag input coherences are discarded.

Put T=Phi_n ... Phi_1. Direct multiplication gives

 T_hat([[X,z],[z*,t]])
   = [[epsilon^n T(X),0],
      [0,(1-epsilon^n)tr(X)+t]].                        (2)

Consequently

 T_hat is EB  <=>  T is EB.                             (3)

The reverse direction follows because (2) is a sum of EB maps whenever T is EB. The forward direction follows by CP compression to the signal input and output blocks, which recovers epsilon^n T. The EB cone is invariant under CP compression and positive rescaling.

For every initial density matrix, the signal probability after i steps is at most epsilon^i. Thus the evolving state is within trace distance at most 2epsilon^i of the pure flag state. Starting from the maximally mixed density matrix, even its smallest eigenvalue is bounded above by epsilon^i/r. If the original signal maps have full global output support, the intermediate states can remain faithful for every finite i while their smallest eigenvalues decrease this rapidly.

At channel level, let R_f be the pure-replacer channel. Equation (2) gives

 ||T_hat-R_f||_diamond <= 2epsilon^n.                    (4)

Thus arbitrarily strong absolute exponential approach to EB and arbitrarily rapid trajectory concentration coexist with precisely the original word's exact EB status. Postselecting the signal flag restores the original normalized word T.

The construction does not provide nonEB words of arbitrary length unless they already exist for the original dimension. Its point is the exact preservation (3), not a solution of the unrestricted conjecture.

### Consequence for a proof

Concentration alone cannot supply an absolute separable margin that overwhelms every possible surviving quantum component. In this example the surviving component has weight epsilon^n and carries all remaining entanglement. A successful exact argument must positively isolate or control that conditional branch. Here the flag does isolate a smaller-dimensional branch, so lower-dimensional induction is applicable; an unflagged near-singular state does not automatically furnish the same positive decomposition.

For any fixed nonEB example, sufficiently small depolarizing perturbations make all enlarged factors Choi-positive and keep their finite product nonEB by continuity. The concentration can remain arbitrarily strong. This observation concerns a fixed word length and does not assert an unbounded family of nonEB lengths.

## 2. A map-level exact rank drop from near-singularity would imply the Schmidt-number conjecture

Consider the following proposed shortcut, for fixed d>=2:

There is eta>0 such that every PPT CPTP map Phi satisfying

 lambda_min Phi(I/d)<eta

is (d-1)-superpositive.

This shortcut is equivalent to the full inclusion PPT_d subset SP_(d-1), rather than a weaker concentration fact.

The inclusion trivially implies the shortcut. Conversely, let Psi be any strictly output-positive PPT CPTP map. Fix P=|a><a| and define

 A_t=P+t(I-P),
 Y_t=Psi*(A_t^2),
 Theta_t=Ad_(A_t) Psi Ad_(Y_t^(-1/2)).

As proved in EXACT_UNRESTRICTED_GATE_REDUCTIONS.md, Theta_t is CPTP and PPT, its two filters are invertible for t>0, and

 Theta_t -> [X -> tr(X)P].

Hence lambda_min Theta_t(I/d) tends to zero. The proposed shortcut makes Theta_t (d-1)-superpositive for sufficiently small t. Invertible local filtering preserves the Schmidt number of its Choi matrix in both directions, so Psi must also be (d-1)-superpositive.

Every non-strictly-output-positive PPT map is already (d-1)-superpositive by the rectangular support split. Finally arbitrary non-TP maps can be regularized and input-normalized into PPT CPTP maps; invertible filters and closure of SP_(d-1) transfer the conclusion back. Thus the shortcut gives PPT_d subset SP_(d-1) in full scope.

This inclusion is explicitly Conjecture II.1 of Christandl–Mueller-Hermes–Wolf, arXiv:1807.01266v2. The present programme does not assume or establish it.

## Remaining legitimate target

The exponential approximation theorem does not resolve the rare conditional branch in (1)–(4). The faithful-trajectory theorem resolves words with a common lower eigenvalue bound, conditionally on the exact lower-dimensional word theorem. The remaining target must combine multiple PPT factors with a positive decomposition or an error estimate that survives conditioning on the relevant low-weight output sector.

Neither ordinary small trace/Frobenius error, nor mere closeness of a one-step output to a rank-deficient state, supplies that missing estimate. The two equivalences above prohibit treating those shortcuts as already-established lemmas.
