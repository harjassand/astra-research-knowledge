# Root construction: dilute unflagged sensors and occupation prices

2026-11-01. Proposed constructive replacement; global join not yet independently checked. Retain prior legal-sector source proof and its failures separately.

## Target and change of mechanism

Earn an autonomous bounded-arity syndrome service with noisy physical clocks, without assuming reliable collision flags or accepted-report histories. Allow collisions and wrong reports. Their actual occupation, not a forbidden-event probability through the whole storage time, is charged in a positive potential. Strong active extraction receives identical interactions, clocks, resets, gates and rates. No superiority claim.

## Independent cycle clocks

For each bounded-weight check, use an idle phase 0 followed by m bounded-degree progress phases. Idle departure rate r; each progress rate k. Every phase instrument is TP and advances on all outcomes, so the classical clock law is independent of quantum data, even for overlapping gates. No active/bad flags. Accept every terminal X-probe readout into its cache. Reset/preparation at idle departure. Controlled-Pauli prefixes dress all actual stabilizers; completed check prefixes commute stabilizers and logicals. Valid clock operations preserve those dressed quantities exactly. Every probe has a slow idle and fast finite cycle.

Stationary active fraction f=mr/(k+mr). For independent neighboring clocks, simultaneous active occupation has probability f_p f_q=O((r/k)^2). This is a property of the specified joint generator, not an independence assumption about errors or quantum records.

Own-clock Poisson prices t and xi follow the existing corrected derivation: t solves killed time-to-readout; xi pays the accepted-readout gain using post-readout t, and readiness is killed at readout. t_max, xi_max=O(1/r) for fixed m and k, as r goes to zero. Readiness is transported except by interfering neighboring controlled-Pauli gates. Each such defect change has bounded norm and is supported on simultaneous active clock states. Hence, with sensor reward scale A,

L V_sensor <= -A e + C A (k/r) sum_neighbors I_overlap + C A epsilon I.

Here epsilon is physical preparation impurity; detector noise is separately charged. Coefficients C depend on fixed check weight/degree, not code size. This displayed estimate still needs direct operator verification; especially verify effects of neighboring readout/reset on readiness and include all such overlapping events. Arithmetic source budgets for Boolean overwrite can be included by nonconstant killed reward, as in the sibling weighted-rate join.

## Centered pair occupation price

For every overlapping check pair let Q_r be its actual independent finite clock generator. Solve

Q_r h = -I_overlap + pi_r(I_overlap),

and shift h by its minimum so h>=0. Adding C A(k/r) h times identity cancels the pointwise overlap remainder and leaves floor

C A(k/r) pi_r(I_overlap)=O(A r/k).

Unlike a marginal collision estimate, this is an exact generator identity for every clock state and every quantum state. Off-diagonal clock states cause no problem for a diagonal observable with classical clock-labelled TP jumps.

The span of h is O(1/k), uniformly as r approaches zero: at r=0 the unique recurrent state is both idle; every other state reaches it in bounded expected time O(m/k), and the centered Poisson problem normalized h(0,0)=0 is invertible on the transient complement. Its finite matrix inverse is continuous at r=0. The source term pi_r(I) vanishes quadratically. This proves existence of finite uniform constants, not their practical size. The positive pair price has height O(A/r), so it must be charged in the energy barrier budget.

## Physical malformed clocks

Encode each cycle by the previously derived domain-wall/mode qubit clock. Decode arbitrary bit strings by mode and rank. Sorting 01->10 preserves that decoded rank and the associated Pauli-prefix dressing; it reduces inversion count I_clk by one. Valid configurations have one correct enabled transition. Any deviation of the actual native local transitions from decoded-cycle dynamics is confined to I_clk>=1, so its contribution to any bounded local potential is bounded above by a finite constant times I_clk. This includes a premature CP reset and all wrong microgates; they are NOT declared harmless.

Let native sorting rate nu. Its action on a diagonal inversion penalty a_clk I_clk gives -nu a_clk N_01. Since I_clk<=M^2 N_01, repair supplies -nu a_clk I_clk/M^2. Other transitions can raise inversion by a fixed amount at total local rate O(k), also supported on I_clk>0. Base witness W may change under malformed native gates by O(1), yielding O(k I_clk), independent of A. Thus choose nu a_clk/M^2 to dominate both this and all source-price deviations. To keep the positive clock penalty density small, choose nu sufficiently large relative to k and a_clk sufficiently small. This is a fixed intensive hierarchy; it is not free noise suppression. Noise of high-rate sorting hardware must be admitted at its actual strength.

This paragraph is a proposed inequality scheme, not a completed check of all local transitions. Mode endpoint and reset operations need explicit malformed-state enumeration. A local condition accidentally enabled on a valid state at the wrong phase would defeat the claim.

## Full-potential and barrier budget

Let V=W+Z, with Z positive and local. It is sufficient to bound Z<=z n I and

L V <= -c W + b n I,

which implies L V<=-c V+(b+c z)n I. No artificial negative drift for every readiness term is required. Source and pair prices have z=O(A/r); Boolean consistency weights and inversion penalties add their actual finite density. Choose actuation scale A proportional to c small relative to r, so z can be made smaller than the protected barrier density. Choose r/k small so b/c from collisions is small, and preparation/readout impurity small enough for its actual floor. Finally choose sorting nu to dominate malformed-state production while retaining a small positive penalty. All are constants independent of n; these constants may be prohibitive.

The existing noncommuting local exponential expansion applies if this global mean inequality is proved: e^(-aV/2) L*e^(aV) e^(-aV/2)=a L*V+O(a^2)n. Sensor readiness projectors need not commute each other. They must commute the protected base-W barrier for the intended cut; verify this using dressed stabilizers, not bare check inputs. Full jump-norm J†J logical flatness and finite boundary bandwidth remain mandatory in the killed-channel comparison.

## Consequence gate

If these inequalities close, the new operation is autonomous low-arity parity acquisition inside a fixed-rate protected memory, with wrong reports, overlapping probes and malformed clocks charged. This removes an essential implementation premise. It still does not supply microscopic two-body interactions, economical Tanner constants, Euclidean wiring, or a same-hardware advantage. Do not label it a civilisation-level result or optimize its constants before those next gates are evaluated.
