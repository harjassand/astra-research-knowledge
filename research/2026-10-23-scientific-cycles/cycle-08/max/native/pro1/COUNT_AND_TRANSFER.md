# Owner derivation: exact collision count and unconditional nonlinear transfer

This is the principal investigator's Cycle7 construction, receiving the
all-length token classification and simultaneous symmetric-prefix minimizer.
The full physical proof is assembled in `SHARP_TEMPORAL_GROWTH.tex`.
The unchanged Cycle6 archive remains the source of the bulk representation,
uniform norms, remainder and actual operator-drift coding interface.

## 1. Exact counting identity

Let `S_n` be a fair nearest-neighbor walk starting at zero, and
`M_n=max_{0<=j<=n} S_j`. Distinct occurrences below are independent.
Reversing the increments shows that the unmatched input-push count after
`i` prefix calls, `S_i-min_{j<=i} S_j`, has law `M_i`. Sign symmetry
shows that the unmatched-pop count in a length-`r` middle also has law `M_r`.
The two walks use disjoint charge bits. The token/dual proof therefore gives

    v_k=(1/2) sum_{i,r>=0, i+r<=k-2}
           [Pr(M_i>M_r)+(1/4)Pr(M_i=M_r)].                 (1)

There are `N=k(k-1)/2` terms. The triangular index set is invariant under
`i<->r`. Put `C=sum_triangle Pr(M_i=M_r)`. Interchanging the two independent
walks gives `sum_triangle Pr(M_i>M_r)=(N-C)/2`, hence

    v_k=k(k-1)/8-C/8.                                    (2)

In particular `C<=N`, so `v_k>=k(k-1)/16>=k^2/32` for every `k>=2`.
This lower bound is already all-length and full-prefix; it does not require
the more precise generating-function evaluation that follows.

Write `p_n(a)=Pr(S_n=a)`. Reflection at the first visit to a level gives

    Pr(M_n=m)=p_n(m)+p_n(m+1),  m>=0.                     (3)

For `m>=1`, subtract the reflection formula
`Pr(M_n>=m)=Pr(S_n>=m)+Pr(S_n>=m+1)` at consecutive levels.
For `m=0`, the same identity follows by sign symmetry. All parities are
included in (3); this avoids replacing the lattice maximum by `|S_n|`.

For `|z|<1` set `D=sqrt(1-z^2)` and `r=(1-D)/z`, with `r(0)=0`.
The walk resolvent (or its nearest-neighbor recurrence) is

    sum_{n>=0} p_n(m) z^n = r^m/D, m>=0.

Consequently `F_m(z)=sum_n Pr(M_n=m) z^n=(1+r)r^m/D`.
The convolution in the two time indices satisfies

    sum_{t>=0} z^t sum_{i=0}^t Pr(M_i=M_(t-i))
      =sum_{m>=0} F_m(z)^2
      =(1+r)/[(1-r)D^2]
      =1/[(1-z) sqrt(1-z^2)].                            (4)

All sums are absolutely convergent for real `0<=z<1`, or valid as formal
power series. Since `1/sqrt(1-z^2)=sum_n p_n(0)z^n`, comparing coefficients
and then summing over `t<=k-2` yields the exact formula

    v_k=k(k-1)/8 -(1/8) sum_{n=0}^{k-2}(k-1-n)p_n(0).    (5)

Here `p_(2m)(0)=binom(2m,m)/4^m`, and odd terms are zero. This is an
aggregate convolution identity. Endpoint contributions are not separately
translation invariant; assigning (5)'s summands to pairs of the same
distance would be false.

For a closed finite expression put `N0=floor((k-2)/2)` and
`a_N=binom(2N,N)/4^N`. The elementary recurrences give

    sum_{m=0}^N a_m=(2N+1)a_N,
    sum_{m=0}^N m a_m=N(2N+1)a_N/3.

Both follow by induction using `a_(N+1)/a_N=(2N+1)/(2N+2)`.
Thus the collision sum in (5) is

    (2N0+1)a_(N0) [k-1-2N0/3].                          (6)

Stirling's formula in (6) gives

    v_k=k^2/8-k^(3/2)/(6 sqrt(2 pi))-k/8+O(sqrt(k)).      (7)

In particular `v_k/k^2 ->1/8` and
`A_k/k^2 ->ln(2)/64`. These are exact restricted variational asymptotics,
not a capacity formula. Initial values are `1/8,1/2,17/16,15/8,185/64`
for `k=2,3,4,5,6`; the proof of (5) does not depend on those checks.

## 2. An explicit analytic optimizer and actual input

Let `zeta_sym=P_sym/(k+1)=integral |u><u|^tensor k du`. The independent
token and dual contributions prove, on the actual finite bulk prefix,

    H=H_(zeta_sym),  Tr(sigma H^2)=v_k,
    T_k(sigma H)=v_k I, ||H||<=k^2, ||G1||<=k^2.          (8)

The matrix H is specified directly by charge-pattern blocks: an input-only
`P(I-SWAP)` when `h>d`, `P/2` when `h=d`, and zero when `h<d`, together
with adjoints. This removes the optimization search, but does not make
the exponentially large matrix or subsequent code efficient.

Let `l=ln2`, `b=beta^2`, `m=3 l v_k/16`, and set

    X=-(l/2)sigma H,
    Y=(4m/k)sigma(Q-k/2),
    rho=sigma+bX+b^2Y.                                  (9)

The prefix density in (8) is a dual variable only. The input (9) is a
finite input density; no bath preparation, control or reachability is used.

The inherited exact bulk expansion and cancellation are

    G(b)=G0+bG1+R_b, ||R_b||<=4k^5 b^2,
    Tr_A[(sigma tensor I)G(b)]=0                         (10)

for `beta<=1/2`. Contract the remainder against `rho-sigma`, not sigma.
For every `k>=2` impose

    b k^4<=delta0=2^-12.                                (11)

The charge/off-diagonal orthogonality gives normalization and
`Tr(QX)=0`, `Tr(QY)=m`. With `Z=sigma^-1(rho-sigma)`,

    ||Z||<=l b k^2<1/2,
    ||X||_1<=l sqrt(v_k)/2,
    ||Y||_1<=3l v_k/(8 sqrt(k)).                         (12)

Therefore rho is strictly positive. The exact leading bulk drift is
`-l v_k b^2 I/8`, using the scalar identity (8). The complete remainder
divided by its magnitude is bounded by

    3 b k^(3/2)+16 b k^5/sqrt(v_k)+12 b^2 k^(9/2)
       <=(3+16 sqrt(32)+12)delta0 <1/2.                 (13)

The first term uses `k>=2`; the second uses `v_k>=k^2/32`; for the third,
`b^2 k^(9/2)=(bk^4)(b sqrt(k))<=delta0`.
Thus the exact bulk drift is at most

    -kappa I,  kappa=l v_k b^2/16>0.                    (14)

The actual finite root region remains in the inherited Lyapunov inequality.

For entropy, `-log2 sigma=k+Q` and the two moments above give
`S(rho)-3k/2=b^2 m-D2(rho||sigma)`. Since `[sigma,Z]=0`, ordinary scalar
Taylor bounds apply in their common eigenbasis. Exactly,

    Tr(sigma Z^2)=l^2 v_k b^2/4+9l^2 v_k^2 b^4/(64k).

The correction to `D2` beyond `l v_k b^2/8`, divided by the intended
gain `l v_k b^2/16`, is at most

    (9/8)b^2v_k/k+||Z||[8/3+(3/2)b^2v_k/k] <1/2.        (15)

This follows from `v_k<=k^2`, (11)--(12), and the bound
`|(1+z)ln(1+z)-z-z^2/2|<=(2/3)|z|^3` for `|z|<=1/2`.
Consequently the same rho with exact inward drift has

    S(rho)-3k/2 >=l v_k b^2/32 >=l b^2 k^2/1024.        (16)

All estimates are uniform in growing k under (11), rather than `O_k`
statements with uncontrolled constants.

## 3. Unconditional operational consequence

For each fixed `0<beta<=2^-8`, choose

    k=floor(beta^(-1/2)/8).

Then `k>=2`, `k>=beta^(-1/2)/16`, and `b k^4<=2^-12`.
The inherited homogeneous-Kraus operator Lyapunov theorem, spectral-type
domination and repaired joint compression now apply to the ACTUAL density
(9). They give one initializer-independent deterministic unassisted code
sequence, pointwise for every fixed normal bath initializer, with vanishing
FULL-diamond error and achievable rate

    Q(V_beta,tau)>=S(rho)/k
       >=3/2+(ln2/16384) beta^(7/2).                    (17)

For the actual tau_pi its repeated-block coherent information tends to the
same S(rho)/k, by the finite bath-entropy argument in the inherited proof.
Beta, k and rho are fixed BEFORE the coding horizon. There is one evolving
bath, no terminal-return promise and no fresh-channel tensor-product claim.

This promotes the previous explicitly CONDITIONAL quadratic transfer to an
unconditional device theorem by proving its missing all-prefix premise.
It improves the asymptotic attainable power `64/17` to `7/2`, not the full
capacity exponent. At beta=1/512 the coarse displayed lower in (17) is
slightly below the preserved pair floor beta^4/1024; that stronger existing
pointwise comparator is retained. No coefficient tuning or finite-angle
dominance over the actual pair/four-call constructions is asserted.

## 4. Continuation and cost boundary

The sharp v_k frontier is resolved in this exact bulk variational problem.
The next selected question concerns the nonlinear transfer for the now
explicit H: determine the true k-dependent contracted remainder
`Tr_A[((bX+b^2Y) tensor I) R_b]`, retaining its full prefix operator norm,
and whether useful exact inward drift survives beyond `b k^4=O(1)`.
The current derivative estimate pays `||R_b||<=4k^5b^2`; its looseness
is a new well-defined bottleneck, not evidence for a better rate exponent.
Any future window must pay positivity, entropy, the root remainder and
the same arbitrary-reference code. No new result is claimed about it here.

The walk calculation and transfer above are analytic. Bounded rational
replays record their own time/memory only. Total discovery, inference and
review costs are unknown. Internal proof/challenge, historical priority,
efficient realization, physical usefulness and delivery are separate.
