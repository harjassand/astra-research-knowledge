# Focused independent review: finite-band positive-tilt escape

**Reviewer:** `quantum_walk_comparison` (the helper previously responsible for the focused primary-literature comparison).  
**Source reviewed:** `../FINITE_BAND_ESCAPE.tex`, as read on 2026-10-21.  
**Scope:** The abstract finite-band escape lemma and the supplied heavy-tail counterexample. The separate coherent-moment/corrector proof is an input, not independently certified by this review. No capacity or novelty conclusion is inferred from escape alone.

## Verdict

I find the lemma correct under its stated hypotheses. In particular, the bounded correction need not itself have finite depth bandwidth. The stated second-order constant \(5+8M\), the sign of the tilt, the passage from additive drift to multiplicative operator contraction, and the uniformity over all normal initial densities survive direct checking.

The heavy-tail counterexample is also correct. Its precise logical role is to show that bounded positive drift alone does not imply exponential escape. Finite bandwidth is a sufficient hypothesis which rules out that counterexample; the example does not prove that finite bandwidth is necessary among all possible propagation or tail hypotheses.

No repair to a displayed inequality in the lemma is required. The expanded domain and compact-observable arguments below make explicit the points most likely to be misused when this operation is transferred.

## 1. Grade decomposition without a domain assumption

Write \(P_\ell\) for the finite-dimensional level projections and \(L_{\rm out}=L\otimes I_{\mathcal K}\). The bandwidth hypothesis is a statement about a particular bounded isometric dilation \(W\), not a statement only about one-use probabilities. For \(d\in\{-1,0,1\}\), define

\[
 W_d=\sum_{\ell\ge\max(0,-d)}
       (P_{\ell+d}\otimes I)WP_\ell.
\]

This series converges strongly. Its summands have orthogonal input spaces and orthogonal output depth spaces, so for every vector \(\psi\),

\[
 \|W_d\psi\|^2
 =\sum_\ell\|(P_{\ell+d}\otimes I)WP_\ell\psi\|^2
 \le\sum_\ell\|P_\ell\psi\|^2=\|\psi\|^2.
\]

Thus \(\|W_d\|\le1\). The bandwidth hypothesis gives \(W=W_{-1}+W_0+W_1\), first on finite-depth vectors and then everywhere by boundedness. This directly verifies the Fourier-coefficient construction used in the source without needing to interchange unbounded operators and integrals.

On the finite-depth core,

\[
 L_{\rm out}W-WL=W_1-W_{-1}.
\]

The right side is bounded. In fact this identity also shows \(W\operatorname{Dom}(L)\subseteq\operatorname{Dom}(L_{\rm out})\): approximate a domain vector by finite-depth truncations and use closedness of \(L_{\rm out}\). All appearances of \(W^\dagger L_{\rm out}W\) needed by the proof are consequently legitimate on the stated core. The proof does not require a normal input state to have a finite depth moment.

## 2. The exponential conjugation is genuinely bounded

For \(Z_t=e^{-tL/2}\), define directly

\[
 W_t=e^{t/2}W_{-1}+W_0+e^{-t/2}W_1.
\]

This is bounded. Its formal representation

\[
 W_t=(Z_t\otimes I)We^{tL/2}
\]

is only initially asserted on the finite-depth core. The bounded identity which is actually used later is

\[
 W_tZ_t=(Z_t\otimes I)W. \tag{R1}
\]

Both sides of (R1) are bounded, and their equality on the core extends to the whole space. Thus for every bounded operator \(A\),

\[
 \Phi^*(Z_tAZ_t)
 =Z_tW_t^\dagger(A\otimes I)W_tZ_t. \tag{R2}
\]

There is no use of \(e^{tL/2}\) on an arbitrary vector and no use of a conjugation of the form \(e^{tL/2}Ce^{-tL/2}\). In particular **arbitrary bounded selfadjoint \(C\) is permitted**; no unmentioned bandwidth or domain-invariance condition on \(C\) is needed.

## 3. Independent check of the remainder constant

Set

\[
 D_t=W_t-W,\qquad D'=\frac12(W_{-1}-W_1),
 \qquad E_t=D_t-tD'.
\]

For \(0\le t\le1\), the nonnegative scalar coefficients give

\[
 \|D_t\|\le e^{t/2}-e^{-t/2}=2\sinh(t/2)\le2t,
\]

\[
 \|E_t\|
 \le(e^{t/2}-1-t/2)+(e^{-t/2}-1+t/2)
 =2(\cosh(t/2)-1)\le t^2/2.
\]

The last inequality follows, for example, from \(\cosh x-1\le x^2\) on \(0\le x\le1/2\). Since \(W^\dagger W=I\),

\[
 W_t^\dagger W_t-I-t(W^\dagger D'+D'^\dagger W)
 =W^\dagger E_t+E_t^\dagger W+D_t^\dagger D_t,
\]

whose norm is at most \(2(t^2/2)+(2t)^2=5t^2\). No term of first order or mixed second order has been discarded.

The grade commutator and isometry identity imply, as forms on the core,

\[
 W^\dagger D'+D'^\dagger W=L-W^\dagger L_{\rm out}W
 =L-\Phi^*(L).
\]

The left side is bounded, so it supplies the unique bounded extension of this difference. For \(\|C\|\le M\),

\[
 \|W_t^\dagger(C\otimes I)W_t-W^\dagger(C\otimes I)W\|
 \le M(2\|D_t\|+\|D_t\|^2)
 \le8Mt.
\]

With \(\mathfrak T_t(A)=W_t^\dagger(A\otimes I)W_t\) and \(A_t=I-tC\), these two estimates therefore give exactly

\[
 \mathfrak T_t(A_t)-A_t=-tK+\mathcal R_t,
 \qquad \|\mathcal R_t\|\le(5+8M)t^2.
\]

The remainder is selfadjoint. Hence its norm bound is a valid upper bound in the Loewner order, which is what the next step needs.

## 4. Positivity and the multiplicative contraction

The assumptions \(tM\le1/2\) and \(t(5+8M)\le\nu/2\) give

\[
 \tfrac12I\le A_t\le\tfrac32I,
 \qquad
 \mathfrak T_t(A_t)\le A_t-\tfrac12\nu tI.
\]

Since \((\nu t/3)A_t\le(\nu t/2)I\),

\[
 \mathfrak T_t(A_t)\le(1-\nu t/3)A_t=\lambda A_t.
\]

The direction of this inequality is correct: the upper bound on \(A_t\), rather than its lower bound, is the relevant comparison. The separate requirement \(\nu t<3\) ensures \(0<\lambda<1\). By (R2), conjugating this bounded inequality by \(Z_t\) gives

\[
 \Phi^*(X_t)\le\lambda X_t,
 \qquad X_t=Z_tA_tZ_t.
\]

Also

\[
 (1-tM)e^{-tL}\le X_t\le(1+tM)e^{-tL}.
\]

This argument never exponentiates the drift inequality for \(L+C\), and it does not assume that the scalar exponential is operator monotone. Such a substitution would be unjustified in general; the bounded positive tilt is what avoids it.

## 5. Escape, compactness, and quantifiers

Positivity and iteration yield

\[
 \operatorname{Tr}(X_t\Phi^n(\tau))
 \le\lambda^n\operatorname{Tr}(X_t\tau)
 \le(1+tM)\lambda^n
\]

for every positive trace-class density \(\tau\). No integrability assumption involving \(L\) occurs. For every real \(h\ge0\), spectral calculus gives

\[
 P_{\le h}\le e^{th}e^{-tL}
 \le\frac{e^{th}}{1-tM}X_t.
\]

Pairing with \(\Phi^n(\tau)\) proves the first claimed bound. The inequalities \((1+tM)/(1-tM)\le3\) and \(\lambda^n\le e^{-\nu tn/3}\) prove the second one. The constants are independent of \(\tau\), so the estimate really is uniform over all normal initial densities. This is stronger than merely obtaining one estimate for the selected stationary bath of the unperturbed device.

For \(h=vn\) with \(0\le v<\nu/3\), the explicit exponent is \(-t(\nu/3-v)n\). For a negative \(v\), the low-depth projection is empty once \(n>0\), so the source's broader phrase “every \(v<\nu/3\)” is harmless with that convention. Nonnegative speeds would be the clearest formulation.

Each level is finite dimensional, so \(Z_t\) is compact. Hence \(X_t\) is compact. It is injective because

\[
 \langle\psi,X_t\psi\rangle\ge\tfrac12\|Z_t\psi\|^2>0
\]

for every nonzero \(\psi\). Any nonzero normal positive density has strictly positive expectation of this injective positive operator. An invariant normal density would contradict the strict contraction of that expectation.

For completeness, compact-observable escape follows without assuming diagonal bath states. Let \(Q\) be any compact operator and \(P=P_{\le h}\). Then \(\|Q-PQP\|\to0\) as \(h\to\infty\), while

\[
 |\operatorname{Tr}(PQP\Phi^n(\tau))|
 \le\|Q\|\operatorname{Tr}(P\Phi^n(\tau)).
\]

First send \(n\to\infty\) at fixed \(h\), then \(h\to\infty\). This proves convergence against every compact operator, including operators with off-diagonal level blocks. It does not assert trace-norm convergence to zero or exclude singular invariant states supported at infinity.

Finite-dimensionality of levels is needed for the asserted compactness of \(X_t\). The exponential depth estimate itself uses the level decomposition and the finite-band dilation, but not the dimensions of the levels. The compact-observable convergence argument also only uses \(P_{\le h}\uparrow I\) strongly and the mass bound: compression converges in norm for each compact \(Q\), even if a level has infinite dimension.

## 6. Independent check of the counterexample

Let the classical increments have distribution

\[
 \Pr(X=1)=\tfrac34,
 \qquad
 \Pr(X=-2^j)=\tfrac3{16}4^{-j},\quad j\ge0,
\]

and let \(Y_{n+1}=\max(0,Y_n+X_{n+1})\). The negative probabilities sum to \(1/4\), so this is a probability distribution. At a state \(y\in\mathbb N_0\),

\[
 \delta(y)=\mathbb E[Y_{n+1}-Y_n\mid Y_n=y]
 =\tfrac34-\tfrac3{16}\sum_{j\ge0}4^{-j}\min(y,2^j).
\]

Since

\[
 0\le\tfrac3{16}\sum_{j\ge0}4^{-j}\min(y,2^j)
 \le\tfrac3{16}\sum_{j\ge0}2^{-j}=\tfrac38,
\]

one has \(3/8\le\delta(y)\le3/4\). In particular the drift is a bounded positive operator with \(C=0\).

This is also a normal quantum-channel counterexample on \(\ell^2(\mathbb N_0)\). A countable Kraus representation is

\[
 K_{y,x}=\sqrt{p_x}\,|\max(0,y+x)\rangle\langle y|,
 \qquad \sum_{y,x}K_{y,x}^\dagger K_{y,x}=I
\]

in the strong topology. It removes position coherences and then performs the stated transition. On the finite-coordinate core,

\[
 \Phi^*(L)-L=\sum_{y\ge0}\delta(y)|y\rangle\langle y|,
\]

which has a bounded extension between \((3/8)I\) and \((3/4)I\). The channel has arbitrarily long downward transitions, so it cannot have a fixed finite depth-bandwidth dilation.

Starting from \(Y_0=0\), every path satisfies \(Y_{n-1}\le n-1\). For \(n\ge1\), put \(J=\lceil\log_2 n\rceil\). A final increment from the set \(\{-2^j:j\ge J\}\) forces \(Y_n=0\), regardless of the earlier history. Consequently

\[
 \Pr(Y_n=0)
 \ge\sum_{j\ge J}\tfrac3{16}4^{-j}
 =\tfrac14,4^{-J}
 \ge\frac1{16n^2}.
\]

This contradicts every bound \(\Pr(Y_n=0)\le A e^{-cn}\) with fixed \(A<\infty\) and \(c>0\) for all sufficiently large \(n\).

The exact failed step in the tilt proof can be located. For any \(t>0\), the squared norm of the formal weighted dilation on a coordinate vector is

\[
 \|W_t|y\rangle\|^2
 =e^{ty}\,\mathbb E[e^{-tY_1}\mid Y_0=y]
 \ge e^{ty}\Pr(X\le-y).
\]

For integers \(y\ge1\), the same geometric-tail calculation bounds the last probability below by \(1/(16y^2)\). Thus this norm is unbounded as \(y\to\infty\). The first-order drift exists and is uniformly favorable, but no bounded positive exponential deformation exists by this route. This is a genuine failure of the missing tail hypothesis, not an artifact of a loose Taylor constant.

## 7. Scope and receiving instruction

The receiver may reuse the abstract lemma with the assumptions exactly as stated. The actual device's purified one-step dilation must have bath-depth bandwidth one, and its bounded correction and positive drift bound must be supplied independently. For the qutrit repeated-interaction channel, the stated blocks \(R,S_1,S_2,S_1^\dagger,S_2^\dagger,I\) do have depths \(0,+1,+1,-1,-1,0\), respectively; purification of the finite-dimensional port input does not change these grades. This explains why the abstract finite-band interface is appropriate, without redoing the separate corrector proof.

Escape invalidates any proposed proof which requires this bath orbit to remain uniformly tight in finite-depth coordinates. Escape alone is not a capacity converse: a coding argument may retain information through mechanisms other than coordinate tightness, and the total-channel coherent-information or arbitrary-reference error analysis remains a separate obligation.

This review is internal mathematical checking, not external certification or a historical-priority finding. No broad literature search, numerical simulation, theorem rerun, external communication, purchase, or upload was performed for this focused review. The source was read once and the estimates and counterexample were checked analytically. Exact wall-time and cumulative discovery cost were not instrumented; they are unknown.
