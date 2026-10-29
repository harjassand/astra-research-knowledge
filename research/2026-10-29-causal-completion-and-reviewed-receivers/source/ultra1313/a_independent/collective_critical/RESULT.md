# A qualified collective thermal readout at the canonical critical boundary

29 October 2026. Producer result; independent review pending. Earlier boson
packets remain frozen. This packet constructs a bounded-output thermal
operation, not a generic many-body sampler or a physical platform.

For the unchanged balanced Hamiltonian

`H=b†Tb+c†Tc+U sum_i(nb_i-nc_i)^2`,

with real PSD T having one uniform zero mode and an acquired positive
complement gap, the exact canonical K,K sector has

`E0=C sqrt(K)+O(1)`, `C=sqrt(2U/M)Tr sqrt(T)`

at fixed M and fixed U>0. The constants are explicit. A number-conserving
Gaussian charge filter has acquired normalization, moments and hopping
ratios; a global operator sum of squares provides the MATCHING lower
coefficient without assuming small depletion. Retaining its annihilation
defects and using the actual Gibbs entropy bound gives an explicit
Gaussian characteristic-query error O(K^(-1/4)sqrt(log K)) at fixed M.
No interacting partition function, permanent or assumed closure appears.

The finite operation compiles a positive five-outcome Fejer charge-readout
law with a proved total-variation error. It evaluates only native
one-particle matrix functions, ordinary determinants and explicit scalar
errors. A dyadic table samples that approximate finite law using48 FAIR
bits and at most5 comparisons; the saved execution generates no samples.

| Native input, U=beta=1 | Qualified K per flavor | Certified TV upper | First outcome of proxy |
|---|---:|---:|---:|
| Frustrated trimer | 2^64 | <0.002131 | 0.659155154 |
| Connected32-mode trimer chain | 2^192 | <0.000783 | 0.453603484 |

The M32 query has weights+17 on the first15 sites and-15 on the remaining17,
with phase `(sum_i w_i q_i)/K^(1/4)`. It is constant on every complete
trimer; removing the weak connecting bus makes its T0 value vanish. Thus
this execution probes a chain-wide collective charge, rather than another
observable confined to the first trimer. Any state strictly supported on
bare onsite pairs gives first outcome1. The ACTUAL thermal first outcome
is below0.4544, by the error theorem. This is a finite discriminating
prediction for a nonperturbatively dressed critical charge sector.

The outward compilation took0.838031s after imports,0.982224s internal
process time; M32 matrix acquisition took0.800950s. It used2048-bit Arb,
zero random draws and zero Fock states/permanents. The canonical two-flavor
space at the M32 input has dimension greater than2^11678, but that fact is
NOT a lower bound on an informed tensor or semiclassical method. The
initial local-query run, an aborted endpoint-serialization run and a failed
768-bit width check are retained with their costs. See SOURCES_AND_COSTS.md.

ALL_M_COST_AND_SCOPE.md gives explicit polynomial high-occupation gates
for joint M,K scaling when the gap/condition/query inputs are polynomially
bounded. This is not solely a fixed-trimer asymptotic. It also makes the
limitation plain: the conservative occupancies above are fantastically
large and do NOT qualify a single-band material or fixed-density phase.

Ordinary number-conserving Bogoliubov/rotor/continuous-population methods
predict the SAME leading coefficient and covariance. The constructed link
is their finite-input, fixed-U qualification for actual canonical readouts.
The source-specific canonical ED, tensor/MPO, AFQMC importance/MCMC and
strong-coupling alternatives retain their full input and are not declared
inefficient. Historical priority and practical advantage are UNKNOWN.

Full relative partition normalization, full Gibbs/occupation sampling,
arbitrary observables, fixed K=rho M, real-time dynamics and physical
preparation remain NOT_ACQUIRED. The free-energy interval has width
O(log K) at fixed M; it cannot be promoted to a relative-Z estimate. The
result is a mathematical high-occupation operation with a clear next
missing interface, not achievement of the civilisation-level mission.

Governing chain: LOWER_OPERATOR_PROOF.md -> TRIAL_NORMALIZATION.md ->
THERMAL_READOUT.md -> MATRIX_ACQUISITION.md. The full cost/quantifier
closure is ALL_M_COST_AND_SCOPE.md. Actual inputs, outward output and
finite table are in INPUT_M3.json, INPUT_M32.json and READOUT_RECEIPT.json.
