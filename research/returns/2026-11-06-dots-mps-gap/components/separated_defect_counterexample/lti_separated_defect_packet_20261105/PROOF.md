# Exact value obstruction for the LTI gap hierarchy

5 November 2026

The original one-dimensional LTI SDP of Rai et al., Eq. (17), has value exactly **1 at every finite level** for the nearest-neighbor ferromagnetic Ising projector chain, whereas the periodic spectral gap is exactly **2**. The same phenomenon holds for the explicitly defined rectangular finite-cutoff analogue applied to the square toric code. Matching positive primal and dual witnesses prove these statements without solving an SDP or invoking strong duality.

These examples refute unrestricted convergence to the exact gap value for the stated hierarchy. They do **not** refute eventual detection of a positive gap: the certificates already give the positive bound 1. The physical spectra and separated-defect mechanism are standard. No novelty or external-review claim is made.

## 1 The original one dimensional program

Let a qubit chain have nearest-neighbor positive interaction h, and let h_i denote its translate to sites i and i+1. On n consecutive sites, define the anticommutator {A,B}=AB+BA and

    q_n = h_1^2 + sum_(j=2)^(n-1) {h_1,h_j}.

The displayed nearest-neighbor dual in Rai et al., Eq. (17), is

    delta_LTI(n) = inf_rho Tr(rho q_n),
    rho >= 0,
    Tr_1(rho) = Tr_n(rho),
    Tr(rho h_1) = 1.

The marginal matrices are identified using the order-preserving translation between the remaining n-1 sites. There is no constraint Tr(rho)=1. In particular, rho is an energy-normalized positive operator, not necessarily a density matrix of unit trace.

The associated primal, Eqs. (11)-(12), maximizes delta subject to

    q_n - delta h_1 + I tensor Y - Y tensor I >= 0,

where Y is any Hermitian operator on n-1 sites. For every dual feasible rho, the marginal equality gives

    Tr[rho(I tensor Y - Y tensor I)] = 0.

Consequently every feasible primal delta is at most every feasible dual objective. Producing both at the same value proves the optimum without a duality regularity assumption.

The paper's target in Section 2 is the lowest nonzero eigenvalue Delta_N of the **periodic** Hamiltonian H_N=sum_i h_i, and its thermodynamic limit. Ground-space uniqueness is not assumed in that setup. Its Section 5 leaves exact-value convergence open, separately from positive-gap detection. This packet addresses that open value-convergence question, not an asserted theorem of general convergence.

## 2 The Ising counterexample

Take

    h_i = (I - Z_i Z_(i+1))/2.

All h_i are commuting projectors. In the computational basis H_N counts domain walls, with site labels taken modulo N. Every periodic binary string has an even number of walls. The two constant strings are the zero-energy states, and a nonempty proper interval of flipped spins has exactly two walls. Thus, for N>=3,

    Delta_N = 2,  and therefore lim_(N to infinity) Delta_N = 2.

For every n>=3, define on the open n-site SDP window

    rho_n = (1/2) sum_(j=1)^(n-1) [
        |0^j 1^(n-j)><0^j 1^(n-j)|
        + |1^j 0^(n-j)><1^j 0^(n-j)| ].

This operator is positive and has trace n-1. Its support consists of strings with exactly one internal wall. For every internal bond i, exactly two summands have a wall at i, each with coefficient 1/2. Hence

    Tr(rho_n h_i) = 1,
    Tr(rho_n h_i h_j) = 0 for all distinct i,j.

The complete marginal identity is

    Tr_1(rho_n) = Tr_n(rho_n)
        = rho_(n-1) + (1/2)(|0^(n-1)><0^(n-1)|
                              + |1^(n-1)><1^(n-1)|).

To see this, an end trace either leaves a one-wall string or removes the wall adjacent to that end, producing a constant string. Every surviving one-wall string and each constant string has coefficient 1/2 on either side. Both matrices are diagonal, so this verifies every matrix entry, including all zero off-diagonal entries. The condition is full LTI, not merely an equality of energy moments.

It follows that rho_n is dual feasible and Tr(rho_n q_n)=1. Conversely,

    q_n - h_1 = 2 sum_(j=2)^(n-1) h_1 h_j >= 0,

because commuting positive operators have positive products. Thus delta=1 and Y=0 are primal feasible. The matching bounds prove

    delta_LTI(n) = 1 for every n>=3,
    lim_n delta_LTI(n) = 1 < 2 = lim_N Delta_N.

### The loss occurs before the marginal relaxation

Fix n. On a sufficiently large ring, choose a binary string with one long zero domain and one long one domain, with both walls separated by more than the retained displacement cutoff in either periodic direction. Its energy is 2. Average its rank-one density matrix over all N translations, restrict to the n-site window, and multiply by N/2. The resulting positive operator has full LTI, Tr(rho h_1)=1, and every retained distinct-bond product has expectation zero. Its objective is again 1.

This witness extends to a genuine translation-invariant state on that larger ring. It can also be obtained from an infinite periodic classical spin configuration, averaged over a period. Thus nonextendibility of LTI marginals is not required for this obstruction.

On the separated-wall eigenstate, H_N has eigenvalue 2 and H_N^2 has eigenvalue 4. Its finite-displacement truncation retains only the two self-energies, of total expectation 2, and discards the cross contribution 2 between distant walls. Normalizing by the energy 2 gives objective 1.

For every finite cutoff a larger separation is available. This is not an exchange of limits: the hierarchy at any fixed level must certify arbitrarily large rings. If one instead fixed a ring and enlarged the cutoff until the complete H_N^2 were restored, this particular loss would disappear.

### The specified Ising vacuum representation

In the GNS representation of the all-zero infinite product state, finite-flip configurations form a complete orthonormal basis. Every nonempty finite set of flipped spins has at least two boundary bonds, and a single spin flip attains two. The closure of the diagonal nonnegative Hamiltonian on the finite-flip domain therefore has spectrum {0,2,4,...} and gap 2. An infinite single-kink configuration belongs to a different representation; it is not a local excitation of this vacuum. The periodic counterexample does not depend on the GNS statement.

## 3 The rectangular analogue and a separated defect lemma

The original Eq. (17) is one-dimensional. The following two-dimensional program is defined here explicitly; it is not presented as a two-dimensional equation copied from that paper.

Let h_x be translates of a positive interaction supported within x+[-1,1]^2 cells. For an integer L>=2, set

    D_L = ([-L,L]^2 intersect Z^2) minus {0},
    Lambda_L = ([-L-1,L+1]^2 intersect Z^2),
    q_L = h_0^2 + (1/2) sum_(z in D_L) {h_0,h_z}.

All terms of q_L are supported in Lambda_L. The factor 1/2 is necessary because D_L contains both z and -z: after summing translates, every retained unordered pair contributes exactly one anticommutator.

A positive operator rho on Lambda_L is full LTI when, in each coordinate direction, tracing out the minimum face gives the same matrix as tracing out the maximum face, after translation identifies the remaining cells. Define

    gamma_L = inf Tr(rho q_L),
    subject to rho >= 0, full LTI, and Tr(rho h_0)=1.

The matching primal adds arbitrary face-translation coboundaries to q_L-delta h_0 and requires positivity. Concretely, embed an arbitrary Hermitian Y on the rectangle with one face removed in its two translated positions, subtract the embeddings, and sum these differences over the two axes. Full LTI annihilates every such difference. The same weak-duality argument as in Section 1 applies.

The proof below also works for any fixed finite symmetric displacement set and any containing rectangular window. In a noncommuting model, a valid H-squared lower-bound truncation must retain all overlapping pairs. Our examples commute everywhere, so every omitted distinct-pair product is positive in any case.

**Separated-defect lemma.** Suppose the h_x commute, have nonnegative integer spectra, and for each fixed cutoff there is a sufficiently large periodic system with a common eigenvector such that exactly k cells have eigenvalue h_x=1, all other h_x have eigenvalue 0, and all distinct occupied-cell displacements avoid the retained set modulo the torus. Then the finite-cutoff LTI value is exactly 1.

**Proof.** Let V be the number of torus cells. Translation-average the eigenstate and restrict to the window. The averaged local expectations are

    <h_x> = <h_x^2> = k/V,
    <h_x h_(x+z)> = 0 for every retained z!=0.

The finite-window marginal has exact full LTI because it is a restriction of an exactly translation-invariant state, with the window embedded without site identifications. Multiplying it by V/k gives a feasible rho with objective 1.

For the reverse inequality, the integer-spectrum hypothesis gives h_0^2-h_0>=0. All h_x commute and are positive, so

    q_L-h_0 = (h_0^2-h_0) + (1/2) sum_z {h_0,h_z} >= 0.

This is a primal certificate at delta=1 with every coboundary zero. The matching witnesses prove gamma_L=1. The one-sided one-dimensional generator satisfies the identical argument. No SDP attainment or strong-duality theorem is needed. QED.

## 4 The toric code analogue

At each cell r=(i,j), put a horizontal outgoing edge qubit h and a vertical outgoing edge qubit v. The cell Hilbert-space dimension is four. Define

    A_(i,j) = X^h_(i,j) X^h_(i-1,j) X^v_(i,j) X^v_(i,j-1),
    B_(i,j) = Z^h_(i,j) Z^h_(i,j+1) Z^v_(i,j) Z^v_(i+1,j),
    Q^A_r = (I-A_r)/2,  Q^B_r = (I-B_r)/2,
    h_r = Q^A_r + Q^B_r.

The support of h_r fits inside the 3-by-3 cell box r+[-1,1]^2. Every star and plaquette overlap on either zero or two edges, so the stabilizers and all h_r commute. Each h_r has eigenvalues 0,1,2.

On an N-by-N periodic square lattice, N>=3,

    product_r A_r = I,  product_r B_r = I.

These are the only relations within the star and plaquette families. Indeed, a star product is identity only if its vertex subset has empty edge boundary, and the torus graph is connected; the subset is therefore empty or all vertices. The dual graph gives the same result for plaquettes. X and Z masks cannot cancel each other into identity. Thus the combined stabilizer rank is 2N^2-2 on 2N^2 qubits, and the all-plus ground space has dimension four.

Each simultaneous syndrome has an even number of star defects and an even number of plaquette defects. Hence every nonzero energy of H_N=sum_r h_r is at least 2. An open Z string on a primal path, applied to a ground vector, flips precisely its two endpoint stars and no plaquettes. It attains energy 2. Therefore

    Delta_N = 2 for every N>=3.

Fix a cutoff L. For example, take an even N>=8(L+2) and choose endpoint stars u=(0,0) and v=(N/2,0). Their relative displacement in either orientation is outside D_L modulo N. The Z-string state has h_x=1 at exactly u and v, and h_x=0 elsewhere. Applying the lemma with k=2 gives

    gamma_L = 1 for every L>=2,
    lim_L gamma_L = 1 < 2 = lim_N Delta_N.

The explicit dual is rho=(N^2/2) times the Lambda_L marginal of the translation-averaged two-star-defect state. This verifies positivity, full face-marginal equalities, energy normalization, and the objective at once. All retained products vanish; h_0^2-h_0=2 Q^A_0 Q^B_0>=0 supplies the local lower certificate.

If a convention requires norm(h)<=1, replace h by h/2. Both the hierarchy value and physical gap scale linearly, giving the same discrepancy as 1/2 versus 1. No physical conclusion depends on the overall energy unit.

### A direct finite window density

The included independent audits also construct full-LTI operators without invoking a torus marginal. On an a-by-b cell rectangle, let m=(a-1)(b-1), Q=2ab, and include every fully contained star and plaquette. There are m of each and 2m independent generators. Let P_t be the projector onto the syndrome with exactly the contained star t negative and all other contained generators positive, with boundary degrees of freedom unconstrained. Each P_t has rank D_0=2^(Q-2m). Then

    rho_(a,b) = (1/D_0) sum_t P_t
              = 2^(-Q) sum_(S,T) (m-2|S|) A_S B_T.

Positivity follows from the projector sum. Products of crossing star generators cannot cancel on a removed extreme face because their boundary edge masks are independent; the corresponding statement holds for plaquettes. Mixed X and Z masks cannot cancel to identity. Consequently partial trace keeps exactly the subgroup generated by individually surviving stabilizers. If m' stars remain, the reduced operator is the one-defect sum on the smaller rectangle plus (m-m') copies of its normalized all-plus syndrome state. Opposite faces have the same m', so the entire reduced matrices coincide after translation.

The first audit proves this support claim for arbitrary translated subrectangles. The second checks complete Pauli expansions and independent boundary-mask ranks. The torus construction above is already sufficient for the all-level theorem, so the result does not depend on extrapolating these finite checks.

### The specified toric vacuum representation

In the frustration-free plane vacuum, all stars and plaquettes have eigenvalue +1. Finite-support Pauli operators applied to the vacuum span the dense local domain. Each such Pauli creates an even number of star defects and an even number of plaquette defects. A nonzero syndrome therefore costs at least 2. A finite Pauli with no defects is a product of contractible stabilizers on the plane and acts as a scalar on the vacuum. Thus the local vectors decompose into the vacuum and syndrome eigenvectors of energy at least 2, and their closure gives a vacuum GNS gap at least 2. A single-edge Pauli attains 2.

This also follows from Naaijkens, Proposition 2.2, which gives the lower gap 4 for the convention -sum A-sum B; the projector convention here divides excitation energies by two. The statement concerns the specified frustration-free vacuum representation. The plane also has charged algebraic ground states in other representations. An isolated anyon is not a local excitation vector in this vacuum representation, and no claim about a charged-sector GNS gap is needed.

## 5 Exact scope of the conclusion

- The 1D result concerns the original displayed Rai Eq. (17), including its complete marginal constraint and its periodic-gap target. Replacing that target by the open Ising gap 1 would change the question.
- The toric result concerns the rectangular finite-displacement H-squared hierarchy explicitly defined in Section 3. The original 1D Eq. (17) is not silently relabeled as a 2D theorem.
- At every finite level the value 1 is a valid positive lower bound on the gap 2. Detection completeness is not refuted, and finite-level certificate validity is unaffected.
- The upper witnesses are restrictions of genuine translation-invariant larger-torus states. Adding constraints that are satisfied by all such restrictions cannot remove these witnesses. Changing the local coboundary while keeping the same truncated global operator cannot restore the discarded distant-defect contribution.
- The Ising model is noninjective and has two product vacua. The toric code is topological and has degenerate torus ground spaces. These examples do not satisfy the separately scoped primitive proper-MPS or strict-product/finite-depth-trivial-circuit promises. They do not settle exact-value convergence for genuinely injective PEPS.
- This is an obstruction to the stated hierarchy, not to all possible SDP gap methods. No repaired complete hierarchy is supplied.

## 6 Sources and review status

Rai, Kull, Emonts, Tura, Schuch and Baccari, *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, Quantum 10, 2065 (2026), arXiv:2411.03680v3: https://arxiv.org/html/2411.03680v3 . The exact original formulation and scope are documented in SOURCE_SCOPE.md. Section 2.3 already warns that the truncation may change the minimizer; Section 5 leaves completeness open. This packet does not allege an error in a proved general convergence theorem.

Kitaev, *Fault-tolerant quantum computation by anyons*: https://arxiv.org/abs/quant-ph/9707021 .

Naaijkens, *Localized endomorphisms in Kitaev's toric code on the plane*, Proposition 2.2 and Section 3: https://arxiv.org/html/1012.3857v2 .

Nachtergaele, Sims and Young, *Quasi-Locality Bounds for Quantum Lattice Systems. Part II. Perturbations of Frustration-Free Spin Models with Gapped Ground States*: https://doi.org/10.1007/s00023-021-01086-5 . This later source discusses non-frustration-free algebraic toric-code ground states, motivating the precise vacuum qualification above.

Two separate internal algebraic audits and their original check scripts are included unchanged. They are not external peer review. Targeted prior-art searches did not locate an explicit published calculation of this exact all-level plateau, but that is not sufficient evidence of novelty, priority, or publishability. The Ising/toric spectra and pair-creation mechanism are established facts; the claim established here is the elementary exact calculation for the specified optimization programs.
