# Principal acceptance of the new adverse families

Astra PRO3 directly read the complete lower proof, independently reconstructed
its branch probabilities and accepted it before integrating the main theorem.
The final lower source is reviews/vanishing_lower_proof.md: 18348 bytes,
SHA256 95461aac0b6fdd7687876e24eebfe87067a41b9c79f7546ce7f75a5532363619.
Its diagnostic source is reviews/vanishing_lower_checks.py: 13224 bytes,
SHA256 9a1e8604dee3853076b2100041dc04c6bf77cd03d72bb00eb1275cd9610319ad.
The contributor's source receipt records minor post-inspection formatting,
portable invocation and resource additions; the scientific proof did not change.

The principal checked the following obligations independently of the numerical
results. The three-state vectors are positive, their KL limit has strict slack,
and W_B<W_*<W_A fixes every acceptance branch used. The B exit probabilities
and A escape probability are exact. The event's time/retention comparison
is relative, uniformly for eta log n up to any fixed multiple of loglog n.
Subtracting the actual target terminal mass is retained.

For the growing path, m=O(loglog n) makes z vanish sufficiently fast; the
geometric sums keep the star probabilities positive and control KL uniformly
as support grows. Q is symmetric stochastic and does not use target
observations. Forward local acceptance is z^eta, reverse acceptance is
n^-2 z^eta. The marked transition has probability beta z^eta/4. The total
exit upper bound includes star exits, global forward and backward transitions,
and local reverse transitions. The exit lower bound is positive by the star
global move. Requiring a marked next exit within each deterministic window
has a multiplicative success correction. Terminal global/local escapes give
the displayed retention factor. Thus the finite event bound applies to the
actual unmodified chain, with no single-crossing or no-return assumption.

The path exponent follows with O(1) integer-rounding error in log probability.
Its variational derivative and unique minimizer equation are correct. The
rational example uses strict KL slack and the exact integer inequality
321^27<25^27 16^25. It disproves the proposed universal multiplier-one
threshold; it does not identify the exact minimax crossover.

The upper-proof challenger separately checked the conversion of this accepted
path exponent to max(K,1/(d chi)) for epsilon log T. That scoped check is in
reviews/vanishing_transport_source_binding.md. It is not represented as an
additional independent review of the entire lower construction.

The proof, not floating-point agreement, carries acceptance. The source retains
all finite calculations and the failed precision assertion. No statement is
made that moderate tested horizons already display the proved slow divergence.
