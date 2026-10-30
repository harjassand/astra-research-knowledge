# Independent audit: general-order active credit

Reviewed 2026-10-30. Source: `ACTIVE_CREDIT_GENERAL_ORDER_EXTENSION.md`.

**Verdict: the stated local capped trace and cost bound pass.** Constants depend on the fixed composition dimension, m,q, graph, and positive coefficient bounds. No global recurrence or dimension-uniform complexity conclusion is earned.

## Exact residual

With h=q-m, activation adds m-1 to N and q-1 to B. If initially inactive and A>=1, its target has A>=m and is active, so its credit change is -h and its Z increment is exactly zero. From an active source its increment is +h. Immigration adds one to both N and B, so only an activity turn-on changes Z, by -h. Clearing starts active because A>=m; it changes B-N by -h and turns the credit off exactly when its target is inactive, giving total increment zero in that case and -h otherwise. Fast invariance of I follows from the enabled complex return path as in the cubic audit.

Every pure mX_i is a genuine source because k>=2 and the fast graph is strongly connected. Thus inactivity implies X_i<=m-1 for all i and N<=k(m-1); there is no singleton empty-graph loophole here.

## Uniform block estimates

A bounded complex path from any enabled source to mA followed by clearing gives a polynomial normalized absorption bound. The desired path length depends only on the finite graph; normalized total rates are <=C(1+N)^m and every prescribed enabled channel has a positive lower bound. This remains valid for adapted coefficients in a fixed positive compact box by conditional jump-probability and holding-time estimates.

On the logarithmic cap, ANY competing birth—not only activation—before clearing has probability <=Z^{-(q-1)+o(1)}, since its rate is <=C(1+N)B and the active mean clearing time is <=C(1+N)^ell/(B)_q. The corresponding stopped time is Z^{-q+o(1)}. Fixed powers of log Z are subpolynomial for every fixed p>0.

At an inactive A>=1 state, prescribe activation before immigration and then clearing before any birth. Conditional on both being neutral, total N falls by exactly one. At most k(m-1) such successful macrosteps reach inactive A=0 or a down exit. From inactive A=0 the first prescribed immigration is the only enabled event; at most m-1 more immigrations are needed, each with conditional probability at least c/Z against activation. Hence the successful down block probability is >=c Z^{-(m-1)}. An earlier activity turn-on only helps.

The large-active alternative is valid above N>k(m-1)+m: clearing leaves N-m>k(m-1), so its target must stay active and Z decreases by h. All intermediate bounded-head paths fit inside the cap after increasing the threshold.

Every failed prescribed choice either stops at a residual/cap exit or restarts neutrally at exactly the same Z. Upward exits arise only from activation during one of a bounded number of active episodes, so their block probability is <=Z^{-(q-1)+o(1)}. Each block has uniformly bounded conditional mean duration. Conditional renewal therefore gives expected block count O(Z^{m-1}), the claimed up probability Z^{-(q-m)+o(1)}, and mean stopping time O(Z^{m-1}). Independence is unnecessary.

## Factorial cost and control scope

The only live residual exits are Z+h and Z-h. Their exact factorial ratios have leading powers Z^{alpha h} and Z^{-alpha h}, respectively. Combining them with the up-probability estimate gives Z^{-(1-alpha)h+o(1)}+O(Z^{-alpha h}), tending to zero for every fixed alpha<1. A compatible tilt and a fixed polynomial multiplier preserve contraction. Finite capped neutral state spaces prevent explosion inside each interval; the contraction bounds the total number and cost of residual intervals before the target. Thus the stopped cost is finite and bounded by C(1+Z)^{m-1}phi(Z).

For a fixed homogeneous generator this defines the usual state-only value. If arbitrary adapted/time-dependent coefficients are intended and a common state-only generator inequality is desired, define the value as the supremum of stopped costs over admissible policies. The same uniform bounds prove finiteness; finite-target epsilon-policy concatenation yields the common local inequality. A single uncontrolled expectation should not be silently used as a common value for all controls.

## Actual cap entries

Eventually L(Z+h)-L(Z)<=1. An active activation adds m-1>=1 to N. Starting outside, N>=L(Z)+1, so its new N is at least L(Z)+2, whereas the new cap is at most L(Z)+1. Thus it cannot enter, including the borderline m=2 case. Inactive activation and immigration also cannot enter; fast jumps preserve both variables. Only clearing can enter, with N decreasing by m and Z unchanged or decreasing by h. Its source lies in L(Z)<N<=L(Z)+m. The target weight does not grow under that residual change. Threshold-entry sources form a finite set because residual jumps and capped target N are bounded.

The separation B-Z=N+hI>=N is correct and supports the earlier collar ratio if the independent outer negative margin exists. It does not create that margin or resolve the higher-dimensional entropy mismatch.

Reviewed source hash:
ad6febc173ca9ab3d2bb424a6c2ec88a744e7051bf1c7050a4bca7bc4788ed2d  chemical_joint_shell_20261030/ACTIVE_CREDIT_GENERAL_ORDER_EXTENSION.md
