# Collision review: copositive path certificates

29 October 2026. Complementary targeted primary-source review for root's
`COPOSITIVE_PATH_CERTIFICATES.md`, with an exact conventional comparator.

## 1. Assessment

The candidate survives as a specific analytic certificate and acquisition
interface. It does not establish the broad discovery that time-symmetric
observations can force hidden entropy production. The strongest directly
relevant predecessor is Skinner and Dunkel's 2021 PNAS hidden-network
minimization, including its finite reduction for two-step flux data. The
comparison must include that method, not only observed-path KL, currents,
ordinary PSD tests, or an arbitrarily selected hidden topology.

A defensible proposed addition is the combination of an explicit copositive
observable witness, positive midpoint geometry of the entropy half-tilted
killed semigroup, and an entrywise arithmetic-geometric deficit bounded by
microscopic path entropy. It gives a short certificate from a bounded
endpoint/duration-bin score without selecting hidden dimension or imposing
a microscopic rate ceiling. The first-moment version trades bounded
acquisition for a second-duration-moment premise. These are substantive
distinctions in representation and certification. An existing constrained
optimizer can adopt the certificate; this does not erase the construction.
Neither historical priority nor a general computational or sample advantage
is established by this targeted review.

## 2. Primary antecedents and read scope

### Skinner and Dunkel, PNAS 2021

[Improved bounds on entropy production in living systems](https://pmc.ncbi.nlm.nih.gov/articles/PMC8106300/)
minimizes entropy over compatible hidden Markov networks. Its O2 statistics
include successive macrostate transitions. The paper provides finite local
optimization and positive bounds even when the entire observed process is
time-reversal symmetric. Thus the conceptual claim and unrestricted
hidden-model benchmark already exist.

Read: main optimization, two-step estimator and time-symmetric-observation
sections; reduction, finite-size argument and analytic example in the
[November 2020 preprint appendix](https://arxiv.org/pdf/2011.08765),
pp. 10–16. The published supplement was blocked; the appendix is explicitly
a preprint version. The general global estimator sums local bounds and is
not automatically the optimal use of every O2 statistic jointly.

### Skinner and Dunkel, PRL 2021

[Estimating entropy production from waiting time distributions](https://arxiv.org/pdf/2105.08681)
develops hidden-network minimization using waiting times, including moment
constraints and equilibrium complete monotonicity. Read: abstract,
formulation, principal optimization discussion and appendix proof of the
equilibrium waiting-time restriction. The C5 fixture has exponential scalar
interior durations. Joint endpoint geometry retains information discarded
by that scalar statistic; this does not make the general optimization
principle unable to accept endpoint information.

### Dechant, Garnier-Brun and Sasa, 2023

[Thermodynamic bounds on correlation times](https://arxiv.org/pdf/2303.13038)
derives entropy bounds from time-symmetric correlations. An example has
time-reversal-symmetric observed paths and a positive bound. Read:
entropy-estimation discussion, equations 20–21, discussion and appendix
treatment of path symmetry. The main development concerns overdamped
Langevin dynamics, with jump-process extension mentioned as future work.
It is a strong conceptual antecedent, not the same finite-CTMC copositive
endpoint/bin certificate.

### Caputo, Chen, Gu and Polyanskiy, 2024

[Entropy Contractions in Markov Chains: Half-Step, Full-Step and Continuous-Time](https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf),
section 2.3 and Lemma 2.9, explicitly connect completely-positive Markov
factorization to its strict distinction from nonnegative PSD kernels
starting at dimension five. Read: that section through the relevant lemma.
CP geometry and the PSD/nonnegative-factorization distinction are existing
ingredients. The quantitative native-path entropy certificate is the
candidate use.

### Lebowitz and Spohn, 1999

[A Gallavotti–Cohen-Type Symmetry in the Large Deviation Functional for Stochastic Dynamics](https://arxiv.org/pdf/cond-mat/9811220),
equation 2.14, gives the entropy/action tilted generator with off-diagonal
entries q_xy^(1-lambda) q_yx^lambda and unchanged diagonal. At lambda=1/2
it is the geometric operator. With D=diag(pi), root's operator satisfies

    D^(1/2) Q_geo D^(-1/2) = L_(1/2).

Read: section 2.1 through equation 2.17 and the start of time reversal.
The half-tilted operator is established; its nonnegative Gram output and
copositive observable entropy certificate are the proposed use.

### Reflected histories: Jorgensen, Neeb and Olafsson, 2016

[Reflection Positive Stochastic Processes Indexed by Lie Groups](https://www.emis.de/journals/SIGMA/2016/058/sigma16-058.pdf)
treats positive semigroup/path-space constructions and Markov reflection
positivity. Read: introduction, the reflected cylindrical-function Gram
calculation in the reconstruction proof (pp. 17–18), and section 3.4's
Markov characterization. It credits Klein (1978) and Klein–Landau (1975)
for the path-space/semigroup antecedents; those earlier papers were not
retrieved directly. Thus midpoint reflection geometry for complete
half-histories is classical. Keeping nonnegative indicator functions gives
the candidate's CP specialization. The paper does not provide, in the
read passages, a copositive violation-to-entropy-production estimate.

The nearby title [Entropy inequalities from reflection positivity](https://arxiv.org/abs/1004.4599)
by Casini (2010) concerns subsystem Renyi/vacuum entropies, not stationary
Markov entropy production. Only its primary abstract was read. It is not
evidence for the desired quantitative collision.

### Current adjacent work: Franco, Kepka and Velazquez, 2026

[Characterizing the Detailed Balance Property by Means of Measurements](https://link.springer.com/article/10.1007/s00205-026-02183-7)
(published 3 April 2026) uses reciprocal response functions of finite linear
networks. Their time-independent response ratio is necessary but generally
insufficient; sufficiency is obtained under graph and stability assumptions.
Read: primary abstract and introduction through the main informal theorem.
This is an adjacent response-access result, not the copositive quantitative
entropy witness. Its substantive structural-stability premise should remain
distinct from actually acquiring perturbation information. The rest of its
proof was not audited.

## 3. Exact conventional comparator for the C5 endpoint record

This is our explicit specialization, not a claim that the cited paper
printed the five-port formula. It uses ordinary entropy-lowering rerouting
and the binary Jeffreys inequality independently reviewed earlier.

Distinguish unweighted endpoint flux N=integral K(t)dt from the residence
matrix M=integral tK(t)dt. They coincide in this fixture because
K(t)=exp(-t)M; they do not coincide generally.

**Proposition.** Among finite reciprocal CTMCs with resolved singleton
ports, no direct port jumps, and exact native endpoint flux

    N = I + (17/30) C5,

the minimum unnormalized entropy is

    E_min = (16/3) log(5/3).

No hidden clock ceiling, residence moment or dimension is required for this
endpoint-record statement. Root's fifteen-state construction attains it.
The endpoint zeros are exact hypotheses, not facts certified by merely
failing to observe a transition in finitely many trials.

### Proof

Infinite entropy is harmless. For finite entropy, every edge has its
reverse. Any connected hidden component touching ports i,j gives positive
N_ij through a positive-probability interior path. Its attached port set
is therefore a clique of the support graph of N. Since C5 has no triangle,
every component touches at most two ports.

Such a component reduces to hidden stars, preserving full endpoint and
port flux while never increasing entropy. Here is the elementary reduction
with its two-port scope explicit. For a hidden vertex x put

    a_i=f_ix, b_i=f_xi, h=sum_i a_i=sum_i b_i.

Replace passage i->x->k by a_i b_k/h. If at least one endpoint remains
hidden, reroute an ordinary edge; hidden self-loops may be discarded.
Collect the port-to-port block, with at most two attached ports, into one
new hidden star. If A=sum_ports a_i and B=sum_ports b_i, its fluxes are

    u_i=a_i B/h, v_i=b_i A/h, total s=AB/h.

Its excursion flux is u_i v_k/s=a_i b_k/h, including returns. A one-port
star is balanced. Leave these new stars while eliminating the original
hidden vertices. Before merging parallel edges, entropy is preserved:

    sum_{i<k} (a_i b_k-a_k b_i)/h
        * log[(a_i b_k)/(a_k b_i)]
      = sum_i (a_i-b_i) log(a_i/b_i).

The two-port star contributes exactly its pair term. Joint convexity and
homogeneity of (u-v)log(u/v) make parallel-edge merging entropy decreasing.
Holding-time laws need not be preserved. This last point prevents automatic
reuse for arbitrary duration-bin constraints.

The resulting binary or one-port stars satisfy

    N=sum_x h_x alpha_x beta_x^T,
    E>=sum_x h_x J(alpha_x,beta_x).

For r_x=alpha_x dot beta_x, the reviewed inequality J>=g(r_x) also holds
for one-port stars (r_x=1). Convexity yields

    E >= R g(trace(N)/R), R=sum_ij N_ij=32/3.

Here trace(N)/R=15/32 and g(15/32)=(1/2)log(5/3). The ten constructed
stars have this return fraction and swapped probabilities (5/8,3/8), so
the binary and Jensen equality conditions both hold. QED.

The uncensored linear copositive bound E>=8/3 is about 97.88% of this
optimum. The unit-window bound E>=(8/3)(1-exp(-1)) is about 61.87% of the
same full-record optimum. These compare population bounds, not acquisition
costs. The reduction does not assert that arbitrary many-port stars admit
binary replacements preserving their entire endpoint matrix and port
budgets: a balanced three-port star already disproves that assertion.

## 4. Equal information and complete task costs

For completed excursions, both methods can use the same endpoint/duration
records; the copositive score is their fixed linear compression. A
comparator receiving less information would be unfair. Conversely,
censoring at a fixed time without retaining late endpoints does not provide
the uncensored N above. Published two-step rerouting does not automatically
preserve the duration-bin data.

For a bin-only record, the ideal comparator remains entropy minimization
over all compatible finite microscopic CTMCs with the same confidence
constraints. Root's inequality is an explicit lower certificate for this
optimization. This review proves neither a finite reduction of that
bin-constrained optimizer nor execution superiority over its strongest
implementation.

Charge both methods the same resets, calibrated flux-weighted port
preparation, endpoint resolution, timing tolerance, observation time and
independent-source premise. Full-matrix inference needs valid simultaneous
uncertainty treatment; empirical zeros cannot become exact zeros. A fixed
bounded witness needs only scalar concentration. Data-selected witnesses
or windows require a selection correction or independent validation.

The half-history extension preserves the same distinction: midpoint
conditional independence and reflection positivity are antecedents;
the entropy certificate and its observation/preparation cost are the
proposed capability. It does not establish that CP for every observed
history is sufficient for an equilibrium process completion.

## 5. Public implementation inspected

Read the complete 116-line
[EntropyEst.m](https://github.com/Dom-Skinner/ImprovedBoundsOnEntropyProduction/blob/main/EntropyEst.m)
and repository README. It implements a two-neighbor hidden-star problem
with four internal states and twelve optimization variables, using MATLAB
fmincon/SQP inside GlobalSearch. Initial constraint tolerance is 1e-6,
function tolerance 1e-7, input/log regularization 1e-10; retries relax the
constraint tolerance. README notes convergence/runtime sensitivity. This
routine is not the entire general six-per-pair mathematical reduction.

No MATLAB solver was executed or timed. A returned feasible candidate is
not by itself a rigorous lower certificate for a nonconvex minimum. This
qualification does not weaken the mathematical comparator. The analytic
witness can certify a lower bound alongside such an implementation.

## 6. Search and scope conclusion

Targeted searches used both search engines for copositive/CP/reflection
positivity combined with entropy production, reversible hidden Markov
models and reflected paths. They did not locate the same quantitative
classical copositive entropy formula. Most CP hits concern quantum maps,
which are a different use of the term. This is not a priority finding.

The result separates from weaker PSD/current/path-reversal tests, while
the full endpoint fixture already has a stronger ordinary completion
optimum. The candidate contribution is the explicit analytic entropy
certificate, its sharp coefficient if independently established, and its
bounded native-data implementation under stated hypotheses.

Companion `check_endpoint_comparator.py` checks exact rational endpoint
rerouting and the C5 equality with outward entropy intervals. It performs
no source observations and does not execute external MATLAB software.
