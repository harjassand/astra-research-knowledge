# What normalized hard-sphere output actually enables

The operation constructed in GENERATOR.md and PROOF.md gives independent
unit-weight f_t outputs at any fixed finite time, with finite expected cost.
For a supplied observable phi in [-1,1], the ordinary empirical average of n
outputs therefore obeys

    P(|average(phi)-int phi f_t|>epsilon) <= 2 exp(-n epsilon^2/2).

For J such observables, a union bound changes 2 to 2J. Thus
n>=2 epsilon^(-2) log(2J/delta) is a distribution-free output-sampling
guarantee in the ideal model. No second moment of a random importance weight
is required. This is a standard consequence of the newly normalized output,
not a new concentration inequality or a numerical proof of Boltzmann dynamics.

With a=e0>0 and B,L from PROOF.md, one complete g tree has
E N<=exp(Lt)-1, hence at most 2exp(Lt) expected frames across the final
physical rejection. It has at most 4exp(Lt) expected exponential draws and
2exp(Lt) expected event proposals, with the sharper additive constants in
the governing proof. Finite-table source preprocessing and categorical
selection must be charged separately. Rejection-based g0 construction also
costs (a+R^2)/c raw source draws per g0 draw in expectation.

An explicit high-confidence work cap follows, if wanted, by Markov's inequality:
for n requested outputs and an expected total primitive work bound W, a cap
2W/delta causes at most delta/2 probability of an unfinished computation.
Use delta/2 for the Hoeffding event. An over-cap execution returns an explicit
failure, not a biased substitute sample. This cap can be very large; expected
finite work is not a useful worst-case or long-time complexity bound.

The same claim cannot be assigned to Fournier's weighted output merely by
inserting its observed finite empirical weight variance: E[M_t^2] is not
established by that construction. Conversely, finite-N Kac/DSMC is far cheaper
in the executed comparison, and standard propagation-of-chaos/numerical tools
may qualify its population error on a chosen task. No superiority over that
equally informed qualified route is established here.

The literal program uses binary64 and a seeded generator. Its outputs are
diagnostics of the ideal operation, not exact continuous-law or bit-complexity
receipts. Root's separate finite-bit Maxwell work is not consumed for the
velocity-dependent-rate model.
