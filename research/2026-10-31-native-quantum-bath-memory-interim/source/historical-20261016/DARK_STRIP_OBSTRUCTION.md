# Dark winding strips and the limit of syndrome-dephasing arguments

Independent adversarial note, 16 October 2026. **Result:** an exact, finite-
volume obstruction to making the code space the only slow space of the
completed two-outgoing-edge pair channel. It is **not** a no-go theorem for
long-time memory starting in the code space, nor a proof of coherent-error
robustness. The clean perturbative access-order bound below is only a
necessary condition on individual histories.

## Model and convention

Use the side-\(L\) periodic four-dimensional cubical complex, \(L\geq3\),
with qubits on faces. In the Z-error sector let \(S_e^X\) be the X-type edge
check. For \(i<j\), let \(f=(v;i,j)\) be the positive \((i,j)\)-face and
\(e_i=(v;i),e_j=(v;j)\) its two outgoing edges. Set

\[
P_{v;ij}=\frac{I-S_{e_i}^X}{2}\frac{I-S_{e_j}^X}{2},\qquad
Q_{v;ij}=Z_f.
\]

The active correction is \(\kappa\mathcal D[QP]\), with
\(\mathcal D[J](\rho)=J\rho J^\dagger-\{J^\dagger J,\rho\}/2\).
The completed clock uses
\(\kappa(\mathcal C_{v;ij}-\mathrm{id})\), where
\(\mathcal C(X)=QPXPQ^\dagger+(I-P)X(I-P)\). Include the dual X-error
sector with its Z-type cube checks and X-face corrections. This explicitly
anticommuting convention is the correctly typed one; the printed X/Z
notation in Pastawski--Clemente--Cirac's Appendix D is internally
inconsistent [1], while the later two-edge definition is explicit [2].

There is **no stochastic data noise** in the unperturbed statements below.

## Explicit dark syndrome and stationary operator algebra

Let \(f_x=((x,0,0,0);1,2)\), \(x\in\mathbb Z_L\), and define the Z Pauli
strip

\[
E=\prod_{x\in\mathbb Z_L}Z_{f_x}.
\]

Its X-edge syndrome is the mod-two cellular boundary of the face strip:

\[
s(E)=\{((x,0,0,0);1),((x,1,0,0);1):x\in\mathbb Z_L\}.
\]

It consists of two straight, parallel winding loops, each length \(L\).
At every occupied vertex, exactly one *outgoing* edge is occupied (and one
incoming edge). Consequently every primal pair predicate \(P_{v;ij}\)
vanishes on \(E\mathcal C\), where \(\mathcal C\) is the code subspace.
Because \(E\) is Z-type, it commutes with all Z-type cube checks, so all
dual-sector pair predicates vanish as well. All pair predicates also vanish
on \(\mathcal C\).

Set \(\mathcal D=E\mathcal C\). Since the X-edge syndrome is nonzero,
\(\mathcal D\perp\mathcal C\). For every pair predicate, \(P\) annihilates
\(\mathcal C\oplus\mathcal D\). Therefore, for **every** operator
\(X\in\mathcal B(\mathcal C\oplus\mathcal D)\),

\[
\mathcal D[QP](X)=0,\qquad \mathcal C(X)=X.
\]

The active and completed pair-only Lindbladians both fix the entire
operator algebra \(\mathcal B(\mathcal C\oplus\mathcal D)\). In particular,
dark-strip populations and code--dark coherences are stationary. At every
finite \(L\), the code is not the unique attractive stationary sector, and
the unperturbed generator cannot be inverted on the whole complement of the
code for an adiabatic-elimination or global code-recovery argument. This
does **not** say the spectral gap above the *full* fixed-point algebra is
zero. It also does not say a weak *local* Hamiltonian can efficiently reach
\(\mathcal D\) from \(\mathcal C\).

The displayed \(E\) has only \(L\) face factors and a known inverse \(E\).
Its dark state is not itself a logical error; final syndrome-aware recovery
could reverse it. Hence the obstruction targets **code-only attraction**
and a code-only inverse-generator argument. A theorem about preservation
of a larger recoverable sector is still possible and would need a separate
uniform certificate.

An unconditional measurement/dephasing of every stabilizer does not repair
the population obstruction. For a stabilizer \(S\), its dephasing channel is
\(\mathcal M_S(X)=(X+SXS)/2\); the continuous dephaser is
\(\mu\mathcal D[S]\). Any density operator supported on \(\mathcal D\)
has a definite syndrome, so \(\mathcal M_S(\rho_D)=\rho_D\) and
\(\mathcal D[S](\rho_D)=0\) for every \(S\). On the other hand, for a
code--dark matrix element \(X=|\psi_C\rangle\langle E\phi_C|\), any one of
the \(2L\) violated X-edge checks obeys \(SXS=-X\). That measurement kills
\(X\) exactly, and \(\mu\mathcal D[S]\) damps it at rate \(2\mu\).
Thus full stabilizer measurement separates syndrome blocks but still
leaves the non-code dark population fixed. Keeping the measurement record
does not itself supply a correction for that outcome.

## Geometry of any dark syndrome and local access order

The syndrome of a Z-face Pauli configuration is a mod-two 1-cycle, hence
has even degree at each vertex. Suppose a nonempty connected syndrome
component has fewer than \(L\) edges. Every simple cycle in it has length
less than \(L\), so it cannot have nonzero torus winding; the same follows
for every closed walk by cycle decomposition. It lifts
consistently to a finite connected graph in \(\mathbb Z^4\), with coordinate
range at most its edge count in each direction. Choose a lifted occupied
vertex minimizing the coordinate sum \(h(v)=v_1+\cdots+v_4\). It has no
incoming occupied edge, while its positive even degree is at least two.
Thus it has two outgoing occupied edges and activates a pair predicate,
a contradiction. Hence any nonempty dark syndrome has at least \(L\)
edges. This is a geometric *size* statement; it does not assert that each
dark component is homologically nontrivial. The explicit strip has \(2L\)
edges and is the boundary of a face chain.

For a legal pair correction, both checked outgoing edges of its face are
occupied. The face flip toggles exactly four boundary edges; its other two
edges may have occupancy 0, 1, or 2. Therefore its syndrome-length change
is respectively \(0,-2,-4\): a pair correction never increases syndrome
length. A Pauli term supported on at most \(q\) faces toggles at most
\(4q\) X-edge syndrome bits. Expand a bounded-support local Hamiltonian
into such Pauli terms. In any termwise Dyson/unravelled history beginning
at zero syndrome, after \(k\) local Hamiltonian insertions and any number
of active corrections, completed inactive clock events, or stabilizer
dephasings/measurements,

\[
|s|\leq 4qk.
\]

Reaching any nonempty dark syndrome needs \(k\geq\lceil L/(4q)\rceil\).
Reaching the displayed two-loop syndrome needs
\(k\geq\lceil L/(2q)\rceil\). The same statement applies separately to
each CSS sector. It counts *insertions in a Pauli-expanded history*; it is
not a uniform-in-\(L\) bound on the sum of histories, a transition rate,
or an all-time logical-error estimate. The extensive number of locations,
coherent interference, and long-time resummation remain open.

## What a Zeno route would still need

There is a concrete **formal second-order** positive mechanism if one adds
full stabilizer dephasing at rate \(\gamma\) per check. Let \(\mathcal P\)
dephase onto the joint stabilizer-syndrome blocks and let
\(\mathcal L_d=\gamma\sum_S\mathcal D[S]\). On an operator between two
syndrome blocks differing in \(m\) checks, \(\mathcal L_d\) acts as
\(-2\gamma m\). For the restricted Hamiltonian
\(H=\sum_f h_f Z_f\), each single-face term changes exactly four X-edge
checks, and distinct faces have distinct syndrome changes (\(L\geq3\)).
Consequently \(\mathcal P\mathcal L_H\mathcal P=0\), and the fixed-volume
second-order Schur-complement coefficient is exactly

\[
-\mathcal P\mathcal L_H
 (\mathcal L_d|_{\operatorname{ran}(I-\mathcal P)})^{-1}
 \mathcal L_H\mathcal P
=\sum_f \frac{h_f^2}{4\gamma}
 \mathcal P\bigl(\operatorname{Ad}_{Z_f}-\mathrm{id}\bigr)\mathcal P,
\qquad \mathcal L_H=-i[H,\cdot].
\]

The coefficient follows from the off-diagonal damping rate \(8\gamma\)
and \(\mathcal L_{h_fZ_f}^2=2h_f^2(\operatorname{Ad}_{Z_f}-\mathrm{id})\).
The completed pair generator preserves syndrome-diagonal operators, so it
appears in the leading slow dynamics alongside these effective fault
rates when \(\gamma\gg\kappa\). This formula is **not an exact identity
for finite \(\gamma\)** or a theorem for arbitrary local \(H\). Terms
with identical syndrome changes can interfere, syndrome-preserving local
terms contribute at first order, and higher-order remainders have not been
bounded uniformly in \(L\). Although \(\mathcal L_d\) has a uniform gap
to its *full* syndrome-diagonal algebra, \(\|H\|=O(L^4)\) under bounded
local strength, so an ordinary global-norm adiabatic-elimination theorem
does not yield the required volume-uniform control.

There is a genuine local one-clock estimate. For a pair projector \(P\),
\(R=I-P\), a state initially supported in \(R\), and isolated Hamiltonian
motion \(U_t=e^{-itH}\), the off-diagonal block obeys
\(\|PU_tR\|\leq t\|[P,H]\|\). If an independent rate-\(\kappa\) pair clock
rings after \(\tau\sim\mathrm{Exp}(\kappa)\), its chance to find the pair
active is at most

\[
\mathbb E\,\mathrm{tr}(P U_\tau\rho U_\tau^\dagger)
\leq 2\|[P,H]\|^2/\kappa^2.
\]

For a bounded-range, bounded-strength Hamiltonian with bounded local
coordination, \(\|[P,H]\|\) is independent of \(L\), since only terms
touching this 11-qubit predicate contribute. The premise is **isolated
motion from \(\ker P\)**. Other pair corrections may transport syndrome
into \(P\), and the state at successive clocks need not start in
\(\ker P\). Thus the estimate cannot simply be multiplied over clocks or
substituted for the classical fault-chain certificate. A positive route
would have to control those conditional histories, their interference,
the large stationary syndrome algebra, and their sum uniformly in volume
and for all times from a code input. Standard finite-system Zeno/adiabatic
elimination projects onto the *full* slow manifold [3,4], which here
contains the dark sector.

Known comparator only: a sign-calibrated, high-rate compensating reservoir
can algebraically cancel a known Hamiltonian drift and leave Pauli
dissipation [5]. That is active Hamiltonian cancellation, with its own
control and rate costs; it does not resolve passive suppression of an
unknown local Hamiltonian by the completed pair channels.

## Check and sources

`dark_strip_check.py` constructs these face chains and F2 boundaries for
\(L=3,4,5,7\) and every width \(1\leq w<L\). It checks \(wL\) faces,
exactly \(2L\) boundary edges, one outgoing syndrome direction at each
occupied vertex, and zero eligible pair predicates. It also exhausts the
four possible occupancy patterns of the other two face edges and confirms
pair-correction syndrome length is nonincreasing. This is a finite geometry
check of the construction, not a proof of coherent memory stability.

1. Pastawski, Clemente, Cirac, *Quantum memories based on engineered
   dissipation*, Appendix D, Eqs. (29), (33), (38):
   https://arxiv.org/pdf/1010.2901
2. Drechsler, Oreg, Aharonov, Definition 6.2 and discussion of the open
   asynchronous boundary: https://arxiv.org/html/2610.05589v1#S6
3. Zanardi and Campos Venuti, *Coherent Quantum Dynamics in Steady-State
   Manifolds of Strongly Dissipative Systems*:
   https://arxiv.org/html/1404.4673
4. Azouit, Sarlette, Rouchon, *Adiabatic elimination for open quantum
   systems with effective Lindblad master equations*:
   https://arxiv.org/html/1603.04630
5. Shang and França, local dissipative implementation / compensator
   identity: https://arxiv.org/html/2604.18533v2
