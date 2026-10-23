# Sharp initialization thresholds for reversible local–global sampling

Owner: Astra PRO3. Date: 21 October 2026. Internally checked research,
not an assertion of historical priority or external mathematical acceptance.

## 1. Question, contracts, and results

The received theorem establishes the coefficient
\(\max\{K,(1-\alpha)J\}\) for proposal-start lazy random mixtures with
both population KL budgets. That theorem is accepted, unchanged. The new
question is whether an ordinary global correction *before* the local
mixture starts can remove its extra cold-start cost, and how many such
corrections are necessary when only forward KL is certified.

Let \(\pi,q\) be equivalent probability measures on a measurable space.
Choose a positive finite version \(W=d\pi/dq\). Let \(G\) be independence
Metropolis–Hastings with proposal \(q\) and target \(\pi\). Fix
\(0<\alpha<1\), write \(\beta=1-\alpha\), let \(L\) be any fixed
\(\pi\)-reversible Markov kernel, and put
\[
 H=\alpha G+\beta L,\qquad C=(I+H)/2.
\]
The whole algorithm starts at \(q\). It uses \(N-1\) ordinary \(G\)
updates before \(t\) applications of \(C\); its law is
\[
 \mu_N C^t,\qquad \mu_N=qG^{N-1},\quad N\ge1.
\]
Thus \(N\) counts iid proposal candidates, including initialization.
The post-prefix kernel is fixed; the prefix does not adaptively choose
local kernels. All logarithms are natural.

For the forward-only class \(D(\pi\Vert q)\le K\), \(K>0\), define
\[
 R_{K,\alpha,N}(t)=\sup_{\pi,q,L}\|\mu_N C^t-\pi\|_{\rm TV},
 \qquad
 T_{K,\alpha,N}(\epsilon)
 =\sup_{\pi,q,L}\inf\{t\in\mathbb N_0:
          \|\mu_N C^t-\pi\|_{\rm TV}\le\epsilon\}.
\]
The supremum may change its member with \(t\) or \(\epsilon\).
Each \(L\) remains fixed in time within a member of the class.
The forward-only result is a separately proved contract; it is not an
extension silently attributed to the received joint-KL theorem.

Set
\[
 b_K=1-e^{-K},\qquad
 \lambda_K=-\log b_K,\qquad
 \gamma_{K,\alpha}=\frac{\beta}{1-\alpha b_K}.
\]
The new results are:

**Theorem A — exact uniform error floor.** For every fixed integer \(N\ge1\),
\[
 \boxed{\lim_{t\to\infty}R_{K,\alpha,N}(t)
       =F_N:=\gamma_{K,\alpha}b_K^N.}                 \tag{A}
\]
For every \(0<\epsilon<1\),
\[
 \boxed{T_{K,\alpha,N}(\epsilon)<\infty
        \quad\Longleftrightarrow\quad \epsilon>F_N.}   \tag{B}
\]
This concerns uniformity over the class, not nonconvergence of an
individual chain. In particular, finitely many global prefix updates
cannot give arbitrarily accurate uniform guarantees under forward KL alone.

**Theorem B — minimal-order safe prefix and sharp subsequent cost.**
The smallest candidate count permitting any finite uniform subsequent
mixing time is exactly
\[
 N_{\rm crit}(\epsilon)
 =\max\!\left\{1,\,
   \left\lfloor\frac{\log(\gamma_{K,\alpha}/\epsilon)}
                         {\lambda_K}\right\rfloor+1\right\}. \tag{C}
\]
The strict inequality in (B) is why a floor plus one occurs. A convenient
safe choice is
\[
 N_{\rm safe}(\epsilon)=
 \max\!\left\{1,\,
  \left\lceil\frac{\log(\gamma_{K,\alpha}/\epsilon)}
                        {\lambda_K}\right\rceil+1\right\}. \tag{D}
\]
This is at most one candidate more than \(N_{\rm crit}\), and
\(F_{N_{\rm safe}}\le b_K\epsilon\). It satisfies
\[
 \boxed{\lim_{\epsilon\downarrow0}\epsilon
    \log T_{K,\alpha,N_{\rm safe}(\epsilon)}(\epsilon)=K.} \tag{E}
\]
Consequently the optimal leading prefix length is
\[
 N_{\rm crit}(\epsilon)\sim
 \frac{\log(1/\epsilon)}{-\log(1-e^{-K})}.
\]
The same asymptotic holds for the number \(N_{\rm crit}-1\) of prefix
transitions. Formula (E) is for the explicit safe rule (D), not for
arbitrary approaches to the exact threshold (C).

**Theorem C — one correction under both KL budgets.**
If, in addition, \(D(q\Vert\pi)\le J\) for fixed \(J>0\), then for every
fixed \(N\ge2\),
\[
 \boxed{\lim_{\epsilon\downarrow0}\epsilon
   \log T_{K,J,\alpha,N}(\epsilon)=K.}                  \tag{F}
\]
Thus one preliminary global transition, \(N=2\), removes the extra
\(\beta J\) coefficient. For \(N=1\), the received theorem instead gives
\(\max\{K,\beta J\}\). When \(\beta J\le K\), there is no change in the
leading coefficient.

The proofs below are self-contained apart from elementary spectral
theory for self-adjoint contractions. No initial \(L^2(\pi)\) density,
bounded weights, finite state space, empirical KL estimate, or target
normalizing constant is assumed.

## 2. Forward-entropy tail bounds

For \(R>e\), binary entropy data processing gives
\[
 a:=\pi(W>R)\le\frac K{\log R-1}.                       \tag{2.1}
\]
Indeed \(q(W>R)\le a/R\), so the binary relative entropy is at least
\(a\log R+(1-a)\log(1-a)\ge a(\log R-1)\).
Taking
\[
 M=e^{2K+1},\quad A_0=\{W\le M\},\quad s_0=\pi(A_0)
\]
gives \(s_0\ge1/2\).

For \(0<h<1/2\), put \(b_h=q(W<h)\) and \(a_h=\pi(W<h)\).
Then \(a_h\le h b_h\le h\). With
\(\mathsf H_2(x)=-x\log x-(1-x)\log(1-x)\),
\[
\begin{split}
K&\ge d(a_h\Vert b_h)\\
 &=-\mathsf H_2(a_h)-a_h\log b_h
                  -(1-a_h)\log(1-b_h)\\
 &\ge-\mathsf H_2(h)+(1-h)\log\frac1{1-b_h}.
\end{split}
\]
Therefore
\[
 b_h\le\bar b_K(h):=
  1-\exp\!\left[-\frac{K+\mathsf H_2(h)}{1-h}\right]
  =b_K+O_K(h\log(1/h)).                                  \tag{2.2}
\]
The expansion is for the uniform envelope \(\bar b_K\), not for every
actual tail probability. The latter can be much smaller.

When reverse KL is also bounded,
\[
 b_h\le\frac{J}{\log(1/h)-1},\qquad 0<h<e^{-1},            \tag{2.3}
\]
by applying (2.1) to the reversed pair.

## 3. An exact first-high-candidate decomposition

Generate \(Y_0,\ldots,Y_{N-1}\) independently from \(q\), with \(Y_0\)
the initial state and the rest the proposals for the prefix. Its output
is one of these candidates. Hence
\[
 \mu_N\le Nq.                                            \tag{3.1}
\]
This is a measure inequality, obtained by the union bound on the event
that any candidate belongs to a specified measurable set.

Fix \(h>0\), write \(A_h=\{W<h\}\), and let \(q_{\rm hi}\) denote the
unnormalized restriction of \(q\) to \(A_h^c\). On the event that the
first candidate in \(A_h^c\) has index \(j\), every preceding state has
weight below \(h\); candidate \(j\) is certainly accepted (or initializes
the chain when \(j=0\)). Later candidates and uniforms are independent.
Thus
\[
 \mu_N=\nu_N+
       \sum_{j=0}^{N-1}b_h^j q_{\rm hi}G^{N-1-j},         \tag{3.2}
\]
where \(\nu_N\) has mass \(b_h^N\), supported on \(A_h\).
It represents the event that every candidate is in \(A_h\).

Because \(q_{\rm hi}\le\pi/h\) and \(G\) preserves \(\pi\), each propagated
summand without its factor \(b_h^j\) is at most \(\pi/h\).
For any \(D\subset A_h\), the \(j=N-1\) term is exactly zero on \(D\).
Consequently
\[
 \boxed{\mu_N(D)\le b_h^N+
       \frac{\pi(D)}h\sum_{j=0}^{N-2}b_h^j.}             \tag{3.3}
\]
The empty sum for \(N=1\) is zero. In particular it is at most \(N-1\).
This proof avoids an invalid shortcut: after reaching a weight above
\(h\), an MH path can descend through intermediate weights before
entering \(D\). A single-crossing argument would not suffice.

The exact IMH prefix law and its priority representation are established
machinery in the primary literature; see SOURCES.md. Here (3.2) gives
the required bound directly on arbitrary measurable spaces.

## 4. Observable smoothing and the exact low-set competition

Fix \(B,R>e\). Write
\[
 D=\{W<1/B\},\ E=\{W>R\},\ S=(D\cup E)^c,\quad
 b=q(D),\ a=\pi(E),\ d=\mu_N(D).
\]
For a measurable test event \(F\), put \(g=C^t1_F\), so \(0\le g\le1\),
and let \(z=s_0^{-1}\int_{A_0}g\,d\pi\in[0,1]\).

### 4.1 Pointwise near-harmonicity

For \(p_j=2^{-t}\binom tj\), extended by zero outside \(0,\ldots,t\),
\[
 (I-H)C^t1_F=\sum_{j=0}^{t+1}(p_j-p_{j-1})H^j1_F.
\]
The positive coefficient sum and the absolute negative coefficient sum
both equal the maximum binomial probability, by unimodality. Therefore
\[
 |g-Hg|\le\eta_t:=2^{-t}\binom t{\lfloor t/2\rfloor}
             =O((t+1)^{-1/2}).                           \tag{4.1}
\]
This is the received trial's crucial pointwise lemma; it is explicitly
credited rather than claimed as a new principal construction.

### 4.2 Anchor and core

The exact IMH Dirichlet form is
\[
 \mathcal E_G(g,g)=\frac12\iint
  \frac{(g(x)-g(y))^2}{\max(W(x),W(y))}\,\pi(dx)\pi(dy).
\]
Restricting only the \(y\)-leg to \(A_0\), and applying Jensen there,
\[
 \mathcal E_G(g,g)\ge\frac{s_0}{2}
      \int\frac{(g-z)^2}{\max(W,M)}\,d\pi.
\]
Reversibility and laziness make \(C\) a self-adjoint contraction with
spectrum in \([0,1]\). The centered event indicator has variance at
most \(1/4\). Since
\((1-\xi)\xi^{2t}\le1/(2t+1)\),
\[
 \mathcal E_C(g,g)\le\frac1{4(2t+1)},\qquad
 \int\frac{(g-z)^2}{\max(W,M)}\,d\pi
       \le\frac1{\alpha s_0(2t+1)}.                       \tag{4.2}
\]

Let \(f_N=d\mu_N/d\pi\). By (3.1), \(0\le f_N\le N/W\).
Since \((f_N-1)^2\le f_N^2+1\), splitting the core at \(W=M\) gives
\[
\begin{split}
 \int_S\max(W,M)(f_N-1)^2\,d\pi
 &\le M(N^2B+1)+N^2+R=:U_N .
\end{split}                                             \tag{4.3}
\]
Below \(M\), use \(W^{-2}\le B/W\); above \(M\), use
\(W(N^2/W^2+1)=N^2/W+W\), whose integrals are at most
\(N^2+R\). The identity \(\int W^{-1}d\pi=1\) is used.
The core multiplier for \(\int_S|g-z|\,dq\) is
\(\int_S\max(W,M)W^{-2}d\pi\le MB+1\le U_N\).
Thus with
\[
 \Delta_N=\sqrt{\frac{U_N}{\alpha s_0(2t+1)}},
\]
weighted Cauchy–Schwarz proves
\[
 \left|\int_S(g-z)(d\mu_N-d\pi)\right|\le\Delta_N,\qquad
 \int_S|g-z|\,dq\le\Delta_N.                              \tag{4.4}
\]
Since \(q(E)\le a/R\),
\[
 |q(g1_{D^c})-(1-b)z|\le\Delta_N+a/R.                    \tag{4.5}
\]

### 4.3 Exact competition while in the low-weight set

For every \(x\in D\), every proposal in \(D^c\) is accepted.
Every proposal in \(D\), accepted or rejected, leaves the state in \(D\).
Consequently
\[
 G(x,D)=b,\qquad Gg(x)=bP_Dg(x)+q(g1_{D^c}),              \tag{4.6}
\]
where \(P_D\) is a Markov kernel on \(D\) when \(b>0\).
If \(b=0\), the low-set integral is zero and the following bound follows
directly, so no normalized restricted kernel is needed.

Combining (4.1), (4.5), and (4.6), and taking bounded suprema and infima
of \(g-z\) on \(D\), gives
\[
 -\kappa_b z-\delta_N
 \le g(x)-z
 \le\kappa_b(1-z)+\delta_N,\qquad x\in D,                 \tag{4.7}
\]
where
\[
 \kappa_b=\frac{\beta}{1-\alpha b},\qquad
 \delta_N=\frac{\alpha(\Delta_N+a/R)+\eta_t}{1-\alpha b}. \tag{4.8}
\]
For example, if \(u=\sup_D(g-z)\), then
\[
 u\le\alpha b u+\beta(1-z)+\alpha(\Delta_N+a/R)+\eta_t,
\]
which proves the upper side. The lower side is identical with infima.
No maximum need be attained. All denominators are at least \(\beta>0\).

This step improves the earlier \(O(b^2)\) error treatment when \(b\) does
not vanish. It retains the possibility of repeated proposals back into
\(D\), producing the denominator \(1-\alpha b\). It is the principal
new upper-bound construction.

### 4.4 Signed tails without a sign assumption on the prefix law

On \(D\), integrate (4.7) against the positive measure \(\mu_N\).
On \(E\), integrate the elementary range \(-z\le g-z\le1-z\)
against \(-\pi\). Their upper sum is at most
\(\kappa_b d(1-z)+az+\delta_Nd\), and the absolute lower sum
is bounded by \(\kappa_b dz+a(1-z)+\delta_Nd\).
Both are at most \(\max\{\kappa_b d,a\}+\delta_Nd\).
The two remaining terms, \(-\pi\) on \(D\) and \(\mu_N\) on \(E\),
cost at most \(\pi(D)+\mu_N(E)\le b/B+Na/R\).
Together with (4.4), and centering the full mass-zero signed measure,
\[
 \boxed{\|\mu_NC^t-\pi\|_{\rm TV}
 \le \max\{a,\kappa_b d\}
       +\Delta_N+\delta_Nd+\frac bB+\frac{Na}{R}.}        \tag{4.9}
\]
No assertion that \(\mu_N-\pi\) has the same signs as \(q-\pi\) is used.
If \(1/B<h\), (3.3) further gives
\[
 d\le b_h^N+\frac b{Bh}\sum_{j=0}^{N-2}b_h^j.             \tag{4.10}
\]

Equations (2.1), (2.2), (4.8)–(4.10), with \(s_0\ge1/2\),
are a finite-time certificate using only \(K,\alpha,N,t,B,R,h\).
For the budget-only substitutions retain \(1/B<h<1/2\).
Replace \(a\) by \(\min(1,K/(\log R-1))\), \(b\) by
\(\bar b_K(1/B)\), and \(b_h\) by \(\bar b_K(h)\); the displayed
right sides are nondecreasing in the substituted masses. Clamp the
bound for \(d\) at one. The thresholds are proof parameters, not
quantities the sampler must evaluate.

## 5. Exact fixed-prefix floor: upper bound

Keep \(N\) fixed and let
\[
 B=R=t/(\log t)^4,\qquad h=B^{-1/2}.
\]
For large \(t\), all conditions hold. Uniformly over the forward-KL class,
\[
 a\to0,\quad b\le\bar b_K(1/B)\to b_K,\quad
 b_h\le\bar b_K(h)\to b_K,
\]
\[
 d\le\bar b_K(h)^N+(N-1)/\sqrt B,\qquad
 \Delta_N=O_{K,\alpha,N}((\log t)^{-2}),\qquad\delta_N\to0.
\]
Applying (4.9) proves
\[
 \limsup_{t\to\infty}R_{K,\alpha,N}(t)
 \le\frac{\beta b_K^N}{1-\alpha b_K}=F_N.                \tag{5.1}
\]
This is a uniform estimate. A fixed-pair convergence assertion has not
been interchanged with a supremum.

## 6. Matching construction and the equality endpoint

The independent lower contributor supplied and checked this refinement.
Fix \(0<b<b_K\), \(0<\rho<1\), and
\(0<\kappa<K+\log(1-b)\). For small \(p>0\), let
\[
 s=p e^{-2\kappa/p},\quad r=p e^{-\kappa/p},\qquad
 \pi_p=(p,s,1-p-s),\quad q_p=(r,b,1-b-r).                \tag{6.1}
\]
The states are \(A,B,C_0\) (the last name is distinct from kernel \(C\)).
All masses are positive for sufficiently small \(p\). Moreover
\[
 D(\pi_p\Vert q_p)
 =\kappa+s\log(s/b)+(1-p-s)\log\frac{1-p-s}{1-b-r}
 \longrightarrow\kappa-\log(1-b)<K.                    \tag{6.2}
\]
Thus all sufficiently small \(p\) are admitted. This is an exact
continuous-limit admissibility argument with a strict margin; the
independent note supplies explicit finite sufficient inequalities.

Use the fixed symmetric local proposal with edge probabilities \(\rho\)
on \(A-B\) and \(1-\rho\) on \(B-C_0\), and diagonal complements.
Ordinary MH for \(\pi_p\) gives
\[
 L_{BA}=\rho,\quad L_{BC_0}=1-\rho,\quad
 L_{AB}=\rho s/p,\quad
 L_{C_0B}=(1-\rho)s/(1-p-s).
\]
Each finite member is irreducible, reversible, and has a fixed kernel.
The matrix limits as \(p\downarrow0\) are
\[
 G_0=\begin{pmatrix}1&0&0\\0&b&1-b\\0&0&1\end{pmatrix},
 \quad
 L_0=\begin{pmatrix}1&0&0\\\rho&0&1-\rho\\0&0&1\end{pmatrix},
 \quad q_0=(0,b,1-b),\quad\pi_0=(0,0,1).
\]
For fixed finite \(N,t\), finite matrix multiplication is continuous,
and
\[
 q_0G_0^{N-1}=(0,b^N,1-b^N).
\]
The limiting lazy hybrid has absorbing \(A,C_0\); at \(B\) its self-loop
is \(z_b=(1+\alpha b)/2\) and the probability of eventual absorption in
\(A\) is \(\gamma_{b,\rho}=\beta\rho/(1-\alpha b)\).
Its exact TV distance at time \(t\) is
\[
 b^N\{\gamma_{b,\rho}+
             (1-\gamma_{b,\rho})z_b^t\}.                 \tag{6.3}
\]
This is not an admitted singular limit instance; for each finite \(t\)
its value is approached by admitted positive finite chains.

First choose \(b<b_K,\rho<1\), then \(\kappa\) within the positive
entropy slack, then sufficiently small \(p\). Letting \(b\uparrow b_K\)
and \(\rho\uparrow1\) in the lower envelope yields, for every finite \(t\),
\[
 R_{K,\alpha,N}(t)\ge
 F_N+b_K^N(1-\gamma_{K,\alpha})
                \left(\frac{1+\alpha b_K}{2}\right)^t>F_N. \tag{6.4}
\]
The strict inequality uses \(0<\alpha<1\) and \(0<b_K<1\).
This proves the lower half of (A) and rules out a common finite
sufficient time even at \(\epsilon=F_N\).

TV under a fixed invariant \(C\) is nonincreasing. Hence failure at
each finite \(t\) implies the supremum of first hitting times is
infinite. Conversely (5.1) supplies a common finite time whenever
\(\epsilon>F_N\). This proves (B), and solving \(F_N<\epsilon\)
gives (C). Endpoints \(\alpha=0,1\), \(K=0\) are not covered by this
statement; \(K=0\) separately forces \(q=\pi\).

## 7. Near-minimal prefix restores the sharp forward exponent

Use \(N=N_{\rm safe}(\epsilon)\) in (D). Direct integer arithmetic gives
\[
 F_N\le b_K\epsilon,\qquad
 N=O_{K,\alpha}(\log(1/\epsilon)).
\]
Fix any \(\zeta>0\) and take
\[
 t=\left\lceil e^{(K+\zeta)/\epsilon}\right\rceil,\quad
 B=R=t/(\log t)^4,\quad h=\epsilon^2.
\]
For sufficiently small \(\epsilon\), \(1/B<h<1/2\).
Using the envelope in (2.2),
\[
 \bar b_K(h)^N
 =b_K^N\exp\{N\,O_K(h\log(1/h))\}
 =b_K^N[1+o(1)].                                       \tag{7.1}
\]
The constants are uniform over \(\pi,q,L\), with fixed \(K,\alpha\).
The second term of (4.10) is at most \(N/(B\epsilon^2)=o(\epsilon)\).
Also \(\kappa_b\le\gamma_{K,\alpha}+o(1)\). Therefore
\[
 \kappa_bd\le b_K\epsilon[1+o(1)]+o(\epsilon).
\]
The other leading term obeys
\[
 a\le\frac{K}{\log R-1}
   =\frac{K}{K+\zeta}\epsilon[1+o(1)].
\]
Both coefficients are strictly below one. Moreover
\[
 \Delta_N=O_{K,\alpha}\!\left(\frac{N+1}{(\log t)^2}\right)
        =O(\epsilon^2\log(1/\epsilon))=o(\epsilon),
\]
and \(\delta_Nd,b/B,Na/R=o(\epsilon)\). Applying (4.9)
gives a common sufficient time with
\(\limsup\epsilon\log T\le K+\zeta\). Let \(\zeta\downarrow0\).

For the lower bound choose \(L=I\), \(\ell>1\),
\[
 p=\ell\epsilon,\quad r=p e^{-K/p},\quad
 \pi=(p,1-p),\ q=(r,1-r),\ u=e^{-K/p}.
\]
Then \(D(\pi\Vert q)<K\) and the exact distance is
\[
 \|\mu_NC^t-\pi\|_{\rm TV}
 =p(1-u)^N(1-\alpha u/2)^t.                              \tag{7.2}
\]
For \(N=O(\log(1/\epsilon))\), \(Nu\to0\).
Choose \(0<c<\log\ell\) and
\(t_\epsilon=\lfloor 2c/(\alpha u)\rfloor\).
The distance divided by \(\epsilon\) tends to \(\ell e^{-c}>1\);
therefore this time is insufficient, and
\(\liminf\epsilon\log T\ge K/\ell\).
Letting \(\ell\downarrow1\) proves (E).
The same lower argument holds for any prefix with
\(\epsilon\log N(\epsilon)\to0\).

The fixed-\(N\) floor alone would not justify this result for growing
\(N\). Equations (7.1) and the explicit \(N\)-dependent core multiplier
are the required uniform bridge.

## 8. One preliminary global transition with joint KL

Keep \(N\ge2\) fixed, impose \(D(q\Vert\pi)\le J\), and choose
\(B=R=t/(\log t)^4,\ h=B^{-1/2}\).
Equation (2.3) and (4.10) give uniformly
\[
 d\le\left[\frac{J}{\tfrac12\log B-1}\right]^N
           +\frac{N-1}{\sqrt B}
     =O_{J,N}((\log t)^{-N})+O_N(B^{-1/2}).
\]
Therefore \(\kappa_bd=o(1/\log t)\),
\(\Delta_N=O((\log t)^{-2})\), and all errors in (4.9) are
\(o(1/\log t)\). Only the high-weight target tail remains:
\[
 \limsup_{t\to\infty}(\log t)
  \sup_{\pi,q,L}\|\mu_NC^t-\pi\|_{\rm TV}\le K.
\]
Uniform inversion gives the upper half of (F).
For the two-state lower family in Section 7,
\(D(q\Vert\pi)\le-\log(1-p)\to0\), so it is admitted for every
fixed \(J>0\). Its finite fixed prefix does not affect (7.2)'s
leading exponent. This proves (F).

## 9. Operations, costs, and comparison

The operation uses ordinary cached unnormalized MH ratios. It costs
\(N\) iid draws from \(q\) and at most \(N\) target/proposal evaluations
for the prefix, followed by \(t\) lazy-mixture selections. The latter
use \(\alpha t/2\) global proposals and \(\beta t/2\) local transitions
in expectation; the identity branch needs neither. The number of
selected global/local branches is random, and local transitions can
have application-specific costs not bounded by this theorem.
These expectations refer to a fixed number \(t\) of mixture steps.
Stopping instead after an exact number of global proposals is a different
random-time operation and is not covered by substitution of its expected time.

Pure proposal-start IMH has sharp coefficient \(K\) at matched global
proposal counts. Our safe prefix restores that same exponential
coefficient, with additional local work; it does not establish a
finite-budget advantage, a reduction in target evaluations, or a
successful application. At \(K=1,J=4,\alpha=1/2\), the received
unprefixed mixture has coefficient \(2\), while the one-step-prefixed
mixture and pure IMH have coefficient \(1\).

A deterministic sufficient time can be chosen by evaluating (4.9)'s
budget-only envelope. Such a certificate may be very conservative.
The numerical implementation in this archive evaluates certificates
and finite-law diagnostics; it does not run exponentially many
sampling steps. Exact real kernels and a valid population KL certificate
remain mathematical assumptions. Floating-point MH, approximate local
kernels, uncertified learned losses, and wall-clock costs require
separate error/resource analyses.

For finite certificate evaluation one may replace \(\eta_t\) by
\(\sqrt{2/(t+1)}\). One elementary verification is to induct on
\(k\) that \(\binom{2k}{k}^2/16^k\le1/(k+1)\), using the successive
ratio \(((2k+1)/(2k+2))^2\le(k+1)/(k+2)\); odd central probabilities
are the preceding even one multiplied by \((2k+1)/(2k+2)\).
This supplies the stated loose bound at every nonnegative integer \(t\).

## 10. Status and remaining boundary

The new result is a sharp robustness threshold for composing standard
samplers, not a new sampling primitive. The principal constructed the
exact low-set competition bound (4.7), the finite-time envelope, and
the sharp safe-prefix cost proof. Independent contributors checked the
prefix decomposition, constructed the matching floor and equality
obstruction, reviewed the changing-\(N\) scaling, and examined primary
literature. The received pointwise lemma and older anchored smoothing
are credited at their use.

The exact threshold (C) answers existence of a finite uniform guarantee.
It does not quantify the cost when \(\epsilon-F_N\) is arbitrarily tiny.
One extra candidate avoids that unresolved boundary, but can be an
unnecessary operation for an easy pair. A precise next question is
whether a stopping rule using only observed iid proposal weights,
with unknown target normalizer and the same certified forward budget,
can safely shorten the correction prefix while retaining the uniform
robustness and sharp exponent. Only prefix stopping would be allowed;
the subsequent \(C\) would remain fixed. A proof would need an explicit
observable certificate and a lower comparator for unobserved proposal
mass. No adaptive guarantee is claimed here.
Kurennoy–Yarullin–Reid's Theorem 6 already establishes a related
fixed-budget remaining-error certification barrier without this certified
KL restriction. The next step must account for that result and isolate
what, if anything, the known \(K\) and the weaker prefix-safety objective
change; merely reproving an unrestricted unseen-mass obstruction would
not advance this question.
