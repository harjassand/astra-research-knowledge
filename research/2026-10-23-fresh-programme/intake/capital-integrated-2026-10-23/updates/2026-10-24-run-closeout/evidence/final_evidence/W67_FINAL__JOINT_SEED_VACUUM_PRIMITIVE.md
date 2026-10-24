# A complete joint logical--seed channel with a vacuum-word target

W67, 24 October 2026. NEW strengthening of the reviewed common-row
receiver proof, in response to root's precise reuse question. Fresh
review pending. The generic polar/square-root recovery argument is
established prior; this file makes its retained-memory quantifier
explicit for the actual static-sector device. It does not claim a
paid-program reuse theorem, local-noise theorem or outer code.

## J1. Exact channel being compared

Fix ONE ideal good finite-block code program P and one actual theta in
its allowed band. The program and decoder do not depend on theta. Let
L be the logical register, S the physical two-dimensional bath seed,
and F the bath WORD register. Input F is the word vacuum. The input on
L,S and any external reference Z is OTHERWISE ARBITRARY: L may already
be entangled with S and Z. This is stronger than a product initial seed
assumption for a marginal logical channel.

The block appends its fixed terminal zeros, applies the actual ordered
physical interaction, and runs the fixed deterministic receiver. Retain
the physical S and F at output; trace only ordinary decoder work. Denote
this joint CPTP channel by

    M_(P,theta): L tensor S -> L_out tensor S tensor F.

The target to prove is ONE CPTP seed channel Phi_(P,theta), independent
of the logical state and reference, such that

    ||M_(P,theta) - id_L tensor
           [Phi_(P,theta)(.) tensor |vac><vac|_F]||_diamond
       <= epsilon_joint.                              (J1)

The diamond input here is L tensor S jointly. For each fixed actual
theta, the same Phi is used for EVERY joint input and every use of this
same finite block. Phi is allowed to depend on the fixed theta and P;
one theta-independent seed evolution is neither needed nor asserted.
Phi is a comparison channel, not an acquired operation to be applied.

## J2. Sector conservation and common row premises

Let R_seed have eigenstates |s>, s=+,-. The physical involution commutes
with R_seed tensor I_F: its prepend/pop maps are identity on the seed,
and its root action uses R_seed. Consequently every physical word is
controlled on s, and the decoder acts only on the received ports/work.
Seed-sector populations are conserved even for nonvacuum words.

Let K_(s,theta) be the vacuum-word amplitude on the PARENT code space,
and E_(s,a) its exact finite Fourier coefficients. Let V be the outer
logical frame, and write the common row on coefficient tensor logical
space as

    Frow(|i> tensor |psi>)=E_i V|psi>, A=Frow^*Frow,
    Gamma_ij=Tr_parent(E_i^* E_j)/D_parent.

The already reviewed full cross-KL event supplies

    Gamma>=0,
    ||A-Gamma tensor I_L||<=omega.                    (J2)

For each sector and actual theta, the exact coefficient vector c_s
has J=2T+1 unit-modulus entries in its sector block and zero elsewhere.
Its norm squared J is at most the padded row count R. The actual
vacuum amplitude on the code is Frow(c_s tensor I_L). Suppose the
PARENT mean final-word deficit is at most m<1 in each sector, so

    mu_s:=c_s^* Gamma c_s
      =Tr_parent(K_(s,theta)^*K_(s,theta))/D_parent
      in[1-m,1].                                    (J3)

For the new compound-band rows, m<=q; the old safe bound m<=2q is
also sufficient below. These are mean deficits before the outer frame,
not a presumed physical reset. Compressing(J2) by c_s gives the CODE
nonvacuum effect bound

    I-V^*K_(s,theta)^*K_(s,theta)V <=u I_L,
    u=m+R omega.                                    (J4)

Thus the entire physical bad-word isometry in each sector has norm
at most sqrt(u). This is an operator bound, including logical reference
entanglement, rather than a Bell-state or average fidelity statement.

## J3. Keep the receiver's whole isometry

Use the actual explicit receiver isometry D_rec before its ordinary
work-register discards. Include every helper/low-singular/TP-completion
flag in the environment register A_rec. The reviewed implementation
maps the retained left singular subspace to the right polar partner
with FULL subspace error xi. Its action elsewhere is its fixed unitary
completion, not a successful branch selected after measurement.

If Frow=Rpol sqrt(A), then Rpol^*Frow=sqrt(A). The positive square-root
operator inequality and(J2) give

    ||sqrt(A)-sqrt(Gamma) tensor I_L||<=sqrt(omega).

Set e_s=sqrt(Gamma)c_s, embedded in A_rec with the known ideal recovery
flags. The exact polar comparison costs at most sqrt(R omega). For
right singular values below sqrt(nu), both the actual receiver image
and the polar target applied to Frow(c_s tensor I) have norm at most
sqrt(R nu). The full unitary cutoff therefore costs at most2sqrt(Rnu).
The high-part full-isometry approximation costs xi, since K_s V is a
contraction. Hence, exactly as in the reviewed F10--F12 argument,

    ||D_rec K_(s,theta)V - I_L tensor e_s||
       <=e_good:=sqrt(R omega)+2sqrt(R nu)+xi.       (J5)

No entry or eigenvector of Gamma is queried. The vector e_s is only
a proof object. Importantly, it is the SAME vector for every logical
state, including states entangled with the physical seed.

## J4. One normalized CPTP seed map for all joint inputs

By(J3), ||e_s||=sqrt(mu_s)>0. Normalize each SECTOR vector separately:

    f_s=e_s/sqrt(mu_s), ||f_s||=1,
    ||e_s-f_s||=1-sqrt(mu_s)<=m.                    (J6)

These scalars depend on theta and P, not on the input seed populations
or the logical state. A normalization chosen separately for each
input density would not define the required single channel; J6 avoids
that problem.

The following isometry is defined on ALL L tensor S inputs:

    T_(P,theta)|psi,s>
       =|psi>_L tensor |s>_S tensor |f_s>_Arec
                                      tensor |vac>_F. (J7)

Its isometry property follows from the orthogonal retained seed labels,
even when f_+ and f_- overlap. Tracing A_rec produces id_L tensor Phi
with final word vacuum, where

    Phi(|s><t|)=<f_t|f_s>|s><t|.                    (J8)

The coefficient matrix is a Gram matrix with unit diagonal. Thus Phi
is a completely positive trace-preserving Schur channel. It may change
seed phases/coherences; seed identity preservation is not asserted.

Retain all physical seed labels in the ACTUAL Stinespring isometry too.
Because different s outputs remain orthogonal, the norm of a controlled
error is the MAXIMUM of its sector errors, not a seed/logical dimension
factor. Restoring the complete bad-word part costs sqrt(u) in isometry
norm by(J4). Combining(J5),(J6) gives the operator bound

    ||V_actual-T_(P,theta)|| <=e_good+sqrt(u)+m.      (J9)

Tensoring an arbitrary reference does not change this operator norm.
The elementary isometry-to-channel inequality therefore proves(J1) with

    epsilon_joint<=2[e_good+sqrt(u)+m]
                  <=4[e_good+sqrt(u)].             (J10)

The last relaxation uses m<=sqrt(u). It is exactly the conservative
receiver bound ALREADY paid in the finite ledger. Thus the strong joint
logical--seed/vacuum target needs no additional rate, precision or
logical-dimension loss.

## J5. Native comparison, uniform band and actual quantifiers

The native sender and digital receiver are compared to one consistent
exact completion at the full-unitary level, with the two squared-
signal tolerance steps of d814. These telescopes remain valid while
retaining S,F and any reference, since physical intervening unitaries
have norm1 and later local CPTP conversions contract trace norm.
No inverse of CPTP physical-port legalization is used. Their aggregate
joint-channel error is the SAME charged native envelope as before.

For the selected compound policy, omega=128R sqrt(q),
nu=z^2/(2^16R), xi=z/128 and u<=2q+Romega. The established scalar guards
give the ideal joint bound<=3z/32. The full native envelope is at most
z/4+z/2048, hence the VACUUM-START block joint bound is at most

    705z/2048 < z.                                 (J11)

The separately paid initial-prefix term z/32 is not included in this
vacuum-start primitive. It cannot be reinserted as a free fresh bath
assumption after a block. A single common program event makes J2--J4
uniform across the allowed parameter band. The same decoder is used;
Phi_(P,theta) varies with the fixed unknown physical theta as allowed
in J1. All arbitrary joint logical--seed--reference states are covered.

The seed may have been disturbed by previous known inputs, root phases,
receiver records, or correlations with future message registers. That
is permitted here. Only the WORD-vacuum input embedding is a premise.
No actual word measurement, bath control or seed preparation is called.

## J6. What this does not prove about reuse or outer coding

J1 is a composable approximate RESET TARGET, not an exact physical
reset on every branch. On the rare error component the actual word
can be nonvacuum and can carry correlations. The block map on such
inputs is not bounded by J1. Therefore a local-stochastic fault law,
forgetfulness, independent block errors or a standard outer-code
threshold theorem does NOT follow from this primitive alone.

For example, consider a different abstract memory channel with a
classical memory flag F. At F=0 it applies logical identity and stays0
with probability1-p, or applies X and sets F=1 with probabilityp.
At F=1 it applies X forever and keeps1. The isolated vacuum-start joint
channel is within EXACTLY2p of id tensor |0><0|, even on references.
Nevertheless r consecutive logical faults starting at the first block
have probabilityp, not p^r. This example is not asserted to be the
actual recurrent device; it falsifies that generic implication.

A legitimate telescoping bound from the vacuum start is B times the
one-block joint error, using an ideal-past/actual-future hybrid so each
single replacement has vacuum input. That bound alone is not a paid
installation/amortization result and is not presented as one. The
remaining task is an explicit resource and memory/noise argument that
supports the intended outer/bootstrap protocol under this actual
device, without fresh-normal product assumptions or message copies.

No new physical operation, seed acquisition, outer code, paid program
transport or practical gain was performed. The source/finite compound
rows and this stronger memory statement await separate criticism.
Priority UNKNOWN; practical advantage NOT_ESTABLISHED; physical
NOT_PERFORMED; mission NOT_ACHIEVED.
