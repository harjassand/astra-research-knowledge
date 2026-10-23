# Branching transport closes the vanishing-screen mixing coefficient

Owner and principal construction: Astra PRO3. Scientific date: 2026-10-22,
Australia/Brisbane. Exact-real finite-space theorem. This source contains the
principal's proof; a separate contributor develops the lower construction and
an independent challenger checks its lift and the final proof. See `STATUS.md`
for source-bound acceptance, not an assumed status inferred from delivery.

## 1. Native family and the result

Fix K>0 and 0<alpha<1; write beta=1-alpha. An instance consists of a finite
labelled space, strictly positive probability vectors pi,q satisfying
D(pi||q)<=K, and a symmetric stochastic target-independent proposal Q.
The independence Metropolis-Hastings kernel G uses proposal q and target pi.
For x!=y let

\[
 L_\eta(x,y)=Q_{xy}\min\{1,(q_y/q_x)^\eta\}
 \min\{1,(\pi_y/\pi_x)(q_x/q_y)^\eta\},
 \qquad C_\eta=(I+\alpha G+\beta L_\eta)/2. \tag{1}
\]

The diagonal completes the actual stochastic kernel. Each run starts at q.
The screen eta in (0,1], Q, alpha, pi and q stay fixed during a run. Supports
and instances may vary in the class supremum. Neither empirical KL estimates
nor adaptive choices of Q or eta are admitted. The target normalizer is not
given to the sampler; the proof may describe normalized witness probabilities.

Define

\[
 R_\eta(n)=\sup_{\text{admitted instances}}
    \|qC_\eta^n-\pi\|_{\rm TV},\quad
 F(c)=c(1-c)^{(1-c)/c},\quad r_0=\alpha e^{-K}/\beta.
\]

Let c_*=1 if r_0>=1; otherwise c_* is the unique c in (0,1) with
F(c)=r_0. All logarithms are natural. TV is the supremum of event-probability
differences, equivalently half the finite l1 distance.

**Theorem 1 (sharp logarithmic risk exponent).** If the deterministic
across-run screens satisfy

\[
 \frac{\eta_n\log n}{\log\log n}\longrightarrow
 \lambda\in(0,\infty),
\]

then the exact minimax risk obeys

\[
 \boxed{\displaystyle
 \lim_{n\to\infty}\frac{-\log R_{\eta_n}(n)}{\log\log n}
       =\min\{1,\lambda c_*\}.} \tag{2}
\]

In particular, if lambda<1/c_*, then `(log n) R_{eta_n}(n)` diverges;
if lambda>1/c_*, the received upper and the ordinary tail lower give
`(log n) R_{eta_n}(n) -> K`. At lambda=1/c_* formula (2) determines only
the logarithmic power, not the coefficient of 1/log n or its existence.

**Theorem 2 (exact accuracy-policy coefficient).** Fix a deterministic policy
eta(epsilon) in (0,1], held fixed throughout the run at requested accuracy
epsilon, and suppose

\[
 \eta(\varepsilon)/[\varepsilon\log(1/\varepsilon)]
      \longrightarrow d\in(0,\infty).
\]

For each instance let its mixing time be the least integer t>=0 at which
TV is at most epsilon, and let T_policy(epsilon) be the supremum of these
times over the native class, with the policy's fixed eta(epsilon). Then

\[
 \boxed{\displaystyle
 \lim_{\varepsilon\downarrow0}\varepsilon\log T_{\rm policy}(\varepsilon)
       =\max\{K,1/(d c_*)\}.} \tag{3}
\]

For K=1, alpha=1/2, d=1 this is `1/c_* = 1.542211419737745...`, not the
previous interval `[1.0884827657...,1.5422114197...]`. The implicit equation,
not the printed decimal, defines the theorem constant. Pure IMH has coefficient
K; at these parameters the hybrid's worst-case coefficient is strictly worse.

## 2. Dependencies and what changes

The accepted incoming proof establishes, for every fixed c<c_*, a uniform
finite upper bound with proof exponent theta=c eta once eta is small enough:

\[
 R_\eta(n)\le A_R+\rho_h^{\lfloor n/2\rfloor}
 +S\{(A_R/R)^{c\eta}+[B_h/(n+1)]^{c\eta}\}
 +O(R^{1/2}n^{-1/2}+n^{-1/2}), \tag{4}
\]

where `A_R=min(1,K/(log R-1))`, and h,S,B_h and the constant in O depend only
on K,alpha,c. The full exact finite formula is in the accepted control proof,
Section 6; this display is used only for asymptotics. With R=n/(log n)^4,
the two transport bases have logarithms `-log n+O(loglog n)`. Its proof uses
actual killed dynamics up to the first safe hit and full dynamics after it.
The matching upper in (3), and the K lower independent of eta, are received
mathematical capital. `INCOMING_ACCEPTANCE.md` binds exact source digests.

The new step is a native symmetric tree that realizes nearly unit forward
local proposal mass at EVERY transient level. A single symmetric path allocates
only one half of its proposal mass forward, producing the earlier factor two.
At a vertex with D children, D equal edges can carry total D/(D+1) forward
mass; the unique parent edge carries only 1/(D+1). All individual edges are
still symmetric. Cardinalities are counted in both probabilities and acceptance
ratios. This construction proves a mixing lower bound from a reachable q-start
law; it is not an inference from a positive induced-norm gain.

## 3. A finite symmetric tree and its exact quotient

For the asymptotic family take fixed b in (0,1-exp(-K)), integer D>=2,
fixed v>0 and fixed M>2. Put L=log n, u=eta log n, and assume
`u -> infinity`, `u=O(log L)`. For large n set

\[
 m=\lfloor u/v\rfloor\ge1,\quad p=L^{-M},\quad
 z=\left(\frac{p}{b n L^2}\right)^{1/m},\quad
 s=(z/D)^\eta. \tag{5}
\]

The state space is the complete rooted D-ary tree of depth m, plus a state
star. Level i has exactly D^i vertices. At every vertex x of level i define

\[
 q_x= b z^i/D^i,\qquad
 \pi_x= p n^{-2(m-i)}/D^i. \tag{6}
\]

Give star the remaining q and pi masses. Thus level totals and common weights
are

\[
 q_i=bz^i,\quad \pi_i=pn^{-2(m-i)},\quad
 W_i=(p/b)n^{-2(m-i)}z^{-i},\quad
 W_m=nL^2,\quad W_{m-1}=L^2z/n. \tag{7}
\]

On each undirected tree edge set Q_xy=Q_yx=1/(D+1). Give the root diagonal
1/(D+1), each leaf diagonal D/(D+1), and star diagonal 1. Internal tree
diagonals are zero. This is exactly symmetric and stochastic. Its definition
uses only the public rooted tree and D, not target evaluations. Its support
may grow with n; it is fixed for every individual run.

The weights increase strictly with depth since W_(i+1)/W_i=n^2/z. Also z->0,
q_star->1-b and pi_star->1, so for all sufficiently large n,

\[
 0<W_0<\cdots<W_{m-1}<1<W_\star<W_m. \tag{8}
\]

Positivity follows from the geometric sums: sum_i q_i->b<1 and
sum_i pi_i<=p/(1-n^-2)->0. Forward KL has a particularly simple admission
bound. Every preterminal tree weight is below one, hence its KL contribution
is negative. Consequently

\[
 D(\pi\|q)\le p\log(nL^2)+\log(1/q_\star)
       \longrightarrow -\log(1-b)<K. \tag{9}
\]

This proves eventual strict admission without relying on rounded probabilities
or a minimum q. The bounds remain valid with m growing as O(log L).

**Exact local probabilities.** For a child y of x,
`q_y/q_x=z/D` and `pi_y/pi_x=n^2/D`. For sufficiently large n, the forward
two-factor acceptance is s, because its second factor is
`min(1,n^2/(D s))=1`. The reverse acceptance is **D s/n^2**, not s/n^2.
Multiplication by the parent-edge probability removes the apparent extra
factor D. Define

\[
 f=\frac{\beta D}{2(D+1)}s. \tag{10}
\]

The aggregate local contribution to C from each nonleaf level to the next
level is exactly f; from each nonroot level to the previous level it is
exactly f/n^2. This identity is also required by detailed balance of the
level totals. Omitting the D in the reverse acceptance would fail that check.

All global transitions between distinct levels j,k are exactly
`alpha q_k min(1,W_k/W_j)/2`; analogous formulas include star. Because all
vertices in a level have the same q,pi and neighbor counts, transition
probabilities into each level are independent of the current vertex label.
The partition into levels and star is therefore strongly lumpable. Same-level
global moves belong to the quotient diagonal; they are not deleted or treated
as failures. The lumped local proposal is not symmetric as a matrix on levels,
but it is the exact quotient of the admitted symmetric native Q. One must use
the per-vertex ratio z/D in (10), not replace it by the total-mass ratio z.

## 4. Actual competing exits, capture and retention

Let e_i be the probability that the actual chain leaves level i in one step,
for 0<=i<m. The event used below marks a forward LOCAL exit and treats every
other level exit as failure. It leaves all within-level behavior unchanged.

Set

\[
 a=\alpha(1-b)/2,\quad D_0=\alpha q_\star/2,
 \quad E=f+a+\frac{\alpha b}{2(n^2-1)}+\frac f{n^2}. \tag{11}
\]

Then `D_0 <= e_i <= E`. The lower bound is the accepted global proposal to
star. For the upper bound, global proposals to star or any higher level have
total q mass `1-sum_(j<=i) b z^j <=1-b`. A global proposal to a lower level
j<i contributes

\[
 q_j W_j/W_i = b z^i n^{-2(i-j)}.
\]

Their total is at most b/(n^2-1). The forward local exit is f and the backward
one is at most f/n^2. These terms include every type of level exit. In
particular, a direct global jump to the leaf set is conservatively counted
as failure, not improperly added to the lower bound.

Let H=floor(n/(2m)). Starting from any vertex of a transient level, the
probability that its next level exit is the marked forward local one and
occurs within H steps is exactly

\[
 \frac f{e_i}[1-(1-e_i)^H]
    \ge \frac fE[1-e^{-D_0 H}]. \tag{12}
\]

This uses the level chain's actual self-loop, including rejections and
same-level global proposals. It is valid after each conditional arrival by
the Markov property. Requiring m such successes reaches the leaves by time
mH<=n/2. No independence of the successive waiting times is assumed.

For the leaf UNION, not an individual leaf, its one-step escape probability
is exactly

\[
 e_m=\frac{\alpha(1-p)}{2nL^2}+\frac f{n^2}. \tag{13}
\]

All nonleaf weights are below W_m, so the global term sums their target
mass, and the local term is the parent-edge probability above. Moves between
leaves stay in the event. Retaining the leaf union for the rest of the run
has probability at least `(1-e_m)^n`. Starting from the root, whose q mass
is b, yields the exact finite lower certificate

\[
 R_\eta(n)\ge b(f/E)^m[1-e^{-D_0H}]^m(1-e_m)^n-p. \tag{14}
\]

For an elementary lower version, replace the two retention/time factors by
`[1-m exp(-D_0 H)]_+ [1-n e_m]_+`. These are multiplicative errors, so a
small capture probability is not destroyed by an unrelated absolute error.
This lower certificate concerns an actual subset of trajectories in the
unchanged chain. Other capture paths, returns and failed marked paths still
exist in the chain; omitting them only weakens a lower bound.

## 5. Asymptotic capture exponent with growing support

For fixed b,D,v,M under (5), `m=O(log L)` and

\[
 \log(1/z)=[L+(M+2)\log L+\log b]/m.
\]

Hence z->0 extremely rapidly. In particular D_0 tends to positive
alpha(1-b)/2, H is of order n/m, and the timing factor in (14) tends to one.
Also `n e_m=O(L^-2+n^-1)->0`. All corrections are relative.

Let v_n=-log s. Multiplying its error by m is useful:

\[
 m v_n=u+\eta[(M+2)\log L+\log b]+m\eta\log D=u+o(1). \tag{15}
\]

Here `eta=u/L=O(log L/L)` and m=O(log L). Thus v_n=u/m+o(1/m) tends to v,
and f tends to the positive constant `beta D exp(-v)/(2(D+1))`.
The extra terms in E in (11) are O(n^-2). Define

\[
 r_{b,D}=\frac{\alpha(1-b)(D+1)}{\beta D},\quad
 \phi_r(v)=\frac{\log(1+r e^v)}v. \tag{16}
\]

It follows, including integer rounding of m, that

\[
 \log[(f/E)^m]
 =-m\log(1+r_{b,D}e^{u/m})+o(1)
 =-\phi_{r_{b,D}}(v)u+O(1). \tag{17}
\]

For example, the last O(1) follows by differentiating
`x log(1+r exp(u/x))` for x between u/v-1 and u/v; its derivative is bounded
uniformly as u grows with v fixed. Combining (14)-(17), for fixed parameters,

\[
 R_\eta(n)\ge b\exp[-\phi_{r_{b,D}}(v)u+O(1)](1-o(1))-L^{-M}. \tag{18}
\]

The total native number of states is `1+sum_(i=0)^m D^i`, so its logarithm
is O(m log D)=O(loglog n) for fixed D,v and bounded u/loglog n. The support
is large but finite and grows only as a fixed power of log n in this regime.
No hidden support bound is assumed by the class. All parameters b,D,v,M are
chosen before taking n to infinity; a diagonal limit with uncontrolled D is
unnecessary.

## 6. The variational identity and parameter order

For r>0 let chi(r)=inf_(v>0) phi_r(v). If r>=1, then phi_r(v)>1 and tends
to 1 as v grows, so chi(r)=1. If 0<r<1, put `t=r exp(v)/(1+r exp(v))`.
The stationary condition for phi is

\[
 v t=\log(1+r e^v)=-\log(1-t).
\]

It gives `v=-log(1-t)/t` and
`r=t(1-t)^((1-t)/t)=F(t)`. Since
`d log F(t)/dt=-log(1-t)/t^2>0`, there is exactly one solution t in (0,1).
The derivative numerator of phi increases strictly with v; it is negative
at v=0 and tends to -log r>0 as v grows. This solution is therefore the
unique minimum, with value phi(v)=t. The capped inverse chi is continuous
and increasing, including at r=1.

As b increases to 1-exp(-K) and fixed integers D increase without bound,
`r_(b,D)` decreases to r_0=alpha exp(-K)/beta from above. Thus

\[
 \inf_{0<b<1-e^{-K},\ D\ge2,\ v>0}\phi_{r_{b,D}}(v)=c_*. \tag{19}
\]

This statement is used only by strict approximation: for every zeta>c_*
one first chooses finite fixed b,D,v with phi<zeta, then takes n to infinity.
It neither saturates the KL budget with a singular distribution nor sends
D to infinity during a trajectory. When r_0>=1, (19) uses large fixed v;
no finite minimizing v is claimed. This order is essential to uniform
admission and timing estimates.

## 7. Proof of Theorem 1

Write L=log n and suppose u/log L->lambda in (0,infinity). For each fixed
c<c_* the received finite inequality (4), at R=n/L^4, gives

\[
 R_{\eta_n}(n)\le O(L^{-1})+O(\exp[-c u+o(1)])+O(L^{-2}). \tag{20}
\]

The constants depend on c but not n. Consequently the liminf of
`-log R/log L` is at least `min(1,c lambda)`; increase c to c_*.

For completeness the ordinary two-state lower independent of eta can be
seen directly. Choose any k<K, terminal target mass p_0=k/L and proposal
mass q_0=p_0/(n L^2), and take Q=I. Its KL tends to k<K. The nontrivial
eigenvalue of C is `1-alpha/(2n L^2)` and its exact deficit at time n is
`(p_0-q_0)(1-alpha/(2n L^2))^n~k/L`. Thus `liminf L R>=K` by increasing k
to K, and the limsup logarithmic risk exponent is at most one.

If lambda c_*<1, choose any zeta in (c_*,1/lambda). By (19), choose fixed
b,D,v with `phi_(r_bD)(v)<zeta` and choose M>2. Equation (18) gives
`R >= L^(-lambda phi+o(1))`, since the subtracted L^-M is negligible.
Its limsup exponent is at most lambda phi<lambda zeta. Decrease zeta to c_*.
If lambda c_*>=1, the ordinary lower already supplies the matching upper
bound of one on the exponent. This proves (2), including equality.

For lambda<1/c_*, the same strict choice makes `L R` diverge. For
lambda>1/c_*, the received finite bound makes both transport terms o(1/L)
and gives limsup L R<=K, matching the lower. This latter conclusion requires
a strict multiplier margin; (2) alone would not prove the prefactor K.

## 8. Proof of Theorem 2 without a diagonal monotonicity assumption

The received upper gives the limsup in (3). To reconstruct its quantifiers:
for A>max(K,1/(d c_*)), choose fixed c<c_* with c A d>1 and the associated
fixed proof constants. At n=ceil(exp(A/epsilon)), eta is fixed for that run,
the entropy term is `(K/A+o(1)) epsilon`, transport is
`epsilon^(c A d+o(1))=o(epsilon)` and the other terms are o(epsilon).
The strict K/A<1 margin proves uniform accuracy.

For the new lower, fix any A in (0,1/(d c_*)). Select finite fixed b,D,v
using (19) so `A d phi_(r_bD)(v)<1`. Set n=floor(exp(A/epsilon)) and use
the native tree above with the policy's eta(epsilon). Then

\[
 u=\eta(\varepsilon)\log n
   =(Ad+o(1))\log(1/\varepsilon),\quad
 \log\log n=\log(1/\varepsilon)+O(1).
\]

All tree assumptions therefore apply. Its actual leaf error from (18) is
at least `epsilon^(A d phi+o(1))`, up to a positive fixed factor, after
subtracting `p=O(epsilon^M)`. Choose M>2. Since A d phi<1, its error divided
by epsilon diverges. This supplies an admitted instance with TV>epsilon
at n for each sufficiently small epsilon. Fixed-kernel TV decreases with
time in this instance, so its mixing time exceeds n. Let A increase to
1/(d c_*). Together with the eta-independent K lower, this proves the
liminf `max(K,1/(d c_*))`, establishing both existence and equality.

No monotonicity of the sequence R_(eta_n)(n) is used. All monotonicity used
here holds within one fixed chain for each requested epsilon.

## 9. Scientific meaning, costs and remaining boundary

The factor-two gap came from the predecessor's one-dimensional path, not
from a proved benefit of a broader transport norm. A symmetric branching
geometry makes forward proposal mass approach one while the per-edge symmetry
remains exact. The incoming norm ceiling c_* is therefore attainable as a
true minimax risk exponent by reachable chains. The incoming three-state
norm witness still is not itself a mixing lower; this new tree is the missing
capture-and-retention construction.

The new theorem is about exact-real worst-case iteration count. It is not a
finite-time ordering result, a practical speedup, a deterministic-schedule
theorem, a nonreversible-kernel theorem, or a guarantee from observed training
loss. The local algorithm is the existing two-stage delayed-acceptance
operation. Its proposal/target-query/cache/precision accounting remains in
`EXPERIMENT_CONTRACT.md`. Giving a verifier the explicit target table is not
a change to the sampler's oracle contract; a user who possesses that whole
table may use direct sampling instead.

The finite risk prefactor at the critical window
`eta log n = (loglog n)/c_* + O(1)` is not determined here. Parameters b,D,v
approach the entropy/branching optimum only by strict approximation in this
proof. Obtaining a second-order equivalent requires retaining those parameter
costs and the full hitting distribution. This is the next owned question;
the exact first-order policy coefficient and log-risk exponent are now closed.

The independently checked finite quotient is an executable identity/admission
check, not a numerical proof of (2) or (3). Historical originality and external
mathematical acceptance remain unestablished. All prior sources, failures and
closed programmes remain preserved unchanged.
