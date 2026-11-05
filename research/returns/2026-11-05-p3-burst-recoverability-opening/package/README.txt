ASTRA - BURST RECOVERABILITY QUESTION SELECTION
5 November 2026

START HERE
Astra_Burst_Recoverability_Question.pdf is the governing 12-page question
dossier. STATUS.txt states what is proved and what is still unproved.

SELECTED QUESTION
The exact heavy-tail boundary for uniformly reliable finite-seed local memory,
including corruptible control/decoding state, finite causal readout and all
finite-horizon resources. The two-dimensional alpha=3 boundary is the first
concrete construction target. The necessity theorem is proved. The local
recovery converse is not proved and no apparatus is claimed.

QUANTIFIERS
Law and sufficiently small fixed positive intensity first; finite seed radius
may depend on them and the fixed accuracy target, but not on the horizon T.
One uniform algorithm may construct different input-independent local hardware
and schedules for each T; that hardware and its execution are charged. The
governing refinement does not require autonomous self-fabrication. Every
mutable information/control/decoding record is exposed to the fault model.

CONTENTS
- PDF, editable ReportLab source build_report.py and extracted report_text.txt.
- check_opening.py, exact/numerical check receipts, and analytic plot files.
- independent/: three independent constructions and audits, with code/checks.
  These are chronological research notes; the main dossier and
  fault_tolerance/uniform_horizon_refinement.md govern the final selection.
- root_screening.txt: the root's rejected energy/locality-only opening.
- SOURCES.json: primary research citations and exact P2 provenance.
- preserved/: the complete preceding productive-control package, unchanged.
  It contains the direct acquired-prevention and first-event predecessors,
  complete independent constructions and their preservation receipts.
- PRESERVATION_RECEIPT.json and SHA256_MANIFEST.json.

REPRODUCE
Requirements: Python 3, numpy, scipy, matplotlib, reportlab, Pillow; DejaVu
Serif/Sans fonts under /usr/share/fonts/truetype/dejavu for the PDF builder.
From this directory:
  python3 check_opening.py
  python3 independent/fault_tolerance/check_opening.py
  python3 independent/first_principles/check_opening.py
  python3 build_report.py
The root checker writes figures/ and results/. The PDF builder recreates the
report in a sibling deliverables/ directory. It creates equation PNGs locally.
The independent scripts test only their declared algebraic/finite examples.
build_package.py records the original assembly and expects the original
workspace layout; it is retained as provenance, not as the extracted-package
verification command. To verify this extracted package, hash every file named
in SHA256_MANIFEST.json and compare with its recorded digest.

SCIENTIFIC LIMITS
The checks do not establish the unproved recurrence or sufficiency theorem.
The plot is a lower bound, not measured or simulated recovery performance.
No laboratory experiment or physical platform reduction was performed.
Strict finite-speed circuits are the governing class. Poisson local clocks
and Lieb-Robinson tails require an additional probabilistic-cone bridge.
The inherited Gibbs, skip-free, repair and loaded-LTI classes remain separate.
No new tournament proposal from another Pro researcher informed selection.
