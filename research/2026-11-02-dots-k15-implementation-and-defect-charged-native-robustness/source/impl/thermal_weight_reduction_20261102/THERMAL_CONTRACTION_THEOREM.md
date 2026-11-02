# Full-thermal local cone transfer theorem

Derived here, 2026-11-02. Not a theorem quoted from the weight-reduction literature. Chain convention: C2 --d2--> C1 --d1--> C0, qubits in degree 1, X generators columns of d2, Z generators rows of d1. All algebra is over F2. Hamiltonian violation energies are J_g(1-S_g)/2, not -J_g S_g.

## 1. Constructive local contraction

Suppose the enlarged complex A is a direct sum of local blocks A^x,A^q,A^z plus attachment differential δ, with block differential d0. Each block has at most M coordinates in total, and attachment edges follow the original Tanner incidence. Block homology is one-dimensional in degree 2,1,0 respectively and zero otherwise. Attachments strictly lower the stratum x→q→z (an x→z attachment is harmless). The induced adjacent homology maps are the actual original check matrices.

This is the **all-degree**, not merely H1, structural input supplied by Hsieh–Li–Lin v2 Sections 2.4, 4.1.2 and 5.2. The vanilla local-cone construction is sufficient here; distance-amplifying dummy faces may be used only with the same contractible-cone and tree-product certificates. A modified gadget with additional endpoint homology is NOT covered by the exact preimage formula below. The construction has new check weight ≤5 and qubit degree ≤6 (Theorem 4.6). Retain every original check coordinate, including redundant checks; this is not Gaussian elimination of the global check set.

Within each finite block choose a normal-form contraction (p,i,h) by finite-field elimination:

 pi=1, p d0=0, d0 i=0, d0 h+h d0=1+ip, h²=hi=ph=0.

These maps never leave their blocks. Since h preserves stratum and δ strictly lowers it, (hδ)^3=(δh)^3=0. Define

 I=(1+hδ+(hδ)²)i,
 P=p(1+δh+(δh)²),
 H=(1+hδ+(hδ)²)h.

The elementary finite homological perturbation identity gives

 PI=1, P D=d P, D I=I d,
 DH+HD=1+IP, PH=HI=H²=0,

where D=d0+δ and the effective d is pδi+pδhδi+pδhδhδi. The terms containing two or more δ vanish after p: they go from stratum x to z while lowering chain degree by only one, whereas the retained homology degrees differ by two. Thus d=pδi is exactly the source differential, with no hidden effective incidence.

Every matrix entry involves at most three neighboring blocks. Consequently support radius is bounded by two Tanner edges plus block diameter. Both row and column norms are bounded and computable from finite blocks. No elimination over a growing connected region occurs. The identities are exact in degrees 0,1,2, including source H0/H2 relations.

Here P maps fine→source and I maps source→fine; d is the source differential, not an identity matrix.

## 2. Exact decoder on every valid fine syndrome

For chain-sector error e'∈A1, s'=D1 e'∈A0, let the source decoder satisfy d1 R(s)=s for s∈im d1. Set

 R'(s')=I1 R(P0 s')+H0 s'.

The endpoint identity D1 H0=1+I0P0 proves D1R'(s')=s'. Further,

 P1[e'+R'(s')]=P1e'+R(P0s'),

and I,P induce inverse logical-class maps. A fine physical Pauli fault f' maps to the bounded-support source error P1 f'. Thus the logical jump of the new decoder is **exactly** the source decoder jump under this mapped fault, for every syndrome, at every energy.

For the other Pauli sector use the transposed contraction: projection Iᵀ, inclusion Pᵀ, homotopy Hᵀ. In particular its syndrome projection is I2ᵀ, not P2ᵀ. This distinction is essential when bounding adjoints or hooks. The same formulas preserve the canonical X/Z logical pairing: for closed fine chain a and fine cochain b, a·b=(P1a)·(I1ᵀb), because 1+IP=DH+HD and closedness kills both extra terms.

## 3. Entire finite-temperature syndrome law

Let S=im d1, S'=im D1. From the endpoint homotopy,

 **S'=P0^(-1)(S).**

One direction is the chain-map identity. Conversely if P0s'=d1e then s'=D1[H0s'+I1e]. This equivalence holds for all endpoint vectors, not just previously valid ones.

In a stabilizer Hamiltonian all allowed joint syndromes have identical Hilbert-space multiplicity; CSS X and Z relation spaces separate. At finite beta let the independent fine bit b_j have probability p_j=1/(1+exp(beta J_j)). Then the actual fine syndrome distribution is exactly

 law(s') = law(b | P0 b∈S).

Hence the exact old-syndrome marginal is

 Pr(P0s'=s) = 1_{s∈S} Pr(P0b=s) / Pr(P0b∈S).

This sums every auxiliary excitation. It is a parity convolution of independent defects, conditioned on source validity. Unless the columns of P0 have special structure, it is **not** the original source Gibbs distribution. Both Pauli sectors obey this statement, with their respective projections. The full quantum Gibbs state also contains the equal logical degeneracy, not an omitted excited gauge band.

## 4. Rigorous local-stochastic transfer (nonoptimal fallback)

For a positive stabilizer Hamiltonian, its allowed syndrome law is q-local-stochastic with q=exp(-beta J_min): Pr[T⊆supp s']≤q^|T|, including dependent checks (the imported source Walsh-positivity lemma).

Let P0 have row weight ≤r and column weight ≤c. For each requested nonzero old bit choose a contributing nonzero fine bit. There are ≤r^|T| choices; any such choice contains ≥|T|/c distinct fine bits. Thus

 Pr[T⊆supp(P0s')]≤[r q^(1/c)]^|T|.

The opposite sector uses row/column norms of I2ᵀ separately. If the source decoder works for every local-stochastic syndrome law of parameter q_* and every fixed bounded-local fault, a sufficient condition is

 beta J_min ≥ c[log r+log(1/q_*)].

This is full-temperature protection of the actual reduced Hamiltonian; it is not fixed-temperature Gibbs equivalence. Mapped physical faults and native-prefix faults must be admitted with their actual support bounds. A finite pinned source fault set costs only a fixed prefactor in the rooted contour estimate, but that prefactor must not be called unity.

## 5. Distance, filling, traces, and native transfer

Distance: d'_chain≥d_chain/||P1||col and d'_cochain≥d_cochain/||I1ᵀ||col. The stronger HLL distance theorem can alternatively be imported; it is not needed when w is fixed.

Actual-generator filling: for a fine stabilizer e', d1P1e'=0 and P1e'=d2b. Then

 e'=D2[H1e'+I2b].

Thus the source polynomial-radius fill transfers with the finite map-radius/norm overhead. Transpose for the other sector. This uses actual fine generators.

Full traces: prepend the linear P0 syndrome prepass and H0 correction, recording every nonzero input's complete bounded stencil, INCLUDING gates whose outputs cancel. Retain all nonzero operands of every linear identity row; zero outputs do not activate further empty computation. Connect collisions before decomposing into components. Compose with the source's input-seeded removable full traces. A restricted trace component with fine top τ', old top u=P0τ' and source correction r satisfies d1r=u, so

 D1(I1r+H0τ')=τ'.

Thus its fine top witness is a valid removable syndrome. One fine top bit seeds only a fixed number of prepass gates, and source top mass is at most c|τ'|. Whole-trace connected entropy remains exponential in |τ'|, but the exponent changes with the explicit prepass and source constants. Additivity across disjoint complete traces follows from the source decoder's additivity and linear pre/postpasses. Large expanded final lifts are used algebraically, not silently inserted into the entropy graph.

The root's full-spectrum native-clock and generic-perturbation theorem therefore applies to this **new** weight-5 code once its changed constants satisfy that theorem. Clock levels are ≤5; bare-data and dressed/native syndrome frames must remain distinct. All cone qubits/checks, clock sites, source dictionary norms, projection/homotopy hooks, contact degrees, filling/adjoint growth, and new entropy margins enter the new admission. No claim of unchanged permissible perturbation strength follows from chain equivalence. At fixed source weight and fixed admitted new constants, n_new=A(w)n and native size is a further constant multiple, so the inherited stretched-exponential exponent remains positive (indeed the same ancestry exponent can be used), with changed constants and prefactors.

## 6. Geometry and physical noise

Each finite block is anchored at its original check/qubit; attachments lie between old adjacent anchors. If the original 3D family has bounded density and interaction radius, the new family has the same spatial dimension, with density increased by the actual block overhead. One can instead dilate the layout by a fixed factor and place the finite gadget sites in distinct microcells, restoring a chosen minimum spacing while increasing physical interaction range/volume. This is a new bounded-overhead layout argument, NOT automatic reuse of the original source's unchanged-cell density constant. It does not require a fourth spatial dimension.

General bounded-range noise may touch several new gadget sites inside a physical ball. Its arity and number of affected cones must be counted at the new density (or after the charged dilation). Mapping a local fine error back to the source costs the actual P1/I1ᵀ column norm. Native clocks at most 5 levels do not eliminate that coarse decoder overhead. Ideal Gibbs resource, ideal overwrite, and ideal/conditional READ assumptions remain unchanged.
