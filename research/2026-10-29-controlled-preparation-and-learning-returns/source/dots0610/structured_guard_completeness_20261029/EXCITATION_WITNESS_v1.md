# A nonempty bath-coupled family with exact occupation gap one
2026-10-29. Complementary existence/identifiability construction; not a way to force arbitrary sources to become informative.

In the unknown true local frames, let every training call consist of ANY full-joint collective-algebra operation U on the n data qubits and retained bath, followed by a fresh uniform collective rotation from the24 proper signed-permutation rotations of the Bloch sphere. The rotation is sampled independently of the bath/history and current probe settings. Its label may be retained by the source afterward. Neither the rotation label nor the fixed local frames is available to the learner. Arbitrary bath-coupled collective dynamics before this fresh randomization are allowed, as are source adaptivity and no reset. This fresh second-moment condition is a supplied source-family promise.

For a pair i,j, octahedral averaging gives exactly

 E_R[(R† sigma_a R)_i (R† sigma_b R)_j]
   = delta_ab/3 * D_ij,
 D_ij=sum_c sigma_c,i sigma_c,j = 2 SWAP_ij-I.

Every full-joint collective-algebra U commutes with every permutation, hence with D_ij tensor I_M. Pulling the observable back through U therefore leaves D_ij unchanged, regardless of the bath state or entanglement. The expected pair correlation map in the true frame is exactly

 T(A)=trace(A) I3/3

on the9-dimensional correlation coefficients. There are no identity or single-site coefficient contributions, since the pulled-back observable is precisely the pair-dot observable. Thus the16x9 defect (including its zero extra rows) is Pi-I9, the NEGATIVE orthogonal projector on this correlation sector (the governing convention is M=T-J). Its kernel is vec(I3)/sqrt3 and all other singular values are exactly1. Unknown local frames act by orthogonal coordinate changes, preserving these singular values. Every conditional expectation, and hence every actual predictable occupation average, has this same kernel and gap1. No iid bath assumption is present.

This closes a NONEMPTINESS obligation for the structured completeness premise even with nontrivial retained bath dynamics. It does not show typical laboratory noise has such excitation, or provide a way to impose this fresh randomization without knowing the hidden frames. Source operations after training need only remain in the same full joint algebra; the fresh octahedral rotation is not needed for guard soundness or deployment completeness once the frame is learned. The witness is an explicit subclass, not a claim that each generic collective source has gap1.

`check_excitation_witness.py` verifies the24 rotations and the exact rank-one twirl using symbolic rational arithmetic. The group moment and permutation commutation argument are conventional representation facts; no novelty claim is made for either individually.
