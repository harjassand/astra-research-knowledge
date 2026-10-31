# A stronger two-rate frontend: acquired leverage, not an entrywise straw man

Working proof, 31 October 2026. Not independently reviewed or in the frozen
checkpoint. This sharpens the preliminary entrywise discussion in
QUESTION_AND_FIRST_LEMMA.md. It uses established matrix concentration rather
than claiming it as a new probabilistic ingredient.

## Shared access and comparison

There are m unknown row-stochastic n-by-n matrices. A row-generative query
returns an independent next-state label from a named row. All methods can
retain every observation. The coarse phase uses uniformly selected rows; the
fine phase uses an acquired distribution h. Source queries, selecting row
labels, all retained counts, matrix/basis work, failed candidates and bits are
paid. No reverse sampler, exact stationary law, good features, gap or probes
are supplied.

The comparison is NOT against weak entrywise estimation alone. A full-operator
spectral estimator gets the same matrix-Bernstein tool, the same learned
geometry and the best appropriate downstream error analysis. Selective
goal-oriented methods may already implement this precision allocation; exact
prior matching remains open. The result sought is a certificate-level
acquisition benefit, not exclusive ownership by a new learner.

We use the rectangular matrix Bernstein inequality, Theorem 1.6 of Tropp:
independent centered matrices Z with norm at most R and one-sample left/right
variance norm at most v obey

    Pr(||average Z|| >= t)
       <= (d1+d2) exp[-N*t^2/(2*v+(2/3)*R*t)].

Primary statement: https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf .
The following moment bounds and staged protocol are derived for this access
interface. Replacing a logarithm by its ceiling base-two logarithm gives a
conservative rational sample schedule because ln(2)<1.

## 1. Acquire an incoming-mass bound before using it as a variance parameter

For each generator, take N0 independent pairs with I uniform on [n] and
J drawn from A(I,.). Write q_j=Pr(J=j)=sum_i A_ij/n, and let X_j count J=j.
With K0=ceil(log2(2*m*n/delta0)), the simultaneous statement

    q_j <= (2*X_j+8*K0)/N0

fails with probability at most delta0/2. To see this, if N0*q_j<=8*K0 the
inequality is automatic. Otherwise its failure implies X_j<N0*q_j/2, whose
Chernoff probability is at most exp(-N0*q_j/8)<=exp(-K0). Union over m*n.

Thus acquire

    B = min(n, max(1, max_(a,j) n*(2*X_(a,j)+8*K0)/N0)).

On that event, every column sum of every generator is <=B. It is not an input
promise. If desired choose N0=n*K0. A matching upper-tail Chernoff argument
gives X_j<=2*N0*q_j+2*K0 simultaneously with another failure delta0/2;
therefore B<=4*B_true+12 on the combined event, up to the explicit cap n.
The upper-tail claim follows directly from the Bernoulli mgf at log(2).
No assertion of a small B is made when the acquired value is large.

## 2. Coarse full-operator spectral data

Use a fresh batch for each generator and the random matrix

    Y = n*e_I*e_J^T,    E[Y]=A.

For Z=Y-A, its norm is <=2n, because ||A||_2<=sqrt(B)<=sqrt(n)<=n. Also

    E[Z Z^T] <= n I,
    E[Z^T Z] <= n*diag(column_sums(A)) <= n B I.

These are PSD inequalities; subtracting the mean outer products only helps.
Consequently a sufficient common batch size is

    Ncoarse >= Kc*[2*n*B+(4/3)*n*t]/t^2,
    Kc=ceil(log2(2*m*n/deltac)).

Let Chat be the average. On the acquired event, ||Chat_a-A_a||_2<=t for all a.
The raw Chat need not be stochastic. This is harmless: only TRUE A is used
for the stochastic boundedness theorem. Any normalized center or stationary
solve used to propose h is only a proposal, never the unknown truth.

After seeing Chat, choose any positive rational h, H=diag(h). Then

    ||Chat_a-A_a||_H <= sqrt(kappa_h)*t,
    kappa_h=max h_i/min h_i.

This is deterministic for every h on the same spectral event, so fitting h
on those data creates no independence loophole. The actual kappa_h is checked.
An automatic geometric-precision schedule with summable failure allocations
can refine until the coarse certificate passes, paying every failed round.
No efficient complete search for the best h or task space is presumed.

## 3. Fine projected sampling and the acquired leverage bound

Lock the acquired h and rational full-rank V before taking fresh fine data.
Let G=V^T H V. For analysis put W=V G^(-1/2), so W^T H W=I. The irrational
square root is NOT an implementation requirement: the actual projected
estimate is Khat=G^-1 V^T Phat V, where Phat_ij counts pairs (i,j)/N and
I is sampled from h before drawing J from the true row A(I,.).

Acquire the rational maximum leverage

    Lambda = max_i V[i,:] G^-1 V[i,:]^T
           = max_i ||W[i,:]||_2^2 >= r.

This is stronger than bounding each entry and union-bounding r^2 estimates.
For Y=W[I,:]^T W[J,:], its expectation is the orthonormal-coordinate
projection Ktilde, and ||Y||<=Lambda. The moment bounds are

    E[Y Y^T] <= Lambda I,
    E[Y^T Y] <= Lambda*kappa_h*B I.

For the second inequality, use (A^T h)_j/h_j<=kappa_h*B, which follows from
the acquired incoming-mass bound. The first uses E_h W[I,:]^T W[I,:]=I.
Both are valid even when h is not invariant. Centering subtracts PSD mean
outer products.

If the coarse geometry lemma supplies ||A||_H<=beta, then
||Y-Ktilde||<=Lambda+beta. Thus a sufficient fine batch per generator is

    Nfine >= Kf*[2*Lambda*kappa_h*B
                  +(2/3)*(Lambda+beta)*zeta]/zeta^2,
    Kf=ceil(log2(2*m*r/deltaf)).

With probability at least 1-deltaf conditional on the entire coarse history,
||Khat_a-K_a||_G<=zeta simultaneously. The fine dimension enters through the
ACTUAL Lambda, not an assumed rank surrogate. For well-spread acquired
features Lambda can be order r. For localized task directions it can be
order n even at small rank, eliminating the prospective acquisition saving.

The constant column can be set to its known exact value when V starts with
1 AND every other column has zero h mean (so the first Gram row/column has
no off-diagonal terms). In orthogonal coordinates this removes an error
column and cannot enlarge the spectral error. Merely starting an arbitrary
nonorthogonal basis with 1 does not suffice. Other structural postprocessing
needs its own proof.

## 4. What precision separation this can actually certify

The first lemma in the companion note yields

    d <= a^2/[2*(1-gamma^2)] + 2*zeta + 2*rho + omega.

Combine it with the checked off-space leakage product and the finite integer
replay theorem. For acquired bounded task constants/gaps and coarse
a,e_in,e_out of order theta, coarse contributions are order theta^2 while
the fine projected uncertainty is order zeta. Therefore an admission can use
theta of order sqrt(epsilon) and zeta of order epsilon, at fixed horizon and
checked constants. The actual nonasymptotic inequality, not big-O notation,
must pass before any future query is admitted.

With all those explicitly checked quantities bounded, the displayed source-
sample counts have the conditional form

    coarse: O(m*n/epsilon),
    fine:   O(m*Lambda/epsilon^2),

up to the shown horizons, gaps, metric/incoming factors and logarithms. A
uniformly fine full-operator spectral frontend instead pays an n/epsilon^2
term under the same concentration argument. This is a meaningful candidate
precision-allocation gain when Lambda<<n and coarse acquisition is genuinely
successful; it is NOT a lower bound on every equally informed learning
method, and does not establish that prior goal-oriented methods lack it.

## 5. Statistical timing, computation and finite bits are not optional

Each batch size is fixed before that fresh batch, conditional on prior data.
The distribution h and space V are frozen for its projected confidence
argument. A changed space/metric cannot reuse the old fine concentration
claim as if it had been selected independently. Refinement requires fresh
data or a separate uniform/time-uniform argument, with all failures paid.

The initial incoming-mass budget, all coarse rounds and all fine rounds use
summable failure allocations. Their intersection supports adaptive future
word queries; it does not validate outcome-dependent stopping inside a batch.

Sampling h exactly must be implementable. One option proposes h as normalized
positive integer weights of an explicitly bounded common denominator, checks
all geometric certificates, builds a cumulative table and samples a uniform
integer by rejection. Expected source-independent random-bit and lookup cost
are paid. An exact stationary solve with an enormous denominator is not
silently declared a cheap sampler.

Streaming fine feature outer products costs r^2 arithmetic per pair. An
alternative retains pair counts (up to n^2 integers), updates a count per
draw, then projects once at paid dense/sparse matrix cost. Both memory and
bit budgets are explicit choices. Count numerators grow with log(N), and
learned basis/metric rational lengths must be measured; source-sample counts
alone are not a full operation or wall-time ledger.

Coarse basis/geometry/norm certification may cost dense n^3 work or worse
for a naive search. Integer replay still needs paid coefficient rounding,
common denominators, Gram conditioning and output rounding. The proposed
consequence must survive these costs and the same forgetting/direct-query
baselines that defeated the earlier fixture.
