# From uniformly learned subsystem extraction to complete-memory CP domination

2026-10-28. Root candidate; independent review pending. This is a separate stronger composition principle, not an amendment to the exact isolated-output factorization. It imports a state-uniform extraction certificate, not merely an average or Bell score on a sampled gauge state.

## 1. Interface

Let L have dimension D=2^q and G be the emitted gauge. A native use has the complete CP form

    E(rho_LM)=Ad_(U tensor I_M') sum_alpha (Ad_Palpha tensor G_alpha)(rho_LM),

where G_alpha:M->G M' are CP and sum_alpha Tr_G G_alpha is TP. The source may change with time and exposed classical history. The physical output P=U(L G) goes to the receiver; the source retains only M'. The emitted gauge and receiver ancillas are ultimately discarded and are NOT later returned to source access. Let Dhat:P->L be a fixed CPTP receiver with no externally retained decoder measurement record. The true extraction is D*=Tr_G Ad_Udagger.

Assume a certificate

    F_e(Dhat Ad_U( . tensor sigma_G)) >=1-b

for EVERY density sigma_G, with one b in [0,1]. No lower bound on eigenvalues of actual future gauge states is required. The earlier exact/approximate on-site constructions provide such a certificate on a calibration good-record event; this lemma is independent of how it was acquired.

Use a fresh uniform q-qubit Pauli Q on the logical input and Qdagger on the recovered output. Q is independent of the entire current apparatus and source state and has no direct leakage through the complete source port; source maps do not depend on Q. Applied-frame records are retired privately. Output data may later be used by a common external controller. Neither a protected calibration reference nor a source reset is introduced by this step.

## 2. Pauli-resolved gauge effects, with all normalizations

Let A_l:L G->L be Kraus operators of Dhat Ad_U. Expand uniquely

    A_l = sum_gamma P_gamma tensor <v_lgamma|,
    <v_lgamma| = D^(-1) Tr_L[(P_gamma^dagger tensor I) A_l].

Here the partial trace expression denotes the corresponding logical matrix-block contraction, leaving a row on G. Define

    T_gamma=sum_l |v_lgamma><v_lgamma| >=0.

Taking normalized logical trace of sum_l A_l^dagger A_l=I_LG gives sum_gamma T_gamma=I_G. Feeding a logical Bell pair and gauge sigma yields

    F_e(Dhat Ad_U(. tensor sigma))=Tr(T_0 sigma).

Therefore the uniform hypothesis is EXACTLY T_0 >= (1-b) I_G. This is an operator inequality on the emitted gauge, not a scalar estimate for its occupied state.

For a positive effect T on G define the completely positive contraction

    C_T(X_GM')=Tr_G[(sqrt(T) tensor I) X (sqrt(T) tensor I)].

Equivalently C_T(X)=Tr_G[(T tensor I)X]. The latter expression need not be manifestly positive termwise but equals the sandwich after partial trace. The map T->C_T is linear, and T>=cI implies C_T>=_CP c Tr_G.

Pauli character orthogonality removes cross gamma terms under the private frame average. Since P_alpha Q differs from Q P_alpha only by an irrelevant phase, the ACTUAL framed recovered complete map is

    E_framed = sum_(alpha,gamma)
       Ad_(P_gamma P_alpha) tensor (C_Tgamma composed G_alpha). (1)

The equality acts on arbitrary logical-memory-reference correlations. It is not a model obtained by fitting a classical trajectory.

## 3. Complete CP domination, not just Bell-success domination

All summands of (1) are CP. Keeping gamma=0 and using T_0 >=(1-b)I gives

    E_framed >=_CP (1-b) E_exact,
    E_exact=sum_alpha Ad_Palpha tensor (Tr_G composed G_alpha). (2)

Both maps are TP on L M. For 0<b<=1 the difference divided by b is consequently CPTP:

    E_framed=(1-b) E_exact+b F,                         (3)

for a generally source-dependent complete-memory channel F. At b=0 the maps are equal. This is a virtual convex decomposition; there is no accessible 'clean' flag or herald, and F can contain arbitrary coherent retained-memory correlations.

An arbitrary small failure EFFECT elsewhere does not automatically imply (2). Here the clean logical-Pauli branch acts on the emitted gauge only through a scalar effect, and that gauge is completely traced. This specific interface makes C_T0-(1-b)Tr_G CP. If decoder records or the emitted gauge are retained and exposed, the effect alone does not control their state-update instrument, and the asserted comparison is not licensed. This distinction is material, not bookkeeping.

Global CP identity dominance G_I>=G_alpha is NOT used in (2). The exact-extraction benchmark may have large native logical noise. Service-time positive X/Z contrast is likewise unnecessary once the uniform extraction certificate has been acquired: future G_alpha can be arbitrary CP maps obeying TP and the declared Pauli/gauge source form. A persistent approximate algebra bound is still required if U changes.

## 4. Adaptive repeated service and counterfactual memory handled correctly

Take a fixed finite number T of slots. At every slot and every possible exposed history require the same certificate b for the actual selected nominal receiver and source U, and the complete interface above. Interleave ANY common CPTP controller, including coherent processing/reuse of prior logical outputs, references, measurements and classical feedback. The controller must preserve current frame privacy and the promised source class. It must not access retired frame records or discarded emitted gauge. An arbitrary controller is allowed only insofar as those physical contracts remain true.

Apply (3) at every slot, including each classical-history-controlled block. Expanding the finite composition into CP branches gives an all-clean branch of weight (1-b)^T EXACTLY equal to the whole process with true extraction at every slot and the SAME initial source memory/controller. All other branches form a CPTP residual after normalization. Consequently, for the complete accessible final channel or interactive process,

    E_learned,process=(1-b)^T E_exact,process
                         +[1-(1-b)^T] F_process,
    half diamond/operational strategy distance <=1-(1-b)^T<=Tb. (4)

The strategy statement means every permitted common tester/controller has distinguishing advantage at most this bound; it is not an unqualified norm comparison on an arbitrary leaked-key extension. For varying known b_t, replace (1-b)^T by product_t(1-b_t).

No source-memory reset or output isolation is needed for this bound. Earlier exact output-noise factorization fails with output feedback; this more general CP-mixture proof does not move errors through that feedback. In error branches the memory can differ arbitrarily from the ideal trajectory. In the all-clean branch it is exactly the ideal trajectory, which is why the reference-process comparison is justified rather than inferred from same-occupation regret.

For an induced payload-only diamond comparison the initial joint payload/reference is product with the source conditional on calibration record. Alternatively (1)--(4) are complete linear identities on the enlarged logical-plus-memory input, including arbitrary initial correlations. The exact benchmark is true per-slot extraction, NOT automatically a collective full-CPTP optimal receiver or a noiseless computation.

## 5. Acquired on-site specialization and costs

The received exact on-site fit certifies b<=9 epsilon_train/32 on a record event of probability >=1-beta. The approximate on-site construction (separate version-bound receipt required) certifies

    b <= min(1,(3 sqrt(q/2) tau+sqrt(epsilon_train)/3)^2).

Use epsilon_train=epsilon/T, beta<=epsilon/8, and complete calibration-record TV debit nu_cal plus whole-T-service implementation debit nu_svc<=epsilon/4 jointly. Good-record probability is at least1-beta-nu_cal. Uniformity over all emitted gauge states transfers this certificate to physically actual post-calibration memory. Combining (4), the simple squared-sum bound, and one bad-event debit gives

    actual mean process distance to exact-extraction process
       <= min(1,9 T q tau^2+epsilon).                 (5)

In the exact case tau=0, use the sharper exact certificate, obtaining <=21epsilon/32 under the stated budget. For the approximate case the finite fine-bank cap is ceil[65536 q T ceil(log2(24q/beta))/(kappa^2 epsilon)] and the coarse bank is unchanged. These are supplied calibration contrasts, not future lower noise bounds. Every block prepares q logical probes and reads n physical outputs.

Service requires 2q fresh frame bits and q fitted one-qubit inverses per slot in the on-site specialization, with all routing, actual feedback, holding, resets and frame retirement included. A sufficient complete-register per-slot error nu_svc/T gives the whole-service debit by an ordinary hybrid. Fresh finite-bounded randomness generation, its failure probability and preparation/readout calibration remain paid as in the received sources. No source parameter or classical 'clean' flag is revealed by the convex proof.

This result is a certificate-to-architecture transfer: an acquired state-uniform subsystem receiver can be reused in an adaptive quantum process without rebuilding the environment model. It is NOT a threshold theorem. The exact-extraction source can still have highly correlated or large Pauli errors. Operator-norm proximity of generators does not by itself imply a local-stochastic distribution across many logical qubits. Generic redundant-code acquisition and physical validation of the complete interfaces remain separate obligations.
