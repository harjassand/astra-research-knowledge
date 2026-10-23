# Joint forward/reverse KL: a bounded continuation lemma

Status: independently derived continuation material, separate from the established checkpoint in PROOF.md. No historical novelty claim is made here. Section 6 independently checks root's latest anchor argument from JOINT_KL.md: the lazy reversible joint-KL envelope has leading upper coefficient max(K,J). Together with the lower constructions below, this proves the exact coefficient K when J is at most K; the J greater than K regime remains bounded between max(K,(1-alpha)J) and J. Section 5 preserves the weaker intermediate upper bound as part of the proof history.

## Question

For fixed \(K,J>0\) and \(0<\alpha<1\), constrain both
\[
D(\pi\Vert q)\le K,\qquad D(q\Vert\pi)\le J.
\]
Can the existing three-state reversible entrance-to-trap construction produce a doubly exponential mixing obstruction as target accuracy \(\epsilon\downarrow0\)?

Answer: the same construction yields a nontrivial **singly exponential** lower bound. Its one-step funnel mechanism cannot yield a doubly exponential trap-residence obstruction, because the reverse KL budget controls the stationary mass feeding the trap, and reversibility supplies a corresponding escape flow. This does not settle the envelope over arbitrary larger local kernels.

## 1. A joint-KL lower family

Fix
\[
L>\frac{2}{1-\alpha},\qquad \kappa=K/2.
\]
For sufficiently small \(\epsilon>0\), define
\[
b=L\epsilon,\quad p=\epsilon^2,\quad
s=b e^{-J/b},\quad r=p e^{-\kappa/p},
\]
and
\[
\pi=(p,s,1-p-s),\qquad q=(r,b,1-b-r)
\]
on \(A-B-C\).

The following are explicit sufficient finite conditions:
\[
p\le \min\{1/4,b/2\},\qquad
s\le p,\qquad
b+p\le1-e^{-\kappa}.
\tag{1.1}
\]
They hold for all sufficiently small \(\epsilon\), for any fixed \(K,J,L>0\). These conditions ensure positivity, \(\pi_C\ge1/2\), \(q_C\ge e^{-\kappa}\), and \(q_C\le\pi_C\).

The forward divergence obeys
\[
\begin{aligned}
D(\pi\Vert q)
&=\kappa+s\log(s/b)+\pi_C\log(\pi_C/q_C)\\
&\le\kappa-\log q_C\\
&\le2\kappa=K.
\end{aligned}
\tag{1.2}
\]
The reverse divergence obeys
\[
\begin{aligned}
D(q\Vert\pi)
&=r\log(r/p)+J+q_C\log(q_C/\pi_C)\\
&\le J,
\end{aligned}
\tag{1.3}
\]
because both the first and third terms are nonpositive.

The likelihood ratio at \(A\) is \(e^{\kappa/p}\), which is the maximum: the bulk ratio is at most \(e^\kappa\), and the entrance ratio \(s/b=e^{-J/b}\) is below one.

Use the same fixed symmetric path proposal for local MH:
\[
L_{BA}=L_{BC}=\tfrac12,\quad
L_{AB}=s/(2p),\quad L_{CB}=s/(2\pi_C).
\]
This local kernel is irreducible, aperiodic and \(\pi\)-reversible.

The global and local exit probabilities from \(A\) are
\[
h_G=(1-p)e^{-\kappa/p},
\qquad
h_L=\frac{s}{2p}
=\frac{L}{2\epsilon}e^{-J/(L\epsilon)}.
\tag{1.4}
\]
For the mixture \(H=\alpha G+(1-\alpha)L\), write
\[
h=\alpha h_G+(1-\alpha)h_L.
\]
The first-step guaranteed injected mass is
\[
d=\frac{(1-\alpha)b}{2}
=C\epsilon,\qquad C=\frac{(1-\alpha)L}{2}>1.
\]
Thus, for \(n\ge1\),
\[
\|qH^n-\pi\|_{\rm TV}\ge
C\epsilon(1-h)^{n-1}-\epsilon^2.
\tag{1.5}
\]

Because \(\kappa/\epsilon^2\) grows faster than \(J/(L\epsilon)\),
\[
h\sim \frac{(1-\alpha)L}{2\epsilon}
          e^{-J/(L\epsilon)}.
\tag{1.6}
\]
Fix any \(0<a<\log C\), and take \(n_\epsilon=\lfloor a/h\rfloor\). Then the lower bound divided by \(\epsilon\) tends to \(Ce^{-a}>1\). Hence this many steps are insufficient, and
\[
\liminf_{\epsilon\downarrow0}
 \epsilon\log T_{K,J,\alpha}^{\rm hybrid}(\epsilon)
\ge \frac{J}{L}.
\]
Since any fixed \(L>2/(1-\alpha)\) is admitted,
\[
\boxed{\liminf_{\epsilon\downarrow0}
 \epsilon\log T_{K,J,\alpha}^{\rm hybrid}(\epsilon)
\ge \frac{(1-\alpha)J}{2}.}
\tag{1.7}
\]
This is a lower bound for the whole admissible class, not an asserted sharp value. The factor \(1/2\) comes from the fixed equal-edge local proposal; alternative fixed edge probabilities could improve that particular coefficient.

### Laziness does not alter the exponential scale

For \(C_H=(I+H)/2\), binomial subordination and (1.5) give
\[
qC_H^n(A)\ge
\frac{d}{1-h}
\left[(1-h/2)^n-2^{-n}\right].
\tag{1.8}
\]
Choosing \(n\) of order \(2a/h\) gives the same leading exponential lower bound (1.7). Do not discard a factor two of injected mass merely by inspecting the very first lazy step; the first nontrivial update can occur later.

### Matched global-call schedules

For \(LG\) cycles, the first guaranteed trap mass is
\[
(b/2)(1-h_G)\sim L\epsilon/2.
\]
Taking fixed \(L>2\) yields the same argument with exponent \(J/L\), so
\[
\liminf_{\epsilon\downarrow0}
 \epsilon\log T_{K,J}^{LG}(\epsilon)\ge J/2.
\tag{1.9}
\]

The original first-cycle \(GL\) lower bound is \(b^2/2\), not \(b/2\). With \(b=L\epsilon\), this is too small to establish error exceeding \(\epsilon\). This difference must not be hidden. Choosing instead \(b=L\sqrt{\epsilon}\), \(L>\sqrt2\), and still \(p=\epsilon^2\), gives a valid joint-KL construction and an obstruction with
\[
\log T^{GL}(\epsilon)\gtrsim \frac{J}{L\sqrt{\epsilon}}.
\]
That is weaker than an \(\exp(\mathrm{constant}/\epsilon)\) lower bound. The present calculation does not determine the sharp \(GL\) envelope.

### Stronger coefficient for the whole arbitrary-local-kernel class

Use any fixed \(0<\rho<1\) as the symmetric proposal probability on edge \(A-B\), with \(1-\rho\) on edge \(B-C\). At the endpoints the remaining proposal stays put. The resulting local MH kernel has
\[
L_{BA}=\rho,\quad L_{BC}=1-\rho,\quad
L_{AB}=\rho s/p,\quad L_{CB}=(1-\rho)s/\pi_C.
\]
It is still irreducible and reversible. The one-step injected mass is now
\(d=(1-\alpha)\rho b\), and the local escape is \(\rho s/p\). Choose the scale \(L>1/[(1-\alpha)\rho]\) in \(b=L\epsilon\). Every KL calculation is unchanged. The preceding proof, including binomial subordination for laziness, gives
\[
\liminf_{\epsilon\downarrow0}
\epsilon\log T_{K,J,\alpha}^{\rm lazy}(\epsilon)
\ge (1-\alpha)\rho J.
\]
Because the class permits every fixed \(\rho<1\), letting \(\rho\uparrow1\) yields
\[
\boxed{\liminf_{\epsilon\downarrow0}
\epsilon\log T_{K,J,\alpha}^{\rm lazy}(\epsilon)
\ge (1-\alpha)J.}
\tag{1.10}
\]
No reducible \(\rho=1\) kernel is needed: every individual construction has \(\rho<1\).

The pure-IMH lower bound \(K\) also survives both constraints and laziness. Use the earlier two-state pair, for which
\(D(q\Vert\pi)\le-\log(1-p)\to0\), and choose the local kernel to be the identity. Then the lazy mixture is
\((1-\alpha/2)I+(\alpha/2)G\), whose exact two-state contraction replaces \(r/p\) by \(\alpha r/(2p)\). This changes time by a constant factor and leaves the leading exponent \(K\). Thus the whole class has lower coefficient at least
\[
\boxed{\max\{K,(1-\alpha)J\}.}
\tag{1.11}

## 2. Why the one-step funnel cannot give double exponential trapping

This argument does not require the specific exponential parameterization above.

Suppose \(q(B)=b\), \(\pi(B)=s\), and \(D(q\Vert\pi)\le J\). Binary data processing gives
\[
\begin{aligned}
J
&\ge b\log(b/s)+(1-b)\log\frac{1-b}{1-s}\\
&\ge b\log(b/s)-b,
\end{aligned}
\]
so
\[
\boxed{s\ge b e^{-1-J/b}.}
\tag{2.1}
\]

For the fixed path local kernel, if \(\pi(A)=p\) and \(\pi(B)=s\le p\), the mixture exit probability from \(A\) is at least
\[
h\ge (1-\alpha)\frac{s}{2p}
\ge \frac{(1-\alpha)b}{2p}e^{-1-J/b}.
\tag{2.2}
\]

To make the original one-step trap lower bound exceed \(\epsilon\), it is necessary that
\[
d=\frac{(1-\alpha)b}{2}>\epsilon+p>\epsilon.
\]
Thus \(b>2\epsilon/(1-\alpha)\). The function \(b e^{-J/b}\) is increasing for positive \(b\). Using \(p\le1\) gives
\[
\boxed{
h\ge
\epsilon\exp\left[-1-\frac{(1-\alpha)J}{2\epsilon}\right].
}
\tag{2.3}
\]
Therefore the no-exit residence factor \((1-h)^n\) dies on at most a singly exponential scale in \(J/\epsilon\), up to powers and logarithms of accuracy. Modifying \(r\) to be doubly exponentially small cannot help: it suppresses the global escape while the local escape in (2.3) remains.

Equivalently, one cannot independently choose the local influx that injects \(>\epsilon\) starting mass and the reverse stationary flow that releases that mass. Reversibility/invariance ties them together, and reverse KL prevents the source stationary mass from being arbitrarily small at a fixed injected \(q\)-mass.

This proves a limitation of the current residence-based construction. It does **not** prove a singly exponential universal upper bound for all local-global chains, rule out multilevel mechanisms, or establish the sharp joint-KL envelope. A further construction would need to avoid this one-step flow constraint, or a new comparison theorem would need to show that every harmful mechanism obeys an analogous bound.

## 3. Relation to the forward-only obstruction

The old fixed-\(b\) family has
\[
D(q\Vert\pi)\sim 2bc/p,
\]
which diverges. Setting \(b\) to zero with accuracy resolves that objection, but then the reverse budget controls the entrance mass and local return rate, leading to the singly exponential construction above.

The forward-only nonuniformity theorem remains unchanged. The joint-KL result here is new continuation material and should not be silently inserted into a previously frozen scientific claim without a new version/receipt.

## 4. Chosen next obligation

At the time this construction was derived, the genuine unresolved step was whether arbitrary reversible local kernels could create a more complicated obstruction beyond this flow-limited funnel, or whether a uniform single-exponential joint-KL bound could replace the nested-exponential truncation certificate. Root has since supplied such an upper-bound construction. The independent check is recorded below. The remaining issue is the sharp leading coefficient, not the existence of a single-exponential envelope.

## 5. Independent check of root's new core-indicator smoothing upper bound

This section checks the principal investigator's supplied argument. The principal owns its construction and full proof. Let
\[
C=\frac12[I+\alpha G+(1-\alpha)L],
\]
where \(L\) is \(\pi\)-reversible and \(\pi\)-invariant. Under both finite divergences, \(\pi\) and \(q\) are mutually absolutely continuous. Put \(W=d\pi/dq\), and fix \(B,R>e\). Let
\[
S=\{1/B\le W\le R\},\quad s=\pi(S)>0,\quad
a=\pi(W>R),\quad b=q(W<1/B).
\]
The two entropy-tail inequalities give
\[
a\le K/(\log R-1),\qquad b\le J/(\log B-1).
\]
Moreover
\[
q(S^c)+\pi(S^c)\le a(1+1/R)+b(1+1/B),
\quad
s\ge1-a-b/B.
\tag{5.1}
\]

For an arbitrary measurable event \(A\), set \(g=C^t1_A\) and
\(m=s^{-1}\int_Sg\,d\pi\). Both \(g\) and \(m\) lie in \([0,1]\). Centering on the core gives
\[
\left|\int g\,dq-\int g\,d\pi\right|
\le \max\{q(S^c),\pi(S^c)\}
+ \left|\int_S(g-m)\,dq\right|.
\]
Here the two terms on the right are added. To justify the improved outside term, write \(Q=q(S^c)\), \(P=\pi(S^c)\). Since \(g-m\in[-m,1-m]\),
\[
\int_{S^c}(g-m)(dq-d\pi)
\in[-mQ-(1-m)P,\ (1-m)Q+mP].
\]
The absolute value is therefore at most \(\max\{Q,P\}\), not merely \(Q+P\). This improvement was supplied by another independent reviewer and communicated by root; it has been checked here.
Since \(f=dq/d\pi=1/W\le B\) on \(S\),
\[
\left|\int_S f(g-m)\,d\pi\right|
\le\sqrt{\left(\int_S f^2d\pi\right)
          \left(\int_S(g-m)^2d\pi\right)}
\le\sqrt{B\int_S(g-m)^2d\pi}.
\]
The independence-MH Dirichlet formula restricted to \(S\times S\) gives
\[
\mathcal E_G(g,g)
\ge \frac1{2R}\int_S\int_S(g(x)-g(y))^2\pi(dx)\pi(dy)
=\frac{s}{R}\int_S(g-m)^2d\pi.
\]
Consequently the core contribution is at most
\(\sqrt{BR\mathcal E_G(g,g)/s}\).

Laziness and reversibility imply that \(C\)'s spectrum lies in \([0,1]\). The spectral measure of \(1_A-\pi(A)\) has total mass at most \(1/4\), and
\[
\sup_{0\le\lambda\le1}\lambda^{2t}(1-\lambda)
\le1/(2t+1).
\]
Thus
\[
\mathcal E_C(C^t1_A,C^t1_A)
\le\frac1{4(2t+1)}.
\]
The mixture form gives
\(\mathcal E_C\ge(\alpha/2)\mathcal E_G\). Therefore, uniformly over \(A\),
\[
\boxed{
\|qC^t-\pi\|_{\rm TV}
\le \max\{a+b/B,\ b+a/R\}
 +\sqrt{\frac{BR}{2\alpha s(2t+1)}}.
}
\tag{5.2}
\]
All normalization factors in the supplied formula check out. No initial \(L^2(\pi)\) density assumption was used.

The initial sum-of-outside-masses bound would give leading upper coefficient
\((\sqrt K+\sqrt J)^2\). The improved maximum permits both tail budgets to be approximately \(\epsilon\), rather than sharing a single \(\epsilon\) budget.

For \(K,J>0\), allocate
\[
a\sim\epsilon,\qquad b\sim\epsilon,
\]
with a vanishing positive slack, and choosing \(\log R=1+K/a\), \(\log B=1+J/b\), yields
\[
\boxed{
\limsup_{\epsilon\downarrow0}
\epsilon\log T_{K,J,\alpha}^{\rm lazy}(\epsilon)
\le K+J.
}
\tag{5.3}
\]
The \(s^{-1}\), \(\alpha^{-1}\), and accuracy-polynomial factors in the required \(t\) do not change this leading exponent. For a fully explicit slack choice, set \(\zeta=\sqrt\epsilon\), use \(a=b=(1-\zeta)\epsilon\), and also enforce \(B,R\ge1/\zeta\). Then the maximum of the two tail errors is at most \(\epsilon-\epsilon^2\), \(s\ge1-\epsilon\), and
\[
t\ge\frac{BR}{4\alpha(1-\epsilon)\epsilon^4}
\]
suffices for the remaining error. Integer rounding only enlarges the sufficient budget.

Combining the independently checked upper bound with (1.11) gives
\[
\boxed{
\max\{K,(1-\alpha)J\}
\le\liminf_{\epsilon\downarrow0}\epsilon\log T
\le\limsup_{\epsilon\downarrow0}\epsilon\log T
\le K+J.
}
\tag{5.4}
\]
This was the intermediate envelope before the anchor argument in Section 6. It closes the tentative doubly-exponential premise for the stated lazy reversible class but is superseded quantitatively by (6.5). Historical novelty of the particular upper or lower statements has not been assessed in this continuation challenge.

## 6. Independent verification of the stronger anchor upper bound

This section checks root's latest proof from JOINT_KL.md. It retains the hypotheses from Section 5: K,J are positive, alpha lies strictly between zero and one, G is independence MH with proposal q and target pi, L is a pi-reversible Markov kernel, and C=(I+alpha G+(1-alpha)L)/2. Both KL divergences are finite, so q and pi are mutually absolutely continuous. No bounded initial density or finite initial chi-squared divergence is assumed.

Write W=dpi/dq and fix B,R greater than e. Set
\[
S=\{1/B\le W\le R\},\qquad
a=\pi(W>R),\quad b=q(W<1/B).
\]
The previously checked binary-entropy estimates give
\[
a\le\frac K{\log R-1},\qquad
b\le\frac J{\log B-1},
\]
and
\[
\pi(S^c)\le a+b/B,\qquad q(S^c)\le b+a/R.
\tag{6.1}
\]

For any measurable event A, let g=C^t1_A. Thus 0<=g<=1. Instead of centering g on the truncation core, use a fixed anchor:
\[
M=e^{2K+1},\quad A_0=\{W\le M\},\quad
s_0=\pi(A_0)\ge\tfrac12,\quad
m=s_0^{-1}\int_{A_0}g\,d\pi.
\]
The bound on s_0 follows from the same forward-KL tail bound at M. In particular, m belongs to [0,1] and M does not depend on accuracy.

The IMH Dirichlet form has the exact representation
\[
\mathcal E_G(g,g)=\frac12\int\pi(dx)\pi(dy)
\frac{(g(x)-g(y))^2}{\max\{W(x),W(y)\}}.
\]
Restrict its y-leg to A_0, lower-bound the reciprocal denominator by 1/max(W(x),M), and apply Jensen to the conditional probability pi(.|A_0). This gives
\[
\mathcal E_G(g,g)\ge\frac{s_0}{2}
\int\frac{(g-m)^2}{\max(W,M)}\,d\pi.
\tag{6.2}
\]
The factor one-half is retained because only one integration leg was restricted. No symmetric double-counting is used.

Both q and pi have total mass one, so centering the full signed measure difference gives
\[
(q-\pi)g=
\int_S(g-m)(1/W-1)\,d\pi
+\int_{S^c}(g-m)(dq-d\pi).
\]
The outside contribution has absolute value at most max(q(S^c),pi(S^c)). The argument from Section 5 still applies: g-m is contained in [-m,1-m]. It does not require m to be the mean of g on S.

Weighted Cauchy--Schwarz and (6.2) bound the core contribution by
\[
\sqrt{\frac{2\mathcal E_G(g,g)}{s_0}\ I},\qquad
I=\int_S\max(W,M)(1/W-1)^2\,d\pi.
\]
Split the integral at W=M. For W<=M, use
\[
M(1/W-1)^2\le M(1/W^2+1),\qquad
1/W^2\le B/W\quad\hbox{on }S,
\]
and the identity integral (1/W) dpi = 1. This contribution is at most M(B+1). For W>M>1, the integrand equals W-2+1/W, which is at most W and hence at most R on S. Therefore
\[
I\le M(B+1)+R.
\tag{6.3}
\]

The spectral smoothing calculation from Section 5 gives
\[
\mathcal E_C(C^t1_A,C^t1_A)\le\frac1{4(2t+1)},\qquad
\mathcal E_G(g,g)\le\frac1{2\alpha(2t+1)}.
\]
Indeed, C has spectrum in [0,1], the centered indicator has spectral mass at most 1/4, and lambda^(2t)(1-lambda)<=1/(2t+1). The form comparison uses E_C >= (alpha/2) E_G.

Combining these inequalities and taking the supremum over measurable A proves the reviewed finite-time bound
\[
\boxed{
\|qC^t-\pi\|_{\rm TV}\le
\max\{a+b/B,\ b+a/R\}
+\sqrt{\frac{M(B+1)+R}{\alpha s_0(2t+1)}}.
}
\tag{6.4}
\]
All constants and normalizations check independently. This is an additive B+R dependence, with a fixed K-dependent multiplier on B, rather than the earlier multiplicative BR dependence.

For a fully explicit asymptotic choice, let zeta=sqrt(epsilon), let a_0=b_0=(1-zeta)epsilon, and choose
\[
R=\max\{1/\zeta,\exp(1+K/a_0)\},\qquad
B=\max\{1/\zeta,\exp(1+J/b_0)\}.
\]
Then actual a<=a_0 and b<=b_0. The first term in (6.4) is at most
\[
(1-\zeta)\epsilon(1+\zeta)
=\epsilon-\epsilon^2.
\]
Since s_0>=1/2, any integer
\[
t\ge\frac{M(B+1)+R}{\alpha\epsilon^4}
\]
makes the square-root term at most epsilon^2. Consequently the uniform leading upper coefficient is max(K,J).

Together with the lower families in Section 1, the current envelope is
\[
\boxed{
\max\{K,(1-\alpha)J\}
\le\liminf_{\epsilon\downarrow0}\epsilon\log T_{K,J,\alpha}^{\rm lazy}(\epsilon)
\le\limsup_{\epsilon\downarrow0}\epsilon\log T_{K,J,\alpha}^{\rm lazy}(\epsilon)
\le\max\{K,J\}.
}
\tag{6.5}
\]
For J<=K this proves that the limit exists and equals K. For J>K it leaves the precise interval from max(K,(1-alpha)J) to J. No sharpness claim or claim that the limit exists is made in that remaining regime. The restriction to lazy reversible mixtures belongs to the theorem; arbitrary state-dependent schedules are not covered. This independent check establishes mathematical validity, not historical novelty.

