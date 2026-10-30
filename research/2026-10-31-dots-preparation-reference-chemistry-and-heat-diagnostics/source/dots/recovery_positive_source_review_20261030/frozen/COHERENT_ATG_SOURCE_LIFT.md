# Coherent ATG source lift from actual product-defect moments
2026-10-30. Source-bound receiving theorem. The subset-moment hypothesis below is supplied/proved separately by root; this note constructs its circuit, deterministic target span and physical sign interface. Not an autonomous controller theorem.

## 1. Explicit circuit and resources
Let the base CSS code be ell-LDPC. Construct the alternating Tanner graph G on 2T+1 code layers with the usual alternating check vertices, leaving the two end DATA layers unmeasured. Each graph vertex has degree at most Delta<=ell+2. Let B be the measured bulk and ∂ the 2n boundary DATA vertices. Use one actual pointer R_v for each v in B.

Prepare graph vertices in |+> and pointers in |0>. Execute

 U = [parallel CNOT(v -> R_v), v in B]
     [parallel H_v, v in B]
     [product CZ_(uv), (u,v) in E(G)].

A greedy edge coloring uses <=2Delta-1 CZ layers; adding H and CNOT gives depth <=2Delta+1, independent of n,T. Gates have support<=2 and fixed graph-local degree. Space is O(ell nT), including pointers. Each gate can be run for a fixed O(1) physical duration with bounded Hamiltonian norm; that is a declared scheduled source, not an autonomous clock/compiler.

An arbitrary fixed-body perturbation conjugated by any partial ideal circuit has support in a constant-size backwards lightcone (conservative size <=q*2^(2Delta+1)) and bounded incident norm enlarged only by Delta-dependent constants. Intermediary partial gates need not be Clifford for this locality statement. The completed ideal circuit is Clifford.

After U, pointers may be dephased/read in Z and measured graph vertices discarded, but neither operation is needed for the source-span claim: retain both registers coherently and resolve the pointer computational components only in the analysis. No quantum feedforward is used in this circuit. Any further waiting/capture interval must be separately protected and is not silently included in its constant depth.

## 2. Exact product-defect dictionary
Use the complete orthonormal input basis obtained by Z flips on graph |+> inputs and X flips on pointer |0> inputs. Denote their bit labels by a_v and c_v. The corresponding commuting projectors are (I-X_v)/2 on graph inputs and (I-Z_Rv)/2 on pointers.

Because every input graph Z commutes with every graph CZ, after deferred readout/discard:

 - for v in B, effective raw outcome error f_v=a_v+c_v (mod2);
 - for v in ∂, physical boundary error is E_B=Z^(a|∂).

Pointer X commutes through its target CNOT; graph Z becomes the ordinary sign flip of an X measurement. The measured graph qubits may retain branch phases, but these multiply amplitudes only and do not change the target span in a fixed recorded branch. Thus this dictionary is valid for coherent superpositions of defect basis vectors, not only a sampled Pauli channel.

The effective bulk support is covered by the OR of TWO disjoint input-defect bits per bulk vertex; boundary vertices have one. If input defect distribution obeys

 Pr[S subset defect support] <= q^|S|,

then the effective covering support obeys the same inequality with Q=2q. For a set of k bulk/boundary vertices, choose one of at most two distinct defect bits at each vertex, union-bound over <=2^k choices, and apply the subset bound. No source-volume factor occurs.

## 3. Deterministic common decoder convention
Fix a minimum-weight bulk estimate beta(y) as a deterministic function ONLY of metasyndrome y, using a fixed tie-breaking order. For the actual record m, y=M m. Ideal graph outcomes obey M s=0, so y=M f and beta depends only f, not on random valid s.

Choose the boundary Pauli frame P(m) by solving the boundary/Bell stabilizer sign equations for m+beta(Mm), with a fixed deterministic rule. For each effective bulk pattern f, all nonzero ideal measurement branches then satisfy

 P(m)^dagger |boundary_(m,f)> = scalar(m,f) Rep(f)|Bell_L>.

The residual stabilizer and logical signs are linear functions of f+beta(Mf); all appearances of the random valid record cancel. Hence Rep(f) may be chosen once for f, uniformly over every allowed m. Arbitrary branch phases are retained. This fixed tie-breaking is essential: letting beta depend unnecessarily on all raw bits would not earn the uniform statement.

The actual output is NOT required to apply P(m) at this stage. It is an analysis frame for the physical record-dependent input module of the receiver.

## 4. Hereditary good-support certificate
Use the two bounded-degree syndrome adjacency graphs of the ATG decoder. The deterministic clustering facts are extracted in source_certificate/DETERMINISTIC_ATG_SOURCE_SPAN.md. Here is the exact criterion needed, stated as excluded witnesses in the EFFECTIVE covering support F, so that it holds for every f subset F:

(A) No connected bulk witness of size s>=T with at least s/2 occupied F vertices.
(B) No completed connected witness of size s>=d with at least s/4 occupied F vertices.
(C) For any selected set of a=floor(t/2)+1 boundary roots in either sector, no union of connected sets containing those roots, with EVERY component containing at least one selected root, of total size s>=2a, has at least s/4 occupied F vertices. Actual repair components meeting the selected erroneous boundary sites satisfy this rooted condition.

Minimum-weight component replacement proves the occupancy constants; temporal telescoping relates boundary repairs to bulk mismatches. (A) excludes boundary-bridging mismatches. (B) excludes any component carrying a nontrivial logical class. (C) bounds the two physical repair weights by total t. Consequently

 Rep(f) has no logical residual and |Rep(f)|<=t

for every effective Pauli label covered by F and every allowed actual record. The condition is hereditary: removing input faults cannot create one of its occupied-support witnesses. It therefore controls the complete linear span of good defect basis vectors, not merely one chosen classical trajectory.

Define the terminal tests on the COVERING support itself: at most t_B occupied boundary sites and at most floor(u/kappa) occupied sites in the O(n)-sized adjacent-check-record neighborhood. Here b extracts those records as baseline bits, and kappa is its bounded maximum multiplicity (kappa<=2, allowing the shared X-check layer at T=1). These hereditary tests imply |a|∂|<=t_B and |b(f)|<=u for every covered defect label. No global bulk-count requirement is imposed.

## 5. Positive rarity, not a signed fault union
Take the actual positive distribution obtained by jointly measuring the commuting toggling-frame input-defect projectors. Assume the root subset-moment lemma supplies its parameter q. Ordinary union bounds are legitimate for THIS positive distribution.

For fixed adjacency degree, constants A,c depend only on ell. The excluded connected witnesses give bounds of the forms

 A nT (A sqrt(Q))^T /(1-A sqrt(Q)),
 A nT (A Q^(1/4))^d /(1-A Q^(1/4)),
 2 binom(2n,a) (A sqrt(Q))^a /(1-A Q^(1/4)).

The O(n)-neighborhood exclusions add binomial tails such as binom(Cn,ceil(u/kappa))Q^ceil(u/kappa) and binom(2n,t_B)Q^t_B, with harmless integer-threshold adjustments. Constants are deliberately nonoptimized. These are support-witness counts; they do not multiply by exp(eta nT).

For d=Omega(n), T=Theta(n), and t,t_B,u fixed sufficiently small positive fractions of n, all terms are exp(-Omega(n)) at sufficiently small fixed q. Space O(nT)=O(n^2). Taking n=Theta(log(L/epsilon)) yields polynomial-logarithmic source space. This statement is conditional on the actual q moment estimate and the deterministic witness derivation, not on a stochastic noise assumption imposed on the bath.

## 6. Gentle lift with full retained bath
Let Pi_good be the diagonal projector onto the hereditary good input-defect basis vectors, and let rho_tilde be the actual toggling-frame source state, including bath/reference. If tr[(I-Pi_good)rho_tilde]<=delta, gentle projection gives

 ||rho_tilde - Pi_good rho_tilde Pi_good||_1 <= 2 sqrt(delta).

Apply the SAME ideal U to both terms, optionally followed by any genuine pointer dephasing/discard. Contractivity preserves this bound. No ideal final measurement is assumed: retain pointer coherences and the measured graph as gauge. The projected output, in every pointer computational component m, lies in the COMMON span

 span{ E_B Rep(f)|Bell_L> : |E_B|<=t_B, |Rep(f)|<=t }

after the same frame P(m)^dagger (or their single pointer-controlled direct sum when pointer coherences are retained). It thus lies in physical Pauli radius t+t_B of the fixed encoded Bell target; the bath retains arbitrary coherent coefficients. No branch-count loss, independent noise assumption, or signed Boolean union is used. A uniform moment estimate for arbitrary bath/reference gives the corresponding complete source-map bound.

## 7. Actual fixed-baseline discrepancy
Let b(m) be the measured adjacent-check baseline used by the receiver, and D(m)=b(m)+sigma(P(m)). The local boundary stabilizer identities yield

 D(m)=sigma(Rep(f))+b(f),

because the separate E_B syndrome cancels from the actual-source versus corrected-source comparison. Hence on every nonzero good branch

 |D(m)| <= nu*t + u,

where nu is base check incidence. This is the same D for ALL coherent components with that actual m. Therefore the good output is supported only on records with sparse fixed target discrepancy, even though their absolute frame P(m) may be extensive. This is the source condition needed by a native fixed-wrong-baseline receiver.

## 8. Exact remaining seams
The source circuit is scheduled and assumes fresh product inputs; actual autonomous preparation/termination, reliable capture and retention of random records, and the full native receiver remain separate. This note does not replace any of them with trusted ARM/DONE. The analyzed classical frame can be expensive to compute; output storage must cover its real runtime. The final known-|0> conversion from a Bell target requires its actual readout/feedforward interface, not an ideal logical decoder.

Primary source for the ATG and decoder conventions: Bergamaschi–Liu, arXiv:2411.04405v1, sections3–5, https://arxiv.org/html/2411.04405v1 . The new receiving argument is the product-defect dictionary, positive-subspace lift and actual-record fixed-baseline interface above.
