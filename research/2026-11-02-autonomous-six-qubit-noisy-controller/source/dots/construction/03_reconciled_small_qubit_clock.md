# Reconciliation: physical-qubit restartable monotone clock

Exposure update 15:30 UTC: after the independent construction was recorded, read FINITE_DILATION_JOIN_DRAFT.md, TANNER_WITNESS_DOWNHILL_CONTROLLER.md, and LOW_ARITY_PROGRESS_DRESSING_AND_MUTEX_GATE.md supplied by the parent. First attempted receipt path was missing; no scientific conclusion depends on reading it. The following is a new construction developed after that exposure, not an independent-origin claim.

## A. Replace the giant phase qudit by actual noisy qubits

Take an M-gate compiled energy-preserving cycle U=U_M...U_1, [U,Q]=0, with each U_j on at most two data/work qubits. Use M physical clock qubits c_1,...,c_M and one mode qubit b. Define x_i=c_i XOR b, with virtual sentinels x_0=1,x_(M+1)=0. Let r=sum_i x_i.

Legal clocks have x=1^r 0^(M-r). For b=0 the moving wall performs the computation; for b=1 it recycles the physical clock without acting on data.

At position j offer a jump with the local source condition
 x_(j-1)=1, x_j=0, x_(j+1)=0.
Flip c_j. If b=0 apply U_j to data; if b=1 apply identity. This jump uses b, at most three c bits, and at most two data qubits: AT MOST SIX PHYSICAL QUBITS, independent of M. Boundary cases omit sentinel qubits. No arbitrary M-level transition is invoked.

When x_M=1, offer a mode-flip jump b -> 1-b (separate directed channels for the two b values). Its support is just b,c_M. In a legal clock this occurs only at r=M and changes every decoded x_i from1 to0, giving r=0 without changing any physical c_i. Thus a full cycle computes U, switches mode, erases the c register progressively, then switches back. There is no global clock or pure controller reset. Corrupt configurations are handled below.

## B. A dressing defined on EVERY clock state

Let P_r=U_r...U_1, P_0=I. Define D(c,b)=P_r for b=0 and D(c,b)=I for b=1. Define Q_d=D(Q tensor I_clock)D†. Its support overhead is the full finite gadget patch, but that patch consists of physical qubits, not a single hidden qudit. The definition on invalid clocks is intentional.

For a legal b=0 wall step, r=j-1 ->j and the physical data gate is U_j=P_j P_(j-1)†, so Q_d is exactly preserved. Legal return steps have identity dressing. At the b=0 endpoint, P_M=U commutes with Q; hence the mode flip preserves Q_d. The other endpoint also preserves it. An energy-ancilla lowering reset must still be permitted only in b=1 (or otherwise conjugated); b=1 has Q_d=Q, even on invalid clocks.

## C. Explicit repair of zero/multiple/domain-wall corruption

Set the inversion number
 I(c,b)=sum_(i<j) (1-x_i)x_j.
I=0 iff x is a legal prefix. A repair jump swaps an adjacent 01 to10 in the x variables, conditioned on b. It is supported on b,c_i,c_(i+1), i.e. THREE PHYSICAL QUBITS. Every such swap decreases I by exactly1 and preserves r,b. Consequently it preserves D and Q_d EXACTLY, with no data abort cost or unknown history reconstruction. Every invalid clock has at least one adjacent01. Repeated sorting repairs reach a legal clock at the same r in at most M(M-1)/2 swaps.

The potential Q_tilde=Q_d+A I is positive. I is diagonal and commutes with Q_d; its terms have at most three clock-qubit support (via b), although they connect nonadjacent clock positions. This is an ANALYTIC potential, not an interaction requirement. Clock sites need only neighbor swaps and connections to b/data used by their gate. The degree of b is O(M), explicitly charged; M is fixed with code degree but may be enormous.

Let F=exp(a Q_tilde). For sorting rate nu per adjacent pair,
 L_sort^* F = -nu(1-exp(-aA)) N_01 F,
where N_01 counts adjacent01 pairs and N_01>=1_(I>0). This is an operator identity on all clock coherences because F is clock-diagonal, each jump has an injective classical source-to-target map, and the data dressing is unchanged. No stochastic assumption about the quantum state is used.

## D. Invalid microactivity can be dominated

During an invalid clock, the local wall predicate can enable the wrong U_j; endpoint mode flips can also occur prematurely. They are NOT called correct operations. Their decoded data action has bounded support in the fixed gadget patch, hence a bounded energy-range B under the commuting Q terms. A single wall flip changes I by at most M-1; a mode flip by at most M(M-1)/2. Thus an upper energy cost B_total=B+A M(M-1)/2 is a conservative bound. There are at most M+2 clock transition channels of rate at most kappa per gadget.

A sufficient local exponential-potential domination is
 nu(1-exp(-aA)) > (M+2) kappa (exp(a B_total)-1).
For fixed finite M,B,A,kappa, this holds with finite nu and sufficiently small positive a. All choices are independent of total memory size. The statement is strongest if the data-energy-range estimate is derived by finite-support commuting-Q conjugation, as in the parent's note; it is not an appeal to operator monotonicity of exp. Valid transitions conserve Q_d and I; invalid transitions' possible increase is charged to the sorting decrease.

This supplies a real fixed-small-dimensional clock-validity repair operation. It is not merely a probability of successful initialization or an assumed one-hot subspace. Clock noise, including coherent b flips, is still admitted separately through the parent's local perturbation estimate; the b qubit is not protected for free.

## E. Exactly what remains unclosed

1. The six-qubit gate-labelled dissipative jump is a genuine bounded-arity primitive, but NOT a microscopic two-body Hamiltonian plus simple reset implementation. A further arity-2 restriction remains open. Merely decomposing the data U_j does not decompose its correlated jump with the clock.
2. The gadget's M clock qubits, O(M) mode-bit degree, potentially huge repair rate and dressed-support constants must be included in the parent's C_loc and noise budget. No useful finite engineering constants established.
3. Multiple overlapping gadget dressings require the parent's fixed-color global D. Sorting preserves the complete phase label (b,r), so it still leaves that global D unchanged. Legal microsteps preserve the global dressing only under valid exclusive ownership. This construction does not implement a small-qubit resource owner/claim system or prove extensive legal progress.
4. From any isolated valid clock state, the same forward/return sequence eventually completes a full U and visits an ancilla reset stage. A finite-time positive-probability event exists with constants independent of memory size. That alone is NOT the global extensive quantum drift theorem, because competing gadgets change enabled moves and ownership can starve progress.
5. Initial arbitrary clock patterns can carry extensive A I. Cold preparation/tail admission must explicitly include their energy and count, just as the accepted dilation charges warm ancillas.

## F. Why my earlier p premise is strictly stronger than the parent's admission

Local-stochastic faults assert a joint classical probability inequality P(S faulty)<=p^|S|. The parent admits sums of arbitrary bounded local Hamiltonians and local bath/dissipative terms, including coherent data-apparatus coupling and clock superpositions. Such evolution has no unique classical fault set. Persistent coherent amplitude, entangled baths, and interference between fault paths are not covered by the probability inequality merely because each term is local and small.

One may derive a separate amplitude-norm fault-path theorem under particular bath/locality assumptions, but it is not the previously proved p lemma. My exact circuit compilation only transfers a pre-existing stochastic circuit threshold. The parent's direct exponential positive-operator route, if extended to this actual clock generator, is the appropriate stronger consumer; replacing it by my p premise would weaken the target.

## G. Equal-resource comparator

The active Tanner competitor receives the same physical graph, qubits, gates, resets, owner registers and rates. A six-qubit jump clock with direct positive drift would establish autonomy under noisy controllers, not an automatic lifetime/resource improvement over active Tanner decoding. The passive 3D thermal benchmark assumes its actual specified stabilizer Hamiltonian and thermal generator; Gibbs/detailed-balance protection cannot simply be imported under this same fixed nonthermal noisy controller or arbitrary local Hamiltonian perturbations. These are different admissions, not dominance comparisons.

## H. Frozen exponential-order justification (parent reconciliation, 15:36 UTC)

This section makes the bound in D precise and supersedes any interpretation based solely on a norm difference of noncommuting energies. It is NOT valid to infer exponential operator order merely from Q_new <= U Q_old U†+B I.

Work in the globally dressed frame. A clock transition c->c' is an injective partial permutation with data operation U_step. Its effective data operation is O=D(c')† U_step D(c). Because the global dressing is finite-depth with fixed finite-support gates, O has a fixed expanded support R, including for illegal local clock states. For legal exclusive ownership O preserves the base potential; for an illegal step use locality instead.

Write the base positive commuting potential Q0=Q_far+Q_near, choosing Q_near to contain every term intersecting R. Then [O,Q_far]=0, [Q_far,Q_near]=0, and 0<=Q_near<=B_R I, where B_R is the sum of norms of the finitely many near terms. Consequently

 ||exp(aQ0/2) O exp(-aQ0/2)||
 =||exp(aQ_near/2) O exp(-aQ_near/2)||
 <= exp(aB_R/2).

Here ||O||<=1 suffices; the compiled gate case is unitary. Squaring this norm inequality gives the legitimate operator bound

 O† exp(aQ0) O <= exp(aB_R) exp(aQ0).

Include the scalar clock-penalty change separately. If I(c')-I(c)<=Delta_I, the weighted jump gain is bounded by exp[a(B_R+A Delta_I)]. For this clock Delta_I<=M(M-1)/2 covers mode flips, and <=M-1 covers wall flips. Take B to be a uniform B_R over actual expanded supports. This proves the positive illegal contribution used in D, without operator monotonicity of the exponential.

F is diagonal in clock configurations. Each jump's clock map is an injective partial permutation, so J†FJ is also clock-diagonal; distinct source configurations have no cross terms. Therefore the zero contribution from legal sectors and bounded positive contribution from illegal sectors are valid sectorwise OPERATOR inequalities, not assumptions that the input clock state is classical. Sorting retains (b,r), hence the global D, and its negative drift identity is exact. Unknown Hamiltonian clock errors are not asserted to preserve clock diagonality: they belong to the parent's separate local coherent-noise admission.

Frozen scope: this establishes the physical-qubit clock-validity repair and domination of invalid clock microactivity, assuming the explicit bounded-arity gate-labelled GKSL primitives and valid exclusive resource ownership for legal operations. It does not establish owner-register qubit representation, extensive progress, or a two-body microscopic realization. No further scouting or extension is included.
