# Finite-pulse diffusion versus local reset

Let c(x,t) be a concentration perturbation in a semi-infinite region x>0, obeying c_t=D c_xx. A boundary concentration step Delta c causes an electrode flux of magnitude Delta c sqrt(D/pi)/sqrt(t). Superposition for a boundary excursion on -a<t<0 gives a post-pulse opposite-sign flux magnitude

J_a(t) = C [1/sqrt(t) - 1/sqrt(t+a)], t>0,

where C=Delta c sqrt(D/pi), with electrochemical charge/current prefactors absorbed. At periodic steady state with P=5+a seconds, the prediction is the sum over t+nP, n>=0. The code sums 10,000 past pulses; contributions from still older pulses are nearly a constant over the 0.2–4.8 s comparison window and cancel under two-point affine normalization.

A local, finite, regenerable inventory with dn/dt=-n/tau during the cathodic phase instead gives J=A(a) exp(-t/tau)+B. Pulse duration changes initial inventory A(a), but not normalized shape if tau is fixed.

The test compares r(t)=[J(t)-J(4.8)]/[J(0.2)-J(4.8)]. This is conditional shape validation: the two anchor points in each validation trace are used to fix scale and offset. All 22 interior phase points are prediction targets. No validation time constant or diffusion exponent is fitted. The diffusion model does not have an adjustable exponent.

Neither equation is a complete electrochemical mechanism. Total current includes CO2 reduction, hydrogen evolution, charging, and possibly coupled chemical reactions. The cell is stirred. A successful diffusion shape would not identify a chemical species, and a successful exponential can reflect several ordinary kinetic/transport mechanisms. The model comparison is a screening test of the proposed cross-pulse concentration-memory explanation, not a claim to identify an elementary reaction.
