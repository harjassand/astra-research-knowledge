# Zero private activation beyond antidegradability

This package preserves one mathematical research note and its layout-preserving source PDF. It is intentionally a package-level route, not multiple frontier cards. No existing claim status or claim-ledger entry was changed.

## Source-reported theorem

Let

`S = {XX, YI, IZ, XZ, IY, YZ}`,  
`F(A) = (1/6) sum_{P in S} P A P`,  
`R(A) = Tr(A) I_4/4`, and `N_q = (1-q)F + qR` for `0 <= q <= 1`.

The note claims:

- `N_q` is transpose-antidegradable for every `q`.
- For `q >= 1/10`, the complementary channel admits a complete variance-dominating Hermiticity-preserving signed lift. Using the cited sufficient criterion, the note derives complete SLD and relative-entropy / less-noisy dominance.
- `N_q` is antidegradable if and only if `q >= q_AD = (3 - sqrt(5))/5`.
- Thus, for `1/10 <= q < q_AD`, the note gives a transpose-antidegradable but non-antidegradable channel whose complement has the stated complete order. It concludes that tensoring with any antidegradable helper still gives zero private and quantum capacity in this interval. It also says every member of this family already has zero unassisted private capacity by transpose simulation.

## Proof structure reported in the note

The note constructs a transpose simulator through the complementary channel, then an explicit Gaussian-rational Hermiticity-preserving unital lift with an exact positive Gram-defect certificate. It transfers the certificate to complete SLD and relative-entropy order using cited sufficient results. Separately, it characterizes antidegradability through symmetric extension of the normalized Choi state, gives an exact polynomial identity for an integer matrix bounding the extension witness, and constructs an attaining symmetric extension at the threshold.

The note reports that displayed identities were checked independently in exact arithmetic. Intake preserved that statement but did not reproduce those checks, reconstruct the proof, or examine the cited literature for priority. The note identifies no external peer review or exhaustive historical-priority result.

## Boundaries and unresolved questions

- The signed-lift criterion is used as a sufficient condition; necessity is not claimed.
- The complete-order transition for `q < 1/10` remains undetermined.
- The sharp threshold proved is for antidegradability, not a general complete-order membership algorithm.
- The result is a scoped counterexample to a proposed activation implication, not a claim that the general activation question or related capacity questions are settled.
- Correctness, external validation, and historical originality remain open at intake.

## Files and source authority

- [`zero_private_activation.pdf`](zero_private_activation.pdf) is the supplied source, copied byte-for-byte. All mathematical formulas and notation in the PDF are authoritative.
- [`EXTRACTED_TEXT.txt`](EXTRACTED_TEXT.txt) is a page-separated convenience extraction using `pypdf 6.19.0`. PDF text extraction linearizes equations and may distort notation; when any expression is ambiguous, use the PDF page.
- [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json) records source hashes, extraction method, page count, and intake limits.

The five pages were rendered and visually inspected; equations, the eigenvalue table, and the page transitions were legible and not clipped. No code or reproducible checker was included in the supplied PDF, and no scientific computation was run during intake.
