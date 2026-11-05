# A uniform ordered-area obstruction to real multiplicity-free compression

5 November 2026. This theorem closes the natural real spin-fusion hierarchy described in hierarchy_closure_audit.md. It is a restricted physical converse with explicit finite-angle quantifiers, not an unrestricted receiver-memory lower bound.

## 1. Exact scope in terms of physical instrument effects

At a prefix of n>=3 emitted carriers, completely refine the receiver instrument into Kraus maps K_x. Set A_x=sqrt(K_x^dagger K_x). The theorem assumes:

1. A_x commutes with every collective spin J_a=sum_i sigma_i^a.
2. A_x is invariant under physical spin time reversal Theta=(i sigma_y)^(tensor n) K.
3. In the Schur decomposition H_n=direct_sum_j (V_j tensor M_j), write A_x=direct_sum_j(I_(V_j) tensor a_(x,j)). Each positive a_(x,j) has rank at most one.

Completeness is sum_x A_x^2=I. All classical records are allowed. Real projective Clebsch-Gordan/fusion trees retaining a payload qubit times a spin-J register satisfy these assumptions: each branch contains at most one copy of either total spin J-1/2 or J+1/2. More generally, real intertwining Kraus maps with scalar branch labels and such output multiplicities satisfy them.

A generic covariant CPTP map is NOT automatically covered. Kraus tensor operators can exchange spin with discarded ancillas; their effects need not satisfy these hypotheses. An independently initialized asymmetric frame can likewise make the composed prefix effects non-invariant even when every later gate is covariant. Thus a real payload-qubit-times-spin-register description is covered only when its composed effects satisfy the three stated hypotheses. Complex multiplicity control, a branch retaining multiplicity rank two or larger, and non-invariant effects also lie outside the theorem.

## 2. A chirality component annihilated by every covered effect

Define the Hermitian vector and scalar

    Y_a=sum_(i<j) (sigma_i cross sigma_j)_a,
    C=J dot Y=sum_(i<j<k) sigma_i dot (sigma_j cross sigma_k).

The local repeated-site terms in J dot Y cancel, and the three contributions from each distinct triple have signs +,-,+, giving the displayed scalar. C is invariant under collective rotations and odd under time reversal. In a real Schur basis, its multiplicity matrix in each spin sector is Hermitian and purely imaginary antisymmetric. A real rank-one multiplicity effect therefore obeys

    A_x C A_x=0.

Let J^2=sum_a J_a^2, and take its inverse on positive spin sectors. C vanishes on spin zero. The within-spin part of the vector Y is exactly

    Y_parallel,a = J_a (J^2)^+ C.

This follows from the uniqueness of a spin-j vector operator within one irrep: every within-spin vector is J_a tensored with a multiplicity matrix. Contracting with J determines that matrix. The within-spin/off-spin decomposition is orthogonal in tracial Hilbert-Schmidt norm.

The unital, trace-preserving, self-adjoint Lüders map

    Lambda(X)=sum_x A_x X A_x

consequently annihilates every Y_parallel,a. It is a Hilbert-Schmidt contraction, so I-Lambda is positive as an operator on Hilbert-Schmidt space. The same statements hold after tensoring the identity map on the actual source.

Put tau(X)=2^(-n)Tr X and

    K_n = sum_a ||Y_parallel,a||_(2,tau)^2
        = tau[C^2 (J^2)^+].

## 3. Exact moments and a growing-prefix lower bound

Pauli orthogonality gives

    tau(C^2)=n(n-1)(n-2).

For the second weighted moment, J^2=3n I+2sum_(i<j) sigma_i dot sigma_j. The overlap count is

    sum_(i<j) tau[C^2 (sigma_i dot sigma_j)]
       = -18 binom(n,3)+24 binom(n,4)
       = n(n-1)(n-2)(n-6).

The -18 term comes from the three pairs inside one chirality triple, each contributing -6. Two distinct triples contribute only when they share two sites. For each ordered set of four sites, the six unordered triple-pair signs are +,-,+,+,-,+; including both orders and the Pauli trace gives +24. Therefore

    tau(C^2 J^2)=n(n-1)(n-2)(5n-12).

Cauchy-Schwarz, using that C commutes with J^2, yields the exact bound

    K_n >= n(n-1)(n-2)/(5n-12).                 (K)

In particular the leading Yangian instrument energy is at least

    E4 = [1/(16*2^n)] sum_(x,a)||[Y_a,A_x]||_2^2
       >= K_n/8
       >= n(n-1)(n-2)/[8(5n-12)] ~ n^2/40.    (LEADING)

To derive this for nonprojective effects, expand the commutator sum as
(1/8)sum_a <Y_a,(I-Lambda)Y_a>. The map preserves spin blocks and kills Y_parallel, while I-Lambda is positive on the remaining orthogonal subspace. No projectivity is needed.

The first inequality is saturated by the three-site rank-two/rank-six cut: K_3=2 and E4=1/4. Thus that cut preserves all area except the unavoidable within-spin chirality component for this class.

## 4. Exact finite-angle physical witness

The previous coefficient bound is not extrapolated to a growing n. Instead use the exact source-Pauli expansion supplied by the physical collision rule.

Let c=cos(theta), s=sin(theta), and W_a=U_(S,n)...U_(S,1) sigma_S^a U_(S,1)^dagger...U_(S,n)^dagger. Its source-traceless term of bath Pauli weight two is

    (W_a^Q)_(weight2)=c^(2n-2)s^2 sum_(i<j) T_(ij,a),
    T_(ij,a)=sigma_j^a (sigma_S dot sigma_i)
             -sigma_S^a (sigma_i dot sigma_j).

Under reversal of the bath order, the odd part of sum T is

    -1/2 (sigma_S cross Y)_a.

Define the three kernel witnesses

    F_a=(sigma_S cross Y_parallel)_a.

They have normalized Gram matrix

    <F_a,F_b>_(tau_S tensor tau)=(2K_n/3) delta_ab.

They are reversal odd, and their bath part is time-reversal even. The reversal-even weight-two term is orthogonal to them. Moreover <Y_a,Y_parallel,b> equals the Y_parallel Gram matrix because Y_parallel is an orthogonal projection of Y. Thus the exact weight-two projection onto span{F_a} is

    Pi_F[(W_a^Q)_(weight2)] = -1/2 c^(2n-2)s^2 F_a.

The bath time-reversal parity implies that F_a contains only even bath Pauli weights, and its bath trace is zero. Thus weights zero, one, three, five, ... cannot contaminate this overlap. Only even weights four and above remain.

The exact source-Q mass at bath weight k is

    q_(n,k)=binom(n,k)c^(4n-2k)2^k s^(2k).

Set

    T_even(n,theta)=sum_(even k>=4) q_(n,k).

Equivalently, with x=s^2 and r=1-x^2,

    T_even = [r^n+((1-x)(1-3x))^n]/2
             -(1-x)^(2n)-2n(n-1)(1-x)^(2n-2)x^2.

The nonnegative finite sum is preferable near cancellation points. Orthogonal projection and the triangle inequality give

    ||Pi_F W_a^Q||_2 >=
       [c^(2n-2)s^2 sqrt(K_n/6)-sqrt(T_even)]_+.

Because Lambda(F_a)=0 and I-Lambda is positive, the actual balanced source-Q norm lost by the instrument is at least the square of this expression. Using (K), every covered prefix instrument has the exact finite-angle lower bound

    d_n(theta) =
      [ c^(2n-2)s^2 sqrt(n(n-1)(n-2)/(6(5n-12)))
        -sqrt(T_even(n,theta)) ]_+^2.            (FINITE)

This is valid for every integer n>=3 and every 0<theta<pi/2. It may be vacuous in some parameter regions. No fixed-n Taylor remainder appears.

For clarity about the operational bridge, the balanced map of a completely refined Kraus instrument obeys V^dagger V=Lambda. Therefore its retained squared norms are <W,Lambda W>, including for nonprojective effects. Granting the actual source at the prefix can only help recovery. The source-granted Petz visibility is at most 1-d_n(theta). The accepted sharp recovery comparison then gives, for ANY later continuation of the receiver,

    epsilon >= (3/4)[1-sqrt(1-d_n(theta))].      (RECOVERY)

The proof uses inaccessible source information only for this converse relaxation; no source access is supplied to a constructed reader.

## 5. Uniform weak-angle consequence

Take n=floor(alpha/sin(theta)^2), with fixed alpha>0. Then

    d_n(theta) -> d(alpha),
    d(alpha)=exp(-2alpha)
      [ alpha/sqrt(30)
        -sqrt(cosh(2alpha)-1-2alpha^2) ]_+^2.

The bracket is positive for sufficiently small positive alpha. For alpha=0.1,

    d(alpha)=0.0000833039858474650...,
    liminf epsilon >= (3/4)[1-sqrt(1-d(alpha))]
                     =0.0000312396453031050... .

This nonzero constant applies whenever a covered prefix instrument occurs at that diffusive prefix. A real multiplicity-free fusion hierarchy has such an instrument at every prefix and therefore cannot approach perfect recovery in the weak-angle quartic-horizon regime. This conclusion does not rely on treating theta^4 E4_n as a uniform approximation.

For independent blocks with n sin(theta)^2 ->0, (FINITE) gives d_n of order n^2 theta^4, whereas unrestricted block acquisition is of order n theta^4. Thus growing such real multiplicity-free blocks cannot yield loss negligible compared with acquisition either.

## 6. Consequences for the hierarchy and charge measurements

The real gamma fusion family retains collective spin and some off-spin ordered-area coherence, but all its branch representations are multiplicity free. The chirality component is exactly erased. Its fourth-order losses are not summable; the finite-angle witness shows a physical error floor on a uniform growing prefix.

A fine real spectral resolution of open-chain conserved quantities into single multiplicity vectors has the same obstruction. Coarse spectral bins may retain several multiplicity vectors and therefore evade the theorem. A successful alternative must establish how many such coherent multiplicities survive, how much rank is removed, and how much of Y and higher ordered information is retained. Large magnetic-spin dimension or a distributional collective-spin central limit alone does not meet those requirements.

Complex multiplicity rotations can retain the time-reversal-odd scalar C and are not ruled out. The theorem also does not exclude arbitrary CPTP instruments. It narrows a concrete hierarchy rather than closing the unrestricted joint memory/processing problem.

## Verification and dependencies

The exact weight-two and q_(n,k) identities are the independently derived physical identities in joint_operational/clt_block_analysis.md. The chirality moments and the uniform projection/tail argument are derived here.

chirality_check.py verifies both exact moment polynomials for n=3,...,7. chirality_uniform_check.py checks the kernel, contamination bound, and actual finite-angle loss for a real multiplicity-free gauge-Schur/payload instrument at n=3,...,6 and theta=.03,.1,.3,.7. Maximum kernel residual was 7.05e-15; every finite-angle loss inequality passed, with minimum slack 5.39e-7; the largest contamination-minus-tail residual was 1.61e-17. These are checks of the proved identities, not an optimization result.
