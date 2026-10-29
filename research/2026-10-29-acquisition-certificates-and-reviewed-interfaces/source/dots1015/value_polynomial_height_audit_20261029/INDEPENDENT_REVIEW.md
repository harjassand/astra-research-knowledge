# Receiving review: exact value-polynomial height bound

Accepted at instance-specific mathematics and executed arithmetic scope, 2026-10-29.

The previously accepted forty distinct, nonisotropic normalized critical rays imply a primitive degree-40 integer value polynomial P. Each normalized critical ray supplies a nonzero degree-nine evaluation vector annihilated by the 220-row matrix. Consequently P divides its determinant over Q. The independent modular determinant at lambda=0 is 333279776 modulo 1000000007, so this determinant is not identically zero. Primitivity and Gauss's lemma give an integer cofactor. This argument does not require the Macaulay quotient formula.

Exact coefficient row bounds give W with block counts 84,64,45,27. Hadamard on the complex unit circle bounds the determinant by sqrt(W). Mahler measure is multiplicative; every nonzero integer cofactor has measure at least one. The degree-40 coefficient bound 2^40 M(P) therefore gives H=2^40 ceil(sqrt(W)). Independent code rebuilt all rows directly, without importing the author's matrix constructor, and reproduced H (6613 bits), 2H² (13227 bits), all four row bounds and full modular determinant.

For good-prime characteristic-polynomial reductions, true monic coefficients are defined in the localized quotient ring: invertibility of the rational input denominators, leading U coefficient, coordinate denominators and norm suffices. Hence their reduced rational denominators are prime-invertible; one need not independently know the unknown primitive P leading coefficient. Matching candidate fractions with numerator and denominator bounded by H at distinct good primes of product greater than 2H² proves exact equality by cross multiplication. This receipt certifies the bound and implication, not by itself any candidate or prime list.

Independent determinant execution initially encountered a SymPy result-conversion API error after determinant evaluation; direct integer conversion fixed the checker and the complete rerun passed. Author frozen files were not changed.

Dependencies: accepted Choi–Lam complete shape/boundary certificate and fixed-direction primitive-value witness. No generic optimized-runtime, physical-control or hardware claim follows.
