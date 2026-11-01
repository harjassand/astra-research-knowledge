# Conditional microscopic source: a warm real-wavefunction meter gives Hermitian branches

Independent derivation of the root-proposed measurement interface, 2026-11-01. This is standard measurement algebra used to specify an honest conditional source, not a physics novelty claim or evidence of an implemented apparatus. No hardware actions or additional literature search.

## 1. Exact premises and Kraus derivation

The finite-dimensional spin system couples to a fresh meter initially independent of the system/history-conditioned environment. Its state is

ρ_M=Σ_n p_n |ψ_n><ψ_n|, p_n≥0, Σ_n p_n=1,

where ψ_n(y) can be chosen REAL in the position readout basis. A finite-temperature harmonic oscillator thermal state is an example of such an INITIAL meter state: its energy eigenfunctions can be chosen real. No pure or zero-temperature meter is necessary.

Assume that the ACTUAL joint interaction over the entire coupling window is

U=exp(−i g L⊗p), L=L†,

with units absorbing ℏ, and that no additional unaccounted evolution acts before the relevant readout. Translation gives the system Kraus density

K_(y,n)=√p_n <y|U|ψ_n>=√p_n ψ_n(y−gL).

Functional calculus on the Hermitian finite-dimensional L makes every K_(y,n) Hermitian. It remains Hermitian when L and g are unknown: their being fixed and Hermitian is the structural premise, not their known numerical calibration.

For a recorded detector label/window r with classical response 0≤w_r(y)≤1, the actual selected map is

Φ_r(X)=Σ_n ∫dy w_r(y) K_(y,n) X K_(y,n).

It is CP and Hilbert–Schmidt self-adjoint. This map includes the inaccessible mixed-meter component n; no measurement or purification of n is required. Finite bins, classical readout errors, missed detections, or coarsening preserve this statement if they are represented by nonnegative classical response weights and do not introduce additional coherent feedback/phases.

Completeness of translation gives Σ_n∫dy K_(y,n)²=I. Thus Φ_r(I)≤I, and because Φ_r†=Φ_r it is also trace nonincreasing. The full outcome-summed channel is unital and trace preserving when the response weights sum to one.

## 2. HS contractivity, explicitly

Write L=Σ_j λ_j Π_j. The branch is diagonal on operator blocks:

Φ_r(Π_j X Π_k)=c_r(λ_j,λ_k) Π_j X Π_k,

c_r(λ,μ)=Σ_n p_n∫dy w_r(y) ψ_n(y−gλ)ψ_n(y−gμ).

This coefficient is real and symmetric in λ,μ. Cauchy–Schwarz yields

|c_r(λ,μ)|²≤c_r(λ,λ)c_r(μ,μ)≤1.

Orthogonality of the Π_j X Π_k blocks therefore gives ||Φ_r(X)||_HS≤||X||_HS. The same proof holds for HS normalization by d_C in a code-conditioned source. No eigenvalue gap, known eigenbasis, cold meter, or dissipative inverse is used.

The physical operation implementing Φ_r† is simply the same selected measurement primitive Φ_r with a fresh identically prepared meter. A return word uses the specified branch at each primitive, and any branch failure contributes zero. Reversing primitive order implements the composite adjoint. Conditioning/renormalizing on success would instead create a different nonlinear object and is NOT allowed.

## 3. What measurement backaction does and does not defeat

The ideal measurement backaction above is exactly what the Kraus derivation includes; it does not defeat the source. Unknown strength and thermal width can change the retained scalar model while preserving its structural adjoint identity, provided they remain stable. Strong measurement need not be a projector, and weak measurement need not be rank preserving: neither is required.

The dangerous condition is UNACCOUNTED COHERENT EVOLUTION. A warm harmonic oscillator's having real thermal eigenfunctions does not mean its finite-duration interaction is exactly U above. Its own free Hamiltonian can act during the pulse; the system can have drift; the coupling/readout can carry extra phases. Those effects must be included in the actual propagator. In particular [H_M,p]≠0 for an ordinary harmonic oscillator, so exp[−it(H_M+gL⊗p)] cannot simply be replaced by exp(−itgL⊗p). Forced-oscillator evolution can produce system-dependent phases. An impulsive approximation is a bounded-error approximation, not an exact adjoint identity.

Even a commuting system phase gives a simple explicit failure. Append V=exp(−iθL) to the ideal branch. Then

Φ'_r(X)=V Φ_r(X) V†,

whose coefficient on Π_j X Π_k is exp[−iθ(λ_j−λ_k)]c_r(λ_j,λ_k). Its HS adjoint has the conjugate coefficient. Except when the relevant phase is real or c_r=0, Φ'_r is NOT self-adjoint. Hermitian POVM effects alone therefore do not establish Hermitian instruments. Looking only at outcome probabilities can miss exactly this coherent backaction.

Likewise a meter wavefunction with nontrivial position-dependent phase generally produces non-Hermitian K_(y,n). Free spreading before a selected position readout can matter even when an outcome-summed channel has extra symmetries. Detector response matrices that are merely classical and nonnegative are benign; coherent detector dynamics or outcome-dependent system feedback requires separate analysis.

To claim the exact family physically, one must actually isolate/engineer the stated interaction or include controls that make the complete branch satisfy the identity. Known compensation may help but its implementation and noise are charged. Unknown extra Hamiltonians are not corrected by writing the desired model. No universal exact suppression service is presumed.

## 4. Paid source obligations

Each episode pays for the actual code/product preparation used, meter thermalization or other real-state preparation, fresh meter replacement/reset and decoupling, coupling duration/energy, detector time and energy, all failure branches, records, and calibration. Thermal preparation is not zero-cost just because it is warm. A fresh thermal marginal uncorrelated with the system is a requirement; reusing a meter whose conditional state depends on previous outcomes generally changes the source.

For finite-temperature infinite-dimensional meters, controlling an impulsive approximation may require energy-constrained bounds and thermal tail estimates; an unqualified operator-norm bound on an unbounded free Hamiltonian is not available. These physical bounds must be translated into the return-bias budget, not presumed negligible. Source stationarity across the entire acquisition/deployment period remains necessary.

If actual primitive errors have trace/diamond-norm bounds suitable for the prepared states, then word errors can be telescoped and charged in the scalar mean error budget. The bounded-projection theorem currently assumes the source contract; this note does not supply a bias-robust theorem or transfer an unreviewed commutator-admission argument.

## 5. Verdict

The microscopic derivation is SOUND under its explicit actual-interaction and real-meter premises. It gives a legitimate finite-temperature family of physically executable self-adjoint CP contraction branches, including selected noisy detector bins. It strengthens the code-conditioned conditional source beyond merely postulating ideal projectors.

It does not establish that generic measurement hardware has those branches, that finite pulses eliminate drift, that fresh meters are cheap, that successful holonomic words have low task dimension, or that the acquisition algorithm beats ordinary retaining learners. The current same-seed theorem remains the only theorem invoked; any multiple logical seed/readout construction is a separately paid collection or pending extension, not silently inherited here.

## 6. Root-proposed finite-pulse repair: exactly matched two-quadrature drive

This closes the finite-oscillator objection for a CONCRETE MORE STRONGLY ADMITTED interaction family, without an impulsive approximation.

Let the actual meter free Hamiltonian be H_0=ωN (an additive zero-point constant is irrelevant), R(t)=exp(−itH_0). Supply two phase-controlled couplings to the SAME fixed Hermitian system operator L so the actual lab interaction is

H_int(t)=u(t)L⊗[R(t)pR(t)†].

For dimensionless oscillator quadratures the bracket is p cos(ωt)+q sin(ωt). Thus this is an explicit q/p waveform with finite amplitude whenever u(t) has finite amplitude. In the interaction picture defined by I⊗R(t),

H_I(t)=(I⊗R(t)†)H_int(t)(I⊗R(t))=u(t)L⊗p.

These Hamiltonians commute at all times. Consequently the exact finite-duration propagator is

U(T)=(I⊗R(T)) exp[−igL⊗p], g=∫_0^T u(t)dt.

There is no time-ordering-induced L² phase. Measure the rotated quadrature Q_T=R(T)qR(T)†, whose eigenvectors are R(T)|y>. Then

<y|R(T)†U(T)|ψ_n>=ψ_n(y−gL),

giving exactly the real Hermitian Kraus family already proved. Alternatively choose T to be a full oscillator period, so R(T)=I up to an irrelevant global phase, and use ordinary position readout. Neither option requires a cold pure meter or an inverse-L² gate.

The construction requires actual matching of the q and p couplings to the SAME L, a stable/admitted oscillator frequency and phase reference, the specified timing/waveform, and an actual rotated-quadrature readout or full-period timing. An unknown mismatch between coupled system operators, unknown system drift, anharmonic meter evolution or unwanted terms is not corrected by this identity. In particular an extra system Hamiltonian commuting with L can still leave a non-self-adjoint system phase. Hardware capability is not demonstrated by writing the control Hamiltonian.

This is finite-time and finite-envelope. For a finite-dimensional system with bounded ||L|| and a finite-temperature oscillator, the displaced state has finite mean energy. With standard dimensionless normalization and an initially centered thermal meter, the ideal final displacement adds at most ωg²||L||²/2 to the meter's mean oscillator energy. That is only a stored-energy bound, not the complete work or energy budget of preparation, driving and readout. Meter reset, drive bandwidth, phase tracking, both coupling channels, detector resources and all error bounds remain paid.

Updated verdict: the ordinary single-quadrature finite-pulse warning remains valid, but it is NOT a no-go. The explicitly phase-matched two-quadrature interaction plus rotated/full-period readout gives an exact warm-meter implementation of the required self-adjoint selected branches. It strengthens the conditional physical source family without establishing availability, low task dimension, source precision or a practical learning advantage.
