# Constant-gap singlet-membership test using three measurement axes

2026-10-29. New author derivation; independent review pending. No historical
novelty or hardware advantage is claimed.

For even n, let P be the full total-spin-zero projector. Choose a uniformly
random axis a in {x,y,z}, measure each of the n qubits in that Pauli basis,
and pass iff the total measured magnetization is zero (exactly n/2 outcomes
of each sign). Let T=(Pi_x,0+Pi_y,0+Pi_z,0)/3 be the pass effect.
Then

    P <= T <= P + beta_n (I-P),
    Tr[(I-P)rho] <= q/(1-beta_n), q=1-Tr(T rho),

with exact beta_n:
- n=2: 1/3;
- n=4 or6: 1/2;
- all even n>=8: 7/12.

Thus at most (12/5) times the failure probability bounds singlet leakage,
independent of n, without a coherent total-spin measurement or encoder matrix.
The bound holds for the reduced state of a register entangled with any reference.

## Proof
Decompose the n-qubit Hilbert space into integer spin-j representations tensored
with permutation multiplicities. Each Pi_a,0 is block diagonal in j and is
|j,0_a><j,0_a| tensor the identity on that multiplicity. For j=0 all three are
identity. For integer j>=1, the overlap between two zero-magnetization states
whose axes are perpendicular is c_j=P_j(0), the degree-j Legendre polynomial
at zero, after consistent phase choices. This is the standard Wigner d^j_00
rotation matrix element. Equivalently these vectors are normalized zonal
spherical harmonics centered on the three axes.

For odd j, c_j=0. For j=2r,

    c_(2r)=(-1)^r binom(2r,r)/4^r.

The three-vector Gram matrix has diagonal1 and all off-diagonal entries c_j;
its eigenvalues are 1+2c_j,1-c_j,1-c_j. The nonzero eigenvalues of the spin-j
pass effect are those values divided by3. At j=1 the value is1/3; at j=2 the
largest is1/2. For positive c_j with j>=1, the largest is c_4=3/8. For negative
c_j, the most negative is c_2=-1/2. Indeed the absolute values decrease because
|c_(2r+2)|/|c_(2r)|=(2r+1)/(2r+2)<1. Therefore the global largest non-singlet
pass eigenvalue is (1+2*(3/8))/3=7/12, attained at spin4, if that sector exists.
For n<=6 it does not, giving the stated sharper coefficients. Positivity and
block diagonality yield the operator inequality and leakage bound.

## Encoder acquisition interface
For an actual unknown encoder E:C^K->(C^2)^tensor n, prepare uniformly random
computational basis inputs (mean I_K/K), invoke E, and apply the three-axis
test. This directly bounds lambda=Tr[(I-P)E(I_K/K)]. No full encoder tomography,
logical entangled reference, or ideal inverse-encoder implementation is used.

This is an average-input leakage certificate, not a dimension-free bound for
every unrandomized logical input. A subsequent logical Pauli randomization can
make this average relevant in a full-channel construction, but that is an
actual additional operation with a separate proof.

For a learned local frame W, measure in the corresponding conjugated local
axes, or undo W before the three-axis readout. Their calibration must be part
of the trusted measurement interface; common-axis measurement does not verify
unknown miscalibrated detectors against itself.

The test requires n single-qubit measurements and at most n basis-change gates,
plus one uniform trit and classical counting. It needs no two-qubit gates.
Under an iid stationary encoder with trusted measurements, zero failures in N
trials gives q <=1-alpha^(1/N) with confidence1-alpha. Thus leakage lambda<=epsilon
can be certified at zero observed failures using
N>=log(alpha)/log(1-(1-beta_n)*epsilon).
These statistical statements do NOT transfer automatically to a future encoder
with arbitrary changing memory. The per-state operator inequality remains
valid for each actual trial, but future control guarantees require a valid
common channel/causal acquisition argument.

## Primary comparison
Imai, Toth and Guhne, Phys.Rev.Lett.133,060203 (2024), develops collective
randomized measurements; collective measurement is established machinery.
https://doi.org/10.1103/PhysRevLett.133.060203 (abstract read 2026-10-29).
The Wigner/Legendre relation is also explicitly stated in the primary research
paper Laliena et al., J.Appl.Cryst.53 (2020),512-529, Appendix B, Eqs39-43:
https://journals.iucr.org/j/issues/2020/02/00/in5032/ .
Neither source is claimed to state this precise three-axis leakage coefficient;
priority has not been cleared. The all-j calculation above is the governing
argument; finite matrix checks are supplementary.
