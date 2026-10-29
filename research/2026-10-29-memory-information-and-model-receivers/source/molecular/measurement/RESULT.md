# Complete-consumer bridge for phase-sensitive recoil spectroscopy

Constructed and internally accepted at MODEL/RECEIVER scope: park the optical
logical SPAN in the ground doublet using an ordinary RF swap and allowed
optical shelving; test the actual return, uncat and fluorescence on coherent
recoil histories. A hot arbitrary Hadamard is unnecessary. Smooth BB1 succeeds
in this bounded consumer despite a standalone hot gate error near.03.

Governing assumptions/proof: [MODEL_AND_RECEIVER.md](MODEL_AND_RECEIVER.md).
Primary sources, strongest ordinary comparison, failures and costs:
[PRIOR_AND_COSTS.md](PRIOR_AND_COSTS.md). The source is a pinned public Ca+/CaOH+
model. No added RF, physical Zeeman assignment, new noise parameter, molecular
coherent pulse or measurement was acquired.

The reusable receiver keeps the finite cross-history kernel. Pointwise
unitarity of U(x)=sum_h exp(i h kx)M_h implies PSD coefficient matrix C with
exact diagonal-sum constraints. The complete output is Tr(CK). Quotienting
phase-invisible Toeplitz terms and certifying PSD Gram matrices bounds a
uniform residual D phase without knowing the molecular Hamiltonian or imposing
a memory-dimension cap. Finite science band, product preparation and a warranted
fixed instrument remain assumptions, not device acquisitions.

A independently consumed the frozen9x9 model kernels, without propagation.
Conservative smooth-BB1 PROBABILITY bounds are:

| Science class | raw Z/Y | nonzero normalized5^3 harmonic Z/Y |
|---|---|---|
| all degree4 histories | .001689 / .001226 | .001087 / .000791 |
| extra initialG/charge promises, q2 reversed | .000554 / .000472 | .000351 / .000304 |

Exact certificates are in `../a_span_transfer_interface/`. Its stipulated
p=.03 two-band control has NONZERO Z/Y harmonics1.7691e-4 /4.2277e-4 and exact
same-model error uppers3.20e-7 /2.19e-7. p is not measured CaOH excitation.
X is a null science control, not a useful substitute because its error is tiny.

Both S levels are bright; modeled optical analysis is included. The reference
analyzer is not automatically an ideal complex-coherence detector: that
interpretation needs another qualified kernel/error term. `NOISE_SCOPE.md`
preserves Wu's explicit magnetic/trap model and distinguishes optical T2 from
unmeasured added-memory noise. The parameterized noisy prototype is UNEXECUTED.
Source contrast0.52 is not assigned to the new instrument.

Added modeled control is182.642us; total Hamiltonian clock about0.539ms before
science delay and all preparation/reset/readout costs. Kernel generation took
.865s CPU; A's final exact receiver5.356s after imports, earlier5.419s preserved.
No physical shots or paid compute. Physical spectroscopy, affordable full-cycle
advantage and historical novelty remain NOT_ACQUIRED / UNKNOWN.

This wave is complete and frozen at its explicit constructive model scope.
