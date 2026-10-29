# A literal copy-only inverse-mean signal for the ordinary recovery consumer

30October2026. C's finite control admission, using root's controlled-sine
suggestion and ordinary QSVT/oblivious-amplification machinery. This closes
the copy-to-block-encoding port in C_STRONG_ORDINARY_ROUTE.md without
an unknown purification, inverse unitary, or a free "taking logarithms"
oracle. It is deliberately polynomial rather than optimized.

Let S be an unknown density matrix, available as fresh stored copies,
whose NONZERO spectrum is in[mu,1], with public rational0<mu<=1/2.
Its support projector is not given. The input presented to recovery will
lie in this support; every implemented circuit is physical on the whole
carrier, including all zero eigenspaces.

## 1. A bounded native signal from samples

Controlled partial-SWAP simulation, including positive and negative time,
implements controlled exp(plus/minus i S/2). With an ancilla, their
known linear combination

 (exp(i S/2)-exp(-i S/2))/(2i)=sin(S/2)=B

is the top block of a known-format unitary. Public Hadamard/phase gates
and controlled branches supply this block; no postselection is performed
when this unitary is used inside QSVT. Its adjoint is simulated by the
reversed PUBLIC circuit and fresh negative-time sample simulations,
not by attempting to invert a noisy implemented channel.

For the IDEAL signal, occupied eigenvalues lie in[sin(mu/2),sin(1/2)].
Both bounds are separated from0 by at least mu/4. Approximation of every
sample-based unitary call is paid at full reference-safe channel level
over its declared total use count.

## 2. A self-contained polynomial inverse signal

For y in[-1,1], set c(y)=min(3/4,max(mu/4,abs(y))) and

 g(y)=sqrt(mu)/(8 sqrt(2 arcsin(c(y)))).

This even real function is bounded in[0,1/4] and is Lipschitz with constant
at most1/mu. Indeed, where it varies,

 |g'(y)|=sqrt(mu)/[8(2arcsin|y|)^(3/2) sqrt(1-y^2)]
       <=sqrt(2/7)/mu <1/mu;

the cap and floor are1-Lipschitz and make it constant elsewhere. On the
occupied signal, c(sin(lambda/2))=sin(lambda/2), so

 g(sin(lambda/2))=sqrt(mu)/(8sqrt(lambda)).             (S1)

Given rational0<eta<1/4, choose an EVEN integer N>=16/(mu^2 eta^2).
Use the Bernstein polynomial on[-1,1], evaluating g at its N+1 grid
points to rational error<=eta/4 and clipping these coefficients to[0,1/4].
Since g is even, symmetrize its polynomial under y->-y. Call the result p.
It is a real EVEN polynomial with rational coefficients, degree<=N,
and exactly0<=p(y)<=1/4 on[-1,1]. The binomial variance bound gives

 sup_|y|<=1 |p(y)-g(y)|
 <=1/(mu sqrt(N))+eta/4 <=eta/2.                      (S2)

The roots/arcsines needed only for scalar coefficient generation are
known real elementary functions on explicitly bounded intervals. Their
directed series/bisection precision is polynomial in the rational input
bit size and log(1/eta); no unknown spectrum is evaluated. Expanding the
Bernstein representation has polynomial cost in N and coefficient bits.

Gilyen--Su--Low--Wiebe,1806.01838, Corollary10/18 and Lemma19, implement
this admissible even polynomial as a block using O(N) calls to the ideal
signal unitary and its inverse and public phase controls. Finite classical
phase synthesis is charged; Haah1806.10236v4 Section4 gives a stable
rational/finite-precision algorithm rather than unit-cost real arithmetic.
An extra eta/2 synthesis allowance gives total signal error<=eta.
All retained circuits, including the QSVT ancillas, are unitary before
the final declared discards. No output support test is assumed.

By(S1)--(S2), the occupied top block approximates

 (sqrt(mu)/8) S^(-1/2)

with error eta. The normalization8/sqrt(mu) is explicitly paid and is
polynomial in1/mu. Outside the support the signal is merely bounded;
it is not asserted to be the algebraic zero-extended pseudoinverse.

## 3. Physical Petz completion and finite sample cost

For reference I_k/k and Stinespring unitary of output-environment dimension
dE, combine this inverse signal with a public maximally entangled dE pair,
the inverse Stinespring query and the known input-ancilla projection.
On the occupied output support, the successful block is the exact Petz
isometry scaled by the KNOWN amplitude

 a_Petz=sqrt(k*mu)/(8sqrt(dE)).                         (S3)

This follows directly from Gilyen etal.2006.16924v2 Eq9: its Petz
isometry includes1/sqrt(k) and an UNNORMALIZED environment entangled
vector, whereas our environment pair is normalized by1/sqrt(dE).
Ordinary robust oblivious amplitude amplification with this known
amplitude uses a polynomial number m of the base unitary/inverse calls
and public reflections. It need only be accurate on the occupied range.
Choose internal inverse-signal error eta at most the desired final block
error divided by the fixed count m, and then choose N from(S2). There is
no circular choice: m is fixed first by(S3), independent of polynomial N.

One subtlety is important for amplification: p(0) is not forced to zero.
Nevertheless every Kraus K_l of F_xi satisfies K_l* Pi_(ker S)=0,
because S=sum_l K_l K_l*/k and each summand is positive. Thus the exact
projected inverse-Stinespring base block ANNIHILATES ker S, regardless
of p(0). Globally its comparison target is a_Petz V_Petz Pi_(supp S),
a partial isometry with singular values a_Petz on the support and0
outside. This is the proper robust-OAA premise; there is no uncontrolled
off-support success block. Root and A independently reconstructed this
kernel cancellation. Approximate Stinespring/sample gates are first paid
by the whole-circuit hybrid against this ideal algebraic block.

The resulting executed unitary/ancilla/discard circuit is CPTP on ALL
carrier inputs. On the occupied range its successful block approximates
the Petz isometry. If that block error is e, its failure amplitude is at
most sqrt(2e); hence the total isometry error is at most e+sqrt(2e).
Choosing the block tolerance quadratically smaller pays any requested
composed-channel accuracy. This explicit completion observation was
independently supplied by A, after directly reading the primary's
minimum-NONZERO-eigenvalue/support convention. No unknown support
projection is physically implemented.

Let Q_S be the total O(mN) ideal sine-signal calls. A single such call
uses a constant number of controlled sample evolutions of bounded time.
Allocate full-diamond error gamma_S/Q_S per signal call. B's explicit
controlled-DME estimate4T^2/n gives a total S-copy count

 O(Q_S^2/gamma_S),                                    (S4)

plus public phase/gate precision. All these copies may be prepared and
stored before a late payload. In the paired construction they are copies
of ACTUAL F_xi(I/k), obtained by source calls; the RDS reflection program
uses a separate store and a separate count. Equations(S2)--(S4) are
polynomial in k,dE,1/mu,1/accuracy, with logD carrier gates/storage paid.
The proof does not assert a competitive constant or an optimal exponent.

## Scope

This is an ordinary signal-polynomial/programmable-Petz construction,
not a new QSVT or recovery theorem. The important interface is that all
black-box primitives in the strong ordinary route can be supplied from
finite forward-source/copy stores. Global CPTP behavior and accuracy on
the source's occupied range are distinct, both explicitly provided.
Implemented-filter leakage/full rank is handled by the completed-factory
hybrid in C_STRONG_ORDINARY_ROUTE.md, not by an invented rank promise.
