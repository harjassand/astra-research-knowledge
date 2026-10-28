# Full-ambient unknown reset: rank-signal-classical compilation lower

2026-10-27. Root candidate; independent receiving requested.

Fix s>3r, 0<p<=1 and a=3r/s. Haar U in SU(s) defines rank-r logical projectors P_i and code P=sum_i P_i. The channel is
 E_U(X)=p V_U(X tensor I_r/r)V_U*+(1-p)TrX (I-P)/(s-3r).
Unknown orthogonal replacement background fills the entire remaining ambient space. No source-dependent quantum storage is retained by a classical compiled decoder; calibration may be arbitrary coherent adaptive, but precedes independent datum. A more general decoder retains at most m quantum dimensions plus arbitrary classical memory. Uniform averaged unhalved complete error is <=p/4 versus G_p.

Let Jinfo=D_Ber(p||a)+2p ln3, natural logarithms and 0log0=0. Then
 n>=sr/(32 Jinfo) (classical),
 nm>=sr/(64 Jinfo) (bounded quantum memory).

Proof: for arbitrary prequery qutrit Q and memory M, the exact orthogonal output decomposition gives
 S(B|M,U)=h(p)+p[ln r+S(Q|M,U)]+(1-p)ln(s-3r).
Information increment is S(B|M)-S(B|M,U)-I(U:Q|M), bounded above by
 ln s-h(p)-p ln r-(1-p)ln(s-3r)+p ln3=Jinfo.
Thus I(U:deployment storage)<=n Jinfo. Source-dependent conditional inputs, reset support information and mixing entropy are all retained.

For decoder label effects T_i, center Ttilde_i=T_i-(sum_j T_j)/3. The common replacement term cancels exactly, leaving
 f(U)=p/(3r) sum_i Tr_B[P_i(U) Ttilde_i], with Haar mean zero.
The received HS-SU(s) scalar gradient argument gives Gamma(f)<=2p²/r; bounded-m-memory operator version gives <=4mp²/r. Received heatflow transport with entropy rate s yields witness <=2sqrt(Gamma_bound I/s). Complete error<=p/4 implies witness>=p/2. Thus I>=sr/32 or sr/(64m), respectively. Combine with the physical information budget.

If p>=a, the second Bernoulli term (1-p)ln[(1-p)/(1-a)] is nonpositive. Hence Jinfo<=p[ln(p/a)+2ln3]=p ln(3sp/r), and the classical bound implies n>=sr/[32p ln(3sp/r)]. At fixed accuracy, this matches a proposed reusable unknown-background O(sr/p polylogs) upper in rank/ambient/signal exponents, if its relative-learning bridge is received. For p<a no such simplified p^-1 assertion is made. At p=a the bound reduces to sr/(64p ln3), consistent with the known canonical flat family. At p=1 reset vanishes and Jinfo=ln(3s/r).

Dependencies: joint_rank_ambient_signal_compilation_tradeoff.md (centering, gradient, complete memory treatment), complete_mlsi_direct_heatflow_transport_lemma.md. The new source/entropy calculation is explicit above. Fixed query caps only; no online/interleaved, expected-cost, or universal pointwise noise lower claim. Historical novelty unassessed.
