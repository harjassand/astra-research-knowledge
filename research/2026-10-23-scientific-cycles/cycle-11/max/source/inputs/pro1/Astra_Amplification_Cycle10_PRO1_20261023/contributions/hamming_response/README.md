# Cycle10 all-distance response contribution

The complete proof is `FULL_HAMMING_RESPONSE.tex`. It extends the actual
Cycle8 paired-history mechanism to every even Hamming-distance sector and
then proves a full bath-operator estimate in a weighted input norm.

For the actual sigma, any Hermitian charge-preserving Y, A=Q-k/2, a=1-b,
and r=bk, on initial bath depths at least k:

    ||D_b(sigma Y) - 2a Tr(sigma A Y) I||
      <= r exp(2r^2) ||Y-P(Y)||_(2,sigma).

Here P pinches complete binary input charge patterns. The result is uniform
over every coherent/entangled bath prefix. The exact diagonal response is
P(G)=a(2Q-k) tensor I. For r<=1/2 the norm coefficient is at most 2r.

## Load-bearing proof steps

1. Equal output charges pair identical spectator stay choices and complementary
   endpoint choices at an input Hamming difference of 2m.
2. Unitarity cancels the entire spectator output-charge contribution, leaving
   norm at most c_m=m binom(2m,m) after extracting (b(1-b))^m.
3. A fixed charge row of weight q has binom(q,m)binom(k-q,m) such columns.
   Complete-pattern pinching of the square is a sum of positive block squares.
4. Its operator bound is r^2 sum_j(4r^2)^j/(j!)^2 <= r^2 exp(4r^2).
5. A completely positive weighted input partial trace and operator
   Cauchy--Schwarz give the bound without choosing a prefix expectation.

The diagonal charge term and deep-bulk restriction are essential. Actual
within-model counterexamples are included in the proof. The interface by
itself does not establish input positivity, entropy gain, or a coded rate.
Its intended receiving use is the owner's normalized positive Gram input.

## Distinct bounded diagnostic

`physical_hamming_check.py` evaluates the actual coherent device
(6 U+i I)/sqrt(37). It checks the new diagonal and Hamming block formulas
on k=2,3 full input/prefix spaces, and one k=4 four-endpoint block family.
Gaussian-integer path numerators make the isometry and diagonal tests exact
in these bounded integer ranges; eigenvalue/norm checks are numerical.

Run from any directory with NumPy installed:

    OPENBLAS_NUM_THREADS=1 python physical_hamming_check.py

The saved `physical_hamming_check.json` records all inputs, exact identities,
norm observations, wall time 0.075077694 seconds and peak RSS 28,952 KiB.
These are diagnostic execution costs. Discovery, inference, and proof/review
costs were not instrumented. Finite checks do not prove the all-length theorem.

The owner and independent operator challenger independently obtained the
normalization/row mechanism. This contribution does not assert a causal
advantage from the number of agents or historical originality.
