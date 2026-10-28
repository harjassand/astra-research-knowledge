# A common clean subchannel suffices when memory keeps the error record

28 October 2026. Root candidate, independent receiving pending. This preserves a distinction that matters to the learned identity-module architecture: a uniform bad EFFECT does not generally give CP domination by a fixed ideal continuing-memory channel. Nevertheless a common-clean-subchannel argument gives the finite complete-process error bound without requiring the source to forget its actual errors.

## 1. Complete Pauli-memory interface

At each allowed slot/history the complete module is

    R=sum_beta Ad_Pbeta tensor F_beta,
    F_beta CP,    T=sum_beta F_beta TP.                 (1)

Logical Pauli identity is beta=0. Memory can be coherent, correlated with caller/reference, and may retain an orthogonal record of beta. Accessible classical native/decoder outcomes can be included as explicit output blocks if their full instruments, not merely outcome probabilities, are represented in (1). Native labels and controller feedback are classical where stated; the controller may otherwise be arbitrary causal CPTP processing.

The actual complete form (1) must be supplied or constructed. If obtained from private Pauli frames, their keys are retired before any later controller/source use. A state-averaged logical Pauli fit or current-output Bell score alone does not establish (1). No normalized postselection is assumed.

Suppose the uniform bad-effect bound holds:

    sum_(beta!=0) F_beta^*(I) <= eta I_M,
    F_0^*(I)>=(1-eta)I_M,  0<=eta<=1.                 (2)

It is a bound at EVERY allowed history and conditional memory state, not an empirical average over calibration occupation. It can hold even when no nonzero multiple of T is CP-dominated by F_0.

Define the comparison module

    R_id=id_L tensor T.                               (3)

This replaces logical Pauli errors by identity while retaining their actual total memory/record evolution. It is not a perfect or reset environment.

## 2. What fails: the stronger CP-mixture inference

Let a qubit experience an I or X error with probabilities 1-p,p, and let output memory record the actual error in orthogonal states |0>,|1>. The complete maps are

    R(rho)=(1-p)rho tensor |0><0|+p XrhoX tensor |1><1|,
    R_id(rho)=rho tensor[(1-p)|0><0|+p|1><1|].

The bad effect is exactly pI. Yet R-(1-p)R_id is NOT CP: on the normalized Bell input, its expectation in |Phi+> tensor |1> is -p(1-p). For p=1/4 this is -3/16. Thus neither a state-uniform error probability nor conditional iid logical error sampling licenses the full CP inequality unless the retained memory update is also qualified.

In the narrower scalar-mixture model F_f=sum_a w_f(p_a)K_a, the SAME K_a output is used for each sampled physical pattern f, with no extra retained which-pattern tag. There the good/bad scalar coefficients can prove the stronger CP mixture used by ordinary_learned_repetition_identity_module_20261028.md. If a physical sampler records f in continuing memory, that stronger interface changes. The present theorem covers such records by (2), without pretending the stronger inequality survives.

## 3. Common all-clean branch and full adaptive comparison

For one slot set G=id_L tensor F_0. Both R-G and R_id-G are CP. Their trace effects coincide and are bounded by eta I, so

    half ||R-R_id||_diamond <=eta.

For J slots interleaved with the SAME arbitrary permitted causal controller, define the complete all-clean CP map G_all by selecting the beta=0 branch at EVERY slot and retaining the controller's actual classical records unnormalized. Classical history-dependent choices of native source maps are included as controlled CP maps. The complete real process Phi and comparison process Phi_id both contain EXACTLY this same CP subchannel: every selected logical operation is identity, every selected memory/record map is the same F_0, and every controller operation is unchanged.

Since each selected branch obeys (2), backwards positivity and TP controller adjoints give

    G_all^*(I)>=(1-eta)^J I.                           (4)

Equivalently each additional all-clean step retains at least1-eta of the mass of every previous positive branch; this argument holds on full correlated inputs and not only on scalar observed trajectories.

Consequently B=Phi-G_all and B_id=Phi_id-G_all are CP, with the SAME trace effect

    B^*(I)=B_id^*(I)=I-G_all^*(I)
                          <=[1-(1-eta)^J]I.

A CP map has diamond norm ||B^*(I)||op. Triangle inequality therefore proves

    half ||Phi-Phi_id||_diamond <=1-(1-eta)^J<=J eta.   (5)

For fixed per-slot bounds eta_j, replace the power by product_j(1-eta_j). Stopping before a finite cap is handled by common identity padding. This also bounds every permitted operational tester's distinguishing advantage. Actual and ideal memory can diverge in bad branches; the proof does not replace one policy's memory occupation by another. It compares two full processes sharing the all-clean subchannel.

Unlike CP domination, (5) does NOT assert Phi=(1-eta)^J Phi_id+[1-(1-eta)^J]F with F CPTP. G_all need not be a constant multiple of Phi_id. The recorded-error example disproves that stronger assertion already at one slot. Do not use (5) as permission to inherit a physical 'clean flag' or a constant-weight ideal memory trajectory.

For independent recorded errors on distinct payloads, product Bell inputs attain half trace distance1-(1-p)^J: every nonzero error string has an orthogonal Bell state with its retained record. Thus the finite envelope can be sharp even when the stronger CP-domination interpretation fails completely.

## 4. Learned extraction plus a native bad-effect certificate

Suppose the native encoded source has Pauli/gauge blocks G_alpha:M->G M', and exact extraction produces F_alpha=Tr_G composed G_alpha. Let

    sum_(alpha!=0) F_alpha^*(I)<=r I.                  (6)

A learned receiver, privately framed as in the received complete-CP-domination source, has gauge effects T_gamma>=0, sum_gamma T_gamma=I_G and T_0>=(1-b)I_G. Its complete logical Pauli-memory maps are

    Fhat_beta=sum_(gamma alpha=beta up to phase)
                           C_Tgamma composed G_alpha.

They sum to the SAME total memory map T=sum_alpha Tr_G G_alpha. In particular

    Fhat_0^*(I)>=G_0^*(T_0 tensor I_M')
               >=(1-b)G_0^*(I_G tensor I_M')
               >=(1-b)(1-r)I_M.

Therefore the actual learned module satisfies (2) with

    eta=b+r-br.                                      (7)

This step needs only the native bad EFFECT (6), not F_0>=_CP(1-r)T. The complete learned source Pauli representation and the all-gauge extraction bound are still essential; fitted probabilities alone do not supply them.

A MORE GENERAL known-code application does not assume that an arbitrary CPTP decoder produces a logical Pauli instrument. Let physical native noise be sum_f Ad_Pf tensor F_f, let Enc be the known encoder, and let Dec be any known CPTP decoder correcting a declared set Good EXACTLY: Dec Ad_Pf Enc=id_L for every f in Good. Put T_good=sum_(f in Good)F_f and T=sum_f F_f, with (T-T_good)^*(I)<=rI. Suppose the learned PHYSICAL inverse has the separately proved complete CP domination by (1-b) times the exact physical-noise channel. Composing Enc and Dec preserves that inequality. The resulting learned module and the reference id_L tensor T then share the CP subchannel

    G=(1-b)(id_L tensor T_good),
    G^*(I)>=(1-b)(1-r)I.

The proof in section 3 uses only a common CP subchannel with this trace-effect lower bound; apply it with eta=b+r-br. No logical Pauli decomposition of the bad decoded branches, extra logical twirl, or constant ideal-memory mixture is needed. The actual known code, physical inverse certificate and full complete-interface conditions remain essential.

For example, three sequential bit-flip locations with a uniform complete conditional error-effect bound p_max at each location have probability of every specified pair of faults <=p_max^2, by backwards positivity. The union of the three pair events gives r<=3p_max^2 for majority decoding, without requiring the environment to discard the fault record or independent errors within the block. Exact iid scalar-mixture sources can use the sharper3p_max^2−2p_max^3 where its premises hold.

This is not an acquisition theorem for (6). Uniform error-effect/local-fault promises must be physically justified or independently certified. Nor does it automatically certify the positive calibration contrasts required by a particular learner. In a full physical-register port with trivial emitted gauge, weaker scalar bias-effect bounds can sometimes suffice for learning fixed conjugated physical Pauli generators; that is a separate construction.

## 5. Records, acceptance and resources

On a learned good-record event, use a fixed accepted target b (or explicitly average record-dependent bounds). Compare protocols with the SAME actual calibration/acceptance record law and the same abort branch. Bad-certificate probability, calibration-record discrepancy and whole-service implementation error are paid once in addition to (5). Conditional-on-acceptance guarantees retain their denominator; forced service after abstention needs a separate abort/fallback mass. Full payload/reference product with source memory is required for a payload-only induced channel; the abstract map inequality can instead retain the complete joint input.

All encoders, source calls, physical traffic, learned receiver/reflection gates, ancillas, private frames, gauge/record disposal and actual holding/control errors retain their previously declared cost. If per-module control errors are order p_max, the nominal quadratic native correction does not become a quadratic PHYSICAL guarantee. This theorem is neither a full hardware fault-tolerance threshold nor a generic unknown-noise discovery algorithm.

Astra N1004 already establishes positive task effects and specified-fault-set/binomial bounds under its complete port assumptions. The present proof makes the common-subchannel distinction explicit for a PARTICULAR identity-logical/total-memory comparison and arbitrary common feedback. No invention of Pauli twirling, fault envelopes, or broad historical novelty is claimed. It must not silently expand older source scopes or erase their physical-interface qualifications.
