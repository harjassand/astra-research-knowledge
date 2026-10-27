# Constant-overhead Choi simulation of classically specified fresh probes

2026-10-27. Scoped reduction candidate, independent receipt requested. This does NOT simulate arbitrary coherent adaptive channel queries.

## Repreparable probe access

Consider a strategy making at most n physical training/decoder calls. Each call uses a classically specified state of the qutrit input and, optionally, a NEW known/repreparable reference. This joint state is prepared freshly and uncorrelated with existing retained quantum memory conditional on the classical history. The choice may depend on prior measured outcomes; outputs/new references may subsequently be stored and processed collectively. The unknown datum may be retained, but it is not coherently fed into a query or entangled with that query input.

For any trace-preserving channel E with normalized Choi state J_E, measure the Choi reference using the two-outcome effect rho^T and its complement. The success probability is EXACTLY1/3, independent of E and rho, because Tr_B J_E=I3/3. Conditioned on success, the remaining physical output is exactly E(rho):

 Tr_A[(rho^T tensor I)J_E]=E(rho)/3.

More generally, for a known fresh pure state |psi>_(R,L)=sum_(x,a)Psi_(x,a)|x>_R|a>_L, apply the reference-side Kraus filter F=sum_(x,a)Psi_(x,a)|x>_R<a| to J_E. Since F*F<=I and Tr(F*F)=1, this is a valid heralded operation with success probability1/3. Its successful unnormalized output is(id_R tensor E)(|psi><psi|)/3. A known mixed joint probe can first be purified using an additional new reference, then the unwanted purification part is discarded. Thus entanglement with a NEW fully known reference is allowed with the SAME1/3 success probability.

A failed attempt consumes only that Choi copy and any fresh disposable reference. Since rho is a known fresh probe, no unknown quantum input has been destroyed and the attempt can be retried. On success the original strategy resumes with the correct output state. Conditional success probability stays1/3 after every adaptive classical history, so the number of attempts is governed by independent geometric trials.

## Fixed-cap simulation

Choose0<epsilon<1 and

 N=ceil[6n+24log(1/epsilon)].

Use at most N independent Choi copies. If fewer than n successful simulated calls are available, output a fixed abort/erasure result. Padding unused calls to the original deterministic cap is allowed.

For X~Binomial(N,1/3), its mean is N/3>=2n. Chernoff gives

 Pr(X<n)<=exp[-(N/3)/8]=exp(-N/24)<=epsilon.

A coupling with the exact strategy therefore bounds the complete unhalved diamond difference of the capped simulation by2epsilon, uniformly in the channel and unknown datum/reference. The successful branches are exact; abort probability is bounded independently of all such inputs.

## Consequence for the mixed-flag model

Suppose a strategy in this FRESH CLASSICALLY SPECIFIED probe class achieves complete error at most p/8 from p identity+(1-p)erasure on the all-real-p mixed-flag lower family. Choose epsilon=p/32. The simulated Choi-program strategy has error at most3p/16<p/4, so the received Choi lower applies:

 ceil[6n+24log(32/p)]>=9r²/(32768p²).

In particular

 n>=3r²/(65536p²)-4log(32/p)-1/6.                   (1)

Thus the same quadratic rank/signal exponents hold asymptotically for this ordinary classically chosen fresh-probe access, despite the fact that a single chosen probe can outperform a single Choi copy.

The reduction also covers known mixed probe states, via the effect rho^T. It does not require that the labels be sampled uniformly or fixed in advance.

## Crucial exclusions

A query entangled with retained UNKNOWN quantum memory cannot in general be retried after postselection failure. This proof therefore does NOT close the general adaptive coherent-query gap, does not furnish an exact one-copy simulation, and does not contradict the one-probe1/(2r) versus one-Choi1/(3r) distinguishing example.

The permitted new-reference filter is not a purification of the channel program: it is a known local heralded operation on a MIXED Choi copy. No purified channel/environment access is supplied.
