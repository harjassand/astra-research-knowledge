# Primary-source ledger

Accessed 15 October 2026. All listed publications are primary research except the explicitly labelled correction. Public-source observations are reported evidence, not results reproduced here. Short excerpts below are exact; each quoted source contributes fewer than 25 quoted words. Source summaries in REPORT.md are deliberately compact. No paywall, credential or access control was bypassed.

## S1: isotope-sensitive displacement

J. C. Meyer et al., **Accurate Measurement of Electron Beam Induced Displacement Cross Sections for Single-Layer Graphene**, Physical Review Letters 108, 196102 (2012). DOI: [10.1103/PhysRevLett.108.196102](https://doi.org/10.1103/PhysRevLett.108.196102). [Author HTML, arXiv:1203.2372v2, 8 May 2012](https://arxiv.org/html/1203.2372).

Excerpt: "Subsequent sputtering of this atom may effectively double the cross section."

Access: full author HTML and supplementary text inspected. It supports the collateral-risk motivation; no optimized overwrite protocol or collateral count was inferred from it.

## S2: measured rates and visible refill

T. Susi et al., **Isotope analysis in the transmission electron microscope**, Nature Communications 7, 13040, published 10 October 2016. [Main article](https://www.nature.com/articles/ncomms13040), [author HTML](https://arxiv.org/html/1608.04676).

Excerpt: "the vacancy is filled already in the next frame"

Access: publisher main HTML and author HTML inspected. The first PMC open encountered a browser check; another public primary route was used. Supplementary files could not be read by the web tool; the public publisher URLs were downloaded directly with Python urllib. No raw microscope videos were reanalysed.

[Supplementary PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fncomms13040/MediaObjects/41467_2016_BFncomms13040_MOESM333_ESM.pdf): downloaded, p.4 rendered and visually checked. Experimental cross sections in millibarn are:

| Beam kV | Light carbon | Heavy carbon |
|---:|---:|---:|
| 85 | 1.2 (+.8,-.5) | unmeasured |
| 90 | 10.9 (+9.5,-4.8) | 2.0 (+1.3,-.8) |
| 95 | 56.6 (+24.0,-16.7) | 2.1 (+1.0,-.7) |
| 100 | 328 (+119,-87) | 13.3 (+6.0,-4.1) |

The table caption calls these standard errors, whereas Supplementary Fig. 2 explicitly presents CI95 labels. No simultaneous-confidence ratio bound is claimed. Calculations use central values only. Model-only values at 80/85 kV must not be substituted for unmeasured experimental isotope selectivity.

## S2c: correction

T. Susi et al., **Corrigendum: Isotope analysis in the transmission electron microscope**, Nature Communications 8, 15780, 30 August 2017. [Correction PDF](https://www.nature.com/articles/ncomms15780.pdf).

Excerpt: "the labels ‘12C’ and ‘13C’ in the key should be reversed."

Access: correction PDF text inspected. It corrects Fig. 3c and Eq. 23. Interpret the original isotope-map key accordingly.

## S3: repair and sculpting conditions

Q. Xu et al., **Controllable Atomic Scale Patterning of Freestanding Monolayer Graphene at Elevated Temperature**, ACS Nano 7, 1566–1572 (2013), published online 30 January 2013. DOI: [10.1021/nn3053582](https://doi.org/10.1021/nn3053582). [Author-hosted PDF](https://ceesdekkerlab.nl/wp-content/uploads/Controllable-Atomic-Scal-Patterning-of-Freestanding-Monolayer-Graphene-at-Elevated-Temperature.pdf).

Excerpt: "self-repair is faster than carbon removal"

Access: complete author PDF downloaded and text inspected. This high-temperature 300 kV apparatus is contextual repair evidence; its parameters were not treated as the 95 kV isotope writer's measured repair law.

## S4: strongest demonstrated small-period comparator

E. Whiteway, M. Lee and M. Hilke, **Real-space Raman spectroscopy of graphene isotope superlattices**, Physical Review B 102, 235429, 23 December 2020. [Publisher article](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.102.235429), [author HTML arXiv:2007.12272v1, 23 July 2020](https://arxiv.org/html/2007.12272).

Excerpt: "superlattices with periods as low as 6 nm"

Access: publisher abstract and full author HTML, including synthesis method, inspected. The report attributes the period claim to this primary article; it does not claim atomically resolved compositional interfaces were measured.

## S5: strongest local isotope-growth comparator

R. Senga et al., **Imaging of isotope diffusion using atomic-scale vibrational spectroscopy**, Nature 603, 68–72 (2022), published 2 March 2022. [Publisher article](https://www.nature.com/articles/s41586-022-04405-w), [author manuscript arXiv:2306.15861, submitted 28 June 2023](https://arxiv.org/abs/2306.15861).

Excerpt: "the crack was closed by embedding with a newly formed graphene domain."

Access: publisher abstract/search text; publisher full web open failed with a redirect. Publisher date metadata was subsequently verified through public urllib access. Full author PDF downloaded and text inspected, especially manuscript p.5 for growth conditions. The author version, posted after journal publication, is the version used for the numerical growth comparison. No supplementary movie replay or isotope spectrum fitting was performed.

## S6: separate Si-handle gate

M. Tripathi et al., **Electron-Beam Manipulation of Silicon Dopants in Graphene**, Nano Letters 18, 5319–5323 (2018), published online 27 June 2018. DOI: [10.1021/acs.nanolett.8b02406](https://doi.org/10.1021/acs.nanolett.8b02406). [Author manuscript arXiv:1712.08755](https://arxiv.org/abs/1712.08755).

Excerpt: "are consistent with 13C atoms"

Access: complete author PDF plus public primary text inspected, including the 150 ms detector feedback and the two outlier waiting times. The tentative isotope explanation is preserved as tentative. No isotope-rate classifier was acquired or validated.

## Acquired-byte receipts

Receipts establish byte identity only. They do not validate claims, experiments or historical novelty.

| Local file under sources/ | SHA256 |
|---|---|
| susi2016_supp.pdf | d2c6440e99c512aabf7cec87c875aaeab394062ccb6f780e80e0fb02d6c15e50 |
| susi2016_data2.txt | b4899fe2805ae9387b196cbfe0964f28d2717ef2fa24099d8ecc77d3831093b7 |
| susi2017_corrigendum.pdf | db24ed86586cba4e8987d75454ad55c3fa1b2dbaee3091ec64b0b9bda50005bf |
| xu2013.pdf | 109d6a71b947ffec5e3c29639602a82aefafd7f0efbd8fbf6572257a73be12dd |
| senga2022_author.pdf | a0e15bbdccab6e808250352396fa33a05b64537c26b1099ad45c393a9e570202 |
| tripathi2018_author.pdf | 3ec0baf940eac6318a469b34c3c2966f119324a9a49b9ce48ef8bd573450bb5d |

The downloaded Susi data file is an acquired Mathematica-text supplement, not an executed script. It was preserved without execution. Extracted-text companions are navigation aids; consult original PDFs for table structure. The visually reviewed table render is sources/susi2016_supp_p4.png.

## Priority-search boundary

Targeted public searches covered isotope-selective sputtering, electron-beam isotope enrichment, isotope exchange/healing, isotope superlattices and isotope-dependent Si bond inversion. They found strong existing writing and manipulation comparators but did not establish priority for the exact event-conditioned natural-feed protocol. Absence from these searches is not novelty clearance. Patents and reviews were search leads, not evidence of a demonstrated superior operation.
