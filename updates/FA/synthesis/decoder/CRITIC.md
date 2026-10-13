# Independent criticism of decoder consequences

13 October 2026. Internal mathematical review, not external validation or
historical novelty clearance. The original theorem was read in full from
`rqa/outputs/COMPARISON_DECODER_THEOREM.txt`. No research-capital files were edited.

## 1. Exact recognition has an exponential comparison obstruction

**Verdict: correct**, with the following explicit recognition contract.

The input oracle is allowed to be any strict total order on the labelled points
of `F_2^n`. The procedure must accept the identity rank with probability at least
`1-alpha` and accept each specified outside-class rank with probability at most
`beta`. The degree parameter satisfies `n>=3` and `1<=d<=n-2`. This is a membership
recognition task on arbitrary oracles; the source decoder theorem instead takes
membership as a supplied promise.

For `a in F_2^(n-1)`, put

    I_a(x_1,...,x_(n-1)) = product_(i=1)^(n-1) (1+x_i+a_i),
    Q_a(x) = (x_1,...,x_(n-1), x_n+I_a(x_1,...,x_(n-1))).

Every operation in these formulas is over `F_2`. The indicator is one exactly
on prefix `a`, so `Q_a` is the permutation which swaps only the adjacent ranks
`(a,0)` and `(a,1)` of the identity order. A comparison involving any other
unordered pair has the same answer as identity: every other rank lies either
below both swapped ranks or above both. Either orientation of the special pair
distinguishes the oracles. A repeated point comparison distinguishes nothing.

The last coordinate of `Q_a` has exact Boolean algebraic degree `n-1`: its
multilinear ANF contains `x_1 ... x_(n-1)` with coefficient one, and the added
`x_n` cannot cancel this term when `n>=3`. An invertible affine substitution
preserves exact Boolean algebraic degree. Indeed, substitution preserves every
degree filtration (followed by the reductions `x_i^2=x_i`); applying the inverse
affine substitution gives the reverse inequality. Every coordinate in the
source class has degree at most `d`, including after the hidden affine input
change. Hence `Q_a` is outside the degree-`d` class. No assumption about a
particular triangular representation is needed to establish this exclusion.

Fix the internal random seed of a recognition procedure and couple its identity
and `Q_a` runs with that same seed. Until it asks the special unordered pair, all
answers and internal states coincide. Therefore an identity run which accepts
without asking that pair also yields an accepting `Q_a` run. Writing `A` for
acceptance on identity and `H_a` for asking that pair on identity,

    Pr(A and not H_a) <= Pr(accept Q_a) <= beta,
    Pr(H_a) >= Pr(A)-beta >= 1-alpha-beta.

If `N` is the number of comparison calls on identity, then pointwise
`N >= sum_a 1[H_a]`, including adaptive and repeated calls. Thus

    E_identity N >= max(0,1-alpha-beta) 2^(n-1).

In particular, deterministic exact recognition that terminates and accepts on
identity needs every one of the `2^(n-1)` special pairs along that transcript.
If an algorithm does not terminate, infinite expected cost already satisfies
the lower bound; acceptance probabilities are interpreted in the usual way.

This does not contradict polynomial promised-class decoder acquisition. It
separates cheap acquisition under a supplied class promise from exact global
certification of that promise. It does not exclude approximate recognition,
distributional testing, recognition with richer rank queries, or recognition
under an additional structural promise on the outside alternatives. For
`d>=n-1`, the displayed alternatives themselves lie in the triangular class,
so this particular argument gives no obstruction.

## 2. Noisy comparison compilation

**Verdict: correct after making the noise and stopping contracts explicit.**

Use a source capped learner with tournament erasure parameter `beta_t`, so

    P = binom(n,2),
    T = ceil(log_2(P/beta_t)),
    B = D+(2T+2)P,
    D = sum_(j=0)^d binom(n,j+1).

Assume the true comparison oracle belongs to the original class. For every
logical comparison, hold its chosen pair fixed and obtain an odd number `r` of
repeat answers. The true answer to that pair is unchanged during the repeats.

A sufficient noise contract is the following: conditional on the complete
adaptive history before each repeat, including the chosen pair and all earlier
repeat answers, the probability that this repeat is wrong is at most
`1/2-rho`, where `0<rho<=1/2`. Conditional independence of repeat answers given
the query history, together with that error bound for each repeat, is a
sufficient special case. Independence is unnecessary under the stronger
full-history conditional bound.

To verify the adaptive claim, let `E_s` be the repeat error indicator and let
`F_(s-1)` include the complete history before repeat `s`. Then

    m_s = E[E_s | F_(s-1)] <= 1/2-rho.

Conditional Hoeffding's lemma applies to `E_s-m_s`, whose conditional range has
length one. Iterating its moment-generating-function inequality and applying
Chernoff gives

    Pr(sum_s(E_s-m_s) >= r rho | initial query history)
      <= exp(-2 r rho^2).

A wrong majority requires `sum_s E_s >= (r+1)/2`, which in particular implies
the displayed tail event. Thus each logical comparison has conditional error
at most `exp(-2 r rho^2)`, despite adaptive query selection.

Choose `r` to be any odd positive integer satisfying

    r >= log(B/beta_n)/(2 rho^2),  0<beta_n<1.

The logarithm here is natural. Enforce a global budget of at most `B` logical
comparisons and define invalid internal states or budget exhaustion to return
`UNKNOWN`. Such a wrapper is necessary for the unconditional resource bound:
the source learner's structural invariants and promised-input query accounting
need not hold after a noise-corrupted answer. The cap has no effect on a fully
correct-answer source execution.

A union bound over at most `B` logical comparisons gives probability at most
`beta_n` of any majority error. On the complement of that event the execution,
using the same learner randomness, agrees with the exact source learner. A
separate union bound with its tournament erasure event therefore gives

    Pr(return an exact decoder) >= 1-beta_t-beta_n,
    Pr(return an incorrect decoder) <= beta_n,
    Pr(return UNKNOWN) <= beta_t+beta_n.

The last two upper bounds are conservative. They do not assert zero semantic
error: a wrong decoder can be returned on the majority-error event. Fresh
uniform learner draws must retain the source theorem's sampling contract; no
independence between the final erasure and noise events is used. Total physical
comparison calls are at most `r B`, with majority processing, input transmission,
noise calibration and other original learner/source resources charged
separately. This is a generic robustness wrapper, not a new decoder primitive
or a proof of optimal noisy-query complexity.

**Necessary exclusion.** Marginal per-repeat error bounds alone do not justify
amplification. For example, independently for a query choose a latent coin
which is bad with probability `1/2-rho`; when bad, return the wrong answer on
every repetition, and otherwise return the correct answer on every repetition.
Every repeat has the required marginal error, but every majority remains wrong
with probability `1/2-rho`, regardless of `r`. The full-history conditional
bound fails after the first repeat reveals the latent answer pattern. Arbitrary
adversarial bias, correlated systematic errors and insufficient repeat access
remain outside the claimed compilation.

## Scope of this review

Both consequences have direct proofs under the stated interfaces. This review
does not clear novelty, assess a real physical comparison source, certify the
whole evidence archive, or make a civilization-level capability claim. The
recognition obstruction is a general comparison decision-tree argument applied
to this class; the noise wrapper is standard majority amplification with an
adaptive conditional concentration bound.
