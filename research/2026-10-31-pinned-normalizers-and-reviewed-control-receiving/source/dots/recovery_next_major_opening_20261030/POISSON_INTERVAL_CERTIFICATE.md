# A rare-event-aware physical reliability interface: exact interval model

30 October 2026. Independent construction/screen, not a new threshold theorem or historical-priority claim. The parent retains the central research choice.

## Question and answer earned

Can small, integrable measured correlations replace a worst-case local noise norm without assuming Gaussianity? Not by themselves. Even temporally independent, translation-invariant noise with every polynomial spatial correlation moment finite can force super-polylogarithmic physical diameter to store one unknown qubit to accuracy epsilon. This does not contradict Gaussian thresholds. A particular non-Gaussian geometric model instead admits an exact **tail acquisition operation**: endpoint count covariance equals the hazard of a single interval spanning the entire device. Thus the required datum is operationally interpretable, but high-confidence empirical exclusion of a tiny hazard costs inverse hazard; it is not supplied for free by the present CP-cavity theorem.

This is an explicit mechanism and resource lower bound, not a claim that real hardware has the chosen tail or that computation is impossible. Distributed machines can buy separation, shield/modify the tail, or use different physics; those costs are precisely outside a local gate-error number.

## 1. Fully specified stationary environment

Sites are Z. In each unit time layer independently, for each left endpoint a in Z, draw a Poisson(lambda) number of intervals. Each interval has independent integer length ell>=1 drawn from law nu; its affected sites are a,...,a+ell-1. Let N_x be the number of intervals covering x. E ell<infinity makes every local count finite almost surely despite the infinite environment. Different time layers are independent. Spatial translation invariance and ergodicity follow from the iid marked Poisson inputs.

Every covered data site is replaced by a fixed state, once per layer. Conditional on the coverage flags, this is the tensor product of onsite replacement maps. There is no large-body system gate. One physical dilation uses one renewed local dump qubit per site/layer and a simultaneous bounded-duration SWAP controlled by the classical local coverage flag. The dump is inaccessible thereafter. All system and controller quantum information in the declared footprint is included; no clean external quantum copy is allowed. An omniscient erasure alert may be given to the decoder: the lower bound survives it.

These are order-one rare local interactions, not weak worst-case local interactions. The flags are correlated. Therefore the bounded incident-norm assumption of CP_CAVITY_LOCAL_FAULT_BRIDGE.md is NOT satisfied at a small strength. Nor is this a Gaussian bilinear-bath model. The spatial flags are supplied by the correlated environment; no local finite-speed bath-generation theorem is claimed. A propagation-speed/energy restriction could exclude the instantaneous broad events and would be additional structural information, not a consequence of finite correlation moments. The exact replacement channel is a deliberately severe transparent test, not an empirical cosmic-ray model.

## 2. Exact connected correlation formula

The joint probability generating function is

 log E exp(sum_x t_x N_x)
   = lambda sum_a E_nu[ exp(sum_(x in [a,a+ell-1]) t_x)-1 ]

for finite-support t where the expression is finite (or as a finite-order derivative at zero). Consequently

 cum(N_(x1),...,N_(xk))
   = lambda E[(ell-(max_i x_i-min_i x_i))_+].                 (1)

All these connected cumulants are nonnegative. In particular

 C(r):=Cov(N_0,N_r)=lambda E[(ell-r)_+], r>=0.              (2)

Summing (1) over x2,...,xk gives the exact identity

 sum_(x2,...,xk in Z) cum(N_0,N_(x2),...,N_(xk))
   = lambda E ell^k.                                    (3)

Proof: for fixed length ell there are ell possible intervals containing 0; each permits ell choices independently for each other coordinate. Time-integrated cumulants gain no long-time factor because distinct layers are independent.

Choose any finite K and any desired positive bounds a_1,...,a_K. For a length law with all moments finite, lambda <= min_(k<=K) a_k/(E ell^k) makes all these integrated cumulants as small as requested. This does NOT claim one lambda makes an arbitrary infinite sequence uniformly small. Spatial polynomial weights also have finite integrals whenever the corresponding length moment is finite.

## 3. Exact single-spanning-interval hazard is an endpoint covariance

A contiguous device occupying sites 1,...,L is covered by a single interval iff its left endpoint belongs to L-ell+1,...,1. There are (ell-L+1)_+ such endpoints. Poisson thinning therefore gives exactly

 h_L = lambda E[(ell-L+1)_+] = C(L-1),
 P(at least one single interval covers entire footprint) = 1-exp(-h_L).     (4)

Multiple overlapping intervals can jointly erase the entire footprint without any one interval spanning it. Thus h_L is the exact rate of the single-spanning-interval event, not the total erasure hazard; its event probability is a lower bound on total full-footprint erasure probability.

For T independent layers, the probability of at least one single-spanning-interval event is

 p_cat(L,T)=1-exp(-T C(L-1)).                              (5)

A disconnected footprint of diameter L-1 has the same rate of single intervals covering the entire footprint. Empty space is therefore a real resource if used to separate modules.

Any full-footprint erasure destroys entanglement with a retained reference, even when its time and footprint are reported perfectly. Conditional on that event, later operations have an output independent of the unknown qubit. For a maximally entangled input, overlap with the target Bell state is exactly 1/4 for any fixed recovered qubit state (there are no retained input-dependent external classical records in this contract). On the other branch overlap is at most 1. Hence every deterministic storage/decoding protocol entirely inside the footprint obeys

 entanglement infidelity >= (3/4)[1-exp(-T C(L-1))].        (6)

If the decoder outputs an erasure instead, (5) is an availability lower bound rather than an accepted-output infidelity bound. Restarting a computation on a known reproducible input is a different task. No unavailable source acquisition or secret auxiliary quantum backup is smuggled into (6).

## 4. All moments finite still does not buy polylog overhead

Let X~Normal(0,sigma^2) and ell=ceil(exp X). Then E ell^k is finite for every fixed k, bounded by 2^(k-1)[1+exp(k^2 sigma^2/2)]. Also

 C(L-1) >= lambda P(ell>=L) >= lambda P(X>log L).

For z=log L/sigma>0, the elementary Gaussian Mills lower bound gives

 C(L-1) >= lambda (1/sqrt(2pi)) exp(-z^2/2) z/(1+z^2).

If physical diameter is L=O((log(1/epsilon))^c) for any fixed c and T>=1, this lower bound decays only as exp[-O((log log(1/epsilon))^2)], which is asymptotically much larger than epsilon. Thus no deterministic architecture with that diameter achieves accuracy epsilon for this environment. All fixed-order correlation integrals can simultaneously be small for any fixed chosen K; all polynomial-weighted integrals are finite. The missing control is an exponential/stretched-exponential spatial tail, or a physical architecture paying more diameter, not mere finiteness of more moments.

This result is 1D and charges DIAMETER, not qubit number without a bounded-density/connectivity assumption. A sparse nonlocal architecture can pay huge distance with few qubits; communication time/wiring/geometry then need their own accounting. It does not establish a universal impossibility of FT or an optimal upper bound for the model.

## 5. A genuinely acquired tail operation in this model

The model provides exact discrete inversion:

 C(r)-C(r+1)=lambda P(ell>=r+1),
 C(r-1)-2C(r)+C(r+1)=lambda P(ell=r), r>=1.                (7)

Thus an equally informed ordinary method can recover interval intensities from spatial count covariance. It need not assume Gaussianity or reconstruct the microscopic bath Hamiltonian. More directly, paired endpoint sensors identify the single-spanning-interval hazard C(L-1). Sensors here observe environmental interval counts, NOT arbitrary qubit readout outcomes. Whether real readouts identify those counts, whether sensing is trusted, and whether events truly have interval geometry are additional paid identification steps, not established facts.

Even perfect noiseless event labels cannot cheaply rule out an unmodeled catastrophic component. Compare null hazard 0 against hazard h in a monitored region for duration n. Their transcripts coincide with probability exp(-nh). Any procedure that accepts the null with high probability also accepts the alternative on this event. To exclude h>=h_* with false acceptance <=alpha using zero observed catastrophes requires

 n >= log(1/alpha)/h_* .                                 (8)

For a mission of duration T and target failure epsilon, h_* is order epsilon/T, so direct event exclusion costs order T log(1/alpha)/epsilon. A parametric physical tail certificate or controlled shielding experiment may beat this by transferring stronger structural information; finite absence-of-events data alone does not.

## 6. Strong ordinary comparator and source boundary

Ng--Preskill, *Fault-tolerant quantum computation versus Gaussian noise*, PRA79 032318 (2009), actual PDF read at https://preskill.caltech.edu/pubs/preskill-2009-gaussian.pdf . Section III, equations (25)--(27), assumes all higher correlations obey Wick factorization; Section V's derivation explicitly needs it. Its spectral criterion is not a promise for arbitrary non-Gaussian noise. Our construction therefore cannot be advertised as refuting that theorem. The ordinary informed comparator uses Poisson thinning, connected cumulants, and compound-event/erasure reasoning with the same full model, not an artificially uninformed independent-error decoder.

Catastrophic chip-level bursts and hardware mitigation are already established research topics: McEwen et al., *Resolving catastrophic error bursts from cosmic rays in large arrays of superconducting qubits*, https://arxiv.org/abs/2104.05219 and https://www.nature.com/articles/s41567-021-01432-8 . This paper is motivation for asking about tails, not evidence for our chosen radius distribution or exact erasure map. No novelty claim is made for Poisson Boolean-model identities or the event-observation lower bound.

The present contribution to Astra is a concrete next-interface discriminator: after a bounded-noise threshold, a physical reliability certificate must either acquire a structural high-tail law and its geometry, or explicitly pay for rare-event uncertainty and spacing. The exact endpoint covariance receiver makes that statement testable in one model. It is not itself sufficient reason to redirect the main mission.

## 7. Remaining consequential hard step and stopping condition

A stronger research target would be a model class of realistic burst propagation with an acquired finite-size tail envelope, physical sensors and mitigation, plus a matching constructive fault-tolerant architecture with all spacing, latency and confidence costs. The useful end-to-end outcome is a certified mission failure bound from raw experimental event data and audited structural assumptions, not another assumed microscopic norm. A finite covariance fit alone cannot be declared sufficient outside a justified model class.

No such hardware inference or optimal architecture is established here. This pass stops at an exact counterexample + exact model-specific acquisition mechanism + statistical lower bound. Further work requires selecting a concrete physical model/source of new information; broad scanning or increasing cumulant order is not justified as a substitute.

## 8. Stronger receiving operation: binary coverage flags suffice, but can cost more

Counts are not essential inside this exact model. Let U_x=1 when site x is untouched in a layer. Put m=lambda E ell and a=P(U_x=1)=exp(-m). The measure of intervals touching at least one of 0,r is 2m-C(r), so

 b_r:=P(U_0=U_r=1)=exp[-2m+C(r)],
 C(r)=log(b_r/a^2),
 p_single_span(L,1)=1-a^2/b_(L-1).                               (9)

This is exact for the event that at least one single interval spans the footprint, even with arbitrarily many overlapping intervals. It separates a spanning burst from coincident endpoint incidents; it does not equal the total probability that the union of several intervals erases the whole footprint. The measured variables remain actual environmental coverage/erasure flags, not arbitrary decoder syndromes. Detecting them reliably and verifying interval geometry still need an instrument/model contract.

The distinction between full event labels and only two binary sensors matters. For a fixed untouched marginal a in (0,1), consider the symmetric pair distribution

 P00=a^2 exp(h), P01=P10=a-P00, P11=1-2a+P00,             (10)

where 0 denotes untouched and h>=0 is small. It is produced by a common Poisson shock of intensity h plus independent endpoint shocks of intensity -log(a)-h. The common shock erases the whole segment. Both alternatives have exactly the same marginal erasure probability. At h=0 all four cells are strictly positive, and

 KL(P_h || P_0) = [a^2/(2(1-a)^2)] h^2 + O(h^3).         (11)

Proof: the derivative vector is a^2(1,-1,-1,1); half its squared norm weighted by reciprocal independent probabilities is a^2/[2(1-a)^2]. Consequently distinguishing h=0 from small h with fixed nontrivial confidence using only independent endpoint pairs needs Omega(h^-2) layers (product KL and Pinsker, or the usual two-point testing bound). More confidence needs a corresponding logarithmic factor under standard binary-testing bounds. This is a restricted sensor-interface lower bound, not a lower bound when full event marks or all intermediate sensor outputs are available.

Thus the exact covariance-to-single-spanning-catastrophe reconstruction is a real operation but not a free precision oracle: at a fixed background local error rate, ruling out h of order epsilon/T using just pair statistics can cost order (T/epsilon)^2. A noise spectrum can be informationally sufficient within a known model while being too expensive to acquire at mission reliability. Both the raw event-label comparator and pair-sensor comparator receive exactly the same data as the corresponding proposed procedure.
