# Explicit finite-depth certificate for the encoded countershift

This audit fixes the active-permutation convention: permutations act on configurations, products compose right-to-left, and a bit physically moves to its destination. The radius discussion is for the induced Heisenberg automorphism on the full operator algebra, not only the classical bit dependencies.

## Exact order and cancellation

Let the fine chain be partitioned into \(L\)-site blocks
\(B_k=[kL,(k+1)L-1]\), with the distinguished \(q\) register at local position \(L-1\). Let \(C_\to\) shift only these registers one coarse block to the right, and let \(C_\leftarrow=C_\to^{-1}\). Let \(R\) cyclically rotate each block right by one site. For a source site \((k,j)\), \(C_\to\) does nothing if \(j<L-1\), and \(R\) sends it to \((k,j+1)\); if \(j=L-1\), \(C_\to\) first sends it to \((k+1,L-1)\), and \(R\) then sends it to \((k+1,0)\). Thus
\[
 S_\to=R C_\to,
\]
where \(S_\to\) is the one-site fine right shift. This identity includes the wrap from one block to the next; it is not an approximation.

Write \(P\) for the parallel encoder on the unshifted blocks and
\(P_{+1}=S_\to P S_\to^{-1}\) for the same encoder on the blocks translated one fine site to the right. Starting from
\[
 \Omega=S_\to P^{-1}C_\leftarrow P,
\]
insert \(S_\to^{-1}S_\to\) and use \(S_\to=R C_\to\):
\[
 \begin{aligned}
 \Omega
 &=(S_\to P^{-1}S_\to^{-1})(S_\to C_\leftarrow)P\\
 &=P_{+1}^{-1}R P.
 \end{aligned}
\]
The first equality is the exact group identity
\((S P^{-1}S^{-1})(S C_\leftarrow)P=S P^{-1}C_\leftarrow P\); the second uses \(S C_\leftarrow=R C_\to C_\leftarrow=R\). In Schrödinger state order the three layers act as \(P\), then \(R\), then \(P_{+1}^{-1}\). The shifted blocks supporting \(P_{+1}^{-1}\) are \([kL+1,(k+1)L]\), which tile the chain and are pairwise disjoint. This is an explicit three-layer block circuit, not merely an index-one existence argument.

## Strict forward and inverse radii

Each of \(P\), \(P^{-1}\), \(R\), and \(P_{+1}^{\pm1}\) is block-local on an interval of length \(L\), so each has strict radius at most \(L-1\). Summing three generic layer radii would give the valid but loose \(3(L-1)\). The sharper bound follows from the actual cone.

For forward Heisenberg evolution \(A_i\mapsto \Omega^*A_i\Omega\), the first conjugation is by \(P_{+1}\); it confines the image of a one-site operator at \(i\in[kL+1,(k+1)L]\) to that shifted block. Conjugation by \(R\) can spread it only to the unshifted blocks it intersects, namely \(B_k\cup B_{k+1}=[kL,(k+2)L-1]\). The final blockwise \(P^{-1}\) cannot enlarge this union. Write \(i=kL+s\), \(1\le s\le L\). The distances from \(i\) to the two extreme sites of the union are \(s\le L\) and \(2L-1-s\le2L-2\). Hence
\[
 \operatorname{rad}(\Omega)\le\max\{L,2L-2\}=2L-2\quad(L\ge2).
\]
For the odd encoder length \(L\ge3\), this is the claimed direct strict-radius bound.

The inverse permutation is
\[
 \Omega^{-1}=P^{-1}R^{-1}P_{+1}.
\]
Its Heisenberg cone begins with the unshifted block gate \(P\), remains within that block under \(R^{-1}\), and the last shifted-block gate can enlarge support only to \([kL-L+1,kL+L]\), the union of the two shifted blocks intersecting \(B_k\). For \(i=kL+s\), \(0\le s<L\), the distances to those endpoints are \(s+L-1\le2L-2\) and \(L-s\le L\). Thus \(\operatorname{rad}(\Omega^{-1})\le2L-2\) as well. The bound is symmetric in the forward and inverse maps and applies to arbitrary quantum operators, since each block gate can spread a noncommuting operator across its full block.

For \(L=1\), the encoder and within-block rotation are trivial and the coarse shifts cancel, so \(\Omega=I\) with radius zero. The displayed \(2L-2\) formula also gives zero; the intermediate two-block cone argument is only needed for \(L\ge2\).

## What the finite-depth statement costs

At the block-gate abstraction, the certificate has depth three, one \(L\)-site gate per block per layer. This does not make it a constant-time nearest-neighbor protocol. In particular, the encoder's output \(q=\mathrm{majority}(x_1,\ldots,x_L)\) depends on the far-end input bit: choose the other \(L-1\) bits to contain exactly \((L-1)/2\) ones. A circuit of two-site nearest-neighbor gates therefore needs depth at least \(L-1\) for that dependence to reach the final register. The inverse encoder also has long-range dependence: at fixed syndrome, changing \(q\) complements the reconstructed string, including its first register. The cyclic block rotation itself can be implemented by \(L-1\) adjacent SWAPs per block and has an \(\Omega(L)\) endpoint-transport lower bound. The permutation-level finite-depth result consequently leaves synthesis, clock, and control costs growing with \(L\) to be charged; it claims no fixed-time bounded-range Hamiltonian implementation.

## Finite rings

On a periodic ring of \(N\) sites the exact identities hold when \(L\mid N\), using cyclic blocks and cyclic coarse shifts. If \(N\) is not divisible by \(L\), these uniform block partitions and the cancellation formula are not defined as written. The operator has an ordinary three-layer circuit realization on each compatible finite ring, but GNVW index is an infinite-chain invariant; the index-one claim is the infinite-chain QCA statement (or its stable large-ring interpretation), not a nontrivial index assigned to a finite ring. For a geometric radius interpretation on a finite ring, take \(N\) larger than twice the claimed radius so the causal interval does not wrap onto itself.

## Exact small replay

`check_factorization.py` uses the opening's majority/syndrome encoder at \(L=3\), two blocks on a six-bit ring, and the active source-to-destination convention above. It exhaustively checks both \(S_\to=R C_\to\) and \(S_\to P^{-1}C_\leftarrow P=P_{+1}^{-1}RP\) on all 64 basis strings. The replay is a sign/order sanity check; the algebra and support-cone argument above establish the general result.
