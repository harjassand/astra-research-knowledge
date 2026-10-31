# Independent review: fixed-activity precision query obstruction
31 October 2026. Reviewer: independent internal mathematical review.

## Source and verdict
PASS. I read the complete actual source
graded_reservoir_consequence_audit_20261031/EXACT_PRECISION_QUERY_LOWER_BOUND_CANDIDATE.md,
4,821 bytes, SHA-256 ae7687f4fb3c5510704ed40246bea266080a8392c9629232ab28de801f3331a5,
and independently verified its size and hash.

The exact hard-core clock/access source dd9648df785e7a22fbdd7ec7452a20f383ae86d6d97d4d6bd87e2b562652abb0 and its accepted receipt 45c3a56734dd4df9b4ad9d4ad7b2cd52dee9f5bca44f219ccce34e20233e4e0e remain binding. This new argument is a uniform channel-approximation query lower bound at fixed physical activity, not an efficient rare-event measurement scheme.

## 1. Exact critical renewal
At g=lambda=1, the two-state equations have the repeated-root solution u(t)=(1+t)e^(-t), v(t)=t e^(-t). The next-emission density is 4v(t)^2=4t^2e^(-2t), exactly the Erlang(shape3,rate2) density.

The earlier exact hard-core renewal proof makes the successive cycle waiting times independent and identical. Thus the Nth emission time is Erlang(shape3N,rate2), and
P(S_N<=1)=e^(-2)sum_(k>=3N)2^k/k!>=c_N=e^(-2)2^(3N)/(3N)!.
No approximation in damping or elimination has entered.

The population of clock N also includes possible coherent arrival before the final emission. Every such clock-N component has the complete accumulated parity. The clock-N probability P_N is independent of the unknown bits because every scalar two-state cycle and jump reset is bit-independent apart from its carried parity label. Therefore P_N>=c_N.

## 2. Observable and Fourier argument
The accessible observable projector(clock=N) tensor Z_parity has operator norm one, and its exact expectation is P_N times the full parity character. A uniform output trace-norm error epsilon consequently bounds the absolute expectation error by epsilon. No factor of one half is used for this signed observable.

A simulator with a worst-case total budget q of coupling/access queries can be compiled into Q=O(q) standard bit-oracle calls. This includes all bit-dependent preprocessing and compilation; the actual block and inverse constructions have constant bit-query overhead.

The resulting observable expectation is a multilinear polynomial of degree at most 2Q in the input signs. Auxiliary systems, classical randomness and intermediate measurements do not invalidate this standard degree statement when the final algorithm is unconditional; normalized successful postselection is not available.

Multiplying the uniform approximation inequality by the full parity character and averaging over independent input signs shows that the degree-N Fourier coefficient differs from P_N by at most epsilon. If epsilon<=c_N/2, it is strictly positive. Every polynomial of degree below N has zero such coefficient. Hence Q>=N/2 and q=Omega(N).

This is the ordinary polynomial-method ingredient credited to Beals, Buhrman, Cleve, Mosca and de Wolf, primary source https://arxiv.org/abs/quant-ph/9802049 . The present deduction does not turn an exponentially rare signal into a constant-success single-shot algorithm.

## 3. Precision asymptotics and interpolation
For epsilon_N=c_N/2,
log(1/epsilon_N)=log(2)+2+log((3N)!)-3N log(2)=Theta(N log(N+1)).
Stirling bounds give the claimed Omega(log(1/epsilon)/log log(1/epsilon)) query lower bound along this sequence.

The sequence decreases strictly for N>=1. Choosing the largest N with epsilon<=epsilon_N gives epsilon_(N+1)<epsilon<=epsilon_N. Consecutive logarithms both have order N log(N+1), so the same asymptotic bound holds between sequence points. Harmless positive constants inside the logarithms cover small parameters.

Here G=Gamma T=1, ell=lambda T=1 and mu=1/4 are fixed. The system clock dimension grows with N, using O(log N) clock qubits. This is not a lower bound at fixed full Hilbert dimension, and the source properly records the growing clock.

## 4. Scope
The physical reservoir remains one private HARD-CORE qubit. The construction does not rely on a bosonic ladder, public bath measurements, controls or a difficult free Hamiltonian.

Very small P_N can require substantial statistical work to estimate. Postselecting the completed clock would introduce a different, rare-success resource; it is not granted by the trace-norm channel guarantee. The proof concerns the degree of a synthesized channel expectation, not efficient access to that expectation as a classical scalar.

The activity and precision lower bounds are separate necessary dependences. They do not establish an optimal joint interpolation formula, match all logarithms or mode factors in the upper schedule, or imply practical advantage, historical novelty or a classical-complexity separation. Total acquisition cost and unconditional worst-case query accounting remain essential.
