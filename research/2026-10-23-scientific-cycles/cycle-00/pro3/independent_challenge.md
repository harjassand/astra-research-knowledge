# Independent challenge: forward-KL control of independence MH

Status: direct mathematical derivation by the independent challenger. This is not a literature novelty determination. Root retains the main construction. No B3 scientific output was reopened.

## 1. Setup and exact scope

Let \(\pi\ll q\) be probability measures, \(w=d\pi/dq\), and \(D(\pi\Vert q)=\int\log w\,d\pi\le K\), where \(K>0\) is fixed. The independence Metropolis--Hastings (IMH) chain proposes from \(q\), accepts \(y\) from \(x\) with probability \(\min(1,w(y)/w(x))\), and starts with \(X_0\sim q\). At zero-weight states use acceptance one for positive-weight proposals; the convention for two zero weights is immaterial to the target.

Define
\[
R_K(n)=\sup_{D(\pi\Vert q)\le K}\|qP^n-\pi\|_{\rm TV},
\qquad
T_K(\epsilon)=\sup_{D(\pi\Vert q)\le K}
 \min\{n\ge0:\|qP^n-\pi\|_{\rm TV}\le\epsilon\}.
\]
The suprema range over probability pairs (and may vary with \(n\) or \(\epsilon\)). TV means \(\sup_B|\mu(B)-\nu(B)|\), not twice that value.

The root's claimed result is correct, subject to this algorithm-specific and accuracy-dependent minimax interpretation:
\[
\lim_{n\to\infty}(\log n)R_K(n)=K,
\qquad
\lim_{\epsilon\downarrow0}\epsilon\log T_K(\epsilon)=K.
\]
The first statement is slightly stronger and gives a particularly clean proof of the second.

## 2. A uniform finite-time upper bound

Fix \(M>e\), write \(A=\{w>M\}\), \(p=\pi(A)\), \(r=q(A)\). Since \(r\le p/M\), the KL chain rule / log-sum inequality gives
\[
D(\pi\Vert q)
 \ge p\log(p/r)+(1-p)\log\frac{1-p}{1-r}
 \ge p\log M+(1-p)\log(1-p)
 \ge p(\log M-1).
\]
The last inequality is \((1-p)\log(1-p)\ge-p\). Interpret boundary cases by continuity. Thus
\[
p\le b:=K/(\log M-1),\qquad r\le p/M.
\]
Only use the following bound when \(b<1\).

Run \(X_0\sim q\) and an independent \(Y_0\sim\pi\) with common proposals and uniforms. The second chain stays stationary. On the event that both initial weights are at most \(M\), before the first common acceptance both weights remain at most \(M\): a proposal of weight greater than \(M\) is accepted by both and couples them. At a step with both weights at most \(M\), the probability of common acceptance is at least
\[
a_M=\int \min(1,w(z)/M)\,q(dz)
 =M^{-1}\int\min(M,w)\,dq
 \ge(1-p)/M.
\]
The probability of an initially bad pair is at most \(p+r\). A common acceptance sets the two chains to the same proposed state, after which common randomness preserves equality. This construction works on general measurable spaces; one can use a measurable "already coalesced" flag without requiring the diagonal to be measurable.

For every integer \(n\ge0\),
\[
\boxed{
\|qP^n-\pi\|_{\rm TV}
 \le p+r+(1-a_M)^n
 \le b(1+1/M)+\exp[-n(1-b)/M].
}
\]
The bound can of course be clipped at one. It proves finite uniform \(T_K(\epsilon)\) for every positive \(\epsilon\).

For sufficiently large \(n\), take \(M=n/(\log n)^2\). Then
\[
b=K/[\log n-2\log\log n-1],\quad
\exp[-n(1-b)/M]=\exp[-(1-b)(\log n)^2].
\]
Multiplying the preceding bound by \(\log n\) gives
\[
\limsup_{n\to\infty}(\log n)R_K(n)\le K.
\]

## 3. Exact two-state lower bound

Use state 1 as a rare target region:
\[
\pi(1)=p,\quad q(1)=r,\quad 0<r<p<1.
\]
The IMH transition probabilities are
\[
P(0,1)=r,\qquad P(1,0)=r(1-p)/p.
\]
Consequently,
\[
qP^n(1)=p+(r-p)(1-r/p)^n,
\]
and the exact error is
\[
\boxed{\|qP^n-\pi\|_{\rm TV}=(p-r)(1-r/p)^n.}
\]

Set \(r=p\exp(-K/p)\). This already satisfies the KL budget:
\[
D(\pi\Vert q)
 =K+(1-p)\log\frac{1-p}{1-r}<K.
\]
No normalization correction is necessary for feasibility. One may solve a scalar binary-KL equation to saturate the constraint if finite-parameter constants matter.

For large \(n\), set
\[
p_n=\frac{K}{\log n+2\log\log n},
\quad
r_n=p_n e^{-K/p_n}
 =\frac{p_n}{n(\log n)^2}.
\]
Then \(n r_n/p_n=(\log n)^{-2}\to0\), so
\[
(p_n-r_n)(1-r_n/p_n)^n\sim p_n\sim K/\log n.
\]
This gives \(\liminf(\log n)R_K(n)\ge K\), proving the sharp risk asymptotic.

Alternatively, directly for mixing time, choose
\(p_\epsilon=\epsilon(1+\sqrt\epsilon)\) and
\(r_\epsilon=p_\epsilon e^{-K/p_\epsilon}\). The exact threshold satisfies
\[
t_\epsilon=
\left\lceil
\frac{\log[\epsilon/(p_\epsilon-r_\epsilon)]}
     {\log(1-r_\epsilon/p_\epsilon)}
\right\rceil
\sim e^{K/p_\epsilon}\log[(p_\epsilon-r_\epsilon)/\epsilon],
\]
hence \(\epsilon\log t_\epsilon\to K\).
Together with the upper bound this proves the claimed sharp leading exponent.

An alternative way to deduce the mixing-time statement from the risk statement is to use TV contraction and monotonicity: for any \(a<K<b\), eventually \(a/\log n\le R_K(n)\le b/\log n\), and invert the two inequalities. Integer rounding does not affect the limit.

## 4. Important limitations that must accompany this theorem

1. **Algorithm-specific, not universal computational hardness.** The two-state target is explicitly sampleable in constant time if its probabilities are available. The result is about the performance of IMH from its proposal. It does not lower-bound all samplers under the usual unrestricted target information. A broader oracle lower bound would require a separately specified and justified information model.

2. **The worst-case pair changes with accuracy.** For a fixed \((\pi,q)\) with finite KL, \(\int(\log w)_+\,d\pi<\infty\), so
   \[
   t\,\pi(\log w>t)\to0.
   \]
   Indeed the negative part is integrable because
   \(\int_{\{w<1\}}-w\log w\,dq\le1/e\).
   The same coupling with \(M=n/(\log n)^2\) then gives
   \[
   (\log n)\|qP^n-\pi\|_{\rm TV}\to0
   \]
   for each fixed pair. Thus no fixed finite-KL pair attains the positive constant \(K\). Do not describe the minimax result as the asymptotic rate of every fixed trained proposal.

3. **Initialization matters.** An arbitrary initial state can already lie in an arbitrarily high-weight trap. Forward KL alone then gives no uniform bound at a fixed TV accuracy. The \(X_0\sim q\) hypothesis is essential.

4. **Reverse KL is different.** The proof depends on \(D(\pi\Vert q)\), not \(D(q\Vert\pi)\), and cannot silently be applied to variational reverse-KL training.

5. **Exact target invariance does not mean a finite-time exact draw.** The result concerns TV approximation after an exactly invariant MH transition.

6. The root should obtain literature clearance before claiming novelty; this derivation may sharpen or restate known IMH explicit-rate results.

## 5. A counterexample to an unrestricted local/global hybrid extension

A useful and less obvious obstruction is that arbitrary \(\pi\)-reversible local MH moves can destroy the proposal-start guarantee. This is not merely a constant penalty from using fewer global proposals.

Fix \(K>0\), let \(c=K/4\) and \(b=1-e^{-K/4}\). On the fixed three-node path \(A-B-C\), for sufficiently small \(p>0\) define
\[
s=p e^{-2c/p},\quad r=p e^{-c/p},
\]
\[
\pi=(p,s,1-p-s),\qquad q=(r,b,1-b-r).
\]
All entries are positive. Directly,
\[
D(\pi\Vert q)
 =c+s\log(s/b)+(1-p-s)\log\frac{1-p-s}{1-b-r}
 \longrightarrow c-\log(1-b)=K/2<K.
\]
An explicit sufficient finite range is
\[
0<p\le p_0:=\min\{1/4,e^{-c}b\}.
\]
Then \(s\le p\le b\), so the entrance contribution to KL is nonpositive; \(q_C=e^{-c}-r\ge e^{-2c}\); and \(\pi_C\log(\pi_C/q_C)\le-\log q_C\le2c\). Hence
\[
D(\pi\Vert q)\le3c=3K/4<K
\]
throughout this explicit range. Also \(\pi_C\ge1/2\) and \(w_C\le e^{2c}\le e^{c/p}=w_A\), so the claimed ordering of weights and every transition formula below hold in this finite range.

Let \(G\) be global independence MH with proposal \(q\). For small \(p\), \(A\) has the largest likelihood ratio, so its exact global exit probability is
\[
h_G=(1-p)e^{-c/p}.
\]

Let \(L\) be ordinary random-walk MH using a *fixed symmetric proposal* on the path: from \(B\), propose \(A\) or \(C\) with probability \(1/2\) each; at endpoints propose \(B\) with probability \(1/2\) and self otherwise. Then
\[
L_{BA}=L_{BC}=1/2,\quad
L_{AB}=s/(2p)=\tfrac12 e^{-2c/p},\quad
L_{CB}=s/[2(1-p-s)].
\]
The remaining probability stays put. Thus \(L\) is irreducible, aperiodic and \(\pi\)-reversible, with exact exit probability from \(A\)
\[
h_L=\tfrac12e^{-2c/p}.
\]
This is a standard local MH kernel, not an artificially nonlocal or nonreversible update.

### Mixture

For \(H=\alpha G+(1-\alpha)L\), \(0<\alpha<1\), initialization \(q\) puts mass \(b\) in \(B\). With probability \((1-\alpha)/2\), the first update moves this mass into \(A\). Hence for \(n\ge1\),
\[
qH^n(A)\ge
 \frac{b(1-\alpha)}2(1-h_H)^{n-1},
\quad
h_H=\alpha h_G+(1-\alpha)h_L.
\]
Therefore
\[
\|qH^n-\pi\|_{\rm TV}\ge
 \frac{b(1-\alpha)}2(1-h_H)^{n-1}-p.
\]
For every fixed \(n\), the lower bound tends to \(b(1-\alpha)/2\) as \(p\downarrow0\). Consequently, for every
\[
0<\epsilon<b(1-\alpha)/2,
\]
the worst-case mixing time of this hybrid family is infinite under the same fixed KL constraint, whereas pure IMH has the finite bound above.

### One local and one global step per cycle

For a cycle \(LG\), the first local step puts at least \(b/2\) into \(A\), and the subsequent global step retains a fraction \(1-h_G\). Each later cycle retains at least \((1-h_L)(1-h_G)\). Thus
\[
q(LG)^n(A)\ge
 \frac b2(1-h_G)[(1-h_L)(1-h_G)]^{n-1}.
\]
For a cycle \(GL\), the event \(X_0=B\), first global proposal \(B\), then local proposal \(A\), has probability \(b^2/2\), so
\[
q(GL)^n(A)\ge
 \frac{b^2}{2}[(1-h_G)(1-h_L)]^{n-1}.
\]
Both limits are positive at every fixed cycle count as \(p\downarrow0\). Thus the failure survives matching the number of global proposals; an extra local step can create a large transient trapping component absent from the pure-IMH proposal-start guarantee.

This does not contradict spectral-gap/Dirichlet-form comparison. The small-target-mass slow mode already exists in pure IMH but has negligible initial amplitude under \(q\); the local update moves large initial proposal mass into it. A uniform warmness or reverse-divergence control would change the admissible family and needs a separate theorem.

At finite \(p\), every integer \(n\ge1\) satisfying
\[
\frac{b(1-\alpha)}2(1-h_H)^{n-1}>\epsilon+p
\]
is rigorously insufficient for mixture mixing to accuracy \(\epsilon\). This supplies a directly evaluable resource lower bound, without taking an asymptotic limit.

## 5a. A valid but limited scheduling repair

If one first performs \(m\) pure IMH steps from a fresh \(q\) draw, then applies any Markov kernel \(L_*\) satisfying \(\pi L_*=\pi\), the same pure bound remains valid:
\[
\|qG^mL_*-\pi\|_{\rm TV}
\le\|qG^m-\pi\|_{\rm TV}.
\]
This is ordinary total-variation contraction under a Markov kernel. A fixed composition of invariant local kernels, or an externally randomized mixture whose randomness is independent of the chain, is allowed. Selecting a supposedly invariant kernel based on the current state or trajectory need not make the resulting overall update invariant; that adaptation requires its own proof. The scheduling repair certifies preservation of accuracy after the pure-IMH budget, and does not itself prove a smaller required budget or acceleration.

## 6. Suggested precise continuation

The immediate constructive question is which additional, realistically checkable control on the initial proposal or local kernel restores a uniform hybrid guarantee, and whether a hybrid scheme can enforce that control without knowing the target normalizer. Candidate hypotheses include bounded proposal-to-target density or a controlled reverse divergence, but neither is established here. Another route is an algorithm that always preserves the pure-IMH proposal-start comparison rather than assuming local invariant moves can only help.

The pure-IMH theorem should remain scoped to its exact algorithm; the hybrid counterexample is a genuine warning against a common but unjustified extension.

