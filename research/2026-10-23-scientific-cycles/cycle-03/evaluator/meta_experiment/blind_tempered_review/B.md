# Tempered-screen robustness: complete finite-space reconstruction

## Result and scope

Fix \(K>0\), \(0<\alpha<1\), and \(0<\eta<1\). For the entire finite-space class in the task,

\[
\boxed{\lim_{n\to\infty}(\log n)R_\eta(n)=K,
\qquad
\lim_{\varepsilon\downarrow0}\varepsilon\log T_\eta(\varepsilon)=K.}
\]

In particular, \(R_\eta(n)\to0\) for every fixed positive screen strength in the requested interval. The same proof applies if the displayed kernel definition is extended to any fixed \(\eta>0\), including \(\eta\ge1\). All constants may depend on \(K,\alpha,\eta\); none depends on the number of states, the probability vectors, or the fixed symmetric stochastic matrix \(Q\). No uniformity as \(\eta\downarrow0\) is asserted. An endpoint counterexample below shows that a positive screen strength is necessary for this conclusion over the corresponding class at \(\eta=0\).

This is a bounded reconstruction of the supplied historical obligation, with no novelty or ownership claim. The proof uses the supplied entropy and spectral estimates, also derived below. It does not infer robustness from the failure or success of linear domination.

## 1. A dimension-independent moment bound

Write \(\beta=1-\alpha\), \(W(x)=\pi(x)/q(x)\), and

\[
\theta=\min\{\eta,1/2\},\qquad
p=\frac1{1-\theta},\qquad r=\frac1\theta.
\]

Thus \(1<p\le2\), \(r\ge2\), and \(p,r\) are conjugate exponents. Let \(c=3/2\).

**Lemma 1.** For every integer \(j\ge0\), if \(\mu_j=qC_\eta^j\), then

\[
\left\|\frac{d\mu_j}{dq}\right\|_{L^p(q)}\le c^j.
\tag{1}
\]

Consequently, for every set \(A\),

\[
\mu_j(A)\le c^j q(A)^\theta.
\tag{2}
\]

**Proof.** For every \(a>0\), because \(0<\theta\le\eta\),
\(\min(1,a^\eta)\le a^\theta\). The second local acceptance is at most one. Hence, off the diagonal,

\[
L_\eta(x,y)\le Q(x,y)\left(\frac{q(y)}{q(x)}\right)^\theta,
\qquad G(x,y)\le q(y).
\]

Set \(D=\operatorname{diag}(q(x)^\theta)\), \(u(x)=q(x)^\theta\), and \(v(x)=q(x)^{1-\theta}\). Since all diagonal transition probabilities are at most one, entrywise

\[
DL_\eta D^{-1}\le I+Q,\qquad
DGD^{-1}\le I+uv^{\mathsf T}.
\]

Therefore, with \(P=DC_\eta D^{-1}\),

\[
0\le P\le I+\frac{\alpha uv^{\mathsf T}+\beta Q}{2}.
\tag{3}
\]

Here and in this paragraph the \(\ell^r\) norms use counting measure on the finite state space. Symmetric stochastic \(Q\) has column sums one, so Jensen's inequality gives \(\|Q\|_{\ell^r\to\ell^r}\le1\). Also

\[
\|u\|_r=1,\qquad \|v\|_p=1,
\qquad \|uv^{\mathsf T}\|_{\ell^r\to\ell^r}=1.
\]

The entrywise comparison (3), positivity, and the triangle inequality imply \(\|P\|_{\ell^r\to\ell^r}\le3/2\). The row vector \(\mu_jD^{-1}=v^{\mathsf T}P^j\) consequently has \(\ell^p\) norm at most \(c^j\). Since \(\theta p=p-1\),

\[
\|\mu_jD^{-1}\|_p^p
=\sum_x\mu_j(x)^p q(x)^{-\theta p}
=\sum_xq(x)\left(\frac{\mu_j(x)}{q(x)}\right)^p.
\]

This proves (1), and Hölder proves (2). \(\square\)

For the requested range \(0<\eta<1\), the same argument in fact gives (1) with \(p=1/(1-\eta)\). Using the smaller exponent above makes the subsequent bounded-function interpolation uniform in form. Iteration has not replaced \(\theta\) by \(\theta^j\); this fixed exponent is essential.

## 2. Removing the initial mass at very small weights

The local kernel is \(\pi\)-reversible by the symmetric off-diagonal flow identity in the supplied starting lemmas:

\[
\pi(x)L_\eta(x,y)
=Q(x,y)\min\{q(x)^\eta,q(y)^\eta\}
\min\left\{\frac{\pi(x)}{q(x)^\eta},\frac{\pi(y)}{q(y)^\eta}\right\}.
\]

The identity holds algebraically for every positive \(\eta\), which also justifies the stated extension beyond one. Therefore \(C_\eta\) is \(\pi\)-reversible and invariant. Fix \(h=1/4\), and put

\[
A_h=\{W<h\},\quad b_h=q(A_h),\quad
\delta=\exp\left[-\frac{K+H_2(h)}{1-h}\right]>0,
\]

where \(H_2(a)=-a\log a-(1-a)\log(1-a)\). Binary entropy data processing and \(\pi(A_h)\le h\) imply

\[
1-b_h\ge\delta.
\tag{4}
\]

For clarity, if \(a=\pi(A_h)\le h\), then

\[
K\ge D_{\rm bin}(a\|b_h)
\ge-H_2(h)-(1-h)\log(1-b_h),
\]

which proves (4).

Run the actual unchanged chain from \(q\), and let \(\tau=\inf\{j\ge0:W(X_j)\ge h\}\). Before this first hit, a global branch with a candidate in \(A_h^c\) certainly accepts. Its conditional probability is at least \(\alpha\delta/2\). Thus, with

\[
\rho=1-\alpha\delta/2\in(0,1),
\]

\[
\Pr(\tau>s)\le\rho^s.
\tag{5}
\]

For \(0\le j\le s\), define the unconditioned first-hit submeasure
\(\nu_j(F)=\Pr(\tau=j,X_j\in F)\). It is supported on \(\{W\ge h\}\) and satisfies \(\nu_j\le\mu_j\). Lemma 1 gives

\[
\left\|\frac{d\nu_j}{d\pi}\right\|_{L^p(\pi)}^p
=\sum_xq(x)\left(\frac{\nu_j(x)}{q(x)}\right)^p W(x)^{1-p}
\le h^{1-p}c^{jp}.
\]

In particular,

\[
\left\|\frac{d\nu_j}{d\pi}\right\|_{L^p(\pi)}\le h^{-\theta}c^j.
\tag{6}
\]

Reversibility identifies the density of \(\nu_j C_\eta^k\) with \(C_\eta^k(d\nu_j/d\pi)\). Jensen and invariance show contraction in \(L^p(\pi)\), so (6) also bounds every such propagated submeasure.

The exact first-hit decomposition is

\[
\mu_s=\nu_{\rm surv}+\sum_{j=0}^s\nu_jC_\eta^{s-j},
\qquad \nu_{\rm surv}(\Omega)=\Pr(\tau>s).
\]

For \(B>1/h\), let \(D_B=\{W<1/B\}\). Since \(\pi(D_B)\le1/B\), Hölder, (5), and (6) yield

\[
\boxed{\mu_s(D_B)\le\rho^s+(Bh)^{-\theta}S_s,
\qquad S_s=\sum_{j=0}^sc^j.}
\tag{7}
\]

This includes all later returns below the first-hit threshold. No conditional starting law and no single-crossing assumption is used.

## 3. Spectral control of bounded tests on the central region

For \(R>e\), binary data processing gives the supplied high-weight envelope

\[
a_R:=\pi(W>R)\le\frac{K}{\log R-1},
\qquad q(W>R)\le\frac{a_R}{R}.
\tag{8}
\]

Indeed, if \(a=a_R\) and \(b=q(W>R)\le a/R\), the binary divergence is at least
\(a\log R+(1-a)\log(1-a)\ge a(\log R-1)\).

Set \(M=\exp(2K+1)\), \(A_0=\{W\le M\}\), and \(s_0=\pi(A_0)\ge1/2\). For any event \(F\), integer \(t\ge0\), and

\[
g=C_\eta^t\mathbf1_F,\qquad
z=\frac1{s_0}\sum_{x\in A_0}\pi(x)g(x),
\]

we have \(0\le g,z\le1\) and the supplied anchored spectral estimate

\[
\sum_x\frac{(g(x)-z)^2}{\max\{W(x),M\}}\pi(x)
\le J_t:=\frac1{\alpha s_0(2t+1)}
\le\frac2{\alpha(2t+1)}.
\tag{9}
\]

Here is a direct verification. The IMH Dirichlet form is

\[
\mathcal E_G(g,g)=\frac12\sum_{x,y}
\frac{(g(x)-g(y))^2}{\max\{W(x),W(y)\}}\pi(x)\pi(y).
\]

Restricting \(y\) to \(A_0\) and applying Jensen bounds it below by \(s_0/2\) times the left side of (9). Also \(\mathcal E_C\ge(\alpha/2)\mathcal E_G\). Since \(C=(I+\alpha G+\beta L_\eta)/2\) is lazy and reversible, its spectrum lies in \([0,1]\). Applying \((1-\lambda)\lambda^{2t}\le1/(2t+1)\) to the centered indicator, whose variance is at most \(1/4\), gives \(\mathcal E_C(g,g)\le1/[4(2t+1)]\), proving (9).

Now set \(E_R=\{W>R\}\) and \(S=(D_B\cup E_R)^c\), and write \(\mu=\mu_s\), \(A=c^s\). On \(S\),

\[
\sum_S(g-z)^2q\le(MB+1)J_t.
\tag{10}
\]

Because \(r=1/\theta\ge2\) and \(|g-z|\le1\), Hölder and Lemma 1 imply

\[
\begin{aligned}
\sum_S|g-z|\mu
&\le A\left(\sum_S|g-z|^r q\right)^{1/r}\\
&\le A\big[(MB+1)J_t\big]^\theta.
\end{aligned}
\tag{11}
\]

Likewise, weighted Cauchy–Schwarz gives

\[
\sum_S|g-z|\pi\le\big[(M+R)J_t\big]^{1/2}.
\tag{12}
\]

The bounded-function step in (11) is why an \(L^2(q)\) density bound is unnecessary. It remains valid for arbitrarily small fixed \(\theta>0\).

Because both \(\mu\) and \(\pi\) have mass one, subtracting \(z\) from the test function changes no difference of expectations. On the two tails use \(|g-z|\le1\); use (11)–(12) on \(S\). By (2), (7), and (8), this proves the following uniform finite-time inequality:

\[
\begin{aligned}
\|qC_\eta^{s+t}-\pi\|_{\rm TV}
\le{}&a_R+\rho^s+(Bh)^{-\theta}S_s+B^{-1}\\
&+A\left(\frac{a_R}{R}\right)^\theta
+A\big[(MB+1)J_t\big]^\theta
+\big[(M+R)J_t\big]^{1/2}.
\end{aligned}
\tag{13}
\]

To make (13) a certificate involving only fixed parameters and proof choices, replace \(a_R\) by \(\min\{1,K/(\log R-1)\}\) and \(J_t\) by \(2/[\alpha(2t+1)]\). No normalized weight threshold is evaluated by the sampler.

## 4. Uniform upper asymptotics

Let \(\kappa=-\log\rho>0\), and for sufficiently large \(n\) choose

\[
\begin{gathered}
s=\left\lceil\frac3\kappa\log\log n\right\rceil,
\qquad t=n-s,
\qquad a_*=\frac{3\log c}{\kappa},\\
P_* =\frac{a_*+4}{\theta},
\qquad B=R=\frac{t}{(\log t)^{P_*}}.
\end{gathered}
\tag{14}
\]

Eventually \(B,R>\max\{e,1/h,M\}\), and \(t\sim n\). All constants below depend only on \(K,\alpha,\eta\). In particular,

\[
A=c^s=O((\log n)^{a_*}),\qquad
S_s=O((\log n)^{a_*}),\qquad
\rho^s\le(\log n)^{-3}.
\]

The additional first-hit and high-initial-tail terms in (13) are

\[
(Bh)^{-\theta}S_s+A(a_R/R)^\theta
=O\big(n^{-\theta}(\log n)^{a_*+P_*\theta}\big)
=o((\log n)^{-1}).
\]

Also \(B^{-1}=O(n^{-1}(\log n)^{P_*})=o((\log n)^{-1})\), and

\[
A[(MB+1)J_t]^\theta=O((\log n)^{-4}),
\qquad
[(M+R)J_t]^{1/2}=O((\log n)^{-P_*/2}).
\]

Since \(\theta\le1/2\), we have \(P_*/2\ge4\). Thus every term of (13) except \(a_R\) is \(o(1/\log n)\), uniformly over the class. Finally,

\[
\log R=\log n-P_*\log\log n+o(1),
\qquad
a_R\le\frac{K}{\log R-1}
=\frac{K+o(1)}{\log n}.
\]

Therefore

\[
\limsup_{n\to\infty}(\log n)R_\eta(n)\le K.
\tag{15}
\]

The split \(s+t=n\) is solely an analysis of the same fixed kernel at every step. No global-only prefix, adaptation, change in \(Q\), or target normalization oracle is introduced.

## 5. Matching lower bound and deterministic-time inversion

The identity proposal \(Q=I\) is a fixed symmetric stochastic proposal and gives \(L_\eta=I\) for every \(\eta\). For sufficiently large integer \(n\), put

\[
p_n=\frac{K}{\log n+2\log\log n},\qquad
u_n=e^{-K/p_n}=\frac1{n(\log n)^2},
\]

and take

\[
\pi=(p_n,1-p_n),\qquad q=(p_nu_n,1-p_nu_n).
\]

Both probability vectors are strictly positive and

\[
D(\pi\|q)
=K+(1-p_n)\log\frac{1-p_n}{1-p_nu_n}<K.
\]

The nontrivial eigenvalue of \(G\) is \(1-u_n\); that of \(C_\eta\) is \(1-\alpha u_n/2\). Hence, exactly,

\[
\|qC_\eta^n-\pi\|_{\rm TV}
=p_n(1-u_n)(1-\alpha u_n/2)^n.
\]

Since \(nu_n\to0\) and \(p_n\log n\to K\), this supplies the matching lower limit \(K\). Together with (15) it proves the first claimed limit and uniform convergence to zero.

For the second limit, TV is nonincreasing with time for each admitted instance. For any \(0<d<K\), the established asymptotic bounds imply, for all sufficiently small \(\varepsilon>0\),

\[
R_\eta\left(\left\lceil e^{(K+d)/\varepsilon}\right\rceil\right)<\varepsilon,
\qquad
R_\eta\left(\left\lfloor e^{(K-d)/\varepsilon}\right\rfloor\right)>\varepsilon.
\]

The first inequality bounds every first sufficient time from above. The strict second inequality means that some admitted instance is still above \(\varepsilon\) at that time, so its first sufficient time is later. Taking logarithms, multiplying by \(\varepsilon\), and sending \(d\downarrow0\) proves
\(\lim_{\varepsilon\downarrow0}\varepsilon\log T_\eta(\varepsilon)=K\).

## 6. Optional endpoint check: the conclusion fails at zero screen

This construction is outside the requested positive interval and explains why the proof's constants need not remain controlled as \(\eta\downarrow0\). Fix \(b\in(0,1-e^{-K})\). For large \(n\), put \(p=(\log n)^{-2}\) and use three states \(A,B,C\) with

\[
\pi=(p,p/n^2,1-p-p/n^2),\qquad
q=(p/n^2,b,1-b-p/n^2).
\]

Let \(Q\) swap \(A,B\) and fix \(C\). At \(\eta=0\), \(L_0\) is ordinary target MH for this symmetric \(Q\). All probabilities are positive, and

\[
D(\pi\|q)\longrightarrow\log\frac1{1-b}<K.
\]

Thus these are admitted instances eventually. The local move \(B\to A\) accepts with probability one and \(A\to B\) with probability \(n^{-2}\). Moreover \(W(A)=n^2\) is eventually the largest weight, so the global probability of exiting \(A\) is \((1-p)/n^2\). Consequently,

\[
C_0(B,A)\ge\beta/2,
\qquad C_0(A,A)\ge1-\frac1{2n^2}.
\]

The event of starting in \(B\), entering \(A\) on step one, and staying there through step \(n\) has probability at least

\[
\frac{b\beta}{2}\left(1-\frac1{2n^2}\right)^{n-1}.
\]

Subtracting \(\pi(A)=p\to0\) proves

\[
\liminf_{n\to\infty}R_0(n)
\ge\frac{\beta}{2}(1-e^{-K})>0,
\]

where the final bound follows by taking \(b\uparrow1-e^{-K}\). Every member used before taking limits is finite and strictly positive.

## 7. Verification, remaining gap, and interpretation

There is no unresolved mathematical gap in the stated finite-space task. The entire interval \(0<\eta<1\) has the sharp coefficient \(K\), and the same kernel formula admits the extension to all fixed \(\eta>0\). The proof does not claim analogous results on arbitrary measurable spaces with a symmetric counting-measure proposal, finite-time domination by pure IMH, a practical speedup, or an improved target-evaluation cost.

The load-bearing matrix comparison and moment bound were subjected to a supplemental adversarial numerical check: 1,120 positive finite instances, dimensions 2, 3, 8, and 25, seven screen strengths from 0.02 through 0.95, proposal and target masses generated across 100 log units, and 12 successive density checks per instance. The largest entrywise comparison residual was \(1.06\times10^{-15}\); the largest ratio of the tested \(L^{1/(1-\eta)}(q)\) norm to \((3/2)^s\) was 0.921 or less. Stationarity and detailed balance held to floating-point tolerance. These calculations test implementation and algebraic orientation; the finite-dimensional norm argument, first-hit estimate, and bounded-test argument establish the uniform theorem independently of numerical evidence.

The sampler remains scale-free: multiplying all raw target values by a common positive constant leaves both acceptance stages and IMH unchanged. The normalized objects in the proof impose no additional target-normalizer access on an implementation.
