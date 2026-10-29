# Primary comparison: opaque-channel recovery
2026-10-29. Selective source comparison, not a historical novelty certificate.

## Direct physical predecessor that must not be omitted
Utsumi, Nakata, Wang and Takagi, *Quantum algorithms for Uhlmann transformation*, arXiv2509.03619v2, https://arxiv.org/pdf/2509.03619v2 , Sec IX, Proposition33, Eqs403–410 (PDF pp41–42).

This paper already constructs approximate physical Petz recovery from forward channel access and reference-state samples, without supplied Stinespring/inverse access. Its construction synthesizes canonical purification and Uhlmann operations. Equation407 displays ambient output-dimension and minimum-output-eigenvalue dependence; Eq404 also includes a Choi-eigenvalue dependence or a larger dimension-based alternative. The square-root block-encoding components require additional costs not developed there. Therefore “physical recovery from forward-only unknown channels” is NOT an appropriate new-capability claim for our work. Our candidate distinction is ambient-output-dimension-independent, spectrum-free near-optimal recovery under bounded hidden output support, using joint quantum records and later payload compression. That distinction needs comparison against further work and does not itself establish novelty.

## Random dilation predecessor and interface boundary
Yoshida, Niwa and Murao, *Random dilation superchannel*, arXiv2512.21260v1, https://arxiv.org/html/2512.21260v1 , Theorems2,3,6 and SecIV.

Theorem2 physically converts parallel channel slots into a mixture of common random dilation-isometry slots. It includes known coherent preprocessing on all channel inputs. This is a significant stronger established resource conversion, but not free reusable inverse access, nor an operation that merely appends a synthesized environment to an already-encoded later payload. Theorem6 gives exact probabilistic Petz for the special least-Kraus-rank case r=dI/dO, which implies dI>=dO. Our expanding hidden-support setting is not directly that theorem's case. SectionIV explicitly discusses the difficulty of extending the first construction to sequential access. A useful new bridge must preserve these input-timing distinctions.

## Recent polar implementation
Zhao and Xu, arXiv2610.20515v1, https://arxiv.org/html/2610.20515v1 , Introduction and SecIV.

This develops a single-polar/QSVT implementation of Petz, with explicit block-encoding circuits and spectrum-weighted approximation objectives. Its Introduction expressly cites the Uhlmann predecessor for synthesizing dilation access and virtual recovery as a different interface. Thus neither polar structure nor the standard squared-optimum Petz guarantee should be presented as new here.

## Our current claim boundary
The proposed support-compression construction combines established Schur compression, conventional tomography, CPTP regularization and known-matrix Petz implementation. Any claim of a new theorem must identify the paid query/control/resource interface and ambient-dimension/spectrum dependence, rather than rename these ingredients. Current packets establish mathematics at their own scoped internal-review status; no historical-priority or practical advantage result follows from this note.
