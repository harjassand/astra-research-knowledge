# Finite classical meta-selector operation, no environment tomography

2026-10-29 UTC. New construction, pending independent review. The existing accepted baseline-protected theorem is the governing statistical result; this note makes its EXP3 arithmetic and private-expert sampling operational. Physical source instruments remain numerical simulations and quantum-control/pruning synthesis remains separately paid.

## Operation

For square horizon N=s^2, two unnormalized positive INTEGER weights start9,1. Exploration gamma=1/s and learning rate eta=1/(4s). At each call their exact rational expert probability is

p0=[2(s-1)w0+(w0+w1)]/[2s(w0+w1)], p1=1-p0.

Two private fair bits choose the shadow role with probability1/4. On the evaluation role, sample an expert with the above rational probability. Observe the actual positive failure bit ell in{0,1}. Its selected importance estimate is ell/[(3/4)p_i]. If ell=0 leave weights unchanged. Otherwise x=eta/[(3/4)p_i]<=2/3.

`exp_factor` rounds x DOWN/UP to a64-bit dyadic bracket, uses odd33/even32 alternating Taylor sums at the appropriate endpoints to bracket exp(-x), and rounds the LOWER exponential bound down to a64-bit dyadic q. The exact rational relative deficit rho satisfies

0<q<=exp(-x), q>=exp(-x)(1-rho), rho<1/2.

Its upper bound is rounded UP to the same fixed dyadic grid before accumulating. This avoids recursive denominator growth in the debit ledger. Update chosen integer weight by the numerator of q and the other by2^64; remove only common powers of two. No floating exponential, floating normalization, or source/environment matrix is needed. Weight bit length is at most64 times the number of loss updates plus the initial bit length, a deliberately paid polynomial cost rather than unit-cost real arithmetic.

## Arithmetic debit proof

Writing Q for normalized weight probabilities, q<=exp(-x) preserves the usual upper potential bound exp(-x)<=1-x+x^2/2. For comparator j the lower log-weight bound loses at most -log(1-rho)<=2rho on each update to j. Bounding by all updates, the usual EXP3 regret adds at most

2 sum_t rho_t/(eta N)=8s sum_t rho_t/N

to average loss regret. Losses are nonnegative actual failure bits. On the ideal exact-probability evaluation process the importance estimate remains unbiased under the actual current conditional occupation; it does not require iid noise. The additional role selection remains post-source and source-blind. The original theorem's ordinary regret constants can therefore be retained with this added debit. This does not turn that theorem into small-loss or counterfactual policy regret.

## Finite private coins

For probability n/d, draw b=ceil(log2 d) fair bits and reject values>=d. Conditional on accepting, the outcome is exact. At most128 attempts are made; if all reject, select baseline and flag failure. Since each attempt accepts with probability>1/2 (or exactly1 when d is a power of two), failure probability is at most2^-128 per selection. Coupling with the uncapped exact sampler bounds the entire N-call instrument trajectory discrepancy by N*2^-128, including all later retained-memory steering. For a single bounded score this is an additive N*2^-128; for a regret difference between two scores a safe debit is2N*2^-128. The cap event is not silently treated as an unbiased draw. In the simulation Python's seeded pseudorandom bits reproduce the test, not a claimed hardware entropy acquisition.

Unlike sampling a fixed64-bit approximate p, exact rational sampling here can consume O(N*64) bits per draw and O(N^2*64) in total expectation; the deterministic cap multiplies the per-draw bound by128. This is finite polynomial execution, not a claim of optimal practical control cost.

## Actual retained-memory integration

`run_finite_meta_v1.py` keeps the previous high-recoverability source/isometry and exact compressed learner update interface, replaces floating EXP3 with this kernel, and uses separate private bit generation for roles/expert coins. Seeds9301--9303 are distinct from the earlier fixture; the actual conditional occupation is recomputed after each actual chosen measurement. The output includes exact arithmetic/coupling debits, projection certificates, and complete compact acquisition records. Source-defined scores are diagnostics only; the learner consumes recorded labels and flag measurements, not those matrices. Quantum POVM implementation, physical calibration and teleportation control have not been certified by this classical arithmetic test.

## Completed numerical operation, before independent review

The three N1024 runs completed3,072 simulated source calls and772 exact certified learner updates. All actual capped-coin failure counts were zero. Maximum recorded projection gap1.055e-9 is below xi=1/(256*1024^2)=3.7253e-9. New-seed learner means .76878/.82052/.83117 and meta .56547/.60036/.56553 do not establish high-fidelity recovery or an advantage over equally informed adaptive alternatives. They show that finite classical arithmetic can be executed without supplying source matrices to the learner.

The conservative per-run extra average-regret arithmetic debits are661/73786976294838206464,621/73786976294838206464,673/73786976294838206464 (all<9.2e-18). Whole-trajectory coin coupling per run is1/332306998946228968225951765070086144 (~3.01e-36). Each run used11.21--12.43million private pseudorandom bits for expert selection; maximum weight integers were17,333--19,650bits. These are measured classical simulation costs, not zero-cost assumptions or hardware timing results. All certificates and complete acquired records are retained. The exact proof/kernel and new data await independent review; no earlier receipt silently covers them.
