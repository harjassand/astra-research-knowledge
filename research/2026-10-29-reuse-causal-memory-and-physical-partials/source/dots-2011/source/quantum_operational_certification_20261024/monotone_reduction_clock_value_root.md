# A monotone reduction-cone clock pays the full entropy integral

27 October 2026. Root construction, independent receiving requested.
The pointwise reduction-cone determinant theorem is an imported, already
received dependency. The moving-primitive argument below is new work in
this programme; historical novelty has not been assessed.

## 1. Abstract finite matrix clock

Work on A tensor L, dim(A)=3, dim(L)=m<infinity. Write

    N=W3 tensor id_L,  W3(T)=(Tr(T) I_3-T^transpose)/2,
    R(B)=Tr_A B,       E(B)=I_3 tensor R(B)/3.

Let H(s)=sum_j M_j/(s+y_j), with finitely many M_j>=0 and y_j>=0.
Set B(s)=s H(s) and R(s)=R(B(s)). Suppose

    B(s)<=I_3 tensor R(s)                                (1)

for every s>=a>0. Define the original Gram-clock kernel

    F_orig(s)=2 logdet(I+N(B(s))/s)
             -3 logdet(I+B(s)/(3s))
             -logdet(I+R(s)/s).

Then both

    I(a)=integral_a^infinity F_orig(s) ds >=0,
    I(a)+a F_orig(a)>=0.                                 (2)

If (1) holds for every s>0, the value assertion extends to a=0.
No commutation of the residues is assumed. This is not a claim that all
matrix Stieltjes clocks satisfy (1).

## 2. Separate a pointwise paid determinant from a moving primitive

The standard entropy determinant kernel of a fixed B is

    F_B(s)=2 logdet(I+N(B)/s)-logdet(I+B/s)
                            -3 logdet(I+R(B)/(3s)).

The received `reduction_criterion_whole_entropy_root_theorem.md` proves
the POINTWISE statement F_B(s)>=0 whenever B<=3E(B), s>0. It follows
by reference normalization of B+sI into the strict cap-three interval.
Using only integrated VALUE, without this pointwise dependency, would
not justify the present argument.

Put

    h_s(x)=log(1+x/s)-3log(1+x/(3s)),
    k_s(x)=3(s+x/3)log(s+x/3)-(s+x)log(s+x)-2s log s.

Direct algebra gives

    F_orig(s)=F_(B(s))(s)+Tr h_s(B(s))-Tr h_s(R(s)),
    partial_s k_s(x)=-h_s(x),
    k_s'(x)=log[(s+x/3)/(s+x)]
           =integral_s^(3s) (x+t)^(-1)dt-log 3.            (3)

Here the prime is the x derivative. The last expression proves that
k_s' is operator antitone on positive matrices. Since k_s(0)=0,

    k_s(x)/x=integral_0^1 k_s'(u x)du

is operator antitone too, with its continuous value at x=0.

Define K_s(B)=Tr k_s(B)-Tr k_s(R(B)). Under (1), operator antitonicity
and Tr_A B=R give

    K_s(B)>=0,
    G_s(B):=k_s'(B)-I_3 tensor k_s'(R)>=0.                 (4)

For the first inequality, multiply the PSD difference between
k_s(B)/B and I_3 tensor k_s(R)/R by B and take the trace. This means
functional calculus with the continuous divided function, not an
inverse of a possibly singular B. For the second use (3) directly.

## 3. The actual clock direction has the correct sign

The Stieltjes representation gives

    B'(s)=sum_j y_j M_j/(s+y_j)^2>=0.

Trace Frechet differentiation is valid without commuting B and B':

    d/ds K_s(B(s))
       =-[Tr h_s(B(s))-Tr h_s(R(s))]+Tr[G_s(B(s)) B'(s)].

Therefore

    integral_a^infinity [Tr h_s(B(s))-Tr h_s(R(s))]ds
       =K_a(B(a))+integral_a^infinity Tr[G_s(B(s))B'(s)]ds
       >=0.                                               (5)

At infinity B(s) is bounded, B'(s)=O(s^-2), K_s(B(s))=O(s^-1),
and G_s(B(s))=O(s^-1). Thus the boundary term vanishes and the
direction integral converges. Equations (1),(4) pay the ACTUAL matrix
direction; this is not positivity of an arbitrary entropy gradient.
Adding the pointwise nonnegative F_B term proves the first assertion.

For the Euler assertion, let

    j_a(x)=x log[(x+3a)/(x+a)].

One has k_a(x)+a h_a(x)=j_a(x)-x log3. Equal traces of B and R cancel
the linear term. Moreover j_a(x)/x=integral_a^(3a)(x+t)^(-1)dt is
operator antitone. Hence

    K_a(B)+a[Tr h_a(B)-Tr h_a(R)]
      =Tr j_a(B)-Tr j_a(R)>=0.

The other terms are the nonnegative direction integral, integral F_B,
and a F_B(a). This proves the second assertion in (2).

For a=0 the finite Stieltjes clock grows at worst as O(1/s), so its
log-determinant kernel is O(1+|log s|) near zero. The integral converges
and is the limit of I(a) as a decreases to zero. No unproved boundary
coercivity or scalar single-crossing property is needed.

## 4. Actual reversible main with low-effective-rank reference reset

Let V:C^3 tensor C^m -> R_out be an isometry, C>=0 on C^m, Y>=0 on
R_out, and a>=0. Use the UNNORMALIZED vector
Omega=sum_{i=0}^2 |i>_A |i>_code, so ||Omega||^2=3. Consider

    Z=(I_A tensor V)(|Omega><Omega| tensor C)(I_A tensor V*)
          +I_A tensor (a I_Rout+Y).                       (6)

The standard Gram determinant/Sylvester identity and the qutrit
antisymmetric complementary isometry give its original entropy kernel
as F_orig for

    H(s)=C0^(1/2) V*(sI_Rout+Y)^(-1)V C0^(1/2),
    C0=I_3 tensor C.                                      (7)

This identity is also the source-native clock used in the earlier
reversible-main and nonwhite Gram interfaces. In particular, the
isometry V is not replaced by a compression of Y before inversion.
Coherent reset-only spectators are retained in (7).

Writing T_s=V*Y(sI+Y)^(-1)V gives

    B(s)=C0-C0^(1/2)T_s C0^(1/2),
    R(s)=3C-C^(1/2)(Tr_code T_s)C^(1/2).

Thus the sufficient condition

    Tr_code[V*Y(aI+Y)^(-1)V]<=2I_m                        (8)

for a>0 ensures R(s)>=C and B(s)<=I_3 tensor C<=I_3 tensor R(s)
for all s>=a. The monotonicity in s follows from functional calculus
of the ORIGINAL Y. At a=0 use the support projection of Y in (8).

In particular rank(Y)<=2 suffices in every ambient dimension: T_s is
a positive contraction of rank at most two, so its partial trace is
bounded by 2I. This is not a bound on the main rank or on m.

The clock identity and (2) therefore prove

    Delta(Z)>=0

for arbitrary reversible mixed-success rank, arbitrary isometric
embedding, and white plus rank-one OR rank-two positive reference reset.
More generally the effective-rank condition (8) suffices. The Euler
payment in the white parameter is nonnegative as well.

For normalized P_Phi=|Omega><Omega|/3, replace C in (6),(7) by C/3.
No trace-one convention is imposed: Delta is homogeneous, and any
normalization uses the trace of the ACTUAL source (6). Singular C and
a=0 follow by finite-dimensional entropy continuity; the low-rank
reset condition and the exact source are preserved.

## Boundaries and dependencies

The result does not cover a general nonwhite reset whose actual clock
leaves the reduction cone, arbitrary nonreversible main operators, or
negative rank-one holes merely by changing a sign. It does not imply a
reference-filter minimum-eigenvalue anchor or a universal one-crossing
kernel, both of which have separate counterexamples.

The only prior sign input is the received pointwise cap-three/reduction
determinant theorem. The scalar antitone identities, positive actual
clock derivative, trace-gradient payment and moving-boundary argument
are explicitly derived above. The actual-source kernel convention and
all finite/singular endpoints require independent receipt before this
candidate is promoted.
