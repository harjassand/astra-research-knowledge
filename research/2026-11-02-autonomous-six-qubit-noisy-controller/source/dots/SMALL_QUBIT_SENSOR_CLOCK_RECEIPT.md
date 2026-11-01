# Explicit TP sensor clock and malformed-state domination — constructive receipt

2026-11-01. Scope: the ACTUAL small-qubit clock generator, all legal endpoints, malformed states, and arbitrary clock coherences. The sensor readiness/collision Poisson inequalities and full memory join are separate obligations. No hardware action or external source retrieval.

## Result first

The mode/domain-wall encoding works for the proposed unflagged sensor, with explicit at-most-six-qubit gate-labelled GKSL jumps. No complete-phase M-qubit projector is used by the generator. Every legal state has exactly its intended next phase. All deviations from the decoded ideal sensor cycle are supported on inversion I_clk>0, and their action on a fixed bounded local potential is dominated by a finite constant times I_clk. Three-qubit sorting leaves every decoded-phase-dependent term unchanged and supplies exact negative inversion drift.

Important bookkeeping correction: M forward operations plus forward endpoint flip, M return operations and return endpoint flip form a cycle of 2M+2 legal phases. With one slow idle departure and all remaining transitions at k, the effective number of fast phases is m_eff=2M+1. Recompute every own/pair Poisson price for THIS cycle, including readout before the return leg.

## 1. Native clock states and jumps

Physical clock qubits: mode b and c_1,...,c_M. Define analysis variables x_i=c_i XOR b, x_0=1, x_(M+1)=0, rank r_x=Σ_i x_i. A legal word is x=1^r_x0^(M−r_x).

For every b∈{0,1} and j=1,...,M define G_bj as the computational-basis projector onto mode b and the local decoded pattern

(x_(j−1),x_j,x_(j+1))=(1,0,0).

Sentinels are constants and omit the corresponding physical qubit. Thus G_bj uses at most mode plus three adjacent c qubits. Define S_bj=X_(c_j)G_bj. For a TP local phase instrument {K_bj,μ}, use jumps

L_bj,μ=√λ_bj S_bj⊗K_bj,μ,
Σ_μ K_bj,μ†K_bj,μ=I,
λ_0,1=r_slow, all other λ_bj=k.

Assume 0<r_slow≤k. The return-mode instruments K_1j are identity. The forward instruments are specified below. All outcomes advance the clock; no postselection or data-conditioned rate is introduced.

At each endpoint use a separate directed mode jump

E_b=√k X_b |b><b|_b 1_(c_M XOR b=1).

Its support is two clock qubits. It has identity quantum instrument. In particular NO probe reset is hidden in the endpoint. If a different endpoint instrument is desired, it must be included in the ideal decoded-cycle source equations and malformed bound explicitly.

For each i=1,...,M−1, sorting uses the three-qubit jumps

R_bi=√ν SWAP_(c_i,c_(i+1)) |b><b| 1_(x_i x_(i+1)=01).

Every generator term is D[L](ρ)=LρL†−{L†L,ρ}/2. No rate depends on the quantum state.

## 2. A concrete forward sensor instrument list

For a check of weight w, take M=w+2:

j=1: finite-impurity probe preparation;
j=2,...,w+1: the successive controlled-Pauli factors;
j=M: X-probe readout and unconditional overwrite of its cache.

Preparation to ρ_p=(1−ε)|+><+|+ε|−><−| has Kraus

K_(s,t)=√p_s |s_X><t_Z|, s∈{+,-}, t∈{0,1}.

This is TP on ANY incoming probe state. It is not a pure reset assumption; ε is an actual preparation parameter paid by the source budget.

For ideal X readout/cache write, let P_s^X be the probe projector and encode s as a cache computational bit. Use

K_(s,t)=P_s^X⊗|s><t|_cache, s,t∈{0,1}.

For classical detector confusion p(o|s), replace this by

K_(s,t,o)=√p(o|s) P_s^X⊗|o><t|_cache.

These maps are TP even for coherent/entangled probe/cache inputs. All s,o,t branches use the SAME clock transition and their rates sum to λ_bj G_bj, not an extra rate per outcome. Detector error remains separately charged; accepting wrong reports is not postselection.

A controlled-Pauli has one probe plus one data qubit. Readout has one probe plus one cache. Thus the maximum support is four clock qubits plus two quantum qubits = SIX physical qubits. Preparation uses at most five; endpoint two; sorting three. The mode qubit has O(M) incidence and every ancilla, gate channel and rate is paid. This is a bounded-arity GKSL construction, not a microscopic two-body reservoir synthesis.

## 3. Legal-sector proof and endpoints

If x=1^r0^(M−r) with r<M, precisely j=r+1 satisfies 100 (with sentinels). Its flip makes rank r+1. The endpoint guard x_M=1 is false. If r=M, no wall guard is enabled and precisely E_b is enabled. Flipping b complements all decoded x_i, so all ones become all zeros and (b,M)->(1−b,0).

Hence every legal state has EXACTLY one intended outgoing phase, all legal transitions remain legal, and neither mode endpoint can accidentally fire early on a legal clock. The idle state is (b=0,r=0); only its departure has rate r_slow. The return path, including (b=1,r=0), runs at k.

The legal cycle is

(0,0)->...->(0,M)->(1,0)->...->(1,M)->(0,0).

Its active fraction, if every nonidle phase is conservatively called active, is

f=(2M+1)r_slow/[k+(2M+1)r_slow].

Readout occurs on (0,M−1)->(0,M), not at the final cycle endpoint. Readiness killing and post-readout prices must use that exact location. A narrower forward-only overlap indicator can be used only after recomputing its Poisson problem; the all-nonidle indicator is an available upper-bound convention.

The completed controlled-check prefix commutes with the physical stabilizers and logicals assumed by the sensor construction. Therefore switching to identity return dressing is legal for those observables. Sorting and malformed domination below need only that every chosen observable is a function of decoded phase (b,r) and the quantum state; they do not reprove the source's completed-check commutation premise.

## 4. Exact malformed combinatorics

Define

I=Σ_(i<j)(1−x_i)x_j, N01=Σ_i 1_(x_i x_(i+1)=01).

I=0 exactly on legal prefixes. Every malformed binary string has N01≥1. Every adjacent 01->10 swap preserves rank and mode and decreases I by EXACTLY one. Hence sorting preserves every own-clock price, pair-clock price, readiness term and prefix/global dressing that depends only on decoded phases.

For M≥2, the sharper uniform bound is

I≤C_M N01, C_M=floor(M²/4).

The looser M² bound in the root draft is safe. For a wall flip at j,

ΔI=#zeros before j − #ones after j,

so |ΔI|≤M−1. For a mode flip, rank becomes M−r and

I'=r(M−r)−I, ΔI=r(M−r)−2I,

so |ΔI|≤floor(M²/4). Every positive ΔI has a malformed SOURCE. Let Δ_M=max(M−1,floor(M²/4)). There are at most M wall channels and one endpoint channel enabled at a given configuration; their total rate is at most (M+1)k.

A premature endpoint on a malformed string is a real erroneous operation/phase jump. It is covered by these bounds, not called harmless. It may even turn the malformed source into a legal target; support of the error is the source projector I>0.

## 5. Why arbitrary clock coherences do not invalidate the bounds

All observables considered here are diagonal in the COMPLETE physical clock basis, with operator-valued quantum blocks V(c). This allows arbitrary off-diagonal clock density matrices; it is not an assumption that the state is classical.

For each separately labelled b,j or b,i transition, the clock source-to-target map is injective. For each instrument Kraus operator,

L† V L =Σ_(c in source) |c><c|⊗K†V(c')K.

There are no cross terms between distinct source clock configurations because target configurations are distinct. The anticommutator is likewise clock-diagonal, and TP gives Σ_μ L_μ†L_μ=λ G. All legal/malformed sector estimates are therefore OPERATOR inequalities on arbitrary clock/data/bath states.

For a scalar clock function h, TP reduces the adjoint exactly to the corresponding finite classical generator on the clock populations. Even if sensor quantum systems overlap, their nominal clock population generators are independent because no guard involves another sensor and all instruments are TP. This does not assume independent quantum errors. Physical clock-noise perturbations can spoil the independent stationary law; they belong to the separate admission, and malformed ideal activity is handled below.

## 6. Actual-minus-decoded generator bound

Let V0=W_dressed+Z be the base plus all finite sensor/pair/Boolean prices, with every block depending on physical clocks only through their decoded phases. Define the DECODED reference adjoint blockwise: at phase (b,r) apply its ONE prescribed ideal cycle transition and TP instrument. This is an analysis map, NOT a hidden native M-bit predicate. It can equivalently be lifted with separate Kraus operators for each full clock basis state and any canonical target representing the intended next phase.

On every legal source clock, the actual adjoint and decoded adjoint agree exactly. On malformed sources, include every potentially wrong gate, premature preparation/readout, extra enabled wall and premature endpoint. Only a fixed neighborhood of potential terms can be affected. Let B_g bound the norm of each actual/reference change in the sum of these affected terms. For positive finite price terms one may use twice their summed norm; for extensive base W use ONLY the finite affected W terms, never ||W||=O(n).

Because a TP map has unital contractive adjoint, a conservative comparison is

L_(g,clock)* V0 ≤ A_(g,decoded) V0 + D_g 1_(I_g>0)
                           ≤ A_(g,decoded) V0 + D_g I_g,
D_g=(M+2)k B_g.

The M+2 accounts for at most M+1 actual channels and one reference channel. B_g includes changes of neighboring readiness/pair prices touched by that gate. It can depend on A/r_slow and the fixed sensor graph degree; it is independent of total code size. This comparison isolates CLOCK MALFORMATION. Genuine collisions between two legal active sensors are not asserted to be supported on I>0; they remain the root's separate overlap-price term.

Summing the root's decoded source/Poisson inequalities blockwise is legitimate if those inequalities hold for every decoded phase and every quantum state. No stationary sampling assumption is needed for the centered Poisson identity. Its price must use the corrected 2M+2-state cycle.

## 7. Sorting pays the complete malformed contribution

Sorting leaves V0 EXACTLY unchanged and

L_sort*(a_clk I_g)=−ν a_clk N01_g
                 ≤−ν a_clk I_g/C_M.

Nonsorting ideal clock transitions can add at most

a_clk(M+1)k Δ_M 1_(I_g>0)
≤a_clk(M+1)k Δ_M I_g

to the inversion penalty. Hence, for M≥2,

L_actual*(V0+a_clkΣ_g I_g)
≤Σ_g A_(g,decoded)V0
 +Σ_g [D_g+a_clk(M+1)kΔ_M−ν a_clk/C_M] I_g.

Choosing a finite sorting rate satisfying

ν a_clk/C_M ≥ D_g+a_clk(M+1)kΔ_M+margin

uniformly over sensor types removes the positive malformed-sector remainder. Every term in D_g and every hardware noise contribution from that larger ν must be paid. Making a_clk small by increasing ν is not free suppression of physical sorter errors.

For M=1 there are no malformed states, so no sorting bound is needed. Real check sensors have M≥3.

## 8. Exhaustive finite verification

Executed clock_audit/verify_guards.py for ALL c∈{0,1}^M, b∈{0,1}, M=1,...,12: 16,380 configurations total. Results: PASS.

Verified: legal iff I=0; exactly one intended legal successor; legal successor remains legal; every malformed string has an adjacent 01; sorting preserves rank/mode and drops I by one; I≤floor(M²/4)N01; wall/mode inversion formulas and bounds; any positive inversion increment has malformed source; each separately labelled native clock map is injective. Detailed counts are in clock_audit/guard_results.json. This enumeration checks the implementation guards and endpoint cases, not the full sensor/readiness operator inequality.

## Frozen scope

This receives the actual small-qubit clock MALFORMED-STATE DOMINATION subproblem at the stated bounded-arity GKSL level. It does not certify the root's neighboring-sensor readiness bound, the size of its Poisson prices, a full protected-memory theorem, a microscopic two-body implementation or competitive constants. All quantum-state coherence assertions here are operator-level. No clean global clock, clean controller reset, trusted invalid flag or complete M-qubit phase predicate was inserted.
