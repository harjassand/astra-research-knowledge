# Complete construction of the quadratic certificate

## Result

The answer is **yes**, for every dimension and every family in the question.

Put \(n=r+1\), choose any strictly positive generator \(k\) of \(\ker N\), and set
\[
a_i=k_i^2,\qquad A=\sum_{i=1}^n a_i.
\]
The following construction always works.

* If \(a_m\ge A-a_m\) for some index \(m\), take \(\theta_m=1\) and \(\theta_i=0\) for \(i\ne m\).
* Otherwise all \(a_i<A-a_i\). Choose an index \(m\) attaining \(\max_i a_i\). The scalar construction in Section 4 produces strictly positive weights with sum one and a number \(\tau>0\) such that
  \[
  \theta_i(1-\theta_i)=\tau a_i\quad\text{for all }i.
  \]

Both cases imply
\[
\sum_i\theta_i(v_i\cdot z)^2\le \sum_i(v_i\cdot z)_-^2
\qquad(z\in\mathbb R^r).
\]
No equality of the coefficients or lengths is assumed. The first case explicitly permits zero weights and a singular certificate matrix.

## 1. Exact reduction to a hyperplane

The map \(z\mapsto x=N^Tz\) is a linear bijection from \(\mathbb R^r\) onto
\[
H=\{x\in\mathbb R^n:k\cdot x=0\}.
\]
Indeed, it is injective because \(N\) has rank \(r\), and its image is the orthogonal complement of \(\ker N=\operatorname{span}\{k\}\). Thus it suffices, and is necessary, to prove
\[
\sum_i\theta_i x_i^2\le\sum_i(x_i)_-^2\qquad(x\in H). \tag{1}
\]
Every nonzero vector in \(H\) has at least one positive and one negative coordinate, because every \(k_i\) is strictly positive.

## 2. The dominant-coordinate case

Suppose \(a_m\ge\sum_{i\ne m}a_i\), and take \(\theta=e_m\). We must show \(x_m^2\le\sum_i(x_i)_-^2\).

If \(x_m\le0\), this is immediate. If \(x_m>0\), let \(M=\{i:x_i<0\}\). Since \(k\cdot x=0\),
\[
k_mx_m\le\sum_{i\in M}k_i(-x_i).
\]
Cauchy–Schwarz gives
\[
a_mx_m^2
\le\left(\sum_{i\in M}a_i\right)\left(\sum_{i\in M}x_i^2\right)
\le\left(\sum_{i\ne m}a_i\right)\sum_i(x_i)_-^2
\le a_m\sum_i(x_i)_-^2.
\]
Division by \(a_m>0\) proves (1). This includes the boundary \(a_m=\sum_{i\ne m}a_i\).

When \(n=2\), at least one coordinate is dominant, so this already resolves every \(r=1\) instance.

## 3. An interior certificate lemma

**Lemma.** Suppose \(0<\theta_i<1\), \(\sum_i\theta_i=1\), and for some \(T>0\),
\[
a_i=T\theta_i(1-\theta_i)\qquad(i=1,\ldots,n). \tag{2}
\]
Then (1) holds for every \(x\in H\).

**Proof.** Set \(q_i=k_ix_i\). Then \(\sum_iq_i=0\), and \(q_i\) has the same sign as \(x_i\). For \(x\ne0\), put
\[
P=\{i:q_i>0\},\qquad M=\{i:q_i<0\},\qquad
b=\sum_{i\in M}\theta_i>0,
\]
and
\[
s=\sum_{i\in P}q_i=\sum_{i\in M}(-q_i)>0.
\]
Using (2), the difference between the right and left sides of (1) is exactly
\[
\begin{aligned}
\sum_i(x_i)_-^2-\sum_i\theta_ix_i^2
&=\sum_{i\in M}(1-\theta_i)x_i^2-\sum_{i\in P}\theta_ix_i^2\\
&=\frac1T\left(
\sum_{i\in M}\frac{q_i^2}{\theta_i}
-\sum_{i\in P}\frac{q_i^2}{1-\theta_i}
\right). \tag{3}
\end{aligned}
\]
Weighted Cauchy–Schwarz yields
\[
\sum_{i\in M}\frac{q_i^2}{\theta_i}\ge\frac{s^2}{b}. \tag{4}
\]
For every \(j\in P\), all indices in \(M\) differ from \(j\), so
\[
1-\theta_j=\sum_{i\ne j}\theta_i\ge b.
\]
Consequently,
\[
\sum_{j\in P}\frac{q_j^2}{1-\theta_j}
\le\frac1b\sum_{j\in P}q_j^2
\le\frac1b\left(\sum_{j\in P}q_j\right)^2
=\frac{s^2}{b}. \tag{5}
\]
The second inequality uses \(q_j>0\). Equations (3)–(5) give the claim. At \(x=0\), (1) is equality. \(\square\)

## 4. Construction in every nondominant case

Assume now
\[
a_m=\max_i a_i<\sum_{i\ne m}a_i. \tag{6}
\]
Define
\[
t_* =\frac1{4a_m},\qquad
h_i(t)=\frac{1-\sqrt{1-4ta_i}}2\quad(0\le t\le t_*),
\]
and \(H(t)=\sum_i h_i(t)\). These functions are real and continuous on the whole interval. Each \(h_i\) is strictly increasing, vanishes at zero, and satisfies
\[
h_i(t)(1-h_i(t))=ta_i,\qquad 0\le h_i(t)\le\tfrac12. \tag{7}
\]
In particular, \(h_m(t_*)=1/2\).

### Case 4a: \(H(t_*)\ge1\)

Since \(H(0)=0\), continuity gives a \(\tau\in(0,t_*]\) with \(H(\tau)=1\). Take
\[
\theta_i=h_i(\tau)\quad\text{for all }i.
\]
These weights are strictly positive, sum to one, and satisfy
\(\theta_i(1-\theta_i)=\tau a_i\). Apply the lemma with \(T=1/\tau\).

This is a complete scalar construction: the root is unique because \(H\) is strictly increasing, and ordinary bisection on \([0,t_*]\) converges to it.

### Case 4b: \(H(t_*)<1\)

Define
\[
F(t)=\sum_{i\ne m}h_i(t)-h_m(t).
\]
At the upper endpoint,
\[
F(t_*)=H(t_*)-2h_m(t_*)=H(t_*)-1<0. \tag{8}
\]
Rationalization gives
\[
\frac{h_i(t)}t=\frac{2a_i}{1+\sqrt{1-4ta_i}}\longrightarrow a_i
\quad\text{as }t\downarrow0.
\]
Therefore (6) implies
\[
\lim_{t\downarrow0}\frac{F(t)}t
=\sum_{i\ne m}a_i-a_m>0. \tag{9}
\]
In particular, \(F(t)>0\) for all sufficiently small positive \(t\). Together with (8), continuity gives a **positive** root \(\tau\in(0,t_*)\) of \(F\). The root at zero is not used.

Set
\[
\theta_m=1-h_m(\tau),\qquad
\theta_i=h_i(\tau)\quad(i\ne m).
\]
All weights lie strictly between zero and one, and
\[
\sum_i\theta_i=1-h_m(\tau)+\sum_{i\ne m}h_i(\tau)=1+F(\tau)=1.
\]
Equation (7) is unchanged when \(h_m\) is replaced by \(1-h_m\). Thus again
\[
\theta_i(1-\theta_i)=\tau a_i
\]
for every index, and the lemma applies.

For an explicit convergent construction, search the sequence \(t_*/2,t_*/4,t_*/8,\ldots\) until finding \(\varepsilon\) with \(F(\varepsilon)>0\). Equation (9) proves that this search terminates. Bisection between \(\varepsilon\) and \(t_*\), maintaining opposite signs, converges to a positive root. No monotonicity or uniqueness of \(F\) is asserted or needed.

Cases 2, 4a and 4b exhaust all positive vectors \(a\). This proves the theorem.

## 5. Why the reformulation is exact

The construction above is sufficient on its own. The following characterization also shows that the interior algebraic representation does not merely guess a sufficient condition.

Let \(\theta\) be a probability vector with every \(\theta_i<1\), and define
\[
B_j=\sum_{i\ne j}\frac{a_i}{1-\theta_i},\qquad
T=\sum_i\frac{a_i}{1-\theta_i}.
\]
If (1) holds, restrict to vectors with \(x_j=1\) and \(x_i\le0\) for \(i\ne j\). The hyperplane condition is
\[
\sum_{i\ne j}k_i(-x_i)=k_j.
\]
The exact minimum of \(\sum_{i\ne j}(1-\theta_i)x_i^2\) under this constraint is \(a_j/B_j\). Cauchy–Schwarz gives this value, and it is attained by
\[
-x_i=\frac{k_jk_i}{B_j(1-\theta_i)}\quad(i\ne j),
\]
which has the required signs. Consequently,
\[
\theta_jB_j\le a_j\qquad\text{for every }j. \tag{10}
\]
Writing \(b_j=a_j/(1-\theta_j)\), relation (10) becomes
\[
T\theta_j\le b_j.
\]
Both sides sum to \(T\). Every inequality must therefore be equality, giving
\[
a_j=T\theta_j(1-\theta_j)\qquad\text{for every }j. \tag{11}
\]
Since \(a_j>0\), this also forces every \(\theta_j>0\). Conversely, (11) implies (1) by the interior certificate lemma. Thus among probability vectors having no entry equal to one, (1) is **equivalent** to (11).

The remaining probability vectors are precisely the vertices \(e_j\). Section 2 proves that \(e_j\) is feasible when \(a_j\ge\sum_{i\ne j}a_i\). Necessity follows from the same single-positive-coordinate minimization, now with all other quadratic coefficients equal to one: feasibility requires
\[
1\le \frac{a_j}{\sum_{i\ne j}a_i}.
\]
This gives a complete characterization, including every possibility for zero weights.

There is a second exact interpretation of (11): assign complete-graph edge weights
\[
w_{ij}=T\theta_i\theta_j\quad(i\ne j).
\]
Then the weighted degree at vertex \(i\) is \(\sum_{j\ne i}w_{ij}=a_i\). Thus the interior obstruction is a rank-one positive weighted-degree realization. The square-root construction proves coverage of every strictly nondominant degree vector; vertex certificates cover the remaining boundary and dominant cases. For \(n\ge3\), positivity of all edges also directly shows that each \(a_i\) is strictly smaller than the sum of the other degrees.

## 6. Matrix and common-quadratic conclusion

Define
\[
S=\sum_i\theta_i v_iv_i^T.
\]
The matrix is positive semidefinite, and \(z^TSz=\sum_i\theta_i(v_i\cdot z)^2\le\Phi(z)\) for every \(z\).

In the dominant case, \(S=v_mv_m^T\) has rank one; it is singular whenever \(r>1\). The proof never inverts \(S\). In the nondominant case all weights are positive, so the spanning hypothesis makes \(S\) positive definite. Thus the argument explicitly covers singular matrices and zero entries of \(\theta\).

For any common quadratic \(Q\),
\[
Q(z)+z^TSz
=\sum_i\theta_i\bigl(Q(z)+(v_i\cdot z)^2\bigr)
\le Q(z)+\Phi(z).
\]
This is exactly the requested global lower bound and convex-combination certificate.

## 7. Adversarial checks of load-bearing steps

These checks supplement the proof; they are not substitutes for its quantified argument.

1. **Single-positive equality witnesses.** Under (2), fix \(j\), set \(q_j=1-\theta_j\), and set \(q_i=-\theta_i\) for \(i\ne j\). Then \(\sum_iq_i=0\), and both estimates (4) and (5) are equalities. Thus the reduction has retained the sharp constraints imposed by every single-positive sign cone.
2. **Branch transition.** For \(a=(4/3,1,1)\), the construction reaches \(\theta=(1/2,1/4,1/4)\), exactly at the junction where the largest-coordinate square root is zero. For \(a=(19/10,1,1)\), the upper branch is necessary and gives \(\theta=(19/21,1/21,1/21)\). These identities were also checked with exact rational arithmetic.
3. **Dominance boundary and dimension one.** The proof in Section 2 retains non-strict inequalities throughout, so \(a_m=\sum_{i\ne m}a_i\) is included. For \(n=2\), this covers unequal entries and equality; the interior characterization also correctly permits any strictly positive probability vector when \(a_1=a_2\).
4. **Mixed signs.** The key step (5) uses positivity only on \(P\); no extension of a sign-constrained minimizer to arbitrary vectors is assumed. An exact four-coordinate mixed-sign check and exhaustive negative-face/positive-ray checks for small sampled dimensions found no violation.

No unresolved mathematical gap remains in the stated obligation. No novelty claim is made.
