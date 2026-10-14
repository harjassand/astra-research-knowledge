# Late capital: reflected snapshot certificates, clock geometry and acquisition

15 October 2026. Source PR87 is pinned at
`a69ae39e8a23cc4d5b337bfa01ef2bd5ccbb7a0c`, base
`00631610750c708263d5cf6d812ebbb8edc77335`. Its actual theorem, comparator
addendum and exact calculation code were read. This packet neither merges that
branch nor adopts its claim card as a main-branch dependency. The deductions
below are internal and externally unreviewed; priority and physical capability
remain UNKNOWN. The independent source bytes and late worker evidence are
preserved under `late_capital/`, separately from the previously frozen science.

## A positive clock kernel is the actual proof interface

The source considers a stationary finite all-even CTMC with generator Q,
stationary distribution pi, ordinary reversal, and three conditionally independent
memoryless Bernoulli emissions with probabilities b_i. Let
W=Y_0(Y_-−r)(Y_+−r), c=r(1−r), and −E W=D>0. Its killed geometric-path
generator G is self-adjoint in L2(pi), with nonpositive row sums. For gaps s,t,
its unnormalized geometric-measure score is

    sum_i pi_i b_i g_i(s)g_i(t),  g(s)=exp(sG)(b−r1).

The source imposes iid gaps. A strictly wider sufficient interface is any
specimen-independent symmetric gap-pair probability measure K such that

    integral h(s)h(t) K(ds,dt) >= 0

for every bounded real measurable h. Assume finite positive
m=E_K[(S+T)/2]. Then each i term is nonnegative. Symmetry ensures that reversal
of the path and interchange of the clock endpoints preserve the observable law.
For the common clock mixture, mu=(P+P^R)/2 dominates the geometric measure nu.
Consequently D<=c(1−A). For each total duration S+T, path-entropy Jensen gives
A_(S+T)>=exp(−sigma(S+T)/2); clock Jensen gives A>=exp(−sigma m). Thus

    sigma >= −log(1−D/c)/m,  0<D<c.

This is a proof extension, not a finite-test inference. Mixtures
K=integral rho_z tensor rho_z dmu(z) satisfy the premise directly as mixtures
of squares. A shared random gap S=T is an example. More general symmetric
positive-semidefinite clock kernels also qualify when the displayed integrals
exist. Identical marginals or exchangeability alone do not suffice: the source's
anti-correlated clock pair has a negative eigenvalue and an equilibrium
counterexample. Dependence on specimen state, uncharged adaptive selection,
readout memory or a different physical reversal is outside this extension.

For a finite clock grid with marginal vector p, an acquired spectral bound
D_p^(-1/2) K D_p^(-1/2)>=−eta I gives a controlled defect. Sub-Markov
contractivity bounds |g_i(s)| by R=max(r,1−r), so the killed score is at least
−eta R^2 p1, where p1=E Y0. The same proof therefore uses
D_eff=D−eta R^2 p1 if it is positive. Mean timing, eta and p1 need valid bounds;
this correction does not repair specimen-dependent clocks. A common clock
reused across trials also needs dependence-aware sampling analysis.

## The acquisition budget can use variance, with its calibration charged

The source's near-optimal short-gap ring score has both a negative mean and
second moment of order t^2. A bounded-score Hoeffding calculation therefore
scales as t^-4, while a valid variance-sensitive Bernstein calculation can
scale as t^-2. This is standard statistical machinery applied to the actual
score; it is not a new concentration theorem or a necessary lower bound.

A separate rational signed-matrix Taylor calculation at t=1/1000 and
r=39991/40000 encloses D around 9.00637398037e−8 and E W^2 around
3.36012578317e−8. Using Var W<=E W^2, range width R=max(r,1−r),
delta=D_lower/2, and log(20)<3, the sufficient one-sided confidence-radius
budget is

    n >= 2 log(20) (v + R delta/3) / delta^2.

The exact conservative calculation gives n=143821410 iid triplets, versus
739359815185143 from the same conservative-log Hoeffding calculation. These
are sufficient planning counts for a confidence radius half the expected
margin. Neither count guarantees a particular realized estimate, proves an
optimal budget, nor provides physical independent stationary trials. A supplied
exact mathematical generator provides v here; a specimen needs a separately
valid variance bound or a valid variance-adaptive confidence procedure, with
calibration data and selection corrections charged. Matched incumbents receive
the same variance information and observations. Roughly 143.8 million trials
still do not establish a useful experiment.

## No automatic transfer to the exchange or polarity programmes

A positive snapshot certificate concerns a stationary path law under its
specified reversal. Conditional quantum exchange compares a routed,
reference-tagged future task. Their information interfaces differ: reversible
memory can support a task contrast, and independent driven dissipation can
coexist with zero contrast. Neither positive quantity supplies the other's
missing joint operation certificate. Driven wall writing is not a stationary
all-even autonomous specimen model either.

Postselecting middle snapshots with Y_0=1 requires multiplication by the
stationary prevalence p1: E W=p1 E[(Y_-−r)(Y_+−r)|Y_0=1]. Preparing a conditioned
state afresh does not automatically reproduce the stationary path ensemble.

Detector calibration must constrain its temporal and specimen-conditioned
behavior. A driven hidden detector can reproduce a negative three-snapshot
score while an equilibrium or clamped specimen supplies no such dissipation.
Its one-time Bernoulli marginal can equal a chosen calibration marginal. This
falsifies marginal-only certification, not a complete truth-conditioned,
memoryless multitime readout contract. The ordinary path-entropy floor then
belongs to the joint specimen-plus-detector model; attributing it to specimen
heat requires the source's stronger detector and physical-parity premises.

## Decisive continuation

The positive clock kernel permits experimental timing flexibility without
sacrificing the proof. Test one physical readout with calibrated temporal memory,
back-action, reversal/parity, clock independence, stationarity and a valid
variance/dependence bound. Compare the reflected statistic, optimized hidden-model
inference and equally informed task-specific estimators using the same raw
records and full acquisition ledger. Extra finite-generator checks cannot
acquire those missing premises.

Source: [PR87](https://github.com/harjassand/astra-research-knowledge/pull/87).
The exact source theorem and comparator are preserved in
`late_capital/adversarial/late_pr87_sources/`; separate late overlap and
adversarial reports record reconstruction and finite-check scope.
