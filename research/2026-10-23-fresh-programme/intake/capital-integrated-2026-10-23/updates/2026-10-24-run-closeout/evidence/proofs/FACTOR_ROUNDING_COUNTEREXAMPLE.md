# Factor inputs do not restore dimension-free simultaneous repair

23 October 2026. Self-contained candidate proof. Independent audit and historical
priority remain UNKNOWN. This does not claim an experiment, computational
advantage, or general inventor capability.

## 1. Statement

For each integer d>=4 put m=d-1 and N=md. There are explicit unital FACTOR
subalgebras A_d,B_d of M_N, each isomorphic to M_d, whose trace-preserving
conditional expectations E_A,E_B satisfy

    ||[E_A,E_B]||_cb <=2delta_d ->0,
    delta_d=2(1-m^2/d^2)=2(2d-1)/d^2.                     (1)

Nevertheless every pair F,G of exactly commuting trace conditional expectations
onto arbitrary unital subalgebras of this same M_N satisfies

    max(||F-E_A||,||G-E_B||) >=(1-delta_d)/2 ->1/2.         (2)

The distances in (2) are ordinary induced operator norms, so the same
obstruction holds for cb distance and full diamond distance of the preduals.
The repaired algebras are not assumed to be factors. Their required vector
dimensions follow from proximity alone.

The same obstruction holds for the algebras themselves in the usual
Kadison--Kastler metric (Hausdorff operator-norm distance between their unit
balls). Every pair of unital subalgebras C,D whose trace expectations commute
satisfies

    max(d_KK(A_d,C),d_KK(B_d,D)) >=(1-delta_d)/4 ->1/4.    (2b)

Section 4b proves this directly; it does not assume that closeness of algebras
automatically gives closeness of their trace expectations.

Every input factor has a single central atom of trace1. Thus a minimum
CENTRAL-weight hypothesis, even weight1, does not repair the unrestricted
statement. Its minimal matrix projections have trace1/d ->0. This distinction
must be preserved when comparing with the binary minimum-outcome theorem.

## 2. Explicit unitary and the reduced channel

Use H=C^m tensor C^d and put A=I_m tensor M_d. For Z_d=diag(1,omega,...,
omega^(d-1)) and X_d|j>=|j+1 mod d>, omega=exp(2pi i/d), define

    U=D_X (F_m tensor I_d) D_Z,
    D_X=sum_(a=0)^(m-1) |a><a| tensor X_d^a,
    D_Z=sum_(b=0)^(m-1) |b><b| tensor Z_d^b,
    (F_m)_(a,b)=m^(-1/2) exp(2pi i ab/m).

Each factor is unitary, hence so is U. In environment block form,

    U_(a,b)=m^(-1/2) exp(2pi i ab/m) X_d^a Z_d^b.           (3)

Let B=U A U*. Write iota(T)=I_m tensor T and T_env=Tr_env/m, so E_A=iota T_env
and E_B=Ad_U E_A Ad_(U*). The reduced channel is

    Phi(T)=T_env[U iota(T) U*]
          =(1/m^2) sum_(a,b=0)^(m-1) X_d^a Z_d^b T Z_d^(-b)X_d^(-a).
                                                                    (4)

Thus Phi is the uniform random-Weyl channel using exactly m^2 of the d^2
distinct Weyl unitaries. Let D_d(T)=Tr(T)I_d/d. The full d^2-Weyl twirl is D_d,
and

    ||Phi-D_d||_cb=||Phi-D_d||_diamond=delta_d.              (5)

For clarity, equality of both displayed norms does not rely on Phi being
self-adjoint: Phi* is another uniform subset-Weyl twirl of the same size.
The coefficient l1 distance from the full uniform distribution is

    m^2(1/m^2-1/d^2)+(d^2-m^2)/d^2=2(1-m^2/d^2).

The triangle inequality gives the complete-norm upper bound. The diamond
lower bound follows by applying the predual difference to a maximally entangled
state: the Weyl operators produce d^2 orthogonal Bell states, so the output
trace norm equals that l1 distance. Apply the same argument to Phi* and use
complete-norm duality to obtain the cb equality. The full Weyl-twirl identity
itself follows by testing the matrix units: phase averaging kills off-diagonal
entries and shift averaging makes every diagonal entry Tr(T)/d.

## 3. Nearly commuting input expectations

Let E_0(Y)=Tr(Y)I_N/N be the scalar expectation. Direct factorization gives

    E_A E_B-E_0=iota(Phi-D_d) T_env Ad_(U*).

All maps outside the middle factor are completely contractive, hence

    ||E_A E_B-E_0||_cb<=delta_d.                            (6)

In fact equality holds: precompose the left side with Ad_U iota and use that
iota is completely isometric. The reverse product uses Phi* in the same way,
so ||E_B E_A-E_0||_cb=delta_d. Their difference gives (1).

This also records the strong comparator: the product is already delta_d-close
to the scalar intersection expectation. The obstruction concerns simultaneously
changing both original input expectations, not finding their robust intersection.

There is also an exact Hilbert--Schmidt norm diagnostic. Weyl characters
diagonalize Phi. Apart from its scalar eigenvalue 1, its singular values are
1/m with multiplicity 2(d-1), and 1/m^2 with multiplicity (d-1)^2. Indeed,
the sum of the first d-1 powers of a nontrivial d-th root is minus its last
power, of modulus 1; the trivial character has sum m. The two character sums
in (4) multiply and are divided by m^2.

These are precisely the nontrivial cosines of principal angles between the
Hilbert--Schmidt subspaces A and B. To see this, their isometric embeddings
iota and Ad_U iota have cross-Gram operator Phi. On each associated
two-dimensional principal-angle plane, the two expectation projections have
commutator eigenvalues +/- i sigma sqrt(1-sigma^2). Since m>=3, the largest
modulus occurs at sigma=1/m. Thus

    ||[E_A,E_B]||_(2->2)=sqrt(1-1/m^2)/m.                 (6b)

The commutator is Hilbert--Schmidt skew-adjoint and normal. Its spectral
radius equals (6b), and every induced norm dominates spectral radius by
testing an eigenmatrix. Therefore the ordinary operator-norm and cb defects
are at least (6b), as well as at most 2delta_d. The defect is Theta(1/d),
the same order as the minimum trace 1/d of an input factor's nonzero matrix
projections. The claim is not that (6b) is the exact cb norm.

## 4. Why no close exact repair exists

We need two elementary facts, both written here to avoid a C*-type-rigidity
import.

Rank stability. If linear projections R,S on a finite-dimensional normed space
obey ||R-S||<1, then their vector-space ranks are equal. Indeed S restricted
to range(R) is injective, because Sx=0 and Rx=x would imply
||x||<=||R-S|| ||x||. Reverse R,S for the other rank inequality.

Product-dimension bound. If C,D are quasiorthogonal unital subalgebras of M_N,
meaning tau(cd)=tau(c)tau(d) for c in C,d in D, then

    dim(C) dim(D)<=N^2.                                   (7)

This is established prior art: Weiner, *On quasi-orthogonal systems of matrix
algebras*, arXiv:1002.0017v1, section 2.3, equation (15), gives this same
product-orthogonality proof as a necessary dimension condition. It is written
out here to make its use and conventions explicit, not claimed as new.

To prove it, choose tau-Hilbert-Schmidt orthonormal bases {c_i},{d_j}. Cyclicity
of the trace and algebra closure give

    tau((c_i d_j)* c_k d_l)
       =tau(c_i* c_k d_l d_j*)
       =tau(c_i* c_k) tau(d_l d_j*)
       =delta_(i,k)delta_(j,l).

Thus all dim(C)dim(D) products are orthonormal inside the N^2-dimensional
matrix space. No assumption that C,D commute as operators is made in (7).

Now suppose F,G commute and put epsilon=max(||F-E_A||,||G-E_B||). If epsilon>=1,
(2) is automatic. Otherwise rank stability forces

    dim(range F)=dim(range G)=d^2.

Because F,G are trace expectations, they are orthogonal projections in
Hilbert-Schmidt space. Their commuting product FG is the expectation onto
the intersection of their algebras. If 2epsilon+delta_d<1, then (6) and
contractivity give

    ||FG-E_0||<=||FG-E_AE_B||+||E_AE_B-E_0||
               <=2epsilon+delta_d<1.

Rank stability now forces rank(FG)=rank(E_0)=1. Hence FG=E_0 and the two
repaired algebras are quasiorthogonal. But (7) would then require

    d^4<=N^2=d^2(d-1)^2,

which is false. Therefore 2epsilon+delta_d>=1, proving (2). QED.

## 4b. Direct obstruction in Kadison--Kastler algebra distance

For unital subalgebras C,D of M_N let

    h=max(d_KK(A,C),d_KK(B,D)),

where d_KK is the Hausdorff distance between operator-norm unit balls. Suppose
their trace expectations F,G commute and h<(1-delta_d)/4. In particular
2h<1. For a in the unit ball of A, there are c in the unit ball of C with
||a-c|| arbitrarily close to h. Since F is contractive and F(c)=c,

    ||F(a)-a||<=2h.

After scaling, this implies that F restricted to A is injective. Conversely,
E_A restricted to C is injective by the other half of the Hausdorff distance.
Therefore dim(C)=dim(A)=d^2. The same argument gives dim(D)=d^2. This is only
a linear-space dimension argument; no C*-type-rigidity theorem is imported.

If C intersection D were larger than the scalars, it would contain a traceless
x with ||x||=1. Closeness of C to A and of D to B then implies

    ||x-E_A(x)||<=2h, ||x-E_B(x)||<=2h,
    ||x-E_A E_B(x)||<=4h.

But E_0(x)=0 and (6) gives ||E_A E_B(x)||<=delta_d. Thus

    1<=4h+delta_d<1,

a contradiction. The intersection is scalar. Commutation of F,G now forces
FG=E_0, so C,D are quasiorthogonal. Their dimensions violate (7), exactly as
in section 4. This proves (2b). If delta_d>=1 the bound is vacuous; for all
d>=4 used here it is positive. QED.

## 5. Resource and extension boundaries

The algebras and U are supplied by the explicit Weyl/Fourier rule. No unknown
basis, channel, or apparatus is learned. N=d(d-1); an explicit sparse block
matrix U has O(m^2 d)=O(d^3) nonzero coefficients, while the structured rule
has O(log d) discrete metadata plus roots of unity. Exact phases are algebraic
data, not fixed-precision floating numbers. Input/output size, Fourier work,
precision, mixed-environment initialization, trace/discard, gate synthesis,
readout, reset, physical noise and energy remain charged; no physical cost or
speed advantage has been established.

At each fixed d there is no limiting zero-defect counterexample. The sequence
changes dimensions and lets minimal matrix projection weights go to zero.
The output algebras remain in the same M_N for each instance; allowing a
different ambient algebra is a different contract.

The dimension budget (7) and Weyl twirling are established machinery. Whether
this particular uniform-rounding counterexample and its explicit constants
are historically new requires primary priority review. The proof imports no
large algebra-stability theorem and makes no claim that Ranard-Walter-Witteveen's
robust-intersection theorem is incorrect. Its intended simultaneous-repair
question must be compared with the exact uniformity and ambient contract here.
Equation (2b) addresses algebra closeness directly in the standard
Kadison--Kastler metric; (2) additionally controls expectation-map closeness.
