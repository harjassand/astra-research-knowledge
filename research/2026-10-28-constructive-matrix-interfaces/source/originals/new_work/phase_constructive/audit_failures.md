# Retained audit failure: target-variation harness

The first E6 audit passed all 825 geometric pair-of-flag types, all 36
independent finite-field rank/phase histograms, the raw 72-input circuit,
its separate left-matrix linear-solve oracle, 128 original-gate evaluations,
and all 256 affine phases at the native target. The final target-variation
loop then failed the existing one-joint-simple-copy admission check.

The fault was in the new audit harness: `source_free_program` shifts the
quadratic frontier by constants before its reversible suffix. The loop
changed targets in the original output-mixing coordinates without carrying
those constant shifts into the actual acquired frontier. The resulting
target was a different vector and could occupy several joint simple copies.

The corrected harness recovers the frontier correspondence from actual ANFs,
including each constant shift, verifies that it maps the planted native
target to the target acquired from the original circuit, and applies that
same correspondence to every varied target. The production E6 algorithm
was unchanged. The check correctly rejected the malformed audit input.
