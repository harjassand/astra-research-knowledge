# Native critical amplitudes and the discrete crossing mechanism

Contributor: `/root/cycle10_transport`, 23 October 2026 Australia/Brisbane.
This is a bounded lower-construction contribution for principal integration.
It does not claim a universal lattice upper for arbitrary reciprocal graphs.

## 1. Source, contract, and statements

Read source: unchanged Cycle9 `SHARP_DISTORTION_RATE.md`, Sections 6–10,
and `CONTINUATION_SEED.md`, from the exact 3,121,759-byte owner archive,
SHA256 `959dcd192aef8487bcd19fcb3466fe6ea6360d4780c3b9a8c892d04b8af03299`.
The source principal proof SHA256 is
`5f76de8b2e7567cadae8ae06d272de8e1bdbae1e6e29ddf1a34800f090e5ce2f`.
No original source or old frozen fixture is modified or rerun.

Use the exact native class in that source: finite labelled positive pi,q,
one population D(pi||q)<=K, q initialization, fixed alpha in (0,1),
beta=1-alpha, target-independent reciprocal row-stochastic Q, actual local
acceptance and rejection diagonal, C=(I+alpha G+beta L)/2. Supports may
grow across runs, while all policies and kernels are fixed within a run.

Fix d>0 and assume public policies satisfy

    D_n=|kappa_n-eta_n| A_n=d,
    u_n=eta_n log n,
    u_n c(d)=loglog n+s+o(1),

where s is fixed. Put

    ell=log n, L=log ell,
    b0=1-exp(-K), r=alpha exp(-K)/beta,
    h(a)=log(1+r exp(a)), gamma=h(0), t=h'(0)=r/(1+r),
    d_star=gamma/t,
    c(d)=inf_{a>=0} h(a)/(d+a).

The regime r>=exp(d), where c(d)=1, is treated separately by one crossing
in Theorem D. The strong-discrepancy statements d>=d_star automatically
have c(d)<1. Logs are natural and TV is half l1.

### Theorem A: attainable interior and joining-point amplitude

For r<exp(d) and 0<d<d_star, let a_star>0 be the unique finite minimizer of
h(a)/(d+a). For d=d_star put a_star=0. Under EVERY public policy sequence
above, there are admitted native instances, with the actual public bound
and either possible mismatch sign, for which

    ell TV(q_n C_n^n,pi_n) -> b0 exp(-s).                 (A)

This is a statement about the original full-chain law, not only a selected
capture event. The construction has pure-IMH error O(ell^-4) at j/n->t0>0.

### Theorem B: attainable strong-discrepancy phase profile

For d>d_star define

    B=d t-gamma>0,
    Psi(x)=min(B x, gamma(1-x)), 0<=x<=1,
    x_n={u_n/d}.

There are admitted native instances, selected from two explicitly defined
integer depths, for which

    ell TV(q_n C_n^n,pi_n)
       = b0 exp(-s) exp[-Psi(x_n)] + o(1).              (B)

All errors tend to zero along the entire policy sequence, including when
x_n approaches either endpoint or the two branches tie. In particular,

    limsup ell R_n >= b0 exp(-s),
    liminf ell R_n >= max(K,
        b0 exp(-s-gamma(1-d_star/d))).                  (C)

The K lower is the unchanged ordinary information-tail family and is
combined by a MAX, not by sharing its KL allocation with the present tree.

Formula (B) is an exact amplitude for an attainable family. It does not
prove that the class-supremum R_n oscillates, and does not exclude a better
heterogeneous native geometry filling its troughs. If a principal upper
proves limsup ell R_n <= max(K,b0 exp(-s)), then (C) and the tail family
immediately give equality of that limsup. This logical use is separate
from an unproved universal phase profile.

### Theorem D: attainable clipped-branch amplitude

For r>=exp(d), where c(d)=1 and u_n=L+s+o(1), a native one-crossing family
obeys

    ell TV(q_n C_n^n,pi_n) -> b0 exp(d)/r exp(-s).       (D)

This includes r=exp(d). It is a matched lower for the principal's proposed
weighted-energy upper; that upper is a separate obligation. The actual
local forward acceptance is order ell^-1, and its preparation, label,
query and precision costs are not waived.

## 2. Public construction and moving information slack

For all sufficiently large n let

    b_n=b0-L^-2, p_T=ell^-4,
    delta_n=kappa_n-eta_n, R_A=exp(A_n),
    H_n=4 log(L+1).

Finitely many earlier horizons can use pi=q and Q=I; they do not change
any limit or violate the public asymmetry upper bound.

Since d>0, A_n>0 and delta_n is nonzero. Its sign may vary with n. Use a
complete M-ary tree plus one core vertex. Set native edge probabilities

    Q_parent,child=1/(M+R_A),
    Q_child,parent=R_A/(M+R_A).

Every internal row sums exactly to one, with its M children and one
parent. The root and leaves receive the real completing diagonals; the
core has Q_core,core=1. All edges are reciprocal and have absolute log
asymmetry A_n. These proposal rows use only public quantities and labels.

For delta_n>0 use progress from root to leaves and

    M=ceil(R_A exp(H_n)), chi=M/R_A.

For delta_n<0 use progress from leaves to root and

    M=ceil(R_A exp(-H_n)), chi=R_A/M.

In the negative case kappa_n>=0 implies A_n>=d/eta_n. The critical scale
has eta_n=Theta(L/ell), so A_n is much larger than H_n. Consequently M>=2
eventually in both signs and

    chi=(L+1)^4(1+o(1)),
    f=chi/(1+chi),
    J(1-f)=o(1) whenever J=Theta(L).                    (1)

The rounding in expansion is an O(1/R_A) additive error in chi, hence a
relative O(exp(-H_n)/R_A) error. In coalescence it is a relative
O(exp(H_n-A_n)) error. Neither estimate suppresses a native multiplicity.

Let J be one of the integer depths specified below and put

    T_n=ell+6L+log b_n,
    a_{n,J}=[eta_n T_n/J + eta_n log chi-d]_+,
    V=(d+a_{n,J})/eta_n-log chi,
    z=exp(-V),
    q_i=b_n z^i,
    pi_i=p_T n^(-2(J-i)), 0<=i<=J.                     (2)

Split these level totals uniformly among M^i vertices in expansion and
M^(J-i) vertices in coalescence. The core completes both probabilities.
The depths and a_{n,J} depend only on the public policy, K,alpha and n.
Thus Q is fixed before the target is specified and is target-independent.
The proof's use of normalized masses is not a free sampler target table.

The multi-level choices below satisfy

    J=Theta(L), a_{n,J}=O(1), V~ell/J, V/L->infinity,
    T_n<=J V<T_n+V,                                   (3)

with equality J V=T_n whenever the positive part in (2) is positive.
In the only zero-positive-part case used below, J=ceil(u_n/d) and (3)
follows from Jd-u_n<d (or equality at an integer, where the positive part
is in fact positive because of the cutoff and multiplicity corrections).
The clipped one-crossing choice instead has J=1, a_{n,1}=u_n-d+o(1)
and V=T_n~ell; the same terminal-weight inequalities and admission hold.

In particular z is smaller than every fixed power of ell^-1. Positivity
of the core masses follows from b_n->b0<1 and p_T->0.

## 3. Actual native acceptance, KL admission and retention

The native per-vertex progress ratio is z/M in expansion and zM in
coalescence. The reverse Q ratio is respectively R_A and R_A^-1. Direct
substitution into the specified screen gives S_xy=exp(-a_{n,J}) in BOTH
orientations. The target Hastings ratio is n^2/chi, so the second forward
acceptance is one eventually. Reverse acceptance is chi exp(-a_{n,J})/n^2.
Counting every child gives the exact aggregate local transitions

    L(i,i+1)=f exp(-a_{n,J}),
    L(i,i-1)=f exp(-a_{n,J})/n^2,                       (4)

where nonexistent directions are omitted at endpoints. The diagonal is
the actual completion of these accepted transitions. This computation
uses per-vertex probabilities, not level masses as acceptance ratios.

The level-plus-core partition is strongly lumpable: all permutations
within a level induced by tree automorphisms preserve q,pi,Q and all
transition sums to another level. The initial q is uniform within every
level, as are all its evolved laws. Native and quotient TV therefore
coincide for the whole terminal union and core events used here. This
does not assert sufficiency for a different within-level subset query.

For W_i=pi_i/q_i, (2)-(3) give

    n ell^2 <= W_J < n ell^2 exp(V),
    W_{J-1}<ell^2/n,
    W_{i+1}/W_i=n^2 exp(V).                            (5)

Thus all transient W_i<1<W_core<W_J eventually. All their entropy
contributions are negative. With q_core=1-sum_i q_i,

    D(pi||q) <= log(1/q_core)+p_T log W_J.

Now

    q_core=exp(-K)+L^-2+O(z),
    log(1/q_core)=K-exp(K)L^-2+o(L^-2),
    p_T log W_J=O(ell^-3)=o(L^-2).                      (6)

Hence D(pi||q)<K for every sufficiently large n. This is a single complete
information allocation. Moving b_n toward b0 is legitimate because its
explicit entropy slack dominates every positive contribution.

The full-chain escape probability from the entire terminal union is

    d_T=alpha(1-p_T)/(2W_J)
             +beta f exp(-a_{n,J})/(2n^2),
    n d_T <= alpha/(2ell^2)+beta/(2n) ->0.              (7)

All global moves within that union remain in it. The actual chain is
never modified to retain mass; the selected stay event is only a lower
bound, and Section 4 supplies a matching upper for the original law.

## 4. A multiplicative full-law calculation

Set sigma=exp(-a_{n,J}), c_f=beta f sigma/2 and
g_core=alpha q_core/2. The CORE hazard remains bounded away from zero;
the forward hazard may tend to zero in Theorem D. Let tau be
the first hit of the core or terminal union, starting at level zero.
Every transient state has the exact per-step core hazard g_core, by (5).
Therefore

    P(tau>m) <= (1-g_core)^m,
    E[tau] <= 1/g_core.                                (8)

Before tau, call a transition exceptional if it is a local reverse move
or a global move to a different tree level (including a global terminal
jump). Same-level global moves and global rejections are holds in this
counter. The per-step exceptional probability is uniformly

    O(z+n^-2).                                        (9)

Indeed global upward proposals have total probability at most
sum_{j>=1}q_j=O(z), while global moves toward preceding levels have accepted
mass

    sum_{j<i}pi_j/W_i = q_i sum_{k=1}^i n^(-2k)
                       <= b_n/(n^2-1).

Local reversal is bounded by (4). Equations (8)-(9) imply that the chance
of any exceptional transition before tau is O(z+n^-2).

For this calculation ONLY, couple to a counter that replaces exceptional
transitions by holds. The counter has local forward probability c_f,
core killing probability g_core, and the remaining probability as a hold.
Its probability of making all J forward exits before the core is exactly

    [c_f/(c_f+g_core)]^J.

The original law and this counter differ in their first-hit answer by at
most the probability of an exceptional transition before tau. Including
q initialization, whose mass at other tree levels is O(z), gives

    P_q(tau_T<tau_core)
      =b_n [c_f/(c_f+g_core)]^J + O(z+n^-2).            (10)

No later transition of the original chain has been deleted. To control
the original n-step TV from above, decompose at the first core hit. Every
core-started remaining law has TV at most pi_tree=sum_i pi_i from pi,
by contraction of the original C and TV(delta_core,pi)=pi_tree. The
remaining mass is bounded by the event in (10), plus the probability of
neither boundary being hit by time n. For the lower, require a terminal
hit before n/2 and then terminal retention through n, using (7)-(8).
Thus

    TV(q C^n,pi)
       = b_n [c_f/(c_f+g_core)]^J (1+o(1)),             (11)

provided the main term is Theta(ell^-1), as established below. All
additive errors O(z+n^-2), pi_tree=O(ell^-4), and exp(-c n) are then
negligible. This also proves that the counter has merely evaluated an
original-chain first-hit probability to a paid error; it is not a sampler.

Finally, uniformly for every a=a_{n,J}>=0,

    log[1+alpha q_core exp(a)/(beta f)]
       = h(a)+O(L^-2+1-f+z).

The bound is uniform in a because the logarithmic ratio changes by at
most the absolute logarithmic change in alpha q_core/(beta f), whose
limit r is fixed and positive. Multiplying by J=O(L) and using (1) gives
o(1). Consequently the
complete native full-law formula is

    TV(q C^n,pi)=b_n exp[-J h(a_{n,J})](1+o(1)).         (12)

The actual full-chain returns are retained throughout this argument.

## 5. Interior minimizer: integer rounding disappears at first order

Assume r<exp(d) and d<d_star. The finite minimizer a_star>0 obeys

    h'(a_star)=c(d),
    h(a_star)=c(d)(d+a_star).

Choose J to be a nearest positive integer to u_n/(d+a_star). Then

    a_{n,J}=a_star+O(J^-1)+o(J^-1)>0,
    J(d+a_{n,J})=eta_n T_n+eta_n J log chi=u_n+o(1).

Here eta_n=Theta(L/ell), J=Theta(L), log chi=O(log L), so every added
cutoff and multiplicity term is o(1). Taylor expansion with bounded second
derivative gives

    J h(a_{n,J})
      =c(d)J(d+a_{n,J})+O(J(a_{n,J}-a_star)^2)
      =c(d)u_n+o(1).                                  (13)

Substitution into (12) proves Theorem A in the interior. This is the
stationary cancellation behind the absence of an integer-phase loss.

At d=d_star, use J=floor(u_n/d), not an arbitrary nearest integer. The
positive part in (2) is positive, a_{n,J}=O(J^-1), and d h'(0)=gamma.
Therefore

    J h(a_{n,J})
      =J gamma+t(u_n-Jd)+o(1)
      =(gamma/d)u_n+o(1).                              (14)

This proves the joining-point case of Theorem A. Choosing the ceiling
with zero attenuation can lose a nonvanishing factor and would not prove
the joining-point amplitude.

## 6. Strong discrepancy: two exact native depths

Suppose d>d_star. Let J_-=floor(u_n/d) and J_+=ceil(u_n/d), ignoring the
duplicate when they coincide. Both tend to infinity. For each depth use
the same construction (2), with its own a_{n,J}. Each is admitted by the
preceding sections under exactly the same public policy.

For J_-, a is positive and O(J_-^-1), and Taylor expansion gives

    J_- h(a_{n,J_-})
      =J_- gamma+t(u_n-J_-d)+o(1)
      =(gamma/d)u_n+(dt-gamma)x_n+o(1).                (15)

For J_+, the positive part in (2) is at most
eta_n(6L+log b_n)/J_+ + eta_n log chi=o(J_+^-1).
It exactly pays a possible near-integer shortfall caused by the cutoff
and row-multiplicity corrections. Thus

    J_+ h(a_{n,J_+})
      =J_+ gamma+o(1)
      =(gamma/d)u_n+gamma(1-x_n)+o(1)                  (16)

when x_n>0. At x_n=0, J_+=J_- and its excess is o(1). The minimum of
the two displayed costs is therefore represented continuously by
Psi(x)=min((dt-gamma)x,gamma(1-x)), with Psi(0)=Psi(1)=0.

Select the lower-cost depth (a deterministic function of public quantities).
Equations (12), (15), (16), and c(d)=gamma/d prove Theorem B.
No empirical optimization or target-dependent proposal selection is used.

The maximum phase penalty is

    max_{0<=x<=1} Psi(x)
       =gamma(dt-gamma)/(dt)
       =gamma(1-d_star/d).                             (17)

This gives the liminf lower in (C). For the limsup lower, take integers n_j
nearest to exp(exp(j gamma-s)). Then L(n_j)+s=j gamma+o(1), while the
critical policy relation gives u_{n_j}/d=j+o(1). Its fractional part tends
to an endpoint, so Psi(x_{n_j})->0. Any allowed o(1) policy perturbation
preserves this conclusion. The unproved all-class lattice upper is not
used to obtain the limsup lower.

## 7. A scoped finite crossing-control theorem

This section explains the mechanism but is NOT a reduction of arbitrary
native reciprocal graphs. Consider a killed directed transport control
model with remaining progress U>0. A crossing may contribute x>0 progress
and has attenuation a=(x-d)_+; a local proposal of aggregate weight one
competes with fixed killing ratio r. Its crossing survival is

    1/(1+r exp(a)).

Allow any finite sequence of crossings, overshoot, and randomized choices
of crossing types. Holding has no cost besides the same competing killing
and does not change the exit survival ratio. For a fixed count J, convexity
of h and sum x_i>=U imply the least survival cost

    H_J(U)=J h((U/J-d)_+).                             (18)

Equality is attained by equal lengths above d; when U<=Jd, use lengths
at most d (or overshoot with length d), all with zero attenuation.

Mixtures of outgoing types do not improve the Bellman value at a state.
If type i has proposal share w_i, attenuation a_i and continuation value
V_i, with sum_i w_i=1, its exit value is

    [sum_i w_i exp(-a_i) V_i]/[r+sum_i w_i exp(-a_i)].

This is a convex combination of V_i/(1+r exp(a_i)), with weights
proportional to w_i(r+exp(-a_i)). Therefore a pure outgoing type is at
least as good. Induction over finite horizons, and monotone limits over
the possible number of crossings, reduce this CONTROL MODEL to pure paths.
Every additional crossing has survival at most exp(-gamma), so arbitrarily
long paths cannot produce an unaccounted positive limiting value.

When d>=d_star, the real-variable function
J -> J h(U/J-d), on J<=U/d, is nonincreasing: its derivative is

    h(a)-(d+a)h'(a)=-B(a),
    B(0)=d h'(0)-gamma>=0,
    B'(a)=(d+a)h''(a)>0.

For J>=U/d the cost is J gamma and is increasing. Hence the exact optimum
for U>=d is

    min{ floor(U/d) h(U/floor(U/d)-d),
         ceil(U/d) gamma }.                            (19)

This proves the phase penalty in its valid directed control class.
An all-native upper would still need to justify the reduction to a scalar
remaining-progress variable with this fixed killing ratio, preserving the
q-weighted mass, graph returns, reciprocal proposal budgets, and one KL
constraint. Neither the convex-combination observation nor a scalar cost
minimum supplies that bridge.

## 7A. Clipped branch: one strongly screened crossing

Assume r>=exp(d). Then c(d)=1 and u_n=L+s+o(1). Keep b_n, M, chi, f and
the actual native row construction from Section 2, but set J=1. Equation
(2) gives, eventually without a zero positive part,

    a_{n,1}=eta_n T_n+eta_n log chi-d
           =u_n-d+o(1) -> infinity,
    V=T_n,
    q_1=b_n exp(-T_n)=1/(n ell^6),
    W_1=n ell^2,
    sigma=exp(d-u_n+o(1)).                             (20)

There is a single transient progress level. Both signs of mismatch remain
native and admissible; negative mismatch still gives A_n>=d/eta_n much
larger than log chi. The target preterminal mass is pi_0=ell^-4/n^2.

The core hazard g_core is uniformly positive, so the rare forward
acceptance sigma does not invalidate the stopping-time estimate (8).
Exceptional moves have probability O(z+n^-2), which remains negligible
relative to ell^-1. Terminal retention (7), the KL admission (6), and
the original-chain core contraction are unchanged. Thus (12) applies:

    TV(q C^n,pi)
       =b_n/[1+(alpha q_core/(beta f)) exp(a_{n,1})]
          (1+o(1))
       =b0 exp(d-u_n)/r (1+o(1)).                      (21)

This proves (D). The ordinary pure-IMH bound below is still O(ell^-4).
No singular limit of a fixed finite-spacing lower was invoked; the actual
one-crossing probabilities and full n-step law were computed directly.

## 8. Ordinary comparison, resource boundary and decisions

The q and pi level totals remain the geometric totals of the accepted
Cycle9 family. Its ordinary comparison therefore applies directly:

    TV(q G^j,pi) <= p_T/(1-n^-2)
                    + b_n z/[(1-b_n)(1-z)] + b_n^(j+1).

At j/n->t0>0 this is O(ell^-4), while the constructed critical hybrid
has a positive order-ell^-1 amplitude. Direct analytic sampling remains
allowed if the actual recipient is given that analytic target. There is
no practical sampler speedup, wall-time comparison or target-call gain.

The native support is 1+sum_{i=0}^J M^i. Labels, reverse-Q evaluation,
target evaluations, preparation, caching and arithmetic precision remain
charged. No enormous native graph is materialized here; no fixed-word
implementation theorem is asserted. The proof counter is not an absorbed
simulation oracle.

Important failed premise: a lattice-shaped family lower does not establish
oscillation of the minimax risk. A heterogeneous native construction may
exceed the pure-path profile. The exact interior/joining amplitude, if
combined with a valid upper, and the exact all-class limsup at stronger d
are sound consequences. The general strong-discrepancy liminf remains
open without the missing native upper or a better construction.

No numerical experiment, historical replay, primary-literature search,
source mutation, public sharing, spending or delivery operation was run by
this contributor. Recorded costs are local source reads, mathematical
reasoning and this source write. CPU, inference/token and total discovery
costs are unknown. The principal owns review, integration and delivery.
