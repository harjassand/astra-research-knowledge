# A slower unframed local inverse that transfers to arbitrary coherent source memory

28 October 2026. **New candidate fallback; independent receiving pending.** This does not repair the false CP-domination claim for a merely reduced Pauli channel. Instead it pays tighter operator learning and uses the actual coherent extraction circuit's complete-norm closeness. It targets the PARTICULAR fixed inverse Vdagger, not an identity-logical source or a recovery oracle.

## 1. Calibration needs only a reduced-port structure

Use the full physical n-qubit input/control/readout port and fixed unknown V with width-w output Pauli-generator supports from the separate physical-port sources. The true complete calibration channel is

    N=(Ad_V tensor id_M') o A,

where A:P M->P M' can retain COHERENT physical-error amplitudes, not only a classical Pauli-instrument label. Require only its reduced physical output to obey, on every input rho_P and memory state omega,

    Tr_M' A(rho_P tensor omega)
       =sum_alpha Tr(E_alpha omega) P_alpha rho_P P_alpha^dagger,
    E_alpha>=0, sum_alpha E_alpha=I_M.                           (1)

The equality for all product states extends linearly to all operators; a complete joint Pauli-instrument representation of A is NOT assumed. At each prior history impose the qualitative effect inequalities

    A_(i,j)=sum_alpha chi_(i,j)(alpha)E_alpha>=0, j=X,Z.         (2)

Effects, V and the microscopic completion are unknown. Current private preparation/readout coins do not leak to the source's selected current map. The effects/completion may change with all exposed past history. As before this is a trusted reduced-port model, not membership certified by ordinary tomography.

For example A|psi>=sqrt(1-p)|psi>|0>+sqrt(p)Z|psi>|1> has reduced physical Pauli noise and positive X/Z effects for p<1/2, but retains coherent error branches. It is NOT the complete CP-instrument model. Its off-diagonal environment blocks are not discarded in the guarantee below.

Equation (1) is exactly enough for the actual calibration observations: rho_J=I/2^|J| and, on any envelope containing the true support B_(i,j)=V sigma_(i,j)Vdagger,

    Delta_(i,j,J)=B_(i,j,J) theta_(i,j)/2^|J|,
    theta_(i,j)=Tr A_(i,j)omega in [0,1].                        (3)

Disjoint signed reductions vanish. Thus the same paired-axis coarse discovery and finite matrix-martingale/rational-sign argument as the effect-level acquisition source gives individual OPERATOR certificates. Only observed reduced conditional means and positive physical output states enter concentration; no positivity of a signed outgoing-memory map or classical which-error representation is needed.

## 2. Tighter finite fitting, not a Bell-to-diamond shortcut

Fix a desired per-use complete inverse error 0<zeta<=1. Let delta be the largest positive dyadic with

    delta<=zeta/(3n),

so delta<=1/4 and delta>zeta/(6n). Use the received support stage/caps unchanged. In each fine bank use EXACTLY its matrix estimates, rational Jacobi residual a_s/4 and raw-sign reflection. Replace its acceptance tolerance by delta:

    e_s=5a_s/4, h=min|D_kk|,
    h>e_s,  2e_s<=delta(2h-e_s).                                (4)

The same simultaneous event of probability >=1-beta then gives

    ||S_(i,j)-B_(i,j)||op<=delta for all 2n generators.          (5)

Different generators can be retained at different informative stages. The fixed finite cap can end in ABSTAIN before requesting an unknown payload. All exact-control operators are physical even on bad records; good records supply the extra deterministic approximation guarantee.

With W=min(n,3w-2), a_s=2^-s/(16*2^W), N_s=8*3^W L/a_s² and the same finite union logarithm as the received margin-free source, a true signed gap gamma permits acceptance once a_s<=delta gamma/5. At the first sufficient scale,

    N_s<800*3^W L/(delta² gamma²)
       <28800*n²*3^W L/(zeta² gamma²),                          (6)

and cumulative fine calls are <(4/3)N_s. All source blocks prepare/read n physical qubits. Under persistent effect margin theta_* the instance rate is O_tilde(n²12^W/(theta_*² zeta²)), plus coarse discovery. This slower inverse-square-accuracy upper resource bound is NOT a lower bound or a practical budget. No numerical margin need be given to the learner; a funded sufficient cap and informative histories remain necessary for completion.

## 3. Actual circuit closeness is dimension-free and unframed

Let W_hat be the literal colored coherent three-controlled-reflection SWAP receiver with n fresh mixed receiver qubits, using the learned S. Let W_* use the true B and the SAME receiver initialization/order. For each logical i the ideal three blocks swap its true physical logical factor into its receiver qubit. Across all n factors W_* implements exact Vdagger on the retained receiver output.

A controlled-reflection difference has norm at most its reflection difference. A telescoping expansion of the ACTUAL 3n unitary blocks therefore yields

    ||W_hat-W_*||op
       <=sum_i[2||S_(i,Z)-B_(i,Z)||+||S_(i,X)-B_(i,X)||]
       <=3n delta<=zeta.                                       (7)

This uses the circuit itself, not a dimension-dependent generic conversion from an n-qubit Bell score. For any input entangled with arbitrary memory/reference and any purification of the fixed receiver initialization, the two output vectors differ in norm by at most zeta. Their trace distance is at most 2zeta, and tracing discarded physical/receiver workspace cannot increase it. Hence the unframed extracted channels satisfy

    (1/2)||Dhat-Ad_Vdagger||diamond<=zeta.                      (8)

No Pauli frame or current-key covariance is used. In particular the fallback does NOT pay the 2n service frame bits required by the faster CP-instrument route. The rest of the local reflection, ancilla, routing, synthesis and storage bill is unchanged. This does not grant any unmodelled access to receiver records; it simply compares the declared complete physical circuit outputs.

Now (8) can be composed after ANY actual future source N_future, even with coherent retained-memory branches or a reduced channel that has changed after calibration:

    half-diamond[(Dhat tensor id)N_future,
                 (Ad_Vdagger tensor id)N_future]<=zeta.         (9)

The comparator is still the PARTICULAR fixed Vdagger. It need not be an oracle or undo the whole source. A supplied known quantum encoder/decoder can be composed on the two sides without increasing the bound. No native error suppression or identity-logical guarantee is inferred for an arbitrary coherent completion.

## 4. Finite causal reuse and limits

With an arbitrary common permitted causal controller and J finite uses, an ordinary complete-norm hybrid gives process-distance allowance at most min(1,J*zeta), with the same actual calibration record, initial source memory and controller. This remains valid with coherent output feedback because the per-use complete-channel discrepancy is uniform over its incoming state. There is no all-clean CP branch, ideal-mixture coefficient or assumption that errors commute through feedback. For a total target choose zeta proportional to epsilon/J, leading to the stated J²/epsilon² calibration accuracy cost.

Bad-certificate probability beta, full retained calibration-record discrepancy nu_cal and WHOLE J-service implementation discrepancy nu_J are paid once as

    min(1,J*zeta+beta+nu_cal+nu_J).                              (10)

Both protocols share acceptance/abort; the unknown payload is introduced only after acceptance. Conditional-on-acceptance risk pays the acceptance denominator. For payload-only induced channels the usual conditional product input/source contract applies; alternatively the comparisons are complete maps on the enlarged joint input.

The sharp coherent-error-flag obstruction is preserved: a reduced Pauli channel does NOT support the faster complete CP-domination theorem, and complete error can scale as the square root of a learned inverse's Bell deficit. The present fallback intentionally buys a linear operator-error guarantee instead. It permits that coherent retained memory without reconstructing its microscopic environment, at a substantially worse calibration accuracy rate. The strongest equally informed conventional learner can use the SAME port and algorithm. No generic model-membership test, unknown-code learner or fault-tolerance threshold is established.
