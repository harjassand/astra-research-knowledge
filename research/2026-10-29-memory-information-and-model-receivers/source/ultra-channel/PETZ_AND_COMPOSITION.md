# Divergence-uniform thinning and its exact composability boundary

The broader Petz formulation was independently noticed in this branch and by root, who requested the explicit endpoint/boundary argument. Root also supplied the block-erasure distinction below. These are consequences of the SAME operator proof; no new numerical source or fixture is introduced.

## 1. The gauge is an abstract quadratic identity

Take arbitrary positive definite operators A_i on one complex Hilbert space, vectors x_i, Lambda=sum_i A_i, and x=sum_i x_i. Set l=Lambda^-1 x and x_i^0=x_i-A_i l. For every column-stochastic output map P, expansion gives

    Q_P(A,x)=Q_P(A,x^0)+<x,Lambda^-1 x>.                       (1)

Indeed the adjusted output vectors sum to0, and the baseline operators sum to Lambda. This proof uses neither Hermiticity of the x_i nor the Jordan form of the A_i.

If m Lambda<=A_i<=M Lambda and the pair kernels and graph gap are as in EXPANDER_DESIGN, the identical parallel-sum/weighted-Poincare proof gives

    Q_E-Q_F >= gamma [Q_id-Q_ref],
    gamma=delta*m*lambda_2/(2M),
    Q_(Er_gamma(E)) >= Q_F.                                  (2)

The last row of Er_gamma is gamma times the sum of all inputs, so its contribution is exactly gamma Q_ref. This is a finite quadratic-perspective inequality, not a numerical approximation to an entropy.

## 2. Every operator-convex Petz generator, with the SAME budget

For faithful quantum input pairs rho,sigma on A R, let rho_i,sigma_i be their primitive reference blocks. For every s>=0 put

    A_i=L_(rho_i)+s R_(sigma_i),        x_i=rho_i-sigma_i.

The primitive effect bounds mI<=M_i<=MI imply

    m A_ref<=A_i<=M A_ref,
    A_ref=L_(rho_R)+s R_(sigma_R),

uniformly in s and reference dimension. The quadratic in (2) is the Petz divergence for f_s(t)=(t-1)^2/(t+s). The reference row is the SAME resolvent divergence of rho_R,sigma_R. Thus

    Q_f_s(F_R rho||F_R sigma)
      <=(1-gamma)Q_f_s(E_R rho||E_R sigma)
           +gamma Q_f_s(rho_R||sigma_R).                       (3)

The quadratic endpoint f_infinity(t)=(t-1)^2 is covered separately with A_i=R_(sigma_i). It is not discarded in a limit of measures. Affine generators contribute zero for normalized states. The standard positive integral representation of an operator-convex normalized generator f, including its nonnegative quadratic endpoint coefficient, now proves

    Q_f(F_R rho||F_R sigma)
       <=(1-gamma)Q_f(E_R rho||E_R sigma)
            +gamma Q_f(rho_R||sigma_R)                         (4)

for EVERY such f, with the SAME gamma. Equivalently Er_gamma(E) dominates F for all these Petz divergences after every finite reference. Noncommuting blocks and complex right multiplication are fully retained. No simultaneous diagonalization or equality of reference marginals is assumed.

For boundary states the governing formulation is the unsubtracted, extended-valued FLAGGED inequality Q_f(Er_gamma(E)_R rho||Er_gamma(E)_R sigma)>=Q_f(F_R rho||F_R sigma), obtained by common faithful regularization and the usual Petz extension. At infinite support values there is no infinity-minus-infinity subtraction and no coefficient ratio. Nonnegative kernel integrals and their endpoint extensions justify passing to this formulation. Formula(4) is read as that extended-value flag identity, with 0<gamma<1.

The theorem is NOT an assertion for sandwiched Renyi divergences, measured divergences, the trace norm, conditional min-entropy, or every decision loss. Petz Renyi orders in their operator-convex generator ranges follow, but a linear contraction of their logarithms by1-gamma has not been claimed. The existing guessing reversal therefore contradicts no premise. Positive Petz-generator integration and N675's resolvent bridge are established inputs; the f-uniform budget is a consequence of the explicit abstract coercivity proof.

## 3. Independent per-record thinning composes

Complete order is stable under tensoring by any other channel: first apply that channel to the spectator input and treat its output as the untouched reference for the complete comparison. Replacing factors one at a time consequently gives

    [Er_gamma(E)]^(tensor k) >=_complete Q_f F^(tensor k)        (5)

for every finite k and every f in Section2. This is the standard complete-order tensorization mechanism (Hirche–Rouze–StilckFranca Lemma3.1 for the entropy order), not a new tensorization theorem. The physical classical postprocessor independently erases each record. It uses k Bernoulli coins, retains(1-gamma)k records in expectation, and emits the pattern/erasure flags. It does not make fewer input preparations or erase flags for free.

## 4. The single-use strict factor does NOT tensorize

Neither (5) nor the one-use bound I(R:F)<=(1-gamma)I(R:E) implies

    I(R:F^k)<=(1-gamma)I(R:E^k)                                (6)

for arbitrary correlated block encodings. The same fixed faithful binary inputs in the qubit receiver give an explicit obstruction. Let a fair classical reference bit prepare rho_+^(tensor k) or rho_-^(tensor k). E and F each have distinct output laws for the two inputs. A repeated classical test distinguishes them with error tending to0, so

    I(R:E^k) -> log2,          I(R:F^k) -> log2.

Their ratio tends to1. More quantitatively, one F outcome has probabilities3/40 versus1/20 for the exact original qubit states. A midpoint count test has error at most exp(-k/3200) by Hoeffding. Fano gives I(R:F^k)>=log2-h_2(exp(-k/3200)) once that upper error is below1/2. For ANY fixed gamma0>0, choose k large enough that this binary entropy is less than gamma0 log2. Then I(R:F^k)>(1-gamma0)I(R:E^k), since I(R:E^k)<=log2. This uses a specified conditional-product preparation model, not a statistical assumption about acquired data.

In particular, erasing the ENTIRE block with probability gamma0 gives mutual information(1-gamma0)I(R:E^k), and eventually fails to dominate F^k. It has the SAME expected retained-record count as independent thinning but a different failure pattern. Expectations alone do not pay composability. An ordinary classical repetition/Chernoff argument already supplies this obstruction; it is not a claimed new strong-data-processing theorem.

Thus the scalable operation is independent per-record divergence-safe thinning with flags, rather than a dimension-free block compression ratio or universal decision improvement. The distinction also prevents promoting a structured one-use complete relative coefficient into the unresolved general coefficient/tensorization programme in Belzig–Gao–Smith–Wu Section7.
