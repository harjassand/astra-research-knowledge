# Weighted spectral tails and positive clipping

Astra Pro1 Cycle9, distinct constructive contribution. 22 October 2026.

## Scope

This contribution starts from the actual Cycle7 endpoint operator, as used in
Cycle8 `NONLINEAR_ENDPOINT_RESPONSE.tex`. It does not repeat its nonlinear
response theorem. The new fact is a dimension-independent weighted spectral
tail bound on the **scale k**, although the operator norm can be much larger.
It gives a positive input repair whose error is paid in the full bath-operator
drift. The parent proof chooses the actual temporal scale and carries the
inherited root/coding theorem through.

## 1. Abstract endpoint-moment lemma

Let the input space have binary charge-pattern projections P_x, x in {0,1}^k.
Let sigma be a density diagonal in these charge sectors. Suppose

* H = sum_{i<j} H_ij is Hermitian;
* ||H_ij|| <= 2;
* P_y H_ij P_x vanishes unless y = x xor e_i xor e_j.

For the actual source these properties hold: H_ij connects 01 and 10 at its
two endpoints, and its color block is P(I-SWAP), P/2 or zero. No tensor-product
locality in the spectator colors is required.

For every integer p >= 0,

    Tr(sigma H^(2p)) <= (4p-1)!! k^(2p),                (1)

with (-1)!! = 1. Consequently, for 0 <= t < 1/(2k),

    Tr(sigma cosh(tH)) <= 1/(1-4t^2 k^2),              (2)

and

    Tr(sigma exp(|H|/(4k))) <= 8/3.                    (3)

If H commutes with sigma, this is the exponential moment of its ordinary
sigma-weighted spectral distribution. Even without that commutation the
spectral measure B -> Tr(sigma 1_B(H)) is positive and the same tail holds:

    Tr(sigma 1_{|H|>u}) <= (8/3) exp[-u/(4k)],         (4)

    Tr(sigma (|H|-u)_+) <= (32k/3) exp[-u/(4k)].       (5)

### Proof

Expand H^(2p). A product with a nonzero input diagonal block must flip every
charge bit an even number of times. Thus every vertex of its ordered sequence
of 2p unordered endpoint edges has even degree. Orienting those edges produces
2^(2p) ordered endpoint strings, each of length 4p. Every even-multiplicity
endpoint string admits a pairing of equal labels. There are (4p-1)!! perfect
matchings of 4p positions, and at most k^(2p) assignments of vertex labels to
the matched pairs. This overcounts even-multiplicity strings, which is harmless.
Therefore the number of potentially nonzero edge products is at most

    (4p-1)!! k^(2p) / 2^(2p).

The trace of each product has absolute value at most its operator norm, hence
at most 2^(2p). Taking absolute values in the expansion proves (1). Possible
color permutations and noncommutation of different H_ij do not affect either
argument. Odd signs of individual traces are also harmless.

Now

    (4p-1)!!/(2p)! = binom(4p,2p)/4^p <= 4^p.

Insert (1) in the nonnegative even power series for cosh to obtain (2).
Spectral calculus gives exp(t|H|) <= 2 cosh(tH); put t=1/(4k) to get (3).
Markov's inequality gives (4). Integrating (4) from u to infinity gives (5).
All statements hold for each finite k without an asymptotic interchange.

### Essential premise and counterexample

Total-charge preservation alone does not imply (1). On k qutrits take the
actual sigma, put Z_1 = (|1><1|-|2><2|) on the first qutrit, and assign
H_ij = 2 Z_1 to every pair label. These operators are Hermitian, commute with
charge and sigma, have norm two and zero sigma mean, but do not flip their
named endpoint charge bits. Their sum is 2 binom(k,2) Z_1, with

    Tr(sigma H^2) = 2 binom(k,2)^2,

which exceeds 3 k^2 already at k=6. The endpoint-parity condition, not merely
charge preservation or a list of pair labels, is load-bearing.

## 2. A full-operator positive-repair interface

Correction incorporated from the integrated review: the generic reference must
also obey [sigma,Q]=0 for the charge-preserving conclusion. This was always
true of the actual sigma=f(Q). The main proof gives the B=I counterexample
if the premise is omitted; no operational constant changed.

Write A = Q-k/2, ||A|| <= k/2. Suppose sigma is faithful, [sigma,Q]=0,
[sigma,Z]=[Q,Z]=0,
Z=Z*, Tr(sigma Z)=0. The affine trial rho_lin=sigma(I+Z) need not be positive.
Assume its exact bulk drift satisfies

    D_b(rho_lin) <= -kappa I,      kappa>0.

The bounded physical displacement has norm at most k. Define

    barZ = clip(Z, -r, r),    W = barZ-Z,
    epsilon = Tr(sigma |W|),  mu=Tr(sigma barZ),
    rho = sigma(I+barZ)/(1+mu),

where 0<r<1 and epsilon<(1-r)/2. Then rho is a faithful normalized input
density preserving charge, and |mu|<=epsilon. This is input-only spectral
calculus: no analytic bath-prefix state is physically prepared.

Its exact bulk drift obeys

    D_b(rho) <= -(kappa-k epsilon)/(1+epsilon) I       (6)

whenever k epsilon < kappa. Indeed, linearity gives numerator
D_b(rho_lin)+D_b(sigma W); the second term has norm at most k epsilon.
The positive denominator lies between 1-epsilon and 1+epsilon. This is an
operator-norm statement on the entire prefix, not an averaged-prefix estimate.

Let

    M=Tr(sigma Z A),      V=Tr(sigma Z^2),

and suppose M-k epsilon/2 >= 0. Then, with logarithms in bits,

    S(rho)-3k/2 >= (M-k epsilon/2)/(1+epsilon)
                  - V/[2 ln(2)(1-r-2epsilon)(1-epsilon)].       (7)

Here the entropy baseline uses the actual sigma, -log2(sigma)=k+Q.

### Proof of (7)

Put Z'=(barZ-mu)/(1+mu), so rho=sigma(I+Z'), Tr(sigma Z')=0. Since clipping
contracts absolute values, Tr(sigma barZ^2)<=V. Therefore

    Tr(sigma Z'^2) <= V/(1-epsilon)^2,
    ||Z'|| <= r'=(r+epsilon)/(1-epsilon) < 1.

For |z|<=r', Taylor's integral remainder for
g(z)=(1+z)ln(1+z)-z gives g(z)<=z^2/[2(1-r')]. Joint spectral calculus of
sigma and Z' gives the stated relative-entropy upper bound. Also

    Tr(rho A) = [M+Tr(sigma W A)]/(1+mu)
               >= (M-k epsilon/2)/(1+epsilon).

The exact identity S(rho)-3k/2 = Tr(rho A)-D_2(rho||sigma) proves (7).
No continuity bound with a dimension factor and no assumption that rho_lin is
positive is used.

## 3. Specialization to the actual Cycle8 trial

Let ell=ln 2, c=ell/2, v=v_k, m=3ell v/16 and b=beta^2. The preserved trial is

    Z = -c b H + (4m/k)b^2 A.

It commutes with sigma and Q and has zero mean. Its exact charge and square
moments are

    M=m b^2,
    V=ell^2 v b^2/4 + 9ell^2 v^2 b^4/(64k).

Let eta=2m b^2=3ell v b^2/8. Because H and A commute, ordinary joint spectral
calculus gives |Z| <= c b |H| + eta. For any r>eta, (5) yields the explicit
two-sided clipping cost

    epsilon <= (32 c b k/3)
                 exp[-(r-eta)/(4 c b k)]
             = (16 ell b k/3)
                 exp[-(r-eta)/(2 ell b k)].             (8)

This exponential smallness is available when b k is small, even if b k^2
is large. Clipping introduces higher endpoint coherences, but (6) charges
their entire physical response by a trace-norm error. It therefore does not
misapply the Cycle8 pair-supported lemma to a nonlinear function of H.

The inherited pair-supported response is used **only for rho_lin**, where it
is exact. Equations (6)--(8) provide the missing positive-input bridge. A
complete operational theorem must still pick actual k(beta), establish the
numerical margins in (6) and (7), and invoke the exact root-retaining coding
theorem. Those tasks remain with the scientific owner; this contribution alone
does not assert a final capacity exponent.

## 4. Independent check of the owner's simpler positive-part repair

The owner subsequently chose a smaller linear coefficient and a positive-part
repair. This removes the need for two-sided clipping or a cubic entropy Taylor
remainder. The following independently checks that interface.

Let ell=ln 2, gamma=ell/4, m=3ell v/32, and

    L = I - gamma b H + (4m/k)b^2 A,    rho_lin=sigma L.

Then E_sigma L=1. Define L_+=max(L,0), L_-=max(-L,0),

    epsilon=Tr(sigma L_-),     rho=sigma L_+/(1+epsilon).

This is a normalized positive, charge-preserving density. It may have zero
eigenvalues; its rank is rank(L_+) <= 3^k, not automatically 3^k. The inherited
type/compression theorem permits this and uses only positive eigenvalues.

For f=L_+/(1+epsilon),

    Tr(sigma(f-1)^2)=Tr(sigma f^2)-1
       <=Tr(sigma L^2)-1=Tr(sigma(L-1)^2)=V.

Here L_+^2<=L^2 in spectral calculus and (1+epsilon)^2>=1. The elementary
global scalar inequality f ln f-f+1 <= (f-1)^2, for every f>=0, follows
from ln f<=f-1 (and continuity at f=0). Since rho commutes with sigma,

    D_2(rho||sigma) <= V/ell,
    S(rho)-3k/2 >= (M-k epsilon/2)/(1+epsilon)-V/ell,       (9)

where

    M=3ell v b^2/32,
    V=ell^2 v b^2/16+9ell^2 v^2 b^4/(256k).

The exact bulk response of the signed comparison is

    D_b(rho_lin)=gamma b^2(1-b)[(3v/4)I-F_k(b)].

If r=bk<=1/64, the actual Cycle8 bound gives F_k(b)>=(7v/8)I, and hence
D_b(rho_lin)<=-kappa_0 I with kappa_0=ell v b^2(1-b)/32.
The actual positive density has the exact full-prefix bound

    D_b(rho) <= -(kappa_0-k epsilon)/(1+epsilon) I.        (10)

Again this follows directly from the physical displacement norm <=k;
no unsupported pair decomposition of the nonlinear positive part is assumed.

For the tail, the diagonal correction has norm
eta=2m b^2=3ell v b^2/16. Whenever eta<=1/2, joint spectral calculus gives

    L_- <= gamma b (H-1/(2gamma b))_+.

Using (5), with a one-sided tail bounded by the two-sided tail,

    epsilon <= (8ell/3) r exp[-1/(2ell r)].               (11)

This precisely matches the owner's proposed repair bound.

### Uniform scalar margins proposed by the owner

For 0<b<=1/256, put T=ln(e/b) and k=floor[1/(16 b T)]. Then k>=2,
k>=1/(32 b T), and r=bk<=1/(16T)<1/64. The exponential in (11) obeys

    exp[-1/(2ell r)] <= exp[-8T/ell] <= exp[-8T] <= b^8
                    <= 3b/65536.

The last step follows from b^7<=2^-56<3/65536; it is not a numerical fit.
Since v>=k^2/32, (11) therefore implies

    epsilon <= ell v b^2/(256k).                        (12)

For clarity, this sufficient scalar comparison has far more margin than
needed. Write B=ell v b^2. Since v<=k^2/8 and r<=1/64, B<=2^-15 and
epsilon<=B/(256k)<=2^-24. Also eta<=3ell r^2/128<1/2.

The following intentionally loose rational margins make the entropy check
transparent. From (12),

    M-k epsilon/2 >= 47B/512,
    1/(1+epsilon) >= 16/17,
    V/ell <= B(1/16+1/512)=33B/512.

The last bound uses v b^2/k <= br/8 <= 1/131072 < 1/18. Therefore (9) gives

    S(rho)-3k/2 >= B(47/544-33/512)=191B/8704 > B/64.

For (10), using 1-b>=1/2 and epsilon<=1/16 gives an inward magnitude at
least (3B/256)(16/17)=3B/272>B/128. Thus a safe exact physical bulk drift
certificate is D_b(rho)<=-(B/128)I. The finite-root coding obligation is
unchanged and is handled in the owner's complete theorem.

These inequalities independently validate the proposed rate arithmetic:

    [S(rho)-3k/2]/k >= ell b^2 k/2048
                    >= ell b/[65536 ln(e/b)].

This contribution establishes the finite-input and exact-bulk interfaces;
the final communication statement additionally uses the preserved root and
arbitrary-reference coding proof, not a fresh-bath approximation.

## Source and evidence

Read actual Cycle8 main proof, especially its endpoint norm, nonlinear response,
positive trial and the four-endpoint counterexample. The endpoint three-case
normal form and scalar susceptibility certificate are inherited from the exact
Cycle7 source. The new moment and clipping arguments above are elementary finite
dimensional proofs. No numerical fit or finite-check count proves them.

Observed derivation/review cost is not metered. Any executable checks are
diagnostics of elementary arithmetic only, not discovery-cost measurements.
