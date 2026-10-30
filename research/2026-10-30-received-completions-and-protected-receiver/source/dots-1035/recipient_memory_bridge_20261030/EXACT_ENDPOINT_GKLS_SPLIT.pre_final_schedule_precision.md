# Exact endpoint GKLS split: no old clock-record inference
2026-10-30. Governing V2 simplification. V1 and all earlier freezes are preserved. This note replaces V1's endpoint positive old-attempt/fault-count bookkeeping; it does not change the long-wait source theorem.

## 1. Individually removable physical bundles
In the accepted ATOMIC apparatus, each actual independent attempted operation is a specified bounded-body CPTP map Phi with generator ell(Phi-Id). This is a complete GKLS jump bundle, including its loss term, not an isolated gain. Its adjoint annihilates identity and its joint cb norm is <=2ell.

Choose the ENTIRE Alice worker attempt map at rate ell. If the worker's current state requests READ this bundle performs the atomic stabilizer measurement and reply; on SYNC or disabled states it performs the corresponding classical action or identity. Slowing the entire bundle avoids any assumption that a fast general worker somehow suppresses only its quantum branch. Choose the Bob current-read/correct commit attempt bundle at rate ell as well. All its conditional classical branches are part of the SAME CPTP Phi. These are precisely the old bundles that can touch DATA. Other queue-hop, watchdog, purge and auxiliary maps remain at their declared fixed rates.

During the finite endpoint define L0 by REMOVING both whole kinds of bundles, including -ell Id, from the physical generator. Their independent jump generators are legitimate summands, so the remainder is still CPTP. The retained old dynamics now act on old auxiliary registers only. They may stall because a slow worker was omitted from this analytical nominal process; no endpoint service or delivery is requested from them. Fresh raw-mask carriers are a separate actual finite apparatus.

The physical old machine is NEVER actually paused by this analytical split. Its complete removed generators are added to the perturbation

    M_old=sum_h ell_h (Phi_h-Id),
    max_site sum_(h incident) ||M_h||cb <= 2 C_old ell.

No guarded attempt is declared to have occurred or not occurred in the real evolution for this endpoint proof. There is no need to preserve old positive jump records under coherent or dissipative calibration perturbations.

## 2. Complete finite-stage split
The rest of L0 is exactly the actual declared nominal endpoint: DATA-independent boots and old auxiliary dynamics, the finite column Bell Hamiltonian pulse, actual pointer measurements and measured COPY carriers, the finite latch-controlled Pauli pulse, source/new-native first-initiation-OFF ramps, and retained bath-only nominal CPTP dynamics. Each stage is CP on every interval. Removing first Hamiltonian edge-plus-adjoint bundles is also legitimate. No dissipator is inverted and no non-CP remainder is used as the base propagator.

Put into M(t): the complete old DATA bundles, the weak source/new first-edge Hamiltonians, and all bounded local endpoint noise/control/calibration terms. Identity-annihilating local centering, when necessary, retains support and pays its explicit factor-two norm constant. The full actual joint evolution remains CPTP by the physical assumption; the summands of M need not individually be CP.

With fixed endpoint duration T_end and actual physical support incidence,

    integral ||M(t)||cb dt <= N zeta,
    zeta <= C[ell T_end+eta_endpoint T_end
                 +epsilon_Q Delta_access+epsilon_new Delta_on].       (2.1)

The endpoint may therefore use the normal bounded local continuous-noise class. The pre-endpoint atomic Bell waiting/source still uses its separately declared exogenous Poisson-CPTP fault model; nothing here upgrades that long-duration theorem.

Forward variation of constants about L0 gives order-r norm <=(N zeta)^r/r!. For any fixed rho>0,

    ||tail_(r>=rho N)||cb
       <= exp(N zeta)[e zeta/rho]^(rho N).                           (2.2)

Choose zeta/rho sufficiently small for exponential decay. Finite stage-boundary auxiliary compressions are CP/TNI and do not increase this bound. Source/resource comparison errors are first passed through the ACTUAL CPTP endpoint and are never multiplied by the norm of a signed truncation.

## 3. Support, including old controllers and shared bath
Every retained insertion is a bounded normal local HP map on finite SYSTEM legs and the same external bath. Expand only those finite legs as a support observation, after the norm tail has been bounded. One old generator insertion may contain a sum of measurement/correction Kraus terms and both ket/bra actions; all are on its fixed physical footprint. No sum of absolute Kraus/Pauli coefficients is estimated.

Between insertions, old auxiliary transport cannot create DATA action: every old READ or commit would require a subsequent insertion of one of the removed whole bundles. It may carry arbitrary stale correlations, but those remain coefficients until a bounded-footprint DATA map is inserted. Fresh raw-carrier propagation stays inside its fixed matched column; new native first-OFF dynamics can activate no owner outside the existing ready-mask support. Thus every coefficient's exceptional DATA support is bounded by

    incoming canonical support + boot/busy/unfinished footprints + q_endpoint r.

This is precisely the existing support module; replace V1's separate rho_old+rho_fault+rho_D by the single retained-order density rho. Coherent masks and common bath coefficients are not pinched. There is no stochastic-Pauli assumption.

The carrier waiting moment remains valid under the actual complete perturbation: old DATA bundles themselves annihilate every WAIT test, while generic terms touching physical pointer/carrier registers enter its same local norm bound. Preparation/truth still require actual reset-to-WAIT and charged support; a no-WAIT effect alone is not a truth certificate.

## 4. Positive warm entry and long overlap are unchanged
The low-order map is signed and has the joint signed-Bell/common ordinary-code module. The actual positive auxiliary/basin compressions and positive ancillary replacement in FINITE_NATIVE_ACTIVATION_AND_WARM_CHANNEL_V2.md turn it into an earned P_small-supported logical-identity warm input, paying the norm and gentle errors. This is the only place the new long-time theorem is restarted; no conditional rare Bell branch or arbitrary dirty state is supplied to it.

After the actual new native generator is fully on, the same complete old bundles are ordinary bounded local perturbations of strength <=2 C_old ell. Their finite physical rate ramp to zero is covered by the new native theorem. All old auxiliary-only dynamics remain spectators, with every cross-system fault still charged in the common incident model.

The rate order is noncircular: select new native hardware/warm margins and the fixed weak-edge ramp durations; select all finite boot/carrier/pulse durations; select ell>0 so both ell T_end and 2 C_old ell satisfy the respective endpoint/native margins; recompute old Bell service at these positive rates; select long-wait external Poisson noise below its resulting threshold and the new threshold; select endpoint control/noise below (2.1) and the carrier/boot moment thresholds. The old service time may be huge; it is not the fixed endpoint latency and is not inserted into ell T_end.
