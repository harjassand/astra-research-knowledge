# Acquiring an arbitrary source from approximate nonnegative predictive width

30 October 2026. NEW proposed statistical principle; whole challenge pending.
The frozen exact-rank compiler and sample-only operation are consumed at their
accepted scopes without changing their bytes, algorithms or experimental data.
No new source instance, optimizer, learner or benchmark has been run.

## 1. Consequence and input

An exact finite predictive-rank promise is inappropriate for many scientific
sources. The compiler can instead have a model budget r and an oracle inequality
for arbitrary truth P. It need not receive, evaluate or sample a low-rank shadow,
know its approximation error, or force the shadows at different cuts to define
one coherent global generative model.

P,Q are arbitrary fixed laws on [O]^T, O>=2,T>=1. Inputs remain iid FULL P
trajectories and fresh iid conditional Q future samples at positive-Q prefixes.
No probability VALUE service, P conditional/likelihood, supplied KL bound,
target singular gap, or TRUE rank(P) bound is supplied. The integer r>=1 is a
model budget. Ordinary rational input length, source queries, returned symbols,
conditional/reset acquisition and fair-bit/arithmetic costs are paid as in the
accepted sample-only construction. Source sampling is not passive P data alone.

For a cut t with prefix law P_t and future law p_h=P(.|h), define w_r(P) by the
following FINITE-DIMENSIONAL EXISTENCE optimization. Choose at each cut an
arbitrary family of PROBABILITY vectors s_(t,h), one for each P-positive prefix,
whose linear span has dimension<=r. No consistency across cuts is required.
Set

    e_t = E_(h~P_t) ||p_h-s_(t,h)||_1,
    w_r(P) = min_(all such families) max_(1<=t<T) e_t.    (1)

For T1 take w_r(P)=0. These witnesses are not oracle inputs. The minimum exists:
at each cut the product of finitely many probability simplexes is compact,
the rank<=r constraint is closed by vanishing minors, and the finite weighted
L1/max objective is continuous. The feasible set is nonempty (one uniform row
for every prefix). The width lies in[0,2] and is0 exactly when every true
predictive cut has rank<=r. It is a quantitative approximation to that property,
not a positive hidden-state count or a supplied latent realization.

Let A0=ceil[10000(r+O+T+1/delta)], kappa=1/131072. The proposed SAME completed
sample-only/grid-selection algorithm returns a finite teacher-free rational
autoregressive H such that, with probability at least1-delta,

    TV(P,H) <= epsilon+256 A0^2
                 [D(P||Q)+w_r(P)]^kappa.               (2)

The algorithm is not given either term in this bracket. Infinite KL makes the
guarantee vacuous, while candidate construction remains valid. Work and size are
fixed polynomials in A0,1/epsilon relative to input source services; exact-law
output uses EXPECTED polynomial fair-bit work. Practical constants, moderate
misspecification, physical acquisition and historical priority are not claimed.

## 2. The cutwise row family is the whole structural resource

Fix any witnesses in(1), before algorithm randomness. At a cut, sample raw prefixes
h_i from ACTUAL P trajectories as before. Their hidden rows s_(t,h_i) are iid
under that actual prefix law and lie in one r-dimensional space. The population
max-volume/sample-compression proof therefore applies to these rows, even though
they are not sampled futures from P or from any global shadow source. The
conditional-on-fixed-index-subset union bound does not require that the law
sampling prefix indices and the law defining each probability row coincide.

The learner still computes only selected EMPIRICAL-TEACHER R rows. The hidden
s rows serve as the low-rank witness matrix for robust geometry. To pay their
proximity, put d_R=D(P||R). Conditional chain rule and Pinsker give

    E_(h~P_t)||p_h-R_h||_1^2 <=2d_R.

Both p_h and s_h are probability distributions, so their L1 distance is<=2 and

    E||p_h-s_h||_1^2 <=2 e_t.

The triangle-square inequality thus yields

    E_(h~P_t)||R_h-s_h||_1^2 <=4d_R+4e_t.              (3)

Consequently ALL NT raw teacher rows are eta-close to their hidden low-rank rows
except with probability at most

    4NT(d_R+max e_t)/eta^2.                            (4)

This replaces the exact-rank proof's2NTDelta/eta^2. It uses only actual P sampling
and teacher R queries; no s_h value, sample, conditional reset or prefix mass is
queried. With2(d_R+max e_t)<=x^-4096 the SAME old resource/geometry proof applies.

The finite mixture sketch, rational subspace/spanner and L1 uniform-concentration
steps then represent the hidden s_h, for all but gamma0 ACTUAL P-prefix mass,
by selected R rows to error<=4r zeta after mass normalization. Their coefficient
bound, uniform-row padding and feature-feasibility arguments are unchanged:
they require a NONNEGATIVE normalized s_h, not that s_h is the actual truth.
The family is probability-valued by construction, so the positivity proof is
fully paid. Fresh projection features remain independent of geometry.

## 3. Actual-P propagation, without shadow children

The full-state signed KL projection and normalization telescope always use the
ACTUAL conditional p_h and the teacher's joint restrictions. They do not invoke
low-rankness of p_h, nor restrict/renormalize the hidden s_h at a child. Thus
there is no reason to impose inter-cut consistency on the witnesses.

At a good feature-history, choose the feasible proxy z0 approximating s_h within
9tau. Its approximation to p_h obeys

    ||p_h-z0||_1 <=9tau+||p_h-s_h||_1.

Insert this in the accepted signed projection inequality and average under the
fixed actual P-prefix law. Its extra cost is at most B e_t. Bad feature histories
still cost B times their P mass; their coverage is obtained from the hidden-row
distribution sampled by P prefixes, so there is no selected-child bias term.
All other negative-mass, actual-token KL, child-normalizer, clipping, arithmetic
and first-order budgets are identical. Therefore the accepted fixed-tau bound
extends to

    D(P||H_tau) <= d_R+40T(B+1)tau + B sum_t e_t.        (5)

The target of this KL is P, not a shadow. No sum of shadow KL divergences and
no approximation of future conditional children is assumed. The algorithm is
UNCHANGED: only the existence witness in its analysis has changed.

## 4. Full sample-only fixed-tau qualification

Use the accepted support-safe empirical teacher with gamma<1/16 (as in the
frozen grid) and x=A_gamma/tau,
rho=alpha=x^-8192. Conceptual independent tapes, irreversible escape and the
global uniform mixture give, on its tree event,

    d_R <= d+TO rho+2alpha+(TO rho+sqrt(d/2))L,
    d=D(P||Q), L=TlogO+log(1/alpha)<=x^2.               (6)

Assume for this candidate that

    d+w_r(P) <= x^-16384.                             (7)

Choose the minimizing witnesses in(1). Then d_R<=5x^-8188 and w_r(P)<=x^-16384.
Hence2(d_R+w_r(P))<=12x^-8188<=x^-4096, paying(4) with the original huge schedule.
Also w_r(P)<=tau (tau>=x^-1), so(5) is bounded by

    D(P||H_tau)<=x^-4096+41T(B+1)tau.                  (8)

The root's coarse Pinsker bound TV(P,H_tau)<=64A0^2 tau^(1/4) still follows:
changing40 to41 leaves ample slack, since41*100/2=2050<64^2 and A0>=1.
The same confidence events, not an uncountable union of shadow choices, are used.
The deterministic witnesses were fixed for the true P before randomness.

Outside(7) every candidate is still a defined bounded-work rational law. The
accepted rank-budgeted geometry, uniform-suffix fallback and fixed-bit inference
completion are explicitly unconditional. None requires knowing w_r(P), d or
whether(7) holds. Every Q query remains support-safe even if d is infinite.

## 5. Unknown-error grid and ordinary finite-family selection

Consume root's frozen UNKNOWN_KL_SELECTION exactly, except replace its scalar d
by s=d+w_r(P) in the ANALYSIS. The algorithm receives neither quantity and hence
needs no change. Its grid satisfies x_j<=tau_j^-2, so

    s<=tau_j^32768 => s<=x_j^-16384.

The literal confidence translation remains delta_T=4gamma_j: its tree event and
core event each have failure gamma_j. The raw-row geometric event now follows
from(4) and(7); all other events and their union allocations are unchanged.

The good candidate has the same64A0^2 tau^(1/4) error bound by(8). Every candidate
is frozen before P holdout/model samples, and the SAME rational law is used for
sampling and Yatracos likelihood comparisons. The ordinary score selector still
gives3v*+4e. Root's best-grid/fallback algebra therefore proves(2) with its SAME
constant256 and exponent1/131072. It does not estimate the structural width,
construct the minimizing shadows or test their existence from data.

All finite-law, encoded-input, conditional-query, returned-symbol, arithmetic,
inference and expected fair-bit work qualifiers of the frozen producer/root
proofs remain in force. No new source, oracle or exact-rank truth promise is
introduced by this transfer.

## 6. Consequence for approximate global models, including null prefixes

Let C_r be all probability laws S on[O]^T of predictive linear rank<=r at every
cut, interpreted on positive-S prefixes. Define

    eta_r(P)=min_(S in C_r) TV(P,S).                    (9)

This minimum also exists: rank of each joint prefix/future flattening equals
the conditional-row rank after deleting zero columns and positive rescaling.
Thus C_r is a closed subset of a finite probability simplex, given by vanishing
minors; TV is continuous. It is nonempty (Uniform has rank1).

For ANY S, at a P-positive prefix with S(h)>0 use s_h=S(.|h). At a prefix with
S(h)=0 choose one arbitrary POSITIVE-S conditional row at the same cut. Such a
row exists because S has total mass1. These choices keep the whole hidden row
family inside S's existing r-dimensional span, without a support-inclusion or
conditional-S oracle. At every h,

    P(h)||p_h-s_h||_1
      <= sum_f |P(hf)-S(hf)|+|P(h)-S(h)|.              (10)

For S(h)>0 this is the ordinary joint/marginal triangle; when S(h)=0 its right
side is2P(h), which bounds the left side for ANY probability s_h. Sum(10) over h:

    e_t<=2||P-S||_1=4 TV(P,S),
    w_r(P)<=4 eta_r(P).                               (11)

The complete all-P theorem therefore implies the model-class oracle inequality

    TV(P,H)<=epsilon+256A0^2[d+4eta_r(P)]^kappa
            <=epsilon+512A0^2[d+eta_r(P)]^kappa.        (12)

The model budget r is not asserted to be truth's rank. Even low-rank shadows
excluding rare true words are covered. Neither an attaining model nor its
parameters, probabilities, samples or error is an algorithm input.

## 7. Novelty, ordinary comparison and remaining questions

The accepted exact-rank machinery, Liu--Moitra's geometric/KL/empirical primitives,
and ordinary finite-family selection remain the constructive predecessors.
Kakade--Krishnamurthy--Mahajan--Zhang2302.14753/COLT2023 was screened at its exact
target-rank/conditional-query definitions and theorem scope; its fidelity-
qualified sample model is not silently replaced by the present teacher interface.
A narrow literature screen found no identical all-P width oracle inequality;
historical priority remains UNKNOWN, not established by that search.

The width witnesses need not be consistent global models, but STRICT separation
from the best global rank-r TV model is not claimed without an additional proof.
The quantitative implication(11) and full all-P theorem already hold. Likewise
low logit rank is a different promise: the live primary2512.09892v1 uses logit
queries and bounded approximate logit geometry, with an explicit sample-only
question. No logit-rank transfer is inferred here.

This is a broader statistical operation, not exponent/certificate tuning and
not a finite fixture claim. It removes exact low-rank truth as an input promise.
The tiny Holder exponent, enormous sample/arithmetic costs, actual conditional
reset service, practical forecasting, historical novelty and all-method advantage
remain outside the result. Whole internal challenge is pending; no new program,
data acquisition, scientific instance or optimizer was executed for this proof.
