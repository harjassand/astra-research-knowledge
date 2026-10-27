# Shared-pair balancing theorem for the stable one-column boundary

Let h,d>=0, |c|^2<=hd, x in [0,1], and populations a,b>=0. The correlated source is the coefficient matrix T=[[d,c],[conj(c),h]] on span{|kk>, sqrt(x)|ii>+sqrt(1-x)|jj>}, with populations a|ik><ik|+b|jk><jk|. At fixed h,d,c,a+b, its WH3 entropy deficit is minimized by x=1/2 and a=b=(a+b)/2.

This is a global balancing theorem, not a whole-value sign theorem. The remaining balanced receiver is an explicit three-parameter homogeneous matrix-entropy problem.

## Exact jointly convex shared-pair function

For x,b>0 define

 L(x,b)=[[d+b,sqrt(x)c],[sqrt(x)conj(c),xh]],
 F(x,b)=xh log(xh)+b log b-Tr L(x,b)log L(x,b).

Then F is jointly convex. Here is a direct positive Hessian proof. For integration variable t>=0 write

 B=xh+t, C=d+b+t, A=hC-|c|^2,
 D=CB-x|c|^2, e=b+t.

The usual scalar-resolvent representation of Tr L log L, differentiated twice (or integration by parts of log det(L+t)), yields

 Hess F=integral_0^infinity M(t)dt,

 M11=h^2/B^2-A^2/D^2,
 M22=1/e^2-B^2/D^2,
 M12=M21=t|c|^2/D^2.

Indeed the determinant is D, affine in each of x,b, with mixed derivative h, and hD-AB=t|c|^2. To check M>=0 pointwise, first note

 A>=he, D>=Be, dB-x|c|^2>=dt.

These give M11,M22>=0. Their product is

 t|c|^2 (hD+AB)(dB-x|c|^2)(D+Be)/(B^2 e^2 D^4).

The three nontrivial factors obey

 hD+AB>=2hBe,
 dB-x|c|^2>=dt,
 D+Be>=2Be.

Their product is at least 4hd t B^2e^2, hence at least |c|^2 t B^2e^2. This is exactly the bound required for M11 M22>=M12^2. Degenerate h,d,c and boundary x,b follow by continuity. This proof retains the square-root offdiagonal dependence; it does not incorrectly treat L as affine in x.

## Physical receiving identity

The two populated output pairs before division by two are L(x,b) and L(1-x,a). The remaining correlated pair has spectrum {h,0}; the population singleton has value a+b. The reference marginal diagonal is (xh,(1-x)h,d+a+b). Consequently, all x and population-allocation dependence of Delta at fixed h,d,c,s=a+b is precisely

 F(x,b)+F(1-x,a).

Jensen for the jointly convex function proves

 F(x,b)+F(1-x,a)>=2F(1/2,s/2),

which is the asserted balancing theorem. Boundary cases follow by continuity. No normalization changes because Tr A=h+d+s is fixed.

## Remaining balanced scalar-matrix receiver

Put q=s/2 and define

 T=[[d,c],[conj(c),h]],
 L=[[d+q,c/sqrt(2)],[conj(c)/sqrt(2),h/2]],
 tau=h+d+2q.

The balanced deficit is exactly

 Delta_bal=Tr T log T-2Tr L log L
           +(d+2q)log(d+2q)+tau log(2/3)+d log2.

Proving Delta_bal>=0 for all h,d,q>=0, |c|^2<=hd would close the entire stable rank-two-kernel one-column boundary. This last inequality is not asserted here. At q=0 it is covered by the maximally-correlated theorem; c=0 is covered by the physical-2+1 block theorem (the correlated pair may remain entangled, so this is not a classical/CQ claim); |c|^2=hd is covered by the rank-one-plus-population theorem. The possible nontrivial minimum lies in the faithful coherent interior.

## Exact interior-stationary scalar receiver

At a normalized stationary point with h,d,q>0 and 0<|c|^2<hd, let delta=Delta_bal/tau. Differentiation in |c|^2 gives equality of logarithmic divided differences ell(T)=ell(L)=ell>0. Scale all entries by ell, so that the common divided difference becomes one; delta is scale invariant.

Write U=Tr T, V=Tr L, D_T=det T, D_L=det L in this scaled convention. There exist theta,phi>0 such that

 U=2theta coth(theta), D_T=(theta/sinh(theta))^2,
 V=2phi coth(phi),     D_L=(phi/sinh(phi))^2.

For a matrix with this divided difference, log T=T+alpha_T I with alpha_T=(log D_T-U)/2, and similarly for L. The stationarity equations are partial_h Delta=partial_d Delta=delta and partial_q Delta=2delta. Subtracting the d and q equations gives

 alpha_T-alpha_L=q-log2.

The h and q equations give

 log(d+2q)=alpha_T+V.

Putting r=h/2+q and m=d+2q, the complete necessary relations simplify to

 r=log(4D_T/D_L),             delta=r-log3,
 m=2V-U>0,                   m^2 exp(-m)=D_T,
 r^2-(U-V)^2=4D_L-2D_T.                           (S)

The last identity is the source relation 2det L-det T=hq. Reconstruction is

 d=V-r, h=r+U-V, q=(r-U+V)/2,
 |c|^2=dh-D_T.

All these reconstructed quantities must satisfy the strict source inequalities; equations (S) without those inequalities are not sufficient. A negative stationary candidate requires theta>phi and r<log3.

Two targeted Newton solves of (S), initialized at (theta,phi)=(2,1.5) and (3,2.5), both reached theta approximately1.51555707, phi approximately1.30256489, delta approximately0.10999170055. This is only a diagnostic for the exact reduced equations. It does not prove uniqueness, exclude other roots, or establish the balanced value theorem. No such conclusion is being used.
