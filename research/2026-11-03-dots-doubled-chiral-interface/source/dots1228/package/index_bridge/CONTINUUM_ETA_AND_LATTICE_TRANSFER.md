# Continuum eta charge and the actual Wilson-slab transfer gate

2026-11-03. Independent constructor. Status: a concrete continuum eta derivation and sign calibration are supplied; the requested finite open-slab equality is NOT proved. The closed-torus replacement fails the current onsite-symmetry contract and is not presented as the same slab.

## Primary machinery: exact scope

The 2026 article DOI10.1007/s11005-026-02080-w (preprint2407.17708) compares twisted Dirac operators on a closed flat torus with Hermitian Wilson operators. Its proof uses lattice/continuum interpolation, a priori estimates and compactness contradiction to obtain sufficiently small spacing. Its boundary discussion explicitly leaves the lattice boundary extension open. Thus its finite index equality is strong but not an open-slab boundary-Higgs theorem or a supplied explicit refinement bound.

Kubota2009.03570 Theorem1.6 proves the corresponding closed-torus index for cutoff-scale Wilson mass0<m<2 and also a sufficiently large fixed mass. The operator is twisted by a bundle connection; a boundary SU(2) Higgs mixing is not such input without an additional transfer.

1910.09675 writes a lattice domain-wall eta invariant and evaluates the bulk/edge formula perturbatively up to O(a), in a hierarchical mass regime. Its boundary contribution is essential, including the far boundary. It does not supply a nonperturbative theorem for our Higgs slab.

Sources: https://doi.org/10.1007/s11005-026-02080-w ; https://arxiv.org/html/2407.17708 ; https://arxiv.org/html/2009.03570 ; https://arxiv.org/html/1910.09675 .

## 1. An actual continuum eta argument, not an assumed anomaly coefficient

Let the compact flat3-torus carry any fixed spin structure. On8-component spinors take

h_M=alpha_i p_i+M beta_a n_a(x), a=0,1,2,3,

with seven Hermitian anticommuting Clifford matrices and n:T³→S³ smooth. Put L1=sum_i||partial_i n||_infinity in the corresponding matrix norm. Then

h_M²=p²+M²+V, V=−iM alpha_i beta_a partial_i n_a,
||V||<=M L1,

so gap(h_M)>=sqrt(M²−M L1). In particular M>L1 gives an actual volume-independent continuum one-particle gap.

For a smooth variation of a zeroth-order mass field Phi=beta_a phi_a, the derivative of the eta invariant is proportional to the t^{−1/2} heat coefficient of Tr[deltaPhi exp(−t h²)]. In3 spatial dimensions this is the integrated trace of deltaPhi times the Laplace-potential term (flat curvature is zero). Here that trace vanishes identically: it contains either one Clifford matrix, or three Clifford matrices. Therefore eta is locally constant along every gapped mass-only path. In particular eta(h_M) is constant for every M>L1.

Its value can then be evaluated as M→infinity. Use

sign(h)=(2/pi) integral_0^infinity h(h²+omega²)^{−1} d omega

with a spin-compatible heat/spectral regulator. Expand the resolvent around R0=(p²+M²+omega²)^{−1}. Terms with fewer than three V factors have zero Clifford trace. The first nonzero term is the mass numerator and three V insertions. The kinetic numerator at that order has zero trace. Replacing the three smooth fields at intermediate kernel points by their value at the trace point gives the local winding term.

This asymptotic step is controllable rather than a formal expansion: for M>=2L1 the resolvent Neumann series converges in norm; the remainder from four or more V factors is bounded by a constant times Vol(T³)L1^4/M. Kernel first-moment bounds control replacement of the fields in the cubic term by O(Vol L1²L2/M), L2 a bound on second derivatives. The torus sum differs from the Euclidean momentum integral by exponentially small image terms. The exact numeric remainder constant has not been optimized, but every term tends to zero. Since eta was already proved constant in M in this region, the limiting value fixes it exactly for all M>L1, without needing a numerical asymptotic remainder smaller than one.

The scalar integral is

integral_0^infinity d omega integral d³p/(2pi)³ (p²+M²+omega²)^{−4}
=1/(96pi M^4).

For alpha_i=−rho_z tensor sigma_i tensor I, beta_0=rho_x tensor I tensor I, beta_j=−rho_y tensor I tensor tau_j,

tr(alpha1 alpha2 alpha3 beta0 beta1 beta2 beta3)=−8i.

Combining the cubic resolvent term with Q_eta=−eta/2 yields

Q_eta=degree(n)
=(1/(12pi²)) integral epsilon_ijk epsilon_abcd n_a partial_i n_b partial_j n_c partial_k n_d.

The uniform positive raw norm of the barycentric texture allows an explicitly local smoothing and renormalization at fixed fraction of its coarse scale. It preserves degree, changes the first-derivative bound by a controlled constant, and gives finite higher derivative bounds needed above. This is a continuum regulated number, not yet the finite Wilson occupied count.

## 2. Texture convention fixes a sign

For the SU(2) completion used in the code,

U=[[z,w],[−w*,z*]]=n0 I+i(n1 tau_x+n2 tau_y+n3 tau_z),

so n=(Re z, Im w, Re w, Im z). Relative to the spinor coordinates (Re z,Im z,Re w,Im w), this permutation reverses orientation. Thus degree(n)=−degree(q)=−s. For the continuum kinetic convention alpha_i=−rho_z sigma_i, the preceding calculation gives exactly Q_eta=−s.

## 3. The actual code has the opposite near-face kinetic orientation

The current Wilson representative uses Gamma_i=X tensor sigma_i (i=1,2,3), Gamma4=Y tensor I, Gamma5=Z tensor I and normal hopping

T=−Gamma5/2−i Gamma4/2.

At tangential momentum zero,m=−1, a surface state at the massed face w=0 obeys T†psi=0, equivalently

i Gamma5 Gamma4 psi=psi.

Since i Gamma5 Gamma4=X tensor I, that surface has X=+1 and Gamma_i restrict to +sigma_i. Consequently the current w=0 boundary corresponds to alpha_i=+rho_z sigma_i, NOT the minus convention in Section1. It reverses the Clifford trace and gives Q_eta=+s in the same x,y,z orientation. The opposite face gives the opposite sign.

Therefore the desired minus-s target requires an explicitly chosen slab/root orientation (or a declared opposite boundary orientation). It cannot be inferred merely by quoting the continuum anomaly. This algebra does not prove the lattice count is plus-s either; it calibrates the continuum branch that the lattice should approach.

## 4. Why the closed-torus index gadget is not an earned repair

Clutching the SU(2) texture into a bundle on T³×S¹ gives a genuine Dirac index equal, with orientation chosen, to its winding. A finite-range Hermitian Wilson operator then has filled-number shift N_neg−dim/2=−eta/2. This is a valid index-to-filled-number operation for that DIFFERENT closed, gauge-twisted model.

But our global V acts as U→D(alpha)U, not conjugation. At one seam U can intertwine a D-charged patch and a neutral patch. A second fixed identity seam on a closed circle is then not covariant. The Maurer-Cartan connection U†dU being invariant does not remove the transition data: discarding the nontrivial clutching makes a trivial bundle and loses the index. A global rotor anchor can supply another frame but violates the requested locality; choosing U again cancels the net degree. A smooth equivariant S³→S¹ frame cannot be obtained from the spinor alone (it would trivialize the Hopf bundle).

This is a failure of the proposed gadget's actual symmetry contract, not a theorem excluding every possible local auxiliary construction. Extra fields, discontinuous patch prescriptions or changed fermion representations would need their own explicit locality, covariance and index proof. None are assumed here.

## 5. Quantitative facts that do not by themselves close the slab transfer

For smooth clutching connection A=f(y)U†dU, curvature is

F=f' dy wedge(U†dU)+(f²−f)(U†dU) wedge(U†dU).

Thus ||F|| is bounded by O(L1/L_normal+L1²). A lattice of spacing a has plaquette deviation O(a²||F||). Standard Wilson admissibility estimates then give a nonzero gap for the CLOSED gauge operator; e.g. a conservative four-dimensional m0=1 bound is (aH_W)²>=1−30 epsilon when every plaquette differs from identity by at most epsilon. This can pay a gap scale for that operator. It does not identify the open Higgs-slab eta, and a small plaquette norm alone is not a bound on the unspecified index-matching threshold in the compactness theorem.

For the actual slab the required independent ledger is:
- boundary mass window L1<<M<<a^{-1}, avoiding the previously verified strong-mass mirror relocation;
- finite-range Wilson half-space spectral convergence in that window, including all UV/doubler contributions to the RELATIVE eta, not only low modes;
- far-face sector and finite-volume Fermi gap, with thickness chosen so face hybridization is smaller than that gap;
- exact reference subtraction and orientation calibrated above.

Low-energy norm-resolvent convergence alone is insufficient for eta: infinitely many/UV modes can carry the integer counterterm. The closed-torus source supplies no automatic bound for these missing entries. Thus exact finite-slab charge minus-s and a paid uniform UV refinement are not claimed.
