# Uniform entanglement breaking for arbitrary bistochastic PPT words

9 October 2026. Complete proof candidate, developed for the nonstationary gate. This is a restricted theorem: every factor is both unital and trace preserving. It does not resolve arbitrary nonunital PPT words. No priority or external-certification claim is made.

## Theorem

For every d there exists an integer N_bs(d) such that every serial composition of N_bs(d) arbitrary bistochastic PPT maps M_d -> M_d is entanglement breaking.

The factors may vary independently and need not commute or belong to a finite alphabet. All longer words are EB too. The proof provides a finite recursive existence bound; its constants are not estimated efficiently.

Conventions: products compose from right to left; J(T)=sum T(E_ij) tensor E_ij; D(X)=tr(X)I. The notation >=_EB means the difference is EB, whereas >=_CP means its Choi matrix is positive.

## Inputs

The proof uses the following established mechanisms, with the exact interfaces made explicit.

1. The Kraus-lift and rank-one word-truncation estimates in Sections 1–2 of ../filter_closed_uniformity/FULL_SEMIALGEBRAIC_MAPPING_CONE_UNIFORMIZATION.md. They apply unchanged to different CPTP factors: if T_j has a Kraus family with b_j=sum_a ||wedge^2 K_{ja}||, then a product of m such factors has an EB approximation E satisfying

   ||J(T_m ... T_1-E)||_F <= c_d product_j b_j,
   c_d=sqrt(d^2-1).

   Indeed use the product Kraus family and truncate every Kraus word to rank one. No stationarity is used in this estimate.

2. The compact semialgebraic Lojasiewicz inequality, and semialgebraicity of separability through a finite pure-product decomposition.

3. Davidson–Marcoux–Radjavi, Transitive Spaces of Operators, arXiv:0706.2449, Theorem 4.9: a product span of k-transitive and l-transitive rectangular operator spaces is min(k+l, the endpoint dimensions)-transitive. Consequently the product span of d transitive subspaces of M_d is M_d. Applied to Kraus spaces, any product of d strictly output-positive CP maps has positive-definite Choi matrix. The two properties are distinct for one factor. Primary source: https://arxiv.org/html/0706.2449 (arXiv:0706.2449v1, Section 4, Theorem 4.9).

4. The elementary separable ball ||Z||_F<=1/d^2 around I tensor I, proved in Appendix A of the uniformization record.

5. The projection-to-projection block splitting used below is already present in Rahaman–Jaques–Paulsen, Eventually Entanglement Breaking Maps, arXiv:1801.05542v2, Theorem 3.2. The short argument here makes its moving-coordinate use explicit. Their Theorem 4.4 treats iteration of one channel; it is not being cited as an arbitrary-word theorem. Primary source: https://arxiv.org/abs/1801.05542v2 ; HTML inspected at https://arxiv.org/html/1801.05542 .

None of these inputs assumes the new nonstationary conclusion.

## 1. A finite boundary window from moving supports

Induct on d, with N_bs(1)=1. Let

 M=max_{1<=r<d} N_bs(r),       L=(d-1)M.

Let Phi_1,...,Phi_L be bistochastic PPT maps and put T=Phi_L ... Phi_1. Suppose T is not strictly output-positive. There is a rank-one density matrix rho_0 with singular T(rho_0). Put

 rho_i=Phi_i(rho_{i-1}),       P_i=supp rho_i,       r_i=rank P_i.

Every rho_i has trace one. For a unital TP positive map, supp Phi_i(P_{i-1}) has rank at least r_{i-1}: Phi_i(P_{i-1})<=I and its trace is r_{i-1}. The support of Phi_i(rho_{i-1}) equals the support of Phi_i(P_{i-1}), because rho_{i-1} is bounded above and below by positive multiples of P_{i-1}. Hence r_i>=r_{i-1}. Since the final output is singular,

 1<=r_0<=r_1<=...<=r_L<=d-1.

There are at most d-2 strict rank increases. The remaining edges form at most d-1 constant-rank runs. If each such run had fewer than M edges, then L<=(d-2)+(d-1)(M-1)=(d-1)M-1, impossible. Thus some consecutive run has at least M equal-rank steps.

At an equal-rank step P->P', unitality and the equal traces give exactly

 Phi_i(P)=P',        Phi_i(I-P)=I-P'.

Its Kraus matrices are block diagonal between the input decomposition P+(I-P) and output decomposition P'+(I-P'). The PPT condition annihilates the cross transfer between these blocks: the zero diagonal rows in the partially transposed Choi matrix must be zero rows. Therefore the map is the direct sum of two corner maps. In orthonormal moving coordinates these corners are bistochastic PPT maps on M_p and M_(d-p), respectively.

By the dimension induction, a length-M subrun has EB corner products and is itself EB. The full word T is EB by composition with the remaining CP factors.

Thus every L-word satisfies

 f(T)=0  ==>  T is EB,                                  (1)

where

 f(T)=min_{rho>=0, tr rho=1} lambda_min T(rho).

The minimum can equivalently be taken over pure rho. This boundary statement uses only the already-established lower-dimensional BISTOCHASTIC nonstationary theorem.

## 2. Uniform rank-one approximation near this boundary

Let K be the compact semialgebraic set of bistochastic PPT maps on M_d, and B=K^L its set of length-L products. This is a compact semialgebraic polynomial image. It is closed under Hilbert–Schmidt adjoint, because reversing an adjointed word gives another word in K.

Let g(T) be the Frobenius Choi distance to the compact set of EB CPTP maps. Both f and g are continuous semialgebraic functions on B. By (1), f=0 implies g=0. Lojasiewicz and the Kraus-lift estimate give constants A>0 and alpha>0 such that every T in B admits a Kraus representation satisfying

 b(T):=sum_a ||wedge^2 K_a|| <= A f(T)^alpha.             (2)

The notation b(T) selects a suitable representation; no uniqueness or continuous selection is asserted or required.

Also

 f(T*)=f(T).                                             (3)

Indeed f(T) is the minimum of <y,T(|x><x|)y> over unit x,y; the adjoint interchanges x and y. The adjoint of a bistochastic map is again CPTP. These are precisely the properties needed for the reverse-word argument below.

## 3. One-sided anchor lemma

Let U be CPTP and let E be EB with delta=||J(U-E)||_F. Let Psi be CPTP and strictly output-positive with f(Psi)=s>0.

If delta<=1/(2sqrt(d)), then

 E*(I)>=I/2.

Write E(X)=sum_a tr(F_a X) sigma_a with density matrices sigma_a. Then

 Psi E(X) >=_EB s tr(E*(I)X) I >=_EB (s/2) D(X).

Further,

 ||J(Psi U-Psi E)||_F <= sqrt(d) delta.

The separable ball therefore proves Psi U is EB whenever

 delta <= s/C_d,           C_d=2d^2 sqrt(d).             (4)

Since s<=1/d, (4) also implies the preceding smallness requirement. For bistochastic Psi one could improve sqrt(d) to 1, but no improvement is needed.

If U and Psi are bistochastic, the same conclusion applies to U Psi: apply the proved statement to Psi* U* and use (3). It is important that the adjoint of U is TP here.

## 4. Every sufficiently long weak-block word is EB

Choose an integer m with alpha m>1. Choose epsilon>0, epsilon<=1/d, small enough that

 c_d A^m epsilon^(alpha m-1) <= 1/C_d.                   (5)

Put W=2m+1. Consider any W blocks T_W,...,T_1 in B for which f(T_i)<=epsilon. Let s=max_i f(T_i), and choose an attaining block T_k.

If s=0, every block is EB by (1), so the conclusion is immediate. Otherwise, either at least m blocks lie immediately to its right, or at least m lie immediately to its left.

In the first case let U be the m-block product immediately to its right. Rank-one truncation and (2) give an EB E with

 delta <= c_d product b(T_j) <= c_d A^m s^(alpha m) <= s/C_d.

The anchor lemma shows T_k U is EB. In the second case reverse and adjoint the word and apply exactly the same argument, using (3). All exterior factors preserve EB.

Consequently every W-consecutive-block word with f<=epsilon throughout is EB. This is the step that replaces equal-map repetition: a maximal positive margin supplies the anchor, and bistochasticity makes either direction available.

## 5. Many strong blocks yield uniformly faithful chunks

Call a block strong if f(T)>=epsilon; blocks with f(T)<epsilon are weak.

Composing a bistochastic map of margin at least epsilon on either side by a bistochastic map preserves that lower margin. On the input side use TP; on the output side use unitality. Thus any grouped segment containing a strong block is itself bistochastic and has f>=epsilon.

Let

 K_epsilon={C in K: f(C)>=epsilon}.

This set is compact. By Input 3, every product of d maps in K_epsilon has positive-definite Choi matrix. Compactness gives a common eta>0 such that every such d-fold product V satisfies

 eta D <=_CP V <=_CP d D.                               (6)

If K_epsilon is empty, all blocks are weak and Section 4 already finishes the proof.

The positivity in (6) is uniform over the whole compact K_epsilon, so the number and lengths of the grouped intervening segments do not enter eta.

## 6. Faithful chunks may vary independently

For completeness, the faithful-word expansion extends to different factors. Let V_1,...,V_t satisfy

 eta D<=_CP V_j<=_CP beta D,        beta=d,

and take t>=2. Put R_j=V_j-eta D and z=1-eta/beta. Then 0<=_CP R_j<=_CP z V_j, so

 R_t...R_1 <=_CP z^t V_t...V_1.

Expand every V_j=R_j+eta D. The sum F of all terms containing D is EB, and T:=V_t...V_1=F+R_t...R_1. With H=V_(t-1)...V_2 (the identity when t=2) and w=tr H(I),

 T <=_CP beta^2 w D,
 F >=_EB eta^2 w D.

For the latter inequality, group all expansion terms whose leftmost factor is eta D into eta D H V_1=eta^2 w D+eta D H R_1. The residual grouped terms also contain D and are EB.

Moreover

 ||J(R_t...R_1)||_F <= tr J(R_t...R_1)
                    <= z^t beta^2 w d^2.

The elementary separable ball absorbs the residual into eta^2 w D as soon as

 z^t beta^2 d^4 <= eta^2.                               (7)

Choose a common finite t>=2 satisfying (7). If eta=beta every factor is already EB. If w=0 the entire word is zero. Hence every such t-chunk product is EB.

This is the existing faithful-word mechanism, with its varying-factor interface written out; it is not claimed as a separate discovery.

## 7. A finite total length

Put H=d t. A word containing at least H strong blocks contains a consecutive interval that can be partitioned into H segments, each containing one strong block. Absorb all intervening weak blocks into those segments. Section 5 groups every d consecutive segments into a chunk satisfying (6); Section 6 makes the resulting t-chunk interval EB.

On the other hand, if a block word contains fewer than H strong blocks and no W-consecutive weak blocks, its total length is at most

 (H-1)+H(W-1)=H W-1.

Thus every word of H W blocks in B is EB. Define recursively

 N_bs(d)=L H W.

This completes the dimension induction and proves the theorem. No exponent bound is asserted for the nonunital CPTP or arbitrary-CP PPT classes.

## Exact outstanding boundary

The analogous moving-support split survives without unitality, but its corners need not be bistochastic. More importantly, the maximal-margin anchor cannot be reversed for arbitrary CPTP factors: the adjoints are generally unital but not TP, so the EB approximation need not supply the input normalization used in Section 3.

A nonunital sequence can have successive positivity margins decrease arbitrarily rapidly. The estimate product b_i <= A^m product f_i^alpha alone does not dominate the final margin uniformly when only a small power of that final margin appears. No statement in this proof removes that obstruction.

## Verification record

The parent checked the primary Theorem 4.9 interface and read this complete argument for consistency. The adjacent verify_bistochastic_anchors.py and bistochastic_anchor_verification.json record nine unequal-word numerical checks, covering 482 Kraus words, of both positive Holevo margin decompositions and the associated contraction bounds. These computations are checks of the local inequalities, not a proof of universal quantifiers. No separate broad review or external certification was commissioned. Source provenance is recorded in NONSTATIONARY_SOURCE_PROVENANCE.md.
