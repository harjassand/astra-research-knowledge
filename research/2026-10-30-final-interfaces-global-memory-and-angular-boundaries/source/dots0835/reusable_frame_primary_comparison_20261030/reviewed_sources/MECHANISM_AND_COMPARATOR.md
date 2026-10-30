# Reusable absolute-frame tracking: root check and consequential boundary
2026-10-30. Working note, not an independent whole-theorem review.

## Exact finite clock check
For a finite group with m chosen matrix representatives, use m ready labels r_g and m(m−1) transit labels e_ab. Assign physical frame W(r_g)=g, W(e_ab)=b. The permanent onsite controlled unitary G defines the actual memory generator by conjugation. A target v selects disjoint Hamiltonian pairs r_g ↔ e_gv for g≠v. All e_ab→r_b resets are distinct resolved channels. Coherent aggregation of these resets is inadmissible: it creates dark stale combinations.

In the fixed G frame every command is DATA identity. With Ω=κ=1 the exact killed-clock Poisson witness is the block [[2.25,−i/2],[i/2,2]] on every active pair, scalar3.25 on e_ab with b≠v, and zero at r_v. The jump gain into r_b explains the extra waiting cost on stale transits. Its adjoint drift is exactly −I_active. The included numerical regression checks all targets for m=2,...,8. This checks finite matrix algebra, not a hardware experiment or full many-body theorem.

The analytic extremal eigenvalues are independent of m, although the actual local register dimension is m² and the number of independently specified transitions grows. Thus group size need not degrade this isolated clock lifetime estimate, but the entire apparatus and control synthesis are not resource free. Fixed bounded local body size after grouping still requires physical joint access to the b constituent blocks.

## Why the seam is removed
The SAME G and SAME memory forest are used for every command. No native engine is reset, no busy clean prefix is erased, and no ideal frame operation occurs between commands. This avoids the false inference that the global energy bound makes all clean busy controllers sparse. That energy only charges raw syndrome and bad-history defects.

To implement relative gates h_j, the prescribed absolute targets are cumulative v_j=h_j...h_1, with an explicitly chosen representative. Projective scalar phases do not change the desired logical channel, but controlled physical hops must use the exact chosen matrices v_j g† consistently.

Final output still uses the target native-frame inverse F_v† and ordinary DATA recovery. A settled-output theorem is not an executable noisy readout theorem or a proof that arbitrary mid-command interventions compose. Native stored logical information is protected on one uninterrupted killed trajectory; physical commands act through G, not through inserting the target into the DATA decoder.

## Strong comparator and next obligation
For fixed b uniform transversal Clifford operations, an arbitrarily long command string compresses classically to its final finite group element. An informed ordinary implementation can track this Clifford frame and apply only the final physical layer, or alter eventual measurement bases where allowed. Therefore absence of a sum of per-command errors does not by itself create deep computational power or a speedup.

The narrow capability under investigation is repeated physical target tracking while continuous native correction remains active, without synchronized local completion or native reset. The external target distribution, bounded calibration deviations, dwell time, exact paired hardware and final ideal output remain paid premises.

A major computing bridge would need operations that cannot be deferred into one uniform finite frame: actual protected measurement/feedback, addressable logical operations, a resource-consuming non-Clifford interface, or changing partners without hiding growing support. Those are substantive missing operations, not consequences of a larger clock alphabet. No universality or practical advantage is claimed.

## Primary comparisons being inspected
- Lebreuilly et al., Autonomous quantum error correction and quantum computation, https://arxiv.org/abs/2103.05007. General engineered-Lindbladian/error-transparent computation is established prior machinery; whole source comparison is assigned separately.
- Roy et al., Error semitransparent universal control of a bosonic logical qubit, https://arxiv.org/abs/2603.15356. Dynamic encoding is not automatically novel; error model and preparation/control interface must be compared from the paper, not the abstract.

## Code-preservation correction (independent challenge)
The finite physical group must consist ONLY of transversal automorphisms of the actual code, with specified logical actions. Generic Tanner CSS codes do not supply transversal H, S or arbitrary uniform Pauli gates. A safe concrete family on b identical CSS blocks is the CNOT/SWAP-generated GL(b,2), represented by exact computational-basis permutation matrices. Earlier references in this working note to a Clifford group are conditional on this code-preserving restriction, not a grant of the whole Clifford group. The stronger primary comparator above is therefore at least as relevant.
