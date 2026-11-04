# Ensemble closure for physical swap annealing

## Main result
An autonomous physical implementation does not need to execute a Monte Carlo accept/reject routine or reverse a realized Brownian path. A permutation-symmetric material with conserved discrete state counts and reversible exchange has exactly the desired fixed-composition equilibrium for unlabeled observables. This is an application of established canonical sampling and reversible Markov dynamics, not a new theorem. It identifies an experimentally testable requirement that generic swelling or charge redistribution does not meet.

## 1. Exact binary-state construction
Let particle i have position r_i, internal conformation xi_i and a discrete label s_i in {0,1}. Write z=(r,xi), and assume H(Pz,Ps)=H(z,s) for every permutation P of otherwise identical particles. Conserve sum_i s_i=M exactly. The full equilibrium is
pi(z,s) proportional to exp[-beta H(z,s)] 1_{sum s=M}.

Let s0 be any fixed assignment with M ones. Every assignment s is a permutation of s0. Change variables by that permutation in each configurational integral. Its Jacobian is one, so all constrained partition functions Z_s are equal. For any observable A with A(Pz,Ps)=A(z,s), all constrained numerator integrals are likewise equal. Summing over the binomial(N,M) assignments cancels between numerator and denominator. Therefore
E_exchange[A] = E_fixed_assignment_s0[A].

This statement covers the SAME actual soft, anisotropic, fluctuating material, not only ideal hard spheres. Internal state free energies f0,f1 may differ: with fixed M their total is constant. Continuous shell fluctuations need not be eliminated if they are present and modeled consistently in BOTH ensembles. Conversely, an ideal fixed-radius hard-sphere target is not established just by showing soft particles swell.

What is unchanged: equilibrium permutation-invariant structure and static material statistics. What is NOT unchanged: material-particle self-diffusion, physical time correlations, or transport coefficients of the exchange-disabled material. The operation would accelerate preparation/equilibration, not simulate its original physical dynamics.

## 2. Dynamics that realize the invariant law
At fixed s, use equilibrium thermal dynamics for z with H. For an exchange s->s' at the current z, impose local detailed balance
k(z,s;s')/k(z,s';s)=exp[-beta(H(z,s')-H(z,s))].
For example, symmetric attempt prefactors multiplied by the Metropolis acceptance probability satisfy this. A real transition-state mechanism can satisfy the same ratio without an explicit computer choosing acceptance. The sum of these reversible generators preserves pi.

State-dependent mobility must include the appropriate thermal drift/noise convention. Distance-dependent exchange prefactors must be symmetric between the two endpoint configurations. A forward-only chemical fuel cycle or an external electron reservoir generally changes this conclusion unless its work/chemical affinity is included and vanishes around the cycle.

Invariance is not rapid mixing. If the accessible exchange graph is disconnected, geometry excludes nearly all exchanges, or rates are tiny, the desired law is still invariant but inaccessible on useful time scales. No relaxation acceleration follows from the proof alone. Comparison must include local swaps with the actual pair selection and rates, not only ideal long-range swap MC.

## 3. Finite-duration physical transitions: reversible trace process
A physical exchange can involve an intermediate state: free token, bridged token, partially switched shell, etc. Include it in the full reversible process X_t. Let A be the set of desired endpoint configurations. The endpoint law is correct only if the conditional physical equilibrium pi(.|A) equals the specified target, including all binding and conformational free energies.

Define accumulated endpoint time u(t)=integral_0^t 1_A(X_s) ds. Delete time outside A and invert this clock. The resulting trace process is reversible with invariant distribution pi(.|A). For a finite-state generator Q partitioned into endpoint A and intermediate B blocks,
Q_trace = Q_AA - Q_AB Q_BB^{-1} Q_BA,
assuming the intermediate block is transient before return. The stationary block equations give pi_A Q_trace=0. Reversibility follows because the corresponding symmetrized Schur complement is symmetric.

This is standard trace-process theory. Source: C. Landim, Metastable Markov chains, Probability Surveys 16 (2019), equations 2.4–2.6, https://doi.org/10.1214/18-PS310 ; explicit Schur-complement derivation: https://www.wias-berlin.de/preprint/1881/wias_preprints_1881.pdf .

The result constructively allows Brownian motion during intermediate excursions. It does NOT require holding every position fixed or restoring a rejected trajectory. It also does not make discarded wall-clock intervals free. In a stationary run, endpoint-clock time grows at fraction pi(A) of real time. Burn-in/mixing must be counted, just as for any sampler.

### Entry sampling is not endpoint-time sampling
Consider three states A1,A2,F with equilibrium (.49,.49,.02), generator rows
[-1,0,1], [0,-10,10], [24.5,245,-269.5].
Detailed balance holds. Conditional endpoint equilibrium is (1/2,1/2), but returns from F land with probabilities (1/11,10/11). Recording each returned configuration once therefore produces a badly biased histogram. The trace generator has symmetric off-diagonal rate 10/11 and correctly samples the equal endpoint weights when dwell time is retained.

Likewise, freeze on the first completed transfer is not a general exact preparation protocol. At a prespecified independent time, a stationary snapshot conditioned on A is correct. A converged trace process sampled in its accumulated time is also correct. Repeatedly trying until a first success, or selecting first-entry events, needs a separate stopping-bias analysis. One cannot infer correctness from the stationary conditional law alone.

A sudden global shutdown followed by completion of existing intermediate transfers can also bias the result. In the example above, absorbing the equilibrium F population into A1/A2 yields final probabilities .491818 and .508182, not .5/.5. The error is proportional to the intermediate population in this example; a general observable error requires its own bound.

## 4. Global exactness versus local accuracy and throughput
If M tokens are independently non-endpoint with probability f, pi(A)=(1-f)^M. Frequent global all-endpoint configurations require f=O(1/M). This independence approximation is not universal, but illustrates the extensive cost of a global endpoint condition.

By contrast, allowing local O(f) material defects does not demand the same global event. A macroscopic sample can have small local defect fraction while almost surely containing some intermediate. This is an approximate material, not exactly the fixed-composition endpoint ensemble; near jamming, small fractions may cause large responses, so local error must be measured rather than assumed.

General stationarity bookkeeping: mean number of transfers in progress equals transfer-initiation throughput times mean transit duration (count each defined initiated excursion once). Hence a low fraction of in-progress events constrains throughput for a fixed transit time. This is not a universal no-go: a genuine catalytic transfer route could shorten transit time without changing endpoint equilibrium weights. Strong permanent bridges, however, change the material rather than implementing harmless instantaneous swaps.

## 5. Conserved electrons are not conserved particle types
For two otherwise identical microgels, each with K independent redox sites, hold the total number of oxidized sites at K. If n sites are oxidized in the first particle, the other has K-n. With equal site energies and no extra interactions,
P(n) proportional to binomial(K,n)^2.
Normalization is binomial(2K,K). The state count therefore favors intermediate oxidation, not permutation of completely reduced and oxidized particles. At K=100, probability of either pure endpoint is 2.20876e-59. Conserving total charge does NOT conserve the multiset of particle radii or the number of swollen particles. Radius-volume conservation would additionally require a particular affine constitutive relation, which has not been established.

A single transferable token with at most one binding site per particle is a better discrete-state candidate in principle. But unbound tokens, bridges and partially occupied conformations must be included, and actual shape control by one token must be demonstrated. A 2021 shape-changing DNA-origami paper initially suggested as an example was checked by the implementation investigator and found to use 16 removable strands and 24-hour incubation; it is NOT evidence for a single conserved binary token. No such physical implementation has been established here.

### Scoped cooperative-redox test
An explicit model can favor endpoint oxidation states: assign each particle energy J n(K-n)/K, where J is measured in kBT. With K conserved oxidations across the pair,
log w_n=2 log binomial(K,n)-2J n(K-n)/K.
Let electron count change by nearest-neighbor steps with rates nu min(1,w_{n±1}/w_n), nu=10^6/s per direction. This is an intentionally simple reversible birth-death model, NOT a measured microgel mechanism. Exact mean first-passage time from n=0 to n=K follows
T_0K=sum_{i=0}^{K-1} [sum_{j=0}^i w_j]/[lambda_i w_i].
For K=100:
- J=3: pure endpoints only 5.98e-5 probability; mean crossing ~10^6.49 seconds.
- J=5: endpoints .6315; within one electron of endpoints .9484; mean crossing ~10^45.68 seconds.
- J=7: endpoints .9905; within one electron .9999706; mean crossing ~10^88.82 seconds.

The enormous numbers arise from THIS all-to-all cooperative energy and sequential-electron path. They reject the claim that adding strong endpoint cooperativity automatically supplies a rapid swap in this model. They do not rule out spatial nucleation, alternative free-energy landscapes, concerted or catalytic exchange, or a genuinely single-token conformational switch. Physical attempt multiplicity and microscopic energy parameters must be measured. `ensemble_test.py` computes the exact distributions and first-passage sums.

## 6. Strongest same-resource comparison and conclusion
Conserved binary exchange is established Kawasaki-style dynamics, not a new sampling principle: K. Kawasaki, Phys. Rev. 145, 224 (1966), https://doi.org/10.1103/PhysRev.145.224 . Swap acceleration with radius degrees of freedom is directly analyzed in https://doi.org/10.1103/PhysRevX.8.031050 and modern swap algorithms are discussed in https://doi.org/10.1021/acs.jpcb.4c06702 .

The constructive advance of this pass is an explicit physical specification, not novelty: conserved discrete type counts, permutation-symmetric endpoint Hamiltonian, reversible transition mechanism, correct endpoint-time observation, and measured wall-clock rates. A material meeting those conditions could physically realize swap-assisted preparation. The implementation investigator is comparing real actuation against ordinary annealing, softness changes and existing particle controls. No superiority, industrial-scale leverage, or new foundational principle is demonstrated yet.

## 7. Certified approximate shutdown
There is a useful limited preparation guarantee. Assume the system initially has its full stationary law pi. Stop initiation of new transfers without changing endpoint energies. For realizations initially in A, subsequent exchange-disabled dynamics must preserve pi(.|A). Let every realization initially outside A eventually resolve to some endpoint law kappa, with no restriction on its bias. Then the final law is
nu = pi(A) pi(.|A) + pi(A^c) kappa,
so ||nu-pi(.|A)||_TV <= pi(A^c).
This provides an approximate output guarantee when the global intermediate probability is small. It requires actual equilibration beforehand and an endpoint-preserving shutdown; abruptly changing binding free energies or shell mechanics invalidates those assumptions. It does not remove the extensive difference between controlling a global defect event and merely controlling local defect fraction.

## 8. Dissociative-token kinetic ceiling
For equilibrium single-site binding in a well-mixed idealized reservoir, let f be the fraction of tokens free. Then f/(1-f)=Kd/c_empty, while k_off=k_on Kd. Successful transfers per bound token cannot exceed k_off, giving
k_transfer <= k_on c_empty f/(1-f).
An optimistic diffusion-limited fully absorbing receiver of radius R in a dispersion with occupied volume fraction phi and token occupancy theta gives
k_on c_empty <= 4 pi D_token R n_empty = 3 D_token phi(1-theta)/R^2.
This uses dilute Smoluchowski capture and independent receivers as a benchmark, not a rigorous dense-suspension bound in arbitrary hydrodynamics. Sparse reactive sites, geminate rebinding and inaccessible gaps reduce useful capture.
For illustrative D_token=1e-10 m²/s, phi=.6, theta=.5, the benchmark capture rate is 360/s at R=.5 micrometre and 36000/s at R=50 nm. Therefore local f=.001 is not automatically fatal for nanoscale kinetics. Requiring f of order delta/M for a frequent globally exact endpoint event is much more restrictive. These are feasibility requirements, not measured rates or a no-go for associative handover.
