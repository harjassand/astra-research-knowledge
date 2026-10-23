# Tempered screen robustness: complete uniform result

## Outcome and scope

For every fixed \(K>0\), \(0<\alpha<1\), and **every fixed \(0<\eta<1\)** in the stated finite-space class,

\[
\boxed{\lim_{n\to\infty}(\log n)R_\eta(n)=K,
\qquad \lim_{\varepsilon\downarrow0}\varepsilon\log T_\eta(\varepsilon)=K.}
\]

In particular, \(R_\eta(n)\to0\) for every positive tempering exponent in the question. Thus the interval proved is the entire requested interval. The same conclusion holds at \(\eta=1\), and also for \(\eta>1\) if the displayed kernel definition is extended there. At \(\eta=0\), uniform convergence fails; an explicit positive three-state family is given below.

All suprema allow the finite labelled space, its size, its positive probabilities, and its symmetric stochastic \(Q\) to vary. Every individual instance uses one fixed kernel throughout. Constants below depend only on the fixed \(K,\alpha,\eta\); none depend on the instance or its number of states. No normalizing constant is used by the sampler.

This is a bounded historical reconstruction. No novelty, ownership of the underlying scientific programme, practical speedup, or external acceptance is asserted. The supplied `SAFE_LOCAL_THEOREM.md` supplies the entropy and spectral-anchor ingredients; they are restated with their short proofs here. The supplied `TEMPERED_STARTING_LEMMAS.md` correctly rules out uniform linear domination, but that condition is not needed below.

## 1. A change of representation prevents exponent degradation

Write \(\beta=1-\alpha\), \(\rho=1+\beta/2\), and let row vectors denote measures. Define

\[
D=\operatorname{diag}(q(x)^\eta),\qquad
M=D^{-1}QD,\qquad J(x,y)=q(y).
\]

Here \(M\) is only a nonnegative matrix, not a Markov kernel. Crucially,

\[
M^k=D^{-1}Q^kD.
\tag{1}
\]

Because \(Q\) is symmetric stochastic, every \(Q^k\) has row and column sums one. For every set \(A\) and integer \(k\ge0\), Hölder's inequality on pairs \((x,y)\), restricted to \(y\in A\), gives

\[
\begin{aligned}
(qM^k)(A)
&=\sum_x\sum_{y\in A}
 Q^k(x,y)q(x)^{1-\eta}q(y)^\eta\\
&\le
 \left(\sum_x\sum_{y\in A}Q^k(x,y)q(x)\right)^{1-\eta}
 \left(\sum_x\sum_{y\in A}Q^k(x,y)q(y)\right)^\eta\\
&=[qQ^k(A)]^{1-\eta}q(A)^\eta
\le q(A)^\eta.
\end{aligned}
\tag{2}
\]

The inequality also holds for \(k=0\), when the left side is \(q(A)\).

The local first-stage acceptance is at most \((q(y)/q(x))^\eta\), and its second stage is at most one. All off-diagonal global transitions are at most \(q(y)\). Diagonal probabilities are at most one. Therefore, entrywise,

\[
L_\eta\le I+M,\qquad G\le I+J,\qquad
C_\eta\le I+\frac\alpha2J+\frac\beta2M.
\tag{3}
\]

Let \(\mu_j=qC_\eta^j\). Since \(\mu_j\) has total mass one, \(\mu_jJ=q\). Positivity and induction applied to (3) yield

\[
\mu_s\le q(I+\tfrac\beta2M)^s
 +\frac\alpha2\sum_{j=0}^{s-1}q(I+\tfrac\beta2M)^j.
\]

Expanding the powers and applying (2) proves, for every set \(A\),

\[
\boxed{\mu_s(A)\le A_s q(A)^\eta,\qquad
A_s=\rho^s+\frac\alpha\beta(\rho^s-1)
=\frac{\rho^s-\alpha}{\beta}\le\frac{\rho^s}{\beta}.}
\tag{4}
\]

The exponent remains **\(\eta\), independently of time**. The telescoping diagonal conjugation in (1), together with the rank-one reset \(\mu_jJ=q\), is the load-bearing representation change. Merely applying a nonlinear one-step bound repeatedly would not supply this result.

## 2. Nonlinear set bounds survive invariant evolution

Suppose a finite positive measure \(\nu\) satisfies

\[
\nu(A)\le c\,\pi(A)^\eta\quad\text{for every set }A.
\]

For any function \(0\le f\le1\), layer cake and concavity give

\[
\nu(f)=\int_0^1\nu(f>u)\,du
\le c\int_0^1\pi(f>u)^\eta\,du
\le c\,\pi(f)^\eta.
\tag{5}
\]

Consequently, if \(P\) preserves \(\pi\), then

\[
(\nu P)(A)\le c\,\pi(A)^\eta.
\tag{6}
\]

Neither \(\nu\) nor its bound needs to be a probability measure. This observation controls every return after a first entrance; it does not assume a path crosses a threshold only once.

## 3. A first-entrance estimate removes the low-weight mass

Set \(W(x)=\pi(x)/q(x)\), \(h=1/2\), and \(B_h=\{W\ge h\}\). We have \(\pi(B_h)\ge1/2\). Binary relative-entropy data processing gives, with \(p=\pi(B_h)\) and \(b=q(B_h)\),

\[
K\ge p\log(1/b)-H_2(p)
\ge\tfrac12\log(1/b)-\log2.
\]

Thus

\[
q(B_h)\ge c_K:=e^{-2K}/4.
\tag{7}
\]

Let \(\tau=\inf\{j\ge0:W(X_j)\ge h\}\) for the actual unchanged chain started from \(q\). While \(\tau>j\), a global branch and a proposal in \(B_h\) is accepted. Its conditional probability is at least \(\alpha c_K/2\). Put

\[
\theta=1-\alpha c_K/2\in(0,1),\qquad
\kappa=-\log\theta>0.
\]

It follows that \(\Pr(\tau>s)\le\theta^s\). Define the unconditioned first-entrance submeasure

\[
\nu_j(A)=\Pr(\tau=j,X_j\in A).
\]

Using (4), its support in \(B_h\), and \(q\le\pi/h\) on \(B_h\),

\[
\nu_j(A)\le A_j\,[q(A\cap B_h)]^\eta
\le A_jh^{-\eta}\pi(A)^\eta.
\tag{8}
\]

The local flow formula in the supplied starting lemmas proves \(\pi\)-reversibility of \(L_\eta\); hence \(C_\eta\) preserves \(\pi\). Apply (6) to (8), and then use the exact first-entrance decomposition

\[
\mu_s=\nu_{\rm surv}+\sum_{j=0}^s\nu_jC_\eta^{s-j}.
\]

For \(D_B=\{W<1/B\}\), \(B>2\), this yields

\[
\boxed{d_s:=\mu_s(D_B)
\le\theta^s+(2/B)^\eta\sum_{j=0}^s A_j.}
\tag{9}
\]

Indeed \(\pi(D_B)\le1/B\). Since \(\rho>1\),

\[
\sum_{j=0}^s A_j\le
\frac{\rho^{s+1}}{\beta(\rho-1)}.
\tag{10}
\]

All local entrances, rejected moves, and subsequent returns are included in this argument.

## 4. An initial-law estimate from a nonlinear set bound

For \(R>e\), the entropy tail envelope is

\[
a_R:=\pi(W>R)\le\frac{K}{\log R-1}.
\tag{11}
\]

To verify it, \(q(W>R)\le a_R/R\), and binary divergence is at least
\(a_R\log R+(1-a_R)\log(1-a_R)\ge a_R(\log R-1)\).

Put \(M_0=e^{2K+1}\), \(E_0=\{W\le M_0\}\), and \(s_0=\pi(E_0)\ge1/2\). For a test event \(F\), write

\[
g=C_\eta^t1_F,\qquad z=s_0^{-1}\sum_{x\in E_0}g(x)\pi(x).
\]

Both \(g\) and \(z\) lie in \([0,1]\). The inherited spectral-anchor estimate is

\[
\sum_x\frac{(g(x)-z)^2}{\max(W(x),M_0)}\pi(x)
\le\frac{1}{\alpha s_0(2t+1)}
\le\frac{2}{\alpha(2t+1)}.
\tag{12}
\]

For completeness, \(C_\eta\) is reversible and lazy, so its spectrum lies in \([0,1]\). The spectral theorem and \(\operatorname{Var}_\pi(1_F)\le1/4\) give
\(\mathcal E_C(g,g)\le1/[4(2t+1)]\), using \((1-u)u^{2t}\le1/(2t+1)\). Also \(\mathcal E_C\ge(\alpha/2)\mathcal E_G\). The IMH form is

\[
\mathcal E_G(g,g)=\frac12\sum_{x,y}
\frac{\pi(x)\pi(y)}{\max(W(x),W(y))}(g(x)-g(y))^2.
\]

Restricting its second index to \(E_0\) and applying Jensen proves
\(\mathcal E_G\ge(s_0/2)\sum_x\pi(x)(g(x)-z)^2/\max(W(x),M_0)\), establishing (12).

Now take any probability measure \(\mu\) satisfying

\[
\mu(A)\le A_*q(A)^\eta\quad\text{for every set }A.
\tag{13}
\]

Let \(D=\{W<1/B\}\), \(E=\{W>R\}\), and \(S=(D\cup E)^c\), with \(B,R>e\). Write \(v=|g-z|\le1\) and

\[
e_{B,t}=\frac{2M_0B}{\alpha(2t+1)}.
\]

On \(S\), \(\max(W,M_0)/W\le M_0B\), so (12) implies

\[
q(v^2 1_S)\le e_{B,t},\qquad
\pi(v1_S)\le
\sqrt{\frac{2\max(M_0,R)}{\alpha(2t+1)}}.
\tag{14}
\]

For every \(u>0\), Chebyshev and (13) give

\[
\mu(v1_S)\le u+\mu(S\cap\{v>u\})
\le u+A_*(e_{B,t}/u^2)^\eta.
\]

Choosing \(u=(A_*e_{B,t}^{\eta})^{1/(1+2\eta)}\) proves

\[
\mu(v1_S)\le2(A_*e_{B,t}^{\eta})^{1/(1+2\eta)}.
\tag{15}
\]

This remains valid if the chosen \(u\) exceeds one. Furthermore,

\[
\pi(D)\le B^{-1},\qquad \mu(E)\le A_*(a_R/R)^\eta.
\]

Since \(\mu\) and \(\pi\) have the same total mass, subtracting \(z\) from \(g\), splitting into \(D,S,E\), and using \(v\le1\) yields the following fully uniform bound:

\[
\boxed{
\begin{aligned}
\|\mu C_\eta^t-\pi\|_{\rm TV}
\le {}&a_R+\mu(D)+B^{-1}+A_*(a_R/R)^\eta\\
&+2(A_*e_{B,t}^{\eta})^{1/(1+2\eta)}
+\sqrt{\frac{2\max(M_0,R)}{\alpha(2t+1)}}.
\end{aligned}}
\tag{16}
\]

There is no unproved density bound in (16). In particular, it does not replace the nonlinear set bound by linear domination.

## 5. Uniform upper asymptotics for every fixed positive exponent

For sufficiently large integer \(n\), define

\[
\ell=\log n,\quad s=\lceil\sqrt\ell\rceil,\quad t=n-s,
\quad\lambda=\log\rho,\quad
c=\frac{\lambda+2}{\eta},\quad
B=R=t\exp(-c\sqrt\ell).
\tag{17}
\]

Eventually \(t>0\), \(B=R>\max(e,M_0)\), and \(t\sim n\). Equations (4) and (10) imply

\[
A_s=O(e^{\lambda\sqrt\ell}),\qquad
\sum_{j=0}^s A_j=O(e^{\lambda\sqrt\ell}).
\tag{18}
\]

The first-entrance bound (9) therefore gives

\[
d_s\le e^{-\kappa\sqrt\ell}
+O\!\left(n^{-\eta}e^{(2\lambda+2)\sqrt\ell}\right)
=o(1/\ell).
\tag{19}
\]

Take \(\mu=\mu_s\) and \(A_*=A_s\) in (16). Because \(B/t=e^{-c\sqrt\ell}\),

\[
A_s e_{B,t}^{\eta}=O(e^{-2\sqrt\ell}),
\]

so the first core error in (16) is
\(O(e^{-2\sqrt\ell/(1+2\eta)})=o(1/\ell)\). The other core error is
\(O(e^{-c\sqrt\ell/2})=o(1/\ell)\). Also

\[
B^{-1}=o(1/\ell),\qquad
A_s(a_R/R)^\eta
\le A_sR^{-\eta}
=O\!\left(n^{-\eta}e^{(2\lambda+2)\sqrt\ell}\right)
=o(1/\ell).
\tag{20}
\]

Finally,

\[
\log R=\ell-c\sqrt\ell+o(1),\qquad
\ell a_R\le\frac{K\ell}{\log R-1}=K+o(1).
\tag{21}
\]

Every error estimate is uniform over all admitted instances. Applying (16) to \(\mu_s C_\eta^t=qC_\eta^n\) proves

\[
\limsup_{n\to\infty}(\log n)R_\eta(n)\le K.
\tag{22}
\]

The split at \(s\) is only an analysis of the same fixed chain. It introduces neither a separate global prefix nor a change in transition rules. The constants become poor as \(\eta\downarrow0\), as is consistent with the endpoint obstruction below.

## 6. Matching lower bound and deterministic hitting-time inversion

Choose the symmetric proposal \(Q=I\), so \(L_\eta=I\) for every \(\eta\). For sufficiently large \(n\), let

\[
u=\frac1{n(\log n)^2},\qquad
p=\frac{K}{\log n+2\log\log n},\qquad
\pi=(p,1-p),\quad q=(pu,1-pu).
\]

All probabilities are positive, and

\[
D(\pi\|q)
=K+(1-p)\log\frac{1-p}{1-pu}<K.
\]

The two off-diagonal IMH probabilities sum to \(u\). Since the initial rare-state deficit is \(p(1-u)\), exact two-state evolution gives

\[
\|qC_\eta^n-\pi\|_{\rm TV}
=p(1-u)(1-\alpha u/2)^n.
\tag{23}
\]

We have \(nu\to0\) and \(p\log n\to K\). Thus (23) gives the matching liminf \(K\), proving the asserted limit and hence uniform convergence.

For the hitting-time statement, each fixed invariant kernel contracts total variation, so the distance from stationarity is nonincreasing. Given \(0<\delta<K\), the established asymptotic places \(R_\eta(n)\) eventually between
\((K-\delta/2)/\log n\) and \((K+\delta/2)/\log n\). At

\[
n_+=\lceil e^{(K+\delta)/\varepsilon}\rceil,
\qquad n_-=\lfloor e^{(K-\delta)/\varepsilon}\rfloor,
\]

the former upper bound is below \(\varepsilon\), while the latter lower bound is above \(\varepsilon\), for sufficiently small \(\varepsilon\). The upper bound applies to every instance. The lower bound ensures some admitted instance still has distance exceeding \(\varepsilon\) at \(n_-\), and hence its first sufficient deterministic time exceeds \(n_-\). Therefore

\[
K-\delta\le\liminf_{\varepsilon\downarrow0}\varepsilon\log T_\eta(\varepsilon)
\le\limsup_{\varepsilon\downarrow0}\varepsilon\log T_\eta(\varepsilon)
\le K+\delta.
\]

Letting \(\delta\downarrow0\) completes the inversion.

## 7. Boundary checks and an extension beyond the stated range

### Exponents at least one

For \(\eta\ge1\) and every \(r>0\), \(\min(1,r^\eta)\le r\). Consequently accepted incoming \(q\)-mass at \(y\) is at most

\[
\sum_x q(x)Q(x,y)\frac{q(y)}{q(x)}=q(y),
\]

using the column sums of \(Q\). Rejected mass is at most \(q(y)\), so \(qL_\eta\le2q\). The supplied accepted theorem applies with \(\Lambda=2\), while (23) supplies the same lower bound. Thus the result extends to all fixed \(\eta>0\) under the same formula.

### At zero, uniform convergence fails

Let \(k=K/4\), \(b=1-e^{-K/4}\), and, for large \(n\), set

\[
u=\frac1{n(\log n)^2},\qquad
p=\frac{k}{\log(1/u)},
\]

\[
q=(pu,b,1-b-pu),\qquad
\pi=(p,pu^2,1-p-pu^2).
\]

Label the states \(A,B,C\), and let \(Q\) interchange \(A,B\) while fixing \(C\). This is a fixed symmetric stochastic matrix. Every sufficiently large member is strictly positive. Directly,

\[
D(\pi\|q)\longrightarrow k+\log\frac1{1-b}=K/2<K,
\]

because the \(A\) term is exactly \(k\), the \(B\) term tends to zero, and the \(C\) term tends to \(\log(1/(1-b))\).

At \(\eta=0\), local \(B\to A\) acceptance is one, while local \(A\to B\) acceptance is \(u^2\). Also \(W(A)=1/u\), so the global escape probability from \(A\) is at most \(u\). Therefore

\[
qC_0^n(A)
\ge\frac{b\beta}{2}
 \left(1-\frac{\alpha u}{2}-\frac{\beta u^2}{2}\right)^{n-1}
\longrightarrow\frac{b\beta}{2}.
\]

Since \(\pi(A)=p\to0\),

\[
\liminf_{n\to\infty}R_0(n)
\ge\frac{(1-e^{-K/4})(1-\alpha)}2>0.
\tag{24}
\]

This also tests the necessity of keeping a strictly positive exponent in (2), (15), and (17).

## 8. Exact limits of the claim

The full mathematical obligation is resolved for the stated class. No theorem about dimension-dependent proposals without column sums one, approximate transitions, finite-precision implementations, a varying \(\eta\) tending to zero with time, or constants uniform in \(\alpha,K,\eta\) is asserted. The lower construction uses an admissible identity local proposal and establishes robustness, not a speedup over pure IMH. All target values appear in transition rules only through ratios, so multiplication of raw target values by a common positive constant changes none of the conclusions.
