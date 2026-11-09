ROOT NEW EXACT CHECK ON THE FIXED FAMILY:
Let B^c_ij=P[F^c_ij.grad], B^s_ij=P[F^s_ij.grad]. On meanzero divergence-free trigonometricv,
 ||grad v||2^2 <= sum_(i!=j)(||B^c_ij v||2^2+||B^s_ij v||2^2) <=2||grad v||2^2.
Here is the usable calculation. Combining sine and cosine cancels cross terms between opposite frequency shifts:
 ||B^c_ij v||2^2+||B^s_ij v||2^2
 =2pi^2 sum_k k_i^2[||P_(k+e_j)v_k||^2+||P_(k-e_j)v_k||^2].
For integerk_i!=0 andj!=i, the angle betweenk andk+/-e_j hascosine>=1/sqrt2; thus each projection onk-perpendicular vectors preserves at least half squarednorm. Summing the two possiblej and threei gives the lower bound; contraction of each Leray projection gives the upper. Zeroshifts withk_i=0 contributezero. Consequently this family has NO common nonconstant kernel.

There is also NO nonzero COMMON INVARIANT SUBSPACE consisting of finitely supported Fourier fields. For a putative such finite-dimensional space, take its finite union of supports, choosei with somek_i=n!=0 and j!=i, then choose maximal k_j among that fixedn slice. The complex control B^c_ij+iB^s_ij=P[e^(2pi i x_j)partial_i] produces the UNIQUE nonzero coefficient at k+e_j, outside that union; the projection lower bound prevents cancellation. This proves precisely finite-FOURIER noninvariance, NOT absence of a general smooth/H1 finite-dimensional invariant subspace, a quantitative mixing rate or the full control theorem. These checks provide an actual opening; do not silently strengthen them.

