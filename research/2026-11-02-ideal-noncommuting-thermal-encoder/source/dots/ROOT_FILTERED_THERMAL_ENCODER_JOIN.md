# Root join candidate: a deterministic weakly noncommuting thermal encoder

1 November2026. Proposed construction, pending whole-interface review. This is an IDEAL quantum algorithm with fully counted classical/quantum operations, not a noisy physical deployment claim.

## Target capability
Prepare a logical encoding close to the actual finite-temperature Gibbs overwrite of a weakly noncommuting 3D code Hamiltonian, with a finite ACCESSIBLE engineered spin bath, without exponential global postselection, a target-marginal oracle, or dense synthesis on a logarithmic-radius volume. This is the preparation operation missing from the earlier exact-H storage theorem.

Inputs: the actual RX/RZ family and its fixed decoder; known bounded local H=Href+V with Href=H0+HB, HB onsite on N_B accessible qubits; fixed finite beta interval; sufficiently small local V; a supplied encoded logical ground-state input, possibly entangled with a reference. All N=n+N_B spins must be accessible during preparation. Baths are finite and N_B is polynomial in n for a polynomial-in-memory claim. Coupling acquisition, encoded input, reset/ancillas, gate faults and readout are separately charged interfaces. No claim of preparing an inaccessible infinite reservoir.

## 1. Classical sampling of actual quantum diagonal weights
For a valid memory syndrome sigma and product bath basis string b, let B_a: C²→H_MB be the matched code isometry into a=(sigma,b). Put
 G_a(s)=B_a† exp(-sH) B_a.
The diagonal-sector weight is p_a=Tr G_a(beta)/Z_H, with Z_H=Tr exp(-beta H). There is NO extra factor1/2 in p_a; sum_a p_a=1.

The actual quantum component expansion around Href, the code's filling property, and the logical distance cutoff are intended to give
 G_a(s)=g_a(s)[I+R_a(s)], ||R_a(s)||<=r_n
uniformly in a and s∈[0,beta], with r_n=poly(n)q^(d_n/c). Bath-only components are scalar at every size; memory-touching large components account for the relative remainder.

Small scalar quantum clusters produce a real, positive log-potential on the reference classical variables: actual memory trace polymers plus bath bits with independent onsite Gibbs prior. Polynomial filling gives polynomial dependence-set sizes and anchor reach, while cluster weights decay exponentially. This supplies the anchored potential moments required for the reviewed interacting-polymer sampler. Add ordinary single-bit heat-bath updates for bath variables; at sufficiently small V, joint weighted path coupling remains contractive. Finite connected-set inclusion–exclusion and local matrices on O(log(N/epsilon)) spins evaluate the truncated potential with polynomial cost. The resulting classical distribution approximates p_a, with truncation, large-component and finite-bit errors explicitly charged.

This sampler is a substantive interface under derivation/review, not an assumed TFD or conditional-marginal oracle.

## 2. Exact filtered parents
For the sampled a, let Q_j^a be the commuting violation projectors defining its reference code sector (signed memory checks and onsite bath basis projectors). They annihilate ran(B_a). Define
 A_a(s)=exp(-sH/2) B_a,
 L_j^a(s)=exp(-sH/2) Q_j^a exp(sH/2),
 F_a(s)=sum_j L_j^a(s)† L_j^a(s).
Then F_a(s)>=0 and its EXACT zero eigenspace is ran(A_a(s)), of dimension2. This follows from invertibility of exp(-sH/2); it is not a numerical gap assertion.

At V=0, [Href,Q_j^a]=0, so F_a(s)=sum_j Q_j^a for every s. For fixed beta, sufficiently small V gives an exponentially decaying local interaction expansion for F_a(s)-F_a(0), uniformly in a. The reason is the commuting-reference interaction picture: a perturbation term's imaginary-time support expands only to one bounded check-star before connected V insertions. A k-label connected cluster has O(k) physical spins and geometrically decaying activity for q=C beta v exp(C beta J) sufficiently small.

All orderings/repetitions are summed using inclusion–exclusion of exact finite-cluster conjugations, not k! ordered-history enumeration. Cutoff k=O(log(N/epsilon)) yields polynomial classical construction and Hamiltonian simulation cost. The Hamiltonian terms remain physically synthesized through their actual finite supports; shortcut graph edges below are ANALYTICAL and are not free physical gates.

## 3. Gap gate through an honest analysis-graph change
The actual filling proof uses only O(log(1+m)) ancestry levels for a weight-m stabilizer. A bounded-degree O(n)-vertex multilevel host tracks this support. A bounded-load internal-to-descendant-leaf matching converts it into a shortcut supergraph on REAL top-level check vertices, without adding Hamiltonian terms or physical qubits. Pair it with a compatible qubit graph using support cliques and complete bipartite support links for adjacent checks, retaining physical finite-range adjacency with bounded degree.

In this analysis graph, required stabilizer generators lie within O(log(1+m)) distance of their support, giving the linear-radius TQO-II condition used in De Roeck et al2411.02384v3. The code distance supplies TQO-I. A separate proof audit checks that their argument extends to this compatible bounded-degree supergraph pair; this is not a literal unchanged application to an independently enlarged metric.

If the geometry and theorem-extension gates pass, their spectral-band stability applies to the small quasilocal filtered-parent perturbation. Valid signed syndrome parents are Pauli conjugates of the original one, so the constants are uniform. Since the exact filtered parent already has a two-dimensional ZERO kernel, the gap above it remains bounded below by a fixed positive constant.

## 4. Deterministic adiabatic preparation, not postselection
Starting from B_a rho_LR B_a†, evolve adiabatically under F_a(s), s:0→beta. A uniform gap and polynomially bounded global derivatives give a polynomial run time for target error. The exact ground energy stays zero, avoiding uncontrolled dynamical logical phases. Simulate the finite-cluster parent to global error epsilon divided by the charged run time; cutoff and precision remain logarithmic/polynomial respectively. No product of heralded success probabilities appears.

The canonical endpoint isometry is W_a(s)=A_a(s)G_a(s)^(-1/2). Because H is fixed and s alone varies, A_a† A_a'=G_a'/2 is Hermitian. If G_a=g_a I exactly, W_a†W_a'=0 exactly: canonical filtering IS parallel transport. Uniform relative Gram error r_n instead gives a polynomial(N)*r_n bound on accumulated logical connection, provided the derivative estimate is earned. This is special to this beta-only path; no arbitrary-path holonomy is assumed away.

## 5. Quantum ensemble and storage interface
Average the canonical filtered isometries with p_a. Near-scalar Gram matrices make this channel close to the thermal insertion
 rho_LR -> 2 sqrt(rho_H) (rho_LR tensor I_GB) sqrt(rho_H)
with the appropriate tensor ordering. The reviewed actual-H logical-twirl estimate rho_H≈I_L/2 tensor tau_GB and square-root continuity then make the ensemble close, reference-safely, to rho_LR tensor tau_GB: the exact thermal overwrite used by the storage theorem.

Total error is the SUM of classical sampling error, classical numerical error, parent simulation/adiabatic error, logical transport error and thermal-ensemble comparison error. Later exact-H storage adds its independently proved memory error. Initial preparation discrepancies are not multiplied by the exponentially long hold time.

## What this would and would not close
If all interfaces pass, this is an explicit polynomial IDEAL thermal-encoding algorithm for the actual weakly noncommuting code/accessible-bath class, rather than an assumed interacting-Gibbs input. It also provides a scientific state-preparation capability on an ideal or fault-tolerantly encoded quantum processor.

It does NOT by itself yield a native autonomous device, an inexpensive finite-size implementation, robustness of the released physical state to arbitrary final gate noise, or preparation without access to bath spins. A fault-tolerant simulation can keep the prepared state encoded, but releasing it into unprotected physical hardware needs a separate admitted terminal interface. The calibrated commuting terminal-noise theorem and the positive quantum inverse-noise state are components, not an already earned generic noisy release.

All fixed construction/temperature constants can be extremely large or small. No practical advantage over active FT, experimental demonstration, peer review or civilisation-level breakthrough is asserted. The code, gap-stability machinery, conventional polymer sampling and adiabatic algorithms are credited to their governing sources; the candidate contribution is their earned actual-code representation and constructive filtered-parent join.

## Accuracy and compilation clarifications

The scalar-small-component sampler has an intrinsic relative remainder eta_n=poly(n)q^(d_n/c). Its stated cutoff L=O(log(N/epsilon)) must remain below the logical-component cutoff. This covers every inverse-polynomial requested computational accuracy for N polynomial in n, and a stretched-exponential regime; it is NOT an arbitrary-precision exact sampler of p_a. Retain that intrinsic remainder in the final encoding error rather than hiding it inside an unrestricted epsilon claim.

Parent linked sets are ROOT-connected: C union {Q_a} must be connected. The perturbation set C alone may have several branches meeting the root. All finite connected-set counts and O(k)-spin matrix computations are unchanged under this fixed-root convention. Global Hamiltonian/transport norms scale with TOTAL accessible N=n+N_B.

The ideal circuit can in principle be run in an admitted fault-tolerant encoded representation, with its ordinary overhead and input-interface error charged. That does not automatically release the desired state into a noisy unencoded physical memory; such a release is a distinct operation.

## Finite-bath gap completion

For accessible bath QUBITS, diagonalize each known onsite reference Hamiltonian by its local eigenbasis and add its actual rank-one basis violation as an onsite signed Z check to the preparation parent. This is an auxiliary PARENT Hamiltonian term, not an added interaction in the storage Hamiltonian. Complete the analysis graphs by adding these actual bath check/qubit vertices and the bounded-degree lifts of physical finite-range interaction edges. The parent code remains one logical qubit: product bath checks do not reduce memory code distance. Any stabilizer product splits into a memory stabilizer and onsite bath Z factors; the all-support anchored memory filling plus onsite bath filling gives the same TQO-II condition. Thus the gap theorem's d_*>=c log N requirement follows when N=n+N_B is polynomial in memory n. No arbitrary-volume or inaccessible-bath algorithm is inferred.

## Explicit final accuracy statement

In the admitted cutoff regime, the intended output encoding error is
 C[epsilon + beta N eta_n + sqrt(delta_tw,n)],
where epsilon includes all chosen classical and quantum computational tolerances, eta_n is the uniform small-sector logical remainder, and delta_tw,n is the actual Gibbs-to-logical-twirl distance. Constants are fixed by the construction and finite-temperature interval. This is polynomial-cost preparation to any inverse-polynomial computational tolerance with an explicit stretched-exponentially small intrinsic remainder, not arbitrary exact precision for fixed n.

## Strongest inspected predecessors

The filtered-parent and linked-set computational method is established: Ge–Molnar–Cirac1508.00570v2 treats high-temperature noncommuting Gibbs preparation. Xun–Cao–Watanabe2610.27939v1 supplies a closely related low-temperature diagonal sampling/filtered-parent architecture for classical gauge references, without claiming efficient elementary-gate decomposition. METTS supplies the weighted-filtered-state ensemble identity. The candidate contribution here is the earned actual QUANTUM code/host gap, polynomial compilation and reference-safe degenerate logical transport, not invention of the general architecture. See PRIMARY_PRIOR_CAPABILITY_GATE.md for exact scope and sources.
