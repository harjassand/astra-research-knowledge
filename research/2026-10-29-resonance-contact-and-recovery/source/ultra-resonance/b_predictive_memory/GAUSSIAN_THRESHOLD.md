# An extensive sharp boundary for positive Gaussian trajectories

This is a constructive challenge to the proposed Gaussian simulation route,
not a classical-complexity lower bound or a novelty clearance. It identifies
an exactly sharp physical noise threshold on a whole family and the fair
ordinary global-feedback comparator. No new physical input was acquired.

## 1. Model and exact statement

There are `2(p+q)` fermionic modes, grouped into `p+q` ordered dual-rail pairs.
The initial and invariant sector has exactly ONE fermion per pair. On pair a,
write `Z_a=n_(a,+)-n_(a,-)` and let `r=(1,-1)^T`. The interaction is

    H_int = sum_(a in L,b in R) J_ab Z_a Z_b,

for an arbitrary real p-by-q matrix J. Any additional quadratic Hamiltonian
acts within individual pairs. The dephasing convention is

    L rho = -i[H,rho] + gamma sum_i D[n_i]rho,
    D[L]rho = L rho L* - {L*L,rho}/2.

Equivalently, the physical dephasing matrix can be `Gamma=gamma P`, where P
is block diagonal with blocks `rr^T/2`; it gives precisely the same channel
on this sector. Each pair has logical dephasing `(gamma/2)D[Z_a]`.

**The threshold is gamma_c=2||J||_op.** At and above the threshold, every
Gaussian initial state in this sector stays convex-Gaussian for all times.
Below the threshold, the explicit bonding-product Slater state leaves that
set immediately. This statement concerns this invariant sector and positive
Gaussian decompositions. It does NOT say that every method of classical
simulation fails below the threshold.

The sufficiency extends to a supplied efficiently sampled Gaussian mixture.
Existence of an arbitrary convex-Gaussian decomposition is not an initial
sampling oracle, and a complete finite-precision trajectory implementation
is not acquired by this note.

## 2. Why the sector makes Gaussianity a testable physical boundary

A Gaussian density operator supported on fixed total particle number has
zero anomalous covariance and `Var(N)=Tr[C(I-C)]=0`. Consequently C is a
projection and the state is a pure Slater determinant. Exact pair charges
make its off-pair covariance blocks zero. Each remaining 2-by-2 block has
rank one. Thus it is a product of one occupied orbital in each dual rail.

If a convex-Gaussian state is supported on the pair-charge sector, every
positive component in its Gaussian decomposition is supported there:
`Tr(P_sector^perp rho)=0` is a sum of nonnegative terms. Hence, under the
ordered dual-rail identification, convex-Gaussian states in this sector are
exactly fully separable logical-qubit states. The converse follows by taking
the wedge product of the one-particle orbitals. Fermionic ordering only
fixes a common convention for this identification.

This argument would be invalid after arbitrary hopping between pairs:
those pair charges would no longer be conserved. Only total-charge
conservation is insufficient for this particular separability equivalence.

## 3. A general infinitesimal lower bound, with no many-body reconstruction

Start all logical qubits in |+>, a known bonding-product Slater state. Use
the X basis, so the initial state is the vacuum |0...0>. Partially transpose
the RIGHT logical partition. Compress the derivative of rho^T_R at time
zero to the single-flip vectors, first those in L and then those in R.
The exact compressed matrix is

    K = [[gamma I_p/2, -i J],
         [ i J^T,       gamma I_q/2]].                 (1)

To check the Hamiltonian sign directly, `-iJ[Z_aZ_b,rho_0]` is
`-iJ(|ab><0|-|0><ab|)` before partial transpose and
`-iJ(|a><b|-|b><a|)` afterwards. Local dephasing creates a single flip with
weight gamma/2. A pair-local Hamiltonian connects the vacuum to a single
flip and has zero compression to the single-flip nullspace; it does not
alter (1).

For singular vectors `Jv=sigma u`, `J^T u=sigma v`, the vector
`(u,-iv)/sqrt(2)` has eigenvalue `gamma/2-sigma`. If gamma<2||J||, its
expectation is zero at t=0 and has strictly negative derivative. Analyticity
of the finite-dimensional semigroup makes rho^T_R nonpositive for every
sufficiently small positive t. The state is therefore entangled across
L/R and, by section 2, is not convex-Gaussian. The argument works for every
p,q and every nonzero real J; no small-mode extrapolation is involved.

More generally, for two dual rails with correlated logical dephasing G,
the compressed 2-by-2 matrix is

    [[G11, -G12-iJ], [-G12+iJ, G22]].

Its determinant is `det(G)-J^2`. This is the familiar
measurement/noise-versus-entanglement test, transferred explicitly to a
fixed-charge fermionic sector, not a new entanglement principle.

## 4. Matching ordinary global-feedback upper bound

In physical occupation coordinates,

    U = [[0,J],[J^T,0]] tensor rr^T,
    H_int = n^T U n/2,          ||U||=2||J||.

For gamma>0 choose local measurement strengths `D=gamma I/2`, and
feedback observables `F_i=sum_j U_ij n_j/(2 sqrt(D_ii))` coupled to
measurements `L_i=sqrt(D_ii)n_i`. The standard measurement-feedback master
equation has Hamiltonian

    sum_i (L_i F_i+F_i L_i)/2 = n^T U n/2

and dephasing matrix `D+U D^-1 U/4`. The imaginary cross terms cancel
because U is real symmetric. The residual phase-noise matrix is

    R = gamma I/2 - U^2/(2 gamma) >=0

exactly when gamma>=||U||. Each local number measurement is Gaussian
because `n_i^2=n_i`; feedback and residual stochastic phase rotations are
quadratic Gaussian operations. Pair-local quadratic evolution also stays
inside this class. Their normalized, positive measurement trajectories
prove the all-time upper bound, including equality at the threshold. The
zero-interaction/zero-noise corner follows separately by free evolution.

This uses established full global/broadcast feedback. On the pair-charge
sector the replacement `Gamma=gamma P -> gamma I` adds only Lindblad
operators proportional to conserved pair charges, hence adds ZERO physical
dephasing there. Therefore the singular covariance does not, in this
family, produce a separation from an equally informed ordinary global
feedback construction. A projected cone is a useful compiler for the
equivalence; it is not a new physical noise-removal mechanism.

## 5. Exact separation from every gauged edgewise row-sum rule

Let p=q=k, let H_k be a normalized real Hadamard matrix, and set J=H_k/2.
Then the exact threshold above is ONE. For powers k=4^r all data can be
rational; the conclusions are not limited to those powers when algebraic
input is allowed.

Give an edgewise row-sum incumbent every diagonal and pair-charge
Hamiltonian gauge `U'=U+diag(s)+CV^T+VC^T`, with C the pair-incidence
matrix. In each 2-by-2 cross-pair block B_ab, the signed contrast is

    r^T B_ab r = 4 J_ab.

Every allowed gauge cancels in this contrast. Thus the sum of absolute
entries in B_ab is at least 4|J_ab|. Counting also the transpose blocks,
the total off-diagonal absolute sum is at least `8 sum_ab |J_ab|`.
There are 4k physical rows, so

    max_i sum_(j!=i)|U'_ij| >= 2 sum_ab|J_ab|/k = sqrt(k).

The original U attains equality. Therefore the optimized row-sum threshold
is EXACTLY sqrt(k), while full global feedback and the necessary physical
Gaussianity threshold are both ONE. This identifies where the gain comes
from: coherent global feedback geometry, already present in the ordinary
mechanism, rather than fixed-charge wording or a new family of noiseless
predictions.

## 6. Consequence for the current allocation

The root cone is worth retaining as a constructive, input-checkable
tractability compiler. The honest opportunity is an explicit useful model
whose ACTUAL noise and available initial-state preparation pass the cone
and whose requested output is costly for equally informed existing
Gaussian-trajectory/global-feedback software. A separation from edgewise
thresholds alone does not supply that evidence. In particular, making the
added noise invisible by putting it entirely in conserved-charge
directions cannot pay for a genuine non-Gaussian interaction on the sector.

The threshold above is a sharp lower certificate for this representation,
not a hardness theorem. It suggests testing a different representation
below the cone, rather than trying to optimize the same positive-Gaussian
promise indefinitely. No finite-temperature Gibbs preparation, arbitrary
convex-mixture sampling, physical calibration or advantage is inferred.

Primary comparison: Gaona-Reyes--Carlesso--Bassi (2021), arXiv:2007.11980,
sections III/IV, already supplies broadcast/multibody measurement feedback;
Kafri--Taylor--Milburn (2014), NJP16 065020, supplies the sharp two-system
noise/entanglement antecedent. Gonzalez-Garcia et al. (2025), PRL135190401,
arXiv:2502.05658, proves efficient positive Gaussian-mixture simulation
above dephasing thresholds, with intersite extensions in its supplement.
Their statements must not be replaced by a weaker generic-noise baseline.
This note does not claim a priority clearance for the sector/compiler or
for its transferred extensive threshold.
