# Complete all-k diagonal block payment

9 November 2026. Constructive block of the endpoint-matched upper-triangular
support. The remaining off-diagonal Hessian coupling is not paid here.

Let k>1/3, ell=3k-1, m=3k+1, n=k+1. For a diagonal perturbation X=diag(x,y)
put d=kx^2-y^2, j=xy, E2=d^2+4kj^2. The endpoint-matched translator is

    lambda(A)=2det A+(ell/m)[k|A1|^2-|A2|^2+(3n/2)det A].

The explorer's literal original-density invariant extraction gives

    E2 det M_diag=ell^2 P(d,j)/(64n^2m^2),

where

    P=2m^2 d^4-2m(6k^2-7k-1)d^3j
       +ell(9k^3-23k^2-7k+1)d^2j^2
       +4k ell(9k^2+4k-1)dj^3+4kn(33k^2-1)j^4.             (1)

The diagonal two-mean block uses the invertible variables
s=k alpha x-delta y, tmean=alpha y+delta x. Formula(1) is its full affine
Schur determinant, including the original cubic forcing and quartic
offset, not a sampled necessary condition.

## 1. One positive definite Gram for the entire parameter range

Define

    a=2m^2, f=6k^2-7k-1, t=2k-1/3,
    c=ell(9k^3-23k^2-7k+1),
    e=4k ell(9k^2+4k-1), f0=4kn(33k^2-1).

On the monomials (d^2,dj,j^2), an EXACT Gram of P is

    [[a,      -m f,       -a t],
     [-m f,   c+2a t,     e/2 ],
     [-a t,   e/2,        f0  ]].                         (2)

Its Schur complement after the first diagonal a is [[B,O],[O,C]], where

    B=c+4m^2t-f^2/2,
    C=f0-2m^2t^2,
    O=e/2-m f t.

In the positive parameter ell, these are

    B=ell^4/9+16ell^3/9+41ell^2/6+88ell/9+16/9,
    C=20ell^4/27+188ell^3/27+50ell^2/3+392ell/27+104/27,
    O=2ell^4/9+22ell^3/9+55ell^2/9+6ell+16/9.

The determinant is

    BC-O^2=(8ell^8+244ell^7+2576ell^6+13006ell^5
              +34520ell^4+48448ell^3+34064ell^2
              +10240ell+896)/243>0.                       (3)

Every displayed coefficient is positive. Thus (2) is positive definite
for every k>1/3. Equivalently, the full rational three-square payment is

    P=a[d^2-f dj/(2m)-t j^2]^2
           +B[dj+(O/B)j^2]^2+[(BC-O^2)/B]j^4>0             (4)

for (d,j)!=(0,0). No source coefficient is selected by optimization.

## 2. The complete diagonal mean metric is positive

The same literal invariant extraction gives

    det Q_diag=ell N(d,j)/(4E2 n m^2),
    N=3m^2d^2-m(18k^2+7k+1)dj
                       +(54k^4+69k^3+16k^2+k)j^2.

The discriminant reserve of N is m^2 times

    324k^4+576k^3+107k^2-2k-1
      =4ell^4+(112/3)ell^3+(899/9)ell^2
                                +(928/9)ell+320/9>0.

Hence det Q_diag is strictly positive. At j=0 its first diagonal is
3ell/(4n)>0; continuity on the connected nonzero (d,j) plane therefore
makes the whole metric positive definite.

The upper off-diagonal affine mean beta decouples when X is diagonal:
its cubic forcing and mean cross terms vanish. Its quadratic coefficient
is exactly

    ell[(x-y)^2/(4n)+xy/m]
      =ell[m(x^2+y^2)+2(1-k)xy]/(4nm)>0,

because m>|1-k|. Thus this is the COMPLETE three-mean diagonal-perturbation
support block, not merely the alpha,delta subblock.

## 3. Scope and receipt

Combining the positive metric with (4) proves the endpoint-matched
pointwise support for every upper-triangular A and every nonzero diagonal
X, for ALL k>1/3. It does not pay a general symmetric-Hessian perturbation
with V!=0, still less an arbitrary compatible transverse field.

As a standalone periodic diagonal-Hessian class, this would not be a new
deep quasiconvexity class: separate one-variable laminations already have
a rank-one-convex Jensen payment. Its value here is the exact all-k
coupled block of the full affine Schur construction, with a reusable
positive Gram and no parameter grid.

One frozen intrinsic expansion, derive.py SHA
24fd1d9b281998ed7d6f0aecc8bdf48b24baf7e9e24e0b825e8c27e6f0f2f02a,
expanded the fixed B,C,O,BC-O^2 in ell. It completed in 0.104 seconds,
rc0, and all coefficient gates passed. No field, optimizer, parameter
search, coefficient retuning, or independent partial audit ran. The
input invariant matrix is preserved in
quartic_all_k_endpoint_matched_support_20261109/DIAGONAL_INVARIANTS.json.
