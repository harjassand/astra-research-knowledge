# Independent source-bound challenge of the Cycle8 convergence criterion

Reviewer: `/root/cycle8_criterion_challenge`.
Scientific date: 22 October 2026. Scope: the new asymmetry-budget criterion,
with the accepted Cycle7 finite interface held fixed.

## 1. Verdict and exact source identity

**PASS: I find no unresolved load-bearing mathematical defect in Theorems 1
and 2 or Corollary 3 at the principal source hash below. No mathematical
repair is required by this review.** The necessity proof covers the full
moving-policy quantifiers, including vanishing `eta`, arbitrarily large
finite `kappa` and `A`, either sign of mismatch, and `A` tending to zero
while positive mismatch grows. The sufficient bound is uniform over the
native finite class and the public policy.

This is an independent internal proof challenge, not a claim of historical
novelty, external mathematical acceptance, formal verification, or practical
sampling advantage.

The following files were read completely, except that the predecessor was
used specifically through its accepted Sections 2–4 and the class definition
needed to identify that interface:

| Source | SHA256 |
|---|---|
| `cycle8_pro3/research/ASYMMETRY_BUDGET_THEOREM.md` | `eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1` |
| `cycle8_pro3/research/contributors/ASYMMETRY_ENERGY.md` | `0343c506f365bc8a5d16e6a2d86d6cdd3386faf5ff14132f8ca75ae89182b630` |
| `cycle8_pro3/research/contributors/ASYMMETRY_LOWER.md` | `31a6a06c7f2099205062512121ee3f385baca376742da6a4680b673f598c9ea0` |
| `cycle7_pro3/research/RECIPROCAL_PROPOSAL_THEOREM.md` | `584c2fcbedcead37578b91596ace85eeb75426537d564cdd646d44831f4dbc6a` |

The verdict attaches to these exact bytes. A change to a load-bearing formula
requires checking that change; this report does not silently cover a later
principal version. I did not mutate any principal or contributor source.

## 2. The proposition actually established

For fixed `K>0` and `0<alpha<1`, let `beta=1-alpha`. The native instance
has a finite labelled space, strictly positive probability vectors `pi,q`,
one budget `D(pi||q)<=K`, initialization `q`, and a fixed target-independent
row-stochastic proposal `Q` with reciprocal off-diagonal support. Its actual
edge ratios obey `A(Q)<=A_n`. The run uses the displayed two-stage acceptance,
the actual rejection diagonal, and the lazy random mixture
`C=(I+alpha G+beta L)/2`.

Writing

\[
u_n=\eta_n\log n,\qquad D_n=|\kappa_n-\eta_n|A_n,
\qquad v_n=\frac{u_n}{1+D_n},
\]

the proof establishes convergence of the supremum of the actual full-chain
TV error if and only if `v_n -> infinity`. This is equivalent to the two
conditions `u_n -> infinity` and `D_n=o(u_n)`.

The proof also establishes the stated coarse finite upper bound with constants
depending only on `K,alpha`, and amplitude `K` under the stronger sufficient
condition `v_n/log log n -> infinity`. It does **not** establish the exact
transport exponent, the exact positive floor, a necessary amplitude-`K`
condition, or a sharp critical law inside the convergent region. The source
keeps these distinctions explicit.

## 3. Changed local energy and the unchanged finite interface

The new screen satisfies

\[
S_{xy}=r_{xy}^{\eta}e^{\xi_{xy}},\qquad
|\xi_{xy}|\le D=|\kappa-\eta|A.
\]

Reciprocity gives `S_yx=1/S_xy` and `t_yx=1/t_xy`, so the two acceptance
factors give `a_xy/a_yx=t_xy`. Thus the changed `L` remains `pi`-reversible,
and the original lazy mixture has the same positive-spectrum and IMH
Dirichlet properties required by the accepted full-return interface.

For `a>0`, `a<=exp(D)r^eta` directly yields

\[
w a^p r^{-\theta p}-a
\le w e^{D\theta p/\eta}a^{p(1-\theta/\eta)}-a
\le H_w(D).
\]

The case `a=0` is separate and harmless because `H_w(D)>=0`. This is valid
for every positive `r`; it does not presume the screen is below one. With
`0<theta<=eta<1`, one has `0<=tau=p(1-theta/eta)<1`. The stated interior
maximum, boundary maximum, and `tau=0` supremum are all correct. In particular
the endpoint does not require assigning a value to `0^0`.

The proof then uses the **outgoing row at the output vertex** through
`B_xy=Q_yx`, rather than imposing an unadvertised counting-column bound.
The powered off-diagonal coefficient is exactly

\[
T_{xy}^p/B_{xy}^{p-1}
=Q_{xy}a_{xy}^p r_{xy}^{-\theta p}.
\]

The diagonal coefficient remains the actual `L_xx`. Subtracting every
accepted outgoing flow before dropping killed exits is the step that justifies
the coefficient `1+H_w(D)`. There is no fictitious renormalization of a killed
row and no use of only an off-diagonal scalar estimate as a matrix norm.

The resulting absorbed energy bound has precisely the form needed by the
accepted Cycle7 Sections 2–4. Combining it with the distinct global
`q`-density Jensen calculation produces the displayed
`Gamma(e)`. The initial transformed energy is exactly `b`, and the
`Gamma(e)^(N(1-theta))` multiplier accumulates all first-hit times in the
absorbed vector.

The changed use of the accepted full-return certificate is legitimate:
reversibility, positive spectrum, the actual global killed mass, initialization,
and the single KL premise are retained. Every first hit is subsequently
propagated by the original `C^(n-j)`. No pathwise return is removed from the
upper bound. The same-instance binary KL estimates may be used simultaneously
for this coarse upper; they are not being added as incompatible separate
entropy allocations to claim a sharp critical amplitude.

## 4. Uniformity when eta is arbitrarily small

This is a load-bearing part of the review. The chosen parameters satisfy

\[
\theta=\frac{\eta\varepsilon_0}{2(1+D)},\qquad
\theta\le\eta/8<1/2,\qquad p\le2.
\]

Consequently both
`lambda=D theta p/eta` and
`c_eff=theta p(1-eta)/eta` are at most `epsilon_0`, independently of
`eta,kappa,A`. The bound

\[
H_1(D)\le e^{\varepsilon_0}-1+\varepsilon_0
\le3\varepsilon_0\le3r_0/8
\]

is valid. The binary KL bound with `h=(log n)^-2` gives
`1-b>=exp(-K)/2` at a threshold depending only on `K`. Therefore
`beta H_1(D)-alpha(1-b)` is uniformly strictly negative eventually. Its
positive part is exactly zero; there is no hidden accumulated error from
this term.

The remaining deterministic estimates have uniform constants:

\[
N=O_{K,\alpha}(\log\log n),\qquad
\bar e\le E_n=C_1(\log n)^6\log\log n/n,
\]

and the smoothing, test, and survival contributions are
`O_{K,alpha}((log n)^-2)`. The displayed explicit bound on `E_n` follows
from `N<=n/2`; no minimum-atom or support assumption is used.

With the positive part removed,

\[
\Gamma(\bar e)^{N/p}
\le\exp\{N\theta\log2+\alpha N\bar e\}.
\]

Indeed `Gamma(e)<=2^(p-1)(1+alpha e)` and `(p-1)/p=theta`.
The exponent of the full first-hit term is therefore at most

\[
-\theta\log n+\theta O_{K,\alpha}(\log\log n)
+\alpha N E_n.
\]

Choose a policy-independent threshold at which the `O(log log n)` expression
is at most `(log n)/2`, and `alpha N E_n<=log 2`. This gives
`2 exp(-theta log n/2)` for **every** positive `theta`, however small.
It does not divide the final error by `theta`, and therefore does not require
a lower bound on `eta`. The proof correctly avoids the false assertion that
the accumulated multiplier itself tends to one when `eta` is fixed.

These observations prove the finite upper and sufficiency with the stated
uniform quantifiers. They also justify the stronger sufficient amplitude
regime. The two-state `Q=I` example has exactly the displayed nontrivial
eigenvalue and a single eventually admissible KL allocation, so its matching
`K` lower is valid for all policies.

## 5. Native lower geometry, multiplicities, and the second screen

On the adverse subsequence, `A>0`, `delta!=0`, and
`M=ceil(exp(A))>=2`, with `1<=M/exp(A)<2`. The underlying labelled tree
has finitely many actual vertices at each horizon, even when that number is
arbitrarily large.

For expansion, each parent has `M` forward probabilities `1/(2M)` and each
child has reverse probability `R_A/(2M)`. For coalescence these directions
are interpreted in the opposite progress order. At an internal native vertex
the outgoing proposal total is

\[
1/2+R_A/(2M)\le1,
\]

so the remaining proposal diagonal is nonnegative. Endpoint rows use their
actual one-direction totals. Every positive edge has absolute log proposal
ratio exactly `A`; the core state is isolated for `Q`. Thus both row budgets
and the public asymmetry promise hold natively. `Q` is specified from public
quantities and labels before the target masses.

Uniform splitting over each level gives per-vertex `q` ratios
`z/M=R_A^(-kappa/eta)` in expansion and
`z M=R_A^(kappa/eta)` in coalescence. These, rather than the level-total
ratio alone, give the exact forward screen `S=1`. The target Hastings ratios
are `n^2 R_A/M` and `n^2 M/R_A`; both exceed one for `n>=2`.
Forward acceptance is one, reverse acceptance is the reciprocal target
Hastings ratio, and summing the actual native reverse proposals gives

\[
L(i,i+1)=f,\qquad L(i,i-1)=f/n^2.
\]

In particular the internal local diagonal is `1-f-f/n^2`, including all
self-proposals and rejections. Tree automorphisms preserve the entire
instance and are transitive within each progress level. The level partition
is strongly lumpable, and uniform-within-level initial and target measures
make native and quotient TV equal. The proof uses the resulting aggregate
probabilities without claiming free access to a quotient sampler.

## 6. One KL allocation for unbounded V and actual retention

The relation `V=-log z>=a_0 log n-log 2` gives `V->infinity`, without
requiring an upper bound on `V`. The choice

\[
p=\frac{1}{(\log n)^2(1+V)}
\]

is sufficient for the entire instance to obey the one KL budget. Native
multiplicities cancel because `pi,q` have the same uniform split within
each level, and every level satisfies
`log W_i<=log(1/b)+J V`. Therefore

\[
D(\pi\Vert q)
\le\log(1/q_\star)+
\frac{\log(1/b)+J}{(\log n)^2(1-n^{-2})}
\longrightarrow-\log(1-b)<K.
\]

This estimate remains valid if `V` grows faster than every prescribed
function of `n`. In particular no hidden assumption that transient
importance weights lie below the core weight is present.

For fixed integer `J` with `J a_0>1`, the monotonicity of
`(1+v) exp(-Jv)` on `v>=0` proves

\[
n/W_J=O_{a_0,J,b}(n^{1-Ja_0}(\log n)^3)\longrightarrow0.
\]

The terminal weight is eventually maximal over the tree and the core.
Consequently the exact escape probability from the **whole terminal union**
is `alpha(1-p)/(2W_J)+beta f/(2n^2)`, with `n d_T->0`.
Global transitions between different terminal vertices remain inside that
union and are correctly retained. Since the escape probability is the same
from every terminal vertex, retention for at most `n` remaining steps is
at least `(1-d_T)^n` in the original chain.

## 7. Deterministic windows, capture, and moving-policy exhaustion

Marking all global attempts as failures before capture is a valid conservative
event in the mixture's genuine trajectory space. It does not assert that a
rejected global proposal actually left the current level. It avoids any
need to order transient weights relative to the core. The local backward
failure and all unmarked holds are also accounted for using the actual
local diagonal.

At progress level `i`, the marked hazard is exactly
`e_i=c+g+1_{i>0}c/n^2`, with success probability `c=beta f/2`.
The geometric calculation over `H=floor(n/(2J))` actual transitions is
`c[1-(1-e_i)^H]/e_i`. The stated lower bound follows from
`c+g<=e_i<=E_0`. Applying the Markov property at each successful arrival
multiplies `J` such lower bounds and reaches the terminal union by `JH<=n/2`.
The remaining original-chain retention then gives the displayed finite lower.
Independent waiting times and a replacement of random attempts by their
expectation are not needed.

The timing and retention factors tend to one because `J` is fixed. In the
positive sign, `f=1/2`. In the negative sign, `kappa>=0` gives
`D/eta<=A`, so the adverse condition forces `A>=a_0 log n`; hence
`R_A/ceil(R_A)->1` and again `f->1/2`. This also covers alternating signs.
The resulting positive subsequential floor is valid, with no claim of
optimality.

The separate symmetric three-state witness correctly covers every bounded
`u_n` subsequence. Its forward screen has liminf at least `exp(-U)`, its
terminal importance ratio is `n(log n)^2`, and its actual terminal escape
probability is `o(1/n)`. Its first-step-crossing event is conservative and
uses one eventually admissible KL calculation.

Finally, if `v_n` fails to diverge, choose an infinite subsequence with
`v_n<=B`. Either `u_n` has a bounded further subsequence, covered by the
three-state witness, or `u_n->infinity` along the selected subsequence.
In the latter case `D_n>=u_n/(2B)` eventually, giving the multilevel adverse
condition with a fixed `a_0=1/(2B)`. These cases exhaust the policy sequences;
no assumption of bounded mismatch or fixed mismatch sign is introduced.

## 8. Ordinary comparator and finite arithmetic spot checks

The same-instance pure-IMH comparison is valid. The root union has the
smallest importance ratio, so all proposals out of it are accepted. Starting
there, the probability of another tree level before the core is
`s_q/(1-b)`. Initial mass on other levels contributes `s_q`, while initial
root mass contributes at most `b s_q/(1-b)`; their sum is exactly
`s_q/(1-b)`. Thus the displayed bound has not accidentally omitted the
initial off-root mass. Root survival contributes `b^(j+1)` from the `q`
start. After a first core hit, TV contraction of the original `G` bounds
all remaining error by `pi_tree`, including returns. This proves convergence
for every deterministic `j->infinity` in the stated instances.

As a narrow algebraic spot check, I independently evaluated exact rational
native edge identities with `R_A=3/2`, `M=2`, `n=16`, `eta=1/2`, using
`kappa=5` for expansion and `kappa=0` for coalescence. This was not a numerical
mixing suite and was not used as a substitute for any asymptotic argument.

| Exact quantity | Expansion | Coalescence |
|---|---:|---:|
| Positive forward screen squared | `1` | `1` |
| Forward target Hastings ratio | `192` | `1024/3` |
| Aggregate forward `L` probability | `1/2` | `3/8` |
| Aggregate reverse `L` probability | `1/512` | `3/2048` |
| Actual internal `L` diagonal | `255/512` | `1277/2048` |

The exact proposal internal diagonal was `1/8` in both orientations. These
checks confirm selected native identities only. The principal's separate
finite validation programme, its implementation, and any resulting evidence
files are outside this report's numerical-validation claim.

## 9. Defects, repair demands, and limits

**Unresolved substantive defects:** none found.

**Required repairs:** none for the reviewed theorem and proof at the named
hashes. This verdict depends on retaining the actual rejection diagonals,
the accumulated first-hit multiplier, the `1/(1+V)` entropy scaling or an
equally effective replacement, the native multiplicities, and the conservative
capture event. Omitting one of these would require a fresh argument.

The review holds the accepted Cycle7 finite interface fixed and checks the
changed use of it. It does not reopen the earlier critical-law programme,
consult outside owner programmes or external source routes, or issue a
historical-priority verdict. It is a mathematical review of a finite exact-real
minimax statement. It does not certify finite-precision implementation,
computability for arbitrary real input policies, constant-cost index or target
access, wall-time superiority, target-call superiority, or any resource
advantage over the ordinary comparators. The very large native supports and
arithmetic magnitudes in the lower are explicitly admitted by the theorem's
class and explicitly charged in its discussion.

The sharp convergence criterion survives this source-bound challenge. Its
remaining mathematical frontier is the rate and critical amplitude within
the convergent region, which the principal correctly leaves open.
