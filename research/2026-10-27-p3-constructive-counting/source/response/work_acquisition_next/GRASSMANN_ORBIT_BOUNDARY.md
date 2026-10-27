# A strict boundary for block-row orbit acquisition

27 October 2026. This is an exact representation obstruction, not a counting lower bound. The earlier generic low-rank compiler handles the example efficiently; the point is to retain that compiler alongside the new orbit-diversity method.

Fix an integer block width b>=1. Let W range over all b-dimensional subspaces of F_2^r, with r>b. Their number is the Gaussian binomial

    s = [r choose b]_2 = product_(i=0)^(b-1) (2^r-2^i)/(2^b-2^i).

Choose a full-row-rank b by r basis matrix U_W for every subspace and stack them into U, an n by r matrix with n=bs. Set D=UU^T. Because U has full column rank, rank(D)=r. Take the raw alternating B with the same off-block entries as D and arbitrary diagonal blocks. Thus B has a rank-r completion after arbitrary diagonal-block corrections and no off-block errors.

## All distinct block rows stay far apart under every gauge

The block row of D at W is the profile (U_W U_V^T)_V. Let W and W' be distinct. For any G in GL_b(F_2), the matrix Delta=G U_W-U_W' is nonzero, since otherwise their row spaces would coincide. Select any nonzero row v of Delta.

If Delta U_V^T=0, the entire subspace V lies in the hyperplane ker(v). There are exactly

    s0 = [r-1 choose b]_2

such b-dimensional subspaces. For every other V, Delta U_V^T has positive rank. Therefore the quotient rank metric satisfies

    d([D_W],[D_W']) >= delta = s-s0.

For fixed b, s0/s=(2^(r-b)-1)/(2^r-1), so delta/s tends to 1-2^(-b)>0. Thus every two distinct hidden row orbits are separated by a constant fraction of the number of blocks.

## Every small-type approximation has a quadratic residual

Consider any symmetric approximation C whose block rows have at most c orbits under independent invertible left gauges. Its diagonal blocks may be corrected arbitrarily afterward. In one orbit class A of size t>=2, the quotient triangle inequality gives

    delta <= d([D_a],[C_a])+d([D_z],[C_z])

for each unordered pair a,z in A, because [C_a]=[C_z]. Summing all pairs yields

    sum_(a in A) d([D_a],[C_a]) >= t delta/2.

At least s-c blocks belong to nonsingleton classes. Hence total row-orbit discrepancy is at least (s-c)delta/2.

If C agrees with raw B off the diagonal blocks except at M' unordered scalar entries, its directed rank-metric discrepancy from D is at most 2M'+n: each scalar error can contribute at most one rank unit per directed block, while each arbitrary diagonal block contributes at most b. Since quotient distances do not exceed these direct distances,

    M' >= (s-c)(s-s0)/4 - n/2.

For fixed b and c=o(s), this is Omega(n^2). The conclusion holds for arbitrary acquired gauges and arbitrary choices of the c representative profiles, not merely for a specific clustering heuristic or for observed-row centers.

Meanwhile r=Theta(log n) for fixed b. Thus this family has extremely small global rank but cannot have both sublinear weighted orbit-type count bc and a nearly-linear scalar residual. It is a strict boundary of the orbit-diversity representation. It does not contradict any raw low-rank acquisition theorem; with M=0 that earlier machinery applies.

## Compatibility with the cubic centroid partition

Choose b=3 and add the volume cubic x_(W,1)x_(W,2)x_(W,3) inside every block. Its third derivative is the nonzero alternating volume trilinear form on F_2^3. It has zero radical and no nontrivial direct-sum split: a split of a three-dimensional space has summands of dimension at most two, on which an alternating trilinear form vanishes. Its centroid consists exactly of scalar matrices, as the defining identities force off-diagonal entries to vanish and all diagonal entries to agree. The direct sum has primitive centroid blocks equal to these three-dimensional blocks. Every GL_3(F_2) matrix has determinant one, so the volume cubic's third-derivative form is preserved by all internal gauges. The obstruction therefore survives exactly the block freedom relevant to the root construction.

The family can be disguised by an arbitrary global invertible affine coordinate change before centroid acquisition; recovering the intrinsic blocks leaves this orbit-distance obstruction unchanged. Such a disguise changes lower-degree terms in the usual way and does not establish any new computational hardness.

## Executed checks

The companion program constructs all dimension-three subspaces for ambient dimensions four, five and six, checks their counts and the corresponding hyperplane counts, verifies the stacked column rank, and computes exact quotient distances for all block pairs in the first fixture and sampled pairs in larger fixtures. Every GL_3 alignment is checked for those pairs. The largest family has 1,395 blocks and 4,185 scalar variables. This is a representation-certificate calculation; it does not execute an exponential phase sum or an asymptotic counting solver.
