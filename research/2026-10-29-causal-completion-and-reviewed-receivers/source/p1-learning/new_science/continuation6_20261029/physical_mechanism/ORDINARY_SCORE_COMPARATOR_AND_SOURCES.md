# The strong ordinary comparator and the resulting claim boundary

29 October 2026. Companion to `VISIBLE_RESPONSE_DESIGN_WITHOUT_HIDDEN_MODEL.md`.
The initial proposal was to acquire response derivatives by physically inserting
an intervention between two random prefixes. The close ordinary comparison
does more than provide context: it prevents claiming a generally superior or
new physical gradient operation.

## 1. The exact ordinary tangent score is smaller than the raw-count score

Write q=1-rho, c=rho/q, P_w=sum_j w_j P_j and
F(w)=q <f,(I-rho P_w)^(-1)f>. A geometric trajectory has N native calls,
controller counts N_j, and bounded endpoint product Y=f(X_0)f(X_N).

The ambient derivative can be written E[Y N_j/w_j]. Its raw-count second
moment contains c/w_j+2c^2. Using that bound to dismiss the ordinary comparator
would be a mistake: optimization occurs on the simplex. For direction e_j-w,

    S_j=N_j/w_j-N,
    E[Y S_j]=g_j-w dot g,
    E S_j=0,
    E[S_j S_k]=c[1_(j=k)/w_j-1].                       (1)

Thus every tangent coordinate is estimated by the same trajectory, with
variance at most c(1/w_j-1). The learner needs its recorded selector counts,
not hidden-state transition probabilities. An expected c native calls acquire
all these estimates together. This is an ordinary likelihood-ratio identity.

For two modes, with w the probability of mode 1,

    S=N_1/w-N_2/(1-w),
    E[Y S]=F'(w),   E[S^2]=c/[w(1-w)].                 (2)

At fixed interior w, score variance grows at most linearly in the mean
geometric horizon. The forced-insertion derivative has a multiplier c and
can have variance of order c^2, while its path costs 2c+1 calls. This is a
material ordinary advantage, not a small constant correction.

## 2. The ordinary route supplies a finite confidence certificate too

No asymptotic CLT or mixing rate is needed to turn the score into a finite
confidence interval, because independent warranted baseline starts are part
of the common interface. Let V=c/[w(1-w)] for the two-mode derivative. Split
n=b s independent samples into b odd blocks of size s. Each raw-score block
mean has variance at most V/s. For

    xi=sqrt(8V/s),

Chebyshev gives probability at most 1/8 of a block error exceeding xi. The
median of the block means fails only when at least half the blocks fail.
The binomial Chernoff bound therefore gives

    Pr(|median-F'(w)|>xi) <=(7/16)^(b/2).              (3)

The exact convex gap is max(w F'(w),-(1-w)F'(w)). With confidence (3), an
acquired global upper bound is

    max(0, w(median+xi), -(1-w)(median-xi)).            (4)

For m controls use the simultaneous tangent coordinates in (1), a union
bound over coordinates, and the identity G=-min_j(g_j-w dot g). This gives
the same kind of global physical design certificate as the insertion method.
It does not need microscopic model fitting or a small finite-difference step.

There is a boundary limitation: the on-policy score for an absent action is
undefined at w_j=0, because data without that action do not reveal its
intervention response. Actual forced exploration fixes this. A competent
ordinary optimizer can use exactly such exploration or mix score and
weak-derivative sampling. The proposed sandwich cannot claim an exclusive
capability by withholding that admissible option from the comparator.

## 3. Reward baselines strengthen the comparison further

For any baseline b independent of the current sampled word,

    E[(Y-b)S]=F'(w).

In the binary-readout checker, Y is always +/-1. Let
v=E S^2 and d=F'(w). Then the minimum-variance constant baseline and variance
are

    b_*=E[Y S^2]/v,
    Var[(Y-b_*)S]=v[1-b_*^2]-d^2.                    (5)

This baseline is not silently supplied to the actual learner. The executed
comparison estimates it from its own independent pilot subset and charges
those preparations and native calls. The exact b_* is used only in the
separate population variance comparison, to give the ordinary method a strong
benchmark. The finite-confidence certificate (3) uses RAW scores, so it does
not accidentally apply the smaller raw variance bound to a baseline-corrected
variable of magnitude as large as 2|S|.

Population values of (5) can be evaluated without simulating repeated trials.
For the two-mode matrices put D=P_1-P_2, R=(I-rho P_w)^(-1), and
P''=P_1/w+P_2/(1-w). The tilted-word generator gives

    E[Y S^2]
       =q rho <f,R P'' R f>
          +2q rho^2 <f,R D R D R f>.                 (6)

Indeed replace P_w by w exp(t/w)P_1+(1-w)exp[-t/(1-w)]P_2 in the geometric
series and differentiate twice at t=0. The path exponential has exponent tS.
Equation (6) is a population check; hidden matrices are not exposed to the
learner or to the actual baseline-selection calculation.

For a forced sandwich let m_j=<f,S_w P_j S_w f>. With n independent paths
per intervention, its contrast variance is

    c^2[(1-m_1^2)+(1-m_2^2)]/n.

The expected native calls are 2n(2c+1). Its variance times expected call budget
is therefore

    2c^2(2c+1)[2-m_1^2-m_2^2].                       (7)

For the score estimator the analogous coefficient is c times its single-path
variance. These comparisons count real native calls. They are not full cost
rankings: the shorter score paths use more baseline preparations at the same
native-call budget. If preparation dominates cost, the winner can change.

## 4. Relation to size-biased and weak-derivative trajectories

For the raw ambient derivative, differentiating a geometric word marks one
of its calls. The marked word has probability proportional to its length.
Its total length is distributed as N_1+1+N_2 with independent geometric
N_1,N_2, and the marked call can be forced to the differentiated action.
This is exactly the two-prefix insertion experiment.

Thus the insertion and score routes are two standard representations of the
same derivative. Neither requires branching a microscopic specimen into two
futures. An uncharged same-state coupling or common bath-noise replay WOULD
be a different resource and is not used. Boundary importance sampling and
variance tradeoffs are real, but do not turn this product-rule identity into
a new law of physical computation.

## 5. Primary predecessors read early

The preserved Astra mission source, scientific-acceptance source, and
FIFTH_CONTINUATION_HANDOFF.md were read before developing this construction.
Their instructions to choose a consequential question, preserve actual
operation interfaces, and compare the strongest supported ordinary route
governed the choice. Historical operational limits remain historical; current
user and role instructions govern. No N675 result was reopened.

### Convex physical network design

S. Boyd, P. Diaconis and L. Xiao, *Fastest Mixing Markov Chain on a Graph*,
SIAM Review 46, 667-689 (2004),
[primary author PDF](https://web.stanford.edu/~boyd/papers/pdf/fmmc.pdf),
[DOI](https://doi.org/10.1137/S0036144503423264).
Read the declared graph/transition interface and Section 2's convex and SDP
formulations. Optimization of a reversible physical/Markov dynamics over
admissible transition weights is established. Our objective is a measured
finite-filter response, not their global second-eigenvalue objective; this
difference does not make convex kinetic design itself novel.

A. Ghosh, S. Boyd and A. Saberi, *Minimizing Effective Resistance of a Graph*,
2006 MTNS paper and SIAM Review 50, 37-66 (2008),
[primary author conference paper](https://stanford.edu/~boyd/papers/pdf/eff_res_mtns06.pdf),
[journal DOI](https://doi.org/10.1137/050645452).
Read the objective, inverse-Laplacian formulas, first/second derivatives,
gradient interpretation and dual-gap discussion. This is the closer objective
predecessor: inverse positive operators, quadratic response derivatives,
convex conductance allocation and global optimality bounds are already
explicit. The present hidden-source acquisition interface differs from an
available graph matrix, but ordinary score estimation closes that distinction
without a new microscopic principle.

### Ordinary gradient access and weak derivatives

R. J. Williams, *Simple Statistical Gradient-Following Algorithms for
Connectionist Reinforcement Learning*, Machine Learning 8, 229-256 (1992),
[full primary paper scan](https://gwern.net/doc/reinforcement-learning/model-free/1992-williams.pdf),
[DOI](https://doi.org/10.1007/BF00992696).
Read the REINFORCE theorem, episodic score accumulation, and baseline
discussion. Recorded randomized controls already support unbiased
model-free gradients; reward-baseline variance reduction also has a direct
predecessor. Unknown hidden physics does not invalidate the likelihood-ratio
identity when only the known selector distribution depends on the design.

B. Heidergott, A. Hordijk and H. Weisshaupt, *Measure-Valued Differentiation
for Stationary Markov Chains*, Mathematics of Operations Research 31,
154-172 (2006), [primary publisher](https://doi.org/10.1287/moor.1050.0171).
Read the publisher abstract and stated scope, not the unavailable full paper.
Its operator derivatives, phantom estimators and score estimators are explicit
close predecessors. B. Heidergott and F. J. Vazquez-Abad's
[*Measure-Valued Differentiation for Random Horizon Problems*](https://math-mprf.org/journal/articles/id1093/),
Markov Processes and Related Fields 12, 509-536 (2006), was likewise read at
its primary abstract. No priority claim is based on not obtaining their full
proofs. The present geometric product-rule construction is proved directly.

### Random-scan adaptation

C. Chimisov, K. Latuszynski and G. O. Roberts, *Adapting the Gibbs Sampler*,
[primary preprint](https://arxiv.org/pdf/1801.09299).
Read the operation/selection framework, covariance-based Gaussian surrogate,
and the asymptotic-variance comparisons and limitations. Their adaptive
selection is already a practical ordinary design mechanism. The present
criterion uses an exact measured response instead of a covariance-derived
surrogate, at potentially much greater acquisition cost. This is a scope
difference, not evidence that adaptive scheduling or learning a good scan was
previously unavailable.

## 6. Result of the comparison

The physical design problem is constructive and has a rigorous visible-only
global certificate. It does not earn a claim of a generally superior gradient
operation. The ordinary selector-score method can use the same actual menu,
same sensor and same baseline resource, can produce a finite certificate,
and can be more efficient in the long-horizon interior. The executed learner
therefore USES that ordinary route in its pilot and compares it directly at a
matched expected native-call budget.

The candidate addition is at most the scoped acquisition-to-global-response-
design assembly for a hidden reversible source, plus its explicit physical
filter consumer and failure boundaries. Historical novelty and substantial
practical advantage have not been established. The unit is retained as useful
capital and a strong conventional comparator for broader inverse-design ideas.
