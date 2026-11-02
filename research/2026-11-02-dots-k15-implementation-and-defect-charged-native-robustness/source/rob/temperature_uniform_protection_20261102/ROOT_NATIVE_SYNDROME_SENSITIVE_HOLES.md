# Native-clock transfer candidate: charge singleton pressure only to actual defects

Root, 2026-11-02. Proposed refinement of the ALREADY EARNED full-column/singleton-normalized native source dictionary. This is not obtained by deleting positive terms from a noncommuting native Hamiltonian. Independent construction/audit needed before claiming the transfer.

For clock a let M0_a=integral_0^infty rho_a, J_a,beta=integral_0^beta rho_w,a and h_nv,a,beta=integral_0^beta(rho_a-rho_w,a). Set

 delta_a = M0_a-h_nv,a,beta-J_a,beta = integral_beta^infty rho_a >=0.

The raw marked-column norm bound contributes exp(beta M0_a), its owned nonwinding singleton deletion contributes exp(-beta h_nv,a,beta), and its owned winding deletion contributes EXACTLY exp(-beta J_a,beta s_a). Their product is

 exp(beta delta_a) exp[2 beta J_a,beta 1{s_a=-1}].

This is the same cancellation previously bounded uniformly by exp(2 beta J_a). Keeping the sign gives a finite-capacity positive check hole, not a constant Boltzmann penalty.

For an exterior contact clock, the winding singleton response is exp(integral rho_w s_a(B_pin-1)), B_pin in {0,+1,-1}. Since B_pin-1<=0, its modulus is <=1 for s_a=+1 and <=exp(2 beta J_a,beta) for s_a=-1. Exterior nonwinding and wrap responses have modulus<=1. Hence the normalized source envelope refines to

 integrated |z_Gamma(s)| <= q_native^m exp[sum_{a in T_Gamma} 2 beta J_a,beta 1{s_a=-1}],

 q_native = K_max^b_c d_B^b_B exp(beta delta_max b_c)
                [exp(beta v_dict)-1],

with actual heterogeneous product factors available instead of K_max. All dictionary/incidence overhead remains explicit. The positive tail delta_a decays at the native clock gap scale; it is not a constant exp(beta J) tax.

## Exact background to retain

The one-winding pressure provides the additive commuting syndrome energy with B_a=2 beta J_a,beta. Keep all multi-rod connected clock clusters as the independent complex EVENT species of the previous exact two-species construction. Their event-event factor remains 1. Each event's syndrome dependence is a character on the clocks of its winding rods, hence supported on at most its rod count. Its source-event factor is the already earned B_Gamma(event) in {0,+1,-1}.

The baseline can therefore be written as additive reference defects plus these independent clock events. No multi-rod correction is discarded or assumed positive. Its weighted rooted activity E_gamma is O(beta J D eta²) plus wraps, and must meet an explicit margin.

## Combining with finite-capacity swallowing

Use the new exact canonical defect trace gas for the additive B_a syndrome weights. Swallow into each source group every defect polymer whose occupied top support hits T_Gamma. At most d_c m defect bits can lose their positive energy. The finite-capacity summation should charge their entropy by constant^m instead of exp(B d_c m).

After extracting the hole factor, a fixed source history has a bounded function of s restricted to T_Gamma, times its actual finite-support Pauli stabilizer character. Expand only this O(m)-bit contact function, costing at most 2^O(m). Do NOT Fourier-expand the whole polynomial-size stabilizer filling. The residual character is handled by the audited two-certificate asymmetric KP lemma.

Retain clock events as a third independent species. They interact with defect polymers by their check characters, with source histories by the earned pins, and with decorated groups by the product of these factors. Cross factors still have modulus<=1. Rooted event/source/defect rows must all be checked at inflated charges. In particular a group of total mass u=m+M can contact events through its source contacts O(m) and occupied defect checks O(M), so a potential row cost O(E_gamma u) is plausible but not yet a proved join.

## Required checks and scope

Check exact singleton signs including all thermal wraps; the finite-time delta identity and uniform tail; bounded contact-function expansion for generic clock/bath matrix insertions; exact three-species reconstruction; event row counts after swallowing; marked fugacity tilts and exceptional logical matrix roots. The original prefix-gauge dictionary and physical Hamiltonian are unchanged.

If these checks pass, this is a same-native-H finite-temperature generic perturbation improvement with source admission governed by beta v and finite local dimension/dictionary constants, rather than an extra exp(C beta J). It does not prove a fixed nonzero v window as beta tends to infinity, remove clock dimension or large energy ratios, provide a physical WRITE operation, or establish practical advantage over active error correction.
