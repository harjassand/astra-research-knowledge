# Reset-free sign epochs: linear-time logical error candidate

Status: root construction, unreviewed. Depends on the accepted private-sign-pair theorem, not a claim of new randomization or a new cooling operation. The target remains the effective logical system channel, with arbitrary reference and system-only control records, NOT a retained source process.

## Interface and schedule

Retain the sign-pair physical interface: actual +/-K settings with identical G and H0, or an exactly equivalent paid system conjugation; one fresh fair private bit per epoch, independent of the entire current source/system/history state. The bit is not exposed or used by the logical control policy. Old bath and private-controller correlations may remain; there is no bath reset between epochs. Previously correlated sign bits cannot simply be reused as fresh ones. Every old private sign/controller register must cease controlling subsequent hardware after its epoch; merely hiding an old bit from the user is insufficient. Any retained private registers are then traced or idle, so their correlations cannot condition later source dynamics or sign settings.

Assume fixed b>0, ell>0 and C1,C2 from the generic reduction. Set a known rational-safe epoch length

    tau0=b ell/C1.

Choose certified rational bounds for b, ell, d and derive C1,C2 consistently from those same bounds; the displayed ratio is then exact rational. If an implementation instead chooses a smaller epoch cap, it must charge its actual N (or redo the ceiling bound) rather than reuse the displayed constant19 for free. Since C1>=16b^3 ell^2, C1>0. If b=0 there is no interaction and the logical evolution is already exact; do not evaluate this ratio.

Place epoch boundaries at every prescribed user-control time. Within each positive-duration interval split into equal pieces of length at most tau0. Each piece receives a new private sign. Zero-duration intervals are skipped. If p controls occur over physical time T>0, the number N of nonzero epochs satisfies

    N<=p+1+T/tau0.

This is a conservative real upper bound on the integer sum of ceilings. Bit generation, sign setting, any conjugation gates, storage/erasure, clock scheduling and their errors are paid. In particular the epoch frequency does not scale with lambda. The source is continuously present; its dissipator is neither paused nor replaced.

## Why the logical bounds compose without a source reset

For any actual joint input rho_k at an epoch boundary, including arbitrary correlations with retained prior records/reference, the accepted one-epoch theorem states

    ||Tr_source F_k(rho_k)-E_eff,k(Tr_source rho_k)||_1<=delta_k.

This holds uniformly, not only for a prepared source or a source independent of the logical system. Apply it to the ACTUAL rho_k, then compare its system marginal with the ideal previous marginal by contractivity of E_eff,k. Induction gives total marginal error <=sum delta_k. It does not construct a fictitious replacement source state or claim closeness of the full bath output.

An exact system-only user instrument at an epoch boundary is a contraction on the retained system/reference/record state, so it adds no model error. Its actual implementation errors are separate. The next actual source state can be arbitrarily correlated with its outcome and is again covered. No coupling-commutator calibration of the instrument is necessary in this boundary version; the price is additional epochs. Alternatively, previously admitted commuting controls can remain inside epochs and use the original commutator-sensitive theorem.

## Explicit linear-time bound

For a control-free epoch of length tau, substitute f1=2b ell and f2=4b^2 ell^2 into the accepted sign-pair bound:

    delta_epoch<=A(tau)/lambda+B(tau)/lambda^(3/2),
    A(tau)=12b^2 ell^2+tau(C2+6b ell C1)+tau^2 C1^2,
    B(tau)=tau C1(8b^2 ell^2+tau C2).

Each delta may be capped at2. Since sum tau=T, sum tau^2<=tau0 T and N<=p+1+T/tau0, total logical error is at most2 and at most

    [12b^2 ell^2(p+1)+T(C2+19b ell C1)]/lambda
     +T[8b^2 ell^2 C1+b ell C2]/lambda^(3/2).

This is linear in logical duration and prescribed control count. It is uniform over arbitrary initial quantum source correlations. For target model error epsilon_model, a sufficient positive rate is

    lambda>=max(2 A_total/epsilon_model,
                (2 B_total/epsilon_model)^(2/3)),

where A_total and B_total are the two displayed coefficients. This is a sufficient rate, not an optimal lower bound or evidence that an unpaired implementation actually fails at a smaller rate. If T=0 the exact user controls alone have zero model error; no epochs are required.

No global source-history simulation, physical-jump discretization, or rapidly repeated source projection is performed by this protocol. It runs the admitted physical source for the original time T, with N sign choices. It does not certify that any laboratory already supplies the interface. Source construction and calibration, acquired g/h/kappa and b/d, the effective target operation, and all controls remain real costs.

## Strong comparison and unresolved value

This is an explicit microscopic implementation of a familiar randomization objective: prevent coherent finite-rate errors from accumulating. Non-Markovian randomized compiling is an essential informed comparator, not a discarded alternative. A known system involution can sometimes implement the sign operation by ordinary frame changes and boundary gates. In simple cooling/GAD examples a direct small-ancilla channel is already cheaper; those examples do not demonstrate a new useful capability.

The serious remaining question is whether an actually available, costly-to-replace quantum apparatus supplies a consequential target operation for which these reset-free sign epochs reduce the total preparation, calibration, dissipation or correction burden compared with the strongest ordinary construction. No such practical separation is established by this theorem alone.
