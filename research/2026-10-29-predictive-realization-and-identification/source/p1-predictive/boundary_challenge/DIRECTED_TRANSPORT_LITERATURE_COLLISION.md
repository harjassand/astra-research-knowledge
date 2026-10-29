# Directed boundary-record realization: targeted literature collision check

Research check: 2026-10-28 UTC. This note compares a new theorem under construction by root and the other proof agent with selected primary sources. It is not a proof review, an exhaustive priority search, or an assertion of historical novelty. No new stochastic experiment was needed.

## Target and finding

The target fixes an irreducible Eulerian boundary Laplacian `S`, positive labelled port weights `w_B`, nonnegative excess source vectors `v_R=b_R-w_B` and `v_L=b_L-w_B` with common total `V>0`, and a scalar residual `c`. Put `F_ij=-S_ij` off the diagonal. Among nonnegative matrices `M` with row sums `v_R`, column sums `v_L`, and `M_ij=0` whenever `i!=j` and `F_ij=0`, define

\[
 J_* = \min_M\sum_{i\ne j:F_{ij}>0}\frac{M_{ij}^2}{F_{ij}}.
\]

Diagonal entries are permitted without an `F` denominator. The proposed theorem is: a finite positive stationary CTMC realizing the calibrated record exists exactly when this polytope is nonempty and `2c>J_*`. The related construction preserves `S,b_R,b_L,w_B` exactly while allowing `c<=c_hat<=(1+epsilon)c`, with `O(m^2/epsilon)` positive states. These are the claims being compared, not independently re-proved here.

**No checked primary source stated this joint-margin, Schur-budget criterion or supplied it as a direct theorem with the same inputs and conclusion.** The closest sources supply substantial ingredients. The informative proposed addition is the identification of the residual-record realization problem with a scalar convex transport threshold, followed by a positive stationary completion. It is not the invention of moment matching, phase representations, Schur reduction, exact selected-mean aggregation, or quadratic programming for Markov models.

## Closest collisions

### 1. Telek–Horváth: moments and positive realization of PH/MAP laws

M. Telek and G. Horváth, *A minimal representation of Markov arrival processes and a moments matching method*, Performance Evaluation 64 (2007), 1153–1168, [DOI 10.1016/j.peva.2007.06.001](https://doi.org/10.1016/j.peva.2007.06.001). The [author-uploaded manuscript](https://www.researchgate.net/publication/222578381_A_minimal_representation_of_Markov_arrival_processes_and_a_moments_matching_method) was read at Theorems 3–4 and Sections 4–6, including 6.2; publisher metadata and the introduction were also checked.

This is the strongest realization/moment collision. For a fixed nonredundant order, it parameterizes PH/MAP laws by finitely many moments and characterizes equivalent representations through similarity transformations. The MAP moment representation uses marginal interarrival moments plus consecutive-arrival joint moments. Section 6 searches for a similarity transform producing valid generator matrices, with numerical failures near the feasible boundary discussed explicitly.

**Exact overlap:** finite moment coordinates, stationary process information, and conversion from algebraic to positive Markov representations. **Difference in the checked theorem:** the paper reconstructs a specified fixed-order process law, whereas the proposed result leaves most of the excursion law free and characterizes realizability of only the calibrated boundary record, permitting additional states. Its matrix-similarity criterion does not supply the proposed transportation polytope or `J_*`. “Minimal representation” there is not a proof of minimality of our record or state count.

### 2. MacKay–Robinson: exact directed aggregation on entrance edges

R. S. MacKay and J. D. Robinson, *Aggregation of Markov flows I: theory*, Philosophical Transactions A 376 (2018), 20170232, [DOI 10.1098/rsta.2017.0232](https://doi.org/10.1098/rsta.2017.0232); [author manuscript](https://wrap.warwick.ac.uk/id/eprint/97255/8/WRAP-aggregation-Markov-flows-I-theory-MacKay-2018.pdf). Sections 2–4 and 6 are the relevant checked passages.

Their directed semi-Markov formalism keeps stationary masses, fluxes and selected mean first-passage times. Equations (3)–(4) give elimination with mean waiting times; equation (7) aggregates using entrance-edge dependence. Section 6 explains how retaining Laplace transforms can retain dynamics, with increasing rational-function degree.

**Exact overlap:** Schur/renewal elimination, entrance memory, compositional selected-mean reduction. This substantially precludes a broad novelty claim for those ideas. **Difference:** this is forward reduction of a supplied model. The checked formulas do not characterize which arbitrary tuples `(S,b_R,b_L,c,w_B)` admit a finite positive CTMC completion, nor the infimum over entrance/exit occupation couplings. Replacing general edge waiting laws with exponential waits preserves their stated first-moment tasks, but does not automatically preserve the equilibrium residual-age contribution represented by `c`.

### 3. Classical scalar phase-type moment fitting

T. Osogami and M. Harchol-Balter, *Closed form solutions for mapping general distributions to quasi-minimal PH distributions*, Performance Evaluation 63 (2006), 524–552; [publisher record](https://www.sciencedirect.com/science/article/pii/S0166531605000738), [author manuscript, with earlier title](https://www.cs.cmu.edu/~osogami/code/momentmatching/closedform.pdf). Definitions 1–6 and the moment-matching discussion in Section 2 were checked; the manuscript constructs closed-form PH fits to three moments. Their discussion also identifies older two-moment Erlang/hyperexponential and Coxian fitting methods.

**Exact overlap at ingredient level:** choosing scalar PH channels with prescribed first and second moments, and using Erlang phases for small variance, is classical. Our already checked Aldous–Shepp result supplies the finite-order variance obstruction. The proposed theorem should explicitly credit this phase machinery. **Unmatched step in these sources:** jointly selecting channel occupation masses with both source margins, under off-diagonal Schur-flow budgets, and showing that this completely characterizes a stationary network record. The `1/epsilon` phase growth in an approximation constructed by Erlang channels is an expected consequence of their variance scaling, not independently surprising machinery.

### 4. Crommelin–Vanden-Eijnden: a convex generator fitting problem

D. T. Crommelin and E. Vanden-Eijnden, *Fitting timeseries by continuous-time Markov chains: A quadratic programming approach*, Journal of Computational Physics 217 (2006), 782–805, [DOI 10.1016/j.jcp.2006.01.045](https://doi.org/10.1016/j.jcp.2006.01.045); [author manuscript](https://homepages.cwi.nl/~dtc/pubs/generator_final.pdf). Sections 1 and 2.1–2.3, particularly equations (10)–(13), were checked.

They estimate a transition matrix from time-series observations, extract spectral information, and fit a same-state-space CTMC generator by a convex quadratic objective subject to nonnegative off-diagonals and zero row sums. **Related conventional machinery:** convex optimization over valid generators. **Different task:** spectral approximation of an observed process, rather than exact completion of a boundary Schur/source record with unrestricted hidden dimension. Its quadratic objective is not the transportation threshold above. This paper is not a collision merely because both methods use a QP.

## Further realization checks

T. Kaczorek, *Positive partial realization problem for linear discrete-time systems*, International Journal of Applied Mathematics and Computer Science 17 (2007), 165–171, [DOI 10.2478/v10006-007-0015-2](https://doi.org/10.2478/v10006-007-0015-2); [primary PDF](https://zbc.uz.zgora.pl/Content/78645/AMCS_2007_17_2_3.pdf). Section 2, Theorem 1 and the conclusions were checked. It constructs internally positive discrete-time systems matching finite impulse-response sequences, with sufficient coefficient conditions. It does not impose our continuous-time stationary closure, labelled port masses, or two different source margins. It is relevant partial-realization history, not a theorem that establishes the stated `iff`.

K. Kim, *On the Relation between Phase-Type Distributions and Positive Systems*, Abstract and Applied Analysis (2015), 731261, [primary full text](https://onlinelibrary.wiley.com/doi/10.1155/2015/731261). Sections 3.1–3.2, especially Theorem 4, show how an excitable stable Metzler realization is transformed into a normalized PH representation. This supplies a broad bridge between positive-system and phase-type descriptions. It does not by itself solve our incomplete moment constraints with fixed boundary trace and masses. The extracted page omits some displayed equations; the comparison uses the readable hypotheses and conclusion, not a new audit of that theorem.

The 2026 paper *A convex approach for Markov chain estimation from aggregate data via inverse optimal transport*, [DOI 10.1016/j.ejcon.2026.101592](https://doi.org/10.1016/j.ejcon.2026.101592), was checked only through primary publisher/abstract and indexed method passages. It estimates a transition matrix and latent transport matrices from distributional observations using an entropy-based optimization. That is a different estimation problem. No claim about all its detailed theorems follows from this limited reading.

## Precise conventional framing of the proposed addition

An economical framing is **a stationary network completion theorem for an incomplete excursion-moment record**. Conditional on a channel `i->j`, classical scalar moment geometry says that entrance flux `f`, occupation mass `M=f E tau`, and second-moment contribution `q=f E tau^2` obey `q>M^2/f` for a nondegenerate finite positive-duration PH channel. The network problem contributes the physical identification of the row and column occupation margins, the constraint `f_ij<=F_ij` off the diagonal, and freely chosen return flux on diagonal channels. Eliminating the flux/moment choices yields the transport objective; classical phase constructions then implement the interior points.

This explanation makes the genuine proposed bridge assessable while keeping familiar mathematics intact. A general positive-realization theorem does not automatically provide it: the relevant full transfer function has not been specified. Conversely, our result should not be advertised as solving general PH/MAP realization, hidden-system identification, or full-memory realization.

Balanced `v_R=v_L` allows diagonal occupation transport with `J_*=0`. Therefore the compact exact regime should be described through this balance of acquired source information. Detailed balance is sufficient for it, but directed boundary circulation need not prevent it. This is a consequence of the proposed criterion and root's construction, not a historical claim extracted from the cited papers.

## Retrieval and remaining priority uncertainty

Targeted Astra searches used the current published input `9301bf5171d4110151e38e5ddebeb1212f593a1c14f7751e019e9a8264a3b8ef` and revision `d6672151ce8e86d4af3e74b3b880abcdc82ae304`. Their new candidate menus did not yield an applicable source for this criterion; no un-fetched candidate is used as a premise. Previously fetched complete N798 and its governing source already supply source-aware Schur composition and remain credited at their established scope. This was not another audit of those accepted results.

Web queries covered positive partial realization, stationary PH/MAP moment representations, Markov-flow aggregation, inverse stochastic complementation and Markov/transport formulations. The two root-suggested primary collision candidates were read in the sections identified above. Failed retrievals were replaced with author/repository copies where available. The note does not establish priority: unexamined network-synthesis, compartmental and matrix-valued moment literature could still contain an equivalent formulation. The defensible statement is limited to **no exact overlap found in these checked sources**, with the classical ingredients and the remaining bridge explicitly identified.
