# Finite rational-rate consumer: baseline only

This is a separate join to the frozen global-odd candidate, not a modification
of its proof. The received sharper storage/vector theorem may be used with
**zero additional processing**, on the global mean-zero subspace. Its actual
evolution is the original self-adjoint Markov semigroup, so all its energy,
chronology and neutrality premises hold. No stirring or controlled process is
received by this consumer.

For the candidate's epsilon, the sharper uniform trial-vector bound is

 G = (1/2)sqrt(epsilon(1+epsilon)) + epsilon/exp(1).

Use the rational upper 3 epsilon/8 for its last term. Multiplication by the
normalized trial norm sqrt(N/Ztot)<=1 is safely discarded. The original
sqrt(epsilon) bound remains valid without this optional improvement.

## Exact, externally interpretable clock scale

Outward scalar receiving gives M in [Ml,Mh], R in [Rl,Rh]. Define

 l=1/(beta Mh Rh), u=1/(beta Ml Rl),
 lambda_star=(l+u)/2, d=(u-l)/(u+l)<1.

The true lambda=1/(beta M R) belongs to
[(1-d)lambda_star,(1+d)lambda_star]. For every t>=0 the mean-value theorem gives

 |exp(-2lambda t)-exp(-2lambda_star t)|
 <= |lambda-lambda_star|/[exp(1) min(lambda,lambda_star)]
 <= 3d/[8(1-d)] = rate_error.

An external rational x>0 specifies a **physical deterministic spacing**
Delta=x/lambda_star, not a grid defined using unknown exact M or R. Its
comparison chain has flip probability q=(1-exp(-2x))/2 per observation.
If eta bounds S0/M and s=eta/(2+eta), C=2+eta, then

 delta = (1/2)sqrt(epsilon(1+epsilon)) + 3epsilon/8
         +2sqrt(s)+rate_error

is a uniform whole-sign vector bound against this rational-rate chain. For n
steps the entire hysteretic sampled record has total variation at most

 T_grid = sqrt[C n delta^2 / (2(1-exp(-4x)))] + n eta.       (F1)

The reference starts A. Exact outward roots and exponentials, input reading,
scalar receiving and any finite-record event evaluation are separately paid.

## Continuous hysteretic jitter with the same rational rate

For a bin of length Delta, the actual stationary count upper is
(1+d)x. Its odd-label lower bound uses exp(-2lambda Delta), which is at most
exp[-2(1-d)x]. Since for a>=0,

 (1-exp(-2a))/2 >= a-a^2,

the actual stationary multiple-jump probability is at most

 d x + x^2/2 + epsilon/4 + 3s/2.

Transfer this whole event to Gibbs|A with factor C. The comparison chain's
multiple-jump probability is at most n x^2/2. Combining with (F1) yields

 T_jitter = T_grid +(C+1)n x^2/2 + C n epsilon/4
                    +(3/2)n eta + C n d x.              (F2)

Thus, with failure probability at most T_jitter, the actual and reference
hysteretic paths on [0,n Delta] have matching ordered jumps whose times differ
by at most Delta. This is time-jitter coupling, **not** total variation of
continuous jump-time vectors. Bounds above one provide no useful certificate.
Requested error gates are conjunctions: a consumer must refuse rather than
label a width it did not achieve. A finer numerical integral cannot remove
all intrinsic current/vector/cluster slack at a fixed model dimension.

## Paid finite-record event

For equal spacing, comparison-chain flip indicators are independent Bernoulli
with parameter q. An event that the **number of sampled label changes** lies
between external integers L and U is evaluated by a capped finite-state
dynamic program with states 0,...,U,U+1 (last state is overflow).
It costs O(n(U+2)) interval arithmetic operations, not an uncharged general
predicate oracle. Its actual probability lies between the outward comparison
endpoints minus/plus T_grid, clipped to [0,1]. Hidden within-bin transitions
are not counted by this event; their distinct continuous guarantee is (F2).
The initial A-label, raw actual model, exact once-only full Gibbs|A law, and
external n,x,L,U/error/budget arguments are all bound by recomputation.

Sources actually bound for this join:

- `GLOBAL_ODD_MODE_AND_RENEWAL_CANDIDATE.md`, SHA
  `4a8110be17507c8f0552a6ff5553e7b8f5caecfc94808900a4a05fda31cc1892`.
- `NEUTRAL_VECTOR_AND_PATH_SHARP_V2.md`, SHA
  `8da465ed3817a2e5cf0088cd0efba23e056a148422bf5a3120b96606a960a403`.
- Its `audit_vector_path_20261101_0049/INDEPENDENT_ACCEPTANCE.md` (hash in
  the local manifest), specifically the zero-processing/global mean-zero join.
- The generic root path theorem and its controlling independent cost audit
  listed in the local manifest. Neither generic receipt accepts this new
  global current or executable automatically.
