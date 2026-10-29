# Sharp elementary flagged-normalization bound

Root and receiving-review refinement,2026-10-29.
If two complete flagged output instruments are within half trace distance Delta on the actual joint input/reference, their accepted subnormalized blocks A,B with probabilities p,q satisfy ||A-B||_1+|p-q|<=2Delta: the other flag blocks contribute at least |p-q|. For p,q>0, divide by the larger probability and use a triangle inequality to obtain
 D(A/p,B/q)<=min(1,Delta/max(p,q)).
If the full instruments have half-diamond distance Delta this holds uniformly for every input/reference. Conditioning is not itself a linear channel when success probabilities depend on input, so do not call the normalized rule a diamond norm without additional constant-success assumptions.

A genuine per-use full-interface half-diamond bound epsilon gives Delta<=N epsilon by telescoping a fixed N-call known adaptive circuit. Known-control inaccuracies add similarly. This is stronger than the safe2Delta/p bound in the original draft but can still be vacuous. It does not follow from reduced input-output agreement when a retained bath differs.
