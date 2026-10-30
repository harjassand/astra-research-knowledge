# Actual FREE sector and weak-LOAD activity on the accepted LOCC FSM
2026-10-30. New local operator lemma. The accepted physical alphabet and its I-watchdog are NOT changed.

## Correct predicate

For an owner h define

    FREE_h = 1_{phase in {I,Q_0,...,Q_k}}
             product_(r in R_h) 1_{tag_r not in {o_h,z_h}},
    A_h = I-FREE_h.

Workspace/program/outer registers are unrestricted. This is not the I-only readiness predicate: the actual I->Q0 watchdog would leave I, but it preserves FREE.

## Full table audit

Every Hamiltonian preserves A_h exactly:

- all A/C/B/R phases are active; acquisition, payload, rollback, and their R leaves stay active;
- Q verification stays Q and preserves the absence/presence of own tags;
- a failed-test edge from I or Q can be enabled only when an own o_h/z_h tag is present, so its source is already active; the R leaf is active;
- cleanup o_h<->z_h preserves the predicate that an own tag is present;
- other owners' operations preserve h's own-tag predicates.

Every reset other than LOAD is noncreating:

- I/Q watchdog stays I/Q with unchanged tags; I->Q0 is FREE-preserving;
- C/B/R/A retirement to Q0 can enter FREE only if no own tags remain, otherwise it stays active;
- READY Qk->I preserves the same no-own-tag predicate even on malformed states;
- workspace refresh has no effect;
- z_h->free can only remove activity, and removes it exactly when the phase is I/Q and this was the last own tag;
- all classical messages/master/worker transitions leave engine phase/tags unchanged.

LOAD I->A0 is the only activation. Its guard includes WANT or Alice REQUEST but does not require a perfect ownership certificate. On a FREE I source it creates activity; on an already-active I source with orphan own tags it merely preserves activity. If its rate is lambda_h, the actual source-resolved generator satisfies

    L^* A_h = -D_h + lambda_h P_(FREE,I,load-guard),
    0<=D_h,       L^* A_h <= -D_h + lambda_h I.          (1)

D_h is the sum of actual healing effects; no negative term or gain was dropped in identifying the unique positive source. Complete source resolution keeps all losses explicit.

## Actual return when LOAD=0

Retain the I watchdog. From any phase, take the actual complete-retirement path if needed, then clear each own o_h by cleanup drive and z reset, clearing preexisting z similarly. Q0 with no own tags is already FREE; READY or a halt of the watchdog is unnecessary. This uses at most L+3+2k selected native steps, up to fixed padding, and does not acquire resources or clear neighboring owners.

Finite-rate native monitors and the all-background local norm estimate give a uniform full-Hilbert absorption effect for A_h when LOAD=0, with rates independent of how small the removed LOAD was. Cleanup/retirement/monitor lower bounds remain required. The positive OWN-corner polynomial construction yields

    alpha_A A_h<=Z_h^A<=A_h,
    L_(LOAD=0)^* Z_h^A<=-r_A A_h.                       (2)

No clean workspace or prepared tag premise is used for this controller-return statement. It does not protect DATA from damage before a dirty engine retires.

One may remove only BOB LOAD for this lemma while keeping Alice READ activity strong. Alice operations and all classical messages do not create Bob ACTIVE; its actual return path does not need an Alice reply.

## Weak-load density with continuous noise

Treat restored local LOAD channels of rate <=lambda as bounded local generator perturbations of the zero-LOAD reference (their adjoint norm is bounded by 2lambda), alongside local continuous joint-noise norm eta. Apply the separated-product moment hierarchy in ACTUAL_DEBT_HEALING_AND_CONTINUOUS_MOMENTS.md to the commuting A_h family. At fixed theta and after warm-up it yields

    log <exp(theta sum_h A_h)>
       <= C_theta N [exp(-r_A t)+lambda+eta].            (3)

Thus actual current activity is O(lambda+eta) in the exponential-density sense, with no fiction that I is absorbing. This is a pointwise activity estimate, not proof of useful correction throughput or a continuous-noise memory threshold. If only Bob LOAD is weak, (3) is asserted only for Bob activity.

## Regression

`check_free_sector.py` uses the EXACT accepted I/A/C/B/Q/R transition definitions and checks all 66,825 basis configurations and 449,190 directed transitions. Every Hamiltonian preserves activity, only LOAD creates it (702 such fixture transitions), and all other resets are noncreating. With LOAD removed but I watchdog retained, all states reach one of 16 global FREE configurations; maximum shortest path is 11. Workspace is unrestricted. The finite regression checks the table, not the finite-rate operator probability proof.
