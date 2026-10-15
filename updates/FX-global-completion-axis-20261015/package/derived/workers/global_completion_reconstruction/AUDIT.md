# Independent global-completion reconstruction

15 October 2026. This worker reconstructed the equations from the frozen
`global_compatible_positivity` JSON and defining quartics, without importing
producer code. Its source replay ran only in `disposable_source`. Receiving
proofs were read at main `ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25` in the
assigned W checkout, which this worker did not modify.

**Conclusion:** the load-bearing universal identities, projected-cone
characterization, Schur positivity construction, heat-to-QC argument, and
determinant-square integrated heat obstruction withstand this internal audit.
No mathematical correction to Theorems A-D was needed. The receiving negative
branch already has a substantially stronger sharp theorem. The combined
capital also proves a stronger ordinary-polyconvexity obstruction than the
new source states: every finite-H completion on the nonzero curved projected
boundary is non-polyconvex, including all positive parameters.

This is internal model-assisted reconstruction. It is not external review,
formal proof verification, historical novelty clearance, or a physical or
computational capability demonstration.

## 1. Exact reconstruction method and receipts

`reconstruct_global_completion.py` reads only the frozen JSON as algebraic
data and differentiates the integrands itself. For each of the ten quadratic
monomials in A, it compares the complete symmetric 6-by-6 coefficient matrix
in the compatible second jet. This differs from the producer's scalar
polynomial-expansion implementation. It verifies all three universal
identities, closedness, Euler primitives, the displayed null form, the moving
kernel/support, quotient matrices, LDL formulas, projection necessities and
decomposition, the entire invariant/contact linear spaces, the receiving
four-square acoustic identity, and a direct Fourier dissipation calculation.
Its exact rational instances include r=-11/4, r=1, and r=1/2.

`reconstruct_receiving_sharp.py` independently reads the receiving universal
negative-branch certificate and checks its ten tensor identities, all
denominators, exact primitive, natural diffusion, congruence, zero off-block
entries, and newly recomputed block LDL pivots. It does not import or run
receiving source code. `verify_no_polyconvex_completion.py` reads no producer
data at all and differentiates the all-alpha local support obstruction.

The exact receipts are `RECONSTRUCTION_RECEIPT.json`,
`RECEIVING_SHARP_RECEIPT.json`, and
`NONPOLYCONVEX_COMPLETION_RECEIPT.json`. `logs/` preserves executed output.
An initial receiving-reader schema-key error is retained in
`logs/receiving_sharp_schema_read_error.log`; the worker was corrected to use
the actual exported pair/monomial keys. It was not a mathematical or source
verification failure. The inspected producer verifier passed in the worker's
disposable copy, with its own receipt retained there.

## 2. Precisely what is universal in the new algebra

Use x=(a,b,c,d), u=a^2+c^2, j=ad-bc,
H=((a-d)^2+(b+c)^2)^2, and

\[
P_{\alpha,r}=\alpha H+\frac{r(r-1)}6u^2+j^2+ruj.
\]

For every real r except -1, and every A and compatible second jet z, the
JSON gives exact identities

\[
Z^TC_rS_0C_r^TZ=\mathcal D_{P_{3,r}}+\omega_{0,r}(B_1,B_2),\quad
Z^TC_rS_NC_r^TZ=\omega_N(B_1,B_2),\quad
Z^TC_rS_HC_r^TZ=\mathcal D_H,
\]

where both two-forms are closed and exact. Their Euler primitives are
`Omega.T*x/4`, in the stated coordinate convention. The null correction and
its reduced Gram are constant in r after cancellation. Neither the null form
nor its Gram is asserted to be nonnegative on all jets.

The old acoustic curve produces six forced kernel vectors. The reconstruction
finds a six-row minor equal to r+1 and checks their annihilation by C_r^T.
The identity minor in C_r proves rank 18. The separate constant kernel basis
N and complement R have det[N,R]=1. On this basis, S_H is zero on ten
directions and positive on eight; its eight LDL pivots are

\[
12,4,4,32/3,5/2,12,20/3,4.
\]

The null correction restricts on the ten-dimensional kernel precisely to
diag(0_6,I_4). The six-dimensional remaining block A_6 has pivots

\[
2q/3,\quad2(q+3)/3,\quad2q(r+1)^2/(q+3),\quad
2(r+1)^2,\quad2q(5q+3)/(9(r+1)^2),\quad2q/3,
\]

where q=r(r+2). These are all positive for every q>0. This is a universal
sign proof on two unbounded components, rather than a parameter-grid test.
The pole r=-1 is outside those components.

## 3. Both completion estimates are valid

Write N^TS_0N=[[A_6,B],[B^T,E]]. Since A_6 is positive definite for q>0,
let K_4=E-B^TA_6^{-1}B. The row-sum choice

\[
\lambda=1+\max_i\sum_j |K_{4,ij}|
\]

makes K_4+lambda I positive definite: the operator norm of a real symmetric
matrix is at most its maximum absolute row sum. The first Schur complement
therefore makes P=N^T(S_0+lambda S_N)N positive definite.

Now write the full congruence in blocks [[P,U],[U^T,V]] and set
K_8=V-U^TP^{-1}U. For H_8=R^TS_HR=L D L^T and
T=L^{-1}K_8L^{-T}, the source choice

\[
\mu=1+\max_i\frac{\sum_j|T_{ij}|}{D_{ii}}
\]

gives mu D+T positive diagonal and strict row diagonal dominance. The second
Schur complement therefore proves S_0+lambda S_N+mu S_H positive definite.
The added null correction changes no integrated compatible energy.

The single-rational alternative is also sound. Put T_4=B^TA_6^{-1}B>=0,
choose lambda=1+tr(T_4)+tr(E^2), and let e=||E||op. Then

\[
E-T_4+\lambda I\succeq[1+\operatorname{tr}(E^2)-e]I\succeq3I/4.
\]

The last step follows from tr(E^2)>=e^2 and 1+e^2-e>=3/4. After the first
Schur complement, M=H_8^{-1/2}K_8H_8^{-1/2} is symmetric and
tr((H_8^{-1}K_8)^2)=tr(M^2)>=||M||op^2. Hence choosing
mu=1+tr((H_8^{-1}K_8)^2) gives mu I+M>=3I/4. All inverses exist by the
preceding positivity, so both formulas are finite for every fixed q>0.
At rational r, they use exact finite rational matrix arithmetic.

The resulting Gram certifies P_(3+mu,r). Consequently P_(4+mu,r)-H is QC,
as stated by the source. A slightly fuller reading is useful: defining
c(r)=3+mu, P_(c(r),r) is QC, and for every alpha>=c(r),

\[
\int_\Omega[P_{\alpha,r}(B+D\phi)-P_{\alpha,r}(B)]
\ge\frac{4[\alpha-c(r)]}{1875}\int_\Omega|D\phi|^4.
\tag{A1}
\]

At alpha=c(r)+1 this recovers the source's stated margin. This is an explicit
sufficient threshold, with no optimality assertion.

## 4. All-background heat implication and gradient constant

Fix any q>0 and a completed coefficient. For a smooth compact perturbation,
use A_t=B+D exp(t Delta)phi and the relative energy

\[
E(t)=\int_{\mathbb R^2}[F(A_t)-F(B)-DF(B):D\phi_t].
\]

At every t>0, derivatives of the heat perturbation are Schwartz. Since the
two-form coefficients are homogeneous quadratic, its global primitive is
cubic in A. The pullback of that primitive also contains one derivative of
A_t; it therefore decays at infinity even when B is nonzero. Stokes gives
zero integral for the correction. Integration by parts gives
E'(t)=-integral corrected_heat_density<=0.

Quartic Taylor growth is bounded by a constant times
|B|^2|Dphi_t|^2+|B||Dphi_t|^3+|Dphi_t|^4. The ordinary two-dimensional heat
kernel gives ||Dphi_t||p<=Cp t^(-1+1/p)||Dphi||1 for p=2,3,4, so these
integrals decay as t^-1,t^-2,t^-3. Thus E(infinity)=0. Strong heat continuity
in L2,L3,L4 gives E(0)>=0. The integrated affine term is zero. Strong
W1,4 approximation gives the result on bounded Lipschitz domains. Periodic
Stokes and heat decay give the torus version. A zero-end periodic strip
extends by zero in the nonperiodic direction and then periodizes; only the
zero function trace is needed, not a zero derivative trace.

For x,h in R2,

\[
|x+h|^4-|x|^4-4|x|^2x\cdot h-|h|^4/3
=6(x\cdot h+|h|^2/3)^2
+2(|x|^2|h|^2-(x\cdot h)^2)\ge0.
\]

For f=phi1+i phi2, 2 barpartial f=C Dphi and partial f=Beurling(barpartial f).
The complex-valued L4 bound sqrt(24) in Bañuelos-Janakiraman Theorem 1.1
was checked in the actual PDF, including a rendered page 2. It gives

\[
\|D\phi\|_4^2\le2(24+1)\|\bar\partial f\|_4^2
=\frac{25}{2}\|C D\phi\|_4^2.
\]

Squaring and combining with the quartic inequality proves 4/1875 per unit
of QC-subtractable H. Zero extension handles bounded zero-boundary data.
For periodic data, multiplying a periodic perturbation by a cutoff varying
on scale L, dividing by L^2, and passing L to infinity transfers the same
whole-plane constant; the derivatives of the cutoff have lower order.

Primary bound: [Bañuelos-Janakiraman, Theorem 1.1](https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf).
This is a nonsharp inherited operator estimate, not a new transform theorem.

## 5. Projected cone: exact necessity and sufficiency

For F=alpha H+beta u^2+gamma j^2+delta uj, the direct acoustic curve is

\[
D^2F(A_t)[e_1\otimes(t,1)]^2
=[12\beta+2\gamma(1-s)^2+(6-4s)\delta]t^2
+2s^2(2\beta+\delta)t^4.
\]

The superscript 2 denotes repeated Hessian direction, not a square of its
value. The independent tests give alpha>=0 and gamma>=0. If gamma=0, the
coefficient linear in s forces delta=0, beta>=0. If gamma>0, minimizing the
t^2 coefficient gives 6beta gamma-delta^2+delta gamma>=0. The large-t
coefficient gives 2beta+delta>=0. More decisively the (b,c) block of
D²F[e11,e11] has determinant

\[
8\alpha(2\beta+\delta)-\delta^2.
\]

For delta!=0, finite completion therefore requires 2beta+delta>0. At r=-2
on the curved family this determinant is -4 for every alpha. For q<0 a
rank-one acoustic test is negative. These are genuine ROC obstructions.

For delta!=0 satisfying the source conditions, p=6beta+delta is positive,
lambda=delta²/p>0, rho=p/delta satisfies rho>0 if delta>0 and rho<-2 if
delta<0, and gamma>=lambda. Exact coefficient matching gives

\[
F=\lambda P_{\alpha/\lambda,\rho}+(\gamma-\lambda)j^2.
\tag{A2}
\]

The core has a finite QC completion by Sections 2-4, and the remaining
determinant square is polyconvex. Delta=0 is immediate from nonnegative
H,u²,j². Thus pi(ROC)=pi(QC) is proved with exactly the source alternatives.
It is equality after deleting alpha, not equality of all alpha fibres.
The projection is nonclosed at the curved limit r=-2. The necessary lower
bound 3r/[8(r+2)] diverges there; the compiler's much faster blow-up is not
proved necessary.

The entire nine-dimensional invariant space and the contact codimension five
were also regenerated directly: the infinitesimal target-rotation operator
on all 35 quartic monomials has rank 26, and the zero-acoustic-contact
gradient system has rank five on that nine-dimensional kernel. Its remaining
four-dimensional span is precisely H,u²,j²,uj.

## 6. Strongest receiving theorem and actual new scope

The receiving pinned checkout already proves the exact ROC characterization
by two positive semidefinite matrices,

\[
P=\begin{pmatrix}6\beta+\delta&\delta\\\delta&\gamma\end{pmatrix},
\qquad Q=\begin{pmatrix}8\alpha&\delta\\\delta&2\beta+\delta\end{pmatrix},
\]

and QC equivalence throughout delta<=0. Its sharp curved coefficient is
a0(r)=3r/[8(r+2)], and its universal negative-branch certificate establishes
QC at a0(r) for every r<-2. The reconstructed receiving pivots are positive
rational functions throughout that branch. For arbitrary negative-delta
triples, the exact receiving decomposition is

\[
F=\lambda J_\rho+(\gamma-\lambda)j^2+(\alpha-\alpha_0)H,
\quad J_\rho=P_{a_0(\rho),\rho},
\quad\alpha_0=\frac{\delta^2}{8(2\beta+\delta)}.
\]

The two PSD conditions imply both remainder coefficients are nonnegative.
Its coercivity constant for alpha>alpha0 is 4(alpha-alpha0)/1875. These
existing receiving results dominate the new nonsharp negative completion.
For example, at r=-11/4 the receiving sharp floor is 11/8, whereas the new
compiler offers integer 27 for the H-subtracted example.

The receiving positive sharp branch has a distinct local fixed-input-heat
obstruction and still lacks a QC proof. The new completion does not contradict
that result: raising alpha removes the second sharp acoustic contact. Its
18-dimensional support imposes only the original contact, rather than the
12-dimensional sharp support forced by both contacts.

The actual added candidate mathematical capital is therefore:

- The explicit isotropic universal identity and one parameter-independent
  null correction with the 6+4+8 completion mechanism.
- All-background QC completion at sufficiently large finite coefficient for
  every positive r, and hence positive-delta projected triples.
- Equality of the entire projected ROC and QC cones, while the positive sharp
  fibre boundary remains unresolved.
- The actual negative integrated determinant-square heat dissipation,
  which is stronger than merely a local or SOS ansatz obstruction for that
  same heat operation.

The short proof in `EXACT_NONPOLYCONVEX_COMPLETION.md` strengthens the source's
limited non-PC example: every P_(alpha,r), for every finite alpha and q>0,
is non-polyconvex. It applies to arbitrary convex lifts and survives every
C3 penalty flat through order three at I. Consequently the entire nonzero
rank-one first-LMI boundary in the completion projection has no finite-H
polyconvex completion, while it has a QC completion.

One fully exported positive example is

\[
62385H+j^2+uj.
\]

`POSITIVE_R1_COMPLETION.json` contains its exact rational isotropic certificate
for subtraction of one H and 18 positive LDL pivots. The independent compiler
bound before rounding is 1006132469/16128. The integrand is non-polyconvex by
the ordinary support proof and has affine Jensen margin at least 4/1875.
Neither this large coefficient nor the source's representative table is an
optimal threshold. The sharp positive floor is only 1/8 at r=1, and QC at
that floor remains unknown.

## 7. Determinant-square obstruction: exact and operation-specific

On the normalized square torus, use k=exp(-t) and

\[
f=k(\sin x+\sin y),\quad
g=-\frac{k^4}{2}(\cos2x+\cos2y)+2k^2\sin x\sin y.
\]

The independent derivative and finite Laurent-coefficient calculation gives

\[
J=2(k^3-k^5)\cos x\cos y(\sin x-\sin y),\qquad
\langle J^2\rangle=\frac12(k^3-k^5)^2,
\]
\[
\frac{d}{dt}\langle J^2\rangle=k^6(1-k^2)(5k^2-3).
\]

The integrated Hessian dissipation was also differentiated and averaged
directly; it is the negative of this derivative for every k. At k=9/10 its
value is exactly -212044959/2000000000. This is a compatible map, not a
sampled noncompatible jet or a floating-point simulation.

For any fixed SPD input diffusion D, take L=D^(1/2), y=L^-1x and the same
map in y. It solves D-heat, and its normalized determinant-square energy
and derivative are multiplied by (det L)^-2>0 on the transformed lattice.
Large smooth cutoffs produce compactly supported compatible maps with the
same negative sign: the leading dissipation is the negative periodic average
times the positive cutoff-fourth-power integral, and differentiated-cutoff
errors are lower order after division by area.

Any correction whose integral is universally zero cannot make this same
fixed-heat dissipation pointwise nonnegative, because its integral would
still be negative on the witness. This excludes all such corrections for
that operation, not merely SOS or two-form corrections. It does not exclude
other flows, output operators, nonzero-integral additions, or a separate
minor-Jensen channel. The integrand j² itself remains polyconvex and QC;
there is no negative Jensen energy and no Morrey counterexample.

## 8. Proof gaps, finite checks, and unresolved boundaries

No load-bearing algebraic or analytic gap was found in Theorems A-D under
the stated conventional smoothness, diffusion and domain assumptions.
The proof's universal components are the rational coefficient identities,
exact pivot functions with sign proofs, the two symbolic Schur estimates,
and the analytic heat/density argument. Finitely many rational instances
are additional safeguards and concrete exports, not universal premises.

The following remain separate open or unaudited matters:

- Positive-delta sharp QC fibres, especially QC of J_r for r>0, are UNKNOWN.
  A failure to exceed the compiler bound is not a non-QC proof.
- The full nine-coefficient Morrey implication, other contact types, and
  singular backgrounds are not settled by the projected face result.
- Ordinary polyconvexity of strict interior projected triples is not decided
  here. The no-completion theorem concerns the nonzero curved boundary.
- The source's contextual Calderon representation of the entire acoustic
  cone is not a premise of the completion proof and was not independently
  reconstructed in this worker.
- Historical novelty, external mathematical correctness review and formal
  proof-assistant verification remain UNKNOWN. A same-team reconstruction
  is internal evidence, and successful replay establishes its exact scope.
- No optimizer complexity, useful numerical storage computation, experimental
  response, material interface, or practical advantage follows from these
  mathematics alone.

The source report, JSON and scripts remain frozen. `SOURCE_BEFORE.json` and
`SOURCE_INTEGRITY_RECEIPT.json` record the byte-preservation check.
