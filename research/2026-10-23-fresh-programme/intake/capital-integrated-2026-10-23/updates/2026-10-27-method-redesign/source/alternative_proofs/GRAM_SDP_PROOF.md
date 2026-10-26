# Exact Gram SDP and independently checkable global certificates

This construction starts from the supplied accepted free representation for the conditional-Umegaki comparison coefficient. The N965/N970 equal-marginal/conditional equality and binary theorem are priors, not claims of this construction. No historical priority conclusion is asserted for the following use of ordinary Gram matrices, semidefinite programming, and exact rational arithmetic.

## 1. Closure and denominator

Write `u3=-u1-u2`. For a channel C and output y put

`a_Cy=(C_y1-C_y3,C_y2-C_y3)` and `v_Cy=a_Cy,1 u1+a_Cy,2 u2`.

Every row has `m_Cy=min_i C_yi>0`. For PSD effects summing to I, `m_Cy I <= W_Cy <= M_Cy I`, where `M_Cy=max_i C_yi`. Thus inverse forms are continuous even on the PSD boundary. Replacing each Q_i by `(Q_i+epsilon I)/(1+3 epsilon)` proves that the closed PSD and open PD domains have the same supremum.

Let

`V=sum_y a_Ly a_Ly^T / M_Ly`.

The hypothesis on L implies V>0. With `u=(u1,u2)` the denominator obeys `F_L >= <u,(V tensor I)u>`. Consequently it vanishes only for the zero witness, and nonzero witnesses can be scaled to `F_L=1`.

## 2. The finite exact SDP

Introduce the eight vector labels

`r=(u1,u2,x_K1,x_K2,x_K3,x_L1,x_L2,x_L3)`,

where `x_Cy=W_Cy^-1 v_Cy`. For each input i form the 8-by-8 Hermitian matrix

`M_i[a,b]=<r_a,Q_i r_b>`.

It is PSD; `M0=sum_i M_i` is the ordinary Gram matrix of r. Let e_Cy denote the coordinate vector for x_Cy, and extend a_Cy by six zeros to length eight. Define the 8-by-6 real matrix D_i whose output-C,y column is

`d_Cy,i=C_yi e_Cy-a_Cy`.

The inverse equations are exactly

`sum_i M_i D_i=0`.                                                   (1)

For each i let CKi be diagonal, with diagonal entries K_yi on the three x_K labels and zero elsewhere. Define CLi similarly on the x_L labels. Because `v_Cy=W_Cy x_Cy`,

`F_K=sum_i tr(CKi M_i)`, `F_L=sum_i tr(CLi M_i)`.                     (2)

Therefore the coefficient equals the value of the finite SDP

```
maximize  sum_i tr(CKi M_i)
subject to M_i >= 0,
           sum_i M_i D_i=0,
           sum_i tr(CLi M_i)=1.
```

The matrices are only 8-by-8, with three PSD blocks. The data are rational and generated from the input channels.

Here is the converse, which prevents treating this merely as a relaxation. Given feasible Hermitian M_i, let M0=sum_i M_i and work on its support. Positivity gives `ker M0 subset ker M_i`. Set `R=M0^(1/2)`, `r_a=R e_a`, and

`Q_i=R^(-1) M_i R^(-1)` on that support.

These are PSD and sum to identity. Multiplying (1) by R^(-1) gives `sum_i Q_i R D_i=0`. Each column says `W_Cy x_Cy=v_Cy`. Since W_Cy>=m_Cy I, this makes the labelled x vectors their genuine inverse solutions. Equations (2) now give exactly the feasible SDP objectives and denominator. If some effects are singular, the closure argument in section 1 applies. There are no spurious feasible objectives.

Complex Hermitian witnesses do not require a complex solver: taking entrywise real parts of all M_i preserves PSD as real symmetric matrices, all equations (their coefficients are real), and both real diagonal objectives. Conversely a real witness is allowed in the complex domain. Thus the real SDP has exactly the same value. This argument is about the Gram representation, not a scalar or commuting restriction on Q_i.

The reconstruction has dimension at most eight. The supplied one-sided inverse-action compression further reduces active dimension to at most three if desired. That cutoff is accepted prior; it is not a new cutoff claim here.

## 3. A rational trace bound

Let `beta=det(V)/tr(V)>0`, so V>=beta I, and define

`T1=(1+sum_(C in {K,L},y) ||a_Cy||^2/m_Cy^2)/beta`.

For any witness normalized to F_L=1, `||u1||^2+||u2||^2<=1/beta`; also `||x_Cy||<=||a_Cy|| ||u||/m_Cy`. Hence `tr M0<=T1`.

A tighter optional bound uses the ordinary matrix comparator

`U=sum_y a_Ky a_Ky^T/m_Ky`,

`c0=tr(V^(-1)U)`.

The positive matrix `V^(-1/2)U V^(-1/2)` has largest eigenvalue at most its trace, so `F_K<=c0 F_L`. Further, `W^-2 <= W^-1/m` gives

`sum_y ||x_Ky||^2<=c0/min_(y,i) K_yi`,

`sum_y ||x_Ly||^2<=1/min_(y,i) L_yi`.

Therefore

`T2=1/beta+c0/min K+1/min L`

is also a valid rational trace bound. The executable uses `T=min(T1,T2)`. This also proves boundedness of the SDP feasible set; PSD plus a trace bound bounds every entry.

## 4. Exact upper certificate, independent of solver correctness

A certificate consists of rational `c>=0`, a rational 8-by-6 matrix X, rational `eta>=0`, and the input-derived T above. Form the three rational symmetric matrices

`P_i=c CLi-CKi+(D_i X^T+X D_i^T)/2+eta I8`.

Check each P_i positive definite by exact LDL pivots. Positive semidefiniteness would suffice; a small positive eta makes strict rational checking convenient.

For any genuine normalized witness, trace against M_i and sum. The D_i terms vanish by (1), yielding

`0 <= sum_i tr(P_i M_i) = c-F_K+eta tr(M0)`.

Thus

`F_K <= c+eta T`.                                                     (3)

This is a global noncommuting certificate for every finite dimension, not a numerical maximum claim. The floating SDP is used only to acquire c and X. After rational rounding, eta is increased until the exact LDL test succeeds; the effect of eta is fully charged in (3). A solver's `optimal_inaccurate` status is retained and has no role in the certificate's validity.

## 5. Exact lower witness, independent of approximate SDP feasibility

The floating primal Gram matrices generally fail exact equation (1). We do not use them as exactly feasible. Instead round them to rational symmetric matrices and add rational diagonal shifts until all three are exactly positive definite; call them G_i and G0=sum_i G_i.

Define an actual positive-effects witness on dimension eight by

`R=G0^(1/2)`, `Q_i=R^(-1)G_i R^(-1)`,

`u1=R e1`, `u2=R e2`, `u3=-u1-u2`.

All effects are strictly positive and sum to identity. For a row c_y let `S_Cy=sum_i C_yi G_i`, and let a_Cy again be extended to length eight. Direct multiplication gives the exact identity

`F_C=sum_y (G0 a_Cy)^T S_Cy^(-1) (G0 a_Cy)`.

Every quantity on the right is rational and is evaluated by exact rational linear solves. Its K/L ratio is a valid lower bound by the accepted representation. The printed lower endpoint is rounded downward and the upper endpoint in (3) upward. No supplied optimal witness is used. A conventional density-operator realization follows from the accepted active/vacuum lift; no experimental state preparation is claimed.

## 6. Executable and fallback

`evaluator.py` generates its SDP solely from rational input matrices, acquires primal/dual candidates with CVXPY/Clarabel installed only under this team's `vendor/`, and emits rational certificates. `exact_core.py` and `verify_certificate.py` use Python's standard library only. The latter rechecks all input hypotheses, all rational positivity pivots, the trace bound, the exact lower witness, and endpoint inequalities without importing CVXPY, NumPy, SciPy, or the optimiser.

A numerical SDP/certificate-acquisition exception triggers a separately checked ordinary matrix bound with a rational scalar witness. This keeps the executable a general interval evaluator, while honestly marking a possible width failure. Neither favorable conditioning nor numerical convergence is assumed for validity. The stringent width/runtime endpoint must still be demonstrated on the specified development/holdout instances; a fallback alone does not establish that endpoint.

Identical and constant K controls are returned exactly as 1 and 0. They are correctness controls and contribute no frontier claim.

## 7. Executed conditioning refinement

The executable can use positive rational vector scales `s_a`, recorded in every certificate, and a positive rational objective scale g. Let `S=diag(s_a)` and let `H=diag(s_xKy,s_xLy)` on the six inverse-action labels. The scaled labels are `r'_a=s_a r_a`, so `M'_i=S M_i S`. Define

`D'_i=S^(-1)D_i H`, `CK'_i=S^(-1)CKi S^(-1)`, `CL'_i=S^(-1)CLi S^(-1)`.

Then the identical SDP has constraints `sum M'_i D'_i=0`, denominator `sum tr(CL'_i M'_i)=1`, and objective `sum tr(CK'_i M'_i)/g`. Thus no domain or quantum witness is removed by conditioning. The upper residual checked in code is

`P'_i=c CL'_i-CK'_i/g+sym(D'_i X^T)+eta I`.

A valid rational trace bound is

`T'=max_(a=1,2) s_a^2/beta + max_(K labels) s_a^2 c0/min K + max_(L labels) s_a^2/min L`.

Accordingly the certified original coefficient upper bound is `g(c+eta T')`. The rational lower-witness formula uses `a'_Cy=S^(-1)a_Cy` in place of a_Cy. These are exactly the `vector_scales`, `objective_scale`, and `trace_bound` fields checked by the standalone verifier. The certificate does not trust how the scales were chosen.

The numerical acquisition now retries Clarabel with looser tolerances and then SCS if the initial solve fails. All attempted solver settings/errors are retained in each certificate; the exact positivity/witness checks remain the acceptance criterion. The original unscaled solver and its genuine generated-case fallback failures are preserved under `unscaled_*`. The final scaled/retry implementation closed all 22 generated cases, including four L channels approaching constant output, without a width failure. These generated cases are diagnostics and do not substitute for the withheld endpoint.
