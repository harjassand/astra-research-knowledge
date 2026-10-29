# Nonrectangular multiplicity boundary for the transposition construction

Independent derivation, 28 October2026. This is a useful failure of a naive extension, not part of the received rectangular decoder theorem.

For lambda=(a,b), a−b>=2 and b>=2, restriction to S_(k−1), k=a+b, has two removable corners. Hence the standard representation has multiplicity1 in End(V_lambda). Restriction to S_(k−2)×S2 has four inequivalent components: remove two top-row boxes (horizontal), remove two bottom-row boxes (horizontal), or remove one from each row, which permits both the trivial and sign S2 representations because the two removed boxes are in distinct rows and columns. Therefore the two-subset permutation module occurs with inner product4, and

multiplicity_(k−2,2) = 4 − 1 − 1 = 2.

The transposition label module contains only one copy of (k−2,2). Thus identity plus all transpositions CANNOT span the full low-defect error space for these labels, irrespective of their conditioning or implementation efficiency. A decoder using that span must charge the missing copy as uncorrected source weight. This is an exact representation obstruction, not a failed numerical solver.

For a=b+1 and b>=2, the top-two-box horizontal removal is invalid. There are only three restriction components, so the same multiplicity is1; standard multiplicity remains1. This near-rectangular odd-k case is a possible separate extension, not covered by the even rectangular receipt.

The star operators provide a conditioning diagnostic. Let delta=a−b>0 and J_k=sum_(i<k) p_lambda((i,k)). On the two restriction branches J_k has contents a−1 and b−2. Their normalized dimensions are

p_top=delta(a+1)/[k(delta+1)],
p_bottom=b(delta+2)/[k(delta+1)].

Thus Var(J_k)=delta(delta+2)b(a+1)/k². The standard eigenvalue of the edge Gram matrix is this variance divided by (k−1)(k−2)/k, namely

h_standard = delta(delta+2)b(a+1)/[k(k−1)(k−2)].

It is positive. In the almost rectangular case delta1 it is of order1/k, so that new component does not immediately create exponential conditioning. This does not resolve the missing multiplicity for delta>=2.

A possible next representation is products of two transpositions, a polynomial O(k^4)-sized coefficient family. Its extra multiplicity directions, full selected support, positive Gram eigenvalues and efficient error-space projections need proof; polynomially many candidate matrices alone does not establish these obligations.
