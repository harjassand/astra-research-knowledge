# Constant-TV approximate probability rank cannot supply FPT acquisition

30 October 2026. Unconditional representation theorem. This is NOT a
computational lower bound on every nonlinear learner. It complements the
explicitly conditional PACKED_GUARD_THEOREM.md and uses the same source.

## 1. A nonnegative matrix lemma

Let D_N be the uniform diagonal law on [N]x[N]. If a nonnegative matrix B
has total mass1 and TV(B,D_N)<=eta, then

    rank(B)>=(1-6*eta)*N.                                          (1)

Indeed the diagonal deficit sum_i(1/N-B_ii)_+ is at most eta, and the
total off-diagonal mass is at most eta. Fewer than2*eta*N indices have
B_ii<1/(2N). At most4*eta*N rows have off-diagonal sum>1/(4N). On the
remaining at least(1-6*eta)*N indices the corresponding principal
submatrix is strictly row-diagonally dominant: its diagonal is at least
1/(2N), while its restricted off-diagonal row sum is at most1/(4N).
It is nonsingular. One direct proof is to select a largest-modulus
coordinate of a putative nonzero null vector and compare that row.
No symmetry, PSD, or bounded matrix conditioning is assumed.

## 2. Use the packed source without any cryptography

Fix packing p and let n=p*s grow through its positive multiples, n>=2.
Use the source in PACKED_GUARD_THEOREM Sections2--4 with the public read
schedule1,2,...,n and EVERY permutation the identity. Thus L=n, m=n*s,
all hidden Boolean computation is absent, and q_acc can be chosen0.
The proof of exact cut-logit rank<=d=2p+9 and magnitude<=T is unchanged.
Supply alpha=d*T+1. The source is fully supported and rational.

The first input word X is uniform in{0,1}^n. Every block is scanned at
least once. From the future scan tape extract a word Y by retaining the
FIRST scan of each of the p blocks in order. This is a fixed deterministic
map of the future alone. By the same copy union bound,

    TV(P_(X,Y),D_(2^n)) <=e_n :=m*2^[-2(n^2+1)].                   (2)

In particular e_n<1/64. The output label and all padding can be discarded;
no fact about their distribution is needed for(2).

## 3. Every accurate global surrogate has high probability rank

Let Q be ANY normalized length-T law, with or without full support, and
TV(P,Q)<=1/64. Its marginal joint law B=Q_(X,Y) is within eta=1/64+e_n
of D_(2^n). By(1)--(2),

    rank(B)>=(1-6(1/64+e_n))*2^n > (13/16)*2^n.                   (3)

At the cut after X, let G_Q be the matrix of conditional complete-future
probabilities on positive-probability prefixes; extend zero rows by0.
The joint prefix/future matrix is a diagonal scaling of G_Q. Marginalizing
the future to Y is a column-summing linear map. Therefore

    probability_predictive_rank(Q) >=rank(B) > (13/16)*2^n.         (4)

This applies even if Q was obtained by nonlinear training or has signed
INTERNAL coefficients: its normalized output law is nonnegative, which
is all that the lemma uses. It does not apply to a compact nonlinear
generator whose output probability rank is allowed to be high.

## 4. FPT consequence for this representation route

For the explicit sources above,

    d=2p+9,  alpha=d*T+1,
    log2 T =2n/p+O(log n),                       p fixed.          (5)

For ANY function f and ANY universal polynomial degree c, choose a fixed
p>4c and then let n grow through multiples of p. The lower bound(4)
eventually exceeds f(d)*(T+alpha)^c, by(5). Thus there is NO theorem
which supplies an accurate global surrogate of probability rank

    f(d)*poly(T,alpha,1/epsilon)

for EVERY bounded exact-logit-rank target at fixed epsilon=1/64.
More generally an o(d) degree in T+alpha is impossible by the same
calculation. The lower bound is asymptotic over actual normalized,
constant-TV source laws, not exact-rank discontinuity or tiny singular
values of a Cauchy matrix.

This is also not a benefit conferred by artificial padding: remove the
fair suffix, keep the active horizon T0=poly(n), and supply the same
alpha=d*T+1 bound. Then log2 alpha=2n/p+O(log n), and the identical argument
excludes f(d)*poly(T0,alpha,1/epsilon) probability rank. Padding merely
matches the primary's logit-magnitude<=horizon convention.

## 5. What changes, and what does not

The established probability-rank route of Mausberg Appendix B (and its
finite-alphabet variant in Appendix E) first builds
a consistent low-probability-rank comparison law and then runs the
Liu--Moitra learner. The theorem here shows that no uniformly better
comparison law of FPT probability rank can close the whole target.
Changing the polynomial basis, using a rational approximation before a
linear realization, or fitting the best low-probability-rank law cannot
avoid(4). The source already permits a small explicit nonlinear state
and cheap exact source coins, so this is a limit of the linear output
representation, not an economic difficulty of generating the law.

It does NOT prove a lower bound on the smoothed LOGIT rank, on arbitrary
nonlinear standalone programs, or on native conditional acquisition.
It does NOT turn the cryptographic assumption into an unconditional
FPT impossibility. In particular the copy law is easy when its coordinates
and program are given. An equally informed ordinary nonlinear generator
retains that advantage. The unresolved unconditional acquisition question
must use nonlinear representation or stronger structural/access promises;
the conditional full-law obstruction in PACKED_GUARD_THEOREM gives a
separate reason not to expect such a general operation for free.

## 6. Independent cutwise probability shadows fail too

This also blocks the broader accepted ROOT25 cutwise-width supplier; global
consistency of a surrogate was not essential. At the cut after X let s_X
be ANY nonnegative normalized complete-future rows spanning a common
r-dimensional real vector space, with

    E_(X uniform) ||P(.|X)-s_X||_1 <=eta0.

The rows need not be conditionals of a single sequential law. Form the
joint law by weighting s_X by2^(-n), then extract Y from its future as
before. Its matrix B has rank<=r. Contraction of L1 under that extraction
and(2) give

    TV(B,D_(2^n)) <=eta0/2+e_n.

Therefore(1) yields

    r >=(1-3*eta0-6*e_n)*2^n.                                    (6)

Thus even an independently chosen, distribution-weighted probability-row
span at ONE cut cannot have FPT dimension for these low-logit-rank sources
at a fixed small approximation error. No shadow is queried or granted as
an oracle in this statement. A native nonlinear state can still be compact;
the obstruction is to replacing its future laws by a small linear span.
