# Independent unknown-KL grid and teacher-free selection reconstruction

30 October 2026. This reconstructs the proposed root
root_predictive/UNKNOWN_KL_SELECTION.md after the support-safe lazy-law interface.
It is not a new selection principle, numerical experiment or likelihood oracle.
The conditional premise is the fixed-tau sample-only wrapper, whose complete
producer proof is reviewed separately. The calculations below use its conservative
d<=x^(-16384) sufficient condition; no exponent optimization is intended.

## 1. The fixed-tau quantitative port

At compiler confidence gamma set

    A_gamma=ceil(1000(r+O+T+1/gamma)), x=A_gamma/tau,
    rho=alpha=x^(-8192).

For x>=100 A_gamma^2, all numerical cutoffs below are met. In the lazy-law
transfer B0=T log O+8192 log x<=x^2, using T,O<=A_gamma and x>=10^8.
If d<=x^(-16384), the transfer error is bounded by

    d+TO rho+2alpha+(TO rho+sqrt(d/2))B0
      <=5 x^(-8188) <=x^(-4096).

Thus the old accepted fixed-tau VALUE construction applies to the acquired
rational R, without any original-Q value service. The implementation does not
need d to decide whether this inequality is true. It runs its fixed cap and
returns a valid law even on failure of the approximation promise.

The rank, scientific horizon and alphabet parameters in the clipped-log bound
are bounded by A0, not by the confidence-inflated A_gamma. In particular, with
C=8(r+1), a=tau/(2O), theta=tau/[4(r+1)] and
K=(r+1)C/a+2, direct expansion of log[K/(theta a^T)] gives the conservative

    B+1<=100 A0^2 log(1/tau).

From the accepted KL bound x^(-4096)+40T(B+1)tau, Pinsker and
tau log(1/tau)<=sqrt(tau), the stated sufficient estimate follows:

    TV(P,H_tau)<=64 A0^2 tau^(1/4).

This separation of scientific A0 from grid confidence is important. Replacing
it by a confidence-dependent A_gamma in the final noise coefficient and then
hiding its log(1/epsilon) dependence would not prove the proposed uniform modulus.

## 2. A grid whose confidence cost fits its own admissibility gate

Let A0=ceil(10000(r+O+T+1/delta)). For j>=0 define

    tau_j=2^(-j)/(10000 A0),
    beta_j=gamma_j=delta/[32(j+1)^2],
    A_j=ceil(1000(r+O+T+1/gamma_j)).

The elementary bounds

    A_j<=4 A0(j+1)^2,
    (j+1)^2<=(9/4)2^j

give A_j tau_j<=9/10000<1/100 and A_j<=1/tau_j. Hence every grid point satisfies
the original compiler's gate and x_j=A_j/tau_j<=tau_j^(-2). In particular,

    d<=tau_j^(32768) implies d<=x_j^(-16384).

No supplied upper bound on d appears in any algorithm parameter. The sum of
tree and fixed-tau confidence allocations is less than delta/8. Independence
between different grid candidates is convenient but unnecessary for this union
bound. It is the P holdout and model-selection sampling that must be fresh after
all candidates are frozen.

Stop at the first J with

    tau_J <= tau_acc=[epsilon/(1024 A0^2)]^4.

Then tau_acc/2<tau_J<=tau_acc and J=O(log(A0/epsilon)). The largest A_j and inverse
smallest tau_j are fixed polynomials in A0 and 1/epsilon. Their logarithmic
factors do not introduce a horizon-dependent exponent. Composing the finite
sample-only service cost with the accepted compiler therefore remains a fixed
polynomial, although its degree is enormous.

## 3. Selection needs samples and deterministic model values, not P values

For the K=J+1 frozen finite laws H_i, define
A_ij={x:H_i(x)>H_j(x)}. The finite model's deterministic rational inference rule
gives H_i(x) by a product along x. Exact rational comparison defines a fixed
tie convention. No original-Q callback, P likelihood or exact TV computation
occurs in this step.

Draw n fresh samples from each of P,H_1,...,H_K. The same sample from a law can
be evaluated on all K^2 sets; independent samples for each set are not needed.
The K^2(K+1) indicator estimates simultaneously have absolute error at most e
with failure at most delta/2 provided

    n>=log[4(K+1)K^2/delta]/(2e^2).

All K^2 comparisons and all model evaluations are charged polynomial work.
They are not an oracle supplying the masses of the comparison sets.

Choose k minimizing max_ij |P_emp(A_ij)-H_k,emp(A_ij)|. If k* is a closest
candidate with error v*, its empirical score is at most v*+2e. The selected
candidate therefore has true discrepancy from P on A_(k,k*) at most v*+4e.
Adding the discrepancy between P and H_k* on that set bounds
TV(H_k,H_k*) by 2v*+4e. Triangle gives

    TV(P,H_k)<=3v*+4e.

This proves the stated factor three rather than silently assuming the exact
candidate-set masses are computable. It also makes no claim that the selected
candidate's KL is estimated or bounded. Conditional empirical-score validity
holds because the laws were frozen before the holdout/model samples.

## 4. The complete misspecification modulus

Put s=d^(1/32768) for finite d. If s<=tau_J, the last candidate qualifies and
its TV error is at most epsilon/16. If tau_J<s<=tau_0, the smallest grid value
which is at least s is below 2s. That candidate has error below

    64*2^(1/4) A0^2 d^(1/131072)
      <77 A0^2 d^(1/131072).

With e=epsilon/16, the selected law therefore satisfies

    TV(P,H_selected)
      <=7epsilon/16+231 A0^2 d^(1/131072)
      <=epsilon+256 A0^2 d^(1/131072).

If s>tau_0, the last claimed noise term is already greater than
256 A0^2 tau_0^(1/4)=25.6 A0^(7/4)>1. Thus that regime is legitimately vacuous.
For d=0 the first regime applies. For infinite d, every output law satisfies the
vacuous right side, while its computation is still defined and capped.

The noise coefficient has no hidden epsilon-dependent confidence logarithm.
Neither choosing J nor evaluating the models requires estimating d, entropy,
target conditional laws or target likelihoods.

## 5. Completion and scope

Bad candidates must remain normalized finite laws, with deterministic bounded
inference and a feasible fallback at every step. All finite token rows are
rational and nonnegative after the declared clamp/normalization, even without
the approximation event. A model sampler and its likelihood evaluator must use
that same deterministic rule; numerical warm starts or fresh randomized solver
choices are not a replacement for this contract.

Rational categorical sampling has expected polynomial bit work. If the theorem
is stated with a high-probability finite work cap, truncate the number of fair-
bit rejection rounds at a prescribed cap with its separately reserved failure
budget over the known finite compilation/model-selection experiment. The returned
exact rational law has expected polynomial fair-bit sampling cost. A fixed
worst-case cap on each future output instead defines a slightly changed law and
must pay its per-output TV reserve; no single delta union is asserted over an
unlimited future stream. The original conditional-Q service's own runtime and the cost of full
P trajectories remain input acquisition costs. They cannot be inferred from a
query-count theorem.

No additional benchmark is necessary for these arguments. They remove the former
VALUE and supplied-Delta premises at a strong conditional-reset interface; they
do not make those resets physically available, improve the enormous formal
polynomial into a practical one, or overcome the usually vacuous noise modulus.
