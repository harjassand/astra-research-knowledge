# Example6.8 polygon compression: pending incidence-completeness audit

The program `recursive_t_polygon_certificate.py` transcribes the actual two polygon lists in Example6.8, Fig.20, preserving abstract vertex distinctions D0,D1,P even where their images coincide. It reconstructs shared edges from polygon boundaries.

For the six-face left list it finds internal shared edges RQ,PD0,PD1 and inherited three-face seams OP,PQ. For the nine-face right list it finds six internal shared edges PA1,PC0,QC1,PB1,QB2,QB4 and three-face seams OP,PQ,QR.

**Audit condition:** the internal shared edges must have no additional incident face omitted from this displayed OPQ-incident portion. The program establishes relative algebra for the listed incidence, not this physical-incidence completeness. An independent primary-source audit has been requested before calling this an actual-model certificate.

Conditional on that check, each of the upper/right/lower face groups is degree2-connected. Its face syndrome reduces to its parity at a chosen anchor with no increase in weight. The inherited seam then acts by precisely the original code F on these three anchor bits. The minimum syndrome weight of every local relative coset equals the minimum weight of its 3-bit parity vector modulo F. Thus no syndrome-budget constant is lost in this refinement subpatch.

Exhaustive checks: 64 input patterns for the left list and512 for the right list, each for both blue repetition F={000,111} and red parity F={000,011,101,110}. Relative ranks are4/5 and7/8, respectively. All conditional cost identities pass.

Even if the incidence audit passes, this checks the displayed local subpatch, not the whole surrounding recursive vertex star or the gluing of coarse carries.


## Independent verdict

The requested audit did not establish degree2 completeness from the available primary description. The exact missing datum is a full abstract coface list for each listed internal edge, or an explicit subdivision map showing that it lies strictly within one old face. Coordinate overlap and apparent line thickness are not sufficient. Therefore this remains a conditional algebraic certificate, not a completed physical refinement proof. No claim is made that the complete source figures could never be reconstructed; that reconstruction has not been verified here.
