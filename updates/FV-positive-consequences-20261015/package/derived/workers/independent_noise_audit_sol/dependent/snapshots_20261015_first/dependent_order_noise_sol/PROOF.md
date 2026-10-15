# Dependent scalar noise for the Pauli Margenau–Hill kernel

Status: independently derived, internally checked, externally unreviewed. The exact dependent optimum is **not determined**. The theorem below gives a strict global lower bound, a fully positive infinite-support construction, an existence theorem for an optimizer, and an exact independent-noise comparator. No current worker's output was read.

Input DATA: `sources/mathematics_pasted.txt`, SHA256 `c4608c8794bd9c9705bc8236226c2193d385d4305a59a300ef9c65a4bcc30876`. Repository context was pinned at `a6190a1083f688a7e4bf64adbc5244ef150ff2c4`. No repository files were changed.

## 1. Contract and result

Let $a,b>0$, $A=a\sigma_z$, $B=b\sigma_x$, and

\[
J(s,t)=\tfrac12(e^{isA}e^{itB}+e^{itB}e^{isA}).
\]

We require one scalar probability law $\nu$ on $\mathbb R^2$, with finite covariance, for which

\[
\widehat M(s,t)=\widehat\nu(s,t)J(s,t)
\tag{1}
\]

is the characteristic operator of a normalized POVM. Dependence is unrestricted. Absolutely continuous, singular continuous, and discrete laws are all included. No exponential moment is assumed.

Translations of the noise merely translate $M$, so the noise may be centered. Put $D=\operatorname{diag}(a,b)$, $\Gamma=D^{-1}\operatorname{Cov}(\nu)D^{-1}$. The normalized trace is $\operatorname{tr}\Gamma$. All statements for unit Pauli scales transfer by this coordinate change.

**Theorem.** Let $v_*$ be the infimum of the normalized noise trace in (1).

\[
\boxed{L_0<v_*\le U_0<4,}
\qquad
\begin{split}
L_0&=2.6621752331925296967\ldots,\\
U_0&=\frac{5949040524880}{1857425454953}
     =3.2028421431483687\ldots.
\end{split}
\tag{2}
\]

The lower bound is exact as an algebraic constant: if $t_0>1$ is the unique root of

\[
2t_0^3-3t_0-2=0,
\]

then

\[
L_0=\frac{4(\sqrt2-1)t_0^2(t_0+1)}{2t_0^2-1}.
\tag{3}
\]

The infimum $v_*$ is attained, and some optimizer is supported on a single translate of $2a\mathbb Z\times2b\mathbb Z$. This does not assert that its translate is centered at an integer lattice site or that its probabilities have separate reflection symmetry.

For independent coordinates the complete variance frontier is

\[
\boxed{\operatorname{Var}(N_1)\operatorname{Var}(N_2)\ge4a^2b^2,}
\tag{4}
\]

with every point of equality attained by double-geometric noise. In particular the independent minimum normalized trace is $4$, and its minimum physical trace is $4ab$. Thus dependence strictly improves the fixed scalar-convolution contract. The exact arbitrary-dependent optimum remains in the interval (2).

The usual unbiased joint-measurement moment bound is only $\det\Gamma\ge1$, with normalized trace $2$ attainable by a different POVM. The strict $L_0>2$ is an obstruction specific to (1), rather than a restatement of that bound.

If either $a$ or $b$ is zero, the observables commute and zero noise is admissible; this degenerate case is excluded above.

## 2. Four-corner representation and the exact local cone

Pauli anticommutation gives

\[
J(s,t)=\cos(as)\cos(bt)I
 +i\sin(as)\cos(bt)\sigma_z
 +i\cos(as)\sin(bt)\sigma_x.
\]

Consequently its inverse Fourier transform is the finite operator measure

\[
T=\frac14\sum_{\epsilon,\eta=\pm1}
 (I+\epsilon\sigma_z+\eta\sigma_x)
 \delta_{(\epsilon a,\eta b)}.
\tag{5}
\]

Each corner operator has one negative eigenvalue. Uniqueness of Fourier transforms of finite measures makes (1) exactly equivalent to positivity of $T*\nu$. There is no inverse Fourier regularity or analytic continuation assumption here.

In unit scales, if $\nu$ is supported on $u+2\mathbb Z^2$, with masses $w_{kl}$, the output atom at $u+(2k+1,2l+1)$ is

\[
\frac14(S_{kl}I+X_{kl}\sigma_z+Y_{kl}\sigma_x),
\tag{6}
\]

where, writing $p=w_{kl},q=w_{k+1,l},r=w_{k,l+1},s=w_{k+1,l+1}$,

\[
S=p+q+r+s,\quad X=p+r-q-s,\quad Y=p+q-r-s.
\]

Thus the exact condition is

\[
\boxed{S\ge\sqrt{X^2+Y^2}\quad\text{for every cell}.}
\tag{7}
\]

The probabilities must also be nonnegative and sum to one. Condition (7) is a countably infinite second-order cone condition. Finite LP angle tests are relaxations, not full certificates.

For an arbitrary law $\nu$, disintegrate over the quotient $\mathbb R^2/(2\mathbb Z^2)$. All four translates in (5) have the same quotient shift, so the conditional operator measure on each output coset is (6). Positivity of $T*\nu$ is equivalent to (7) for the conditional probability array on almost every coset. Countably many cells allow a common null set. This supplies an exact reduction covering continuous and singular laws.

## 3. A strict global bound from a radial positive test

This proof does not restrict to lattice laws. Center the noise $N$, and write

\[
M(dx)=p(dx)I+m_z(dx)\sigma_z+m_x(dx)\sigma_x.
\]

The scalar probability $p=\tfrac12\operatorname{tr}M$ is the law of the auxiliary classical random variable

\[
Y=N+S,
\]

where $S$ is independent of $N$ and uniform on the four corners $\{(\pm1,\pm1)\}$. This auxiliary identity is for the scalar trace measure; it asserts no classical hidden-state model for the POVM.

Finite noise covariance implies finite output second moments, directly from (5). The first-moment identities give

\[
\int x\,m_z(dx\,dy)=1,
\qquad
\int y\,m_x(dx\,dy)=1.
\tag{8}
\]

For every point $y=(y_1,y_2)$, the matrix

\[
F(y)=|y|I-y_1\sigma_z-y_2\sigma_x
\]

is positive. Integrating the trace pairing with the positive POVM is legitimate because it grows only linearly. Equations (8) yield

\[
\boxed{\mathbb E|N+S|\ge2.}
\tag{9}
\]

For a fixed $z=(x,y)$, put $u=x^2+y^2$, $c=u+2$. The four squared lengths are $c\pm2x\pm2y$. Let

\[
\phi_c(v)=\sqrt{c+2\sqrt v}+\sqrt{c-2\sqrt v}
           =\sqrt{2c+2\sqrt{c^2-4v}}.
\]

On its domain $0\le v\le c^2/4$, this is concave: both square roots in the last expression are concave, and the outer root is increasing. The two arguments $(x+y)^2,(x-y)^2$ have average $u$. Therefore

\[
\frac14\sum_{s\in\{\pm1\}^2}|z+s|
\le h(u):=\sqrt{\frac{u+2+\sqrt{u^2+4}}2}.
\tag{10}
\]

Equality holds in the angular maximization on either coordinate axis. Thus (10) is the exact maximum over the direction of a vector of fixed length.

Define

\[
K_0=\sup_{u>0}\frac{h(u)-\sqrt2}{u}.
\tag{11}
\]

It follows pointwise that the left side of (10) is at most $\sqrt2+K_0|z|^2$. Combining this with (9) proves

\[
\operatorname{tr}\operatorname{Cov}(N)=\mathbb E|N|^2
\ge\frac{2-\sqrt2}{K_0}.
\tag{12}
\]

To evaluate (11), set $h(u)=\sqrt2\,t$, $t\ge1$. Solving for $u$ and canceling the removable factor gives

\[
\frac{h(u)-\sqrt2}{u}
=\frac{2t^2-1}{2\sqrt2\,t^2(t+1)}.
\]

Its derivative has the sign of $-2t^3+3t+2$. The function $2t^3-3t-2$ is strictly increasing for $t\ge1$, is negative at $1$, and tends to infinity. Hence the maximum occurs at its unique root $t_0>1$. Substitution in (12) gives exactly (3).

The file `lower_bound_certificate.json` encloses this algebraic constant using exact rational intervals:

\[
2.6621752331925291926<L_0<2.6621752331925301971.
\]

The global bound is the analytic proof above. The symbolic and interval script checks the evaluation; it is not the proof of the inequality. $L_0$ is the sharp constant obtained by this single radial-moment test and the affine majorant (11). It is **not claimed to be the sharp scalar-convolution optimum**.

In fact the infimum is strictly larger than $L_0$, although the additional gap is not quantified here. If an admissible law attained equality in (12), every inequality in (9)–(12) would be equality. The slope in (11) has a unique maximizing positive radius, and the angular maximization (10) is strict away from the coordinate axes at a positive radius. Hence the noise would be supported on at most five points: the origin and the four axial points at that radius.

No nonzero finitely supported probability law is admissible. Choose a support point with maximal first coordinate and, among those, maximal second coordinate. At that point plus $(1,1)$, precisely one translated noise atom contributes to (5), so the output has a positive multiple of $I+\sigma_z+\sigma_x$, which has a negative eigenvalue. Equality is therefore impossible. Section 5 proves attainment of the global minimum, and thus upgrades $v_*\ge L_0$ to $v_*>L_0$.

## 4. A fully positive dependent construction

Take $q=11/64$, and the symmetric positive integer matrix

\[
C=\begin{pmatrix}
1000000&149000&5200&14\\
149000&48600&7120&72\\
5200&7120&2450&420\\
14&72&420&73
\end{pmatrix}.
\tag{13}
\]

For $k,l\in\mathbb Z$, define

\[
\widetilde w_{kl}
=C_{\min(|k|,3),\min(|l|,3)}
 q^{(|k|-3)_++(|l|-3)_+},
\qquad w_{kl}=\widetilde w_{kl}/Z.
\tag{14}
\]

Let $N=(2k,2l)$ with probability $w_{kl}$. Both signs are symmetric, so its mean and cross covariance vanish. It is dependent: for example $C_{00}C_{11}\ne C_{10}^2$.

All cells reduce by separate reflection to the nonnegative quadrant. There are three types.

1. **Core:** $0\le k,l<3$. The integer values of $S^2-X^2-Y^2$ in (7) are

\[
\begin{pmatrix}
3007640000&39417600&325596\\
39417600&3139100&154076\\
325596&154076&9511
\end{pmatrix},
\]

all positive.

2. **One tail coordinate:** a cell has one ratio $q$, and its other pair is $x=C_{3,j},y=C_{3,j+1}$. Put $u_q=(1-q)/(1+q)=53/75$. Condition (7) reduces exactly to

\[
(1-u_q^2)(x+y)^2-(x-y)^2\ge0.
\tag{15}
\]

The three values are strictly positive, as certified with rational arithmetic in `exact_construction_certificate.json`. Reflection and coordinate interchange cover every strip.

3. **Both tail coordinates:** both ratios are $q$, so (7) reduces to

\[
2u_q^2=5618/5625<1.
\tag{16}
\]

These three analytic cases cover the entire infinite lattice. The certificate is therefore not a truncated numerical positivity test.

For normalization and moments let

\[
m=(1,2,2,2/(1-q)),
\]

\[
\tau=(0,2,8,2[9/(1-q)+6q/(1-q)^2+q(1+q)/(1-q)^3]).
\]

Then

\[
Z=\sum_{i,j=0}^3m_i m_j C_{ij}
  =\frac{5289926536}{2809},
\]

and

\[
\operatorname{tr}\operatorname{Cov}(N)
=\frac{4\sum_{i,j}(\tau_i m_j+m_i\tau_j)C_{ij}}{Z}
=U_0.
\tag{17}
\]

Its covariance is exactly $(U_0/2)I$. For general $a,b$, use noise $DN$, obtaining covariance $(U_0/2)\operatorname{diag}(a^2,b^2)$.

The noise has all polynomial moments and a finite exponential neighborhood. Its moment generating function is finite precisely when

\[
|g_1|<\tfrac12\log(64/11),\qquad
|g_2|<\tfrac12\log(64/11)
\]

in normalized coordinates. Thus it does not contradict the all-exponential obstruction in the supplied DATA.

## 5. An optimizer exists and may be taken on one lattice coset

For any positive definite quadratic cost, take a centered minimizing sequence of admissible laws with bounded second moments. Tightness gives a weakly convergent subsequence. Uniform second-moment bounds imply uniform integrability of the first moments, so the limit remains centered. Its second moment is at most the limiting cost by lower semicontinuity.

Convolution with the finite operator measure (5) is weakly continuous. Positivity is closed: integration of every bounded nonnegative continuous scalar test against every diagonal matrix coefficient $\langle v,M(\cdot)v\rangle$ remains nonnegative. The limiting operator measure is therefore a positive normalized POVM. Its covariance is finite, and the lower-semicontinuity inequality plus the definition of the infimum shows that it attains the infimum.

Disintegrate an optimizer $\nu$ into conditional laws $\nu_u$ on quotient cosets as in section 2. For almost every $u$, the conditional law is admissible and has finite covariance. Centering each conditional law preserves admissibility. The law of total covariance gives

\[
\operatorname{tr}\operatorname{Cov}(\nu)
=\int\operatorname{tr}\operatorname{Cov}(\nu_u)\,\pi(du)
 +\int|\mathbb E_{\nu_u}N-\mathbb E_\nu N|^2\,\pi(du).
\tag{18}
\]

Every centered conditional law has cost at least the global infimum. Since the left side already equals it, the second term must vanish and almost every conditional law must also attain it. Selecting one such conditional law proves the single-coset assertion. The same proof works for an arbitrary positive definite quadratic covariance cost.

This is a rigorous infinite-dimensional reduction. It does not license a finite truncation, separate reflection symmetry within the selected coset, or a choice of coset phase without further proof.

## 6. Exact independent-noise frontier

Suppose $\nu=\nu_1\otimes\nu_2$. In one coordinate write the two shifted measures as $\mu_+$ and $\mu_-$, set $p=(\mu_++\mu_-)/2$, and write the signed difference as $f p=(\mu_+-\mu_-)/2$. Let $c=\|f\|_\infty$.

In two coordinates the operator density with respect to $p_1\otimes p_2$ is

\[
I+f_1(x)\sigma_z+f_2(y)\sigma_x.
\]

Thus positivity is equivalent to $c_1^2+c_2^2\le1$. For an admissible finite-variance independent law, both $c_j$ lie strictly between zero and one: $c_j=0$ would make a probability law invariant under a nonzero translation.

The bound $|f|\le c<1$ is equivalent to the translated-measure inequalities

\[
r\nu(E)\le\nu(E+2a)\le r^{-1}\nu(E),
\qquad r=\frac{1-c}{1+c}.
\tag{19}
\]

**One-dimensional lemma.** Every finite-variance probability law satisfying (19) obeys

\[
\operatorname{Var}(N)\ge\frac{8a^2r}{(1-r)^2}
=2a^2\frac{1-c^2}{c^2}.
\tag{20}
\]

**Proof.** Disintegrate by the quotient modulo $2a$. Each conditional integer-valued probability sequence obeys $p_{k+1}\ge rp_k$ and $p_k\ge rp_{k+1}$. Write $V_r=2r/(1-r)^2$. For $k\ge2$, put

\[
\lambda_k=\frac{(k-1)[k(1-r)+2r]}{(1-r)^2}>0.
\]

Direct summation gives the exact dual identity

\[
\begin{split}
\sum_k[k(k-1)-V_r]p_k
={}&\sum_{k\ge2}\lambda_k(p_k-rp_{k-1})\\
 &+\sum_{k\le-1}\lambda_{1-k}(p_k-rp_{k+1})\ge0.
\end{split}
\tag{21}
\]

Finite second moments justify the sums; the multipliers grow quadratically. Translate the integer index so that its mean $m$ lies in $[0,1]$. Equation (21) then implies

\[
\operatorname{Var}(K)
=\mathbb E[K(K-1)]+m-m^2
\ge V_r+m(1-m)\ge V_r.
\]

Rescale by $2a$ and use total variance over the quotient to get (20). Equality is attained by $P(K=k)=(1-r)r^{|k|}/(1+r)$. This proves the lemma for arbitrary continuous or singular input laws as well as lattice laws.

Applying (20) in both coordinates gives

\[
\frac{2a^2}{V_1+2a^2}+\frac{2b^2}{V_2+2b^2}\le1,
\]

which is equivalent to $V_1V_2\ge4a^2b^2$. Equality is attained by taking double-geometric coordinates with $c_1^2+c_2^2=1$. This proves (4). Additional independent centered noise gives all points above the frontier if desired.

For normalized trace, choose $c_1=c_2=1/\sqrt2$, hence $r=3-2\sqrt2$. Each normalized noise variance is $2$, and the total is $4$. For physical trace choose $c_1^2=a/(a+b),c_2^2=b/(a+b)$; both physical variances are $2ab$, and the total is $4ab$.

## 7. What remains open

The exact dependent minimum, its optimizer's probability array, uniqueness, and its complete covariance frontier are unresolved. The universal lower bound $L_0$ and explicit upper bound $U_0$ do not match.

Numerical angle-LP diagnostics under separate reflection symmetry and an integer-centered coset suggest traces near $3.176$. They omit some cone directions, truncate the lattice, and have nonzero cone residuals. They also impose a symmetry/phase restriction not established for a global optimizer. They are search guidance only. None of those numbers is used in the theorem, the lower-bound proof, or the exact construction certificate.

The closest rigorous next step is an analytic dual for the full infinite lattice problem together with optimization over coset mean/phase, or an exact optimizer construction with a matching dual. More finite LP runs would not settle that obligation.
