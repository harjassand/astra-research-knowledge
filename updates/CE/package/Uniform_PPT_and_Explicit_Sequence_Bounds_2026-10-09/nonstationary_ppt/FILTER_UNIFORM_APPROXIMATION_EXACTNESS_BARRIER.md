# Filter-uniform approximation and positive EB domination do not give exactness

9 October 2026. A precise obstruction to an attractive upgrade of the postselection-robust approximation theorem. This record gives explicit examples, not a counterexample to finite exact EB length of PPT words. The examples use one qutrit PPT map. They do not assert that these maps can be factored into arbitrarily many PPT maps.

## Result

There are bistochastic PPT nonEB maps T_t on M_3, for every arbitrarily small t>0, with all of the following properties:

1. A single EB bistochastic reference S obeys

   (1-t/2) S <=_CP T_t <=_CP (1+t/3) S.                 (1)

2. For every joint positive input, the same reference gives a relative trace-norm approximation. After every additional separability-preserving CP postselection, the conditional outputs are still uniformly close, independently of the success probability.

3. For q_t=7/(7+3t), the explicitly repaired channel

   E_t=q_t T_t+(1-q_t)D_3,   D_3(X)=tr(X)I_3/3,         (2)

   is EB. In particular E_t-q_t T_t is EB, not merely CP, and q_t tends to one.

4. The construction has a full-Choi-rank variant that remains PPT and nonEB, with both marginals exactly maximally mixed, retaining (1) with a corresponding full-rank EB reference and retaining (2).

Thus no dimension-only positive threshold on filter-uniform distance, relative CP-order error, or the weight 1-q of a depolarizing EB repair can by itself force exact EB. Any exact serial-word proof needs additional information about the factors, or a genuine separable interior margin measured relative to the residual. Exponential decay of these output certificates alone does not suffice.

## 1. A concrete qutrit family

All indices below are modulo three. Set

 |Omega>= (|00>+|11>+|22>)/sqrt(3),    P=|Omega><Omega|,
 sigma_+=(1/3) sum_i |i,i+1><i,i+1|,
 sigma_-=(1/3) sum_i |i,i-1><i,i-1|,
 sigma_0=(1/3) sum_i |i,i><i,i|.

For 0<=t<=1 define

 rho_t=[2P+(3+t)sigma_+ +(2-t)sigma_-]/7.                (3)

These are the established Horodecki states with parameter alpha=3+t. The primary source is P. Horodecki, M. Horodecki and R. Horodecki, *Bound entanglement can be activated*, arXiv:quant-ph/9806058v1, equations (2), (4), and (5): https://arxiv.org/pdf/quant-ph/9806058 . That source supplies the historical family and classification. All properties used in this obstruction are also verified below directly. The obstruction is not claimed as a new state construction or priority result.

Each rho_t is positive and has trace one. Both reduced density matrices are I_3/3. Using the convention J(T)=sum_ij T(E_ij) tensor E_ij, define

 J(T_t)=3 rho_t.

Then T_t is CP, unital, and trace preserving. Explicitly,

 T_t(X)=(2/7)X
       +((3+t)/7) sum_i X_(i+1,i+1)|i><i|
       +((2-t)/7) sum_i X_(i-1,i-1)|i><i|.              (4)

No non-TP normalization or small-success branch is hidden in this example.

### PPT

The partial transpose of rho_t has three diagonal one-dimensional blocks 2/21 on |ii>. Each remaining two-dimensional block, in an appropriate orientation of |ij>,|ji>, is

 (1/21) [[3+t,2],[2,2-t]].                              (5)

Its determinant is [2-t-t^2]/441, which is nonnegative for 0<=t<=1. Hence every rho_t in (3) is PPT. For t<1 its partial transpose is positive definite.

### An explicit separable reference

Let omega=exp(2 pi i/3), and for a,b in {0,1,2} put

 u_(a,b)=(1,omega^a,omega^b)/sqrt(3).

The nine-term product-state average

 A=(1/9) sum_(a,b) |u_(a,b)><u_(a,b)|
                    tensor |conj u_(a,b)><conj u_(a,b)|

satisfies

 A=(P+sigma_++sigma_-)/3.                               (6)

To verify (6), averaging phases retains precisely the computational diagonal entries and the entries |ii><jj|; diagonal entries are counted only once. Therefore

 rho_0=(6/7)A+(1/7)sigma_+                              (7)

is explicitly separable. Let S=T_0; it is EB and bistochastic.

### An elementary witness detects every t>0

Define

 W=sum_i |ii><ii| + sum_i |i,i-1><i,i-1|
     -sum_(i != j) |ii><jj|.                           (8)

This W is block-positive. Here is a direct proof, including complex product vectors. For a fixed first-system vector x, put a_i=|x_i|^2. The quadratic form on the second-system vector is a positive diagonal matrix with entries 2a_i+a_(i+1), minus a rank-one matrix. For strictly positive a_i, this matrix is positive exactly when

 sum_i a_i/(2a_i+a_(i+1)) <= 1.

After multiplication by the positive common denominator, the difference between the right and left sides has numerator

 a_0^2 a_2+a_0 a_1^2+a_1 a_2^2-3a_0a_1a_2 >= 0,      (9)

by AM-GM. Zero coordinates follow by continuity. The phases of x change the rank-one vector but not this rank-one-update criterion. Consequently W has nonnegative expectation on every product vector, and hence on every separable state.

On the three mutually orthogonal components in (3),

 tr(WP)=-1,    tr(W sigma_+)=0,    tr(W sigma_-)=1.

Thus

 tr(W rho_t)=-t/7 <0                  whenever t>0.     (10)

So T_t is nonEB for every 0<t<=1. No range-criterion inference or unverified entanglement threshold is needed.

## 2. Two-sided CP-order approximation with exact marginals

The three supports of P, sigma_+, and sigma_- are mutually orthogonal and do not vary with t. The ratios of the respective coefficients of rho_t to rho_0 are

 1,       1+t/3,       1-t/2.

It follows exactly that

 (1-t/2)rho_0 <= rho_t <= (1+t/3)rho_0.                  (11)

The Choi correspondence gives (1). Since both channels are bistochastic,

 T_t*(I)=S*(I)=I,        T_t(I)=S(I)=I.                 (12)

In particular the obstruction survives exact matching of both the input effect and global output, not merely matching total Choi trace.

The CP order is stronger than a trace-distance approximation: it is preserved after adjoining any reference and applying the maps to any positive joint input, and under arbitrary CP preprocessing or postprocessing. Even simultaneous relative approximation in both CP-order directions has no nonzero exact-separability threshold.

## 3. Uniformity under arbitrarily rare postselection

The following elementary lemma records the relevant implication of CP order.

Suppose 0<delta<1 and positive operators A,B obey

 (1-delta)B <= A <= (1+delta)B.                         (13)

Then A-B=B^(1/2) K B^(1/2) on supp B for a Hermitian contraction with ||K||_infinity<=delta. Holder's inequality gives

 ||A-B||_1 <= delta tr B.                              (14)

This argument works at singular B; (13) makes both A and A-B supported on supp B.

If p=tr A>0 and r=tr B, then r>0 and

 ||A/p-B/r||_1
 <= [||A-B||_1+|p-r|]/p
 <= 2delta/(1-delta).                                 (15)

For any finite reference R and any positive joint X, apply this to

 A=(id_R tensor T_t)(X),
 B=(id_R tensor S)(X),
 delta=t/2.

Here B is separable and p=r=tr X, so the sharper unconditioned conclusion is

 ||(id_R tensor (T_t-S))(X)||_1 <= (t/2)tr X.            (16)

Next apply any CP map L to both joint outputs. CP order is preserved, so (15) gives, for each nonzero successful outcome,

 ||L(A)/tr L(A)-L(B)/tr L(B)||_1
 <= t/(1-t/2).                                        (17)

When L preserves the separable cone, including arbitrary local CP filters and finite LOCC postselected branches without ancillary entanglement, the comparison output remains separable. The bound is independent of both success probabilities, reference dimension, input X, and conditioning operation. The conditional probabilities for T_t and S need not be equal after this further postselection; inequality (15) explicitly accounts for that difference.

Thus even a hypothetical strengthening of the serial-word approximation theorem that controls all further local postselection would not, by itself, supply a positive distance gap separating every nonEB PPT map from the EB cone.

The statement concerns one use of T_t and additional separability-preserving operations. It makes no tensor-power or entanglement-activation claim.

## 4. Positive EB domination with an EB residual

First, (11) gives the simple domination

 (1+t/3)^(-1) T_t <=_CP S.

The residual for this particular choice need not be EB. More strongly, an EB residual can also be imposed explicitly.

Put q=7/(7+3t) and define the normalized Choi matrix of E_t by

 e_t=q rho_t+(1-q)I_9/9.                               (18)

Using (6), direct coefficient comparison gives

 e_t=[6A+t sigma_0+(1+2t)sigma_+]/(7+3t).               (19)

All coefficients in (19) are nonnegative and add to one. Hence e_t is separable, and E_t is exactly the EB map in (2). The remainder is the EB channel contribution

 E_t-qT_t=(1-q)D_3.

There is also an even smaller-weight repair using a non-depolarizing EB residual:

 [7/(7+t)]rho_t+[t/(7+t)]sigma_-
     =[7rho_0+t sigma_+]/(7+t),                        (20)

which is separable by (7). Every state in (18)--(20), including both residual states, has both marginals I_3/3.

Consequently the inference

 "E is EB, E=qT+(1-q)R with R EB, and q is sufficiently close to one"

is false as an exact-EB criterion even for bistochastic PPT T and even with R the completely depolarizing channel. The separable cone is convex but not closed under subtraction of one of its positive elements.

Choosing t_n=exp(-cn) makes the repair weight and all filter-uniform errors exponentially small while each selected T_(t_n) remains nonEB. This parameter n only indexes the examples. It is NOT a PPT factorization length and does not refute any theorem about long PPT words.

## 5. A full-Choi-rank version

For 0<t<=1/5 define

 rhohat_t=(1-t^2)rho_t+t^2 I_9/9,
 shat_t=(1-t^2)rho_0+t^2 I_9/9.                        (21)

Both are positive definite and PPT, and both marginals remain I_3/3. The comparison state shat_t is separable. The same coefficient inequalities give

 (1-t/2)shat_t <= rhohat_t <= (1+t/3)shat_t.             (22)

On the other hand tr W=6, so

 tr(W rhohat_t)=-(1-t^2)t/7+(2/3)t^2 <0.               (23)

For the stated interval the inequality follows from

 3-14t-3t^2 >= 3-14/5-3/25=2/25>0.

Thus the full-rank map That_t with normalized Choi rhohat_t remains nonEB. If q is as in Section 4, then

 q rhohat_t+(1-q)I_9/9=(1-t^2)e_t+t^2 I_9/9

is separable as well. So the two-sided CP-order obstruction and depolarizing-repair obstruction both persist at full Choi rank. In particular neither zero Choi eigenvalues nor a singular global output is essential to these failures of inference.

For completeness there is also a fixed-full-rank-reference existence version. Join I_9/9 to any fixed full-rank PPT-entangled state with maximally mixed marginals, such as a chosen rhohat_t. The line meets the closed convex separable set in an initial interval [0,s_*], with 0<s_*<1 by the separable ball and entanglement of the endpoint. Its last separable point is still positive definite. Points immediately beyond it are PPT entangled and approach it in relative operator norm, uniformly under all the filters in Section 3. This statement needs no explicit value of s_*.

## 6. What this eliminates, and what it leaves open

This eliminates an output-only argument of any of the following forms:

- postselection-robust distance below a dimension-only threshold implies EB;
- a sufficiently tight CP-order sandwich around an EB map implies EB;
- an EB map that CP-dominates almost all of a PPT map implies that PPT map is EB;
- the preceding domination becomes sufficient when its positive remainder is EB, or specifically depolarizing;
- full Choi rank, exact input/output marginals, or bistochasticity repairs one of these output-only implications.

It does not eliminate a factor-sensitive use of positive repairs. A successful exact proof could still extract a separable interior anchor from several actual factors and compare its margin to the residual. Nor does it eliminate positive dimension reduction along the concentrating branch. What cannot be discarded is the serial factor structure: the repaired output and its exponentially small positive remainder do not retain enough information to infer exactness by themselves.

The accompanying script verify_filter_uniform_exactness_barrier.py checks the explicit phase decomposition, witness expectations, PPT matrices, both CP-order inequalities, depolarizing repair, full-rank modification, and bounded random local-filter instances. The exact inequalities above are the proof; numerical checks are only consistency tests.
