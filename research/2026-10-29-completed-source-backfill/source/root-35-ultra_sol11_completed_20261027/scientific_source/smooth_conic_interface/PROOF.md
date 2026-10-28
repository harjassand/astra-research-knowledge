# Calibrated finite SOS primitive

This concerns the accepted rational-selector planar quartic F. Frozen inputs
are R180 and `../support_gram_compiler/COMPILER_PROOF.md`. Smoothness is
proved near the entire graph, not throughout the five-dimensional domain.
In fact the representative is real analytic on that graph neighborhood.

## Definition

Write m(A)=(A,q(A)), q=det, T=|A|^2. Fix

    epsilon=1/100, kappa=1/20000000, e=epsilon-kappa,
    H=F-kappa q^2, pH=p6-2kappa q T^2,
    sigma=1/34, D(A)=(T(A)+sigma)^2, k(A)=pH(A)/D(A).

The compensated graph energy is f=H+eT=W_epsilon-kappa|m|^2. Define

    ell_A(B,s)=f(A)+[Df(A)-k(A)cofA]:(B-A)+k(A)[s-q(A)],
    N(A,(B,s))=D(A)[-3H(A)-eT(A)+DH(A):B+2e A:B]
                                      +pH(A)[s+q(A)-cofA:B].

Euler's identity gives ell_A(z)=N(A,z)/D(A). N has degree at most8
in A and is affine in z. With v4 the70 monomials of degree at most4,

    V(z)=min_t t subject to D(A)t-N(A,z)=v4(A)^T Q v4(A), Q>=0,
    G(z)=V(z)+kappa|z|^2.                                  (1)

There are495 affine coefficient equations and one70 by70 PSD matrix.
This is a fixed conic operation, not a hierarchy limit or positivity
oracle. It is larger than the prior15 by15 moment operation. Their
off-graph values represent different convex extensions.

## Graph matching and global finiteness

Exactly

    T^2 B_H-pH q(X)=R180-kappa[T(cofA:X+q(X))]^2=:R_H.

The squared expression is a linear form in the180 features with norm
squared24; R180>=I/400000 leaves a positive-definite Gram. The26 Gram
for B_H+C T|X|^2, C33/400, also stays positive definite after subtracting
the canonical B_(q^2) correction. Its row norm is at most44 and the
frozen26 Gram exceeds I/25000. The denominator-shift identity is

    D B_(H+eT)-pH q(X)
      =R_H+(2sigma T+sigma^2)[B_H+C T|X|^2]
       +[(e-2C sigma)T^2+sigma(2e-C sigma)T+e sigma^2]|X|^2. (2)

All three residual coefficients are positive. Substituting X=B-A gives
the SOS polynomial D(A)[f(B)-ell_A(m(B))]. Hence t=f(B) is feasible
at m(B), and evaluation at A=B gives the converse bound. Therefore

    G(B,detB)=F(B)+epsilon|B|^2                            (3)

for every B, including zero. The feasible epigraph is convex in(z,t).
Every z=(B,s) is the average of m(B+Y),m(B-Y) with detY=s-detB;
averaging their graph SOS certificates proves finite feasibility at
every z. Also ell_0=0, so V>=0. Closedness of the fixed-degree SOS cone
gives attainment. Thus G is globally finite and2kappa-strongly convex.

Both SDPs have explicit strict Slater points. A graph certificate has a
full70 Gram of rank69, with kernel spanned by the evaluation vector
v4(B). Choose distinct graph atoms B+Y,B-Y, including a nonzero rank-one
Y when s=detB. Their evaluation vectors are nonproportional, so averaging
their graph Grams gives a PD primal Gram at every rational query.
The standard dual is

    max_y L_y N(A,z), subject to M4(y)>=0, L_y D=1,

with495 moments. A full Gaussian functional divided by its positive
expectation of D is strict dual Slater. Standard SDP duality gives equal
values and attainment on both sides. Dirac evaluation divided by D(a)
is the local dual lower certificate below. Exact affine correction and
mixing with these strict points can certify global numerical proposals
if that optimization is later performed. This does not assert global
equality to the supremum of actual calibrated supports away from the graph.

## Local exactness of this fixed finite cone

At each graph base B, the polynomial in(2) after X=B-A has a Gram
positive definite on ALL69 centered monomials of degrees1,...,4:

* e sigma^2|X|^2 supplies every linear feature;
* sigma^2[B_H+C T|X|^2], with its PD26 Gram, supplies X_iX_j;
* (e-2C sigma)T(A)^2|X|^2 supplies A_iA_jX_k;
* the PD180 Gram R_H supplies A_iA_jX_kX_l.

Under A=B-X the cubic group spans every highest-degree3 monomial, with
lower terms already spanned. The quartic group spans degree4, with lower
terms already spanned. Thus the combined feature matrix has full69-column
rank. Other terms add PSD matrices. The resulting centered69 Gram is PD.
Its quadratic Hessian at X=0 is positive definite.

Therefore A=B is a nondegenerate maximum of ell_A(m(B)). The implicit
function theorem gives a smooth stationary point a(z) near B for z near
m(B). Set t(z)=ell_(a(z))(z). The polynomial

    D(a(z)+Y)t(z)-N(a(z)+Y,z)

has zero constant and linear terms. The coefficient map from symmetric69
Grams to polynomials of degrees2,...,8 is surjective: every such monomial
splits into two nonconstant monomials of degree at most4. A fixed linear
right inverse corrects nearby coefficients by a small Gram perturbation.
The PD69 graph Gram remains positive. Thus t(z) is feasible in(1).
Evaluation at A=a(z) proves the reverse bound, so

    V(z)=ell_(a(z))(z)                                     (4)

on an open neighborhood of every graph point. This proves local exactness
and smoothness of the FINITE70 value, not merely an infinite supremum.
The union of these neighborhoods contains the entire graph.

Because ell=N/D is rational with D>0, it is real analytic. The analytic
implicit function theorem applies to the same nondegenerate stationary
equations, so a(z), V(z), and G(z) are REAL ANALYTIC on these neighborhoods.
No analyticity or smoothness away from their union is asserted.

Because ell is affine in z, its local Hessian is

    D2 V=-ell_(zA)[ell_(AA)]^-1 ell_(Az),

PSD of rank at most4. Hence D2G>=2kappa I throughout this neighborhood.
The single calibrated selector removes the competing normal supports
behind the old moment value's corners. Smoothness elsewhere is not claimed.

## Reusable compiler contract

A sufficient reusable planar input is a rational quartic H, degree-six p,
and GIVEN positive-definite Grams for T^2 B_H-p detX on the full
A^3X,A^2X^2 features, and for B_H+C T|X|^2 on the full AX,X^2 features.
Their identities and strict margins must be verified, not only numerical.
For rational e>0 choose0<sigma<e/(2C). The compiler returns D,N and(1),
with exactly70 features and495 coefficient equations. The proofs above
give global finiteness, exact H+eT graph matching and smoothness near the
entire graph at this fixed degree. Strong convexity additionally requires
the compensated input Grams to be verified before adding kappa|z|^2.

Abstractly the same proof works for polynomial graphs m and positive D,
with N affine in z and of bounded A-degree2r, when every calibrated graph
polynomial has a PD Gram on ALL centered nonconstant monomials through r,
and the finite convex hull of the graph is the whole target space. The
cone size is binomial(n+r,r); its coefficient count is binomial(n+2r,2r).
Arbitrary rational selectors need not satisfy this strict input contract.
A supplied graph Gram and derivative bounds also permit a certified
local box to be found by shrinking until Gram and concavity tests pass.
Strictness ensures termination at a fixed base. No polynomial bit-cost,
uniform radius or efficient generic SDP solver is asserted.

## A certified local evaluator from an untrusted rational proposal

For rational z,a put t0=ell_a(z), Y=A-a. Expand exactly

    D(a+Y)t0-N(a+Y,z)=2l:Y+v69(Y)^T Q v69(Y).               (5)

The constant is zero and 2l=-D(a)D_A ell_a(z). Suppose an exact test
proves Q-b I_linear>=0, b>0, where I_linear has ones only on the four
linear features. If |a|^2<=sigma/4, then

    D(a+Y)-sigma^2/2=T(a+Y)^2+sigma|Y+2a|^2+sigma|Y|^2
                                            +sigma^2/2-2sigma|a|^2

is explicitly SOS. Put eta=2|l|^2/(sigma^2 b). The identity

    (5)+eta D(a+Y)
      =[v69^T Q v69-b|Y|^2]+b|Y+l/b|^2
                                  +eta[D(a+Y)-sigma^2/2]  (6)

proves an exact70-SOS upper certificate, since constants cancel. Evaluation
at a supplies a lower certificate. Consequently

    ell_a(z)<=V(z)<=ell_a(z)+eta.                          (7)

Add exact kappa|z|^2 for G. Newton supplies a proposal only; its numerical
accuracy or convergence is not a proof premise. A poor proposal gives a
wider interval or fails the Gram test. Explicit uniform coefficient bounds
and actual executions are separate certified inputs, not assumed here.

## Ordinary comparison and prior

The old15-moment representative is valid globally, with a smaller cone,
and remains nondifferentiable at every graph point. This construction
spends a larger fixed cone to obtain smooth local values and an exact
local evaluator. No equality of off-graph values or generic speed gain is
claimed. Convex jet-extension formulas are established, for example
[Azagra–Le Gruyer–Mudarra](https://arxiv.org/pdf/1706.02235). SOS finite
convergence under optimality assumptions is established, for example
[Nie](https://arxiv.org/pdf/1206.0319). Those are prior context; their
general theorems are not invoked to infer this fixed-degree conclusion
on a noncompact domain. The strict69 Gram and right-inverse argument
prove the specialized local exactness directly. Historical priority of
that specialized composition is UNKNOWN.

The primary comparison also includes the established SDP representation
results of [Helton–Nie](https://arxiv.org/abs/0705.4068) and their
[local-to-global convex-hull construction](https://arxiv.org/abs/0709.4017).
The retrieved abstracts concern compact semialgebraic sets and curvature/
positivity conditions. No unread theorem is invoked to supply this
explicit noncompact70 operation or its measured local evaluation domain.
These sources reinforce that SOS, curvature and SDP representation are
prior machinery.
