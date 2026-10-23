# Matching the two screening exponents is a robustness condition

Principal extension: Astra PRO3, 22 October 2026 Australia/Brisbane.
This consequence was developed after the complete reciprocal-proposal proof
and the contributed q-only-screen counterexample. It is a classification
within an explicitly defined two-power family, not a claim that all robust
screens must have this form. It neither changes nor reopens the accepted
symmetric critical law.

## 1. Family and exact statement

Keep the enlarged finite class from RECIPROCAL_PROPOSAL_THEOREM.md:
positive pi,q, one population D(pi||q)<=K, fixed alpha in (0,1), beta=1-alpha,
fixed target-independent row-stochastic Q with reciprocal off-diagonal support,
start q, and the actual lazy mixture with proposal-q IMH G. On each proposal
edge define, for eta>0 and kappa>=0,

\[
 S_{xy}=(q_y/q_x)^\eta(Q_{yx}/Q_{xy})^\kappa,
 \qquad r_\pi(x,y)=\pi_yQ_{yx}/(\pi_xQ_{xy}),
\]
\[
 L_{\eta,\kappa}(x,y)=Q_{xy}\min(1,S_{xy})\min(1,r_\pi/S_{xy}),
 \quad C_{\eta,\kappa}=(I+\alpha G+\beta L_{\eta,\kappa})/2.    \tag{1}
\]

Complete L with its true rejection diagonal. Absent edges are not evaluated.
Both factors reverse reciprocally, so every such L is pi-reversible.
Both exponents and Q stay fixed during each run. Let R_(eta,kappa)(n)
be the proposal-start TV supremum over this class. A known K is an assumption,
not an estimated training quantity. Proposal and target access/cost conventions
are unchanged.

**Theorem 1 (fixed-power classification).** Fix 0<eta<1 and finite kappa>=0.

1. If kappa=eta, then
   \[
   \lim_{n\to\infty}(\log n)R_{\eta,\eta}(n)=K.              \tag{2}
   \]
2. If kappa!=eta, then
   \[
   \liminf_{n\to\infty}R_{\eta,\kappa}(n)
     \ge \frac{\beta(1-e^{-K})}{\alpha e^{-K}+\beta}>0.       \tag{3}
   \]

Thus equality of the two fixed exponents is necessary and sufficient for
uniform convergence in this power-factor family. Equation (3) is only a
lower floor, not an asserted exact minimax floor. Individual finite chains
remain irreducible and lazy, hence converge to pi.

**Theorem 2 (arbitrarily small mismatch can remain adverse).** More generally,
let positive eta_n and nonnegative kappa_n be deterministic across-run
policies with |eta_n-kappa_n|<=C for a finite constant C. If they differ on
infinitely many horizons, along those horizons there are admitted instances
whose TV tends to the positive expression

\[
 A_b=\frac{b\beta}{\alpha(1-b)+\beta},\qquad 0<b<1-e^{-K}.     \tag{4}
\]

Consequently a uniformly converging such policy on the unbounded-support
class must have kappa_n=eta_n eventually. This is a necessary condition only;
a matched screen tending to zero too quickly need not converge uniformly.
No moving-exponent sufficiency is supplied except the separately proved
matched critical policies. No bounded support or precision claim is implicit.

## 2. Balanced fixed exponents: complete upper and ordinary matching lower

When kappa=eta, (1) is exactly the full-Hastings screened kernel of the
principal theorem. Fix theta=min(eta/2,1/4)>0 and w=1. Its finite Lemmas 2-3
apply with p=1/(1-theta), tau=p(1-theta/eta), and H_1=F(1-tau), all fixed.

Write ell=log n, v=log ell. For sufficiently large n use

\[
 h=v^{-4},\quad R=n/\ell^4,\quad d_{test}=\ell^{-2},\quad
 N=\left\lceil\frac{8}{\alpha e^{-K}}\log\ell\right\rceil.    \tag{5}
\]

The entropy lower bound q(B)>=exp[-(K+H_2(h))/(1-h)] bounds global escape
away from zero. In the principal finite certificate, the uncapped bar e is
O(n^-1 ell^4 v^5) uniformly and tends to zero, so its cap is inactive.
Gamma_{theta,1}(bar e) is bounded by a fixed constant independent of Q,
support, atoms and n. Therefore, for a finite constant C1,

\[
 b^{1-\theta}\bar e^\theta\Gamma^{N/p}
 \le n^{-\theta}\ell^{C1}v^{5\theta}=o(1/\ell).              \tag{6}
\]

This bound pays the possibly growing accumulated multiplier explicitly;
Gamma is not assumed to tend to one. Smoothing and test errors are
O(ell^-2), the unhit mass is at most ell^-2, and initial bad mass is
o(ell^-1). The remaining high-W tail is at most
K/(ell-4 log ell-1), by the one population budget. Hence

\[
 \limsup(\log n)R_{\eta,\eta}(n)\le K.
\]

For the lower take Q=I, so L=I for every exponent pair. For any fixed k<K,
on two states put rare target mass p=k/log n and proposal mass
e=p/[n(log n)^2]. Then KL tends to k, all masses are positive eventually,
and the exact proposal-start error of the lazy mixture is

\[
 (p-e)\left(1-\frac{\alpha}{2n(\log n)^2}\right)^n
       \sim k/\log n.
\]

Let k increase to K. This proves (2). It is a new-class consequence of the
new finite operation and an unchanged ordinary lower, not a rerun of the
old symmetric fixed-screen campaign.

## 3. Two admitted geometries for a mismatch

Fix 0<b<b_K. Put, at integer horizon n sufficiently large,

\[
 e=b/n^4,\quad p=1/n,\quad t=1/n^3,\quad
 q_z=1-b-e,\quad\pi_z=1-p-t.                                \tag{7}
\]

The total root, leaf and core masses will always be (b,e,q_z) under q and
(t,p,pi_z) under pi. All are strictly positive. For each mismatched pair
write d=|eta-kappa|>0 and choose the finite integer

\[
 m=\left\lceil n^{4\eta/d}\right\rceil.                      \tag{8}
\]

It can be extremely large near equality; no degree or support cap is present
in the class. The proposal is public and depends only on n and the exponents,
not on pi or observations. It stays fixed throughout that run.

### Case I: eta>kappa, many roots feed one leaf

There are m roots r_i, one leaf l and one core z. Set

\[
 q(r_i)=b/m,\quad\pi(r_i)=t/m,\quad q(l)=e,\quad\pi(l)=p,
\]

with the core masses in (7). Use Q(r_i,l)=1, Q(l,r_i)=1/m, Q(z,z)=1.
The native, individual-state forward edge ratios are

\[
 q_l/q_{r_i}=m n^{-4},\quad Q_{lr_i}/Q_{r_il}=1/m,
 \quad r_q=n^{-4},\quad r_\pi=p/t=n^2.
\]

Thus the actual first-screen factor is

\[
 S=n^{-4\eta}m^{\eta-\kappa}.                              \tag{9}
\]

This includes the contributor's q-only example kappa=0, where m=n^4 and
the individual q masses are equal. For general exponents the individual
q masses need not be equal; their ratios have been retained explicitly.

### Case II: kappa>eta, one root feeds many leaves

There is one root r, m leaves l_i and one core z. Set

\[
 q(r)=b,\quad\pi(r)=t,\quad q(l_i)=e/m,\quad\pi(l_i)=p/m,
\]

and the same core. Use Q(r,l_i)=1/m, Q(l_i,r)=1, Q(z,z)=1. The native
edge ratios now are

\[
 q_{l_i}/q_r=n^{-4}/m,\quad Q_{l_ir}/Q_{rl_i}=m,
 \quad r_q=n^{-4},\quad r_\pi=p/t=n^2.
\]

Consequently

\[
 S=n^{-4\eta}m^{\kappa-\eta}.                              \tag{10}
\]

In both cases Q is row-stochastic with reciprocal support. Neither a
level mass nor a quotient proposal has been substituted in the native
acceptance ratio. Both have the same bound, since n^(4eta/d)<=m<=2n^(4eta/d):

\[
                       1\le S\le2^d.                      \tag{11}
\]

For fixed exponents this is eventually at most n^2. More generally it is
at most 2^C on every mismatch horizon in Theorem 2, again at most n^2
eventually, uniformly in the possibly varying exponent 4eta/d.
Therefore the actual total acceptance is EXACTLY one from root to leaf
and EXACTLY n^-2 in the reverse direction: min(1,S)min(1,n^2/S)=1,
while min(1,S^-1)min(1,n^-2 S)=n^-2.

### Admission uses one KL budget independently of multiplicity

In either geometry weights are constant on each block:
W_r=t/b,W_l=p/e=n^3/b,W_z=pi_z/q_z, with W_r<W_z<W_l eventually.
The complete KL is

\[
 D(\pi\|q)=t\log(t/b)+p\log(p/e)+\pi_z\log(\pi_z/q_z)
       \longrightarrow-\log(1-b)<K.                         \tag{12}
\]

The multiplicities cancel because individual pi and q have the same uniform
split within each nonsingleton block. This is actual KL of the full native
space, with strict eventual slack. It is independent of m and hence uniform
across the mismatch policies. No singular target or second budget is used.

## 4. Exact quotient and full-law limit

Permutation symmetry within roots in Case I, or within leaves in Case II,
proves strong lumpability into root block, leaf block, core. The initial
laws and every evolved law are uniform inside the nonsingleton block, so
native TV equals quotient TV. The ACTUAL quotient matrices are

\[
 L^\#=\begin{pmatrix}0&1&0\\n^{-2}&1-n^{-2}&0\\0&0&1\end{pmatrix},
\quad
 G^\#=\begin{pmatrix}
 b&e&q_z\\t/W_l&1-(1-p)/W_l&\pi_z/W_l\\t/W_z&e&1-t/W_z-e
 \end{pmatrix}.                                                \tag{13}
\]

In Case I, the root-block hold includes global moves between distinct
roots. In Case II, the leaf-block hold includes global moves between
distinct leaves. Those are not called individual-state rejections. The
native diagonal is completed before lumping; all of those moves remain.

Put a0=alpha q_z/2,c0=(alpha e+beta)/2,v=a0+c0 and

\[
 d_l=\alpha(1-p)/(2W_l)+\beta/(2n^2).
\]

This is the actual probability of leaving the ENTIRE leaf block in one
mixture step. Retaining the whole block, and allowing all moves within it,
gives the finite lower. First-core decomposition with the original remaining
chain gives the finite upper:

\[
 b(c0/v)[1-(1-v)^{\lfloor n/2\rfloor}](1-d_l)^n-p
 \le TV(qC^n,\pi)
 \le p+t+e+b(c0/v)+b(1-v)^n.                                 \tag{14}
\]

For the upper, the mass that has hit the core has remaining TV at most
TV(delta_z,pi)=p+t by contraction, with all subsequent returns. The residual
is at most e+b c0/v+b(1-v)^n. The lower simply selects root-origin paths
that reach the leaf block promptly and do not leave that block afterwards.
No actual path is deleted from the chain.

The quotient (13), its input masses and bounds (14) are independent of m,
eta and kappa once (11) is at most n^2. Since n d_l->0, v tends to a
positive constant and p,t,e->0, both bounds tend to A_b in (4).
This proves the fixed-pair adverse limit and the claimed limit along every
infinite mismatch subsequence for bounded d. Finally let fixed b increase
to b_K after taking the limit to obtain (3). There is no assertion that
the positive floor is optimal over the alternative class.

For comparison, on the SAME input a matched full-Hastings first screen
has forward factor n^-4eta and reverse acceptance n^-2 n^-4eta in either
geometry. For fixed eta>0 the first-core upper is O(n^-1+n^-4eta)->0.
Pure IMH on both native families satisfies, for deterministic j,

\[
 p-(j+1)e\le TV(qG^j,\pi)
       \le p+t+e/(1-b)+b^{j+1}.                             \tag{15}
\]

Hence it is asymptotic to n^-1 when j/n tends to a positive constant,
including matched expected global attempts. This is a distributional
comparison; known analytic block sampling and full caching remain allowed.

## 5. Consequence, resources and next boundary

The enlarged sharp law does not rely on proposal symmetry. Its uniform
robustness does rely, within this two-power factorization, on pairing the
proposal-density and reverse-proposal exponents. A deficit in the latter
can be defeated by many-to-one transport; an excess can be defeated by
one-to-many transport. Both constructions preserve reversibility and the
same KL budget. This identifies a structural condition stronger than
correctness of the invariant measure.

The small-mismatch statement is a worst-case unbounded-support fact. The
graph uses m=ceil(n^(4eta/|eta-kappa|)) labels in its large block; specifying
an index requires at least order log m bits, and proposal generation, target
evaluation, cache work and precision must be charged. No such large graph
was materialized and no numerical simulation is used to establish the limit.
A small discrepancy in coefficients is NOT equated with a bounded per-step
floating-point error, nor does this theorem claim any particular software
implementation is unstable. Exact use of one common exponent remains allowed.

Within practical proposal families, an a priori bound on proposal asymmetry
or degree may prohibit these multiplicities. The chosen next question is
the quantitative robustness boundary when that information is supplied:
how do a bound on |log(Q_yx/Q_xy)| and an allowed exponent mismatch combine
with eta_n to control reachable transport, retaining the one KL budget and
actual costs? No necessary-and-sufficient bound for that restricted class
is claimed here. Replacing the unbounded class by a bounded one must be an
explicit new information/resource contract, not a hidden restriction.

The counterexample relies on the contributed fan-in construction and its
full-return comparison; the principal supplied the general powers, the
opposite fan-out geometry, fixed-balanced upper and bounded moving-policy
obstruction. Source-bound review scope is recorded separately. Historical
novelty, external acceptance, formal verification and useful implementation
are unestablished. The exact original source chain is preserved unchanged.
