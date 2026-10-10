# Uniform exact serial length for completely positive 2-copositive maps

9 October 2026, after the unrestricted PPT edition. New internally derived extension candidate. The frozen PPT proof and integrated archive are unchanged. This note checks the exact additional interfaces needed to replace complete copositivity by 2-copositivity throughout that proof. It is not covered by the earlier focused review reports and carries no external certification or priority claim.

## Statement

For each d there is a finite integer M(d) such that every serial word of M(d) completely positive, 2-copositive maps on M_d is entanglement breaking.

Here 2-copositive means that transpose composed with the map is 2-positive. It does not mean 2-entanglement breaking. Factors may vary arbitrarily and need not be TP or unital. The claim concerns serial composition; it makes no tensor-power distillability statement.

The proof is the dimension induction in UNRESTRICTED_PPT_WORD_THEOREM.md with the class CP intersect 2-CoPos in place of PPT. The only use of complete copositivity that requires a new argument is the rectangular moving-support split. Sections 1–3 below verify that argument and every closure interface. The semialgebraic exponent and hence M(d) may differ from the PPT constants.

## 1. A qubit test gives the same support split

Let Phi:M_a -> M_b be CP and 2-copositive. Let P,P' be input and output projections, Q=I−P, Q'=I−P', and suppose

 Q' Phi(P) Q'=0.

Complete positivity gives triangular Kraus matrices K_j=[[A_j,B_j],[0,C_j]]. For any u in ran P and v in ran Q, consider the pure input vector

 omega=|0> tensor u + |1> tensor v.

The two-dimensional-reference output has block matrix

 M=[[Phi(|u><u|),Phi(|u><v|)],
    [Phi(|v><u|),Phi(|v><v|)]].

It is positive by CP. By 2-copositivity its partial transpose on the output is positive. Taking the full transpose, which preserves positivity, shows that the partial transpose on the qubit is positive as well:

 M^(T_qubit)=[[Phi(|u><u|),Phi(|v><u|)],
             [Phi(|u><v|),Phi(|v><v|)]] >=0.

For y in ran Q', the vector |0> tensor y has zero quadratic form against this positive matrix. A positive matrix annihilates any vector with zero quadratic form. Its lower block therefore yields

 Phi(|u><v|)y=0.

Thus Phi(|u><v|)Q'=0. In the triangular Kraus coordinates this is exactly

 sum_j A_j |u><v| C_j*=0.

Rank-one u v* span the entire rectangular P-to-Q cross space, so sum_j A_j X C_j*=0 for every cross input X. The entry coefficient spaces of the A_j and C_j are orthogonal in the Kraus index. Rotate that index to obtain

 Phi=F+G,

with F CP and output-supported in P', and G CP and input-supported in Q. As in the PPT proof, the full summands need not themselves be 2-copositive. The diagonal corner maps equal CP compressions of Phi and retain 2-copositivity.

Consequently every proper moving-support chain again has only one-switch positive terms, and the same conditional length 2M(d−1)+1 makes it EB.

## 2. Closure and rectangular padding

For a rectangular CP map Lambda define bar(Lambda)=T_out Lambda T_in, which is CP by complex conjugation of its Kraus matrices. If Phi is 2-copositive, then for arbitrary compatible CP maps A,B,

 T (A Phi B)=bar(A) (T Phi) B

is 2-positive. Thus CP pre/postcomposition, matrix filters, corner compression and isometric embedding preserve the class. Composition of two members is included as a special case, and addition and nonnegative scaling preserve it by convexity. In particular EB depolarizing completions stay in the class.

Padding a rectangular corner map into M_(d−1) uses exactly such CP compressions and embeddings, so the induction hypothesis for arbitrary square maps applies to its corner chains. Zero maps cause no difficulty.

The dimension-one base case is immediate. No qutrit-specific statement is needed for the induction.

## 3. Compact semialgebraic parameter sets

CP is a closed semialgebraic constraint on Choi matrices. For 2-copositivity, it is enough to test

 (id_2 tensor T Phi)(|z><z|)>=0 for all z in C^2 tensor C^d,

because all positive inputs are sums of pure projectors. This is a universal finite real-polynomial condition after separating real and imaginary parts and using principal minors, or scalar quadratic forms against all test vectors. Quantifier elimination shows that the set of such maps is semialgebraic. It is closed as an intersection of closed positivity conditions.

Its CPTP and unital slices are closed subsets of the respective compact CP slices. Hence they are compact. In the normalized boundary relation of the PPT proof, replace each raw-PPT and normalized-PPT constraint by CP plus 2-copositivity. All other equations, bounded variables and tags are unchanged. No inverse is introduced on the boundary.

At zero tag, the same moving-support proof makes the raw first block EB. If a limiting forward state is faithful, the bounded filtered prefix is EB. Otherwise the normalized maps transport the proper kernels of the limiting dual state path, and Section 1 plus lower-dimensional exactness makes the tail EB. Thus the same compact semialgebraic zero-set implication, Kraus-lift bound and multiplicative normalized-pair estimate hold for the larger class.

## 4. Remaining dependencies are unchanged

The following parts of the unrestricted proof use no complete copositivity beyond the class properties already checked:

- tagged boundary counting and compression at globally output-singular factors;
- forward-state unital normalization and its inverse-free intertwining and dual identities;
- separable Choi distance, finite rank-one Kraus lift and multiplicative exterior-square defect;
- the maximal-tag forward and reverse separable-margin anchors;
- the strict-output-positive arbitrary-CP-gap theorem, which uses no copositivity at all;
- density by adding a small depolarizing channel;
- exact backwards-effect normalization, including its EB singular-support completion.

Applying those sections verbatim with the new class yields the stated finite dimension-only exact length. The earlier explicit quantitative approximation already used CP and 2-copositivity, so the exact extension aligns the classes without changing that rate proof.

## 5. The enlarged class is genuinely larger

For d>=3 and 1/d<beta<=1/2, define

 Phi_beta(X)=[tr(X) I−beta X^T]/(d−beta).

With the usual unnormalized Choi convention,

 J(Phi_beta)=[I tensor I−beta F]/(d−beta),

where F is the swap. Its eigenvalues are proportional to 1−beta and 1+beta, so Phi_beta is CP. Its partial traces are I, so it is bistochastic. Its Choi partial transpose is

 [I tensor I−beta |Omega><Omega|]/(d−beta),

where Omega=sum_i |i,i>. A normalized vector of Schmidt rank at most two satisfies |<Omega,z>|^2<=2. Therefore this partial transpose is 2-block-positive when beta<=1/2, proving 2-copositivity. But it has negative expectation on Omega when beta>1/d, so the map is not PPT.

This elementary Werner-form example establishes strict enlargement of the allowed factors. It is not evidence about tensor-power distillability, and the theorem does not claim that its universal exponent is optimal even for this family.

## Attribution boundary

The published 2-EB iteration theorem of Christandl–Muller-Hermes–Wolf remains a different statement: CP and 2-copositivity do not in general imply 2-EB in higher dimensions. The new support-split argument uses positivity of qubit partial-transpose tests at an exact zero corner, not separability of all those outputs. The full unrestricted-PPT primary comparison is preserved separately; a complete literature priority check for this larger class has not been made.

The existing general_cp_eventual_eb/FINITE_CRITERION.md, Sections 6–7, already records the programme's equal-map eventual 2-copositivity equivalence, CP-and-2-copositive uniform equal-power consequence, and the same standard transpose-depolarizing example. The new conclusion here is the unrestricted arbitrary-factor word bound. For the published unital equal-map comparison, Bhat–Dey–Saha, arXiv:2609.24168v1 (21 September 2026), Theorem 6.11, includes eventual 2-copositivity among its equivalent unital-channel properties: https://arxiv.org/html/2609.24168v1 . That precise source interface was inspected and recorded in general_cp_eventual_eb/SOURCE_PROVENANCE.json.
