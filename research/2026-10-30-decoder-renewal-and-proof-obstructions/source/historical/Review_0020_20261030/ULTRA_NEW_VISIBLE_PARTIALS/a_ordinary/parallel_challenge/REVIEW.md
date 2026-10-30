# Independent whole challenge of the two-parallel-query boundary

30 October 2026. Disposition: ACCEPTED at the stated exact flat k=2,r=2,D=4,
deterministic complete-payload, two-parallel-query scope. This is an
independent reconstruction of the model and its rational dual, not an
acceptance based on solver status. The adaptive lower bound has its separate
C-owned CPTP construction; this review does not rerun that producer or its
decoder optimization. No asymptotic query theorem, physical experiment or
historical-priority claim is accepted here.

## 1. The payload-present covariance issue

Let Q=2. The complete parallel receiver is a positive comb W, with its input
wire B0 the ALREADY encoded payload, its output A0 the decoded logical qubit,
and its open query wires A1,A2 -> B1,B2. The ordinary deterministic parallel
comb equations are

    Tr_A0 W=I_B1B2 tensor W_pre,
    Tr_A1A2 W_pre=I_B0.                                   (R1)

They permit every known CPTP preprocessing of B0 into the query inputs and
retained quantum memory, arbitrary entanglement of both query inputs and that
memory, and every known CPTP postprocessing. Initial known ancillas and
randomness cannot depend on U without a charged source acquisition. No
assumption that B0 is absent, ignored, measured or repreparable is made.

The performance operator is invariant under simultaneous physical U(D)
conjugation on all B wires. Twirl the WHOLE W by that representation. Positivity
and (R1) are preserved, as is its Haar-average objective. The left side after
Tr_A0 remains invariant. Since the right side already has I_B1B2, invariance
reduces to

    (I_A1A2 tensor V_B0) W_pre
       (I_A1A2 tensor V_B0^*)=W_pre   for EVERY V in U(D).

The defining representation on B0 is irreducible, so its operator commutant
on A1A2 tensor B0 is End(A1A2) tensor I_B0. Consequently

    W_pre=rho_A1A2 tensor I_B0, rho>=0, Tr rho=1.           (R2)

There is NO factor1/D in (R2): W_pre is an unnormalized channel Choi
operator, and its partial trace is I_B0. In particular Tr W=D^3. The
factorization constrains the query-input MARGINAL, not the entire receiver
or its quantum-memory correlations. The full W still includes every
payload/query correlation permitted by (R1). Thus (R2) is not an iid-programme
or known-probe simplification, and it remains valid with a present payload.

An average upper bound on this class suffices for the claimed worst-source
comparison. It does not require physically implementing an ideal Haar twirl.
For every original receiver its twirl has identical average fidelity, so
restricting to that invariant model loses no optimal average value.

## 2. Normalization, transpose and native moments

Use J_N=sum_ij |i><j| tensor N(|i><j|), with Tr_B J_N=I_A.
At Q=0 the entanglement fidelity is

    Fe(R N)=k^-2 sum_(i,j,b,c)
       [N(|i><j|)]_(b,c) [R(|b><c|)]_(i,j).

If W is the Choi matrix of the receiver in (A0,B0) order, this is exactly
Tr(W J_N^T)/k^2, where the transpose is on ALL displayed indices. Linking
each further channel slot to its matching query wires supplies the same full
transpose per queried J_N. The resulting operator is therefore

    Omega=k^-2 E_U[(J_N^tensor3)^T].                       (R3)

Only the single Bell target contributes k^-2. Dividing additionally by k per
query would incorrectly convert physical channel slots to normalized Choi
programmes. As a normalization check, at zero queries E J_N=I_A tensor I_B/D,
so every deterministic decoder has Fe=1/k^2, as it must with no source frame.

For the public input embedding, write J0=Phi_un,k tensor I_r/r. If P_t moves
tensor position j to t(j), tracing its physical action gives

    Tr_B[(P_t^*) J0^tensor3]
       =r^[c(t)-3] P_t^A.                                (R4)

This follows by closing each junk cycle and by the EPR transpose identity;
the inverse in P_t^* is important. Let G_(t,s)=D^[c(t^-1 s)]. At D=4 this
six-by-six Gram is invertible. Orthogonal projection onto the physical
commutant yields the coefficients

    Omega=sum_(s,t) (G^-1)_(t,s) r^[c(s)-3]/k^2
                        P_s^A tensor P_t^B.              (R5)

Simultaneous inversion (s,t)->(s^-1,t^-1) leaves the coefficients unchanged,
so the full transpose in (R3) leaves this real operator unchanged. Contracting
with an arbitrary permutation basis operator cancels the physical Gram:

    Tr[(P_a^A tensor P_b^B)Omega]
       =k^[c(a b^-1)] r^[c(b)-3]/k^2.                    (R6)

I reconstructed (R3)--(R6) analytically. The independent consumer also checks
ALL36 moments (R6) by direct sparse native Choi index enumeration, without
using the producer's moment formula or its permutation implementation. This
finite exact check confirms the admitted Q2 coefficient conventions; it is
not the reason the general contraction identity holds.

## 3. Completeness of the six positivity blocks

Logical right-frame invariance permits twirling all A wires by the same
U(k) representation as well. The input-frame transpose only replaces this
group by its complex conjugate/inverse, whose commutant is the same. Both
twirls preserve (R1) and the objective. Schur--Weyl duality then makes the
entire averaged operator a sum of P_s^A tensor P_t^B; no fixed spin or
logical multiplicity vector has been selected.

For (C^2)^tensor3 the nonzero S3 irreps are trivial and standard; the sign
sector is the zero third exterior power. For (C^4)^tensor3 all three irreps
occur. Operator positivity is consequently equivalent to positivity in
exactly the six logical/physical irrep pairs in the certificate. The omitted
logical sign block is null, not an untested negative block. All representation
multiplicity spaces carry identities after the independent unitary twirls.

In the standard basis (e0-e2,e1-e2), the metric is H=[[2,1],[1,2]]. Its
permutation matrices obey R(p)^T H R(p)=H. A self-adjoint operator block M in
this basis is positive iff H M is an ordinary symmetric positive matrix.
For two standard factors the metric is H tensor H. Thus the producer's
metric-multiplied rational block, rather than an incorrectly Euclidean-
interpreted nonorthogonal matrix, is the right positivity object.

Inverse-paired real coefficient symmetrization makes the saved Y Hermitian.
There is no restriction from ignoring complex optimal coefficients: the
objective and all constraints are real, so (W+conj(W))/2 preserves positivity,
causality and value. The certificate itself is real and is a valid complex
operator inequality regardless of that observation.

## 4. Weak duality is sufficient and globally normalized

Let Y act on A1,A2,B0,B1,B2 and obey

    I_A0 tensor Y-Omega>=0,
    Z=Tr_B0B1B2 Y<=lambda I_A1A2.                         (R7)

For every positive complete parallel comb, (R2) gives

    Tr(W Omega)
      <=Tr[W(I_A0 tensor Y)]
      =Tr[(rho_A1A2 tensor I_B0B1B2)Y]
      =Tr(rho Z)<=lambda.                                (R8)

This uses only weak duality. No numerical optimum, exact primal point,
strong-duality assumption or Slater bound is needed. Y need not itself be
positive; its slack in (R7) is positive. The two input symmetry eigenvalues
are exactly sum_t D^[c(t)](y_I,t +/- y_SWAP,t), because Tr P_t=D^[c(t)].
The saved bound is

    lambda=29751457437/68719476736.

The independent stdlib/Fraction consumer reconstructs G^-1, every irrep
matrix/product/metric, every entry of all six slack blocks, their exact
positive LDL pivots, the Hermitian inverse-pairing and both input-sector
values. Both latter values equal lambda. It imports NO producer code and
calls NO solver. Its recorded execution is EXACT_CONSUMPTION.json.

## 5. Operational consequence and exact limits

C's separate coherent-feedback proof supplies the lower fidelity

    f=55716029295809/123760695281664,
    f-lambda=71638340317230378547/4152719834101315534848>0.

I read its mathematical physical-query controller and its Pauli-intervention
argument. Each physical operation is a permutation on full carriers and
their physical registers are eventually discarded, so its entire logical
composite, not just its Bell fidelity, is independent of U. Preapplying the
same public Pauli to EACH fresh query and the matching decoded post-Pauli
then realizes an ordinary Pauli twirl without acting on the unknown payload
code. The internally averaged channel has half-diamond error exactly1-f.
This is the needed operation beyond a generic fidelity-to-diamond claim.
Its precise feasible lower value still rests on its separately qualified
rational CPTP decoder; this consumer does not rerun that qualification.

Conversely, for ANY parallel receiver, half-diamond error on a particular
source is at least1-Fe on the logical Bell input. Its average Fe is at most
lambda, so some source has complete half-diamond error at least1-lambda.
Hence the two exact inequalities establish a strict minimax gap at full
throughput IF the separate adaptive CPTP construction is admitted. A seed-
conditioned public channel would not have the same twirling guarantee; the
known random seed here is internal and discarded. Source latency and memory
remain charged to the adaptive protocol.

The D=4 upper also obstructs a uniformly better parallel controller for
every D>=4: restrict its sources to a fixed PUBLIC4-dimensional output
subspace, and simulate its larger known registers using the arbitrary
ancillas already allowed at D=4. This is a subfamily argument, not a new
ambient-dimensional certificate or a restriction on unknown source support.

No generic r^2 physical-query lower, linear-r upper, useful high-fidelity
inverse or per-query asymptotic advantage follows. One online adaptive call
is an important timing resource and cannot be made offline by renaming its
unknown correlated logical input as a known calibration probe.

## 6. Strongest ordinary comparison and what was not found

The pure qubit adaptive gap is already established by Quintino--Ebler
2109.08202v3 and the isometry conversion2401.10137v3. General mixed-channel
discrimination already has strict sequential/parallel gaps, notably
Bavaresco--Murao--Quintino2011.08300. The new primary2609.40218v2 also gives
two-query separation of bare versus averaged-purification resources and
sequential discrimination consequences. Their classical decision outputs or
extra environment access do not constitute the present arbitrary-payload
inverse. None of those abstract consequences makes quantum adaptivity new.

The RDS and Uhlmann/Petz constructions are granted as complete forward-only
ordinary inverses with their actual programme costs, as in the two existing
A governing files. Virtual comb inverses output signed expectation estimates,
not a retained arbitrary quantum payload. The attractive title1308.3254,
"Optimal processing of reversible quantum channels", explicitly concerns
unitary group-representation transformations; its claimed parallelization
must not be transferred to this mixed encoding/inversion anti-homomorphism.

The targeted primary search did NOT acquire a stronger same-input TWO-query
mixed adaptive decoder which absorbs this particular exact gap. That is a
bounded search result, not an absence/novelty proof. Historical priority
remains UNKNOWN. The earned result is the explicit mixed-source operation
and its complete exact parallel comparison, not the general fact that
adaptivity can help.

## 7. Acquisition and independence

I whole-read root ROOT_MECHANISM.md and parallel_dual_certificate.py, the
saved rational certificate, and C's coherent-feedback/comparison/prior
proofs. I analytically reconstructed the comb, frame reduction, link
transposes, moment contraction, full commutant, metric positivity and weak
duality before running the separate consumer. The source primary ports
were reused at their previously read scope; selected new primary statements
were read directly. No fresh model, Haar sample, source, optimizer, quantum
or physical experiment was run. Consumer time is an exact-arithmetic replay
cost, not an operational quantum cost or new scientific test case.
