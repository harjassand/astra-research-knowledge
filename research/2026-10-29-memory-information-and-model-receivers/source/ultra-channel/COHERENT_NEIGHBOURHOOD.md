# From exact support to an open coherent design region

This develops Theorem1 beyond a sparse comparison compiler. Its conclusion concerns a FULL open neighbourhood of quantum POVM pairs: the perturbed effects need not be positive mixtures of a common primitive or retain pair-supported coefficient rows. All untouched reference dimensions are covered by one quantitative coercivity argument.

## 1. General input contract

Let M_1,...,M_n be a strictly positive, linearly independent informationally complete POVM on C^d, with n=d^2. Supply rational bounds

    m I <= M_i <= M I,          0<m<=M.

Let P,Q be the pair-supported channels of the main theorem and E=P M, F=Q M. Suppose a connected graph G on the n primitive outcomes and delta>0 satisfy

    k_ij(t) >= delta/(1+t)  for every edge of G and every t>0.         (1)

Other pair kernels may be nonnegative and can be discarded in a lower bound. Supply a rational graph bound lambda>0 with

    L_G >= lambda (I-11^T/n).                                       (2)

Let r_y=sum_i P_yi (and similarly for Q); every output row is nonzero. Write m_y=m r_y. Take eta>0 with eta<=1 and eta<=min_y m_y/2. Let c be any rational upper bound on sqrt(n), and define

    K = sum_(all P and Q rows y)
         [4c/m + 2n/(m r_y) + 2/m^2],
    alpha = delta*m*lambda/(2M^2).                                  (3)

The conclusions below hold whenever K eta < alpha. These conservative constants are not claimed sharp.

## 2. Remove the reference gauge before perturbing

For a faithful baseline on A R and any Hermitian tangent, let S_i and X_i be the primitive reference blocks. Their sums are S=rho_R>0 and X=H_R. Put Lambda=J_S and L=Lambda^-1 X. Replace X_i by

    X_i^0 = X_i-J_{S_i}L,             sum_i X_i^0=0.                  (4)

Every trace-preserving measurement channel has the same reference marginal. Its SLD quadratic form therefore equals its quadratic form on the adjusted tangent plus <X,Lambda^-1 X>. To see this, expand each output inverse quadratic after subtracting J_(output baseline)L. The cross terms sum to 2 Tr[(sum output X^0)L]=0, and the gauge squares sum to <L,Lambda L>. Consequently the E-minus-F gap is UNCHANGED by (4). The same holds for every perturbed POVM below. No equal-reference restriction has been inserted into the original order; (4) is an exact gauge identity.

Whiten Lambda and set

    B_i=Lambda^-1/2 J_(S_i) Lambda^-1/2,
    x_i=Lambda^-1/2 X_i^0,           l_i=B_i^-1 x_i.

Then sum B_i=I, mI<=B_i<=MI, and sum x_i=0. Effect-order bounds imply the baseline and Jordan bounds by positivity of partial evaluation and of the anticommutator quadratic form. They do not depend on dimR.

## 3. Connected edge losses control all conditional directions

The unit pair loss obeys the exact parallel-sum identity

    L_11(B_i,B_j;x_i,x_j)
       = <l_i-l_j,(B_i^-1+B_j^-1)^-1(l_i-l_j)>
       >= (m/2)||l_i-l_j||^2.                                     (5)

By (1), the main theorem's spectral identity gives

    g_E-g_F >= (delta m/2) sum_edges ||l_i-l_j||^2.

Let lbar=n^-1 sum_i l_i and d_i=l_i-lbar. The constraint sum_i B_i l_i=0 and sum_i B_i=I imply sum_i B_i d_i=-lbar. Hence

    V=sum_i <l_i,B_i l_i>
       =sum_i <d_i,B_i d_i>-||lbar||^2
       <= M sum_i ||d_i||^2,
    S0=sum_i ||x_i||^2 <= M V <= M^2 sum_i ||d_i||^2.

Use (2) to conclude the reference-uniform COERCIVE gap

    g_E-g_F >= alpha S0.                                          (6)

Informational completeness means S0=0 only for the removed reference-gauge tangent. This is what permits a full coherent perturbation region. A binary primitive that leaves input coherences unseen would not supply this norm control.

## 4. Arbitrary coherent output perturbations

Since the M_i form a real basis of Hermitian input matrices, write every perturbed effect uniquely as

    E'_y=E_y+sum_i e_yi M_i,      F'_z=F_z+sum_i f_zi M_i,
    |e_yi|,|f_zi|<=eta.                                          (7)

Assume both perturbed collections sum to I. The coefficients in (7) may have either sign and every perturbed row may involve all primitive letters. Positive definiteness follows from the bounds below when the stated radius is used; it need not be separately guessed from numerical eigenvalues.

After the same reference whitening, an original output has B_y=sum_i P_yi B_i>=m_y I and x_y=sum_i P_yi x_i. Its perturbations satisfy

    ||Delta B_y||<=eta,
    ||x_y||<=r_y sqrt(S0),
    ||Delta x_y||<=sqrt(n) eta sqrt(S0).

The first bound uses sum_i B_i=I and -eta I<=sum_i e_yi B_i<=eta I; it is not an entrywise matrix estimate. Resolvent subtraction and expansion give

    |<x_y+Delta x_y,(B_y+Delta B_y)^-1(x_y+Delta x_y)>
        -<x_y,B_y^-1x_y>|
    <= {[2r_y sqrt(n) eta+n eta^2]/(m_y-eta)
         +r_y^2 eta/[m_y(m_y-eta)]} S0
    <= [4c/m+2n/(m r_y)+2/m^2] eta S0.                            (8)

All inverses are on the full Hermitian Hilbert space, independently of reference dimension. Summing (8) for BOTH channels and using (6) proves

    g_(E')-g_(F') >= (alpha-K eta) S0 >=0.                         (9)

The removed reference contribution cancels exactly even for E',F'. Thus (9) proves complete SLD order and, by accepted N675, unrestricted complete Umegaki order. This is a local design theorem, not a characterization of all ordered pairs or an algorithm to find their interior.

## 5. Executed full open qubit neighbourhood

For the main proof's path source, take

    n=4, m=1/8, M=3/8, delta=3/200, lambda=1/2, c=2.

The primitive bounds follow from (4±sqrt3)/16. The path graph satisfies (2); the exact three-dimensional restricted LDL certificate is recorded by compile_neighbourhood.py. Equation(7) of the main proof gives (1). Equations(3) give alpha=1/300. The script acquires the exact K from all23 actual rows and chooses

    eta=1/10,000,000,
    tau=1/70,000,000.

It verifies K eta<alpha/2 exactly. Here an arbitrary Hermitian perturbation T=x0 I+x dot sigma has primitive coefficients x0+4s_i dot x. Since ||T||=|x0|+||x||, every coefficient has magnitude at most4sqrt3||T||<7||T||. Therefore ANY trace-preserving pair of Hermitian effect lists within operator norm tau PER EFFECT of E,F lies in (7), is strictly positive, and has complete entropy order. This is a full open ball in the affine POVM-pair space, including arbitrary coherent perturbations, not merely an open set of graph parameters.

For the same fixed faithful binary states, a coefficient perturbation changes each signed measurement score by at most eta/8, because the primitive signed vector is (1,-1,0,0)/16. Optimal success changes by at most N_outputs eta/16. Thus throughout the entire ball,

    p_guess(F')-p_guess(E') >= 1/640-23 eta/16 >0.                 (10)

No postprocessing simulator exists anywhere in this open ball, since postprocessing cannot improve binary guessing. This remains a separation of channel orders, not a physical realization or a complementary-channel/quantum-capacity example.

An actual interior query is also constructed: add tau sigma_x to E's first effect and subtract it from the second; add tau sigma_z to F's first effect and subtract it from its second. Its unique primitive coefficient tables have negative entries, so the original nonnegative pair-row compiler cannot accept that representation. Nevertheless (9) qualifies its order. All candidate matrices, signed coefficients, exact success probabilities, and input/cost records are saved in NEIGHBOURHOOD.json. No reference was sampled or truncated.

## 6. Consequence and incumbent boundary

The new derivation is the conditional-coercivity bridge from an edge-local exact order to arbitrary coherent perturbations. It supplies a finite, directly checkable INNER DESIGN REGION of a reference-uniform order whose generic decision problem is accepted noncomputable. The proof does not infer a generic cutoff, a generic efficient algorithm, or that a measured device lies in the ball without qualification.

The underlying binary BEC/BSC comparison, inverse-pencilled spectral calculus, graph Poincare inequality, informationally complete tomography, and resolvent perturbation bounds are ordinary tools. They are all available to the matched comparator. Prior work already separates less-noisy/informational orders from simulation; neither the existence of that separation nor an entropy-monotone flagged interpolation should be promoted as a new operation. What the present construction adds at its proved scope is an explicit dimension-uniform coercive modulus and a full coherent interior synthesized from arbitrary connected support graphs. World priority and a consequential physical/design advantage remain UNKNOWN.
