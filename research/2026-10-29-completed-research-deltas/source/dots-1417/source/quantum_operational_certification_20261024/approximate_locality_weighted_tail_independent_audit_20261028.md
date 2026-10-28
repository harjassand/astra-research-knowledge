# Independent approximate-locality bridge: weighted tails, robust packing, and ideal-subset causal comparison

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

This is a new analytic audit, not an edit or extension by implication of an earlier receipt. The received exact-locality source `ordinary_colored_pooled_joint_recovery_20261028.md`, SHA-256 `d63c30417caee39cc16f8b80f44bb01ac25933c7cab647f33897a651bdd22c47`, remains immutable. The present task is to establish three structural bridges for a proposed approximate-locality construction. No new acquisition theorem, full statistical cap, hardware run, or source experiment is certified here.

## 1. Assumptions actually used

The exact global representation remains

\[
 \rho=U[(I_{2^q}/2^q)\otimes\bar G]U^\dagger,
 \qquad B_{j,i}=U(\sigma_{j,i}\otimes I)U^\dagger,
 \quad \operatorname{Tr}\bar G=1.
\]

Thus true generators are exact compatible logical Pauli factors and commute with rho, even though they need not be physically local. For each logical i, there EXIST two Hermitian unitary reflections V_Xi,V_Zi on one common unknown physical interval I_i of at most w qubits, with

\[
 \operatorname{Tr}\rho(B_{j,i}-V_{j,i})^2\le\tau^2.
\]

The V's need not obey either within-pair anticommutation or cross-pair commutation, and need not commute with rho. They are proof-only comparators, not supplied controls. Gauge rank and eigenvalues have no lower bound.

For the coarse X contrast, write X=B_X R, where R is positive, commutes with the exact true logical algebra, and

\[
 \kappa\rho\preceq R\preceq\rho,
 \qquad B_ZXB_Z=-X.
\]

The corresponding Z contrast has the analogous X/Z interchanged statement. R need not commute with rho. The exact operator-valued Pauli/gauge model gives these properties; the inequalities alone, without the polar-factor/anticommutation structure, would not suffice.

Throughout 0<kappa<=1 and 0<=tau<=kappa/8. Known output geometry, independent source resets, private mixed-ancilla preparation, restored physical routing and the other operational contracts remain necessary when these lemmas are used in a learner.

## 2. A floor-free trace-norm tail lemma

For any Hermitian D and X=BR with commuting reflection B and positive R,

\[
 \|DX\|_1=\|DR\|_1
 \le \|D\sqrt R\|_2\|\sqrt R\|_2
 =\sqrt{\operatorname{Tr}RD^2}\sqrt{\operatorname{Tr}R}.
\]

Since R<=rho and Tr R<=1, D=V-B_0 with weighted squared error at most tau^2 gives ||DX||_1<=tau. Also ||XD||_1=||DX||_1 by Hermitian conjugation. This is valid for noncommuting R,rho and requires no inverse or minimum eigenvalue.

### 2.1 Disjoint patches

If J is disjoint from I_i, local V_Z acts only on the subsystem traced out. Consequently

\[
 X^J=\operatorname{Tr}_{\bar J}(V_ZXV_Z),
 \quad -X^J=\operatorname{Tr}_{\bar J}(B_ZXB_Z).
\]

The Hermitian difference has trace-norm-contractive partial trace, so

\[
 2\|X^J\|_1
 \le\|V_ZXV_Z-B_ZXB_Z\|_1
 \le\|(V_Z-B_Z)XV_Z\|_1+\|B_ZX(V_Z-B_Z)\|_1
 \le2\tau.
\]

Thus **||X^J||_1<=tau**, not exact cancellation. No support assertion about B_Z was used.

### 2.2 The proxy's own patch

Because V_X is supported on I_i and has operator norm1,

\[
 \|X^{I_i}\|_1\ge|\operatorname{Tr}V_XX|
 \ge\operatorname{Tr}B_XX-\tau
 =\operatorname{Tr}R-\tau\ge\kappa-\tau.
\]

The same argument applies to any width-w interval containing a narrower proxy interval. In fact the real overlap identity yields the stronger lower bound Tr R−tau^2/2, but the proposed linear-tail bound suffices and is retained for consistency.

### 2.3 Received finite coarse errors still separate

The existing two-state Bures guarantee at m0=kappa^2/512 gives trace-norm error at most kappa/8 on each estimated contrast. A certified trace-norm numerical score error at most kappa/16 then gives

- score on a proxy-containing interval >=kappa−tau−kappa/8−kappa/16 >=11kappa/16;
- score on an interval disjoint from I_i <=tau+kappa/8+kappa/16 <=5kappa/16.

The first score strictly exceeding kappa/2 therefore overlaps the proxy interval on simultaneous estimation success. This does not claim the selected patch itself contains the proxy; expansion by w−1 on both sides does. The same coarse call counts apply if every individual bank is acquired with the received marginal-law and record restrictions. No unknown source tail is inferred from successful scores.

## 3. Robust local packing via an explicit virtual random-access ensemble

The exact-locality dimension-algebra packing argument is NOT applicable to approximate local proxies. The following independent replacement proves the conservative density bound required by the colored construction.

Suppose s different logical labels have their local X proxies supported on a common L-qubit physical region J. Consider a proof-only ensemble: choose independent uniform signs z=(z_1,...,z_s), prepare these s LOGICAL X eigenstates, all other logical inputs maximally mixed, append the fixed gauge state Gbar, and apply U. This defines normalized physical states Omega_z. It is not a proposed source query or supplied inverse. Their average is rho, and after averaging all bits except z_i the two states are

\[
 \Omega_{z_i}=\rho(I+z_iB_{X,i}).
\]

The actual binary projective measurement of the proof-only local reflection V_Xi, with effects (I±V_Xi)/2 on J, predicts z_i with average error

\[
 p_i=\tfrac12\sum_{z_i=\pm1}\operatorname{Tr}
     \rho(I+z_iB_{X,i})\frac{I-z_iV_{X,i}}2
 =\frac{\operatorname{Tr}\rho(B_{X,i}-V_{X,i})^2}{4}
 \le p:=\tau^2/4.
\]

The equality uses the exact logical product structure and [rho,B_Xi]=0, not [rho,V_Xi]=0. These s alternative measurements need not commute and are not performed simultaneously.

Let Q be the L-qubit register J of this cq ensemble. In base-two entropy units, Holevo information obeys I(z:Q)<=L. On the other hand, conditional-entropy subadditivity (strong subadditivity) and data processing to the i-th binary measurement give

\[
 H(z|Q)\le\sum_i H(z_i|Q)
 \le\sum_i H(z_i|\widehat z_i)
 \le\sum_i h_2(p_i)\le s h_2(p).
\]

Since the signs are independent uniform, H(z)=s. Hence

\[
 \boxed{\quad s[1-h_2(\tau^2/4)]\le L.\quad}
\]

This proof tolerates arbitrary correlated, noncommuting and rank-deficient gauge states. The ensemble is a mathematical dimension witness and adds no acquisition capability or reference.

For tau<=1/8, p<=1/256. Binary entropy is increasing on [0,1/2], and

\[
 h_2(1/256)\le\frac8{256}+\frac1{256\ln2}
 <\frac{10}{256}=\frac5{128}<\frac12,
\]

where −(1−p)ln(1−p)<=p and ln2>1/2 suffice. Thus the safe integer-independent statement **s<=2L** follows. The sharper factor is [1−h2(tau^2/4)]^−1, but is unnecessary.

If W=min(n,3w−2), this proves a safe color cap

\[
 C_{\max}=\min(q,2(2W-1)).
\]

All envelopes through one site lie in at most2W−1 physical sites, and contain the corresponding X proxies on the good coarse event. An optimal interval sweep coloring uses at most Cmax colors. The observable coloring guard must therefore use the robust cap, not silently retain the exact-locality value 2W−1. Passing the guard is still not a certificate of source membership or localization.

## 4. Repairing the causal proof when the true generators are nonlocal

### 4.1 Actual support graph only

The learned, synthesized reflections are exactly supported on their known envelopes W_i. The actual receiver is the same kind of three-controlled-reflection block for each i, with a distinct maximally mixed leaf ancilla A_i. Each NET macro has support W_i union {A_i}; routing is restored/tracked. The spatial graph uses ONLY these actual net support envelopes, with edges from lower to higher color on intersection.

For output i, let S_i=Anc(i). In the Heisenberg evolution of the actual Bell projector Phi_(R_i,A_i), remove actual blocks outside S_i. This is an exact operator identity for all input states. Arbitrary initial quantum gauge correlations do not enlarge a circuit's Heisenberg causal cone.

**Do not spatially remove nonlocal ideal elementary gates.** The old description of a common actual-and-ideal geometric cone is no longer justified.

### 4.2 An ideal index subset, not an ideal spatial cone

Instead form a proof-only ideal circuit consisting of exactly the complete block indices S_i, in the same restricted order, replacing learned generators by the true exact global B's. This ideal circuit need not have spatial support within the actual cone.

Each complete ideal block is precisely an abstract SWAP of logical factor j with A_j, conjugated by the common U on the physical register. Different complete ideal blocks commute because the exact global logical algebras commute and have distinct ancillas. Since i belongs to S_i, the ideal subset swaps the entire i-th logical qubit to A_i and gives Bell success1 for R_i,A_i, regardless of which other complete ideal blocks are included.

This conclusion is established algebraically; it is not inferred by deleting spatially disjoint ideal gates. The initial full purification keeps all logical Bell references, the gauge purifier and receiver-ancilla purifiers. The proof must not condition on individual mixture coins used to prepare maximally mixed registers.

### 4.3 Invariant prefixes and the unchanged weighted gate bound

Every ideal elementary gate acts only on the abstract logical factors and receiver ancillas, and as identity on the gauge. Thus it preserves

\[
 \rho_{PA}=U[(I_{2^q}/2^q)\otimes\bar G]U^\dagger\otimes I_A/2^q
\]

exactly. This holds for every arbitrary ideal index subset and each elementary prefix of that subset, whether or not the true B's are physically local. It is not an assertion about actual prefixes.

Let delta_jX,delta_jZ be the learned-to-TRUE weighted squared generator errors in rho. The squared purified elementary gate discrepancies remain delta_jZ/2, delta_jX/2, delta_jZ/2. Telescope the actual restricted circuit against this ideal subset, using ideal prefixes and unitary actual suffixes. Then

\[
 p_i\le3|S_i|\sum_{j\in S_i}
          (\delta_{jZ}+\delta_{jX}/2).
\]

These p_i are the marginal failures of the one actual full receiver because only its exact Heisenberg deletion was used. The ideal subsets used for different i need not be one common smaller physical circuit. The final Bell projectors commute, so their operator union bound applies to the actual joint receiver without independence assumptions.

### 4.4 Robust geometric bounds and joint loss

With Cmax actual envelope colors, the backward and forward graph spans have width at most

\[
 L_K=W+2(C_{\max}-1)(W-1).
\]

Each included label has its proxy supported within that span on the good coarse event. The robust packing lemma gives at most

\[
 K=\min(q,2L_K)
\]

ancestors per output and at most K output cones per block. Therefore

\[
 \ell_{0,\mathrm{joint}}
 \le3K^2\sum_j(\delta_{jZ}+\delta_{jX}/2).
\]

The global ideal-prefix hybrid remains available as well, giving coefficient3 min(q,K^2). At fixed w the robust K is independent of q. Any nonzero proxy tail must still enter the eventual learned-to-TRUE deltas and hence the final error floor; this audit does not erase that floor or certify a fine-estimation oracle bound.

## 5. Exact independent evidence

`approximate_locality_weighted_tail_independent_check_20261028.py` is a deterministic SymPy exact-rational check, with zero source calls and no RNG. It creates only its own JSON result.

1. A two-physical-qubit partial-SWAP fixture uses c=8320/8321, s=129/8321, tau=258/8321 and kappa=1/4. The logical/gauge rotation makes the true logical generators physically nonlocal. The gauge density is diag(99/100,1/100), while H=[[7/10,1/100],[1/100,1/200]] satisfies kappa sigma<=H<=sigma and does not commute with sigma. Consequently R and rho also do not commute. Both disjoint-patch contrasts are strictly nonzero, not an accidental exact cancellation. Exact squared trace norms verify the disjoint upper and true-patch lower bounds. The literal virtual-bit measurement verifies p_i=delta_i/4. Mixed-gauge ideal elementary prefixes preserve rho_PA exactly, with the required delta/2 errors.
2. A two-logical partial-SWAP encoding has nonlocal true generators and disjoint local actual swap blocks. Full actual marginal Pauli observables equal their one-block restricted observables exactly. Each corresponding one-block ideal subset has Bell fidelity1. The actual marginal loss is49923/276956164, restricted purified squared norm is49923/138478082, and the bound is149769/69239041. The joint Bell loss is49923/276956164 and obeys the marginal union bound.
3. The safe entropy and threshold constants are checked with exact rational arithmetic. The general entropy inequalities and geometric proof are analytic, not inferred from a finite simulation.

## 6. Verdict and limits

The requested weighted-tail coarse localization and ideal-index-subset causal comparison are valid under the exact global logical/gauge structure. The approximate proxies do not justify the old exact operator-algebra packing, but the explicit random-access entropy argument repairs this with safe density2. These three lemmas together preserve a q-independent geometric coefficient at fixed width while retaining nonlocal ideal generators and arbitrary gauge correlations.

No source sampling, source inverse, environment reconstruction, received-file mutation, free alignment, spectral floor or exact unknown control is used. Fine local ERM with a nonzero approximation floor, the complete revised source/precision ledger, and its final oracle statement must be separately established and audited in the forthcoming approximate-locality manuscript.
