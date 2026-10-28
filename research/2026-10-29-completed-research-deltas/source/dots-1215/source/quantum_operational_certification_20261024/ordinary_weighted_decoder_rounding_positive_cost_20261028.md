# Weighted decoder leverage: a positive-cost reduction and a rounding trap

28 October 2026. Exact algorithmic interface following the received generic k^6 learner. This does NOT yet improve its dimension exponent.

## 1. The actual primary rounding theorem inspected

Naor, Regev and Vidick, *Efficient Rounding for the Noncommutative Grothendieck Inequality*, Theory of Computing10(2014), pp.257–295, was inspected directly: https://theoryofcomputing.org/articles/v010a011/v010a011.pdf . Theorem1.1 gives constant-factor polynomial rounding for bilinear forms on orthogonal/unitary matrices; Section3.2 treats Hermitian contractions, and Proposition5.1 accommodates direct sums of matrix variables. These are established powerful ingredients. They do not directly impose the decoder partial-trace equality, its positive affine slice, or a varying positive denominator. No transfer to our full weighted decoder problem is asserted from their names alone.

## 2. Every admitted affine denominator has a positive matrix-cost representation

Fix an encoder x and the interior decoder body

    K_s={C>=(s/2)I, Tr_out C=I_k}, 0<s<1,
    C=s C_0+(1-s)D,  C_0=I/2,
    D>=0, Tr_out D=I_k.

Let u(C) be a KNOWN real affine function, globally certified u(C)>=tau>0 on K_s, as in the received affine-envelope learner. Absorb its scalar constant into the coefficient of Tr D=k, and write

    u(s C_0+(1-s)D)=Tr(U D),                              (1)

for an explicitly known Hermitian U. It need not itself be positive.

The ordinary full-decoder SDP dual is

    m_*=min_(D>=0,Tr_out D=I) Tr(U D)
        =max_Y {Tr Y: U-Y tensor I_2>=0}.                 (2)

Both sides have strict feasible points, and m_*>=tau. Thus an optimal dual Y gives

    W=U-Y tensor I_2>=0,
    u(C)=m_*+Tr(WD).                                     (3)

For a finite rational construction it suffices to find a dual-feasible Y with Tr Y>=tau/2. Then the EXACT identity becomes

    u(C)=m+Tr(WD),  W>=0, m>=tau/2.                      (4)

Standard certified decoder-SDP arithmetic attains this with objective debit at most tau/2. It has no hidden source-conditioning parameter. Indeed Y tensor I<=U implies lambda_max(Y)<=||U||. Combined with Tr Y>=tau/2, this bounds lambda_min(Y)>=tau/2-(k-1)||U||, hence ||Y||<=k||U||. A bounded dual domain and the strict point Y_0=-(||U||+1)I give polynomial outer/inner radius bounds; inward mixing or a scalar downward shift pays the final exact PSD rounding. Since U in the received learner has polynomial coefficient magnitude and bit length, this is a polynomial classical step.

Equation(4) is a CLASSICAL optimization representation. It is not a free physical measurement of W, a source-whitening map or an acquired channel. All returned source actions must still be actual feasible CPTP decoders.

## 3. A useful sufficient rounding contract

Let N(D)>=0 be the positive quadratic numerator of a leverage objective, and write its cost using(4). Suppose a candidate SDP relaxation and rounding construction were proved to produce actual feasible decoder matrices D_round with

    E N(D_round)>=alpha S,
    E D_round <= beta D_bar  (Loewner order), beta>=1.     (5)

Here S is a justified relaxation numerator benchmark and D_bar a specified feasible mean reference. Then positivity of W gives

    E u(C_round)<= beta[m+Tr(W D_bar)].                   (6)

Consequently at least one rounded feasible decoder has

    N(D_round)/u(C_round)
      >= (alpha/beta) S/[m+Tr(W D_bar)].                  (7)

A mean-preserving rounding is a special case beta=1. For the design's fixed positive leverage threshold, a finite repeat/selection bound would additionally follow from explicitly bounded numerator/cost and a positive expected margin; it is NOT supplied merely by existence in(7). No such relaxation/rounding satisfying(5) is proved here. Equations(4)–(7) identify the missing useful interface: preserve a positive cost as well as numerator value, and return feasible CPTP matrices, not unconstrained contractions.

## 4. Constant interior shrinking destroys the needed weighted guarantee

There is an exact failure already at k=2. Let the true source be the identity qubit channel. Its ordinary error-bit mean is q(C)=(2/3)ell(C). For the identity decoder C_Id=2Phi and the replacement C_0=I_4/2,

    q(C_Id)=0, q(C_0)=1/2.

The feasible interior decoder C_s=(1-s)C_Id+s C_0 has q(C_s)=s/2. Take the positive affine denominator

    u(C)=tau+q(C),

and constant positive quadratic numerator N(C)=1=(Tr C/2)^2. Then

    N(C_s)/u(C_s)=1/(tau+s/2).

If an operator-contraction rounding is repaired by a FIXED shrink toward C_0,

    C'=t C_s+(1-t)C_0, 0<t<1 fixed,

its ratio is

    N(C')/u(C')=1/[tau+(1-t+t s)/2]<=2/(1-t).             (8)

The ratio of achieved to original leverage tends to zero as tau+s->0. The same issue occurs with centered linear numerators, whose squared values shrink by t^2 while the loss floor becomes constant. Thus a constant-factor numerator approximation followed by constant interior mixing is not a constant-factor weighted leverage approximation.

This is an obstruction to THAT REPAIR, not an optimization-hardness result: the one-coordinate example itself is solved by the ordinary linear decoder SDP. The received k^6 coordinate method avoids the trap by optimizing each fractional coordinate directly over the EXACT feasible decoder body. No change to its received source or guarantees follows from this note.

The equally informed conventional learner has the same mathematical tools. The next rate problem remains a stronger feasible weighted-quadratic decoder oracle or a matrix-valued confidence method, with an actual source/control budget; random projection, an unweighted Grothendieck citation or an unproved mean-preserving rounding is not that theorem.
