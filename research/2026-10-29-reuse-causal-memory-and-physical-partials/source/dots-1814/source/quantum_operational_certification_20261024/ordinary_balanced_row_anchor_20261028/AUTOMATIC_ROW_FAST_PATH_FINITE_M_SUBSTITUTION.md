# Finite-M substitution for the received automatic row fast path

28 October 2026. Short composition candidate. This applies the already received private-framed multi-payload wrapper to the now received automatic local learner. It does not add a new acquisition primitive or change the communication rate/comparator.

## Frozen governing versions

- Local learner: `AUTOMATIC_VALIDATED_ROW_FAST_PATH.md`, SHA `69b012d669b6e8a32a587b804768acf2bc3155906ea2598727275c357a89fd05`.
- Its independent receipt: `automatic_row_fast_path_independent_receipt.json`, SHA `52388d7dc9184fe4fa26a5ebb7971992f655abb772c00a14912940ac63309044`.
- Required resource-event clarification: `FAST_PATH_RESOURCE_EVENT_IMPLEMENTATION_CLARIFICATION.md`, SHA `cea657a43f9b6fac5a9567a285de21676e523b0cb54b1b2f768332896f74d3b0`.
- General received wrapper: `../ordinary_generic_matrix_gls_multipayload_relative_20261028.md`, SHA `cee0f8d6755f6a50ed8e21e7aea94da42703e1ffca4d5ef38e4f427df693c518`, with its root receipt.
- Governing original private-framed optimum: `../direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md`, SHA `718c8658211d88a135ff8aea28be652bed14dc16e025f518ca0e4c4b35db9708`.

All source, ordinary-input, known-physical-basis, stationary-reset, fresh-bank and full-CPTP conventions are unchanged. A generic random receiver frame is not used to infer the row promise. The local learner is sound without that promise by its paid generic fallback.

## Parameter substitution and shared-history risk

For integer M>=1 and 0<gamma,epsilon<=1, calibrate entirely before any unknown payload at

    gamma_local=gamma/2, epsilon_local=epsilon/(4M).

Equation (3) of the local learner then gives its IDEAL calibration output

    E ell_h<=(1+gamma/4)ell_star+17epsilon/(16384M).   (1)

The same calibrated encoder and actual full-CPTP decoder are used on each of the M payloads, with fresh local ancillas and independent private Pauli frames. A classical finite circuit description is retained, not an unknown quantum program copied for free. The known basis persists throughout.

Let a_*=1-ell_star, f_h=1-ell_h. For every ideal training history, f_h<=a_* because the returned policy is physical and belongs to the same family. Conditional on that frozen history the stationary reset source gives the ideal product service law, so the global identity weight is f_h^M. After averaging it is E[f_h^M], NOT (E f_h)^M. The received comparator theorem gives optimum identity weight a_*^M even for its permitted original collective recovery and predetermined encoder lists.

For 0<=f<=a<=1,

    a^M-f^M<=M a^(M-1)(a-f),
    M a^(M-1)(1-a)<=1-a^M.

Apply these inequalities before averaging, then use (1). With g_M(t)=1-(1-t)^M,

    E g_M(ell_h)<=(1+gamma/4)g_M(ell_star)
                                +17epsilon/16384.   (2)

Private framing makes the IDEAL averaged service's unhalved complete error equal to twice this loss. Thus if Delta_*M=2g_M(ell_star),

    Delta_ideal<=(1+gamma/4)Delta_*M+17epsilon/8192.

One separately budgeted WHOLE-H implementation discrepancy at most epsilon/2, where H=N_cal+M, yields the actual guarantee

    Delta_actual<=min{2,(1+gamma)Delta_*M+epsilon}.    (3)

The original one-payload implementation allowance is NOT applied M times. Preparations, finite record sampling, all calibration operations, optimization, M actual decoder uses and private frames are compiled against the new single horizon. The actual implemented channel need not literally have the ideal Pauli/product law; the whole-process comparison transfers it once.

## Source caps and the actual fast-path event

The deterministic generic source cap becomes

    O_tilde(k^4 M/(gamma epsilon))+M.                (4)

On the exact rank-one row subclass, with unknown intrinsic balance kappa_*, the actual number of source calls is, with the received high probability,

    O_tilde((d+dr) M/(kappa_* gamma epsilon))+M.      (5)

The constant factor eight from gamma_local epsilon_local=gamma epsilon/(8M) changes no order. The geometric schedule and the state bank are run only once during calibration. Failed fast-path histories still obey the declared generic cap.

For a direct actual-event bound, retain the module's stricter predecision allowance

    nu_pre<=epsilon_local/1024=epsilon/(4096M)

inside the overall epsilon/2. The received actual fast-completion failure probability is then less than epsilon_local/256=epsilon/(1024M). This controls the actual resource event, not only the ideal branch probability. It is not an additional error allowance outside (3).

The comparator keeps one physical source use per logical payload in the declared fixed encoder family and the same private-frame contract. New joint encoders, changed coding rate, source-generated protected references, public training/Pauli records, or a conditional-on-acceptance guarantee are not introduced. The equally informed conventional learner has the same route. Equations (4)-(5) do not claim practical runtime or a universal k^2 dimension rate.
