# Three exact obstructions to a causal circuit extension of the replacement-form method

This note concerns a proposed extension, not a flaw in the governing ETH paper. The source is the supplied *The Exponential Time Hypothesis is False*, revised 25 October 2026: Sections 3.1–3.5 (factor-product counting), Lemmas 4.1–4.3 (the auxiliary matrix and replacement rows), Lemmas 4.5–4.8 (balanced placement and costs). The source explicitly sums over independent Boolean coordinates; its occurrence copies are repeated values, not additional independent variables.

## 1. A causal version of the auxiliary correction needs nearly full measurement rank

Let `B=([r]×[r])^Q`, `D=r^(2Q)`, with `u=(a_u,d_u)` as in source Section 4.1. For labels u,v put

\[
E_{u,v}=\{t\in[Q]:a_v(t)\ne d_u(t)\},\qquad m_u=|E_{u,u}|.
\]

Suppose a rational D×D matrix M and a measurement matrix C satisfy the exact conditions used in source Lemmas 4.1–4.3:

\[
M\xi=\xi\quad(\xi\in\ker C),\qquad
M_{uv}\ne0\Longrightarrow |E_{u,v}|\le R-1.
\]

**Theorem 1.** If M is triangular in any ordering of these coordinates (a simultaneous permutation of rows and columns), then

\[
\boxed{\operatorname{rank}C\ge\operatorname{rank}(I-M)
\ge\#\{u:m_u\ge R\}.}
\]

**Proof.** The kernel inclusion implies that every row of I−M lies in the row space of C, giving the first inequality. For every u with m_u≥R, the support condition forces M_uu=0, so (I−M)_uu=1. The principal submatrix on those indices is triangular with all diagonal entries equal to one. It is nonsingular, proving the second inequality. The argument is unchanged by the common permutation. ∎

For a uniform label u, each event a_u(t)≠d_u(t) has probability 1−1/r, independently across t. Hence

\[
D^{-1}\#\{u:m_u\ge R\}
=\Pr\{\operatorname{Bin}(Q,1-1/r)\ge R\}.
\]

For r≥2 and R≤Q/4, Hoeffding's inequality gives

\[
\operatorname{rank}C\ge D\bigl(1-e^{-Q/8}\bigr).
\]

Thus the low-degree regime R/Q→0 cannot retain a vanishing measurement fraction after imposing triangular support on this auxiliary M. The original construction escapes this conclusion by using nontriangular swap matrices. This does not exclude every imaginable causal compiler; it excludes causalizing this particular low-rank-correction construction by imposing a temporal triangular order.

### Executed exact fixture

For r=2, Q=3, R=2, choose the source interpolation interval I={0,1}, with f(z)=1−2z. Let Π_s exchange the two entries in position s, V=Π_1Π_2Π_3 and W=(3I−Π_1−Π_2−Π_3)/2. Then

\[
M=V(I-2W)=V(-2I+\Pi_1+\Pi_2+\Pi_3).
\]

Exact rational Gaussian elimination in the accompanying program gives:

- D=64.
- rank(I−M)=10.
- All nonzero entries satisfy |E_uv|≤1.
- Exactly 32 diagonal labels have m_u≥2.
- Every triangular admissible M needs rank(I−M)≥32.
- The diagonal matrix with entry zero on these 32 labels and one elsewhere attains rank 32, so this restricted lower bound is sharp.

The fixture is outside the asymptotic parameter choice, but is an exact finite instance of the support/rank obstruction.

## 2. Normalized causal gate kernels can create arbitrarily many effective random inputs

For a Boolean gate state y and a rational putative output probability p, define

\[
K(y;p)=yp+(1-y)(1-p).
\]

The identity K(0;p)+K(1;p)=1 holds for every rational p, including signed values. It is tempting to use this normalization to integrate out all internal circuit states with cost controlled only by the original independent inputs. The following exact reduction shows why normalization is insufficient.

Let G:{0,1}^m→{0,1} be an arbitrary Boolean circuit. The original circuit has **one** independent input x. It first makes m copies y_i=x and then evaluates G(y). Its accepting-input count is only G(0^m)+G(1^m).

Deform each copy gate to the normalized causal kernel

\[
K_i(y_i;x,T)=K(y_i;a(T)x),\qquad a(T)=1-T/2.
\]

All later gates remain deterministic Boolean gates. Their unique consistent states can be summed out, giving the exact accepted mass

\[
H(T)=\sum_{x\in\{0,1\}}\sum_{y\in\{0,1\}^m}
G(y)\prod_{i=1}^mK(y_i;a(T)x).
\]

**Theorem 2.** This family is causal and every gate kernel is normalized, but

\[
H(0)=G(0^m)+G(1^m),\qquad
\boxed{H(1)=G(0^m)+2^{-m}\#G.}
\]

**Proof.** At T=0, a=1, so the kernels enforce y_i=x. At T=1, a=1/2. For x=0 they enforce y=0^m. For x=1 every y has weight 2^−m. Summing gives the identities. ∎

Consequently an algorithm evaluating arbitrary normalized causal kernel networks with polynomial description cost and an exponential factor depending only on the number of original independent inputs would exactly count arbitrary Boolean circuits, even in this family with original input count one. The deformations have manufactured m independent Bernoulli choices among the internal states. This is an explicit complexity transfer, not an unconditional lower bound for deterministic circuit counting.

Normalization eliminates an unobserved terminal gate, but output conditioning changes its mass. In particular,

\[
\sum_y K(y;p)=1,\qquad \sum_y yK(y;p)=p.
\]

A single output indicator—or a measurement fixing that output—therefore defeats the step that discards it by normalization. Fanout creates joint moments in its ancestors rather than a closed list of singleton expectations.

There is also an unconditional degree obstruction. Taking G(y)=∏_i y_i gives

\[
H(T)=(1-T/2)^m,
\]

whose degree is m although the original input count is one. In the paper's Taylor/Hermite routine, the degree budget now sees the internal branching, and cannot be replaced by O(n) merely from causal normalization.

The executed program checks 48 reproducible fan-in-two Boolean circuits with m=2,…,9, using exact fractions. All formulas for H(0), H(1), and H(2)=2G(0^m) hold. It also checks normalization at T=0,1,2,3,4, including negative transition weights. This is an identity verification; it is not a speed benchmark.

## 3. Boolean degree resets are incompatible with a nontrivial low-degree interpolation path

A second attempted repair keeps intermediate states Boolean at all interpolation points, so the quotient identity y²=y can be used without a growing formal degree.

**Lemma 3 (affine Boolean maps over characteristic zero).** If

\[
L(x)=b+\sum_{i=1}^na_ix_i\in\mathbb Q[x]
\]

belongs to {0,1} for every x∈{0,1}^n, then L is one of 0,1,x_i,1−x_i.

**Proof.** Reduce L²−L in the Boolean quotient x_i²=x_i. Its constant coefficient is b²−b, its x_i coefficient is a_i²+(2b−1)a_i, and its x_ix_j coefficient is 2a_ia_j. The polynomial vanishes at every Boolean point, and multilinear Boolean evaluation is injective, so all these coefficients vanish. Thus b∈{0,1}, at most one a_i is nonzero, and its value is 1−2b. ∎

The interpolation obstruction is stronger and does not require affine dependence on x.

**Theorem 4 (Boolean-preserving path rigidity).** Let P(T,x) be a polynomial whose T-degree is at most R. Suppose P(0,x) is Boolean for every Boolean x, and P(t_j,x) is Boolean for all Boolean x at Q distinct nonzero points t_j. If Q+1>2R, then for every Boolean x,

\[
P(T,x)=P(0,x)\quad\text{as a polynomial in }T.
\]

**Proof.** Fix x. The scalar polynomial p(T)=P(T,x) has degree at most R. The polynomial p(T)(p(T)−1), of degree at most 2R, vanishes at Q+1 distinct points. It is identically zero. Since Q[T] is an integral domain, p is identically zero or identically one; its value is fixed by T=0. ∎

If the replacement rows are affine in x and restore x_i at zero, this yields P(T,x)=x_i identically. Thus any attempt to preserve Boolean semantics at all the easy evaluation points, while keeping the paper's favorable ratio R/Q→0, freezes the deformation. The non-Boolean easy points are essential to the original construction.

These statements identify three different costs that a successful extension must overcome: noncausal dependence, additional branching among internal states, and Boolean-to-rational degree growth. None implies that a subexponential algorithm for arbitrary original-input circuits is impossible.

## 4. Low-degree copy deformations cannot confine internal branching to a few nodes

A possible repair of Theorem 2 is to enumerate only the gates that have non-Boolean transition probabilities at an evaluation point. The following elementary count limits that strategy.

**Proposition 5.** Let p_1,…,p_m∈Q[T] be nonconstant polynomials of degree at most R with p_i(0)=1. At Q distinct nonzero nodes t_1,…,t_Q, there is a node where at least

\[
m\left(1-\frac{2R-1}{Q}\right)
\]

of the values p_i(t_j) lie outside {0,1} (round the lower bound upward to an integer).

**Proof.** The nonzero polynomial p_i(p_i−1) has degree at most 2R and already has a root at zero. Therefore p_i is Boolean at at most 2R−1 of the specified nonzero nodes. Sum these upper bounds over i and average over nodes. ∎

This proposition concerns copy-gate deformations sharing a reachable witness input x=1, exactly as in Theorem 2. In the favorable interpolation regime R/Q→0, a node must have (1−o(1))m potentially branching copy gates. This remains an obstruction to the stated repair rather than a lower bound against every possible representation compiler.
