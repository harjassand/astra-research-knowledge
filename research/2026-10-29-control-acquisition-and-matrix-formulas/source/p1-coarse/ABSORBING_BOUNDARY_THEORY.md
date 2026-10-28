# Finite boundary certification without a global contraction gap

28 October 2026. The new construction removes the previous externally
warranted strict source norm cap. It replaces that premise with a stronger
observation interface: irreversible absorption is distinguished from a live
hidden excursion. The executed source has infinitely many reachable slow
states and norm exactly one. No hidden rank is assumed.

Classical first-return and Schur-complement algebra are established ingredients.
The addition developed here is finite statistical acquisition of the local
source forms needed to certify all subsequent switched programs, with an
estimated boundary model, observation uncertainty and complete source costs.

## Source and interface

Every primitive is a symmetric substochastic kernel A_i on one finite or
countable live-state space. It is a selfadjoint contraction on counting-measure
l2. Cemetery is excluded from the live operator. The learner prepares a finite
set of actual boundary states and nonintrusively observes a boundary-state
label, alive outside, or irreversibly absorbed. No outside identity is revealed.

Irreversibility and sensor accuracy are access premises, not facts established
by a finite run. A coarse label merging distinct boundary states cannot
justify reset-state reuse. This access does not follow from a scalar endpoint
oracle and does not automatically transfer to quantum intermediate measurements.
The structural norm bound <=1 remains; no strict cap a<1 is supplied.

Let V embed the boundary coordinates. Partition one primitive as

    A = [ T  C* ] ,  T=V*AV,  D=AV-VT=[0;C].
        [ C   B ]

T is the true boundary compression; T_hat is the estimated model. The hidden
restriction B is not supplied to the learner. Define first-return matrices

    F_l=C*B^(l-2)C, l>=2,
    K_+=sum F_l,  K_-=sum (-1)^l F_l,  E=(K_++K_-)/2.

Their entries are path probabilities or signed sums thereof. K_+ and E are
entrywise nonnegative and symmetric. K_+, K_-, and E are positive semidefinite,
although an individual odd-time F_l need not be. The entries converge
absolutely because total first-return probability is at most one.

Put H_+=I-T-K_+, H_-=I+T-K_-. When these finite Schur matrices have positive
lower bounds, the local source forms are

    M=V*(I-A^2)^(-1)V = [H_+^(-1)+H_-^(-1)]/2,
    Q=D*(I-A^2)^(-1)D
      =E+[K_+H_+^(-1)K_+ + K_-H_-^(-1)K_-]/2.             (1)

Here the full-space inverse denotes a quadratic form. It need not be a bounded
operator. Apply block inversion to zA, 0<z<1, and pass to z increasing to one:
entrywise first-return convergence gives convergence of the finite Schur
matrices; their strict positivity bounds the boundary resolvents. Spectral
monotone convergence then establishes finite M and Q and their required
bounded inverse-square-root factorizations. No pseudoinverse erases an
uncontrolled kernel component. A separate scoped review in branches/physical
gives the full Abel/form argument and model-transfer proof.

## Finite censored observations supply the bounds

For each primitive and each boundary start, stop at the first boundary return,
observed absorption, or a fixed censor time H. Observe after every executed
step. Time-one boundary transitions end immediately. Three indicators suffice:

1. excursion return observed, or still alive outside at H;
2. even-time excursion return observed, or still alive outside at H;
3. absorption observed before any boundary return.

Denote their probabilities by u_j,e_j,a_j. Every unobserved future return
requires the trajectory to remain unresolved and alive at H. Therefore

    row_j(K_+)<=u_j,  row_j(E)<=e_j,
    row_j(T+K_+)<=1-a_j.                                  (2)

All possible later return mass is charged now; no relaxation-time estimate is
needed. Acquired simultaneous bounds u_j^U,e_j^U,a_j^L and T_jj^L imply

    H_+>=kappa_+ I, kappa_+=min_j a_j^L,
    H_->=kappa_- I, kappa_-=min_j(2T_jj^L+a_j^L).          (3)

For the second inequality, |K_-|<=K_+ entrywise yields Gershgorin margin
at least 1+2T_jj-row_j(T+K_+). The implementation also improves kappa_+
using one minus acquired upper row masses of T and K_+. It emits only with
positive margins. It does not promise every source will yield them cheaply.

Set u=max u_j^U, e=max e_j^U and m=(1/kappa_++1/kappa_-)/2.
Symmetric row-sum and entrywise-domination bounds give

    M<=mI,  Q<=qI,  q=e+mu^2.                              (4)

This acquires a local inverse-dissipation upper bound without reconstructing
the source or certifying a global spectral gap.

## Estimated maps and all future words

Pool opposite boundary-transition counts using source symmetry. Fixed-sample
Chernoff intervals enclose T; their empirical centers define T_hat. If
||T-T_hat||<=delta, Minkowski in the acquired local form gives

    D_hat=AV-VT_hat=D+V(T-T_hat),
    D_hat*(I-A^2)^(-1)D_hat <= (sqrt(q)+delta sqrt(m))^2 I.

Accept theta only after exact rational verification that the last upper
bound is <=theta^2 R, where R=I-T_hat*T_hat is positive definite.

The same categorical counts also bound row-sum errors rho_j and off-diagonal
entry errors r_jk. For symmetric Z=T-T_hat,

    Z=diag(Z1)-sum_(j<k) Z_jk (e_j-e_k)(e_j-e_k)*.

Thus U=diag(rho_j)+sum r_jk(e_j-e_k)(e_j-e_k)* bounds its bilinear form by
|x*Zy|<=sqrt(x*Ux)sqrt(y*Uy). Verify U<=zeta R exactly. The already proved
second-order energy certificate and two telescoping energy sums now imply

    |y*V*A_w Vx-y*T_hat_w x|
       <= [2 max_i theta_i^2+max_i zeta_i] ||x|| ||y||       (5)

for every finite word w. A single confidence event covers all words, including
ones selected after acquisition. It does not cover a new within-run feedback
policy conditioned on intermediate outcomes.

Floating point only proposes confidence and semidefinite endpoints; rational
logarithm enclosures and principal-minor checks accept them. This is a
frequentist false-emission bound, not a probability conditional on emission.

For nonnegative endpoints a stronger existing computational route retains T
as an interval variable. Its Galerkin weak defect vanishes. An acquired
boundary row cap rho_T<1 gives dynamic remainder 2 max q/(1-rho_T^2).
Positive matrix interval propagation encloses T_w; hidden paths only add
nonnegative probabilities. This route beats the corrected point model on
the executed example, while using the same acquired physical residual form.

## Infinite reachable source and executed acquisition

The three boundary states and two noncommuting boundary kernels are those in
the preceding multi-boundary experiment; each boundary row sums to .98.
Boundary j couples to a fast hidden state by .002, with fast diagonal
1/4,1/3,2/5 respectively. It also couples to every slow state (j,n), n>=0:

    w_n=2^(-21-n),  eta_n=2^(-10-n).

That slow state stays with probability 1-eta_n, returns to j with probability
w_n, and is absorbed with probability eta_n-w_n. Total slow entry mass per
boundary is 2^-20. All slow states are reachable with positive probability.
The learner receives none of these hidden details.

Symmetry and substochasticity imply contraction. Slow basis-state diagonal
expectations tend to one, proving norm exactly one. Every row has strictly
positive absorption. The Dirichlet form of I-A therefore has no nonzero
kernel. This is not a finite source padded by an unreachable invariant block.

The implementation executed two million trials for each of six action/start
pairs, with censor time H=32. Integer transition draws and an untruncated
geometric bit sampler implement the countable source. The six return-or-pending
counts are 9,19,15,13,9,13. The acquired point-model bound is

    uniform absolute error <= .0399059846.

The stronger true-Galerkin dynamic remainder is <=.001112504539, before
adding a word's parameter-interval uncertainty. For transport 0 to 2 compare
ten operations 0 followed by ten operations 1 with the reverse block order:

    f(0^10 1^10)-f(1^10 0^10) in [.1080212656,.1337115038].

Here word notation is chronological. Neither program was used in acquisition.
The corrected point-model route also resolves the sign, with interval
[.0855606224,.1558500901]. Exact finite truncation plus an explicit bound on
omitted branch-entry probability checks actual infinite-source probabilities
for these and seven other programs, including 100-step words. The ordinary
theorem, not those finite checks, establishes the all-word claim.

| Resource | Reusable acquisition | Fresh direct test of the two words |
|---|---:|---:|
| Logical trials | 12,000,000 | 20,000 |
| Primitive steps | 12,036,469 | 400,000 |
| Categorical observations | 12,036,469 | 20,000 |
| Preparations with exact boundary reuse | 1,758,723 | 13,715 |
| Certified transport difference | [.1080213,.1337116] | [.0867624,.1476626] |

The direct comparator uses the same infinite source and boundary interface,
with endpoint-only readings and every scheduled primitive step charged. It
answers this one pair much more cheaply. It does not acquire an all-word
reusable certificate. No laboratory operation or sensor calibration occurred;
these are executed software trajectory experiments and resource ledgers.
The direct execution reports 13,715 preparations; its receipt omits the last
boundary bit, so counts alone independently certify the upper 13,717. The
acquisition preparation ledger is independently exact.

A trial ending at its requested start state supplies the next initial state
without preparation. Strong Markov restart preserves the trial law. The
exact ledger charges an initial preparation, then a preparation only when
the preceding terminal state differs from the requested start. Hidden backend
shortcuts never reduce unobserved source time. During acquisition, observed
absorption legitimately stops the trajectory because it is an interface report.

There are 54 retained one-sided acquisition tails and four for the fresh direct
comparator. Exponent 12 gives total failure below .001. Raw counts and exact
witnesses are in results/ABSORBING_BOUNDARY_RESULTS.json. A missing reporting
key after the first acquisition was fixed by replaying the saved counts;
the acquisition was not resampled.

Future predictions require no new source trials. A length-h prediction on r
boundary states uses O(h r^2) arithmetic operations; rational bit lengths
still grow with h. This count is not a constant-bit-cost runtime promise.
Searching all useful words remains a separate computational problem.

## Consequence, limits, and antecedents

The slowest hidden relaxation time can be infinite while the local source
forms needed for a useful boundary representation are small and finitely
certifiable. The measurable object is unresolved excursion return mass,
together with observed irreversible loss. This is stronger than merely
assuming a global spectral gap and fitting a low-dimensional response.

There is no universal finite-cost guarantee. Many unresolved live excursions,
little observed loss, a poor boundary representation, or an inaccurate sensor
can prevent useful certification. The retained-rate calibration lower bound
in branches/scalar/CALIBRATION_COST_THEOREM_REVIEW.md still applies, even with
fully visible absorption and zero hidden residual. A source-form certificate
does not acquire numerical precision for free.

First-return generating functions and stochastic complementation are classical.
Carl D. Meyer, *Stochastic Complementation, Uncoupling Markov Chains, and the
Theory of Nearly Reducible Systems*, SIAM Review 31 (1989), 240-272,
DOI 10.1137/1031050, develops that boundary elimination machinery. This work
uses it for finite source-form acquisition and subsequent arbitrary switching;
it does not claim first discovery of the Schur identities. The original scalar
acquisition, energy theorem and familiar interval methods remain useful
components of this stronger construction.

ABSORBING_BOUNDARY_EXTENSIONS.md proves the complete g^-3 calibration rate
under observable conditions, constructs a norm-one family where this weighted
certificate vanishes while the unweighted bound stays at least 1/4, and
quantifies sensitivity to a bounded loss-sensor error. These refinements do
not change the frozen main acquisition or its scoped independent review.
