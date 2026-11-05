# Restricted higher-dimensional LTI convergence candidate

Date: 2026-11-05. Internal research packet. No publication, priority, or practical-speed claim.

## Useful result

A complete proposed surface/volume argument yields O(1/L) convergence of an explicitly defined rectangular LTI gap hierarchy for positive finite-range interactions whose local kernel is exactly one product-vacuum vector on a full cube. Translates can be fully noncommuting. The construction pads an arbitrary feasible local dual witness with the vacuum and bounds BOTH the seam second moment and the interior/seam cross moment by boundary size, using the bounded objective's sum of disjoint pair correlations.

One-site-translation-covariant finite-depth circuit conjugation transports the result to a concrete entangled PEPS subclass. The explicit example has a square-lattice cluster-state ground state but generic noncommuting parent terms. This is not a theorem for generic injective PEPS, nonunitary filters, sparse supports, or fixed-period circuits without further bookkeeping.

The class was already manifestly gapped. The possible contribution is convergence to the actual spectral-gap value, including the product/circuit-state GNS gap, rather than another proof of positivity.

## Files

- `PROOF_CANDIDATE.md`: exact hierarchy, assumptions, constants, padding operation, GNS identification, and concrete circuit transport.
- `FIRST_INDEPENDENT_AUDIT.md`: first independent near/far and literature audit.
- Sibling directory `lti_rectangular_independent_audit_20261105`: second independent review of the exact frozen proof, geometry tests through p=3, and correlated two-particle witness tests.
- `check_padding.py`: standalone executable operation checks. It does NOT solve an SDP.
- `padding_results.json`: reproducible floating-point results.
- `interaction.npy`: concrete 2x2 qubit interaction used by the checks.
- `resource_accounting.json`: full dense hierarchy cost and conservative proof constant.
- `LITERATURE_AND_STOP_DECISION.md`: closest prior methods and why the generic PEPS route was not claimed.

## What actually ran

The local 2x2-qubit term has vacuum kernel and nonzero eigenvalues from 1 to 2. Two overlapping translates have commutator norm 0.6050580662, so this is not a commuting-projector demonstration.

For a particular translation-invariant one-particle dual witness, complete sparse enumeration of the output H|psi> executed vacuum padding for L=2,3,4,8,16,32. No output amplitude was discarded. At L=32 the complete output had 11,697 configurations. The normalized core energy was L² as required, and the exact first/second moment decomposition was checked. Seam second moment divided by L went from 9.63 at L=2 to 6.27 at L=32; cross moment divided by L went from 10.94 to 12.45. These checks exercise the operation; the general proof, not this selected witness, supplies the theorem candidate.

On a 3x3 periodic example, exact dense diagonalization gave gap 5.3735309115 and a unique vacuum. The circuit-conjugated spectrum agreed within 6.4e-14; the cluster-state ground residual was 5.7e-15 and its single-site entropy was one bit. This small-system gap is not represented as a thermodynamic gap estimate.

## Resource honesty

Already at L=2, R=2, p=2, d=2, the defined SDP variable is a 65,536 by 65,536 matrix. One dense complex128 copy occupies 64 GiB, excluding solver overhead. At L=3 the matrix dimension is 2^36. No such SDP was solved here. The sparse witness tests do not make the general SDP inexpensive.

For the sample bounds c=1,M=2,R=2,p=2, the deliberately loose analytic constant is C=76,712. Using that bound alone to guarantee error 0.01 would require L>=7,671,200. This is an asymptotic completeness result, not a usable error bar at that tolerance or a numerical improvement over existing methods.

## Status

Two independent internal audits found no remaining algebraic defect in the restricted theorem. The second review covers proof SHA-256 a2a3e72ab2b0a35fe72281ffdfee6711c1f270592e64792ffb87ff469f7d036f. Its separate executable checks include positive far-pair correlations and a genuine near-compression-factorization failure that the proof correctly avoids. A targeted literature search found no exact matching strict-vacuum O(1/L) LTI theorem, but originality is unresolved. Existing finite-size, martingale, and PEPS-factorization methods are substantial prior art and already prove many gaps.
