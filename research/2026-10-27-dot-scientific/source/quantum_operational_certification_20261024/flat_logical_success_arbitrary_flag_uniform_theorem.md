# Arbitrary flat logical rank: whole value and dimension-free heralded-erasure rigidity

## Theorem

Let k>=1, V:C3 tensor Ck -> R be an isometry, f any unit output vector, and 0<=p<=1. The actual TP channel

 E(rho)=p V(rho tensor Ik/k)V*+qTr(rho)|f><f|, q=1-p,

has nonnegative WH3 normalized-Choi deficit. Put theta=||V*f||^2. Equality holds exactly when p q theta=0.

After a fixed output isometric padding to dimension at least3k+1 if required, there is a generalized-erasure channel with the SAME p and flat logical success state Ik/k such that

 ||E-E_hat||_diamond<=min(2,72sqrt(Delta(E))).    (1)

The constant is independent of k and of output dimension. Success is reversible after discarding the logical ancilla; failure is an orthogonal, measurable reset flag. No uniform conditional recovery is claimed when success probability tends to zero. The square-root exponent cannot be improved for this whole class, by its already-audited k=2 subfamily.

## 1. Actual spectra and joint Schmidt-allocation concavity

Write f=sqrt(theta)g+sqrt(1-theta)f_perp. The unit g in C3 tensor Ck has Schmidt probabilities lambda_i, i=1,2,3, with zero entries padded and rank s<=min(3,k). Flat logical symmetry and physical covariance give an exact Schmidt-frame reduction.

Set
 a=p/k, b=q/3, c=pq/(9k),
 Aout=2p/(3k), Bout=2q/3,
 Sin=a+b, Sout=Aout+Bout, r=p/(3k).

The source is a weighted projection sum aP+bQ, with ranks k and3 and nonzero overlaps theta lambda_i/3. Its actual spectrum consists of s principal-angle 2x2 blocks, k-s unmatched eigenvalues a, and3-s unmatched eigenvalues b. Equivalently its trace entropy is the algebraically uniform formula

 f(input)=sum_(i=1)^3 f2(Sin,c(3-theta lambda_i))+(k-3)f(a).  (2)

For k<3 the last coefficient is merely bookkeeping, NOT a negative spectral multiplicity: each artificially padded lambda_i=0 block contributes exactly f(a)+f(b), and (2) reduces to the actual nonnegative spectator counts just stated.

The unscaled output is Aout P_antisym tensor Ik+Bout Q. Its three overlap eigenvalues are theta(1-lambda_i)/2. Its entropy is

 f(output_unscaled)=sum_(i=1)^3 f2(Sout,2c(2-theta+theta lambda_i))
                    +(3k-3)f(Aout).            (3)

The reference entropy, independent of all lambda_i, is

 f(reference)=(3k-1)f(r)+f2(r+q,rq(1-theta)).     (4)

Here f2(S,P) is trace entropy of a positive2x2 matrix with trace S and determinant P. The weighted-projection formulas follow from determinant ab(1-overlap) in each principal-angle span. These are actual source spectra, and the factor2 on the output is retained.

For each paired denominator,

 2Pin,i(z)-Pout,i(z)
 =z^2+(4p/(3k))z+2c(1+theta-2theta lambda_i)>=0. (5)

The input determinant slope is -c theta and the output slope +2c theta. Since partial_P^2 f2=integral_0^infinity dz/(z^2+Sz+P)^2, the contribution of each lambda_i to Delta has nonpositive second derivative. More importantly the lambda dependence is a SUM OF SEPARATE ONE-VARIABLE TERMS plus a constant. Its Hessian is diagonal and negative semidefinite, so Delta is JOINTLY CONCAVE on the full Schmidt simplex. Separate concavity alone would not suffice without this separability. It is strictly concave on nonzero simplex tangents when p,q,theta>0.

Thus its minimum lies at a rank-one Schmidt endpoint. The same algebraic simplex extension receives k=1,2 and their zero-padded feasible Schmidt sets: a concave function is bounded below by the convex combination of its vertex values, all of whose vertices are physically feasible.

## 2. Endpoint receiving and exact zero set

At a Schmidt vertex the flag has support only on one logical success mode (and possibly its outside component). The source is an orthogonal-reference direct sum of one coherent star

 aPhi3+q(I3/3) tensor P_f

and k-1 untouched pure-maxent modes of mass a. The whole-star theorem pays the first; all other deficits are zero. This proves the full value theorem.

If p,q,theta>0 the endpoint star has nonzero flat reset bath, nonzero coherent center, and a remaining physical bath of rank at least two. The exact star equality classification makes its deficit strictly positive. Therefore the entire simplex has strictly positive deficit. When theta=0 the reset is orthogonally flagged; when p=0 orq=0 it is respectively reset or reversible flat-logical encoding. These all have deficit zero.

## 3. Quantitative endpoint cost

Let tau=q+a be the affected star's mass. Its normalized scalar parameters are

 t=a theta/(3tau), a_star=q/(3tau), x_star=a/(3tau).

The audited scalar coherent-star payment gives, after homogeneity,

 Delta(E)>=a^2 q theta/[36(q+a)^2].             (6)

Joint concavity transfers this SAME vertex bound to every Schmidt allocation.

## 4. Actual dimension-free code/flag comparison

Moving only the reset flag to a unit vector orthogonal to ran V costs 2q sqrt(theta) in diamond norm. For theta<1 use its normalized outside projection; at theta=1 use the padded outside direction.

Alternatively keep f and replace V by the polar isometry W of (I-P_f)V, completed in the padded outside direction if theta=1. The sole changed domain direction is g (output direction Vg), and ||V-W||<=sqrt(2theta). Crucially W equals V on C3 tensor L_perp, where L is the Schmidt support of g in the logical space and dim L=s<=3. The flat logical state has no off-block coherences, so the unchanged k-s logical modes cancel EXACTLY in the channel difference. The changed branch has weight p s/k=s a. Hence its diamond cost is at most

 2sqrt2 s a sqrt(theta),

not the dimension-dependent full success weight bound. This is a comparison of actual CP maps on the logical block, including arbitrary input ancillas; no logical outcome is postselected.

Choose the smaller comparison. Its cost is at most

 2sqrt2 min(q,s a)sqrt(theta).

For a,q>0 put R=q/a. Combining with (6), the cost divided by sqrt(Delta) is at most

 12sqrt2 (q+a)min(q,s a)/(a sqrt(q))
 =12sqrt2 sqrt(q)(R+1)min(R,s)/R
 <=12sqrt2(s+1)<=48sqrt2<72.                   (7)

The inequality follows separately from R<=s and R>=s, and q<=1. If a=0, q=0 or theta=0 the comparison is exact without division. This proves (1), including all output-dimension and rank endpoints.

## 5. Heralded access and sharpness scope

The code/flag measurement and logical-ancilla discard of E_hat are actual deterministic output operations and can be applied to E. Diamond contraction preserves the bound for the joint heralded instrument. The successful CP map differs from p id3 by at most zeta=min(2,72sqrt(Delta)) in diamond norm. For p>zeta, every normalized successful output, including entangled inputs, has trace error at most2zeta/p. No unconditional recovery near reset follows.

The k=2 TP family and generalized-erasure commutator obstruction in `two_mode_flat_success_arbitrary_flag_value_theorem.md` establish a lower error of order sqrt(Delta), even allowing arbitrary logical eigenweights in the comparison target. Hence the exponent in the uniform theorem is sharp, though the constant72 is not optimized.

The original one-code erasure target is insufficient already for rho -> rho tensor I2/2, which has zero deficit but ordinary-erasure distance at least2/3. Arbitrary NONFLAT logical success states are not covered by this theorem. Their Schmidt-allocation concavity is explicitly false, so no flat-to-nonflat convex mixing is inferred.

## Subsequent spectrum extension

`arbitrary_logical_success_reset_flag_value_theorem.md` now proves the value and exact-zero theorem for arbitrary logical sigma, with dimension-free generalized-erasure distance280sqrt(Delta). Its proof is a shared-resolvent signed-measure compensation, not a continuation of the concavity argument here. The present flat theorem retains its sharper constant72 and its independent elementary principal-angle proof.
