# Why closing and repeating this cell cannot amplify it

30 October2026. Root whole composition. This is a scope/operation deduction,
not a new general query lower bound.

The exact positive two-query cell has all-U fidelity
55716029295809/123760695281664 at r=2. Root independently composed its
complete normalized logical Choi operator using the FIVE equality patterns
of three fresh junk labels, with no producer import. The result is in
PHYSICAL_CONTROLLER_INTAKE.json. The physical query-Pauli twirl has weights
(I,X,Z,Y) saved there, all nonnegative and summing exactly to one.

Its Bloch contraction coefficients in order X,Y,Z are exactly

    528551635039621/1980171124506624,
    528551635039621/1980171124506624,
    12584559055855/47146931535872.

All three are positive and their sum is

    24775855475393/30940173820416 <1.

Consequently the ENTIRE twirled logical cell is exactly the convex mixture

    (1-sum_i lambda_i) Replacement_(I/2)
           + sum_i lambda_i Dephase_(Pauli_i).

Each dephasing channel measures its known Pauli basis and prepares the
corresponding eigenstate. Replacement discards its input. This is an explicit
measure-and-prepare decomposition, hence the closed cell is entanglement
breaking. No imported fidelity-to-entanglement criterion is needed.

If only this decoded logical output is retained, every later operation on
it, fresh query ancillas and the fixed source is a CPTP map on the same side
of the reference cut. It cannot create entanglement with an inaccessible
reference from this separable state. Fresh source queries do not change
that fact. This is why this cell cannot simply be closed and iterated into
a high-fidelity inverse. It does not invalidate its exact adaptive-versus-
parallel minimax error gap; both facts hold simultaneously.

More generally, suppose an intermediate relational memory channel M_U from
the logical payload is EXACTLY one common channel M independent of U after
all physical carriers are discarded. Define F_opt(M) as its best Bell
fidelity under any known CPTP final decoder. Any further source-query
algorithm, for each fixed U, is some CPTP postprocessor R_U on M. Thus its
fidelity is at most F_opt(M) even if R_U was acquired by new queries. This
does not identify F_opt(M) with one numerical proposal or claim a certified
global optimum for C's rational decoder. It states the correct information
boundary: once the entire unknown-frame history has become an invariant
memory, additional queries cannot beat its optimal known extraction.

The live constructive task therefore keeps the physical/history carriers
and their coherent logical memory until a growing controller can extract
useful quantum information. The exact-heralding Schur obstruction separately
shows why insisting on an EXACT success branch cannot make that a
subquadratic-r route. Approximate coherent history remains open.

No source, quantum circuit or physical experiment was run. The calculation
uses the already qualified rational physical controller; the interpretation
does not promote a simulator into an operational device.
