# Dots separation and aqueous-iron evidence — 23 October 2026

This append-only source update follows the completed Capital intake and the Dots v3 correction in PR #116. It keeps separation/return and aqueous iron as distinct evidence streams. It does not claim a combined process, a winning route, novelty, or practical advantage.

## Separation and return

The Dots report retires the proposed hot pressure-selective return advantage at the current evidence boundary. It retains ordinary cooled bicarbonation, filtration, precipitation and recycle as a comparator. A 2026 petalite study reports about 94% lithium extraction after bicarbonation, but the experiment used a different mineral residue and did not measure final carbonate return, iron recovery, silica removal from a mixed iron purge, or a closed molten-ore loop. The extraction percentage is not a return yield.

The other cited observations are component evidence. A 1970 government evaluation reports a 65 wt% melt fly-ash cake from a different carbonate process; its 50 wt% design value and commercial-filter performance were assumptions. A ferrite study measures phase-sensitive CO2 uptake and a phase transition near 425 C, not lithium/iron recovery from this purge. A molten-salt press-filtration study reports electrolyte extraction from a carbon-nanotube composite, not separation of dissolved silicate or iron-bearing gangue. Battery-leach precipitation data also do not transfer to this mixed purge.

The conditional mass-balance screens use an explicitly chosen 1 kg Li per tonne Fe target and a 1% Fe-loss target. These are design discriminators, not economic thresholds or measured separation specifications. The carbonate-equivalent entrainment variable is not an actual wet-cake melt fraction. No measured joint Fe/Si/Al/Li purge response or complete recovery plant is established.

## Aqueous iron

The 2025 goethite study's Table 1 reports an operando-XRD endpoint containing 34.0% Fe in magnetite, 64.8% in Fe(OH)2, and 1.2% as metal. The paper's 76% Faradaic figure covers reduction into that mixture. The selected exact-arithmetic reconstruction gives a conditional metal-only charge fraction of 513/14950, about 3.43%, using those phase fractions and the reported charge definition. It is not an absolute metal assay, raw-current integration, or cell-energy result. Amorphous inventory and phase quantification uncertainty remain unresolved.

The 2023 hematite paper reports a high-efficiency nickel/H-cell/argon case. Its source workbook's H-cell/argon row stores 4085 C and 0.98 g as theoretical Fe. Faraday's law for Fe(III) to Fe(0) gives 0.7881 g at 4085 C; 0.98 g would require about 5079.5 C. The workbook calculates 0.96444 g experimental Fe and divides by its stored 0.98 g to report about 98.4%. With the Faraday-derived denominator, that mass would imply about 122.4%. This is an internal workbook charge/mass inconsistency. It does not establish super-Faradaic physics, identify which field is wrong, or accuse the authors of misconduct.

The simpler nickel/iron-anode beaker/air control remains a source-supported comparator: its stored charge and theoretical mass agree with Faraday's law, and the workbook endpoint corresponds to about 80.5%. An unpaired mean of two released current traces gives a conditional estimate near 80.0%; per-run mass/current pairing and complete cell and auxiliary energy remain unavailable. The H-cell discrepancy does not invalidate aqueous iron reduction or show that the control is superior.

## Source handling and checks

`source_manifest.json` pins both received archives and all nine selected source members. The Dots return archive's 17 members passed CRC checking; the selected files from the 27-member aqueous-iron archive passed CRC and SHA-256 checks against its member manifest. The two small standard-library scripts included here were replayed from isolated copies; all substantive result fields matched their source JSON receipts after excluding run-specific time and memory fields. The source workbook was inspected read-only. The 2023 raw traces and reconstruction scripts were not replayed by Capital.

The public package excludes the received archives, primary article PDFs, the source workbook, supplementary information, raw current traces, acquisition/access receipts, and private routing data. It preserves producer-authored analyses and result receipts with links to the primary sources.

## Primary sources

- Zaitsev and Zhang, “Metso caustic leach process: alkaline extraction of lithium from petalite and micaceous aluminosilicates,” *Canadian Metallurgical Quarterly* (2026), [publisher page](https://www.tandfonline.com/doi/abs/10.1080/00084433.2026.2650964).
- Singmaster and Breyer, *Evaluation of the Atomics International Molten Carbonate Process* (1970), [U.S. EPA archive](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=9100DXHE.TXT).
- Yanase, Kameyama and Kobayashi, “CO2 absorption and structural phase transition of alpha-LiFeO2,” *Journal of the Ceramic Society of Japan* (2010), [J-STAGE article](https://www.jstage.jst.go.jp/article/jcersj2/118/1373/118_1373_48/_article/-char/en).
- Wang, Licht and Licht, “Green and scalable separation and purification of carbon materials in molten salt by efficient high-temperature press filtration,” *Separation and Purification Technology* (2021), [ScienceDirect article](https://www.sciencedirect.com/science/article/pii/S1383586620321936).
- Ramirez Velazquez et al., “Recovery of lithium from Li-ion battery leachate by gas-liquid precipitation,” *Journal of Crystal Growth* (2024), [DOI](https://doi.org/10.1016/j.jcrysgro.2024.127625).
- Arumugam et al., “Electrochemical Reduction Pathways from Goethite to Green Iron in Alkaline Solution with Silicate Additive,” *ACS Sustainable Chemistry & Engineering* (2025), [publisher page](https://pubs.acs.org/doi/abs/10.1021/acssuschemeng.4c08451).
- Maihatchi et al., “Electrolytic iron production from alkaline suspensions of solid oxides: compared cases of hematite, iron ore and iron-rich Bayer process residues,” *Journal of Electrochemical Science and Engineering* (2020), [DOI](https://doi.org/10.5599/jese.751).
- Fayaz et al., “Deoxidation Electrolysis of Hematite in Alkaline Solution: Impact of Cell Configuration and Process Parameters on Reduction Efficiency,” *ChemElectroChem* (2023), [publisher page](https://doi.org/10.1002/celc.202300451); producer data and supplementary information [Zenodo record](https://doi.org/10.5281/zenodo.10036927) and [SI record](https://doi.org/10.5281/zenodo.8388660).
