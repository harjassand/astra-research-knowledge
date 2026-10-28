# Physical discrimination characterizes recovery utility up to constants

2026-10-27. Root candidate, independent receiving requested. This concerns a precise utility, not an asserted sharp diamond-distance equivalence.

Let E(rho)=p V(rho tensor sigma)V*+q Tr(rho)tau, q=1-p, any finite ambient, rank sigma<=r. NO rank or orthogonality condition on tau. Put A=p V(I3/3 tensor sigma)V*, Y=q tau/3, and e=e(A,Y)=(TrA+TrY-||A-Y||1)/2. For an accepted decoder with erasure completion let L=2p/3-(f-a/3), where f is accepted normalized-Choi entanglement overlap and a is its trace.

Let L_all be the infimum over all accepted CP trace-nonincreasing decoders and L_r the infimum with the low-trace condition Tr D_acc^dagger(I)<=3r. Then
 (2/3)e <= L_all <= L_r <= 2e.

Lower proof: for Q=D_acc^dagger(I), 0<=Q<=I, genuine missed mass p-a_s=TrA(I-Q), reset acceptance a_n=3TrYQ. The received exact utility-loss identity gives
 L >=(2/3)(p-a_s)+(2/9)a_n
   =(2/3)[TrA(I-Q)+TrYQ] >=(2/3)e.
No restriction on the decoder or trace budget was used.

Upper proof: choose the Helstrom projection Q deciding A against Y. The analytic filtered known-V inverse has effect F=(I tensor Q)Pi(I tensor Q), feasible with TrF<=r and Tr_A F<=I/3. If alpha=TrA(I-Q), beta=TrYQ, its genuine entanglement weight is >=p-2alpha and reset acceptance<=3beta. Thus L<=2alpha+(2/3)beta<=2e. The comparator only establishes existence; learned implementation uses the acquired convex SDP, not an unknown Helstrom oracle. This proof is the direct-test refinement of the already received overlapping-reset comparator.

Operational consequence: the optimal complete unhalved diamond recovery error delta_opt obeys
 delta_opt >=(4/3)e,
 while an explicit existence comparator has error<=6sqrt(3pe)+18e.
For the lower, the utility difference is the expectation of Phi-I_accepted/3 (zero on erasure) against a trace-zero normalized Choi difference. This observable has spectral diameter1, so L<=one-half the Choi trace norm<=one-half diamond error. The upper is the received complete bound at L<=2e. These different powers are NOT claimed optimal.

This provides a necessary obstruction as well as sufficient utility control for arbitrary reset rank. Since low-trace restriction loses at most a factor3 in optimal utility, it is not an arbitrary restrictive learning model for this source family. A good classical learned optimizer can transfer near-optimal utility via the separately received relative acquisition inequality. Entropy is optional: the rank<=2 reset entropy theorem is one sufficient way to control e, not part of this equivalence's hypothesis.

Known source vs unknown source remain distinct: this note proves geometry of the optimum. The acquired estimator/SDP theorem separately pays the source queries. No novelty or physical demonstration claim is made.
