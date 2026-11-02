# Finite interface test correction

The first execution of root_filtered_parent_test.py failed its normalization assertion because the implementation used Tr(G_a)/(2Z) as the sector probability. Since Z is the full partition function, the correct sector probability is Tr(G_a)/Z. The erroneous sum was one half. This factor was corrected before reporting numerical results; no theorem uses the erroneous normalization.

The corrected standard-five-qubit interface test passes. It is not the actual recursive-family gap proof and does not certify the asymptotic algorithm.
