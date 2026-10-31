# Independent review: canonical activity with coherent source creation

31 October 2026. Reviewer: challenge_graph_profile_compiler.

**PASS as a scoped mathematical resource bound.** I read the entire source `SOURCE_CREATION_ACTIVITY_CANDIDATE.md`, SHA-256 `fb8bdb0fb230ad62a60247b1834b1ea36154a3752bea4c604d186bbb26f10dd6`, and checked the expectation balance and tilted operator inequalities. This is not a fault-amplitude certificate by itself, a simulation algorithm, or an energy/heat/power estimate.

## Model and count scope

The count is precisely the specified canonical Markov loss and injection jumps. Loss rates satisfy lambda_i>0; the Markov input fields are initialized. Finite source/system/reference correlations are arbitrary. Each creating block acts on its own source cell and the admitted system/spectator factors, commuting with the other cells' charges. Its aggregate off-diagonal norm is at most c_i. An uncharged sum of separately bounded terms, a block creating several cell occupations at once, or an additional source-changing control operation is not covered by these per-cell formulas.

Number-conserving hopping and all other real terms commuting with N=sum n_i may remain on. Intended system-only operations preserve N and W, including the averaged action of system-only instruments with retained records. Source-changing preparation/reset interventions require their own occupation/count accounting. Spectator events are not part of the displayed count; additional spectator dynamics must commute with the weight and obey the inherited initialized-field/domain premises. In infinite spectator formulations, those premises are supplied rather than derived from formal unbounded generator algebra.

## Mean bound

For p_i=Tr(rho n_i), positivity of the two-block state and the operator norm bound imply

    |Tr rho i[K_i,n_i]| <= 2c_i sqrt(p_i(1-p_i)) <= 2c_i sqrt(p_i).

Young's inequality gives the claimed lambda_i p_i/2+2c_i²/lambda_i bound. If L=E J_- and I=E J_+, the exact balance integrated in time therefore yields

    E N(T)-E N(0) <= -L/2+I+2 integral sum_i c_i(t)²/lambda_i(t) dt.

Dropping the nonnegative final occupation and using I<=integral sum_i a_i(t) dt proves

    E(J_-+J_+) <= 2 E N(0)+3 integral sum_i a_i(t) dt
                               +4 integral sum_i c_i(t)²/lambda_i(t) dt.

The constant-coefficient version in the source follows immediately. No stochastic occupation path or factorization of source states is used. The bound is conservative; for example zero creation allows sharper loss accounting, but that does not invalidate the displayed inequality.

## Exponential moment

Fix u>0 and W=e^{2uN}. Tilt both canonical count channels by e^u. Loss maps an occupied cell to an empty one, so the adjoint contribution is exactly

    -lambda_i(1-e^{-u}) n_i W.

Injection maps an empty cell to an occupied one, so its contribution is

    a_i(e^{3u}-1)(1-n_i)W <= a_i(e^{3u}-1)W.

Conjugate the Hamiltonian commutator by W^{-1/2}. The off-diagonal block becomes, up to phase/sign, (e^u-e^{-u})C_i, with norm at most 2c_i sinh u; the number-preserving blocks vanish. For any such operator X, d>0 and A=||X||²/d,

    [[0,X*],[X,0]] <= A I+d Q,

because A(A+d)>=||X||²; the X=0 case is direct. Taking d=lambda_i(1-e^{-u}) cancels the full negative loss term and leaves exactly the scalar B(u) in the source.

The positive tilted evolution need not have trace one. Direct weighted Gronwall gives Tr(W rho_u(T))<=Tr(W rho_0) exp(integral B_t(u)dt). Since W>=I, the unweighted trace, which is the canonical count MGF, is no larger. This proves the result without applying Jensen to a nonnormalized tilted state. For time-dependent bounded aggregate coefficients, use the pointwise rates/bounds in B_t and integrate; the same fixed W works throughout. System-only instrument slots preserve the weighted trace after summing outcomes.

As u approaches zero the source-creation quotient behaves as 4c_i² u/lambda_i and the injection term as 3a_i u, consistent with the separate mean coefficients and initial factor 2 E N(0). This is a consistency check, not a replacement for the independent mean proof.

## Interpretation

For c_i=sqrt(lambda)b_i with common loss, the coherent mean contribution is 4T sum_i b_i², not a squared norm of the sum of all system operators. This follows because the local Schur budgets use each actual loss channel separately. It is not a statement that physical activation, cooling bandwidth or control effort can be kept fixed for free. In particular injection proportional to loss makes its own count cost grow.

No thermodynamic interpretation of N is assumed. A number-preserving unprotected logical term can produce logical failure without source jumps, so the count estimate alone proves no useful computation. The distinct clamped-weight fault theorem retains its PP-zero/support requirements and its nonvanishing fixed-diffusion disturbance. No hardware, practical advantage or historical novelty is inferred here.
