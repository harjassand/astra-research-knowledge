# Precision obstruction at fixed activity: exact hard-core renewal
31 October 2026. Root candidate pending independent review. This is a channel-approximation oracle bound; it is not an efficient rare-event measurement claim.

## 1. Reuse the acquired clock instance
Use the clock/parity partial permutation A_x and ONE private hard-core qubit from EXACT_ACTIVITY_QUERY_LOWER_BOUND_CANDIDATE.md (source dd9648df785e7a22fbdd7ec7452a20f383ae86d6d97d4d6bd87e2b562652abb0, accepted receipt45c3a56734dd4df9b4ad9d4ad7b2cd52dee9f5bca44f219ccce34e20233e4e0e). All bit-dependent information is accessed through O(1)-query implementations of the supplied coupling encoding and its inverse, including compilation/preparation.

Set g=lambda=Gamma=1 and physical time T=1. Then G=Gamma T=1, ell=lambda T=1 and mu=g^2/(4lambda^2)=1/4 are fixed, independent of precision. H_f=0 and no interventions are used. The exact physical hard-core cutoff is1. The clock size grows with N, using O(log N) system qubits plus parity and reservoir.

## 2. Exact Erlang law
The single-cycle no-jump equations are u'=-v, v'=u-2v. At the critical repeated root their solution is

    u(t)=(1+t)e^-t, v(t)=t e^-t.

The next-emission density is4t^2 e^-2t, the Erlang law of shape3 and rate2. Successive cycles are independent and identically distributed by the exact renewal reset. The Nth emission time S_N is Erlang(shape3N,rate2). Consequently

    P(S_N<=1)=e^-2 sum_(k=3N)^infinity 2^k/k!
              >=c_N:=e^-2 2^(3N)/(3N)! .             (1)

No adiabatic approximation or exposed emission record is assumed. Define P_N=P(clock=N at time1). This probability is independent of the unknown bits: each no-jump two-state cycle has identical scalar coefficients and each emission simply carries the next parity label. Also P_N>=P(S_N<=1), since the Nth emitted state is absorbing. Coherent arrival at clockN before its final emission only increases P_N.

## 3. A bounded observable detects a necessary Fourier coefficient
On the accessible system define the Hermitian observable

    O=|clock=N><clock=N| tensor Z_parity.

It has norm1. Its exact expectation is

    E_x[O]=P_N chi(x), chi(x)=(-1)^(x_0+...+x_(N-1)).

Suppose a uniform simulator uses at most q supplied-coupling queries in every branch, counting all preprocessing, and its final accessible output has trace-norm error at most epsilon for every x. Composing each coupling query with its constant-query bit-oracle construction gives at most Q=O(q) ordinary bit-oracle calls. The resulting expectation p(y), y_i=(-1)^x_i, is a multilinear polynomial of degree at most2Q. This remains true with auxiliary qubits, randomness and intermediate measurements by ordinary deferred measurement / polynomial-query reasoning.

Since ||O||=1, the state-error promise implies

    |p(y)-P_N product_i y_i|<=epsilon

for every input. Average after multiplying by product_i y_i. The degree-N Fourier coefficient of p differs from P_N by at most epsilon. If epsilon<=c_N/2, then (1) makes that coefficient strictly positive. A multilinear polynomial of degree belowN has zero such coefficient. Hence Q>=N/2 and q=Omega(N).

This uses the ordinary polynomial-method fact of Beals, Buhrman, Cleve, Mosca and de Wolf, *Quantum Lower Bounds by Polynomials*: https://arxiv.org/abs/quant-ph/9802049 . The application here is to uniform absolute channel accuracy, not to a constant-success parity algorithm extracted from one rare event.

## 4. Precision scaling and exact scope
Choose epsilon_N=c_N/2. Stirling bounds give

    log(1/epsilon_N)=Theta(N log(N+1)).

Thus the family requires

    Omega(log(1/epsilon)/log log(1/epsilon))

coupling queries at fixed G=ell=1 for sufficiently small epsilon, with the customary harmless positive constants in the logarithms. The sequence epsilon_N decreases, and choosing the largest N with epsilon<=epsilon_N extends the asymptotic lower bound between sequence points. The number of clock qubits is O(log N), and all non-oracle circuit bookkeeping is independent of x.

The accepted activity obstruction and this fixed-activity precision obstruction are separate necessary dependences, not a proof of an optimal joint interpolation formula for arbitrary G and epsilon. The near-linear upper schedule still has additional precision factors. No statement that all its logarithms are necessary follows.

The signal P_N is extremely small. Estimating O experimentally to the required accuracy can be very costly; postselecting clockN does not turn this argument into a free bounded-error parity algorithm. The proof only says that a claimed uniformly accurate channel cannot synthesize the required tiny full-parity coefficient with too few oracle calls. It gives no practical crossover, classical-complexity separation, priority claim or measurement-cost exemption.
