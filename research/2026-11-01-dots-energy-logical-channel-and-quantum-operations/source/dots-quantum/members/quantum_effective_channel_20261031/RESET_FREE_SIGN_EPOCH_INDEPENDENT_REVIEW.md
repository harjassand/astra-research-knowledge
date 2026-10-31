# Independent review: reset-free private-sign epochs

Verdict: scoped mathematical PASS, with the operational independence condition below binding. This is a logical-output composition theorem, not a retained-bath approximation, a new randomization primitive, or a practical advantage claim.

Fully read source: RESET_FREE_SIGN_EPOCH_COMPILER_CANDIDATE.md, SHA-256 599de683a90e919d354f5735bbad029daace60370faa76a4ab2e994a0a9980a2. Review date: 2026-10-31. Dependency: the separately accepted private-sign-pair theorem and its complete, uniform-input estimate.

## Actual-state induction

At epoch k use the one-epoch bound on the actual joint source/system/reference/history input rho_k. It compares the actual outgoing logical marginal to E_eff,k applied to the actual incoming logical marginal. Contractivity then compares that latter marginal to the ideal preceding logical marginal. The triangle inequality adds only delta_k. This induction never chooses a replacement bath state and never needs the full bath output to be close to any ideal bath.

Retained user records and arbitrary initial source-system-reference correlations are permitted by the complete one-epoch estimate. A system-only instrument at an epoch boundary contracts the marginal error, and its outcome may correlate the actual bath with retained records. The next uniform-input theorem covers that actual correlation. There is consequently no instrument commutator term when all such instruments are placed at epoch boundaries. Actual implementation errors still require their own summed complete-error budget.

The new bit must be independently sampled from the entire current source/system/controller/history state. An earlier private bit may remain correlated with the bath and may be retained as an inert reference or discarded. It must, however, cease controlling subsequent hardware: neither its hidden status nor its absence from user records permits an old sign to influence the next source generator, interaction setting or control policy. The new epoch must implement exactly the admitted same-G, same-H0 positive mixture of +/-K with a fresh sign. This condition is explicit in the parent's task and binds the source's phrase 'each piece receives a new private sign.' No assertion is made for a persistent or correlated sign controller.

## Schedule and constants

For b>0, C1>=16b^3 ell^2 implies C1>0. The epoch threshold tau0=b ell/C1 is therefore positive. Supplied certified bounds can be used consistently; a finite rational implementation must use a length no larger than its certified threshold and account for its actual resulting epoch count. Exact irrational arithmetic is not granted.

Splitting each positive-duration interval between prescribed controls into pieces of length at most tau0 gives N<=p+1+T/tau0. Zero-duration intervals require no epoch. With equal subdivision of each interval, no accumulated time-rounding assumption is needed for the mathematical schedule; finite clock/control errors remain paid separately.

The control-free single-epoch bound expands to

    A(tau)=12b^2 ell^2+tau(C2+6b ell C1)+tau^2 C1^2,
    B(tau)=tau C1(8b^2 ell^2+tau C2).

Using sum tau=T and sum tau^2<=tau0 T, the constant endpoint contribution is bounded by 12b^2 ell^2(p+1)+12b ell C1 T. Adding the direct linear contribution 6b ell C1 T and quadratic contribution b ell C1 T produces exactly the displayed coefficient 19b ell C1 T. Similarly the second sum is T[8b^2 ell^2 C1+b ell C2]. Thus the stated complete logical error bound, capped at 2, is valid. The proposed sufficient rate makes each inverse-rate contribution at most epsilon_model/2.

The endpoint price grows with epochs; it has not been silently removed by fresh randomization. The resulting bound is linear in T and the prescribed control count for fixed source/task constants. It is a sufficient upper bound, not a lower bound on necessary rate. Choosing a more conservative rational epoch cap changes the explicit count constant unless all theorem parameters and the threshold are chosen consistently; this does not affect the qualitative result.

## Degeneracies, access and comparison

For b=0 the interaction vanishes and system-only evolution is exact; the ratio tau0 is not evaluated. For T=0 only the prescribed zero-time controls act and the model error is zero. Displayed inverse-lambda estimates are for lambda>0; lambda=0 retains the trivial distance-2 comparison if needed.

Each physical branch runs for the actual original duration; the source is not reset, paused or projected. Sign generation, actual +/-K acquisition with unchanged G and H0, switching/frame gates, private-controller handling, clocks, calibration and synthesis are paid. A symbolic minus sign or block encoding is not analog sign-control access. The frequency is independent of lambda only with fixed certified task/source constants and an actually available sign-setting interface.

The target is the effective logical system channel with reference and system-only records, not source output or exposed sign records. Ordinary randomized compiling, antithetic mixtures, frame changes and direct effective-channel implementations remain required comparators. The theorem alone establishes no useful experimental or computational separation; the simple GAD example still has a cheap ordinary ancilla implementation.
