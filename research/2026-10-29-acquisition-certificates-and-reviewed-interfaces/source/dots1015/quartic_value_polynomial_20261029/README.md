# Exact normalized-value polynomial from a cached critical shape
2026-10-29. Completed one-instance algebraic execution; independent review requested.

## Result

For the retained rational perturbation G of the non-SOS Choi–Lam quartic, this package computes the degree40 polynomial of NORMALIZED stationary values, proves its identity exactly, isolates its real values, and combines the least value with a fresh ordinary feasible candidate. The original objective receives

- exact upper0 at rational unit quaternion(1,0,0,0), found by the ordinary candidate routine with20 random plus four coordinate starts;
- exact lower −200928513451/16884590606400000;
- gap1.1900111654163489e−5 < requested1e−4.

`GLOBAL_VALUE_CERTIFICATE.json` binds the decisive files. The known independent nonnegativity of the original Choi–Lam quartic is not used as a solver lower-bound shortcut. The upper is merely exact evaluation of a feasible point.

## Acquired prerequisites and no hidden recomputation

The earlier accepted critical shape is A=Q[z]/(U), degree U40, squarefree, with x=P(z), y=Q(z). Its exact source files and boundary charts are copied unchanged under `received/`. All projective stationary rays with q0=0 have been excluded. The separately accepted modular witness proves the norm N=1+P²+Q²+z² is invertible in A and the normalized value

v=(∂0G)(1,P,Q,z)/(4N)

is primitive:1,v,...,v39 span A. The common factor1/4 is essential: this is the objective value on the unit sphere, not the unnormalized gradient eigenvalue.

Earlier proof dependencies: `cholam_algebraic_instance_audit_20261029/REVIEW_RECEIPT.json` and `fixed_direction_quartic_audit_20261029/REVIEW_RECEIPT.json`. They are relied on at their accepted scope; this packet does not silently redo the250.3-second shape/Groebner computation.

## Modular discovery, then two exact verifications

`modular_value.py` reduces the actual shape and derivative modulo successive admissible primes. It checks structural denominators, inverts N modulo U, forms v, and solves the40×40 Krylov relation for its monic degree40 polynomial. Full rank supplies the primitive modular relation, not a numerically fitted spectrum. CRT plus rational reconstruction proposed the candidate after208 primes (6219-bit product), in18.77 seconds on this execution. A fresh-prime agreement was only a discovery check, NOT proof.

The candidate primitive integer polynomial has maximum coefficient height3063 bits. By comparison the cached coordinate polynomials have approximately27,670-bit coefficients (U itself is only864 bits). This explains why direct value isolation can be easier than evaluating giant coordinate polynomials at very narrow z intervals.

### Primary executed proof: exact quotient remainder

`exact_common_denominator.cpp` uses GMP integers with one common denominator per polynomial. It computes num=∂0G(1,P,Q,z) and den=4N in the quotient, then evaluates

Σ_{i=0}^{40} c_i num^i den^(40−i) mod U.

The result is EXACTLY zero in18.85 seconds. Because den is invertible, this is exactly p(v)=0 in Q[z]/U. Degree40 and the primitive witness imply p is the complete characteristic/minimal polynomial, up to its declared scalar normalization. No rational-reconstruction probability remains in this proof.

The reduction algorithm is elementary: if a high coefficient a occurs at degree k≥40 and U has leading coefficient b, let g=gcd(a,b), multiply the remaining polynomial and its denominator by b/g, and subtract(a/g)z^(k−40)U. This preserves its quotient element and cancels the high coefficient. Polynomial-wide content normalization avoids repeated expensive coefficientwise rational gcds. Addition and multiplication are exact common-denominator arithmetic. The verifier checks the final zero remainder, not approximate eigenvalues.

### Independent deterministic modular proof

The separately derived `VALUE_POLYNOMIAL_HEIGHT_BOUND.md` constructs the integer220×220 degree9 monomial matrix of D(∂iG/4−lambda q_i Q). At each stationary eigenray its nonzero degree9 monomial-evaluation vector is in the matrix kernel, so the true value polynomial divides its determinant. The full determinant atlambda0 is333279776 modulo1000000007, certifying that determinant is not identically zero. Thus no specialized resultant-quotient division is needed.

Exact row norm bounds on the complex unit lambda-circle, Hadamard, Gauss's lemma and multiplicativity of Mahler measure bound every coefficient of the unknown primitive degree40 value polynomial by an explicit6613-bit integer H. This bound is proved independently of the proposed polynomial. Candidate coefficients also satisfy it. `verify_height_modular.py` checks443 good primes, with13245-bit product M>2H², all modular Krylov ranks40 and all modular p(v) identities. Cross-multiplied rational coefficient differences have magnitude≤2H² and are divisible by M, so they are exactly zero. This is deterministic exact verification, not random-prime confidence. Final verification replay took14.12 seconds; earlier recorded replay took20.82 seconds. The source height-bound script also executes its determinant witnesses. All timings are observations, not resource guarantees.

## Why the smallest real root is a genuine global lower bound

The accepted reduced critical algebra has40 complex points. Primitive v means its values on those points are all distinct. A real value therefore has exactly one critical point above it; complex conjugation preserves both the equations and that value, so uniqueness forces its q0=1 coordinates to be real. Nonisotropy then gives positive normalization N. Conversely every real sphere stationary point is covered and has normalized objective value v by Euler's identity. Thus the LEAST REAL root is the sphere minimum of G. This argument cannot be replaced by the false general assertion that a real stationary value always comes from a real stationary point.

`isolate_and_candidate.py` performs exact rational interval isolation of all28 real roots of the degree40 value polynomial in0.628 seconds; it does NOT refine or evaluate all28 old z-coordinate roots. It then runs the ordinary candidate routine on the ORIGINAL objective and evaluates its rational unit candidate exactly (0.098 seconds). Subtracting the exact coefficient-l1 perturbation budget19/1600000 from the least value's lower endpoint transfers a global lower bound to the original objective. The final gap is checked exactly.

This is a fast certificate path when an ordinary feasible candidate meets the resulting global bound. It does not guarantee that a local search will always supply such a candidate, and it does not implement the general value-to-coordinate extractor. The previously accepted complete grid fallback remains available at its actual cost.

## Failed execution routes and paid costs

Both coefficientwise GMP rational approaches were attempted with explicit240-second caps. The first used a rational extended-Euclid inverse of N; it progressed through the inverse but did not finish the later identity. The second used the homogeneous identity but retained coefficientwise rational arithmetic; it only reached Horner degree36 before its240-second cap. Their source/logs are preserved, and neither is reported as completed verification. The common-denominator successor completed under its90-second cap with exit0.

Direct normalized4/5-variable Groebner experiments belong to the sibling author and were stopped without a basis after about7 minutes; they are not silently counted as successes here. The successful warm-shape route's discovery plus direct verification plus root/candidate stages total roughly38 seconds of measured program stages, in addition to already-paid shape computation. The independent height proof/replay is additional audit work. Repeated failed exploration and tool/host contention are not zero-cost. This is not a cold-start38-second universal optimizer or a practical padded online controller.

## Reproduce

Python/SymPy/NumPy/SciPy and C++17 with GMP are used. From this folder:

1. `python modular_value.py` (bounded512-prime candidate search).
2. `g++ -O3 -std=c++17 exact_common_denominator.cpp -lgmpxx -lgmp -o exact_common_denominator`.
3. `./exact_common_denominator quotient_input.txt candidate_value_polynomial.txt exact_common_denominator_verification.json`.
4. `python certify_value_polynomial_height.py`, then `python verify_height_modular.py` for the independent exact proof.
5. `python isolate_and_candidate.py`, then `python assemble_certificate.py`.

The candidate and root-stage files deliberately retain their original provisional labels; the assembled certificate and exact verifier outputs establish completion. Original Astra source files are unchanged. Known modular reconstruction, common-denominator arithmetic, elimination, Mahler bounds and univariate root isolation are not claimed as new mathematical inventions. The constructive gain is an executed exact value interface for this retained non-SOS oracle instance.
