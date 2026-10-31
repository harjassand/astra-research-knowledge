# Independent whole review: finite-Jensen conductance receiver

## Verdict and exact source bindings

**PASS** for the declared acquired raw coupled-quartic model, exact additional scalar resistance, externally requested total interval width and finite-budget receiving. No correction was required. This is a new receiving operation for the already accepted finite Jensen inequality, not a new physical model, an asymptotic accuracy substitution, or a claim that all requested tolerances are achievable.

I read the complete proof, producer/receiver, author tests, README, costs, executed-results and dependency records. I previously reviewed the exact inherited raw engine and parallel proof/interfaces; their source hashes were checked again. All nine current manifest entries and all seven dependency entries remain unchanged.

- `FROZEN_SHA256.txt`: `abf5200d5425e6952380c4db22a63f7ffe3b63f172d7c53101b5e0005673b632`.
- `FINITE_JENSEN_PROOF.md`: `29cb423e98dd34153a63020f5569a9b6a6333cc1df6c040b916a72f5ef547d57`.
- `receive_jensen.py`: `430d5e82d4ee782cd5fe8069635b4601c54c6b15426dc774ad3ac9f818b00769`.
- `check_finite.py`: `57573489a465d5efc70e5547a7f23f038cf0f15d867f8ea88d72608804389cee`.
- `finite_results.json`: `f79164f2a62dca84e2c5e0b2556f0b3b4f1e48d45242f99bf50dbe6b1578a8af`.
- `check_results.json`: `90e92541e49476f11fc158647464a76b8909a538ea363fd423d4955a9c1743f1`.
- `COSTS_AND_SCOPE.md`: `622511e3ca087befa069d36ca3375f6af3ccbb831a2828e969db9b4e71fe61fc`.
- `DEPENDENCIES.json`: `e97496f6fc55f9285f9a8da881c0f5513b5f26d056f10be965a73ebc511575d1`.

The actual imported raw/scalar source is SHA `45d75db5d0dac774df58070c66d11e9f7d0918bdd903489fdf71b61b9ea03fbf`, with whole receipt `047366599e87f9311bc4b2d933359837472ae4225cb87d4a0e331434b0397a6e`. The finite parallel theorem is source `05eee3b87028cd70a43d65de2a34abe0e0ab4c52213d1b490ce74bbeae8f18f4`, receipt `7411ba7cdcaaf0d623e14802b29d111ad458e07c227cfb978cfd20d56b8141ef`. The additional fixed-factor wrapper receipts are provenance, not substitute proofs of this new arithmetic.

All immutable candidate/pending headers are retained; this later separate receipt supplies the acceptance status. No earlier review script, producer, saved result, timing report or archive was overwritten. The audit artifacts use a dedicated directory named below.

## 1. Mathematical join and normalization

For alpha=m/4, a=1+kappa, v=1+kappa(1-y^2)^2 and Delta=a-v, the accepted finite parallel bound is

    I_minus/I_plus <= k_full/k_free <= 1,
    R0=a^alpha I_minus,
    I_plus=a^alpha integral(2a-v)^(-alpha)dy.

Substituting k_free=1/(beta MA R0) cancels I_minus and both explicit powers of a. Thus the lower denominator is precisely

    R_plus = integral [a^2/(2a-v)]^alpha dy,

and the full finite sandwich is [1/(beta MA R_plus),1/(beta MA R0)]. There is no missing Gamma normalization, slab-length factor or extra a^alpha. The Gamma expectation was used only to prove the already accepted inequality; no Gamma integral, fiber partition evaluation or conditional sampler is needed at runtime.

On the half slab [0,1/2], v decreases, so 2a-v increases and r=a^2/(2a-v) decreases. Its denominator is at least a>0. The identity a^2-v(2a-v)=(a-v)^2 shows r>=v. Hence R_plus>=R0 and its ratio is genuine finite structural slack. No asymptotic theorem is required for the numerical output.

The actual model is still the full isotropic reversible diffusion in the acquired physical coordinates, with the complete raw identity, coercivity, conservative global process and finite Gibbs law earned by the inherited engine. The old explicit unbounded longitudinal tail remains part of MA. Full-fiber boundary conditions and global evenness remain essential. No projected Markov process, fast angular equilibration or arbitrary-state hitting-time relation is introduced.

## 2. Exact added operation and interval directions

`PlusIntegrator` evaluates only the proven half slab. At rational y it constructs positive rational r, computes r^m with the inherited PRE-exponentiation bit guard, and applies the accepted outward integer fourth-root routine. This works equally for m not divisible by4. The inherited monotone Darboux implementation applies because r^alpha is decreasing; the half integral is doubled.

For outward intervals [L_M,U_M], [L_0,U_0], [L_plus,U_plus], the reported full interval is

    [1/(beta U_M U_plus), 1/(beta L_M L_0)].

The lower bound uses upper denominators and the upper bound uses lower denominators. The positive lower mass and old resistance are inherited; positive lower new resistance is explicitly checked. The reported structural-ratio interval

    [max(1,L_plus/U_0), U_plus/L_0]

is also valid: R_plus/R0>=1 analytically, while interval division gives the other bounds. Its upper endpoint cannot fall below1 for a correct enclosure. The inherited free-rate interval remains valid and is checked separately. No obsolete radial factor is used in the new lower endpoint.

I independently checked the special m=4 case against direct exact rational endpoint sums, without relying on the fourth-root implementation to construct the reference integrand. All outward sums and their one-dyadic-unit rounding allowances agreed.

## 3. External TOTAL accuracy and finite refusal

`full_ratio` is either None or a strictly typed Fraction>1, checked before raw acquisition. Its input bit size is bounded by the same effective coefficient budget. Unknown external task keywords are rejected. The inherited exact beta/quadrature tolerance and strict integer budgets are still validated.

The output's exact endpoint quotient is computed as a rational and compared to the separately requested full ratio. This is TOTAL width, not quadrature-only width. A mismatch returns UNKNOWN. The requested ratio and actual ratio are bound by the verifier; changing or omitting a non-None requested ratio does not receive a certificate for that task.

The method does not loop indefinitely trying to eliminate Jensen slack. It executes the inherited bounded quadrature request, performs one added sum on the resulting N/precision, then either admits or refuses. At fixed m/kappa, even an ideal exact integral can leave an intrinsic Jensen gap. Numerical failure therefore does not prove a broad true capacity interval; it says this sufficient computation did not meet the requested task. Any finer subsequent request and its failed work are separately paid.

## 4. Global point, precision and dependency accounting

The program hashes the exact inherited source BEFORE importing it. That engine uses only Python's standard library; this extension is not silently linked to a different Gaussian or determinant backend. It reruns all raw coefficient/axis/kappa/coercivity/full-identity acquisition, mass and old resistance, tail cutoff, adaptive grid, fixed precision and old radial-factor arithmetic.

The available new-point budget is max_points minus the inherited count, including all inherited cached distinct points from attempted refinements and the seed. The added function has its own cache, so even coincident physical coordinates are conservatively charged as new scalar evaluations. Exactly N+1 additional values are needed. There is no reset of the caller's point allowance inside the wrapper. My boundary tests reject a total budget one below this sum and accept the exact sum.

The inherited count is distinct function evaluation count, not a cap on every repeated sum/addition. Adaptive quadrature accumulation, exact Fraction arithmetic and output serialization remain real costs. The power/root-shift guard is not a whole-program memory bound. Its scope is honestly stated. The new largest-power diagnostic likewise does not authenticate peak memory or total arithmetic.

The old radial factor is calculated before being deleted. Its arithmetic/serialization limits can still cause UNKNOWN even when the finite Jensen mathematics itself has no d_min conditioning. The new implementation therefore inherits real incompleteness; independence of the final structural ratio is not zero acquisition cost or admission for arbitrary ill-conditioned inputs.

## 5. Recomputing receiver and tamper scope

The verifier calls the complete producer on ORIGINAL raw input and the externally supplied task. It strictly binds schema/method, scalar source hash, requested ratio, actual exact width, original task/budgets, acquired model except timing, numerical grid/cutoff/tail/precision and all twelve exact endpoints of the six intervals. A stale `factor_upper` field is explicitly rejected. Recursive exact type comparisons prevent integer/bool/float aliases in proof fields.

Optional displays, timing and operation counters are not proof fields. They may differ without altering acceptance. Thus a PASS authenticates the declared exact interval/task and acquisition under this implementation, not arbitrary extra metadata, claimed benchmark performance or empirical physical model correctness. This is a deterministic exact receiver, not a general proof assistant accepting every alternative valid enclosure.

## 6. Actual executions and independent checks

The full source/test/result set was copied into `producer-workspace/finite_jensen_review_20261031` with the inherited engine in the required sibling directory. The original saved files were never regenerated in place.

- All **2,458 author assertions** passed.
- All **seven saved certificates** were actually recomputed from raw fixtures, including the costly m512 case, and passed receiving. The regenerated author report is byte-identical to the frozen report.
- **296 additional exact checks** passed: independent rational m4 Darboux sums, outward root errors, multiple kappa/physical dimensions, pointwise order and monotonicity, total evaluation-budget boundary, exact requested-width equality and refusal, all six interval endpoint corruptions, recursive typed metadata, changed external task/model, invalid slab and pre-power refusal, and beta/graph receiving scope.

Audit artifacts are uniquely located in `audit_control_agent_20261031_1933/`:

- `check_control_agent.py`: `aa758669b105e7f02ebf606647764fcf2bcce07672063925b87a8c9878001240`;
- `independent_control_results.json`: `a761c273e43ceaa15c63f2f8969a35a510a90c343e5dc8a32105646238cd3c83`;
- `author_replay_results.json`: `90e92541e49476f11fc158647464a76b8909a538ea363fd423d4955a9c1743f1`.

Run the independent script beside a COPY of receive_jensen.py, with the copied engine in the sibling `acquired_quartic_consumer`. The script prints its report and does not modify source files. The author test writes reports beside its copied working files; copy before replay.

## 7. Finite consequence and honest scope

The received physical dimension513 fixture has3,069 raw monomials represented by513 exponents each. Its requested full ratio101/100 is actually satisfied: the exact rational interval displays approximately

    [2.369045057852262e-37, 2.384988210037886e-37],

with endpoint ratio1.0067297800574877. This is a finite certificate, not substitution of an asymptotic equivalence. It pays98,305 inherited evaluations plus32,769 additional ones, total131,074, with N32768, cutoff2 and1664-bit dyadic precision. Additional powered numerator/denominator size reaches33,793bits. The reported81-second producer timing excludes fixture creation/import/JSON work and is not a controlled hardware or algorithm-comparison result. Verification here really paid the recomputation cost.

The supported scientific operation is an exact known-model interval for the full isotropic diffusion's equilibrium capacity divided by basin mass, without acquiring the unknown angular partition function. Neither inverse arbitrary-state MFPT, finite-time sampling, angular relaxation, noisy model acquisition, arbitrary coordinate recognition nor physical experimental feasibility follows. Ordinary methods supplied the same finite Jensen inequality can obtain the same result; no separation from ordinary mathematics or exhaustive novelty claim is made. Strong existing variational/free-energy/capacity methods remain comparators, not only blind transition sampling.

**Conclusion:** the proof-to-operation-to-external-task conjunction is sound. All frozen source and dependency bytes remain unchanged. No later fiber-stirring theorem, other receiver or physical interpretation is automatically included in this PASS.
