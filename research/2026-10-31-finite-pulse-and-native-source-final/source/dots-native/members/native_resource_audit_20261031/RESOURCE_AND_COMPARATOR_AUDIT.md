# Frozen native protocol: conservative resource and ordinary-comparator audit

31 October2026. This audit does not alter the accepted native theorem or its archives. It instantiates the released bounds rather than an optimized hypothetical algorithm. Main conclusion: the theorem earns asymptotic rapid-rate independence, but its present conservative construction has no demonstrated practical advantage.

## 1. Inputs and reproducible arithmetic

Use the accepted open zero-field weak-chain binding, n=4,8,16, localized coupling normalization b=1, T=1, alpha_0 T=1, no instruments, and channel tolerances 10^-2 and10^-4. The certificates before scaling are g=19/20, kappa=19/39, h=alpha_H=n, alpha_L=sqrt(2n). After scaling:

    B=20/19, mu=19 lambda/20,
    h=alpha_H=20n/19, kappa=20/39, alpha_L²=40n/19.

The physical high-branch threshold is

    lambda_hi=4096(20/19)^2(39n/19)^2.

Its integer ceilings are305954,1223813,4895249. Evaluate these first points and lambda=10^8,10^12,10^18,10^24. The actual dyadic window is1/256, within a factor two of the allowed19/2560. We add one safe deterministic-window slot, so Wcap=258, and use the source's extra count/call margins.

`resource_ledger.py` computes all30 cases with mpmath interval arithmetic at90 decimal digits. Integer caps use upper endpoints; tolerances use lower endpoints; endpoint floors p0,pz are halved conservatively. Results are in `resource_ledger.json`. The script uses no exponentials of positive lambda-scaled times: rates and very small probabilities are represented at arbitrary exponent, and logarithmic caps are evaluated without underflow. It is a mathematical resource fixture, not a quantum circuit implementation.

The binding source is `../native_lyapunov_source_20261031/NATIVE_FULL_FIRST_EVENT_RECEIVING.md`, SHA f503c80089c85006856e6ca1ea8b536bb36e0aa4931db071320a33a056a07192. The resource fixture uses its count cap, scalar source, OAA normalizer, numerical hierarchy and time floors without replacing them by expected-path heuristics.

## 2. Actual displayed cap ledger

The padded source-kernel slot proxy is

    P_slots=Scap * dA * (Kcap+1), dA=2Aamp+1.

It counts one potential source-kernel interval per padded word slot, per amplification call, per first-event call cap. It is NOT a gate count, nor an intrinsic lower bound on all implementations. The values below run from the high threshold to lambda=10^24; Scap,Aamp,dA do not change across those rates.

| n | epsilon | Scap | Aamp / dA | Kcap range | P_slots range |
|---|---:|---:|---:|---:|---:|
|4|.01|4151|256 /513|1466–1528|3,123,922,221–3,255,948,927|
|4|.0001|4759|256 /513|1610–1671|3,933,042,237–4,081,965,624|
|8|.01|12576|256 /513|1503–1562|9,703,037,952–10,083,675,744|
|8|.0001|13788|256 /513|1645–1705|11,642,559,624–12,066,954,264|
|16|.01|43049|512 /1025|1587–1645|70,070,857,300–72,630,120,350|
|16|.0001|45471|512 /1025|1728–1786|80,584,842,975–83,288,093,925|

This already entails billions of padded interval visits. Each nontrivial interval may contain an LCHS quadrature/selection and slack-amplification routine; each first-event call additionally needs bridge inversion, finite Poisson scans, sorting, projected coupling operations and controlled system evolution. None of those costs is included as a unit gate here. The released theorem only supplies polynomial bounds for several such operations, not optimized numerical gate constants. Turning this table into a gate count by assigning every interval one gate would be false.

The rate growth is genuinely mild: multiplying lambda by roughly10^18 changes Kcap by about60. That is the asymptotic benefit actually visible in the frozen construction. It does not erase the large prefactor and conservative precision costs.

## 3. Precision and expected-versus-capped costs

The exact displayed numerical hierarchy is

    e_step=epsilon/(1000Scap),
    beta=(e_step/(10^6 dA²))^4,
    sigma=(beta/(100Aamp))^4.

For epsilon=.01 at the three threshold points, the required bits for beta are267,273,288; for sigma they are1124,1150,1214. The derived inner time tolerances require3351,3443,3638 bits respectively. With endpoint-strip and bisection comparison allocations, the inner uniform budgets range from3647 bits (n4,epsilon.01,threshold) to4753 bits (n16,epsilon.0001,lambda10^24). The JSON records outer representative-time and outer-uniform budgets separately. These are sufficient source precision budgets, not machine floating-point choices or an optimized necessity claim.

The source leaves the exact total number of elementary kernel/synthesis operations inside a base call to the selected implementation. Therefore no final gate-synthesis bit count is invented. Since there are at least Kcap+1 source intervals in this padded layout, its per-kernel error allocation is at most beta/[10^4(Kcap+1)]. The JSON records only the corresponding necessary precision floor,291–339 bits over these cases. A complete implementation would tighten it further by its actual operation count and LCHS/SVA robustness factors. An earlier informal297–346-bit figure used an illustrative extra100 operation factor; it is superseded here by the explicitly labeled lower floor, not promoted to an acquired exact gate budget.

The actual jump cap is not the expected number of jumps. For epsilon=.01, Mcap is3891,12316,42789. The available MGF plus Jensen gives loose expected-count upper bounds2370.79,9282.72,36731.06, independent of lambda in the high branch. These are bounds, not measured typical counts. The physical process may emit far less. Conversely, the compiled coherent sources still have fixed caps and padded words; replacing every capped routine by its expected length requires a separately proved variable-time implementation. No such improvement is assumed in this audit.

## 4. Ordinary baselines under the same model

### Generic stacked Lindblad simulation

The acquired physical stack has normalization sqrt(lambda)*sqrt(2n). The standard normalized action is exactly bounded by

    tau_generic=1+sqrt(lambda)+2n lambda.

At the high-threshold points this is approximately2.4482e6,1.9582e7,1.5665e8. At lambda10^24 it is approximately8e24,1.6e25,3.2e25. General query-optimal stacked algorithms charge this action plus their precision term. Their queries are not our padded kernel slots: their primitive encodings and additional gates must also be paid. Consequently these numerical columns do not certify a crossover. They illustrate why the asymptotic log-rate theorem can beat that particular general action bound eventually, but not why it beats the best model-specific algorithm.

The freshly checked primary theorem interfaces and gauge qualification are in `../native_lyapunov_source_20261031/NATIVE_PRIMARY_COMPARATOR_RECHECK.md`. In particular scalar-rate trajectory results do not directly receive this dark stack, while generic full-diamond algorithms already retain arbitrary references and compose with prescribed controls. Those capabilities must not be claimed as unique to our construction.

### Direct classical source paths, for the CQ task only

For the rational example q_i=21/20, every flip rate lies between400/841 and441/841 (boundary sites have a narrower range). At physical rate lambda, the expected number of actual Glauber flips in time1 is between those constants times n lambda, for every classical initial source law. Uniformization at total rate n lambda is an explicit exact alternative: each tick chooses a site and accepts its heat-bath flip. Expected ticks are n lambda, including self-loops. The all-trajectory sampler must pay their generation and the intervening system evolutions; if the system is a single qubit these interval evolutions are especially cheap.

This is a baseline for classically labeled source inputs and algebra-preserving controls, not for arbitrary coherent joint source inputs. It is not a lower bound on all classical or quantum simulation methods. Lazy local updates, coupling, reduced memory, elimination and dense solvers may avoid enumerating these ticks. A repeated-observable estimation task also has sampling costs separate from the requested single-channel approximation error; both methods must pay the chosen observation protocol.

### White-noise/elimination alternative

At large lambda a centered source generally produces an order-one effective dissipator, not just its mean Hamiltonian. Fixed-order elimination plus reconstruction/boundary corrections can be much cheaper at a fixed tolerance. Its actual finite-rate uniform error and source/control boundary maps must be supplied. No such general bound is inferred from the numerical check below. Nevertheless, comparison only to microscopic paths is misleading: for lambda10^24 and epsilon10^-4, an honestly certified ordinary effective model is a particularly strong competitor.

## 5. Actual small dense CQ countercheck

`small_cq_dense_check.py` constructs the full64×64 CQ generator for n4, q_i=21/20, H0=X, K=Z_system tensor Z_source,0, T=1. The source begins in its stationary pi and the system in |0><0|. This is a small specified state-output test, not arbitrary-input diamond error.

It also solves the unit-rate classical Poisson equation for f(s)=s_0. The integrated covariance is c_int≈1.001191184807. The ordinary4×4 effective system generator is

    L_eff(rho)=-i[X,rho]-c_int[Z,[Z,rho]].

The comparison uses the actual finite-rate64×64 matrix exponential, not the new compiler. Double-precision `expm` is crosschecked against eigenvector reconstruction, with source trace and positivity diagnostics.

| lambda | finite vs white system trace norm | finite vs pi⊗white retained-CQ trace norm | expm/eig output discrepancy |
|---:|---:|---:|---:|
|305954|1.67e-6|9.79e-4|3.24e-11|
|10^6|5.11e-7|5.42e-4|3.82e-10|
|10^8|at numerical floor|5.42e-5|1.12e-7|

The last system-marginal discrepancy is below the numerical crosscheck's floor and is not reported as a resolved physical error. These are diagnostic state comparisons, not certified channel tolerances, not an all-initial-state elimination theorem and not evidence of correct physical means under every intervention. The dense source table is exponentially large in n, so this particular calculation does not extrapolate as a scalable method for arbitrary large systems.

The useful negative finding is concrete: on this small instance, an ordinary64×64 solve is easy and a4×4 effective system model is already accurate for the displayed observable. Retaining the source raises the finite-rate discrepancy by orders of magnitude, demonstrating why output scope matters. Even then, a dense calculation remains the sensible small-n method. The new worst-case padded construction is not practically competitive here.

## 6. Investment decision

Current evidence supports only an asymptotic, certificate-dependent capability: finite-rate high-precision retained simulation without linear rapid-loss cost. It does not yet establish an end-to-end useful computational regime beyond that theorem. The severe released caps are sufficient bounds, not unavoidable complexity; improving them might matter, but must not be sold as an existing implementation or a practical crossover.

For this localized coupling, a proposed intrinsic-energy count refinement can reduce the global n-dependent activity bound. It is separate, unbound to this ledger, and cannot retroactively change these released figures. It also would not by itself remove source arithmetic, complete-isometry amplification, LCHS calls and their acquisition costs.

Do not pursue another source variant merely to enlarge the theorem's domain. A stronger next investment would require either a genuinely implementable lower-overhead assembly or a concrete task whose best retained ordinary reduced-memory/optimized elimination method has a priced bottleneck. No such winner is earned by this audit. All accepted proofs remain valid capital; the practical and north-star significance remains unproved.
