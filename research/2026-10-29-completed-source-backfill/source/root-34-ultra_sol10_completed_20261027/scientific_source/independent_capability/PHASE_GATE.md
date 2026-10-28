# A restricted phase-only logical operation; not a cleared new capability

This calculation imports the already completed chiral loader in
../../sol8_opportunity_selection_20261027/chiral_loading/OPERATION.txt.
Bath doubling, the central rather than ground gap, and the physical cost
of coupling the two bath copies by Q remain unchanged. There is no new
loader claim. The new local derivation concerns a logical operation after
loading and unloading. It is not independently audited, and its historical
priority and advantage over ordinary holonomic control remain UNKNOWN.

## Supplied control contract

The bare logical space is C²; the two auxiliary spaces have dimension r.
Fixed Q=Q*>=B I>0 and G:C²->C^r are unknown. The supplied chiral plant is

    H(eta,phi) = [[0, eta D(phi)* G*, 0],
                  [eta G D(phi), 0, Q],
                  [0, Q, 0]],
    D(phi)=exp(i phi P), P=diag(1,0).

Only a scalar eta and the phase of one source column are changed. No
arbitrary G->GU port mixer is assumed. A calibrated native phase D(phi)
can also be applied to the bare logical code when eta=0. These bare phase
controls all commute and do not already provide a mixing gate.

An engineering bound Gamma>=||Q^-1G|| and a gap bound B are supplied.
Quantum preparation/readout of the three positive Pauli eigenstates and
Pauli measurements on the returned bare code are supplied separately.
Their accuracy, reset cost and physical realization are not inferred from
the Hamiltonian. Leakage is counted as an erasure, not postselected away.

Put W=Q^-1G, L=W*W, a=1/(2 Gamma), C=(I+a² L)^(-1/2), and M=C P C.
The case Gamma=0 is trivial and has no mixing capability.

## Exact ideal logical action

Load eta from zero to a at phi=0. The supplied parallel dark isometry is

    V_eta=(I,0,-eta W)^T (I+eta²L)^(-1/2).

At fixed eta=a, use the frame E_phi=diag(D(phi)*,I,I)V_a. It satisfies

    E_phi* dE_phi/dphi = -i C P C = -i M.

Its parallel logical coefficient is therefore exp(i phi M). Unloading at
the final phase gives D(phi)* exp(i phi M) on the original bare code.
Apply the known native D(phi) to obtain exactly

    U(phi)=exp(i phi M).                                  (1)

Resetting the source phase while eta=0 has no Hamiltonian effect. Equation
(1) is a physical logical operation after a closed source-coupling path,
with the specified endpoint-frame correction. It is not a claim that the
phase-dependent Hamiltonian automatically supplies a free arbitrary gate.

M has rank one, p=tr M in [4/5,1], and can be written
M=(p/2)(I+n.sigma). The nonzero component of C|0> determines n. If L01!=0,
then n is not the native z axis. This activates an additional logical
rotation axis using only the restricted controls above.

For Lambda=Gamma² and rho=|L01|/Lambda, the divided-difference formula for
f(t)=(1+a²t)^(-1/2) gives

    |C01| >= a² |L01|/[2(1+a²Lambda)^(3/2)]
           =rho/(5sqrt(5)),
    C00<=1.

The angle delta between n and z therefore obeys

    delta=2 arctan(|C01|/C00)
          >=2 arctan[rho/(5sqrt(5))]>0.                    (2)

This is a conditioned statement. No universal quantitative capability
follows if the off-diagonal Gram entry can be arbitrarily small or zero.

## Finite-time bound independent of bath size and upper bandwidth

For a linear eta ramp over duration T_l, the accepted reduced-inverse
identity, with its ordered noncommuting factors, is

    H_eta^+ V'_eta=(0,-Q^-1 W(I+eta² L)^(-3/2),0)^T.

Endpoint norms are at most Gamma/B. The eta derivative norm is at most
3 eta Gamma³/B. Duhamel integration by parts on eta in [0,a] yields

    ||U_load V_0-V_a||
       <=a[2Gamma+(3/2)a²Gamma³]/(B T_l)
       =19/(16 B T_l).                                 (3)

The reverse ramp has the same bound. No spectrum of L is needed for this
weak-dressing linear ramp. This is not a claim about strong transfer or
an improvement of the old optimized loading schedule.

For a linear phase sweep phi(t)=omega t, T_p=|phi/omega|, transform to the
rotating frame. The constant Hamiltonian there is H_a-omega P_C, where P_C
is the projector P extended by zero on the auxiliary spaces. Let Pi be the
dark projector and Y=H_a^+(I-Pi)P_C V_a. Then ||Y||<=1/B and
H_a Y=(I-Pi)P_C V_a. Compare the exact evolution with
V_a exp(i omega t M). One integration by parts, using H_a-omega P_C,
not an invented inverse with a preserved gap, bounds the error by

    2|omega|/B+2omega² T_p/B
       =2|phi|(1+|phi|)/(B T_p).                         (4)

The two integral terms use ||M||<=1 and ||P_C||=1. This argument does not
differentiate the unknown Q or commute it through L. Summing (3), (4)
and the reverse-ramp error gives the complete primitive's operator-norm
isometry error. It includes an untouched entangled reference and every
leakage branch. Native phase-pulse errors are additional paid terms.

For a logical rotation angle at most pi about n, choose phi=-theta/p.
Since p>=4/5, |phi|<=5pi/4. The bound is finite and dimension independent,
but it scales as 1/(B epsilon) and is not a speed advantage.

## Actual logical synthesis and action-only acquisition

Native z rotations and rotations about n allow arbitrary SU(2) synthesis.
The synthesis principle is established prior science: Lowenthal's theorem
and Hamada, [Royal Society Open Science 1:140145 (2014)](https://doi.org/10.1098/rsos.140145).
Here is an explicit construction used by the replay, rather than a claim
of a new two-axis theorem. Rotate the azimuth of n into the xz plane using
native z phases. To implement Ry(beta), 0<=beta<=pi, split beta into pieces
b<=2delta. For each piece put

    theta=2 arcsin[sin(b/2)/sin(delta)],
    zarg=arg[cos(theta/2)-i cos(delta)sin(theta/2)],
    alpha=zarg+pi/2, gamma=zarg-pi/2.

Then Rz(alpha) Rn(theta) Rz(gamma)=Ry(b) in that aligned frame. At most
ceil(pi/(2delta)) non-native rotations and native z phases implement any
middle Euler rotation. The source phase is -theta/p. No arbitrary logical
unitary was supplied through a source mixer.

Calibrate the returned primitive at phi0=pi/2 using only three input Pauli
states and three output Pauli measurements: nine settings. Its Bloch
rotation angle lies in [2pi/5,pi/2], away from the axis-estimation
singularities at zero and pi. Thus p and n are stably acquired without
learning Q, G or the bath spectrum. The replay retains the actual synthetic
multinomial records, including erasures, and compiles Ry(pi/2) from the
estimated generator. The generator used to synthesize those records is
separate from the synthesis routine's input.

For a prespecified entry tolerance t and confidence failure alpha, bounded
Pauli outcomes in [-1,1] require at least

    nshot=ceil[2 t^(-2) log(18/alpha)] per setting

by a simultaneous Hoeffding bound. Finite primitive error epsilon_cal adds
at most 2epsilon_cal to every mean error. An entry error e gives Frobenius
error at most 3e; closest-SO(3) projection at most doubles that error. In
the stated angle interval, the recovered M error is bounded by 12e when
the rotation-matrix error is below 1/10. The finite word then has generator
error at most (5pi/4)N||Mhat-M|| plus N execution errors and native phase
errors. These are finite-cost bounds, not the much smaller point estimate
reported by a particular synthetic draw.

With a supplied rho floor, N=O(1/rho), t=O(epsilon/N), and primitive accuracy
O(t), the conservative preparation/readout count is
O(N² epsilon^-2 log(1/alpha)); total calibration evolution time is
O(N³ epsilon^-3 log(1/alpha)/B). Native phases, reset, readout, SPAM
calibration, control precision and host acquisition are extra costs.

## Why this is parked rather than promoted as a new capability

Geometric logical gates, indirect control and qubit process tomography are
established methods. The restricted-control formula and bounds above are a
specific derived operation, not evidence of world novelty. A competent
equally informed holonomic-control comparator can use the same phase loop,
the same qubit-only calibration and the same two-axis synthesis. No sample,
time, energy or hardware advantage over that comparator has been shown.

The original d-by-d Schur counterterm has not become an r-by-r tomography
cost merely because r is large. The chiral replacement still purchases the
second complete bath and its off-diagonal Q coupling. Chiral-symmetry
breaking error Delta H accumulates at most ||Delta H||T by Duhamel; the
slow calibration/gate bounds can therefore require very small detunings
and losses. A central spectral gap does not supply passive ground-state
protection. No physical doubled-bath device or qualified logical qubit is
acquired. Broad unknown-bath cancellation alone is not an advantage claim.

This bounded operation is retained, but the independent breadth search
must move on rather than treat a modest holonomic bound as a breakthrough.
