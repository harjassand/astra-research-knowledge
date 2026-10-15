# Source and acquisition index

Retrieved on 2026-10-15. Third-party originals are segregated in third_party.
Acquisition JSON files record exact URL, status, size and SHA256 where obtained.
An HTTP success is not scientific validation. Extracted PDF/HTML text in evidence
is a convenience derivative; original bytes and rendered pages decide ambiguities.

| ID | Primary source | Acquired scope | Use |
| --- | --- | --- | --- |
| S1 | Kautz et al., Nature Materials 25, 1037–1044 (2026), DOI 10.1038/s41563-026-02511-y | Publisher HTML, source-data XLSX MOESM2–5, SI PDF, latest retrieved arXiv PDF | Electrical/conductance observations, source-data analysis, same-regime limits |
| S2 | Grossman et al., arXiv:2511.20174v1 | HTML | Electrical control, current interpretation, sample scope |
| S3 | Herman et al., PRX Energy 2, 023001 (2023); arXiv:2202.01429 | Retrieved arXiv PDF | Prior art and imposed-potential/screening boundary |
| S4 | Herman and Segev, arXiv:2402.09096 | Retrieved arXiv PDF | Coupled ambipolar model, not measured Li/Na response |
| S5 | Rahav, Horowitz and Jarzynski, PRL 101, 140602 (2008); arXiv:0808.0015v2 in retrieved PDF | PDF | Established stochastic pumping and precise no-pumping scope |
| S6 | Mandal and Jarzynski, arXiv:1109.2871v1 | PDF | Periodic-state no-pumping assumptions |
| S7 | Nanocomposite CEM paper, Nature Communications (2025), DOI 10.1038/s41467-025-63660-3 | Publisher HTML, SI PDF, simulation XLSX | Selective ED comparator; acquired XLSX is not measured Li/Na time series |
| S8 | Abels, Yang and Tarpeh, IECR 64, 704–718 (2025), DOI 10.1021/acs.iecr.4c03482 | Publisher search record and public Figshare SI PDF | Na/Li counterflow prior art, draw gradient, measured/model distinction |
| S9 | Bilal et al., ACS AMI 18, 6769–6781 (2026), DOI 10.1021/acsami.5c20493 | Publisher search record and public Figshare SI PDF | Detection-limited Li/Na ED benchmark, pH consumables, test duration |
| S10 | Kong et al., Nature Communications 16, 806 (2025), DOI 10.1038/s41467-025-56071-x | Publisher HTML | Collected lithium-product benchmark |
| S11 | Sarkadi et al., JGP 72, 249–265 (1978), DOI 10.1085/jgp.72.2.249 | Primary abstract through web search only | Historical 1:1 biological Li/Na antiport; no transfer to inorganic membrane |

Stable links:

- [S1](https://www.nature.com/articles/s41563-026-02511-y),
  [source Fig4 workbook](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41563-026-02511-y/MediaObjects/41563_2026_2511_MOESM4_ESM.xlsx)
- [S2](https://arxiv.org/html/2511.20174v1)
- [S3](https://doi.org/10.1103/PRXEnergy.2.023001), [preprint](https://arxiv.org/abs/2202.01429)
- [S4](https://arxiv.org/abs/2402.09096)
- [S5](https://arxiv.org/abs/0808.0015)
- [S6](https://arxiv.org/abs/1109.2871)
- [S7](https://www.nature.com/articles/s41467-025-63660-3)
- [S8](https://doi.org/10.1021/acs.iecr.4c03482),
  [SI landing page](https://acs.figshare.com/articles/journal_contribution/28083343),
  [SI bytes](https://ndownloader.figshare.com/files/51358825)
- [S9](https://doi.org/10.1021/acsami.5c20493),
  [SI landing page](https://acs.figshare.com/articles/journal_contribution/31144398),
  [SI bytes](https://ndownloader.figshare.com/files/61311465)
- [S10](https://www.nature.com/articles/s41467-025-56071-x)
- [S11](https://doi.org/10.1085/jgp.72.2.249)

## Actual data and absent data

The Kautz Fig4 source workbook was read without changing it. Exact input locations
are Fig4b!A3:B356 (dilution), C3:D356 (reference), and E3:F42879 (voltage).
Header cells A2:F2 define units. Conductance minimum is A191:B191, corresponding
reference C191:D191. The first half crossing is bracketed by A187:B188. The last
conductance values are A356:D356. CSV exports retain each original source row.
Fig5 includes model grids and is not wholesale experimental raw data.

Bilal SI PDF pp. S6–S7 contains exemplary pH/conductivity values and summarized
fluxes/voltages. The publisher describes raw Li/Na concentration tables among the
SI contents, but those time-series tables were not identified in the acquired
13-page SI; do not claim a raw Li/Na flux re-fit. Table S3's zeros and infinite
selectivities remain detection-limited source statements. The Na/Li=80 header is
visually verified. Table S2 pH corrections include 50 uL of 0.1 M acid/base.

Abels SI pp. S2–S3 contains process/composition tables, and p. S15 Table S8
distinguishes measured values from model predictions in parentheses. This packet
uses those tables without digitizing experimental curves. Continuous pilot-scale
results in the source are modeling, not a demonstrated pilot here. The 1–5 M
draw gradient is a resource; the low pumping estimate in its comparison table
does not establish a closed-regeneration energy cost.

The nanocomposite ED source XLSX contains twelve sheets of LAMMPS coordinates
and configurations, including initial/final LiCl and NaCl solution geometries.
It is simulation data, not measured concentrations. Its experimental claims are
read from the article and SI only.

No source supplies an acquired Li/Na/Cl response surface, species-gated loading,
reset map, full work series, or repeated collected charge-silent antiport for the
gold/alumina ratchet under the proposed mixed electrolyte.

## Access failures retained

Direct ACS publisher and ChemRxiv PDF requests for S8/S9 returned 403. Public
Figshare search and article APIs yielded SI files successfully, and their article
metadata matches each exact DOI/title. The failed preprint request is not a
downloaded preprint. The attempted Kautz v3 HTML request returned 404; the PDF and
publisher data were acquired separately. The saved 1978 PubMed HTML response had
status 203 and is a challenge page, not an acquired article; only the primary
abstract returned by web search supports S11. These failures do not close any
physical evidence gate.

## Capital and memory use

Read-only capital: W/AGENTS.md, W/00_START_HERE.txt,
W/technology/README.md, W/frontier/dossiers/N774.txt, and exact direct-force
proof W/updates/EZ/synthesis/lattice/REPORT.md lines 87–172 at the pinned revision.
N774's conditional mechanism identification boundary was retained; no physical
parameters or source theorem were assumed for this aqueous membrane.

Memory guidance used only for acquisition/comparator discipline:
MEMORY.md lines 454–466, particularly keeping source evidence, full costs and
equally informed comparators separate. It supplied no ion-transport measurements.
