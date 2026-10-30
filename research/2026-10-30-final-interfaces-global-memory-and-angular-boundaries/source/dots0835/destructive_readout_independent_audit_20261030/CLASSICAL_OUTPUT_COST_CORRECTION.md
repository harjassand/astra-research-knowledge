# Resource correction: linear queue work is not linear complete logical-coordinate readout
2026-10-30. This precise qualification preserves and supplements the original receipts.

## Affected statement
In `INDEPENDENT_REVIEW.md` (SHA b241e391e4bf8b540ddb42dfebdbf891fb7cb194e082fe7d7896f37ffeae55c7), §7 concludes that ideal classical work and memory are O(N). Read as a claim about ALL k=Theta(N) final logical-Z coordinate bits in an arbitrary supplied logical basis, that is too broad. The proved linear bound covers syndrome formation, the sector queue, the correction mask, and formation of the corrected physical bit string. It does not cover a generic final dense logical-coordinate transformation. This addendum supersedes the broader interpretation, without changing the measurement-correctness or quantum-noise proof.

## Correct resource accounting
For bounded-degree CSS checks and fixed local GPT tables:

1. Form the physical Z-check syndrome from N measured bits: O(N) bit work and storage.
2. Execute the current-syndrome X-error queue and accumulate its correction mask: O(N) bit/table work and storage after the fixed local tables are supplied.
3. XOR that mask into the received word: O(N), yielding an N-bit word y in the correct logical coset inside ker(H_Z).
4. To output a SPECIFIED k-bit logical-Z coordinate vector, evaluate a supplied binary map

       l = L_Z y,       L_Z in F_2^(k x N),

   whose rows are logical-Z representatives. For a generic dense supplied basis, the direct implementation costs O(kN)=O(N^2) bit operations and O(kN)=O(N^2) storage for the matrix, in addition to O(N) working/output bits. Generic offline basis construction by ordinary Gaussian elimination can cost O(N^3) bit operations. Word packing or specially structured logical bases may improve these bounds, but no such structure has been earned here.

The total complete k-bit decoded-output process is therefore polynomial-time, with a conservative O(N^2) online classical bit-work/dense-map-storage bound, not an established O(N) bound. The quantum storage/controller apparatus can remain O(N) fixed-dimensional sites; this does NOT make all classical postprocessing resources linear. There is no established constant-latency fully decoded logical output.

## Alternative output representation
One may stop after step 3 and output the corrected N-bit representative y, explicitly stating that its equivalence class modulo the X-stabilizer space is the logical outcome. This is an O(N)-work OUTPUT REPRESENTATION, not literally the fixed k-bit output alphabet of the ideal logical-Z instrument. Its within-coset distribution can depend on decoder/noise details; no uniform representative distribution is promised. Applying the known L_Z map recovers the fixed logical coordinates and the instrument theorem.

## Effect on other receipts and physical claims
The retirement receipt's O(N) queue assertion was a syndrome-to-correction-map statement; it does not construct a linear-cost quantum logical decoder or a dense logical-coordinate map. The finite shutoff receipt likewise imports queue correction only. Every end-to-end claim must keep step 4 explicit when the requested output is ALL k logical coordinates.

Since physical DATA has already been destructively measured before classical queue/parity processing, even the conservative O(N^2) classical latency does not require ongoing quantum memory protection. Reliable classical storage/computation and faithful output transfer remain declared paid primitives, not consequences of the quantum threshold theorem. No noisy-classical theorem or favorable total resource/latency advantage is inferred.
