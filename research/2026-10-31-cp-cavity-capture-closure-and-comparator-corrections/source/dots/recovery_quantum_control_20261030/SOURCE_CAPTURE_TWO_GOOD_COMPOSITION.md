# Source/capture composition by two good sets, not multiplied marginal laws
30 October 2026. Conditional complete receiving theorem. Source, capture and quantum waiting each retain their declared physical scope.

## Useful result
A joint stochastic law for virtual source defects and actual capture errors is unnecessary. Strengthen each support certificate separately, project the source once in the analysis, then use the actual capture theorem on that projected source. The genuine source instrument still produces classical m with arbitrary conditional DATA/bath, exactly the capture contract. Two separately good supports have a good union. No virtual source defect is measured, and no marginal local-stochastic probabilities are multiplied.

## 1. Actual interfaces and meaning of m
Let H be an immutable mathematical copy of the genuine source instrument's classical output m; it is an analysis reference, not a protected physical register. The raw latch is initially |m>. This m is the actual instrument label, NOT a fictitious noiseless graph trajectory. Any imperfect-detector error must already be included in the proved source instrument/dictionary or separately charged. A merely coherent pointer is not silently declared a genuine classical instrument.

The source interface is COHERENT_ATG_SOURCE_LIFT.md with its fixed syndrome-only tie rule, actual graph/pointer defect dictionary and retained-bath moment bound. The genuine-m instrument must be the actual pointer-Z instrument compatible with that span, or an explicitly proved source-module-preserving noisy instrument. An arbitrary instrument that merely emits classical m and raw |m> is insufficient: it could mislabel the pointer or destroy DATA. Such additional measurement errors must be paid in the effective source/capture support before using the identity below. Its virtual input-defect basis has positive inclusion law q_s^|S|; the effective covering support F has parameter p_s=2q_s. For an effective bulk flip f covered by F and a genuine record m, write the source boundary relation (ignoring a separate physical boundary error E_B)

 |psi_(m,f)> = scalar * P(m) Rep(f)|Bell_L>.

Both the same Pauli frame P(m) and the repair Rep(f) are the fixed ones in the source certificate. Extra graph/pointer registers and bath are retained as gauge. Boundary input errors are separately bounded by t_B.

Let R be the ACTUAL capture plus waiting channel, retaining H untouched. Its final physical ports have computational value m'. Define g=m'+m. Capture's uniform complete effect hypothesis is, for every selected port set B and every genuine historical m,

 R_m^*(E_B(m)) <= p_c^|B| I,
 E_B(m)=product_(j in B) 1[port_j != m_j].                 (1)

The inequality must hold on every admissible conditional DATA/bath/reference state, including the virtually projected source state below. This is the promised actual-port statement of SOFT_PHASE_RETENTION_AND_PORT_THEOREM.md, read with TWO_PARAMETER_MOMENT_FAMILY.md and its independent audit; its physical and scheduled assumptions remain binding. It is not a law for virtual source defects.

## 2. Explicit separate forbidden families
Use the source's two bounded-degree syndrome adjacency graphs, maximum degree z, with O(nT) vertices and 2n boundary vertices per sector. Fix residual target t, a=floor(t/2)+1, ell_*=min(T,d), and terminal baseline budget u. Let kappa<=2 be the maximum multiplicity of the local baseline extraction b.

Call a support J strongly good if all these hold in BOTH sectors:

(G1) No connected vertex set W of size s>=ell_* has |J intersect W|>=s/8.
(G2) For every choice of a boundary roots, no union W of connected sets containing those roots, EVERY component containing at least one selected root, of total size s>=2a, has |J intersect W|>=s/8.
(G3) In the adjacent-check-record neighborhood N_b, |J intersect N_b|<=floor(u/(2 kappa)).

The source additionally has the separate boundary-DATA covering count <=t_B. Capture support lives only on record vertices, so contributes no boundary DATA faults by definition.

If F and G are each strongly good, then their union has occupancy strictly below s/4 in every G1/G2 witness. Hence it excludes the original source certificate's quarter-occupied large/logical and residual witnesses, and also its half-occupied bridging witnesses. Since ell_*<=T,d, all original forbidden connected sizes are covered. Moreover

 |b(f+g)| <= kappa (|F intersect N_b|+|G intersect N_b|) <= u.

Thus EVERY f subset F and g subset G has a combined repair with no logical residual and |Rep(f+g)|<=t. The original f alone also has |Rep(f)|<=t. These are hereditary support statements; XOR cancellation is not used to certify goodness.

## 3. Rarity estimates are separate and positive
For a support with inclusion bound p^|S|, a specified s-vertex witness with >=s/8 occupied vertices has probability at most 2^s p^(s/8), for p<=1. Let z_+=max(2,z), let V bound the number of graph vertices, and choose L0=64 z_+^2 (a deliberately loose fixed counting constant). Connected and rooted-union counts then yield, whenever L0 p^(1/8)<1,

 delta_wit(p) <= 2 V * (L0 p^(1/8))^ell_* /(1-L0 p^(1/8))
            + 2 binom(2n,a) * (L0 p^(1/8))^(2a)/(1-L0 p^(1/8)).  (2)

This uses the standard bounded-degree rooted-set count; every union component is required to contain a selected root. Extra fixed sector/count constants can be absorbed in V or L0.

Let N0=|N_b|=O(n), v=floor(u/(2 kappa))+1. Add binom(N0,v)p^v for violating G3. For source boundary defects add binom(2n,t_B+1)p_s^(t_B+1). Define delta_s from these source terms with p_s, and delta_c from the record-only terms with p_c. These bounds use TWO different positive probability/effect arguments, never a hypothetical joint law.

For d=Omega(n), T=Theta(n), and t,u,t_B fixed positive fractions of n, both deltas are exp(-Omega(n)) at sufficiently small fixed p_s,p_c. The threshold constants worsen relative to the source-only certificate, but no exp(eta nT) factor or unmarked-record-volume factor appears.

## 4. First good projection: source only
Let Pi_s be the diagonal projector onto strongly good source defect basis states and the boundary count condition. On the actual toggling-frame source state rho,

 Tr[(I-Pi_s)rho]<=delta_s,
 ||rho-Pi_s rho Pi_s||_1<=2 sqrt(delta_s).                 (3)

Pi_s is an analysis projection; it is NOT physically measured. Here rho is the ACTUAL completed-source state in the toggling frame. Restore BOTH states by the SAME ideal frame unitary U (a change of representation, not rerunning the noisy preparation), then apply the same actual source-compatible instrument and R. Complete contractivity preserves (3).

Crucially the projected source, after the actual instrument, is still of the form

 sum_m |m><m|_H tensor |m><m|_raw tensor tau_m,

with arbitrary subnormalized conditional tau_m on DATA/gauge/bath. Therefore (1) applies to it. Projecting the source has not required independent capture faults, and has not turned source-defect labels into an actual trajectory.

## 5. Second good projection: actual physical ports
Let Q_c be the commuting final projector selecting g=m'+m strongly good, controlled by H. The union bound from (1) and (2) gives, on the source-projected state after R,

 Tr[(I-Q_c) R(rho_s)] <= delta_c Tr(rho_s) <=delta_c.      (4)

The second gentle projection costs at most2 sqrt(delta_c). Hence the subnormalized twice-good output differs from the actual output by at most

 2 sqrt(delta_s)+2 sqrt(delta_c).                        (5)

This statement is a record/source truncation estimate only. A bound on port errors alone says NOTHING about preservation of the quantum logical state.

## 6. Necessary physical quantum receiving condition
A minimal counterexample is a channel that keeps every port perfect (g=0, p_c=0) but resets DATA to a wrong logical state. It satisfies every classical effect bound and invalidates a claimed quantum composition. Thus require one of the following actual per-(m,m') interfaces:

(Spectator) The capture instrument acts as identity on DATA, with arbitrary conditional operators on record/gauge/bath. Then every surviving branch has the original graph-state identity with f replaced by f+g, and corrected radius <=t+t_B under P(m').

(Quantum waiting receiver) There is an actual final logical-module projector Q_q, controlled by H, which COMMUTES with Q_c and with the computational port projectors. On the source-projected input, the actual R obeys

 Tr[(I-Q_q)R(rho_s)]<=delta_q Tr(rho_s).

For each historical m, its range must preserve the ORIGINAL logical Bell module, not merely the entire code space:

 range Q_q(m) subset span{ E P(m)|Bell_L> tensor gauge : wt(E)<=r_q }.  (6)

For a full native apparatus, (6) must be replaced by its actually proved common compiler-module embedding and verified Pauli-frame covariance; a global-code-support bound or an ideal final decoder is insufficient. No physical final frame application is supplied by this definition.

Because the two final projectors commute, their joint bad probability is <=delta_c+delta_q on the positive source-projected state. One final gentle projection therefore gives total error

 2 sqrt(delta_s)+2 sqrt(delta_c+delta_q).                 (7)

All bounds are complete when their input hypotheses hold uniformly with arbitrary retained references. No separate marginal gentle sum over individual records occurs.

## 7. Frame change after a genuine waiting memory
Waiting memory may REMOVE the original source repair rather than preserve raw graph amplitudes. Its correct reference is then P(m)|Bell_L>, so the spectator radius must not be reused unchanged.

For every historical m occurring in the source-good support, choose any contributing good f. For every capture-good g, put m'=m+g. The identical ideal graph outcome underlying (m,f) and (m',f+g) yields

 P(m')^dagger P(m)|Bell_L>
   = phase * Rep(f+g) Rep(f)|Bell_L>,                    (8)

up to a stabilizer of the fixed Bell target. The Pauli frame difference therefore has a representative of weight<=2t on that target. Commuting it past E only changes a Pauli phase. Consequently (6) becomes an error span of radius

 r_final <= r_q+2t                                      (9)

under the single actual-record frame P(m'). Choose the original budgets so this fits the receiving code's common correctable radius. The existence of f is sufficient to prove the range inclusion; it is NOT obtained by measuring a hidden defect label. All choices of f and their coherent coefficients satisfy the same range bound.

The new baseline discrepancy also follows directly from the source identity:

 D(m')=b(m')+sigma(P(m'))=sigma(Rep(f+g))+b(f+g),
 |D(m')|<=nu*t+u,                                       (10)

uniformly over all surviving components with that same actual port value m'.

## Scope and stopping boundary
This construction closes the statistical/combinatorial source-capture seam WITHOUT multiplying marginal laws. It receives genuine classical instrument semantics, the complete capture-port bound, and the quantum waiting logical-module condition as separate physical hypotheses. It does not prove those hypotheses, grant an ideal detector, supply autonomous scheduling, or implement the final dense frame. The final frame is an analysis/receiving statement until its actual operation or decoder interface is independently earned.
