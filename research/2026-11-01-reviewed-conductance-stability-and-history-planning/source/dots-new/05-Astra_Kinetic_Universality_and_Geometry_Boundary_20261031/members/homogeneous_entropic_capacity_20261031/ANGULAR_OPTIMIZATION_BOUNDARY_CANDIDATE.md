# A hard angular question that the rate certificate does not need to solve

Status: ROOT comparison note, UNREVIEWED. The graph optimization identity is the classical Motzkin–Straus mechanism, not a new hardness theorem. This does not claim hardness of the partition function or of sampling for this entire family.

For a graph G on m>=2 vertices define the admitted quartic

  U_G(z)=sum_i z_i^4+2 sum_{ij in E(G)} z_i^2 z_j^2.

It satisfies the cheap, exact bound U_G>=sum_i z_i^4>=||z||^4/m. The optimal Euclidean coercivity constant is instead

  a_*(G)=min_{||z||=1} U_G(z)=1/alpha(G),

where alpha(G) is the largest independent-set size.

Here is the elementary reduction. Set w_i=z_i^2, so w_i>=0 and sum w_i=1. The objective is Q(w)=sum w_i^2+2 sum_edges w_i w_j. If an edge i,j has both weights positive, hold their sum fixed and move weight between them. Their self/edge contribution is the constant (w_i+w_j)^2 and their interactions with other vertices are affine in w_i. One endpoint therefore does not increase Q and removes a vertex from the positive support. Repeating yields an independent support S. On such a support Q=sum w_i^2>=1/|S|>=1/alpha(G). Uniform weights on a maximum independent set attain equality. Thus exact optimal coercivity, or its threshold a_*<=1/k, contains the standard maximum-independent-set decision problem.

This is the complement form of Motzkin and Straus, *Maxima for Graphs and a New Proof of a Theorem of Turán* (1965), DOI https://doi.org/10.4153/CJM-1965-053-6 . The support-compression proof is included to make the comparison self-contained; neither the identity nor NP-hardness of maximum independent set is presented as an invention.

Now set F(y,z)=[1+(1-y^2)^2]U_G(z), beta=1, and use the acquired full-fiber basins y<=-1/2 and y>=1/2. The received homogeneous rate theorem uses only the sufficient bound a=1/m. It supplies a constant-factor full-diffusion capacity/mass interval from scalar integrals q(y)=[1+(1-y^2)^2]^(-m/4), identical for every graph at a fixed m. The reviewed radial factor is157/125, before numerical quadrature width. The independent parallel-channel theorem can tighten it when its separate receiving is complete.

Consequently the rate computation neither computes a_* nor needs an angular minimizer. For this fixed-parameter family the raw coefficient list and scalar integration have polynomial costs in m and the declared numerical accuracy; a sparse graph description is not confused with an expanded generic quartic. The weaker verified coercivity is sufficient for the requested rate uncertainty. Demanding the optimal constant would introduce an unnecessary NP-hard subproblem.

This is a separation between two DISTINCT tasks on the same model family. It is not a proof that every other rate algorithm is expensive, not a solution of maximum independent set, and not evidence that arbitrary stochastic kinetics or equilibrium sampling are tractable. It explains why choosing an adequate task-specific certificate can matter more than reconstructing an optimally sharp full landscape description.
