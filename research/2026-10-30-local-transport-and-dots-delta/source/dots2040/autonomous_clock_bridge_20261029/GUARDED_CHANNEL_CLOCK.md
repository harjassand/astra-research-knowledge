# Exact finite-rate channel clocks with coherent local exclusion

2026-10-29. Root construction, submitted for independent challenge. This is an exact model-level compiler, not a noise-threshold theorem, two-body implementation, measured device, or historical novelty claim.

## Intended consequence and actual contract

Approximate adiabatic elimination of damped auxiliaries gives useful local-observable simulation bounds but does not automatically give a threshold-compatible fault law uniform in runtime. Seek a different mechanism: every completed physical reset event should enact the desired channel EXACTLY at finite coupling/decay rates. Overlapping channels must not corrupt pending operations.

Input: finitely supported CPTP maps Phi_x(rho)=sum_s K_xs rho K_xs*, sum_s K_xs* K_xs=I. Make an overlap graph: an edge connects any two boxes with overlapping data support. Assume bounded support, graph degree and Kraus number if claiming fixed local resources. All operators, their calibration and geometric placement are supplied, not learned here.

At each x provide one (m_x+1)-level auxiliary with ready |0> and excited labels |s>, s=1,...,m_x. Define

    V_x = sum_s K_xs tensor |s><0|_x,
    P_x=|0><0|_x, Q_x=I-P_x,
    G_x=product_{y adjacent x} P_y,
    H=sum_x g_x G_x(V_x+V_x*) ,
    L_xs=sqrt(kappa_x) I_data tensor |0><s|_x.

H is Hermitian because its guard acts on different auxiliaries. The resets are one-body; H is local but generally many-body, not two-body. Positive finite g_x,kappa_x are arbitrary; no fast-reset limit is taken. Initialize all auxiliaries ready.

## Exact invariant isometry

Let independent sets S of the overlap graph label an abstract clock Hilbert space. Put W_empty psi=psi tensor |0...0> and

    W_S psi=product_{x in S} V_x W_empty psi.

For independent S the data supports are disjoint, so products commute. Completeness of each Kraus family makes W_S an isometry; distinct S have orthogonal auxiliary occupancy patterns. Thus W(|S> tensor psi)=W_S psi is an isometry.

Let a_x|S>=|S\{x}> if x in S and0 otherwise. Its adjoint creates x only when the enlarged set is independent. Then

    H W = W [sum_x g_x(a_x+a_x*) tensor I],
    L_xs W = W [sqrt(kappa_x) a_x tensor K_xs],
    (sum_s L_xs* L_xs) W = W [kappa_x a_x* a_x tensor I].

Proof: adding a nonadjacent box appends its isometry. Removing an active box uses V_x*V_x=I on ready inputs. Guards prohibit all incompatible additions. After emission at x, every still-active box is disjoint from x, so K_xs commutes past its pending isometry. The summed no-jump term is kappa_x Q_x. An individual L_xs*L_xs need NOT preserve the image of W; only the summed term does. Keeping that distinction is essential.

Therefore the FULL Lindblad generator preserves W's image and is intertwined with an abstract hard-core clock Hamiltonian and jump operators sqrt(kappa_x) a_x tensor K_xs. This is not an approximate effective generator.

## Exact event semantics and its boundary

Condition on emission times and locations but sum over Kraus labels. No-jump evolution acts only on the abstract clock. An emission at x applies a_x to its clock and EXACTLY Phi_x to data. If clock and data start uncorrelated, they remain uncorrelated conditional on the time/location history; the distribution of that history is independent of the quantum input. This also holds with an arbitrary external reference entangled with the data.

Without conditioning, clock and data can be classically correlated through the event history. In physical coordinates pending operations are coherent encodings W_S; tracing auxiliaries at an arbitrary time does NOT necessarily reveal just the completed channel sequence. A readout must drain or decode pending operations, or use an output contract that explicitly retains them. Global empty-clock postselection is not free and may be exponentially unlikely. No such readout operation is assumed here.

For an isolated box, the bundled-Kraus construction reduces to scalar damped Rabi motion and exact renewal events. The independent worker derives a three-stage phase-type waiting law in the overdamped regime. Interacting hard-core clocks are not independent renewal processes; importing isolated timing distributions into the overlap graph would be wrong.

## A bounded-depth local frame, not a physical gate assumption

For each x choose a unitary U_x on data-support x and the excited auxiliary subspace that maps psi tensor |1> to sum_s K_xs psi tensor |s>. Extend it by identity on ready auxiliary states. Such a unitary exists because the two subspaces have equal dimension and the Kraus map is isometric. Guard U_x by all adjacent auxiliaries being ready. These guarded unitaries preserve every auxiliary occupancy bit.

Two adjacent guarded U's cannot both act nontrivially in any occupancy sector; two nonadjacent ones act on disjoint data (and only share commuting guard projectors). Hence they commute, and coloring gives a bounded-depth geometrically local extension U whose restriction to the abstract independent-set code is W. The abstract excited label is fixed |1> before this change of frame.

Consequently conjugating a local physical error by U enlarges its support by at most a fixed neighborhood and preserves its operator norm. This is a useful locality interface, NOT a proof that errors remain in the clean invariant subspace. Errors may create incompatible occupied auxiliaries or excite internal complementary directions; their subsequent recovery and fault spread still require analysis. A small global channel error cannot replace that analysis.

## Exact finite test

`check_guarded_channel_clock.py` builds a72-dimensional physical system: two data qubits, amplitude-damping channel on each, and an overlapping CNOT channel in the middle. The overlap graph is a three-vertex path, with five independent clock states. Exact rational arithmetic verifies isometry, Hamiltonian intertwining, every emission intertwining, and total no-jump intertwining. Removing the guards fails; treating individual Kraus no-jump terms as separately preserving the image also fails. This is a finite regression for the general algebra, not a threshold test.

## Remaining decisive operations and comparator

1. A joint timing/fault law for the interacting clocks, sufficient for autonomous correction, not just mean progress.
2. Repair/control of occupancy and Stinespring-complement errors under imperfect resets and physical storage noise.
3. Actual bounded two-body implementation of the guarded many-body H, preserving a local fault contract at fixed resources.
4. Preparation, pending-update readout, and the physical entropy/work interface for the reset reservoirs. One-body Markovian resets are supplied ideal operations at this stage; finite-temperature excitation is not included in the exact theorem.

Classical antecedents must be compared before novelty: Feynman/space-time circuit-to-Hamiltonian isometries, dissipative computation, precisely timed dissipative gadgets (Kastoryano–Wolf–Eisert2013, DOI10.1103/PhysRevLett.110.110501), and damped-ancilla analogue simulation (arXiv:2404.11081). The proposed distinction is an exact finite-rate completed-channel semantics with local coherent exclusion, not the invention of autonomous computation or a claim to have built its missing microscopic hardware.
