# An exact three-carrier permutation-memory receiver

30 October 2026. C construction. Native fresh memoryless flat encoding;
no inverse, source environment, microscopic label or controlled source.
This supplies an exact all-order dynamics/readout interface for specified
controllers. It does not assert a high-fidelity scalable inverse.

## 1. State representation, including correlations

Let N_U(X)=U(X tensor I_r/r)U*, U:C^k tensor C^r -> C^D, D>=kr.
Three live physical carriers have logical factors L0,L1,L2 and junk
J0,J1,J2 in the common unknown input frame. E is known retained memory;
an arbitrary inaccessible reference can be included as a spectator.
Use the convention

    P_g |x0,...,x(n-1)> = |x_(g^-1(0)),...,x_(g^-1(n-1))>,
    P_g P_h=P_(g h).

Starting with fresh independent junk and using only known physical
permutations controlled by known memory, the EXACT live state has form

    rho = r^-3 sum_(pi in S3) X_pi tensor P_pi^J.          (1)

X_pi acts on (L0,L1,L2,E), and can be nonpositive/non-Hermitian. The
convenient Hermitian coefficient choice is X_(pi^-1)=X_pi*. No independence
between junk and logical/reference memory is imposed by (1). It contains
precisely the permutation-valued correlations omitted by a marginal-only
description. At r>=3 the six permutation matrices are linearly independent;
at r=1,2 the same formula remains valid with its physical representation
quotient. We retain formal coefficients instead of treating null relations
as an extra source resource.

The trace is

    Tr rho = sum_pi r^[cycles(pi)-3] Tr X_pi.              (2)

Individual X_pi are not density matrices and their traces are not classical
path probabilities. Positivity always means positivity of the physical
operator in (1), obtained by the literal circuit below.

## 2. One new native call, arbitrary controlled-permutation stages

Append the fourth fresh junk I_r/r. A known memory/source-input circuit,
with any paid permutation-control stages on the four physical wires,
has an input-frame branch expansion

    W_z =sum_(g in S4) P_g^L tensor P_g^J V_(z,g),       (3)

where V_(z,g):E -> L3 tensor E' is a known linear map. z labels a discarded
known controller environment; sum_z W_z* W_z=I is required at the ACTUAL
physical circuit level. This normalization is not inferred from arbitrary
coefficient choices. Pure isometries have one z. Pre-query controls alone
give g fixing wire3. Post-query known permutations may use full S4.

To justify (3), expand each known controlled physical permutation in its
memory label basis. All whole-register permutations commute with the same
U on each occupied carrier. Memory/source-input maps before the query and
memory maps after it combine into the displayed V. The new source call is
always an ordinary forward logical-input N_U. A controlled unknown channel
is never introduced by this algebraic expansion.

For PRE-query stages, where every g fixes the new wire3, a sufficient
normalization that works at every physical dimension is the group-algebra
identity

    sum_(z,g) V_(z,g)* V_(z,g h)=delta_(h,e) I
                                                        (4)

for every h in that S3 subgroup. Here the old physical permutations
commute with maps appending the new logical input. For a general combined
S4 expansion, V_g includes the new logical-input preparation and cannot
be commuted through arbitrary permutations of that same new wire. In
that case use the ACTUAL staged circuit normalization, not (4) without
its premise. Known controlled permutations and their unitary compositions
already have native isometry identities. The recurrence accepts actual
circuits, not arbitrary normalized-looking coefficient tables.

## 3. Exact S4 to S3 trace and logical coefficient update

Choose an old programme d in {1,2} to discard. The target wire0 is not the
named discarded wire. A known permutation may of course have moved logical
information before the discard, and the update tracks that fact.
Let s=(s0,s1,s2) be the declared order of surviving physical wires; by
default it is the increasing order of {0,1,2,3}\{d}. Define del_d(kappa)
by deleting d from its cycle and then relabeling survivors in that order.
For example, when d is not fixed, its predecessor is connected directly
to its successor. Then

    Tr_Jd P_kappa = r P_(del_d kappa),  kappa(d)=d,
                   P_(del_d kappa),    kappa(d)!=d.       (5)

For pi in S3 let tilde_pi fix wire3, and for each branch pair put

    kappa=g tilde_pi h^-1,
    sigma=del_d(kappa),
    e(kappa,d)=0 if kappa fixes d, and -1 otherwise.

The exact next coefficients, normalized again as r^-3 in (1), are

    Y_sigma =sum_(z,pi,g,h : del_d kappa=sigma)
      r^e Tr_Ld[ P_g V_(z,g) X_pi V_(z,h)* P_h* ].        (6)

The new logical output order is the SAME declared survivor order s, then
E'. The discarded known environment z is summed, with NO cross terms
between different z. Formula (6) includes complex controls and arbitrary
operator-valued reference correlations. It is an equality of physical
channels, not a Kraus model for unknown junk flags.

The rank factor is only 1 or 1/r in a single step. This does not mean
that all modes suffer 1/r per round. A nontrivial permutation fixing the
discarded wire survives without attenuation. The scalar closure in the
two-carrier disposal theorem cannot be transplanted to (6).

## 4. A four-to-one insertion table, not an exponentially growing history

Every sigma in S3 has exactly FOUR predecessors kappa in S4 under del_d.
One is its embedding fixing d and has coefficient1. The other three are

    kappa=iota(sigma) (x d),  x a survivor,

which insert d after x in a cycle and have coefficient1/r. Thus the
normalized partial trace E_d=(1/r)Tr_d is the unital CP conditional
expectation from the four-carrier operator algebra to the survivors.
It has the bimodule property

    E_d(P_a Z P_b)=P_a E_d(Z) P_b

for permutations a,b of survivors. This is ordinary permutation/partial-
trace structure, not a new trace principle.

For fixed known memory dimension M and k, (6) is a finite linear transfer
on six operator coefficients of size k^3 M:

    X_next = [T0+(1/r)T1] X.                            (7)

Here T0,T1 are determined by the supplied known control maps. For controls
independent of rank they are literally rank-independent transfer matrices;
if control parameters themselves depend on r, retain or substitute that
additional explicit known dependence rather than calling the whole map
affine in rank without qualification.

Each specified fixed controller can therefore be iterated at ALL orders,
or studied by its finite transfer operator, rather than optimized only at
Q=3. Real rational controls give exact rational arithmetic. Bit cost still
grows with the number of iterations and input bit lengths; exact huge-time
prediction does not become free through repeated squaring. If all known
reference history is retained, M itself grows and its full coefficient
matrices can be exponential. No small-M closure is then asserted.

There is an important sharper cut for PRE-query S3 controls. Every g,h
and tilde_pi fixes newborn wire3. After tracing old d, the newborn junk
is still an independent I/r. At the immediate post-cell cut only TWO
permutation coefficients can remain: identity and the SWAP of the two
surviving OLD carriers. The full S3 span is still needed during the next
control stage. Post-query S4 stages can populate all six at the cut.
This is an exact factorization consequence, not a reset of an old carrier.

## 5. Positivity can be checked in three finite blocks

For S3 the irreducible junk representations are trivial, standard and
sign, of dimensions 1,2,1. Let D_lambda(pi) denote their matrices. The
physical junk Schur blocks of (1) are

    B_lambda=sum_pi X_pi tensor D_lambda(pi),

repeated with multiplicities

    m_triv =r(r+1)(r+2)/6,
    m_std  =r(r^2-1)/3,
    m_sign =r(r-1)(r-2)/6.                              (8)

These formulas follow directly by taking the inner product of the S3
characters with Tr P_pi=r^cycles(pi). They sum with irrep dimensions to
r^3. Only irreps with nonzero multiplicity are required at r=1,2.

A rational basis for the standard representation is e0-e2,e1-e2, with
metric H=[[2,1],[1,2]]. In that basis ordinary Hermitian positivity means

    (I tensor H) B_std >=0,

and B_triv,B_sign>=0 for their present blocks. This is metric-congruent
operator positivity, not entrywise positivity of X_pi. Actual CPTP
circuits preserve it automatically. A numerical finite-block positivity
test is not substituted for a native normalization proof.

## 6. A finite native final readout, with no exponential decoder oracle

There is a literal known circuit extracting all the needed relational
moments of the THREE retained physical carriers. Prepare a uniform group
register G over S3; controlled-permute the physical carriers by g, invert
the group label, and discard the physical carriers. It uses a six-state
known register (three qubits with off-support completion), O(log D)
known controlled whole-register swaps and no extra source calls.

For pi in S3, define the operator on E and any spectator reference

    M_pi =sum_sigma r^[cycles(sigma pi)-3]
                      Tr_(L0,L1,L2)[X_sigma P_pi^L].     (9)

The actual normalized positive output is

    Omega_(E,G)=(1/6)sum_pi M_pi tensor L(pi^-1),         (10)

where L is the left regular representation on six labels. Its group
entry (g,h) is M_(h g^-1)/6. The inverse and ordering in (9)-(10)
matter: there is no hidden conjugation or replacement of sigma pi by a
non-equivalent logical action. Tr Omega=Tr M_e=1 by (2).

For fixed M, a proposed final CPTP map E tensor G -> logical space is a
known finite 6M-dimensional receiver. It still needs to be supplied,
qualified and synthesized; its existence/performance is not granted.
Padding the unused group labels gets an explicit reset branch. The
interface removes an unbounded final-history oracle, but does not
assert that the finite receiver achieves near-perfect recovery.

When the initial payload and all auxiliary preparations have the stated
native source form, the X coefficients are known linear functions of the
logical input, independent of U. Consequently (9)-(10), followed by a
fixed known decoder, give ONE common logical channel for every U, not
only equal Haar-average fidelities. The physical frame cancels in this
particular readout because every physical carrier is discarded after
known permutations. This says nothing about an arbitrary alternative
final decoder that retains physical outputs.

## 7. A useful surviving mode and an exact failure of marginal-only closure

Keep physical carriers0,1 persistent and discard/replace the spectator
programme2. Prepare a known flag C in |+>. Perform a known controlled
SWAP_(0,1), make the fresh source query on a fixed known input, and discard
programme2. Repeat the SAME controlled SWAP in the next cell, again
replacing only carrier2. All source queries are ordinary forward calls.

The nontrivial junk coefficient P_(01) is created in the off-diagonal
flag blocks after the first cell. It fixes the discarded wire2, so (5)
passes it with coefficient1. The second controlled SWAP multiplies it
back to identity with coefficient1. The final flag is EXACTLY |+>, and
both persistent physical carrier states are restored, for every r and
every input/reference. This is a known reversible echo, not an inverse
of the unknown encoding or a high-fidelity decoder.

The control flag is never measured, so the same controlled-unitary
identity returns an arbitrary flag state and its entanglement as well.
The |+> input makes the visibility explicit; the exact matrix-unit
consumer keeps its four separate flag blocks and therefore checks their
individual transformations. Doing nothing would restore the same data
with no calls, so this echo is only a discriminating history-memory
control, not a claimed resource advantage or a decoder.

At every intermediate stage the junk MARGINAL is nevertheless I/r^3:
the nontrivial junk mode is correlated with an off-diagonal flag whose
trace is zero. Replacing it by an independent I/r^3 while preserving the
exact logical/known-memory marginal changes the operation. Such a reset
maps coefficients to

    X'_e=sum_sigma r^[cycles(sigma)-3] X_sigma,
    X'_(sigma!=e)=0.                                   (11)

With (11) inserted between the two cells, the final flag coherence is
1/r^2 instead of1. The full exact algebraic consumer checks this for
EVERY target/programme logical matrix unit, as a polynomial in q=1/r,
not by testing selected ranks or a model trajectory. It proves that even
a correct maximally mixed junk marginal cannot justify the scalar reset.

## 8. Consequence and remaining gate

The exact receiver consists of the all-order transfer (6), its finite
positivity interpretation (8), and the native finite readout (9)-(10).
For a fixed known-memory recurrent controller, it is a constructive
classical prediction/design interface independent of the unknown ambient
frame, with physical source/control costs explicit. It preserves an
actual interference mode excluded by spent-carrier disposal.

The echo does not show useful logical information extraction: it returns
the same encoded carriers and a known flag. Neither r-independent mode
transport nor a constant number of coefficient blocks proves linear-r
decoding. A controller must convert these retained physical correlations
to the finite known output while protecting the unknown logical qubit.
That is root's central operational construction; the current interface
does not silently supply it. General approximate near-linear-r inversion
remains OPEN. No source, quantum circuit, physical experiment, optimizer,
Q=3 fidelity fit or new source-model case is needed for this algebra.
