# Required comparator: direct service tomography, not full environment tomography

2026-10-28. Root comparison companion to the IC-port and signed-core routes. This is an elementary established comparator, not a new discovery. It narrows what an advantage claim could mean.

If calibration is permitted to execute the same fixed H-call service and its accessible payload/output dimensions p,k are small, ordinary end-to-end channel tomography already avoids reconstructing the environment. Prepare an IC family rho_u on the payload, run the full declared service from each independent source start, and apply an IC POVM E_v on its final accessible output Y. Keep any classical record that is part of Y; its dimension/cost cannot be silently discarded.

Let D_u and B_v be known Hermitian duals, so X=sum_u rho_u Tr(D_u X) and Y=sum_v B_v Tr(E_v Y). Then

    J_N=sum_(u,v) p_uv D_u^T tensor B_v,
    p_uv=Tr[E_v N(rho_u)].

If every probability error is <=w,

    half ||Nhat-N||_diamond <=(w/2) C_J,
    C_J=sum_(u,v)||D_u||_1 ||B_v||_1.

There are p^2 input settings and at most k^2+1 output outcomes. All outcomes for the SAME input setting come from the same multinomial sample, so no need to pay a separate bank for each outcome. With K=p^2(k^2+1), N_per_input>=log(2K/beta)/(2w^2) independent starts per input suffices for the simultaneous event. The total native calls are at most H p^2 N_per_input. Preparations, final POVM, holding/routing/controls, data storage and final channel/decoder SDPs are also charged.

Project the signed accessible Choi estimate to CPTP and optimize the full decoder using the same paid physical synthesis mechanism as the proposed core method. The actual channel is a feasible point of the projection, so its approximation and recovery regret follow by the same triangle arguments. No hidden-memory model, hidden-memory dimension bound, source generator, prior Pauli model or environment readout is needed. Source stationarity and independent starts are still required.

Thus a claim that a core method merely permits fixed-service recovery 'without environment tomography' would not by itself establish a new capability or an advantage. Direct service tomography already does so under this access contract. Conservative short-core certificates can require precision proportional to1/H and hence H^2 sample growth, while the direct method pays H native calls per shot. Core conditioning and IC dual norms can make the short-core method much worse at modest H.

What the short-core route can change is the MAXIMUM acquisition episode depth (bounded by2d_M^2−1), and reusability of one calibration for many later coherent/adaptive controllers and services. A direct fixed-service estimate generally supplies neither arbitrary-controller prediction nor a different service channel. A useful comparison must state an actual acquisition-depth restriction, a real many-controller/amortized task, or another missing interface that the common short core supplies. No such cost advantage is established by the present theorem alone.

If Y includes exponentially many histories or a large quantum register, direct tomography may be expensive; but the core method's final accessible Choi/decoder representation can then also be expensive. A compressed task representation or controller search mechanism must be constructed before claiming that this cost has been removed. Neither method certifies arbitrary future nonstationary memory from independent-reset data.
