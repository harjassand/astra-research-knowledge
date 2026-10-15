# Acquisition, execution, and scope limits

Date: 2026-10-15. These are scope receipts; none is a mathematical counterexample unless explicitly described in the proof/comparison documents.

- The incoming full audit ZIP was not supplied. Only `regularization_pasted.txt` was supplied DATA. PR94 is a separately pinned acquired source.
- Diamond-Essen1978 and Anderson1969/1970 publisher article/PDF routes returned403; unkeyed Elsevier API routes returned429. They remain unread fulltext priority gates.
- Werner1984 original publisher access failed. Accessible Luef-Skrettingland2017 primary definitions were read instead, with the representation restriction stated.
- Kamynin-Ostrovskii1982 English endpoint returned200 **HTML** at a URL ending in `.pdf`. The preserved `sources/kamynin_ostrovskii_1982_english.pdf` is an HTML response, not an acquired PDF. Its receipt records MIME and magic. Russian MathNet route returned403. No original theorem claim rests on these files.
- Hensley1986 requested publisher PDF returned403. Its abstract was used only for routing. The original Vervaat1972 monograph was subsequently acquired and read for the actual generalized-Dickman theorem.
- Mattner1999 original PDF has an embedded-font extraction problem. Exact mathematical characters were read visually on printed615–617. Rendering emitted font/bounding-box diagnostics, preserved in the render log; the actual page images were legible.
- Vervaat1972 is scanned: pypdf returned empty text for the attempted PDF79–105 extraction. The retained empty page text files record this; PDF97–102 were rendered and visually read. The initial attempt to view `vervaat-97.png` failed because Poppler padded the filename as `vervaat-097.png`; corrected path succeeded.
- The first OpenAI/math recursive root-tree API response was truncated. A nonrecursive root and complete preprints subtree replaced it. No absence claim was based on the truncated tree.
- Two arXiv bytes/metadata mismatches are explicitly preserved: Schwonnek-Werner requested v1 carries a 2018 stamp but internal manuscript date2024; Iksanov-Iksanov requested v2 carries an August2026 stamp while search metadata reported April. Byte hashes identify the actual inspected files. No historical conclusion depends on the search date label.
- The system `python3` lacks requests, and an earlier optional HTML parser lacked bs4. Acquisition continued with bundled Python's standard-library urllib. These are environment diagnostics, not source-access permission failures or proof failures.
- No Lean compilation, external mathematical review, full direct-proof reconstruction of OpenAI's constant-two Crouzeix result, quantum circuit compilation, hardware test, or numerical regularizer replay was performed by this worker. The saved SymPy check verifies only its stated symbolic identities.
- The first phase was independent of construction/adversary workers. Subsequently the parent explicitly coordinated reading the new arbitrary-D, W, and endpoint proof snapshots. No other-worker files were edited and no direct worker-to-worker exchange was used.
