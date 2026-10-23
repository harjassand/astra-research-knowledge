# Independent check: proposal-reversible local safeguard

Contributor: `/root/safeguarded_mh_mechanism`. First observed clock:
2026-10-21 16:10:00 UTC (22 October 2026 in Brisbane).

## Scope and outcome

I explored the root's proposed local-kernel change, then independently checked
the load-bearing one-step domination and first-hit argument that the root
supplied. I did not re-review the received optional-prefix impossibility.

**Outcome:** the first-hit argument is valid under the stated fixed-kernel
measure domination. It gives a route to removing the forward-KL cold-start
floor without an operational prefix. The general condition is a fixed,
uniform bound `q L <= Lambda q`, together with the original target
reversibility of L. A q-reversible local proposal followed by the usual
importance-weight MH acceptance supplies Lambda=2. The numerical checks
below supplement, and do not prove, these measure statements.

The tempting stronger auxiliary assertion `q L^t <= (t+1)q` is false. An
exact rational counterexample is retained below. None of the accepted
argument uses it.

## 1. One-step domination, including arbitrary measurable spaces

Let R be a q-reversible Markov proposal and let W=dpi/dq be positive and
finite q-almost everywhere. Define L by proposing R(x,dy), accepting with
`a(x,y)=min(1,W(y)/W(x))`, and otherwise retaining x. Standard pairwise
symmetry gives pi-reversibility: the off-diagonal flow is

    q(dx) R(x,dy) min(W(x), W(y)).

For every measurable A, the total accepted incoming mass satisfies

    integral q(dx) integral_A R(x,dy) a(x,y) <= (qR)(A)=q(A).

The rejected mass left in A is at most q(A). Hence

    qL(A) <= 2 q(A).

This needs only q-invariance of R for the domination step; q-reversibility
is what justifies the displayed acceptance formula and pi-reversibility.
No conditional density, disintegration, or finite-state representation is
required. The same argument with R(x,dy)=q(dy) gives qG<=2q.

For C=(I+alpha G+beta L)/2, beta=1-alpha, this yields

    qC <= (3/2)q,       qC^j <= (3/2)^j q.

More generally, if pi-reversible L satisfies qL<=Lambda q uniformly in
the admitted class, then

    qC <= c q,   c=(1+2alpha+beta Lambda)/2,
    qC^j <= c^j q.

Since integration of qL<=Lambda q implies Lambda>=1, this c is strictly
greater than one for fixed alpha>0. Iteration uses positivity of Markov
kernels, not a claim that q is invariant under C.

## 2. Exact first-hit decomposition

Fix h>0 and integer s>=0. Let X_0~q evolve under this fixed C, and put

    tau = inf{j>=0 : W(X_j)>=h},
    b_h = q(W<h),
    theta_h = 1-alpha(1-b_h)/2.

Whenever the current state has W<h, a global proposal in {W>=h} is
certainly accepted. Thus the probability of remaining below h for the
next C step, conditionally on the entire past, is at most theta_h. It
follows that

    P(tau>s) <= b_h theta_h^s.                         (R1)

Define the subprobability measure

    nu_j(A)=P(tau=j, X_j in A),       0<=j<=s.

This measure is supported on {W>=h}, and

    nu_j <= (qC^j)|_{W>=h} <= c^j q|_{W>=h}
         <= (c^j/h) pi.                              (R2)

The first inequality is a subevent inequality. It does not condition
the qC^j law on tau=j and then assume that conditioning preserves
domination. This distinction is essential.

Let nu_nohit be the law at time s restricted to {tau>s}. Strong Markov
at these bounded deterministic-index events gives the exact decomposition

    qC^s = nu_nohit + sum_{j=0}^s nu_j C^{s-j}.       (R3)

All continuation kernels are the same fixed C. Since pi C^k=pi, (R2)
survives propagation. For D subset {W<h},

    (qC^s)(D)
      <= b_h theta_h^s + [pi(D)/h] sum_{j=0}^s c^j.  (R4)

The j=s term is zero on D and can be dropped; keeping it is a harmless
upper bound. Independently, qC^s<=c^s q. These two inequalities are
exactly the hypotheses needed to replace the old deterministic-prefix
density bound in the inherited anchored smoothing argument. There is
no random stopping output: the actual sampler runs C for a deterministic
total number of steps. The first-hit time is only an analysis device.

## 3. Uniform asymptotic bridge checked

Write

    theta_0 = 1-alpha exp(-K)/2,
    kappa = -log(theta_0)>0,
    s = ceil[2 log log n / kappa],
    h = (log n)^(-2),
    A = c^s,
    d0 = 2 log(c)/kappa,
    t = n-s,
    B = R = t/(log t)^P,

where P is any fixed number larger than 2d0+4. These are proof choices,
not observables or thresholds the algorithm must evaluate. For large n,
0<h<1/2, 1/B<h, and t is positive.

The inherited forward-KL envelope is

    b_h <= bar_b_K(h) = b_K + O_K(h log(1/h)),
    b_K = 1-exp(-K).

Consequently theta_h <= theta_0+O(h log(1/h)). The correction in the
exponent is s O(h log(1/h))=o(1). Thus (R1) is uniformly
O((log n)^(-2)), and A<=c(log n)^d0. The second term in (R4), with
D={W<1/B}, is at most

    [1/(Bh)] sum_{j=0}^s c^j
      <= [c/(c-1)] A/(Bh)
      = O(n^(-1) (log n)^(P+d0+2)).

This is smaller than every fixed inverse power of log n. Therefore the
low-set mass is O((log n)^(-2)). The generalized core multiplier is

    U_A = M(A^2 B+1)+A^2+R,
    Delta_A = sqrt[U_A/(alpha s0(2t+1))].

Its order is O((log n)^(d0-P/2)), which is o((log n)^(-2)) under the
stated P. The remaining terms in the inherited finite-time bound are
also o(1/log n). The high tail obeys

    pi(W>R) <= K/(log R-1),
    log R = log n - P log log n + o(1),

so its coefficient tends to K. This verifies the root's uniform upper
bridge; the logarithmic exponents are fixed once K, alpha and Lambda
are fixed. It would not be valid to let Lambda grow uncontrolled with n.

The lower comparator is admissible: R=I gives L=I and
C=(1-alpha/2)I+(alpha/2)G. The ordinary two-state IMH lower family
therefore retains the coefficient K. A complete statement of the lower
limit and mixing-time inversion belongs in the root's principal proof.

## 4. Exact finite diagnostic

`check_safeguarded_mechanism.py` uses only standard-library rational
arithmetic. It constructs 15 positive finite pairs, q-reversible
proposals, and MH corrections. It checks 250 exact first-hit
decompositions and 6,740 scalar inequalities, covering (R1)--(R4), the
one-step domination and its iterates. All passed on the first recorded
execution. These are implementation diagnostics, not a proof of
arbitrary measurable-space claims.

The same script retains this exact rational counterexample:

    q=(99/100, 1/2000, 19/2000),
    raw W=(1,2200,17),

    R = [[98849/99000, 13/99000, 23/16500],
         [13/50,       6/25,       1/2],
         [69/475,      1/38,   787/950]].

R is q-reversible. With L=MH(R,W), at t=12 the middle state's density
ratio is

    (qL^12)(1)/q(1) = 13.06223283030371... > 13.

The exact fraction is in `safeguarded_mechanism_checks.json`. The
normalized target is (660/1501,2200/4503,17/237), with rounded forward
KL 3.1517157346862703. This refutes the unrestricted proposed linear
bound while respecting a fixed finite forward-KL budget (for example
K=4). The correct exponential domination c^s is sufficient because
the proof spends only O(log log n) early steps.

An initial float search found a nearby three-state counterexample at
t=6. The displayed rational example was then chosen and verified
exactly; it is not a pristine holdout or a simulated scientific
measurement. No trajectories or old mixing diagnostics were rerun.

## 5. Operational and scientific limits

For evaluable q and a target-independent local proposal Q with known
Hastings ratio, R=MH(Q,q) is q-reversible. Correcting its proposals
again by min(1,W(y)/W(x)) is the standard two-stage delayed-acceptance
construction. The target normalizer cancels. A first-stage rejection
can avoid the new target evaluation. This is a structural route to
the hypothesis, not a learned estimate of qL<=2q.

Ordinary single-stage MH with Q accepts at least as often as the
two-stage product. Therefore the new guarantee does not establish
better stationary variance or a finite-time speedup; the original
counterexamples already show why an ordering of accepted moves does
not imply proposal-start TV dominance. Pure IMH already has exponent
K. The old deterministic N_safe prefix is still a relevant comparator
for an unrestricted local kernel.

The new hypothesis is a restriction on local-kernel construction, not
a claim that all reversible local kernels are safe. It requires exact
q access adequate to implement the declared proposal correction.
An actual application must price q evaluations, Q proposals, target
evaluations, acceptance operations and the local kernel's lost moves.
No end-to-end wall-clock advantage is established by this review.

## Observed resources

The saved exact script reports wall 0.23954809000133537 seconds, CPU
0.239530683 seconds and peak RSS 9,472 KiB for its first recorded run.
These are diagnostic execution costs, not total proof-discovery costs.
The unmetered conceptual work includes the initial failed linear-bound
search, root/contributor exchanges, and verification of the first-hit
and scaling steps. No hardware expenditure or external intervention
was used.
