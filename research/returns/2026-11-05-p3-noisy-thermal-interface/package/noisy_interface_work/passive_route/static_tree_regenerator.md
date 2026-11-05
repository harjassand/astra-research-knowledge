# A static noisy-majority tree erases correlated classical interface history

This construction replaces the proposed randomly permuted majority pools. It uses a fixed circuit, so it needs no mutable random routing, private permutation memory, or annealed-versus-quenched reuse assumption. It is deliberately conservative in space: polynomial overhead is sufficient for the quantum-interface bridge.

## 1. Primitive model and input contract

There is a classical bit b, possibly correlated with an arbitrary quantum reference R. There are M physical classical copies x_j=b XOR E_j. Their error pattern E can be correlated with b, R and prior interface syndromes. It obeys the local-stochastic support bound

\[
\Pr[S\subseteq E]\le q^{|S|}
\qquad\text{for every leaf set }S.
\tag{1}
\]

It is enough that this bound hold uniformly in the incoming quantum state; it need not hold after conditioning on a rare retained record. If the pool-generation circuit has an additional global trace/diamond error epsilon_pool, that error is charged separately.

Arrange the M=3^L copies as leaves of a balanced ternary tree. Every edge independently flips its transmitted bit with probability e, including its fixed-duration copy/wire/idle exposure. Each internal vertex computes the majority of its three received bits and independently flips the result with probability v. All these fresh faults are independent of the old pool/reference and of faults at other vertices/edges. The tree has fixed wiring, fan-in three, fan-out one, O(M) gates and links, and depth L. No raw bit waits for an unbounded classical computation between levels.

The classical majority gate is a specified bounded-arity noisy component. If it is implemented by a finite lower-level circuit, its actual truth-table noise must satisfy this model, or the generalization in Section 6 must be used. A generic faulty subcircuit cannot simply be assigned an input-independent output-flip probability without proof.

## 2. Explicit independent reference law

If child errors are independent Bernoulli(u), their post-wire error probability is

\[
z(u)=e+(1-2e)u.
\]

The parent error probability is

\[
F(u)=v+(1-2v)[3z(u)^2-2z(u)^3].
\tag{2}
\]

In the reference process, set every leaf to the exact classical bit b and use the same fresh edge/voter faults as the actual process. Disjoint subtrees make the reference errors independent at every level. Its root is exactly b XOR Z, where Z is independent of b,R and old histories and

\[
\Pr[Z=1]=r_L,\qquad r_0=0,\quad r_{\ell+1}=F(r_\ell).
\tag{2a}
\]

The entire reference law is explicitly computable from the finite local truth tables. Its dependence on L is allowed: an interface law can depend on its chosen size and schedule while its noise strength remains uniformly bounded. For known inhomogeneous nodes, evaluate the corresponding three-child probability recursion up the tree; independence of disjoint reference subtrees still holds.

The ideal reference leaves are a proof coupling, not physical ancillas that the actual operation has to prepare. No ideal encoder or output port is inserted into the actual circuit.

## 3. Coupling theorem

Suppose there is u_bar such that

\[
q\le\bar u,
\qquad v+3(\bar u+e)^2\le\bar u,
\qquad\alpha:=6(\bar u+e)<1.
\tag{3}
\]

Then the actual root bit, jointly with b,R and every pre-existing retained record, is within trace distance

\[
\delta_L\le q\alpha^L
\tag{4}
\]

of the fresh BSC(r_L) output in (2a). This uses trace-distance convention one half of the trace norm. An additional pool-generation error is added once.

More generally, put p_0=max(q,e,v)<=1/100 and take u_bar=2p_0. Then alpha<=18p_0 and v+3(u_bar+e)^2<=p_0+27p_0^2<=2p_0. In particular r_L<=2p_0=O(p_0) at every depth. At p_0<=1/100 this gives

\[
\delta_L\le0.01(0.18)^L.
\]

To reach accuracy delta, choose L=O(log(1/delta)) and M=3^L=poly(1/delta). The component error probabilities stay fixed.

### Proof

At each node let D indicate disagreement between the actual and reference processes, and let U indicate that at least one of them has an error relative to b. We prove the mixed local-stochastic bound

\[
\Pr\!\left[\bigcap_{i\in A}\{D_i=1\}\cap
\bigcap_{j\in B}\{U_j=1\}\right]
\le d_\ell^{|A|}u_\ell^{|B|}
\tag{5}
\]

for every disjoint pair A,B of nodes at level ell.

At the leaves, D=U=E because the reference leaf has no error. Equation (1) therefore gives (5) with d_0=u_0=q, even if the old errors correlate arbitrarily with external records.

A shared edge flip does not change disagreement. It changes union error only if a previous union error or the fresh edge flip occurs. Thus its mixed parameters are d_ell and u_ell+e.

At a majority vertex, a union error before the voter flip requires at least two union-error children. Hence

\[
u_{\ell+1}\le v+3(u_\ell+e)^2.
\tag{6}
\]

If the two majorities disagree, at least one child disagrees and a distinct child must be erroneous in at least one process. Otherwise both majorities equal b. There are six ordered choices of those children. The shared voter output flip cannot change disagreement. Therefore

\[
d_{\ell+1}\le6d_\ell(u_\ell+e).
\tag{7}
\]

The mixed bound (5), not merely its one-node version, propagates: for each requested disagreement parent expand into its six ordered child witnesses; for each requested union-error parent expand into its voter-fault event or its three unordered two-child witnesses. Different parents have disjoint child/fault sets. Apply (5) to the selected children, multiply the probabilities of fresh independent faults, and sum the witness choices. The resulting factors are exactly (6) and (7).

Condition (3) keeps u_ell<=u_bar and gives d_ell<=q alpha^ell. The root disagreement probability bounds trace distance under this coupling, including a quantum reference because the operation is classical on the error labels and leaves the conditional reference state untouched. More explicitly, attach each old classical error label to its original conditional quantum-reference state, use the same fresh faults in both processes, and bound the trace norm difference by twice the total mass of labels on which the two root bits disagree. The reference root has the stated independent BSC law. This proves (4).

An optional stationary version chooses iid Bernoulli(u_star) reference leaves with u_star=F(u_star). It gives a size-independent reference BSC law and error at most (q+u_star)alpha^L, under the stronger initial condition q+u_star<=u_bar. It is unnecessary for the physical interface: using (2a) is simpler and has a better bound.

## 4. Many bits and quantum byproducts

Use disjoint trees for all Bell-result or frame bits. The initial pools may be correlated across trees. Couple each tree to its own ideal logical-bit leaves and independent fresh faults. A union bound gives total error at most sum_j delta_j. The reference root errors are independent across trees and independent of all old gauges/records.

Consequently a logical Bell result can control a final **raw local** Pauli correction without allowing old syndrome correlations into the fresh Bell half. Keep that half untouched by the old coherent controller throughout its encoded waiting and independent descent. Only the regenerated raw classical bit acts at the terminal bounded-size physical port. The residual control-bit BSC noise is part of the local endpoint Pauli channel; all earlier controller/pool faults are either included in the LS pool model or charged as epsilon_pool.

The input pool must genuinely satisfy (1). Replicating one already faulty raw Bell bit does not work: a single common error then flips every leaf with constant probability, violating (1). The required operation is protected logical fan-out followed by independent noisy output interfaces, whose shared auxiliary systems are allowed but whose fault support has a local-stochastic bound. This precursor must be derived from an actual noisy-controller fault-tolerance construction.

## 5. Deployment and reuse

The tree can be an ordinary fixed hardwired classical circuit. It reuses safely because the proof is uniform over any new LS pool and all prior records, provided the new wire/voter faults satisfy the stipulated fresh-noise contract. There is no dependence on fresh routing randomness.

In the currently declared active architecture, nonlocal links have specified clock duration, cost and independent noise, so each layer has fixed time. Count all M leaf-output interfaces, O(M) voter/link uses, L time steps, protected waiting of the fresh quantum Bell half, reset and controller memory. This does not prove that arbitrary-distance links have constant latency in a bounded-density three-dimensional implementation. A local deployment must include its actual routing, protection and timing.

## 6. Extension to arbitrary faulty classical voter functions

If an internal gate equals exact majority with probability 1-v and otherwise applies a known random Boolean function (or a known classical stochastic truth-table channel), the same coupling gives

\[
u_{\ell+1}\le v+3(u_\ell+e)^2,
\qquad
d_{\ell+1}\le[3v+6(u_\ell+e)]d_\ell.
\]

At a faulty gate, disagreement requires at least one disagreeing child, giving the extra 3v term. The reference error recursion is computed from the actual truth-table channel. If that channel is complement covariant, it has the same error law for b=0 and b=1 and the same BSC conclusion follows. Without complement covariance one obtains an explicitly known asymmetric binary channel independent of old histories. That weaker conclusion may suffice for some uses, but it must not be substituted silently for the independent symmetric Pauli correction required by a twirling argument.

Put p_0=max(q,e,v)<=1/100 and take u_bar=2p_0. The reference error remains in [0,2p_0], and the mixed coupling contraction is at most

\[
\alpha=3v+6(\bar u+e)\le21p_0\le0.21,
\qquad\delta_L\le0.01(0.21)^L.
\]

For the optional stationary version, the reference recursion has derivative magnitude at most 6z(u)+3v<=0.21 on [0,1/50], because the expectation of a bounded Boolean truth table on three iid Bernoulli bits has derivative magnitude at most three. Hence it has a unique small fixed point. The main compiler does not need that fact.

### An explicit complement-covariant physical voter

If CNOT and Toffoli are the specified bounded-arity classical operations, apply CNOT a→b, CNOT a→c, then Toffoli with controls b,c and target a. Retain a and discard b,c. The retained bit is

\[
a\oplus(a\oplus b)(a\oplus c)=ab\oplus ac\oplus bc=\operatorname{maj}(a,b,c).
\]

For every pattern of intervening bit flips, complementing all three initial bits complements only the final retained target: after the CNOTs, the two Toffoli controls are unchanged by that global complement. Thus each fault-conditioned Boolean map is complement covariant. Pauli faults on computational-basis bits reduce to bit flips for this purpose. The macro fault probability v is at most the sum of its finite elementary gate and idle fault probabilities. This construction pays all three gates and the discarded-wire reset. If a Toffoli is decomposed into a longer quantum circuit, the same covariance must be checked for that actual decomposition rather than presumed.

Alternatively, symmetrize any fixed finite implementation of a majority voter with a local complement twirl. Draw a fresh uniform raw bit r; XOR it into all three input bits; execute the voter; XOR the same r into the output. The seed exists only for this constant-depth gadget. Its copies, idles, mask gates, final readout and reset remain noisy and are included in v. Under state-independent gate Pauli/bit-flip noise, every used seed copy has form r XOR a fault bit. Replacing the input by its complement and changing the summation variable r→r XOR 1 leaves the central voter's input unchanged and complements the final output. Hence the averaged macro channel is exactly complement covariant. A Pauli-noisy |+> preparation and computational-basis measurement supplies the uniform seed without an ideal random source. This is a bounded-size local use of randomness; it does not revive the global mutable-permutation problem.

The static-tree proof is new work in this research exchange. It uses elementary coupling and fault-support bounds; its complete operation depends on the explicitly identified protected-pool precursor, not on an ideal encoder or perfect classical output bit.
