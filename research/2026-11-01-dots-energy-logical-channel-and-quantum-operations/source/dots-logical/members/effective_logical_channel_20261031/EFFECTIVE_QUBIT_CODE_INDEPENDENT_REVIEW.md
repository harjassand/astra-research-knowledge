# Independent executable review: rational effective qubit acquisition

## Exact source binding and verdict

I read the complete final implementation, test harness, and mathematical CP/numerical proof, reran the author checks without overwriting their JSON, and added an independent adversarial suite.

Bound artifacts:

- `acquire_effective_qubit.py`: `c6d8134e4964e696e01faf24bd5ef46571cab4a2722067ea63cfd2bb987599ee`.
- `test_effective_qubit.py`: `fb8a9d37d916509235f1fe271e614e7bf6c7e947b5a4f9086bee16a26e46fa51`.
- Author `effective_qubit_checks.json`: `857977c151e6c197cb23ff9b39e9898ac6f6b99c5258de93d608514d3ed7c188`.
- `EXACT_RATIONAL_CP_ACQUISITION.md`: `a9a8e801b7b11c6bfd2c4b7932cc0a3f33b155f6e1e50153799c07cd026213a2`.
- Independent `independent_effective_qubit_audit.py`: `503ca0725476173ee71dd40ff01a143aeeb2b6cbb5a69a3c4b7b94cf3de547d2`.
- Independent `independent_effective_qubit_checks.json`: `b89039c3233774d1455d7a37f2079eaefd31d42e117c5f4e73624708085be29c`.

Verdict: PASS for this restricted classical acquisition prototype and its exact CP-channel certificate, receiving the separately reviewed effective logical-channel theorem. The optional quantum gate realization is a constructive finite-dimensional interface, not an executed backend. No physical-source learning, black-box model validation, source-output simulation, or general controlled-system implementation is claimed.

## 1. Validated task and actual coefficient acquisition

The public acquisition entry validates integral nonboolean n/site and the declared positive rational parameters, rejects excessive uniform bond strength, and returns ABORT when the finite-rate error certificate cannot fit its assigned budget. Rational coercion is interpreted as the actual exact supplied value, not evidence about a physical mechanism. Internal algebra helpers receive the validated positive-domain arguments; they are not separate general-purpose public validators.

The succinct uniform model matters. The program does not read an arbitrary length-n table and then pretend that only local input was required. With t=(q-1)/(q+1), the actual uniform interior absolute row sum is 2|t|/(1+t^2)<=1/20, and the boundary sum is |t|. Thus the code's |t|<=1/40 condition really supplies kappa=19/20, including both endpoints and negative bonds. This is a direct row certificate; it does not incorrectly infer |J|<=1/40 merely from |tanh J|<=1/40.

The integer computation isqrt(floor(lambda)) equals floor(sqrt(lambda)), so the model bound uses a safe lower denominator. The lambda<1 branch is conservatively uninformative and aborts for the admitted epsilon range. The radius loop uses the proven channel coefficient-tail bound, with exact zero error when the full chain is present. The tridiagonal coefficients and covariance column are oriented correctly. Strict row diagonal dominance makes the Thomas pivots nonzero; the accepted weak uniform family also keeps them positive. The returned D is positive and bounded by 1/kappa.

Only O(R) local sites enter the solve, with R logarithmic in requested coefficient accuracy until physical boundaries are reached. Exact fraction lengths grow polynomially in local input size and accuracy bits. Large n enters as an integer description and boundary comparisons. This is not arbitrary-data acquisition at sublinear cost.

## 2. Rational Taylor/scaling certificate

The Schrödinger generator is exactly -i[X,.]+2D(Z(.)Z-(.)), with diamond norm at most C=2+4D. Choosing N=2^s>=4C gives single-slice action at most one quarter. The explicit Taylor remainder 2/4^(K+1) is conservative; the actual factorial denominator only improves it. The integer inequality e0<=delta/(4N) is checked by exact fraction arithmetic.

The polynomial slice is exactly trace- and Hermiticity-preserving. Its complete norm is at most 1+e0 because the exact slice is a channel. Telescoping N products yields (1+e0)^N-1<=2N e0<=delta/2. This is not an assumption that the approximate slice is CP. Squaring preserves its exact TP/HP identities.

Since D<=1/kappa, N<=32 in this fixture. K and rational arithmetic bit lengths are polynomial in the encoded input and precision; there is no inverse-accuracy time-step loop hidden in the procedure. The code computes actual exact fractions, not a floating exponential labeled exact.

## 3. Choi, repair and Kraus orientation

Column vectorization and the implemented reshuffle agree with

J[2i+a,2j+b]=E[a+2b,i+2j].

The output partial trace is the code's two-by-two marginal. From the diamond error delta/2, the unnormalized qubit Choi trace-norm error is at most delta, so Jhat>=-delta I. The repaired matrix (Jhat+2delta I)/(1+4delta) is strictly positive and has exact TP marginal. Positivity is earned by the padding, not by an assumed spectral gap of the true channel.

Equivalently the repair adds 4delta times the completely depolarizing qubit channel before normalizing. Its distance to the true effective channel is at most delta/2+8delta<9delta=eps_num. The proof and implementation constants agree. Both the raw HP/TP assertions and the repaired marginal are checked exactly.

Positive exact Hermitian LDL factors yield the four Kraus operators K_j[a,i]=sqrt(d_j)L[2i+a,j] with the stated orientation. Their algebraic square roots are a representation, not rounded entries. TP gives sum K_j dagger K_j=I. A valid Choi factor is therefore a genuine CP channel, not a postselected normalized dense map.

## 4. End-to-end budgets and optional circuit interface

The code assigns epsilon/2 to finite-rate admission, epsilon/4 to source coefficient truncation, epsilon/8 to numerical CP acquisition, and reserves epsilon/8 for optional gate synthesis. The actual record carries both the represented-channel total and the combined total with the gate reserve. The latter remains at most epsilon. No gate synthesis is silently declared already performed.

Stacking the four Kraus operators gives an 8-by-2 isometry. A constant-dimensional unitary completion and ordinary two-level synthesis provide an acquired gate interface on paper. TP makes the two input columns orthonormal. Pivoting on a largest remaining component or discarding a sufficiently tiny pair with charged norm error avoids a free tiny-pivot inverse. Algebraic square-root entry errors and the total unitary/rotation error are paid at the proposed absolute tolerances. The induced channel error is at most twice the Stinespring operator error, fitting the reserved budget with slack. This is ordinary fixed-dimension channel synthesis, not a new gate compiler or a source-sized operation.

## 5. Verifier scope and actual repair history

The final `verify_channel` checks ONLY the exact CP/TP representation. It enforces four-by-four complex-rational matrices, exactly four positive pivots, positive denominators, reduced fractions, integer-not-boolean components, and the unit-lower LDL convention. It checks Hermiticity, the TP marginal and exact factor reconstruction. Shape/number/parser failures return False rather than being accepted as a different-dimensional object.

The separately named `verify_record` recomputes the entire deterministic known-program acquisition and compares its full structure and exact types, then checks CP. It therefore rejects changed task/scope text, radii, coefficients, error claims and malformed declared inputs. This remains an algebraic binding to the declared known program, not a test of whether a physical black box obeys that program.

An actual issue was found during the unbound working-code audit: plain Python dictionary equality accepted bool/float aliases in unchecked metadata. On a valid n=1 record, local_sites[0]=False or 0.0, and an error numerator=True, were accepted by that working full-record checker. The final code uses recursive strict type-and-value equality, and those probes now reject. The author added the aliases to the test harness. Earlier working shape-check concerns were already being repaired concurrently; no failure is attributed here to the final c6d8134e bytes. This receipt preserves the distinction rather than erasing the caught verifier issue.

Exact large JSON integers must remain arbitrary-precision integers. Parsing certificates through IEEE floating-point values destroys this contract. A valid CP factor with deliberately altered source/error metadata can still pass `verify_channel`; my tests confirm that `verify_record` rejects the same object. That difference is intentional and load-bearing.

## 6. Independent executions and artifact checks

I reran all 83 author assertions through the imported test function, without overwriting the frozen author JSON. I also ran 93 independent checks, including strict aliases, malformed top-level objects and five-by-five factors, invalid denominators and number types, altered scope/error metadata, invalid acquisition inputs, an honest ABORT, signed weak-bond endpoints, and covariance symmetry under uniform bond-sign reversal.

The independent admitted cases included n=10^30 with a radius-four local solve. That verifies the code path uses the succinct uniform program and local radius rather than enumerating n states. It is not a physical experiment or proof about arbitrary huge source data. Observed runtimes are recorded in the independent JSON and are environment-dependent; they are not universal performance guarantees.

I separately loaded and exactly verified both current saved records:

- `effective_qubit_certificate.json`, SHA `9325ff4e7596335589d0995901901428c95db29872ee62c251bb11b56fda3ebc`, uses sites [6,10].
- `effective_billion_spin_certificate.json`, SHA `2ddbe85170b476fdbc4d003eae3dd35e99e00552fec25594b7ae9434b624b2c4`, uses sites [499999996,500000004].

Both passed CP-only and full-known-program verification. The older 1e-4 artifact is not relabeled as current output. Floating SciPy Choi comparisons in the author harness remain diagnostics; the complete-norm certificate is the rational proof above, not a numerical eigentest.

## Consequence

The implementation concretely acquires a certified ordinary logical-qubit channel for the admitted known uniform source task, including arbitrary initial correlations under the received invariant-algebra theorem, with the bath discarded. It does not execute the old full retained-source simulator and does not validate source observations. For this deliberately weaker task, the ordinary reduced-channel method is a real constructive alternative, not a hypothetical oracle. No practical quantum advantage, novelty, or equally informed ordinary-method superiority is asserted.
