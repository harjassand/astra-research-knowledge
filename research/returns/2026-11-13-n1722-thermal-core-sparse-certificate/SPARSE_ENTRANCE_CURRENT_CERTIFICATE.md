# Sparse critical components: a finite actual-current certificate

## What is covered

Let K=floor(5R²). Consider genuine one-spin entrances y from M5\B into D=outside(M5∪B). The new plus spin can create only one violating augmented-plus component C. Restrict to entrances for which C has an embedded nonwinding filled outer domain, and m=|C|≤M<K+1.

This includes thin rings and irregular, branched or merging sparse components without requiring a prescribed square, minus guards, a future collar, or a local-magnetization restriction. It does NOT cover dense critical components or winding violations.

## Perimeter pays for the negative interior

Let V≥K+1 be the component's filled outer area. The total physical boundary P(C) includes its outer boundary and all hole boundaries. The outer boundary has length at least4sqrt(V). The holes have total area V−m; other nested plus components are included in the corresponding filled holes because they are not part of C. Summing the lattice isoperimetric bound over holes gives

    P(C) ≥ 4sqrt(V)+4sqrt(V−m)
         ≥ 4sqrt(K+1)+4sqrt(K+1−m).

Equivalently, set H=D\C for the filled-site set D. No physical nearest-neighbor edge connects H to D-complement, because C is its actual enclosing component boundary. Consequently P(C)=P(D)+P(H), and the lattice inequality P(S)≥4sqrt(|S|) applies separately to D and H, including disconnected H. This uses the same embedded filled-contour area/physical-perimeter conventions as the governing source. Fixed diagonal contact resolution must preserve the usual outer/hole decomposition (equivalently take nonintersecting contour regularizations and their area/perimeter limits). No convexity is assumed. P(C) is the TOTAL physical perimeter, not only the outer perimeter.

## Erasure retains all other thermal information

For a fixed augmented-connected support C, change precisely its m plus spins to minus, leaving every other spin unchanged. All nearest-neighbor spins outside C adjacent to C are minus, because C is an augmented plus component. Therefore

    w(y)/w(F_C y)=exp[−2θP(C)+2φm].

Every unaffected component already belonged to M5 in the predecessor. Erasing C thus produces a configuration in M5. For fixed C the map is injective; its inverse restores plus on the recorded support. Thermal spins in holes and exterior are never erased or independently resampled.

Every transition y→M5 must delete a site of C. Since native heatbath rates≤1 and voltage differences≤1,

    j_M5(y) ≤ m w(y).

## Pay all support labels

The augmented graph has degree≤8, as allowed by the source's fixed diagonals. A connected m-site support has a canonical spanning-tree depth-first walk of length2(m−1). There are at most n8^{2(m−1)}=n64^{m−1} such supports. This coarse count overcounts but does not omit labels or assume a fixed ring.

Summing the injective weight comparison gives the explicit finite bound

    j_sparse/Z_M5
       ≤ sum_{m=1}^M n m 64^{m−1}
          exp{−8θ[√(K+1)+√(K+1−m)]+2φm}
       ≤ n M²64^{M−1}
          exp{−8θ[√(K+1)+√(K+1−M)]+2φM}.

This is an actual current bound; no Gibbs entrance distribution or committor lower bound is presumed.

## Bulk-free normalization and remaining scope

Use `BULK_FREE_SPARSE_CURRENT_COROLLARY.md` for the final combination with the thermal-core capacity lower bound. It replaces the earlier bare-allminus capacity/contour-pressure normalization and is the intended certificate in this package.

The complementary dense compact/rough components and winding entrances remain unhandled by this family-specific inequality. Some sparse mergers and hole-closing entrances are included, but not every merger or hole-closing configuration has at most M plus sites. No physical growth-duration or full mean-transition conclusion follows solely from this current bound.
