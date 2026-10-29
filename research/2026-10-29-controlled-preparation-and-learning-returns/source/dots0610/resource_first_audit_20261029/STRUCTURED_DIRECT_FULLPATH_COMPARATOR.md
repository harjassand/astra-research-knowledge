# Equally informed direct full-path alternative
2026-10-29. Independent algebraic comparator, no new historical-priority claim.

For the SAME h-block four-spin singlet code Q=(P4)^tensor h, K=2^h, its maximally mixed state factors across blocks. One-body means vanish; same-block pair covariance is−delta_ab/3; different-block covariance vanishes. Therefore for H=(1/2)sum_i h_i.sigma_i,

 Tr(Q H²)/K = (1/3) sum_blocks sum_{i in block} ||h_i−hbar_block||²
              ≤ (1/3) sum_i ||h_i||².

Q is inside full P. The source is identity on full P tensor the same bath operation, so the identical physical-vector argument, now on a Q-logical Bell input, gives

 p_raw,Q ≤4||Pperp W Q||F²/K ≤4 Tr(QH²)/K
          ≤16 pi²(n−1)e²/gL² ≤16 pi² n e²/gL².

Here Pperp is the complement of the FULL singlet P, not Qperp; source cancellation on P makes this distinction valid. Completing the fixed Q decoder can only add overlap to the exact decoded Bell projector, so its entanglement infidelity is no larger.

Use actual full-path two-MUB survival tests on h bare logical qubits (computational/Hadamard product bases) including the same E→source→D. Their first-moment average is I_K/K, so their average failure q≤1−Fe; their usual witness bound is1−Fe≤2q. Fresh private bare-logical Pauli pads before E and after D produce the accepted arbitrary-memory guard interface, at O(h) single-qubit gates and2h random bits. No encoded-Pauli compiler or physical permutation is needed.

Choose e_target=g0/(600sqrt n). With gL≥g0/2,
 p_raw,Q≤64pi²/360000<1/512.
The exact matrix-radius requirement is m≥(1800+62e_target)ell/e_target², still O(n g0^−2 log(n/delta)); e.g. conservative650000000 n ell/g0² suffices for the same n≥20,g0≤4 range. Set witness coefficientC=2 and service probability1/3. The same outer B-symbol code, t=B/8, b=B/32 and cap6B then satisfy the SAME displayed soundness and completeness tail bounds and asymptotic source-exposure order.

This comparison assumes the same known implementable four-spin block encoder/decoder and trusted controls. Full-path tests pay those endpoints; matching tests bypass them and have a different interface. Conversely full-path tests directly include deployed endpoint errors, while matching requires additional trust/calibration/isolation. The two architectures need an explicit control/cost model to establish any advantage. Both have linear-in-n endpoint/matching-test elementary work when the four-spin blocks are fixed-size compiled modules.

Thus polynomial structured-family completeness is not exclusively enabled by the physical orbit. The orbit's separately proved model-free removal of the d/K penalty for MATCHING-only tests remains valid and useful; do not confuse that specific transfer with necessity for all equally informed full-path certification.
