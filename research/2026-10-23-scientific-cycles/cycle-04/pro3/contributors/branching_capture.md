# Branching capture closes the vanishing-screen coefficient gap

Contributor: `/root/branching_capture`, 2026-10-21 UTC (scientific date
2026-10-22 Australia/Brisbane). This is a new constructive lower argument,
not an inference from the incoming one-step norm witness. Principal acceptance
and independent challenge are recorded separately by the owner.

## 1. Contract and result

Fix K>0, 0<alpha<1, beta=1-alpha. Each instance has a finite labelled state
space, positive pi,q with D(pi||q)<=K, and a symmetric stochastic Q defined
without using evaluated target values. G is proposal-q independence MH,

    L_eta(x,y) = Q_xy min(1,(q_y/q_x)^eta)
                    min(1,(pi_y/pi_x)(q_x/q_y)^eta), x!=y,
    C_eta = (I+alpha G+beta L_eta)/2,

with true rejection diagonals and initial law q. Eta,Q stay fixed during the
entire trajectory; they may vary across admitted instances and requested
accuracies. Define R_eta(n) as the supremum of proposal-start TV error over
this class. All logarithms are natural. Put

    F(c)=c(1-c)^((1-c)/c), 0<c<1,
    r_* = alpha exp(-K)/beta,
    c_*=1 if r_*>=1,
    F(c_*)=r_* with 0<c_*<1 otherwise.

The incoming killed-operator upper is treated as a separately proved dependency:
for every strict c<c_* one has a support-uniform finite first-hit certificate
with transport exponent c eta for small eta, and therefore

    liminf eta_n log n/loglog n > 1/c_*
        implies (log n)R_{eta_n}(n) -> K.

For eta(epsilon)/[epsilon log(1/epsilon)] -> d in (0,infinity), it gives
limsup epsilon log T_policy(epsilon) <= max(K,1/(d c_*)).

The new tree family proves the matching lower. Specifically, if

    eta_n log n/loglog n -> lambda in (0,1/c_*),

then (log n) R_{eta_n}(n) -> infinity. Consequently the exact accuracy-policy
coefficient exists and equals

    lim epsilon log T_policy(epsilon) = max(K,1/(d c_*)).

The old eta-independent Q=I lower supplies the K part. Combining the same
construction with the finite incoming upper also gives the more detailed
logarithmic power law, for any lambda in (0,infinity):

    -log R_{eta_n}(n) / loglog n -> min(1, lambda c_*).

The coefficient of R itself at the critical horizon lambda=1/c_* is not
identified by this power-law assertion. No finite-time TV improvement,
practical speedup, historical novelty, or result for different information,
nonreversibility, adaptation or schedules is claimed.

## 2. Tree, public proposal, and exact probability vectors

Choose fixed b in (0,1-exp(-K)), an integer D>=2, and v>0. Let

    L=log n, u=eta_n L,
    m=max(1,floor(u/v)), p=L^(-M),
    z=(p/(b n L^2))^(1/m),

where M>2 is a fixed constant chosen below. We assume u tends to infinity
and u=O(log L), as applies to the claimed finite-lambda regimes.

The labels are a separate state star and all words over {1,...,D} of lengths
0,...,m. The empty word is the root. There are D^i vertices in level i.
For every vertex x in level i set

    q_x = b z^i / D^i,
    pi_x = p n^(-2(m-i)) / D^i.

The remaining masses are assigned to star:

    q_star = 1 - sum_{i=0}^m b z^i,
    pi_star = 1 - sum_{i=0}^m p n^(-2(m-i)).

Thus the total masses of a level, denoted Q_i and P_i below, are exactly

    Q_i=bz^i,  P_i=p n^(-2(m-i)).

These capital letters denote level masses, not transition proposals. The
proposal matrix Q assigns 1/(D+1) to every tree edge in both directions.
Its root diagonal is 1/(D+1), internal diagonals are zero, leaf diagonals
are D/(D+1), and Q(star,star)=1. It is symmetric and stochastic. Its definition
uses only the public labelled tree, not the target values. The support has

    1 + (D^(m+1)-1)/(D-1)

states, finite in every instance. D remains fixed throughout each limiting
construction. Its size is polynomial in log n because m=O(loglog n), although
there is no fixed dimension bound across the class.

Since

    log z = -[L+(M+2)log L+log b]/m,

z tends to zero faster than any fixed negative power of L. Hence q_star tends
to 1-b, pi_star tends to 1, and all entries are strictly positive eventually.
The per-vertex weights are constant on levels and equal

    W_i=P_i/Q_i = W_m (z/n^2)^(m-i),
    W_m=n L^2.

In particular W_{m-1}=L^2 z/n ->0, so eventually

    W_0 < ... < W_{m-1} < W_star < W_m.

These inequalities fix every global acceptance branch used below.

## 3. Forward-KL admission uniformly in the growing tree

The cardinalities cancel from the likelihood ratios. The exact KL is

    sum_{i=0}^m P_i log W_i + pi_star log(pi_star/q_star).

The leaf contribution p log(n L^2) tends to zero. For j=m-i>=1,

    P_i = p n^(-2j),
    log W_i = log(n L^2)+j(log z-2L).

Here |log z|=O(L), with constants independent of m along the construction.
Thus

    sum_{i<m} P_i |log W_i|
      <= p sum_{j>=1} n^(-2j) [O(L)+j O(L)]
      = O(p L/n^2) ->0.

The star contribution tends to -log(1-b)<K. Therefore D(pi||q)<K for every
sufficiently large n, with strict asymptotic slack. The argument controls the
entire support as it grows and does not use a positive lower bound on entries.
All examples are finite positive laws, not singular limits used as instances.

## 4. Actual local branches: the cardinality factor matters

Write

    s=(z/D)^eta_n,
    f= beta D s/[2(D+1)].

For a parent x and child y, q_y/q_x=z/D and pi_y/pi_x=n^2/D.
Consequently the forward second-stage ratio is n^2/(D s), which exceeds one
for all sufficiently large n. The forward local acceptance is s.
The reverse local acceptance is **D n^(-2) s**, not n^(-2)s: the ratio of
per-vertex target masses contains the factor D. Since the single parent edge
has proposal probability 1/(D+1), the actual mixture probabilities are

    total marked local forward probability from a transient vertex = f,
    marked local reverse probability from a nonroot vertex = f/n^2.

There are D children, which explains the aggregate forward factor D/(D+1).
The exact detailed-balance equality on an edge is

    pi_x Q_xy s = pi_y Q_yx (D n^(-2) s).

The resulting local chain is the prescribed one; no outward directed proposal
has replaced the symmetric Q. Root and leaf self loops retain the full
rejection mass.

## 5. A finite event lower bound with all competing exits charged

For a transient vertex x in level i<m let e_i=1-C(x,x). Symmetry of the
construction makes this independent of the chosen vertex within that level.
Define

    S_q=bz/(1-z),
    a=alpha(1-b)/2,
    D_0=alpha(1-b-S_q)/2,
    delta_n=alpha/2 [ S_q + b n^(-2)/(1-n^(-2)) ] + f/n^2,
    E=f+a+delta_n.

For sufficiently large n, D_0>0 and

    D_0 <= e_i <= E,  0<=i<m.                              (A)

For the lower bound, the global move to star accepts and has probability
alpha q_star/2 >=D_0. For the upper bound, its probability is at most a.
All global moves to the same or higher level other than the current vertex
have total proposal mass at most S_q (at the root, the same-level set is
empty). This includes global moves to siblings and cousins, which do exist
and cannot silently be discarded from the exit probability. Global moves to
lower levels have exactly

    sum_{j<i} P_j/W_i = Q_i sum_{r=1}^i n^(-2r)
                     <= b n^(-2)/(1-n^(-2))

acceptance mass before the factor alpha/2. The forward local contribution
is f, and the reverse local contribution is at most f/n^2. Adding these
proves (A). Any other global path is a competing exit, not a successful mark.

At each visited transient vertex require that its next nonself exit is a
marked local move to one of its D children, and that this exit occurs within
h integer steps. This is an event of the actual mixture with its usual random
coins, not a renormalized transition rule. For h>=1, its conditional probability
is exactly

    sum_{j=1}^h (1-e_i)^(j-1) f
      = (f/e_i)[1-(1-e_i)^h]
      >= (f/E)(1-exp(-D_0 h)).                          (B)

Set h=floor(n/(2m)); this is at least one eventually. Iterating (B) along the
chosen random child path gives arrival in the leaf set by time mh<=n/2 with
probability at least

    b (f/E)^m (1-exp(-D_0 h))^m
      >= b (f/E)^m [1-m exp(-D_0 h)]_+.

The event starts from the actual root mass q_root=b. The child is not fixed
in advance: all D successful child moves are included at each stage. Bounding
only one designated ray would lose the essential branching factor.

Let H be the entire leaf set, whose target mass is pi(H)=p. From every leaf,
the global probability to leave H is (1-p)/W_m. Global moves to another leaf
stay in H and are retained. Its only local exit is to its parent. Therefore
the exact per-step escape probability from H is constant across its vertices:

    e_H = alpha(1-p)/(2 n L^2) + f/n^2.                (C)

Starting at any leaf, the probability to remain in H for k steps is exactly
(1-e_H)^k; this follows from the constant killed row sums on H. In particular
retention until time n after arrival costs at most the multiplicative factor

    (1-e_H)^n >= 1-alpha/(2L^2)-beta/(2n).

Combining the actual capture and retention event gives the fully explicit
finite lower certificate

    R_eta_n(n) >=
      b (f/E)^m [1-m exp(-D_0 floor(n/(2m)))]_+
        [1-alpha/(2L^2)-beta/(2n)]_+ - p.             (D)

No return has been deleted from the chain. The selected event excludes some
returns before capture and requires retention afterwards; all excluded paths
are simply omitted from a lower bound. The timing correction is relative to
the small capture event. It is not an absolute error subtraction that could
swamp its probability. All relevant quantities in (D) are finite and explicit.

## 6. Capture exponent and how branching removes the old factor two

Put

    a_{b,D}=alpha(1-b)(D+1)/(beta D),
    phi_a(v)=log(1+a exp(v))/v.

The screening logarithm is exactly

    log s = -u/m
      -eta_n[(M+2)log L+log b]/m -eta_n log D.

Because D is fixed and u=O(log L), multiplying the last two error terms by m
gives O((log L)^2/L)=o(1). Also m delta_n ->0, s->exp(-v)>0, and
m=u/v+O(1). Thus the finite capture factor obeys

    log[b(f/E)^m]
      = -m log(1+a_{b,D} exp(u/m))+log b+o(1)
      = -phi_{a_{b,D}}(v) u + O(1).                 (E)

Both relative timing and retention factors in (D) tend to one. If
u/log L ->lambda in (0,infinity), choose the fixed M larger than
lambda phi_{a_{b,D}}(v)+2. Then p is negligible relative to capture and

    R_eta_n(n) >= L^(-lambda phi_{a_{b,D}}(v)+o(1)).  (F)

For a>0, elementary differentiation gives

    inf_{v>0} phi_a(v) = 1,                         a>=1;
    inf_{v>0} phi_a(v) = c with F(c)=a, 0<c<1,      0<a<1.

For completeness, the derivative sign is that of

    g(v)=v a exp(v)/(1+a exp(v))-log(1+a exp(v)),
    g'(v)=v a exp(v)/(1+a exp(v))^2 >0.

When a<1, g(0+)=-log(1+a)<0 and g(infinity)=-log a>0, so the minimizer is
unique. With c=a exp(v)/(1+a exp(v)), its equation is cv=-log(1-c), yielding
F(c)=a and phi_a(v)=c. When a>=1, phi_a(v)>1 for finite v and tends to one.
The inverse of F is continuous since d log F(c)/dc=-log(1-c)/c^2>0.

Now let b approach 1-exp(-K) from below and let the fixed integer D increase.
Then

    a_{b,D} -> alpha exp(-K)/beta = r_*,
    inf_{b,D,v} phi_{a_{b,D}}(v) = c_*.

The choices are made in the correct order: for any strict desired exponent
margin, select a finite D, then a fixed b with KL slack and a finite v. Hold
all three fixed while n tends to infinity. No claim uniform in D is needed.
Thus every lambda<1/c_* admits fixed b,D,v with
lambda phi_{a_{b,D}}(v)<1, and (F) proves (log n)R->infinity.

The old line graph forced forward proposal mass 1/2. The rooted tree has
forward mass D/(D+1), approaching one while every edge remains symmetric.
The extra first-screen price D^(-eta) is negligible in (E). Branching makes
sustained adverse transport reachable from the actual q-root mass, whereas
the incoming induced-norm witness alone had no such mixing implication.

## 7. Policy coefficient and logarithmic risk exponent

Let eta(epsilon)/[epsilon log(1/epsilon)] ->d in (0,infinity), with eta held
fixed within each requested-accuracy run. Fix A>0 and put
n_epsilon=floor(exp(A/epsilon)). Then

    eta(epsilon) log n_epsilon / loglog n_epsilon -> d A.

If A<1/(d c_*), Section 6 gives

    (log n_epsilon) R_eta(epsilon)(n_epsilon) ->infinity,

and therefore R_eta(epsilon)(n_epsilon)/epsilon ->infinity. In particular,
an admitted instance still exceeds epsilon at that deterministic horizon.
Fixed-kernel TV monotonicity therefore forces the worst-case mixing time
beyond n_epsilon. Let A increase to 1/(d c_*) to obtain the new lower.
The inherited eta-independent Q=I family yields the additional K lower.
Together with the incoming upper, this proves the exact limit

    epsilon log T_policy(epsilon) -> max(K,1/(d c_*)).

No monotonicity of a diagonal sequence with changing eta was assumed.

For the stated power law, suppose u/log L->lambda in (0,infinity). The
incoming finite certificate with any fixed c<c_* gives

    R_eta_n(n) <= (K+o(1))/L + L^(-lambda c+o(1)).

(The fixed multiplicative certificate constants are absorbed into o(1) in
the exponent.) It follows that
liminf [-log R/log L] >=min(1,lambda c_*).
The eta-independent K lower gives limsup [-log R/log L]<=1. Formula (F),
valid for every fixed b,D,v, gives limsup <=lambda phi_{a_{b,D}}(v).
Taking the infimum over those fixed parameters yields the matching bound
min(1,lambda c_*). This argument includes lambda=1/c_* only at the power
level; it supplies no limiting prefactor for L R there.

## 8. An exact strict improvement at K=1, alpha=1/2

Choose

    b=63/100, D=64, v=log 4, M=4,
    eta_n=(3/2) loglog n / log n.

The KL slack is exact: e>65/24>100/37, hence -log(37/100)<1.
The effective competition is a_{b,D}=(37/100)(65/64), and

    1+4 a_{b,D}=801/320.

The condition (3/2)phi_{a_{b,D}}(log 4)<1 is precisely

    801^3 < 16 * 320^3.

Both sides are integers; no floating root or positivity claim is needed.
Therefore this fixed-degree tree has (log n)R_eta_n(n)->infinity at multiplier
3/2, strictly strengthening the old path's certified multiplier 27/25.
Taking the legitimate fixed-parameter limits in Section 6 reaches the exact
incoming threshold 1/c_*=1.5422114197... in the supremum sense. This exact
example is illustrative, not the proof of that full threshold.

## 9. Costs, failed shortcuts, and implementation boundary

The scientific calculation above is analytic. No old search or numerical
campaign was rerun by this contributor. Root may supply an independent
exact/lumped finite diagnostic, whose arithmetic and cost status are separate.
Model/token/monetary discovery totals are unavailable. This source is not a
certificate produced by a formal proof assistant.

Corrections and invalid shortcuts that mattered:

* The first proposed extension omitted a factor D in reverse acceptance.
  Correcting it gives D n^-2 s and aggregate reverse f/n^2, preserving the
  argument. The per-vertex ratios, rather than level-mass ratios, determine
  the actual acceptance branches.
* Same-level global jumps exist on a tree and contribute to a full-state exit.
  They are bounded by S_q in (A). They cannot be treated as absent.
* A single fixed ray loses D at every step. The event must include every child
  marked move; this gives f=beta D s/[2(D+1)].
* Retention concerns the entire leaf set, not one leaf. Global moves among
  leaves are retained, and its killed row mass is exactly 1-e_H.
* The incoming one-step norm obstruction does not itself prove this lower.
  Reachable capture from q, strict KL admission, and terminal retention are
  additional construction obligations, discharged above.
* Letting D grow with n is unnecessary and would need extra error accounting.
  The proof chooses D fixed for every strict lower bound before taking n large.
* Matrix powers on accessible examples could check finite formulas but cannot
  prove the asymptotic result or its strict positivity/normalization.

The implicit tree is fully specified by D,m,b,z,p,n. One can sample q by first
selecting its level (or star) and then a uniform word at that level, and sample
Q by a uniformly chosen neighbor slot. Target/proposal log ratios are explicit
for this verification family. This does not grant a black-box recipient a
normalizer or a whole-target table. If the complete finite target law is itself
available, direct target sampling is an ordinary stronger comparator. Pure IMH
already has coefficient K in the admitted black-box comparison; the theorem
quantifies the robustness cost of adding weakly screened local transitions and
provides no end-to-end computational speedup.
