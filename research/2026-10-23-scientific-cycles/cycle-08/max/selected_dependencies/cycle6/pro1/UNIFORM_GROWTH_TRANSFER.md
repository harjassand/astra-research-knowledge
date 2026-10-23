# Owner construction: uniform susceptibility-to-code transfer

This note is a complete conditional transfer argument. Its finite-dimensional
susceptibility lower premise is being investigated separately; do not read
the conditional conclusion as an unconditional capacity theorem until that
premise is proved. It preserves the Cycle5 same-device coding operation.

## Exact objects and sufficient premises

Let b=beta^2, k>=2, sigma=rho_c^tensor k. Use the exact charge-pinched bulk
G_k(b) from Cycle5. Write G0=(2Q-k) tensor I and G1 its b coefficient.
For a prefix density tau, set

    H_tau=Tr_prefix[(I tensor tau)G1]+(2Q-kI).
    v(tau)=Tr(sigma H_tau^2),  v_k=min_tau v(tau).

H_tau is charge preserving, Hermitian and input off-diagonal, hence
Tr(sigma H_tau)=Tr(sigma Q H_tau)=0. A minimizer exists on the finite
prefix density matrices. The following are the sufficient bounds:

    k^2/32 <= v_k <= k^2,
    ||H_tau|| <= k^2,
    ||G1|| <= k^2.

The last two estimates can be weakened polynomially without destroying the
method. The first lower bound is the substantive unresolved premise in this
working note. The helper's endpoint-pair decomposition is the candidate proof.

Let tau_* minimize v, and put H=H_tau_*. For any prefix density xi,
the first variation of v along xi-tau_* is nonnegative. Thus, for
M=Tr_input[(sigma H tensor I)G1],

    Tr(xi M)>=Tr(tau_* M)=v_k,
    M>=v_k I.

The equality uses input orthogonality to Q and I. This is the complete
operator inequality; it is not a prefix average.

## A uniform remainder from the actual unitary

For W_k(s), every derivative of one factor V_s has norm one, so
||W_k^(r)(s)||<=k^r. With ||Q||=k,
||G^(r)(s)||<=2^r k^(r+1). Charge pinching and bulk compression are
norm contractions. Exact bulk evenness gives

    ||G(s)-G0-s^2 G1|| <= (2/3) k^5 s^4.

For beta<=1/2, s^2<=b/(1-b), s^2-b<=4b^2/3 and s^4<=16b^2/9.
Even the coarse ||G1||<=2k^3 therefore proves

    ||G_k(b)-G0-bG1|| <=4k^5 b^2.                 (R)

The bound is uniform in all bath-prefix vectors. No initializer change or
finite reflecting dynamics is involved. The critical sigma has exact zero
bulk drift at every b, a stronger cancellation than merely G0 cancellation.

## Positive actual density and exact negative drift

Let l=ln 2, v=v_k, choose

    X=-(l/2) sigma H,
    m=3lv/16,
    Y=(4m/k) sigma(Q-k/2),
    rho= sigma+bX+b^2Y.

All factors commute with sigma and Q. Trace rho=1, Tr(QX)=0 and
Tr(QY)=m. Put Z=sigma^-1(rho-sigma). Since ||H||<=k^2 and v<=k^2,

    ||Z|| <=(l/2)b k^2+(3l/8)b^2 k^2 <= l b k^2.

Impose b k^4<=delta=2^-12 and beta<=1/2. Then ||Z||<1/2, so rho is a
strictly positive, charge-preserving actual input density.

The leading drift obeys

    T(X)+2mI <= -(l/2)v I+(3l/8)v I = -lv I/8.

Using (R), ||X||_1<=l sqrt(v)/2, ||Y||_1<=3lv/(8sqrt(k)) and
||G1||<=k^2, the remainder divided by lv b^2/8 is at most

    3 b k^(3/2) +16 b k^5/sqrt(v)+12 b^2 k^(9/2)
    <=(3+16sqrt(32)+12)delta <1/2.

Here b k^(1/2)<=1 follows from the imposed bound. Consequently the
exact bulk drift is at most -lv b^2 I/16. Apply the proved Cycle5
operator-drift coding theorem, including its actual finite root remainder.

## Uniform entropy excess

H and Q commute, and Tr(sigma HQ)=0. Thus

    Tr(sigma Z^2)=l^2 v b^2/4+9l^2 v^2 b^4/(64k).

For |z|<=1/2, the scalar Taylor remainder of
(1+z)ln(1+z)-z-z^2/2 has magnitude at most 2|z|^3/3.
Therefore the correction to D_2(rho||sigma) beyond lv b^2/8 is at most

    9lv^2 b^4/(128k)
      +(2/(3l))||Z||[l^2 v b^2/4+9l^2 v^2 b^4/(64k)].

Dividing by the intended entropy gain lv b^2/16 gives the upper bound

    (9/8)b^2 v/k +||Z||[8/3+(3/2)b^2v/k] <1/2

under b k^4<=2^-12, v<=k^2 and k>=2. Hence

    S(rho)-3k/2 >= lv b^2/32 >= l b^2 k^2/1024.

This rho yields actual reliable rate S(rho)/k by the inherited code,
with its pointwise all-normal full-diamond guarantee. For actual tau_pi,
its product-block coherent-information limit is the same value.

## Conditional improved power

For sufficiently small beta take

    k=floor(beta^(-1/2)/8).

Then b k^4<=2^-12. If beta<=1/256, k>=2 and
k>=beta^(-1/2)/16. The sufficient premises would imply

    Q(V_beta,tau) >=3/2+(ln2/16384) beta^(7/2)

for every fixed normal initializer, using one initializer-independent code
sequence at each fixed beta. The block length is fixed before its horizon;
only the outer small-beta family changes k. No efficient minimizer computation,
useful blocklength or full-capacity order formula follows.

The exact stronger statement currently depends on the all-tau quadratic lower
for v_k. Record its proof or its failure before promoting this conditional
result. Finite scalar-pattern checks alone cannot close that obligation.
