# A uniform receiver for arbitrary weak quantum resets

This is a new local mathematical construction in this work. Historical
priority and independent acceptance are not asserted. It uses standard
entropy pinching, relative-entropy joint convexity and operator Jensen.
The unrestricted Werner–Holevo contraction/CLR conjecture remains open.

## 1. Exact operation and theorem

Let A and B be qutrits, L a finite r-dimensional logical register, and
Omega=sum_i |i,i> the UNNORMALIZED maximally entangled vector on AB.
Let C>0 act on L and Y>=0 act on BL, with no rank, commutation, product,
Schmidt-alignment or spectral-multiplicity restriction. Define

    X=|Omega><Omega|_AB tensor C + I_A tensor Y,
    N=W3 tensor id_BL, W3(Z)=(Tr(Z)I3-Z^T)/2,
    E=(I3/3) tensor Tr_A,
    f(Z)=Tr Z log Z, f(0)=0,
    Delta(X)=f(X)+f(EX)-2f(NX).

Choose certified scalar bounds

    0<mI<=C<=MI, 0<=Y<=bI, kappa=M/m>=1, T=TrY.

For b>0 the receiver is

    Delta(X)>=T [(4/3)log(m/b)-2log((M+b)/m)
                  +4/3-(8/3)log3-9log2].                 (1)

In particular the rational condition

    b<=m/(512 kappa²)                                    (2)

guarantees

    Delta(X)>=T/3.                                      (3)

If Y=0, Delta=0 exactly. This is a whole arbitrary-reset cone in every
finite reference dimension, including arbitrary nonflat C. It does not pay
large arbitrary resets or singular C with coherently coupled reset support.
The numerical constant is a conservative sufficient condition, not an
optimal reset threshold or a physical noise requirement.

## 2. Standard entropy tools, with all singular terms retained

For an orthogonal projector P, Q=I-P, set

    Phi_P(Z)=PZP+QZQ,
    c_P(Z)=f(Z)-f(PZP)-f(QZQ).

Then

    0<=c_P(Z)=D(Z||Phi_P Z)<=Tr(Z)log2.                  (4)

Pinching gives Z<=2Phi_P Z. Operator monotonicity of log gives the upper
bound; entropy monotonicity under pinching gives the lower bound. Singular
cases follow by the usual support restriction or addition of epsilon I.
Joint convexity and homogeneity of relative entropy give subadditivity

    c_P(A+H)<=c_P(A)+c_P(H).                             (5)

If A is supported on P and positive definite there, c_P(A)=0. Therefore

    f(A+H)>=f(A+PHP)+f(QHQ),
    f(A+H)<=f(A+PHP)+f(QHQ)+Tr(H)log2.                   (6)

For the second inequality (5) was used before the upper bound (4). Using
the pinching bound on A+H directly would leave a spurious Tr(A)log2 term
that does not vanish with the reset and would destroy the receiver.

The operator-convex function t log t has value zero at zero. Its compression
inequality is

    f(PHP)<=Tr[P H log H].                              (7)

Combining (4) with (7) on the complementary block gives

    f(QHQ)>=Tr[Q H log H]-Tr(H)log2.                     (8)

Finally, for m_A P<=A<=M_A P and 0<=PHP<=bP,

    Tr(PH)(1+log m_A)
      <=f(A+PHP)-f(A)
      <=Tr(PH)(1+log(M_A+b)).                            (9)

The lower bound is the supporting tangent of Tr Z log Z. The upper bound
integrates Tr[PHP(log(A+tPHP)+I)] for t from zero to one. These are finite
matrix inequalities, with no continuity estimate whose constant grows
with reference dimension.

## 3. Qutrit source bookkeeping

Write p=|Omega><Omega|/3 on AB, p_-=the antisymmetric projector on AB,
and q_+=I-p_-. Set

    A0=3p tensor C, H=I_A tensor Y,
    N A0=p_- tensor C, E A0=I_AB/3 tensor C,
    NH=EH=H.

The spectra of the three unperturbed terms show Delta(A0)=0: their f(C)
contributions cancel, and the two log3 terms cancel. The relevant masses
and H-log-H traces are exact:

    TrH=3T,
    Tr[(p tensor I)H]=T/3,
    Tr[(p_- tensor I)H]=T,
    Tr[(I-p)tensor I H logH]=(8/3)TrYlogY,
    Tr[(q_+ tensor I)H logH]=2TrYlogY.                    (10)

These follow from Tr_A p=I_B/3, Tr_A p_-=I_B and
Tr_A q_+=2I_B, so they hold for arbitrary coherently oriented Y.

For f(X)-f(A0), use the first line of (6), then the lower bounds (9),(8):

    f(X)-f(A0)
      >=(T/3)(1+log(3m))+(8/3)TrYlogY-3Tlog2.           (11)

The E term is full rank and obeys

    f(EX)-f(EA0)>=3T(1+log(m/3)).                       (12)

For the N term, use the second line of (6), the upper bound (9), then (7)
for its kernel block:

    f(NX)-f(NA0)
      <=T(1+log(M+b))+2TrYlogY+3Tlog2.                  (13)

Equations (11)+(12)-2(13), together with Delta(A0)=0, yield

    Delta(X)>=T[4/3+(10/3)log m-(8/3)log3
                       -2log(M+b)-9log2]-(4/3)TrYlogY.

Since every eigenvalue of Y is at most b,
TrYlogY<=Tlog b, including zero eigenvalues by continuity. This proves (1).

## 4. The rational radius

Under (2), b/m<=1/(512 kappa²) and
(M+b)/m<=kappa(1+1/512). Consequently the bracket in (1) is at least

    3log2+(2/3)log kappa+4/3-(8/3)log3-2log(513/512).

Use log2>=2/3, log3<=10/9, log(1+x)<=x and kappa>=1. The first two bounds
follow directly from log x=2 sum_(j>=0) z^(2j+1)/(2j+1), z=(x-1)/(x+1):
keep the first term for x=2, and bound every denominator after the first
by 3 for x=3. The displayed bracket is at least

    10/27-1/256=2533/6912>1/3,

with exact rational gap 229/6912. This proves (3) without evaluating any
matrix logarithm or choosing a reference-dimension cutoff.

## 5. Operational consequence and what is still missing

Let alpha3=p_-/3 on two qutrits. A minimal purification of alpha3 uses a
third qutrit; applying the channel

    Lambda(M)=[M tensor C+Tr(M)Y]/(TrC+TrY)              (14)

to that purifying qutrit generates a physical extension of alpha3. This
channel succeeds as identity transfer with a mixed logical register of
state C/TrC, or replaces its input by arbitrary Y/TrY, without revealing
a success/reset flag. Its reset probability is

    p_reset=TrY/(TrC+TrY).

The normalized Choi state of Lambda is rho=X/[3(TrC+TrY)]. The antisymmetric
qutrit isometry V has W3 as both complementary outputs, so

    I(Bout:Cout|R)_(V rho V*)-log3=Delta(rho).

Thus (2) proves the concrete conditional-mutual-information margin

    I(Bout:Cout|R)>=log3+p_reset/9.                     (15)

This is a certified class of actual CPTP squashing channels. It needs no
accessible flag, no reset Schmidt basis, no measured bath label, and no
dimension bound on the finite logical register. It does not construct a
physical instrument or acquire C,Y from a device. A channel model and
operator-order certificates are required inputs; tomography, structural
qualification and implementation costs are unacquired.

The missing GLOBAL operation is still Delta(Z)>=0 for every finite qutrit-
reference state Z. Via twirling it would prove
E_sq(alpha3)=log3/2 and the N=3 value in CLR Conjecture4.5. An unbounded
reference and a large/structured reset are not reduced to (2) here.
The family certificate and numerical searches do not decide that conjecture.

## 6. A general boundary identity, beyond reset directions

There is an exact reason for the positive small-reset logarithm. For ANY
H>=0 on ABL, let ell=Tr[(I-p)tensor I H]. The qutrit adjoint identity is

    N*((q_+ tensor I))=(3/4)(I-p)tensor I.                (16)

For fixed C>0 and H, finite-dimensional eigenvalue perturbation at zero
gives

    Delta(A0+epsilon H)
        =-(ell/2)epsilon log epsilon+O(epsilon).         (17)

Indeed the epsilon-log-epsilon coefficient in f(A0+epsilon H) is ell,
the E term is full rank and contributes none, and the N term contributes
-2Tr[(q_+ tensor I)NH]=-3ell/2. The expansion is finite-dimensional,
direction-specific, with fixed C,H; (17) alone supplies no uniform radius.
For H=I_A tensor Y, ell=8TrY/3, agreeing with the leading coefficient
4TrY/3 in (1). If ell=0 and H>=0, positivity forces H to be supported on
p tensor I; this remains a mixed-isometric equality source. The explicit
receiver (1) adds the missing uniform finite radius for arbitrary resets.

## 7. Exact failure of the simplest orbit-curvature shortcut

The attack first tried to mix two orthogonal maximally entangled reset
vectors Phi0=sum_i|i,i>/sqrt3 and Phi1=sum_i|i,i+1>/sqrt3 on BL, r=3.
Let D=I_A tensor(P_Phi0-P_Phi1). On the admissible curve

    X(t)=3p tensor I3+aI27+tD, |t|<a,

the exact second derivative at t=0 is

    K(a)=-1/(3a)+6/(a+1/3)-1/(a+1)
              +(4/9)log(1+3/a)-6log(1+1/a).             (18)

The two projector block calculations behind (18) use

    TrD²=6,
    Tr(PDPD)=0, Tr(PD(I-P)D)=2/3, P=p tensor I3,
    Tr(RDRD)=1/2, Tr(RD(I-R)D)=3/2, R=p_- tensor I3.

The BKM divided difference between eigenvalues a and a+c is
log(1+c/a)/c. Thus the formula is analytic, not a numerical Hessian fit.
At a=1 it becomes 11/3-(46/9)log2. Using log2<=25/36 from the same series
as above proves K(1)>=19/162>0. At a=1/100, drop the two negative terms
-1/(a+1) and -6log(1+1/a), and use log301<log512<9 to obtain

    K(1/100)<-100/3+1800/103+4=-3664/309<0.

Consequently this orbit is not uniformly convex or uniformly concave over
white baseline strength. The positive receiver (1) does not rely on either
false shortcut. This is a restricted structural result, not a negative
Werner–Holevo entropy value.

## 8. The shortest global operational equivalence pays its flag

If unrestricted Delta positivity were proved, all extensions of alpha3
would have CMI>=log3, and the trivial extension attains equality. Conversely,
suppose a finite input rho_AR had Delta(rho)<0. Apply the nine qutrit Weyl
unitaries U_j on A, storing j in a nine-dimensional classical flag F at
the reference. Their exact twirl makes the new A marginal I3/3.

The N channel is covariant under the conjugate output unitary. Each flagged
block has the original deficit, and its classical log9 terms cancel between
f(rho), f(Erho) and 2f(Nrho). Hence the flagged state's deficit is still
Delta(rho)<0. Applying V therefore gives an actual extension of alpha3
with smaller CMI. This finite construction enlarges the reference by a
factor of nine; it does not assume a free classical flag of unbounded size
or invoke a continuum Haar label. Finite Weyl twirling is established
machinery; the equivalence identifies the operational consequence of the
missing global inequality and does not solve it.
