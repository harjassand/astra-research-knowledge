# Recursive positive fusion: exact closure calculation and obstruction

5 November 2026. This is the complete follow-up attempt to turn the positive three-carrier cut into a recursive representation. Collective spin closes exactly. The ordered-area vector closes under real fusion in a one-parameter family, but the full physical Lax/channel does not close as a unitary Yangian evaluation module. The natural real multiplicity-free hierarchy has a uniform recovery obstruction; complex or higher-multiplicity alternatives remain outside that conclusion.

## 1. The two compressed representations

Use Pauli-normalized generators

    J_a=sum_(i=1)^3 sigma_i^a,
    Y_a=sum_(i<j) (sigma_i cross sigma_j)_a.

Let P be the rank-two projector in positive_block_reader.md, and Q=I-P. The P doublet is

    |p,+> = sqrt(2/3)|010>-(|001>+|100>)/sqrt(6),
    |p,-> = (|011>+|110>)/sqrt(6)-sqrt(2/3)|101>.

In this basis,

    P J_a P = sigma_a,     P Y_a P=0.                       (1)

The Q space consists of the symmetric spin-three-halves quartet and the outer-site-singlet doublet

    |q,+>=(|001>-|100>)/sqrt(2),
    |q,->=(|011>-|110>)/sqrt(2).

Identify this quartet/doublet with the usual coupled basis of a spin-one register A and a spin-one-half register B. There is a real SU(2) intertwiner V from A tensor B onto Q. Let J_A=2S_A and J_B=sigma_B. Direct exact contraction gives

    V^dagger J V = J_A+J_B,
    V^dagger Y V = (2/sqrt(3))(J_A cross J_B).              (2)

Thus the proposed renormalization parameter is real and definite: gamma=2/sqrt(3), not the ordinary coproduct value one. This calculation is exact on all three vector components.

Compression also has an exact Schwarz defect:

    sum_a P Y_a Q Y_a P = 4 I_P,
    sum_a Q Y_a P Y_a Q = 4 Pi_(Q,spin1/2).                (3)

Both traces are eight. The missing terms are not a change of basis. They are the discarded transitions between the two recorded branches.

## 2. Full Lax closure fails, including on the rank-two branch

Let

    M_3(u)=(uI+iP_(S,3))(uI+iP_(S,2))(uI+iP_(S,1)).

Compress its quantum-space legs to the P doublet. The exact result is

    M_P(u)=alpha(u)I+beta(u)P_(S,eff),
    alpha(u)=(6u^3+6iu^2+3u-i)/6,
    beta(u)=i(6u^2+6iu+5)/6.

For a spin-half Yangian evaluation Lax operator, up to a scalar factor, the ratio i alpha/beta must be an affine evaluation parameter u-a. Here it is instead

    i alpha/beta = u-(2u+i)/(6u^2+6iu+5).                  (4)

It is not an affine shift. Retaining only the first two generator levels hides this failure.

There is also a direct RTT check using R(u-v)=(u-v)I+iP on the two auxiliary spaces. For the component with indices (i,j,k,l)=(0,1,1,0), at u=0,v=1, the full monodromy has zero defect. The compressed P monodromy has defect

    diag(-4/9+i/6, 4/9-i/6),

with squared Hilbert-Schmidt norm 73/162. The compressed Q monodromy has squared defect norm 67/162 in the same component. These exact nonzero polynomial identities rule out ordinary rational RTT closure of either compressed family. The spectral check at u=0 is an algebraic polynomial test, not a use of the excluded full-SWAP endpoint as an emitter operation.

### The physical branch is a noisy channel, not just P M P

The emitter input bath is maximally mixed. If x is the measured outgoing branch, its conditional channel contains all unobserved incoming sectors y:

    N_x(rho)= [1/rank(P_x)] sum_y
      U_(x<-y) (rho tensor I_y) U_(x<-y)^dagger,
    U_(x<-y)=(I_S tensor V_x^dagger) U_3 (I_S tensor V_y).

One cannot replace this expression by U_(x<-x) alone. Postselection of an outgoing branch does not prepare that representation before the fixed emitter collisions.

This distinction is exact at every physical finite u=cot(theta)>0. The conditional P-branch channel from the logical qubit to S tensor P has Choi rank eight, the maximum possible, whereas a unitary collision with an independently tracial two-dimensional gauge has Choi rank at most two.

An exact rank proof uses a time-reversed Bell reference. The unnormalized Choi-amplitude intertwiner splits into a spin-three-halves scalar i/(2sqrt(3)) and a spin-one-half multiplicity matrix

    K(u) = [[u^3+3iu^2/2+i/4,              sqrt(3)i/4],
            [sqrt(3)(6iu^2-6u+5i)/12,    u/2+i/4]].

Its determinant is

    det K(u)=(i/4)[(1-i)u^2+(1+i)u+1]
                   [(1-i)u^2+(1+i)u-i].

Both factors are nonzero for real u>0: their real parts are u^2+u+1 and u^2+u respectively. Hence the two spin-one-half multiplicity channels and the spin-three-halves channel are all present. Multiplying by the physical normalization does not change this rank. The extra spin-half amplitude starts at order theta^2, so its noise probability occurs at the same fourth-order scale as acquisition.

## 3. A genuine closed recursion exists at the J,Y level

The failure of full RTT does not prevent an exact recursion for the compressed first two generators. This gives a well-defined hierarchy candidate and makes its loss explicit.

Suppose the current branch is a spin-j gauge A times a payload qubit B, with

    J_current=J_A+sigma_B,
    Y_current=gamma (J_A cross sigma_B).

Append one new carrier E. The physical coproduct is

    J_new=J_A+sigma_B+sigma_E,
    Y_new=gamma(J_A cross sigma_B)
             +(J_A+sigma_B) cross sigma_E.                (5)

Couple A with E first. The two gauge branches have j_+=j+1/2 and j_-=j-1/2. The only freely rotatable multiplicity block is total spin j, which has two copies. Apply a real rotation of angle phi there, then measure only the branch and keep its entire payload-times-gauge quantum space. The branch maps are genuine projective CPTP instruments; earlier records may control phi.

For j>0 define

    a_+ = (2j gamma-1)/(2j+1),
    b_+ = sqrt(j/(j+1)) (gamma+2j+2)/(2j+1),
    a_- = ((2j+2)gamma+1)/(2j+1),
    b_- = sqrt((j+1)/j) (2j-gamma)/(2j+1).

The exact compressed branch generators have the same form, with

    gamma_+ = a_+ cos(phi)+b_+ sin(phi),
    gamma_- = a_- cos(phi)-b_- sin(phi).                   (6)

Relative real irrep phases permit sign changes of gamma without changing its norm. If j_-=0, the cross product vanishes and gamma_- is irrelevant. At j=0 the unique next branch has j=1/2 and |gamma|=1 after a basis convention.

At the tracial baseline the branch probabilities are

    p_+=(j+1)/(2j+1),       p_-=j/(2j+1).                  (7)

For the initial j=1/2,gamma=1 state, phi=pi/2 gives the three-carrier cut: the smaller branch has j=0 and the larger branch has j=1,gamma=2/sqrt(3).

The recursion follows from real Clebsch-Gordan intertwiners and Wigner-Eckart. A real, time-reversal-even vector on a multiplicity-free pair of irreps j+1/2 and j-1/2 has only the imaginary off-diagonal reduced matrix element, hence is proportional to J_A cross sigma_B. This is why a scalar gamma closes at this level. Complex rotations introduce additional diagonal and off-diagonal reduced components and do not obey the one-parameter recursion.

## 4. Exact leading-loss ledger for this recursive operation

In normalized trace on spin-j times a qubit,

    sum_a ||Y_current,a||_2^2=8 gamma^2 j(j+1).

Appending the fresh carrier in (5) adds 8j(j+1)+6 to this squared norm. The new term is orthogonal to the old one because its new-carrier factor is traceless. Therefore the added leading instrument energy is exactly

    Delta E4 = j(j+1)(gamma^2+1)+3/4
      -sum_(sign=+,-) p_sign gamma_sign^2 j_sign(j_sign+1). (8)

This is a true recursion of the fourth-order coefficient of the physical positive instrument, rather than a signed variational vector. Projective histories give nested orthogonal physical subspaces, so the losses add with their tracial branch probabilities.

The retained expression in (8) is a quadratic form in (cos(phi),sin(phi)). With t=j(j+1), its 2x2 matrix has

    trace T = t(gamma^2+1)+(3-gamma^2)/4,
    determinant D = gamma^2(t-3/4)(t+1/4).

For j>0, the locally minimum increment is obtained from the largest eigenvalue (T+sqrt(T^2-4D))/2. In particular

    Delta E4 >= gamma^2/4.                                (9)

The forced term has a direct meaning. Within total spin j, the two-copy multiplicity part of Y is an imaginary antisymmetric 2x2 matrix. Every real branch rotation leaves its off-diagonal nature unchanged, and measuring the branch discards it. For gamma=1 the locally optimal increment is exactly j^2. A large magnetic-spin gauge does not make that area loss small.

The numerical recursion in real_fusion_recursion.py checks these explicit formulas. A greedy policy begins with E4_3=1/4, then E4_4=1.171578..., E4_5=2.737862..., and E4_15=57.180273.... These values are diagnostics of that policy; the stronger obstruction below is independent of the policy and includes nonmyopic real choices.

## 5. The cumulative loss cannot be made summable in this real hierarchy

The complete prefix effects of the recursive real instrument are SU(2)-invariant, time-reversal-invariant, and rank at most one on every spin multiplicity space. The theorem in chirality_uniform_obstruction.md therefore applies.

Its scalar witness is C=J dot Y, the ordered scalar chirality. Every covered effect satisfies A_x C A_x=0. The within-spin part Y_parallel=J(J^2)^+C is consequently in the exact kernel of the physical Petz-back map. The trace identities prove

    E4_n >= n(n-1)(n-2)/[8(5n-12)] ~ n^2/40.             (10)

This is uniform in n as an algebraic coefficient statement. Crucially, the accompanying finite-angle proof does not extrapolate it perturbatively. It isolates the exact bath-weight-two coefficient and bounds possible contamination using only even bath weights four and above. At n=floor(0.1/sin(theta)^2), it gives the nonzero physical limit

    liminf_(theta->0) epsilon >= 0.0000312396453031050... .  (11)

This holds for arbitrary later continuation once such a prefix compression has occurred. It excludes the real multiplicity-free hierarchy as an arbitrary-accuracy reader at the quartic acquisition horizon. It does not exclude complex multiplicity rotations, higher retained multiplicity, or general CPTP instruments.

There is also an independent fixed-angle obstruction for any hierarchy beginning with the actual three-carrier cut. If x=sin(theta)^2, its exact source-granted visibility is

    g_3=1-x^2(7x^4-6x^3-6x^2+4x+6)/18.

Every later continuation has

    epsilon >= (3/4)(1-sqrt(g_3))
              =theta^4/8+O(theta^6).

Thus a fixed initial seed cannot attain arbitrary precision at fixed theta. Delaying or changing the initial compression is a different parameterized construction and requires a new guarantee.

## 6. Remaining possible alternatives and stopping point

The small gamma deformation is a genuine closed description of J,Y for real fusion, but it is not a closed physical Lax representation. The full compressed monodromy violates RTT, and the actual conditional channel contains additional noisy incoming-sector transitions. Their fourth-order loss cannot be omitted at the acquisition scale.

Allowing complex multiplicity rotations can preserve chirality and introduces a larger vector-operator family. Keeping multiple copies of a spin irrep also escapes the obstruction; this is exactly what the successful finite balanced n=6,n=7 projectors do. These alternatives require a new physical closure and a uniform cumulative-loss theorem. No such theorem, summable-loss hierarchy, or matching unrestricted joint boundary was obtained here.

Coarse measurements of real XXX conserved quantities remain possible only if their bins retain enough quantum multiplicity. Refining those measurements into individual real multiplicity vectors falls under the chirality obstruction. Rank/entropy control for genuinely coarse bins is still missing; a low Dirichlet eigenmode by itself does not supply it.

The requested hierarchy attempt therefore stops at the exact closure failure and the proved restricted physical obstruction, rather than claiming that a spin label or a formal renormalized Yangian parameter solves the recovery problem.

## Reproducible records

* compressed_yangian.py / compressed_yangian_verified.txt: exact embeddings, J/Y compression, projected monodromies, RTT defects, Schwarz defects.
* closure_additional_checks.py / closure_additional_checks_complete.txt: full RTT convention check and conditional Choi-rank proof, including the reduced amplitude determinant.
* real_fusion_recursion.py / real_fusion_exact.jsonl: exact finite-history scalar recursion; real_fusion_mc.jsonl is an optional large-history numerical diagnostic only.
* chirality_check.py / chirality_check.jsonl: exact moment-polynomial checks.
* chirality_uniform_check.py / chirality_uniform_checks.jsonl: finite-angle physical kernel, tail, and loss checks.

All Python paths are relative to each script's own directory; saved prior data have been preserved.
