# Occupation-carrying terminal reduction and a local certificate

Status: internal analytic derivation, not externally reviewed. The theorem is a finite supplied-graph theorem. The mechanism is a specialization of classical goal-oriented equilibrated-flux error estimation; it is not a claim to invent Schur elimination, graph transformation, the complementary-energy principle, or the primal/dual residual identity.

## Input and requested output

Let G be a finite connected undirected graph, c_e>0 its supplied conductances, and w_i>0 its supplied reversible CTMC masses. Fix distinct singleton source s and target t. Put q_ij=c_ij/w_i. Ground t, and let A be the grounded conductance Laplacian. Put a=e_s and b=(w_i)_{i!=t}. The requested directional MFPT is

    T = a^T A^{-1} b = E_s[tau_t].                         (1)

Indeed the first-step/backward equation is A u=b with u_t=0. The ground-state Green function v=A^{-1}a satisfies v_s=1/C, and h=Cv is the s-versus-t committor. Therefore (1) also equals sum_i w_i h_i/C. A singleton target's own mass is absent from b. No equilibrium partition sum needs to be computed.

## The certificate for arbitrary trial potentials

Choose any two potentials x,y, both zero at t. Define residuals

    r_a=a-Ax,                 r_b=b-Ay.

Choose any two edge flows f,g whose divergences at non-target vertices equal r_a,r_b, respectively. Let

    E_a=sum_e f_e^2/c_e,      E_b=sum_e g_e^2/c_e,
    J=sum_e f_e g_e/c_e,
    T_0=a^T y+x^T r_b.

Then the following two-sided bound holds:

    T_0 + (J-sqrt(E_a E_b))/2 <= T
         <= T_0 + (J+sqrt(E_a E_b))/2.                     (2)

The lower endpoint may be replaced by its maximum with zero. If an independently certified positive lower bound is available, it may also be used.

### Proof

By expansion, T=T_0+r_a^T A^{-1}r_b. Orient all edges arbitrarily and let B be their grounded incidence matrix, so A=BCB^T, C=diag(c). Define p=C^{-1/2}f and q=C^{-1/2}g. Since Bf=r_a and Bg=r_b,

    r_a^T A^{-1}r_b=p^T P q,
    P=C^{1/2}B^T(BCB^T)^{-1}BC^{1/2}.

P is an orthogonal projection: P=P^T=P^2. Hence ||2P-I||_2<=1. Since p^Tq=J, ||p||^2=E_a and ||q||^2=E_b,

    |p^T P q-J/2|=|p^T(2P-I)q|/2
                  <=sqrt(E_a E_b)/2.

This proves (2). It is valid for signed residuals, without a condition-number estimate, without exact coarse solves, and without any lumpability assumption. It is the graph version of a complementary-energy primal/dual output bound.

## A reduction whose certificate uses local trees

Delete a set D of edges while preserving a connected retained graph G_d. Partition its vertices into connected clusters, without putting s and t in the same cluster. Choose one tree inside each cluster. Contract the clusters, retain every nondeleted intercluster conductance, and aggregate masses:

    w_C=sum_{i in C} w_i.

The target cluster is grounded; its aggregated mass does not enter the coarse RHS. Let P lift coarse potentials to constants on clusters, zero on the target cluster. The coarse matrix is A_H=P^T A_d P, not an exact Schur complement. Solve the two coarse RHS

    A_H v=P^T a,             A_H u=P^T b,
    x=Pv,                    y=Pu.

Only one coarse factorization is needed. There is no full committor or full occupation solve. For exact solves, P^T(a-A_d x)=P^T(b-A_d y)=0. Thus each non-target cluster's residual has zero sum. On the target cluster its residual may drain into t.

Root each cluster tree at a representative (at t for the target cluster). Route each residual toward its root: the flow from child z to its parent is the sum of the residual over z's subtree. This is one postorder traversal per cluster, O(n) arithmetic after the full residual scan. Let the resulting flows be f_F,g_F.

Restore a deleted edge e=(i,j) by assigning the additional flows

    f_D(e)=-c_e(x_i-x_j),     g_D(e)=-c_e(y_i-y_j).

Their divergences are -L_D x,-L_D y. Therefore the disjoint-support combined flows f_F+f_D and g_F+g_D have precisely the original-graph residuals. The certificate ingredients are

    E_a=sum_F f_F^2/c + sum_D c (delta x)^2,
    E_b=sum_F g_F^2/c + sum_D c (delta y)^2,
    J  =sum_F f_F g_F/c + sum_D c delta x delta y,
    T_0=T_H-sum_D c delta x delta y,
    T_H=(P^Ta)^T A_H^{-1}(P^Tb).

This is a computable local error budget: every tree edge/deleted edge has an explicit contribution. Summing products only within arbitrary contraction clusters is not justified in general because the original Green operator couples clusters. The next exact decomposition does justify additive budgets over a graph-determined partition.

For inexact coarse solves, retain one original intercluster edge for each edge of a coarse spanning tree. Together with the cluster trees this forms a full spanning tree. Route the complete residuals on that tree. Equation (2) remains valid. High-precision/outward arithmetic can expose the very small numerical cluster imbalances without assuming exact Galerkin orthogonality. A full tree is therefore also a simple independent verifier.

## Exact cycle-block decomposition removes weak-trap pollution

The global product in (2) can be disastrously pessimistic. A large mass on a very weak pendant edge gives enormous E_b, while a tiny source residual elsewhere contributes E_a. Their product manufactures a large error budget even though the pendant flow cannot couple to any external cycle. This failure occurred in the first synthetic diagnostic and was repaired, not ignored.

Partition the graph's edges into its vertex-biconnected edge blocks, treating bridges as one-edge blocks and parallel edges correctly as a possible two-edge cycle. Let B range over these blocks. Define E_a,B, E_b,B, J_B by restricting the edge sums to B. Then

    T = T_0 + sum_bridge_blocks J_B
            + sum_cyclic_blocks J_B/2 + epsilon,
    |epsilon| <= (1/2) sum_cyclic_blocks sqrt(E_a,B E_b,B).  (3)

The sum is over the actual graph's cycle blocks, not the chosen coarse clusters. It is an additive, computable, local budget. A bridge's contribution is exact, however small its conductance or large its mass.

### Proof of (3)

The orthogonal complement of the gradient space is the weighted cycle space ker(B C^{1/2}). It is spanned by weighted simple-cycle vectors. Every simple cycle is contained in one biconnected edge block. Distinct blocks have disjoint edge support. Consequently the weighted cycle space is the orthogonal direct sum of its restrictions to those blocks, and its orthogonal projection is block diagonal. So is P=I-P_cycle. In a one-edge bridge block the cycle subspace is zero and P_B=I. On every cyclic block, apply the proof of (2) to p_B,q_B, and add the resulting intervals. This proves (3).

Tarjan's edge-block algorithm computes the partition in O(n+m) time/storage. It requires no rate solve. The implementation uses an iterative traversal to avoid recursive stack limits and distinguishes parallel edges by their edge identifiers.

For an arbitrary tree, every block is a bridge, so (3) computes the exact bilinear Green output from any trial potentials after one residual/routing pass. This is the familiar tree/network identity, not a generic exact-elimination discovery. On graphs with cyclic traps attached at one articulation, the decomposition also prevents their enormous mass-only flow energy from inflating error in other blocks. Within one large cyclic block, the Cauchy product can still be loose; there is no universal successful compression guarantee.

## Why it survives the leaf counterexample

Suppose a connected subgraph meets the rest of G only at a single articulation r, contains neither s nor t in its interior, and is contracted to r with its full mass. The electrical potential A^{-1}a is constant on this subgraph: the harmonic maximum principle, with the sole boundary value v_r, forces this. Its source residual is zero there. Contracting any collection of such appendages gives an exact source Green function after lifting, hence r_a=0 everywhere if the remaining source problem is solved exactly. Equation (2) then has zero width even if E_b is enormous. The aggregated masses still contribute to the numerator through the correct attachment potential.

In the three-state supplied example, contracting z into s gives w_s'=M+1 and T_H=M+1; contracting z into t gives T_H=1. The leaf conductance delta can be arbitrarily small. The certificate does not charge an artificial delta^{-1} error because the source residual is exactly zero. This exact appendage fact is classical electrical-network structure, not a priority claim.

## A sharp information obstruction remains

Consider one cluster containing vertices s,z and a distinct target t. Let w_s=1,w_z=M,w_t=1. Inside the cluster let c_sz=d>0. Between the cluster and t let total conductance be c_zt=k>0, with no s-t edge. The contracted graph has only an edge of conductance k and source-cluster mass M+1, for every d. It returns T_H=(M+1)/k. The original chain has

    T=(M+1)/k+1/d.

Proof: A=[[d,-d],[-d,d+k]] and A^{-1}_{s,*}=[1/d+1/k,1/k]. Thus even the same aggregated masses and the exact contracted terminal conductance do not bound the directional lifetime without internal routing information. As d tends to zero the missing term is unbounded. In this example, the forest flow for the unit-source residual is 1 along sz and for the mass residual is 1 along sz. Therefore E_a=E_b=J=1/d. Bound (2) gives [T_H,T_H+1/d], and the upper endpoint is attained. The factor 1/2 and the Gram correction cannot be uniformly decreased from these global-Gram data alone. The stronger bridge identity (3) recovers the missing 1/d exactly; this is why retaining the local routing data matters.

More generally, equality in the projection bound is possible whenever the paired residual flows lie in suitable gradient/cycle subspaces. The certificate has no generic small-core or relative-width guarantee. If a positive 1% interval is required, a contraction can be accepted only when the computed endpoints meet that requirement; otherwise refine/retain states or return UNKNOWN.

## Costs and scope

All n masses and m conductances are supplied/loaded and paid. Sorting or maximum-spanning-forest selection costs O(m log m); quotient construction and a residual/tree verification pass use O(n+m) storage/arithmetic. A k-state quotient requires one sparse factorization and two RHS; its fill/storage and precision are paid. Worst case it has k=n and the reduction adds overhead to a direct selected-output solve. The arithmetic verifier uses interval Decimal operations and costs much more than an unverified float64 residual scan.

The method certifies a directional mean. It supplies no first-passage CDF or relative rare-tail guarantee. Carrying mass fixes the particular mean numerator interface, not arbitrary waiting-time distributions. Given the same full input, graph transformation already retains waiting times exactly. An equally informed full solve can use this same output certificate, so certification alone is not an algorithmic advantage.

## Primary-source comparison discovered during this tranche

- Mozolevski and Prudhomme, *Goal-oriented error estimation based on equilibrated-flux reconstruction for finite element approximations of elliptic problems*, 2015, DOI 10.1016/j.cma.2014.09.025, combines primal/dual residuals with equilibrated fluxes. https://doi.org/10.1016/j.cma.2014.09.025
- Parés, Nguyen, Díez and Peraire, *A posteriori goal-oriented bounds for the Poisson problem using potential and equilibrated flux reconstructions*, arXiv:2106.10945, gives two-sided complementary-energy output bounds. https://arxiv.org/abs/2106.10945
- Creusé, Nicaise and Tang, *Goal-oriented error estimation based on equilibrated flux and potential reconstruction*, 2023, DOI 10.1016/j.camwa.2023.07.008, explicitly splits a computable correction and a product-bounded remainder. https://doi.org/10.1016/j.camwa.2023.07.008
- Supplied PyGT snapshot fa0e106958d9948209daff04360290d50de82572, GT.py and mfpt.py, carries branching probabilities and waiting times, and obtains singleton MFPTs after elimination to two nodes. This is an exact-elimination competitor, not the operation claimed above.

These primary sources decisively preclude advertising the general residual/output theorem as a fundamentally new computational principle. Priority for this particular local forest specialization is UNKNOWN. Practical superiority must be established by matched complete-cost runs, not inferred from the theorem.
