# Source receipts and reuse boundary

Read `REPORT.md`, then `ASSAY.md`. `calculate.py` generates `calculations.json` using the Python standard library. `READ_RANGES.json` pins the decisive source ranges. `MANIFEST.json` inventories this worker directory. These receipts establish retrieved bytes and analysis provenance, not independent experimental correctness.

## Main pressure-quench paper

- DOI: https://doi.org/10.1073/pnas.2536178123
- Official PMC HTML: https://pmc.ncbi.nlm.nih.gov/articles/PMC12993975/
- Acquired official published XML: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12993975/fullTextXML
- Acquired official supplementary ZIP: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12993975/supplementaryFiles
- Supplementary ZIP SHA256: `93a291ca558b9038c7efa8b4fdbb101e17d2c952e001edb79b3d7d0b25b37578`.
- Published SI PDF SHA256: `a83139a67eecfa9256f8bfbee8b67fd465bffca3b62ba035bfb15ea4fd790b2e`.
- Supplement inventory: `sources/hg1223_europepmc_supp.inventory.json`. Nine entries: one SI PDF and eight article image files. No raw data table/time-series attachment found.
- `sources/hg1223_published_xml_wrapped.txt` is derived extraction with stable line references, not the original XML bytes. MathML flattened text may lose fraction layout; the source XML and original PDFs remain authoritative.
- Visual reads: published SI pages 4–7 (S3–S6), article Fig. 2, and arXiv combined PDF pages 22–25. Renders are under `tmp/pdfs/`. The published SI's S1–S6 caption text matches the corresponding arXiv captions; differences on SI pages 1 and 9 are logged in `sources/published_arxiv_si_text_diff.txt` and not presumed substantive.
- The original absent `astra_pressure_write_audit.zip` was not acquired. The official supplementary ZIP is a different, identified artifact.

## Baselines

- Gapud et al., PRB 56, 862 (1997): https://journals.aps.org/prb/abstract/10.1103/PhysRevB.56.862 . Publisher abstract acquired as HTML. Numerical transport values were verified in the author-posted primary paper at https://www.researchgate.net/publication/230822693_Effects_of_1-MeV_proton_irradiation_in_Hg-based_cuprate_thin_films via web tool; exact returned text is preserved in `sources/film_1997_author_web_receipt.txt`. Direct local retrieval was blocked, and the linked PDF returned 404. Do not call this a locally acquired 1997 PDF.
- Moriwaki et al., Physica C 303 (1998): https://www.sciencedirect.com/science/article/pii/S0921453498002470 . Primary publisher abstract acquired through indexed web result, preserved in `sources/film_1998_publisher_web_receipt.txt`. Direct HTTP request returned 403. Only the publisher portion of that saved result is used; unrelated results are not evidence.
- The adjacent 1999 IEEE paper DOI was resolved from Crossref, https://doi.org/10.1109/77.784953, but its full content was not acquired and its numerical claims are not relied on. Metadata receipt retained to distinguish it from the 1998 paper.
- Li et al., SST 39 055021 (2026): https://doi.org/10.1088/1361-6668/ae6c9c . Publication verified in publisher-deposited Crossref metadata and arXiv abstract metadata. Detailed read is the acquired author version https://arxiv.org/html/2605.05800v1 . Full IOP PDF remains unacquired; the response is an HTML browser check. This is not a pressure-quench replication.
- Hartwig et al., TFMC program, IEEE published paper: https://doi.org/10.1109/TASC.2023.3332613 . Published PDF obtained from KIT, https://publikationen.bibliothek.kit.edu/1000166953/151963422 . SHA256 `9b1b19e0032b2cb417c15720974ca4af2be9272f3161fc3661454fb097eadf3c`; 16 pages. Page 12/Fig. 7 was visually read, alongside the text ranges for the current holds and quench damage. Primary measured system operation is used; no claim of full cost superiority is inferred.

## Failed responses and search limits

Files named `hg1223_main.pdf`, `hg1223_si.pdf`, and `hg1223_irradiation_iop.pdf` are preserved failed HTTP responses with `pdf_magic=false`, **not PDFs**. Their JSON receipts state MIME type and status. No browser challenge was bypassed. Official Europe PMC retrieval resolved the pressure SI access independently. The current report relies on the actual `hg1223_published_si.pdf`.

`sources/data_replication_search_receipt.txt` preserves a bounded exact-title/DOI and repository search. Search engine failure to return a dataset or replication is not proof none exists. No external correspondence, laboratory action or physical measurement was undertaken.

## Astra capital and memory

Read-only checkout pin: `0c789ca775808e23e57138b56a393ad1e58cb15c`, verified at beginning and end. Followed its `AGENTS.md` and `00_START_HERE.txt`; read the technology entry point and only hypothesis-matched N654 conservation/loaded-output ranges. Exact paths/hashes appear in `READ_RANGES.json`. No repository or other worker files were changed.

A lightweight memory pass supplied workflow guidance only: `MEMORY.md:429` and `MEMORY.md:437`, associated with rollouts `01a138d8-86fc-7590-a31c-7de3bb724a5a`, `01a1399d-13fe-71a2-b89b-69206acbcb42`, and `01a13b0f-a137-7362-b163-26280b854b1d`. All material facts in this audit were refreshed from acquired sources. Memory supplied no Hg1223 performance premise.
