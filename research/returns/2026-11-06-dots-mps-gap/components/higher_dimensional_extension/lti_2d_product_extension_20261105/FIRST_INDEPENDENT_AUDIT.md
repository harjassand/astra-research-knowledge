# Independent audit: 2D LTI completeness with strict product vacuum

## Finding
The parent's full-box strict-vacuum candidate admits a credible complete O(1/L) proof, not only O(L^{-1/2}). The crucial input is bounded dual objective, not clustering or LTI alone. The argument extends in the same way to fixed dimension D by replacing L^2 and O(L) with L^D and O(L^{D-1}). This is a proof audit, not a verified literature claim of novelty.

## Setup audited
K={0,...,R-1}^2, 0<=h<=M, ker h=span{|0_K>}, h>=c Q_K, Q_K=I-|0_K><0_K|. A={0,...,L-1}^2, D=A-A, Lambda=D+K, L>=R. rho>=0 obeys full local translation invariance wherever both operators fit and Tr rho h_0=1. Let
v=Tr rho [h_0^2 + (1/2) sum_{delta in D,delta !=0}{h_0,h_delta}].
Write c_delta=Tr rho h_0 h_delta and d=Tr rho h_0^2. Then c_{-delta}=conj(c_delta); disjoint-patch correlations are real nonnegative. Let s=R-1, q=(2R-1)^2-1. Each |c_delta|<=M by positive-functional Cauchy-Schwarz and local TI, and d<=M. Therefore
P := sum_{delta in D, ||delta||_infty>=R} c_delta <= v+qM.
Only the q overlapping offsets can be negative.

## Interior second moment
H_A=sum_{a in A}h_a, U=A+K. Exact pair counting gives
E H_A^2 = sum_delta (L-|delta_1|)(L-|delta_2|) c_delta.
For disjoint terms the multiplicity is <=L^2 and correlations are nonnegative. For overlapping terms the deficit in multiplicity is <=2sL. Hence
E H_A^2 <= L^2 v+2sqML.
This uses only the restriction of rho to U, which is contained in Lambda.

## Vacuum padding and clamp
Embed U in ANY torus of side N>=L+3R and put all exterior spins in the product vacuum. The nonzero-action terms consist of H_A and crossing terms V=sum_{y in Y}h_y, where in unwrapped coordinates
Y=[-s,L+s-1]^2 \ A,
|Y|=(L+2s)^2-L^2<=4sRL.
Terms completely in the exterior annihilate the padded state, so they contribute neither first nor second moments, even though they need not commute with crossing terms.
For y in Y let a(y) be the coordinatewise clamp of y into A. The retained support (K+y) intersect U is contained in K+a(y). With J the vacuum-padding isometry,
B_y=J* h_y J <= M Q_{(K+y) intersect U} <= (M/c)h_{a(y)}.
Set alpha=M/c. Each clamp fibre has cardinality <=m=R^2.

## Cross moment
J*{h_x,h_y}J={h_x,B_y} for x in A. If ||x-a(y)||_infty>=R, then h_x commutes with B_y and h_{a(y)}, and
{h_x,B_y} <= 2 alpha h_x h_{a(y)}.
For a fixed displacement a(y)-x, there are at most |Y| pairs (x,y). Summing far pairs thus costs <=2alpha |Y| P.
For each y at most u=(2R-1)^2 nearby x remain. The quadratic inequality +/-{h_x,h_y}<=h_x^2+h_y^2 and h^2<=Mh imply padded expectation <=M(1+alpha) per nearby pair. Therefore
E{H_A,V} <= |Y| [uM(1+alpha)+2alpha P].

## Seam second moment and the compression pitfall
Never write J*h_y h_z J=B_yB_z for overlapping crossing supports. Instead classify pairs as near if ||a(y)-a(z)||_infty<=3s. There are <=m(6s+1)^2 near z for each y. Positive-functional Cauchy-Schwarz gives |E h_y h_z|<=M alpha. For far pairs, the original supports are disjoint (clamp shifts have size <=s) AND the assigned interior supports are disjoint. Thus compression factorizes and tensor-factor monotonicity gives
J*h_y h_z J=B_yB_z <=alpha^2 h_{a(y)}h_{a(z)}.
For each displacement a(z)-a(y), multiplicity is <=m|Y|. Consequently, with w=(6s+1)^2,
E V^2 <=m|Y|[wMalpha+alpha^2 P].

## Consequence
E H_N>=L^2 and
E H_N^2<=L^2v+2sqML+|Y|[uM(1+alpha)+mwMalpha+(2alpha+malpha^2)(v+qM)].
The finite-torus gap inequality gives gamma_N L^2<=E H_N^2. This holds for EVERY sufficiently large N with exactly the same moments. Therefore one can take liminf or limsup in N without assuming periodic-gap convergence.
The strict kernel assumption already gives H_N>=c sum_i n_i and thus gamma_N>=c. A one-site defect trial state gives gamma_N<=R^2M. For feasible rho with v<=U0=R^2M, one may use the explicit constant
C=2sqM+4sR[uM(1+alpha)+mwMalpha+(2alpha+malpha^2)(U0+qM)].
Then v>=Delta_infinity-C/L. For v>U0 the same lower bound is automatic.
Soundness gives the reverse hierarchy bound lambda_L<=Delta_infinity: take the normalized reduced density matrix of a TI-averaged first-excited torus eigenstate and discard only nonnegative, disjoint-support pairs. The dual has a strictly positive feasible rho proportional to identity. Together with primal feasibility, this gives ordinary finite-dimensional SDP strong duality. The result is 0<=Delta_infinity-lambda_L<=C/L.
No trace bound on rho is needed, and an arbitrarily large vacuum component is harmless.

## Extension to entangled examples
A translation-covariant bounded-depth local unitary circuit (or locality-preserving *-automorphism with bounded spread and bounded-spread inverse) sends every positive local certificate and every translation coboundary to another such certificate, with only constant support expansion. This transfers the hierarchy limit and O(1/L) rate to its conjugated Hamiltonians. A fixed-period circuit can be handled after blocking a unit cell. The resulting ground states are explicit finite-bond-dimension PEPS. These are a restricted short-range-entangled class, not generic injective PEPS, and the conjugated interaction need not be the canonical projector parent interaction associated with a chosen PEPS tensor.

## Obstructions and limitations
1. LTI alone does not imply area-order seam second moment. For h_i=n_i, the all-excited translation-invariant state gives E(sum_{i in seam}n_i)^2=|seam|^2. Its dual objective is extensive in the displacement set, so bounded objective is the essential extra control.
2. Do not replace positive operators by larger ones inside a product unless the required disjoint tensor-factor commutation is checked.
3. A bound on boundary-state trace distance or ground-projector factorization alone does not yield a completely positive repair of arbitrary dual states with controlled H^2. Existing PEPS theorems below are not such a result.
4. Exact circuit conjugacy works; generic nonunitary PEPS filtering does not inherit it, because inverses/condition numbers can grow with boundary length.

## Verified sources and scope (literature search, not full independent proof verification)
- Rai, Kull, Emonts, Tura, Schuch, Baccari, "A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems", Quantum 10, 2065 (2026), arXiv:2411.03680v3. https://arxiv.org/html/2411.03680v3 . Original H^2 local-positive-decomposition/LTI hierarchy, finite-size criteria inclusion; paper explicitly says 1D FF completeness remains open and does not prove the present strict-vacuum result. Secs. 2, 5, App. A are closest baseline.
- Kastoryano, Lucia, Perez-Garcia, "Locality at the Boundary Implies Gap in the Bulk for 2D PEPS", CMP 366, 895-926 (2019), arXiv:1709.07691. https://arxiv.org/pdf/1709.07691 . Definition 9 and Theorem 10 give relative-norm boundary approximate factorization => ||P_AB P_BC-P_ABC||<=8 epsilon => bulk gap; supports MPO-injective extension under pulling-through conditions. Necessity from a gap is Conjecture 30, not proved there. This is no arbitrary-dual-state reconstruction theorem.
- Perez-Garcia and Perez-Hernandez, "Locality Estimates for Complex Time Evolution in 1D", Commun. Math. Phys. (2023), https://pmc.ncbi.nlm.nih.gov/articles/PMC10113381/ . A subsequent boundary-Gibbs/factorization source; useful for quasi-local 1D boundary assumptions but no generic gapped-PEPS implication was established in this audit.
- Kastoryano, "Spectral Gap of the Hexagonal AKLT Model via Boundary-State Factorization", arXiv:2609.27993v1 (Sept. 23, 2026). https://arxiv.org/html/2609.27993v1 . Theorem 1 assumes positive-definite cut paths, compatible shared initial half-boundary factors, and an integrated small remainder in the instantaneous relative boundary metric after subtracting one common response. It proves error exp(theta)-1. Corollary 3.1 additionally requires injective regional/ground-space and finite-scale hypotheses. The preprint claims AKLT application with cut-length times exponential-overlap error. Its theorem statement and scope were inspected; its long AKLT proof was not independently verified. Its formal verification covers a scalar majorant, not the whole operator proof.
- Perez-Garcia, Verstraete, Cirac, Wolf, "PEPS as unique ground states of local Hamiltonians", Quantum Inf. Comput. 8 (2008), arXiv:0707.2260. https://arxiv.org/pdf/0707.2260 . Explicit critical injective PEPS on hexagonal lattice show injectivity alone does not imply a gap.
- Schwarz, Buerschaper, Eisert, "Approximating local observables on projected entangled pair states", PRA 95, 060102(R) (2017), arXiv:1606.06301. https://arxiv.org/pdf/1606.06301 . Local-observable contraction/local indistinguishability results under uniform parent-gap assumptions, not a general repair map for arbitrary excited states.
- Lemm, "Finite-size criteria for spectral gaps in D-dimensional quantum spin systems", arXiv:1902.07141. https://arxiv.org/abs/1902.07141 . General-dimensional Knabe-type threshold 3/n for nearest-neighbor interactions, finite-range 3D extension. Closest standard combinatorial method, not exact-gap LTI completeness.
- Lemm and Mozgunov, "Spectral gaps of frustration-free spin systems with boundary", JMP 60, 051901 (2019), arXiv:1801.08915. https://arxiv.org/abs/1801.08915 . Criteria taking both bulk and edge gaps into account, n^{-3/2} threshold, not removal of generic boundary obstruction.
- Lemm and Xiang, "Quantitatively improved finite-size criteria for spectral gaps", J. Phys. A 55, 295203 (2022), arXiv:2112.07756. https://arxiv.org/abs/2112.07756 . Improved subsystem weighting across Euclidean/honeycomb/triangular lattices; no exact-gap completeness assertion found.
- Xu et al., "The bulk spectral gap is certifiable from above but uncomputable from below", arXiv:2606.03836v5 (Oct. 28, 2026). https://arxiv.org/abs/2606.03836 . General bulk-gap upper hierarchy and impossibility of general convergent lower algorithms already for 1D TI chains. The result must NOT be automatically applied to the present FF strict-product-vacuum restriction or to generic PEPS without checking their construction.

No source found proving exactly the bounded-objective seam estimate or O(1/L) strict-product-vacuum LTI completeness theorem. This is a bounded targeted novelty search, not a certification of originality.
