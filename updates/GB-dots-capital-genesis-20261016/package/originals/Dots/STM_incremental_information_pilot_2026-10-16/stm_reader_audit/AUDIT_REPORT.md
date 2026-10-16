# Symbolic STM record reader audit

## Decision

PASS for bounded, inert parsing of the qualified format with `safe_reader.py`. Only the three already acquired diagnostic files (00000, 01500, 02920) were read. No additional episodes were fetched or parsed. This is a narrow engineering gate, not proof of a physical fresh scan or policy performance.

The old `inspect_static.py`, both old audit scripts, and their outputs remain unchanged. Do not use the old reader to extend parsing. The new reader was written independently here; it does not import the old reader, NumPy, pickle, or author modules.

## Security and correctness

- `pickletools.genops` tokenizes bytes. GLOBAL names are matched against a four-name allowlist and stored in inert `Node`s. REDUCE constructs an inert node. BUILD attaches inert state. None resolves symbols, imports modules, allocates NumPy objects, invokes a callable, or runs author code.
- File and payload reads are capped at 16,000,000 bytes (file read uses limit plus one). Header length is capped at 4,096 bytes. Opcodes 500,000; memo indices/entries 100,000; stack 100,000; appended items and graph visits 500,000; nesting 64; dimensions 8; elements per array 1,000,000. Cycles fail closed, including memo-created cycles. Alias depths are checked even when a shared subtree was previously validated.
- Only NPY v1, scalar object header, protocol 3, approved opcodes and strictly validated reducer argument/state schemas are accepted. Persistent IDs, extensions, arbitrary class constructors, unknown globals, protocol changes, memo redefinitions, malformed stack operations, duplicate/non-string dictionary keys, and trailing bytes are rejected.
- Numeric types are f8, f4, and b1. Numeric arrays must be little-endian (boolean byte-order-neutral), C-order, exact shape/byte-length matches, finite, and bounded. Boolean bytes must be 0 or 1. Unknown types, endian states, versions, structured dtypes and array schemas fail closed.
- The O8 NumPy wrapper is only a scalar wrapper containing one inert dictionary. Nested arbitrary object arrays are rejected. No object dtype data is deserialized by NumPy.
- Memo lookups reference the same Node object; BUILD mutates that same inert node. Decoding also caches aliases, but raw `parse` identity is the designated evidence. Presentation summaries are not a scientific identity surrogate.

## Semantic changes from old reader

1. Replace assertions with explicit ReaderError checks that remain active under Python `-O`.
2. Bounded reads, full NPY header validation, strict protocol and STOP/trailing-data checks.
3. Explicit resource and graph depth/cycle bounds rather than only opcode/stack/memo counts.
4. Reject malformed mutations, duplicate keys, non-string keys and memo overwrites instead of implicit Python behavior.
5. Validate all NumPy schemas, array shape/length, dtype state, endianness, order, finite values and boolean encodings. Old reader ignored these and unconditionally interpreted bytes little-endian.
6. Restrict O8 to a scalar dictionary wrapper rather than blindly selecting element zero.
7. Memoize presentation conversion, preserving shared-object aliases and avoiding repeated expansion work inside decode. JSON encoding a general alias-rich graph is not an unrestricted export API; use bounded/schema-specific outputs.
8. Accept SETITEM in addition to SETITEMS with the same strict dictionary schema; no other newly executable semantics.
9. Correct scan audit inference: replace `source_supported_new_scan` with `distinct_serialized_image_pair` plus `physical_new_scan_verified: false` and explicit unknown status. Distinct object identity or changed pixel bytes cannot prove physical acquisition; identical bytes cannot disprove one.
10. Compare image bytes directly. No image-byte hashes are generated or exported by the new reader/audit. SHA-256 of whole input files appears only in the separate provenance manifest.

The three diagnostics retain exactly the previous decoded JSON values. Legacy image identity and image-byte equality flags are independently checked and match. Endpoint checks remain: transition alignment, terminal done, goal/end-position distance, terminal-image dimensions and identity, and trace-length consistency. These checks establish record consistency only.

## Hash/predictor boundary

Reader output has no image hash fields and imports no hash library. The audit computes exact equality directly and never returns image hashes. The only hash-producing code is a whole-file provenance manifest in the explicitly separate `input_manifest_audit_only.json`. `scan_identity_audit.json` is tagged audit-only, never predictor input. There is no predictor in this deliverable. Any future predictor must accept only its pre-registered feature allowlist from parsed records and reject all audit/provenance artifacts; do not merge audit output into a feature table. This future boundary needs enforcement in that predictor, not a claim that arbitrary future code is impossible.

## Reproduce

From this directory:

    python -m unittest -v
    python -O -m unittest -v
    python run_diagnostic_audits.py

Both standard and optimized Python runs passed all 12 test groups. Tests use original harmless byte streams, no pickle serializer/deserializer, and the three existing diagnostic files. Coverage includes non-execution, unknown callbacks, invalid operations, memo identity, cyclic/deep graphs, aliased depths, resource caps, headers, dtype/shape/byte-length rejection, finite and boolean validation, and diagnostic equality. Test logs are stored beside this report.

## Residual limitations

This is a hand-audited strict subset parser, not a sandbox or general pickle loader. New legitimate schemas may fail closed and require review before expanding support. No runtime behavior of the acquisition hardware can be inferred from serialized object identity alone. The `d` versus image timing question is outside this byte-parser audit; only equal trace lengths were verified here. Generalization and causal/policy value are not established by three burned diagnostic records.
