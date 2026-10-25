# Fixed-gap charge elimination with relative detuning control

26 October 2026. This is an actual full-charge reduction of the canonical
memory, not an assumed two-level Hamiltonian. Its load-bearing benefit is
RELATIVE control of the sector-changing term at fixed E_R, plus an explicit
normal-ladder truncation bound. It does not turn the resulting common bath
into a Gaussian bath or supply finite-temperature infrared universality.

## 1. Exact block structure

Use the unrephased ladder of CANONICAL_SECTOR_RESPONSE.md, normal j>=0,
d_j=j+1/2, T the half-line adjacency, P_0=|0><0|:

    H_eta=H_G+E_R d^2-lambda Y(T+sigma_z P_0)
                         +2E_R eta sigma_x d+E_R eta^2.           (1)

All Gaussian support/lead modes remain in H_G. Let P select normal j=0,
while retaining its two sector labels and the WHOLE Gaussian Hilbert space.
The complement j>=1 has no sigma_z term at all. In the sigma_x eigenbasis
its two exact operators are

    H_ex,s=H_G+E_R(d+s eta)^2-lambda Y T_ex,
    s=+1,-1.                                        (2)

The sole P-to-complement matrix is -lambda Y from normal0 to normal1,
times the spin identity. Let R_s,11(z) be the first normal block of
(H_ex,s-z)^-1 and set

    Sigma_s(z)=lambda^2 Y R_s,11(z)Y,
    Sigma_0=(Sigma_++Sigma_-)/2,
    Sigma_x=(Sigma_+-Sigma_-)/2.

The EXACT Schur/Feshbach inverse on P is

    P(H_eta-z)^-1P = F_eta(z)^-1,
    F_eta(z)=H_G+E_R/4+E_R eta^2-z-Sigma_0(z)
             -lambda Y sigma_z+[E_R eta-Sigma_x(z)]sigma_x.     (3)

The operator products are understood as quadratic forms on the natural
Gaussian energy core, then by closure. A finite Gaussian/charge regulator
gives the elementary matrix identity; the bounds below justify its form
limit. Equality of compressed inverses is not equality of Hilbert spaces,
thermal ensembles, observables or real-time generators.

At eta=0, Sigma_x=0 EXACTLY. The entire high-charge correction is then
common to the two sectors. At nonzero eta it creates a transverse operator,
not an unpriced longitudinal bias. This follows from the literal block
structure, not from a truncation-error slogan.

## 2. A uniform energy form for the actual Gaussian host

At finite pinned lead length put E_G=inf spec H_G, H_g=H_G-E_G>=0.
Let

    C=<v,K^-1v>, V_g=<Y^2>_(Gaussian ground).

The exact normal-mode annihilation estimate gives the operator form

    Y^2 <=2C H_g+2V_g.                               (4)

Indeed write Y=a(f)+a^dagger(f). Then
||Ypsi||^2<=4||a(f)psi||^2+2||f||^2||psi||^2,
||f||^2=V_g, and ||a(f)psi||^2<=C<H_g>/2.
This includes bound and propagating modes. It does not replace H_G by
its extensive absolute ground energy in a local estimate.

For the actual fixed Rubin port, uniformly in its finite pinning regulator,
C<=1/k_0 and V_g<=hbar/(2sqrt(B_0 k_0)). These constants remain finite
in the local chain limit. All results below can first be retained as
uniform regulator statements; no infinite global Fock ground is assumed.

## 3. Convergent all-normal resolvent, with an actual tail bound

Take |eta|<=1/8 and Re(z-E_G)<=3E_R/4. On the jth excited block, j>=1,
define the positive diagonal operator

    A_j=H_g+E_R(d_j+s eta)^2-Re(z-E_G).

Then A_j>=H_g+E_R j^2. Equation(4) gives

    ||Y A_j^-1/2||^2<=2C+2V_g/(E_R j^2),
    ||A_j^-1/2 Y A_(j+1)^-1/2||<=gamma/(j+1),
    gamma=sqrt(2C/E_R+2V_g/E_R^2).

Set

    q=2|lambda|gamma, and choose fixed E_R such that q<=1/2.      (5)

The normalized offdiagonal block matrix has norm at most q by its scalar
row-sum majorant. For real z it gives

    H_ex,s-z >=(1-q) diag(A_j),
    ||(H_ex,s-z)^-1||<=1/[E_R(1-q)].                  (6)

For nonreal z, the remaining diagonal factors
I-i Im(z) A_j^-1 have inverses of norm at most1. Expanding around those
factors gives the same convergent Neumann WALK expansion and norm bound.
The expansion contains every excited charge level and every Gaussian mode.

Truncate the normal ladder after j=N, leaving the Gaussian system exact.
A walk from1 back to1 that notices the missing level N+1 has at least2N
offdiagonal steps. Sum norms of the missing walks using the positive scalar
Jacobi majorant. Therefore

    ||R_s,11(z)-R_s,11^(N)(z)||
                <=q^(2N)/[E_R(1-q)],                (7)
    |<phi,[Sigma_s-Sigma_s^(N)]psi>|
       <=lambda^2 q^(2N)/[E_R(1-q)] ||Yphi|| ||Ypsi||.

For real z below the excited block, the finite normal first-block inverses
also increase monotonically to the full one by the positive Schur formula.
Thus (7) is an explicit UV normal-resolution operation, rather than a
statement that a small normal population implies a small response error.
At fixed q<1, an error epsilon times the DISPLAYED lambda^2 Y^2/E_R
form scale needs N=O(log(1/epsilon)) excited levels. This is not a relative
error in an unknown vanishing infrared vertex. Evaluating the Gaussian
operator matrix elements is a separate task, not a free numerical oracle.
Individual walk products can be represented by positive-time Gaussian
semigroups and Y insertions; their Gaussian contractions use the actual
known spectral measure. The number of walks and required integration/
arithmetic accuracy must still be counted in any computational claim.

## 4. Higher charges renormalize the detuning RELATIVELY

For real z in this region, Sigma_s>=0 and

    0<=Sigma_s(z)<=[2lambda^2/E_R]Y^2,
    0<=partial_z Sigma_s(z)<=[4lambda^2/E_R^2]Y^2.     (8)

The inequalities are forms. The derivative contains the FULL excited
resolvent squared, not merely the square of its first diagonal block.

Also d^2<=4 diag(A_j)/E_R and (6) imply
||d(H_ex,s-z)^-1||<=4/E_R. The resolvent identity, retaining the actual
unbounded d in H_ex,+-H_ex,-=4E_R eta d, consequently gives

    ||R_+(z)-R_-(z)||<=32|eta|/E_R,
    |Sigma_x(z)|<=[16lambda^2|eta|/E_R]Y^2.           (9)

Here the final absolute form bound means both signed quadratic-form
inequalities. For eta>0, H_ex,+>=H_ex,-, so inverse order gives
Sigma_x<=0; the sign reverses for eta<0. Thus

    E_R|eta| I <=sign(eta)[E_R eta I-Sigma_x(z)]
           <=E_R|eta| I+[16lambda^2|eta|/E_R]Y^2.     (10)

There is NO eta-independent offsector remainder. On any specified state
with bounded Y^2, the transverse Schur coefficient has an explicitly small
relative correction at large but FIXED E_R. This is the useful completion
of the microscopic selection rule. It is not yet a renormalized transition
rate or a lower bound on a physical energy splitting.

In particular, reconstruction of a full eigenvector of energy E below
the excited threshold gives

    ||Psi||^2=<psi_P,[I+partial_E Sigma(E)]psi_P>.

The extra metric and the energy dependence in (3) must be retained when
turning Schur coefficients into response residues or energies. Treating
the coefficient in (10) as a free Pauli splitting would be incorrect.

## 5. The common correction is real physics, not a vanishing error

Even at eta=0 and finite E_R, Sigma_0 generally does NOT vanish. Its first
normal step is already the explicit operator

    Sigma^(1)(z)=lambda^2 Y[H_g+9E_R/4-(z-E_G)]^-1Y.  (11)

For z=E_G+E_R/4+e, its leading large-E_R term is
lambda^2 Y^2/(2E_R), an ordinary spring softening in (3). Higher walks
are bounded by (7), not discarded. For a Gaussian vector whose H_g
spectral support is at most E_c, Y creates at most one Gaussian quantum.
If the fixed Gaussian normal spectrum has maximum frequency omega_max,
then Ypsi has energy support at most E_c+hbar omega_max. This brackets
the first denominator in (11) between2E_R-e and
2E_R+E_c+hbar omega_max-e whenever the lower endpoint is positive.

Thus this softening can be bracketed from the actual host spectrum and
the normal tail, rather than fitted to a free spin model. It persists at
fixed E_R as temperature falls. Discarding a fixed microscopic correction
is especially dangerous when a cold bare-control prescription depends on
a logarithmically amplified response exponent. The resulting common bath
is generally energy-dependent and non-Gaussian, despite the exact linear
sector force that remains visible in (3).

## 6. Exact scope and the next infrared step

These are full-Hamiltonian low-energy resolvent statements, uniform in
the finite Gaussian lead regulator and with an actual infinite-ladder
error bound. They apply to ground/low-energy scattering channels. They
do NOT turn a many-body zero-temperature energy window into a thermal
spectral gap after the reservoir volume goes to infinity. At nonzero
temperature the total reservoir excitation energy is extensive; a fixed
global energy cutoff is not a finite-T trace approximation.

The finite-pulse response theorem remains valid at its own all-mode moment
scope. For the persistent cold heat law, the remaining step is to follow
the physical common bath and the vertex in (3)/(9), with its actual
low-frequency dressing and control calibration. The earlier literal-spin
Gaussian Coulomb formula cannot simply be inserted after (3). Conversely,
an absolute discarded-level error is no longer the only available tool:
(7)--(10) provide controlled all-normal and RELATIVE detuning information
at fixed E_R, force and geometry. No growing normal gap, free TLS,
imaginary-time oracle or unpriced material completion is being supplied.

## 7. Internal finite-matrix discriminator and settled boundary

check_fixed_normal_resolvent.py keeps a12-level Gaussian oscillator and
up to eight EXCITED normal levels, E_R=8,lambda=.4,eta=.02. Its q is
.412310563, below1/2. The complete retained Schur inverse matches the
actual full Hamiltonian's compressed inverse within4.8e-16. It verifies
the signs and quadratic-form upper bounds in(8)--(10). First-block normal
errors at cutoffs1,2,3 are6.36e-5,2.44e-8,3.21e-12, each below(7);
the complex-energy version also passes its stated tail bound. This is a
finite-cutoff/floating normalization check, not the infinite-bath proof
or a heat calculation.

At the authorised close of this investigation, the fixed-gap UV
elimination and relative detuning bounds are internally reconstructed;
the infinite-volume, finite-temperature infrared dressing/cold heat law
of THIS full canonical-memory Hamiltonian is OPEN. In particular no
two-level thermal ensemble, free Coulomb-gas vertex, prepared KMS/NESS
state or actual finite-aperture hardware has been supplied by this
resolvent construction. The proved finite-pulse operation and the earlier
literal-spin cold theorem retain their separate, exact scopes.
