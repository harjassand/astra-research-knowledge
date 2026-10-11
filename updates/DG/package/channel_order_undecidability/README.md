# Undecidability of complete quantum channel information order

This package preserves the supplied 27-page research note as a single source record. The PDF is authoritative; the page-separated `EXTRACTED_TEXT.txt` is a convenience route for web retrieval and may linearize or distort equations.

## Source-reported results

The note claims that complete symmetric-logarithmic-derivative (SLD) information order on finite rational-complex strictly positive POVM pairs, with input dimensions and outcome counts supplied as part of the instance, is coRE-complete; failure is RE-complete. It further claims that for arbitrary finite-dimensional channels, complete SLD order is equivalent to unrestricted complete Umegaki relative-entropy order, where all finite untouched references and all input-state pairs are allowed, without an equal-reference-marginal restriction. It claims no total computable reference-dimension bound from the rational POVM pair can witness every complete-SLD failure.

A separate source-reported theorem defines a bounded entropy defect `V(E,F)` for strictly positive POVMs and claims that it has no total algorithm for arbitrary requested rational additive accuracy; the note strengthens this to impossibility at fixed additive error `1/4`. This uses a computable witness margin and tensor amplification, not merely the exact-order undecidability argument.

The note imports a finite nonlocal-game promise from MIP*=RE as its external complexity premise. It describes a reduction through an actual normalized two-factor Jordan domain, a Pauli anchor, local completely positive smoothing, an ordered-word inverse-Jordan compiler, positive rational measurement effects, and global completion. Its computability upper bound enumerates rational faithful states, tangents, and finite reference dimensions. These are all claims from the note; this intake has not reconstructed or certified those arguments.

## Scope and relation to existing Astra records

The source explicitly limits its hardness theorem to generic complex POVMs and does not claim hardness for transpose-compatible or restricted subclasses, fixed input dimension, equal-reference-marginal entropy order, numerical contraction coefficients, or a general Hermiticity-preserving-lift characterization. It does not claim an efficient witness-finding procedure.

This is related context for the existing complete-information-order family in [DD](../../../DD/package/quantum_information_orders/README.md), including [N661](../../../../frontier/dossiers/N661.txt). The relation is not a logical dependency or validation: N661's reported finite sufficient lift certificate does not provide a general decision algorithm for the broader generic class, and the undecidability claim here does not refute that certificate in its stated setting. No earlier DD source or checkpoint is modified.

## Evidence and intake limits

- `channel_order_undecidability.pdf` is the user-supplied original, copied byte-for-byte (SHA-256 recorded in `SOURCE_MANIFEST.json`). It contains the mathematical notation and source status.
- `EXTRACTED_TEXT.txt` contains all 27 pages extracted with pypdf 6.19.0 and explicit page separators; consult the PDF whenever extraction is ambiguous.
- The PDF identifies itself as AI-generated and not peer-reviewed, and says originality and historical priority are unconfirmed. No independent proof reconstruction, formal proof, external correctness audit, or exhaustive priority review was performed here.
- Static intake checked the page count, source/copy identity, source hashes, extraction presence, metadata and repository routes. Those checks establish preservation and retrieval only, not theorem validity.

The relevant established external premise cited by the note is [MIP*=RE](https://arxiv.org/abs/2001.04383). Citation of that premise does not independently validate the note's reduction or its use of the cited game properties.
