# One-call coherent filtering: exact instrument, and a cheaper conventional realization
2026-10-29. New local derivation and numerical checks; established coherent-check mechanism, not a new generic quantum capability. Independent review pending.

## Decision
The proposed random m-branch filter is mathematically valid under the stated representation and isolated-control contracts. But for a completed k-qubit logical channel, **b=log2(m) ordinary random coherent Pauli checks plus one Pauli pad implement exactly the same accepted joint CP map with O(bk), rather than O(mk), controlled operations**. This defeats a generic advantage claim for the multiplexor. The useful retained result is a precisely scoped one-call, retained-memory erasure interface and the obligation to acquire reliable coherent flags. Clifford authentication is a second strong comparator, not an overlooked alternative.

## 1. Exact multibranch instrument
Let N have Kraus K_a:L⊗M→L⊗M', with arbitrary retained memory dimensions and arbitrary input/reference correlations. The opaque source acts on L,M only. A fresh b-qubit protected flag F is initialized to |u>=m^(-1/2)Σ_j|j>, m=2^b. Independently draw g_1,...,g_m from a unitary conjugation 1-design on L. No branch key or flag information is leaked through a side port, timing, or retained control record. The source may infer information from L itself; that is included in the same fixed conditional joint N.

Apply V=Σ_j |j><j|⊗U_gj before the one ordinary call and V† after it, then project F onto |u>. This needs no controlled N, environment access, inverse N, or source reset. Accepted Kraus:

A_a(g_1,...,g_m) = (1/m)Σ_j (U_gj†⊗I_M') K_a (U_gj⊗I_M).

Define K_ag by the summand, Kbar_a=E_g K_ag, T=E_g Σ_a K_ag(·)K_ag†, and G=Σ_a Kbar_a(·)Kbar_a†. Then B=T−G is CP: its Kraus covariance expression is E_g Σ_a(K_ag−Kbar_a)(·)(K_ag−Kbar_a)†. Expanding all m² terms and using independent keys gives EXACTLY

A_acc = G + B/m.                                          (1)

The equality is of complete CP maps, not just reduced states, therefore extends to all references and entangled LM inputs. Independence of branch keys, their freshness relative to the full prior apparatus, and retirement after the attempt are load-bearing. Using a single repeated key gives T, not (1). Conditional on a revealed key list the decomposition (1) need not hold. Branchwise different source maps also invalidate it.

For an irreducible logical representation, Schur's lemma gives Kbar_a=I_L⊗B_a0, where B_a0=Tr_L K_a/d. Thus G=id_L⊗B_0, with B_0(σ)=Σ_aB_a0 σ B_a0†. The covariance B is a positive bad map. In the Pauli case write K_a=Σ_r P_r⊗B_ar, with Hermitian orthogonal k-qubit Paulis and B_ar=Tr_L[(P_r⊗I)K_a]/d. Then

T=Σ_r Ad_Pr⊗B_r,  B_r(σ)=Σ_aB_ar σ B_ar†,
G=id⊗B_0, B=Σ_(r≠0)Ad_Pr⊗B_r.

Trace preservation implies Σ_r B_r is TP. In particular p=Tr[B_bad(ρ_M)]∈[0,1], where B_bad=Σ_(r≠0)B_r. The accepted probability is 1−p+p/m even for correlated LM inputs, because each Pauli is unitary. Its actual accepted memory marginal is (B_0+B_bad/m)(ρ_M); it is independent of new logical data. Accepted nonidentity mass is p/m, normalized mass p/[m(1−p)+p]. These are exact averaged-key statements. Comparing with id_L⊗(B_0+B_bad/m) gives unnormalized half-diamond error ≤||Σ_(r≠0)B_r†(I)||/m. A normalized conditional error additionally requires a lower acceptance bound. We do not replace the source memory by an uncorrelated state.

For other irreducible representations, partial output trace of each covariant G,B factors through Tr_L by Schur. The same probability/memory-effect statements follow with the appropriate B_bad. A fixed proper subcode can be used as input only if the physical output representation and subsequent decoder are explicitly retained; one must not relabel the full-sector scalar component as the subcode's own entanglement-fidelity scalar.

## 2. Raw physical code and leakage: representation phases matter
For an input irrep P within a larger physical output H, average U_H(g)† K_a U_P(g). A GOOD identity embedding follows if the input irrep occurs exactly once in H: Schur intertwiners then give Kbar_a=V_P⊗B_a0. All inequivalent leakage sectors average to zero. This applies to the properly specified physical-permutation singlet representation. Multiplicity greater than one allows additional equivalent output copies and invalidates the claimed unique GOOD form unless handled separately.

A mere projective Pauli list on the code, extended as identity on leakage, need not suffice. Concrete counterexample: physical dimension3, code {|0>,|1>}, source replaces every state by |2>. Choose U_g=diag(g,1) for g=I,X,Y,Z. E_g g=(I+X+Y+Z)/4≠0. For m=2 and maximally mixed code input, the actual accepted probability is5/8, all leakage, whereas the false GOOD=0 formula predicts1/2. The full-Choi difference is3/16. Using the honest Q8 group {±I,±iX,±iY,±iZ} on code and its trivial representation on leakage has zero leakage intertwiner and restores1/2. Relative phases outside the code are physical controls, not ignorable global phases.

Using a **completed TP logical decoder** before the inverse logical controls avoids this raw representation issue. It changes which scalar GOOD component is being filtered; raw and completed quantities must not be mixed. The ordinary logical interface is N'=D N E, with E after all initial logical controls and D before all final logical controls. No encoded physical Pauli compiler is needed. Decoder trash must be retired if claiming the same retained-memory marginal boundary.

## 3. Cheaper exact realization: known coherent Pauli checks
Independently choose b uniform k-qubit Paulis Q_i, INCLUDING identity, with replacement; also choose an independent uniform Pauli pad R. Prepare b plus flags. Apply R, then b singly-flag-controlled Q_i gates before N'; after N', undo the controlled gates in reverse order and undo R. Measure all flags in X and accept all plus. The ordering really is an inverse; Q_i need not commute. Each accepted Kraus undergoes commuting adjoint projections

Π_Q(K)=(K+QKQ)/2.

For a Pauli component P_r, Π_Q(P_r)=P_r if Q commutes with P_r, otherwise0. Each nonidentity r commutes with a uniform Q with probability1/2, independently for b checks; identity always survives. The independent pad R kills every distinct-Pauli cross term without changing these survival events. Thus after averaging keys the complete accepted instrument is

id⊗B_0 + 2^(-b) Σ_(r≠0) Ad_Pr⊗B_r,

EXACTLY (1), including rectangular retained memory and arbitrary reference correlations. This proof does not assume a stochastic physical source; stochasticization is produced by the fresh pad. Without the pad coherent cross terms can survive. Choosing checks without replacement or excluding identity changes the exact coefficient and must not be silently substituted.

Conservative all-to-all primitive resources: one opaque N', b protected flag qubits held through it, ≤2bk CNOT-equivalent controlled Pauli gates, ≤4bk basis-change singles, 2b H for flag preparation/readout, and ≤2k pad singles; 2k(b+1) fresh classical bits. Native controlled Y is S-CNOT-S† and controlled Z is H-CNOT-H. Measurements, reset, routing, holding, E/D and all finite-window control errors are additional. This is a circuit construction, not a hardware execution. Increasing b adds gate/flag faults, so ideal suppression is not a physical threshold theorem.

The iid branch circuit instead uses 2m classically programmed multiplexor branches. A simple equality-controlled implementation with b−1 temporary clean work bits costs at most 2mk+24m(b−1) CNOTs (b≥1), plus singles and 2b H; temporary work is uncomputed before the call. This loose upper bound uses 2(b−1) Toffolis per branch per window and6CNOT per Toffoli. It requires2km key bits, versus2k(b+1) for checks. Better multiplexor compilation is possible, but cannot establish an advantage over an already available exact O(bk) realization. No native netlist for the multiplexor is claimed executed here.

## 4. Independent strong comparator: random Clifford tags
Use b protected tag qubits initially |0^b>, apply a uniform Clifford C on k+b bare logical qubits, send only the k payload slots through N'=DNE while tags remain isolated, apply C† and accept tag0. This preserves a noiseless inner code because E follows the first logical Clifford and D precedes the second. It does not require a source acting on the tags.

Let d=2^k, m=2^b, D=dm. By the Pauli/Clifford twirl, each nonzero source Pauli coefficient B_r is uniformly spread over the D²−1 nonidentity Paulis on payload+tags; distinct coefficients vanish after key averaging even with retained memory. Accepted tag Paulis are exactly the m strings of I/Z. Of these, m−1 pair with identity payload and m(d²−1) pair with nonidentity payload. Therefore

A_auth = id⊗[B_0 + (m−1)/(d²m²−1) B_bad]
       + [m/(d²m²−1)] Σ_(s≠0) Ad_Ps⊗B_bad.       (2)

Here B_bad is a memory CP map, not a number. Its accepted bad mass is p*m(d²−1)/(d²m²−1)<p/m. Total acceptance is1−p+p(d²m−1)/(d²m²−1), slightly below1−p+p/m, while some accepted errors are harmless identity-payload updates. At fixed p the conditional nonidentity fraction is lower too. This is not strict domination of every cost/yield objective: it has a slightly different acceptance and redistributes the bad logical Pauli types. Standard polynomial Clifford sampling/compilation, O((k+b)²) elementary-gate upper bounds and comparable key size, are available; no implementation benchmark here. The O(bk) random-check realization is the closest exact comparator.

## 5. Capability boundaries and useful failures
- One expensive source call can suffice for heralded suppression when the logical GOOD weight is already substantial, even if the full bath is unknown. This is an existing coherent-check capability, not a newly discovered universal recovery theorem.
- An ideal full depolarizer on d dimensions has GOOD weight1/d². Normalized bad mass after filtration is (d²−1)/(m+d²−1). Constant target fidelity needs m=Ω(d²), hence b≈2k protected flag qubits; those flags could hold/bypass the whole k-qubit payload. Near-perfect conditional fidelity needs still more. No escape from zero quantum capacity is established without counting the bypass.
- For rare collective bursts with p constant below1, b=O(log(1/ε)) can be much smaller than k. The known checks already exploit precisely this regime with one source use; the multibranch construction offers no generic new access.
- A failed attempt generally destroys an unknown input. Retrying the same unknown quantum state is not authorized by heralding. Prepared entanglement distribution can retry with all uses and correlated-memory updates charged; reliable arbitrary-stream communication needs erasure handling and a throughput argument.
- Complete flag dephasing removes branch interference. For the multibranch circuit it leaves accepted T/m, with no improvement in conditional noise. Identity-source availability falls to1/m. Flag isolation is a substantive quantum resource, not a classical-control assumption.
- Retiring keys is essential for the averaged positive-path assertion. Arbitrary later retained source memory is included; arbitrary access to a flag or key is not.

## 6. Evidence and primary attribution
`check_filter.py` executes8 random nonunital joint CPTP sources with input memory2 and output memory3, b1/2, comparing full Choi matrices for explicit enumeration of all random branch tuples, all padded check tuples, and G+B/m. Maximum discrepancy7.5e−16. One m4 circuit is assembled as actual full flag-controlled pre/source/post matrices, giving exactly the accepted-amplitude formula in floating arithmetic. The qutrit leakage counterexample and its honest-Q8 repair are executed. These are finite-dimensional floating consistency checks of analytical identities, not interval proofs, hardware results, or independent review. Clifford coefficients are analytically counted; no full Clifford circuit was simulated.

Astra first: current plugin N1041 capsule and its governing source were fetched at revision c64402f357e69975df195c4925cb882f5d4b8177, with current notice read. Complete governing original is preserved unchanged as `received_N1041_proof.md`, SHA c5dca84b0bd857dfee66c09f1f32124126b8090269f10db4839641127c177e24. `astra_current_receipt.json` records current capsule/source responses. The reused premise is full-memory known-control bracketing, not automatic dual-rail protection of arbitrary multi-flag gates or a physical noise allowance.

Primary sources actually consulted:
- Gisin, Linden, Massar, Popescu, *Error filtration and entanglement purification for quantum communication*, https://arxiv.org/pdf/quant-ph/0407021, Sections I–II. Error filtration by coherent paths and rejection is established. Their independent-channel/path implementation is not silently equated to our single completed source with controlled conjugations.
- van den Berg et al., *Single-shot error mitigation by coherent Pauli checks*, https://arxiv.org/pdf/2212.03937, Section2, especially random Pauli error detection probability1/2 and nested multiple checks. This is the directly relevant conventional mechanism. Our exact retained-memory CP calculation and fresh-pad bookkeeping specify the present source contract; no priority claim for checks is made.
- Aharonov, Ben-Or, Eban, Mahadev, *Interactive Proofs for Quantum Computations*, https://arxiv.org/pdf/1704.04487, Section3 Protocol3.1, Claim3.1, Lemmas3.5/3.6. These supply the Clifford authentication and correlated-reference twirl mechanism; equation(2) is the explicitly counted present protected-tag specialization.
- Barnum et al., *Authentication of Quantum Messages*, https://arxiv.org/pdf/quant-ph/0205128, Sections4–5. Earlier purity-testing/authentication foundations. No new quantum-authentication primitive is claimed.

The main scientific conclusion is a valid but already conventionally realizable mechanism, plus a concrete raw-leakage phase pitfall. It does not supersede finite acquisition, guard confidence, or outer-code results, and makes no historical novelty or matched practical advantage claim.
