# Audit: second binomial positive noise correction

The proposed construction, signs, deterministic query count and safe full-law constants are valid. This is a standard binomial expansion step using the acquired covariance action; no novelty claim is made. It removes the first correction's deterministic Sigma^2/n^2 covariance remainder, while leaving randomization and the general d^(1/3) bound.

## Acquired word and construction

Let J_Sigma(v) be the four-query GLOBAL covariance action: its time is independent uniform on [0,1], its Gaussian center is fresh, and the two internal heat-Hessian actions have fresh independent seeds. For all supplied v,

    E[J_Sigma(v)|v]=Sigma v,   ||J_Sigma(v)||<=L^2||v||.

A Sigma^2 word uses two fresh global operators in sequence,

    J_Sigma2(v)=J_Sigma^(2)(J_Sigma^(1)(v)).

Conditioning on the first output before using the fresh second operator proves

    E[J_Sigma2(v)|v]=Sigma^2 v,
    ||J_Sigma2(v)||<=L^4||v||.

It costs at most eight original g queries. Reusing a conditional center/time operator would not establish this identity: it could produce an average of conditional squares instead of the square of the global average. A reused stratum is therefore not interchangeable with a fresh global operator.

Take k independent Sigma actions and l independent Sigma^2 words, with the two blocks independent conditional on their common fresh Z. Define

    Y2=Xbar+tau Z-Jbar_Sigma(Z)/(2 tau n)
                    -Jbar_Sigma2(Z)/(8 tau^3 n^2)+eta W,
    tau^2+eta^2=sigma^2,   tau,eta>0.

It is an actual positive pushforward law, has mean exactly mu, costs at most n+4k+8l whole-vector g queries on every execution, and uses O((n+k+l)d) surrounding arithmetic/storage if the sample mean and action sums are streamed.

## Deterministic polynomial comparison

Replace the acquired actions temporarily by their conditional means and put

    M2=tau I-Sigma/(2 tau n)-Sigma^2/(8 tau^3 n^2).

For A=Sigma/(tau^2 n), the exact commuting polynomial identity is

    (I-A/2-A^2/8)^2=I-A+A^3/8+A^4/64.

Thus

    M2^2+Sigma/n+eta^2 I=sigma^2 I+Q2,
    Q2=Sigma^3/(8 tau^4 n^3)+Sigma^4/(64 tau^6 n^4) >=0.

Use the same interpolation as for the first correction, with C_t=sigma^2 I-t Sigma/n+Q2. Since C_t=C_1+(1-t)Sigma/n and C_1=M2^2+eta^2 I, C_t>=eta^2 I for every n>=1. The same analysis Stein fluctuation bound E||T_U-Sigma/n||F<=L^2 sqrt(d)/n^(3/2) applies. A safe deterministic comparison bound is

    L^2 sqrt(d)/(2 eta^2 n^(3/2))+||Q2||F/(2 eta^2).

## Implemented randomization

The difference from the deterministic comparison is conditionally centered given Xbar,Z. Conditional independence of the two blocks and the fresh calls within each batch gives

    E||Delta||^2
      <= d[L^4/(4 tau^2 n^2 k)+L^8/(64 tau^6 n^4 l)].

Gaussian reserve smoothing and Taylor's integral remainder therefore give the safe total bound

    TV(Law(Y2),N(mu,sigma^2 I))
       <= L^2 sqrt(d)/(2 eta^2 n^(3/2))+||Q2||F/(2 eta^2)
          +d[L^4/(4 tau^2 n^2 k)+L^8/(64 tau^6 n^4 l)]/(2 eta^2).

These constants are rounded upward from the centered-indicator Gaussian Hessian contraction; no extra independence between the perturbation and Z is asserted or needed. Its conditional centering is what cancels the first-order test term.

For tau^2=eta^2=sigma^2/2 and r=L/sigma, use Sigma<=L^2 I to get

    TV <= r^2 sqrt(d)/n^(3/2)
          +r^6 sqrt(d)/(2n^3)+r^8 sqrt(d)/(8n^4)
          +r^4 d/(2n^2 k)+r^8 d/(8n^4 l).

All coefficients agree with the proposal. This theorem concerns the implemented random vector, rather than its covariance alone. Neither the first-order iid/stratified shell lower bounds nor a claim of exact covariance matching should be transferred to this second correction. The d^(1/3) general upper rate remains because the source Stein fluctuation and the first action-batch term remain. An all-order polylogarithmic compiler would still need a new cost/cancellation argument.
