# Primary-source screen for the current decoder optimization gap

28 October 2026, 14:43 UTC. This is an attribution/scope note, not a new theorem.

Belov et al., *Semidefinite Programming for Quantum Channel Learning*, arXiv:2601.12502v2 (10 September 2026), https://arxiv.org/html/2601.12502v2 , was inspected at Sections III and IV.5, equations22–23 and34–36. Its relevant objective is quadratic in Kraus entries and becomes linear (or linear-fractional) in the Choi matrix. Our positive leverage numerator is already quadratic in that Choi matrix. The cited SDP therefore does not directly optimize the present objective or preserve its varying positive affine denominator. This is a distinction of optimization variables, not a criticism of that paper or an impossibility result.

The earlier inspected Naor–Regev–Vidick rounding theorem remains relevant established machinery, but its orthogonal/unitary constraints alone do not supply the coupled CPTP partial trace or positive-cost transfer. The new fixed-effect notes explicitly prove their own restricted transfer and leave the globally moving effect open.
