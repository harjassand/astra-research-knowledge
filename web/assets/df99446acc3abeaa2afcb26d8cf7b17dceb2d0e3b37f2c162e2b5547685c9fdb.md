C08_L02 REVISION 001 — CROSS-EXPOSURE AUDIT AND STATIONARY-JOINING FORM
2026-10-07. INITIAL.txt is immutable and predates peer exposure.

ATTRIBUTION CORRECTION
The initial localized invariant-set estimate overlaps the post-initial c08_l06 result `work/cycle6/c08_l06/revisions/invariant_code_power_lemma.md`, which proves a stronger version: the code set need only be invariant under T=phi_1, zeros are allowed off the set, and the local entropy estimate uses the orbit sweep. The iid/reference Fano specialization also overlaps c08_l10's `INITIAL.txt`. I do not attribute either component as an independent c08_l02 scientific increment. The independently frozen de Bruijn finite-window torus obstruction remains a distinct diagnostic.

The synthesis below combines c08_l06's localized work inequality with c08_l10's process-level Fano transfer and sharpens the latter's global-volume bookkeeping. It is a joint cross-exposure result, with the source ideas attributed above; it is not a priority or field-breaking claim. The new formalization uses an external stationary reference process and a stationary joining to the actual physical output. It avoids requiring the reference stream itself to be an observable of the physical phase point, while making the necessary coupling assumption explicit.

THEOREM: STATIONARY-JOINING LOCAL POWER FLOOR
Let (M,g) be a smooth closed Riemannian 3-manifold, V=Vol(M), X a smooth divergence-free autonomous field (zeros are allowed), phi_t its flow, mu=dVol/V, S=Def X, and nu>0. Let U={X!=0}. Fix a sample interval tau>0 and a measurable set C which is invariant modulo mu under T=phi_tau, with beta=mu(C)>0 and mu(C\U)=0. Let eta=mu|C/beta. For a finite alphabet Sigma of size K>=2, let c:C→Sigma be a measurable physical readout; its stationary process law P_c is the pushforward of eta under x↦(c(T^j x))_{j∈Z}.

Let Q be any stationary probability law on Sigma^Z with entropy rate h(Q)>=R nats per sample. Suppose there is a stationary joining lambda of P_c and Q with one-symbol Hamming error lambda{x_0!=y_0}<=delta. Define
  F_K(delta)=h_2(min{delta,1-1/K})+min{delta,1-1/K} log(K-1),
with h_2(p)=-p log p-(1-p)log(1-p) and 0 log 0=0. Then the physical output process has entropy rate
  h(P_c)>= [R-F_K(delta)]_+.
If X is sustained by the closed-manifold strain-viscosity law
  ∇_X X - 2nu div(S) + ∇p = F,
with W=∫<F,X>dVol, then
  W >= 4 nu V beta [R-F_K(delta)]_+^2 / tau^2.                 (1)
The rate is per physical time; logs are natural. If the alphabet carries bits per sample, multiply the rate by log 2 before applying (1).

PROOF
First apply the coordinate Fano inequality under lambda. If p=lambda{x_0!=y_0}, then H(Y_0|X_0)<=f_K(p), where f_K(p)=h_2(p)+p log(K-1) on [0,1-1/K], and the trivial log K bound applies above that range. Since p<=delta, H(Y_0|X_0)<=F_K(delta). Stationarity makes the same bound hold at every coordinate. Subadditivity of conditional entropy gives H(Y_0^{n-1}|X_0^{n-1})<=nF_K(delta). Hence
  H(Y_0^{n-1}) <= H(X_0^{n-1}) + nF_K(delta).
Divide by n and take entropy-rate limits: h(P_c)>=h(Q)-F_K(delta)>=[R-F_K(delta)]_+. The physical readout is a measurable factor of (C,eta,T), so h(P_c)<=h_eta(T).

For the localized transport estimate, on U put r=|X|, e=X/r, P=I-e⊗e, q=<Se,e>, b=PSe, and B=PSP on e-perp. Since div X=0, tr B=-q; writing its eigenvalues as -q/2±s gives |S|^2=2s^2+(3/2)q^2+2|b|^2>=2s^2. The moving-normal quotient cocycle obeys
  log||Q_t(x)|| <= integral_0^t s(phi_u x)du - (1/2)log(r(phi_t x)/r(x)).
For eta-a.e. x in C, Oseledets applies to the full derivative and quotient; recurrence under T shows the flow-line exponent and the endpoint logarithm divided by n vanish even if r approaches zero near C. The normal determinant has zero exponent, so the full spectrum is chi,0,-chi. Ruelle's C1 inequality for the invariant probability eta gives h_eta(T)<=integral chi deta. Applying the cocycle estimate at n tau, Birkhoff to s_tau(x)=integral_0^tau s(phi_u x)du, and the recurrent endpoint gives
  h_eta(T) <= integral_C s_tau deta.
This is the local estimate supplied and separately derived by c08_l06; it uses no full-flow invariance of C.

For every t, phi_t preserves mu and mu(phi_t C)=beta. Therefore
  integral_M s^2 dmu
   >= (1/tau) integral_0^tau integral_{phi_t C} s^2 dmu dt
   = beta (1/tau) integral_C integral_0^tau s(phi_t x)^2 dt deta(x)
   >= beta ((1/tau) integral_C s_tau deta)^2
   >= beta (h_eta(T)/tau)^2.
The middle step is Jensen under eta times normalized Lebesgue measure on [0,tau]. Since |S|^2>=2s^2 on U and eta is supported on U, the same lower bound gives integral_M |S|^2dmu>=2 beta(h_eta(T)/tau)^2. Pairing the stationary equation with X gives the exact work identity W=2nu V integral_M |S|^2dmu. Substituting the Fano lower bound proves (1).

COMPARISON WITH THE EXPOSED CLUSTER CLAIMS
- c08_l06's exact local result is W>=4nuV beta kappa^2/tau^2 when h_eta(T)>=kappa. Taking kappa=[R-F_K(delta)]_+ yields (1). This is the local strain-energy step; it is attributed to c08_l06, not newly discovered here.
- c08_l10 takes an iid q-ary ideal stream and noisy decoded stream, then combines the global entropy lower bound with the nonzero-support fraction beta, giving 4nuV alpha^2 r_epsilon^2/(beta tau^2). The local bound (1) yields 4nuV alpha r_epsilon^2/tau^2 for a code set of volume alpha supported in U, with no need for alpha=beta. Since alpha<=beta, this is stronger. Its iid/Fano content is attributed to c08_l10; (1) is a cross-worker synthesis and a local strengthening of the support bookkeeping.
- If the reference process Q is itself a measurable factor on the physical code set, h_eta(T)>=h(Q)>=R already. Then Fano is unnecessary for the power bound; direct substitution gives W>=4nuV beta R^2/tau^2. The joining form is useful only when Q is an external comparator and the acquired object is a stationary low-error joining to the actual output factor.

EXACT SHARPNESS / BOUNDARIES
The Fano correction cannot be uniformly improved using only K, the reference rate and one-symbol joining error. Let the physical readout be constantly symbol 0 and let the external iid reference have probabilities (1-delta, delta/(K-1),...,delta/(K-1)); use their product joining. The error is delta, the reference entropy is exactly F_K(delta), the physical output entropy and strain power are zero, and [R-F_K(delta)]_+=0. The own script `fano_joining_boundary.py` checks this identity exactly for K=3, delta=1/4. This is a sharp boundary example, not a counterexample to (1).

The joining, reference rate and code support are real premises. If a noisy external source is not stationary-coupled to the actual physical output, its entropy says nothing about the flow's entropy. If a reference is factor-measurable from the physical state, the flow already has its entropy and no decoder correction is needed. Empirical mismatch on a finite trace does not certify a stationary joining or entropy rate; the c08_l02 de Bruijn rigid-torus construction has block entropy n log 2 through any fixed horizon N but zero asymptotic entropy and zero strain. Any executable acquisition claim needs an all-time entropy/Markov certificate or explicit mixing and confidence assumptions, plus certified beta and joining-error bounds.

The theorem charges only sustaining strain-viscous power. It does not charge the source generator, data link, sensor, decoder, geometry acquisition, proof of stationary joining, force fabrication, or clock. It does not turn finite simulation, Turing completeness, topological entropy, or a null-volume code into a positive-volume stationary factor. It implies no Navier-Stokes regularity theorem. Its scientific status is CONDITIONAL; its localized step and Fano step are attributed c08_l06/c08_l10 mechanisms; external correctness and priority remain UNKNOWN.

EXECUTABLE EVIDENCE
- `python3 work/cycle6/c08_l02/debruijn_finite_window.py`: PASS, N=6, q=64, every cyclic binary block of widths 1..6 appears uniformly, though the smooth flat-torus time-one map has finite order, zero KS entropy, and zero strain.
- `python3 work/cycle6/c08_l02/fano_joining_boundary.py`: PASS, exact rational probabilities and symbolic entropy identity for K=3, delta=1/4.
These are finite/symbolic diagnostics only. The general local cocycle/Ruelle/Fano proof is analytic and is not validated by scripts.

PROVENANCE AND NEXT GATE
Cross-exposed sources read: outputs/round6/frozen_initials/c08_s01/INITIAL.txt, c08_s02/INITIAL.txt, c08_s03/INITIAL.txt; work/cycle6/c08_l05/INITIAL.txt and INITIAL.json; c08_l06/INITIAL.txt and its invariant_code_power_lemma.md; c08_l07/INITIAL.txt and INITIAL.json; c08_l10/INITIAL.txt and INITIAL.json. No c08_l01/l03/l04/l08/l09 INITIAL was present when checked. The Sol baseline was frozen in outputs/round6/SOL_BASELINE.txt and its manifest before these reads. No cross-cluster peer files were needed for this exact interface audit.

Primary imported result: Ruelle, "An inequality for the entropy of differentiable maps" (1978), Theorem 2(b), for C1 maps and arbitrary invariant Borel probabilities; full five-page original is cached at outputs/research_state/work/cycle1/pde_transport_sources/Ruelle1978.pdf/.txt, URL https://www.ihes.fr/~ruelle/PUBLICATIONS/%5B51%5D.pdf. The strain-viscosity work identity follows the audited conventions in outputs/research_state/work/cycle3/entropy_power_audit.txt and Samavaki-Tuomela 2019v2, https://arxiv.org/html/1812.09015v2. The Fano and factor-entropy steps are proved above. No new literature priority search was sufficient for clearance.

Next decisive gate: acquire a concrete smooth-flow example in which a physical finite-alphabet readout has a certified stationary joining to a useful external source, with positive invariant code volume beta, entropy rate R, mismatch delta, and finite geometry/acquisition costs. Then independently audit the orbit-sweep estimate when X has zeros near C. A finite-window fit alone fails; an ideal factor supplied in advance is circular as an acquisition claim.
