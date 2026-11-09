# Sample-only categorical reuse by rational residual factories

Status: analytic candidate, 9 November 2026. No experiment or implementation qualification. Historical priority and practical leverage are unresolved.

## 1. Contract and result

Let P=(p_i) and Q=(q_i) be fixed distributions on an explicitly encoded finite alphabet [d]. The input is an actual stored X distributed as P. Each subsequent call to either oracle returns a fresh draw from its named distribution, independent of X, all earlier calls and fresh fair bits. Neither probabilities nor density ratios are supplied. An equality test between labels is available. Let s be the cardinality of supp(P) union supp(Q); the algorithm does not need to know s.

For every integer L>=1, the algorithm below terminates almost surely, returns Y with exactly distribution Q, and satisfies

    TV(P,Q) <= Pr(Y != X) <= TV(P,Q) + (1-TV(P,Q))/L.

Its expected number of NEW oracle calls (the supplied X is free) is exactly

    1 + 2 s (L-1).

The expected number of fresh fair bits is exactly 2 s (L-1). This is an expectation guarantee, not a uniform hard stopping cap. All internal operations are equality tests, fair-bit branching, and unit changes of an integer in [0,L]. No approximate real arithmetic occurs.

The same statement applies conditional on an external history H if P_H,Q_H and L_H are fixed conditional on H, X|H has distribution P_H, and all future calls and bits have the stated conditional independence. This does NOT permit selecting Q as an arbitrary function of X while claiming the same fixed-P,Q theorem. Other stored variables may be correlated with X; the joint output coupling is the explicit kernel below, not an arbitrary requested joint law with those variables.

## 2. Executable factory

For a label i, define F(i;U,V,L) as follows. Start an integer Z at 1. If L=1 return UPPER immediately. Otherwise, until Z hits 0 or L:

1. Toss a fresh fair bit.
2. If its value is 0, draw from U; increase Z by 1 if the draw equals i, otherwise leave Z unchanged.
3. If its value is 1, draw from V; decrease Z by 1 if the draw equals i, otherwise leave Z unchanged.

Return LOWER or UPPER according to the boundary hit. This factory is called only with a label having positive probability in its upward oracle.

The reuse algorithm is:

1. Run F(X;P,Q,L). If LOWER, return Y=X.
2. If UPPER, repeat independently: draw J from Q, run F(J;Q,P,L), and return Y=J if UPPER. On LOWER discard this attempt and repeat.

There is no selection based on runtime. When step 1 returns LOWER, its transcript necessarily includes a Q draw equal to X. Thus even retained labels have been observed from the target source. A residual accepted label is itself a fresh Q draw.

## 3. Rational law and exact marginals

For nonnegative p,q with p+q>0, put

    H_L(p,q) = sum_{j=0}^{L-1} p^(L-1-j) q^j,
    r(p,q) = p^L / H_L(p,q),
    s(p,q) = q^L / H_L(p,q).

At L=1, H_1=1. At p=q=0 set r=s=0. The upper-hitting probability of the factory with upward-label probability p>0 and downward-label probability q is

    h(p,q) = p^(L-1) / H_L(p,q).

This follows from the standard finite gambler's-ruin difference equation; holding steps do not change hitting probabilities. It includes q=0 and p=q. The factory has finite expected duration for every such fixed pair since it is a finite absorbing chain with a positive upward probability.

Write r_i=r(p_i,q_i), s_i=s(p_i,q_i). The polynomial identity

    p^L-q^L = (p-q) H_L(p,q)

gives r_i-s_i=p_i-q_i. Therefore

    d_i := p_i-r_i = q_i-s_i >= 0,
    R := sum_i r_i = sum_i s_i = 1-sum_i d_i.

Nonnegativity follows from H_L>=p^(L-1),q^(L-1). For L>=2, one may also write d_i=p_i q_i H_{L-1}/H_L.

Step 1 reaches the residual stage with joint mass p_i h(p_i,q_i)=r_i when X=i. Each residual attempt accepts label j with mass q_j h(q_j,p_j)=s_j. Its acceptance probability is R>0, and its accepted label has law s_j/R. It uses fresh independent randomness, so the complete coupling is

    Pr(X=i,Y=j) = d_i 1{i=j} + r_i s_j/R.

Its row sum is p_i and column sum q_j, including zero-probability coordinates. It therefore gives the asserted exact output law.

In fact R>=1/L. To see this, weighted AM-GM applied to each mixed monomial shows

    (p+q) H_L(p,q) <= L(p^L+q^L).

Hence r_i+s_i >= (p_i+q_i)/L, and summing proves R>=1/L. This inequality is not needed to hide a normalization cost: that cost is explicitly included in Section 5.

## 4. Disagreement bound

Let t=TV(P,Q). Since r_i-s_i=p_i-q_i,

    R = t + sum_i min(r_i,s_i).

If p>=q then H_L>=L q^(L-1), and so s<=q/L. The reversed case is symmetric. Consequently

    R <= t + (1-t)/L.

The actual disagreement is

    delta = R - (sum_i r_i s_i)/R <= R.

Its lower bound delta>=t is the ordinary coupling inequality. At P=Q, the exact formula simplifies to

    delta = (1-sum_i p_i^2)/L.

Thus for a uniform distribution on s labels the excess disagreement is (1-1/s)/L. At L=1 the algorithm simply takes a fresh independent Q sample.

## 5. Exact expected query bill

Let tau(p,q) denote the expected duration in oracle calls of the factory with upward probability p/2 and downward probability q/2. For p>0 and q>=0 it is finite. For p!=q, optional stopping of the bounded-state drift martingale gives

    tau(p,q) = 2 (L h(p,q)-1)/(p-q).

One may justify optional stopping first at a bounded horizon, then use finite mean absorption for this fixed finite chain. For p=q>0, the standard quadratic martingale gives tau(p,p)=(L-1)/p. For p>0,q=0, tau(p,0)=2(L-1)/p. When a multiplier is zero below, its associated weighted duration is defined to be zero; no impossible selected label is run.

For every p+q>0,

    p tau(p,q) + q tau(q,p) = 2(L-1).

For positive unequal p,q this follows by substituting the drift formula and using p h(p,q)-q h(q,p)=p-q. The equal and one-zero cases follow from the explicit formulas above.

Define A=sum_i p_i tau(p_i,q_i) and B=sum_i q_i tau(q_i,p_i). Therefore A+B=2s(L-1). The first stage costs A on average. One residual attempt costs 1+B on average, including its fresh Q proposal; it succeeds with probability R. Even though attempt cost and success are correlated, independent fresh attempts give the first-step identity

    E[complete residual cost] = (1+B) + (1-R) E[complete residual cost]
                             = (1+B)/R.

This is finite since R>=1/L and B is finite. The residual stage is invoked with probability R and is independent of the preceding transcript once invoked. Thus the total expected new calls are

    A + R (1+B)/R = 1+A+B = 1+2s(L-1).

Exactly one fair bit is used in each factory query and none for the Q proposals. The identical argument gives expected fair-bit count A+B. No density evaluation, unknown-probability division, or factory compilation is performed.

## 6. Finite representation, source accuracy and stopping

With labels in [d], auxiliary work memory is O(log d+log L) bits. Per oracle call the local work is O(log d+log L) in a conservative bit model; total expected local bit work is O((1+dL)(log d+log L)), plus the actual charged oracle costs. If either named draw has expected cost at most c uniformly over calls, expected total source work is at most c[1+2d(L-1)]. This assumes each oracle implements its promised distribution exactly, with no runtime-based selective discard.

No finite worst-case call cap is claimed. If a user requires a cap M, stopping after M calls and producing an arbitrary fallback changes the law by at most [1+2d(L-1)]/M in TV by coupling/Markov, but no longer gives an exactly Q-distributed output. The same probability bound controls the change to disagreement. A cap is therefore a separately approximate interface. Large conditional cost when the stored X is a rare label is allowed; only the average over X~P is uniform.

This result does not automatically apply to approximately implemented P/Q oracles as if they were exact. With a coupled per-call source error alpha and a fixed cap M one may add M alpha to TV; an unbounded error ledger requires a separately justified stopping/coupling argument.

## 7. Scope and prior boundary

The construction is not a general atomless sampler, optimal categorical cost theorem, hard-cap optimum, or practical runtime result. It is a finite-alphabet exact-marginal coupling with a uniform expected source-call bill. The fixed-batch empirical-transport comparator and sharp binary reuse law already appear in Astra N1691; classical gambler's ruin, residual maximal coupling and rational Bernoulli factories are established ingredients. Strong-prior comparison is in a separate note. No novelty claim is made here.
