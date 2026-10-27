# Independent receipt: noise-adapted quadratic-training receiver

27 October 2026. PASS for the stated finite-dimensional pure-success/reset source, stationary conditional-IID ordinary mixed T/omega programs, complete accepted-plus-erased instrument, and consumed worst-case resource count. The theorem combines relative p0^-2 polylog training with sufficient entropy tolerance of order p² and p/9 identity throughput. It does not claim practical constants, a reusable decoder, arbitrary-channel robustness, or optimal accuracy dependence.

## Signed-pair operator calculation

Independently expanded the exact adjoint collision composition. All six terms in equation (4), including the scalar trace term and negative double commutator, agree. Since a sigma+b rho=delta H and [H,P]=0, the linear commutator vanishes on the actual spectral projector. This cancellation requires neither program to commute with P.

For a rank-one P and positive density sigma, sigma P sigma<=Tr(Psigma)sigma<=wI. The simple commutator follows from the positive square of P plus/minus i sigma P. For the double commutator, write its first pair as sigma rho P+P rho sigma. The positive square of P plus/minus sigma rho P proves its absolute operator bound by P+sigma rho P rho sigma<=P+wI. The remaining pair sigma P rho+rho P sigma is bounded above and below by sigma P sigma+rho P rho<=2wI. Thus the asserted P+3wI is valid; it does not incorrectly assume sigma rho is positive. Hilbert-Schmidt Cauchy-Schwarz gives the scalar trace bound 2w.

The two coefficient remainders total (1280/3)|delta|³: 128/3+144 for the first and 144+96 for the second. With |delta|<=1, the final coefficients are at most 1280/3+24=450 2/3 on P and 1280/3+52+72+192=742 2/3 on wI. Both fit800. The controlled observable is block diagonal in the collision control; the inactive block is exactly P. Thus the resulting operator inequality applies to arbitrary coherent control/data/reference states. No virtual measurement or trajectory decomposition is introduced.

## Source weights and repeated acceptance

The previous independently received discriminant establishes lambda>=p/3, t<=1/3, q r0<=5e/6, and ideal genuine-code error<=25e/6. Directly, Tr(P omega)<=p/9+5e/6<=5p/18, and Tr(P T)=(lambda+6Tr(P omega))/4<=7p/12, so both weights are <=p. These are properties of the actual programs, not access to a source-dependent gate.

All known phase/control operations preserve I tensor P. Composing the operator inequality yields population <=exp(v)r+p(exp(v)-1)m; selecting an accepted outcome only decreases this positive population. The independent ideal classifier acceptance effect is <=P+eta I, and its full simulation diamond bound yields accepted mass <=r+beta m even with arbitrary coherences and retained references.

The two-variable recurrence therefore holds for the actual unnormalized accepted states. Iteration gives sum m_j<=(1+L Rmax)/(1-beta). The feedback coefficient a0^L b0 L/(1-beta) is below1/16 under the stated conservative constants. More explicitly its solved coefficient on r0 is below2 and on b0 below3, so Rmax<=2r0+3b0, and m_L<=3r0+5b0+beta^L. No normalization or postselection division is hidden here. With beta<=1/16, the chosen L gives beta^L<=p0 xi/16. Since5b0<=p xi/(8L), weighted reset acceptance is <=5e/2+3p xi/16.

## Complete instrument and resources

The accepted rank-one coherence estimate pays both acceptance and erased rejection; the displayed ideal-filter error is below xi/2 for every L>=1 and xi<=1/2. The simulation allocation adds at most xi/256 in total and xi/(256L) per classifier. Its delta² budget is xi/65536, so the population and generic-error budgets use the SAME physical circuit, not incompatible choices. The global sum S includes every Lr QPE repetition; rounding N upward adds at most2Lrm programs. Hence count <=131072 S²/xi+2Lrm, plus the data call.

On genuine source data only, the learned-filter error is weighted by p. Reset output versus erasure costs twice its final accepted mass. The resulting complete error is55e/6+11p xi/8<=50 epsilon_ent+eps p. Choosing eps=nu/2 and epsilon_ent<=nu p/100 gives the stated Delta<=nu²p²/[50000(p+3q)], automatically within the spectral promise. This is meaningful at p/9 throughput only for sufficiently small nu. The exact-erasure adaptive-query lower bound transfers for such fixed small nu; its scope is ordinary definite-causal access and consumed calls, not free coherent oracle access.

Independent numerical corroboration in noise_adapted_quadratic_independent_check.py:168 actual noncommuting signed-pair matrix inequalities, plus144 conservative positive recurrence checks. These tests supplement the analytic operator/CP argument, not replace it.
