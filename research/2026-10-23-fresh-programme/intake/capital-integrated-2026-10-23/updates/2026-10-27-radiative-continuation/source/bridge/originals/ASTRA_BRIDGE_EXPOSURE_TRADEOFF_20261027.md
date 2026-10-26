# ASTRA foundational physics — exact low-exposure transfer through a lossy bridge

27 October 2026. Independent continuation from `ASTRA_FINITE_TIME_JACOBI_FLAG_GATE_AND_LOSS_20261026.md`. All assertions refer to explicitly declared Hamiltonians, not an acquired optical device or historical priority. Code and executed JSON are in `astra_bridge_transfer/`.

## 1. Scientific choice and prior art

The existing strictly positive, gapless Jacobi capture is almost optimal **when the captured target itself is the exposed emitter**: for a one-port coupling-vector norm at most `G`, capture from outside requires emitter population-time at least `pi/(4G)`. The practical bottleneck is therefore topological. I tested an alternative in which the matched photon is captured on a separate buffer `a`, travels through a radiative intermediate `e`, and is held on protected storage `b`. The path has no direct `a-b` hopping. The full operation is capture, exact `a->b`, conditional `b` phase, reverse `b->a`, release.

Known, relevant physics: STIRAP, invariant-engineered nonadiabatic population transfer and shortcut-to-adiabatic passage; see Xi Chen and J.G. Muga, PRA 86, 033405 (2012), DOI 10.1103/PhysRevA.86.033405; Li and Chen, PRA 94, 063411 (2016), DOI 10.1103/PhysRevA.94.063411; Song et al., Optics Express 29, 7998 (2021), DOI 10.1364/OE.417343. Those antecedents mean the three-level transfer idea must NOT be represented as historically new. The scoped additions here are the positive Jacobi/gapless source composition, a sharp interface-conditional occupation-time bound, exact finite-time pulses with and without switch discontinuities, capacity preservation, calibration echo, and full-photon radiation calculations.

## 2. Arbitrary-mediator exposure/time lower bound

Decompose a one-excitation Hilbert space as `P H = span{|a>,|b>}` and `Q H = P^perp`. Assume (i) the controlled `P` block has no `a-b` coupling (it may have independent on-site phases), (ii) `||P H(t) Q||<=Omega` for every `t`, and (iii) an initial `|a>` is transferred exactly to `e^{i alpha}|b>` at a finite time `T`. Let `p_Q(t)=||Q psi(t)||^2` and `A_Q=int_0^T p_Q(t)dt`. If `p_Q(t)<=epsilon<1` at all times, then

    A_Q*T >= pi^2*(1-epsilon)/(4*Omega^2).                (1)

**Proof.** Gauge away the diagonal (non-mixing) `P` block by its local propagator. Writing `x(t)=P psi(t)`, Schrödinger evolution gives `||dot x|| <= Omega sqrt(p_Q)`. With `r=||x||=sqrt(1-p_Q)` and `u=x/r`, the Fubini–Study speed obeys `||P_{u^perp} dot u|| <= Omega sqrt(p_Q/(1-p_Q))`. The initial and final normalized `P` rays are orthogonal, so their Fubini–Study distance is `pi/2`. Integrate and apply the uniform occupancy limit and Cauchy–Schwarz:

    pi/2 <= Omega/sqrt(1-epsilon) * int sqrt(p_Q)
          <= Omega sqrt(T*A_Q/(1-epsilon)).

This proves (1). It applies to any dimension of the mediator `Q` and any internal mediator Hamiltonian. It does **not** apply if there is direct mixing within `P`, unbounded coupling, or another bypass channel. In particular `A_Q=0` is impossible for finite `T` and finite `Omega` without a bypass.

## 3. An exact finite-time transfer asymptotically saturating (1)

Set `B=1` and write the controlled three-site Hamiltonian in the one-photon sector as

    H(t) = mu I + g(t)(|a><e|+h.c.) + J(t)(|e><b|+h.c.).

At all times require `sqrt(g^2+J^2)<=Omega`, and choose `mu=Omega+1` so the complete 3x3 Hamiltonian is positive with eigenvalues at least `1`. For `0<phi<pi/2` construct three stages (in the rotating frame of `mu`):

1. `g=Omega, J=0` during `phi/Omega`. The state becomes `cos(phi)|a> - i sin(phi)|e>`.
2. For `theta:0->pi/2` at `dot theta=Omega tan(phi)`, choose `g=Omega sin(theta), J=-Omega cos(theta)`. The **exact** evolving state is `cos(phi)cos(theta)|a> - i sin(phi)|e> + cos(phi)sin(theta)|b>`.
3. `g=0,J=-Omega` during `phi/Omega`, bringing the state exactly to `|b>`.

The ideal transfer time and intermediate population-time are

    T_fast = pi/(2 Omega tan(phi)) + 2phi/Omega,
    A_fast = [(pi/2)sin(phi)cos(phi)+phi-sin(2phi)/2]/Omega.  (2)

Here `max p_e=sin^2(phi)` and `A_fast*T_fast -> pi^2/(4Omega^2)` as `phi->0`. Therefore the lower bound (1) is asymptotically attained in its declared small-intermediate-occupation regime, with no direct `a-b` edge. The ideal reverse is the time reversal with both couplings sign-inverted, not the same pulses run backward with unchanged signs. The fast protocol has abrupt changes between stages and is a comparison, not a manufacturing-ready waveform.

For `Omega=10, phi=0.10`, `T_fast=1.5855568`, `A_fast=0.015669986` per transfer (two-transfer exposure `0.031339972`), versus previous emitter/store swap exposure `2.45867624` on the emitter. The maximum intermediate occupation is `0.0099667`. Executed 3x3 integration checks all stages and the reverse to approximately `1e-14`.

## 4. Smooth exact construction without bridge-edge discontinuities

For `s=t/T` in `[0,1]`, define

    theta(s) = (pi/2)[s - 2 sin(2 pi s)/(3 pi) + sin(4 pi s)/(12 pi)],
    phi(s) = Phi sin^2(pi s),
    theta_s = (4pi/3) sin^4(pi s), phi_s = Phi pi sin(2pi s).

The desired exact state is

    psi(s) = cos(phi)cos(theta)|a> - i sin(phi)|e>
             + cos(phi)sin(theta)|b>.

Direct substitution into Schrödinger's equation gives continuous, real controls

    g(t) = [theta_s sin(theta)cot(phi) + phi_s cos(theta)]/T,
    J(t) = [-theta_s cos(theta)cot(phi) + phi_s sin(theta)]/T. (3)

The apparent divisions by zero at endpoints cancel: `theta_s=O(s^4)` and `phi=O(s^2)`, so `g(0)=J(0)=g(T)=J(T)=0` by continuous extension. Choose

    T = (1/Omega) max_{0<=s<=1} sqrt[(theta_s cot(phi))^2+phi_s^2].
    A_e = T int_0^1 sin^2(phi(s)) ds.                     (4)

Then `sqrt(g^2+J^2)<=Omega`; the exact state starts in `|a>` and ends in `|b>`. At each time the three-site Hamiltonian shifted by `mu=Omega+1` is positive with smallest eigenvalue >=1. Arbitrary common positive on-site ramps between the capture and bridge stages commute with the internal transfer up to a known scalar phase while the lead port is switched off.

For `Omega=10,Phi=.23`, executed high-precision ODE checks give

    T=1.78898524507337, A_e=0.03503533664073,
    two-transfer exposure=0.07007067328145,
    max p_e=sin^2(.23)=0.051994...,
    transfer state norm error <9e-15.

For `Phi=.5`, `T=.76675290386909`, two-transfer exposure `.1352669146591`; it is faster but populates the lossy intermediate more. Smooth controls sacrifice some asymptotic time-exposure optimality to remove instantaneous bridge-edge changes. The remaining initial buffer-to-lead decoupling is still an independent timed control.

## 5. Complete conditional wavepacket operation and exact all-sector positivity

Use the pre-existing (independently re-read) half-line Jacobi photon source with boundary `|a>`:

    h_capture = I + 0.7 (|a><1|+h.c.)
                  +0.5 sum_{j>=1} (|j><j+1|+h.c.).

Its essential spectrum is `[0,2]`; its zero-energy Schur margin on `a` is `1-2(0.7)^2=.02>0` (this is **not** a global positive spectral gap). An exact zero of the boundary return amplitude occurs at `T_cap in (2.433886050,2.433886053)` as proved by the original rational-moment certificate. The time-reversed source wavepacket has no `a` amplitude. Restricting it to the first 16 lead sites gives the original rigorous phase-error allowance `<2.40e-8`.

After capture, switch the `a`–lead edge off, perform bridge transfer, hold `b` with `U r n_b` for `pi/U` with `U=1`, perform the adjoint bridge, and release with the same Jacobi generator. All distinct stages have nonnegative one-photon Hamiltonians: `h_capture>=0`, bridge 3x3 block >=I, isolated lead >=0, and hold terms positive. Second quantization preserves positivity in every photon sector. With `m` conserved two-level memory sites of energy `-1`, positive Boolean-control penalties, and neutral flag spins, the full instantaneous Hamiltonian satisfies `H_N(t)>=-min(N,m)` for all finite `N`; equality of infima at every control instant is **not** needed or claimed. At photon-vacuum-free stationary stages with zero-energy memory states, the corresponding `-min(N,m)` thresholds are attained in the thermodynamic lead limit.

For an exact capture, the composite photon `root=0` operation has a common outgoing waveform, and `root=1` gives its negative. With the finite 16-site source the relative error is at most `2delta_L<2.40e-8`. Full `N_signal=72` state propagation gave ideal root-relative errors approximately `2e-13`. The Boolean flag computation and its adjoint were separately established in the previous work; they require no photon–flag interaction while the photon is being transferred, and are inputs to this composition. Source generation, gate tuning and flag preparation are not free resources.

## 6. Independent radiation calculations and spectral completion

**Effective Markov comparison.** Explicit orthogonal quantum-jump outputs are included by the complete no-jump amplitude identity `epsilon_full^2=2-2Re<psi_ideal|psi_nojump>`. A smooth `Phi=.23,Omega=10` operation takes `11.587335 B^-1` (including two captures and the conditional hold) and produces, for `kappa_e=2e-5`, `kappa_a=kappa_b=1e-6`, a full state-vector error `0.00321753` for either root. If the buffer rate is `2e-5`, it rises to `0.00934911`. These are effective Markov-model results, not a positive-frequency microscopic radiation derivation.

**Closed positive-frequency radiation bath.** Give the mediator `e` a *permanent* coupling `eta` to the first site of an additional harmonic Jacobi radiation lead:

    h_rad = w I + (w/2) sum_{j>=1}(|j><j+1|+h.c.),
    H_e-rad = eta (e^* c_1+c_1^* e).

The radiation spectrum is `[0,2w]`, down to zero, and its endpoint zero-energy inverse is `2/w`. Thus the isolated `e` sector during capture/hold has Schur margin `1-2 eta^2/w`; the bridge's full local Schur block has margin at least `1-2eta^2/w` due to its uncoupled lower bound `I`. This proves positivity of the entire time-dependent single-photon Hamiltonian in every stage. The radiation coupling cannot be postselected away; its outgoing excitation remains in the full Hilbert space.

At `w=11`, choose `eta=sqrt(5.5e-5)=0.007416198...`, so the surface Green function gives the midband decay scale `Gamma_mid=4eta^2/w=2e-5`. The radiation band `[0,22]` contains the bridge's excitation energies. Executed full closed-system evolution (65 signal sites, 180 radiation sites) at smooth `Phi=.23` gives, comparing to the no-radiation reference:

    root=0 full state deviation: 0.0011734784,
    root=1 full state deviation: 0.0011734793,
    root-relative conditional sign error: 0.0016595497,
    radiation output probability: about 1.37705e-6.

All these are **finite-time, finite-length numerical calculations**, not interval-certified continuum scattering theorems. A contrasting `[0,2]` narrow radiation band produces a much smaller deviation, but that depends on excluding bridge frequencies and cannot be exported to broadband free-space radiation.

**Exact all-frequency radiation bound.** For *any* positive self-adjoint radiation Hamiltonian initially in the vacuum, with bounded source coupling `eta |e><c_1|+h.c.`, Duhamel relative to the radiation-free ideal path gives

    ||psi_eta(T)-psi_0(T)|| <= |eta| int_0^T |<e|psi_0(t)>|dt.

For two smooth bridge transfers, the emitter is unoccupied on the other ideal stages, yielding

    epsilon <= 2|eta| T_bridge int_0^1 sin(Phi sin^2(pi s)) ds
            + explicitly retained source/truncation errors.        (5)

At `Phi=.23,w=11,eta=.0074162` the first term is `0.00303474` per root, a rigorous bound independent of the radiation spectrum or size; the executed error `0.001174` lies below it. The ideal conditional sign error (both roots combined) is at most twice the one-root Duhamel allowance plus the finite-source error. This statement applies to the **full** photon + radiation output without conditioning on a surviving signal photon.

The finite radiation and signal-chain truncations are distinct from long-time scattering. Their distant ends lie well beyond the ballistic propagation regions on the simulated time interval. No asymptotic S matrix for a finite chain is asserted.

## 7. Calibration echo and its failure scope

Let `V` be the actual forward bridge unitary and implement its actual adjoint `V^dagger` after the conditional storage hold. If the storage phase is `Z_b=I-2|b><b|`, then the two root branches on the initial buffer obey the **exact** identity

    ||(V^dagger Z_b V + V^dagger V)|a>||
       = 2 sqrt(1-|<b|V|a>|^2).                          (6)

This proves that **repeatable forward control miscalibration does not accumulate separately in the return path**; the relative oracle error is determined by the transfer population. It is valid for any common coherent miscalibration for which the reverse is truly the adjoint, not merely the nominal reverse.

Executed smooth bridge control tests at `Omega=10,Phi=.23`:

- `+0.1%` multiplicative miscalibration of **both** edges: root-relative error `0.00054922`; root-zero return error `~7e-15`.
- `+0.1%` first edge and `-0.1%` second: relative error `0.00155929`; root-zero echo remains accurate.
- Unreversed residual emitter detuning `0.005`: root-zero return error `0.00056984` and relative error `0.00044941`. The detuning does *not* echo unless its sign is also reversed; a nominally symmetric schedule is not automatically an inverse.

This correction matters for real devices: onsite drift, off-resonant spectators, photon dephasing and environmental loss are not cured by pulse reversal.

## 8. Exact inverse without changing physical hopping signs

A new control simplification removes the need to invert the signs of the two physical hopping amplitudes. Let `Z_e=I-2|e><e|=exp(i pi n_e)` on the one-photon three-mode space. For every real `g(t),J(t)` and no uncompensated intermediate detuning,

    Z_e [g(t)X_ae+J(t)X_eb] Z_e = -[g(t)X_ae+J(t)X_eb].

If `F` is the actual forward bridge evolution and `R_same` runs its *actual* hopping profile in reverse chronological order but **without sign changes**, then

    F^dagger = Z_e R_same Z_e.                              (7)

The identity follows directly from time ordering and conjugation. It holds even if the physical hopping envelopes suffer any repeatable multiplicative calibration error, provided the reverse uses the same actual envelopes. Thus the exact return can use only the original hopping signs, reversed chronological shape, and two one-site phase operations on `e` when the bridge hopping edges have reached zero. Such phase operations can be implemented by positive onsite Hamiltonians; their amplitude, duration and dephasing must still be counted. Because `e` is ideally empty at both endpoints, these local phase operations add no ideal intermediate-emitter occupation.

An independent integration of the actual three-mode propagators verified (7) with operator-norm residual `<5e-13` under both perfect controls and `1%` common or differential hopping miscalibration. The root-zero echo remained accurate to `<1.4e-14` on its initial state. **Decisive failure:** an unreversed intermediate onsite offset `0.02B` is invariant under `Z_e` and causes a root-zero return error `0.00227929`; the identity does not cancel unknown diagonal drift.

This is a chiral/gauge symmetry of the bipartite **controllable three-site** Hamiltonian, not a new form of electromagnetic reciprocity or a cancellation of radiative loss. In the permanent radiation model, `Z_e` also reverses the sign of the uncontrollable `e-c_1` coupling while leaving the radiation bath Hamiltonian unchanged. Therefore (7) is **not** an exact reversal identity for the full photon-plus-radiation Hamiltonian; the full-model deviations have to be bounded by Duhamel or directly computed as in Section 6.

## 9. A genuine two-level intermediate preserves all-particle stability

The lossy mediator need **not** be an unbounded harmonic oscillator. Let `h(t)>=0` be any of the constructed positive one-photon matrices, including the radiation continuum if present, and let `P_N` project its bosonic `N`-particle sector to occupancy `n_e<=1`. The physical model with an ordinary two-level emitter `sigma_+`, `sigma_-` is exactly

    H_TLS,N(t) = P_N dGamma_N(h(t)) P_N

as an operator on the allowed Hilbert subspace, if the two-level transition has the oscillator-ladder coefficient `1` between occupations zero and one and has no extra negative interaction. Compression preserves form positivity: `H_TLS,N(t)>=0` for **every finite N**. Thus the photon/memory sector lower bound `H_N(t)>=-min(N,m)` survives replacing the intermediate oscillator by a saturable two-level emitter. The controlled one-photon protocol is unchanged because the one-excitation sector never populates `n_e>1`.

This is a scope-limited all-particle stability argument, **not** a claim that the multiphoton dynamics remain quadratic after imposing the cap. An independent finite-Fock audit with eight one-body modes and one hard-core emitter reconstructed complete sectors through `N=4` (maximum 294-dimensional) at three hopping angles. All lowest eigenvalues were positive, agreeing with the compression theorem. The theorem itself, not the finite matrices, establishes all-`N` positivity.

## 10. Meaning, resources and decisive limitations

1. The new **universal conditional** principle is the Fubini–Study exposure-time bound (1), which is close to sharp for an explicitly local positive 3-mode Hamiltonian. STIRAP/inverse-engineering as a general mechanism is conventional prior art, not a new physical law.
2. The smooth construction makes low intermediate exposure compatible with exactly zero hopping amplitudes at transfer endpoints. The lead–buffer edge still requires separate time switching; positive common on-site energies must be raised to `mu=Omega+1`, e.g. `11B`, as a control/work resource. Sign reversal of the physical hopping controls can be replaced by the one-local phase-echo identity (7), but the phase-pulse strength, any uncorrected onsite detuning and actual energy slew are still resources.
3. The captured buffer must itself be sufficiently low-loss. If it has the same independent radiative loss as the old emitter, much of the advantage disappears; this is exposed numerically by the dark/bright buffer comparisons, not silently assumed away.
4. The microscopic spectral bath is a **controlled lattice model**, not an acquired Maxwell radiation continuum. Broadband electromagnetic reservoirs could have significant additional modes; the especially favorable narrow-band bath must not be treated as typical.
5. Time-domain sources, timing, leakage into higher photon sectors, flag availability, finite-temperature preparation and hardware control-noise spectra remain unacquired. Exact one-photon transfer and a lower bound do not establish a practical advantage or a new fundamental force.
6. The strongest next distinct physical attack is to derive a passive low-loss guided buffer and tunable, signed two-edge transfer from one electromagnetic/electronic microscopic platform, with independent emission and root coupling included. If that interface cannot be acquired, (1) and the buffer-loss floor delimit how far this approach can progress.

## 11. Executed, accessible source files

All scripts were actually executed with SciPy/NumPy; the JSON files record their numerical outputs and assumptions.

- `astra_bridge_transfer/bridge_protocol_audit.py` and `bridge_protocol_results.json`: exact three-stage transfer, bridge occupation integral, Markov full-output conditional gate.
- `astra_bridge_transfer/smooth_exact_bridge.py` and `smooth_bridge_results.json`: endpoint-smooth exact invariant path, norm bounds, positive control.
- `astra_bridge_transfer/smooth_full_gate_audit.py` and `smooth_full_gate_results.json`: actual matched Jacobi photon capture/release and conditional root phase with full Markov output error.
- `astra_bridge_transfer/microscopic_radiation_audit.py` and `microscopic_radiation_results.json`: positive gapless, **narrow** radiation bath, full closed output.
- `astra_bridge_transfer/wideband_radiation_audit.py` and `wideband_radiation_results.json`: positive gapless **wide** radiation bath and full closed output.
- `astra_bridge_transfer/bridge_control_robustness.py` and `bridge_control_robustness_results.json`: exact return-echo identity and deviations from its assumptions.
- `astra_bridge_transfer/one_local_echo_inverse.py` and `one_local_echo_inverse_results.json`: positive one-local phase replacement for sign-flipped hopping controls, and exact unmatched-detuning failure.
- `astra_bridge_transfer/hardcore_intermediate_fock_audit.py` and `hardcore_intermediate_fock_results.json`: real two-level mediator as an exact all-sector compression and independent finite-Fock cross-check.

No permanent repository write has been made in this continuation; these are currently conversation-accessible files.
