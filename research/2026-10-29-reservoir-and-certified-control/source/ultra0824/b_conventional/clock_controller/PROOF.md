# A finite microscopic preparation apparatus for weak product-phase clocks

29 October 2026. Mathematical construction with a scalar resource compiler.
No quantum state, analogue apparatus, native Hamiltonian case, bath coefficient
table or dynamical trajectory has been executed. The native weak-coupling and
low-temperature constants below remain UNEVALUATED. This package is not a
statement of physical calibration, manufacturing feasibility or memory lifetime.

## 1. Actual operation and hypotheses

Fix a bounded-degree, finite-range family of conditional clock Hamiltonians

    H_s=N+lambda V_s,       N=sum_i (I-|0><0|)_i,

on n clocks of fixed local dimension L. The parameter s denotes the supplied
source-check signs. Assume the exact ground-frame/product-coercivity hypotheses
of the accepted clock_cold_limit packet, uniformly in n and s. In particular,
the ground-frame quasi-local interaction bounds, spatial growth constants and
all local derivative/moment constants are known computable family constants.
There is a fixed positive gate lambda_B and a fixed T_B such that the
bare-seed/Bose-factor extension below has KMS parent gap g=1/16 whenever
0<lambda<=lambda_B and b>=T_B. Neither gate is numerically qualified here.
They need not coincide with the old literal lambda_T recipe or lambda_FF.

The apparatus input consists of the LOCAL table for H_s (or its source-controlled
physical realization), n,L,b, error epsilon in(0,1), a supplied local-term norm
sum E>=sum_X ||(H_s)_X||, and these family promises. It does not include eigenstates,
Bohr gaps, the ground dressing W, an exact Gibbs oracle, or a system-dependent
coherent gate compiler. The source data coupling lambda is fixed as n grows.

The physical resources permitted in the conclusion are:

* Independent passive nearest-neighbour oscillator chains with prescribed real
  Jacobi coefficients, bounded one-particle band[1/2,3/2], and linear end coupling
  to each specified bounded source seed.
* Product oscillator vacua to specified total accuracy, classical random bits,
  and calibrated local linear force pulses with specified finite accuracy.
* Finite local occupation capacity and coefficient/drive calibration paid below.

These are explicit model primitives, not acquired laboratory hardware. In the
ungauged two-body Pauli-clock endpoint a seed is U_prefix^* A_j U_prefix. Its
body order, diameter and overlap are constant, but it is generally not two-body.
The theorem concerns bounded-degree GRAPH locality. A bounded-density 3D layout
of the enlarged apparatus has not been established.

## 2. Main conclusion

For each admitted input there is a finite, graph-local, time-independent cooling
Hamiltonian (after a finite classical initialization/switching stage) whose
reduced clock state at a specified time is within epsilon in trace norm of

    sigma_s=exp(-b H_s)/Tr exp(-b H_s)

from ANY initial clock state. Time, number of modes, local occupation capacity,
peak force/energy bounds, inverse coefficient tolerance, and classical compilation
work are polynomials in n,b,epsilon^-1 and E. The polynomial constants may be
very large and depend on the fixed clock family. Polynomial dependence is in the
NUMERIC inverse temperature b and inverse accuracy, not their binary bit lengths.
No minimum system Bohr-frequency separation occurs in any bound.

The construction is uniform over s. Its bath Hamiltonian/spectrum is independent
of s and of H_s; only the constant-support seed table is source-specific. The
conditional task does not sample the source syndrome marginal. The root's separate
full-thermal syndrome sampler must supply that marginal before full Gibbs
initialization is inferred.

Units: the theorem writes the clock penalty as1. For the actual penalty Delta,
b=beta Delta, physical bath frequencies lie in[Delta/2,3Delta/2], bath coupling
is Delta alpha, and physical time below is divided by Delta. Delta is fixed in
n but may be a very large family constant. It is not silently increased with n.

## 3. Controller with no ground-frame compiler

BARE_SEEDS_AND_AVERAGING.md proves the following two interfaces.

(a) Choose onsite conditional-frame A_j=|0><a|+|a><0|, j=(i,a), with
m=n(L-1). The exact ground dressing W is used only in the PROOF. The dressed
seeds equal A_j+O(lambda) in each fixed spatial moment; their negative-band
jumps annihilate the exact vacuum. Vacuum-CP localization therefore gives
G_minus comparable to N. The all-cold coercivity/stability proof applies at
one smaller fixed lambda gate.

(b) A positive time-translation average of a KMS parent preserves its gap
EXACTLY: every conjugate fixes |sqrt(sigma_s)> and obeys the same operator
inequality. In particular Gaussian averaging at ANY window T preserves g.
This is ordinary operator order, not a new physical reservoir mechanism.

Use one fixed passive coupling measure

    dmu(nu)=f_minus(-nu)^2 dnu/(2pi),  1/2<=nu<=3/2.

Its thermal square-root spectrum h_phys,b differs from the old flat controller
by the Bose factor (1-exp(-b nu))^-1/2. FINITE_RESERVOIR.md(2)--(3a) proves
that all fixed derivative errors are polynomial(b)exp(-b/2), uniformly in n.
The negative support remains exact. Thus the bare-seed parent proof survives
after fixing lambda_B smaller and T_B larger. Higher fixed locality-moment
constants exist by the same finite derivative recurrence; the native gates
are not evaluated. The low-order bath-moment recurrence IS executed here.

## 4. Existing microscopic theorem and renormalization

Scandi--Alhambra, arXiv2505.20064v2, Theorems11,13,15--18, derives precisely
the Gaussian-averaged KMS rates from a thermal Gaussian continuum bath. We use
its corrected renormalized formulation, not a Davies/rotating-wave limit.
Its hypotheses include an initially factorized system/bath state, Wick,
zero bath means, and finite absolute correlation moments. The infinite bath
is a proof model, not the final apparatus.

MICROSCOPIC_COMPOSITION.md explicitly composes its displayed inequalities.
Replace that document's A by the fixed-spectrum A_B from FINITE_RESERVOIR(3a).
Let Gbar,Mbar,Kbar,taubar,R,C and Kgap,Ktot be exactly as defined there. Choose

    alpha=min{1,1/(2bGbar),g/(4Kgap),epsilon/[16(1+Ktot)]}.

Let U be its equation(6). The source observation window T is a PROOF parameter,
not a hardware knob. Its inequalities 1/(2alphaGbar)<=T<=R/alpha suffice.
The Lamb-renormalized target H*=H_s+alpha^2 H_LS^CG/2 has global norm distance
at most alpha^2Gbar/2 from H_s. Filter/sech Duhamel estimates give a polynomial
GLOBAL parent Lipschitz bound, even when the renormalization is increasingly
spread in space. Weyl therefore leaves effective gap at least1/32. No local
weak-product theorem is reapplied to H*.

The effective mixing error is <=epsilon/8, and the sum of microscopic,
renormalization-picture, KMS-correction and bare-target errors is <=epsilon/16.
The cooling time is tau=U/alpha^2. For a bounded-degree fixed-dimensional
family E=O(n), one coarse degree count is

    alpha^-1=O(epsilon^-1 m^5(1+b)^40 U),
    tau=O(epsilon^-2 m^10(1+b)^80 U^3),
    U=O(n(1+b)+log(epsilon^-1)).

These are upper bounds, not practical runtime predictions or optimized degrees.
The microscopic coupling weakens with size/temperature/accuracy. The source
lambda and source penalty remain fixed. This does not supply a fixed-rate
storage controller.

## 5. Finite reservoir, finite initial state, finite occupation capacity

FINITE_RESERVOIR.md pays three replacements separately.

(i) The established Woods--Cramer--Plenio finite-chain theorem, applied to each
independent passive Jacobi chain, is uniform over norm-one system observables
and arbitrary source Hamiltonians. Duality gives full reduced trace error.
The stated length R=O(tau+log(m/epsilon)) pays both infinite-to-R and M-to-R
errors. The infinite Gaussian thermal state is understood as a quasi-free
thermodynamic-limit state; finite-volume covariance estimates are uniform,
so no infinite trace-class Gibbs density matrix is assumed.

(ii) The actual finite chain uses its OWN covariance C_M=(exp(bJ_M)-I)^-1.
Bernstein-ellipse approximation, finite path agreement for Jacobi powers,
and a positive coherent-state coupling prove that its first-R thermal state
approximates the infinite marginal. No inaccessible marginal is given free.
Additional length M-R is logarithmic. Choose epsilon_B=epsilon/8 in its
equations(5),(7),(8); the entire reservoir replacement is <=epsilon/16.

(iii) The finite thermal bath is prepared as a POSITIVE mixture of product
coherent states. Its covariance and Jacobi matrix are classically acquired
from the fixed scalar spectral measure. The explicit moment-Gram lower bound

    lambda_min(G_d)>=1/[32d^3 24^(2(d-1))]

pays polynomial internal precision bits and terminating interval recurrence.
Bath matrix functions and covariance square roots require absolute, not
relative, accuracy at exponentially small thermal occupations. Classical
Gaussian quantization/clipping plus finite force pulses pays the state
preparation without a generic ideal quantum gate compiler.

For eta=epsilon/16, the pulse/clipping construction is arranged within eta
in total initial-state error (including summed local vacuum errors). The
number-moment bound is applied to the WHOLE vacuum-start driven-and-cooling
protocol. A global total-occupation comparison and then a local-cutoff
comparison give physical levels0,...,2K+1 with K polynomial. With the explicit
1024 cutoff gate in FINITE_RESERVOIR(11), their combined trace error is
<=epsilon_B/8<epsilon/16. This pays initialization at finite occupation too;
it does not assume an exactly available finite-dimensional thermal bank.

Finally allocate epsilon/16 to coefficient rounding, waveform/switching and
timing errors using finite-dimensional Duhamel. Every local tolerance is
inverse-polynomial in tau,n,M,K. Summing these terms with Section4 gives

    total trace error <=epsilon(1/8+5/16)=7epsilon/16<epsilon.

The slack is intentional. Bath-state preparation is repeated for repeated
uses; a finite closed reservoir is only guaranteed for the specified horizon.

## 6. What has and has not been acquired

This is a constructive finite-dimensional microscopic MODEL theorem, conditional
on explicit oscillator/control primitives and qualified clock-family gates.
The scalar filter/resource compiler is executed. No bath table, quantum state,
clock Hamiltonian, analogue waveform or dynamics is run in this assignment.
No experimental bath, absolute temperature, physical coupling, geometry,
prefix interaction or error tolerance has been calibrated.

No exact Hamiltonian-dependent spectral controller or generic coherent gate
oracle is needed. The apparatus still requires calibrated classical Gaussian
forces, product vacua, constant-body source couplings and polynomial overhead.
It is not an autonomous thermal-only initializer from unspecified hardware.
It has not been reduced to a two-body-only or uniformly bounded-density 3D
apparatus. The graph-growth obstacle for independent long tails on a full
3D lattice is explicitly recorded rather than ignored.

The GLOBAL microscopic comparison grows linearly with dissipative evolution
time. It pays polynomial-time conditional preparation. It does not pay a
local multi-time fault budget or stretched-exponential storage at fixed
coupling/noise. No such transfer is claimed.

Strongest equally informed ordinary route: the same Scandi--Alhambra physical
coarse-graining mechanism, ordinary passive-chain mapping and Woods truncation,
Gaussian thermal-state methods and polynomial-bit orthogonalization. Our
specific enabling input is the accepted all-cold weak-product parent gap and
its positive-average/bare-seed transfer. There is no claimed speed advantage,
new generic reservoir mechanism, historical priority, or physical capability.
