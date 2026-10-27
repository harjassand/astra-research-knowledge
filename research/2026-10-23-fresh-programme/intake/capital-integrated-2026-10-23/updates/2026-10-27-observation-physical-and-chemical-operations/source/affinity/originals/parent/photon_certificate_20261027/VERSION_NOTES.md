# Version and failure preservation

Initial reviewed code069bbf1daa7a8ec60904e00885a3d81c52ad9ef863b16ebcabe465db46eb4fa3
was followed by two small API/provenance edits in b7b68de1a9917235f34ea3f415c4eb0f63de0c96924085b700818b948defc9ac:
(1) malformed JSON/Unicode/oversized-integer ValueErrors become InputError,
while InputError itself is preserved; (2) returned governing metadata is copied
rather than sharing a mutable global dictionary. Reversing exactly these two
edits reproduces the069bbf hash; SOURCE_DELTA_069_TO_B7.patch retains the diff.
No confidence, clipping, bias or geometry formula changed.

Root then found a genuine iterator-API completeness bug: next(iterator,None)
confused an actual None item with EOF, potentially accepting a valid N-block
prefix and ignoring a later extra item. File/CLI byte streams were unaffected,
but the public API promise was wrong. Final code uses a UNIQUE local EOF
sentinel and rejects nonbytes/nontext values even after N. It also converts
text UTF-8 encoding UnicodeError to InputError. SOURCE_DELTA_B7_TO_FINAL.patch
retains this diff. The regression covers None before/inside/after valid N,
a further invalid item and malformed surrogate text.

Final reviewed executable:
911c9888e11d858fefa66f0c36c903faa7f9e371fe925ff237d90490675965c9.
Root inspected the final delta and reran all independent code/arithmetic
checks, then recorded completed acceptance at that conditional scope. The
intermediate b7b source/failure are separately preserved by root under
../photon_reader_independent/. Final reviewed snapshot and RESULT.json there
bind the executable version. Copies of final review receipts live here.

All13 worker tests and selected fresh CLI replays pass on the final code.
The earlier API failure is not hidden or counted as a successful certificate.
No failed physical/statistical experiment occurred: every fixture is explicitly
NONPHYSICAL, with no claim that its source, cap, coding or IID premises hold.
Some tool writes were cancelled before dispatch by incoming root messages;
they executed no partial scientific or filesystem work. Full research/debugging
costs were not comprehensively instrumented, and remain UNKNOWN.
