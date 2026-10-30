# Explicit positive auxiliary repair and factor-two error budget
30 October 2026. Completion of the TNI cavity receiving note. This is an algebraic receiving lemma with a common channel-domain premise, not a new native-memory proof.

Let F be the FULL decoded CPTP channel from L_in tensor A_in to L_out tensor A_out. L may contain both the native and processor logical registers and their intended joint logical operation U is CPTP. Let K be the decoded native-killed CP/TNI channel on that SAME input/output chart. Suppose

 ||F-K||_diamond<=epsilon,
 K=G+B,  ||B||_diamond<=b,
 G=U tensor A,

where A is a signed linear auxiliary map. The last identity is actual logical factorization of the good fault classes, not an inference from marginal channel fidelities. Then ||F-U tensor A||_diamond<=epsilon+b.

Choose any fixed normalized logical input state sigma and define

 A_+(X)=Tr_(L_out) F(sigma tensor X).

A_+ is an actual CPTP channel. Applying the same CPTP insertion/partial-trace maps to F-U tensor A gives

 ||A_+-A||_diamond<=epsilon+b,

because Tr U(sigma)=1. Since ||U||_diamond=1,

 ||F-U tensor A_+||_diamond<=2(epsilon+b).             (TF1)

This preserves arbitrary logical/reference inputs and performs no survival conditioning. A_+ need not be physically implemented: it is a legitimate comparison auxiliary channel extracted from the actual full process. It also avoids assuming the signed good auxiliary map is CP or TP.

The lemma remains valid after a declared source channel I_L tensor E_aux, with all norms on its common parameter/input space. For a fixed auxiliary preparation, A reduces to a signed scalar/output-state map and the same proof applies. It does NOT justify changing the auxiliary assignment with an unknown logical input, proving separate pointwise bounds on incompatible input domains, or applying an extraction product probe outside the source class on which epsilon is controlled.

A native theorem whose bound is only a weighted warm-state estimate must explicitly provide a common source/channel chart, uniform in the admitted logical and processor input and retained references, before TF1 is quoted as a diamond-channel guarantee. Otherwise retain its original state-restricted norm and do not silently promote it.
