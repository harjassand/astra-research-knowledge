# A stronger ordinary route: consume a preacquired recovery program

30 October2026. C derivation from controlling primary theorems, with
root's independent circuit reconstruction and A's substantive whole
challenge reporting no remaining structural objection. File-bound receipts
are separate. This is not a claim that the least-rank Petz application in
the primary already states our full result.

## 1. What the new primary does and does not supply

Yoshida--Niwa--Utsumi--Takagi--Murao,2512.21260v2, Theorem3/Eq38 supplies
a superchannel converting n parallel calls of one CPTP F:k->B of Kraus rank
at most r into n parallel calls of ONE randomly chosen dilation isometry
V:k->E tensor B, dimE=r. The common random V, not independent draws, is
load-bearing. The proof/actual circuit uses source-input preprocessing;
therefore it cannot be applied retroactively to a received payload to
recover its inaccessible environment. We use it ONLY in offline calibration.

Theorem5, Lemma6 and Eqs44,51 provide a stronger useful program primitive.
For known V0:k->E tensor B, there is a physical offline procedure generating
a joint state with mathematical representation

 integral [P_(V,theta)/k]^tensor n dV dtheta,
 V(theta)=(exp(i theta)|0>V0+|1>V)/sqrt(2),
 P_(V,theta)=V(theta)V(theta)*.                           (O1)

All n copies in(O1) share the SAME V and theta. The controller receives
neither label. The offline circuit is obtained by composing Theorem3 and
Lemma6 and choosing the logical inputs as I_k/k. This is not a product
of separately averaged single-copy programs. The proof representation
can be used in subsequent adaptive channels by linearity, exactly as the
common-frame representation in N1291.

The theorem's direct Petz application, Theorem13/Eqs67--71, is narrower:
r=d_input/d_output, hence a dilation UNITARY and a maximally mixed mean
output. That condition does not hold for a generic expanding approximate
encoder. The route below instead uses Theorem3+5 with the GENERAL Petz
algorithm of Gilyen et al.2006.16924v2, Theorem1.

## 2. One consistent controlled Stinespring unitary from stored copies

Conditional on V,theta in(O1), define

 U_(V,theta)=2P_(V,theta)-I.                             (O2)

This is a Hermitian unitary. Its exact action is

 U_(V,theta)(|0> tensor V0 psi)
       =exp(-i theta)|1> tensor V psi.                  (O3)

This is Eq51--53 in the primary. Choose V0 as a public computational
basis embedding. H=C^2 tensor E tensor B can be identified as logical
C^k tensor workspace of dimension2r dimB/k at input, and B tensor
environment C^(2r) at output. Since r=k*d, the workspace dimension is
the integer2d dimB even for non-power-of-two k. Known binary-register
padding/reversible basis reorderings are paid, with unitary extensions
on unused computational states. The public reordering identifies |0> tensor V0 psi with
psi tensor |0_workspace>. Thus(O2) is an ACTUAL Stinespring unitary of F,
with output-environment dimension2r. Its arbitrary action off the known
input subspace is irrelevant to the represented channel; its inverse is
the SAME unitary(O2). Global phase in(O3) does not change F.

This does not grant an unknown-unitary controlled gate for free. From a
fresh stored copy of P/k, controlled density-matrix exponentiation at time
pi*k approximates

 |0><0| tensor I + |1><1| tensor exp(-i pi P)
   =|0><0| tensor I + |1><1| tensor (-U_(V,theta)).

A KNOWN Z phase on the control corrects that minus sign. This phase cannot
be discarded in a controlled operation. Partial-SWAP simulation with
control-conditioned Hamiltonian |1><1| tensor SWAP pays the same
dimension-independent diamond error as ordinary DME. For each call error
e, O(k^2/e) fresh program copies suffice with an explicit nonasymptotic
constant (B's controlled-DME proof supplies it). For m sequential
controlled/uncontrolled uses, allocate e=gamma_V/m; the total stored
program count is O(m^2 k^2/gamma_V). Every used copy is consumed.

This proves consistency through inverse and adaptive controlled uses:
condition on ONE(V,theta), apply the uniform DME error bound to each
operation, then average the SAME latent mixture. Regenerating(O1)
independently for each query would be invalid and is not this protocol.

## 3. Pay rank and output conditioning by the existing filter

Let the fixed spectral filter P=1_[b,infinity)(N(I/k)) have a<=b<=2a,
and let F=J_P N including its orthogonal failure flag. Its mean has rank
at most d=floor(1/a)+1; positivity of the Choi state implies it is supported
on C^k tensor supp(F(I/k)). Consequently Kraus rank(F)<=k*d.

To avoid inversion of an arbitrarily rare failure flag, define the ACTUAL
known postprocessing

 F_xi=(1-xi)F+xi[Tr(.)|fail><fail|],  0<xi<=1/2.         (O4)

It can be applied to already encoded payloads: perform the existing filter,
then with a public coin replace its output by the flag. This does not
rewire the unknown logical payload before N. On success support the mean
eigenvalues are at least(1-xi)a, while the flag eigenvalue is at least xi.
Thus every NONZERO eigenvalue of S=F_xi(I/k) is at least

 mu=min(xi,(1-xi)a).                                    (O5)

There are zeros outside the actual common support. No spectral or
pseudoinverse control there is needed for a payload in the range of F_xi.
The recovery circuit must be a physical CPTP completion, with arbitrary
output on that orthogonal complement, or retain a declared failure branch;
one must not call the zero-extended algebraic Petz formula globally TP.
All inverses/QSVT polynomial approximations use cutoff mu on the occupied
support and are bounded on the rest of[0,1]. The executed Petz processor
is a fixed unitary/ancilla/discard circuit and is therefore CPTP on EVERY
input, including outside that support. Accuracy is asserted only after
composition with F_xi, whose range lies in that support for arbitrary
references. No unknown support-projector gate is supplied for completion.

Apply the offline RDS program with the KNOWN rank bound r=k*d. The
environment count is2r, rather than2k dimB. This is precisely the
effective-rank information that prevents the ordinary Petz circuit's
environment factor from reintroducing ambient D.

## 4. General Petz implementation with no late source calls

Gilyen et al.2006.16924v2 Theorem1 gives an approximate physical Petz
operation from a Stinespring unitary and its inverse, block encodings of
the reference state and its mean output, with paid conditioning and
environment factors. Here reference I/k is public, its conditioning is k;
environment dimension is2r; output-mean inverse scale is at most1/mu.
Thus the counts of these controlled primitives are polynomial in
k,r,1/mu,1/epsilon, with no polynomial D factor. Known carrier controls
still act on logD qubits and all storage/control costs count.

The public source can prepare fresh S copies during calibration, and
they may all be stored. C_COPY_SIGNAL.md supplies a literal ordinary
replacement for a free block-encoding assertion: controlledDME gives the
bounded signal sin(S/2); a bounded even Bernstein/QSVT polynomial in that
signal approximates (sqrt(mu)/8)S^(-1/2) on the occupied range. Its
normalization, finite coefficient/phase synthesis, inverse/controlled
uses and all fresh copies are paid. This gives the actual inverse-mean
primitive used in the primary's Petz-isometry/amplification proof,
without handing the algorithm a purification gate or a logarithm oracle.
Controlled positive/negative-time partial swaps implement each requested
approximate unitary-channel call. Allocate a separate diamond-error
budget to every primitive in the fixed known Petz circuit; a hybrid bound
applies after(O1)'s latent variables are fixed and is then averaged.
All original-source calls and all random/quantum controls are finite and
polynomial at the stated scales, rather than treating an adjoint as an
oracle. Generic optimal recovery after small-space tomography remains
an admitted alternative as well; there is no claimed best exponent.

The Petz map of F_xi is INDEPENDENT of the Stinespring dilation and its
environment orientation. Hence, for every V,theta in(O1), the ideal
consumer is the SAME channel Petz_(F_xi). This is what allows a preacquired
program to be used on a later already encoded payload; unlike N1291,
the payload need not participate in its training program's Schur frame.

For any predetermined finite number T of later payloads, possibly entangled
with one another, preallocate enough program/S/filter copies and controller
precision for all T uses. Consuming disjoint fresh program blocks with the
same latent V,theta implements T uses of the SAME ideal Petz channel to
total implementation error gamma. It is not an unlimited reusable catalyst.
Ideal recovery noise also composes over T uses by the usual hybrid bound;
no constant single-use error is promoted into a block-independent error.

## 5. Off-promise completion and the implemented filter's full rank

An approximate implemented filter can have full ambient output/Kraus
rank. It is NOT inserted into the rank-r theorem by asserting its actual
rank is r. Instead use ONE fixed completed physical program factory and
compare its finitely many actual calls to ideal F_xi by a comb hybrid.

The controlling PDF2512.21260v2 was visually read at page7, Fig2(a): all
source calls precede QFT over S_n; its lambda label is explicitly measured;
only then are pi_Ulambda^(r) and inverse Schur(r) prepared/applied. Add
the arithmetic predicate len(lambda)<=r at that measured branch. If it
fails, discard the would-be offline program and output a fixed normalized
program state of the SAME known format. If it passes, use the canonical
GT/finite-Haar irrep preparation from C_UNIFORM_TWIRL.md and the ordinary
inverse Schur. All remaining modules are known unitaries, normalized
preparations, measurements or discards, so the completed factory is CPTP
for ANY supplied channel, regardless of its rank. No postselection or
physical rank test is used. A independently derived this same repair.

On ideal rank<=r F_xi the invalid-lambda branch has zero Choi weight by
the random-purification identity Eq32--37. Its branch is CP; zero Choi
trace implies its Choi matrix and hence its map vanish. Thus completion
does not alter the exact promised superchannel, for any input/reference.
Lemma6's subsequent controlled permutations/addition are already known
physical operations; compose them with this same completed factory.

Let Q be the fixed number of F_xi invocations required for program and
S-copy calibration and all later payload postprocessing, before launch.
Set each implemented filter's reference-safe half-diamond error at most
gamma_filter/Q. The completed factory plus all later fixed circuits are
CPTP, hence hybrid comparison costs at most gamma_filter, EVEN THOUGH
the actual intermediate program and mean-output copies may be full rank.
Their rank and spectra are never used as ideal promises. Only the actual
physical source's deviation from the IDEAL FILTER IMPLEMENTATION is paid
here, not its noise versus a hypothetical perfectly correctable source.

There is no circular resource condition: first count ideal program/S
calls from public k,d,mu,epsilon,T. This fixes Q. Then B's polynomial
source-copy filter is compiled at error gamma_filter/Q. Its extra A copies
are obtained directly from the ORIGINAL N(I/k), not by recursively
filtering F copies. Every one of them counts as an original source call.

## 6. Performance and what remains conditional

If the original N has some recovery of Bell fidelity>=1-kappa and filter
tail t, root's proved projection lemma gives a recovery competitor for F
with infidelity<=2kappa+3t. Replacing by(O4) adds at most xi. Ordinary
Barnum--Knill then gives

 halfdiamond(Petz_(F_xi) F_xi,id_k)
   <= k sqrt(4kappa+6t+2xi).                            (O6)

Filtering a received payload also has its separately paid implementation
error. Bad threshold mass and total program/control simulation error add
at instrument/channel level. No n*kappa or n*t comparison of program
carriers with a noise-free source is used.

This is a materially stronger ordinary timing alternative than the basic
joint-payload tomography construction, if all the admitted source-copy
and support-completed Petz ports are implemented as specified. It uses
the SAME opaque, memoryless forward source and protected coherent
storage, plus known controls. It does not assume a physical noiseless
environment, a classical ambient description, an exact-recovery promise,
online source access or a learned reusable original-D classical decoder.

## 7. Explicit agnostic and finite-stream consequence

For logical dimension k, supplied intrinsic index d0 and rational0<eps<=1,
choose

 a=eps^2/(192k^2 d0), xi=eps^2/(32k^2),
 gamma=eps/4, bad-threshold budget q=eps/8.

Equation(O6) and t<=tail_d0(A)+2d0*a give

 halfdiamond(decoded,id_k)
 <=eps+k sqrt(4kappa+6tail_d0(N(I/k))).                 (O7)

Indeed the squared accuracy-only contribution is eps^2/8; its square
root is eps/(2sqrt(2)), and gamma+q=3eps/8 leaves total<eps.
Neither numerical kappa nor numerical spectral tail is an algorithm input.
There are NO tomography calls and no classical learned channel in this
stronger route. Their omission does not mean the program/source/control
stores are cheap or intrinsically bounded in qubits.

For a predetermined finite T of later payloads, choose a and xi with
(eps/T)^2 instead. Retain ONE threshold, charge q ONCE for its common
bad-gap event, and gamma over the ENTIRE program factory and T consumers.
The same argument and a T-use hybrid give

 halfdiamond(decoded_T,id_k^tensorT)
 <=eps+T*k sqrt(4kappa+6tail_d0(N(I/k))).                (O8)

This includes arbitrary entangled payload inputs/references and known
intervening processing through the reference-safe sequential simulation.
Program size, preacquired copies, control precision and consumed blocks
grow polynomially with T. It does not provide a catalyst for an unknown
unlimited stream or an error-independent block compression guarantee.

No numerical cost comparison has been run and no superiority of constants
or practical feasibility is asserted. The new main explanatory point is
to compose a PAID effective-rank filter with an established strong
programmable-recovery route, instead of withholding that route and calling
the batch-only construction uniquely necessary. Historical priority of
the full composition is UNKNOWN.
