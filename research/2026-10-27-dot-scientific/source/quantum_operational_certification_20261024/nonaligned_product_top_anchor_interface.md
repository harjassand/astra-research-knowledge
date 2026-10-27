# First genuinely nonaligned source interface: a product top vector

2026-10-25. Exact reduction; final matrix inequality remains open here.

Let N=W3 tensor id, E=I3/3 tensor Tr_A, 0<=A<=I, and A psi=psi for a product vector psi=a tensor r. Put P=|psi><psi|. No alignment of r with the actual reference marginal is assumed.

Twirl by the subgroup U(1) times U(2) of physical unitaries preserving the line a, tensored with identity on reference. This twirl fixes P and E(A) exactly; WH covariance fixes NP on output. At fixed EA, the actual anchored objective

g(A;P)=Tr EP log EA-2Tr NP log NA

is convex in A. Thus the twirl cannot increase g and gives

Abar=|a><a| tensor X +(I-|a><a|) tensor Y,
0<=X,Y<=I, Xr=r.

The reference marginal is (X+2Y)/3, generally noncommuting with |r><r|. Direct application of W3 gives output blocks Y on the conjugate-a line and (X+Y)/2 on its two-dimensional complement. NP is supported on that complement with weight1/2. Therefore

g(A;P)>=<r|log((X+2Y)/3)-2log((X+Y)/2)|r>.       (P)

This is a genuine source-preserving reduction for arbitrary reference dimension. No reference pinching, flat-marginal replacement, or assumption [X,Y]=0 is used.

## Remaining matrix inequality

Nonnegativity of the right side of (P) for all effects X,Y with Xr=r would exclude every negative stationary minimizer having ANY product vector in its top eigenspace. It is automatic if X,Y commute, but the noncommuting case is not proved here.

Equivalently set B=(X+2Y)/3. Then 0<=3B-X<=2I and (X+Y)/2=(X+3B)/4. Thus this is the stronger top-log problem for a special index-three source interface, not a free index-nine relaxation.

A tempting Loewner shortcut fails: B need not dominate ((X+Y)/2)^2. For projection X=diag(1,0) and Y=[[c^2,cs],[cs,s^2]], c^2+s^2=1, the determinant of 12[B-((X+Y)/2)^2] equals s^2(5-9c^2), which is negative whenever c^2>5/9. This does not refute the compressed logarithmic inequality.

## Resolvent coordinate and a warning

For M_t=(1-t)X+tY, z=t/(1-t), and s>0, let L=X+sI, K=Y+sI and H=L^(-1/2) K L^(-1/2). Since Xr=r, writing a=1+s gives

<r,(M_t+sI)^(-1)r>-1/a
 =z/a <r,(I-H)(I+zH)^(-1)r>.

The desired comparison corresponds to t=2/3 and t=1/2 (z=2 and z=1), after integration in s. Although <r,Hr><=1, H need not be <=I; therefore pointwise positivity of the rational integrand cannot be inferred from its first moment. An integrated matrix-log proof is still required.

## Exact high-resolvent positivity

Set Z=(X+Y)/2, X_s=X+sI, Z_s=Z+sI. The right side of (P) equals the integral over s>=0 of

<r,[2Z_s^(-1)-3(4Z_s-X_s)^(-1)-X_s^(-1)]r>.

The replacement of the scalar normalizing resolvent by X_s^(-1) is exact on r, since X_s r=(1+s)r. Put T_s=X_s^(-1/2) Z_s X_s^(-1/2). The integrand is

(1+s)^(-1)<r,f(T_s)r>,
f(t)=2/t-3/(4t-1)-1=2(1-t)(2t-1)/(t(4t-1)).

One has T_s>=(1+2s)/(2+2s) I and <r,T_s r><=1. For t>=3/4,

f(t)-(2/3)(1-t)
 =(1-t)*[-2(4t-3)(t-1)/(3t(4t-1))]>=0.

Therefore every integrand with s>=1 is nonnegative. The range 0<=s<1 remains unpaid; this is not an integrated proof.

## Jointly convex entropy receiver (parent observation)

The same compressed logarithmic quantity is the X-gradient in direction |r><r| of

F(X,Y)=Tr XlogX+Tr(X+2Y)log((X+2Y)/3)
       -2Tr(X+Y)log((X+Y)/2).

Its nonlinear part is D(X||X+Y)+D(X+2Y||X+Y), so F is jointly convex, up to the displayed linear constants. This does not by itself imply the required boundary-gradient sign. In particular Hilbert-Schmidt positivity of a Hessian is not complete positivity of its associated map. An actual maximal-vector or integrated pencil argument is still needed.

## Exact positive-kernel pencil receiver

The accepted balanced two-source testing-measure theorem (binary_testing_measure_entropy_transfer.md) gives a more faithful scalar calibration than separate operator bounds. For

f(t)=t log t+(t+2)log((t+2)/3)-2(t+1)log((t+1)/2),

one has f''(t)=2/[t(t+1)(t+2)], asymptotic slope log(4/3), and asymptotic intercept 2log(2/3). Integrating the scalar second derivative twice and transferring the balanced entropy identity gives exactly

F(X,Y)=log(4/3)TrX+2log(2/3)TrY
 + integral_0^infinity 2 Tr(tY-X)_+/[t(t+1)(t+2)] dt.

For faithful X,Y, differentiate in X in direction P_r=|r><r|. The pencil has only finitely many zero-eigenvalue crossing parameters, irrelevant to the integral, and ordinary spectral differentiation gives

g=log(4/3)
 - integral_0^infinity 2 q(t)/[t(t+1)(t+2)] dt,
q(t)=<r,1_(0,infinity)(tY-X) r>.

Thus the desired maximal-vector theorem is exactly the positive-kernel budget

integral_0^infinity 2q(t)/[t(t+1)(t+2)] dt <=log(4/3).

This keeps one and the same source pencil throughout. Faithful approximation preserving Xr=r is available by X_e=(1-e)X+eI, Y_e=(1-e)Y+eI, with logarithmic limits on the r-weighted support.

The elementary pointwise bound is q(t)<=min(t,1): set v=Pi_+(tY-X)r/sqrt(q). Then <v,Xv>>=|<r,v>|^2=q because X>=P_r, while <v,Yv><=1. Positivity of the pencil on v implies q<=t. This bound is insufficient: its weighted integral equals 3log(4/3), three times the required budget. An actual source-compatible integrated transport must improve it; positivity of the kernel alone does not close the proof.
