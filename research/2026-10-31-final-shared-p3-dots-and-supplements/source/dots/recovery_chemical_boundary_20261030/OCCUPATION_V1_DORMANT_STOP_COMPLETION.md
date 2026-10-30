# Completion: price the actual D=0 stop in the lower-occupation event

30 October 2026. Prompted by independent reviewer producer-workspace/review_dormant_extension. The frozen V1 source remains unchanged.

Section 4 of OCCUPATION_NORMALIZED_DORMANT_RETURN_V1.md must include the actual episode's D=0 stop in its survival event. The following estimate completes that omission.

On the stopped interval before A leaves its input factor band and before any creation, d<=d_in. The only d-decreasing reactions are 2 and 6; each decreases d by exactly one.

- If d_in>=x, reaching zero requires at least d_in>=x fast events. The already earned bound E(number of fast events before t0 and the other stops)<=C epsilon x gives probability at most C epsilon by Markov's inequality.
- If d_in<x, the total rate of d-decreasing events is at most `C(A d+d(d-1))<=C x d_in` inside the A band. Thus the probability of even one such event before t0 is at most `C epsilon d_in x^2/(x^3+n d_in)<=C epsilon`, because d_in<x. In particular this bounds extinction.

Union this event with the previous band exit, creation, clearing and connector events. Reducing the same fixed epsilon yields probability at least 1/2 that the REAL episode survives through t0 with A in its factor band. The lower bound for its physical A-occupation, and hence the occupation-normalized return comparison, follow as claimed.

This is a local proof completion, not a global recurrence or dormant Green acceptance. V1 alone remains historically incomplete on the explicit survival accounting.
