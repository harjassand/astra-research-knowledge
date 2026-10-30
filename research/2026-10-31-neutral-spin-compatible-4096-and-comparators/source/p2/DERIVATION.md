# Neutral spin blocks with charge-mediated gates and finite error tolerance

Working derivation, 30 October 2026. Earlier accepted constructions and files are unchanged. This is a different, calibrated fermionic resource setting from the signed-spin handles and from the blind positive-exchange compiler. No numerical device threshold or physical advantage is claimed.

## 1. Result and its scope

The construction supplies a finite universal gate set, preparation, encoded readout, and a teleportation leakage-reduction unit for four-electron spin-singlet blocks. Every coherent native operation preserves each block's total spin. The computation is therefore exactly insensitive to an arbitrary, possibly common and noncommuting, collective magnetic bath on each block, including during gates. It does not require that two neighboring blocks see the same magnetic bath.

After explicitly separating this harmless strong coupling from bounded residual faults, the construction fits existing leakage and non-Markovian accuracy-threshold machinery. A fixed, positive tolerance to the residual coupling suffices for arbitrarily long computation. Readout accuracy and charge-control precision can be fixed once below the base threshold; outer encoding supplies the improving accuracy.

The substantive working results here are:

1. An exact five-window, fixed-positive-U coherent singlet-to-double-occupancy capture and reciprocal forward return.
2. A density-mediated entangler that stays in the spin-zero sector of each block throughout.
3. A stronger endpoint statement: every diagonal interaction of the captured charge patterns preserves the computational subspace of a valid block even when other blocks have leaked.
4. The physical mapping needed to apply existing leakage correction in the presence of arbitrarily strong collective magnetic coupling.

Singlet encoding, exchange-only universality, capacitive spin-qubit gates, teleportation leakage reduction, and concatenation of decoherence-free blocks with quantum error correction all have substantial prior art. No priority claim for those ideas or for a new threshold theorem is made.

The architecture requires coherent scalar charge controls, renewable sources and meters, and an addressable capacitive interaction with a bounded residual when inactive. A bare, always-on Coulomb interaction is not automatically such a control. Section 12 treats this qualification explicitly.

## 2. Physical Hilbert space and noise decomposition

One block has four one-orbital sites and four electrons. The fixed-number Fock space has dimension 70. Its total-spin-zero subspace has dimension 20. The computational space is the two-dimensional, singly occupied spin-zero subspace:

\[
 |0_L\rangle=|s_{12}\rangle|s_{34}\rangle,\qquad
 |1_L\rangle={|t_+t_-\rangle+|t_-t_+\rangle-|t_0t_0\rangle\over\sqrt3}.
\]

Let P_b project onto this computational space and S_b be total physical spin on block b. The full local leakage space also includes other particle-number sectors. In the one-orbital model the full local Fock space has dimension 256. The algebraic endpoint proofs below hold there, although the numerical Hubbard checks use the 70-dimensional N=4 sector.

The ideal, potentially strong environment Hamiltonian is

\[
 H_{\rm strong}(t)=I H_M(t)+
 \sum_{b,\alpha} S_b^\alpha\otimes B_{b,\alpha}(t).
\]

The B operators can act on the same memory, need not commute, and need not be slow or small. Well-defined propagators are assumed. Every native coherent control is spin independent and therefore commutes with every S_b. On a neutral block, every S_b annihilates the state. This remains true during charge excursions.

All departures from this symmetry and from the nominal charge-control model enter E(t): magnetic gradients, spin-orbit terms, unwanted tunneling, charge-control drift, spectator coupling, and leakage to additional orbitals. The threshold statement requires local operator-norm/fault-amplitude bounds on the allowed full local spaces, including leakage states, rather than average infidelity on a few prepared inputs.

For example, use

\[
 E(t)=\sum_b E_b(t)+\sum_{b<c}E_{bc}(t).
\]

Each term may act on the retained common memory. There is no independence assumption for this residual Hamiltonian. Physical fermion parity is respected; the intended Hamiltonians are even and block-number conserving. Any charge-transfer errors require the corresponding local fermionic fault model, including the source/reservoir modes. A purported qubit norm bound that silently excludes particle loss is insufficient.

The finite-orbital model is itself a qualification. A gap alone does not prove an operator-norm bound for arbitrary states of an unbounded continuum. A device needs a justified allowed state domain or a separate energy-constrained extension.

## 3. Exact capture with a fixed positive charging energy

For an addressed pair i,j the native Hamiltonian is

\[
 H=U\sum_k D_k
 -g\sum_\sigma(c^\dagger_{i\sigma}c_{j\sigma}+{\rm h.c.})
 +{\epsilon\over2}(n_i-n_j), \qquad U>0.
\]

Here D_k=n_{k\uparrow}n_{k\downarrow}. Controls are a real nonnegative tunneling amplitude g and a scalar detuning epsilon. U is not switched off. Other sites are singly occupied when this pair operation is applied to computational data. This requires access to g=sqrt(3)U/4 and epsilon=U, with the one-orbital description still valid.

The three separated triplets are stationary. In the basis S,D_+,D_-, with D_+=(D_L+D_R)/sqrt(2), the singlet block is

\[
 H_{S,D_+,D_-}=
 \begin{pmatrix}0&-2g&0\\-2g&U&\epsilon\\0&\epsilon&U\end{pmatrix}.
\]

Set

\[
 a=\arcsin\sqrt{2/3},\quad
 \alpha=\arctan(1/\sqrt2),\quad
 \beta=2\pi-2\alpha,\quad g_*=\sqrt3 U/4.
\]

The capture C uses these chronological windows:

| Window | g | epsilon | duration |
|---|---:|---:|---:|
| 1 | g_* | 0 | a/U |
| 2 | 0 | 0 | beta/U |
| 3 | g_* | 0 | a/U |
| 4 | 0 | U | pi/(4U) |
| 5 | g_* | 0 | pi/U |

During the tunneling windows the S,D_+ Rabi frequency is U, including the nonzero detuning U. The first window gives equal S and D_+ populations. The intervening phase and second window cancel the S amplitude exactly:

\[
 C_3 C_2 C_1 |S\rangle
 =e^{i(\pi/2+\alpha-a)}|D_+\rangle .
\]

Window 4 maps D_+ to exp(-i*pi/4)(D_+-i D_-)/sqrt(2). Window 5 multiplies D_+ by i and D_- by -1. Consequently

\[
 C|S\rangle=e^{i\phi}|D_L\rangle,\qquad
 \phi={3\pi\over4}+\alpha-a.
\]

Triplets are unchanged. The capture time is

\[
 T_C={13\pi/4+2(a-\alpha)\over U}
 ={10.889849943\ldots\over U}.
\]

### Reciprocal return

Each source Hamiltonian is real symmetric in the occupation basis. Reversing the chronological order of the same five forward windows gives C^T. Since C maps one orthonormal input exactly onto one output basis vector, unitarity implies that the corresponding row has no other support:

\[
 C^T|D_L\rangle=e^{i\phi}|S\rangle.
\]

This uses no negative U, negative elapsed time, inverse bath evolution, or coherent control of program choices. The transpose identity applies to the nominal scalar charge Hamiltonians. It would be invalid to substitute a generic, strongly memory-entangled source operator into this proof.

## 4. Encoded gates

### Pair singlet phase

Capture, hold with g=epsilon=0, and reciprocal return implement

\[
 R_{ij}(\theta)=e^{-i\theta P_s^{ij}},\qquad
 t_{\rm hold}={(2\phi+\theta)\bmod 2\pi\over U}.
\]

There are 11 windows. The time is 2T_C+t_hold. No spin direction needs to be prepared, measured, or rotated.

On the computational code, the pair swaps are

\[
 P_{12}^{\rm swap}=-Z_L,\qquad
 P_{23}^{\rm swap}={1\over2}Z_L+{\sqrt3\over2}X_L.
\]

They generate all one-qubit operations. The executable construction uses the earlier seven-pair-phase bisector Hadamard. A pair-12 phase pi/4 gives T up to global phase. Z and X follow from these operations, with X also obtainable using the earlier five-rotation construction. The stated resource counts do not assume free Pauli pulses.

For the supplied, unoptimized program at U=1, H takes 177.398908547 time units. This duration is substantial and is included in the base location duration.

### A simple capacitive CZ

Capture pair 12 of both blocks. The logical charge patterns are

\[
 q_0=(2,0,1,1),\qquad q_1=(1,1,1,1).
\]

A density interaction chi*n_A1*n_B1, held for pi/chi, gives the phases

\[
 e^{-i\pi(4,2,2,1)}=(1,1,1,-1)
\]

on 00,01,10,11. Fixed-U phases from double occupancy are removed with a local charging hold:

\[
 t_{\rm corr}={(2\phi-U\pi/\chi)\bmod2\pi\over U}.
\]

Apply the two reciprocal returns. This is an exact logical CZ in the nominal model. Parallel local control lanes give 12 windows, with

\[
 T_{\rm CZ}=2T_C+\pi/\chi+t_{\rm corr}.
\]

At U=chi=1 the time is 25.812415048. CNOT=H_target CZ H_target takes 380.610232142 with the supplied H. The parallel lanes and capacitive edge are new resources; they are not inherited from the earlier one-signed-handle setting.

### A real capacitance matrix

The single density product is an idealized addressable edge. More generally the electrostatic interaction is

\[
 H_V=\sum_{i,j} V_{ij}n_{Ai}n_{Bj}.
\]

In the captured computational basis its exact energies are E_zw=q_z^T V q_w. Let d=q_0-q_1=(1,-1,0,0). The nonseparable coefficient is

\[
 J=E_{00}-E_{01}-E_{10}+E_{11}
   =d^TVd=V_{11}-V_{12}-V_{21}+V_{22}.
\]

If J is nonzero, a hold pi/abs(J), with acquired local phases corrected, yields a maximally entangling controlled phase. This does not require reconstructing the magnetic memory. It does require characterizing the relevant scalar electrostatic phases and implementing the isolation/switching conditions during capture.

## 5. The charge-pattern theorem and the infection obstruction

### Theorem: diagonal charge dynamics cannot leak a valid captured code

Let C map an orthonormal logical basis to states having definite joint occupations q_z, without leaving local spin zero. Suppose R C is the identity on the code up to specified local phases, and R is a full-space unitary. For any unitary W that is diagonal in all the block occupation operators, R W C preserves each block's computational subspace individually, even for arbitrary joint states of other blocks and memory, provided W has no within-pattern action on the internal spin multiplicity.

For the present source take R=C^T times the charging compensation. To prove the statement, every n_i acts as a scalar on each captured code vector. Hence C^dagger n_i C reduces P. Every joint spectral function of the occupations also reduces P on each tensor factor, including when its coefficients are arbitrary operators on another block or memory. The compensated local return loop reduces P and is the identity there. Multiplying these reducing operators proves the result.

An arbitrary memory-dependent diagonal potential can therefore preserve the code while still causing logical dephasing. The theorem is a no-leakage statement, not an error-free gate statement. A wrong phase is a real fault.

The CZ special case can also be written using the reflection Q=C^dagger(-1)^n1 C. On the code Q=Z_L; the charge interaction is a controlled reflection. This gives a short proof of

\[
 [U_{\rm CZ},P_A\otimes I]=[U_{\rm CZ},I\otimes P_B]=0.
\]

The proof is algebraic on the full local Fock spaces, not just the both-valid input sector.

### Why protecting only an all-valid register is inadequate

Let Q_A be a leakage projector and consider

\[
 H_{\rm infect}=\Omega Q_A\otimes\sum_{b>1}X_{L,b}.
\]

This is zero when A is valid. A single leakage amplitude delta on A nevertheless activates simultaneous flips of every target at time pi/(2 Omega). The many-target fault amplitude is delta, not delta to the number of targets. Thus the statement that a large coupling vanishes on the all-valid register does not establish a threshold.

The allowed collective bath is stronger in the required sense: for any set of leaked blocks F, H_strong acts as identity on every still-neutral block outside F. It can perform arbitrary evolution among leaked blocks and memory, but cannot damage another valid logical block. A shared, noncommuting bath does not change this conclusion.

This property is maintained throughout the native gates, since those gates preserve each block's spin zero. At gate boundaries the stronger charge-pattern theorem also preserves the smaller computational code. The resulting model fits the arbitrary leakage-space evolution in the established Aliferis--Terhal leakage theorem.

### A spin-only obstruction

For two fixed spin-singlet blocks, P_A S_i^alpha P_A=0 and P_B S_j^beta P_B=0. Every two-body cross-block spin operator therefore has zero projected entangling action. If a bounded spin-only Hamiltonian assembled from such terms preserves each separate singlet code at every instant, its projected generator is a sum of one-block generators and cannot entangle the blocks.

This does not exclude virtual excursions, higher-body interactions, larger collective domains, measurement resources, or orbital degrees of freedom. The charge construction uses precisely the last escape: the spin-zero multiplicity space grows during the gate, while each block remains neutral to its own collective magnetic bath.

## 6. Supplied preparation, reset, and entropy export

Prepare the occupation pattern (2,0,2,0), then use reciprocal capture on pairs 12 and 34. This produces |0_L> up to a global phase. Both pairs are local spin singlets. The two releases may be scheduled sequentially, costing 2T_C, which avoids assuming additional parallel hardware.

A concrete source model is a fresh spin-independent filling reservoir at sites 1 and 3, and a draining reservoir at sites 2 and 4:

\[
 L^{\rm fill}_{i\sigma}=\sqrt\Gamma\,c^\dagger_{i\sigma},\qquad
 L^{\rm drain}_{j\sigma}=\sqrt\Gamma\,c_{j\sigma}.
\]

During loading, local hopping is off. Number-preserving spin and charging Hamiltonians do not change the defect-occupation equation. The sum of holes in filled sites and particles in emptied sites obeys

\[
 \mathbb E[D(t)]\le8e^{-\Gamma t}.
\]

The target occupation state is unique. Failure probability is at most this bound. Projecting a Stinespring dilation onto the target and using its polar isometry gives a replacement-channel amplitude error at most

\[
 \delta_{\rm reset}\le\sqrt{2\cdot8e^{-\Gamma t}}
 =4e^{-\Gamma t/2}.
\]

This is uniform over an old state correlated with memory and reference. The discarded information is transferred to the reservoir; it has not been erased reversibly or retrieved from the old bath.

The Markov loading law is a separately specified source model, not a deduction from an arbitrary bath Hamiltonian. A real reservoir must supply the needed particles, bandwidth, bias, temperature and renewal rate. In particular, a finite-band source cannot be assumed to retain a uniform Gamma across arbitrarily large unqualified loading transition energies. The strong-bath computational theorem does not remove this source qualification. One may instead supply preloaded closed-shell ports with the same stated preparation-error bound; their production cost must then be charged.

Finite reset time and reservoir replacement are part of every preparation/holding schedule. This is an initialized local resource architecture around an uninitialized retained medium.

## 7. Encoded measurement with renewed meters

After capture, logical 1 has n_1=1 and logical 0 has n_1=2. Only the earlier detector's long setting is needed. Its qualified conditional click probabilities are respectively at least .84 and at most .21. Threshold the frequency at .535.

For m fresh probes the conditional-moment-generating-function Chernoff bound gives

\[
 \eta_m\le e^{-m/4}.
\]

The constants are certified by the retained exact logarithmic bounds:

\[
 D(.535\|.21)>1/4,\qquad D(.535\|.84)>1/4.
\]

This does not use the weaker quadratic Hoeffding exponent and does not assume iid records. The single-call conditional qualification allows arbitrary prior memory/reference state.

Project the record isometry onto correctly and incorrectly classified records. The incorrect component has norm at most sqrt(eta_m). Polar normalization of the correct component costs at most 1-sqrt(1-eta_m). Since code sectors remain orthogonal, an ideal full encoded measurement instrument is within Stinespring norm

\[
 \delta_{\rm meas}\le\sqrt{2\eta_m}
 \le\sqrt2 e^{-m/8}.
\]

Reciprocal return and the known accumulated charging-phase correction restore singly occupied data. The output is the complete encoded Z instrument, not merely a correct classical label.

For a terminal rank-one encoded measurement, phase noise that only distinguishes its two measured sectors is harmless once absorbed into the outcome-conditioned memory map. Spin mixing, hopping during sensing, or disturbances inside the captured spin sector are not harmless. Their norm exposure grows with sensing time and is counted in E.

| Target Stinespring amplitude | Long probes m | Dimensionless reset time Gamma*t |
|---:|---:|---:|
| 1e-2 | 40 | 11.98293 |
| 1e-3 | 59 | 16.58810 |
| 1e-4 | 77 | 21.19327 |
| 1e-6 | 114 | 30.40361 |

These are isolated primitive budgets, not claimed threshold values. A meter cycle includes preparation, interaction, detection, processing and renewal. For cycle time t_m,

\[
 T_Z=2T_C+m t_m+
 { (2\phi-U m t_m)\bmod2\pi\over U}.
\]

The computation below fixes m at its base-level value. It does not increase m with computation length.

For a strictly local unwanted Hamiltonian of norm at most lambda, a useful exposure bound is

\[
 f(m)=\sqrt2e^{-m/8}+\lambda(T_{\rm fix}+m t_m),
 \qquad T_{\rm fix}=2T_C+2\pi/U .
\]

Its continuous minimizing probe count is

\[
 m_*=\max\{0,8\log[\sqrt2/(8\lambda t_m)]\}.
\]

Integer rounding gives the implemented choice. This is an optimum of an upper bound, not an information-theoretic lower bound on the best controller. It shows explicitly why infinite readout repetition is the wrong improvement operation at fixed imperfections. The outer code is used after choosing a finite base point with f(m) below its admitted local fault strength. General two-block residuals require the more conservative square-root fault-amplitude conversion in Section 10.

### Single-call qualification versus a many-location fault model

The earlier uniform detector bound is retained. It alone is not a theorem that arbitrarily many overlapping apparatuses sharing a memory obey a product fault-amplitude bound. For the threshold implementation used here, nominal meters and reservoirs are fresh local resources; nominal charge controls are scalar and local; common disturbances enter the bounded E model. An alternative implementation using strong operator-valued sensing couplings must separately establish the required many-location bound. A collection of average fidelities or individual diamond distances does not establish that bound.

## 8. A renewable leakage-reduction cell

Use three encoded blocks A,B,C. A carries data, possibly leaked. Prepare B,C in |0_L>. Apply H_B and CNOT_BC to create an encoded Bell pair. Apply CNOT_AB and H_A. Measure Z_A,Z_B. For results a,b apply X_C^b Z_C^a, or retain a protected Pauli frame.

For a valid input every corrected branch is the identity transfer A->C times its record amplitude. This statement includes an arbitrary reference and memory. For a leaked input the output C still lies in its computational code: it was prepared there, the Bell preparation keeps it there, A interacts only with B, and the final corrections preserve C's code. The charge-pattern theorem strengthens the physical implementation, since a leaked neighbor cannot force another block out of its code during an ideal entangler.

The circuit uses two preparations, two H gates, two CNOTs, two measurements and up to two physical Pauli corrections: ten base locations. Putting one such LRU before each input of a two-qubit gate gives at most alpha=21 base locations. Pauli-frame use can reduce this, but is not needed for the bound.

This is the established teleportation leakage-reduction construction. It is not a new purification protocol. It turns leakage into an ordinary unknown error on one output block; an outer code must correct that error.

A three-bank layout supplies reuse: data alternates A->C and C->A; the spent pair is reset to prepare the next Bell resource. Each wire needs twelve data spins in these three four-spin blocks, plus charge ports, meters, reservoirs, controllers and outer-code ancillas. Capacitive edges A-B and B-C suffice for the local cell. Cross-wire edges on both data banks supply encoded entangling gates. Any further routing uses actual compiled SWAPs, each three CNOTs, with holding charged throughout.

At the outer-code level, routing must itself be fault tolerant. In particular, swapping two data carriers from the same outer-code block can turn one faulty SWAP into two data errors. The local construction therefore uses dummy transport blocks, appropriately placed ancillas and correction during transit, as in Svore--Terhal--DiVincenzo. Long transport without intermediate correction is not assumed safe. The encoded teleportation cell supplies a finite elementary transport/replacement operation, while the published local compiler supplies its fault-tolerant placement.

## 9. Supplied outer correction operations

Use the established verified-ancilla Steane/concatenated-code compiler and the leakage-resistant version of its gadgets. Its requirements are preparation of |0>, |+>, H, T, T^dagger, CNOT, and X/Z measurement. All have finite implementations above. The code uses logical states of the four-spin blocks as its physical qubits.

For concreteness the Steane parity-check rows in the executable check are

\[
 (1000111),\quad(0101011),\quad(0011101).
\]

They are self-orthogonal over F_2 and have all seven distinct nonzero columns. X-type and Z-type versions give six stabilizers. The 21 single-site nonidentity Pauli errors have distinct nonzero syndrome pairs.

An ideal |0bar> encoder prepares seven |0> states, applies H to the three pivot sites, then nine pivot-to-parity CNOTs to generate the row span. H on all seven sites gives |+bar>. This ideal encoder is not assumed fault tolerant by itself.

The published gadgets encode two identical ancillas, compare them transversally, measure the comparison block and reject a nontrivial check before connecting the retained ancilla to data. LRUs are placed where the leakage-resistant construction requires them. Transversal CNOT, X/Z measurements, classical syndrome decoding and Pauli-frame updates perform correction. The non-Clifford step uses the compiler's verified/injected T resource, with physical T and fresh preparations supplied here.

Ancilla verification can reject. Rejection, finite factories, holding and routing must be included in an actual compiler and its constants. The abstract threshold theorem supplies finite fault-tolerant gadgets; this working construction does not claim to have compiled a complete geometrically local factory layout or calculated its malignant-pair constant. The small code check verifies the encoder and syndrome algebra only, not a device threshold.

A finite factory need not wait indefinitely. For a verification circuit that accepts with certainty in the ideal model, prepare two candidate verified ancillas in parallel and select the first passing one. If both reject, use a fixed fallback and record the failure. Both rejecting requires faults in both disjoint candidates, so this event cannot spoil the one-fault property of a distance-three gadget. More generally, with k candidates of at most s locations each, the local fault-amplitude hypothesis gives the conservative all-reject bound [(1+epsilon)^s-1]^k by inclusion-exclusion over marked sets. Their gates, reservoirs, selection logic and fixed waiting interval are real resources. An intrinsically probabilistic factory additionally needs a capped nominal failure budget; its random waiting time is not free.

## 10. Finite tolerance with retained, correlated memory

Let T_0 be a padded base-location duration including its real source, sensor, classical processing and holding times. Define the residual two-block row-sum action

\[
 \eta=T_0\sup_t\max_b\left(\|E_b(t)\|+
                         \sum_{c\ne b}\|E_{bc}(t)\|\right).
\]

The full norms are required, including leakage input states. A small bound for every pair separately is not sufficient when the row sum grows with system size.

The Aharonov--Kitaev--Preskill contraction argument gives the conservative local fault-amplitude strength

\[
 \varepsilon_{\rm pair}
 \le c_*\sqrt{2\eta},\qquad
 c_*=\exp(1+1/(2e)).
\]

One-body terms may be included as diagonal terms for this conservative bound. Strictly location-local faults can have a better linear bound.

Here is the mapping with the strong neutral bath made explicit. In a fine-grained fault expansion, keep H_strong and the nominal native operations unexpanded; their propagators have norm one. Only weak E insertions mark locations faulty. The norm/combinatorial contraction proof is unchanged by the unexpanded unitary factors. Logical correctness of a good path additionally needs those factors not to damage other valid blocks after leakage. That is precisely the local neutrality property established in Section 5. Intended gates act only on their declared one or two blocks; LRUs convert leaked inputs before later gates. Thus the leakage reduction argument applies. This extra correctness check is why merely observing zero strong coupling on an all-valid state would not suffice.

Let epsilon_0 be the local coherent fault strength of finite fresh source/meter operations and protected classical control in the specified model. Combining its fault expansion with that of E gives

\[
 \varepsilon\le\varepsilon_0+c_*\sqrt{2\eta}.
\]

The statement is an amplitude bound on sums of marked fault paths. It is not a stochastic independence claim and does not use a probability as a coherent amplitude. An imperfect classical controller that can issue an arbitrary correlated command to every block does not satisfy this assumption merely because its average error rate is small.

For an actual fault-tolerant compiler, let A be its maximal relevant pair count in a level-one extended rectangle, including its real routing and ancillas. A sufficient leakage threshold from Aliferis--Terhal has the form

\[
 \varepsilon < \theta,\qquad
 \theta={1\over e A\alpha},\qquad \alpha\le21
\]

for the stated base gate/LRU convention. No numerical A or device threshold is invented here.

This proves a nonzero tolerance constructively. Choose epsilon_0 <= theta/4 by finite readout and source durations. T_0 is then finite. Requiring

\[
 \eta <{\theta^2\over32c_*^2}
\]

makes the Hamiltonian contribution less than theta/4, leaving additional margin. Therefore the allowed row-sum coupling lambda=eta/T_0 is strictly positive and independent of the length of the intended computation.

Concatenation then reduces the logical error at successive levels, with the usual doubly exponential suppression in the number of levels and polylogarithmic overhead for a fixed compiled architecture. The physical sensor length, charge-control accuracy and protection-domain size remain fixed as the logical computation grows. A spatial implementation must use the corresponding geometrically local fault-tolerant compiler; arbitrary long-distance wiring is not free.

All initial memory/reference states are allowed in these norm statements. At an admissible checkpoint the retained memory can be arbitrary. The final guarantee covers the joint computation and its classical records. Conditioning on a rare bad syndrome record can increase conditional error; no claim of correctness for every postselected history is made.

## 11. Acquisition, stability and cost

The new capture requires scalar ratios and phases. The previous gain interval g in [1,2] does not supply them. Ordinary charge-Rabi/Ramsey experiments with renewable preparations and readout can acquire the needed finite collection of parameters. Optimal control, sweet-spot operation, composite pulses and robust phase estimation remain legitimate improvements under their actual assumptions.

The interrogations are available from the supplied operations. Prepare either D_L or D_R by filling/emptying the two source sites, apply a trial hopping pulse, then measure separated versus doubled charge. At zero pair detuning,

\[
 p_{D_L\to S}(t)=p_{D_R\to S}(t)
 ={2g^2\over\Omega^2}\sin^2(\Omega t),\qquad
 \Omega^2=U^2/4+4g^2.
\]

Frequency and contrast determine positive U and nonnegative g in a qualified alias-free scalar interval. Preparing both double occupancies also distinguishes the sign of detuning; near t=0,

\[
 p_{D_L\to S}(t)-p_{D_R\to S}(t)
 =-{2\over3}g^2U\epsilon\,t^4+O(t^6).
\]

The full three-state forward model is preferable to estimating a tiny fourth derivative. The executable ordinary least-squares example fits U,g,epsilon from ten synthetic charge probabilities and checks local Jacobian rank. It does not certify the entire illustrative box or demonstrate a shot-efficient device calibration.

After local gates are calibrated, prepare A in an encoded superposition and B successively in logical 0 and 1. Charge-hold Ramsey measurements on A determine E_00-E_10 and E_01-E_11. Their difference is J. Thus the entangling invariant and local compensating phases can be acquired without reconstructing every capacitance-matrix entry. Each interrogation still requires source preparation, coherent holding, rotations and readout. The strong collective magnetic memory does not enter these ideal signals because the probes remain total-spin zero.

For one simple acquisition upper bound, suppose a monotone measured probability p(x) has |p'(x)|>=s on a qualified scalar interval and a state-uniform model/readout bias at most b. To estimate x to Delta with failure probability alpha, independent or conditionally bounded shots give the sufficient count

\[
 N\ge{\log(2/\alpha)\over2(s\Delta-b)^2},\qquad s\Delta>b.
\]

The interval, slope and operator-norm bias qualification are not proved by this formula. They are physical information. For Delta=1e-3, s=1, b=2e-4 and alpha=.01 this conservative formula costs 4,139,311 prepared shots for one scalar. There is no claim that the present architecture has solved acquisition cost.

If statistical qualification failure is part of an overall target accuracy delta, choose its confidence accordingly; it cannot be left at one percent while claiming arbitrarily small total failure. This increases log(1/alpha) costs but does not require shrinking the admitted physical parameter error with computation length.

A finite calibration campaign cannot certify arbitrary future drift. Stability within the stated E bounds over a specified epoch is required. Recalibration and data holding between epochs must be charged. Long coherent powers for robust phase estimation are available only when the charge-control coherence and oracle implementation support them; they are not granted by the spin symmetry.

The ordinary Duhamel bound gives a useful local control budget:

\[
 \|U_{\rm actual}-U_{\rm nominal}\|
 \le\sum_j t_j\|\delta H_j\|
      +\sum_j\|H_j\||\delta t_j|,
\]

with the appropriate full joint norms. The arbitrarily strong collective term does not enter this budget on the protected sector. No bath derivative or local-orbit speed bound is required for that exactly commuting part. The earlier local-orbit machinery remains relevant to other mechanisms; it is not being misapplied to infer a small residual here.

## 12. Capacitive isolation and spectator costs

Density-density coupling is a real charge interaction, not an assumed logical ZZ operator. Nevertheless its control is an independent requirement.

The twelve-window example assumes a nominal addressable capacitive edge active during the hold and inactive during capture/return. Physical gating, a switched coupler, or motion into and out of an interaction region must realize this with stated finite time and residual error. The present note does not derive an arbitrary on/off ratio from a tunnel barrier. Bare Coulomb coupling does not vanish when interblock tunneling is closed.

An instructive failed shortcut is to replace the switched edge by the same always-on chi*n_A1*n_B1. Its ignored operator norm is at most 4|chi| during both capture/return and the compensating hold. Duhamel therefore bounds the gate discrepancy by

\[
 \delta_{\rm always\,on}\le 4|\chi|(2T_C+t_{\rm corr})
 \le112.2516\ldots|\chi|/U.
\]

Reducing chi/U makes this particular approximation better, but the intended entangling hold then grows as pi/chi. It does not establish a useful speed/noise advantage and does not solve spectator coupling to leaked blocks. This variant is not used to claim the threshold.

For a complete capacitance matrix, idle computational blocks all have the same occupations, so their nominal charge fields are logical scalars. That observation reduces some idle costs, but a leaked neighbor can have a different charge pattern. It cannot be discarded when qualifying the full-space row-sum error.

Long-range residuals require a summable bound. A conducting screening plane, for example, changes the static point-charge kernel from 1/r to 1/r-1/sqrt(r^2+4h^2), which decays as 2h^2/r^3. This can make a two-dimensional full charge row sum finite. It does not by itself make the coefficient small enough, remove dynamical electrode noise, or provide a switch. The threshold parameter must include those costs.

## 13. Comparisons and preserved failures

The older spin/charge compiler remains valuable when broad operator-valued positive coupling promises are available but precise coherent charge pulses are not. Its longer sequences and this calibrated coherent source have different information and hardware.

Kempe--Bacon--Lidar--Whaley already establish decoherence-free computation and concatenation with outer correction. Their explicit intercluster construction merges two blocks into a larger collective domain during the gate. The present charge gate keeps separate local spin-zero protection. This distinction is a noise-algebra statement, not a claim that all existing DFS proposals require a shared bath.

Fong--Wandzura supply exchange-only gates and leakage reduction. Modern reset-if-leaked schemes also have short exchange implementations. They are stronger comparators than an isolated old algebraic word. Singlet-only QUEX architectures already use four-electron total-spin-zero encoding and electric control, source/readout interfaces and charge sweet spots. Recent SAGE work uses gap-protected interblock exchange and refocusing. These may offer much better practical charge-noise performance.

Capacitive EO/ST proposals supply exact entanglers and optimized operating points under stated noise models. The current unoptimized capture is not shown to outperform them. The useful new guarantee to compare is independent-block neutrality plus a full leakage-compatible, retained-memory model.

Cavity-scattering, heralded optical entanglement and optical filtering can also feed error-corrected computation when their real local gates, sources, retained memories and loss/error model are supplied. The old long-photon survival penalty must not be charged to short renewed or heralded alternatives that do not incur it. No comparison by raw segment count establishes an advantage.

Preserved failures include: correct labels with destroyed within-sector information; unresolved dark double occupancy; restoration of apparatus without undoing logical damage; marginally mixed sources with hidden correlations; growing probe number at fixed symmetry-breaking strength; uncontrolled coherent inverse-bath assumptions; acquisition ignored in model-time comparisons; and the all-valid-only neutrality counterexample above.

## 14. Executable evidence

Run:

~~~sh
python p2_neutral_blocks/run_checks.py
~~~

The script verifies the 70-state fermionic Hamiltonian, spin-zero multiplicity, every native spin commutator, exact charge patterns, reciprocal return, pair phases, the supplied logical H, CZ, a general capacitance matrix, and a valid block adjacent to arbitrary leaked reference columns. It also checks a fast noncommuting two-dimensional collective memory, the extended-qutrit teleportation LRU, the infection counterexample, and the Steane syndrome/encoder algebra.

Typical double-precision residuals: CZ 2.3e-15; general capacitance 1.9e-15; local code preservation beside a leaked neighbor below 9e-16; retained noncommuting bath check 1.7e-14. The cross-block spin-exchange leakage witness is sqrt(3)/4 and the chosen magnetic-gradient leakage-generator norm is one. These nonzero witnesses are intentional failures.

The detector's Chernoff constants are rechecked using the preceding exact rational logarithmic enclosures. The matrix calculations are ordinary floating point and are not interval-certified uncertainty-box bounds. No noisy device, full fault-tolerant exRec or physical threshold has been numerically certified.

## 15. Primary research

- Kempe, Bacon, Lidar, Whaley, Theory of Decoherence-Free Fault-Tolerant Universal Quantum Computation: https://arxiv.org/abs/quant-ph/0004064 .
- Aliferis, Terhal, Fault-Tolerant Quantum Computation for Local Leakage Faults: https://arxiv.org/abs/quant-ph/0511065 .
- Aharonov, Kitaev, Preskill, Fault-tolerant quantum computation with long-range correlated noise: https://arxiv.org/abs/quant-ph/0510231 .
- Aliferis, Gottesman, Preskill, Quantum accuracy threshold for concatenated distance-3 codes: https://arxiv.org/abs/quant-ph/0504218 .
- Svore, Terhal, DiVincenzo, Local Fault-Tolerant Quantum Computation: https://arxiv.org/abs/quant-ph/0410047 . The analytic local-architecture construction, not its illustrative stochastic numerical thresholds, is used here.
- Fong, Wandzura, Universal Quantum Computation and Leakage Reduction in the 3-Qubit Decoherence Free Subsystem: https://arxiv.org/abs/1102.2909 .
- A reset-if-leaked procedure for encoded spin qubits: https://arxiv.org/abs/2012.09517 .
- Feng, Zaw, Koh, Two-qubit sweet spots for capacitively coupled exchange-only spin qubits: https://arxiv.org/abs/2103.15681 .
- A quadrupolar exchange-only spin qubit: https://arxiv.org/abs/1807.10471 .
- Foulk, Laubscher, Hoffman, Das Sarma, Singlet-only always-on gapless exchange spin qubits: charge noise effects and two-qubit gates (2026 preprint): https://arxiv.org/abs/2604.15419 .
- Quantum dot spin cellular automata for realizing a quantum processor: https://arxiv.org/abs/1310.4376 .
- Kimmel, Low, Yoder, Robust Calibration of a Universal Single-Qubit Gate-Set via Robust Phase Estimation: https://arxiv.org/abs/1502.02677 . The retained preceding source identifies the 2021 erratum as Phys. Rev. A 104, 069901: https://doi.org/10.1103/PhysRevA.104.069901 . No uncorrected numerical RPE claim is used here.
- Duan, Wang, Kimble, Robust quantum gates on neutral atoms with cavity-assisted photon scattering: https://arxiv.org/abs/quant-ph/0505054 .
- Barrett, Kok, Efficient high-fidelity quantum computation using matter qubits and linear optics: https://arxiv.org/abs/quant-ph/0408040 .
- Leung, Ralph, Improving the Fidelity of Optical Zeno Gates via Distillation: https://arxiv.org/abs/quant-ph/0609224 .

The new derivation retains root-working status. Earlier accepted foundations are not revised by this construction.
