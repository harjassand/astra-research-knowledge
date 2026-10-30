# Physical parking: a legitimate finite-horizon lemma, not autonomous composition
2026-10-30. Supplemental construction and rejected shortcut.

## 1. Exact startup obstruction to an atomic generator identity

A clean ready native transaction does not implement lambda(Phi-Id) on DATA at infinitesimal time. Already one coherent clock edge C0<->C1 with payload unitary U and a C1 terminal reset of rate kappa has successful-terminal probability

    p_success(t) = kappa Omega^2 t^3/3 + O(t^4)

from C0 (bounded watchdogs do not change the leading term). The hypothetical atomic update has probability lambda t+O(t^2). With L necessary coherent edges before the first terminal the initial order is at least t^(2L+1); required initial load/commit jumps can further increase it. Thus no exact first-order generator substitution holds at the supplied ready encoding for fixed nonzero lambda. Eliminating the controller by writing an effective Lindbladian is an approximation whose errors require a local threshold theorem, not an identity.

## 2. A genuinely physical one-shot completion latch

For a standalone requested attempt, duplicate the cleanup rail into Q^success and Q^abort. A SUCCESS enters Q^success; its watchdog/verification/cleanup resets preserve that branch bit. Once its tags are all released, READY enters an absorbing DONE state. A clean abort enters Q^abort, clears tags and retries from clean A0. All changes are finite controller alphabet changes, onsite resolved resets and original two-site edges. No branch can reset the success bit and retry the same channel nominally. While DONE is parked there is no DATA drive, no owned tag and zero workspace. Dirty branches still need the full malformed-state handling, and their emissions are faults, not a free clean reset.

From a clean armed input and with no fresh request after DONE, every nominal successful path applies exactly one Phi, regardless of the number of identity aborts. The actual finite-path argument gives a completion tail 1-p(T)<=C exp(-rT). Conditioned on completion, ancillary clock/monitor histories can be retained; the fixed Stinespring instrument of Phi is the same on every path, while the coarse path distribution is DATA-independent. There is no nominal coherent off-diagonal between the absorbed DONE block and the unfinished block, because entry into DONE descends from a resolved terminal jump and no Hamiltonian leaves it.

On a finite isolated patch, with its actual joint CPTP dynamics L_actual=L0+N(t) and ||N(t)||_cb<=eta_patch, ordinary Duhamel using the ACTUAL propagator on one side and nominal on the other gives

    ||E_actual(T)-E_0(T)||_diamond <= eta_patch T.

Hence the requested one-shot gadget differs from the ideal completed Phi instrument, including an appropriate retained nominal completion record, by at most

    2 C exp(-rT) + eta_patch T.                         (2.1)

Completion compression is onto a real physical DONE flag at a deterministic endpoint, so (2.1) does not posit an actual nominal SUCCESS record under calibration. Full noisy regularity and reference stability are assumed. All preparation, arm and finite patch isolation in this lemma are real supplied controls; they are not derived from autonomy.

## 3. Why this is not the required autonomous compiler

A reusable lattice must retire DONE only after an actual neighbor acknowledgment/epoch protocol. If it rearms immediately, the physical endpoint may contain an unknown number of completed updates; if it waits for a supplied synchronized arm, the desired control problem has simply been assumed. Generic perturbations may corrupt DONE/request/ack bits, and overlapping local computations cannot be separately isolated by fiat. A finite marching-soldier protocol might supply the handshake, but its global valid-cut and damaged-clock analysis are exactly the remaining asynchronous proof.

The finite-horizon bound is therefore useful for a real commanded gadget and for designing an eventual local-cut proof. It is not a solution to reusable autonomous scheduling or to inclusive fault-path resummation under broad joint-generator noise. Conventional scheduled fault tolerance already supplies the stronger comparator when such supplied controls are permitted.
