# Independent challenge: exact common-operator completion interval

Scientific subtask: challenge the root's proposed common-operator completion,
including attainment, endpoint conventions, compatibility, and information scope.
No full matrix calculation or old single-probe construction was repeated.

## Contract

All matrices in this note are exact real matrices. Let `X` be `n by d`, of full
column rank, with `1 <= d <= n`, and prescribe an exact action `Y`. Let `L < U`.
We consider ONLY the information class

    C = {B = B^T : B X = Y, L I <= B <= U I}.

This is not the class of matrices with just independently prescribed scalar
Jacobi moments. It contains their cross-action constraints when X,Y are a
joint transcript. It also discards all known entries of a full input matrix
except those consequences retained in X,Y and the enclosure. A lower bound
for C is therefore not a lower bound for a method allowed to inspect the
entire input or query a different subspace.

Put `G=X^T X`, `T=X^T Y`, `H=Y^T Y`. Require `T=T^T` and

    H_L = T - L G > 0,       H_U = U G - T > 0.

These strict compressed inequalities hold if there exists an actual
`L I < A < U I` with `A X=Y`. They can also hold in some boundary cases.

Define

    Z_L = Y-L X,       Z_U = U X-Y,
    B_L = L I + Z_L H_L^{-1} Z_L^T,
    B_U = U I - Z_U H_U^{-1} Z_U^T.

## Theorem 1: exact compatibility and order interval

Under the displayed compressed strictness assumptions, C is nonempty iff

    N := (L+U) T - L U G - H >= 0.

When nonempty,

    C = [B_L,B_U] := {B=B^T : B_L <= B <= B_U}.

In particular the extrema are feasible and the action constraint is automatic
inside their order interval. Both candidates have rank-d updates of scalar
matrices; they never require an enumeration of the unknown complement.

### Proof: action and necessary order

Symmetry of T gives `Z_L^T X=H_L` and `Z_U^T X=H_U`. Therefore
`B_L X=L X+Z_L=Y` and `B_U X=U X-Z_U=Y`.

If `B` is feasible, set `C_0=B-L I>=0`. Since `C_0 X=Z_L` and
`X^T C_0 X=H_L>0`, factor `W=C_0^{1/2} X`. The matrix
`W(W^T W)^{-1}W^T` is an orthogonal projection, whence

    Z_L H_L^{-1} Z_L^T
      = C_0^{1/2} W(W^T W)^{-1}W^T C_0^{1/2} <= C_0.

Thus `B_L<=B`. Applied to `U I-B`, the same argument gives `B<=B_U`.

If `B_L<=B_U`, the already checked action shows both endpoints feasible:
`L I<=B_L<=B_U<=U I`. Write `D=B_U-B_L>=0`; `D X=0`. If
`B_L<=B<=B_U`, then `0<=B-B_L<=D`, so `X^T(B-B_L)X=0`. Positivity
implies `(B-B_L)X=0`, establishing the whole-interval characterization.

### Proof: reduced compatibility test

For the mathematical argument only, set `Q=X G^{-1/2}` and complete Q to an
orthogonal basis. Write `J=Q^T Y G^{-1/2}` and
`R=Q_perp^T Y G^{-1/2}`. Then `J=G^{-1/2}T G^{-1/2}`, and a completion has
block form

    [[J, R^T], [R, C]].

The lower and upper endpoint complements are

    C_L = L I + R(J-L I)^{-1}R^T,
    C_U = U I - R(U I-J)^{-1}R^T.

Since both functions of J commute,

    C_U-C_L
      = (U-L) [I - R((J-L I)(U I-J))^{-1}R^T].

For any rectangular W, `I-W W^T>=0` iff `I-W^T W>=0` (both are equivalent
to `||W||<=1`). Thus this difference is PSD iff

    R^T R <= (J-L I)(U I-J).

But `R^T R=G^{-1/2}H G^{-1/2}-J^2`. Cancelling `J^2` gives exactly
`G^{-1/2} N G^{-1/2}>=0`, proving the criterion. This also shows that
`N>0` makes `D` strictly positive on the orthogonal complement of X.

If the class contains an actual strictly interior A, then

    N = X^T (A-L I)(U I-A) X > 0.

The multiplication here is legitimate because both factors are polynomials
in the same self-adjoint A. This is a way to establish the strict assumption,
not an assumption that arbitrary two PSD matrices have PSD product.

## Theorem 2: attained CDF extrema and small-matrix inertia formulas

Let `N_B(t)=#{i:lambda_i(B)<=t}` be the INCLUSIVE unweighted eigenvalue count.
For every real t,

    min_{B in C} N_B(t) = N_{B_U}(t),
    max_{B in C} N_B(t) = N_{B_L}(t).

The same two operators attain these extrema simultaneously at all thresholds.
This follows directly from the min-max principle: Loewner order orders every
ordered eigenvalue. Unlike probe-weighted CDFs, no eigenvector leakage issue
occurs for these UNWEIGHTED counts.

No n-by-n eigendecomposition is needed. For `L<=t<U`, define the d-by-d
symmetric matrices

    K_L(t) = H-(t+L)T+L t G,
    K_U(t) = H-(t+U)T+U t G.

With `n_-(K),n_0(K),n_+(K)` denoting exact inertia,

    N_{B_L}(t) = n-d+n_-(K_L(t))+n_0(K_L(t)),
    N_{B_U}(t) = n_+(K_U(t))+n_0(K_U(t)).

For `t<L` both counts are 0, and for `t>=U` both are n.

### Proof of the formulas

`Z_L` has full column rank because `Z_L^T X=H_L` is invertible. The nonzero
eigenvalues of `Z_L H_L^{-1} Z_L^T` are exactly those of

    W_L = H_L^{-1/2} Z_L^T Z_L H_L^{-1/2} > 0.

Hence B_L has n-d eigenvalues exactly L, plus d eigenvalues
`L+lambda_i(W_L)`. For t>=L, their count below t is the nonpositive inertia
of `W_L-(t-L)I`, which by congruence equals that of K_L(t).

Similarly B_U has n-d eigenvalues exactly U, plus d eigenvalues
`U-lambda_i(W_U)`, where `W_U=H_U^{-1/2}Z_U^T Z_U H_U^{-1/2}`. For t<U,
the latter are at most t iff `lambda_i(W_U)>=U-t`. This is the NONNEGATIVE
inertia of K_U(t). Zeros belong in both stated formulas; dropping them
changes the inclusive-CDF contract.

## Corollary 3: exact global retained-information ambiguity

Pointwise, for every `L<=t<U`,

    [N_{B_L}(t)-N_{B_U}(t)]/n >= max(0,(n-2d)/n).

The useful pointwise count can be much larger and is given exactly by Theorem2.

Let `q=rank(B_U-B_L)`. Then, more strongly,

    sup_t [N_{B_L}(t)-N_{B_U}(t)]/n = q/n,

and the supremum is an attained maximum at t=L. If C contains a strictly
interior A, then `q=n-d`, so the global ambiguity is exactly `(n-d)/n`.

### Proof

The pointwise bound uses `N_{B_L}(t)>=n-d` and `N_{B_U}(t)<=d`, together with
nonnegativity of the difference. Since `D=B_U-B_L>=0` has rank q, rank
interlacing bounds the difference of the two inclusive counts by q.
For completeness, a positive rank-q update can move at most q eigenvalues
across any fixed threshold: the min-max variational space for B_L restricted
to `ker D` loses at most q dimensions. This proof includes threshold ties.

At L, B_L has exactly n-d eigenvalues. In the Q,Q_perp block representation,
the leading block of `B_U-L I` is `J-L I>0`. Its Schur complement is exactly
`C_U-C_L`, whose rank is q because D vanishes on Q and equals that matrix
on Q_perp. Sylvester inertia therefore gives

    nullity(B_U-L I) = n-d-q.

All eigenvalues of B_U are >=L, so `N_{B_U}(L)=n-d-q`, and the count gap is
q, proving attainability. Under strict interior support, `B_U>=A>L I`, so
this nullity is zero and `q=n-d`.

Strictness matters. For `A=diag(-1,1)` and `X=(1,1)^T`, with L=-1,U=1,
H_L and H_U are positive but N=0. The prescribed action already fixes A;
`B_L=B_U=A`, so q=0 even though n-d=1. The companion exact test includes
this boundary counterexample.

## Scope and finite-precision obligations

1. X,Y must be one exact joint transcript. Eight separate completed operators
   B_ell do not supply it, even if their individual moments are exact.
2. Numerical rank of the concatenated saved vectors is not exact rank.
   Rational elimination, a certified Gram bound, or another rigorous full-rank
   argument is necessary. Near dependencies can make inversion expensive.
3. If Y=barA X for an exactly represented barA with `||A-barA||<=tau`, the
   theorem applies to barA. For the original A, eigenvalue-count transfer is
   `N_barA(t-tau)<=N_A(t)<=N_barA(t+tau)` by Weyl. The same statement would
   be false for a probe-weighted CDF without leakage terms.
4. Lower information bounds hold for the transcript/support class, not for
   the fully known exact-decimal NIST operator. They do not defeat dense
   diagonalization, access to the stored entries, added structural assumptions,
   or another oracle query. Matrix entries cannot be both discarded from the
   definition and then claimed to be included in an impossibility statement.
5. Transcript-adaptive adversarial completions do not establish a lower bound
   with a fixed original A chosen before random probes. That quantifier needs
   a separate argument.
6. Actual practical expense includes constructing X,Y, exact rank/Gram and
   compressed products, verifying enclosure/compatibility/inertias, and source
   conversion. Matrix dimension reduction alone is not a speedup.
7. The all-threshold floor comes in part from unrestricted eigenvalues at the
   support endpoints on the unqueried directions. It can be inappropriate for
   a richer prior such as exact trace, positivity stronger than the supplied
   lower endpoint, sparsity, graph locality, or an independently known spectral
   interval. Such information changes C and must be charged separately.

## Status and novelty

The formulas survived the independent challenge. They are self-contained
Schur-complement/PSD-completion arguments. This note claims no historical
novelty for the underlying extension theory, min-max principle, or low-rank
inertia reduction. The root's actual-input construction remains separately
responsible for source binding, numerical conditioning and cost.

Executable exact rational checks are in `checks/check_completion_exact.py`.
They verify tiny nonorthogonal and support-boundary fixtures; they complement
the proof and do not prove its universal statements by testing.
