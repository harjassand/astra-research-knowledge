# Explicit top-r projector deployment as an alternative to the learned decoder SDP

27 October2026. Local post-cutoff alternative only. The received SDP receiver remains canonical and has better constants. Independent receiving requested.

Use the same actual acquired Hhat, source H=J-3omega and A=J+3omega as in the received fast Sylvester acquisition. Instead of the operational decoder SDP, maximize Tr Hhat F over the LARGER set

 0<=F<=I, TrF<=r.

A maximizer is the projector P onto at most r largest positive eigenvalues of Hhat. This is computed from the learned classical matrix. The true Bell/active-flag projector Pi and every comparator feasible for the old SDP belong to the larger set. Both received localization lemmas used only the displayed effect/trace constraints, not the old partial-trace constraint. Consequently their comparison bounds transfer verbatim:

 exact orthogonal reset: delta=2p/3-TrHP<=140rt+2kappa;
 arbitrary reset overlap: delta<=3L_*+300rt+2kappa.

Here kappa is a charged additive maximization gap; exact top-r spectral optimization has kappa=0. These are score/effect comparisons. The projector P is not asserted to be the Choi operator of a single accepted CP decoder.

## A physical sequential decoder from the nine conjugate tests

Let S be the success Bell Choi block, O the other eight success Bell blocks, and N=I_A tensor(1-p)tau=3J_reset. Then

 H=2S/3-O/3-2N/3,
 delta=(2/3)TrS(I-P)+(1/3)TrOP+(2/3)TrNP>=0.

The true Pi supports S and is orthogonal to O. Define the nine learned projectors P_j by the known reference-Weyl conjugations of the SINGLE learned P; true Pi_j are the corresponding ideal Bell projectors. Because the true omega is reference-Weyl invariant, each conjugate has the same score deficit delta. No new source samples are needed for these labels.

On the genuine measured-register marginal omega_code=(S+O)/9,

 Tr omega_code(P-Pi)^2
   =[TrS(I-P)+TrOP]/9<=delta/3.

This identity uses P²=P and commutation of Pi with the code marginal, not [P,H]=0. Also omega_reset=N/3 gives

 Tr omega_reset P=TrNP/3<=delta/2.

Thus the received retained-data sequential Bell-ancilla construction applies: measure P_1,...,P_9, keep systems after rejection, perform the known correction on first acceptance, erase after all failures. The complete error bound is

 ||D_spec E-G_p||_diamond<=18sqrt(2p delta)+162delta.   (1)

For genuine data use ideal Pi-prefixes and actual suffixes, exactly as in the independently received projector receiver. For reset use the ALWAYS-REJECT comparison, whose accepted probability is at most81delta. Under overlap the true Pi decoder need not reject reset; it is NOT used as the reset comparator. The branchwise comparison merely bounds the actual linear genuine/reset mixture against G_p, and does not assert the existence of one latent-branch-aware ideal decoder.

## Verification and resource scope

The same annihilating-output-projector argument gives the actual holdout parameters

 b<=243delta, |a-p|<=243delta.

For exact orthogonal reset one safe constant choice is

 t=nu²p0/(10^9 r), kappa<=rt,

giving delta<=142rt, a>=3p/4 and

 b/a<=324*(142/10^9)nu²<nu²/6144.

Therefore the SAME spectral decoder satisfies the learned-throughput verifier's completeness margin at target nu, with supplied acceptance floor p0/2. Only constants worsen relative to the canonical SDP receiver; source-query scaling remains O(sr/(p0nu²) polylogs), and the actual-a holdout cost remains O(log(1/beta)/(a nu²)) in its received expected/high-probability sense.

This alternative makes deployment a finite sequence of nine learned projective tests and known qutrit corrections, rather than synthesis from an arbitrary SDP Choi matrix. It does not supply an unknown source purification or inverse. Approximate eigenspace optimization must pay kappa; implementation of the learned projectors must separately pay circuit error. It does NOT remove the collective Keyl training measurement or its explicitly unknown general-n efficient implementation. No constant-memory or matching accuracy lower is inferred. The robust comparator term L_* remains charged under overlap; no new entropy sufficient condition is asserted here.
