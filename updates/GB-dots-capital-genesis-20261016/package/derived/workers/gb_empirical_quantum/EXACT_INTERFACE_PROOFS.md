# Exact Willow feature and preparation interfaces

Status: internally reconstructed analytic statements and exhaustive finite algebra checks. External correctness and novelty are not established. These are evaluator operations, not a new decoder or physical-memory result.

## 1. Contract and source boundary

Fix one of the supplied `d5_at_q8_7/X/r13` or `/r50` ideal circuit annotations. Let `m` be its entire raw measurement bit string, let `s` be the known 25-bit preparation sweep, and write its actual evaluation observable as

`y = l m + q s + c` over GF(2).

The source map gives terminal indices `[0,5,10,15,20]` for `l`, sweep support `[0,5,10,15,20]` for `q`, and `c=1`. Terminal indices start at raw measurement 312 or 1200. All rank counts below hold at fixed known sweep and therefore omit the 25 known-input coordinates. The script independently parses all `M`, `DETECTOR`, and `OBSERVABLE_INCLUDE` annotations and compares their measurement masks and qubit order with the supplied maps. It does not rederive the reference constant; that comes from the packet's independently simulated reference. The constant does not affect leakage or translation proofs.

The admissible feature interface F consists of every ancilla readout and the twelve terminal stabilizer parities. It includes the detectors. Arbitrary processing of F and the known preparation is permitted by the mathematical statement. No terminal logical parity is an input.

`exact_interface_tests.py` reads no r50 measurement, detector, label or prediction bytes, and reads no r13 outcome bytes. Its sole experimental-record input is r13 `sweep_bits.b8`. Its exact read manifest is in `exact_interface_results.json`.

## 2. Feature-span equivalence and nondetermination

Let H be the twelve terminal stabilizer masks on 25 final data bits. The script gives `rank(H)=12`. Let A select all `24r` ancilla bits. Then

`rowspan(F) = rowspan(A,H)`.

The independently parsed detector rows D, supplemented with the complete first 24-bit ancilla frame I0, have exactly the same row span:

`rowspan(D,I0) = rowspan(A,H)`.

The finite certificate checks rank equality for each set and their union, not merely equal dimension. The resulting ranks are 324 at r13 and 1212 at r50. There are thirteen unresolved raw-bit degrees of freedom in each case. Adding l increases rank by one.

Thus the complete initial frame contributes twelve new algebraic dimensions beyond detectors, and is already sufficient to reconstruct all ancilla outcomes and terminal stabilizer parities in this affine interface. No new information is created by reconstructing later absolute frames from those inputs.

For a stronger statement than exclusion from a linear estimator, the script exhibits a translation z supported on terminal data positions `[0,1,2,3,4]`, physical qubits `[1,4,8,15,23]`. Its raw measurement positions are `[312,313,314,315,316]` at r13 or `[1200,1201,1202,1203,1204]` at r50. Exact bit checks give

`F z = 0`, `D z = 0`, and `l z = 1`.

For every arbitrary raw string m and fixed sweep s, the strings m and m+z therefore have identical admissible features and opposite evaluation targets. Consequently **no deterministic function, linear or nonlinear, of F and s computes y on the whole binary-record domain**.

This is an algebraic nonreconstruction statement. It does not establish empirical independence, nonzero conditional information, absence of all statistical leakage, support of both records under a particular device noise law, or any decoder gain. A narrow physical support can make a target predictable even when it is not determined on the unrestricted domain. If new nonlinear functions of excluded raw bits are admitted, they need their own feature audit.

## 3. Exact minimum extra raw-terminal leakage

Suppose a feature designer appends a set B of individual terminal raw bits to F. Then the label is exactly reconstructible if and only if

`l in rowspan(H,{e_i : i in B})`.

Equivalently, some vector in the affine coset `l+rowspan(H)` is supported within B. Proof: a representation `l=h+b` directly gives such a coset vector b; conversely such a b gives the representation. Ancilla masks cannot help to cancel a terminal-only label once all ancilla coordinates have been separated.

The script exhausts all `2^12=4096` members of this coset. Its minimum weight is **five**, attained by **52 distinct terminal-bit masks**, all saved explicitly. It also exhausts all 8192 members of `ker(H)` and all 4096 that flip l; their minimum weight is five. This second enumeration supplies the explicit indistinguishability witness above.

Therefore fewer than five additional individual terminal raw bits cannot determine the target, even after arbitrary nonlinear processing of the resulting linear feature vector. Some sets of exactly five do determine it, including the released logical-parity support. Five is the minimum addition size, not a claim that every five-bit set leaks. For one minimum leaking set, all five single deletions are independently checked to remove exact leakage.

These counts are specific to these two supplied distance-five X-basis annotations. They are not a new code-distance theorem or evidence about other circuits, soft readouts or learned performance.

## 4. Preparation design and current aliases

The original r13 sweep bytes give exactly ten unique 25-bit configurations, each repeated 5000 times. Their ordered configurations agree with the source control audit. Let S be the ten-row matrix. Exact rank gives

`rank(S)=6`, `rank([1|S])=6`.

For any observed linear-parity value vector, its equivalent masks form one coset of `ker(S)`, with `2^19` members. Allowing a constant gives equivalence classes of size `2^20`. Replicating the same rows cannot change these ranks or equivalence classes.

For the source's strongest determined tag `e22+e23`, exhaustive weights 0, 1 and 2 find exactly eleven weight-two masks: the original plus the ten reported aliases. All are equal on the current ten configurations. This selection was already outcome-informed in the source; no new inference or pristine preregistration is claimed.

## 5. An optimal four-pattern separator for the eleven shortest candidates

For this explicitly restricted finite candidate set, each additional prepared string supplies at most one binary coordinate in its covariate signature. All eleven candidates start with the same old signature. Hence at least `ceil(log2(11))=4` new strings are necessary to distinguish them.

The candidates form eleven edges of a forest on the 25 bit indices. Assign edge signatures 1 through 11 in four-bit binary. For each component, choose a root vertex code zero; propagate vertex codes by `code(v)=code(u) XOR edge_signature(u,v)`. A forest makes these assignments consistent. For each of four bit positions j, take the new contrast mask to contain precisely vertices whose codes have bit j set. Every edge then has its assigned distinct four-bit parity signature.

XOR each contrast into existing configuration zero. The resulting four strings are new, mutually distinct, and separate all eleven candidates. Exact contrast masks are:

- `[4,11,13,16,19,23]`
- `[4,12,21,23]`
- `[9,11,12,16]`
- `[19,21,22,24]`

The complete prepared strings and all eleven signatures are saved in `exact_interface_results.json`. This construction meets the four-string lower bound. Complementing a string does not change any weight-two parity, so adding its complement for balanced preparation would double settings while adding no separator information for this candidate family.

This is a proposed unexecuted control design, not four acquired settings or four sufficient outcome observations. It separates parity covariates under a declared candidate restriction. Repeated noisy responses, randomized/interleaved assignment, stationary calibration, identical acceptance rules and an explicit response model would still be needed for scientific inference. It cannot identify arbitrary nonlinear preparation effects or causal microscopic mechanisms.

## 6. Exact unrestricted rank-completion costs

Each new distinct row raises rank by at most one. Linear-parity identification over all 25 coordinates requires rank 25, so **at least nineteen additional strings** are necessary. Affine-parity identification, including the offset, requires rank 26, so **at least twenty** are necessary.

The script constructs matching upper bounds by greedily appending zero and standard-basis preparation strings only when they increase the applicable rank. It obtains full rank with exactly 19 or 20 new strings. Thus both bounds are sharp for algebraic covariate identification.

If the experimental design must retain complementary pairs, the old row span already contains the all-ones difference between paired strings. In the affine representation that difference is `(0,1,...,1)`, also already present. Each new complementary pair can therefore add at most one rank. Completing the design then needs 19 new pairs (38 settings) for linear masks or 20 new pairs (40 settings) for affine masks. Complementing the explicit completion strings achieves those ranks.

The four-pattern separator raises linear rank only to ten, leaving `2^15` masks per unrestricted linear equivalence class. It must not be described as solving the unrestricted design problem. Time, repeated-shot, physical X-pulse and preparation costs for executing any of these designs remain unacquired. Existing shot count does not replace missing preparation directions.
