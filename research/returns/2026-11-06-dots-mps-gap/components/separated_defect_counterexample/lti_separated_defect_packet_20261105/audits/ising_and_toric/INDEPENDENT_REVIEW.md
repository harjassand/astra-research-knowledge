# Exact counterexamples to unrestricted LTI gap-value completeness

2026-11-05. Independent internal algebraic audit and exact finite-dimensional checks. This is not a priority claim or external review. The counterexamples concern the displayed finite-cutoff H-squared/LTI hierarchy, not every possible SDP gap method.

## Verdict

The obstruction is valid. The hierarchy's value is exactly **1 at every finite level**, while the periodic gap is exactly **2**, for both:

1. the nearest-neighbor ferromagnetic Ising projector chain, using the original one-dimensional Rai LTI formulation; and
2. the usual toric-code projector Hamiltonian, grouped into translation-equivalent two-qubit cells and tested with the full rectangular LTI formulation.

The selected uniform-vacuum Ising GNS gap and frustration-free plane-vacuum toric GNS gap are also 2. These GNS statements require specifying the representation; a single kink or anyon cannot silently be treated as a finite local excitation of that vacuum.

There is no approximate or moment-only marginal assumption. I give explicit positive finite-window densities satisfying the complete face-marginal equalities, and a separate construction using actual translation-averaged two-defect torus eigenstates. The latter witnesses are globally extendible.

This disproves general **exact gap-value** completeness of this hierarchy. It does not disprove eventual detection of a positive gap: the lower bound 1 is already positive. It does not contradict the separately scoped primitive-MPS, strict-product, or finite-depth trivial-circuit results.

## 1. The original one-dimensional hierarchy: an explicit density matrix

Take

    h_i=(I-Z_i Z_(i+1))/2,
    H_N=sum_(i mod N) h_i.

Each h_i is a commuting projector. The periodic Hamiltonian counts domain walls. Every periodic binary string has an even number of walls, and a finite nonempty reversed domain has two. Thus the lowest nonzero periodic eigenvalue is

    Delta_N=2,  N>=2.

The two homogeneous strings span the ground space. Ground degeneracy does not change the definition of the first positive eigenvalue.

On n sites define the unnormalized positive diagonal operator

    rho_n=(1/2) sum_(j=1)^(n-1)
       [ |0^j 1^(n-j)><0^j 1^(n-j)|
         +|1^j 0^(n-j)><1^j 0^(n-j)| ].

Its trace is n-1. The exact full marginal identity is

    Tr_1 rho_n = Tr_n rho_n
       = rho_(n-1)
          +(1/2)[|0^(n-1)><0^(n-1)|+|1^(n-1)><1^(n-1)|].

Since the matrices are diagonal, this equality includes every off-diagonal matrix entry as well: both sides' off-diagonal entries are zero. This is the complete LTI constraint, not just equality of a selected set of moments.

For every internal bond i,

    Tr rho_n h_i=1.

Every basis vector in the support has exactly one internal domain wall, so for every distinct pair i,j,

    h_i h_j rho_n=0.

Consequently the actual nearest-neighbor objective of the original full LTI hierarchy is

    Tr rho_n [h_1^2+sum_(j=2)^(n-1){h_1,h_j}] = 1.

Thus gamma_n<=1 at every valid n>=3. Conversely,

    h_1^2+sum_(j=2)^(n-1){h_1,h_j}-h_1
      =2 sum_(j=2)^(n-1) h_1 h_j >=0.

This is the primal certificate delta=1 with zero coboundary. Matching feasible primal and dual witnesses prove exactly

    gamma_n=1 for every n>=3,  while lim_N Delta_N=2.

No numerical SDP, optimizer assumption, limiting exchange, or questionable strong-duality step is needed.

### A globally extendible version

On a sufficiently large ring choose a string with one long zero domain and one long one domain, with both domain walls farther apart than every retained displacement. It is an exact energy-2 eigenstate. Average its density over all translations. The result is exactly TI, with local energy 2/N. Restrict it to the n-site window and multiply by N/2.

The restricted density is positive, has exact full LTI, has Tr rho h_1=1, and has every retained distinct product equal to zero. Its objective is again 1. A suitable global first-excited state therefore already realizes the ceiling; nonextendibility of general LTI marginals is not the source of this example.

### Ising GNS sector

In the GNS representation of the all-zero product state, the finite-flip configurations form a complete orthonormal basis. A nonempty finite flipped set has at least two boundary bonds; a one-site flip attains two. The closure of the diagonal Hamiltonian has spectrum {0,2,4,...}, with gap 2 and unique vacuum.

An infinite single-kink configuration is not a finite-flip excitation in this representation. Comparing its one local wall penalty with the chosen vacuum-sector gap would be a sector error. The periodic comparison above does not depend on any GNS convention.

## 2. Precise toric-code convention

Use cells r in Z^2, each containing two qubits: the horizontal outgoing edge from r and the vertical outgoing edge from r. Let

    A_v = X_(horizontal v) X_(horizontal v-e_x)
          X_(vertical v) X_(vertical v-e_y),
    B_p = Z_(horizontal p) Z_(vertical p+e_x)
          Z_(horizontal p+e_y) Z_(vertical p).

All stars and plaquettes commute. For a 2x2 cell patch anchored at r define

    h_r = (I-A_(r+e_x+e_y))/2 + (I-B_r)/2.

Every h_r is supported within that 2x2 patch. Summing h_r over cells counts each star and each plaquette once. Each h_r has eigenvalues 0,1,2; all translates commute.

On an N-by-N torus, for N>=3, the two global relations are

    product_v A_v=I,   product_p B_p=I.

There are 2N^2-2 independent stabilizers on 2N^2 qubits, giving a four-dimensional ground space. Star and plaquette violations separately have even parity. A finite open Z string creates exactly two stars of energy one each, so

    Delta_N=2.

These are full-system eigenvalues, not a one-particle dispersion or a chosen logical sector's splitting.

## 3. The simplest toric witness: two distant torus defects

Fix any finite hierarchy window and finite set D of retained nonzero displacement vectors. Choose a much larger torus and two star defects whose two relative displacements avoid D modulo the torus. All plaquettes have eigenvalue +1. This syndrome obeys the two global parity relations and has a nonempty simultaneous-stabilizer eigenspace of exact dimension four.

Use the normalized projector onto that eigenspace, or any pure state in it, then average over translations. The state has total energy 2 and local energy 2/N^2. Since the only occupied local h cells are the two separated star-defect cells, every retained distinct product satisfies

    Tr sigma h_x h_(x+z)=0,  z in D.

Restriction of a translation-invariant state to a finite rectangular window has exactly equal opposite-face marginals. Scaling the marginal by N^2/2 therefore gives a valid full-LTI dual rho with

    Tr rho h_0=1,
    Tr rho h_0^2=1,
    Tr rho {h_0,h_z}=0 for every retained z!=0.

The objective is exactly 1, including the centered rectangular half-sum convention. Positivity and LTI hold by construction, not by a boundary ansatz.

For the lower bound, all h translates commute and are positive, and

    h_0^2-h_0 = 2 Q_star Q_plaquette >=0.

Adding any of the retained positive anticommutators preserves positivity. Thus the zero-coboundary primal certificate delta=1 is feasible, and every such finite-cutoff full-LTI level has exact value 1.

## 4. Independent finite-window toric density and full face verification

The global construction is sufficient, but I independently checked a local construction to test the difficult marginal issue directly.

On an a-by-b rectangular cell window, let Q=2ab be the number of physical qubits and m=(a-1)(b-1). Include every star and plaquette fully contained in the window. There are m of each, and all 2m stabilizers are independent. For each contained star t, let P_t be the joint eigenspace projector with that star negative, every other contained star positive, and every contained plaquette positive. Boundary degrees of freedom are unconstrained. Every P_t has the same positive rank

    D0=2^(Q-2m).

Define

    rho_(a,b) = (1/D0) sum_t P_t.

It has trace m, every contained h_r has expectation one, and every distinct h_r h_s has expectation zero. This yields the same objective 1.

The complete Pauli expansion is especially explicit:

    rho_(a,b) = 2^(-Q) sum_(S,T)
          [m-2|S|] A_S B_T,

where S and T run over subsets of contained stars and plaquettes, and A_S/B_T are their products. Positivity follows from the projector sum, even though some Fourier coefficients are negative.

When tracing an extreme face, a product of crossing star generators cannot cancel on that face: the boundary horizontal or vertical edge associated with each crossing star is unique among the crossing stars. The same argument applies independently to crossing plaquettes using the other edge orientation. A mixed X/Z product cannot cancel a nonzero X or Z mask into identity. Therefore the surviving stabilizer subgroup is exactly the group generated by the individually surviving stars and plaquettes.

Let m' be the surviving number of stars and let d=m-m' be the number removed. Partial trace gives exactly

    Tr_face rho_(a,b)
       = (1/D0') [sum_(surviving t) P_t' + d P_vac'],

where D0' is the rank of a surviving-window syndrome projector. Opposite faces remove the same number d, and after coordinate identification their surviving stabilizer generators and syndrome projectors coincide. Thus the two **entire density matrices** coincide, including nonlocal Wilson-loop and off-diagonal observables.

This is stronger than checking local energies or a finite list of correlations. The exact Pauli-coefficient comparisons and outside-subgroup ranks in the accompanying script verify it directly.

## 5. Toric vacuum-GNS gap and sector caution

Choose the frustration-free plane vacuum with every star and plaquette +1. Finite-support Pauli operators applied to its GNS vector span a dense local domain. Any such Pauli creates an even number of star defects and an even number of plaquette defects: every flipped edge has two endpoints on the appropriate lattice. A nonvacuum syndrome therefore has energy at least 2, and a one-edge Pauli attains 2.

A finite Pauli with no defects is a product of contractible stabilizers on the plane and acts as a scalar on the vacuum. Thus the vacuum kernel is one-dimensional in this GNS representation. Decomposition into the stabilizer syndrome eigenvectors on the dense local domain gives the vacuum-GNS gap 2.

An isolated anyon obtained by taking a string endpoint to infinity is not a local finite-energy vector of this vacuum representation. It belongs to a different superselection representation. Our globally extendible dual construction does not assert otherwise: both anyons are present on every finite torus, but their separation increases with the chosen cutoff. The cutoff omits their positive mutual H-squared contribution.

I also checked the primary source P. Naaijkens, *Localized endomorphisms in Kitaev's toric code on the plane*, arXiv:1012.3857v2, Proposition 2.2 and Section 3, https://arxiv.org/html/1012.3857v2 . Proposition 2.2 supplies vacuum-GNS spectral exclusion below 4 in its -A-B convention; dividing by two gives the lower bound 2 here. A single-edge Pauli supplies the matching upper bound. The source's broad older ground-state uniqueness wording is not used to assert uniqueness among all algebraic ground states: our statement concerns the specified frustration-free vacuum representation and distinguishes charged sectors.

## 6. What fails, and what remains valid

For a separated two-defect state, H has energy 2 and H^2 has expectation 4. The truncated square sees the two self-energies, totaling 2, but drops their cross contribution of 2. After energy normalization, its objective is 1. At each larger finite cutoff, the defects can be moved farther apart again.

The failure is therefore already in the first, finite-displacement truncation of H^2, not necessarily in the later full-LTI marginal relaxation. More local face constraints alone cannot fix these globally extendible witnesses. No repair algorithm is claimed here; a different hierarchy would need information that retains the missing separated-charge contribution.

Precise limits:

- This gives a negative answer to unrestricted **value** convergence for the displayed hierarchy. It leaves positive-gap detection completeness unanswered.
- It does not invalidate the hierarchy's finite-level lower-bound certificates: 1 remains a correct lower bound on 2.
- The 1D Ising model has multiple product vacua and is not a proper **primitive/injective** MPS parent. The toric code is not a strict-product parent or a finite-depth trivial-circuit image. The previously reviewed restricted theorems are not counterexampled.
- Neither the proof nor the exact finite checks establishes novelty. The examples are elementary commuting-projector models, and the physical gaps and sector structure are standard.

## 7. Primary-source convention check

I inspected the primary text of Rai et al., *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, arXiv:2411.03680v3, https://arxiv.org/html/2411.03680v3 . Its Section 2 explicitly uses periodic boundary conditions and defines Delta_N as the lowest nonzero eigenvalue. The displayed nearest-neighbor dual, Eq. (17), has exactly positivity, full left/right marginal equality, and Tr rho h_1=1, with the objective used above. Section 3.2 distinguishes periodic Delta from open epsilon, and Section 5 lists exact value convergence separately from eventual positive-gap detection.

Therefore the Ising counterexample is not explained away by silently replacing the paper's periodic gap with the open-chain gap 1. A limited targeted search did not locate a published statement of this exact hierarchy counterexample; that is a search limitation, not a priority claim. No author contact or external publication has been undertaken.

## 8. Exact computational checks

`check_explicit_witnesses.py` imports no constructor code and uses integer/Fraction arithmetic for all witness, marginal, syndrome-rank, and normalization checks. `results.json` records:

- ten exact Ising full-LTI densities for n=3 through 12;
- three globally extendible Ising torus witnesses;
- seven toric open rectangles, including complete Pauli-expansion face equality through 4x4 cells and outside-support rank checks through 5x7 and 8x6 cells;
- an actual 256-dimensional integer density numerator for the 2x2-cell toric window, with an exact projector polynomial proving positivity;
- three valid large-torus toric syndrome witnesses, with exact stabilizer rank, nonempty four-dimensional syndrome subspace, excluded defect separations, and N^2/2 normalization.

These checks directly address full marginals and finite-dimensional positivity. The analytic constructions establish all levels, not an extrapolation from these examples.
