# Full completely positive survival domain: reset laws and qubit MI

24 October 2026. Parent's negative-survival extension independently checked. All formulas below use the full CP interval rather than silently retaining a lambda>=0 assumption. No historical priority or hardware claim is made.

## 1. Exact CP interval for a nontrivial conditional expectation

Let E be a nonidentity trace-preserving conditional expectation and C its exact complete order index, so C E-id is completely positive. Define Phi_lambda=lambda id+(1-lambda)E.

For -1/(C-1)<=lambda<=0,

    Phi_lambda=(-lambda)(C E-id)+[1+(C-1)lambda]E

is CP, and it is unital and trace preserving. For0<=lambda<=1 it is the usual convex mixture. Conversely, if lambda<0 and Phi_lambda is CP, then the complete order inequality gives C<=1-1/lambda, forcing lambda>=-1/(C-1). A nonzero Hermitian X in ker E satisfies Phi_lambda(X)=lambda X; unital positive-map operator-norm contraction excludes lambda>1. Thus the exact CP interval is

    [-1/(C-1),1].

The trivial C=1, E=id case is excluded from conditional ratio statements. For nontrivial finite-dimensional trace-preserving E, C>=2, also following by tracing the centered quadratic inequality X^2<=(C-1)E(X^2).

## 2. Intrinsic upper bound remains valid for negative lambda

Use the verified conditional-SLD dual expression

    F=lambda^2(A-B)/[lambda A+(1-lambda)T-lambda^2 B],
    0<=B<=A, A/T<=C-1.

On positive-denominator directions,

    partial F/partial B
      =-lambda^2(1-lambda)(lambda A+T)/(denominator)^2.

For negative lambda in the CP interval,

    lambda A+T >= T[1+lambda(C-1)]>=0.

For nonnegative lambda the same sign is immediate. Hence F decreases in B. Set B=0, put x=A/T, and differentiate:

    d/dx [lambda^2 x/(lambda x+1-lambda)]
       =lambda^2(1-lambda)/(lambda x+1-lambda)^2>=0.

The denominator at x=C-1 is 1+(C-2)lambda, whose minimum over the CP interval is 1/(C-1)>0. Therefore the same bound holds throughout:

    c_C(lambda)=(C-1)lambda^2/[1+(C-2)lambda].

At a boundary null direction where both conditional quadratic forms vanish, no ratio constraint is imposed. At lambda=-1/(C-1), the displayed bound equals1; at lambda0 it is0; at lambda1 it is1.

The SLD-to-BKM integral and state-pair interpolation do not require lambda>=0 once the channel is CP and the uniform SLD inequality is established.

## 3. Simplex sharpness survives throughout the stochastic interval

For the N-symbol reset channel K_(lambda,N), the exact stochastic interval is [-1/(N-1),1]. The existing simplex construction has output active eigenvalue

    a'=(1-epsilon)c+epsilon/N,
    c=lambda+(1-lambda)/(N-1)
      =[1+(N-2)lambda]/(N-1).

Throughout that interval c>0, including c=1/(N-1)^2 at the negative endpoint. Its exact BKM ratio is unchanged by the sign of the output tangent because it depends on lambda^2:

    [lambda^2/c]
      log[1+N(1-epsilon)c/epsilon]
      /log[1+N(1-epsilon)/epsilon].

As epsilon decreases to zero, this tends to c_N(lambda). Every finite baseline and sufficiently small perturbation remains faithful. At the negative endpoint the limit is1, including the N=2 endpoint where K is a deterministic swap.

The full-matrix inclusion's flat orthogonal code intertwines Phi_lambda with K_(lambda,C) algebraically for every lambda. Therefore the exact intrinsic law from `general_inclusion_sharpness.md` extends to the entire CP interval. The established unitary-basis theorem used for that code is unchanged; negative lambda introduces no new basis assumption.

## 4. Exact qubit MI on [-1/3,1]

For qubit depolarization, let

    k=(1+lambda)/2, theta=lambda/k=2lambda/(1+lambda).

On its full CP interval lambda in[-1/3,1], k lies in[1/3,1] and theta lies in[-1,1]. Diagonalize the physical marginal and let Delta be dephasing in that basis. The exact diagonal/coherence MI decomposition remains valid because depolarization preserves the basis-diagonal marginal, even when its eigenvalue ordering reverses.

The diagonal binary channel has complete coefficient lambda^2 for negative lambda as well: swapping its output labels replaces lambda by |lambda|. For coherence, the block identity remains a positive mixture:

    D_lambda(rho)=k Gamma_theta(rho)+(1-k)X Delta(rho)X,
    Delta D_lambda(rho)=k Delta(rho)+(1-k)X Delta(rho)X.

Here Gamma_theta=theta id+(1-theta)Delta is CP exactly for |theta|<=1. Negative theta is harmless: Gamma_(-a)=Ad_Z Gamma_a and Delta(rho) is Z-invariant, so its coherence relative-entropy contraction is a^2=theta^2. Joint convexity therefore gives the coherence upper k theta^2=lambda^2/k. This dominates the diagonal upper lambda^2, yielding

    eta_MI(D_lambda,2)<=2lambda^2/(1+lambda).

The same rare-reference product-baseline tangent family gives local limiting ratio

    lambda^2 p/[lambda p+(1-lambda)/2].

Its denominator stays positive on the entire CP interval. Its derivative in p is nonnegative, and p increasing to one gives lambda^2/k. Choose p, then a sufficiently rare reference population, then a sufficiently small faithful finite perturbation. Hence

    eta_MI(D_lambda,2)=2lambda^2/(1+lambda)

throughout[-1/3,1]. At lambda0 the channel is constant; lambda1 is identity; at lambda=-1/3 the coefficient is1/3.

### Ordinary no-reference coefficient

For0<=a<=1/3,

    D_(-a)(rho)=Y [D_a(rho)]^T Y.

Simultaneous global transpose and unitary conjugation preserve relative entropy of a pair, so the ordinary coefficient remains a^2=lambda^2. This argument must NOT be applied as a partial-transpose invariance with a quantum reference.

At lambda=-1/3 the hierarchy is therefore

    ordinary1/9, MI1/3, complete=conditional1.

The boundary channel is entanglement breaking (the optimal approximate universal-NOT channel), not an implementation of the non-CP exact antiunitary spin flip.

## 5. Higher-dimensional MI upper bound

For d-dimensional depolarization, lambda in[-1/(d^2-1),1], define

    k=[1+(d-1)lambda]/d,
    theta=lambda/k.

Then k>=1/(d+1)>0 and theta>=-1/(d-1), exactly the d-sector pinching CP lower endpoint. The diagonal/coherence mixture argument and the full-domain pinching coefficient therefore give

    eta_MI(D_lambda,d)<=U_d(lambda)
       =d(d-1)lambda^2/[1+(d^2-d-1)lambda].

This dominates the diagonal C_d(lambda) bound across the entire interval. All denominators are strictly positive. Comparing it with the exact complete/conditional coefficient yields

    c_(d^2)(lambda)-U_d(lambda)
       =(d-1)lambda^2(1-lambda)
          /{[1+(d^2-2)lambda][1+(d^2-d-1)lambda]}.

This is strictly positive for every allowed lambda except0 and1. At the negative CP endpoint, U_d=1/(d+1) whereas complete=conditional1. The upper is exact for d=2; no exact higher-d MI claim follows. The separate Gao–Zhao phi-based refinement must not be extended to negative theta without checking its actual theorem domain.

## 6. New finite negative-endpoint witness

`complement_balanced_interval.py/json` uses the exact rational simplex parameters N=4, lambda=-1/3, epsilon=7/400 and t=21/1000. Its active-block determinant inequalities, entropy gains, and interval arithmetic check correctly. The balanced incremental CMI ratio exceeds0.60728034212489, with input CMI above0.0075193356733nats and a gap over one-third input CMI above0.0020598995158nats. The negative output tangent sign does not change the active-block eigenvalues.

Bell encoding gives a qubit boundary-depolarizing witness with reference dimension8. The encoded message is independent of the reference marginal. Its incremental CMI ratio exceeds the exact plain-MI coefficient1/3 without contradiction: it is a different information task with baseline correlations. The finite witness is not a capacity theorem, free entanglement resource, or experimental-performance claim.
