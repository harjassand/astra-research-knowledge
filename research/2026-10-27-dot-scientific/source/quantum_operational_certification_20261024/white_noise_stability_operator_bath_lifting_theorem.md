# Positive spectral-mixture lifting from scalar white noise to a noncommuting operator bath

## Theorem

Let A0>=0 act on physical C3 tensor a finite reference R0. Let N=W3 tensor id_R0 and E=I3/3 tensor Tr_phys, and Delta(X)=f(X)+f(EX)-2f(NX), f(X)=Tr XlogX. Define the scalar white-noise value curve

 h(t)=Delta(A0+t I), t>=0.

For arbitrary positive semidefinite operators B,C on another finite reference bath, put

 A=I tensor B+A0 tensor C.

No commutation between B and C is required. Define the convex scalar function

 q(t)=Tr(t C-B)_+, t>=0.

Then the following EXACT positive-mixture identity holds:

 Delta(A)=q'(0+)h(0)+integral_(0,infinity) h(t) d q'(t).       (1)

The derivative is understood as the monotone right derivative of q, and its Stieltjes derivative is a positive measure. The total weight, including the atom at zero, equals TrC.

Consequently, if h(t)>=0 for EVERY scalar t>=0, then Delta(A)>=0 for arbitrary noncommuting B,C. This is a genuine operator-bath value theorem, not a pointwise determinant claim or a BMV/Mellin positivity premise.

## 1. Common-baseline determinant representation

The maps I,N,E are unital and trace preserving on the fixed base space. Hence every baseline I tensor B is fixed and has zero deficit. Put

 Z_s=C^(1/2)(B+sI)^(-1)C^(1/2), s>0,
 F(z)=2logdet(I+z NA0)-logdet(I+z A0)-logdet(I+z EA0).

Diagonalizing the base matrices separately and using the determinant lemma gives

 Delta(A)=integral_0^infinity Tr F(Z_s) ds.                  (2)

Here F is an ordinary scalar function, applied spectrally to Z_s. The trace-leading cancellation implies F(z)=O(z^2) at zero, while F(z)=O(1+log z) at infinity. Thus the integral is absolutely convergent, including singular B,C. These bounds also justify the changes of integration below.

For a scalar baseline tI on the base space, the same representation gives

 h(t)=integral_0^(1/t) F(z)/z^2 dz, t>0,
 h'(t)=-F(1/t),
 h(infinity)=0, h(0)=Delta(A0).                            (3)

The endpoint h(0) follows by ordinary finite-dimensional entropy continuity.

## 2. Exact spectral counting identity

For z>0, congruence and equality of the nonzero spectra give

 # {eigenvalues of Z_s greater than z}
   = # {positive eigenvalues of C/z-B-sI}.

Integrating this counting identity over s>=0 yields

 integral_0^infinity # {eig(Z_s)>z} ds
   =Tr(C/z-B)_+=q(1/z).                                   (4)

This is the load-bearing step. It uses the actual COMMON resolvent B+sI, not independent arbitrary positive matrices at each s.

The trace positive-part variational formula

 q(t)=max_(0<=P<=I) Tr[P(tC-B)]

shows q is convex. Since C>=0, 0<=q'(t)<=TrC, and q'(infinity)=TrC. The spectral occupation measure in (4) has density q'(1/z)/z^2 almost everywhere, because q is locally absolutely continuous. Therefore (2) becomes

 Delta(A)=integral_0^infinity F(z) q'(1/z)/z^2 dz
         =-integral_0^infinity q'(t) h'(t) dt.              (5)

Stieltjes integration by parts, with bounded q' and the endpoints in (3), proves (1). At derivative jumps the positive Stieltjes measure receives the jump. No differentiation of individual eigenvectors or unsupported operator ordering is used.

## 3. Entire ordered operator-valued two-level family

The acquired all-projector/two-level WH3 theorem states that

 Delta(P+tI)>=0 for every projector P and scalar t>=0

on arbitrary finite qutrit-reference spaces. Applying (1) with A0=P proves

 Delta(P tensor(B+C)+(I-P) tensor B)>=0                     (6)

for every projector P and arbitrary B,C>=0, including noncommuting baths. Thus the two operator levels U=B+C and B may be noncommuting; the order U>=B is substantive. The theorem does NOT cover arbitrary unordered operator levels.

For a rank-one projector P=|psi><psi|, this includes every pure base main tensor an arbitrary positive bath C above a common white baseline B. In particular it extends the scalar-profile Stieltjes receiver beyond a rank-one bath correction.

## 4. General closure principle and scope

Any other base class known to remain safe under every scalar white-noise addition enjoys the same lift. Merely knowing Delta(A0)>=0 is insufficient: all t in the support of the measure in (1) must be paid. The identity does not supply positivity for an unknown h(t), nor does it reduce an arbitrary source to two ordered operator levels.

No historical novelty claim is made for the spectral-counting/positive-part trace identity; the proof above is self-contained. This mechanism is independent of the previously disproved nonlinear block-Mellin positivity and central-lowering hopping-coefficient monotonicity conjectures.

Related primary context (not used in place of the proof): Péter E. Frenkel, “Integral formula for quantum relative entropy implies data processing inequality,” Quantum 7,1102 (2023), arXiv:2208.12194v4, https://real.mtak.hu/186629/1/q-2023-09-07-1102.pdf . Its Sections 2–5 develop positive/negative-part trace convexity and matrix-pencil entropy integral representations. No claim is made here that the exact WH3 lifting corollary was stated there.
