# Exact arbitrary-alphabet information-budget synthesis

29 October 2026. Constructed here from the accepted N1038/free-Umegaki
mechanism, standard covariance identities, Schur complements and SDP duality.
No priority or physical advantage is asserted. The proposed generalization
is proved below; its exact-program specialization is the scientific object,
not a finite numerical instance.

## 1. Input, output and the information being budgeted

Let n>=2 and m>=2. L is an explicit strictly positive rational n-by-n
column-stochastic matrix, invertible on the zero-sum tangent space (equivalently
invertible). The unknown release K is m-by-n, column stochastic, with entries
at least a supplied kappa in (0,1/m). Fix a rational budget 0<c<1 and arbitrary
rational linear utility/cost C:K. The entire input is finite channel matrices,
the utility and numerical tolerances. No state sampler, side-information
dimension bound, measured response, trained model or microscopic input
actuator is required to SOLVE this design problem. Applying the resulting
K still requires its owner to have the classical input symbol; access only
to a preexisting L record is a different, more restricted problem.

Write J_A(rho,sigma)=D((A x id)rho||(A x id)sigma)-D(rho_R||sigma_R)
for classical-quantum pairs, using only defined finite differences. The
design constraint is

    J_K(rho,sigma) <= c J_L(rho,sigma)                 (1)

for every finite complex reference and every pair at the shared classical
input boundary. The accepted free-Umegaki theorem, whose whole governing
proof was read, identifies (1) with its equal-reference version and with

    F_K(Q,u) <= c F_L(Q,u),
    F_A=sum_y <sum_i A_yi u_i, (sum_i A_yi Q_i)^-1 sum_i A_yi u_i>,
    Q_i>=0, sum_i Q_i=I, sum_i u_i=0.                  (2)

Positive Q_i suffice by closure; strict positive channel entries keep every
output inverse bounded on the effect domain. This free/entropy identification
is inherited capital, not a new theorem claimed here. Taking
sigma_XR=rho_X x rho_R gives the useful corollary
I(R:K(X))<=c I(R:L(X)) for every classical-quantum source. This is NOT
differential privacy, complete guessing order, Blackwell simulation, a
capacity formula or a guarantee for every future loss.

## 2. Arbitrary n,m comparison, with no reference search

Put p=n-1,q=m-1, B_n=[I_p;-1^T], P_n=[I_p,0], and P_m=[I_q,0]. Define

    R=P_n L^-1, r_y=column_y(R),
    e_i=standard basis_i of R^p (i<n), e_n=0,
    H_i=sum_y L_yi r_y r_y^T-e_i e_i^T,
    D=P_m K B_n, x_i=P_m K[:,i],
    T_i=diag(x_i)-x_i x_i^T, S_i=D H_i D^T.

Each H_i is positive definite: it is the covariance of the r_y under the
strictly positive weights L_yi, whose mean is e_i; their affine span is R^p.
Each T_i is positive definite since the whole K column has positive entries.

For W_1,...,W_s>0 summing to I, direct ordered block multiplication gives

    [B_s^T diag(W_y^-1)B_s]^-1 = diag(W_1,...,W_(s-1))-w w^*,
    w=(W_1,...,W_(s-1))^T.                            (3)

No commuting-effects assumption is used. Consequently the denominator
inverse, on the input tangent coordinates, is

    H_L=J_L^-1=sum_i (H_i+e_i e_i^T) x Q_i - q_in q_in^*,
    q_in=(Q_1,...,Q_(n-1))^T.

Here x means tensor product only in this display. For K, let M_K be the
positive output-coordinate inverse pencil in (3). Then J_K=D^T M_K D.
The contraction equivalence

    J_K<=cJ_L  iff  D H_L D^T<=c M_K^-1               (4)

holds even for singular/rectangular D, by comparing Z^*Z and ZZ^* for
Z=M_K^(1/2) D J_L^-1/2. No inverse of K is required.

Let X=sum_i x_i x Q_i and V=sum_i x_i x_i^T x Q_i-XX^*>=0.
Expanding (4) gives the dimension-free identity

    cM_K^-1-DH_LD^T = sum_i(cT_i-S_i) x Q_i+(c-1)V.  (5)

For t=1-c>0 and any scalar z in R^q this is

    t(X-zI)(X-zI)^* + sum_i B_i(c,z) x Q_i,
    B_i=cT_i-S_i-t(z-x_i)(z-x_i)^T.                  (6)

Thus all B_i>=0 suffice in every finite complex reference dimension.

They are also necessary. Set A_i=c diag(x_i)-S_i-x_i x_i^T. For a normalized
q-component reference vector w, put U=[w_1 ... w_q], E_i=U^*Q_iU,
G=sum E_i, d=sum E_i x_i. Projection onto ran U gives
||X^*w||^2>=d^*G^+d, with equality attained in dimension rank G<=q using
U=G^1/2 and Q_i=G^-1/2 E_i G^-1/2 on its support. Hence the exact universal
minimum of (5) is the finite convex program

    min sum_i tr(A_i E_i)+t s,
    E_i>=0, sum_i tr(E_i)=1,
    [[G,d],[d^*,s]]>=0,
    G=sum_i E_i, d=sum_i E_i x_i.                    (7)

Conjugation averaging leaves its objective unchanged, so real symmetric
E_i suffice. Taking E_i=I/(nq) and s strictly large proves Slater. The
objective is bounded below. Its attained dual is

    max mu such that B_i(c,z)>=mu I for all i.        (8)

To check the sign: a PSD multiplier [[Z,b],[b^T,t]] gives constraints
A_i-mu I-Z-(b x_i^T+x_i b^T)>=0; the strongest Z is bb^T/t, and b=-tz
produces exactly (6). This is the same argument as N1038 with dimensions
left symbolic, not an invocation of an unbounded hierarchy. Universal
positivity is equivalent to a common z. The reference witness rank bound
is q=m-1 for the free problem; faithful Umegaki realization may need the
extra vacuum dimension m. No uniform conditioning of that realization is
claimed.

For c>=1, the covariance term in (5) is nonnegative, so the complete criterion
is simply cT_i-S_i>=0 for all i. Vertex effects prove necessity. At c=0,
the criterion is that K have identical columns. These endpoints are not
needed by the executed subunit design.

## 3. The exact joint release-design lift

The apparent quadratic dependence of (6) on K is benign. Set a=t z.
Rearrangement gives

    B_i = c diag(x_i)-D H_i D^T-c x_i x_i^T
                      -(a-tx_i)(a-tx_i)^T/t.          (9)

Because H_i>0,c>0,t>0, B_i>=0 is equivalent to the affine matrix inequality

        [ c diag(x_i)    D        c x_i    a-t x_i ]
    M_i=[ D^T           H_i^-1   0        0       ] >=0.  (10)
        [ c x_i^T       0        c        0       ]
        [ (a-tx_i)^T    0        0        t       ]

There are n blocks, each of order (m-1)+(n-1)+2=m+n. Every entry of
M_i is AFFINE in the unknown K and a at the fixed supplied c. The exact
set of releases satisfying (1) and K_yi>=kappa is therefore a spectrahedral
shadow. Maximizing any linear utility, or minimizing any linear distortion,
is one SDP with mn+m-1 scalar variables, n PSD blocks of order m+n and
elementary stochasticity constraints. This is a general alphabet-size
operation, not a fixed-dimensional optimization fixture.

There is no lost boundary point from constraining |a_j|<=2. Indeed (6)
implies t(z_j-x_ij)^2<=c x_ij(1-x_ij)<=c/4. Thus
|a_j|<=t+sqrt(ct)/2<=5/4. The box two is a harmless rational convenience.
The feasible set is compact after this box is added, and an optimum exists.

The constant release K0=(1/m)1 1^T, a0=t(1/m)1 gives strict feasibility:
D=0 and (9)=c[diag(x0)-x0x0^T]>0. It also strictly satisfies the entry
floor. All lower blocks in (10) are positive definite. Hence ordinary
weak-SDP algorithms apply with an explicit rational Slater point. This does
not grant a unit-cost real SDP oracle: H_i inversion, rational sizes,
conditioning, solver work and certification are charged.

For rational input, H_i and H_i^-1 have polynomial bit length by determinant
bounds. A quantitative strict-feasibility radius with log inverse polynomial
in input length follows by exact LDL/Schur factorization of the constant
release. The same is true for the finite variable box. Standard weak-SDP
optimization therefore supplies additive-utility accuracy in time polynomial
in n,m,input bit length and log(1/epsilon), with its usual exact-input
arithmetic model. This is not a claim that an arbitrary floating solver has
that uniform running time. An exact optimum need not be rational.

If a numerical optimum is blended by a small theta with the strict constant
release, its matrix slack is at least theta times that of the explicit
baseline, while utility changes by at most theta times the cost range.
Rational rounding can then preserve every constraint. The actual consumer
must check the rational B_i and stochasticity, and must retain failure if
its proposed rounding does not pass. This is the route used in the executed
construction, not a claim that solver status proves the constraints.

## 4. A rational global-optimality receiver, without trusting solver duals

For any rational PSD multipliers Y_i of the blocks (10), define

    L(K,a)=C:K-sum_i tr(Y_i M_i(K,a))
          =r0+sum_yj R_yj K_yj+sum_h b_h a_h.

For every feasible release, C:K>=L(K,a). Minimize this affine expression
EXACTLY over the larger product domain consisting only of each stochastic
column with K_yj>=kappa and |a_h|<=2. It gives

    LB=r0+sum_j[kappa sum_y R_yj+(1-m kappa)min_y R_yj]
                         -2 sum_h |b_h|.             (11)

No stationarity equality, unbounded-center assumption, floating eigenvalue
claim or formally exact solver dual is needed. Each Y_i can be rounded and
made PSD by a checked rational diagonal shift; an actual rational LDL proves
that step. Equation (11) remains valid even for a poor dual proposal. The
feasible rational K supplies UB=C:K. Thus UB-LB is a fully checked global
utility gap, not an optimizer convergence assertion. The receiver is also
usable with an ordinary conic solver or an independently supplied proposal.

## 5. Ordinary alternatives and the exact consequence

The general free-Umegaki representation and inverse-action compression were
accepted before this work. N1038 already supplies the entire small-alphabet
covariance/common-center mechanism. Replacing its dimension two by q, and
then recognizing the joint Schur lift, is an exposed-source mathematical
extension; it is NOT evidence that the ordinary method was unable to find it.
Helton--Klep--McCullough's free convex Positivstellensatz and conventional
SDP/Schur machinery are strong general antecedents. A source-aware ordinary
method may use precisely this generalization or optimize the convex comparison
coefficient with a separation oracle; it should be allowed to match the answer.

A simpler established sufficient release is K=c P L+(1-c)r1^T, where P is
any stochastic postprocessor and r a probability vector. Joint convexity plus
DPI gives (1). Its best linear utility is an ordinary LP, which is admitted
with the same raw symbols, L, utility and budget. It is a sufficient subfamily,
not the strongest possible conventional algorithm. A numerical improvement
over that LP alone does not establish an advantage over all source-aware
convex or free-SOS methods.

The capability furnished by this theorem is an exact arbitrary-alphabet
DESIGN contract at this informative square-reference interface. It removes
reference-state search and a generic nonlinear channel search, but not by
discovering unknown data or improving every decision task. Strict entropy
order need not be a degrader order; earlier accepted counterexamples remain
in force. No extension to rectangular/rank-deficient reference channels,
coherent-input quantum channels, unknown channel calibration, cryptographic
security, or useful physical hardware follows. The exact prior-world priority
of this specialization is UNKNOWN. Its next-step value must be judged against
the informed source-aware convex program, not a deliberately weaker scalar
or fixed-reference search.

## 6. Exact deployment and the actual completed computational boundary

Once rational K is certified, applying it to an available classical symbol
needs no continuous sampler or quantum primitive. For each input i take the
least common denominator D_i of its column and integer multiplicities
N_yi=D_i K_yi. They are positive and sum to D_i. Generate k_i=ceil(log2 D_i)
private independent fair bits, reject their integer if it is >=D_i, and locate
the accepted ticket in the cumulative multiplicity intervals. Its exact law
is K[:,i]. Expected fair bits are k_i*2^k_i/D_i<2k_i, and lookup uses O(log m)
comparisons of O(log D_i)-bit integers. This is established rational categorical
sampling, not a newly invented random source. It does close the execution
interface of this finite release operation: no density or reference oracle
is left in the deployed mechanism.

The standalone receive_design.py reads only SOURCE.json and CERTIFICATE.json,
reconstructs the source H_i from exact rational L, and checks the FULL lifted
matrices (10), all rational duals and the global interval (11). Its lower
coefficients are rebuilt by finite differences of the literal full affine
matrix map, not by importing the producer's coefficient formulas. It also
checks the exact ordinary same-floor LP interval and integer ticket law.
The receiver is dimension-parameterized; the acquisition executable is the
one declared 12-input/7-output source, not an executed coverage claim for all
alphabet sizes. The arbitrary-alphabet algorithm is established analytically.

At c=1/2,kappa=1/1000 the actual returned release has certified globally
optimal cost in [0.0510189742602976,0.0510210624815883], gap<2.089e-6.
Twelve primal and twelve dual blocks have order 19. Exact ticket denominators
need at most 65 bits and mean fair bits at most 520/7 per released symbol.
No actual random draws, quantum reference states or physical data were used
to acquire this law. These finite arithmetic results do not prove the
arbitrary-alphabet theorem or a historical novelty claim by themselves.

The same-floor ordinary positive-replacer/postprocessor family has a
separately exact cost interval [0.0511789044091336,0.0511789138712978].
The relaxed family WITHOUT the entry floor achieves 0.050835275835275834
and is better than the returned floored mechanism. Both outcomes are retained;
neither is relabelled as an all-ordinary-method comparison. The initial code
incorrectly asserted an improvement over that relaxed value and stopped.
Its source, proposal and failure are preserved in development/. The same
input was corrected; no new source, floor, budget or utility case was tuned.
The exact first-attempt runtime was not serialized. Corrected-run times
therefore do not constitute a complete two-attempt wall-clock cost.

Finally, the information guarantee compares two alternative observations.
It does not bound the extra leakage if Y and a correlated L record are BOTH
published. The actual utility prior is used only in the linear objective;
the information constraint still holds for every input distribution and
finite quantum reference. Repeated adaptive disclosure, raw-input access,
calibration and cryptographic task semantics cannot be silently supplied
by this one-release theorem.

In particular a strict factor c does NOT automatically hold for a correlated
block of many uses. Even K=(1/2)L+(1/2)uniform, L=BSC(1/4), satisfies the
single-use factor 1/2, while repetition of the same hidden bit makes the
information in both independent-output blocks tend to log 2. Their ratio
tends to one. Complete preorder tensorization against a COORDINATEWISE
flagged-erasure comparator is a different valid object; it is not a global
block erasure with factor c. Root independently supplied this ordinary
repetition guard; no multi-release guarantee is claimed here.
