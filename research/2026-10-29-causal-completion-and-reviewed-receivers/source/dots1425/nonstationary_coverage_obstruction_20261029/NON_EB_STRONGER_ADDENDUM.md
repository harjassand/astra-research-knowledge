# No CPTP EB minorization even at a faithful fixed state
2026-10-29. Additive stronger obstruction; not an information-loss counterexample.

Let AD have damping γ=1/2 and Kraus operators A0=diag(1,1/√2), A1=|0><1|/√2. Define Φ=Ad_X∘AD. Its Bloch action is (x,y,z)↦(x/√2,−y/√2,−z/2−1/2). Thus its unique fixed state is σ=diag(1/3,2/3), strictly positive.

AD has a full-domain symmetric extension given by the isometry |0>↦|00>, |1>↦(|10>+|01>)/√2. Apply X to both outputs to obtain a symmetric extension of Φ. Thus Φ is self-compatible.

In reference-output ordering, its normalized Choi support is
S=span{|01>+|10>/√2, |11>}.
A vector a(|01>+|10>/√2)+b|11> has coefficient matrix [[0,a],[a/√2,b]], whose determinant is −a²/√2. Consequently the only product ray in S is |11>.

Suppose Φ≥αE in CP order for α>0 and E a CPTP entanglement-breaking channel. Positivity forces supp J(E)⊆S. A separable positive operator supported in S is a sum of product projectors in S, so must be proportional to |11><11|. Its reference marginal has rank1 and cannot equal I/2, a contradiction. Therefore Φ admits NO positive-weight CPTP EB component. The same reasoning proves Φ is non-EB.

In particular Φ−αΦΔσ is never CP. Explicitly w=(|01>−√2|10>)/√3 satisfies <w|JΦ|w>=0 but <w|J(ΦΔσ)|w>=1/3.

This blocks a broader generic-mixture strategy than the first example: neither faithful stationarity nor self-compatibility guarantees any EB CP minorization. It does not exclude an entropy comparator, a prior-adapted measurement/repreparation channel, or an actual-prior bound. It is not a novelty claim.
