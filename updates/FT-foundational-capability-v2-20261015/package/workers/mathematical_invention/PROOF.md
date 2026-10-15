# A scalar-convolution criterion for compact distributions with values in an ordered space

Status: internally reconstructed theorem candidate, 2026-10-15. The argument below is mathematical work, not a claim of historical priority, independent review, formal verification, or exceptional practical capability.

## 1. Result and scope

The supplied quantum-observable candidate suggests retaining a positive real exponential tilt and perturbing only its logarithmic remainder. The extension here removes its quantitative exponential lower-bound assumption and gives an exact criterion for arbitrary compact distributions.

Let \(E\) be a real Banach space and \(C\subsetneq E\) a closed convex cone with nonempty interior. Pointedness is not needed. Write \(u\preceq_C v\) when \(v-u\in C\). Fix \(e\in\operatorname{int}C\). Let
\[
T:C_c^\infty(\mathbb R^m)\longrightarrow E
\]
be a continuous linear distribution with compact support and \(T(1)=e\). Compact support makes evaluation on every smooth function meaningful by inserting a cutoff equal to one near the support. Its real Laplace transform is
\[
\mathcal L_T(g)=T_y(e^{g\cdot y}),\qquad g\in\mathbb R^m.
\]

Define the admissible scalar class
\[
\mathscr E=\left\{p\in C^\infty(\mathbb R^m):
\int_{\mathbb R^m}e^{a|x|}|\partial^\alpha p(x)|\,dx<\infty
\ \text{for every }a\ge0,\ \alpha\right\}.
\tag{1}
\]

Call a distribution \(S\) \(C\)-positive if \(S(\phi)\in C\) for every nonnegative real \(\phi\in C_c^\infty\). **Theorem.** The following conditions are equivalent.

1. \(\mathcal L_T(g)\in\operatorname{int}C\) for every real \(g\).
2. There is a scalar probability measure \(\nu\) satisfying \(\int e^{a|z|}\nu(dz)<\infty\) for every \(a\ge0\), such that \(T*\nu\) is a \(C\)-positive distribution.
3. There is a strictly positive probability density \(p\in\mathscr E\) such that \(M=T*p\) takes values in \(C\).

Moreover, when condition 1 holds, for every \(0<\varepsilon<1\) one can choose \(p\) smooth, radial, and strictly log-concave, with
\[
(1-\varepsilon)p(x)\mathcal L_T(\nabla V(x))
\preceq_C M(x)
\preceq_C
(1+\varepsilon)p(x)\mathcal L_T(\nabla V(x)),
\qquad p=Z^{-1}e^{-V}.
\tag{2}
\]
Thus \(M(x)\in\operatorname{int}C\) at every \(x\), and
\[
\int_{\mathbb R^m}M(x)\,dx=e.
\tag{3}
\]
The output and all its derivatives are integrable in norm after multiplication by every \(e^{a|x|}\).

For \(E=\operatorname{Herm}_d\) and \(C\) the positive-semidefinite cone, the criterion is exactly
\[
\mathcal L_T(g)\succ0\quad\text{for all }g\in\mathbb R^m.
\]
For self-adjoint elements of a unital \(C^*\)-algebra, interior positivity means positive invertibility, with a separate positive lower bound permitted at each \(g\). The proof applies in that setting too.

There is no prescribed decay rate for the positivity margin. In particular, no constants \(\eta,b>0\) satisfying
\(\mathcal L_T(g)\succeq\eta e^{-b|g|}I\) are assumed. Section 7 constructs a compact smooth scalar density with strictly positive Laplace transform for which every such bound fails.

## 2. Compact distributions preserve the admissible class

Choose \(R_1>0\), a cutoff \(\chi\in C_c^\infty(B_{R_1})\) equal to one near the support of \(T\), a nonnegative integer \(N\), and \(C_T<\infty\) so that
\[
\|T(h)\|
\le C_T\max_{|\alpha|\le N}\sup_{B_{R_1}}|\partial^\alpha h|.
\tag{4}
\]
Cutoff differentiation is absorbed into \(C_T\). Such data exist by continuity of a compactly supported distribution.

For completeness, a local supremum can be bounded by local integrals of finitely many derivatives. If \(h\) is compactly supported, repeated use of the fundamental theorem of calculus in the \(m\) coordinate directions gives
\[
|h(y)|\le\int_{\mathbb R^m}
|\partial_1\cdots\partial_m h(u)|\,du.
\]
Apply this to derivatives of \(\chi(y)p(x-y)\). Equation (4) then gives
\[
\|M(x)\|
\le C\sum_{|\beta|\le N+m}
\int_{B_{R_1}}|\partial^\beta p(x-y)|\,dy,
\tag{5}
\]
after increasing the finite constant and derivative index if the cutoff requires it. The same estimate applies to every derivative of \(M\).

Since \(|x|\le|x-y|+R_1\) on the integral,
\[
\int e^{a|x|}\|M(x)\|\,dx
\le C_a\sum_{|\beta|\le N+m}
\int e^{a|z|}|\partial^\beta p(z)|\,dz<\infty.
\tag{6}
\]
This justifies all following integrals in Banach norm and the interchange of \(T\) with the integrals. In particular,
\[
\int M(x)\,dx=T(1)=e,
\tag{7}
\]
and
\[
\int e^{g\cdot x}M(x)\,dx
=\left(\int e^{g\cdot x}p(x)\,dx\right)\mathcal L_T(g).
\tag{8}
\]

The derivative condition in (1) is material. Finite exponential moments of \(p\) alone would not justify applying an arbitrary finite-order distribution and interchanging these integrals.

## 3. Necessity for any scalar probability measure

This proof does not assume derivatives, or even a density, for the input noise. Let \(\nu\) be as in condition 2 and write \(S=T*\nu\). Distributional convolution is well-defined because \(T\) is compactly supported:
\[
S(\phi)=T_y\left(\int\phi(y+z)\,\nu(dz)\right).
\]
Choose a smooth radial cutoff \(\chi\), equal to one on \(B_1\), zero outside \(B_2\), with \(0\le\chi\le1\) and radial profile nonincreasing. Put \(\chi_R(x)=\chi(x/R)\). For a fixed real \(g\), define
\[
h_{R,g}(y)=\int e^{g\cdot(y+z)}\chi_R(y+z)\,\nu(dz).
\]
On every fixed compact \(y\)-set,
\[
h_{R,g}\longrightarrow
\left(\int e^{g\cdot z}\nu(dz)\right)e^{g\cdot y}
\quad\text{in }C^N.
\tag{9a}
\]
Indeed, differentiating under the integral gives sums of
\[
e^{g\cdot(y+z)}g^{\alpha-\beta}
R^{-|\beta|}(\partial^\beta\chi)((y+z)/R).
\]
For \(\beta=0\), the error on \(|y|\le R_1\) is bounded by a constant times
\(\int_{|z|>R-R_1}e^{g\cdot z}\nu(dz)\), which tends to zero. For \(|\beta|>0\), the uniform bound contains \(R^{-|\beta|}\int e^{g\cdot z}\nu(dz)\) and also tends to zero. Thus (4) proves the norm limit
\[
S(e^{g\cdot x}\chi_R(x))
\longrightarrow
\left(\int e^{g\cdot z}\nu(dz)\right)\mathcal L_T(g).
\tag{9b}
\]

At \(g=0\), \(Q_R:=S(\chi_R)\to T(1)=e\) in norm. Choose finite \(A\) with \(Q_A\in\operatorname{int}C\).
For \(R\ge2A\),
\[
e^{g\cdot x}\chi_R(x)
-e^{-2A|g|}\chi_A(x)\ge0
\quad\text{at every }x.
\]
Hence \(C\)-positivity gives
\[
S(e^{g\cdot x}\chi_R(x))
-e^{-2A|g|}Q_A\in C.
\]
Taking the norm limit (9b) and using closedness of \(C\) shows that the limit is the sum of an interior cone element and a cone element, so it is interior. The scalar Laplace transform of \(\nu\) is finite and strictly positive; therefore \(\mathcal L_T(g)\in\operatorname{int}C\).

In finite matrix dimension, \(C\)-positive distributions are positive matrix measures, and the growing cutoffs also establish their normalization and finite exponential moments. The cutoff proof itself works for Banach cone values and avoids assuming that a weakly normalized arbitrary POVM is norm tight.

Condition 3 implies condition 2 immediately. Section 6 proves condition 1 implies condition 3, completing all three equivalences.

## 4. An explicit slow-slope lemma

The main construction is not an unspecified instruction to choose a function slowly enough.

Let \(G:[1,\infty)\to[1,\infty)\) be any finite, nondecreasing function. Fix once and for all a smooth nondecreasing step
\[
\theta(s)=0\quad(s\le0),\qquad
\theta(s)=1\quad(s\ge1).
\]
For example, on \(0<s<1\), take
\[
\theta(s)=
\frac{e^{-1/s}}{e^{-1/s}+e^{-1/(1-s)}}.
\]
Choose the thresholds inductively:
\[
S_1=\max\{2,\ 2\log G(2)\},
\]
\[
S_{n+1}
=\max\{S_n+2,\ 2(n+1),\ 2\log G(n+2)\}.
\tag{9}
\]
Define, for \(s\ge0\),
\[
q(s)=1+\sum_{n=1}^{\infty}\theta(s-S_n).
\tag{10}
\]
The sum is locally finite.

Then:

- \(q\) is smooth and nondecreasing, \(q\ge1\), and \(q(s)\to\infty\).
- \(q(s)\le1+s/2\).
- For every \(k\ge1\), \(\sup_s|q^{(k)}(s)|\le\|\theta^{(k)}\|_\infty\), because the transition intervals are disjoint.
- If \(|s-t|\le1\) and \(s,t\ge0\), then \(q(t)\le q(s)+1\).
- With \(C_G=\max\{1,G(1)\}\),
\[
G(q(s))\le C_G e^{s/2}.
\tag{11}
\]

To check the last assertion, before \(S_1\) one has \(q=1\). Otherwise let \(n\) be the latest activated threshold. Throughout its transition and the succeeding plateau, \(q(s)\le n+1\), and
\[
G(q(s))\le G(n+1)\le e^{S_n/2}\le e^{s/2}.
\]
Every threshold is finite; no restriction is imposed on how rapidly the sequence grows.

One can impose any additional finite lower bounds on \(S_n\), for example to make \(q\) grow beneath a specified unbounded increasing envelope. All conclusions remain true.

## 5. A strictly convex radial potential with controlled jets

For \(z\in\mathbb R^m\), put
\[
\rho(z)=\sqrt{1+|z|^2},\qquad s(z)=\log\rho(z),
\]
\[
H(u)=\int_1^u q(\log v)\,dv,\qquad
f(z)=H(\rho(z)).
\tag{12}
\]
The function \(f\) is smooth and radial. Since \(q>0\) and \(q'\ge0\),
\[
\nabla f(z)=q(s)\frac z\rho,
\tag{13}
\]
\[
D^2f(z)
=q(s)D^2\rho(z)
+\frac{q'(s)}{\rho}\nabla\rho(z)\otimes\nabla\rho(z)\succ0.
\tag{14}
\]
Here \(D^2\rho=\rho^{-1}I-\rho^{-3}zz^\top\), whose radial eigenvalue is \(\rho^{-3}>0\). Thus strict convexity holds even on the plateaus of \(q\).

For every \(k\ge2\), there is a finite \(C_k\), depending only on \(m,k,\theta\), such that
\[
\|D^k f(z)\|\le C_k q(s)\rho^{1-k}.
\tag{15}
\]
Indeed, \(D^j\rho=O_j(\rho^{1-j})\). For \(\ell\ge2\),
\[
H^{(\ell)}(u)
=u^{1-\ell}P_\ell(q'(\log u),\ldots,q^{(\ell-1)}(\log u)),
\]
where \(P_\ell\) is a fixed linear combination. The bounded derivatives of \(q\), and \(q\ge1\), give
\(|H^{(\ell)}(u)|\le C_\ell q(\log u)u^{1-\ell}\).
The chain rule for \(H\circ\rho\) gives (15), term by term.

Also,
\[
\frac{f(z)}{|z|}\longrightarrow\infty.
\tag{16}
\]
For large \(\rho\), the integral defining \(H\) over \([\rho/2,\rho]\) is at least
\((\rho/2)q(\log(\rho/2))\), and this divided by \(|z|\) tends to infinity.

For \(L\ge1\), let
\[
V_L(x)=L f(x/L),\qquad
p_L(x)=Z_L^{-1}e^{-V_L(x)}.
\tag{17}
\]
Equation (16) makes \(0<Z_L<\infty\) and gives every exponential moment.
Equations (13), (15), and \(q(s)\le1+s/2\) show, for every multi-index \(\alpha\),
\[
|\partial^\alpha p_L(x)|
\le C_{\alpha,L}\,p_L(x)
\bigl(1+\log\sqrt{1+|x/L|^2}\bigr)^{|\alpha|}.
\tag{18}
\]
Thus \(p_L\in\mathscr E\). It is radial, smooth, strictly positive, and strictly log-concave.

## 6. Sufficiency and the global error bound

For a point \(w\in\operatorname{int}C\), define its interior radius
\[
d_C(w)=\operatorname{dist}(w,E\setminus C).
\]
It is finite, strictly positive, and 1-Lipschitz on the interior. Define
\[
\mu(t)=\min_{|g|\le t}d_C(\mathcal L_T(g))>0.
\tag{19}
\]
The minimum exists because the real \(g\)-ball is compact and the transform is continuous. The function \(\mu\) is nonincreasing.

Use the slow-slope lemma with
\[
G(t)=\max\left\{1,\
\frac{e^{R_1t}(1+t)^{N+1}}{\mu(t)}\right\},
\qquad t\ge1.
\tag{20}
\]
This is finite and nondecreasing.

Fix \(x\), let \(z=x/L\), \(\rho=\rho(z)\), \(s=\log\rho\), and
\[
g=\nabla V_L(x)=\nabla f(z).
\]
For \(|y|\le R_1\), define the exact logarithmic remainder
\[
F_x(y)=V_L(x-y)-V_L(x)+g\cdot y.
\tag{21}
\]
Assume \(L\ge\max\{1,R_1\}\). The function \(\log\rho\) is 1-Lipschitz, so at \(z-y/L\) its value differs from \(s\) by at most one; the corresponding \(\rho\)'s differ by factors at most \(e\), and the corresponding \(q\)'s differ by at most one.

Taylor's integral remainder for orders zero and one, followed by (15) for higher orders, gives
\[
\max_{|\alpha|\le N}\sup_{|y|\le R_1}
|\partial_y^\alpha F_x(y)|
\le \frac{C_0}{L}\frac{q(s)+1}{\rho}.
\tag{22}
\]
If \(N<2\), the same argument still uses the available second derivative of \(V_L\). For \(k\ge2\), the scaling is
\[
\|D^kV_L(x-y)\|
\le C_k L^{1-k}(q(s)+1)\rho^{1-k}
\le\frac{C_k}{L}\frac{q(s)+1}{\rho}.
\]
The constants in (22) depend only on the fixed seminorm data, \(m,N,\theta\), not on \(x,L\), or the threshold locations.

Because \(q(s)\le1+s/2\), \((q(s)+1)e^{-s}\) is bounded. Increasing \(L\) makes the left side of (22) at most one for all \(x\). The product and chain rules therefore imply
\[
\|e^{-F_x}-1\|_{C^N(B_{R_1})}
\le\frac{C_1}{L}\frac{q(s)+1}{\rho}.
\tag{23}
\]

The identity
\[
p_L(x-y)
=p_L(x)e^{g\cdot y}e^{-F_x(y)}
\tag{24}
\]
is exact. Hence
\[
\frac{M_L(x)}{p_L(x)}
=\mathcal L_T(g)+E_x,
\qquad
E_x=T_y\!\left(e^{g\cdot y}(e^{-F_x(y)}-1)\right).
\tag{25}
\]
Using (4), (23), and \(|g|\le q(s)\), we obtain
\[
\|E_x\|
\le\frac{C_2}{L}
e^{R_1q(s)}(1+q(s))^{N+1}e^{-s}.
\tag{26}
\]
Divide by \(\mu(q(s))\) and use (11), (20):
\[
\frac{\|E_x\|}{\mu(q(s))}
\le\frac{C_2C_G}{L}e^{-s/2}
\le\frac{C_2C_G}{L}.
\tag{27}
\]
Take \(L\) large enough to meet the previous finite lower bounds and
\[
L\ge C_2C_G/\varepsilon.
\tag{28}
\]
Since \(|g|\le q(s)\),
\[
\|E_x\|
\le\varepsilon\,\mu(q(s))
\le\varepsilon\,d_C(\mathcal L_T(g)).
\]
The ball of radius \(\varepsilon d_C(\mathcal L_T(g))\) centered at
\(\varepsilon\mathcal L_T(g)\) lies in \(C\), by homogeneity of the cone.
Therefore
\[
-\varepsilon\mathcal L_T(g)
\preceq_C E_x
\preceq_C\varepsilon\mathcal L_T(g).
\]
This is (2). Since \(1-\varepsilon>0\), its lower bound is interior, proving pointwise strict positivity. Equations (3) and the weighted norm integrability follow from Section 2.

This completes the three-way equivalence.

## 7. The missing exponential margin is a real extension

Here is an explicit compact smooth real scalar density \(t\) with
\(\int t=1\), strictly positive real Laplace transform, and no exponential lower bound. Positivity of \(t\) itself is neither asserted nor needed.

Let
\[
A=\sum_{j=1}^{\infty}j^{-2}=\pi^2/6,\qquad
B(z)=\prod_{j=1}^{\infty}
\frac{\sinh(z/j^2)}{z/j^2}.
\tag{29}
\]
Each factor is the Laplace transform of a uniform probability law on
\([-j^{-2},j^{-2}]\). The product is the Laplace transform of their independent, absolutely convergent sum, supported in \([-A,A]\). It is entire, \(B(0)=1\), and \(B(s)>0\) for real \(s\).

For any complex \(w\),
\[
\left|\frac{\sinh w}{w}\right|
\le e^{|\operatorname{Re}w|}
\min\{1,|w|^{-1}\}.
\tag{30}
\]
The first bound follows from the integral representation of \(\sinh w/w\); the second uses
\(|\sinh(u+iv)|^2=\sinh^2u+\sin^2v\le\cosh^2u\).
For \(n=\lfloor\sqrt{|z|}/2\rfloor\), the first \(n\) minimum factors in (30) are at most \(1/4\). Thus
\[
|B(z)|\le C\exp\{A|\operatorname{Re}z|-c\sqrt{|z|}\}.
\tag{31}
\]
This is a full complex-plane estimate, not just a bound on the imaginary axis.

Let \(r_n=2^{2^n}\), \(H_n=e^{r_n^2}\), \(\delta_n=e^{-H_n}\), and
\[
Q(z)=\prod_{n=1}^{\infty}
\frac{(z-r_n)^2+\delta_n^2}{r_n^2+\delta_n^2}.
\tag{32}
\]
The product converges uniformly on compact subsets because
\(\sum_n r_n^{-1}<\infty\). Each factor is strictly positive for real \(z\), its deviations from one are summable at every fixed real \(z\), and no factor vanishes there. Therefore \(Q(s)>0\) for real \(s\), with \(Q(0)=1\).

The elementary bound
\[
\left|
\frac{(z-r_n)^2+\delta_n^2}{r_n^2+\delta_n^2}
\right|
\le (1+|z|/r_n)^2
\]
and \(r_n\ge2^n\) give
\[
|Q(z)|\le\exp\{C\log^2(2+|z|)\}.
\tag{33}
\]
To see this, split the logarithmic sum at
\(n=\lceil\log_2(2+|z|)\rceil\); the initial part is \(O(\log^2(2+|z|))\), and the remaining geometric tail is bounded.

Set \(L(z)=B(z)Q(z)\). Combining (31)–(33), for every integer \(k\ge0\),
\[
|L(z)|\le C_k(1+|z|)^{-k}
e^{A|\operatorname{Re}z|}.
\tag{34}
\]
The standard smooth Paley–Wiener theorem, applied to \(L(i\xi)\), now yields a real \(t\in C_c^\infty([-A,A])\) whose bilateral Laplace transform is \(L\). Reality follows from \(L(\overline z)=\overline{L(z)}\). One also has \(L(0)=1\) and \(L(s)>0\) for every real \(s\).

At \(s=r_n\), the \(n\)-th factor in (32) is
\(\delta_n^2/(r_n^2+\delta_n^2)\). Apply (33)'s product estimate to the other factors and \(B(r_n)\le e^{Ar_n}\):
\[
0<L(r_n)
\le\exp\{-2H_n+Ar_n+C\log^2(2+r_n)\}
\le e^{-H_n}
\tag{35}
\]
for all sufficiently large \(n\).
Consequently there are no \(\eta,b>0\) with
\(L(s)\ge\eta e^{-b|s|}\) for every real \(s\).

The theorem above still produces a radial—in one dimension, even—smooth strictly log-concave probability density \(p\in\mathscr E\) with \(t*p>0\) everywhere. This example separates the new hypothesis from the exponential-margin sufficient condition in the supplied attachment.

In fact, no scalar noise density bounded above in both tails by
\[
p(x)\le C e^{-c|x|\log|x|}
\quad\text{for any fixed }c>0
\tag{35a}
\]
can regularize this particular \(t\).
To prove this, suppose \(\nu\) is any probability noise with all exponential moments and \(M=t*\nu\) is positive. The cutoff proof gives
\(\mathcal L_M(s)=\mathcal L_\nu(s)L(s)\), and \(M\) has total mass one. Some finite interval \([-D,D]\) carries at least half its mass, so
\[
\mathcal L_M(s)\ge\tfrac12 e^{-D s}\qquad(s\ge0).
\]
With \(K_\nu=\log\mathcal L_\nu\), (35) implies
\[
K_\nu(r_n)\ge H_n-Dr_n-\log2
=e^{r_n^2}-O(r_n).
\tag{35b}
\]
On the other hand, (35a) implies, for any \(0<c'<c\),
\[
K_\nu(s)\le C_1+C_2e^{s/c'}\qquad(s\ge0).
\tag{35c}
\]
Indeed, optimize \(sr-c'r\log r\) to obtain
\(\sup_{r>0}(sr-c'r\log r)=c'e^{s/c'-1}\), and integrate the remaining factor
\(e^{-(c-c')r\log r}\); a bounded central interval contributes only \(e^{O(s)}\).
Equations (35b)–(35c) contradict each other.
Thus the whole fixed positive-coefficient \(r\log r\) upper-tail class can be insufficient for general compact smooth Laplace-positive inputs, although it suffices under the supplied quantum exponential-margin hypotheses.

## 8. Singular matrix masses: the exact extension

For a compact \(\operatorname{Herm}_d\)-valued distribution without the normalization \(T(1)=I\), there is an admissible positive probability \(p\) with \(T*p\succeq0\) if and only if

1. \(\mathcal L_T(g)\succeq0\) for every real \(g\); and
2. \(\ker\mathcal L_T(g)\) is independent of \(g\).

The zero distribution is included.

For necessity with an admissible smooth density, \(Q=T(1)=\int M\succeq0\). For \(v\in\ker Q\), the continuous nonnegative scalar function \(v^*M(x)v\) has integral zero and vanishes everywhere. Positivity then gives \(M(x)v=0\). For \(v\notin\ker Q\), its positive total mass makes its exponentially weighted integral strictly positive. Equation (8) therefore yields
\(\ker\mathcal L_T(g)=\ker Q\).
For an arbitrary probability measure with all exponential moments, the cutoff argument of Section 3 gives the same moment identity and normalization of the positive output matrix measure, so the identical kernel argument applies.

For sufficiency, let \(K\) be the fixed kernel. Each Laplace transform annihilates \(K\), so every corresponding component of the distribution vanishes: the entire Laplace transform is zero on \(\mathbb R^m\), hence identically zero by iterating the one-variable identity theorem; uniqueness of the Fourier transform then applies. Compress to \(K^\perp\), conjugate by the inverse square root of the positive-definite compressed \(T(1)\), apply the normalized theorem, and conjugate back.

Pointwise semidefinite Laplace positivity alone is insufficient. For example,
\[
\mathcal L_T(g)=
\begin{pmatrix}1&g\\g&g^2\end{pmatrix}
\succeq0
\]
is the transform of a distribution supported at zero, but its kernel varies with \(g\). In distribution notation,
\[
T=\begin{pmatrix}\delta&-\delta'\\-\delta'&\delta''\end{pmatrix},
\qquad
T*p=\begin{pmatrix}p&-p'\\-p'&p''\end{pmatrix}.
\]
A positive output would have \(p''\ge0\) and \(\int p''=0\), so \(p''=0\), incompatible with a positive integrable probability density.

## 9. Polynomial and family consequences

If a Hermitian matrix polynomial \(P(g)=\sum_\alpha P_\alpha g^\alpha\) satisfies \(P(g)\succ0\) for all real \(g\), then
\[
T=\sum_\alpha(-1)^{|\alpha|}P_\alpha\partial^\alpha\delta
\]
has real Laplace transform \(P(g)\). After normalizing \(P(0)\), the theorem gives a radial strictly log-concave \(p\in\mathscr E\) such that
\[
P(-\partial)p(x)\succ0\qquad\text{for every }x.
\tag{36}
\]
This is an existence representation for positive polynomial symbols. It is not an algorithm for deciding polynomial positivity.

The same \(q,L\) work for a family \(\{T_\omega\}\) if that family has common support, common finite-order seminorm bound, and
\[
\inf_{\omega,\,|g|\le t}
d_C(\mathcal L_{T_\omega}(g))>0
\quad\text{for every finite }t.
\]
The original bounded quantum tuples have the special transform \(e^{A(g)}\) and explicit exponential margins; their supplied candidate is recovered at the level of existence.

No single fixed density works for every normalized Laplace-positive compact distribution without uniform seminorm/margin bounds. Already
\(T_a=\delta+a\delta''\) has \(\mathcal L_{T_a}(g)=1+ag^2>0\) for all \(a>0\). A fixed smooth positive integrable \(p\) has \(p''<0\) somewhere—otherwise it would be convex and integrable—and \(p+ap''\) is negative there for sufficiently large \(a\).

## 10. Provenance, novelty, and significance

The attachment supplied the retain-the-tilt operation with an explicit exponential positivity margin. The equivalence, arbitrary-margin threshold construction, ordered-space form, singular-matrix classification, and deep-valley example above were reconstructed here. None of the attachment's Pauli obstruction, endpoint-gamma example, numerical checks, or practical claims are premises of this proof.

Related work must be credited. Positive convolution multipliers have a long history. Katkova and Vishnyakova's 2001 Theorems 1–2 treat scalar one-dimensional functions with positive bilateral Laplace transform and positive endpoint neighborhoods; a Poisson-lattice convolution makes them nonnegative. Their multiplier is not radial or log-concave and their theorem has endpoint hypotheses. They cite Diamond and Essén (1978), whose precise scope still needs direct comparison. The finite lattice problem is related to Poincaré–Pólya–Handelman positivity multipliers and boundary faces. These precedents mean the general idea of repairing signs by positive convolution is not new.

The candidate structural contribution is the exact criterion for arbitrary compact distributions with cone values, together with a scalar radial strictly log-concave regularizer carrying every exponential moment and no quantitative lower-margin hypothesis. Historical priority for that full statement is unresolved. The proof is internally complete subject to standard distribution and Paley–Wiener theorems, but has not received independent mathematical review.

The construction may require enormous thresholds \(S_n\), and it queries or presupposes lower margins on entire compact \(g\)-balls. It establishes neither an efficient compiler nor a variance optimum, stable deconvolution, statistical advantage, or a major physical capability. It is a general representation theorem, with potential relevance to ordered distributions and constant-coefficient differential operators, rather than evidence that Astra's ambitious capability goal has been achieved.

Primary sources retrieved:

- O. M. Katkova and A. M. Vishnyakova, A Continual Analogue of a Theorem by M. Fekete and G. Pólya, Positivity 5 (2001), 1–11. DOI: https://doi.org/10.1023/A:1009847605313 . Author/institutional full text: https://ekhnuir.karazin.ua/bitstreams/41e252c6-eba5-435f-bbbb-66a8582ace7e/download .
- H. G. Diamond and M. Essén, Functions with non-negative convolutions, Journal of Mathematical Analysis and Applications 63 (1978), 463–489. DOI: https://doi.org/10.1016/0022-247X(78)90091-4 . Bibliography verified through the preceding primary paper; direct theorem comparison remains outstanding.
- T. Kepka and M. Korbelář, The lowest-degree polynomials with non-negative coefficients (2012), https://arxiv.org/abs/1210.6868 . Used only to qualify the classical polynomial precursor.
- R. Schwonnek and R. F. Werner, Properties of the Wigner distribution for n arbitrary operators (2018), https://arxiv.org/abs/1802.08343 . The general all-linear-marginal Wigner representation predates this investigation.
