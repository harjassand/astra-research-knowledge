# Independent source and phase review of the aspect-parallel flow

Reviewed `../flow_resume_20261114/ASPECT_PARALLEL_FLOW.md` against the recovered four-corner prefix construction. Scope is the source, translation-prefix, merge and late-stage interfaces, not an independent rederivation of the Gaussian/support recurrences or all within-type corner-current estimates.

## Prefix translation
For a fixed corner channel and offset, the prefix is a deterministic monotone translated path. On any oriented physical edge, occupied-site count fixes its step. At that step the flipped site uniquely fixes the torus translation. Hence different translations of this fixed path have disjoint physical edges. With uniform currents 1/n, their summed energy is exactly the single-path energy divided by n. Mixing different corner channels or offsets need not preserve disjointness; Jensen outside this translation averaging is legitimate and is retained in the proof.

The shared source edge is excluded from that division. Its current is one and its normalized resistance contribution is exactly κ^-1.

The prefix energy bound requires the stated overlap-first contiguous row ordering, not arbitrary row-major scanning. The recovered ordering keeps orthogonal convexity and charges remaining corner area plus at most one unfinished row. Initial dimensions are below 400, where the completed rectangle energy increases with either dimension. The stated prefix envelope therefore carries over to unequal initial aspect dimensions under that ordering.

## Merge and late continuation
At dimensions M+k+ and M+k−, with M=600, adding a completed row or column decreases rectangle energy because 16−.04M<0. The unequal rectangle energy is at most that of the 600-square. Corner filling with at least two plus neighbors does not increase energy. Charging all corner additions by the recovered channel envelope is conservative.

After corner filling, all dimensions are at least600. Completing to Q616 and then balanced growth to first majority has completed-side energies no larger than the initial600-square energy; partial side births cost at most16. Thus the conservative 2n exp(E_M+16) resistance bound covers these steps. Stopping on first majority only removes subsequent edges. These sizes stay below n/2 until the expressly defined continuation reaches the target.

Minkowski across phases and across positive/central types correctly pays overlaps. No cross-type offset disjointness is assumed. Within-type geometry and the inherited current bounds remain separate premises of the scalar certificate.

## Source normalization and scope
A physical path starting at all-minus plus the original star→all-minus edge is a valid original soft-source unit flow; zero current on other reservoir edges is permitted. Removing that edge supplies a hard-source physical flow, not an identity between hard and soft capacities or residence times.

The independently constructed explicit box18 thermal core contains either recovered interpretation of original C5. Its normalizer bound is below1.000001 and therefore supports the more conservative1/(1−10^-6) multiplier, under the same fixed-diagonal augmentation and physical energy conventions. This does not resolve the original C5 predicate for exact source sampling.

No source/prefix/merge/late obstruction was found in this review. This is an independently reasoned interface review, not a claim that the entire R200 flow has been explicitly enumerated, or that the resulting finite capacity bound proves practical first-passage simulation.
