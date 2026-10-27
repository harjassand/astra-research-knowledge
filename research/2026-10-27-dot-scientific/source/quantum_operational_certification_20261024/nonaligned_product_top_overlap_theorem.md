# A dimension-free nonaligned product-top overlap theorem

2026-10-25. Exact theorem. It excludes a substantial class of negative stationary minimizers; it is not the full WH3 entropy inequality.

## Statement

Let X,Y be effects on any finite-dimensional Hilbert space, and let r be a unit vector with Xr=r. Write y=<r,Yr> and

g(X,Y;r)=<r,log((X+2Y)/3)r>-2<r,log((X+Y)/2)r>.

Then

g(X,Y;r) >= (63/200)[11/18+log(9/7)-y].             (1)

In particular g>=0 whenever

y<=eta:=11/18+log(9/7) = 0.862425539392... .          (2)

No commutation between X,Y or their marginal and |r><r| is assumed. The bound is uniform in reference dimension and all permitted lower spectra. A simpler independent bound is

g>=log(4/3)-(6-4sqrt(2)) y.                          (3)

## Receiving use for WH3

For a physical top vector psi=a tensor r, twirl only by physical unitaries preserving the line a. This preserves the ACTUAL marginal and P=|psi><psi|, and cannot increase the actual-N anchored gradient. The twirled input is |a><a| tensor X+(I-|a><a|) tensor Y with Xr=r and 0<=X,Y<=I. Its anchored gradient equals g above; see nonaligned_product_top_anchor_interface.md.

Thus (2) excludes a negative stationary minimizer whenever a product top vector has the corresponding complementary physical average overlap y<=eta. In terms of the original input, Y=(1/2)Tr_A[(I-|a><a|)A] and y=(<r,Tr_A(A)r>-1)/2. These are acquired source quantities, not independently chosen marginals.

This theorem is a stationary exclusion, not a pointwise claim that the full entropy deficit is nonnegative on every input satisfying (2).

## One exact positive-kernel pencil

For faithful X,Y set

q(t)=<r,1_(0,infinity)(tY-X)r>, t>0,
w(t)=2/[t(t+1)(t+2)].

The accepted balanced two-source testing-measure identity gives

g=log(4/3)-integral_0^infinity w(t)q(t) dt.           (4)

Indeed the scalar entropy function

f(t)=tlogt+(t+2)log((t+2)/3)-2(t+1)log((t+1)/2)

has f''=w, asymptotic slope log(4/3) and intercept 2log(2/3). Its exact trace lift is

F(X,Y)=log(4/3)TrX+2log(2/3)TrY
       +integral w(t)Tr(tY-X)_+ dt.

Differentiate in X along |r><r| and use Xr=r. The finitely many pencil crossing parameters have measure zero.

## The load-bearing exact sum rule

Differentiating the same two-source representation of D(Y||X) yields

integral_0^infinity q(t)/t^2 dt
 =<r,Dlog_X(Y)r>=<r,Yr>=y.                          (5)

For clarity, the positive-part representation whose derivative is being used is

D(Y||X)=Tr(Y-X)
 +integral_0^1 Tr(tY-X)_+/t^2 dt
 +integral_1^infinity [Tr(tY-X)_+-tTrY+TrX]/t^2 dt.

The derivative of the first trace and the +TrX tail cancel exactly. The remaining derivative is minus the integral in (5). On the other hand, differentiating Umegaki relative entropy gives -Dlog_X(Y); because Xr=r, its r-compression is -<r,Yr>.

## Elementary cap, used without discarding the sum rule

Always 0<=q(t)<=min(t,1). For q>0 put v=Pi_+(tY-X)r/sqrt(q), so |<r,v>|^2=q. Since X>=|r><r| and Y<=I,

0< <v,(tY-X)v> <=t-q.

The endpoint limit supplies the non-strict bound. Using this cap alone gives an insufficient budget 3log(4/3); the exact weighted moment (5) is essential.

## Explicit dual multiplier closes the stated class

Put rho=63/200, a=7/9, b=18/7, so ab=2. The scalar ratio

w(t)t^2=2t/[(t+1)(t+2)]

exceeds rho exactly for a<t<b. Combining the cap and moment gives

integral wq
 <=rho*y+integral_a^b [w(t)-rho/t^2] min(t,1) dt.

Both integrals are elementary. Their cap moment and weighted mass are

integral_a^b min(t,1)/t^2 dt
 =-log a+1-1/b =log(9/7)+11/18=eta,

integral_a^b w(t)min(t,1) dt =log(4/3).

Thus integral wq<=rho*y+log(4/3)-rho*eta. Substitution into (4) proves (1). Also w(t)t^2<=6-4sqrt(2) for all t, proving (3) directly from (5).

## Singular extension and remaining gap

Replace X,Y by (1-e)X+eI,(1-e)Y+eI. The top condition survives and the bounds pass to the limit. Both mixed matrices dominate a positive multiple of |r><r|, so their r-weighted logarithms have the required supported limits.

The range y>eta is not settled by this theorem. At y=1, Yr=r and g=0 exactly, but this endpoint does not justify interpolation across the remaining interval. No positivity of a matrix Hessian or monotonicity under source-free pinching is assumed.
