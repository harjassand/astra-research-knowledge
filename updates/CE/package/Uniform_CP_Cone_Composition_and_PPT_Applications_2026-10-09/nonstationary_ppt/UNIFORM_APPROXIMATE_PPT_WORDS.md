# Uniform approximation by EB channels for arbitrary PPT words

9 October 2026. New complete proof candidate for arbitrary nonstationary PPT channels, including nonunital factors. This is an approximation theorem, not a finite exact EB word bound. It was developed after the preserved focused reviews and is not covered by those reports. No external certification or priority claim is made.

The later EXPONENTIAL_APPROXIMATE_PPT_WORDS.md strengthens the rate to ordinary exponential decay and broadens the factor class to CP plus 2-copositivity. This earlier independent determinant/dimension-induction route is retained as a proof record and supplies the detailed effect-normalization lemma used there.

## Theorem

For every integer d>=2 there are constants C_d,a_d>0 such that every length-n serial word T of PPT CPTP maps on M_d has an EB CPTP approximation E with

 ||T-E||_diamond <= C_d exp(-a_d n^(1/(d-1))).             (1)

The factors may vary arbitrarily, without stationarity, a finite alphabet, unitality, or a common faithful state. Constants depend only on dimension; no efficient numerical values or algorithm are supplied. The conservative exponent in (1) is not claimed to be sharp.

A stronger normalization statement used in the proof is this: if T is a word of n arbitrary PPT CP maps on M_d, then there is an EB CP map E with

 E*(I)=T*(I),
 ||T-E||_diamond <= C_d exp(-a_d n^(1/(d-1))) ||T||_diamond.  (2)

The zero map is harmless. Equation (2) is a norm-relative statement about maps. It does not promise a uniform error after normalizing the output on an arbitrarily unlikely input state.

## 1. A uniform determinant-weight contraction

For a Kraus family K=(K_j) of a CPTP map on M_d, define

 b(K)=sum_j |det K_j|^(2/d).

The arithmetic-geometric mean inequality for squared singular values gives

 |det K_j|^(2/d) <= ||K_j||_F^2/d,

so b(K)<=1. We show that every nonunitary CPTP map has some Kraus family with b(K)<1.

If its Choi rank is at least two, its Kraus span contains a nonzero singular matrix A. Indeed take two independent matrices in the span. The determinant on their two-dimensional complex linear span is a homogeneous polynomial of degree d. Either it vanishes identically or it has a nontrivial zero in the complex projective line. In either case a nonzero singular A exists.

Because vec(A) lies in the Choi range, a sufficiently small positive multiple t|vec(A)><vec(A)| can be subtracted while leaving a positive Choi matrix. Include sqrt(t)A as one Kraus matrix and decompose the positive remainder. Its determinant term is zero but its squared Frobenius norm is positive, so

 b(K) <= 1-t||A||_F^2/d < 1.                            (3)

A rank-one Choi CPTP map is unitary. For d>=2 no unitary channel is PPT: the partially transposed maximally entangled Choi matrix has a negative antisymmetric eigenvalue. Thus every PPT CPTP map satisfies (3).

The strict inequality is locally persistent with a suitable Kraus representation. Given a fixed representation K at Choi matrix J, pad its vectorized-column factor W to at least d^2 columns. Extend its polar partial coisometry to a coisometry U with W=sqrt(J)U. For nearby positive Choi matrices J', the columns of sqrt(J')U are Kraus matrices, depend continuously on J', and equal the original columns at J. Their determinant weight is therefore continuous. The same fixed coisometry works locally; there is no claimed global continuous Kraus choice.

The PPT CPTP slice is compact and contains no unitary channel. A finite subcover of these local neighborhoods consequently gives a constant

 0<c_d<1

such that every PPT CPTP map on M_d has a Kraus family with b(K)<=c_d. Increasing c_d slightly if necessary avoids the irrelevant case c_d=0. No continuity theorem for a convex-roof infimum is needed.

The determinant weight is the familiar pure-state quantity underlying G-concurrence. Its use here is explicitly derived; no novelty claim for that entanglement measure or its determinant multiplicativity is made.

## 2. Long words admit low-rank Kraus approximations

Choose the preceding Kraus families for an arbitrary length-l PPT CPTP word T. Its product Kraus family A_w satisfies, by determinant multiplicativity,

 sum_w |det A_w|^(2/d)
   = product_i sum_j |det K_(ij)|^(2/d)
   <= c_d^l.                                           (4)

Let L_w be obtained from A_w by deleting its smallest singular value, so rank L_w<=d-1. Write R_w=A_w-L_w. If s_d(A_w) is that smallest singular value, then

 ||R_w||_F^2=s_d(A_w)^2<=|det A_w|^(2/d).

Let E(X)=sum_w L_w X L_w*. This is CP, (d-1)-superpositive, and trace nonincreasing because L_w*L_w<=A_w*A_w term by term. Its Kraus Stinespring operators V,W obey

 ||V||=1,    ||W||<=1,
 ||V-W||^2=||sum_w R_w*R_w||<=sum_w ||R_w||_F^2<=c_d^l.

The elementary Stinespring comparison bound gives

 ||T-E||_diamond <= (||V||+||W||)||V-W|| <= 2c_d^(l/2).  (5)

For clarity, this bound follows by writing VXV*-WXW*=(V-W)XV*+WX(V-W)*, applying trace-norm submultiplicativity after any ancilla extension, and using contractivity of partial trace. No approximate separability test is used.

## 3. Effect-preserving extension from TP words to CP words

Let delta_r(k) denote the worst diamond distance of a length-k PPT CPTP word on M_r from EB CPTP maps. Both sets are compact, so the infimum defining the distance is attained.

For arbitrary PPT CP maps A_1,...,A_k on M_r and any matrix B:C^s->C^r, put

 T=A_k ... A_1,          R=T Ad_B.

There exists an EB CP F:M_s->M_r with

 F*(I)=R*(I),
 ||R-F||_diamond <= delta_r(k) ||R||_diamond.             (6)

First suppose the backwards effects below are positive definite. Set Y_k=I and Y_(j-1)=A_j*(Y_j), and define

 Theta_j=Ad_(Y_j^(1/2)) A_j Ad_(Y_(j-1)^(-1/2)).

Each Theta_j is PPT and TP. Telescoping gives

 T=Theta_k ... Theta_1 Ad_(Y_0^(1/2)).

Choose an EB CPTP approximation Z to the normalized product, and set

 F=Z Ad_(Y_0^(1/2) B).

Its input effect is exactly B*Y_0 B=R*(I). Moreover

 ||R-F||_diamond
 <= delta_r(k) ||Ad_(Y_0^(1/2)B)||_diamond
 = delta_r(k) ||B*Y_0 B||_op
 = delta_r(k) ||R||_diamond.

Here a CP map's diamond norm is ||R*(I)||_op. There is no inverse-condition-number loss.

In the general case replace every A_j by A_j+epsilon D, D(X)=tr(X)I. All backwards effects become positive definite. The corresponding F_epsilon have their effects equal to those of R_epsilon and hence have bounded Choi traces. Extract a convergent subsequence as epsilon decreases to zero. Closedness of the EB cone, continuity of effects, and norm continuity give (6).

The same statement remains true after an output isometry, which preserves the effect and diamond norm. This exact effect bookkeeping is needed for the induction below; merely controlling each branch by an unrelated normalization would not suffice.

## 4. Approximate low-rank separators reduce the dimension

Let E_0,...,E_k be (d-1)-superpositive CP maps on M_d and let Phi_1,...,Phi_k be PPT CP maps. Suppose the positive composition

 W=E_k Phi_k E_(k-1) ... Phi_1 E_0

is trace nonincreasing. Then it has an EB CP approximation F with the same input effect and

 ||W-F||_diamond <= d delta_(d-1)(k).                    (7)

Expand each E_j in Kraus matrices K_(j,a) of rank at most r=d-1. Factor each chosen K_(j,a)=U_(j,a) B_(j,a), where U_(j,a):C^r->C^d is an isometry and B_(j,a):C^d->C^r; pad a rank-deficient factor with zero rows. Each branch has form

 W_a=Ad_(U_k) [A_k ... A_1] Ad_(B_0),
 A_j=Ad_(B_j) Phi_j Ad_(U_(j-1)).

Every A_j is a PPT CP map on M_r by filter invariance. Apply (6) branchwise and the output-isometry observation. This gives EB F_a with

 F_a*(I)=W_a*(I),
 ||W_a-F_a||_diamond <= delta_r(k)||W_a*(I)||_op.

Summing preserves complete positivity and EB. Crucially,

 sum_a ||W_a*(I)||_op
 <= sum_a tr W_a*(I)=tr W*(I)<=d.

Thus (7) follows, and F*(I)=W*(I). No individual branch is presumed TP and no exponential count of branches appears in the error bound.

## 5. The dimension recurrence

Take a word of

 n_0=(k+1)l+k

PPT channels on M_d. Divide it into k+1 length-l blocks separated by k unchanged PPT channels. Approximate each length-l block by the trace-nonincreasing, rank-(d-1) Kraus map from Section 2. Since every original factor and every approximation has diamond norm at most one, telescoping gives a trace-nonincreasing W with

 ||T-W||_diamond <= 2(k+1)c_d^(l/2).                     (8)

Apply Section 4 to obtain an EB F with F*(I)=W*(I) and error at most d delta_(d-1)(k). Finally choose a fixed density matrix tau and add the EB deficit channel

 R_def(X)=tr[(I-W*(I))X] tau.

The result E=F+R_def is EB and TP. Its added diamond norm obeys

 ||R_def||_diamond=||I-W*(I)||_op<=||T-W||_diamond.

Consequently

 delta_d((k+1)l+k)
 <=4(k+1)c_d^(l/2)+d delta_(d-1)(k).                    (9)

The base is delta_1(k)=0. Distances delta_d(n) are nonincreasing in n: approximate an initial subword and compose its EB CPTP approximation with the remaining channels. Thus (9) also bounds any longer word.

## 6. Solving the recurrence

For d=2 choose k=1 and l proportional to n. Equation (9) gives an exponential bound C_2 exp(-a_2 n).

Inductively suppose delta_(d-1)(k)<=C exp(-a k^(1/(d-2))). For large n choose positive integers

 l=floor(n^(1/(d-1))/4),
 k=floor(n^((d-2)/(d-1))/4).

Then (k+1)l+k<=n for all sufficiently large n. The first term in (9) is a polynomial factor times exp(-b n^(1/(d-1))); the second has the same stretched-exponential scale. Absorb the polynomial into a smaller positive exponent coefficient and enlarge the prefactor to cover the finitely many smaller n. This proves (1).

Applying Section 3 with B=I proves (2). All constants depend only on dimension because c_d and the lower-dimensional constants do.

## Limits and comparison boundary

Uniform approximation does not imply that a finite word is exactly EB: a sequence can approach the boundary without crossing it. The unrestricted exact finite-word problem remains open within this investigation. The separate exact theorem for bistochastic words remains stronger on its narrower class.

No probability distribution, ergodicity, common invariant state, or lower bound on the individual maps' positivity margins enters this proof. No efficient reconstruction of the exponentially large Kraus expansion is asserted.

See APPROXIMATION_PRIMARY_COMPARISON.md for the targeted primary comparison. The determinant filtering/factorization precursor is Tiersch–de Melo–Buchleitner, arXiv:0804.0208v3, Eqs. (5)–(7). The low-rank sandwich precursor is Christandl–Müller-Hermes–Wolf, arXiv:1807.01266v2, Lemma II.2. Their general exact rank-(d−1) Kraus claim is Conjecture II.1 and is not used here. Kennedy–Manor–Paulsen Theorem 3.5 concerns equal-map asymptotics; Ekblad Theorem 4 concerns almost-sure bistochastic ergodic asymptotics. The tentative new contribution is the effect-preserving, branch-summed quantitative synthesis for deterministic arbitrary nonunital words, not the older constituent mechanisms. The search does not certify novelty.
