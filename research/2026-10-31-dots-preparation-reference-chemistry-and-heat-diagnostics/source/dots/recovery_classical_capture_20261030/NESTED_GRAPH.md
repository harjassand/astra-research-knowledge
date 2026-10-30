# A bounded-degree nested-prefix expander for staged record growth
30 October 2026. Graph-resource construction only. No noisy capture or autonomous read theorem is inferred.

## Result
There is an explicit geometrically growing sequence of finite vertex prefixes V_0 subset V_1 subset ... and regular weighted multigraphs G_k on V_k such that:

1. |V_k|=Theta(4^k), and each G_k has any prescribed fixed normalized nontrivial spectral bound alpha>0.
2. The union over k of all DISTINCT physical adjacency pairs has bounded degree, independent of final k. Graphs need not be induced subgraphs of one another, but no new far-away physical neighbor is added to a fixed vertex at infinitely many stages.
3. A fixed root read vertex stays in every prefix. Its exact weighted neighbor list stabilizes after a fixed number L of stages.
4. A new layer can be initialized by copying the preceding layer with fanout four. Every physical vertex is used as parent only once. These copy edges already belong to the bounded-degree base graph.
5. Graph powering changes fixed constants enormously, but neither degree nor body size grows with the requested storage horizon.

This avoids a false construction in which the old root gets fresh expander neighbors at each growth level, or every old vertex gets one new child at every level.

## 1. Base layered graph and explicit layer sizes
Fix an integer s0>=2. Layer i is L_i={i} x Z_(s0 2^i)^2, with m_i=s0^2 4^i vertices. Put a fixed-degree explicit expander on each layer, with internal edge expansion

 |partial_i S| >= h0 min(|S|,m_i-|S|),  h0>0.

An explicit choice is the 8-regular Margulis--Gabber--Galil multigraph on Z_s^2, with the eight neighbor maps

 (x +/- 2y,y), (x +/- (2y+1),y),
 (x,y +/- 2x), (x,y +/- (2x+1)),

all modulo s. Repeated neighbors and self-loops are kept as multiplicities. Its nonconstant spectral bound gives h0=(8-5 sqrt(2))/2>0. Only this standard internal expansion theorem is imported; the nested-prefix expansion below is proved here.

Write s_i=s0 2^i. Give each (i,x,y) four children (i+1,x+a s_i,y+b s_i), a,b in {0,1}. Thus the parent map is modular reduction Z_(2s_i)^2 -> Z_(s_i)^2, NOT coordinate floor-halving. A noninitial-layer vertex has exactly one parent. Thus base distinct degree is at most 8+4+1=13. Edges are undirected for the expansion graph; they can be directed parent-to-child for the scheduled copying gate.

Let V_k=union_(i=0)^k L_i. Its size is n_k=s0^2(4^(k+1)-1)/3. The finite base prefix contains internal edges and parent-child edges whose endpoints both lie in V_k. Pad absent vertical incidences with integer self-loop weight so the adjacency A_k has constant row sum D=13. This padding does not change cuts. Loop weights use the adjacency-row convention: one unit of diagonal adjacency contributes one vote/one row-sum unit. The multigraph notation can equivalently be read as a symmetric integer-weighted adjacency matrix.

## 2. Uniform prefix edge expansion: exact proof
The proof works for any integer r>=2 with m_(i+1)=r m_i and r-to-one parent-child stars.

For S subset V_k write s_i=|S intersection L_i| and

 e_i=min(s_i,m_i-s_i), D_err=sum_i e_i.

Round each layer to all-in or all-out: choose t_i in {0,1} with |s_i-t_i m_i|=e_i, and let M=sum_i t_i m_i. Internal cuts give

 B := |partial S| >= h0 D_err.                         (1)

Across layers i,i+1 the actual number of crossing edges is at least |r s_i-s_(i+1)|. This follows because there are r s_i edges whose parent lies in S and s_(i+1) edges whose child lies in S; any imbalance must cross. The rounded all-in/all-out cut is

 B_round=sum_(i:t_i != t_(i+1)) m_(i+1).

The triangle inequality gives

 B >= B_round-(r+1)D_err.                             (2)

To bound B_round, take whichever of the rounded layer-set and its complement does NOT contain the last layer k. If it is nonempty, let j<k be its highest selected layer. Its total size T is at most sum_(i=0)^j m_i, whereas the cut between j and j+1 contributes m_(j+1). Hence

 B_round >= m_(j+1) >= (r-1)T >= (r-1)min(M,n_k-M).

The empty case is immediate. Since min(x,n_k-x) is 1-Lipschitz and |S|-M has absolute value at most D_err,

 min(|S|,n_k-|S|)
 <= min(M,n_k-M)+D_err
 <= [B+(r+1)D_err]/(r-1)+D_err
 <= B [1+2r/h0]/(r-1).

Therefore every prefix has the SAME edge Cheeger lower bound

 |partial S| >= h min(|S|,n_k-|S|),
 h=(r-1)h0/(h0+2r).                                 (3)

For the explicit r=4 construction, h=3h0/(h0+8). This is deliberately conservative and need not be optimized.

## 3. Fixed powering gives a strong spectral ratio
Use the lazy matrix B_k=A_k+D I, of row sum 2D=26. Its normalized transition P_k=B_k/(2D) has all eigenvalues in [0,1]. The usual Cheeger inequality with (3) gives the uniform nonconstant bound

 lambda_2(P_k) <= 1-g,   g=h^2/(4D^2)>0.              (4)

Fix the desired alpha>0 and choose one integer L, independent of k, such that

 (1-g)^L <= alpha/2,   (2D)^(-L) <= alpha/2.

Define the majority graph adjacency

 C_k=B_k^L+I,    d=(2D)^L+1.

Its row sum d is odd. Every nonconstant eigenvalue divided by d has absolute value at most

 [(2D)^L(1-g)^L+1]/[(2D)^L+1] <= alpha.              (5)

Thus one obtains the arbitrarily strong constant spectral ratio needed by the parent's majority contraction argument. d and L can be astronomically large. They are FIXED architectural constants; no practical threshold is claimed.

Self-votes and repeated neighbors do not invalidate monotone majority correction. If the d-vote majority is opposite to the current bit, the opposite nonself vote weight is >d/2. Flipping the vertex decreases weighted disagreement-edge energy by at least one, since self-loop votes do not contribute to disagreement energy and the nonself degree is <=d. The physical update needs only the DISTINCT sites in the vote list; weights belong to a finite Boolean truth table, not to additional physical wires.

## 4. Physical union degree and fixed read root
Let B_infty be the infinite bounded-degree layered base graph (ignoring loop multiplicity). Every distinct edge of C_k joins vertices at B_infty-distance <=L. Consequently

 union_k E_distinct(C_k) subset E(B_infty^L).

This union has degree bounded by a constant, for example 1+13+...+13^L. There is no horizon-dependent degree. A majority update has at most that many distinct system-site legs; per-site update incidence has the same constant bound. If one insists on two-body interactions, compiling this fixed high-body operation is a separate obligation.

For a root p in L_0, a base path of length <=L reaches only layers <=L. Once k>=L, the boundary padding at the last layer cannot change any length-L walk starting at p: to see padding at layer k one must first spend k steps reaching it, and only a subsequent step can use that padding. Thus C_k(p,.) is identical for all k>=L. Root couplers to the quantum hub can remain physically fixed throughout. During the first L stages, the root's finite vote table may change, but all involved physical neighbors are in its same fixed radius-L neighborhood. One may instead begin at a seed prefix with k>=L, paying a larger but still fixed seed size.

For any vertex in layer i, the exact vote table stops changing once the frontier is more than L layers beyond it. Changes at growth steps are therefore confined to a fixed-width layer band near the frontier. This is a graph fact, not a claim that the noisy scheduling of these changes is already protected.

## 5. Constant-fiber graph retraction (stronger transfer property)
Define pi_k:V_(k+1)->V_k to be identity on the old prefix and modular reduction from L_(k+1) to L_k on the new layer. Every fiber has size at most five: an old frontier vertex plus its four new children. The root is fixed.

Each MGG neighbor map is affine over the integers and therefore commutes with modular reduction. Consequently every new-layer internal base edge maps to an old frontier-layer base edge with the SAME generator label. Every new vertical parent-child edge maps to a loop, and every old base edge stays unchanged. Thus pi_k is a graph retraction with dilation one on the base graph, allowing zero-length images.

A length-L walk in the new prefix projects to a walk of length at most L in the old prefix. The lazy old matrix B_k has a positive diagonal everywhere, so pad this projected walk to length L. Therefore every distinct powered-majority edge in G_(k+1) maps to an edge of G_k or a loop. In particular the image of a connected new animal-support set is connected in the old powered graph, and its vertex-image cardinality is at least one fifth of the original cardinality.

This statement is about adjacency/support, not equality of powered-edge multiplicities or disagreement energies. The root animal graph has extra edge-check/dummy vertices and completion edges; transferring its weights still needs an explicit lift/projection count. No rooted-moment transfer theorem is claimed here.

## 6. Constant fanout and deterministic growth count
At stage k+1, initialize only L_(k+1) and copy each old frontier bit in L_k to its four children. Old vertices remain in place. If the old prefix has h errors relative to the analysis bit, ideal copying gives at most

 h_new <= h+4 h_frontier <=5h.

No old vertex is reused as parent at all later stages. A fixed number J of synchronous majority rounds on G_(k+1), each with small-set contraction factor c, gives h_after<=5c^J h in the fault-free small-density regime. Taking J so 5c^J<1/2 yields the unnormalized contraction required in the parent's staged skeleton. Faulty-location and coherent-span accounting remains with that larger construction.

The new vertex count multiplies by a factor between 4 and 5. Total allocated vertices through stage k equal n_k, not n_k log n_k, because all stages are nested. The scheduled capture has O(log n_k) stages. Neither warmup nor quantum-port availability during growth is proved here; those require the parent's rooted potential and noisy receiving analysis.

## Source provenance
The internal MGG expansion is the standard Gabber--Galil construction: O. Gabber and Z. Galil, *Explicit Constructions of Linear-Sized Superconcentrators*, Journal of Computer and System Sciences 22 (1981), 407--420, DOI https://doi.org/10.1016/0022-0000(81)90040-4 ; primary paper surfaced at https://core.ac.uk/download/pdf/82074011.pdf (direct open returned403; not read and no bypass attempted). The exact eight-map/spectral statement is also recorded in the authors' expander literature and the IAS-hosted expander text, Theorem 8.2, https://www.math.ias.edu/~avi/BOOKS/expanderbookr1.pdf . The latter was used to verify the numerical 5 sqrt(2) convention; no application-specific noisy-memory theorem is imported from it.
