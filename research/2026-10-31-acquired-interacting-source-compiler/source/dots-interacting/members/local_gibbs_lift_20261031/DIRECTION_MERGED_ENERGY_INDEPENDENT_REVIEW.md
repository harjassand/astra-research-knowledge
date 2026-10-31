# Independent local review: direction-merged energy certificate

31 October 2026. Verdict: PASS for the specified continuous generator and its acquired local/one-dimensional preparation interfaces. This is not a whole fast-source compiler receipt.

## Exact source binding

Full source read: `DIRECTION_MERGED_LOCAL_ENERGY_CERTIFICATE.md`, 10,942 bytes, SHA-256 `8292664fbc215b131e006c9e931d41a658050b4fbfdf0bd375b378c64a87af2b`. No source edits requested. This receipt is separate from the threshold-environment construction.

## 1. Generator and law

With output basis (0,1), v=(sqrt(r0),-sqrt(r1)) and r0+r1=1, the two jumps |1><v| and -|0><v| each have norm one and total L†L=2Pi. The local conditional Gibbs vector is u=(sqrt(r1),sqrt(r0)), orthogonal to v. Both jumps kill the global positive Gibbs amplitude. For a diagonal observable diag(d0,d1), recycling is (d0+d1)Pi, and subtracting {Pi,D} cancels its offdiagonals; the diagonal terms are r0(d1-d0),r1(d0-d1). This is exactly the original flip generator, including its normalization. The same calculation holds for system-valued diagonal blocks and arbitrary tensor references. Receiving prescribed classical controls still requires their adjoints to preserve that observable algebra with the intended restriction.

H=sum_i Pi_i equals the negative reversible similarity of the classical column generator, with flip entries -sqrt(r_i(x)r_i(x^i)). The connected positive-rate hypercube gives a unique ground vector psi. H<=nI and H>=g_cl Q are valid. As the source explicitly notes, the parent gap alone is not a quantum return proof.

## 2. Cross-drift proof

For its own projector, the two recycling terms sum to Pi_i because the two central-bit diagonal entries of Pi_i sum to one. The anticommutator contributes -2Pi_i, so D_i†Pi_i=-Pi_i. Nonadjacent centers commute even if their diagonal control neighborhoods overlap at other spins.

For adjacent i,j, all remaining spins can be frozen because the cross drift only flips these two centers. Removing their connecting edge changes each local conditional field by at most |J_ij|. The normalized two-component vector has derivative norm (1/2)sech(t). The norm derivative of its rank-one projector equals the perpendicular vector-derivative norm; hence both jump and projector perturbations are at most |J|/2, uniformly in the external fields.

The recycling perturbation bound 4delta_i+2delta_j and anticommutator bound 2delta_i+2delta_j follow by telescoping products of contractions. Therefore ||D_i†Pi_j||<=5|J|. The reference cross drift is zero.

The actual conditional two-spin Gibbs vector spans ker(Pi_i+Pi_j): positive amplitude ratios along the connected square determine every component consistently. The Hermitian cross drift annihilates that vector, since both projectors and each i-jump annihilate it. The edge-deleted reference sum has spectrum 0,1,1,2; its norm perturbation is at most |J|. Min-max therefore puts the actual positive spectrum above 1-|J|. Combining norm, kernel annihilation and this gap proves

D_i†Pi_j <= [5|J|/(1-|J|)](Pi_i+Pi_j).

This uses an operator inequality, not an entrywise or dimension-dependent estimate. It remains valid in every frozen block and with a reference system.

## 3. Return and constants

Each undirected edge contributes both ordered cross terms. Its coefficient on either endpoint is 10|J|/(1-|J|). Thus the stated kappa condition gives G†H<=-kappa H. Positivity of the adjoint semigroup propagates this inequality to E_t†H<=exp(-kappa t)H.

Using Q<=H/g_cl, H<=nI gives E_t†Q <=(n/g_cl)exp(-kappa t)I. Pure stationarity makes this positive operator annihilate psi, strengthening the identity bound to the same scalar times Q. Unitality also bounds it by Q. This proves the claimed complete source-return effect, not merely trace convergence on selected inputs.

The classical influence bound tanh|J| and the column-sum Hamming coupling give Lipschitz contraction exp(-g0t). Applying that contraction to a nonconstant reversible eigenfunction yields g_cl>=g0; finite state space ensures its Lipschitz seminorm is finite and nonzero. With maximum degree two and |J|<=1/40, 1-20/39=19/39 and g0>=1-2/40=19/20. The stated time (39/19)log(320n/19) makes (n/g0)exp(-kappa t)<=1/16. These are conservative valid constants, independent of the local fields and pi_min.

## 4. Acquired operations and scope

Bounded-degree local logistic arithmetic and controlled bit rotations give the displayed jump operators to requested finite precision. The safe stacked normalization sqrt(2n) follows directly from summing 2Pi_i. No partition function is needed for these local operators.

For one-dimensional finite-range Gibbs data, sequential positive transfer messages and conditional square-root rotations acquire psi. Log-domain normalization avoids representing an exponentially large partition function. Bounded-size log-sum-exp is stable under absolute input error, accumulated logit error is polynomial in n, and the conservative square-root-probability error bound permits polynomially small per-step tolerances with polynomial logarithmic precision cost. Periodic boundary conditioning and fixed-width boundary registers are legitimate; a growing range is not free. This is a mathematical finite-resource construction, not executed preparation software.

The source correctly keeps the actual sqrt(lambda) system-mean contribution paid, and offers mean block compression rather than an unearned exact numerical expectation oracle. It also correctly refuses to replace this native G by a finite-time collision kernel or to import its certificate into the different threshold lift without a new matching proof.

## 5. Overall qualification

The local energy argument earns a useful pi_min-free return certificate for this exact geometric/direction-merged realization. It does not establish originality, optimal constants, a full controlled high-rate compiler, or a generic higher-dimensional Gibbs preparation method. Established pure-state engineering, classical path coupling, and quantized-coupling methods remain the relevant comparators. This review does not audit the author's separate newer rapid-mixing literature note.
