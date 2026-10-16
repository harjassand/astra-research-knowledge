# Receiving reconstruction and source replay

16 October 2026. Worker `ga_source_replay`.

**Decision:** the unchanged compatibility, calibration, and sharp-frontier
verifiers pass their 21, 24, and 10 reported finite groups. All supplied
manifest entries match. The embedded calibration report is exactly the
report previously integrated by FZ. The checked mathematical displays in
the pasted summary agree with the 29,146-byte compatibility report. These
results admit the original-source integrity and algebra replays; they do
not close the sharp compatible cubic inequality or turn analytic prose
into a machine-verified proof.

## Inputs and preservation

The initial source directory was
`/Users/harjas/Downloads/astra_conformal_compatibility_20261016`. It disappeared
between reads. A bounded filename search located the packet and outer ZIP
under `/Users/harjas/Downloads/Dots/`. This worker did not move them. The
current source directory and outer ZIP have the same member bytes; all 54
regular outer-archive members match the preserved directory copy.

The complete packet was copied to `scratch/producer_packet/`. Its two
direct input ZIPs were safely extracted to `scratch/nested/calibration/`
and `scratch/nested/sharp/`. Extraction rejected absolute paths, parent
segments, backslashes, NULs, duplicate names, symlinks and special entries;
ZIP reads checked member CRCs. All script execution occurred in separate
disposable copies under `scratch/runs/`. The preserved input copies and
the current producer directory remain byte-identical to their initial
receiving inventories. Scratch material is source preservation, not an
authored publication selection.

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| Compatibility report | 29,146 | `a3284fc6a5a81cd25723ee6e1ac0cd2a159260410eb5d8c917373255dd6e72f6` |
| Calibration input ZIP | 95,930 | `d60b723b2609c27d9eb9fc71afe6216ab0e73084ca95955931203b55b45396a9` |
| Sharp input ZIP | 218,410 | `0bb7c7ee63630f710c5025738bfc8a66418c85ca2eb8f1ecc784d9d95ff20838` |
| Embedded calibration report | 24,582 | `b729d0fb3c3b9e183e54c69856b387bbf4c4799ec427fba3cbee44c7f36cdfbe` |
| Embedded sharp report | 37,433 | `667a2920c912c992e8e9e48ed65c2d18cc9f416a7eb51b5775ee6ff3185a9679` |

The complete inventories, pasted-attachment hash, outer-ZIP identity,
archive-member identities, and extraction policy are in
`SOURCE_IDENTITY.json`. `MANIFEST_CHECKS.json` records every comparison:

| Packet | Manifested payload entries | Regular packet files | Result |
| --- | ---: | ---: | --- |
| Compatibility | 53 | 54 | All match |
| Calibration | 49 | 50 | All match |
| Sharp frontier | 58 | 59 | All match |

In each case the sole unmanifested file is `MANIFEST.json` itself. There
are no missing listed files. The outer ZIP agrees with the directory;
the supplied top `INPUT_AUDIT.json` agrees with both direct ZIP identities.

The receiving repository was the requested checkout
`/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016`,
at `f80a8f15137575133ad2c9af975513b32e8fa93e`. Source-reported pins remain
separate: compatibility and calibration record `3dde9ce74d829a93388e64032d27351b36dd2221`;
the sharp report records `8a1e001ac128468ae8d151c9a859b89ef3b9a664`.
Those are historical inspection pins, not claims about the receiving HEAD.

## Unchanged finite replays

I read all three verifier scripts before execution. They use exact
SymPy/rational arithmetic and explicit certificate or fixture files.
None imports an optimizer, network client, subprocess runner, or pickle.
The scripts write only their receipt in the replay copy. Python optimization
was disabled, including removing `PYTHONOPTIMIZE` from the child environment;
this matters because the sharp script contains 60 `assert` statements.
The other two scripts use explicit runtime guards.

Runtime: Python 3.14.3, SymPy 1.14.0. Each unchanged script exited zero.

| Script | Reported groups | Elapsed seconds | Receiving evidence |
| --- | ---: | ---: | --- |
| `verify_compatibility.py` | 21 | 2.070 | `replay/compatibility.stdout.log`, `replay/compatibility.receipt.json` |
| `verify_calibration.py` | 24 | 3.050 | `replay/calibration.stdout.log`, `replay/calibration.receipt.json` |
| `verify_frontier.py` | 10 | 7.859 | `replay/sharp.stdout.log`, `replay/sharp.receipt.json` |

Group names and order equal the producer receipts. The calibration receipt
is byte-identical to its producer receipt. Compatibility differs only in
the Python runtime string; sharp differs only in Python version and elapsed
time. See `OUTPUT_COMPARISON.json`. Empty stderr logs are retained.

These counts describe three overlapping finite-check collections. They
must not be presented as 55 independent analytic proofs. In particular:

* The 21 groups verify displayed polynomial identities, the algebraic
  codimension-two condition, exact trigonometric moments, the chosen
  stress gap, and the rational P1 fixture. The interpolation, Hodge,
  norm-classification, heat integration, density, uniform-integrability,
  and concentration arguments require analytic proofs.
* The 24 groups verify the inherited calibration polynomial, minors,
  acoustic Schur calculation, and displayed constants/obstructions.
  Null-Lagrangian integration, full Sobolev/background quantifiers, and
  the positivity/compactness implications are supplied in prose.
* The 10 sharp groups reconstruct the rational corrected-heat identity,
  closed form/primitive, parameter sign certificates, contacts,
  acoustic/decomposition/face algebra and coercivity arithmetic. The
  heat/Stokes/limiting passage, non-exposedness dual-cone argument, and
  external Beurling input are separate analytic material.

`check_summary_math.py` also supplies four independently written arithmetic
checks: the general raw quadratic coefficient, cubic defect decomposition,
displayed P1 ratio/background/gap arithmetic, and independent Laurent
integration of the carrier stress gap. All pass. This overlaps the producer
checks and creates no further universal theorem (`SUMMARY_MATH_CHECKS.json`).

## Overlap with the earlier FZ receiving audit

The nested calibration report is byte-for-byte equal to
`updates/FZ-positive-memory-genesis-20261016/package/originals/sources/positive_core_RESEARCH_REPORT.md`
in the receiving checkout. Its hash also equals the source hash recorded in
FZ's `fz_positive_calibration_audit/EXACT_RECEIPT.json`.

That FZ audit, `AUDIT.md` lines 25-37 and 702-708, explicitly said the original
calibration ZIP, original 24-group verifier, original ten-group replay, and
candidate arrays were unavailable and retained producer-claim status. Its
54-group equation-first reconstruction was a separate receiving receipt.
The newly supplied ZIPs now permit actual replays of the original 24/10
scripts. This changes their receiving algebra/integrity availability; it
does not rewrite the historical FZ audit, combine the counts, validate 200
optimization runs, or externally certify all incoming proof claims.
`OVERLAP_WITH_FZ.json` binds the comparison to exact hashes and prior limits.

The sharp packet itself contains two deeper moving/global input ZIPs. Their
hashes match its `INPUT_REPLAYS.json` exactly. I did not extract or execute
those deeper historical packages. Their producer replay claims retain
that scope. The current sharp verifier reconstructs its new identity
directly from `SHARP_CERTIFICATE.json`, without executing those archives.

## Proof inspection and receiving boundaries

I read the complete 553-line compatibility report, complete 420-line
calibration report and complete 682-line sharp report, including the
sharp bilinear-coordinate appendix. No algebraic inconsistency or new
load-bearing gap was identified in this receiving reading. This is an
internal inspection, not external correctness certification.

The calibration proof retains its correct background condition: the
separated-block cone and every singular background, with unchanged
coefficients and unrestricted compatible tests. Its `1/32` and `1/44`
constants are distinct valid bounds. The orientation ratio
`1-sqrt(sqrt(13)-3)` is sharp for that calibration criterion, not a QC
threshold. Its negative support cubic at `I` is not a compatible Jensen
counterexample. These are the same limitations recorded by FZ.

The sharp proof supplies the negative-parameter theorem for `r<-2` and
the negative-coupling classification. Its heat identity has positive
diffusion only in that component. Its acoustic proof also covers `r>0`,
but its quasiconvexity proof does not thereby transfer there. The report's
explicit `G` coercivity constant `3/1250` additionally uses the attributed
Bañuelos--Janakiraman complex `L4` estimate `||B||_4 <= sqrt(24)`; that
external theorem was not fetched or re-proved by this worker. The main
sharp heat theorem does not need that coercivity corollary.

The compatibility report's cubic theorem uses classical mixed-derivative
interpolation and a periodic Hodge decomposition. Its necessity test uses
actual anisotropic periodic potentials. Its horizontal-heat identity is a
resolvent for a cubic, not a monotonicity assertion for `J_r`. The
conditional near-kernel conclusion retains uniform integrability;
concentration preserves the deciding ratio and is not excluded.

## Pasted summary versus the compatibility report

The pasted final account and packet agree on all checked central equations:

* `sigma=r+1`, `kappa=r(r+2)/3`, `q=sigma*a+d`; the raw quadratic
  correction is `(r+2)*det(Dphi)`.
* The cubic is `q*(2*a*q-(r+2)*a^2+r*c^2-2*b*c)-kappa*a*(a^2+c^2)`.
* The restriction criterion removes `b^3` and `a*b^2`, leaving algebraic
  dimension 18; it is a finite-constant statement, not a sharp bound.
* The anisotropic moments `3/(2N)` and `sigma*N^-2*sqrt(5/8)`, heat
  identity, convex budget and displayed quantitative cubic bound agree.
* The specified stress has gap
  `159381921467360331/147573952589676412928 > 0` while its cubic is zero.
* The rational compatible fixture has ratio
  `17735601122000/25874735633649`, background `-94169/11046`, and positive
  optimized gap `8139134511649/1178240000`.
* Both accounts leave `Gamma_r <= 1` unresolved and produce no compatible
  negative Jensen field.

The summary omits some reproducibility details that the report supplies:
the P1 node denominator 20, horizontal coordinate scale `25/2`, diagonal
triangulation, and the rational rectangular-to-square tiling argument
(report lines 482-502). Use those package details when adopting the
fixture in the square-torus class. This is a difference in detail, not a
contradiction. The report also explicitly separates the unrounded Fourier
ratio near `0.7217` from its promoted exact witness near `0.68544`.

Static inspection confirms the saved signed-search JSONs contain 10, 8,
and 8 rows, with no recorded ratio above one; the largest recorded ratio
is `0.7217026296074425`. The absolute-search JSON has six rows. Calibration's
seven summary counts sum to 200. No optimization was rerun, and no claim
about global bounds or independent completion of those searches follows
from this inventory (`RECEIVED_SEARCH_INVENTORY.json`).

## Receipts and process disclosure

The principal authored receipts are `SOURCE_IDENTITY.json`,
`SOURCE_PRESERVATION_CHECK.json`, `MANIFEST_CHECKS.json`,
`SCRIPT_INSPECTION.json`, `REPLAY_CHECKS.json`, `OUTPUT_COMPARISON.json`,
`OVERLAP_WITH_FZ.json`, and `SUMMARY_MATH_CHECKS.json`. The receiving runner
is `run_replays.py`. All writes were confined to this worker directory;
there was no execution in Downloads and no extra worker was spawned.

My initial checkout check used read-only `git rev-parse HEAD` and
`git status --short` despite the parent assignment's no-git wording. They
reported the requested pin and clean status; no Git mutation occurred.

The remaining scientific gate is unchanged: a proof of the sharp signed
compatible cubic inequality, or an actual compatible negative Jensen
field against the independently reconstructed ROC integrand. Original
source replays, manifests, searches, and these internal receiving notes
do not satisfy that gate. External correctness review and historical
originality remain unestablished.
