# A preparation-entropy operation from a hemisphere condition

Let `(w_i,S_i)` be a finite weighted rank-one projective 2-design in C^d:
`w_i>0`, `sum w_i=1`, `S_i=|psi_i><psi_i|`, and

    sum w_i S_i=I/d,
    sum w_i S_i tensor S_i=(I+Swap)/[d(d+1)].          (1)

Repeated equal projectors can first be grouped by adding their weights.
For every unit vector v define the hemisphere functional

    H(v)=sum_i w_i (2<v,S_i v>-1)_+.                 (2)

The following gives a structural criterion for the full convex-order
mechanism, then a reusable entropy consequence. Generic Gibbs/
Brascamp--Lieb duality is established prior and is not claimed new here.

**Theorem A (sharp mechanism criterion).** For every integer d>=2, the
following two properties are equivalent:

    H(v)<=1/d^2 for every unit v;                    (H)

    for every Hermitian K and every convex real function phi,
    sum_i w_i phi(2Tr S_i K)
      <=d^(-2) sum_(j,l=1)^d phi(k_j+k_l),           (3)

where k_j are the eigenvalues of K. Thus(H) implies, for every
probability vector p on the supplied frame,

    D(sum p_i S_i || I/d) <= (1/2)D(p||w).           (4)

If w is uniform on n labels, this reads

    S(sum p_i S_i)>=H(p)/2+log d-(log n)/2.          (5)

The number-of-label correction is necessary: at p=w the output is I/d.
The uncorrected S>=H(p)/2 already fails at uniform weights if n>d^2.
Equation(4) is the appropriate weighted contract.

**Theorem B (cheap sufficient input).** A projective 2-design with
`|<psi_i,psi_j>|<=1/2` for distinct grouped frame points satisfies(H),
and therefore admits(4) for ALL preparation weights p. In particular:

* Every SIC in every dimension d>=3 admits S>=H(p)/2.
* Every complete MUB design in every prime-power dimension d>=4 admits
  (4), with uniform n=d(d+1) and the correction in(5).
* Convex mixtures of qualifying design measures, including arbitrary
  unitary rotations, continue to satisfy(H) and(4).

The constant1/2 is sharp for each SIC: a point mass has divergences
log d and log d^2. No optimality is asserted for every redundant design.
The qubit SIC also admits S>=H(p)/2, but does NOT satisfy(H) or(3).
A separate scalar proof below distinguishes entropy from convex order.

## 1. The only unpaid cut: a dimension-uniform matrix lemma

Let 0<=C<=dI, m=TrC in[0,d^2], and suppose

    Tr C^2 - m^2/d <= m(d^2-m)/[d(d+1)].             (6)

Let lambda_1>=...>=lambda_d be its eigenvalues, and write
`Lambda_k=sum_(j<=k)lambda_j`. If C and dI-C satisfy

    2lambda_max(C)<=m+1,
    2lambda_max(dI-C)<=d^2-m+1,                     (7)

then there is a real dxd matrix X with entries in[0,1], whose row AND
column sums are the lambda_j. It can be chosen symmetric.

The ordinary bounded transportation criterion is

    Lambda_k+Lambda_l<=m+kl,     0<=k,l<=d.          (8)

To see this directly, form a network with source-to-row capacities
lambda_i, every row-to-column capacity1, and column-to-sink capacities
lambda_j. Every cut has capacity at least m exactly when
`sum_I lambda+sum_J lambda<=m+|I||J|` for all row and column subsets.
For fixed cardinalities the maximum is Lambda_k+Lambda_l. Thus(8)
is necessary and sufficient for a flow of mass m. Symmetrize X by
averaging with its transpose. No new flow algorithm is claimed.

The cases k0,l0 follow from nonnegativity. If k=d or l=d, use C<=dI.
Assume `1<=l<=k<=d-1`. Replacing C by dI-C transforms a cut with
k+l>d into the equivalent cut `(d-l,d-k)` for the complement, since

    Lambda'_(d-l)=d(d-l)-m+Lambda_l,
    Lambda'_(d-k)=d(d-k)-m+Lambda_k.

The complement has trace d^2-m and the same centered squared norm,
so it also satisfies(6). Hence assume k+l<=d. The sole exceptional
pair is k=l=1, paid by(7).

For every other pair, put

    a=d-k-l>=0, b=dkl,
    V=d(k+3l)-(k+l)^2>0.

Centered Hilbert--Schmidt Cauchy--Schwarz, with weights
`(2 repeated l, 1 repeated k-l, 0 repeated d-k)`, gives

    Lambda_k+Lambda_l
      <=m(k+l)/d+sqrt[m(d^2-m)V/(d^2(d+1))].       (9)

The nonnegative distance from the first term to m+kl is `(am+b)/d`.
After squaring, the desired bound is P(m)>=0, where

    P(m)=(d+1)(am+b)^2-Vm(d^2-m).

Its leading coefficient is positive, and its discriminant is

    disc P = d^2 V [d^2 V-4(d+1)kl(d-k)(d-l)].     (10)

Here is a dimension-uniform proof that the bracket is nonpositive for
each nonexceptional integer pair. The ratio of d^2 V to
`kl(d-k)(d-l)` is exactly

    d^2/[l(d-l)] + d^2/[k(d-k)] + 2d^2/[k(d-l)].   (11)

If l1 and k>=2, all three terms sum to at most
`3d^2/(d-1)<=4(d+1)` for d>=2. If l>=2, then d>=4,
`2<=l<=k<=d-2`, and each of `l(d-l),k(d-k),k(d-l)` is at least
`2(d-2)`. Thus(11)<=`2d^2/(d-2)<=4(d+1)` for d>=4, the last inequality
being `d^2-2d-4>=0`. Therefore disc P<=0 and P>=0 for all real m,
which proves(8). When d2 there are no nonexceptional interior pairs;
(7) alone completes the proof. No scan over dimensions is a premise.

## 2. Projective 2-designs pay the moment hypothesis

For arbitrary scalars f_i in[0,1], set

    alpha=sum_i w_i f_i, m=d^2 alpha,
    C=d^2 sum_i w_i f_i S_i.

The first moment in(1) gives 0<=C<=dI. Put C0=C-mI/d. From the second
moment, for every traceless Hermitian Y,

    sum_i w_i (Tr S_i Y)^2=Tr Y^2/[d(d+1)].

Consequently Cauchy--Schwarz gives

    Tr C0^2
      =d^2 sum_i w_i(f_i-alpha)Tr S_i C0
      <=d^2 sqrt[Var_w(f) Tr C0^2/(d(d+1))].

Since Var_w(f)<=alpha(1-alpha), cancellation yields(6). The same
argument applies to the complement obtained by replacing f by1-f.
Under(H), for every unit v,

    2<v,Cv>-m
       =d^2 sum_i w_i f_i(2<v,S_i v>-1)
       <=d^2 H(v)<=1.

Thus(7) is paid for C and its complement, and the matrix lemma supplies
a bounded transportation matrix for every f, including fractional f.

## 3. Transportation to full convex order, and necessity

For fixed K, the trace rearrangement inequality gives
`2Tr KC<=2sum_j k_j lambda_j`. If X is the symmetric bounded matrix,
the latter equals `sum_(j,l)X_jl(k_j+k_l)`, with total mass m. For every
real threshold t,

    d^2 sum_i w_i(2Tr S_i K-t)_+
       =max_(0<=f<=1)[2Tr KC-mt]
       <=sum_(j,l)(k_j+k_l-t)_+.                  (12)

Both distributions have mean `2TrK/d`, so these hinge inequalities
imply(3), by the integral representation of a convex function on a
compact interval. Conversely apply(3) to K=|v><v| and phi(x)=(x-1)_+.
The right side is1/d^2, giving exactly(H). This proves Theorem A.

Taking phi=exp gives

    sum_i w_i exp(2Tr S_i K)<=(Tr expK/d)^2.        (13)

The weighted classical Gibbs formula yields
`D(p||w)>=2Tr MK-log sum_i w_i exp(2Tr S_i K)`.
Use(13) and take the quantum Gibbs supremum over K to get(4), including
singular outputs by approximation. This is the established general-
channel Brascamp--Lieb/SDPI duality. The acquired ingredient is(13),
paid by the structural condition(H), not a new duality theorem.

## 4. Why incoherent designs need no hemisphere optimizer

Every atom of a projective 2-design has weight at most1/d^2. Fix S_j
and use(1) to compute

    sum_i w_i [Tr(S_j S_i)-1/(d+1)]^2=1/(d+1)^2.

The jth nonnegative term is `w_j d^2/(d+1)^2`, proving the bound.

For arbitrary f put beta_i=d^2 w_i f_i<=1. The nonzero eigenvalues of
C are those of the weighted Gram matrix G, with diagonal beta_i and
off-diagonal absolute values at most `(1/2)sqrt(beta_i beta_j)`.
For every unit vector x,

    x*Gx <= (1/2)sum_i beta_i|x_i|^2
             +(1/2)[sum_i sqrt(beta_i)|x_i|]^2
           <=(max_i beta_i+m)/2 <=(m+1)/2.

This pays(7) for every f, and hence(H). It is a weighted Gershgorin/
variational estimate; no PSD comparison based solely on entrywise
absolute values is asserted.

For a SIC, n=d^2 and `Tr S_i S_j=1/(d+1)` off the diagonal. Its
tight-frame and 2-design identities follow from the standard SIC frame
identities, or directly from the Hilbert--Schmidt Gram matrix. Its
coherence is `1/sqrt(d+1)<=1/2` for d>=3. A complete MUB design has
coherence1/sqrt d and is a projective 2-design, so d>=4 qualifies.

Both(1) and(H) are preserved under convex mixtures of design measures,
and under common unitary conjugation. This additionally receives finite
unions of rotated qualifying designs, even if cross-design coherence
exceeds1/2. For a general finite design, the exact spectral expression is

    sup_v d^2 H(v)
      =max_T [2d^2 lambda_max(sum_(i in T)w_i S_i)
                                  -d^2 sum_(i in T)w_i].

Checking all subsets is an honest exponential qualification operation
when no structural proof is known. The incoherence certificate avoids
it with pairwise overlap checks.

## 5. Qubit SIC: entropy survives although convex order fails

For a qubit SIC put s=sum p_i^2 and t=sqrt[(4s-1)/3] in[0,1]. Its
output spectrum is `((1+t)/2,(1-t)/2)`. The credited sharp entropy/purity
upper envelope (Harremoes--Topsoe2001) bounds the input entropy by that
of `((1+3t)/4,(1-t)/4,(1-t)/4,(1-t)/4)`. Let g(t) be twice the binary
output entropy minus this input upper envelope. Then

    g(0)=g(1)=0, g'(0)=0,
    g''(t)=(1-3t)/[(1-t)(1+t)(1+3t)].              (14)

Hence g' first increases then decreases, crosses0 once after1/3, and
tends to minus infinity. Thus g(t)>0 for0<t<1, proving the qubit SIC
entropy inequality. Yet for v halfway between two tetrahedral Bloch
vectors the four overlaps are `(1+1/sqrt3)/2` twice and
`(1-1/sqrt3)/2` twice. Thus H(v)=1/(2sqrt3)>1/4, refuting(H)/(3).
This separates the mechanism from entropy truth already in dimension2.

## 6. SIC equalities and sharpness

For d>=3 the score distributions' centered second moments differ by
`2(d-1)Tr K0^2/[d(d+1)]` for traceless K0. Therefore(13) is strict for
nonscalar K: the distributions cannot coincide, and exp is strictly
convex. If M=sum p_i S_i is faithful, K=logM proves strict entropy
unless M=I/d; the SIC purity identity then forces p uniform.

For singular M of rank r<d, let J contain ALL frame labels whose
projectors lie in its range, including zero-weight preparation labels.
If m=|J|, subset trace/purity identities and rank at most r give

    m<=rd/(d+1-r)<r^2,      when 1<r<d.             (15)

Take K_R on the range, shift its smallest eigenvalue to0, and extend
it by -t on the orthogonal complement. Let t tend to infinity in the
proved score-majorization partial sums. The m finite scores from J
are weakly majorized by the r^2 pair sums from K_R, after padding the
scores with r^2-m zeros. Indeed the first m sums follow by the limit,
and later sums follow from nonnegative pair scores. Exponentiation gives

    sum_(i in J) exp(2Tr S_i K_R)+(r^2-m)
        <=(Tr_R expK_R)^2.

Undoing the scalar shift preserves a strictly positive missing term.
Choosing K_R=log(M|R), and then the classical Gibbs formula on J, proves
strict entropy. Rank1 forces a point mass. The qubit proof likewise has
only uniform and point-mass equalities. Thus every SIC in every d>=2
has equality exactly at uniform weights and point masses.

## 7. Scope and executable outputs

The theorem receives all preparation weights after frame moments and
incoherence are qualified. An explicit weighted48-state qutrit 2-design
violates(H), so the hypothesis is not automatic from design moments.
`DESIGN_OBSTRUCTION.md` supplies the exact construction and obstruction.
It does NOT assert an entropy counterexample: a mechanism obstruction
is not the failure of(4). The unrestricted design constant is outside
the present theorem.

`compile_frames.py` qualifies an exact d8 Hoggar SIC and an exact d4
complete MUB design. It evaluates an actual64-weight Hoggar source by
rational characteristic-polynomial/Sturm/log certificates, and compares
the sharp scalar entropy/purity relaxation. Costs and ordinary primary
comparisons are recorded separately. No arbitrary SIC existence,
quantum-memory extension, WH_d/CLR theorem, physical implementation,
or civilization-scale leverage follows. Historical priority is UNKNOWN.
