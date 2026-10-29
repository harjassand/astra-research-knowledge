# Sharp complete reverse inequality for two pure preparations

## 1. Earned claim and the separate conditional question

Let `psi0,psi1` be unit vectors, let `s=|<psi0,psi1>|<1`, and set
`beta=1-s^2`. Write `T(i)=|psii><psii|` for the binary cq preparation
channel. For **every finite reference dimension**, and every two cq states
`rho=diag(A0,A1)` and `sigma=diag(B0,B1)`,

`D((T tensor id)rho || (T tensor id)sigma) >= beta D(rho||sigma)`.  (1)

The inequality is in extended nonnegative reals. In particular, on finite
relative-entropy pairs the reverse coefficient is at most `1/beta`.
It is exactly `1/beta`, already without a reference. Thus the complete
**equal-reference** reverse coefficient of the prescribed `|0>,|+>` pair
is exactly **2**. No quantum reference can increase that coefficient.

This theorem is about actual Umegaki entropy and its actual BKM Hessian.
It uses no classical-output free-inverse formula for a cq output.

For unequal reference marginals, define the subtracted quantity
`J_T=D(T rho||T sigma)-D(rho_R||sigma_R)` whenever the finite difference is
defined. Equation (1) alone DOES NOT establish `J_T >= beta J_id`: the
latter would require the extra term `(1-beta)D(rho_R||sigma_R)` on the
right of (1). Consequently the unrestricted subtracted-J reverse
coefficient is a distinct question. The classical-output equivalence
between these two notions is not imported here. Its inherited
heralded-filter upper bound is `1/(1-s)`; for the fixed pair this is
`2+sqrt(2)`. The equal-reference coefficient 2 is a lower bound on it.

## 2. Off-diagonal resolvent lemma

Let `C=[[0,T],[T*,0]]` be Hermitian with `||T||<1`, with equal finite block
sizes. For every block-diagonal Hermitian `X=diag(X0,X1)`,

`Tr[X(I-C)^(-1)X(I-C)^(-1)] >= Tr X^2`.                  (2)

Take a singular-value decomposition `T=U diag(c_i) V*`, `0<=c_i<1`.
Conjugating both blocks, write `A=U*X0U`, `B=V*X1V`, and

`a_i=1/(1-c_i^2)`, `b_i=c_i/(1-c_i^2)`.

Then the left side of (2) is exactly

`sum_ij [a_i a_j (|Aij|^2+|Bij|^2)
          +2 b_i b_j Re(Aij conjugate(Bij))]`.

Its difference from `Tr X^2` is

`sum_ij [(a_i a_j-b_i b_j-1)(|Aij|^2+|Bij|^2)
          +b_i b_j |Aij+Bij|^2]`.                       (3)

Every coefficient is nonnegative, since

`a_i a_j-b_i b_j-1
 = [(c_i-c_j)^2+c_i c_j(1-c_i c_j)]
    /[(1-c_i^2)(1-c_j^2)] >=0`.                         (4)

All matrices are allowed to be complex. The cross term in (3) uses the
Hermitian relation `Bij*=Bji`, so no transpose/conjugation is omitted.
There is no commutativity hypothesis on `A,B`.

## 3. Actual BKM comparison

For `R>0` and Hermitian `Y`, use the usual BKM form

`g_R(Y)=Tr Y Dlog(R)[Y]
       =integral_0^infinity Tr[Y(R+rI)^(-1)Y(R+rI)^(-1)] dr`. (5)

Choose a phase and an output basis so

`V=[psi0,psi1]=[[1,s],[0,sqrt(beta)]]`,
`G=V*V=[[1,s],[s,1]]`,
`G^(-1)=beta^(-1)[[1,-s],[-s,1]]`.

Let `D=diag(A0,A1)>0`, `K=diag(H0,H1)` Hermitian. On the two-dimensional
output span tensored with the reference,

`R=(V tensor I)D(V* tensor I)`,
`Y=(V tensor I)K(V* tensor I)`.

Cyclicity and the exact inverse congruence give

`g_R(Y)=integral_0^infinity
 Tr[K(D+r G^(-1) tensor I)^(-1)
      K(D+r G^(-1) tensor I)^(-1)] dr`.

Substitute `r=beta xi`. Put

`P=diag(A0+xi I,A1+xi I)`,
`E=s xi [[0,I],[I,0]]`,
`C=P^(-1/2) E P^(-1/2)`, `X=P^(-1/2) K P^(-1/2)`.

Then `D+r G^(-1) tensor I=P-E`, `X` is block diagonal, and
`||C||<=s<1`, because each `Ai+xi I>=xi I`. Thus (2) gives

`Tr[K(P-E)^(-1)K(P-E)^(-1)] >= Tr[KP^(-1)KP^(-1)]`.

After integrating,

`g_(T tensor id)(D)((T tensor id)(K))
       >= beta [g_A0(H0)+g_A1(H1)]`.                    (6)

This holds for all Hermitian blocks, including `H0=-H1`, arbitrary
noncommuting positive `A0,A1`, and arbitrary finite reference size.
The parameter `xi=0` causes no difficulty for positive blocks; the
endpoints of the scalar integral have measure zero.

## 4. Finite Umegaki pairs and supports

For faithful normalized `rho,sigma`, set `Z=rho-sigma` and
`rho_t=sigma+t Z`. The Bregman/Hessian identity for
`f(R)=Tr R log R` gives

`D(rho||sigma)=integral_0^1 (1-t) g_(rho_t)(Z) dt`.       (7)

Trace-preservation eliminates the affine derivative term. Applying (6)
pointwise to the block-diagonal line proves (1). Reference equality is
not required for (1); if supplied, it is preserved along this line.

For general cq states, mix both states with the same faithful
block-diagonal state: `rho_e=(1-e)rho+e omega`,
`sigma_e=(1-e)sigma+e omega`. Use (1) for `e>0`, and take `e downarrow0`.
In finite dimension relative entropy of this common regularization
converges to the original relative entropy, including infinity. Lower
semicontinuity gives the lower limit. For finite original entropy, joint
convexity gives the matching upper bound
`D(rho_e||sigma_e)<=(1-e)D(rho||sigma)`. For infinite original entropy,
lower semicontinuity already forces divergence. Input support inclusion
is also equivalent to output support
inclusion here: invertible congruence by `V tensor I` maps the two
direct-sum supports. Thus infinite input entropy cannot be hidden by
the channel in this two-linearly-independent-pure-output setting.

If the original cq pairs have equal reference marginals, choose any
common faithful `omega`; their regularizations also have equal
reference marginals. No dimension cutoff or infinite-reference limit
is used.

## 5. Exact sharpness from scalar priors

Take the scalar input pair

`rho=diag(1,0)`, `sigma_e=diag(e,1-e)`, `0<e<1`.

Then `D(rho||sigma_e)=log(1/e)`. Its output denominator is

`D(tau0 || S_e)=-<psi0,log(S_e) psi0>`,
`S_e=e tau0+(1-e)tau1`.

The eigenvalues are

`lambda_+-=(1 +- sqrt(1-4 beta e(1-e)))/2`.

In particular `lambda_-/e -> beta`, `lambda_+ ->1`. The spectral weight
`w_e=<psi0,P_-(S_e)psi0>` tends to `beta`, since the small-eigenvalue
projector tends to the projector orthogonal to `psi1`. Therefore

`D(tau0||S_e)/log(1/e)
 =w_e log(1/lambda_-)/log(1/e)
  +(1-w_e)log(1/lambda_+)/log(1/e) -> beta`.             (8)

Every e>0 has a finite, nonzero output entropy. If strict faithfulness
of both input hypotheses is required, perturb `rho` by an independently
smaller positive amount; continuity at each fixed e retains the same
supremum. Thus the sharp reverse coefficient is exactly `1/beta`,
not only a nonattained BKM conjecture. For `s=1/sqrt(2)`, it is 2.

For the endpoint `s=0` the preparations are orthogonal and both sides
are identical. For `s=1` the channel loses the label; no finite reverse
coefficient exists. These endpoint cases do not require (6).

## 6. What this changes, and what it does not

For the fixed `0,+` cq channel, the candidate one-family free inverse
was not the BKM metric; its falsification does not affect (2)-(8).
The optimal heralded filter succeeds with probability `1-s`, and gives
a reverse bound `1/(1-s)`. The sharper entropy retention `1-s^2`
cannot be read as a higher-probability physical label-recovery filter.
It is an information comparison. No channel simulation, quantum
capacity advantage, reference-dimension theorem for other cq channels,
or efficient physical experiment is inferred.

The result answers the assigned equal-reference dichotomy analytically:
neither a quantum-reference example above2 nor an approach to
`2+sqrt(2)` is possible there. Whether the separate unequal-reference
subtracted-J problem also has coefficient2 is left open in this file.

## 7. Primary precedents and acquisition

The BKM resolvent formula and the conversion (7) are standard, not
claimed as new. Belzig--Gao--Smith--Wu, *Reverse-type Data Processing
Inequality*, arXiv:2411.19890v3 (8 October2025), Section4.1/Lemma4.1,
explicitly uses BKM comparison for reverse relative-entropy comparisons:
https://arxiv.org/html/2411.19890v3 . Its abstract/impossibility theorem
concerns unrestricted quantum inputs and does not invalidate our
classical-input algebra. The 1999 Lesniewski--Ruskai paper and the
Hiai--Ruskai contraction-coefficient theory are cited there as prior.

The heralded comparator is the ordinary two-state unambiguous
discrimination mechanism, not a new construction: Jaeger--Shimony,
*Optimal distinction between two non-orthogonal quantum states*,
Physics Letters A197 (1995),83--87,
https://doi.org/10.1016/0375-9601(94)00919-G . A primary publisher abstract
was read; no unread detailed claim is imported. The explicit filter
proof supplied by root suffices for the bound used here.

C independently reads Eriksson's AIRR v3 for the distinct complete
maximum-contraction question, which is not this minimum-retention
problem. No claim that either old family or new result has historical
priority is made. This proof is self-contained. The substantive new
step within this investigation is the block-resolvent lower bound (2)
and its application (6); the finite integral machinery is ordinary.

No numerical channel/reference search was needed or executed. The
companion consumer checks the exact scalar/SVD slack identity and one
rational noncommuting block instance as an implementation control;
that control does not establish the all-dimension theorem.
