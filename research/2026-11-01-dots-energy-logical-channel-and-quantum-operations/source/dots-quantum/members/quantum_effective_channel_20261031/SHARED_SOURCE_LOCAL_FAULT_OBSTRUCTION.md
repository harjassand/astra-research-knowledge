# One decaying source can still produce arbitrarily high-weight logical faults

Status: root exact counterexample, awaiting independent check. This limits a proposed multi-site extension, not the received global logical-channel theorems.

Take one source qubit with dark state |0>, jump L=sqrt(2)|0><1|, H=|1><1|, and physical generator lambda D[L]. Thus g=h=1, G^dagger H=-2H, kappa=2. Start the source in |1>. Couple n system qubits by

    sqrt(lambda) K_xi,
    K_xi=H tensor sum_(i=1)^n xi_i Z_i,

where each xi_i is an independent private fair sign held for the whole interval. There is no system Hamiltonian. Each local coupling term has norm1 and commutes with H, so it injects no source energy. The source makes at most ONE physical jump. Its first-jump time is Exp(2lambda), independent of the system. The pure-dark effective logical generator is zero since K_xi(|0> tensor I)=0.

Choose positive time T=pi/(2sqrt(lambda)). On the event of no source jump by T, with probability

    q=exp(-2lambda T)=exp(-pi sqrt(lambda)),

every system qubit undergoes exp(-i xi_i pi Z_i/2), which is Z_i up to a global phase. The product channel on this event is exactly conjugation by Z_1...Z_n, regardless of the private signs.

For earlier jump times t, averaging the independent signs turns each local rotation into a dephasing channel with Z-error probability sin^2(sqrt(lambda)t); conditioned on that t, the joint channel is their product. Thus the full averaged channel is a Pauli channel whose all-n-Z error probability is at least q. This statement refers to a genuine Pauli error distribution, not merely a large trace-distance bound or a chosen decomposition with negative weights.

A local-stochastic fault guarantee with size-independent parameter p<1 would require the probability of errors on all n specified sites to be <=p^n. For any fixed lambda, q>0, so choosing n>log(q)/log(p) contradicts that guarantee. Each individual source energy estimate and the expected jump count remain excellent. The shared dwell-time event causes the high-weight tail.

Consequences:

* Small expected energy or jump count alone does not supply a size-independent local fault theorem.
* Independent private signs on local couplings do not remove this common rare-event mechanism.
* The counterexample has unbounded source-to-system fanout. It does NOT rule out bounded-degree geometrically local sources with earned cluster/mixing bounds, independently refreshed local sources, or a different actual control schedule.
* The global coupling norm is n, so none of the received theorems with their fully charged global b bounds are contradicted. Likewise a cold-input theorem does not apply: the actual source energy here is E0=1.
* This is not an asymptotic lower bound against all correction methods. It identifies precisely which extra spatial/probabilistic structure must be earned before promoting reset-free logical-channel accuracy to fault-tolerant many-qubit computation.
