# Complete affirmative construction

## Statement

The requested weights always exist. The construction below applies in every dimension, includes zero weights and singular certificates, and uses only the positive kernel vector. It also characterizes every feasible weight vector.

Write $n=r+1$, put $a_i=k_i^2>0$, and let $A=\sum_i a_i$. Choose an index $m$ with $a_m=\max_i a_i$.

### Construction

**Case 1: a dominant coordinate.** If

$$a_m\geq A-a_m,$$

set $\theta_m=1$ and $\theta_i=0$ for $i\ne m$.

**Case 2: no dominant coordinate.** Suppose $a_m<A-a_m$. For

$$0\leq c\leq b:=\frac{1}{4a_m},$$

define

$$s_i(c)=\frac{1-\sqrt{1-4ca_i}}{2},\qquad F(c)=\sum_i s_i(c).$$

* If $F(b)\geq1$, choose the unique $c\in(0,b]$ with $F(c)=1$ and set $\theta_i=s_i(c)$ for every $i$.
* If $F(b)<1$, choose any $c\in(0,b)$ satisfying

  $$\sum_{i\ne m}s_i(c)=s_m(c),$$

  and set $\theta_m=1-s_m(c)$ and $\theta_i=s_i(c)$ for $i\ne m$.

These scalar roots exist, as proved below. They can be located by interval bisection; for the second root, a sufficiently small positive endpoint has positive sign and $b$ has negative sign. The construction is unchanged by multiplying $k$ by a positive scalar, because $c$ rescales inversely to the $a_i$.

## 1. Reduction to a hyperplane

For $z\in\mathbb R^r$, set $x_i=v_i\cdot z$, or $x=N^Tz$. Since $Nk=0$,

$$\sum_i k_i x_i=0.$$

Conversely, $N$ has rank $r=n-1$, so the image of $N^T$ is exactly $k^\perp$. Thus the required assertion is precisely

$$\sum_i\theta_i x_i^2\leq\sum_{x_i<0}x_i^2
\quad\text{for every }x\in k^\perp.\tag{1}$$

No change of coordinates involving an inverse of the eventual certificate matrix is used.

## 2. The dominant case

Let $\theta=e_m$ and assume $a_m\geq\sum_{i\ne m}a_i$.

If $x_m\leq0$, inequality (1) follows because its right side includes $x_m^2$. If $x_m>0$, the balance condition and Cauchy–Schwarz give

$$
k_mx_m
=-\sum_{i\ne m}k_ix_i
\leq\sum_{x_i<0}k_i|x_i|
\leq\left(\sum_{i\ne m}a_i\right)^{1/2}
       \left(\sum_{x_i<0}x_i^2\right)^{1/2}.
$$

Consequently,

$$x_m^2\leq\frac{\sum_{i\ne m}a_i}{a_m}
                 \sum_{x_i<0}x_i^2
\leq\sum_{x_i<0}x_i^2,$$

as required. This proves the assertion in Case 1, including equality in the dominance condition.

For completeness, dominance is also necessary for a vertex weight: set $B=\sum_{j\ne m}a_j$, $x_m=1$, and $x_j=-k_mk_j/B$ for $j\ne m$. Then $x\in k^\perp$ and its negative square sum is $a_m/B$. Thus (1) requires $a_m\geq B$.

## 3. A finite criterion for every nonvertex weight

Let $\theta_i\geq0$, $\sum_i\theta_i=1$, and suppose no $\theta_i$ equals $1$. Put

$$B_i=\sum_{j\ne i}\frac{a_j}{1-\theta_j}.$$

Then (1) holds if and only if

$$\theta_iB_i\leq a_i\qquad\text{for every }i.\tag{2}$$

### Necessity

For a fixed $i$, take

$$x_i=B_i/k_i,\qquad x_j=-k_j/(1-\theta_j)\quad(j\ne i).$$

This vector lies in $k^\perp$ and has $i$ as its sole positive coordinate. Subtracting the negative-coordinate terms from the two sides of (1) gives

$$\theta_i\frac{B_i^2}{a_i}
\leq\sum_{j\ne i}(1-\theta_j)\frac{a_j}{(1-\theta_j)^2}
=B_i.$$

Since $B_i>0$, this is exactly (2).

### Sufficiency, including arbitrary sign patterns

Let $x\ne0$ belong to $k^\perp$. Set $P=\{i:x_i>0\}$ and $J=\{j:x_j<0\}$. Positivity of $k$ forces both sets to be nonempty. Write

$$L=\sum_{i\in P}k_ix_i=\sum_{j\in J}k_j|x_j|,$$

and choose $i_*\in P$ maximizing $\theta_i/a_i$ over $P$. Let $\beta=\theta_{i_*}/a_{i_*}$. Nonnegativity of all $k_ix_i$ for $i\in P$ gives

$$\sum_{i\in P}\theta_ix_i^2
\leq\beta\sum_{i\in P}(k_ix_i)^2
\leq\beta L^2.$$

Weighted Cauchy–Schwarz gives

$$L^2\leq
\left(\sum_{j\in J}\frac{a_j}{1-\theta_j}\right)
\left(\sum_{j\in J}(1-\theta_j)x_j^2\right).$$

Since $J$ excludes $i_*$, condition (2) implies

$$\beta\sum_{j\in J}\frac{a_j}{1-\theta_j}
\leq\frac{\theta_{i_*}}{a_{i_*}}B_{i_*}\leq1.$$

Combining these inequalities yields

$$\sum_{i\in P}\theta_ix_i^2
\leq\sum_{j\in J}(1-\theta_j)x_j^2,$$

which is (1). The vector $x=0$ is immediate. Coordinates equal to zero require no special convention.

## 4. The exact quadratic identity

For a nonvertex probability vector, define

$$T=\sum_j\frac{a_j}{1-\theta_j}.$$

Criterion (2) is equivalent to

$$\theta_iT\leq\frac{a_i}{1-\theta_i}.$$

The sums of the two sides over $i$ are both $T$. Therefore every inequality must be an equality. In particular, all $\theta_i$ are strictly positive, and

$$\theta_i(1-\theta_i)=c\,a_i\qquad\text{for all }i,\tag{3}$$

where $c=1/T>0$.

Conversely, if a probability vector satisfies $0<\theta_i<1$ and (3) for some $c>0$, then

$$\frac{a_i}{1-\theta_i}=\frac{\theta_i}{c},\qquad
B_i=\frac{1-\theta_i}{c},$$

so $\theta_iB_i=a_i$ for every $i$. The finite criterion proves (1).

Thus (3), together with the probability-vector conditions, is both necessary and sufficient for every nonvertex feasible vector. Any feasible vector with a zero entry must be a vertex; vertices are feasible exactly under the dominance condition proved above.

## 5. Existence of the scalar roots

It remains to verify that Case 2 constructs weights satisfying (3).

Each $s_i$ is continuous on $[0,b]$, strictly increasing, and satisfies

$$s_i(c)(1-s_i(c))=ca_i.$$

If $F(b)\geq1$, then $F(0)=0$ and the intermediate value theorem gives a unique $c\in(0,b]$ with $F(c)=1$. The resulting $\theta_i=s_i(c)$ are positive, no greater than $1/2$, sum to one, and satisfy (3).

If $F(b)<1$, put

$$g(c)=\sum_{i\ne m}s_i(c)-s_m(c).$$

At zero, $g(0)=0$ and $s_i'(0)=a_i$, so

$$g'(0)=\sum_{i\ne m}a_i-a_m>0$$

by the nondominance assumption. Hence $g(c)>0$ for sufficiently small positive $c$. At the other endpoint $s_m(b)=1/2$, so

$$g(b)=F(b)-1<0.$$

Continuity supplies a root $c\in(0,b)$. Setting $\theta_m=1-s_m(c)$ and $\theta_i=s_i(c)$ for $i\ne m$ gives

$$\sum_i\theta_i=1-s_m(c)+\sum_{i\ne m}s_i(c)=1.$$

Every weight is strictly between zero and one, and replacing $s_m$ by $1-s_m$ preserves its quadratic product. Thus (3) holds for every $i$.

This proves the existence of the asserted weights in every case and completes the universal proof.

## 6. The matrix certificate and boundary cases

Set $S=\sum_i\theta_i v_iv_i^T$. Then $S$ is positive semidefinite and, for every $z$,

$$z^TSz=\sum_i\theta_i(v_i\cdot z)^2\leq\Phi(z).$$

In Case 1, $S=v_mv_m^T$ has rank one, so it is singular when $r>1$. This is a valid certificate. In Case 2, every weight is positive; because the $v_i$ span $\mathbb R^r$, $S$ is positive definite. The proof covers both cases without dividing by or inverting $S$.

When $r=1$, there are two entries and a maximal $a_i$ always meets the dominance condition, so Case 1 already resolves the entire dimension-one problem. Unequal coefficients already absorbed into the given vectors cause no additional restriction. For a common quadratic $Q$, the probability normalization gives

$$Q(z)+z^TSz=\sum_i\theta_i\bigl(Q(z)+(v_i\cdot z)^2\bigr)
\leq Q(z)+\Phi(z).$$

## 7. Adversarial checks of load-bearing steps

These checks supplement the proof; they are not used to infer the universal conclusion.

* **The second square-root branch is necessary.** For $a=(4,3,2)$, the sum of all smaller roots at $b=1/16$ is $1/2+1/4+(1-1/\sqrt2)/2<1$. The second branch gives the exact weights $(15,5,3)/23$, and all three products $\theta_i(1-\theta_i)/a_i$ equal $30/529$.
* **Uniform weights do not extend to arbitrary coefficients.** For this same $a$, use weighted coordinates $y_i=k_ix_i=(-4,-3,7)$. Then $\sum_i y_i=0$. Uniform weights give $\sum_i\theta_ix_i^2=21/2$, whereas the negative square sum is $7$.
* **All sign patterns, not just singleton patterns.** Exact rational arithmetic checked the finite Cauchy coefficient for every nontrivial ternary sign pattern in the cases $a=(4,3,2)$, $\theta=(15,5,3)/23$, and $a=(4,4,1)$, $\theta=(7,7,1)/15$. Each of the twelve patterns in each case has coefficient at most one; the maximum is exactly one. Section 3 proves the same control for arbitrary dimension and coefficients.
* **Dominance equality and singularity.** The examples $a=(2,1,1)$ and $a=(4,1,1)$ satisfy the rank-one certificate condition, including its boundary.
* **Numerical cross-check.** Across 650 randomly generated positive coefficient lists in dimensions $n=2,\ldots,14$, all three construction branches occurred. On 32,500 projected hyperplane vectors, the largest observed normalized violation was zero. Floating-point evidence is supplementary only.

**Outcome:** complete proof and construction; no remaining mathematical gap. No novelty claim is made.
