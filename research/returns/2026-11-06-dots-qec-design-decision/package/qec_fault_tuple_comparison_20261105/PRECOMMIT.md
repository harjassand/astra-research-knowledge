# Same-input bounded published-kernel comparison

Frozen before comparator production. No upstream repository will be run.

Target is exactly qec_fault_tuple_20261105/d21/input_graph.json, SHA256
34da7d8ec1a79176a7e5262baa69fafa49d0742639e92a76e5ccaf249107b493,
with rounded q numerators in parameters.json and the unchanged CircuitModel
integer-weight PyMatching decoder/tie convention. Comparator calculations use
binary64 representations of these probabilities and conventional seeded NumPy
randomness, not outward exact probability arithmetic.

An exponential odds-tilt path is q_i(t)=logistic(logit(q_i)+t), from t=log(8)
to0. Ladder spacing dt=.8/sqrt(sum_i q_i(t)(1-q_i(t))), independent of outcome.
This is a valid auxiliary family of nonuniform edge laws, not a claim to vary
the physical circuit depolarizing parameter. The decoder is fixed throughout.
BAR log density differences are w*(t2-t1)-[A(t2)-A(t1)], where
A(t)=sum_i log(1-q_i+exp(t)q_i). Thus total fault count w is sufficient only
for this explicitly chosen tilt family.

Anchor: 10,000 IID trials at log(8), with additional rejection sampling if
needed to obtain16 independent failure-conditioned starting states.
Two independent published-kernel implementations will each use16 chains,
31 rungs,2,000 burn-in and2,000 retained steps/rung. Warm starts pass each chain's
terminal configuration down the ladder; no candidate-generated samples.

1. Square-root locally balanced single-bit flips (Zanella/Haruna–Murakami).
2. Mullan–Weippert–Brown subregion heat-bath proposal, region probability1/11,
   resampling each selected edge at its current nonuniform q_i(t). This is the
   paper's core-resampling heuristic using ceil(d/2)=11 as a tuning choice,
   not an independently proven minimum failure weight for these weighted edges.
   The proposal is reversible for the product law; only nonfailure rejection
   is needed. Its law is implemented by independent per-edge flip rates
   r*q_i(t) on empty edges and r*(1-q_i(t)) on occupied edges.

Fixed seeds202611054401(anchor),202611054500+j*100+k(Zanella),
20261105460000+j*100+k(subregion). Charge decoder setup, anchor, initialization,
all burn-in/retained proposals, BAR, startup, memory. Each process budget20min,
2GiB RSS monitored. If capped, report partial progress, no completed LER.

Full-ladder cross-chain BAR variation plus anchor variance gives only nominal
99.9% Student-t/delta intervals, not finite-time guaranteed confidence. Report
IAT and conventional Rhat; neither proves mixing. No time-to-matched-accuracy
claim from a fixed-budget miss or unresolved convergence. Any later change
requires an explicit addendum, no silent retuning.
