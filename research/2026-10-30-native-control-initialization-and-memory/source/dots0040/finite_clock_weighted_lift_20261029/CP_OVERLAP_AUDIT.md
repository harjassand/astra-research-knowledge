# Signed-overlap audit: exact algebra, harmonic blocker credit, and finite regression
2026-10-30, child worker cp_clean_overlap.

## Exact linked first-order identity
Let B_h be any positive clock-only observable and define
Z_h(O)=sqrt(B_h) Phi_h^*(O) sqrt(B_h)-{B_h,O}/2.
For a data-only V with d_h=V-Phi_h^*V, one has Z_h(V)=-B_h d_h. In the dressed clock generator, EXACTLY
[L*,Z_h]V=-(L_clock* B_h)d_h
 -kappa sum_j a_j^* B_h a_j Delta_j d_h
 +kappa sum_j sqrt(B_h)n_j sqrt(B_h) Delta_h d_j
 +kappa sum_j D_{sqrt(B_h)}^*(n_j)d_j.
For disjoint enlarged clock/data supports, the second and third terms cancel and the fourth vanishes. This is the proper linked cancellation, not a claim that mixed animal differences vanish.

If j is initially data-inactive but h activates it, Delta_h d_j may be positive while d_j=0. Thus the third term cannot be charged to n_j d_j. HOWEVER it is canceled at first order by the corresponding term in T(L*V). Dropping or reserving a fixed fraction of T(L*V) can destroy this cancellation. In particular a conjugated-generator inequality for T^{-1}L*T is stronger than the desired L*T(V) inequality and can fail for this reason.

## High-reset Poisson blocker structure
Scale kappa=1, e=g/kappa. The clock Poisson solution A with L_clock*A=n_h-p_h has expansion A=-n_h-2eY_h+e^2 A_2+... . On a star with h at its center and m occupied neighboring leaves, the diagonal order-two Poisson equation gives A_2(m)-A_2(0)=4 H_m, where H_m=sum_{r=1}^m 1/r. The own-occupied diagonal shift is 8. The kernel Schur complement contributes 4 for a ready, unblocked center.

Consequently the minimally scalar-shifted positive B_h=lambda_max(A)I-A has one-blocker diagonal of order 4(H_D-1)e^2 when D independent neighbors can be jointly occupied. It is NOT generically O(e^3). The O(e^3) suppression seen on the two-node graph is degree-one-specific.

A three-node star at e=.01 gives the following finite regression (ordering clock states empty,center,leaf1,leaf2,both leaves):
p_center=.00039904210746570534,
diag B_center≈[.000599192131, .999800629, .000200203224, .000200203224, .000000868357955].
This confirms the harmonic obstruction to a naive small-drive argument.

## Concrete CP-product finite-t failure
Use three classical data levels with V=(1,M+1,M+2), center channel h:2->1 (other levels fixed), leaf channel j:1->0 (other levels fixed), and the other leaf's identity channel. All updates are V-monotone. Their overlap graph is the three-node star. Use exact finite clock Poisson solutions and the positive maps
T_h(O)=sqrt(I-tB_h) O sqrt(I-tB_h)+sqrt(tB_h)Phi_h^*(O)sqrt(tB_h).
At kappa=1,g=.01,t=.01,M=1000, composing in the order leaf2,leaf1,center produces POSITIVE drift on data level2 and the clock basis state with only leaf1 excited:
<leaf1| L*T(V)|leaf1>≈+1.60126510e-5.
The maximal eigenvalue of the data2 drift block is ≈+1.60506321e-5. The clean undressed drift is zero on this state. Thus positivity/unitality plus exact Poisson solutions do not by themselves establish the desired signed finite-clock drift for arbitrary product order and t.

This is a numerical regression with a large sign margin, not a symbolic interval-certified theorem. The script check_cp_overlap_star.py uses M=100 by default; replacing V=(1,101,102) by (1,1001,1002) reproduces the positive example. The same code at smaller t recovers negative drift. Order center,leaf1,leaf2 also remains negative in the tested fixtures. Hence the failure is consistent with a local O(t^2 M) ordering error that can be absorbed by t p_min if t is chosen using the actual local comparison constants; it is NOT an impossibility theorem for the CP-product strategy.

## Strongest plausible proof organization
Do not first prove T^{-1}L*T(V)<=-cW or throw away part of T(L*V). Keep each local reset and all nearby CP maps grouped until activated-hub terms cancel. Commute only genuinely disjoint CP maps. The remaining errors should be local connected terms of order t^2, controlled by bounded-patch animal completion and then absorbed by choosing t sufficiently smaller than p_min divided by local constants. Turning this into an exact bounded-depth positive-factor decomposition remains open here; layer overlap means one cannot simply factor the entire circuit into a disjoint near/far product.
