# Close predecessors and constructive boundaries

29 October 2026. Complementary source comparison for operational phase
scrambling and the root's separate acquired mixture-cancellation direction.
No historical-priority claim follows from this targeted search.

## 1. Group orbit averaging is established

Choi, Lim and Wang, *Group-averaged Markov chains II: tuning of group action
in finite state space*, arXiv:2512.13067v1, 15 December 2025:
https://arxiv.org/html/2512.13067v1

Read abstract and introduction. The paper explicitly studies orbit Gibbs,
Metropolis and Barker kernels, GPG sandwiches, spectral/asymptotic-variance
comparisons, information projection and alternating group actions. Conditional
averaging to enforce finite orbit dynamics is therefore a close predecessor,
not a new P1 principle. The present physical-phase calculation attaches an
actual finite-bit/heat operation, retained-history scope and calibration error
to that machinery. It does not establish a new physical apparatus.

Boyd, Diaconis, Parrilo and Xiao, *Symmetry Analysis of Reversible Markov
Chains*, revision 29 November 2004:
https://web.stanford.edu/~boyd/papers/pdf/symmetry_analysis.pdf

Read introduction and orbit-lumping discussion. When a group acts by Markov
chain automorphisms, its orbit process is Markov through the usual block-row
criterion. The phase mechanism here does not assume the native kernels commute
with the scrambling group; the extra randomization changes their realized
endpoint dynamics. This distinction does not make conditional averaging new.

## 2. Randomized compiling already tackles non-Markovian noise

Winick, Wallman, Dahlen, Hincks, Ospadov and Emerson, *Concepts and conditions
for error suppression through randomized compiling*, arXiv:2212.07500v1,
14 December 2022:
https://arxiv.org/pdf/2212.07500

Read pp.2--4, especially Sec.III.B Eq.(2), Theorem 3 and Sec.III.C. The theorem
converts each cycle into a local stochastic Pauli form, with coefficients that
explicitly depend on the environment's state. It therefore does not generally
erase the full record's dependence on retained environmental memory. The paper
also constructs failure when gate-dependent errors leak the randomization key
to the environment. Calling an averaged error channel stochastic is not enough
to claim a memoryless multi-time process. Both the retained-key caveat and the
need to inspect multi-time consequences have strong predecessors.

For the root's candidate acquired cancellation, the potentially distinguishing
condition is independence of the entire next-visible-outcome row from the
retained hidden state for each compiled logical action, with an acquisition
protocol for that condition. The new proof must establish that independence,
not just a favorable one-step form or an averaged equilibrium response.

## 3. Randomized rates and controlled lumpability are established

Cardelli, Grosu, Larsen, Tribastone, Tschaikowski and Vandin,
*Lumpability for Uncertain Continuous-Time Markov Chains*, QEST 2021:
https://www.iris.sssup.it/retrieve/dd9e0b32-58f9-709e-e053-3705fe0a83fd/qest2021.pdf

Read introduction and Sec.3.4 (pp.7--8). The authors relate uncertain rates
to CTMDPs and use probabilistic choices among extremal rates to realize convex
target rates. Their lumpability preserves reachable aggregate probability sets
in a supplied microscopic model. That is different from physically acquiring
hidden conditional Gram products and synthesizing a positive finite mixture
whose unknown omitted directions cancel. It is nevertheless a close warning
against claiming convexification or controlled aggregation as newly invented.

An endpoint mixture sum_j alpha_j exp(tQ_j) is generally different from
exp(t sum_j alpha_j Q_j). A primitive sampled once per complete call realizes
the former. Fast switching or an actual random-rate generator needs its own
clock and actuator contract to realize the latter. No such interchange is made
in OPERATIONAL_PHASE_SCRAMBLING.md.

## 4. Meaningful failures retained

The operational-phase proof exposes four live costs. Exact Haar randomization
is an extra operation. Finite shifts alone remain singular in microscopic TV.
Short physical heat smoothing repairs that singularity, but arbitrarily small
relative-grid imperfections create an O(eta_phase/sqrt(Dtau)) per-stage floor.
Retained current keys or repeated random keys can restore hidden-memory
dependence. None of these costs can be inferred from a small empirical Markov
residual or the number of retained controller bits.
