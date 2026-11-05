# Independent audit of the proposed spatial-burst recoverability question

Date: 5 November 2026. This audit began only after the constructor's independent response-identification route had been derived and rejected. The burst question was then supplied by the parent for a question-level challenge. No sufficiency, novelty, or completed fault-tolerant apparatus is asserted here.

## 1. Exact universal erasure obstruction

Take processors on Z^d and a strict causal speed c. Initially all accessible dependence on an unknown input is contained in an l-infinity ball of radius L. All communication, controllers, flags, logs, repair metadata, and any retained input source that may be used for recovery must be included. An untouched mathematical reference is allowed for testing quantum recovery but is not an accessible backup.

At time t, all accessible input dependence is inside the deterministic ball of radius L+c t. A marked Poisson reset with center z and radius R kills all such dependence whenever

|z|_infinity + L + c t <= R.

Define n_d(u)=(2 floor(u)+1)^d for u>=0, and zero otherwise. The intensity of these sufficient killing events is

h_L(t) = lambda E[n_d(R-L-c t)].

They form a thinning of the marked Poisson process by a deterministic spacetime set. Hence the probability that no such event has occurred by T is exactly exp(-Lambda_L(T)), where

Lambda_L(T)=lambda integral_0^T E[n_d(R-L-c t)] dt.

Its infinite-time value is

Lambda_L(infinity)=(lambda/c) E[integral_0^((R-L)_+) n_d(u) du].

Thus Lambda_L(infinity) is infinite exactly when E[R^(d+1)] is infinite (for fixed finite L, with the usual harmless small-radius qualifications). Finite E[R^d] makes the local reset intensity finite; it does not prevent eventual complete loss of every finite-speed encoding of the unknown input.

For continuum centers with l-infinity burst balls, the exact formula is especially transparent:

Lambda_L(infinity) = lambda 2^d/[c(d+1)] * E[(R-L)_+^(d+1)].

This is a universal necessary condition. Absence of one all-cone reset is not sufficient: many overlapping partial resets can destroy the remaining information.

For a uniform unknown classical bit, any final guessing decoder has error at least [1-exp(-Lambda_L(T))]/2, because on an all-cone erasure event its accessible record is independent of that bit. For a q-dimensional unknown quantum input tested against a maximally entangled reference, the corresponding entanglement-fidelity upper bound is exp(-Lambda_L(T)) + [1-exp(-Lambda_L(T))]/q^2. These require the reset really to erase accessible state, not merely suppress ordinary output.

## 2. Initial encoding is a fatal quantifier issue unless supplied explicitly

For a fixed finite initial support L and any positive short interval, Lambda_L(T)>0 whenever the radius law can cover the initial cone with positive probability. This gives a strictly positive startup loss floor at fixed lambda. Later hardware growth cannot repair that loss. Therefore arbitrary confidence from a fixed bare unknown input is impossible under the stated model.

A meaningful full question must specify one of: a paid encoded seed whose radius grows with target confidence; a protected/repeatable input interface with its own explicit reliability and cost; or a fixed startup-error allowance. Supplying a large already encoded seed changes the input contract. Commissioning it locally in the same burst field must not be silently replaced by a free nonlocal encoder.

If E[R^(d+1)]<infinity, then the all-cone hazard tends to zero as L tends to infinity. This removes that particular obstruction for growing supplied seeds, but proves neither that such seeds can be commissioned reliably nor that a local decoder survives partial resets.

## 3. Why moment finiteness does not imply an exponential lifetime in fixed hardware

For hardware confined to a fixed ball of radius L, full-coverage reset events have constant rate

kappa_L=lambda E[n_d(R-L)].

Any retention time is bounded above by a rate-kappa_L exponential killing clock. With a regularly varying tail P(R>r) proportional to r^(-alpha), alpha>d, kappa_L has order lambda L^(d-alpha), so the expected retention time is at most order lambda^(-1) L^(alpha-d). In N=Theta(L^d) dense hardware this is polynomial, order N^(alpha/d-1), even when alpha>d+1.

The d+1 condition concerns the possibility of indefinite protection while the causal support can expand. It is not a theorem of exponential finite-volume storage or small total resource use. Active hardware, communication, energy, and readout geometry must all appear in any matching operation.

## 4. Flagged erasures, unflagged corruption, and readout are different tasks

With perfectly flagged erasures and one classical bit, the simplest valid-copy protocol has alphabet {blank,0,1}. Local copying makes the valid-copy set a contact/growth process with spatial disasters. A theorem that this set has positive survival probability could be an existing or near-existing percolation result, rather than a new fault-tolerance principle.

If burst corruption can alter valid flags, clocks, addresses, repair records, or data arbitrarily, that reduction fails. The new operation must detect or correct misleading local states without a trustworthy external decoder. Ordinary local-stochastic-noise assumptions also fail for power-law bursts: a single large burst can corrupt a large block with a probability far larger than p^(number of locations).

An undirected infinite path in an offline spacetime picture is not an online local controller. Nor does survival of at least one copy somewhere in an expanding region provide finite-time readout at a specified receiver. The full target must retain causal encoding, damaged recovery metadata, finite-bandwidth communication, and a physically specified decoder/readout.

## 5. Strong primary antecedents

### Poisson hail

Foss, Konstantopoulos and Mountford, *Power law condition for stability of Poisson hail*, Journal of Theoretical Probability 31 (2018), 684-704, DOI 10.1007/s10959-016-0723-3. Theorem 1 gives small-intensity workload stability when both service time and spatial diameter have a finite (d+1+epsilon)-moment. Theorem 2 constructs unstable examples with moments just below that order. The proof uses greedy lattice animals and correlated spacetime geometry.

Primary full text: https://pure.hw.ac.uk/ws/portalfiles/portal/14600619/art_3A10.1007_2Fs10959_016_0723_3.pdf
Constructor references: turn50view1, turn52view2.

Mountford and Wang, *Stable systems with power law conditions for Poisson hail*, Advances in Applied Probability 56(1) (2024), 315-353; online 2023, DOI 10.1017/apr.2023.23. The primary preprint gives the detailed moment-region classification and explicitly excludes some boundaries. Writing spatial critical moment d+alpha and temporal critical moment 1+beta, stability covers alpha*beta>d in the indicated regime, as well as alpha=1, beta>d. For repair time proportional to radius, the exact finite (d+1)-moment endpoint corresponds to a boundary, not an immediately supplied sufficiency theorem.

Primary full text: https://arxiv.org/pdf/2102.07406
Publication record: https://doi.org/10.1017/apr.2023.23
Constructor references: turn52view0, turn54view1, turn50view0.

Hail workload stability is not a recovery architecture. Its FCFS simultaneous-service rule has different state, coordination, and causality requirements, and some versions explicitly permit infinite propagation speed. Any transfer must construct the decoder and prove the comparison; assigning a nominal repair time proportional to radius does not do that by itself.

### Vacant Boolean percolation

Penrose, *Non-triviality of the vacancy phase transition for the Boolean model*, Electronic Communications in Probability 23 (2018), paper 49, DOI 10.1214/18-ECP153, proves a nontrivial vacant phase under the finite D-th radius moment in ambient dimension D>=2. This makes D=d+1 an especially important comparison for a spacetime repair-cone construction. Its conclusion supplies undirected geometric connectivity, not finite-speed causal decoding. That distinction must be proved away, not assumed.

Primary full text: https://arxiv.org/pdf/1706.02197
Constructor references: turn52view1, turn50view3.

### Contact processes with spatial catastrophes

Lanchier, *Contact Process with Destruction of Cubes and Hyperplanes: Forest Fires Versus Tornadoes*, Journal of Applied Probability 48(2) (2011), 352-365, DOI 10.1239/jap/1308662632, shows that catastrophe geometry can change survival even when simple area-based intuition suggests the reverse. The publisher's 2016 online date is not the original publication year. It is directly relevant to any claim that a new damage-volume law alone characterizes survival, but the abstract does not establish the full random-radius coding endpoint here.

Primary publication: https://doi.org/10.1239/jap/1308662632
Constructor reference: turn50view2.

The search did not establish that the precise full causal recovery question is already solved. It also does not establish novelty. An exact correspondence with oriented percolation or a theorem on error-prone local decoders remains to be demonstrated.

## 6. Acquisition limitation

Without a structural tail family or an independently justified tail envelope, no finite ordinary sample can certify that E[R^(d+1)] is finite against all laws with finite E[R^d]. Mix an arbitrarily small mass epsilon of a tail with finite d-th and infinite (d+1)-st moment into a light-tailed law. On any bounded sample count, the modified and original experiments are arbitrarily close, while the proposed classification reverses. Sequential finite-expected-sample procedures have the same issue by truncation/coupling.

Thus a sharp moment theorem can be a foundational classification conditional on a supplied physical law. An acquired physical capability must explain how the relevant tail envelope is earned, or retain it explicitly as substantive prior information. The old productive-control and repair theorems provide no physical reduction that supplies this envelope.

## Judgment

The all-cone erasure argument is sound and provides a consequential necessary condition beyond average erased-volume flux. The full question is worth distinguishing from that lemma: matching causal recovery, corrupted repair metadata, commissioning and readout are the hard operations. Existing Poisson-hail and Boolean-percolation results are close enough that a bare moment/percolation statement would be an inadequate claimed advance. The full useful recovery capability has not been earned by this audit.
