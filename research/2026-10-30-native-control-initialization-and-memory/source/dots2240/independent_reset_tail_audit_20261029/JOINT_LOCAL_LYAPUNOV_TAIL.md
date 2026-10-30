# Joint actual-reset tails from a finite-support killed-generator Lyapunov witness

2026-10-29. This extends the single-owner certificate in `ACTUAL_RESET_INSTRUMENT_TAIL.md`. It closes the spatially separated-owner clean-generator tail; it does NOT provide a data threshold or data-instrument factorization.

## 1. Input and actual killed maps

For each owner h, let J_h(.) be the sum of the gains of its ACTUAL separately recorded terminal/abort reset channels. Let

K_h=L−J_h,  N_h(t)=exp(tK_h).

The preceding finite-rate projected-path certificate gives, uniformly on the FULL Hilbert space,

exp(T K_h*) I ≤ (1−p)I,

with fixed T<infinity and p>0 independent of volume and owner. Take common worst-case constants when local circuits vary within fixed bounds. K_h generates a CP subunital adjoint semigroup. The complete summed designated intensity A_h=J_h*(I) satisfies 0≤A_h≤nu I with fixed nu>0 (indeed nu is the largest terminal/abort rate when their source clock projectors are orthogonal).

Since K_h*I=−A_h≥−nu I, CP comparison gives exp(tK_h*)I≥e^(−nu t)I. Thus the exact integral G_h=int_0^T exp(tK_h*)I dt satisfies

a I≤G_h≤T I,  a=(1−e^(−nu T))/nu,
K_h*G_h=exp(TK_h*)I−I≤−p I.

This exact integral is generally not strictly local. The next construction replaces it by a finite-support polynomial while preserving drift.

## 2. Locality with a nonunital killed term: anchored support

Write K_h* as the sum of bounded finite-range ordinary local Lindblad adjoints plus the modified on-site h term that includes the deleted gains. All ordinary terms annihilate I on their support and consequently annihilate any observable disjoint from that support. The sole nonunital terms are supported at h. Therefore track every intermediate observable on a support that ALWAYS includes the anchor h, even when the observable is initially I. Then all terms disjoint from the tracked support annihilate it, exactly as in the usual connected-interaction expansion.

Let each term have ≤r0 sites and per-site sum of operator-norm bounds ≤J, uniformly over h and volume. Put a_int=max(1,r0−1), C=J a_int. If O has tracked support of s≥1 sites including h,

||(K_h*)^q O||≤C^q(s)_q ||O||,

where (s)_q=s(s+1)...(s+q−1). Indeed at derivative step j the actual union has at most s+j a_int sites; the sum of norms of terms intersecting it is ≤J(s+j a_int)≤C(s+j). Its radius grows by at most q times the interaction range. This bound holds in operator norm and uses no extensive ||K_h||.

For delta C≤1/4, define Q_K(z)=sum_(q=0)^K(delta z)^q/q! and R_K(z)=(Q_K(z)−1)/z. The local Taylor bounds are

||exp(delta K_h*)O−Q_K(K_h*)O||≤2^(s−K−1)||O||,
||int_0^delta exp(tK_h*)O dt−R_K(K_h*)O||≤delta 2^(s−K)||O||.

The slightly loose second estimate covers its shifted truncation index. These follow by bounding binom(s+q−1,q)≤2^(s+q−1), then summing a geometric tail. They are valid for each fixed finite volume with constants uniform in volume. CP-subunital adjoint evolution is operator-norm contractive.

## 3. Arbitrary finite T: telescoping polynomial, not one large Taylor disk

Choose M=ceil(max(1,4CT,T)), delta=T/M, and

eta=min(p/4, a/[4(1+T)], 1/4).

Initialize O_0=I and F_0=0, both tracked on {h}. At stage j choose finite K_j from the currently bounded tracked support s_j, large enough that BOTH Taylor errors above are ≤eta/M and delta eta/M, respectively, for ||O_(j−1)||≤2. Set

O_j=Q_(K_j)(K_h*)O_(j−1),
F_j=F_(j−1)+R_(K_j)(K_h*)O_(j−1).

Induction using contractivity gives ||O_j−exp(j delta K_h*)I||≤j eta/M, hence ||O_j||≤1+eta≤2, justifying the next choice. The support bound at every stage is finite and recursively computable from the fixed local parameters only. It can be astronomically large; no efficiency is claimed.

Crucially, there is an EXACT polynomial telescoping identity:

K_h*F_j=O_j−I.

Thus ||K_h*F_M−K_h*G_h||≤eta, without applying an extensive generator norm to an approximation error. Summing the integral errors and preceding O_j errors gives

||F_M−G_h||≤(T+delta)eta≤(1+T)eta≤a/4.

Every polynomial is Hermitian. Therefore, conservatively, with F_h=F_M,

(a/2)I≤F_h≤(3T/2)I,
K_h*F_h≤−(p/2)I.

Normalize Z_h=F_h/(3T/2), alpha=a/(3T), r=p/(3T). Then Z_h has finite support of a common bounded radius R and

alpha I≤Z_h≤I,   K_h*Z_h≤−r Z_h.

Unlike the bad-projector argument, no invariant projector corner is needed: all approximation errors are bounded relative to I.

## 4. Spatially separated owners: exact product rule

Let S be a set whose Z_h supports are disjoint and buffered enough that EVERY clean local generator term touches at most one such support. Include the monitor and designated reset terms in this support convention. Define Z_S=product_(h in S)Z_h and

K_S=L−sum_(h in S)J_h.

K_S is the actual killed generator for no terminal/abort reset at ANY owner in S. It is CP and trace-nonincreasing. Locality gives the EXACT identity

K_S*Z_S = sum_(h in S)(K_h*Z_h) product_(j in S\{h})Z_j.

Reason: an ordinary local adjoint touching no support annihilates the product; one touching exactly h factors through all other commuting factors. Every deleted gain J_h* is localized inside its own Z_h support and likewise factors through the other factors. Thus no independence of exterior dynamics, and no conditioning on future remote records, is invoked.

Since all complementary factors commute with K_h*Z_h (a term touching two supports was excluded),

K_S*Z_S≤−r |S| Z_S.

CP comparison implies exp(tK_S*)Z_S≤e^(−r|S|t)Z_S. Since alpha^|S| I≤Z_S≤I,

exp(tK_S*)I≤alpha^(−|S|) exp(−r|S|t) I,

and hence

||exp(tK_S)||_diamond ≤ min{1, C0^|S| exp(−r|S|t)},
C0=alpha^(−1)=3T/a.

This is the requested spatially extensive joint actual-no-reset tail, valid for arbitrary entangled initial states and interacting exterior systems. Separation is at the constructed witness radius R plus one generator-range buffer, not merely disjoint original resource sets.

For an arbitrary finite owner set S, bounded geometry gives a buffered subset U with |U|≥|S|/P for a fixed packing number P. Requiring no reset at all of S implies no reset at U, so

||N_S(t)||_diamond≤min{1,C0^|S| exp[−(r/P)|S|t]}.

The prefactor is deliberately weakened from C0^|U| to C0^|S|. This is useful only beyond its fixed onset time; it remains a uniform exponential joint tail.

## 5. Optional perturbations: record must remain real

The clean theorem above is complete under its stated generator hypotheses. A robustness extension is valid ONLY when the same designated reset channels remain actual separately recorded channels of the perturbed physical generator, so that deleting their gains still gives a CP killed instrument. Adding independent local CPTP-kick Lindblad channels is one safe example. An arbitrary Hermiticity-preserving N for which L+N is CPTP does NOT by itself ensure L+N−sum J_h is a valid killed generator. Nominal reset channels cannot be retained as fictional records after an unspecified implementation error.

Under this actual-instrument condition, suppose the added local adjoints annihilate I, have per-Z-support incident norm budget eta_noise, and any added term touches at most b Z supports. A term touching v≤b factors obeys

N_e*(Z_S)≤||N_e*|| alpha^(−v) Z_S≤||N_e*|| alpha^(−b) Z_S.

This uses ||product of touched Z||≤1, then I≤alpha^(−v)product of touched Z; untouched factors commute and factor out. Summing incident budgets gives

(K_S+N)*Z_S≤−[r−eta_noise alpha^(−b)]|S| Z_S.

If that bracket is positive, the same actual-instrument tail holds with the reduced rate. This is a controller-record robustness statement only, not a data-error threshold or a guarantee of reset output quality.
