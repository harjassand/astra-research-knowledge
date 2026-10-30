# Incoming-profile preservation and graded Green completion

30 October 2026. New completion of COLLECTIVE_KILLED_GREEN.md, pending review. Same fixed-n collective contract and actual killing clock; no global transfer.

Write f_s(a)=(1+a)^(-s), s>0. The underlying label process satisfies

    L f_s(A) <= C_s f_s(A).                           (1)

Progress and safe moves cannot decrease A and therefore contribute <=0. An adverse event can lower A by at most k, and the aggregate intensity weighted by the number of target labels it touches is <=bA. For A>=2k, the mean-value bound gives

    f_s(A-d)-f_s(A) <= C_s,k d f_s(A)/(1+A), 0<=d<=k.

Summing gives (1). For A<2k, use f_s(A)>= (1+2k)^(-s), bounded increments, and touch intensity<=2kb. Events not touching a target label cannot lower A. This proves (1) even for correlated adverse batches and arbitrary safe rates.

Thus e^(-C_s t) f_s(A_t) is a nonnegative supermartingale after localization, and deterministic-time expectations obey E f_s(A_t)<=exp(C_s t)f_s(A_0). Killing is imposed by its independent hazard construction; the underlying process may be continued after killing. No survival-conditioned label law is used.

## Graded occupation

From the killed Green proof, for t_n=n^-delta and n large,

    P(tau>t)<=2^(-floor(t/t_n)).

Cauchy-Schwarz in the UNCONDITIONED extension gives

    E[f_s(A_t) 1{t<tau}]
      <= exp(C_(2s)t/2) f_s(A_0) P(tau>t)^(1/2).

Integrating in blocks of length t_n, and choosing n sufficiently large for the fixed grade, yields

    E integral_0^tau f_s(A_t) dt <= C_s t_n f_s(A_0). (2)

This is an actual incoming-grade Green estimate. The occupation integrand and terminal killing are in the exact theorem clock, not a claimed physical-time conversion.

## Terminal incoming-profile preservation

The same geometric survival bound gives E exp(C_(2s)tau)<=C_s for n sufficiently large. Optional stopping of the nonnegative supermartingale at tau, followed by Cauchy-Schwarz, yields

    E f_s(A_(tau-))
      <= [E exp(-C_(2s)tau) f_(2s)(A_(tau-))]^(1/2)
         [E exp(C_(2s)tau)]^(1/2)
      <= C_s f_s(A_0).                               (3)

The displayed Cox killing mark occurs without a simultaneous underlying label jump. If another stopping mark changes labels, use its actual pre-jump state here and pay its output separately. For the displayed kill removing at most m target labels, A>=m at the mark and

    f_s(A_out)<=(m+1)^s f_s(A_(tau-)),

so (3) holds for its actual output, with the displayed-mark indicator. Other exit outputs are not granted this bound without their own bounded-loss verification.

## A useful stronger-output-grade reset

Let p,s>0. At the displayed kill, split at input A<=K, with K>=2m. The kill compensator from the preceding note bounds this low-input probability by C K^m n^-delta. By (3) with grade2s, Cauchy-Schwarz bounds the low-input contribution of f_(s+p)(A_out) by

    C f_s(A_0) K^(m/2) n^(-delta/2).

On A>K, f_(s+p)(A_out)<=C K^-p f_s(A_out), so (3) bounds that contribution by C K^-p f_s(A_0). Choosing K proportional to n^[delta/(2p+m)] yields

    E[f_(s+p)(A_out); displayed kill]
       <= C_(s,p) n^[-delta p/(2p+m)] f_s(A_0).       (4)

This combines a genuine reset with incoming-profile preservation at the cost of an extra output grade. It does not falsely claim a population-small factor with the SAME incoming/output grade for all initial target populations.

All constants and the required finite-head threshold may depend on the fixed requested grades. Equations (2)-(4) do not themselves price immigration, seed deletions, changing n, signed activation credit or complementary large-B dynamics. The completed section theorem cannot be imported without those separate interfaces.
