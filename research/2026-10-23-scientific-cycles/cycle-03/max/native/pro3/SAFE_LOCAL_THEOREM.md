# Proposal-start robustness from a controlled local move

Owner: Astra PRO3. Scientific date: 22 October 2026, Australia/Brisbane.
This is a new continuation after accepting the supplied optional-prefix
obstruction. Historical originality and external mathematical acceptance are
not asserted. The sampler construction below is standard delayed acceptance;
the contribution investigated here is its uniform cold-start error guarantee.

## 1. Question and exact contract

An arbitrary target-reversible local move can take an initially overrepresented
low-weight state directly into a very rare, persistent target state. The previous
forward-KL theorem therefore required a global prefix. Candidate-only stopping
cannot uniformly shorten that prefix by a fixed fraction on all null instances.
Instead of repeating that problem, we ask whether a verifiable structural
restriction on the **fixed local move** prevents the failure.

Let pi and q be equivalent probability measures on a measurable space. Fix a
positive finite measurable version W=dpi/dq. Let G be independence
Metropolis-Hastings (IMH) with proposal q and target pi. Let L be a fixed
pi-reversible Markov kernel. Fix 0<alpha<1, put beta=1-alpha, and set

    H=alpha G+beta L,       C=(I+H)/2.

Initialize at q, and use the same C at every subsequent step. There is no
special global prefix, optional stopping, state-dependent component selection,
or change of L after target observations. Besides the population certificate
D(pi||q)<=K, K>0 fixed, impose the measure inequality

    qL <= Lambda q,                                      (1.1)

where 1<=Lambda<infinity is fixed uniformly over the admitted class. This is
a condition on the **one-step image of q**, not a bound on L(x,.) for every x.
It is not a reverse-KL bound, a bounded normalized-weight assumption, or a
condition on an empirical training loss.

Define

    R_{K,alpha,Lambda}(n)
       = sup ||q C^n-pi||_TV,

and let T_{K,alpha,Lambda}(epsilon) be the supremum of the first deterministic
time at which that distance is at most epsilon. The supremum is over exactly
the above class, including all its measurable spaces. A different admitted
instance may be selected at each n; L remains fixed within an instance.

**Theorem 1 (sharp uniform robustness).** Under this contract,

    lim_{n->infinity} (log n) R_{K,alpha,Lambda}(n) = K,    (1.2)

and consequently

    lim_{epsilon->0} epsilon log T_{K,alpha,Lambda}(epsilon)=K. (1.3)

In particular, the worst-case asymptotic TV floor is zero without a specially
scheduled global prefix. All constants in the upper proof may depend on fixed
K, alpha, Lambda. No uniformity as alpha tends to zero, K tends to infinity,
or Lambda grows with the time or error tolerance is claimed.

**Corollary 2 (standard safeguarded local implementation).** Let R be a fixed
q-reversible proposal kernel. Metropolis-correct R to target pi, accepting a
proposal y from x with probability min(1,W(y)/W(x)), and call the resulting
kernel L. Then L is pi-reversible and qL<=2q. Thus Theorem 1 applies with
Lambda=2. The normalizing constant of pi is not needed.

A concrete implementation starts from a fixed computable proposal Q, first
Metropolis-corrects Q to q, and then applies the W acceptance. This is the
established two-stage delayed-acceptance algorithm. The new theorem does not
claim a new acceptance rule. A q-invariant proposal, even if not reversible,
also supplies qL<=2q for its correctly defined pi-MH correction; the reversible
case is sufficient for the scale-free implementation stated here.

The strongest ordinary comparator remains proposal-start pure IMH: it already
has coefficient K. Theorem 1 establishes robustness of a class of hybrids,
not superiority over pure IMH, finite-time domination, or a practical speedup.

## 2. Elementary domination and the first high state

For any proposal kernel P leaving q invariant, an MH kernel formed by accepting
some of its proposals has accepted incoming q-mass at most qP=q, and rejected
mass at most q. Hence its one-step image is at most 2q. In particular qG<=2q.
From (1.1),

    qC <= c q,       c=(1+2alpha+beta Lambda)/2 > 1.       (2.1)

Positivity of kernels and induction give qC^j<=c^j q for all j>=0. We do not
claim a linear-in-j bound: such a bound fails even for three-state
q-reversible-proposal MH, as the included counterexample demonstrates.

Fix h>0, set A_h={W<h}, b_h=q(A_h), and run X_0~q with kernel C. Let
tau=inf{j>=0: W(X_j)>=h}. A finite-horizon construction uses only the ordinary
iterated-kernel path measures and requires no regular conditional law or
disintegration on the underlying state space.

While tau>j, a global branch followed by a q candidate outside A_h is surely
accepted: its weight exceeds that of the current state. This event has
conditional probability alpha(1-b_h)/2, independently of the past. Thus,
writing theta_h=1-alpha(1-b_h)/2,

    P(tau>s) <= b_h theta_h^s.                           (2.2)

For j=0,...,s define the subprobability measure

    nu_j(F)=P(tau=j, X_j in F).

It is supported on A_h^c and, as a measure,

    nu_j <= (qC^j)|_{A_h^c} <= c^j q|_{A_h^c}
          <= c^j pi/h.                                 (2.3)

The exact first-hit decomposition at deterministic time s is

    mu_s:=qC^s = nu_surv + sum_{j=0}^s nu_j C^{s-j},     (2.4)

where nu_surv is the law restricted to {tau>s}. Every term is an
unconditioned submeasure. Since C preserves pi, (2.2)--(2.4) imply, for any
measurable D subset A_h,

    mu_s <= c^s q,
    mu_s(D) <= b_h theta_h^s + [pi(D)/h] S_s,
    S_s=sum_{j=0}^s c^j=(c^{s+1}-1)/(c-1).              (2.5)

This is not the fixed-prefix law with a random N inserted. It is a new
first-*state*-hitting decomposition along the actual, unchanged hybrid chain.
Local moves can cross the threshold, return below it, or reject; all those
paths are retained. The dominated first-hit submeasure and invariance, rather
than an invalid single-downward-crossing argument, control later returns.

## 3. Entropy envelopes and a general initial-law bound

The following three ingredients are reused with full hypotheses from the
unchanged previous owner archive. They are restated, and the short derivations
needed for the new initial law are supplied here.

For R>e, binary relative-entropy data processing gives

    a=pi(W>R) <= K/(log R-1).                            (3.1)

Indeed q(W>R)<=a/R and the binary divergence is at least
a log R+(1-a)log(1-a)>=a(log R-1). With
M=exp(2K+1), A_0={W<=M}, and s_0=pi(A_0), this ensures s_0>=1/2.
For 0<h<1/2, binary data processing and pi(A_h)<=h give

    b_h <= bar_b_K(h)
        :=1-exp(-(K+H_2(h))/(1-h))
         =b_K+O_K(h log(1/h)),       b_K=1-exp(-K),       (3.2)

where H_2(h)=-h log h-(1-h)log(1-h). The expansion is for the envelope,
not the actual b_h of every instance.

Let mu be any probability measure satisfying mu<=Aq, with A>=1. For B,R>e
put D={W<1/B}, E={W>R}, S=(D union E)^c, b=q(D), a=pi(E), d=mu(D).
For a test event F, let g=C^t 1_F, and let z=s_0^{-1} integral_{A_0}g dpi.

The accepted pointwise near-harmonicity lemma gives

    |g-Hg| <= eta_t=2^{-t} binom(t,floor(t/2)).           (3.3)

To recall why no initial L2 density is used, expand C^t in powers of H.
The coefficients of (I-H)C^t are successive binomial probability differences;
their positive and absolute negative sums both equal the maximum binomial
probability. Each H^j1_F is between zero and one. This proves (3.3) pointwise.

The IMH Dirichlet form is

    E_G(g,g)=(1/2) integral integral
       (g(x)-g(y))^2/max(W(x),W(y)) dpi(x)dpi(y).

Restrict its second leg to A_0 and apply Jensen to get
E_G(g,g)>=(s_0/2) integral (g-z)^2/max(W,M) dpi.
Reversibility and laziness put the spectrum of C in [0,1]. The variance of a
centered indicator is at most 1/4, and (1-x)x^{2t}<=1/(2t+1). Since
E_C >= (alpha/2) E_G, the spectral theorem gives

    integral (g-z)^2/max(W,M) dpi
         <=1/[alpha s_0(2t+1)].                         (3.4)

Write f=dmu/dpi; the measure bound implies 0<=f<=A/W. On S, below M use
W^{-2}<=B/W, and above M use max(W,M)=W. As integral W^{-1}dpi=1,

    integral_S max(W,M)(f-1)^2 dpi
       <= M(A^2 B+1)+A^2+R =: U_A.                     (3.5)

The multiplier for integral_S |g-z|dq is at most MB+1<=U_A. Therefore,
with Delta_A=sqrt(U_A/[alpha s_0(2t+1)]),

    |integral_S (g-z)(dmu-dpi)|<=Delta_A,
    integral_S |g-z|dq<=Delta_A,
    |q(g 1_{D^c})-(1-b)z|<=Delta_A+a/R.                 (3.6)

At x in D, all proposals in D^c accept, while a proposal in D leaves the
state in D even if it rejects. Consequently

    Gg(x)=b P_Dg(x)+q(g 1_{D^c}),                       (3.7)

for a Markov kernel P_D on D when b>0. Taking bounded suprema/infima over D
in (3.3), (3.6), and (3.7), and using 0<=Lg<=1, gives

    -kappa_b z-delta_A <= g(x)-z
                       <= kappa_b(1-z)+delta_A,
    kappa_b=beta/(1-alpha b),
    delta_A=[alpha(Delta_A+a/R)+eta_t]/(1-alpha b).       (3.8)

There is no attained-extremum assumption; null sets can be discarded with
equivalence and invariance. If b=0, the corresponding integral is zero.

Integrate (3.8) against +mu on D and the elementary range -z<=g-z<=1-z
against -pi on E. Their upper and absolute lower sums are each at most
max(kappa_b d,a)+delta_A d. The remaining -pi on D and +mu on E cost at
most b/B+A a/R. Include the core from (3.6) to obtain

    ||mu C^t-pi||_TV
       <= max(a,kappa_b d)+Delta_A+delta_A d+b/B+A a/R. (3.9)

This general-initial-law inequality is the earlier anchored bound with its
actual assumptions exposed. It does not assume that mu-pi has the same tail
signs as q-pi. The received binomial lemma and the previous principal's
signed-tail/anchor argument are dependencies, not newly claimed lemmas.

For the present construction, take mu=qC^s, A=c^s. If 1/B<h<1/2, (2.5)
and pi(D)<=b/B yield the usable finite-time bound

    d <= b_h theta_h^s + b S_s/(B h),                   (3.10)

clamped at one. Equations (3.1)--(3.3), (3.5), (3.8)--(3.10) give a numerical
certificate for the actual time s+t using only K, alpha, Lambda and proof
parameters s,t,B,R,h. Use s_0>=1/2, and the nondecreasing entropy envelopes
for b, b_h and a; no normalized W threshold is evaluated by the sampler.
One may use eta_t<=sqrt(2/(t+1)) for numerical evaluation.

## 4. Uniform upper asymptotics for the unchanged chain

Let n grow. For all sufficiently large n define

    kappa=-log(1-alpha exp(-K)/2)>0,
    s=ceil[2 log log n/kappa],       t=n-s,
    r=2 log c/kappa,                P=2r+6,
    h=(log n)^{-2},                 B=R=t/(log t)^P.    (4.1)

These are proof choices for a deterministic split of n steps of the same
kernel, not instructions to run a separate warm-up kernel. Eventually s<n/2,
t~n, B,R>e, and 1/B<h<1/2. Moreover

    A=c^s <= c(log n)^r,       S_s=O_c((log n)^r).        (4.2)

From (3.2),

    theta_h <= 1-alpha exp(-K)/2+O_{K,alpha}(h log(1/h)).

The logarithmic perturbation multiplied by s is
O_{K,alpha}((log log n)^2/(log n)^2)=o(1). Hence

    b_h theta_h^s=O_{K,alpha}((log n)^{-2}),
    d=O_{K,alpha,Lambda}((log n)^{-2})
       +O_{K,alpha,Lambda}((log n)^{P+r+2}/n)
     =O_{K,alpha,Lambda}((log n)^{-2}).                 (4.3)

Equations (3.5) and (4.2), with P=2r+6, give

    Delta_A=O_{K,alpha,Lambda}((log n)^{-3}),
    delta_A=O_{K,alpha,Lambda}((log n)^{-3}+n^{-1/2}),
    b/B+A a/R=o(1/log n).                              (4.4)

The denominator 1-alpha b is at least beta>0. Also kappa_b<=1. The high
target tail is the only leading term:

    a <= K/(log R-1) = (K+o(1))/log n.                 (4.5)

All O and o estimates above are uniform over the admitted class, with fixed
K, alpha, Lambda. Apply (3.9) to qC^{s+t}=qC^n. This proves

    limsup (log n) R_{K,alpha,Lambda}(n)<=K.             (4.6)

The polynomial-in-log density growth in (4.2) is essential. We have not
inserted a growing warm-up time into a theorem whose constants were only
controlled for a fixed time.

## 5. Matching lower bound and uniform inversion

For large n set

    p=K/[log n+2 log log n],
    u=exp(-K/p)=1/[n(log n)^2],
    pi=(p,1-p),          q=(pu,1-pu),          L=I.

All masses are strictly positive and p<1. Also qL=q<=Lambda q, and

    D(pi||q)=K+(1-p)log[(1-p)/(1-pu)]<K.                (5.1)

The nontrivial eigenvalue of G is 1-u. Direct two-state multiplication gives

    ||qC^n-pi||_TV=p(1-u)(1-alpha u/2)^n.               (5.2)

Since nu=1/(log n)^2 tends to zero, multiplying (5.2) by log n gives the
limit K. These are positive finite admitted instances; a singular limit is
not substituted for an admitted target. This proves the lower half of (1.2).

For clarity, (1.3) is concluded, not assumed from an informal inversion.
For every delta in (0,K), (1.2) supplies eventual uniform bounds between
(K-delta/2)/log n and (K+delta/2)/log n for R(n). At
n_+=ceil exp((K+delta)/epsilon), the upper bound is less than epsilon.
At n_-=floor exp((K-delta)/epsilon), the lower bound is greater than epsilon,
so some admitted instance still has TV>epsilon. Its TV is nonincreasing
under its fixed invariant kernel, so its first sufficient time exceeds n_-.
Consequently K-delta<=liminf epsilon log T<=limsup epsilon log T<=K+delta.
Let delta decrease to zero. This proves (1.3).

## 6. An honest implementation of the structural condition

Assume one can sample q and a fixed proposal Q(x,.) and evaluate the ratios
q(y)/q(x), Q(y,x)/Q(x,y) (or the appropriate Radon--Nikodym ratio). Values
of the positive unnormalized target p_tilde can be evaluated at proposed
points. None of its normalizing constant, the normalized W values, or
unseen target values is supplied for free.

On a selected local branch:

1. Draw y from Q(x,.).
2. Accept stage one with a_1=min(1,q(y)Q(y,x)/(q(x)Q(x,y))).
   If it rejects, remain at x without a new target evaluation.
3. If stage one passes, evaluate p_tilde(y) when not already the current
   state, and accept stage two with
   a_2=min(1,[p_tilde(y)/q(y)]/[p_tilde(x)/q(x)]).

Use independent uniforms for the two stages and cache current-state values.
The resulting off-diagonal pi-flow is proportional to

    min(q(x)Q(x,y),q(y)Q(y,x)) min(W(x),W(y)),            (6.1)

which is symmetric. Its first-stage kernel R preserves q, so the accepted
incoming q-mass argument proves qL<=2q. Multiplying p_tilde by any common
positive constant changes no transition. The mixture selection probabilities
stay fixed; a target evaluation on the local branch is an ordinary part of
this changed sampler, not a secretly free prefix observation.

The old unrestricted hybrid trap family does not satisfy a uniform finite
Lambda. In its low entrance B and rare trap A, q(B) stays positive, the
ordinary local acceptance B->A stays positive, and q(A) tends to zero.
Thus qL(A)/q(A) diverges. In the safeguarded operation, first-stage
q-reversibility suppresses that particular capture. The theorem proves the
full uniform result, beyond this illustration.

## 7. Cost, comparison, and limits

The construction is standard delayed acceptance, so its ordinary local MH
competitor accepts at least as often per identical Q proposal:

    min(1,a) min(1,b) <= min(1,ab).

Here a is the q-stage ratio and b is the W ratio. This ordering does not
establish finite-time TV ordering from q. With one equally priced proposal,
the extra rejection can hurt efficiency; a cheap first-stage calculation may
save expensive target evaluations, but that requires an actual cost model.

At n mixture steps, there are exactly one initial q candidate, expected
alpha n/2 further global candidates, and expected beta n/2 local Q proposals.
Each global proposal requires at most one new target evaluation. Each local
proposal needs a new target evaluation only if stage one passes and it is
not the currently cached state. q-density and proposal-ratio work, uniform
draws, bookkeeping and memory must also be counted. The theorem does not
price these operations. It does not make access to q evaluations cheap or
possible in settings where q is only sampleable.

Pure IMH already matches the exponent K without local work. No application,
wall-clock speedup, lower target-evaluation count at a fixed accuracy, or
finite-time dominance follows from Theorem 1. The accompanying finite-chain
calculations are mechanism and cost diagnostics, not a downstream scientific
adoption test or a measured run of exponentially many transitions.

The exact-real kernel is separate from floating-point code. Finite-precision
ratios, approximate q evaluation, approximate local kernels and invalid
population KL certificates are not covered without additional error analysis.
The condition qL<=Lambda q must be proved structurally or certified; observing
it on finitely many trajectories cannot establish it over an unknown space.

## 8. Status and next boundary

The supplied candidate-only stopping obstruction is accepted and retained
unchanged. The preceding fixed-prefix conclusions, joint-KL theorem and pure
IMH benchmark stay closed. This continuation changes the local-kernel class
explicitly; it does not contradict those results or claim an adaptive prefix.

The first-hit construction, uniform growing-s upper bridge and sharp theorem
above are the principal's new argument. Independent contributors challenge
the first-hit measures and domination condition, the finite-cost comparison,
and the primary-literature boundary. Their actual reports and exact source
bindings are included separately. Review outcomes are not external acceptance.

The next question will be chosen after the finite calculations and literature
checks. A useful direction is a *quantitative tradeoff* between how strongly a
local move is safeguarded and its robustness: can a weaker, scale-free
acceptance control retain the K coefficient, or does its worst-case tail
introduce a provable additional cost? This is an unresolved direction here,
not a claim established by the proof above.
