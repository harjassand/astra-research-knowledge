# Receiving review: exact normalized-value polynomial, perturbed Choi–Lam instance

2026-10-29. Accepted at the exact-instance scope described below, subject to hash-bound governing receipt.

## Two exact identities

The accepted source shape represents a reduced 40-point quotient algebra with no omitted critical rays, invertible norm, and 40 distinct normalized objective values. The copied input, shape, boundary and modular primitive-element witness were checked byte-for-byte against those accepted sources. The author's modular preparation was replayed in a separate directory and regenerated identical quotient input.

The new candidate is a degree-40 rational monic polynomial. Two independent certification routes were inspected and replayed:

1. The GMP checker represents quotient polynomials as integer coefficient vectors divided by one common denominator. Each reduction step multiplies the vector and denominator by the same factor and subtracts an exact multiple of U. Addition, multiplication and content normalization preserve rational quotient values. Homogeneous Horner evaluates sum c_i num^i (4 norm)^(40-i), and returns exactly zero modulo U. Invertibility of norm, inherited from the accepted independent modular witness, proves p(lambda)=0 over Q. Degree 40 and 40 distinct values identify the full polynomial, rather than a partial factor. Independent compiled replay completed in 14.8427 seconds on this runtime.

2. The separately received exact Hadamard/Mahler height bound gives H (6613 bits) for the actual primitive integer polynomial. The independently replayed modular checker proves full Krylov rank and polynomial identity at 443 distinct good primes. Their product has 13245 bits and exceeds 2H² (13227 bits). Candidate coefficients meet the same bound. The denominator/localized-algebra conditions ensure actual characteristic coefficients reduce correctly. Cross multiplication then proves exact rational equality, not a probabilistic CRT confidence statement. Replay completed in 14.41 seconds.

The scalar 220-row determinant and bound were independently rebuilt without the author's Macaulay constructor in the separate height audit. The direct GMP route does not depend on that height argument; the two certificates are complementary.

## Exact global interpretation and candidate

Independent exact univariate isolation gives 28 simple real roots and reproduces every stored interval. Uniqueness of the critical ray per normalized value implies real values have real chart representatives by conjugation. Thus the smallest real value is the sphere minimum of the perturbed quartic. Subtracting the exact coefficient-l1 perturbation budget gives a valid lower bound for the original quartic.

The stored candidate quaternion has norm exactly one and evaluates in the ORIGINAL quartic to exactly zero. The exact original lower bound is -200928513451/16884590606400000, so the certified gap is 1.1900111654163489e-5, below 1e-4. Independent evaluation and all interval checks passed. The known AM-GM original minimum zero is a sanity check, not needed for the reported lower-bound computation.

## Scope and cost limits

This closes one concrete normalized-value polynomial and global objective certificate using accepted shape data. It is not a new from-scratch all-input solver: initial shape acquisition, boundary coverage and primitive-value proofs remain dependencies. Generic fixed-template complexity is a separately reviewed theorem, not supplied by this execution. The per-coefficient rational attempts timed out and must remain visible; no claim combines best separate component timings into an unexecuted end-to-end benchmark. A tighter gap than the earlier ray-coordinate certificate is consistent with finer objective-root isolation, not correction of an invalid earlier bound.

No hardware, universal calibration, unknown-noise practical advantage or clock-private online implementation is established. The ordinary optimizer supplies the candidate; exact algebra certifies its global objective quality.
