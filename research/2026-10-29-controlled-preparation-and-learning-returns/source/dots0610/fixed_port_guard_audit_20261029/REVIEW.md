# Independent review: fixed four-spin-port concatenated guard

**Decision: ACCEPT at the scoped ideal-interface mathematical and finite-execution claims described below, conditional on unchanged governing dependencies.** Not a hardware demonstration, ordinary memoryless quantum-capacity theorem, superior conventional coding algorithm or practical total-runtime rate result.

## 1. New mathematical obligations checked

The generator sampler is uniform over isotropic r-subspaces conditional on successful finite sampling. At dimension j the rejection probability is2^(2j−2ell), independent of the actual subspace, so truncating each rejection loop at a fixed cap does not bias accepted subspaces. Equal isotropic flags and symplectic transitivity give Pr[e∈S-perp]=(2^(ell+k)−1)/(2^(2ell)−1) for every nonzero e. The author's finite code-generation abort bound beta0^R+Rr2^(−L_bit) is conservative and valid. Seeded pseudorandom execution is not physical unbiased randomness.

The low-weight-volume bound uses x=1/48 and x^w≥x^h for w≤h; sum_{w≤h} C(16h,w)3^w≤48^h(17/16)^(16h)<144^h<2^(8h). Thus the claimed union-bound rejection estimate holds. Exhaustive verification, rather than the existence estimate, protects every deployed code. Its O(B^8 poly(h)) upper bound is polynomial but potentially prohibitive; no free code oracle is supplied.

Circuit-induced stabilizer signs correctly define the code via the actual inverse Clifford, avoiding an unsigned-generator ambiguity. The exact i^phase X^x Z^z conjugation updates are correct for H,S,CNOT,SWAP. Distance excludes all nonidentity normalizer elements below h, stronger than needed. Radius u=floor((h−1)/2) gives unique correctable-error syndromes. Default identity correction on all unlisted syndromes makes recovery total; it does not detect every uncorrectable error.

The two-stage concatenated recovery corrects at least t=(B/8)ceil(h/2) native faults: every uncorrected inner block requires at least u+1 support sites, so weight≤t affects at most B/8 residual outer symbols. Arbitrary coherent error operators on each fixed support expand in Paulis. Inner syndrome recovery maps the correctable span to logical identity tensored with syndrome/environment operations; arbitrary residual maps stay supported on the bad outer symbols. The outer QEC span property therefore applies to source-memory-correlated coherent combinations, not only sampled Pauli faults. Prior trusted port isolation and non-revisitation of stored service outputs are indispensable.

With N=16hB, t≥N/256. For b=floor(t/4), the existing R=1 negative-binomial guard gives Pr[Bin(t+b+1,1/2)≤b]. Since t−b+1≥3t/4 and t+b+1≤3t/2, Hoeffding gives exp(−3t/16)≤exp(−3N/4096). With service probability2/9 and cap9N, expected service-coin count2N gives shortage probability≤exp(−N/4). The availability algebra from expected validation failures≤(32/3)L_T and b+1>N/1024 is correct, giving the stated (32768/3)L_T/N term. This step RELIES on the separately reviewed actual-history gap-free learner and collective-algebra promise, not on a new audit of those dependencies. Source-exposure ratio (hB/2)/(4×9N)=1/1152 is exact; construction, arithmetic, gates and trusted buffering are outside that denominator and explicitly remain paid costs.

## 2. Actual independent execution

A different C++ enumeration algorithm traverses lexicographic supports and base-three labels (author uses recursive support traversal). It checked exactly96,10296,1143264,130354980 nonidentity Pauli labels for saved lengths32,48,64,80, respectively. No label below claimed distance2,3,4,5 has zero syndrome. Thus the [[80,5,≥5]] claim is independently confirmed, not inferred statistically. All saved correction-table entries and canonical compiler span were recomputed.

The corrected dense five-qubit and locally scrambled fixtures rerun successfully, preserving arbitrary logical-memory-reference states under coherent correctable errors. The actual generated h5 inner code combined with received GF32 outer binary circuit/decoder reruns all100 concentrated/dispersed native-error cases: N2560, payload80, radius12,8496 outer encoder gates and2118 inner decoder gates. These are exact Pauli/field propagation checks, not a dense2560-qubit simulation. General coherent correctness is the mathematical span argument above, backed by the small dense tests, not by those100 large Pauli samples alone.

The initial compiled verifier's128-bit limit was resolved with a Python arbitrary-integer fallback. The reviewer additionally exercised that branch with a129-generator, n130,k1 isotropic code, exactly checking all390 weight-one Paulis without truncation. This establishes the branch is live; it does not establish practical high-h performance.

## 3. Defect found, correction and preserved negative evidence

The first dense decoder test indexed correction tables by the raw tensor syndrome integer. Tensor order makes wire0 most significant, while table order packs measured outcome_j at2^j. The original perfect five-qubit fixture accidentally had a bit-reversal-symmetric correction table, masking the mismatch. The reviewer constructed a locally Clifford-equivalent distance3 code where direct lookup fails on correctable errors; reversing bits before lookup restores recovery. `order_counterexample.json`, `check_order.py` and the original source snapshot preserve this useful failure.

The author corrected the dense lookup, specified physical readout packing in GOVERNING_v1, and added a scrambled fixture. The corrected files are the ones accepted. This was a real implementation-interface defect, not failure of the stabilizer distance or concatenation argument.

## 4. Resource and claim boundaries

The construction is not gate optimized. SWAP routing, inverse-S implementation, physical control errors, storage and measured-record retirement need separate implementation/budgeting. Earlier eight-CNOT inner four-spin interfaces and complete leakage-reset ordering remain governing. The fixed-port conventional full-path alternative may use the same concatenated code and asymptotic orders; the author correctly does not claim a matching-specific coding or capacity advantage.

Finite code/sampler aborts are paid. Arbitrary noise may always reject. Successful-looking syndrome decoding does not certify actual error weight. No safe retry of the same unknown payload after abort is implied. Theorems depend on private current roles/settings and the declared full-joint source/endpoint separation. Previously accepted dependencies are relied on at their reviewed scope; this review does not silently extend them.

## 5. Reproducibility

`source/` preserves the originally received, defective dense-interface snapshot; `corrected_source/` holds the corrected replay snapshot. `independent_distance.cpp`, `review_checks.py`, `independent_results.json`, `check_order.py`, `order_counterexample.json`, and `wide_syndrome_fallback.json` are new independent review evidence. The receipt binds final governing author sources and review evidence; original and corrected files are not interchangeable.

## Final freeze and parameter replay

The author's corrected GOVERNING_v1.md and AUTHOR_FREEZE.json were received. All corrected dense, scrambled dense, concatenated-circuit and rational parameter output JSON reruns match exactly as parsed JSON. The h50 validation-abort term is0.0464993633959006; h40 is1.5729412998871932 and thus vacuous. This term still excludes role-shortage and separately paid sampler/code abort contributions. The rational parameter script uses the received regret bound; its arithmetic and inequalities were checked, without independently extending the prior learner theorem. No end-to-end high-yield claim follows from the executed h5 code: its displayed conservative validation-abort bound is292678.1269510926, wholly vacuous.
