# Variance-refined comparison for a received dephasing channel

Status: root geometric lemma, independently rederived by constructor; formal
source-bound review pending. This is ordinary Hilbert-space Cauchy--Schwarz,
not a new cancellation principle or a claim of historical novelty.

Let O be a contraction on a common Hilbert space, psi and psi0 unit vectors,
and a=|<psi0,psi>|. Choose psi's irrelevant global phase so this overlap is a>=0.
Put delta=1-a^2 and f=<psi,O psi>, f0=<psi0,O psi0>, r=|f0|. Then

  |f-f0| <= delta(1+r)
               +2 sqrt(delta(1-delta)) sqrt(1-r^2).             (1)

When r>0 and zeta=f0/r, a phase-aligned identity comparison satisfies

  |1-conj(zeta) f|
     <= (1-r)+delta(1+r)
                +2 sqrt(delta(1-delta)) sqrt(1-r^2)
     <= [sqrt(1-r)+sqrt(delta(1+r))]^2.                         (2)

Without any physical phase correction, a certificate R>=|1-f0| gives

  |1-f| <= R+2delta+2sqrt(2delta R),                           (3)

also capped at2. A phase correction in (2) is not free: its calibrated control
and exposure need to be part of the actual consumer if that version is used.
Equation (3) needs no phase correction and retains deterministic phase error.

Proof. For delta>0 write psi=a psi0+sqrt(delta)chi with chi perpendicular to
psi0. Since ||O||<=1, both ||(I-|psi0><psi0|)O psi0|| and the same expression
with O* are at most sqrt(1-r^2). Each cross matrix element is bounded by this
number. The diagonal chi expectation has modulus at most1. Expand the quadratic
form to obtain (1). After rotating by conj(zeta), the reference diagonal term
is the real number r; triangle inequality gives the first bound in (2), and
sqrt(1-delta)<=1 gives its square form. Finally 1-r<=|1-f0|<=R and1+r<=2 imply
1-r^2<=2R; apply (1) and triangle inequality to get (3). Endpoint delta=0 or1
follows directly. A contraction suffices; unitarity is not required.

## Complete-channel meaning and actual cost

For a qubit dephasing channel preserving diagonal entries and multiplying the
off-diagonal entry by f, the diamond distance to identity equals |1-f|, with
the convention that diamond distance has no extra factor1/2. The factor can
be proved by writing the difference as a phase rotation of (Id-Z(.)Z)/2 times
|1-f|; the input |+> attains the bound. Thus (3) is a complete quantum-data
channel bound, including arbitrary reference entanglement, not merely one
state's fidelity or an unproved conversion of emitted power to logical error.

In the proposed passive coherent receiver, O must actually be derived from
the two data-conditioned source/field/receiver evolutions on a COMMON input
space. Retaining cavity memory and all loss outputs gives the relative unitary;
compressing a fixed common receiver initialization gives a contraction. The
actual pure source/entire-field overlap a (or a valid purification comparison)
must be earned. A small photon count alone does not set delta without that
argument. Do not compare two unrelated purifications or discard residual
apparatus correlations before constructing O.

If R=O(b^2/kappa_c) for the received finite-cavity reference and
delta=O((b^2+b^4T)/lambda) for an actually bounded source/reference overlap,
(3) charges R+delta+sqrt(R delta), rather than the generic sqrt(delta)
Stinespring comparison. This is a conditional scaling consequence, not a
physical feasibility claim. Exact constants, source switching, all operation
and readout exposure, routing loss, finite dispersive validity, calibration,
and an actual final release/continuing-apparatus consumer remain to be paid.
