# Authorized comparison with the independent root singleton proof

After the sparse oracle and screening identities were derived, root reported an independently obtained singleton water-filling and sorted-prefix certificate. The initial task prohibited peer outputs; root then explicitly authorized reading only `root/SINGLETON_SCHUR_CERTIFICATE.md`. That file was read and reconstructed. No other worker's output was read.

The singleton derivation agrees with the earlier local calculation. For an active singleton prefix with threshold k and scale tau, the full normalized residual on an active subset S is

```
prod_S eta * (1-|S|+k sum_S 1/eta).
```

Its derivative in any selected multiplier is nonpositive because every active multiplier is at least k. Thus fixed-cardinality minima use the largest multipliers, and maxima are at most k. Inactive-only labels are bounded by k, while adding inactive bits to an active label cannot increase the modulus. This establishes root's exact global infinity norm and its necessity/sufficiency criterion, including complex l1 perturbations through the tangent dual norm. Zero inactive multipliers do not invalidate the argument. A valid nonempty prefix and eta<1 imply k<1, which justifies k^ell<=k.

No mathematical issue was found in that note. Agreement by these same-session calculations is internal consistency, not independent external validation or evidence of novelty. The generic water-filling/KKT elements have direct predecessors; root is handling those sources.

The complementary work here is the full residual screen for arbitrary retained subcubes and the sparse-pattern oracle for arbitrary unequal multipliers, rather than a duplicate implementation of the singleton algorithm.
