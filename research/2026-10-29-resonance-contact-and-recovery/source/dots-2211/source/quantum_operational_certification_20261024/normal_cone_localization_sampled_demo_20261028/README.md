# Executed ordinary common-bank localization with exact score certificates

28 October 2026. Author demonstration; separate audit pending. Governing received mathematics: normal_cone_all_interval_localization_20261028.md and normal_cone_common_bank_variance_refinement_20261028.md, with their version-bound receipts. This package executes the statistical guard on an actual simulated bank rather than reporting only a required budget.

## What was executed

The source is the two-output qubit channel

 N(rho)=[I+(4/5)sum_j r_j sigma_j tensor I+(1/10)r_Z I tensor Z]/4,

followed by distinct fixed rational rotations on BOTH output sites and a hidden SWAP. The learner does not receive those parameters, rotations, swap or probability table. Both physical sites carry input information; in particular the gauge site has a nonzero signed Z-input contrast. The old inference 'every disjoint signed contrast vanishes' is not licensed here.

PREDECLARED_DESIGN.json fixed all three bank sizes, seeds, beta allocations, t=9 confidence-log upper bound and arithmetic precision before the first generation call. Its hash is retained in RESULTS.json. The timestamp is a human-readable design label; the verifiable ordering is that the file was written and hashed before generation in the original run. The three banks are independent acquisitions, not prefixes or selected favorable repetitions. SOURCE_ONLY.json is used only by the generator and post hoc scientific validation; it is not passed into learner().

For every call the generator individually draws a logical XYZ input axis/sign, both physical readout axes and a joint binary output pair. Joint Born probabilities are EXACT rationals with common denominator1800. A uniform integer chooses each output pair; the two outputs are not incorrectly sampled as independent marginal coins. Every raw record is saved in the named NPZ, with integer signed sums. No outcomes are discarded.

Total:75,776 simulated source calls and151,552 physical Pauli readouts across three banks. This is numerical source sampling, not laboratory data or a hardware-qualified random/control implementation.

## The learner and rigorous numerical witness

learner(records,design) uses only observed input/readout/outcome data. For each site it forms rational contrasts M_kj=9 sum(1_inputj 1_outputaxisk s outcome)/N. All interval scores therefore refer to the same actual bank; with w=1 the complete all-length family is the two single-site intervals.

A floating eigenvector only PROPOSES a decoder quaternion. Rounding its four coordinates to integers and normalizing through the rational rotation formula produces an EXACT SO(3) matrix. The script checks Q^TQ=I and detQ=1 algebraically. This is a physical unitary decoder witness, giving an exact rational primal objective.

For the dual it proposes a scalar Y=y I. The complete4x4 Hermitian slack yI-Hhat is checked by ALL15 principal minors using exact rational/complex arithmetic. All are nonnegative. This is a genuine full-CPTP dual bound, not an SVD or solver convergence flag. A rational Gershgorin fallback is coded and checked if the floating proposal ever fails; it was not needed in these banks. Each certificate stores its quaternion, rational primal/dual objectives and all minors. No assumption that the true source is a unitary or that its output is unital is used by these witnesses.

The t=9 bound is justified by an exact rational Taylor lower bound proving exp(9)>3600=2M/beta, with M=18,beta=.01. Square roots in the variance radius and score halfwidth are rounded UP by exact integer arithmetic to the predeclared denominator10^9. These are formal simultaneous confidence allowances, not empirical fit errors. Exact rational comparison then applies the strict disjoint-competitor guard.

## Actual outcomes, including the failure

- N=2,048: ABSTAIN. Score halfwidth0.4034122. Gauge interval[0,.7220635], logical interval[.4248471,1]. Neither strict guard passes.
- N=8,192: ACCEPT physical site1 (the second output). Logical lower0.6601734 exceeds gauge upper0.4771806. Score halfwidth0.1921917.
- N=65,536: ACCEPT the same site. Logical interval[.7868750,.9184260], gauge interval[.2050057,.3365567]. Score halfwidth0.0657755.

Each bank has its separately declared beta=.01 guarantee under the theorem's sampling/model assumptions; the union bound over the three banks is .03. These are frequentist guarantees for the prescribed procedure, not posterior probabilities conditioned on acceptance. The true logical site is consulted only AFTER the learner's decision for validation.

The source's actual oracle fidelities are17/20=.85 on the logical site and11/40=.275 on the gauge site. The normalized global Choi has floor at least1/80, and its true extractor dual gap is3/4. These generator-side facts establish a physical fixture and explain why a genuine score separation exists. They are not learner inputs.

## Reproduction and scope

Run python run_demo.py. It regenerates all raw records, exact score witnesses, rational confidence bounds and results from the predeclared seeds. NPZ archives contain raw records and signed sums; byte-level record hashes are reported, while compressed NPZ metadata bytes need not be deterministic across executions.

This demonstrates executed confidence-qualified localization for the wider normal-cone source family with visible gauge contrast. It does not execute the later local generator fit, full recovery circuit, retained-memory trajectory, generic SDP compiler or hardware controls. The equally informed conventional learner could use the same standard recovery SDP witnesses and data. No generic practical advantage, historical novelty, broad unknown-noise solution or Capital integration is claimed.
