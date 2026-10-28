# Polynomial-bit finite receiver for every positive direction

This independently verifies and strengthens the producer's finite positive-
ray theorem. It goes beyond reset directions while remaining local to the
ORIGINAL isometric equality source. It does not prove unrestricted W3 or
permit iteration from an arbitrary previously accepted state.

## Theorem and exact input

Use PROOF.md conventions. Let C>0 act on an r-dimensional logical register,
with certified C>=mI,m>0. Set A0=P_Omega tensor C, P=p tensor I, Q=I-P.
Let H>=0 be ANY density operator on A tensor B tensor L, TrH=1, and let
ell=Tr(QH). If ell=0, positivity forces H into P and Delta(A0+epsH)=0.
For ell>0,

    0<eps<=m ell^2/(2^14 r^2)
       implies Delta(A0+epsH)>=eps ell/2.               (1)

No maximum eigenvalue or condition number is required. The r^2 and ell^2
costs remain explicit. Rational input and a rational certified m give a
rational endpoint and margin with polynomial bit length in the input
bit lengths and log r. Acquisition of H,C and their PSD/order certificates
is not constant cost.

## 1. Supported increments with weighted log C

By homogeneity take m1,t=eps/m,C'=C/m>=I, then write C for C'. Set
R=p_- tensor I, S=I-R, H1=NH and s=Tr(SH1)=3ell/4. The exact dual leakage
identity gives TrPH=1-ell and TrRH1=1-s. H1 is a density operator, hence
0<=H1<=I. Let w=I_AB tensor log C.

Input pinching, its support tangent and scalar convexity on the8r-dimensional
kernel give

    f(A0+tH)-f(A0)>=t(1-ell)(1+log3)+t Tr(PH w)
                      +t ell log t+t ell log[ell/(8r)]. (2)

The E source is full rank, so its tangent gives

    f(EA0+tEH)-f(EA0)>=t(1-log3)+t Tr(H w).              (3)

On the N support, A_N=R tensor-logical C>=R and RH1R<=R. Therefore
A_N+tRH1R<=(1+t)A_N. Operator-log monotonicity bounds the supported log
increment by log(1+t), regardless of the largest eigenvalue of C.

The kernel B=SH1S has trace s, so every eigenvalue is at most s and
f(B)<=slog s. Subadditive pinching coherence gives
c_R(A_N+tH1)<=t c_R(H1)<=t h2(s). Thus the complete upper bound is

    f(NA0+tH1)-f(NA0)
      <=t(1-s)[1+log(1+t)]+t Tr(RH1 w)
                         +t s log t+t s log s+t h2(s). (4)

Keeping the NEGATIVE kernel entropy is essential. Dropping it before the
binary pinching bound creates an unnecessary inverse-leakage precision debt.

## 2. Exact cancellations and finite estimate

Since N*(S w)=(3/4)Qw and N*(w)=w,

    Tr(PH w)+Tr(H w)-2Tr(RH1 w)
       =(1/2)Tr(QH w)>=0.                              (5)

Here C>=I and [Q,w]=0. H need not commute with either. This estimates the
original source; Delta is not presumed invariant under a congruence filter.
Also -2slog s-2h2(s)=2(1-s)log(1-s). Combining (2)+(3)-2(4) gives

    Delta(A0+tH)/t >=(ell/2)log(1/t)-ell log(24r/ell)
       +ell/2+2(1-s)log[(1-s)/(1+t)]
       +(1/2)Tr(QH w).                                 (6)

Using (1-s)log(1-s)>=-s and log(1+t)<=t yields

    Delta(A0+tH)/t >=(ell/2)log(1/t)
                         -ell log(24r/ell)-ell-2t.     (7)

These are finite matrix inequalities. No asymptotic remainder is used.

## 3. Rational radius and bit cost

For t<=ell^2/(2^14r^2),

    (1/2)log(1/t)-log(24r/ell)>=4log2-log3>=14/9.

The last step uses log2>=2/3 and log3<=10/9, proved in PROOF.md. Since
ell<=1,r>=1, 2t<=ell/8192. Formula (7) therefore gives

    Delta/t >=(5/9-1/8192)ell > ell/2,
    5/9-1/8192-1/2=4087/73728>0.

Restoring m proves (1) in the stated UNSCALED units.

If m and ell are rational, the endpoint m ell^2/(2^14r^2) has bit length
O(bits(m)+2bits(ell)+log r), up to ordinary numerator/denominator reduction.
Reading H costs Theta((9r)^2) entries and exact trace/PSD/order qualification
has its usual matrix and arithmetic cost. There is no exponential-in-
inverse-leakage output precision in this receiver. This is a theorem-level
input/precision improvement over the coarse receiver, not an established
runtime separation from an equally informed ordinary matrix method.

## 4. Original finite-ray theorem independently checked

The producer instead bounds the N support by log(2kappa), its kernel entropy
by0 and coherence bylog2. Its three finite inequalities combine exactly to

    Delta/t >=(ell/2)log(1/t)-ell log(24r/ell)-2log(4kappa)
                       +ell/2+(3ell/2)log(2kappa).

The last two terms are nonnegative. For L=ceil_log2(24r/ell),
K=ceil_log2(4kappa), k=2L+ceil(4K/ell)+1, every t<=2^-k indeed gives
Delta>=t ell/3. That theorem is accepted at its stated scope. Formula (1)
strengthens it by retaining weighted logs, binary outcome probabilities and
the small negative kernel entropy.

## 5. Operational and family boundary

When H has a uniform A marginal, normalized
rho=(A0+epsH)/(3TrC+eps) is already a TP Choi state. The antisymmetric
isometry gives the literal extension margin

    I(Q1:Q2|reference)-log3>=eps ell/[2(3TrC+eps)].      (8)

For arbitrary H the A marginal may be nonuniform. An EXPLICIT nine-Weyl
flagged twirl makes it I3/3 and preserves normalized Delta by W3 covariance
and direct-sum homogeneity. Reference dimension grows3r to27r. Those nine
controlled choices and classical labels are not free physical resources.
The mathematical extension then satisfies the same margin (8). No unflagged
correction of a nonuniform marginal is assumed.

For the producer/root's outside-reset-closure point, use r1,C1 and

    H_star=[I9+(E01+E10) tensor diag(1,-1,0)/4]/9.

It has trace1, minimum eigenvalue1/12, Tr_B H_star=I3/3 and leakage8/9.
Formula (1) gives the larger exact endpoint

    eps_star=1/20736,
    Delta(P_Omega+eps_star H_star)>=1/46656,
    CMI-log3>=4/559881.

The source's off-diagonal reference block has square
eps_star^2 diag(1,1,0)/1296 !=0. Reset seeds have square-zero off-diagonal
blocks; the declared closure preserves this under positive scaling, white
addition, reference isometries/direct sums and common-bath operations. Thus
this is beyond that declared reset/bath closure, not merely a larger reset
fixture. It is not an exclusion from every conceivable positive source class.

The receiver still requires the ORIGINAL A0. It supplies no iteration rule
from general accepted states, unrestricted target representation, global
W3/CLR theorem, or acquired physical CMI experiment.
