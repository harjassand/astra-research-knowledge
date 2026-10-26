## ASTRA Pro3 — New capability: learning hidden physics by changing the experiment

The strongest result in this continuation is a method for making previously unobservable physical responses measurable through a restricted experimental interface.

### 1. Exact reuse after eliminating hidden components

Suppose retained observations establish the entire admissible family of positive-definite response operators,

\\[ S_L\preceq S\preceq S_U. \\]

If a later experiment exposes only selected boundary ports, eliminating the hidden internal coordinates produces another exact operator interval, not merely conservative bounds.

\\[ \boxed{ \\{(PS^{-1}P^\top)^{-1}:S_L\preceq S\preceq S_U\\} = [R_L,R_U]. } \\]

I proved constructive surjectivity: every reduced response in the interval can be realized by an admissible full source. The proof supplies a rational source-reconstruction procedure.

This builds on classical Schur-complement and shorted-operator mathematics.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://epubs.siam.org\&sz=32)

epubs.siam.org

+1



In an executed four-port control, one historical experiment left a rank-two uncertain response. A later two-port boundary experiment reduced that uncertainty to rank one.

Two previously unspecified feedback controllers could then be evaluated jointly. Preserving their common source produced an exact uncertainty interval 8.11× narrower than independently combining their response ranges.

### 2. Stronger advance: creating an informative experiment

The next construction uses a single accessible experimental port. Without modification, its output is completely insensitive to an unknown internal \\(r\times r\\) response matrix \\(T\\).

The learner can instead configure a known positive rank-one coupling:

\\[ J_v=\lambda(e_0-v)(e_0-v)^\top. \\]

The new scalar boundary reading becomes

\\[ \boxed{ R_v=R_0+\frac{\lambda}{1+\lambda v^\top T^{-1}v}. } \\]

Consequently, one scalar experiment reveals one quadratic form of the hidden inverse response. By choosing standard basis vectors and their pairwise sums, the learner reconstructs the entire hidden matrix.

I proved that \\(r(r+1)/2\\) scalar readings are both sufficient and necessary for universal exact recovery under this instrument contract, even against adaptive deterministic alternatives.

| Hidden response dimension | Scalar experiments | Recovery |
| ------------------------- | ------------------ | -------- |
| 2                         | 3                  | Exact    |
| 3                         | 6                  | Exact    |
| 5                         | 15                 | Exact    |

All three constructions were executed with rational arithmetic. The recovered matrices matched the independent hidden-source checks. Each then answered a later skew-coupled equilibrium question without further source calls.

The important change is procedural: the agent identifies how to modify an experiment so that a hidden physical quantity becomes observable.

### 3. Information and precision limits

The research also established three boundaries.

First, for the two-port hidden source, two configured scalar experiments remain insufficient. Two distinct admissible sources produce identical readings; the third experiment separates them.

Second, bounded instrument error cannot be ignored. With errors at most \\(10^{-3}\\) in the three scalar readings, the implemented reconstruction produced a certified hidden-response operator-error bound of approximately 0.05607. That is sound but not claimed minimax-optimal.

Third, three readings can each satisfy the spectral contract individually yet be jointly impossible. The compiler constructed such a record and rejected it using an exact negative determinant certificate.

These are substantive safeguards against inventing physical mechanisms from incompatible observations.

### Preserved research

Complete mathematical research note

Exact transfer and query-minimality proofs, source-realizing constructions, hardware-interface derivation, noisy recovery and counterexamples.

Reproducible research archive

Three research programmes, actual results, independent verifier, clean replay, proofs and SHA-256 manifest.

All four executable suites passed an isolated, byte-identical replay. Independent exact-arithmetic verification checked 24 configured scalar experiments and 15 full-source witness reconstructions.

Scientific assessment: The principal improvement is moving beyond a passive learner that only interprets observations toward an experimental compiler that can design a more informative observation interface.

The major unresolved question is whether those reconfigurable couplings can be implemented in a real system at worthwhile cost, while preserving the assumed source law. The results do not yet demonstrate a physical discovery or an advantage over an equally informed system-identification method.

The strongest next research direction is jointly selecting experimental hardware configurations, measurements and subsequent scientific operations under realistic sensor noise and intervention constraints.