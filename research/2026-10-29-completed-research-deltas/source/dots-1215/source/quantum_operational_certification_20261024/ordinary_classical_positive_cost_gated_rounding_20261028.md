# A cost-preserving gated rounding lemma for the classical decoder cube

28 October 2026. Author construction; independent receiving pending. This is a concrete reduced weighted-leverage algorithm, not a transfer to the full CPTP decoder cone.

## 1. Problem and the genuine positive-cost normalization

Consider binary decoder coordinates z in{0,1}^n, a nonnegative quadratic numerator

    N(z)=||a_0+sum_i a_i z_i||^2 = (1,z)^T A(1,z), A>=0,

and positive affine cost

    u(z)=m+sum_i w_i z_i,  m>0, w_i>=0.                    (1)

Any affine function positive on a binary cube has this form after independently flipping coordinates to its minimizing vertex. This changes the affine vector representation but preserves A>=0. The input matrices/vectors and positive cost bounds are known rational data. Supply a rational a>=max(1,||A||op); no unknown statistical parameter enters this optimization problem.

A basic moment relaxation uses

    M>=0, M_00=1, M_0i=M_ii=p_i, 0<=p_i<=1,
    F=Tr(A M)/(m+sum_i w_i p_i).                           (2)

Every deterministic binary vector gives a feasible rank-one moment matrix, so maximizing(2) upper-bounds the true ratio. It is an SDP after X=tM, t=1/(m+sum w_i p_i): X_00=t, X_0i=X_ii in[0,t], and m t+sum_i w_i X_ii=1. A strictly positive independent-Bernoulli moment point supplies a finite Slater witness; standard certified arithmetic can pay an additive objective tolerance. The rounding lemma below is stated for ANY supplied feasible M, so its statistical content does not assume an exact SDP optimum.

## 2. One dyadic group has a cost-preserving rounding

Take an index group I with p_i in(p/2,p], where p is a dyadic value in(0,1]. Let M_I be its principal submatrix. Define the correlation matrix

    Y=M_I/p+diag(1-p_i/p).

It is PSD and has diagonal one. Draw a centered real Gaussian with covariance Y and put s_i=sign(g_i). Then

    E ss^T=(2/pi)arcsin(Y)>=(2/pi)Y>=(2/(pi p))M_I.       (3)

The Loewner inequality follows directly from the entrywise power series of arcsin: its linear coefficient is1 and every higher odd coefficient is positive; every Hadamard power of a PSD matrix is PSD. This is the established PSD-Grothendieck/Gaussian-sign ingredient, not a new claim about that inequality.

Independently draw ONE COMMON Bernoulli gate B of mean p and set

    z_i=B(1+s_i)/2, i in I;   z_i=0 outside I.             (4)

The common gate is essential. Gaussian symmetry and(3) give

    E z_i=p/2<=p_i,
    E z_I z_I^T=(p/4)(11^T+E ss^T)>=(1/(2pi))M_I.        (5)

Therefore, with S_I=Tr(A_II M_I) and c_I=m+sum_(i in I)w_i p_i,

    E ||sum_(i in I)a_i z_i||^2 >=S_I/(2pi),
    E u(z)<=c_I.                                         (6)

This is a real positive-cost guarantee. Ordinary independent rare-threshold Gaussian rounding would not give(5); the shared gate prevents rare-group mass from being squared.

The numerator can have the affine offset a_0. Pointwise,

    N(z)+||a_0||^2 >=(1/2)||sum_i a_i z_i||^2.

Together with the feasible baseline z=0, whose ratio is R_0=||a_0||^2/m, this yields

    max{R_0, E N(z)/E u(z)} >= S_I/(8pi c_I).             (7)

The baseline is evaluated, not discarded. This avoids a false assertion that every group's affine offset has a favorable sign.

## 3. Tail truncation and only a logarithmic grouping loss

Put delta=min(1/2,m/(64an)). Ignore indices with p_i<delta, and group all remaining indices dyadically. Let L be the number of nonempty groups; when none remain, use z=0. Always L<=1+ceil(log_2(1/delta)).

Write S=Tr(A M), S_0=A_00, S_rest=Tr(A_(1:n,1:n) M_(1:n,1:n)). Positivity gives S<=2S_0+2S_rest. The discarded block has value S_tail<=a sum_tail p_i<=m/64. A second two-block Cauchy bound gives

    S<=2S_0+4S_keep+m/16.                                 (8)

If F>=1 and the baseline is smaller than F/4, then S_keep/(m+sum w_i p_i)>=F/16. For the retained dyadic groups, another PSD Cauchy inequality gives S_keep<=L sum_I S_I. Also

    sum_I c_I =L m+sum_keep w_i p_i
              <=L(m+sum_i w_i p_i).

Consequently some known group satisfies

    S_I/c_I >=F/(16L^2).                                  (9)

Choose the group maximizing this rational ratio. Equations(7) and(9), or the baseline case, imply an achievable ratio at least F/(128pi L^2). In particular an inverse-polynomial tail cutoff costs only O(log^2(an/m)), not a reciprocal rare probability in the approximation factor.

## 4. Fixed polynomial sampling cap and exact feasible output

The existence argument can be made into a capped randomized algorithm because the classical rounding cost is paid but is not a source query. For F>=1 set t=F/(4096L^2). If R_0>=t, return z=0. Otherwise(9) and(6) imply a positive margin

    E[N(z)-2t u(z)] >=t m,

with considerable constant slack (pi<4 suffices). Since N(z)<=a(n+1),

    Pr[N(z)>2t u(z)] >=t m/[a(n+1)].                     (10)

Thus at most ceil[a(n+1)/(tm) log(1/beta)] independent trials suffice to find a ratio at least t except probability beta. Include the baseline and return the largest ACTUALLY evaluated ratio. If F<1, an additive-one relaxation loss is harmless. The useful oracle form is a polylogarithmic multiplicative approximation with additive constant, suitable for a strictly positive leverage threshold.

All generated z are exactly binary and feasible, even on failed histories. The gate uses a bounded dyadic coin. Gaussian/correlation-factor approximation is paid by a joint coupling/record discrepancy: every marginal has variance one, so a finite factor error and Gaussian anti-concentration bound control sign changes without a spectral floor. Since retained p>=delta/2, all magnitudes, sampling caps and numerical precision requirements are polynomial in n,a,1/m and log(1/beta). A source-independent implementation can predeclare its trial cap. No favorable-record or expected-stopping source refund occurs.

If optimizing(2) rather than rounding a supplied M, a fixed finite SDP accuracy and inward rational feasibility rounding are additionally charged. This note's diagnostic program checks the analytic moment and ratio inequalities, not a production SDP or exact Gaussian generator.

## 5. Exact scope of the constructive advance

This solves the weighted positive-quadratic rounding obstacle on a PRODUCT binary decoder action set, up to logarithmic factors. It can be realized for a known classical measurement/prepare decoder frontend. It does NOT show that arbitrary full-CPTP Choi coordinates can be gated independently or grouped while preserving complete positivity and the input partial trace. Those coupled matrix constraints are the remaining quantum transfer problem.

In particular the received positive-cost dual representation u(C)=m+Tr(WD), W>=0, is not by itself a coordinatewise cube representation. One must construct an actual feasible matrix analogue of(4)–(5), or another cost-preserving rounding, before changing the received generic k^6 source rate. The equally informed conventional learner has the same classical optimization algorithm. No generic task-risk improvement, hardware execution or historical priority is asserted here.
