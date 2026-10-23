# How much proposal screening is needed?

Principal continuation within the same checkpoint. Astra PRO3, 22 October 2026
(Australia/Brisbane). This addendum follows the frozen SAFE_LOCAL_THEOREM.md;
it supersedes that file's tentative future-question paragraph, without changing
its accepted theorem or source bytes. The operation is a standard factorized
Metropolis acceptance. The new issue is its uniform entropy-only robustness.

## 1. Precisely changed class and results

Here the space is **finite**, with strictly positive probability vectors q and
pi. Its size may vary within the supremum. The proposal Q is a fixed symmetric
stochastic matrix; it may have zeros and need not be irreducible. We can sample
q and Q and evaluate q and the unnormalized target at proposed points. The same
positive population K, fixed alpha in (0,1), proposal initialization and fixed
lazy mixture are retained. Write beta=1-alpha and D(pi||q)<=K.

For a fixed screening exponent 0<=eta<=1, the local transition from x to y
uses proposal Q and acceptance

    a_eta(x,y)
      = min(1,(q(y)/q(x))^eta)
        min(1,[pi(y)/pi(x)](q(x)/q(y))^eta).            (1.1)

Normalization of pi cancels; so does any common rescaling of its raw oracle.
The first acceptance can be performed before evaluating the new target value.
The whole product is reciprocal-factor delayed acceptance for pi, hence gives
a fixed pi-reversible L_eta. Set

    C_eta=(I+alpha G+beta L_eta)/2.

At eta=0 this is ordinary local MH(Q,pi), in the old obstructed class. At eta=1
it is the fully screened kernel covered by SAFE_LOCAL_THEOREM.md. Lowering eta
weakly increases every off-diagonal local acceptance, as verified below.

Let R_eta(n) be the supremum of TV(q C_eta^n,pi) over exactly this finite-space
class, with K,alpha,eta fixed, and let T_eta(epsilon) be the corresponding
supremum mixing time.

**Theorem 3 (every positive screen eliminates the uniform floor).** For every
fixed eta in (0,1],

    lim_{n->infinity} R_eta(n)=0.                      (1.2)

Thus T_eta(epsilon)<infinity for every epsilon>0. This is a uniform conclusion,
not simply convergence on each finite instance. For eta=0, the inherited sharp
floor remains beta b_K/(1-alpha b_K)>0, with b_K=1-exp(-K): its matching old
construction already uses symmetric Q. The endpoint separation is therefore
real, although this theorem does not quantify a sharp cost for every eta>0.

**Theorem 4 (a proved interval retaining the optimal coefficient).** Put

    theta_K=1-alpha exp(-K)/2.

For every fixed eta with theta_K<eta<=1,

    lim_{n->infinity} (log n) R_eta(n)=K,
    lim_{epsilon->0} epsilon log T_eta(epsilon)=K.       (1.3)

The threshold theta_K is a **sufficient threshold from this proof**, not a
proved transition point. The sharp coefficient for 0<eta<=theta_K is open in
this checkpoint. The theorem at eta=1 is already established in the main file;
the proof below treats theta_K<eta<1.

At K=1,alpha=1/2, the sufficient interval is eta>1-exp(-1)/4, approximately
0.9080301397. Fixed choices in this interval, such as eta=0.95, accept every
local proposal at least as readily as the eta=1 safeguard and retain the same
uniform leading coefficient. This is not finite-time TV dominance or a
computation-saving claim. Ordinary IMH still has coefficient K.

## 2. Reversibility and the one-step power bound

Each factor r in (1.1) has reverse 1/r. Since
min(1,r)/min(1,1/r)=r, the ratio of forward and reverse acceptance products is
pi(y)/pi(x). Symmetry of Q proves pi-reversibility, including rejection mass.

Write z=q(y)/q(x) and v=pi(y)/pi(x). If z<=1, then
a_eta=min(z^eta,v), which is nonincreasing in eta. If z>=1, then
a_eta=min(1,v z^{-eta}), also nonincreasing in eta. This proves the claimed
off-diagonal ordering; it does not give an initial-law TV ordering.

For 0<eta<1, incoming accepted q-mass into A is bounded by

    sum_{x,y in A} Q(x,y) q(x)^{1-eta} q(y)^eta,

where the notation means x ranges over the whole space and y over A.
Applying Holder to this pair sum gives the upper bound

    [sum_x q(x)Q(x,A)]^{1-eta}
    [sum_{y in A} q(y) sum_x Q(x,y)]^eta
      =[qQ(A)]^{1-eta} q(A)^eta <= q(A)^eta.            (2.1)

The equality uses the column sums of symmetric stochastic Q. Add rejected
mass at most q(A). This proves

    qL_eta(A)<=q(A)+q(A)^eta.                          (2.2)

Using qG<=2q,

    qC_eta(A)
      <=(1+alpha/2)q(A)+(beta/2)q(A)^eta
      <=c q(A)^eta,                 c=3/2.            (2.3)

Unlike eta=1, no fixed uniform linear bound qL_eta<=Lambda q exists for any
0<eta<1. To see this, take Q to swap two states, q=(1-r,r), and
pi=(1-p,p), where p=k/log(1/r) and 0<k<K. For all sufficiently small r,
0<r<p<1 and

    D(pi||q)
      =(1-p)log[(1-p)/(1-r)]+p log p+p log(1/r)<k<K.

This divergence tends to k. For a move from the common state to the rare
one, the second acceptance in (1.1) tends to one and eventually equals one;
the first is (r/(1-r))^eta. The exact reverse acceptance is
((1-p)/p)(r/(1-r))^eta. Therefore

    qL_eta({rare})/r ~ r^{eta-1} -> infinity.           (2.4)

These are admitted positive finite targets. Failure of the linear sufficient
condition is **not** failure of robustness: (1.2) and part of (1.3) are proved
by using the weaker power bound instead. The eta=0 and eta=1 endpoint details
are recorded in the independent preparatory note.

## 3. Transporting a setwise power bound

We use the following elementary lemma, valid also for finite positive measures.
If mu(A)<=D nu(A)^r for every measurable A, where 0<r<=1, then for every
Markov kernel P,

    mu P(A)<=D[nu P(A)]^r.                            (3.1)

Indeed, for f=P1_A in [0,1], the layer-cake formula and concavity give

    mu f=integral_0^1 mu(f>u)du
      <=D integral_0^1 nu(f>u)^r du
      <=D [integral_0^1 nu(f>u)du]^r
       =D(nu f)^r.

No independence between a stopped state and its history is required. Apply
this lemma inductively to (2.3). With

    r_j=eta^j,
    D_j=c^{1+eta+...+eta^{j-1}}
       =c^{(1-eta^j)/(1-eta)},       D_0=1,
    D_* = c^{1/(1-eta)},

we have uniformly in the instance

    (qC_eta^j)(A)<=D_j q(A)^{r_j},       D_j<=D_*.      (3.2)

The constants here may depend on fixed eta. No uniform eta->1 or eta->0
estimate is inferred from these particular constants.

Run the same fixed chain from q. For h>0 define the first state-hitting time
tau=inf{j>=0:W(X_j)>=h}, b_h=q(W<h), and
theta_h=1-alpha(1-b_h)/2. As in the principal first-hit argument,

    P(tau>s)<=b_h theta_h^s.                           (3.3)

Its submeasure nu_j(A)=P(tau=j,X_j in A) satisfies

    nu_j(A)<=D_j [q(A intersect {W>=h})]^{r_j}
           <=D_j h^{-r_j} pi(A)^{r_j}.                (3.4)

Use (3.1), with nu=pi and pi C_eta=pi, to propagate (3.4) for s-j steps.
The exact first-hit decomposition then gives, for D subset {W<h},

    mu_s(D):=(qC_eta^s)(D)
       <=b_h theta_h^s+sum_{j=0}^s D_j[pi(D)/h]^{r_j}.

In particular, when pi(D)/h<=1,

    mu_s(D)<=b_h theta_h^s+(s+1)D_*[pi(D)/h]^{r_s}.    (3.5)

Later returns below h are included in the propagated submeasures. This is
again a deterministic-time law; the hit time is only a proof device.

The power bound also gives an explicit bounded-density approximation. Let
f_s=dmu_s/dq, let V>=1, and write

    E_V={f_s>V},       delta_s=mu_s(E_V).

Since q(E_V)<=1/V, (3.2) implies delta_s<=D_s V^{-r_s}. Define the probability

    tilde_mu_s = mu_s restricted to E_V^c + delta_s q.

Then

    TV(mu_s,tilde_mu_s)<=delta_s,
    tilde_mu_s <= (V+1)q,
    tilde_mu_s(D)<=mu_s(D)+delta_s.                    (3.6)

This auxiliary probability is not sampled and need not be computed by the
algorithm. It is a valid deterministic-time comparison measure. TV contraction
and the general-initial-law bound (3.9) of SAFE_LOCAL_THEOREM.md apply to it.

## 4. Proof that every fixed eta>0 has zero uniform floor

Fix eta in (0,1), and let delta>0. Choose h=1/4. The inherited entropy
envelope b_h<=bar_b_K(h)<1 gives a common theta_bar<1. Choose a finite integer
s so bar_b_K(h) theta_bar^s<=delta. Then choose a finite V>=1 so that
D_* V^{-eta^s}<=delta. These constants can be very large but depend only on
K,alpha,eta,delta, and not on the instance or the later time t.

For t->infinity choose B=R=t/(log t)^4. Eventually 1/B<h. Since pi(W<1/B)
is at most 1/B, (3.5) gives

    mu_s(W<1/B)<=delta+(s+1)D_*(1/(Bh))^{eta^s}
                =delta+o(1),                         (4.1)

uniformly over the class. By (3.6), tilde_mu_s has density cap V+1 and low
mass at most 2delta+o(1). In the main bound (3.9), its high-tail term tends to
zero, Delta_{V+1}->0, delta_{V+1}->0, and the small tails vanish. Also the
low-set multiplier beta/(1-alpha b) is at most one. Consequently

    limsup_{t->infinity} sup TV(qC_eta^{s+t},pi)
       <=delta+2delta=3delta.                         (4.2)

The first delta is the approximation error from (3.6). Since delta was
arbitrary, (1.2) follows. Uniformity is preserved throughout. Monotonicity
of TV under each fixed invariant C_eta then implies finite uniform mixing
time for each positive epsilon.

The eta=1 case follows from Theorem 1. The eta=0 nonzero floor is an inherited
result, with its actual source and positive matching families preserved.

A quantitative variant was identified in the independent challenge. Write
kappa=-log(theta_K), ell=-log eta. For any fixed
0<zeta<min(1,kappa/ell), choose v=zeta/kappa in the choices (5.1) below.
Then v ell<1. Every truncation, propagated-hit and smoothing error in that
proof is o(1/log n); its no-hit term is O((log n)^(-zeta)) instead of
o(1/log n). The same displayed bounds therefore prove

    R_eta(n)=O_{K,alpha,eta,zeta}((log n)^(-zeta)),
    T_eta(epsilon)<=exp[O_{K,alpha,eta,zeta}(epsilon^(-1/zeta))]. (4.3)

This is a sufficient, nonsharp resource bound. Its constants are not measured
sampling costs. It does not establish a finite coefficient for epsilon log T
in the unresolved interval, or a lower rate worse than ordinary IMH.

## 5. Sharp coefficient on a sufficient interval

Fix theta_K<eta<1. Write

    kappa=-log theta_K,       ell=-log eta,

so 0<ell<kappa. Choose any fixed v with

    1/kappa < v < 1/ell,

and put a=v ell<1, z=(1+a)/2 in (a,1). For total time n choose

    s=ceil(v log log n),     t=n-s,
    h=(log n)^(-2),          V=exp((log n)^z),
    B=t/[(V+1)^2(log t)^6],  R=t/(log t)^6.            (5.1)

Eventually t~n, B,R>e, 1/B<h<1/2, and log B~log R~log n. Moreover

    eta (log n)^(-a) <= r_s=eta^s <= (log n)^(-a).      (5.2)

The entropy envelope gives theta_h<=theta_K+O(h log(1/h)). Its perturbation
times s tends to zero, so

    b_h theta_h^s=O((log n)^(-v kappa))=o(1/log n).     (5.3)

By (3.6) and (5.2),

    delta_s<=D_* exp[-eta(log n)^{z-a}]=o(1/log n).     (5.4)

For D={W<1/B}, log(Bh)~log n; hence, eventually,

    (s+1)D_*[pi(D)/h]^{r_s}
       <=(s+1)D_* exp[-(eta/2)(log n)^{1-a}]
        =o(1/log n).                                 (5.5)

Combining (3.5), (3.6), and (5.3)--(5.5), the low mass of tilde_mu_s is
o(1/log n), uniformly in the instance. Its density cap is A=V+1. In the main
finite bound,

    A^2 B/t=(log t)^(-6),       R/t=(log t)^(-6),
    A^2/t=exp(2(log n)^z+o(1))/t ->0

faster than any fixed inverse power of log n. Thus Delta_A=O((log n)^(-3)).
Also 1/B and A a_tail/R are o(1/log n), and eta_t=O(t^{-1/2}). The only
leading term is

    a_tail=pi(W>R)<=K/(log R-1)=(K+o(1))/log n.

TV contraction for (3.6) and the main bound therefore prove

    limsup (log n) R_eta(n)<=K.                        (5.6)

For the lower bound, choose Q=I, so L_eta=I for every eta. The positive
two-state family in Section 5 of SAFE_LOCAL_THEOREM.md belongs to this
finite-space class and gives the matching coefficient K. The same explicit
monotone uniform inversion there proves the mixing-time limit in (1.3).

All choices are proof parameters; the actual sampler uses the same fixed
eta and C_eta at every step and never computes a normalized W threshold,
first hitting time or auxiliary measure.

## 6. What is and is not resolved

The eta=1 structural theorem is valid on arbitrary measurable spaces with
the explicit domination condition. This addendum's tempered-Q construction
and supremum are stated only on finite spaces. No continuous-space extension
is silently claimed; a symmetric density and reference-measure formulation
would need its own hypotheses and integrability audit.

The proved picture is:

* eta=0: inherited strictly positive uniform error floor;
* every fixed eta>0: zero uniform floor and finite uniform time at each error;
* eta>1-alpha exp(-K)/2: sharp coefficient K;
* 0<eta<=1-alpha exp(-K)/2: the sharp coefficient is unresolved here.

The sufficient interval is not an optimized threshold. Its limitation comes
from balancing the geometric first-hit hazard against repeated power-bound
deterioration. The two-state example in (2.4) falsifies direct reuse of a
uniform linear-domination theorem but supplies no adverse mixing lower bound.
Calling it a tempered-sampler impossibility would be an error.

Lower eta admits more of the same local proposals, but that is not a
finite-time or end-to-end speed theorem. It can increase expensive target
evaluations by passing more first stages. The pure-IMH comparison and the
memoized finite counterexample to universal hybrid dominance remain intact.
No application trial, eta-optimized empirical benchmark, or new hardware
operation is claimed. This extension is analytic, with no extra trajectory run.

**Chosen next question:** determine the sharp proposal-start forward-KL
mixing coefficient for the fixed tempered family in the remaining interval
0<eta<=1-alpha exp(-K)/2. In particular, is it K for every eta>0, or is there
a positive eta with a strictly larger coefficient (or no finite exponential
coefficient)? A useful next lower construction must respect the public fixed
symmetric Q, positive finite targets, and both stages in (1.1). A useful next
upper proof must improve the accumulated power bound rather than substitute
the invalid linear-domination claim. These are specific mathematical targets;
no search for a favorable application is needed to justify them.
