# A condition-number-free arbitrary-reset receiver for W3

This independently derives the producer's weak-reset bound and strengthens
its admissible cone. It is a finite-dimensional mathematical receiver for
the displayed Choi family, not unrestricted W3 contraction, CLR Conjecture4.5,
a physical channel acquisition or a historical-priority claim.

## 1. Conventions and theorem

A,B are qutrits and L is any finite logical register. Put

    Omega=sum_(i=0)^2 |i,i>,    P_Omega=|Omega><Omega|,
    p=P_Omega/3,               p_-=(I-F_swap)/2,
    W3(Z)=[Tr(Z)I3-Z^T]/2,
    N=W3_A tensor id_(BL),     E(Z)=I_A/3 tensor Tr_A Z,
    f(Z)=Tr Z log Z,           f(0)=0,
    Delta(Z)=f(Z)+f(EZ)-2f(NZ).

Logs are natural. Delta is homogeneous: all scale-log terms cancel because
E and N preserve trace. For C>=0, C!=0 on L and Y>=0 on B tensor L, define

    X=P_Omega tensor C+I_A tensor Y,       T=TrY.

**Receiver.** If

    Y <= (I_B tensor C)/192,                              (R)

then

    Delta(X) >= (869/2592) T > T/3       when Y!=0.        (1)

At Y=0, Delta(X)=0. No condition number, reference-dimension factor, reset
rank, logical multiplicity, commutation or Schmidt-basis restriction occurs.
For C>0, the unweighted sufficient condition ||Y||<=lambda_min(C)/192
also works, but (R) is strictly more useful for nonflat C. Singular C is
allowed only with the support alignment forced by (R).

More generally, if 0<eps and Y<=eps(I_B tensor C), then

    Delta(X)>=T F(eps),
    F(eps)=(4/3)log(1/eps)-2log(1+eps)
                 +4/3-(44/3)log3+12log2.                 (2)

The constant192 is convenient and conservative, not an optimal threshold.

## 2. Pinching loss with the actual outcome probabilities

For a projector P, Q=I-P and H>=0, let

    Phi_P(H)=PHP+QHQ,
    c_P(H)=f(H)-f(PHP)-f(QHQ)=D(H||Phi_P H).

The equality holds because log(Phi_P H) is block diagonal. Thus c_P>=0.
Joint convexity and homogeneity of relative entropy imply

    c_P(A+H)<=c_P(A)+c_P(H).                              (3)

If A is supported on P, then c_P(A)=0. One must use (3) before bounding
coherence; bounding c_P(A+H) by its total trace would charge a nonvanishing
main-state error at Y0 and destroy the receiver.

For t=Tr(PH)/TrH, the sharper dimension-free bound is

    c_P(H)<=TrH h2(t),
    h2(t)=-t log t-(1-t)log(1-t).                         (4)

Proof: normalize H and use the isometry U=P tensor|0>+Q tensor|1>. Its
system marginal is Phi_P(H/TrH), its binary marginal is diag(t,1-t), and
its joint entropy is S(H/TrH). The entropy triangle inequality gives
S(system)-S(joint)<=h2(t). This triangle inequality follows directly by
purifying the joint state and applying subadditivity to the complement.
No reference-dimension continuity estimate enters (4).

## 3. Compression and supported increments

The compression inequality needed here is

    f(PHP)<=Tr[P H log H].                               (5)

It is valid for t log t, including zero eigenvalues. An explicit proof uses
log x=integral_0^infinity[(1+t)^(-1)-(x+t)^(-1)]dt. The difference between
P(H log H)P and (PHP)log(PHP), on range P, is

    integral_0^infinity t [P(H+tI)^(-1)P
                            -(PHP+tP)^(-1)]dt >=0.

The inverse-compression inequality follows from the positive Schur
complement; positive regularization gives the semidefinite case. Taking
the trace proves (5). This is the ordinary Davis/Jensen compression step,
shown explicitly so no scalar Jensen or commutation assumption is hidden.

Combining (5) and the definition of c_P gives

    f(QHQ)>=Tr[Q H log H]-c_P(H).                         (6)

For A positive definite on range P and K=PHP,

    f(A+K)-f(A)=integral_0^1 Tr[K(1+log(A+tK))]dt.         (7)

Consequently the tangent lower bound uses log A. If A+tK<=a A, log
monotonicity gives an upper bound using log A+log a. K need not commute
with A. This observation avoids replacing log C by global log m/log M.

## 4. Qutrit bookkeeping, with noncommuting log C retained

First suppose C>0. Set

    A0=3p tensor C,       H=I_A tensor Y,       D=I_B tensor C,
    L_C=Tr[Y log D],      f_Y=TrYlogY.

The exact channels give

    N A0=p_- tensor C,    E A0=I_AB/3 tensor C,
    NH=EH=H,             Delta(A0)=0.

The last equality follows directly from the spectra: f(A0)=3f(C)+3TrC log3,
f(EA0)=3f(C)-3TrC log3 and f(NA0)=3f(C).

Partial traces of p,p_-,I-p and I-p_- give

    TrH=3T,       Tr[(p tensor I)H]=T/3,
    Tr[(p_- tensor I)H]=T,
    Tr[(I-p)tensor I H log H]=(8/3)f_Y,
    Tr[(I-p_-)tensor I H log H]=2f_Y.                     (8)

The corresponding log C traces on the p, full and p_- supports are L_C/3,
3L_C and L_C. These identities hold for arbitrary coherent Y: the projectors
act on AB, log C acts on L, and no Y/log C commutation is assumed.

The two pinching probabilities are therefore1/9 and1/3. Write

    a=3 h2(1/9),    b=3 h2(1/3).

For X, pinch with p, use nonnegative coherence, then (6) and (7):

    f(X)-f(A0)
      >=(T/3)(1+log3)+L_C/3+(8/3)f_Y-aT.                (9)

The E source is full rank, so its tangent gives

    f(EX)-f(EA0)>=3T(1-log3)+3L_C.                     (10)

For N, its support P=p_- tensor I has

    P H P<=eps P(I_AB tensor C)P,
    P(NA0+H)P<=(1+eps)(p_- tensor C).

Using (3), the tangent upper from (7), and (5) on the kernel block gives

    f(NX)-f(NA0)
      <=T[1+log(1+eps)]+L_C+2f_Y+bT.                  (11)

Adding (9)+(10)-2(11),

    Delta(X)>=(4/3)(L_C-f_Y)
       +T[4/3-(8/3)log3-2log(1+eps)-a-2b].            (12)

The crucial term is the exact weighted entropy L_C-f_Y. There is no global
M/m loss. This is not a nonunitary filter of X, nor an assertion that Delta
is invariant under congruence; it is a bound on the original unfiltered source.

Since Y<=eps D, log monotonicity gives

    TrY(log D-logY)>=T log(1/eps).                      (13)

For singular Y one can use Y+delta I<=(eps+delta/m)D with any positive
minimum eigenvalue m of C, multiply by Y, and let delta decrease to zero.
Here m only establishes a limit; it creates no receiver constant or input
condition-number penalty.

Finally

    a+2b=3h2(1/9)+6h2(1/3)=12log(3/2).

Substitution into (12) proves (2).

## 5. Exact rational radius

At eps=1/192, (2) becomes

    F(1/192)=20log2-(40/3)log3+4/3-2log(193/192).

The elementary log series gives log2>=56/81 (retain its first two positive
terms) and log3<=10/9 (bound all tail denominators after the first by3).
Also log(193/192)<=1/192. Hence

    F(1/192)>=28/81-1/96=869/2592=1/3+5/2592.

No matrix-logarithm computation or numerical entropy tolerance is needed
to receive an exact operator-order certificate for (R).

If C is singular, positivity and Y<=eps(I_B tensor C) force Y to annihilate
B tensor ker C, including all cross terms. Compress L to support C; there
C is positive and the same proof applies. This handles arbitrary coherent
reset inside that support, but does not handle leakage into ker C.

## 6. Independent leakage derivation

W3 is self-adjoint in Hilbert-Schmidt duality. With p_sym=(I+F_swap)/2,

    Tr_A p_sym=2I_B,    (p_sym)^(T_A)=(I+P_Omega)/2,
    N*(p_sym tensor I)=(3/4)(I-p)tensor I.               (14)

For C>0 and any fixed H>=0, the singular epsilon log epsilon terms at
A0+epsilon H have coefficients Tr[(I-p)H] at X, zero at E, and
Tr[p_sym NH] at N. Cross blocks affect the O(epsilon) term, not this leading
coefficient. Thus

    Delta(A0+epsilon H)
      =-(epsilon log epsilon)/2 Tr[(I-p)H]+O(epsilon).   (15)

All fixed spaces are finite and the O(epsilon) constant may depend on them,
C and H. Formula (15) is not itself a dimension-uniform radius. If leakage
vanishes, H>=0 is supported on p and merely changes C, giving Delta=0.
For singular C with unrestricted leakage into its kernel, this argument's
kernel bookkeeping changes; only the aligned support case above is received.

## 7. Actual channel and CMI consequence

For R=B0 tensor L, define the CPTP map on a qutrit by

    Lambda(M)=[M tensor C+Tr(M)Y]/(TrC+T).

Both summands are CP, and its trace is TrM. Its normalized Choi state is

    rho_AR=(id tensor Lambda)(P_Omega/3)
          =X/[3(TrC+T)],      rho_A=I3/3.

Let V:A->Q1 tensor Q2 have V_(jk,i)=epsilon_ijk/sqrt2. Exact matrix-unit
calculation shows both complementary channels are W3 with the displayed
transpose: Tr_Q2(V E_ij V*)=Tr_Q1(V E_ij V*)=(delta_ij I-E_ji)/2.
No extra transpose of Lambda is required.

For omega=(V tensor I_R)rho(V* tensor I_R),

    omega_Q1Q2=p_-/3,
    S(omega)=S(rho),
    S(omega_Q1R)=S(omega_Q2R)=S(Nrho),
    S(Erho)=log3+S(rho_R).

Therefore I(Q1:Q2|R)-log3=Delta(rho). Homogeneity and (1) give

    I(Q1:Q2|R)>=log3+(869/7776)p_reset
                     >=log3+p_reset/9,
    p_reset=T/(TrC+T).                                 (16)

Condition (R) also implies p_reset<=1/65, but a small reset probability by
itself does NOT imply (R). This is an unflagged channel-source certificate,
not a measurement of a hidden branch or a device/tomography guarantee.

The infimum defining squashed entanglement ranges over every extension,
not just this receiver class. CLR Conjecture4.5 has a broader quantifier;
the N=3 specialization concerns E_sq(alpha3)=log3/2. See the actual
[v3 primary source, Sec.4](https://arxiv.org/html/1403.3816v3). No such global
infimum, unrestricted W3/N3 result or historical-priority claim follows here.
