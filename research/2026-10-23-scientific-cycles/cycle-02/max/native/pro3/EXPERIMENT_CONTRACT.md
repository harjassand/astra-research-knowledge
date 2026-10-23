# Calculation contract

The research question and complete mathematical contract are in
PREFIX_THEOREM.md. This file distinguishes its computations from scientific
observation and fixes what their outputs mean.

## Inputs

No empirical dataset, fitted estimator or laboratory intervention is used.
All new numeric inputs are explicitly specified in the scripts:

- Principal scalar calculations: K=1, alpha=1/2; epsilon in
  {0.1,0.03,0.01,0.003,0.001}; additional K-dependence at
  K in {0.1,1,4,8}. Standard-library Decimal at 80 and 120 digits.
- Exact prefix checks: 30 positive rational finite chains, deterministic
  pseudorandom seed 20261021, five thresholds and eight prefix lengths.
- Exact competition checks: three rational parameter triples,
  five prefix lengths and five post-prefix times.
- Exact integer-boundary checks: K=log(2), alpha=1/2, with epsilon
  immediately below, at and above five exact geometric boundaries.

## Outputs and checks

The principal calculates the proved floor, integer critical/safe counts
and sufficient-bound budgets. Its bound search uses a 5% error margin
in the rounded evaluation. It claims neither global optimization of
certificate parameters nor actual mixing times.

The exact checks compare finite laws and formulas using Fraction.
They contain no tolerance. The two Decimal runs compare all saved
scientific values, with integer counts/log budgets required to agree.
A relocated replay checks all five new script configurations without
mutating the source or original receipts.

The written proofs, not these selected instances, establish all universal
statements. These diagnostics are not independent scientific measurements,
a random holdout, a preregistered discovery test or evidence of application
adoption. Some parameter choices were made after deriving the proof to
check its critical identities.

## Resource comparison

The ordinary comparator is proposal-start pure independence MH with
the same target/proposal information and population forward-KL contract.
Its sharp exponential coefficient is K. The principal also evaluates
its explicit common-proposal coupling bound for numerical context.

At fixed t, the prefixed hybrid costs N initial candidates, expected
alpha*t/2 further global proposals and expected (1-alpha)*t/2 local
transitions. Any wall-clock comparison must also price L and evaluations;
no such application-specific timings were measured. Exponential values
are represented by logarithms and were not executed as trajectories.

## Execution and acceptance

First recorded new diagnostic executions passed. Numerical agreement is
reported separately from mathematical review. SOURCE hashes and the
exact proof binding are recorded in REVIEW_BINDING.json.
