# Separate general-q extension via an explicit weighted state 2-design

27 October 2026. Optional extension of the received qubit composition, not a revision of the frozen qubit proof. The construction below is derived here; no historical novelty is claimed. Polynomial dependence on q is dependence on logical Hilbert-space dimension, **not** on log₂q logical qubits.

## 1. A finite design in every dimension, without a MUB assumption

Let q≥2. Choose Q=4^a with q≤Q<4q, and distinct x₁,…,x_q in GF(Q). For each coefficient tuple A=(a₀,a₁,a₂,a₃)∈GF(Q)^4 let

    f_A(x)=a₀+a₁x+a₂x²+a₃x³.

Fix any surjective GF(2)-linear map π:GF(Q)→GF(2)^2 (for example the first two coordinates in a fixed binary field basis), and any bijection c:GF(2)^2→{0,1,2,3}. Put

    z_j(A)=i^{c(π(f_A(x_j)))},
    |v_A>=q^(-1/2) Σ_j z_j(A)|j>.

Uniform A makes every set of at most four distinct evaluations independent and uniform: its Vandermonde evaluation matrix has full row rank. The projection π preserves independence and makes every z_j uniform among the fourth roots. (Using the GF(Q)→GF(4) trace and a fixed phase bijection is an equivalent option.) There are Q^4≤256q^4 equally weighted phase labels. Field arithmetic and an explicit table of all labels have polynomial complexity in q; no design-existence oracle is being assumed.

Use the following weighted ensemble:

- each computational state |j> with weight 1/[q(q+1)], total weight 1/(q+1);
- each |v_A> with weight q/[(q+1)Q^4], total weight q/(q+1).

Let F swap two q-dimensional systems and Δ=Σ_j |jj><jj|. Fourth-root phases and four-wise independence imply

    E_A (|v_A><v_A|)^⊗2 = (I+F-Δ)/q².

Indeed E[z_a z_b conjugate(z_c z_d)] is one exactly when the multisets {a,b} and {c,d} agree, and zero otherwise; the all-equal case is counted once rather than twice. The computational moment is Δ/q. Hence the stated mixture has

    Σ_l w_l P_l^⊗2 = (I+F)/[q(q+1)],

an exact projective state 2-design. Duplicate phase vectors or identical projectors across different labels are harmless and are counted in the explicit bank cap. The design is not claimed cardinality-optimal.

## 2. Exact positive decoder objective and transfer

For any CPTP q→q channel Λ, the design identity gives

    Σ_l w_l Tr[P_l Λ(P_l)] = [q F_e(Λ)+1]/(q+1).

Thus, with b_q=(q+1)/q≤3/2 and rho_l=E(P_l),

    ell(D∘E)=b_q Σ_l w_l [1-Tr(P_l D(rho_l))].

Every loss effect b_q[I-D†P_l] is positive and bounded by b_q I. Replacing the six-label direct sum by weights sqrt(w_l) in the qubit proof gives

    E ell(Dhat∘E) ≤(1+gamma)ell_opt
                         +32 b_q m/gamma+4eta/gamma
                    ≤(1+gamma)ell_opt+48m/gamma+4eta/gamma,

provided each estimated output has expected root-infidelity at most m. A deterministic weighted delta bound gives the corresponding high-probability version. This uses a single optimized CPTP decoder, not independent phase witnesses, so the earlier (2+gamma) factor is unnecessary for this route.

## 3. Resource and implementation consequences

Let E:C^q→C^s have Choi rank≤R. Its common output support has dimension at most k=min(s,qR), and every pure-input output has rank at most r=min(R,k). Acquire n copies of each of the

    M=q+Q^4=O(q^4)

ordinary design inputs. On arrival of one independent datum, jointly reduce all Mn programme registers and that datum once, exactly as in the qubit theorem. All source-Choi output blocks are supported in the same k-dimensional space, so the arbitrary-operator reduction supplies a common frame with arbitrary reference systems intact. At each fixed frame the known optimum is unchanged.

Apply actual random purification separately to each bank, then use exact-Clifford tomography in the padded dimension

    kr≤D<2kr≤2qR².

The qubit proof's choices m≤gamma epsilon/192 and eta≤gamma epsilon/16 still work because b_q≤3/2. The expected-risk route has

    n=ceil[15360 D(log(2D)+1)/(gamma epsilon)],
    N=Mn=O(q^5 R² log(2qR)/(gamma epsilon)).

This is a deliberately loose polynomial-q cap. For failure beta, the union bound instead uses n≥80D log(2DM/beta)/m and eigensolver error a≤sqrt(m)/4. All finite-record confidence qualifications and shared-frame limitations from the qubit theorem remain necessary.

The direct empirical SDP is

    min Tr(H C), C≥0, Tr_output C=I_k,
    H=b_q Σ_l w_l tau_l^T⊗(I_q-P_l),

with C dimension qk. Its fixed strict point is I_k⊗I_q/q; Tr H=b_q(q-1) and ||H||≤b_q. Known finite-bit optimization, affine TP repair and Kraus synthesis remain polynomial in q,k and inverse target accuracy. In the repair, use -(Tr_output C-I_k)⊗I_q/q and charge its q-dependent positivity margin; no qubit-specific margin is silently reused. A Kraus rank at most qk gives a Stinespring output dimension at most q²k. Trusted input-state preparation, the M banks, all receiver gates and finite-randomness errors are counted.

The s=1 trace source is trivial with optimal F_e=1/q². No source inverse, source environment, physical Choi probe, coherent reversal, quantum-memory reuse, or practical generic-noise scalability follows. Both q and R can be exponential in their corresponding qubit counts. Existing frozen multilevel receipts are not changed by this separate direct-decoder extension.

## 4. Known-dimension corollary without a rank promise

If the output dimension k is already known and the learner acts directly there, no joint reduction is needed. Set r=k in actual purification, so D<2k². For qubit logical input, six banks suffice and the expected-risk acquisition cap is

    O(k² log(2k)/(gamma epsilon))

with polynomial gates. This improves the prior finite single-output weighted learner's k³ cap in this full-decoder regime, but does not exploit a small accepted-decoder trace budget and does not automatically upgrade any old adaptive-encoder, approximate-support, or validation receipt. Those compositions must explicitly recheck their input chronology, required confidence interface, rank-test gates, and total precision budgets.

In this **known physical output space** corollary, the classical learned CPTP decoder can be applied to future independent data: there is no latent-frame alignment to lose. Its per-record quality still uses the stated confidence interface, and finite calibration does not promise every record is good. This permitted reuse of a classical decoder in a known k-dimensional space does not provide reusable compression or a reusable frame for the main unknown-support/ambient-s theorem. The quantum calibration bank itself is measured and consumed.
