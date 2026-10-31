# Exact activity-query lower bound with one lossy qubit
31 October 2026. Root candidate, pending independent review. This is an oracle lower bound, not a practical-advantage or novelty claim.

## 1. Input and physical model
Let x_0,...,x_(N-1) be unknown bits accessible only through the usual bit oracle O_x. The system contains a clock j in0..N and one parity bit b. Define a norm-one partial permutation

    A_x=sum_(j<N,b) |j+1,b xor x_j><j,b|.

Set F=g A_x, H=F tensor a^dagger+F^dagger tensor a, H_f=0, and J=2sqrt(lambda) I tensor a on ONE private hard-core reservoir qubit, initially vacuum. The system starts |0,0>. Define Gamma=g^2/lambda>0 and take lambda>=Gamma. This is an instance of the acquired common-loss graded model.

A controlled block encoding of A_x takes O(1) controlled O_x queries plus ordinary clock arithmetic: extend j->j+1 cyclically on0..N with a zero dummy oracle bit at j=N, and multiply this permutation by the projector j<N. The projector is a known success flag, not a postselection assumption. The inverse encoding has the same query cost. All bit-dependent information enters only through these queries. Providing a full classical description of x instead would invalidate this lower-bound access model.

## 2. Exact physical renewal law
After j physical emissions, the state is exactly the pure clock/parity state

    |j, x_0 xor ... xor x_(j-1)> tensor |0>.

Before the next emission, Hamiltonian evolution stays in the two-dimensional pair consisting of this ground state and the next clock/parity state with reservoir excited. In a fixed phase convention its unnormalized no-jump amplitudes are u(t), -i v(t), where

    u'=-g v,  v'=g u-2lambda v,  u(0)=1, v(0)=0.

The next physical emission has density4lambda v(t)^2. Both amplitudes decay to zero for g,lambda>0, so this density integrates to1. The physical emission maps the excited member exactly onto the next pure ground member. Thus successive waiting times before absorption at j=N are independent identically distributed, and do not depend on the unknown bits. This statement uses the exact finite-lambda dynamics, not adiabatic elimination.

To compute the mean waiting time, integrate the identities

    (u^2+v^2)'=-4lambda v^2,
    (u^2)'=-2g uv,
    (uv)'=g u^2-g v^2-2lambda uv.

They imply

    integral v^2 dt=1/(4lambda),
    integral uv dt=1/(2g),
    integral u^2 dt=1/(4lambda)+lambda/g^2.

The mean survival time is therefore

    m=integral (u^2+v^2)dt=1/(2lambda)+lambda/g^2
      =1/(2lambda)+1/Gamma.

Let S_N be the time of the Nth physical emission. Then E S_N=N m. At T=4N m, Markov's inequality gives P(S_N>T)<=1/4. After that Nth emission the state is absorbing: A_x vanishes at clockN and reservoir is vacuum. Hence P(clockN atT)>=3/4. Reaching clockN coherently before its last emission also already has the correct parity, so ignoring that contribution only weakens this bound.

## 3. Reduction to parity
Measure clock and parity after simulation. If clockN is present, output its parity bit; otherwise output an independent fair coin. The exact physical process succeeds with probability at least7/8 on every x. A simulator whose final accessible state has trace-norm error at most1/4 changes any output probability by at most1/8, so still computes parity with probability at least3/4.

The usual quantum query lower bound for parity is linear. For completeness, if Q bit-oracle calls produce output-sign expectation p(y), y_i=(-1)^x_i, then p is a multilinear polynomial of degree at most2Q. Success at least3/4 requires p(y) product_i y_i>=1/2 for every y. Averaging over uniform independent y gives a nonzero coefficient on the degree-N monomial. A polynomial of degree belowN has zero such coefficient. Consequently Q>=N/2. The ordinary polynomial method is due to Beals, Buhrman, Cleve, Mosca and de Wolf, *Quantum Lower Bounds by Polynomials*: https://arxiv.org/abs/quant-ph/9802049 .

Every query to the supplied F/g encoding or its inverse is implemented with O(1) bit-oracle calls, while all other provided operations are independent of x. Therefore any uniform constant-error simulator of this family needs Omega(N) supplied-coupling queries in the worst case (including queries during preparation/compilation).

Since

    Gamma T=4N(1+Gamma/(2lambda)) in[4N,6N]

for lambda>=Gamma, this is Omega(Gamma T). Lambda may be arbitrarily larger than Gamma; the obstruction is accumulated useful interaction activity, not the microscopic damping rate. The system uses O(log N) clock qubits, one parity qubit and one private reservoir qubit, with no external controls or difficult H_f.

## 4. What this does and does not establish
It rules out removing the activity scale altogether from a uniform black-box simulation theorem, even with a single private lossy qubit. It does not match the higher polynomial dependence or large constants of the current compiler, optimize precision scaling, give a practical crossover, prove an advantage over every ordinary simulator, or establish historical novelty. Small fully specified instances can be solved by dense ordinary methods; reading all N oracle bits already pays the lower bound. A method retaining knowledge across future tasks must include that initial acquisition cost rather than treating the oracle table as free.
