# Actual RX/RZ binding to a zero-background trace-polymer sampler

2026-11-01. **Candidate binding proof for independent audit.** This addresses commuting, known-coupling H0 only. It does not claim passive single-site thermal mixing, a noisy loader, or preparation for generic noncommuting perturbations.

## Claimed constructive consequence, conditional only on the abstract trace lemma

The actual recursive decoder can be compiled into a uniform bounded-local-stencil, zero-preserving circuit which accepts exactly the valid syndrome space and whose marked execution size is at most A|sigma| for a constant A independent of system level. Its typed host has O(n) objects and bounded degree for fixed ell. Hence the root's full-stencil splitting/bijection lemma supplies an exact positive polymer gas with original activity exp(−beta E(sigma_gamma)). At sufficiently low fixed temperature, standard algorithmic polymer sampling gives a polynomial-time approximate classical syndrome sampler. The original couplings are never replaced by guessed renormalized couplings.

The ideal quantum preparation consequence is conditional on a supplied encoded input and applying the chosen decoder's Pauli representatives. Physical routing, ancilla/reset costs and noise are separate obligations below.

## 1. Fix the decoder; do not silently change its logical frame

The paper specifies admissible local corrections, not a unique choice among them. Before defining either the memory observables or this loader, fix deterministic choices satisfying ALL source conditions, including the outgoing-weight inequalities and zero-input correction0. A lexicographically first admissible correction is one possible constructive convention; it is not a replacement for a previously frozen different decoder. If a decoder has already been fixed, compile its SAME local choices and use its SAME terminal level-2 representative. Source counting arguments use zero-preserving local corrections; this normalization must be checked explicitly.

Each local gadget contains O(ell^2) cells with bounded parent incidence. Since ell is fixed, the admissible choice can be precomputed by a charged finite search, or implemented by the source's explicit local paths/pairings. The finite search may be astronomically costly in ell; it is not a claim of practical efficiency or polynomial dependence on ell as an input parameter.

## 2. An exact local validity recognizer and reconstruction certificate

Work first with X-error syndromes sigma∈C2, i.e. violations of Z checks. Use the exact actual matrices and restriction maps; retain all redundant check coordinates. An arbitrary bitstring, including an invalid one, is processed as follows.

### RX step

(a) For each X gadget, test sigma_x∈im(delta_x1). This is a fixed-size local linear-algebra test. If it fails, raise a local reject flag. Otherwise select the fixed admissible f_x satisfying

    delta_x1 f_x=sigma_x,
    Σ_{q~x}|g_xq1 f_x|≤|sigma_x|.

Choose f_x=0 at input0. Compute sigma1=sigma+delta1_fine Σ_x f_x through bounded-incidence XOR gates. For globally valid input, source Lemma4.8/Corollary4.9 guarantees the test and |sigma1|≤|sigma|; sigma1 has zero X sector.

(b) For each Q gadget, test sigma1_q∈im(delta_q1). If it fails, reject locally. Otherwise select the fixed admissible f_q with delta_q1 f_q=sigma1_q and the source's outgoing endpoint-weight bound. Choose f_q=0 at0. Compute sigma2=sigma1+delta1_fine Σ_q f_q. For globally valid input, source §4.3.2 uses H1(Y_x)=0 to ensure the local Q input is valid; Lemma4.12/Corollary4.13 supplies the correction and |sigma2|≤|sigma1|. The result has only its Z sector.

(c) Check locally that each pair of Z-sector endpoint-copy bits agrees. Reject unequal pairs. On equal pairs set the parent bit to their common value. Then sigma2=F_RX2 sigma_parent. For valid input,

    |sigma_parent|=|sigma2|/2≤|sigma|/2.

(d) Independently verify every coordinate of the ONE-STEP reconstruction identity by local XOR gates:

    sigma = delta1_fine(f_X+f_Q)+F_RX2 sigma_parent.

Every coordinate uses a bounded stencil. A nonzero residual raises a reject flag. These checks are deliberately retained even when mathematically redundant with(a)–(c); no untested metacheck can pass through the implementation.

### RZ step

Here C2 is the direct sum of local C_z2=(cellular0-chains of connected Y_z). In each block take its parity as the parent syndrome bit, select the fixed local string correction f_z moving that syndrome to the source's designated anchor, and set f_z=0 on0. Every local0-chain is its parity anchor plus a local boundary; no local image obstruction is omitted. The parity rule and connectedness give

    sigma=delta1_fine f+F_RZ2 sigma_parent,
    |sigma_parent|≤|sigma|.

Explicit coordinate-wise reconstruction-identity reject flags are again included. All are bounded-stencil and zero-preserving.

### Actual terminal level-2 block, not an unmodified five-qubit seed

The memory decoder used in §5 is MODIFIED in §5.1.1: it stops at level2 and applies a fixed decoder for the entire O(ell^4)-qubit block C_(2), sets sigma1=sigma0=0, and does not continue the earlier recursion to the five-qubit seed. Preserve this SAME terminal decoder, including its stated radius-2 syndrome correction guarantee and tie-breaking choices. Treat the entire terminal membership test, selected f2, and identity delta2 f2=sigma2 as one finite macro-gate. Its O(ell^4) size and potentially exponential lookup preprocessing are charged to the fixed constants, not hidden as a five-qubit lookup. Mark its complete stencil whenever touched. Zero input maps to correction0 and reject0.

For an invalid terminal syndrome, raise a flag; for a valid one, use the matched fixed terminal correction. Membership is an explicit finite-block image test or precomputed table. This is constant in family level, not efficient as a function of ell. The finitely many system levels below2 can be handled separately. The dual sector uses the same convention with X and Z exchanged.

### Why acceptance is equivalent to global validity

If sigma is globally valid, the source's local cleaning and coarse-syndrome theorems show that every local test succeeds, the parent is globally valid, and the fixed level-2 terminal test succeeds. All reconstruction checks vanish.

Conversely, if all flags vanish and the terminal block accepts, repeatedly substitute the checked identities sigma_i=delta_i f_i+F_{i−1}2 sigma_{i−1}. The actual chain-map identity delta_i F_{i−1}1=F_{i−1}2 delta_{i−1} telescopes to an explicit physical correction

    f=f_top+F_top−1^1 f_top−1+...+F_top−1^1...F_2^1 f2,
    delta_top f=sigma_top.

Thus sigma belongs to the global image. This direction uses only the verified identities and terminal membership, not an assumed absence of hidden metachecks. No global exponentially large constraint oracle or global Gaussian elimination is required.

## 3. Typed bounded-degree circuit and active-size bound

Use wire objects for actual syndrome bits at each intermediate stage, correction bits, coarse-output bits and reject flags; use gate objects for the local lookup/solve maps, bounded-incidence XOR updates, diagonal/parity tests, identity verifiers and the fixed level-2 terminal gate. Complete incidence stencils are recorded, including zero-valued outputs and zero-valued input slots of an active gate. Mark every gate with nonzero input even if all outputs cancel to zero. Mark nonzero top input bits. This is the stronger circuit trace, not the paper's sparse marked-history convention.

Local bound: for fixed ell, each local solve has at most B(ell,z_v,z_e) input/output bits. Each bit influences only a bounded number of neighboring gadget solves/updates; the actual restriction maps, delta maps and F2 maps have bounded support. Fan-in, fan-out, alphabet, stencil size and typed host degree are constants independent of recursion depth. A multi-bit local solve may be treated as one constant-alphabet/constant-size gate, or expanded into finitely many zero-preserving gates. The direct bounded table is sufficient and avoids asserting an arbitrary Boolean compilation preserves the active-size estimate.

Global bound: RX has initial, first-cleaned and second-cleaned syndrome weights each at most |sigma_i|. RZ has at most a constant number of nonincreasing intermediate syndrome copies. Choose a uniform charge of3|sigma_i| for these phase inputs, increasing the fixed stencil charge if auxiliary copies are used. The source's alternating syndrome contraction gives

    Σ_i |sigma_i|≤4|sigma_top|.

Every active local solve is charged to a nonzero input bit in its block. An active update/identity-verifier gate is charged to a nonzero stage input bit or to a correction bit emitted by such an active solve. Each solve emits at most B bits; each such bit has bounded fanout. Thus if S is a sufficiently large fixed complete-stencil charge per nonzero phase bit,

    |trace(sigma)|≤12S|sigma_top|=:A|sigma_top|.

The fixed level-2 terminal stencil is included in S, charged whenever its input is nonzero. All-zero input has empty trace. Intermediate reject flags vanish on accepted inputs. Their gates are still marked if they examine nonzero input, and are charged by the same bound.

No unbounded time or wire lifetime is encoded by copying a bit through all remaining layers. Only actual one-step dependency wires are included; repeated copies within a gadget are absorbed in S.

## 4. Universe size and constructibility

Every check is nonempty and total Tanner degree is bounded, so each level has O(n_i) check/bit/gate objects. In RX,

    n_{i+1}≥Σ_q |Y_q(0)|≥(ell+1)n_i≥4n_i;

RZ obeys the dual count. Hence Σ_i n_i≤(4/3)n_top, and the typed circuit host has N=O(n_top) objects with fixed-ell constants. The fixed bottom block, incidence lists, local tables and typed stencils can be generated recursively in polynomial time in n, with all fixed-ell preprocessing explicitly charged.

Candidate trace membership can be checked in time polynomial in trace size: verify local gate equations, all zero reject flags, inclusion of each active gate's complete input/output stencil, and complete fanout of every nonzero wire; check that top labels and replay values are consistent, and that every outside-boundary input/output is zero. Unlisted gates have zero input and therefore zero output. This provides local validation without replaying the entire system or querying the global syndrome image. A full replay remains a useful polynomial-time verification fallback, but is not needed to invoke a sampler requiring local membership tests.

## 5. Original coupling activities and CSS factorization

For H0=Σ_a J_a(I−S_a)/2 with known efficiently computable 0<J_min≤J_a≤J_max, an admissible syndrome has energy E(sigma)=Σ_aJ_a sigma_a. If the full-stencil lemma gives components gamma, their top syndrome supports are disjoint and

    E(sigma)=Σ_gamma E(sigma_gamma),
    w(gamma)=exp(−beta E(sigma_gamma))≤exp(−beta J_min |gamma|/A).

There is no entropy or multiplicity factor from summing error representatives: every valid stabilizer syndrome has the same logical-sector Hilbert-space dimension. For CSS, X- and Z-type syndrome constraints factor, as do the commuting energies. Sample the two actual syndrome sectors independently and combine them using the fixed correction-order convention.

A bounded-degree finite-label host gives exponentially many rooted size-s candidates, not exponentially many in n at fixed s. Low fixed temperature makes the standard rooted polymer mixing condition hold. Truncation at O(log(n/epsilon)), positive gas inclusion bounds and a conventional polymer sampler provide total variation epsilon accuracy. Coupling values and random probabilities must be computed to charged polynomial precision; no exact-real-number oracle is assumed. This is polynomial in n/epsilon for fixed construction and temperature constants, not claimed polynomial in log(1/epsilon) or practical for the enormous constants.

## 6. Ideal physical use and the remaining loader barrier

Given a supplied encoded logical input rho_L, including one entangled with an external reference, sample sigma and apply the SAME decoder Pauli representative E_D(sigma). The resulting channel is

    rho_L -> Σ_sigma p_beta(sigma) E_D(sigma) Enc0(rho_L) E_D(sigma)†,

the commuting Gibbs syndrome state in that decoder's logical frame. Sampling error at most epsilon in total variation bounds the preparation-channel error correspondingly (up to the chosen trace-distance convention), uniformly for reference-entangled input.

The reconstructed correction can be computed through the hierarchy in polynomial time and applied as single-qubit Paulis after charged classical routing. It need not be an energy-monotone or passive preparation path. If no encoded input is supplied, a separate active encoding circuit is required. Geometrically local compilation using clean communication ancillas and swaps may have polynomial cost, but it must be counted; it is not provided free by the syndrome sampler.

Likewise, fixed-rate noisy gates, resets and final physical output errors are NOT handled by this ideal proof. Generic fault-tolerant circuit simulation does not automatically deliver a bare physical thermal state close in global trace distance; terminal local errors can accumulate over n qubits. An operational noisy-loader theorem and comparison with an actively protected fault-tolerant memory remain separate. This result, if accepted, removes the constructive ideal thermal-syndrome initialization obstruction only.

## Source anchors

Actual decoder and admissibility inequalities: https://arxiv.org/html/2605.10943v1 §§4.1–4.3, Theorems4.6/4.7, Lemmas4.8/4.12 and the intermediate syndrome-weight statements. Recursive reconstruction: Eq.(121). Initialization caveat: §1.3 item2. Abstract trace gas and sampler: the root's separately audited lemma; no novelty claim for conventional polymer mixing.

## Essential trace-footprint boundary

Only local one-step reductions, local corrections f_i and local telescoping-identity checks belong to the activity trace. DO NOT include the full downward physical reconstruction F...F f_i in that trace: a high-level correction may expand to a large physical support and would spoil the linear trace-energy bound. Full physical Pauli synthesis is performed and charged separately AFTER the syndrome sample is selected.

Matched endpoint reference: source §5.1.1, Eq.(206), not merely the earlier §4 unmodified seed decoder.
