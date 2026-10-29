# Independent rectangular Schur error-space and access review

28 October 2026. Reviewed `rectangular_schur_polar_decoder_20261028/GOVERNING_DECODER_v1.md` Sections 1–3 and their access premises. **Accepted at the explicit rectangular selected-error-space scope.** The soft polar filter and its physical error bound require the separate root review; they are not accepted by this receipt. No general Schur decoder, CG oracle, full-rank source guarantee or hardware implementation follows.

## Primary-source context actually inspected

Rizzo–Lami–Eisert–Leone, *Universal quantum coding*, arXiv:2609.38038v1, https://arxiv.org/html/2609.38038v1 , Appendix C and equations 146–152, supplies the selected representation-theoretic error support and weighted reference. Its Appendix C.2 separately asserts an efficient approximate-design encoder and budgets moment error; its Gaussian permutation expression is explicitly not an efficient implementation. These statements must not be conflated. The present review supplies independent finite representation checks and expands the access argument below. The source remains an external preprint, not an internally authored new universal coding theorem.

## Complete span, not an easy subset

Put k=2m>=4, lambda=(m,m), d=Catalan(m). All symmetric-group representations are in a real orthogonal Young basis, so conjugation of matrices corresponds to the diagonal action on vectorized matrices.

The dimension of End(V_lambda) invariants under S_(k−1) is one: restriction removes its unique corner and stays irreducible. Frobenius reciprocity with the point permutation representation gives multiplicity zero for (k−1,1), after subtracting the one trivial copy.

For H=S_(k−2)×S_2, the restriction has two inequivalent, multiplicity-one components. The horizontal strip removes the final two bottom-row boxes and carries the trivial S_2 representation; the vertical strip removes the final column and carries the sign representation. There are no other valid two-box strips from this rectangle. Therefore dim End(V_lambda)^H=2. The two-subset permutation representation is (k)⊕(k−1,1)⊕(k−2,2), giving multiplicity exactly one for (k−2,2).

The map sending an edge {i,j} to p_lambda((ij)) is equivariant. Its standard component vanishes. Its (k−2,2) component cannot vanish, since otherwise every transposition acts as the same scalar matrix; transpositions generate S_k, contradicting irreducibility of dimension d>=2. Thus its image contains the ENTIRE unique (k−2,2) component. Add identity to obtain exactly trivial⊕(k−2,2). At k=4 identity is essential because the transposition class sum is zero. This proves completeness for the selected sectors, not merely inclusion in a larger unknown multiplicity space.

## Gram matrix and no hidden conditioning

Let q=k(k−1)/2, r=k(k−3)/2 and t=(k−4)/(2(k−1)). The central sum of transpositions has content m(m−2)=k(k−4)/4. In normalized Hilbert–Schmidt inner product Tr(A†B)/d, the centered matrices U_e−tI therefore have Gram matrix

G = h P,   h = 3(k²−4)/[4(k−1)(k−3)],

where P projects onto the kernel of the vertex-edge incidence matrix. If B has vertices as rows and edges as columns, BB^T=(k−2)I+J and P=I−B^T(BB^T)^−1B. The diagonal of G is 1−t² and rank(P)=r, so its trace alone determines h=q(1−t²)/r. In particular h>=3/4; the component has a constant lower Gram eigenvalue. No small singular-value promise is hidden in orthonormalizing this polynomial-size coefficient space.

For orthonormal coefficient vectors v_a in range(P), F_a=h^−1/2 sum_e(v_a)_e U_e, together with F_0=I, obey Tr(F_a†F_b)=d delta_ab. Conjugation invariance and Schur's lemma imply both sum F_a†F_a and sum F_a F_a† equal (1+r)I. The reference channel is therefore exactly the equally weighted channel on this full support. The basis change acts only on the error index and does not require implementing a symmetric-group Clebsch–Gordan transformation.

The independent executable constructs Young matrices directly for m=2,...,6, verifies the Coxeter braid relations, and forms every transposition without author imports. Dimensions are 2,5,14,42,132. Centered Gram ranks are 2,9,20,35,54, with predicted nonzero eigenvalues 3,1.6,9/7,8/7,35/33. Maximum Gram entry mismatch is below7e−16. It also verifies sum_(j≠i) U_(ij)=(k−4)I/2 independently. Numerical examples supplement the all-k representation proof, not replace it.

## Efficient representation operations and code-block projectors

A standard tableau of shape(m,m) is a ballot path of length2m: a row bit for each label, with every prefix having at least as many top as bottom labels and exactly m of each. For adjacent labels i,i+1, compute their contents (column minus row). The adjacent transposition acts on at most the tableau and its valid swapped tableau, with diagonal coefficient inverse axial distance and off-diagonal sqrt(1−inverse-distance²). Invalid swaps have scalar action ±1. Axial distances and swap validity require polynomial-time reversible integer arithmetic. A transposition(i,j) uses at most2k−1 adjacent generators. Synthesizing the controlled two-level rotations to precision delta requires polynomial arithmetic and log(1/delta), not a d-entry lookup.

Rank/unrank of ballot paths is also explicit. The number of completions after a top and b bottom entries obeys the two-successor recurrence, with forbidden b>a and counts exceeding m removed. There are O(k²) dynamic-programming entries, each O(k) bits. Lexicographic rank and unrank use O(k) additions/comparisons on those entries. Reversible versions map between valid tableau paths and binary rank registers of ceil(log2 d) bits. Prefix and fixed K-block projectors use integer comparison and division. Invalid padded rank labels are never assumed to be physical tableaux.

The independent rank/unrank program checks 102 ranks each at m=2,3,5,10,25,50, including endpoints, with exact integer arithmetic. A supplied code circuit C and its inverse remain necessary: a prefix projector alone does not create a random code orientation.

## Non-power-of-two approximate designs: a concrete access route

The separate efficient-encoder premise can be supported without granting a Haar oracle or using a padded Hadamard that leaks out of the Specht space. Let qbits=ceil(log2 d), and identify physical tableau labels with binary integers0,...,d−1.

1. On qbits, apply an independent random diagonal two-qubit gate to every pair of bit positions. Each of its four diagonal phases is independently chosen from the fifth roots of unity. For qbits=1 use one random diagonal one-qubit gate. This is an exact diagonal-unitary 2-design. To see this, a second moment survives averaging precisely when, for every pair of positions, the unordered projected pair of input strings equals that of the output strings. The pair constraints determine the unordered global pair: positions where the two strings agree are fixed, and relative orientation among all differing positions is fixed by pair constraints. Thus only global multiset equality survives, exactly as with independent Haar diagonal phases. Fifth roots suffice because each phase exponent has absolute value at most2.
2. Diagonal gates preserve the labels below d. Restriction therefore has exactly the required diagonal second moments on the d-dimensional space, with O(log²d) gates and random choices, even though d is not a power of two.
3. Alternate these restricted diagonal designs with the actual Fourier transform modulo d and its inverse. Nakata et al., arXiv:1609.07021v3, Theorem9 and Corollary10 establish the second-moment contraction for Fourier-type pairs in arbitrary dimension. Their tensor-product circuit restriction is not needed for this dimension argument because the diagonal layer has already been supplied above. For sufficiently large d the contraction is O(1/d); polynomially many repetitions give any required logarithmic precision. Bounded small dimensions can be handled separately; this asymptotic statement does not use the leading-order expression as an exact finite-d numerical constant.
4. Cleve–Watrous, quant-ph/0006004, Section7.1, treats approximate QFT for arbitrary modulus with polynomial(log d,log(1/delta)) circuit size. Thus non-power-of-two labels do not require an exponentially sized unitary table. Each synthesized Fourier transform's error and all circuit errors must be paid across repetitions.

Sources: https://arxiv.org/html/1609.07021v3 (Theorem9, Definitions5/7, Lemma8); https://arxiv.org/html/quant-ph/0006004 (Section7.1); https://arxiv.org/abs/1206.4451 (diagonal-design circuit prior art). The pair-phase argument above is an explicit elementary access derivation, not a claim of historical novelty. Its finite combinatorial check covers qbits=2,...,7, all unordered string pairs, with no collisions of the pair-projection signatures.

The resulting moment precision must still be transferred into the NEW decoder's error estimate, including its constants. The main source's 3k! moment-error amplification is not automatically a received bound for an altered proof. The fixed-C decoder theorem and the approximate-design coding corollary should remain separately labeled until that propagation is checked.

## LCU normalization and boundaries of this receipt

The coefficient one-norm of every nontrivial F_a is at most sqrt(q/h)<2k. Polynomial-sized coefficient preparation plus SELECT over the actual transposition circuits supplies a common2k-normalized block encoding; padding with cancelling terms is allowed. Combining with code circuit C and uniform projection over N=1+r error labels costs another sqrt(N), giving alpha=2k sqrt(N). The projection is part of a coherent unitary dilation, not a repeated physical-postselection success assumption. Register dimension, polynomial classical coefficient arithmetic and each use of C/C† are charged.

This review accepts the representation/access ingredients of that construction. It does not accept the numerical QSVT-phase synthesis, the author's soft-polar error lemma, the probability of observing lambda=mu=(m,m), or a claim that low-defect environment sectors dominate a fixed mixed source. Other-sector weight and rare local sectors remain real yield costs. A rank-two promise alone does not remove them.
