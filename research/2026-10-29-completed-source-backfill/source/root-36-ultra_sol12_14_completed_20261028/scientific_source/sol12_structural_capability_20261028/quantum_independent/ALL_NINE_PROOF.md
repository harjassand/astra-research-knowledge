# All qutrit SIC preparation weights: a majorization receiver

Let S_1,...,S_9 be rank-one qutrit projectors with
Tr(S_i S_j)=1/4 for i!=j. For ANY probability vector p on all nine labels,
put M_p=sum p_i S_i. Then

    2 S(M_p)>=H(p),                                      (1)

with equality exactly when p is a point mass or the uniform nine-vector.
The entropy is natural-log entropy. This is a statement about PREPARATION
weights. No SIC measurement-output distribution is substituted for p.
It uses no Hesse-specific phases. The proof uses ordinary Ky Fan/trace
inequalities, majorization and the Gibbs variational formula; historical
priority of this specialized conclusion is UNKNOWN.

## 1. A nine-vector majorization inequality

For Hermitian K with eigenvalues k1>=k2>=k3, define

    a_i=2Tr(S_i K),             b=(k_j+k_l)_(j,l=1,...,3).

We prove a is majorized by b. First sum_i S_i=3I: its trace is9 and
the trace of its square is9+72/4=27, the minimum possible in dimension3.
Thus sum a=sum b=6TrK.

Subtract k2 I from K; both vectors shift by the same scalar. Write its
eigenvalues as (x,0,-y), x,y>=0. The four largest partial sums of b are

    2x, 3x, 4x, 4x+max(0,x-y).                           (2)

For a subset T of m SIC labels, C_T=sum_(i in T)S_i has

    Tr C_T=m, Tr C_T^2=m(m+3)/4.

The trace rearrangement inequality gives Tr(K C_T)<=x L-y l, where
L and l are its largest and smallest eigenvalues. For m1, L1,l0.
For m2, its spectrum is(3/2,1/2,0). For m3, trace3,purity9/2 imply
L<=2,l>=0. Thus twice the trace is bounded by the first three quantities
in(2), for EVERY subset, hence for the largest score partial sums.

For m4, trace4 and purity7 give the useful universal bounds

    L<5/2,             L-l<2,             l>0.            (3)

For completeness, each eigenvalue lies between(4-sqrt10)/3 and
(4+sqrt10)/3 by Cauchy-Schwarz on the other two eigenvalues. Also
(L-l)^2<=2[7-16/3]=10/3. Rational bounds usable without radicals are

    L<=12/5, l>=4/15, L-l<=11/6.

If x<=y, then2Tr(K C_T)<=2x(L-l)<=4x, strictly for nonzero K;
the x0,y>0 endpoint is strict because l>0. If x>=y, compare with5x-y.
The difference is at least

    x(5-2L)+y(2l-1).

As a function of y/x in[0,1], its endpoint coefficients are5-2L>0 and
4-2(L-l)>0. This proves the fourth partial sum, strictly whenever K
is nonscalar. The displayed rational bounds even give fourth gap
at least(k1-k3)/6.

Apply the same first-four bounds to -K and use total-sum equality.
Complementation supplies the fifth through eighth partial sums. This
proves a is majorized by b, with a strict fourth partial sum for every
nonscalar K. In particular

    sum_i exp[2Tr(S_i K)] <= (Tr expK)^2,                  (4)

strictly for nonscalar K. This is ordinary convex-order reasoning:
majorization bounds sum_i(a_i-t)_+ by sum_i(b_i-t)_+ at every t.
Integrate these hinges against the positive second derivative of exp;
equal constants and linear sums give(4). Strictness follows unless
the two vectors are permutations, excluded by the fourth partial sum.

## 2. Entropy and all equality cases

The classical Gibbs inequality gives, for every finite Hermitian K,

    H(p)+2Tr(M_p K) <= log sum_i exp[2Tr(S_i K)]
                   <= 2log Tr expK.

Taking the quantum Gibbs infimum over K proves(1), including singular
M_p by approximation. If M_p is faithful and nonscalar, choose K=logM_p;
the second inequality is strict. If M_p=I/3, the first inequality is
strict unless p is uniform. Uniform p does give equality.

It remains to classify singular outputs without an unproved limiting
strictness argument. If M_p has rank at most2, every positively weighted
S_i lies in its range. Four such states would have sum C with rank<=2,
forcing Tr C^2>=Tr(C)^2/2=8, contradicting purity7. Thus support size
is at most3. Rank1 forces a point mass, which has equality.

For rank2 let R be the output support, m=2 or3 the number of active
labels, and K_R any finite Hermitian matrix on R. Shift its
smallest eigenvalue to0, so its eigenvalues are(d,0), d>=0. The m scores
2Tr(S_i K_R), padded with4-m zeros, are weakly majorized by

    (2d,d,d,0).

Their first two partial sums are at most2d and3d, from the one- and
two-projector spectra. Their total is at most3d: for m3 the sum is
(3/2)I_R, since its trace3,purity9/2 attain the rank2 minimum; for m2
the largest eigenvalue is3/2. The third/fourth upper target sums are4d.
Increasing convex exp therefore gives, undoing the scalar shift,

    sum_active exp[2Tr(S_i K_R)]
       <=(Tr_R expK_R)^2-(4-m)exp(2lambda_min(K_R)).

Choose K_R=log(M_p|R); the right side is strictly less than1.
The classical Gibbs inequality on the active labels now proves
H(p)<2S(M_p). This completes the equality classification independently
of a numerical support-five receiver.

## 3. Sharp relative-entropy contraction

The same theorem is exactly

    D(M_p||I3/3) <= (1/2)D(p||u9).

The constant1/2 is sharp: a point mass has input divergence log9 and
pure output divergence log3. This is a reference-uniform SIC PREPARATION
channel statement, not a complete quantum-side-information SDPI.

For correlated classical label strings with PRODUCT SIC preparations,
the chain rule and ordinary data processing give

    S(B^n)=sum_i S(B_i|B_<i)
          >=sum_i S(B_i|X_<i)>=H(X^n)/2.

Indeed B_<i is a channel of X_<i, and conditioned on the earlier labels
the single-site mixture obeys(1). This covers arbitrary classical
correlations of product preparation labels, not coherent quantum inputs
or arbitrary entangled code states.

## 4. Bell sources and a whole noncommuting-bath closure

Use the exact channel identity independently reviewed in
`../quantum_composition/SIC_SPARSE_PROOF.md`. For any nonnegative nine
weights x, let X=sum x_i|Phi_i><Phi_i| and T=sum x_i. If T>0,

    Delta(X)=T[2S(M_(x/T))-H(x/T)]>=0.

The scalar white addition X+tI9 has the same Bell eigenvectors and
nonnegative weights x_i+t. Therefore the ENTIRE curve Delta(X+tI)>=0
is paid, without a small positive-ray radius or a spectral condition bound.
The inherited positive common-bath identity then proves

    Delta(X tensor U+I9 tensor V)>=0

for arbitrary finite PSD U,V, including noncommuting and singular ones.
The spectral-mixture bath identity remains an inherited theorem, not
rediscovered here. This is one common ordered bath ray, not arbitrary
independent operator-valued weights on the nine Bell labels.

For bath dimension d and nonzero source Z, Tr_reference Z=(TrZ/3)I3,
so scalar normalization already gives a TP Choi state. Its antisymmetric
extension has reference dimension3d and total dimension27d, with
CMI-log3=Delta(Z)/TrZ>=0. The same product-label argument also covers
classically correlated product-Weyl-Bell mixtures with product WH maps.
No unrestricted WH3/CLR inequality, physical experiment or general
composition theorem outside these declared families follows.

Majorization, trace rearrangement, Gibbs duality and the chain rule are
established tools. The finite support-five purity receiver is an equally
informed ordinary comparator; its failure beyond five is a loss of that
scalar relaxation, not a quantum counterexample. The full-frame subset
spectra supply the additional structure used by this proof. Related SIC
measurement-entropy literature concerns different probabilities. Historical
priority remains UNKNOWN after the bounded primary screen recorded here.

The entropy/trace-exponential equivalence is explicitly covered by Berta,
Sutter and Walter, *Quantum Brascamp--Lieb Dualities* (2023), Corollary2.5,
with one SIC preparation map and weight q1=2. Their Corollary3.10 covers
the relative-entropy contraction formulation. Thus dualizing this problem
and interpreting the result as an SDPI are credited established operations;
the acquired premise here is the all-nine majorization inequality itself.
See `PRIMARY_SCOPE.md` for the bounded prior screen and `CAPABILITY.md`
for the paid constructive receiver and its limits.
