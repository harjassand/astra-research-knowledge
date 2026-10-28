# Physical repetition-code noise supplies an acquired excitation witness

28 October 2026. **Separate author-checked witness, not a receipt for the general acquired-patch theorem.** No calibration source outcomes or random draws occur here. This strengthens the illustrative maximally mixed-gauge example without modifying its parent source.

Encode one unknown logical qubit as |0> -> |000>, |1> -> |111>, pass the three physical qubits through independent bit flips of probability 0<p<1/2, and optionally apply an unknown FIXED three-qubit output unitary V. The latter makes the actual logical generators unknown; it does not change their width-three support or any spectra below. This is a physical unflagged channel: all three physical outputs are accessible, but no syndrome label is handed to the learner. The physical noise/encoder decomposition is a mathematical witness, not an acquired input to the algorithm.

Let e_g run over 000,100,010,001, and let U_maj|l,g>=|l*111 XOR e_g>. Set U=V U_maj. For an error pattern f, either f=e_g or f=111 XOR e_g. Thus the exact channel is

    E(rho)=U[rho tensor G_I+X rho X tensor G_X]U^dagger,
    (G_I)_gg=p^(|e_g|)(1-p)^(3-|e_g|),
    (G_X)_gg=p^(3-|e_g|)(1-p)^(|e_g|).                 (1)

All other logical Pauli blocks vanish. The quantum coherences of rho are retained in this identity; it is not merely a classical computational-basis statement. For p<1/2, G_I-G_X is positive in every syndrome coordinate. Therefore exact majority/syndrome extraction after V^dagger is optimal among ALL full-CPTP logical receivers under the source's Bell-block criterion. Its loss is

    ell_* = Tr G_X = 3p^2-2p^3.                        (2)

The X signed block is H_X=G_I+G_X, while H_Z=G_I-G_X. In the three weight-one syndrome coordinates their relative contrast is exactly 1-2p; the zero-syndrome relative contrast is at least that. Consequently a valid uniform CP margin is

    kappa=1-2p.                                      (3)

The parent coarse support learner still needs a SUPPLIED positive rational lower bound kappa_0<=1-2p. For example, a trusted class bound p<=p_max<1/2 supplies kappa_0=1-2p_max; the actual p, gauge weights, and excitation floor need not be given to the learner. If no positive margin bound is supplied, this corollary does not silently acquire one or inherit the parent's coarse horizon. The direct-gap fine guard can recognize its actual gap without knowing p, but that does not remove the separately paid coarse kappa_0 cost. The displayed value (3) is the witness's actual margin, not an observed input parameter.

When ordinary signed inputs are averaged, the logical input is I/2 and the three-qubit output marginal is U(I/2 tensor G_total)U^dagger. Its gauge eigenvalues are

    g_0=(1-p)^3+p^3=1-3p+3p^2,
    g_1=g_2=g_3=p(1-p).

Since g_0-g_1=(1-2p)^2, the patch marginal floor is EXACTLY

    r=lambda_min(rho)=p(1-p)/2.                       (4)

The smaller of the X/Z signed spectral gaps is EXACTLY

    gamma=p(1-p)(1-2p)/2=kappa r.                     (5)

Thus the acquired-patch procedure can recognize full excitation from actual ordinary records; no special gauge-preparation control or supplied gauge spectrum is necessary. Its finite fine-bank rate specializes to O_tilde(3^3/[p^2(1-p)^2(1-2p)^2 epsilon]) at q=1,A=1,W=3, with the parent theorem's conservative constants and capped certificate/abstention qualifications. This is an existence/structural example, not a practical-budget assertion or an improvement over the equally informed conventional tomography/sign learner.

After the algebra has been operator-norm certified, the future gauge need not maintain this distribution, its rank, or its floor. The fixed U can be serviced with arbitrary emitted gauge states, even coherently correlated with retained memory, through the parent certificate. A later independent physical-flip probability in [0,1/2) still has the same majority algebra and identity dominance; more general future maps need the explicit parent source promise. Acquisition contrast need not stay positive merely to define exact extraction, but current-state full-CPTP optimality still requires the separate dominance condition.

The limiting obstruction is informative. As p tends to zero, this source becomes an excellent physical code channel while the rare-syndrome excitation r and gamma tend to zero. Uniform correctness on completely NEW future gauge directions is harder to certify, even though ordinary current-gauge payload recovery can be easy. It would be false to claim the acquired all-gauge route is optimal for a stationary nearly noiseless source, or that no other recovery learner can work there. At p=0 the full-patch certificate should abstain unless additional access or persistence information is supplied. At p=1/2 the logical Z contrast vanishes; the positive-margin premise fails.

`redundant_repetition_excitation_physical_noise_witness_20261028.py` checks exact rational Choi matrices, TP, every syndrome CP-order inequality, margins, floors, signed gaps and the full-CPTP oracle probability at six rational noise levels. It includes the complete off-diagonal Choi entries and every physical error pattern. These are source-disabled exact algebra checks, not samples or a production learner run.
