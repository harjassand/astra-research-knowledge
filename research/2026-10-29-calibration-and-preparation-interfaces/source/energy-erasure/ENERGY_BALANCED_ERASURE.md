# Energy-balanced erasure of captured loss

Author: `/root`, 29 October 2026. New construction in this tranche; independent review is separate. No historical-priority, hardware-threshold, or net-energy-saving claim.

## Consequence and chosen interface

Can a quantum energy supply be restored after loss without retaining all the backaction of photon counting, and without sending the captured loss mode quantum mechanically back to the computation? The construction does so with a **forward quantum energy carrier, a local coherent loss register, and a backward classical message**. It exactly converts the captured part of a finite bosonic loss process into an erasable record. Uncaptured loss remains an explicit informative record. The result is a finite channel identity, not a weak-loss approximation.

Required ports are coherent capture before any inaccessible count copy, a pure energy carrier, coherent number arithmetic and transfer, controlled local decoding, and a joint measurement downstream. That measurement mixes states of the **same actual energy**, not merely equal abstract charge. If coherent field return is supplied, direct interferometric recombination is a simpler strong alternative. The new interface pays forward supply, local storage, timing and coherent processing instead of quantum return.

## 1. Exact model and actual records

Data have integer excitation Q and the admitted encoding is

`V_N |x> = |x>|m_x>_B`, `m_x=N-q(x)` in `{0,...,N}`.

The logical object is the joint data-plus-battery encoding, not the bare-data marginal. Unknown inputs require an acquired encoder, and bare outputs require an acquired decoder. Degeneracy within a Q sector is allowed and untouched below.

The battery undergoes the exact vacuum attenuator of survival eta. A fraction xi of the emitted mode is captured coherently and the rest is inaccessible. Set

`s=eta`, `c=(1-eta)*xi`, `u=(1-eta)*(1-xi)`, with `s+c+u=1`.

The passive dilation on m photons is, up to calibrated mode phases,

`|m>_B -> sum_(r+j<=m) a_(r,j)(m) |m-r-j>_B |j>_E |r>_F`,

`a_(r,j)(m)=sqrt(m!/[(m-r-j)!j!r!]) s^((m-r-j)/2)c^(j/2)u^(r/2)`. (1)

E is captured and F is inaccessible. This assumes the single-mode vacuum attenuator and its specified mode splitter. Returning or initially correlated baths are not replaced by vacuum. Physical approximations need their own complete-channel allowance.

## 2. Coherent restoration creates an energy-matched eraser

Supply carrier A in Fock state |M>, with photon energy hbar*omega matching B and E, and a **degenerate**, fresh quantum register R in |0>. Coherently compute `ell=N-Q-n_B` into R, then transfer ell quanta from A to B. On the occupied subspace,

`|x>|m-ell>_B|M>_A|0>_R -> |x>|m>_B|M-ell>_A|ell>_R`. (2)

M>=N suffices. This is an isometry because ell remains in R; it preserves actual energy and extends to a unitary separately in finite energy blocks. A basis completion proves existence, **not** cheap hardware access. Coherent arithmetic and selected number transfer are paid ports. Measuring R or leaving an inaccessible copy of ell defeats the eraser.

The resulting state is

`sum_(r,j) a_(r,j)(N-Q) V_N|psi> |r+j>_R |M-r-j>_A |j>_E |r>_F`. (3)

Send A forward to the receiver of E. The pair AE has total energy `(M-r)hbar*omega`. Measuring its total energy gives r without measuring j. This unavoidable uncaptured-loss sector may become an actual classical record.

Within a fixed r, the vectors `|M-r-j>_A|j>_E` are energy degenerate. An energy-conserving interaction can mix their relative phases without a supplied superposition of different total energies. Energy replacement has supplied the missing partner for a charge-respecting eraser. An ordinary optical Lambda pump with a nonzero-frequency drive does not automatically meet this condition; its drive/reference must be retained. The companion finite binary pump distinguishes equal-gap and driven cases.

## 3. Finite record-conversion theorem

Choose M=N. Given r, put `d_r=N-r+1` and measure the Fourier basis of the fixed-energy sector spanned by `|N-r-j,j>_AE`, `0<=j<d_r`. For outcome k the local amplitude is

`C_(r,k)|psi> = (1/sqrt(d_r)) sum_j exp(2*pi*i*k*j/d_r) a_(r,j)(N-Q) V_N|psi>|r+j>_R`. (4)

Zero terms pad charges with r+j>m. Define

`p_r(m)=binom(m,r)u^r(1-u)^(m-r)` for r<=m, and zero otherwise. (5)

The multinomial theorem gives `sum_j a_(r,j)(m)^2=p_r(m)`. For p_r(m)>0 the local vector

`beta_(m,r,k)=sum_j exp(2*pi*i*k*j/d_r)a_(r,j)(m)|r+j>/sqrt(p_r(m))`

has norm one. Acquire a Q-controlled unitary mapping this known vector to |0>_R. A Householder plus a known phase, or a finite Givens decomposition, constructs it in each orthogonal Q block. On zero-probability blocks its action is arbitrary. Because R is degenerate this preserves data charge and energy.

After the classical message (r,k) and local decoding, the **actual corrected instrument** is exactly

`K_(r,k)=D_r/sqrt(d_r)`, `D_r=sqrt(p_r(N-Q))`.                         (6)

B remains in V_N, R is pure and fixed, AE is a known state of energy M-r, F contains r, and all measurement/pointer records can be retained. The full output is therefore the canonical restored-loss instrument (5), with conditionally uniform eraser outcome k and apparatus states depending only on actual records. Equality holds on arbitrary reference-entangled inputs and spectator memory.

The remaining distinguishability is governed exactly by

`u = physical loss probability * uncaptured fraction`.

This is a restored **logical-instrument** identity, not a claim that photons have transmitted with probability 1-u. With perfect capture, u=0, only r=0 occurs, D_0=I, and every eraser outcome has probability 1/(N+1) independently of the input. The corrected complete output factors as the encoded input times its actual record/apparatus state.

### Real padded implementation

For exact real checks choose `d=2^ceil(log2(N+1))`, `M=N+d-1`. Every r<=N sector contains d states `|M-r-j,j>`, `0<=j<d`. Zero-pad the occupied amplitudes and use a Walsh-Hadamard instead of the Fourier matrix. Equation (6) then uses d in every branch. This increases supplied energy by at most a constant factor.

## 4. Why this multijump construction retains a coherent register

The different j components in (4) remain orthogonal locally in R. Hence

`C_(r,k)^dagger C_(r,k)=p_r(N-Q)/d_r`.

The decoder erases the normalized beta vector, but cannot erase its norm sqrt(p_r). This proves (6): the inaccessible field's sector r is precisely the information that must remain informative. Captured phase information can become a harmless record because R stayed coherent until the message arrived.

An inaccessible copy of j or ell leaves extra orthogonal branches and invalidates (4) as a complete amplitude. Uniform observed k alone does not imply correction. Measuring the local loss number first gives the original count instrument, not (6).

Conditional on (r,k), AE is a known state. A record-controlled, energy-conserving unitary can route it to `|M-r>_A|0>_E`. At u=0 this returns A exactly to its original pure state. For u>0, returning A to |M> additionally needs r quanta, of expected energy `hbar*omega*u*<N-Q>`. This is ideal energy accounting, **not** a reset-work advantage. Detection, pure registers, control work, calibration, storage, transport and reuse losses remain paid.

## 5. Binary physical instance without retained R

For an exact one-excitation collision let `C=cos(Theta(Q))`, `S=sin(Theta(Q))`. Thus `[C,S]=0`, `C^2+S^2=I`. A resonant Jaynes-Cummings interaction with a two-level output carrier gives `Theta(Q)=theta*sqrt(N-Q)`. Its output is

`V_N C|psi>|0>_E + V_(N-1) S|psi>|1>_E`,

with a calibrated phase absorbed in the label. Coherently transfer one excitation from a fresh two-level A only in the loss sector, leaving no inaccessible count copy. The outgoing records `|e,0>_AE` and `|g,1>_AE` have the same actual energy when the gaps match. A balanced energy-conserving mixer and number readout give, up to fixed outcome phases,

`M_+=(C+iS)/sqrt(2)`, `M_-=(C-iS)/sqrt(2)`.

These equal `exp(+-i Theta(Q))/sqrt(2)`. Their inverse feedback exactly restores the encoded input, with a uniform actual bit. For one active qubit feedback is a Z rotation. A larger charge range requires a nonlinear function of Q and can be expensive. The companion pump provides a two-sector selector and finite amplitude bounds; an ideal normalized addition is not substituted for that implementation.

This binary statement is exact for a controlled two-level collision. A finite interval of a bosonic Markov bath can emit multiple photons and is not this collision. The multi-loss theorem above avoids that replacement. Common noncommuting operations can occur **between completed corrected cells**. A continuously driven interval is not reduced to the idle attenuator by this theorem; it needs a separate dynamical comparison or captured-field decoder. The continuously driven, counted-replacement theorem in the other root proof has a different interface and a nonzero error.

## 6. Resources and strongest alternatives

Local R needs `ceil(log2(N+1))` qubits in the minimal version and stays coherent through forward transit, joint processing and classical return. The encoded data and battery also survive that delay. R becomes pure only after correction. Small memory size does not bound its noise exposure or processing cost.

The forward carrier has N+1 potentially occupied Fock levels and energy at most N*hbar*omega in the minimal version. At most `2 ceil(log2(N+1))` classical bits return. No quantum return of E is used. Transporting a now known pure A for reuse is a separate service operation. Destructive readout consumes its energy; QND readout and controlled routing permit the ideal recycling statement but are additional physical ports.

A fixed-energy Fourier mixer and Q-controlled local decoder are coherent operations, not free computations. Generic decompositions use polynomially many addressed rotations in N and O(number_of_admitted_charges*N) local amplitude operations. They are not logarithmic-time merely because R is logarithmic in N. The binary version has simpler mixing and single-qubit feedback.

If E can return coherently, a passive interferometric recombiner combines retained and captured amplitudes into a mode of surviving fraction `s+c=1-u`. At full capture the inverse loss beamsplitter restores the original battery without a forward replacement carrier. That route can be cheaper. Both routes need collection and phase calibration. Our construction converts the **direction and type of allowed access**; it does not outperform unrestricted coherent reversal. Ordinary fixed-charge direct coupling can avoid battery exposure altogether.

With unrestricted qualified qudit transduction and Bell/control ports, another strong same-direction alternative distributes entanglement forward, teleports the captured field back using classical messages, then recombines locally. This can reproduce coherent return without a quantum backward channel. Its entanglement supply, coherent storage, Bell analysis, reset and any energy/reference conversion are paid resources. Under strict conservation, translating a Fock superposition into a degenerate qudit and performing the required Bell measurement are additional operations. No universal communication-direction or dimension separation over this conventional route is claimed here.

Gregoratti-Werner environment-assisted correction and Szigeti-Carvalho-Morley-Hush no-knowledge feedback already establish the general correction concepts. The work here is an explicit finite energy-matched one-way instrument, its uncaptured-loss law and its coherent-syndrome/actual-record interface. No historical priority is asserted for environment-assisted correction, erasure, or their general principles.

The particularly close earlier construction is Vitali-Tombesi-Milburn, *Quantum state protection in cavities* (1998): normalized photon replacement and the residual square-root-number phase diffusion are already explicit in its Eq.3 and Eq.11-14. Our original counted-replacement calculation specializes that known mechanism to dressed computation and complete records; it is not a new suppression mechanism. See the overriding `ANCESTRY_CORRECTION.md` for the preserved earlier proof's attribution. The present theorem constructs an energy-matched coherent eraser rather than inheriting that photodetection interface.

Uniform complete-channel implementation allowances are required for preparation, the attenuator model, capture, coherent arithmetic and transfer, forward transit, joint mixing and readout, local holding and recovery, and carrier reuse. Under those contracts ordinary channel telescoping adds the allowances. Source fidelity, an interaction norm, or an expected count is not a device or workload error rate. The exact identity does not constitute a noisy fault-tolerant computer.

## 7. Proof boundaries and useful failures

1. Restoring B and discarding the local syndrome before erasing E can destroy the orthogonal ranges needed by the multi-loss proof. Binary commuting C,S and two-charge dephasing have special random-unitary decompositions; these do not establish the unrestricted multi-charge case without R.
2. A classical count cannot be treated as a coherent control merely because its numerical value is known. Its inaccessible copy preserves the information that the eraser was supposed to remove.
3. Equal abstract excitation is insufficient if carrier and loss photons have different energies. Incommensurate gaps, active frequency conversion and drive references change the interface and must be included.
4. The padded Walsh-Hadamard is a valid number-conserving unitary within one energy sector. It is not generally implemented by a single passive beamsplitter when M>1; number-selective operations are an actual cost.
5. The loss model is exact at idle or for the explicitly given attenuator operation. Noncommuting gates during the loss interval can change its Kraus structure and are not certified by an idle formula.
6. Complete capture makes the informative sector trivial. It does not make capture, the input encoder, local decoding, carrier preparation, or timing free.
7. At partial capture the apparatus is not returned in an input-independent state unless the residual r record and its supply consumption are retained. Equation (6) keeps them.

## 8. Governing primary ancestry

* Ivan, Sabapathy and Simon, https://arxiv.org/pdf/1012.4266, Section IV, Eq.4.6 and Eq.4.11: exact vacuum attenuator in the Fock basis.
* Gregoratti and Werner, https://arxiv.org/pdf/quant-ph/0209025, Proposition 2 with rectangular trace-preserving correction: the isometric-branch criterion.
* Gregoratti and Werner, https://arxiv.org/pdf/quant-ph/0403092, Section IV.A, Proposition 4: specified-instrument polar recovery. A fidelity optimum is not automatically a diamond optimum.
* Szigeti, Carvalho, Morley and Hush, https://arxiv.org/pdf/1401.4493, Eq.5-10: no-knowledge feedback, collection efficiency and reservoir mixing. Its monitoring ports do not acquire the coherent replenishment used here.
* Vitali, Tombesi and Milburn, https://arxiv.org/pdf/quant-ph/9803045, Section II, Eq.3 and Eq.11-14: normalized replacement and square-root phase diffusion, with actual laser/adiabatic and service assumptions.

The source-read ledger states what was actually read. This is a constructed research result with internal reviews, not a claim of externally established historical novelty.


