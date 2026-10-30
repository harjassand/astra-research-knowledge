# Independent hostile audit: local edge barrier and killed quantum basin

2026-10-29 UTC. Primary reviewed source SHA-256:

`65af28d7eff1fb48dd1fd3f1553b5c905b061d7b8cd7352621120cebe46fb18a`

Source: `FULL_ANIMAL_KILLED_BASIN_CANDIDATE.md`, copied as `FULL_ANIMAL_KILLED_BASIN_REVIEWED.md`. Exact dependency hashes are in `SOURCE_SHA256.txt`. Original sources were not edited.

## Scoped verdict

No defect found in Sections 4–5, with the full operator-support bookkeeping of Section 7, conditional on the stated confinement/container geometry and the separately audited weighted Loewner drift. These sections do supply a quantum boundary/compression/Duhamel closure rather than silently assuming a classical trajectory law. The closure works for ideal atomic SSF and bounded joint data/common-bath Hamiltonian and Lindblad operators; it does not require added depolarization or positive noise insertion records.

This review does NOT certify the separate weighted aggregate proof, imported FGL constants, a different check-only container construction, or an actual transactional controller. The source uses a mixed dummy/check animal graph. Its receipt must not be transferred without checking definitions to another graph variant.

Initialization precision: the exact scalar-map assertion E_killed,decoded=a_t id_L uses the standard encoded logical/reference input tensor a fixed bath state independent of logical input. This convention should be stated explicitly in the integrated theorem. Arbitrary pre-existing logical–bath correlation is not automatically a fixed logical input channel with that scalar factorization.

## 1. Large union forces a high SOURCE potential

Fix canonical minimum representatives E and F for source and target syndromes in one CSS sector. For a local Pauli support Z, a component K of E union Z union F contains every whole E-component it meets. Because check supports are cliques in G, no check can touch two such union components. The identity sigma(F)=sigma(E)+sigma(P_Z) therefore restricts componentwise.

Replacing F inside K by (E xor P_Z) inside K leaves its full syndrome unchanged. Global minimum weight of F implies |F∩K|≤|(E xor P_Z)∩K|. Thus |K|≤2(|E∩K|+s). This argument does not assume F is small or locally reached by a decoder.

Every source component in K is small and reduced. Its confined syndrome contributes at least h times its error weight; source components have disjoint syndrome supports, so these contributions cannot cancel against each other or an E-component outside K. These occupied raw source checks all belong to J(K). The dummy/check construction makes J(K) connected and gives |J(K)|≤D0|K|. Hence its single animal term has exponent at least L[(h/2-uD0)|K|-hs]. With u≤h/(4D0), |K|≥ell≥8s gives the displayed M_edge=exp(Lh ell/8).

Therefore a source in the component-safe basin with V<M_edge cannot have ANY union component of size at least ell under a declared local Pauli edge. In particular its target remains component-safe. This is correctly a source-edge barrier, not the false assertion that all globally large minimum representatives have large raw syndrome.

If every union component is smaller than code distance, E xor P_Z xor F is zero-syndrome separately on each component and supported below distance there, hence a stabilizer componentwise. This proves identity canonical logical action up to a syndrome-dependent scalar phase. No hidden minimum-representative continuity assumption is required.

## 2. Both CSS sectors and general local operators

Apply the preceding argument separately to X and Z sector representatives with the corresponding syndrome checks and a common worst-case cutoff below full code distance. A zero-syndrome pure-X (respectively pure-Z) Pauli is a full-code normalizer element; below distance it is a stabilizer. Combining the two canonical sector recoveries changes only scalar commutation phases, not logical action.

With V=V_X+V_Z and the safe condition on both representatives, V<M_edge/2 forces each sector below M_edge. Every local data Pauli therefore has identity canonical logical action between retained source/target sectors. Expanding an arbitrary bounded joint data/bath operator in its finite local data-Pauli basis extends this statement to all its syndrome matrix blocks, with bath coefficients retained. Consequently PHP, PKP, and PK†KP each act as I_logical tensor an ancillary operator on the killed space. Including losses is essential; checking jumps alone would not suffice.

The support bound s must include actual full nominal read-projector/correction Kraus supports, local noise supports, and K†K supports, not merely correction masks. K†K stays on the same data patch even with a common bath. Declared patches must be included in the fixed interaction graph and have bounded incidence. The reviewed Section 7 states these requirements. The number k_max of syndrome bits changed on any such patch is then a fixed constant.

## 3. Compression is CP and substochastic

On P Hilbert space, with Q=I-P, the compressed generator has Hamiltonian PHP, gains PKP rho PK†P, and complete losses PK†KP. Algebraically

PK†KP=(PKP)†(PKP)+PK†QKP,

where the final term is positive. It is a Lindblad generator plus positive killing, so its propagator is CP and trace nonincreasing. Compression is an analytical process, not a claim that the physical system is measured or forcibly projected.

Because P commutes with the positive syndrome observable V, the exact adjoint relation on P is

(L^P)^*(PVP)=P L^*(V)P - sum_K PK† QVQ KP.

The second term is positive; Hamiltonian and anticommutator compression introduce no omitted positive drift. Thus the accepted full-generator Loewner drift on the safe basin transfers to the killed process. Since W≥V, trace mass is at most one, and initial vacuum V is O(N), Gronwall gives the uniform O(N) potential expectation. The factor two from summing CSS sector constants can be absorbed in b,C_V.

Bath-only dynamics commutes with P,V and is retained, not charged to an extensive global bath norm. Joint dynamics must be well-defined; the data-acting joint operators have the stated bounded norms.

## 4. One boundary projector suffices, including anticommutator exits

An edge leaving P from an eligible source cannot leave by generating a large target representative: that would contradict the source-edge barrier. It must have target V≥M. A local Pauli changes each animal weight, and hence total V, by at most theta^(-k_max). Therefore every such source has V≥theta^(k_max)M.

Define B as the union of all eligible source syndrome blocks for QHP, QKP, and QK†KP, over the declared local operator supports. This union is still contained in the SAME high-V spectral region; no extra number-of-terms factor is needed in B≤V/(theta^k_max M). In particular boundary mass in the killed state is O(N/M). The anticommutator source blocks cannot be omitted even if K itself has no exit on a given source. Time-dependent coefficients can use a fixed B formed from all allowed local Pauli edges.

## 5. Completely bounded full-versus-killed comparison

For positive subnormalized rho supported in P, including any external reference, let p=Tr(B rho). Source localization gives ||B rho||_1≤sqrt(p Tr rho)≤sqrt(p).

A local Hamiltonian's difference between full action and embedded compressed action consists of QHP rho and its adjoint; its trace norm is at most 2||h||sqrt(p).

For a jump K, the outgoing gain has QQ trace at most ||K||²p. The two gain cross blocks have total norm at most 2||K||²sqrt(p), by positive-block Cauchy–Schwarz. The two anticommutator cross blocks together cost at most ||K||²sqrt(p), using the separately included QK†KP source blocks. Thus the dissipator difference is bounded conservatively by 4||K||²sqrt(p) for p≤1.

These are joint system/bath/reference inequalities, not estimates on normalized conditional states. Summing gives a bound by Gamma_N sqrt(p), with Gamma_N=2sum||h||+4sum||K||²≤C N. Clean atomic instruments have fixed bounded local Kraus counts/rates, and bounded-incidence noise contributes the same extensive order. A uniform upper rate/norm budget is required as well as any progress lower bound.

Variation of constants uses the full CPTP propagator, which is trace-norm contractive on Hermitian operators including references. Integrating the uniform killed boundary estimate gives C N t sqrt(N/M). The positive-input/reference estimate supplies the corresponding completely bounded channel-difference bound (or the equivalent flagged CP completion argument, with harmless constant adjustment). No conditioned outside record or global bath norm appears.

## 6. Logical output and exponent

In the canonical syndrome gauge, P is logical identity tensor a syndrome projector and every compressed local operator is logical identity tensor an ancillary operator. With a fixed logical-independent initial bath, the killed encoded-to-decoded map is exactly a_t id_L, with 0≤a_t≤1. The full channel is trace preserving, so its diamond distance to the killed map bounds 1-a_t. Applying the fixed decoder and adding this missing scalar mass costs at most a second copy of the comparison error.

For M=exp(Lh ell/8)/2, the displayed result C N^(3/2)t exp(-Lh ell/16), capped by two, follows. This is a conditional ideal-atomic continuous-noise memory bound with a common retained bath, not merely a statement about rare classical noise histories. No noisy-controller corollary follows from this instantaneous drift argument.

The encoded vacuum must belong to P. Since V(vacuum)=O(N), this requires sufficiently large N and an ell scaling making M dominate N; the stated ell proportional to sqrt(N) does so. The source's N≥N0/ell≥8s qualifications are substantive.

## 7. Terminal noiseless SSF readout

Conditional on the separately checked per-move decrease and componentwise active-hub progress, Section 7's readout substitution is consistent: accepted moves keep V below M, the edge barrier keeps representatives component-safe, and integer syndrome weight strictly decreases. A nonzero syndrome cannot be a terminal no-move state in that basin. Each step has trivial canonical logical action, so fixed ideal SSF decoding is correct on the entire killed subspace, including its coherent syndrome/bath states. This does not certify noisy physical readout during continued operation.

## Fresh regression and unresolved scope

`check_compression.py` independently verifies exact compression, positive exit loss, the adjoint drift-deletion identity, and CP/TNI of a finite compressed propagator for random bounded matrices. PASS: compression residual 3.46e-17, drift residual 3.13e-16, positive killed Choi and loss-effect eigenvalues. This is an algebra regression, not proof of weighted SSF drift or a threshold simulation.

No blocker or failed test was concealed. Weighted progress, its graph/container hypotheses, and the imported confinement constants retain their separate audit. No acceptance is transferred to the physical transactional compiler or generic unspecified initial logical–bath preparations.
