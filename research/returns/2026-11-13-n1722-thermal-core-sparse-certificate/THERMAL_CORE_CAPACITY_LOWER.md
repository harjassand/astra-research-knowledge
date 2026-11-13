# A thermal-core-carrying finite capacity lower bound

## Result and exact scope

Use the governing N1722 heatbath Ising graph on the L×L torus, n=L², θ≥4, φ=θ/R. Let A=C_r be its actual acquired thermal core: augmented plus components have contractible lifts fitting in r×r rectangles. Assume

    1≤r,    r+2≤R/3,    r<L/4.

Keep the source's fixed zero-coupling diagonals and its physical nearest-neighbor rates. Let Z_A=sum_A w, B={M≥0}, and Cκ be the capacity from the extra source vertex joined to every x∈A with conductance κw(x), with B grounded.

Set

    ρbar=1/100000,   a=1−2ρbar=49999/50000,
    Γeff=8θR/a+8θ.

Then the explicit flow below proves

    Cκ ≥ Z_A/[κ^(-1)+2n exp(Γeff)].                    (1)

This replaces the bare allminus weight in the elementary path lower bound by the FULL thermal-core normalizer. There is no extensive Z_A/wminus loss and no sufficiently-large-R threshold. The displayed core-size conditions are essential.

This is a concrete application of standard Thomson/Peierls/canonical-flow methods, not a claim of a new general primitive or a sharp nucleation exponent. It does not solve the dense-source growth/occupation problem or acquire the full capacity to relative accuracy.

## 1. Uniform Peierls control for every interpolated field

Consider the Gibbs law conditioned on A with arbitrary inhomogeneous fields h_i satisfying0≤h_i≤3φ, and the same θ bonds.

If spin i is plus, its augmented component has an embedded filled outer contour γ. For that specified contour, flip EVERY spin in its filled domain Dγ, including all thermal holes and islands. This involution preserves A:

* The original component and its filled domain lie in one r×r rectangle in its contractible lift.
* Its plus boundary becomes minus, separated from exterior plus components by the unchanged exterior minus layer along augmented adjacency.
* Any new plus component consists of old interior minus spins, remains inside the same r×r rectangle, and cannot become winding.
* Exterior components and their contractible bounding boxes are unchanged.

This is the same core-preserving filled-domain operation used in the authorized source. It is not erasure or resampling of the interior.

With physical perimeter P and filled volume V,

    w_h(x)/w_h(Fγx)
       =exp[−2θP+2 sum_{j∈Dγ} h_j x_j]
       ≤exp[−2θP+6φV].

To avoid assuming whether the source uses r sites or coordinate span r, conservatively use V≤(r+2)². With P≥4sqrt(V), V≤(r+2)P/4. Hence

    w_h(x)/w_h(Fγx)≤exp[−(2θ−3φ(r+2)/2)P]
                       ≤exp[−3θP/2].                 (2)

The bound is uniform in all the interpolated fields, despite conditioning on A. No FKG claim for the conditioned core is needed.

### A conservative explicit local contour count

A rooted contour can be followed on the dual of the fixed triangulation. Dual degree is3. Each dual vertex has exactly one edge crossing a zero-coupling diagonal, so a nonbacktracking contour cannot cross two zero-coupling edges consecutively. If its physical perimeter is P, its total dual length is at most2P.

For a contour enclosing i, a physical root edge can be chosen with an endpoint within lattice distance P+1 in each coordinate of i. The number of possible root positions is bounded by(2P+3)². Paying both root and traversal orientations and summing nonbacktracking dual walks gives the safe bound

    #contours of physical perimeterP enclosing i
       ≤8(2P+3)²4^P.

This intentionally overcounts; it applies to the source's planar lifted, fixed-diagonal resolved contours. It does not count zero-coupling edges as positive energy. The embedded core and r<L/4 prevent torus winding in this argument.

Combining with (2), P≥4, θ≥4 and4exp(−6)<1/100 gives

    P_A,h(x_i=+)≤ρbar,

because the exact rational upper is

    8 sum_{P≥4}(2P+3)²(1/100)^P
      =1190681/121287375000
      <1/100000.                                     (3)

## 2. The field-tilt moment cancels bulk entropy

For ANY deterministic site set D, let N_D^+(x) be its number of plus spins. Starting from the original conditioned-core law μ_A, introduce weight exp(tN_D^+) for0≤t≤4φ. This changes the field inside D from φ toφ+t/2≤3φ, plus a configuration-independent constant. Therefore (3) applies throughout the interpolation, and

    d/dt log E_μA exp(tN_D^+) ≤ρbar |D|.

Integrating yields the finite exact moment bound

    E_μA exp(4φN_D^+) ≤ exp(4φρbar |D|).              (4)

Let F_Dx flip all spins in D. The physical energy difference obeys

    Hdim(F_Dx)−Hdim(x)
       =2θ sum_{boundary bonds}x_i x_j+2φ sum_{i∈D}x_i
       ≤2θP(D)−2φ|D|+4φN_D^+(x).

Consequently

    E_μA [w(x)/w(F_Dx)]
       ≤exp[2θP(D)−2φa |D|].                        (5)

This is the key cancellation. It compares a thermal configuration with its invertible partial spin flip. It never replaces the source by allminus or forces all target spins plus.

## 3. Explicit paths to the ACTUAL target

Fix one nested-square ordering of ALL torus sites. Start with a1×1 square and append a new column then row to complete the next square, continuing to L×L. Write D_k for the first k sites. Every prefix satisfies

    |D_k|=k,    P(D_k)≤4sqrt(k)+4.

Physical torus identifications can only decrease this perimeter; no source configuration is used to choose the ordering.

From the source vertex, send mass μ_A(x)=w(x)/Z_A to each x∈A. If x∈B, this is already a source-to-target path. Otherwise successively visit

    x, F_{D_1}x, ..., F_{D_n}x=−x,

stopping at the FIRST state in B. Since x∉B has M(x)<0, −x∈B, so stopping occurs within n genuine single-spin transitions. Magnetization need not increase at every step. Every transition uses a native allowed heatbath edge; it is not executed as an instantaneous block update.

For any k, (5) and the prefix perimeter estimate give

    E_μA[w(x)/w(F_{D_k}x)]
       ≤exp[8θsqrt(k)+8θ−2φa k]
       ≤exp(Γeff),                                  (6)

by maximizing the quadratic in sqrt(k).

## 4. Source and physical-flow energy, including cancellation

The source-edge energy is exactly

    sum_A μ_A(x)²/[κw(x)]=1/(κZ_A).

A physical edge changes one particular site i. That site occurs at exactly one position k in the fixed ordering. Hence the edge has at most TWO source preimages, one traversing it in each direction; both are recovered by flipping D_{k−1} back from the respective endpoint. First-B stopping can only remove a preimage.

If the two path masses are u,v≥0, the NET flow has energy numerator(u−v)²≤u²+v². Thus no exponentially many source-label collision and no uncharged frame memory occur.

Native heatbath conductance satisfies exactly

    1/g(z,z^i)=1/w(z)+1/w(z^i).

Summing the preceding source-preimage upper over all k and then using (6),

    energy_physical
       ≤ Z_A^(-1) sum_{k=1}^n E_μA[
              w(x)/w(F_{D_{k−1}}x)+w(x)/w(F_{D_k}x)]
       ≤2n exp(Γeff)/Z_A.

Adding source-edge energy and applying Thomson proves (1). The source definition includes its edges to A∩B, as in the original soft-source normalizer identity. If a different convention omits those edges, replace A by A\B and separately establish the moment bound for that modified conditioned law; do not silently reuse this proof.

## 5. Representation, finite arithmetic and actual baseline

The flow's exponentially many paths need not be listed. To query an edge coefficient:

1. Identify its flipped site and its unique ordering position k.
2. Recover its at most two source preimages by XOR with D_{k−1}.
3. Test each preimage's actual augmented-core membership and whether its prefix path has already hit B.
4. Return the difference of the corresponding w(x)/Z_A masses.

Core membership and the first-B test can be done in polynomial time in n by component lifting/bounding boxes and scanning prefix magnetizations. The scalar lower bound uses only an acquired lower Z_A, actualκ and explicit rationala. Exponentials can be bounded with directed rounding in polynomial arithmetic cost in the numeric input sizes required here; an exponential VALUE is not an exponential trajectory simulation. No independent source sampling or global partition sum is newly required.

Compared with the elementary bare allminus path, the prefactor changes from wminus toZ_A, with only the conservative barrier inflation8θR→8θR/a and n rather thanceil(n/2) path length. Compared with SS/GMV, this is not a sharp thermal Wulff exponent, but it is finite and explicit under the stated core-size conditions.

## 6. Executed finite diagnostic

`thermal_capacity_flow_test.py` constructs the entire flow on a4×4 torus with an explicitly defined singleton-component core, field activity2, edge activity4096 (θ=log4096/2,R12). There are201 configurations in that test core and1314 nonzero physical-flow edges. Exact rational arithmetic verifies every non-target divergence and the energy comparison to the full-prefix moment sum. It stops at the ACTUAL majority target. This checks the finite implementation; the preceding argument supplies the general proof.

This small diagnostic checks the flow algebra, not the governing source's box-width convention or its large-volume/core-size hypotheses, and is not evidence of physical growth at that scale.
