# An independent finite-ensemble PPT concurrence gap

9 October 2026. Complete elementary derivation. This finite-ensemble route proves the conservative bound C(rho)<=1−1/(4d^2) for PPT states on C^2 tensor C^d. The separate Gaussian route improves it to 1−1/(8d). Both are preserved independently; neither is claimed as a sharp bound or as an externally certified novelty result.

## 1. Homogeneous vectors and finite candidate ensembles

Let rho be a density matrix of rank r<=2d, with positive eigenvalues lambda_i and orthonormal eigenvectors psi_i. Put

 v_i=sqrt(lambda_i) psi_i,
 rho=sum_i |v_i><v_i|,
 <v_i,v_j>=lambda_i delta_ij.

For any vector v, set t=||v||^2, R_v=Tr_B |v><v|, B_v=R_v−(t/2)I_2. Its homogeneous concurrence is

 c(v)=2sqrt(det R_v)=sqrt(t^2−2||B_v||_F^2).

The vector's concurrence deficit obeys

 t−c(v)=2||B_v||_F^2/[t+c(v)]>=||B_v||_F^2/t           (1)

when t>0. The zero vector contributes zero.

Consider the following finite list of ensembles, all representing exactly rho:

- the spectral ensemble {v_i};
- for every i<j, replace v_i,v_j by (v_i+v_j)/sqrt(2), (v_i−v_j)/sqrt(2);
- for every i<j, replace v_i,v_j by (v_i+i v_j)/sqrt(2), (v_i−i v_j)/sqrt(2).

All other ensemble vectors remain unchanged. There are 1+r(r−1) ensembles. The two replacement vectors always have squared norm (lambda_i+lambda_j)/2. Thus their probability weights are kept explicitly; they are not treated as normalized vectors with equal original weights.

For an ensemble e, let D_e=1−sum_(v in e)c(v). Define

 D_max=max_e D_e.

Every D_e is nonnegative. The convex roof is an infimum of the concurrence averages, so

 C(rho)<=min_e sum_(v in e)c(v)=1−D_max.                (2)

The maximum DEFICIT, rather than a minimum deficit, is the quantity that upper-bounds the convex roof.

## 2. Pair-rotation control of all purification blocks

Define

 R_ij=Tr_B |v_i><v_j|,
 B_i=R_ii−(lambda_i/2)I_2.

From the spectral ensemble and (1),

 sum_i ||B_i||_F^2/lambda_i<=D_max,
 sum_i ||B_i||_F^2<=lambda_max D_max.                  (3)

For i<j put s=lambda_i+lambda_j, H=R_ij+R_ji and K=i(R_ji−R_ij). The traceless qubit marginals of the two real-rotation vectors are

 (B_i+B_j+H)/2,       (B_i+B_j−H)/2.

Their weights are s/2. Adding their inequalities (1), and discarding the nonnegative deficits of all other ensemble vectors, gives

 [||B_i+B_j||_F^2+||H||_F^2]/s<=D_max.

In particular ||H||_F^2<=s D_max. The imaginary rotation gives ||K||_F^2<=s D_max. Since

 ||H||_F^2+||K||_F^2=4||R_ij||_F^2,

we conclude

 ||R_ij||_F^2<= (lambda_i+lambda_j)D_max/2.             (4)

Purify rho as |Psi>=sum_i v_i tensor |i>_E, and write rho_AE and rho_E for the indicated marginals. The off-diagonal blocks R_ij have trace zero because the v_i are orthogonal. Therefore

 Delta=rho_AE−I_2/2 tensor rho_E

has diagonal blocks B_i and off-diagonal blocks R_ij. Equations (3)–(4) imply

 ||Delta||_F^2
 <=[lambda_max+(r−1)]D_max
 <=r D_max,                                            (5)

because sum_(i!=j)(lambda_i+lambda_j)=2(r−1).

## 3. PPT forces a purity defect

Purification and direct expansion give

 ||Delta||_F^2=tr(rho_B^2)−(1/2)tr(rho^2).              (6)

For a 2-by-2 matrix X, the reduction map is

 tr(X)I_2−X=sigma_y X^T sigma_y.

PPT of rho hence implies

 I_2 tensor rho_B−rho>=0.

Taking its inner product with rho>=0 gives

 tr(rho^2)<=tr(rho_B^2).

Since rho_B has trace one on a d-dimensional space,

 ||Delta||_F^2>=tr(rho_B^2)/2>=1/(2d).                 (7)

Combining (5) and (7),

 D_max>=1/(2dr)>=1/(4d^2).

Equation (2) proves the claimed bound. More precisely, one of the explicitly listed 1+r(r−1) ensembles has average concurrence at most 1−1/(2dr).

## Bounded checks

verify_explicit_concurrence_gap.py checks 39 PPT examples in dimensions d=2,3,4,5,8, spanning 1,625 weighted candidate ensembles. The set includes rank-deficient product mixtures and an additional 2-by-4 PPT matrix family. All pair weights, polarization identities, purity identities and conservative bounds pass at the declared numerical tolerance. The checks do not optimize a convex roof.
