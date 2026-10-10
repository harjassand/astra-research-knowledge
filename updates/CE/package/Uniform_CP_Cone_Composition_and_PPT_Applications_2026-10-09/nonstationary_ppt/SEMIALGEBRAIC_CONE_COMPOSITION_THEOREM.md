# A uniform composition principle for eventually entanglement breaking cones

9 October 2026. New complete internally derived proof candidate. This extends the preserved uniform equal-power theorem to arbitrary products and explains the structural class behind the unrestricted PPT and 2-copositive examples. It is not covered by the earlier focused reviews; external validation and priority remain open.

## Theorem

Let C be a nonzero closed convex semialgebraic cone of completely positive maps M_d -> M_d. Assume it is a CP mapping cone: A Phi B belongs to C whenever Phi belongs to C and A,B are arbitrary CP maps on M_d.

If every Phi in C is individually eventually entanglement breaking, then there is a finite integer N(C) such that every serial product of N(C) arbitrary members of C is entanglement breaking.

Consequently the following are equivalent for such a cone:

1. Every member has some EB power, with the exponent initially allowed to depend on that member.
2. There is a common EB exponent for equal-map powers.
3. There is a common EB length for all independently varying serial words.

Only 1 implies 3 needs the proof below. The quantitative exact exponent is not supplied. Its constants depend on the cone as well as dimension. For canonical dimension-indexed classes such as PPT or CP intersect 2-CoPos, this becomes a dimension-only bound.

The theorem concerns positive composition. It is not an abstract compact nil-semigroup statement, and does not use subtraction to extract separable summands from a separable sum.

## 1. The cone contains depolarization

Since C is nonzero, choose Phi in C and unit vectors u,v such that a=<v,Phi(|u><u|)v>>0. The maps

 B(X)=tr(X)|u><u|,      A(Y)=<v,Yv>I

are CP. Their composition A Phi B=a D, where D(X)=tr(X)I. Thus D belongs to C by the mapping-cone property and positive scaling.

It follows that the CPTP slice is nonempty and that adding any positive multiple of D remains within C. Depolarizing regularization used later is therefore legitimate. No assumption that C contains all CP maps is made.

## 2. Pointwise eventual EB forces rectangular support decoherence

Let Phi in C and let P,P' be input and output projections of arbitrary ranks, with Q=I−P, Q'=I−P', and

 Q' Phi(P) Q'=0.                                      (1)

Complete positivity makes each Kraus matrix triangular:

 K_j=[[A_j,B_j],[0,C_j]].

We prove

 sum_j A_j X C_j*=0 for every X in P M_d Q.             (2)

This argument does not align the full projections, so their ranks may differ or oscillate along a word.

Suppose (2) fails. Rank-one cross matrices span P M_d Q, so there are unit vectors u in P, v in Q, a in P', b in Q' with

 lambda=<a,Phi(|u><v|)b> != 0.

Choose two orthonormal fixed vectors e_0,e_1 in C^d and define matrix filters

 B=|u><e_0|+|v><e_1|,
 A=|e_0><a|+|e_1><b|.

The filtered map Psi=Ad_A Phi Ad_B belongs to C. It is zero on input components outside span(e_0,e_1), has output in that same span, and its Kraus matrices on the active two-dimensional block are triangular:

 L_j=[[a_j,b_j],[0,c_j]],     sum_j a_j conjugate(c_j)=lambda.

Writing E_ij=|e_i><e_j| gives

 Psi(E_00)=alpha E_00,
 Psi(E_01)=gamma E_00+lambda E_01.

Therefore for every n>=1,

 Psi^n(E_00)=alpha^n E_00,
 Psi^n(E_01)=gamma_n E_00+lambda^n E_01.                (3)

Since lambda is nonzero, these powers are not EB. To see this directly, apply id_2 tensor Psi^n to the pure input |0,e_0>+|1,e_1>. After partial transpose on the qubit, the vector |0,e_1> has zero diagonal quadratic form, but its coupling to |1,e_0> has coefficient lambda^n (up to conjugation). A positive matrix cannot have a nonzero coupling from a zero quadratic-form vector. Thus this output is NPT for every n.

This contradicts the hypothesis that every member of C is individually eventually EB, applied to the single filtered map Psi. Hence (2) holds.

The proof uses only a two-dimensional filtered witness, not complete or 2-copositivity of Phi.

## 3. The positive moving-support split

Equation (2) makes the entry-coefficient spaces of A_j and C_j orthogonal in the Kraus index. A unitary change of Kraus coordinates separates them. The Kraus operators with C=0 define a CP map F output-supported on P'; those with A=0 define a CP map G input-supported on Q. Operators with both A=C=0 may be assigned to either set. Hence

 Phi=F+G.

The full summands F,G are not asserted to belong to C. The diagonal corner maps, however, equal CP compressions of Phi and do belong to the corresponding induced corner cones.

For maps transporting proper nonzero projections P_(i−1) to P_i, the splits satisfy G_(i+1)F_i=0. Consequently

 Phi_n ... Phi_1
 =sum_(j=0)^n F_n ... F_(j+1) G_j ... G_1.               (4)

All terms are CP and have at most one switch. A run of k F factors contains k−1 smaller P-corner maps; a run of k G factors contains k−1 smaller Q-corner maps. This is the same positive mechanism as in the rectangular PPT proof, now obtained from the cone's pointwise premise.

## 4. The exact induced lower-dimensional cone

Fix an isometry W:C^(d−1)->C^d. For a map Theta on M_(d−1), define its zero-padded lift

 hat(Theta)=Ad_W Theta Ad_(W*),

and define

 C_small={Theta CP on M_(d−1): hat(Theta) belongs to C}.

This is a nonzero closed convex semialgebraic CP mapping cone. Closedness and semialgebraicity follow by taking the inverse image under the fixed linear lift. CP left/right composition downstairs lifts to CP left/right composition upstairs. Nonzeroness follows because the compression of D supplies D_(d−1).

Every Theta in C_small is individually eventually EB: the identity W*W=I gives hat(Theta)^n=hat(Theta^n), and an EB power upstairs restricts to an EB power downstairs. Thus the induction hypothesis applies to this exact cone. Let R=N(C_small).

All rectangular corner chains of dimensions at most d−1 are governed by this same R, including corners with different ranks and changing subspaces. Choose arbitrary isometries identifying each corner with a coordinate subspace of C^(d−1). Its padded lift through W is a CP input/output filtering of the original map on M_d, hence belongs to C. The padded corner therefore lies in C_small. Compatible embeddings make products reproduce the original rectangular chain after CP endpoint compression.

Equation (4) now makes every proper moving-support word of length

 B=2R+1                                                (5)

EB: one of the two runs in each summand has at least R+1 factors, hence contains R smaller-cone factors.

## 5. Tagged zero boundary in the compact CPTP slice

Set Q=(R+1)B. Work with Q-tuples of CPTP maps from C, a compact semialgebraic set. Give each actual tuple the tag

 s=max f(Phi_(j+B−1)...Phi_j),
 f(U)=min_(rho>=0,tr rho=1) lambda_min U(rho),

where the maximum ranges over all contiguous B-subwords. This tag is continuous and semialgebraic, and s=0 implies the Q-product is EB.

Indeed, R+1 factors with singular global output provide R smaller-cone transitions between their proper output supports and hence force EB. Otherwise at most R factors have singular global output, and Q factors contain a B-long run of full-global-output factors. If this run has zero strict-output margin, a pure input with singular final output gives a chain of nonzero proper supports: TP prevents zero support, and full-global-output maps cannot turn a faithful state singular. Apply (5).

This is the tagged boundary proof in the unrestricted PPT record with the exact smaller cone from Section 4. No uniformity over unrelated cones is assumed.

## 6. Compact normalization retains cone membership

For a faithful forward state path S_i=U_i(S_(i−1)), tr S_i=d, define

 B_i=Ad_(S_i^(-1/2)) U_i Ad_(S_(i−1)^(1/2)).

The mapping-cone property puts every B_i in C. They are CP unital and satisfy B_i*(S_i)=S_(i−1). Both the fixed-trace states and unital CP maps have compact ranges.

To make the boundary relation explicit without any inverse, retain the raw C-CPTP factors, the first tagged Q-product U_1, the constituent maps of a second Q-block U_2,...,U_(Q+1), positive matrices X_i with tr X_i^2=d, maps B_i in the unital slice of C, the tag s, and Z=B_(Q+1)...B_1. Impose

 S_i=X_i^2,
 S_i=U_i(S_(i−1)),
 Ad_(X_i) B_i=U_i Ad_(X_(i−1)),
 B_i*(S_i)=S_(i−1),          B_i(I)=I.                 (6)

Membership in the fixed semialgebraic cone C replaces the PPT constraints in the preceding proof. All equations and conditions are closed semialgebraic and all variables are bounded. Thus (6) defines a compact semialgebraic relation containing every faithful normalization graph and its closure.

At s=0, U_1 is EB. If some S_i with i>=1 is faithful, telescoping (6) gives the EB prefix

 B_i...B_1=Ad_(X_i^(-1)) U_i...U_1 Ad_(X_0).

If all S_i, i>=1, are singular, the dual equation forces B_i to transport ker S_(i−1) into ker S_i for every i>=2. These kernels are nonzero and proper because tr S_i=d. There are Q>=B tail factors in C, so (5) makes the tail EB. Thus in either case Z is EB at every zero-tag point of the entire relation, not just its faithful part.

By compact semialgebraic Lojasiewicz and the bounded-Choi rank-one Kraus lift, there are A,alpha>0, depending only on C and the fixed lengths, such that every such normalized pair Z admits a Kraus family with

 sum_a ||wedge^2 K_a||_op <= A s^alpha.                 (7)

The lift and all multiplicative/truncation bounds use only CP and EB geometry; they make no additional class assumption.

## 7. Exact anchoring and the finite word count

For completeness, the constants and directions from the unrestricted proof specialize as follows. Put kappa_d=sqrt(d^2−1), choose m with alpha m>1, and take epsilon>0, epsilon<=1/d, so that

 kappa_d d A^m epsilon^(alpha m−1)<=1/(2d^2 sqrt(d)).    (8)

Across 2m weak Q-blocks, normalized pair defects multiply to at most (A s^alpha)^m. In the forward direction, undoing the trace-d output filter costs at most d in the defect. In the reverse direction, normalize the CPTP gap's output and absorb its unital initial map, costing at most d/2. The strict anchor Psi remains unchanged and retains its margin s. Rank-one Kraus truncation then gives Choi-Frobenius error at most kappa_d d(A s^alpha)^m.

The forward approximation E has E*(I)>=I/2; the reverse unital approximation has E(I)>=I/2. In either direction, composition with the selected strict anchor has an EB-order buffer (s/2)D. Composition changes the Choi-Frobenius error by at most sqrt(d), and the separable-ball radius 1/d^2 around J(D) makes the final map EB by (8). Undoing the final output filter preserves EB. These are exactly the two detailed positive-anchor calculations in UNRESTRICTED_PPT_WORD_THEOREM.md, Sections 6–7; they involve only CP, TP/unital normalization and the stated defects.

Therefore a run of W=4m+1 weak Q-blocks is EB: select a maximal-tag block, find 2m blocks on one side, and use the corresponding anchor. If the maximal tag is zero, Section 5 already applies.

For strong tags s>=epsilon, the compact strict-output-positive anchor theorem supplies a finite H(d,epsilon) anchor count, even with arbitrary CP maps in all gaps. Its proof uses rectangular transitive Kraus spaces, compact normalized CP gaps and positive depolarizing expansion, with no cone-specific assumption. The targeted normalization check is STRONG_ANCHOR_INTERFACE_CHECK.md.

A word with fewer than H strong blocks and no W-consecutive weak run has at most HW−1 blocks. Thus

 N(C)=Q H(d,epsilon) W                                  (9)

works for faithful-regularized C-CPTP words.

The depolarizing map belongs to C by Section 1, so (1−t)Phi+tD_d stays in the cone and is strictly output-positive. All constants were chosen on the full compact C parameter relation, independently of t. Taking t to zero and using closedness of EB proves (9) for every C-CPTP word.

## 8. Arbitrary CP normalization stays in the same cone

Given any C-word Phi_n...Phi_1, regularize each factor as Phi_i+delta D with delta>0. This remains in C. Set Y_n=I and Y_(i−1)=Phi_(i,delta)*(Y_i); all these effects are positive definite. The normalized factors

 Theta_i=Ad_(sqrt(Y_i)) Phi_(i,delta) Ad_(Y_(i−1)^(-1/2))

are CPTP and belong to C by the mapping-cone property. They have the same number of factors, and their product is the regularized original product followed by Ad_(Y_0^(-1/2)). Its EB property therefore implies the regularized original word is EB. Let delta decrease to zero.

The exact singular-support completion from POSTSELECTION_ROBUST_EB_APPROXIMATION.md gives the same conclusion directly; its completion term is EB and belongs to C because a nonzero CP mapping cone contains all EB maps (rank-one measure-and-prepare maps are CP filters of D, and their sums and limits are in C). The regularized argument above avoids needing this additional observation.

## 9. Dimension induction and scope

For d=1, all CP maps are EB. At d>=2, Section 4 supplies a cone in dimension d−1 with the identical hypotheses, so the universal dimension induction is valid. This completes the candidate proof of 1 implies 3.

The previously established equal-power cone theorem remains a preserved independent proof. This composition theorem does not rely on it: it uses the pointwise premise only in the two-dimensional filtered-coherence contradiction of Section 2 and in passing that premise to the smaller cone.

For the PPT cone, the direct qubit/full-PPT support split already gives the needed mechanism, as proved in the unrestricted PPT record. For CP intersect 2-CoPos, TWO_COPOSITIVE_EXACT_WORD_EXTENSION.md supplies the direct qubit split. Alternatively their pointwise eventual-EB premise is established by the preserved criterion and earlier results, and the present general theorem applies.

No direct implication about noisy approximate membership, efficient numerical constants, NPT tensor-power distillability, or unrestricted quantum networks is asserted. CP controls and filters within the fixed transmitted dimension are included through the mapping-cone property.

## 10. Contrapositive interpretation and a noncopositive example

Under exactly the full cone hypotheses of the theorem, if for every n there is a nonEB word of length n in C, then C contains at least one single map with no EB power. Thus persistent entanglement cannot be an exclusively switching phenomenon in these cones while every individual member eventually destroys it. This statement does not extend here to arbitrary compact sets, nonconvex classes or families without CP-filter closure.

The universal theorem covers more than copositive examples. Fix any strictly output-positive CP map Phi and take the cone generated by all A Phi B with A,B CP. To see the structural hypotheses directly, normalize nonzero A,B by tr J(A)=tr J(B)=1. These filters form compact semialgebraic sets. If Phi(rho)>=epsilon I for all density rho, then

 tr J(A Phi B)=tr A(Phi(B(I)))>=epsilon,

while compactness gives a finite upper bound. The generator slice is therefore compact and bounded away from zero by its positive trace. Its conic convex hull is closed and semialgebraic, using at most d^4 generators by conical Caratheodory, and is a CP mapping cone by construction.

The strict-positive filtered-word theorem gives a finite common seed count for all its products: expand each factor as a finite positive sum of A Phi B terms and use the seed bound on each branch. Thus this cone satisfies the pointwise premise independently. In dimension two, the seed

 Phi(X)=pX+(1−p)tr(X)I/2,       1/3<p<1,

is strictly output-positive but is not 2-copositive: the antisymmetric eigenvalue of its Choi partial transpose is (1−3p)/2<0. This provides a concrete cone covered by the universal principle that is not contained in CP intersect 2-CoPos. The example illustrates scope, not a separate novelty claim.
