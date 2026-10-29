# The source alphabet changes the optimal detector-noise design

Root construction, 29 October 2026 Australia/Brisbane. Status: authored theorem and exact certificates; independent review pending. This optimizes the sufficient complete-instrument bound in `COMPLETE_RECORD_CONVERSION.md`, not the actual channel error.

## 1. The operation-specific problem

Fix a feasible causal memory path S_t, hence real skew increments Gamma_t. The noise-path theorem allows real symmetric N_t satisfying `N_t+i Gamma_t>=0`. For source signs z in {+1,-1}^n, the complete-record conversion uses

    D=max_z z^T N z, N=sum_t N_t,
    epsilon<=sqrt(1-exp(-D)).

The monotonicity of this bound makes minimizing D the relevant sufficient-bound objective. The exact fixed-path problem is

    D_* = min D
    subject to N_t real symmetric, N_t+i Gamma_t>=0,
               D>=z^T(sum_t N_t)z for every sign z.             (1)

This is a finite semidefinite program with exponentially many sign constraints. No efficient exact solution for arbitrary n is asserted. Define

    C_n=conv{zz^T : z in {+1,-1}^n},
    f_Gamma(X)=Tr|i X^(1/2) Gamma X^(1/2)| for X>=0.

**Theorem.**

    D_* = max_(X in C_n) sum_t f_(Gamma_t)(X).                  (2)

One common adversarial correlation matrix selects the noise directions relevant to the finite source alphabet across all batches. Independent mean-square minimizations do not capture this objective.

## 2. Proof and attainment

For positive definite X, the weighted noise-cone calculation gives

    inf_(N=N^T, N+i Gamma>=0) Tr(XN)=f_Gamma(X).                (3)

It remains true as an infimum for singular X. The lower bound follows by congruence with X^(1/2) and the two-dimensional uncertainty trace inequality. For the upper bound, use an optimizer N_delta for X+delta I. Since N_delta is real positive semidefinite,

    Tr(XN_delta)<=Tr[(X+delta I)N_delta]=f_Gamma(X+delta I).

Continuity as delta decreases to zero proves (3). The isolated singular-weight problem need not attain its infimum; no physical infinite-gain construction is inferred from this limiting step.

Assign nonnegative Lagrange weights p_z to (1)'s sign constraints. Minimization in D forces sum_z p_z=1. The coefficient of every N_t is the same matrix X=sum_z p_z zz^T in C_n. The remaining infimum equals sum_t f_(Gamma_t)(X) by (3). Strict primal feasibility follows by choosing every N_t=cI with c greater than the corresponding skew norm, then D strictly above every sign form. Finite-dimensional conic strong duality gives (2).

Both optima are attained. Uniform averaging of the sign constraints gives Tr N<=D. Since each N_t is positive semidefinite on real vectors, an objective sublevel bounds every N_t; closedness gives compactness of a minimizing sequence. C_n is compact and f is continuous, so its maximum is attained. Finite attainment does not make optimization computationally easy.

## 3. Upper relaxations and exact lower certificates

Replacing C_n by the elliptope `X>=0, diag X=1` enlarges the dual feasible set. Equivalently, a sufficient primal design requires

    Diag(lambda)-sum_t N_t>=0

and minimizes sum_i lambda_i. This can overestimate (1); the elliptope is not silently identified with the sign polytope. Numerical feasibility requires enclosure or exact verification before it is a certificate.

For a lower certificate choose an explicit distribution over signs, hence X in C_n. For each t choose real skew Y_t such that Z_t=X+iY_t>=0. Then

    0<=Tr[Z_t(N_t+iGamma_t)]
      =Tr(XN_t)-Tr(Y_t Gamma_t),

and hence

    D>=sum_t Tr(Y_t Gamma_t).                                 (4)

Together with an explicit feasible N_t and a maximizing sign, this certifies a global optimum for the fixed path without numerical square roots or an SDP solver.

## 4. Exact reversal of design choice

Use the four-source three-batch example from the path theorem:

    K1=(3/2)J1+J2, K2=J1+(3/2)J2, K3=0.

J1,J2 are disjoint standard skew 2x2 blocks and one mode is retained. The fixed-plane path has Gamma coefficients `(0,-1)`, `(0,-1/2)`, `(0,3/2)`. Per-cut greedy retention has `(0,-1)`, `(-1,1)`, `(1,0)`.

Before rotation, fixed-plane N=diag(0,0,3,3) has sign maximum 6; X=I (uniform signs) gives the matching lower bound. Thus D_*=6. The greedy path similarly has D_*=8, attained by N=2I.

Apply the same orthogonal source-coordinate matrix O=H/2, with H rows

    (1,1,1,1), (1,-1,1,-1),
    (1,1,-1,-1), (1,-1,-1,1).

This defines a different supplied coupling family; it is not a free change of qubit basis. Put J=O^T J2 O and P=O^T diag(0,0,1,1) O. Then J^2=-P and Tr P=2. The fixed-plane path has Gamma_t=gamma_t J with gamma=(-1,-1/2,3/2), and feasible N_t=|gamma_t|P.

Choose X=2P. It is in C_4: the equal mixture of the outer products of the third and fourth sign rows of H. Choose

    Y_t=-2 sign(gamma_t)J,
    Z_t=2(P-i sign(gamma_t)J).

On range(P), Z_t has eigenvalues 0 and 4; on its complement it vanishes. Thus it is positive semidefinite. Equation (4) gives

    D>=sum_t 4|gamma_t|=12.

The primal N=3P has sign maximum 12, attained by either specified sign row. Therefore **D_*=12 for the rotated fixed-plane path even after optimizing every allowed N_t**. Covariance redistribution cannot improve this path's sufficient complete-error allowance below that value.

For the rotated greedy path, X=I gives lower bound 8 and N=2I attains sign maximum 8. Thus **D_*=8**. The measurement covariance-trace ordering (6 versus 8) and the optimal complete-bound ordering (12 versus 8) reverse.

These are fixed-path optima, not the optimum over all one-mode paths. They optimize the specified sufficient error bound; a direct channel calculation may improve either allowance or its ranking. The associated exact rational code checks primal cones, dual cones, sign-polytope membership and matching values without Fock truncation.

## 5. Reach and ancestry

The path theorem supplies a receiver from finite matrices. The complete-record conversion supplies a source-correction allowance. Equation (2) joins them while keeping the source's finite alphabet rather than substituting a generic covariance-trace objective. Exact upper and lower certificates can guide a receiver decision before an expensive bosonic simulation.

Conic duality, the sign-correlation polytope and uncertainty trace bounds are established tools. The combined construction is new within this research tranche; historical priority is unestablished. No calibration, supply fidelity, storage lifetime or loss capability follows from this optimization alone.
