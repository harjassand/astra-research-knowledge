# Independent challenge of the tempered local screen

Contributor: `/root/safeguarded_mh_mechanism`.
Scientific date: 22 October 2026, Australia/Brisbane.

This is a distinct review of the proposed tempered-screen extension. It
does not alter the already bound `SAFE_LOCAL_THEOREM.md`. The actual final
source binding, if completed, is recorded separately.

## Outcome after actual-source review

The load-bearing construction and actual final source are valid under their
stated finite positive-space, symmetric-Q, fixed-eta contract. The review
below independently checks the setwise power-domination propagation,
first-hit submeasures, density truncation and growing-time parameters.
No numerical diagnostic is needed for these exact inequalities, and none
was run for this extension.

## 1. Structural setwise bound

Let q and pi be positive probability vectors on a finite labelled space,
let Q be a fixed symmetric stochastic matrix, and let 0<eta<1 be fixed.
The two-stage product accepts Q(x,y) with probability

    min(1,(q(y)/q(x))^eta)
      min(1,(pi(y)/pi(x))(q(x)/q(y))^eta).

The product of the two stage ratios is pi(y)/pi(x), so the usual
delayed-acceptance detailed-balance calculation applies. Its accepted
incoming q-mass in a subset A is at most

    sum_{x,y in A on the y leg} Q(x,y) q(x)^(1-eta) q(y)^eta.

Holder's inequality bounds this by

    [sum_{x,y: y in A} Q(x,y) q(x)]^(1-eta)
      [sum_{x,y: y in A} Q(x,y) q(y)]^eta
    <= q(A)^eta.

The second bracket equals q(A), because symmetric stochastic Q has
column sums one. The first bracket is at most one. Rejected q-mass in A
is at most q(A). Consequently

    (qL_eta)(A) <= q(A)+q(A)^eta.

Since qG<=2q and q(A)<=q(A)^eta,

    (qC)(A) <= (3/2) q(A)^eta.                         (T1)

This is a *setwise scalar bound*: A maps to q(A)^eta is not a measure.
It must not be propagated by ordinary linear measure arithmetic.

## 2. The correct power propagation lemma

Suppose finite measures mu,nu satisfy, for all measurable A,

    mu(A)<=D nu(A)^r,          0<r<=1.

For a measurable 0<=f<=1, layer cake and Jensen on the unit interval give

    integral f dmu
      <=D integral_0^1 [nu(f>v)]^r dv
      <=D [integral_0^1 nu(f>v)dv]^r
      =D (integral f dnu)^r.                           (T2)

Applying this to f=P1_A for a probability kernel P gives the desired
propagation. In particular, iterating (T1) yields

    (qC^j)(A)<=D_j q(A)^{r_j},
    r_j=eta^j,
    D_j=(3/2)^[(1-eta^j)/(1-eta)]<=D_*=(3/2)^[1/(1-eta)].

The recursion is D_{j+1}=D_j (3/2)^{r_j}; it does not multiply D_j
by 3/2 at every step without the exponent.

## 3. First-hit submeasures survive propagation

Let tau be the first state with normalized W>=h. As in the main theorem,
the no-hit probability through s is at most b_h theta_h^s, with
theta_h=1-alpha(1-b_h)/2. The time-j first-hit submeasure satisfies

    nu_j(A)<=D_j [pi(A)/h]^{r_j}.

Use (T2) with the reference probability measure pi, and then pi C=pi,
to propagate nu_j for s-j further steps. If D is below threshold and
pi(D)/h<=1, then r_j>=r_s, D_j<=D_*, and hence

    (qC^s)(D)
      <=b_h theta_h^s+(s+1)D_*[pi(D)/h]^{r_s}.         (T3)

All terms are unconditioned submeasures. No stopped-output law is
substituted for a deterministic-time law. Returns below h after the
first hit remain included.

## 4. Density truncation and its complete error charge

Power domination implies mu_s=qC^s is absolutely continuous with
respect to q. Let f_s=dmu_s/dq. For a cutoff V>=1, define

    E={f_s>V},    delta=mu_s(E),
    tilde_mu=1_{E^c}mu_s+delta q.

Since q(E)<=1/V, power domination gives

    delta<=D_s V^{-r_s},
    ||mu_s-tilde_mu||_TV<=delta,
    tilde_mu<=(V+1)q,
    tilde_mu(D)<=mu_s(D)+delta q(D).                  (T4)

The last term must be retained when applying the main theorem's
generalized initial-law bound. It is harmless in the stated asymptotics,
but omitting it from the stopped/perturbed law would be an error. This
is an analytical comparison measure, not an implemented reset of the
sampler. Contraction bounds the final discrepancy by delta.

## 5. Uniform convergence for every fixed eta>0

For any desired intermediate tolerance, choose fixed h in (0,1/2),
then fixed s large enough that the uniform no-hit bound is small.
The entropy envelope gives b_h<=bar_b_K(h)<1, so this is possible.
Next choose a fixed finite V large enough to make D_s V^{-r_s}
small; r_s is positive for every fixed eta>0. Apply the inherited
finite-time initial-law inequality to tilde_mu with A=V+1. As t grows,
choose B=R=t/(log t)^4. The hit contribution in (T3) tends to zero,
as do the high tail, core and perturbation terms. Finally send the
intermediate tolerance to zero.

All choices depend only on fixed K, alpha, eta and the desired error,
not the particular finite target or support size. This proves uniform
convergence, but supplies no sharp coefficient below the separately
proved near-one eta regime.

## 6. Sharp-coefficient parameter check

Let

    theta_K=1-alpha exp(-K)/2,
    kappa=-log(theta_K),      lambda=-log(eta).

When eta>theta_K, lambda<kappa. Choose a_time strictly between
1/kappa and 1/lambda. Put

    s=ceil(a_time log log n),
    a=a_time lambda<1,
    b=(1+a)/2 in (a,1),
    h=(log n)^(-2),
    V=exp((log n)^b),
    A=V+1,
    t=n-s,
    B=t/[A^2(log t)^6],       R=t/(log t)^6.

The symbol V here is the density cutoff and must not be confused with
the fixed anchor M=exp(2K+1) from the main theorem. Then

    r_s>=eta(log n)^(-a),
    delta<=D_* exp[-eta(log n)^(b-a)]=o(1/log n).

The no-hit contribution is O((log n)^(-a_time kappa))=o(1/log n).
Moreover

    log[1/(Bh)]= -log n+2(log n)^b+O(log log n)
               <=-(1/2)log n

eventually. Thus the hit term in (T3) is at most a fixed constant times

    (s+1) exp[-(eta/2)(log n)^(1-a)],

also o(1/log n). The replacement term delta q(D) in (T4) is charged.
For the inherited core multiplier,

    A^2B/t=(log t)^(-6),
    A^2/t=exp(2(log n)^b-log n+o(1)),
    R/t=(log t)^(-6),

so Delta_A=O((log n)^(-3)). All remaining tail/core terms are lower
order. Both log B and log R are asymptotic to log n, leaving the high
tail coefficient K. The admissible Q=I two-state family supplies the
matching lower coefficient. The threshold eta>theta_K is sufficient;
this argument does not establish its necessity.

## 7. Optional quantitative consequence of the same estimates

For any fixed eta in (0,1) and any

    0<z<min(1,kappa/lambda),

choose a_time=z/kappa<1/lambda and use the same construction. The
no-hit term is O((log n)^(-z)), while all other terms except K/log n
are smaller. Thus the same calculation also provides the nonsharp
uniform rate O((log n)^(-z)). This is an optional corollary, not a
claim that the exponent z or the threshold eta>theta_K is sharp.

## Review limits and resources

The argument is mathematical and ideal-real. It does not establish a
wall-clock advantage, an empirical KL certificate, historical novelty,
or an exact floating-point implementation. The main proof and its
existing diagnostic receipts remain unchanged. No scientific script
was executed for this extension; review time includes direct inspection,
symbolic checking and communication with the root. No external spending
or intervention occurred.
