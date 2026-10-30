# Classical QND flush from actual retirement, without quantum data repair

2026-10-30. Candidate completing semantic lemma for the fixed-grid classical adapter only. It is not a flush/rejoin theorem for arbitrary quantum computation.

## 1. Exact architecture choices

For each classical site x:

* X_x is its visible pointer register. The ONLY nominal operation that writes X_x is its onsite COMMIT channel. That channel measure-prepares X_x in its declared basis, with the fresh Rand leaf.
* Observer h=x reads X_(x-1), X_x, X_(x+1) nondestructively and writes only its own persistent snapshot S_x. Its private workspace is distinct from S_x. Every payload, inverse-prefix, failed-test and retirement coefficient commutes with every visible-pointer projector P_(y,a). This is the full-Hilbert read-only compiler property, not merely a clean-input statement.
* No other observer or quantum actuator writes S_x, c_x or its timer. Other observers may read X_x only by the same QND controls.
* Snapshot payload gates are controlled nondestructively by c_x and are identity on the timer stage. Hub-local payload operations involving c_x or S_x use x's OWN local resource tag as their fixed native guard. The fixed read-copy registers remain intact as controls until terminal discard, as required by the read-only compiler.
* The timer and complete COMMIT-OPPORTUNITY channels are exactly the ones in CENTRAL_BOX_ALL_CYCLES_V1.md. Disabled opportunity leaves are identity on X_x and S_x, not measurements of an in-flight snapshot. An enabled commit requires tag x FREE.

All fields named here are on complete finite physical sites. A protected cavity contains those sites, their native service witnesses and every relevant declared write footprint. Perturbations are absent there during the stated fixed interval. Outside nominal owners still run and may start malformed; they remain QND on protected X registers.

## 2. The added channels preserve each observer's clean range

Use the exact compiler's ownership-deleted forest and its invariant owner good projector P_h. The established compiler identity is: every complete retirement maps the owner's ENTIRE Hilbert space into P_h, and nominal prefix/cleanup operations preserve every such good range.

The newly added timer Kraus operators commute with the snapshot prefix dressing: they preserve c, act only on the stage, and any dephasing in c commutes with its nondemolition control. The disabled opportunity projectors involve only c/stage/tag sectors and likewise preserve the dressing.

For an enabled COMMIT, the local tag is FREE. In this sector no observer actually owns X_x or S_x. Its forest factor therefore has no action on those payloads. The choice of x's own guard for its hub-local c/S gates also prevents a malformed unowned prefix from introducing a live dependence on these fields in that sector. Other owners' QND/read-only factors act only on their actually owned resources and private workspace. Hence the enabled onsite commit preserves their good ranges. It may change c, X and its own classical snapshot interpretation, but cannot cut through a legitimately owned prefix.

The actual SUCCESS leaf is the native complete retirement with an additional resolved update of c/stage. Its source effect is uniform on those auxiliary fields. Its target is Q0 with reset native workspace, so it still maps the whole owner space into the good range. Snapshot S_x is not erased by native workspace retirement.

Thus, after h's first actual SUCCESS, all its subsequent attempts are clean in the exact native sense; this statement does not require every other observer to have been clean earlier. Their QND interaction and exclusive ownership cannot corrupt h's private workspace or snapshot. The second SUCCESS after a c=0 reset has necessarily followed retirement/cleanup/new LOAD and has the fresh snapshot semantics explained below.

This is a direct algebraic use of the exact compiler, with the added operator-preservation checks supplied here. It is not an assumed global all-ready/flush detector.

## 3. First physical commits classicalize the visible neighborhood

Let b be a deterministic beginning of a protected interval. Suppose every required SNAP, FREE and TICK tile from b onward passes. From arbitrary c/stage/native state, two actual snapshot SUCCESS leaves occur within 2 delta. Their resolved c updates put c=2 on every retained branch, unless a physical commit has already occurred. The timer then has at most n ticks remaining, even if its initial state was an arbitrary coherent superposition. Every active tick is consumed and its resolved stage leaf makes this assertion branchwise. The count envelope completes it within 3T/4. A free opportunity follows within 2 delta.

Hence each site has at least one PHYSICAL commit by

    b+2 delta+3T/4+2 delta = b+7T/8.                 (1)

A physical commit need not yet be a represented switch: an old snapshot might write the same visible label. This does not matter here. Its output is nevertheless classical in X_x and it resets c=0.

After every site in the finite visible neighborhood has had this first commit, their joint state is block-diagonal in all visible X labels, including its bath/reference correlations. Each local measure-prepare commit removes the corresponding off-diagonal blocks. All other nominal coefficients commute with the X projectors and cannot recreate those blocks. Complete-site cavity protection excludes a perturbation that would rotate them later. This establishes an actual classical pointer history on the protected neighborhood after b+7T/8, not a classical unraveling postulated for coherent noisy evolution.

## 4. Every later cycle is fresh

A physical commit sets c=0. Before the next commit, no operation other than the observer's actual SUCCESS leaves changes c. At most the first subsequent SUCCESS can finish a pre-commit attempt. It changes c=0 to c=1. The next SUCCESS is a new clean attempt, reads c=1 under the full lock, writes the current neighborhood snapshot, then changes c=1 to c=2 and resets the timer to stage0.

The common snapshot linearization time lies strictly after the preceding physical commit. Until the later commit, X_x is unchanged: no other nominal writer exists, and that later commit is disabled until the timer completes. During the snapshot's locked interval its neighbors' commits are also excluded by their tags. Thus the copied tuple is one actual common neighborhood value, and the timer gives the required temporal separation.

Time marking now guarantees that the resulting commit changes Det. Consequently every physical commit after the first one is a represented switch, and each full later cycle has duration in [T/2,7T/8]. In particular every site has undergone a fresh represented switch by b+7T/4.

For a central interval starting at a>=b+2T, every relevant post-a cycle is fresh and the neighboring visible labels already have a classical history. Upper-dwell tests starting at a are covered even if a lies part-way through a cycle. Computation tests use the second switch after a, whose snapshot is strictly after its first switch. Initial time a=0 still requires the explicit initialization qualification in the central-box note.

## 5. Deterministic receiving consequence

Choose W=2T and grid-round the protected past as in CENTRAL_BOX_ALL_CYCLES_V1.md. Include the SNAP/FREE/TICK tests for the finitely many observers/sites whose visible registers enter the tested neighborhood, with their full native service/semantic patches. No separate unproved quantum forest-flush event is needed for THIS classical architecture: first SUCCESS retirement and the QND/commit invariance above supply its local flush.

If any required patch/test fails, mark the corresponding elementary box. If all pass, every represented classical cycle needed by the central primitive condition has the timing and common-snapshot semantics. This is the missing deterministic premise in Section 5 of FIXED_GRID_TIMER_SERVICE_CAVITY_V1.md for this specialized classical read-only implementation.

This lemma does not say a dirty quantum DATA module can be washed clean, that an unknown input can be erased, or that a whole quantum codeblock may be rewound. It concerns visible classical labels, private snapshots and exact native controller retirement only. The Gacs recursive damage map, geometry of a leveled quantum schedule, and bounded open quantum ports remain separate obligations.
