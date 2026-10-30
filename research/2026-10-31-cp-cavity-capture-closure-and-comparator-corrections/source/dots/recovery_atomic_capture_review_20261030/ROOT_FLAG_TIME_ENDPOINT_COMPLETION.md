# Time-dependent weights, endpoint cuts, and the signed flag norm bound
30 October 2026. Root completion to ROOT_SPECTRAL_FLAG_EXPANSION.md. It corrects that note's shorthand propagation/counting claims. Review pending; actual growth/initial-source instantiation remains separate.

## Initial support
The continuous triangular identity starts with rho0 supported in every selected P_j. Otherwise decompose its initial ket/bra sectors by the SAME union-of-violated-cuts rule and supply weighted norms for those initial marked components. No initial support is inferred from a small marginal failure probability. Seed capture can be a separate finite source step, but its common module/joint bounds must be proved.

## Moving weights
For a CP compressed propagator and time-dependent positive F_R(t), the necessary hypothesis is

 dot F_R(t)+K_D^*(F_R(t)) <= a_R(t)F_R(t),

not K_D^*F_R alone. It implies the complete weighted norm bound between the two time-specific metrics. Moving phase cuts must likewise be received through their actual unitary frame or an explicit stage endpoint; a stationary-cut formula cannot simply be used for arbitrary moving projections.

Assume a_R(t)<=sum_(j in R)a_j(t). Set A_j(t)=integral_0^t a_j(u)du. If a_D(t) denotes a nonnegative norm majorant for the signed D component, define

 b_D(t)=a_D(t) exp[-sum_(j notin D)A_j(t)].

The diagonal propagation budget cancels. A transition marking J then carries an extra exp(sum_(j in J)A_j(t_mark)), so each record pays ONLY growth before its own mark. This is the correct way to use geometric prefix volume, rather than paying final block size through the entire longest horizon.

## Counting with D-dependent rates
Fix the first-bad stage k_j for each selected record, and assume its new-mark factor, after the preceding growth correction, is at most epsilon_j=exp(-c n_(k_j)). Rescale marked components by product_(j in D)epsilon_j. Let their remaining insertion coefficients c_(J,D)(t) satisfy the ACTUAL row incidence bound

 sum_(J containing j)c_(J,D)(t)<=C n_j(t)

uniformly in D, and vanish for a newly marked j outside its designated stage window. No literal D-independent exponential coefficient domination is needed.

For z_j in (0,1], the nonnegative norm generating SUM G(z,t)=sum_D b_tilde_D(t) product_(j in D)z_j obeys

 G' <= C[sum_j n_j(t) 1_(j eligible) z_j]G,

because z_J<=z_j and the incidence estimate can overcount each transition. Let V_j be the integrated active insertion budget in its eligible stage, O(n_(k_j)) for fixed-duration stages. Then

 G(T)<=G(0) exp(C sum_j V_j z_j).

Taking z_j=(1+C V_j)^-1 and extracting the one nonnegative all-selected term gives

 a_S(T)<=G(0) product_j[e(1+C V_j) epsilon_j].          (1)

This is a bound on norms of exact SIGNED components, not a probability assertion. If the initial weighted norm is at most A_seed^|S|, absorb it into the fixed per-record factor. Summing first-bad stage assignments in this nonnegative majorant factorizes; geometric n_k makes sum_k C(1+C n_k)exp(-c n_k) uniformly small at sufficiently large fixed seed size.

## Simultaneous endpoint cuts are a separate operation
At a stage endpoint, let Pi_j(X)=P_j X P_j and Delta_j=Id-Pi_j. The exact identity Id=product_j(Pi_j+Delta_j) can mark arbitrarily many records in one endpoint. It does NOT satisfy the bounded-body continuous insertion-rate assumption.

If [F_j,P_j]=0, F_j>=I and Q_j<=F_j/M_j at that endpoint, then

 ||Delta_j||_(F_j F_rest -> F_rest)<=3/sqrt(M_j).

Expand Delta_j into QXQ+QXP+PXQ and use ||Q F_j^-1/2||<=M_j^-1/2 and ||F_j^-1/2||<=1. Other record weights commute and cancel. Good Pi_j is weighted-contracting. Thus a subset J endpoint mark costs product_(j in J)3/sqrt(M_j), AFTER the actual stage CP map's JOINT weighted transport is supplied.

The corresponding generating multiplier is bounded by product_(eligible j)(1+3 z_j) after its barrier factors are removed. Each selected record is eligible at its designated first-bad stage only. This contributes a fixed per-record constant to (1), not a volume factor. Actual stage transport still has to include noisy reset/copy and parameter-change costs; it is not supplied by a marginal endpoint probability.

## Phase identity through growth
The new good cut must also preserve the old encoded classical bit. If old vertices are retained, n_new<=g n_old, and the old block remains within delta_old of its old consensus during copy, then any new consensus within delta_new n_new must be the same provided

 1-delta_old > g delta_new.

Otherwise the retained old correct bits alone exceed the allowed errors relative to the opposite consensus. For equal thresholds choose delta<1/(g+1). A PRE-chart output cut explicitly comparing with the old phase is another legitimate interface. Without one of these arguments, an output union-of-two-basins test could silently accept an opposite consensus after a collective stage.

## Compatibility and remaining receiver
The full flag expansion should be checked to commute with summing out unselected analytic flags. Algebraically this follows by summing their ket/bra sector resolutions back to identity in K+Gamma, but it is needed before using selected-set bounds as a compatible local-error family. If an original phase label must be retained after marking for a quantum reference comparison, that label also needs an explicit linear-map construction and norm cost; no immutable physical register is created by this proof.

The corrected abstract lemma removes the false shortcuts identified in the first note. It does not establish all its hypotheses for the staged native/atomic device, nor a complete factory, physical readout or universal controller.
