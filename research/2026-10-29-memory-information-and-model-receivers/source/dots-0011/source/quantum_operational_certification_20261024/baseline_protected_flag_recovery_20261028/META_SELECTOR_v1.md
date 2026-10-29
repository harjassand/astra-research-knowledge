# Positive-return meta-selection protects an existing flag decoder
2026-10-28. New candidate, pending review. This uses conventional EXP3-type exponential weights, not a novel bandit algorithm. It combines the received compact flag gradient with the actual mixed-role occupation principle of N1161/N1162. Only ONE private terminal resource is claimed; no multipayload conclusion is imported.

## Interface and actual roles
Retain the named n-qubit data port, accessible r-dimensional flag, n Bell-reference halves per call, arbitrary unreset source memory, private controls and padded complete-call boundary. Fix an implementable baseline flag POVM B before this experiment; it can be identity correction after an actually compiled coherent preconditioner. The source conditional Bell/flag coefficients sigma_(t,h), fixed before fresh current role coins, define loss ell_t(M)=1-sum_x Tr(M_x sigma_(t,h)).

Maintain a predictable learned POVM M_t and two meta weights. On every nonterminal call send the same Bell-pair halves through the source and obtain Bell label x. A private role coin, independent of current output, chooses SHADOW with q=1/4 or EVALUATE with e=3/4. The role may be drawn after the complete source call, but is not allowed to depend on x. The two actual post-call instruments differ and change future source memory; their genuine mixture defines the sole occupation law in this theorem.

SHADOW: measure uniform flag Pauli W, outcome b, and give OGD gradient Gtilde=4r b W at label x. EVALUATE: choose candidate i in {0,1} independently of x with predictable meta probabilities p_t; candidate 0 is B and candidate 1 is M_t. Measure that actual flag POVM (including its private unbiased compact realization when used), obtain correction label z, and record POSITIVE failure bit y=1[z!=x]. No unknown payload is measured. For either candidate, E[y|h,i,EVALUATE]=ell_t(candidate_i), even for a coherent source. This is simply the Bell-label/flag discrimination identity.

All actual role, measurement and retained controller records form h. No all-shadow, counterfactual-baseline or reset occupation is substituted. Baseline comparisons are on this mixed controller's expected visited histories.

## Shadow learner on the mixed occupation
On nonshadow calls use zero gradient. Conditional expectation of Gtilde is the true reward gradient, and E||Gtilde||F^2=r^3/q=4r^3. Use step a=1/(2r sqrt N), N a power of4. The same compressed weighted projection and exact feasible slack xi=1/(256N^2) apply. The center perturbation operator norm is now at most2/sqrt N<=1 for N>=4, so the received finite projection norm budget still applies.

For uniform initial POVM, squared initial distance <=r. Expected regret of the learner versus any fixed flag POVM is at most
  (9/4) r^2 sqrt N.
Indeed the initial term and variance term are each r^2 sqrt N, and the projection allowance is at most r^2 sqrt N/4. Starting instead from ANY fixed baseline POVM gives squared distance <=2r and bound (13/4)r^2 sqrt N. More precisely retain the actual comparator-distance term ||M_1-M_*||F^2/(2a); this can be zero against the starting baseline. These bounds do not assert pathwise conditional losses; the acquired-gradient inequality is pathwise and the loss guarantee follows in expectation.

## Two-candidate positive-loss meta learner
Choose prior pi=(pi_0,pi_1) with both entries positive, fixed before any records (e.g.9/10,1/10 to favor the existing baseline). Let w_t be normalized exponential weights initialized at pi. Set gamma=1/sqrt N<=1/2 and eta=1/(4sqrt N). Play p_t=(1-gamma)w_t+gamma(1/2,1/2), so every candidate probability is at least gamma/2.

The only nonzero estimated loss on an evaluation call selecting i is
 Lhat_t,i = y/(e p_t,i).
On shadow calls both estimates are zero. Conditional on h, E Lhat_t,i=ell_t(candidate_i), while
 E sum_i w_t,i Lhat_t,i^2
 =sum_i [w_t,i/(e p_t,i)] ell_t(candidate_i)
 <=2/[e(1-gamma)] <=16/3.

Update unnormalized weights by multiplying exp(-eta Lhat_t,i). For nonnegative z, exp(-z)<=1-z+z^2/2, with no upper restriction on z. The usual log-potential telescoping therefore gives, for either FIXED expert index i (including the predictable time-varying learned candidate),
 E sum_t [sum_j p_t,j ell_t(candidate_j)-ell_t(candidate_i)]
 <=log(1/pi_i)/eta +eta N*8/3 +gamma N
 <=[4log(1/pi_i)+2]sqrt N.

The replacement of w by p costs at most gamma per step. This proof is valid for adaptively changing conditional losses because all candidate POVMs and p_t are predictable and current records are obtained from the actual mixture. Expert 1 may evolve from previous shadow records; no static-model assumption is used. This is an ADDITIVE expected-regret result. The use of positive bits does not by itself establish a sharper first-order/small-loss bound.

## Terminal resource guarantee
Choose private T uniformly in1,...,N before calls. At T retain the reference halves instead of Bell-label measuring them, select i using p_T, and apply candidate_i to the returned data/flag. Isolate the Bell resource. Prefix equality with the mixed-role experiment and the received teleportation consumer yield a later single fresh-payload channel whose averaged half-diamond error is at most the terminal resource loss. Its ideal loss obeys BOTH

 L_service <= L_baseline +[4log(1/pi_0)+2]/sqrt N,
 L_service <= inf_fixed M L(M) +(13/4)r^2/sqrt N
                         +[4log(1/pi_1)+2]/sqrt N,

for a baseline-initialized shadow learner. Here L(M)=N^-1 sum_t E_h ell_t(M) on this actual mixed occupation. With uniform initialization replace13/4 by9/4. The first inequality protects prior scientific capital without an r-dependent adaptation penalty; the second permits improvement when some fixed correction class receiver is materially better. Both bounds concern the same experiment. No claim is made that the controller can do no worse than baseline on every realized path, at every small horizon, or on a different baseline-controlled memory trajectory.

One whole-process implementation allowance nu adds once to the service error while keeping this ideal-interface comparator. This includes finite meta arithmetic, capped random sampling, actual measurements/pruning, receiver synthesis, memory-port controls, resource holding and teleportation. Runtime is padded so current role/candidate timing does not select an external source map.

## Finite arithmetic and cost
The meta probability floor gamma/2 prevents reciprocal-loss blowup beyond Lhat<=2/(e gamma)=O(sqrt N). Therefore eta Lhat is bounded by a numerical constant and cumulative log-weight range is O(N), with an additional paid log(1/min pi) term. Exponentials and normalized probabilities can be approximated with polynomial bit precision and capped finite sampling; allocate per-round uniform conditional TV/complete-instrument discrepancy so their telescoping sum fits nu. Do not silently call the ideal exponential weights rational. Approximation and its known-history certified error bound are an explicit implementation contract; no finite implementation has yet been executed here.

SHADOW uses the prior Bell-label and flag-Pauli controls. EVALUATE additionally applies one actual candidate flag measurement per evaluation, not just a numerical loss oracle. Terminal and evaluation candidates can use the received unbiased compact <=r^2-outcome implementation. Meta selection adds a classical candidate bit; it need not combine their POVMs into twice as many coherent outcomes. All n-reference storage, Bell preparation/readout, classical computation and final teleportation costs remain. The physical source need not be Pauli diagonal for this correction-class result; unrestricted full-CPTP comparisons require the narrower source promise.

This construction has no new simulation result yet. The previously received negative short-horizon shadow fixture motivates it but does not validate a changed mixed-role controller, whose memory occupation must be resimulated through its actual instruments.
