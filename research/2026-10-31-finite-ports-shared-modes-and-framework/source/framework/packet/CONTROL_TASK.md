# Robust entanglement with a moving uninitialised medium

This is a precisely defined hard SUBPROBLEM of Astra P2's original native interface, with known axes/gains granted to remove calibration as a confound. It is not a claim of acquired hardware or the complete P2 model. The goal is a reliable operation, not a new theory for its own sake.

Data qubits are 1 and 2, memory M is an uninitialised qubit together with an arbitrary finite-dimensional spectator, R an arbitrary reference. Write sigma_j for a Pauli operator tensored with the spectator identity. Known signed native Hamiltonians (identity factors omitted) are

A=X_1 tensor sigma_x, B=X_2 tensor sigma_y, C=Y_1 tensor sigma_z.

At most one handle is active at a time with real strength |u|<=1. Idle periods are allowed. The uncontrolled drift is I_D tensor H_M(t), with unknown piecewise-continuous time dependence. The supplied LOCAL motion promise is ||[H_M(t),sigma_j]||<=1 for j=x,y,z. There is no uniform bound on ||H_M||, spectator dimension, bandwidth or higher derivatives. The finite-dimensional propagator exists for each instance. The controller may choose a finite open-loop schedule using PRIVATE random coins. The adversary knows the randomized policy but H_M(t) is fixed independently of the realised private coins and initial data. A bath reacting to current private signs is a different noise game. There is no memory initialization, measurement, reset, reversal or direct control; no extra meter, ancilla, logical pulses or stronger instantaneous pulses. Only finite native evolutions, switching and classical schedule computation are provided.

Implement E=exp(-i*pi*Z_1 X_2/4) on data. For every epsilon>0, does a legal finite randomized schedule exist whose returned data+reference state, AVERAGED over the private coins and after discarding M, is within trace-norm error epsilon of applying E to the original data+reference state, UNIFORMLY for every admitted H_M and every initial joint rho_DMR? Bath-only final evolution is free/irrelevant; demanding the bath remain unchanged would create an artificial no-go. Equivalently compare the averaged channel DMR->DR with Ad_E composed with trace_M in diamond norm. This is a channel guarantee, not a claim for every individual coin realization.

A positive result must give the schedule/family and actual total duration, switching count and parameter-precision scaling with epsilon, respecting strength one and the local-motion promise without importing a bound on ||H_M||. A negative resolution needs a quantitative lower error bound for ALL admitted randomized policies, including arbitrarily long finite words, with the bath independent of private coins. A scope-limited new theorem can be progress, but defeating one echo, replacing arbitrary time dependence by a frozen bath, or proving deterministic exact impossibility again does not settle this approximate task.

Already known and supplied:

1. There is no drift-free controllability gap. With U_J(t)=exp(-itJ), the exact identity

U_A(pi/4) U_C(pi/4) U_B(-pi/4) U_C(-pi/4) U_A(-pi/4)=E tensor I_M

holds (rightmost factor acts first). It follows by two Pauli conjugations; an exact 8x8 check also confirms the signs. Total absolute native time is 5*pi/4. Large blind commutator words are not the correct ordinary baseline in this granted-information subproblem.

2. A simple perturbation bound scales with total time times drift norm and is unavailable uniformly under the local-motion promise. Ordinary decoupling and dynamically corrected gates need their actual error-strength, control and temporal hypotheses; rapid switching of bounded-strength handles does not supply instantaneous pi pulses. Quasistatic/slow-bath results cannot silently become guarantees for arbitrary time dependence. The interaction-frame sigma_j(t) still have norm one and are Lipschitz under the stated local commutator bound; their simultaneous Pauli algebra is preserved.

3. EXACT zero-error deterministic finite-word universality is already obstructed in the qubit subcase. If U_h(T)=E tensor V_h for every h, differentiation with respect to arbitrary localized drift perturbations forces U_0(t)^dagger(I tensor sigma_k)U_0(t) to remain in the memory algebra at every t,k. Thus U_0(t) must always normalise that algebra, hence factorise across D|M. Any nonzero native interaction violates that condition. This preflight lemma excludes deterministic exact finite universality; it does NOT resolve approximate randomized reachability.

4. P2's latest positive operator-force result is a different qualified interface: H=H_M+p^2/(2m)-Q tensor G_M(t) tensor x with g_- I<=G<=g_+ I and a momentum-band source/readout. It gives an instrument K_q=Pi_q tensor V_q, tolerates noncommuting bath motion, and composes into quantum operations. The original A/B/C handles do not supply that positive parity force, meter or coherent readout by declaration. Its complete visible final is included under `control/`; use it as a scientific contrast, not a legal new operation in this task.

An UNPROVED preflight foothold is available equally to all constructors: weak nested commutator cycles with private signs s_A,s_B uniform and s_C=s_A*s_B retain a third-order ABC term while cancelling some lower-order sign monomials. A drift-free ten-segment nested word has log W=-4i*delta^3*Z_1 X_2+O(delta^4), up to orientation. No uniform joint-channel estimate for the moving, correlated medium under the stated local promise is supplied. Averaging a unitary or its Hamiltonian is not the averaged quantum channel. Treat this as a conjectural route to prove, reject or replace, not an established answer. An actual useful resolution must control accumulated error throughout repeated cycles and give finite resources.

You own the proof/control representation. Consider a genuinely different organising object if useful, and seriously challenge your strongest candidate against the full operational contract. Do not identify outcome probabilities with a coherence-preserving instrument, infer a uniform theorem from finite drift samples, or assume a missing physical interface. A useful new barrier theorem is allocation information rather than an enabled quantum computer.

The packet includes source records for the original native handles and the new force-based instrument. All gains and Pauli axes in this subproblem are explicit; no hidden geometry or expensive calibration is needed. Develop one substantial construction or argument with its actual scope, retaining rigorous partial progress if the full frontier remains open.
