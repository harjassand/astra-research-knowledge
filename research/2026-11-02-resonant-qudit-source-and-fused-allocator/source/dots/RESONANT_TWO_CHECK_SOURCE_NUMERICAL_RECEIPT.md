# Actual resonant two-check source: finite-cell numerical receipt

2026-11-01. **Positive finite-cell test, not a uniform graph theorem or a practical memory threshold.** No external source access or hardware actions. This is the resonant sequential source, NOT the off-resonant Raman latch.

## Main result

Two overlapping checks ZZ and XX on the same two data qubits, with private 11-level apparatus each, have the following exact-Lindbladian numerical results at g=gamma=1 and pure plus preparation. Columns refer to either check; symmetry was checked, not assumed.

| pump r | retained cache wrong | per-check report flux | positive Poisson price range | isolated flux |
|---:|---:|---:|---:|---:|
| .001 | .00105851993 | .000994528734 | 1011.291058 | .000994530085 |
| .01 | .0100762664 | .00947750342 | 111.284619 | .00947867299 |
| .05 | .0414867547 | .0391329715 | 31.2652664 | .0392156863 |
| .1 | .0679022374 | .0641489674 | 21.2554088 | .0645161290 |

Total pair report rate is TWICE the displayed per-check rate. Two isolated sources at the same r have total rate twice the isolated column. Pair/isolated per-check flux ratio declines only to approximately .9943 at r=.1, while wrong-cache probability reaches approximately .0679: throughput alone would miss the dominant effect.

With a physical convex minus-preparation branch p=.001, retained wrong values become .00205640289, .0110561139, .0424037812, .0687664329, respectively. Flux is unchanged in these examples. For comparison, an isolated source has retained wrong exactly p, within floating-point error.

The low-duty data support an approximately O(r) overlap error for THIS pair, with no high-order Raman slowdown. They do not establish a uniform-degree coefficient or prove a general asymptotic law. No arbitrary noise threshold or independent progress process was assumed.

## Actual model and gauge verification

Each apparatus basis is

    idle; g1,0 g1,1; e1,0 e1,1; g2,0 g2,1; e2,0 e2,1; final,0 final,1.

Each gate uses H_j=sum_b |e_j,b><g_j,b| tensor P_j^b+h.c. The separate stage jump is the COLLECTIVE sum_b |g_next,b><e_j,b|, with last target final. Probe coherence is not measured by this jump. Preparation jumps are sqrt(r(1-p))|g1,+><idle| and sqrt(rp)|g1,-><idle|. Readout jumps are |idle><final,s_X|, and the classical cache is overwritten with s. These are the actual generator ingredients, not effective operations or external scheduled gates.

Define prefix Q_a(state): idle and g1 have I; e1 and g2 have P_a1^b; e2 and final have S_a^b. Fix order U=Q_Z Q_X. Construct every physical Hamiltonian edge and every physical jump on dimension 11*11*4=484, then form the isometry V mapping each apparatus basis state to that basis state tensor U|Bell>. Reduce each term using V†OV ONLY after computing OV−V(V†OV).

The largest off-sector residual is 1.05e−15. This was checked separately in all four Bell sectors. Thus all physical terms preserve each dressed syndrome sector to the tested precision, including preparation and collective decay. Relative-error, report-flux, and Poisson outputs agree across all four sectors; negative-syndrome readout outcomes are relabelled correctly.

Crucially, the reduced model is NOT a tensor product of independent sensor dynamics. In the chosen gauge the X-gate edges acquire signs conditional on the Z prefix, while Z-readout amplitudes acquire signs conditional on the X prefix. Every such conditional sign is retained by the matrix reduction. There are no intermediate resets or hidden partial-Pauli cleanup channels in this model.

## Retained cache calculation, not error per report

Let L be the apparatus Liouvillian in one dressed Bell sector and rho its steady state. J_c and J_w are the gain superoperators of correct/wrong readouts of the target apparatus. They exclude their anticommutator terms. With K=L−J_c−J_w, the wrong-cache density solves

    K rho_w = −J_w rho.

The two cache densities are rho_w and rho−rho_w. Their traces sum to one. The retained error is mu=Tr rho_w. Numerical minimum eigenvalues of rho, rho_w and rho−rho_w are nonnegative in the pair runs; the smallest correct-cache eigenvalue is approximately 1.79e−12. Steady residuals are below 4e−16, and retained-density solve residuals below 4e−18.

At r=.1,p=0, wrong probability per report is .0678606657, whereas retained wrong is .0679022374. The latter is the quantity needed for the cache potential. Their closeness here is not used as an identity.

## Exact finite-cell Poisson price

The classical cache need not double the quantum Hilbert matrix. For its two observable blocks h_c,h_w, put d=h_w−h_c. The equations

    K* d = −I,
    L* h_c = mu I − J_w* d

give the full retained-cache adjoint equation

    L_cache* h = −e_wrong + mu I.

The arbitrary scalar gauge is fixed by Tr(rho h_c)=0. Shift both blocks by minus their joint minimum eigenvalue to get Z>=0. Its norm is the joint spectral range reported above. Both cache-block residuals are below 4.5e−12, with Hermiticity residuals at floating-point scale. These are numerical certificates, not interval-arithmetic rigorous inequalities.

The O(1/r) price is real. Dilution reduces the mean error but enlarges the unscaled service price. Scaling this price by a slower consumer coefficient, controlling cross-generator action, and keeping its positive potential below a barrier are separate obligations. This finite TWO-check corrector is not automatically a local corrector on a larger graph.

## Same-hardware isolated baseline and resources

The isolated source uses the same 11 levels, g, gamma, pump, preparation impurity, collective decay and readout model. Each driven stage has mean duration 2/gamma+gamma/(4g^2)=2.25 at g=gamma=1; readout adds 1. Thus mean active service is 5.5 and report flux is r/(1+5.5r), matching the independent numerical solve. Isolated positive Poisson range is 1/r+11.3903882032 for these parameters. This is a baseline, not a perfect external controller or a claim of autonomous superiority over active extraction with identical hardware.

Physical charges remain: 11-level selective onsite structure, apparatus/data couplings, the coherent-preserving collective reservoir (which-b indistinguishability), actual pump/readout baths and preparation impurity. Additional thermal absorption, dephasing, spectral drift, data faults, or readout faults were NOT simulated or silently set below a threshold.

Sparse Liouvillian dimension is 14641 by 14641 with 60365 nonzeros; no dense Liouvillian was built. The run's peak resident memory was approximately 85.6 MiB. Eight parameter cases including density, two retained caches, and Poisson prices took roughly 2 seconds of local computation; each additional Bell-sector run was comparable. Dense diagonalization was confined to 121-dimensional density/observable blocks.

## Reproducibility

Directory: `coherent_lyapunov_memory_20261101/sequential_source_audit/`

* `run.py`: full-data construction, sector leakage test, pair solves and exact cache-block Poisson equations. Run `OPENBLAS_NUM_THREADS=1 python run.py`; optional `BELL_SECTOR=1,2,3` selects another sector.
* `results.json`, `results_sector1.json` through `results_sector3.json`: complete pair outputs. Primary-sector output additionally records correct-cache positivity checks.
* `log.txt`, `log_sector*.txt`: numerical logs and primary run memory/sparse size.
* `baseline.py`, `baseline.json`: same-hardware isolated source and analytic flux comparison.

No claim is made that stationary performance or this finite-cell Poisson solve independently proves the separate uniform finite-time refresh theorem. It is a discriminating exact microscopic consistency test of its proposed source family.
