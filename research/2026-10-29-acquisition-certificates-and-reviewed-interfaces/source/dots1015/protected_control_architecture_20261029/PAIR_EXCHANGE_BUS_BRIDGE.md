# A conditional pair-exchange bus closes the algebraic inter-block gate gap

2026-10-29. Author derivation; independent review pending. Known geometric-phase-gate mechanism specialized to the exact four-spin singlet control interface. No acquired hardware or novelty claim. Companion: PROTECTED_CONTROL_BRIDGE.md Sections2,3,6.

Let two four-spin blocks A,B have independent unknown collective spin baths, and encode in P_A tensor P_B. Let S_A=S12^A, S_B=S12^B; both commute with their block's collective generators and restrict to -Z_A,-Z_B. Assume a physical harmonic mediator with [a,a†]=1 and *supplied, calibrated* pair-exchange/oscillator couplings. During the gate, with other logical controls off, let

    H_gate = omega a†a + F(a+a†), F=g_A S_A+g_B S_B, omega>0.

The couplings involve two spins and the oscillator each, not a forbidden single-spin cross term. They preserve each block singlet sector at every instant. Add arbitrary collective bath couplings sum_(r,a) J_a^r tensor B_(r,a)(t) and bath-only H_M(t), provided H_M does not contain unknown oscillator interactions (known oscillator terms are already included). The collective B may act also on oscillator: these couplings vanish on P_A tensor P_B. The noncollective bath dynamics must not secretly alter H_gate. Initial logical/oscillator/memory/reference correlations are allowed on the protected spin support.

Set c=F/omega, b=a+c. Since F commutes with oscillator operators,

    H_gate=omega b†b-F²/omega.

The displacement D(c) obeys b=D(c)† a D(c), so the exact propagator is

    U(t)=exp(i F² t/omega) D(c)† exp(-i omega t a†a) D(c).

At T=2pi/omega, exp(-i2pi a†a)=I on the full oscillator Hilbert space. Thus

    U(T)=exp(i 2pi F²/omega²) tensor I_osc
        = exp[i 2pi(g_A²+g_B²)/omega²]
          exp[i 4pi g_A g_B S_A S_B/omega²] tensor I_osc.

The oscillator is returned exactly as an operator identity, even when initially correlated or not in its ground state. This is stronger than an assertion about a thermal mixture. With g_A=g_B=omega/4 the logical ZZ angle is pi/4, an entangling Clifford, in duration2pi/omega. Combined with the explicit protected X/Z rotations, this is an algebraic universal protected gate set under independent block collective noise.

The NEW RESOURCE is actual pair-exchange modulation by the oscillator coordinate. One possible microscopic route is an exchange splitting J(V) whose gate voltage includes an oscillator quadrature; linear expansion yields J'(V) v_zpf S (a+a†). It also yields static exchange and higher-order terms. Those cannot be dropped without a controlled expansion, accessible parameters, orbital/spin leakage bounds and energy range. For unknown locally twisted frames, the required scalar is S^V, not ordinary lab exchange. The geometric bus does not acquire frame-compensated interactions or prove that the endpoint noise model is instantaneous collective.

## Residual loop closure and noise are decisive

At a wrong duration or frequency the displacement does not close. For a force eigenvalue f the residual displacement magnitude is |f/omega| |1-exp(-i omega t)|. Different logical eigenvalues yield distinguishable oscillator trajectories. For an initially independent thermal state with mean occupation nbar, off-diagonal logical coherence between f and f' acquires magnitude factor

    exp[-(2 nbar+1) |(f-f')/omega|² |1-exp(-i omega t)|²/2].

This formula is only the stated thermal product model, not a bound for arbitrary correlated oscillator states. Any nonzero residual displacement can be distinguished nearly perfectly by sufficiently energetic oscillator states; hence the exact arbitrary-state cancellation is NOT uniformly robust to timing/frequency error without an energy/state promise. Damping, oscillator noise, unwanted number-dependent coupling and control amplitude error remain logical errors inside the singlet code and need their own acquisition/error budget. Code-membership measurement cannot detect them. An unknown bath term acting directly on the mediator is not removed by collective spin protection.

The simulated finite-cutoff diagnostic check_bus_gate.py uses40 Fock levels and audits input levels0–5 at g_A=g_B=omega/4. It reports return/operator error9.27e-15; this is not a proof for high oscillator occupation or a device fidelity. The completed-square proof above establishes the exact ideal infinite-mode statement.

## Primary antecedents and strongest comparator

Harvey et al., 'Coupling Two Spin Qubits with a High-Impedance Resonator', arXiv:1801.04858v4, https://arxiv.org/html/1801.04858, SectionII equations1–3 and AppendixB: explicit longitudinal spin-qubit coupling, closed-loop geometric phase and resonator damping. The microscopic expansion also contains number-dependent coupling; the authors state the approximation used to ignore it. This is a proposal/analysis, not evidence that our four-spin unknown-frame port is implemented.

Ruskov and Tahan, 'Modulated longitudinal gates on encoded spin-qubits via curvature couplings to a superconducting cavity', arXiv:2010.01233v1, https://arxiv.org/html/2010.01233, provides a related encoded-spin longitudinal mechanism and explicitly budgets resonator damping/noise and charge noise. Its encoded qubit choices and approximations must not silently transfer to our four-spin block.

An equally informed conventional exchange-only DFS architecture with these pair-bus controls implements the same gate. This derivation identifies a concrete compatible physical interface, but supplies no advantage over that comparator and no solution for unknown quantum-input loading, microscopic symmetry acquisition or practical residual noise. It is worth retaining because it replaces an unspecified direct four-spin entangler by a checkable mediator interaction rather than assuming global collectivity over all blocks.
