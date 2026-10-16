# Finite-rate parity-dephasing interface with an arbitrary finite bath

## Main result
Let S=S†, S²=I be a fixed parity involution on a finite-dimensional joint system (data, persistent bath, and optional reference). Consider

ρ̇ = −i[H₀(t)+V(t),ρ] + γ(SρS−ρ),

where γ>0, [H₀(t),S]=0, {V(t),S}=0, and ||V(t)||∞≤J. Hamiltonians may be time-dependent and noncommuting at different times, provided their finite-dimensional propagators exist. There is no bound on the bath dimension or ||H₀|| in the result. Define the pinching P(A)=(A+SAS)/2 and Q=I−P. Suppose Pρ₀=ρ₀. If U₀ is the H₀ propagator, then

(1/2)||Pρ(t)−U₀(t,0)ρ₀U₀(t,0)†||₁ ≤ ε(t),

ε(t) = (J²/γ)[t−(1−e^(−2γt))/(2γ)] ≤ min(J²t², J²t/γ).

One can cap any resulting probability or state trace distance at 1. If ρ₀ is supported on one parity sector, the probability of the opposite sector at time t is at most min(1,ε(t)). This is an exact finite-rate upper bound, uniform in arbitrary initial bath states, including bath/reference correlations compatible with the sector. It is stronger than the requested O(J²Δ/γ+J²/γ²) population bound. It is not the same bound for the unpinched full state/channel.

## Proof with constants
Let L₀(t)A=−i[H₀(t),A] and K(t)A=−i[V(t),A]. L₀ preserves P and Q. Oddness of V implies PKP=QKQ=0: its commutator maps block-diagonal operators to off-diagonal ones and vice versa. Therefore

(Pρ)̇=L₀Pρ+PKQρ,
(Qρ)̇=(L₀−2γ)Qρ+QKPρ.

The homogeneous Q propagator is e^(−2γ(t−s)) conjugation by U₀(t,s), a trace-norm isometry times the scalar damping. Since Qρ₀=0,

Qρ(t)=∫₀ᵗ e^(−2γ(t−s)) U₀(t,s) K(s)Pρ(s) U₀(t,s)† ds.

Pρ(s) is positive of trace one. Thus ||K(s)Pρ(s)||₁≤2J, giving

||Qρ(t)||₁≤(J/γ)(1−e^(−2γt)).

Variation of constants in the P equation and ||[V,A]||₁≤2J||A||₁ give

||Pρ(t)−U₀ρ₀U₀†||₁ ≤ 2J ∫₀ᵗ ||Qρ(s)||₁ ds = 2ε(t).

An opposite-sector projector has expectation zero in the comparison state. Its expectation in ρ equals that in Pρ and differs by at most trace distance. The inequalities ε≤J²t² and ε≤J²t/γ follow directly by bounding 1−e^(−2γs)≤min(2γs,1). For small t,

ε(t)=J²t²−(2/3)J²γt³+O(J²γ²t⁴).

For t≫γ⁻¹, ε(t)=J²t/γ−J²/(2γ²)+O(J²e^(−2γt)/γ²). The bound can become trivial at long times; it does not promise eternal storage.

## Exactly solved data qubit
For S=Z, H=hX, write ρ=(I+xX+yY+zZ)/2. Then

ẋ=−2γx; ẏ=−2γy−2hz; ż=2hy.

Set κ=√(γ²−4h²), c=cosh(κt), f=sinh(κt)/κ, using f=t at κ=0 and analytic continuation for imaginary κ. The exact Bloch channel is

x(t)=e^(−2γt)x₀,
y(t)=e^(−γt)[(c−γf)y₀−2hf z₀],
z(t)=e^(−γt)[2hf y₀+(c+γf)z₀].

For the +Z initial state, let z_h(t)=e^(−γt)(c+γf). Its opposite-parity probability is exactly

p_h(t)=[1−z_h(t)]/2.

In particular z_h solves z̈+2γż+4h²z=0, z_h(0)=1, ż_h(0)=0. At short time,

p_h(t)=h²t²−(2/3)γh²t³+O((γ²h²+h⁴)t⁴).

For |h|≪γ, the slow decay rate is r=γ−√(γ²−4h²)=2h²/γ+O(h⁴/γ³). After the initial γ⁻¹ transient, z_h(t) is dominated by ((1+γ/κ)/2)e^(−rt); the second mode has rate γ+κ. Thus in the intermediate window γ⁻¹≪t≪γ/h², p≈h²t/γ with an initial-slip correction of order h²/γ². At late times and h≠0, p tends to 1/2. For 2|h|>γ the solution is damped oscillatory; the exact finite-rate bound remains valid.

### Pauli sectors versus actual channel
The yz off-diagonal transfer entries mean the channel is generally NOT a stochastic Pauli channel. If one explicitly Pauli-twirls it, define

λx=e^(−2γt), λy=e^(−γt)(c−γf), λz=e^(−γt)(c+γf).

Its Pauli probabilities are

pI=(1+λx+λy+λz)/4,
pX=(1+λx−λy−λz)/4,
pY=(1−λx+λy−λz)/4,
pZ=(1−λx−λy+λz)/4.

The combined X/Y sector probability pX+pY=(1−λz)/2 equals the +Z population-flip probability. These twirled probabilities do not define independent physical fault trajectories in the untwirled evolution. Also, Z dephasing itself destroys an arbitrary qubit's phase: even at h=0, pZ=(1−e^(−2γt))/2. The protected object is parity-sector occupancy or information encoded within a degenerate parity sector, not an arbitrary unencoded qubit.

### Explicit obstruction to the quadratic full-channel bound
For initial +Z, the trace distance between the actual output and its pinching equals |y(t)|/2=|h|e^(−γt)|f|. At t=γ⁻¹ and η=|h|/γ→0 this is

[(1−e^(−2))/2]η+O(η³) ≈0.432332η.

Hence no universal constant C makes this coherence error ≤C(h²t/γ+h²/γ²) for all η: the proposed right side is 2Cη² at that time. A full-state comparison to H₀ evolution has the same linear obstruction, since it is at least the magnitude of this off-diagonal component. From the proof one can instead upper-bound full-state trace distance by ε(t)+(J/(2γ))(1−e^(−2γt)). Boundary pinching removes the linear coherence term; claiming it disappeared without performing or explicitly restricting to that operation is invalid.

## Conserved bath observable
Take H=I⊗H_B+J X⊗B with Hermitian ||B||≤1. If [B,H_B]=0 and the initial state is a product ρ_D⊗σ_B, the reduced data channel is exactly the convex mixture

Φ_t(ρ_D)=Σ_b Tr(Π_b σ_B) Φ_{h=Jb,t}(ρ_D).

The spectral weights are arbitrary; initial bath coherences between different b eigenspaces vanish upon bath trace. Consequently the flip probability is Σ_b w_b p_{Jb}(t), and the worst initial bath state selects a maximizing eigenspace. There is no assumption of a thermal bath or random preparation. For initial data-bath correlations, a state-independent reduced channel need not exist; the joint-system theorem above still applies when the joint initial state is parity-pinched.

If [B,H_B]≠0, this scalar-mixture formula generally fails. The general proof does NOT fail: H₀=I⊗H_B still commutes with Z⊗I, V=JX⊗B is odd, and the norm bound is unchanged. Arbitrarily fast bath dynamics cannot defeat this particular upper bound. No Markov approximation to the persistent bath was used. The added dephasing mechanism itself is assumed to be exactly Markovian, independent and ideal at rate γ; deriving or implementing that mechanism is a separate physical requirement.

## Precise serial iterability with real measurements
Let Π±=(I±S)/2, and let Φ_i be the joint CPTP evolution in a deterministic interval of length Δ_i satisfying the hypotheses with J_i,γ_i. Define the actual ideal endpoint measurement instrument

I^{(i)}_{r←s}(A)=Π_r Φ_i(Π_s A Π_s) Π_r.

For every positive A supported on sector s,

Tr I^{(i)}_{−s←s}(A) ≤ ε_i Tr A,

where ε_i=min(1,(J_i²/γ_i)[Δ_i−(1−e^(−2γ_iΔ_i))/(2γ_i)]). Equivalently its Heisenberg effect satisfies

Π_s Φ_i†(Π_{−s}) Π_s ≤ ε_i Π_s.

The inequality includes arbitrary bath/reference states, and scales to subnormalized inputs. It is an honest CP instrument statement, not a decomposition of the unmeasured evolution into fictitious good/bad faults.

Perform ideal parity readout at the start and end of each chronologically nonoverlapping interval; adjoining intervals can share the readout at their common endpoint. Condition on the recorded past. The new initial state is supported on its recorded sector, although its bath can retain all past memory. Thus Pr(flip in interval i | entire past)≤ε_i. For any specified chronological subset A of intervals, the tower property gives

Pr(all specified flip events in A)≤∏_{i∈A} ε_i.

No independence is claimed. Deterministic bounds must hold uniformly for all allowed past-dependent controls. Nonselective pinching changes the same unconditional quantum dynamics, but retained outcomes are needed to call the transitions recorded flip events; a valid instrument representation can be used when actual measurements occur with outcomes subsequently discarded. This theorem does not license inserting unperformed projections into the autonomous dynamics. It does not cover overlapping intervals or arbitrarily postselected future bath states.

## Why the spatial/network leap fails
A per-check bound need not multiply across simultaneous checks. A concrete two-qubit example is H=J X₁X₂ with independent dephasing γ(Z₁ρZ₁−ρ)+γ(Z₂ρZ₂−ρ), initialized in |00>. One coherent term flips both parities at once. The subspace |00>,|11> obeys the same scalar model with effective dephasing 2γ. The joint double-flip probability is J²t²+O(t³), whereas multiplying two one-check bounds would predict O(J⁴t⁴). This is a genuine counterexample to that multiplication, even without a bath.

For a chosen fixed parity S, all odd Hamiltonian terms can be collected into V and the theorem remains true with J=||V|| (at most their summed norms). Overlapping terms can enlarge J and correlate many checks. Terms commuting with S are unsuppressed inside its sectors and can produce logical errors. A many-check theorem needs locality-aware instrument/fault structure, not just this single-parity result. Additional dephasing commuting with S can often be included using a contractive block-preserving propagator, but no broad network conclusion is assumed here.

## Prior art and novelty status
This is an explicit elementary specialization of established quantum-Zeno/strong-damping machinery, not a novelty claim.

- Burgarth, Facchi, Nakazato, Pascazio, Yuasa, [Generalized Adiabatic Theorem and Strong-Coupling Limits](https://quantum-journal.org/papers/q-2019-06-12-152/), Quantum 3,152 (2019): Theorem2 treats GKLS strong-coupling limits; Corollary1 treats strong damping; Remark2 gives nonperturbative error bounds. These establish rigorous context. Our direct two-sector estimate makes its constants, initial pinching, arbitrary-bath uniformity and finite-time dependence transparent; no claim is made that this estimate is absent from prior literature.
- Same authors, [Quantum Zeno Dynamics from General Quantum Operations](https://quantum-journal.org/papers/q-2020-07-06-289/), Quantum 4,289 (2020): finite-dimensional dynamics under frequent general quantum operations, relevant to the measured-boundary protocol. This citation does not identify that protocol with autonomous unmeasured evolution.
- Slichter et al., [Quantum Zeno effect in the strong measurement regime of circuit quantum electrodynamics](https://arxiv.org/abs/1512.04006), New J.Phys.18,053031 (2016): driven-qubit transition suppression under continuous measurement is established experimental/theoretical context. We did not use their device data or infer feasibility for a code from it.

The useful deliverable is the explicit bath-dimension-independent finite-rate interface and its precisely delimited serial measurement iteration, not a new hardware theorem.

## Checks and reproducibility
All calculations are our own NumPy/SciPy matrix exponentials, with no author-code execution or additional Willow outcome analysis. `check.py` compares the exact Bloch transfer matrix against Liouvillian exponentials over overdamped, critical and underdamped parameter cases; maximum discrepancy 1.09e−15. It checks the population bound and twirled positivity (roundoff tolerance), arbitrary noncommuting baths of dimensions2/3 including bath Hamiltonian norm30, six general block-diagonal H₀/off-diagonal V cases, and the conserved-bath mixture (error2.9e−17). The small-η coherence counterexample scales linearly as derived. Main check cost:0.12 CPU seconds, under50 MiB RSS.

`serial_check.py` enumerates all32 outcome histories over five actually measured intervals for a noncommuting persistent bath, and verifies all31 nonempty specified-flip-subset product inequalities. It also exhibits the spatial counterexample: J=.2,γ=1,t=.01 gives joint double-flip probability3.94719e−6, versus invalid product bound1.57884e−11, a factor250,005. These numerical checks corroborate the algebra; the proofs supply uniformity.
