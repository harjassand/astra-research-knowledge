# Whole qutrit entropy order on the reduction-criterion region

27 October 2026. Root proof by a compact two-face log-determinant minimum. Independent receiving requested. The argument keeps the lower spectral-face normal and therefore does not require a singular-boundary classification.

## Theorem

Let N=W3 tensor id_R, W3(B)=(Tr(B)I-B^T)/2, and E(X)=I3/3 tensor Tr_A X, with any finite reference space. For every X>=0 satisfying

 X <= 3E(X) = I3 tensor Tr_A X,

one has

 Delta(X):=D(X||E(X))-2D(NX||E(X)) >=0.              (1)

Equality holds exactly when X=E(X). In particular, this receives every PPT input and hence every separable input, in arbitrary finite reference dimension. The unrestricted conjecture is NOT resolved: reduction-violating inputs remain outside this theorem.

## 1. A pointwise determinant theorem

If M>0, E(M)=I and ||M||<3, then

 F(M)=2logdet(NM)-logdet(M) >=0,                    (2)

with equality exactly at M=I. For faithful M<=3I the weak inequality follows by continuity; no separate pointwise equality classification at the closed cap is needed below.

Fix any 0<epsilon<1<c<3. Minimize the smooth reference-congruence invariant extension

 F_full(M)=2logdet(NM)-logdet(M)-logdet(E M)

over the compact convex set

 epsilon I <= M <= c I, E M=I.

A minimum exists. Every M and NM in this set is faithful; N is unital and positive. The point I is strictly feasible for both spectral inequalities, so the normal-cone/KKT decomposition is valid. Write the actual gradient at a minimizer as

 G=2N((NM)^-1)-M^-1-I.

There are a Hermitian reference-only multiplier Lambda and positive upper/lower normals S_+,S_- with

 G+Lambda+S_+-S_-=0,
 S_+(cI-M)=0, S_-(M-epsilon I)=0.                  (3)

The normals have disjoint spectral supports. No lower-face normal is dropped.

## 2. Reference congruence determines the multiplier

N and E commute with every reference congruence. All three determinant terms acquire the same congruence logarithm, whose coefficients2-1-1 cancel. Hence F_full is invariant under M -> (I3 tensor Z)M(I3 tensor Z*) for invertible Z.

Differentiating this identity in every Hermitian reference-only direction gives

 E(MG+GM)=0.

This is an identity of the function, not an assumption that the congruence variation preserves the spectral caps. Substitute(3), use E M=I and the E-bimodule property, and use MS_+=cS_+, MS_-=epsilon S_-. One obtains

 Lambda=-c E(S_+)+epsilon E(S_-),
 G=c E(S_+)-S_+-epsilon E(S_-)+S_-.                (4)

## 3. The upper normal is impossible

Let P_+ be the spectral projection of M at c. Since M>=cP_+, E(P_+)<=I/c. On the corner algebra P_+ B P_+, the map cE is completely positive and subunital. Its Schwarz inequality gives

 c^2(E S_+)^2 <= c E(S_+^2),
 c||E S_+||_HS^2 <= ||S_+||_HS^2.                 (5)

Pair(4) with S_+. Disjoint supports eliminate Tr(S_+S_-), while positivity gives Tr(E S_+ E S_-)>=0. Therefore

 Tr(S_+G)
 =c||E S_+||_HS^2-||S_+||_HS^2
       -epsilon Tr(E S_+ E S_-) <=0.              (6)

On the other hand, inverse Jensen for unital CP N and the exact identity N^2=(Id+3E)/4 give

 G >= 8(M+3I)^-1-M^-1-I = f(M),
 f(m)=(m-1)(3-m)/[m(m+3)].                        (7)

Since 1<c<3, f(c)>0. Thus Tr(S_+G)>=f(c)TrS_+, contradicting(6) unless S_+=0.

## 4. The lower normal cannot support a nonidentity minimum

With S_+=0, (4) becomes G=S_--epsilon E S_-. Suppose M has an eigenvector psi with eigenvalue m>1. Since epsilon<1, S_-psi=0. Consequently

 <psi,Gpsi>=-epsilon<psi,E(S_-)psi><=0.

But m<=c<3, so(7) gives <psi,Gpsi>>=f(m)>0. This is impossible. Hence M<=I. Since E M=I and E preserves trace, TrM equals the full dimension; therefore M=I.

Every minimum on every compact two-face set is I. Its value is zero, and a nonidentity point cannot also attain that minimum. This proves(2) for arbitrary finite reference dimension. Any faithful E M=I with ||M||<3 belongs to one such set. Faithful cap3 follows by M_delta=(1-delta)M+delta I and continuity.

This proof does not claim the inverse-trace inequality or require any previously derived boundary-coercivity theorem. Those remain separate assets.

## 5. Receive the original entropy, without whitening it

Put tau=E(X), D=X-tau and restrict to the actual product support of tau. Tau is faithful there. For s>0 define

 A_s=(tau+sI)^-1/2 D(tau+sI)^-1/2,
 M_s=I+A_s.

The factors are reference-only. Therefore E A_s=0, E M_s=I, and N A_s is the corresponding congruence of ND. The source bounds0<=X<=3tau imply

 M_s >= s(tau+sI)^-1 >0,
 M_s <= I+2tau(tau+sI)^-1 <3I.                    (8)

The exact trace-entropy Bregman identity is

 D(X||tau)=integral_0^infinity
   [Tr A_s-logdet(I+A_s)] ds.

Here Tr A_s=0 pointwise. Apply the same identity to NX, whose marginal is the SAME tau. Subtraction gives the actual source identity

 Delta(X)=integral_0^infinity
 [2logdet(I+N A_s)-logdet(I+A_s)] ds
         =integral_0^infinity F(M_s) ds >=0.       (9)

No entropy is evaluated on a whitened replacement state; every original congruence is inside its exact resolvent integral. Supported singular inputs are legitimate: one may mix X with tau, apply the faithful identities, and pass monotonically in each individual nonnegative Bregman integrand. Finite-dimensional entropy continuity gives the same finite original divergences.

If X!=tau, then A_s!=0 for every s>0. Equation(2), with the STRICT cap in(8), makes F(M_s)>0 for every s>0. Hence Delta(X)>0. Conversely X=tau is fixed by N and has zero deficit.

## 6. PPT and separable corollary

If X^{T_A}>=0, complete positivity of N gives

 N(X^{T_A})=[I3 tensor Tr_A X-X]/2 >=0.

Thus every PPT source satisfies the hypothesis of(1). Every positive separable source is PPT by termwise physical transposition. The proof does not assert positivity for all NPT inputs or identify every zero-deficit source outside the reduction region.

## Scope guards

The sharp upper threshold of this particular stationary argument is3 because f changes sign there. The proof establishes a whole entropy region, not unrestricted entropy order, a generic arbitrary channel-pair result, or an operational recovery guarantee. Previous false clipping, pinching, local-variance-transfer and inverse-power shortcuts are not used. The existing lower-reference boundary/coercivity proofs are unnecessary for this theorem but are not invalidated.
