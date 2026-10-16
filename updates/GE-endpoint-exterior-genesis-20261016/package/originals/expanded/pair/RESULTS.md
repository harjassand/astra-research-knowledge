# Exact-model receipts and practical boundary

All graphs are synthetic. Rates are supplied, horizon T=1, deterministic initial states, and comparisons use the entire endpoint distribution. The code runs original NumPy/SciPy finite-state linear algebra, not Monte Carlo. No acquired code was executed and no package was installed.

## Three clean-gap cases

All fast internal rates are W=100,000. Every slow boundary edge has rate .2.

1. Ten-vertex exclusion, five occupied sites: five fast dimers connected in an alternating slow ring. Initial occupancy is one occupied vertex per dimer. Full state count 252; fast-orbit quotient count 51. Five fast and five slow edges.
2. Eight-vertex exclusion, four occupied sites: two fast K4 cliques joined by one slow edge. Initial occupancy {0,1,4,5}. Full state count 70; orbit quotient count 5. Twelve fast and one slow edge.
3. Six-vertex full interchange: two fast triangles joined by one slow edge, identity initial permutation. Full state count 720; orbit quotient count 20. Six fast and one slow edge.

The cap budgets below are .05 for rate replacement alone. All certificates integrate to infinite original rate. They do not exploit the finite original W. Lambda is expected uniformization candidate events, not measured CPU time.

| Model | Original Lambda | General local K | General local Lambda | Actual TV at that K |
|---|---:|---:|---:|---:|
| Five dimers, exclusion | 500001 | 645.4126 | 3228.063 | 0.000324808 |
| Two K4s, exclusion | 1200000.2 | 61960.7817 | 743529.581 | 0.0000001683 |
| Two triangles, interchange | 600000.2 | 6758.4813 | 40551.088 | 0.0000102713 |

This general bound is very conservative. The K4 example has only about 1.6-fold certified event-count improvement at W=1e5 despite enormous actual slack. No superiority over established acceleration methods follows.

| Model | Homogeneous-clique K | Homogeneous-clique Lambda | Actual TV | Exact-model observed 5% crossing K |
|---|---:|---:|---:|---:|
| Five dimers | 23.7164 | 119.5819 | 0.00883833 | 4.05533 |
| Two K4s | 26.2545 | 315.2536 | 0.00104247 | 0.880512 |
| Two triangles | 13.0544 | 78.5263 | 0.00568459 | 1.61697 |

The last column is a numerical root of the exact endpoint-TV curve, not a uniform theorem or a proof of global optimality. The specialized certificate uses homogeneous complete fast components, an assumption absent from the general local theorem.

For context, original N727 .05 caps are 7,456,271.5 / 7,555,682.1 / 1,089,483.1. Merely tightening its global constant and entropy integral, without localization, reduces these to 1,313,703.1 / 1,261,495.3 / 161,712.0. All are above the tested W, so applying those uniform thresholds gives no capping acceleration here.

## The clean-gap averaging comparator wins

Uniform-permutation conditional-color shuffling plus exact boundary attempts has these full endpoint errors relative to W=1e5:

| Model | Actual full endpoint TV | Rigorous elementary averaging bound | Boundary attempts Gamma |
|---|---:|---:|---:|
| Five dimers | 0.00000211047 | 0.0000120 | 1 |
| Two K4s | 0.000000274118 | 0.0000132 | .2 |
| Two triangles | 0.000000744516 | 0.0000088 | .2 |

The limiting law was computed independently through fast-orbit projection. The rigorous bounds use the renewal inequality (A1) in the proof file. A practical implementation needs shuffles and boundary attempts, not the enumerated quotient states used for this audit. Thus these examples support the validity of local saturation but do not supply its missing practical advantage over clean-gap averaging.

## One bounded graded-path test

Six-vertex full interchange, identity start, physical path edge rates [1,10,100,1000,10000], T=1, original Lambda=11111. Full state count 720.

| Uniform cap K | Exact endpoint TV | Capped Lambda | Best tested contiguous-cluster finite-rate certificate |
|---:|---:|---:|---:|
| 10 | .0697278 | 41 | 82.1953 |
| 20 | .0280857 | 71 | 44.2585 |
| 50 | .00855634 | 161 | 20.2626 |
| 100 | .00265973 | 311 | 9.44921 |
| 1000 | .0000821388 | 2111 | .656323 |
| 5000 | .00000912035 | 6111 | .0846461 |
| 8000 | .00000227994 | 9111 | .0218380 |

The finite-rate certificate subtracts B_local(W;c,b) from B_local(K;c,b) for each changed edge, minimizing over every contiguous physical interval containing that edge. It remains much too conservative to certify the useful K=20 compression. K=8000 gives only modest certified savings.

The proposed graph also fails to demonstrate a true averaging obstruction:

| Uniformly shuffled fast tail | Actual endpoint TV | Total retained boundary/slow attempts Gamma |
|---|---:|---:|
| Vertices 1–5 | .0488908 | 1 |
| Vertices 2–5 | .00352249 | 11 |
| Vertices 3–5 | .000233302 | 111 |
| Vertices 4–5 | .00000911881 | 1111 |

These are exact-model comparisons, not claims that the elementary renewal bound certifies each graded-path averaging choice. In particular, small actual error does not imply an available useful a priori certificate. Still, this graph provides no actual endpoint-error evidence that capping can do something equilibrium blocks cannot do.

## Numerical checks and files

- 60 random six-vertex exclusion checks varied the distinguished edge and other rates over broad logarithmic ranges. Each checked the local smoothing inequality and full spectral Frechet endpoint derivative against its two-sided envelope.
- 210 independent restricted unordered-pair generator checks covered cluster sizes 2 through 8 and rates over ten orders of magnitude. They checked the improved mean-meeting constant.
- Maximum raw probability-mass defect in the clean-gap endpoint solves was below 1e-9. The computations are floating-point checks, not interval-arithmetic proofs. Tiny negative roundoff was clipped and distributions normalized before TV calculation.
- `run_checks.py`, `run_multiscale.py`: complete original source.
- `results.json`, `endpoint_results.csv`, `run_stdout.txt`: clean-gap numerical results.
- `graded_path_results.json`, `graded_path_stdout.txt`: graded-path results.
- `graded_path_generators.npz`, `graded_path_endpoint_K*.npy`: reproducible full generators and endpoint arrays for independent follow-up.
- `LOCAL_SATURATION_PROOF.md`: the derivation, assumptions, and comparator bound.

Bottom line: the local heterogeneous-cluster bound is valid under the stated model, and its constants can be improved. The clean-gap examples favor a rigorous uniform-shuffle averaging incumbent. The bounded graded example shows large empirical capping compression but the simple local certificate cannot validate the useful cap, and averaging is also accurate. A broader practical advantage remains unestablished.
