# Independent audit of the sparse noise-amplification witness

Contributor: `/root/exact_kernel`, 21 October 2026.

**Verdict: PASS for the stated lower bound.** The exact sparse perturbation
proves that operator error can exceed query-Frobenius error by a factor strictly
greater than 7987.62179 on the nine specified saved directions. This is a lower
bound on recovery sensitivity, not an upper conditioning estimate, a new exact
kernel direction, or a fixed-threshold eigenvalue-count ambiguity claim.

## What was checked independently

The producer source `src/sparse_condition_witness.py` and both saved receipts
were read. A separate checker, `checks/check_sparse_noise_audit.py`, reads the
original source files and the frozen perturbation without importing the producer.
It parses the NIST coordinate data independently, reassembles the nine directions,
and evaluates every entry of the 84-by-9 product using Python `Fraction`.

The source K and Lanczos NPZ hashes agree with the separately pinned original
owner data. The 84 core vertices are distinct, in range, and agree with the
producer's input list. Every nonzero perturbation entry lies in an actual
nonzero coefficient position of the original K matrix, not merely a position
with a stored zero. The symmetric coefficient space on this core has 657
independent entries. The perturbation is exactly symmetric.

The query columns are exactly `basis[ell,:,0]`, for ell=0,...,7, followed by
`basis[0,:,1]`. Their denominator is 2^29. The checker selects the same core
rows, directly from those named columns. A perturbation supported on the core,
padded by zero outside it, has zero action rows outside the core; therefore
the checked core-product Frobenius norm is its full 1074-by-9 action norm.

Positive diagonal mass normalization and the fixed scalar do not change a
matrix's zero pattern. Thus a symmetric perturbation with this pattern is also
in the declared pattern class for the normalized generalized operator. The
claim does not impose or prove any additional physical sign, positive-definite,
material-parameter or constitutive constraint on the perturbation.

## Denominators and norm proof

Let `di`, `xi` and `wi` be the saved integer perturbation, query and Rayleigh
vector. Their displayed denominators are respectively

    DD=2^40, VD=2^29, WD=2^29.

The exact perturbation and query matrices are `D=di/DD` and `X9=xi/VD`.
The independently recomputed squared residual is

    sum_(i,l) [sum_j di[i,j] xi[j,l]]^2 / (DD*VD)^2.

It agrees exactly with the producer's `action_Frobenius_norm_squared` field.
The saved positive rational upper bound has square at least this exact number,
so

    ||D X9||_F <=
    152355647336826394610046721 /
    1267650600228229401496703205376.

The vector norm denominator WD cancels from its Rayleigh quotient. The exact
formula is

    |sum_(i,j) wi[i] di[i,j] wi[j]| /
        [DD * sum_i wi[i]^2].

The denominator is nonzero. Since D is symmetric, this quotient is a lower
bound for its operator norm. Independent direct Fraction evaluation gives

    ||D||_2 >=
    304239822459476695160587940129 /
    316912650309844660241760780288.

The independent squared Frobenius norm also matches the producer. It is close
to, but not exactly, one. No part of the argument replaces the operator norm
by a supposed exact unit normalization or trusts the SVD normalization after
dyadic rounding.

Dividing the rigorous lower operator bound by the rigorous positive upper
action bound yields the exact certified amplification lower bound

    350764633871299866675804884458465259865352699904 /
    43913525575758903042522545433103830119651823
      > 7987.62179.

Thus any inverse Lipschitz bound of the form
`||D||_2 <= C ||D X9||_F` on this symmetric pattern class must have C greater
than 7987.62179. The SVD only selected a candidate; the final inequality follows
from this explicit dyadic D and the exact product and Rayleigh checks.

## Scope and limits

This is a lower bound on an absolute noise-amplification factor under the stated
input/output norms. It is not a full conventional condition number, which would
also involve a forward norm. It neither proves injectivity of the whole sparse
reconstruction map nor supplies a verified upper inverse bound. Those are
separate obligations.

The product is nonzero, so D is not an exact indistinguishable-action direction.
No inference about the unweighted CDF at x follows from a large operator norm
alone. The perturbation's orientation, threshold gaps, and feasibility under any
additional restrictions would need their own argument. The exact nonlinear
constraints of a physical stiffness model are not encoded by its zero pattern.

No premise about how the 84-vertex core was discovered is needed for this
existence witness. Its actual vertices, support, query columns and exact action
are checked. Minimality, maximality or uniqueness of that core is not asserted
by this audit.

## Observed resources and preservation

The independent Fraction-check body took **0.15444528399893898 seconds wall**,
**0.152868259 seconds CPU**, with **34,578,432 bytes peak RSS**. Imports precede
the body timer. Source reading, authoring, tool latency and model inference
remain unmetered. No failed check, new SVD, new eigensolver call, or new query
direction occurred.

`results/sparse_noise_audit.json` records the exact recomputed values and costs.
The original producer and replay receipts were not changed; their hashes before
and after the check are:

- Producer: `283689b38d66a2a87f1a4e40fd6624ac141d36ad101322c77549277cb31c4417`.
- Replay: `cd2b779ce52124c87a21c9a23391b8cad694d0f5431ac2f5244104885af9e3c2`.

The independent audit does not reverse the existing full-pipeline cost defeat
or license a precision sweep. Its positive result is the explicit, source-bound
sparse perturbation and the quantified sensitivity it demonstrates.
