# Quantum-weighted seed effects in an explicit read-off window
30 October 2026. New receiving derivation by the reviewer. Distinct from the frozen source review; not a full source/capture/factory theorem.

## Operational schedule and exact hypotheses
Fix a supplied genuine instrument outcome m. Raw latches are physically |m>; target seed bits may be arbitrary and correlated with quantum DATA/controllers/bath. The reference m is historical, not an immune physical latch. During the finite target-reset and seed-CNOT window of total duration tau_seed, switch OFF the quantum correction/read Hamiltonians and quantum reset service. This is an explicitly scheduled changed resource, not autonomy. Nominal seed operations act only on records. Every physical bit and all quantum apparatus remain exposed to their declared weak joint noise.

Let F_Q>=I be the fixed hard-coded native quantum witness for this m. It is an ANALYSIS observable; switching the physical quantum generator off does not require physically applying F_Q or knowing a global frame. The actual native finite-depth local relative/dilation bound holds for F_Q on the full Hilbert space, uniformly over m and with arbitrary retained bath. All O(N) quantum DATA/controller sites are counted in N_Q. In particular, a bounded-system-support joint HP term of cb strength eta_e acting on Q and arbitrary bath satisfies the corresponding F_Q weighted bound with a fixed C_Q. Noise system body size q and per-site incident cb sums are bounded. The full generator has CPTP propagators.

These are the same local relative bounds used to price broad noise in the native energy theorem, not the stronger negative-drift theorem. No active native correction is used in this window. If some desired physical background Hamiltonian remains on, it must commute F_Q or be separately included with its actual weighted cost.

## Weighted subset inequality
Use the actual mixed-reset test from SEED_MIXED_RESET_SUBSET_LEMMA.md:

 f_S(t)=exp(theta_hi sum_raw-selected B_i+theta_A(t) sum_target-selected B_i),
 theta_A'=kappa(1-exp(-theta_A)), theta_A(0)=theta_lo,
 theta_A(tau_reset)=theta_hi.

The target reset adjoint and the test derivative cancel EXACTLY, also after multiplication by F_Q, because resets act on records only. Raw latches are not reset. The initial raw |m> compression gives the operator bound f_S(0)<=exp(theta_lo |S|)I on the allowed raw-input subspace, even for arbitrary dirty targets and Q correlations.

Partition each actual noise term according to its record support:

- If it meets S, the ordinary bounded record-factor ratio is at most exp(q theta_hi). Combine this with the F_Q native local relative bound if it has Q legs. Sum over the selected record-site incidence budget. The cost is C eta exp(a theta_hi)|S| F_Q f_S. This sum includes Q/record mixed terms that touch S.
- If it misses S and has no Q leg, it annihilates the test: its record factors are identity on its support, and its adjoint annihilates identity on those records/bath.
- If it misses S but has Q legs, f_S is untouched. Its native weighted bound costs C_Q eta_e F_Q f_S. Charge the complete term to its Q incidence. Summation is at most C_Q eta N_Q F_Q f_S, regardless of the number of unselected raw/bulk/seed records.

Thus the actual operator inequality is

 (partial_t+L^*)(F_Q f_S)
 <=[C_Q eta N_Q+C eta exp(a theta_hi)|S|] F_Q f_S.       (WS1)

There is no assumption that conjugating by F_Q preserves locality or trace preservation. The argument uses the known complete local congruence bound directly. A decomposition of noise into independent trajectories is neither needed nor supplied.

During the ideal seed-CNOT circuit, use its partial-circuit chart. The circuit is record-only and commutes F_Q. It enlarges system support and incident constants only by the fixed seed-cone size (n0 was fixed first). The same partition proof applies with fixed enlarged constants. The nominal copy Hamiltonian cancels the moving test derivative exactly.

## Complete effect bound
Integrating (WS1) and using the mixed-reset exponent schedule gives, for every selected input-defect set S, the effect inequality on the allowed raw |m> input subspace:

 T_m^*(F_Q product_(i in S) B_i,out)
 <=exp(C_Q eta N_Q tau_seed) p0^|S| F_Q,              (WS2)

with

 p0=exp[-theta_hi+theta_lo+eta A(theta_hi)],
 A(theta_hi)=C_reset tau_reset exp(a_reset theta_hi)
             +C_copy tau_copy exp(a_copy theta_hi).

The B_i,out are the commuting input-defect projectors in the final copy chart. The input space includes arbitrary dirty targets and Q/bath; F_Q is extended by identity on the former. The scalar e^(C_Q eta N_Q tau_seed) may be absorbed in the Q extensive moment coefficient. Crucially it is not e^(eta nT tau_seed). This bound is uniform with retained references and m.

For disjoint seed cones C_j, A_j=OR_(i in C_j)B_i, and p_seed=c0 p0, positive witness expansion gives

 T_m^*(F_Q product_(j in L) A_j)
 <=exp(C_Q eta N_Q tau_seed) p_seed^|L| F_Q.          (WS3)

Let W_j be the actual combined phase/root seed test with
 W_j<=w_vac+(w_max-w_vac)A_j,
 A_seed=w_vac+(w_max-w_vac)p_seed.

All these record operators commute F_Q. For disjoint L,R expand the positive product exactly as in the unweighted seed lemma:

 T_m^*(F_Q W_R product_(j in L) A_j)
 <=exp(C_Q eta N_Q tau_seed) p_seed^|L| A_seed^|R| F_Q.  (WS4)

If the incoming quantum moment is exp(nu_w N), the full seed quantum/root moment over B driving records is at most

 exp[nu_w N+C_Q eta N_Q tau_seed+|B| log A_seed].

This earns a JOINT moment under common-bath noise. It is not inferred from two separate moments. Choose n0 and root parameters first, theta_hi/reset duration next, then eta small enough to make both the seed residual and C_Q eta tau_seed small. There is a positive simultaneous margin whenever the original warm quantum coefficient has one and the record vacuum factor can be chosen sufficiently close to1. This is a fixed-parameter existence order; no useful numerical threshold is asserted.

## Weighted signed initial flags
The same complete-map Cauchy-Schwarz argument applies after conjugating the input by F_Q^(-1/2). For ket/bra seed cuts whose bad union is D, keep W_R on disjoint remaining records. Both effect estimates have the common factor exp(C_Q eta N_Q tau_seed); their geometric mean therefore has that factor once, not squared. Summing the at-most-three sector choices per marked record yields

 ||initial_union_D||_(F_Q W_R <- F_Q)
 <=exp(C_Q eta N_Q tau_seed)
       (3 sqrt(p_seed))^|D| A_seed^|R|.              (WS5)

This is a complete weighted norm for the actual seed channel with its reference input. It does not make signed components positive or certify subsequent phase insertion maps.

## Remaining physical and source seams
The read-off interval itself is essential here: while initially dirty root latches have no credited phase/root law, enabling all quantum baseline reads would incur an uncontrolled order-N strong source. The present schedule avoids that rather than declaring those ports already reliable.

A small moment does not imply exact support in the quantum safe basin or a common logical span. This derivation does NOT bound quantum logical exits during the read-off window. One must either combine the actual finite-time coherent source-support theorem, or apply a separately justified quantum killed-window/source-strip estimate with its initial support and fixed gap. That step must preserve complete maps and the genuine outcome/frame interface. The subsequent active native receiver, global record phase flags, final record computation/correction, and autonomy remain outside this lemma.
