# Exact endpoint limits, local factories and complete costs

[Return guide](README.md) · [Complete supplied response](P3_NOISY_PREPARATION_CONSEQUENCE_20261105_RETURN.txt) · [Structural and physical operation](full-rank-blocks-and-noisy-operation.md)

## An attaining obstruction

For the Heisenberg dimer `H=(XX+YY+ZZ)/3`, the Gibbs state is `(I-t(XX+YY+ZZ))/4`, with `t=(exp(4 beta/3)-1)/(exp(4 beta/3)+3)`. Compulsory depolarizing endpoints of Bloch contraction `lambda` have exact optimal error, over every possible input state,

```
inf_sigma D((D_lambda tensor D_lambda)(sigma),rho_beta)
    = (3/4) max(t-lambda^2,0).
```

Werner twirling reduces the optimization to one parameter; a preimage of parameter `min(t/lambda^2,1)` attains it. There is an entangled exactly reachable interval when `lambda^2>1/3`; at `lambda=0.8` the reported interval is `0.823959<beta<=1.569926`. This is endpoint-channel reachability, not 20% controller-fault tolerance. Fixed endpoint noise excludes sufficiently cold dimers; the single-spin condition `lambda>=tanh(beta h)` similarly shows why fixed temperature and bounded strengths matter.

Uniform finite-volume reachability also gives positive preimage limits for a compatible infinite family. With depolarizer replacement probability `gamma` inside the sufficient radius, complement postselection in the exact Gibbs state retains `rho_(A|y)>=gamma^|A| I_A/2^|A|`. Approximate delivery incurs error divided by outcome probability; no implemented uniform guarantee for arbitrarily rare conditioning is claimed, nor priority over established Gibbs comparability results.

## Separate weak-factory and assay deductions

At high temperature, established classical product-state samplers already cover noncommuting Hamiltonians. If actual local factories deliver all Pauli states of radius `r_i`, the source gives an apparatus-weighted sufficient condition using `J_app=max_a |J_a| product_(i in supp E_a) r_i^-1`:

```
beta J_app <= 1/(200 K max(1,d)).
```

Here `K` is locality and `d` dual-graph degree. A positive parity mixture implements the sampled factors. Even entanglement-breaking local factories can suffice for sufficiently mixed known targets. Actual palettes, independent refresh and noisy selection must still be acquired; convex-hull tests do not identify arbitrary unknown apparatus.

A narrower completed factory programs preparation probabilities directly from fresh noisy assays. Strictly interior affine functions use unbiased expectation with rare clipping; positive rational settings use a Bernstein rejection race with a finite deadline. At fixed templates and positivity margins, `R` factors cost `O(R log^2(R/epsilon))` fresh assay invocations. Established Bernoulli-factory theory is credited.

For a concrete scalar factory `(I +/- kappa Z)/2`, noisy contrasts `m1=A kappa`, `m2=A kappa^2` program a positive routine with weight `(m2+r m1)/(2m2)`, delivering `(I+rZ)/2`. A symmetric noisy selector and matching homogeneous probe are required. Independent unknown SPAM or arbitrary asymmetric selectors are not covered. The conservative reported example costs 222,912 assay-template invocations per output for `R=1000`, `epsilon=10^-3`; it is neither practical nor optimality evidence. This narrow route does not replace the general all-temperature acquisition bill.

## Strong comparators and full resource conclusion

The source compares established error precompensation, pure bounded-block Gibbs preparation, the newer quantum Dobrushin–Shlosman sampler, fault-tolerant/qLDPC I/O, autonomous 2D dissipative QCA and noisy ETH-based Gibbs preparation. The fastest listed ideal 1D comparator has better size/accuracy scaling than this source sampler. Generic local-stochastic residual output noise is not automatically the required independent product boundary. An ordinary fault-tolerant machine can use the new state theorem with the same machinery and access; no superiority is inferred by withholding them.

The full bill includes source sampling, bounded-block matrix work, protected computation, routing, acquisition, noisy regeneration and reset. Ternary tree export uses `2N 3^h` leaves with `h` logarithmic in `N/epsilon_tree`, giving additional polynomial inverse-accuracy cost. Conservative endpoint-law acquisition requires `O(epsilon/N)` precision; shared-template savings require the actual shared deployment. The exponential finite-bit fallback is charged separately.

Constants are prohibitive. The stated conservative base length is `ceil(exp(r max(1,beta) 2240^(2r)))`; already `r=2,beta=1` gives exponent about `5.0e13`, before later bounds. A positive uniform radius is earned; useful engineering numbers and a total-resource advantage are not.

The source reports passing separate algebra/composition audits, two finite suites and final finite-arithmetic audit. Examples include softened spectral residual `4.64e-15`, mixed-Pauli trace error `4.44e-16`, a nine-qubit variable-cut ring mixture error `3.26e-16`, nonunital inverse restoration, exact dimer attainment and rational-probability identities. These retain their finite scopes and are not a reconstruction of the enormous sampler, physical experiment or threshold measurement. Capital ran no scientific checks. The original report and check files are delivered unchanged. The complete accepted predecessor ZIP matches its published original byte-for-byte, without a science re-audit or change to earlier results.
