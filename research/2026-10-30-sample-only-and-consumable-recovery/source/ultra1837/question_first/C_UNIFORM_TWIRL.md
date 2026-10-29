# A finite uniform growing-rank compression port

30 October2026. C construction, prompted also by root's independently
derived collective-twirl repair. All random-matrix, Schur and synthesis
machinery is ordinary. The point is to pay the growing-rank port that
fixed-d GT enumeration does not pay. No quantum circuit is run here.

## 1. Replace irrep enumeration by one collective twirl

There are M coherent carriers of ambient dimension D, with joint support
inside an unknown rank-d subspace in each carrier; arbitrary references
are untouched. Pad small dimension to the known power of two r>=d, r<2d
(if d=1, take r=1). Ambient carriers can likewise be padded, so assume D>=r
without changing the source. No unknown support basis is supplied.

Apply a known matched Schur transform on the D-dimensional carriers.
Measure/dephase the Young partition lambda, discard the U(D) irrep and
retain its symmetric-group multiplicity register, including every
reference correlation. For lambda with at most r rows, prepare ONE
canonical highest-weight GT basis vector in the U(r) irrep. The row j of
this GT pattern is (lambda_1,...,lambda_j); the interlacing inequalities
hold by monotonicity of lambda. Its O(r^2) entries have O(log(M+1)) bits.
No list of all GT patterns, uniform GT sampler or irrep-dimension coin is
used. Apply the inverse r-dimensional Schur transform with the retained
multiplicity register.

Finally sample ONE Haar U in U(r), apply U to EVERY one of the M carriers,
and discard the sample seed. Within each lambda, irreducibility and Schur's
lemma replace the prepared pure irrep vector by its maximally mixed state;
the multiplicity/reference register is unchanged. This is exactly the
Yoshida--Soeda--Murao compression channel, now at padded dimension r.
Dephasing lambda is licensed: the desired Haar twirl kills cross terms
between its inequivalent fixed-M U(r) irreps. An off-promise partition
gets any fixed CPTP output, e.g. product maximally mixed carriers.

Thus one does NOT need a high-order design theorem or enumerate an irrep
whose dimension can grow as (M+1)^[r(r-1)/2]. The collective U is essential;
independent unitaries on the M carriers destroy the shared latent frame.

## 2. No real-Haar or Gaussian oracle

Fix rational 0<g<=1 as a twirl error budget, M,r>=1. The following gives
an explicitly finite classical random circuit program. Its discrete law
has TV distance1 from continuous Haar. Only the AVERAGED QUANTUM CHANNEL
is approximated; no contrary probability-law assertion is made.

Let G have independent complex standard Gaussian entries, normalized so
E|G_ij|^2=1. Its polar unitary U=G(G*G)^(-1/2) is Haar: for every fixed
unitary W, WG has the same law and polar(WG)=W polar(G). The Gaussian is
nonsingular almost surely, and invariance characterizes Haar.

An elementary useful small-ball estimate is

 Pr[s_min(G)<=s] <= r^2 s^2.                             (10)

Indeed choose a minimum unit vector x and a coordinate |x_j|>=1/sqrt(r).
Then dist(G_j,span{G_l:l!=j})<=sqrt(r)s. Conditional on all other columns,
the component of G_j in a unit orthogonal direction is a standard complex
Gaussian. Its small-ball probability at radius sqrt(r)s is at most r s^2.
Union over j gives (10); rank-deficient other columns occur with probability0.

Use rational constants

 s=g/(16r), u0=g/(16r^2), R=r/u0+1,
 L=(R+1)^2/s^3,
 h=min{s/(2r), g/(64 M r L)}.

Generate each ideal entry by Box--Muller in complex form
G_ij=sqrt(-log U_ij) exp(2pi i V_ij), with independent uniform U,V in(0,1).
Couple these uniforms to their b-bit midpoint truncations. Choose b so

 mesh=2^-b <= min{u0/2, h^2 u0/128}.                    (11)

The actual program samples exactly 2r^2 b fair bits, evaluates the scalar
log/root/sine/cosine functions with directed rational error at most h/4
per complex entry, and obtains a rational complex matrix Ghat.

On the event that every ideal U_ij>=u0, midpoint changes give

 |sqrt(-log U)-sqrt(-log Uhat)|<=sqrt(2mesh/u0),
 |exp(2pi i V)-exp(2pi i Vhat)|<=8mesh.

Also sqrt(-log Uhat)<=2/u0. Equation(11) bounds the resulting complex
entry error by h/2 even after scalar evaluation, hence conservatively by h.
The failure probability of the radial event is at most r^2u0=g/16.
Equation(10) with4s bounds Pr[s_min(G)<4s] by g^2/16<=g/16.
The combined bad mass is at most g/8.

On the good event ||G||<=r/u0<R, ||Ghat-G||<=r h<=s/2 and
s_min(Ghat)>=3s. The rational strict test Ghat*Ghat>s^2 I therefore passes.
If it fails, the actual program outputs the identity unitary instead.
This fallback is physical on every possible random bit string.

## 3. Uniform polar precision and finite gate compilation

Here is a conservative self-contained continuity bound, avoiding a sharp
polar-factor perturbation theorem. If E=Ghat-G, ||E||<=s and the good
event above holds, then both Gram matrices have eigenvalues>=9s^2 and

 ||(G*G)^(-1/2)-(Ghat*Ghat)^(-1/2)||
 <=||(G*G)-(Ghat*Ghat)||/[2(9s^2)^(3/2)].

This follows from the positive resolvent integral for inverse square root:
subtract the two resolvents, bound both by(t+9s^2)^-1, and integrate.
Since the Gram difference is <=(2R+s)||E||, the polar factors satisfy

 ||polar(Ghat)-polar(G)|| <= L ||E|| <= g/(64M).         (12)

The displayed L is deliberately much larger than the sum
1/(3s)+R(2R+s)/(54s^3), so (12) follows for R>=1 and0<s<=1.

Every accepted Ghat has a KNOWN rational singular-value floor s and
bounded entries. The b-bit midpoint Box--Muller law gives |Ghat_ij|^2
<=2(b+1)+2, so ||Ghat||^2<=r^2(2b+4). For example take the rational
perfect-square upper bound O=[4r(b+2)]^2. With H=Ghat*Ghat,

 H^(-1/2)=O^(-1/2) sum_{j>=0} binom(2j,j)4^-j (I-H/O)^j.

The degree-J remainder after multiplication by Ghat is bounded by

 (O/s^2)(1-s^2/O)^(J+1).

For a fully explicit known-unitary compiler put z=g/(16M) and
nu=z^2/(64r). Choose integer Lp with2^-Lp<=nu*s^2/O and
J+1>=Lp O/s^2. All coefficients and matrix arithmetic before known-unitary
gate synthesis are rational. J and the bit costs are polynomial in
r,M,1/g; this conservative proof does NOT claim polylog(1/g) runtime.
It supplies entry evaluation of the exact polar unitary at any desired
precision, with an a priori floor even on unusual accepted random strings.

Reviewer A supplied an explicit constructive completion of this port.
If rational Q approximates exact U=polar(Ghat) by ||Q-U||<=nu<1/4,
row-pivoted complex Givens QR gives Q=V R with positive diagonal of R
(all row permutations are included in V; no uncompensated column
permutation is allowed in this trace calculation).
Every pivot is at least s_min(Q)/sqrt(r)>=(1-nu)/sqrt(r), and
each r_jj>=s_min(Q)>=1-nu. Therefore

 Re Tr(V*U)>=Tr R-r nu>=r(1-2nu),
 ||V-U||<=||V-U||_F<=2sqrt(r nu)<=z/4.

Compute/synthesize its O(r^2) two-level rotations with combined operator
error at most z/2 UP TO A GLOBAL PHASE. A finite universal SU gate alphabet
need not synthesize an arbitrary global phase, so the literal conclusion
is inf_theta||Vimplemented-exp(i theta)polar(Ghat)||<=z. This implements
an ACTUAL unitary circuit, with polynomial floors for all denominators and polynomial
precision. Rounded Kraus matrices are never silently executed as a
channel. All rotations, controls and synthesis errors are charged; no
source-dependent gate is supplied. This is ordinary known-unitary gate
compilation with A's explicit bit-port argument, not a new synthesis claim.

For unitaries U,V, halfdiamond(Ad(U)^tensorM,Ad(V)^tensorM)
<=M inf_theta||U-exp(i theta)V||. Global phase cancels because these are
UNCONTROLLED conjugation channels. Coupling the finite-bit program to ideal G and using (12)
therefore bounds averaged-channel error by

 g/8 + g/64 + g/16 < g/4.                               (13)

This leaves at least3g/4 for the two Schur compilers, highest-weight
preparation/routing and any additional standard known-control error.
The sampled seed must not be retained as an extra output of the compared
compression channel. Later tomography is a fixed CPTP postprocessing, so
(13) remains reference-safe through the entire adaptive decoder.

## 4. Ordinary Schur controls and the growing-d claim

Yoshida--Soeda--Murao2110.00258v4 Lemma4/Eqs22--23 is the exact channel
identity used above; it is all joint inputs including references.
Burchardt et al.2509.22640v1 Theorem1, Table1 and Sections4--7 provide the
corrected high-dimensional Schur implementation in matched YY/GT bases,
with tilde-O(M^4) controls and tilde-O(M^2) workspace; hidden factors are
polylogarithmic in M,D and inverse approximation error. For small local
dimension, the usual BCH circuit gives polynomial dependence on M,r
and precision (the same source's Section8 explicitly discusses both
regimes). Thus use corrected high-D Schur on the ambient carriers and
ordinary uniform polynomial(M,r) Schur on the compressed carriers.

The only nonuniform step in the old fixed-d compiler was not assumed
away: replacing its GT enumeration by Sections1--3 makes this port
polynomial when r itself grows polynomially with inverse target error.
Ambient storage remains M log D qubits, plus references/work and all
random/control records. The quantum circuit is not an acquired native
laboratory capability, a classical data learner or a streaming interface.

Mezzadri's Gaussian-to-Haar constructions are a primary ordinary
predecessor, not a claim of a new random-unitary generator. The exact
polar invariance and finite-bit bounds above are supplied explicitly so
that no Haar, Gaussian or inverse-spectrum oracle enters the theorem.
