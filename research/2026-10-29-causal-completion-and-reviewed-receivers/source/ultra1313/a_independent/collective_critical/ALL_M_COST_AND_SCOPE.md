# A growing-mode qualification and its honest density limit

29 October 2026. The point executions are not the all-M result. This file
gives an explicit sufficient polynomial high-occupation qualification from
the governing formulas, and separates it from fixed-density matter.

## 1. Uniform finite-source gates can be acquired, not postulated

The quantities below depend on the supplied finite matrix, U,beta and query
norm. Let d=M-1, A_M,B_M,tau_M be (N1), and let gmin,gmax be acquired lower/
upper eigenvalue bounds for G. They can always be chosen as

`gmin=sqrt(MU/(2Lambda))`, `gmax=sqrt(MU/(2lambda))`.

The following conservative gates imply theta_A,theta_C<=1/K,
Rdet<=3 and E_K<=(A_M+1)/K:

* K>=4d+4 and K>=d;
* tau_M K>=max(2,2 log_+(B_M/tau_M));
* sqrt(K)>=M/(4gmax);
* with A0=2M gmax/pi^2, K^(1/4)>=4A0 and
  sqrt(K)>=8A0 M;
* sqrt(K)>=dM/(8gmin).

Here log_+(x)=max(0,log x). For the second gate, z exp(-z)<=exp(-z/2)
when z>=2. For the Poisson gates, the Gaussian dual exponent is at least
pi^2 sqrt(K)/(2M gmax). The elementary log K<=2K^(1/4) and
log(8d)<=4M imply that this exponent is at least log(8dK).
Consequently r<=1/(8dK), and exp[4dr]-1<=8dr<=1/K.
The determinant bound uses

`Rdet<=exp[dM/(8sqrt(K)gmin)]<=e<3`.

Also A_M<=2M^3 for M>=2. Therefore, defining D0=13M^3,

`delta_K<=[1+6(A_M+1)]/K<=D0/K`.

Add K>=4D0 and 8K+4>=4cbar^2. These are explicit finite input tests.
Every displayed lower bound on K is polynomial in M, lambda^(-1), Lambda,
U and U^(-1), apart from logarithms of those quantities. In particular
log B_M=O(M log M) and tau_M^(-1)=O(M^3), despite B_M itself possibly
being large. No asymptotic local-limit constant or uncharged tail oracle
is needed to select the gate. The actual consumer evaluates the sharper
original gates instead of these deliberately loose estimates.

## 2. The acquired error goes to zero along a paid joint sequence

Set G0=M+4D0, L1=sum_ij|T_ij|, and let S=Tr sqrt(T). The above gates imply

`gamma_K<=G0/K`,

`Rup(K)<=Rbar`,

`Rbar=(L1/M)[gmax^2/4+2G0]+(4/3)U Tr(G^-1)D0`.

Use Tr(G^-1)=sqrt(2/(MU))S and, if desired, S<=d sqrt(Lambda).
Let B be (C4) and define

`B0=Rbar+B+4d/beta`,

`H0=1+[C+Rbar+8d/beta]/lambda`.

The exact canonical dimension gives

`Bfast<=B0+(2d/beta)log K`,

`Dexc+1<=H0 sqrt(K)`.

The first follows from binomial(K+d,d)<= [e(K+d)/d]^d. The second uses
log K<=2sqrt(K) and K>=1. Since log K<=2K^(1/4), (T8) consequently yields
for every query |t|<=Tmax,

`Err_K(t)<=Aread K^(-1/8)+Bread K^(-1/4)`

`          <=(Aread+Bread)K^(-1/8)`,

`Aread=(Tmax/sqrt(U))[sqrt(B0)+2sqrt(d/beta)]`,

`Bread=d sqrt(Lambda/8)/(2sqrt(U))*Tmax^2`

`      *[8sqrt(H0)+(8/3)Tmax]`.

For an n-outcome Fejer query include its largest harmonic in Tmax. Its
TV error is at most n(Aread+Bread)K^(-1/8)/2. Thus adding the LITERAL gate

`K >=[n(Aread+Bread)/(2epsilon)]^8`

acquires error at most epsilon, with arithmetic rounding paid separately.
The high exponent is conservative and not a practical density threshold.
It proves that when matrix conditioning and query norms have polynomial
M-dependence, an explicitly polynomial joint K(M,epsilon^(-1)) suffices.
The result is stronger than "for each fixed trimer eventually Gaussian";
it remains weaker than a fixed-density thermodynamic theorem.

For the native connected trimer chain lambda>=4epsilon_bus/M^2,
Lambda<=12+4epsilon_bus, L1=O(M), with fixed epsilon_bus=1/100000. All of
these gates have polynomial M-dependence. A global block charge query has
polynomial norm and uses no eigenmode-addressing oracle. The actual M32
query cuts at15 sites, with raw weights+17 on the first15 and-15 on the
remaining17. It is constant on EVERY complete trimer. Therefore its
T0 value is zero if the connecting bus is removed; the finite output
actually resolves the collective connection rather than repeating a
stiff first-trimer mode.

## 3. Complete computational cost and the ordinary route

For a rational input and acquired gap bound, ordinary dense one-particle
linear algebra takes polynomial M/input-bit work. The Newton--Schulz
polynomial needs logarithmically many iterations in condition number and
requested matrix accuracy. Outward working precision is explicitly
validated, not assumed. A conservative existence bound follows by bounding
the scalar polynomial coefficient l1 norms by a_(n+1)<=2a_n^3: their logs
are O(3^n), hence polynomial in the condition number and log accuracy at
the needed n. Refining working precision until the displayed width tests
pass has finite polynomial bit cost in those conservative parameters.
The saved executable uses fixed2048-bit arithmetic for its declared two
inputs; it does NOT implement a universal adaptive precision controller.

Canonical log D is computed from O(M) factors, with O(M log(K+M)) result
bits. Matrix determinants have dimension M, not D^2. The normalizer of the
trial is acquired by the CLT/Poisson proof and ordinary one-particle
determinants; it is never sampled by rare acceptance of the filter.
An accuracy gate can be selected by doubling K and evaluating the proved
finite bounds. A binary representation of the qualified large K takes
O(log K) bits. The n-output proxy table then uses ordinary exponentials/
cosines with outward errors; a B-bit dyadic table emits a sample using B
FAIR bits and O(n) comparisons. No rejection, MCMC mixing time, permanent,
Hamiltonian matrix-element oracle or full many-body state is hidden in
that output contract.

The equally informed harmonic/Bogoliubov/rotor method produces the SAME
leading covariance and energy coefficient at similar one-particle cost.
The constructed link is its explicit nonperturbative fixed-U qualification
for actual canonical finite readouts. It is not an invention of collective
squeezing, a proof of historical priority, or an empirical speed advantage.
Canonical ED and tensor methods may provide sharper finite-occupation
answers. Hilbert dimension alone gives no lower bound on them.

## 4. What has and has not changed physically

The native Hamiltonian has noncommuting frustrated hopping and U sum q_i^2
with U FIXED; there is no expansion in small U, small beta U, or a free
grand-canonical window. Its high-occupation relative-charge sector has an
acquired K^(1/4) bounded-readout description and a sharp sqrt(K) energy
coefficient. This bypasses the earlier normalization/overlap obstruction
for these queries without claiming an all-observable sampler.

The saved conservative gates select K=2^64 for the trimer and K=2^192
for M32. These occupancies are NOT a demonstrated material regime. No
single-band atomic realization at such populations, thermodynamic
stability under omitted interactions, or useful laboratory threshold has
been acquired. The actual computational change is a mathematically
qualified finite-output law whose cost does not scale with D^2.

Full relative partition normalization, full Gibbs trace-norm approximation,
fixed K=rho M, interaction-ordered phases, microscopic material inputs,
physical preparation and real-time predictions remain OPEN. These limits
prevent the operation from being promoted to a general solution of
frustrated matter or a civilisation-level capability on this evidence.
