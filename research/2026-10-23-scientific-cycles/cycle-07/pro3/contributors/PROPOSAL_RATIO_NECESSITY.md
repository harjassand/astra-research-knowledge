# Reciprocal-proposal screening is structurally necessary

Independent bounded construction for Cycle7 by
`/root/proposal_ratio_counterexample`, 22 October 2026 Australia/Brisbane.
The principal owns the main broader-class weighted-absorption theorem. This
note constructs a distinct failure when the proposal ratio is omitted from
the FIRST screen, despite retaining it in the final Metropolis-Hastings ratio.
It neither challenges nor assumes the principal's new theorem.

## 1. Two different reversible kernels on exactly the same inputs

Fix K>0 and alpha in (0,1), and let beta=1-alpha. An instance has finite,
strictly positive pi,q and a fixed target-independent row-stochastic proposal
Q with reciprocal off-diagonal support. The normalizer cancels from every
target ratio. Define, on an edge with Q_xy>0,

\[
 r_\pi(x,y)={\pi_yQ_{yx}\over\pi_xQ_{xy}},\qquad
 r_q(x,y)={q_yQ_{yx}\over q_xQ_{xy}}.
\]

The requested full-Hastings screen is

\[
 \overline L_\eta(x,y)=Q_{xy}\min(1,r_q(x,y)^\eta)
                       \min(1,r_\pi(x,y)/r_q(x,y)^\eta).
                                                        \tag{1}
\]

For comparison, define the DIFFERENT q-only first screen

\[
 \widetilde L_\eta(x,y)=Q_{xy}\min(1,(q_y/q_x)^\eta)
                 \min(1,r_\pi(x,y)(q_x/q_y)^\eta).         \tag{2}
\]

Both have their actual rejection diagonals. Both are pi-reversible: the two
positive factors multiply to r_pi and reverse reciprocally. For any positive
factors a,b, min(1,a)min(1,b) divided by the analogous reversed acceptance is
ab. Consequently the directed accepted-flow ratio in either (1) or (2) is
r_pi, which is the detailed-balance condition with proposal Q. Reversibility
therefore does not distinguish these kernels.

Let G be independence MH with proposal q, and form the actual lazy mixtures

\[
 \overline C_\eta=(I+\alpha G+\beta\overline L_\eta)/2,
 \qquad
 \widetilde C_\eta=(I+\alpha G+\beta\widetilde L_\eta)/2,
                                                        \tag{3}
\]

both initialized at q. Eta and all inputs are fixed within each run. Neither
kernel in this note is an auxiliary absorbed process.

## 2. An explicit growing, positive, target-independent family

Choose any fixed b with

\[
             0<b<b_K:=1-e^{-K}.                          \tag{4}
\]

A rational b in this interval may be chosen if an entirely rational input
family is desired. For integer horizon n>=2 let

\[
 m=n^4,\qquad e={b\over m},\qquad p={1\over n},
 \qquad t={1\over n^3}={p\over n^2}.                      \tag{5}
\]

The labelled space consists of m roots r_1,...,r_m, one leaf l, and one core
z. Define individual-state probabilities by

\[
 q(r_i)=e,\quad q(l)=e,\quad q(z)=q_z:=1-b-e;
\]

\[
 \pi(r_i)={t\over m},\quad \pi(l)=p,
 \quad \pi(z)=\pi_z:=1-p-t.                              \tag{6}
\]

All probabilities are strictly positive and sum to one for sufficiently
large n. In particular no target or proposal is singular. The proposal is

\[
 Q(r_i,l)=1,\qquad Q(l,r_i)=1/m\quad(1\le i\le m),
 \qquad Q(z,z)=1,                                       \tag{7}
\]

and all other entries are zero. Thus Q is row-stochastic, has reciprocal
off-diagonal support, and is asymmetric for m>1. It depends only on the
label count m=n^4. It can be chosen before pi or even b is specified, so it
is target-independent in the declared sense. Q is fixed throughout a run;
the permitted class supremum allows the number of labels to grow with n.

This is a native m+2-state construction. The three-state calculation below
is its proved exact quotient, not a replacement of its acceptance ratios
by level masses.

### One KL budget and weight ordering

The root weight is constant on the root block:

\[
 W_r={t\over b},\qquad W_l={p\over e}={n^3\over b},
 \qquad W_z={\pi_z\over q_z}.
                                                        \tag{8}
\]

Eventually W_r<W_z<W_l. The exact forward KL is

\[
 D(\pi\|q)=t\log(t/b)+p\log(p/e)
              +\pi_z\log(\pi_z/q_z).                    \tag{9}
\]

For sufficiently large n the root term is negative. Since pi_z<=1, the
core term is at most log(1/q_z). Hence

\[
 D(\pi\|q)\le {1\over n}\log(n^3/b)
                    +\log{1\over1-b-b/n^4}
 \longrightarrow -\log(1-b)<K.                          \tag{10}
\]

The whole family is therefore admitted eventually with strict slack in the
SINGLE population KL budget. No fitted/training loss or separate tail budget
has been substituted.

## 3. The individual-state ratios and exact lumping

On r_i->l, q_l/q_ri=1, whereas

\[
 r_q(r_i,l)=1/m,\qquad
 r_\pi(r_i,l)={p/m\over t/m}=p/t=n^2.                  \tag{11}
\]

The reverse ratios are m and n^-2. For the q-only first screen (2), the
first acceptance is one on every root-leaf edge for EVERY eta>0. The
forward second acceptance is one and the reverse is n^-2. The resulting
local root-to-leaf probability is one. The reverse proposal probability
1/m is still present on each individual edge: after summing all roots,
the actual leaf-to-root-block probability is n^-2.

For the full-Hastings screen (1), the forward first acceptance is

\[
                        \sigma=m^{-\eta}=n^{-4\eta},   \tag{12}
\]

and its second acceptance is one. The reverse first acceptance is one,
and its second is sigma/n^2. Thus, AFTER computing native ratios, the two
local quotient matrices on (root block,leaf,core) are unified as

\[
 L^{(\sigma)}=
 \begin{pmatrix}
 1-\sigma&\sigma&0\\
 \sigma/n^2&1-\sigma/n^2&0\\
 0&0&1
 \end{pmatrix},                                         \tag{13}
\]

with sigma=1 for (2), and sigma=m^-eta for (1). All displayed diagonal
entries are the actual rejection/holding probabilities.

The global independence kernel has quotient

\[
 G^{\rm lump}=\begin{pmatrix}
 b&e&q_z\\
 t/W_l&1-(1-p)/W_l&\pi_z/W_l\\
 t/W_z&e&1-t/W_z-e
 \end{pmatrix}.                                         \tag{14}
\]

Every row belonging to a root has identical total transition probability
to each of the three blocks, and the other blocks are singletons. This
proves strong lumpability of both local and global kernels, hence of their
mixtures, under the root/leaf/core map. It preserves all root-to-root
global moves as holds of the root block.

The input laws q and pi are uniform within the root block, and every
transition is equivariant under root permutations. Every evolved law
q C^j is consequently uniform within that block. For these laws, total
variation in the full native space equals total variation of the exact
three-state quotient: summing the m equal root discrepancies gives the
absolute discrepancy of their total mass. Thus every full-law TV statement
below is a statement about the actual m+2-state chain.

## 4. A full-law finite sandwich retaining every return

For any sigma in (0,1] use the genuine mixture

\[
 C^{(\sigma)}=(I+\alpha G^{\rm lump}+\beta L^{(\sigma)})/2.
\]

Set

\[
 a_0={\alpha q_z\over2},\qquad
 c_0={\alpha e+\beta\sigma\over2},\qquad
 v=a_0+c_0,\qquad H=\lfloor n/2\rfloor.
                                                        \tag{15}
\]

At the root block, the actual core exit probability is a_0, leaf exit is
c_0, and holding probability is 1-v. The actual leaf escape probability is

\[
 d_l={\alpha(1-p)\over2W_l}
                 +{\beta\sigma\over2n^2}.               \tag{16}
\]

Starting in the root block, the probability of first exiting to the leaf
by H is exactly (c_0/v)[1-(1-v)^H]. Restrict to such paths which then
stay at the leaf. Their conditional retention probability is at least
(1-d_l)^n. The leaf event yields the exact finite lower bound

\[
 \|q(C^{(\sigma)})^n-\pi\|_{\rm TV}
 \ge b{c_0\over v}[1-(1-v)^H](1-d_l)^n-p.                \tag{17}
\]

The full-chain upper uses tau_z, the first core hit, including time zero.
Paths that start in the leaf have total mass e. Starting in the root
block, failure to hit the core by n is bounded by the probability of first
exiting to the leaf (at most c_0/v) plus the probability of not exiting
the root block at all ((1-v)^n). Thus

\[
                   \Pr_q(\tau_z>n)
                    \le e+b c_0/v+b(1-v)^n.             \tag{18}
\]

After any core hit at time j<=n, the remainder of the path follows the
ORIGINAL full kernel. TV contraction and invariance imply

\[
 \|\delta_z(C^{(\sigma)})^{n-j}-\pi\|_{\rm TV}
       \le\|\delta_z-\pi\|_{\rm TV}=1-\pi_z=p+t.
\]

Conditioning on the unnormalized first-core-hit measures and the residual
therefore gives the finite upper

\[
 \|q(C^{(\sigma)})^n-\pi\|_{\rm TV}
       \le p+t+e+b c_0/v+b(1-v)^n.                       \tag{19}
\]

Every return from the core, leaf or roots is retained in the original
post-hit evolution. Equation (17) merely selects a positive lower event;
(19) separately controls the full law. There is no killed-row normalization,
optional-horizon substitution or inference from an induced-norm witness.

## 5. Positive error floor for the misplaced screen

For the q-only first screen, sigma=1 for all eta. In this case,

\[
 v\longrightarrow {\alpha(1-b)+\beta\over2}>0,
 \qquad {c_0\over v}\longrightarrow
                   {\beta\over\alpha(1-b)+\beta},
\]

and

\[
 n d_l={\alpha b(1-p)\over2n^2}+{\beta\over2n}
                       \longrightarrow0.               \tag{20}
\]

The waiting errors in (17) and (19) vanish exponentially. Also p,t,e->0.
Both sides of the full-law sandwich thus give

\[
 \boxed{\displaystyle
 \lim_{n\to\infty}\|q_n\widetilde C_{\eta_n}^{\,n}-\pi_n\|_{\rm TV}
   ={b\beta\over\alpha(1-b)+\beta}>0.}                  \tag{21}
\]

This holds for EVERY positive deterministic policy eta_n, since this entire
native family's q-only screened kernel is independent of eta. In particular
it holds for every fixed eta>0, arbitrarily large eta, and the proposed
shrinking-screen critical policies.

Each individual finite chain is still irreducible and lazy, because alpha>0
and the positive independence-MH component connects all states. The failure
is of uniform convergence over the growing admitted class, not convergence
of a fixed finite instance or correctness of its invariant distribution.

If the supremum is taken over the declared q-only-screen class, (21) implies
the rigorous uniform-floor lower bound

\[
 \liminf_{n\to\infty}\sup_{\rm q\text{-}only\ class}
    \|q\widetilde C_{\eta_n}^{\,n}-\pi\|_{\rm TV}
 \ge {\beta(1-e^{-K})\over\alpha e^{-K}+\beta}.           \tag{22}
\]

To obtain (22), first apply (21) to each fixed b<b_K with its strict KL
slack, then let b increase to b_K in the continuous increasing expression.
No single instance spends two information budgets. Equation (22) is a
LOWER bound for that alternative class; this note does not assert an exact
minimax floor or its optimality over all alternative proposals.

## 6. Correct screening and ordinary IMH on the same public instance

For the requested full-Hastings screen, sigma=n^-4eta. For every fixed
eta>0, a_0 is bounded away from zero, while c_0=O(n^-4+n^-4eta).
The same full-law upper (19) proves

\[
 \|q_n\overline C_\eta^{\,n}-\pi_n\|_{\rm TV}
      =O(n^{-1}+n^{-4\eta})\longrightarrow0.             \tag{23}
\]

All q,Q,target values, initial laws and mixture coefficients are identical
in (21) and (23). The changed first-screen ratio detects that m distinct
roots are funneled toward one leaf. Proposal symmetry alone is not the
scientific issue: the inverse proposal budget must appear in the first
screen to prevent this particular hidden concentration.

For pure IMH on the same instance, at any deterministic integer horizon j,

\[
 p-(j+1)e\le\|qG^j-\pi\|_{\rm TV}
        \le p+t+{e\over1-b}+b^{j+1}.                    \tag{24}
\]

For the lower, occupation of the leaf requires either leaf initialization
or at least one proposal of it. For the upper, repeat the exact first-core
argument with pure G: its root-to-leaf/core exit ratio is e/(1-b), its
root-block hold is b, and its post-core contraction error is p+t. Combining
the initial leaf mass with the root-to-leaf contribution gives e/(1-b).

If j_n/n tends to any fixed positive finite constant, (24) implies

\[
                \|q_nG^{j_n}-\pi_n\|_{\rm TV}\sim n^{-1}.
                                                        \tag{25}
\]

This includes j_n=floor(alpha n/2), matching expected global attempts in
the hybrid. The q-only-screen hybrid has a nonzero error limit on exactly
this same family; its TV ratio to pure IMH is asymptotic to the constant
in (21) times n. These are law comparisons, not target-evaluation or
wall-clock comparisons. The full-Hastings bound (23) does not assert that
its actual error beats pure IMH, either on this family or generally.

## 7. Exact finite fixture for optional bounded verification

The proof is analytic; no numerical asymptotic curve is used or needed.
For a small independently checkable native fixture take

    n=2, m=16, b=1/4, K=3, alpha=1/2, eta=1/4.

There are 18 actual states, with q(root_i)=q(leaf)=1/64 and q(core)=47/64;
pi(root_i)=1/128, pi(leaf)=1/2, pi(core)=3/8. The exact weight order is
W_root=1/2 < W_core=24/47 < W_leaf=32. KL<3 is certified without floating
logarithms: the root term is negative, the leaf term is (1/2)log32<5/2,
and the core term is at most log(64/47)<=17/47, whose sum is <3.

The q-only local forward acceptance is one, while the correct full-Hastings
forward acceptance is m^-eta=1/2. Every entry of the native G, both local
kernels and both mixtures is rational. It is therefore possible to verify
the native 18-state matrix against the exact three-state quotient, including
all diagonals, and compare exact finite powers with (17)-(19) and (24).
This fixture is supplied, not executed by this contributor. It is not an
asymptotic observation or a claim that n=2 approximates (21).

## 8. Scope, resources and provenance

The m+2-state graphs in (5)-(7) are defined implicitly; none was materialized
by this contributor. Exact uniform root proposals require an index of
ceil(log2 m) bits, and evaluating either proposal direction requires its
actual native probability. Eta stays fixed during each run. The proof's
three-state quotient is not free sampler access or a replacement oracle.
The actual target normalizer, all proposal and target evaluations, cache
operations and arithmetic precision retain their declared costs.

If the explicit normalized analytic family is given as sampler input, it
also permits direct block/categorical sampling followed by a uniform root
index when necessary. That stronger natural ordinary method is allowed;
the adversarial theorem does not hide it or make an implementation claim.
The purpose is to delimit a uniform robustness guarantee for an actual
kernel, even though its invariant distribution is correct.

The contributed construction uses the accepted first-core full-return
comparison from the read Cycle6 GLOBAL_BOUNDARY_THEOREM.md, Sections 7-8,
21,990 bytes, SHA256
`b381b6a052c309ea66716014820573040b6038ed83de0f19b112754d52233c3c`.
The native fan-in geometry, equal individual q masses, two different screen
ratios, finite lumping proof, positive-floor family and comparison (23) are
the new bounded contribution. No claim of historical originality, external
acceptance, formal verification, practical efficiency or method amplification
is made. The principal's independently proved full-Hastings upper, if
accepted, remains a separate theorem with separate proof obligations.

No numerical campaign, old-suite replay, external source-author contact,
paid computation, other-owner task or new spending occurred in this branch.
Model-inference, token, monetary and total discovery costs are unknown.
The adjacent receipt records observed times and source identities. Receipt
delivery is not principal scientific acceptance or integration.
