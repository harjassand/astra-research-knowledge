# Restricted global sunflower constructions

10 October 2026. No general sunflower theorem or historic breakthrough is claimed.

Start with additive_projection_gate_20261010/RESULT.md under independent_programme. It proves that a sunflower-free binary additive block code with w coordinates has dimension at most 2w-1, using Brouwer's 1986 binary cover theorem. Output block ranks are unrestricted. The exact sampler costs 5^w times a polynomial in explicit input size. Its finite checks, exact proof and source distinctions are included. Novelty has not been independently established.

The root_additive_sunflower_20261010 folder is the earlier restricted rank-at-most-two construction, with a polynomial-time finite-field sampler. Its historical statement that a general-rank bound was not then established is superseded by the new additive_projection_gate proof, not silently edited.

The global_sunflower_20261010 folder develops exact supplied latent-product and mixed-alphabet couplings, and proves limitations on acquiring those representations for arbitrary families. The general-family problem remains unresolved. Entropy optimization alone is equivalent to the original combinatorial bound via a known 2009 theorem; it is not a solution.

All code, assumptions, counterexamples, failed searches, primary-source links, and verification results are preserved. Floating-point MILP timeouts do not certify a lower bound. The withdrawn 2022 coset-cover paper is explicitly excluded from the proof dependencies.

Run the indicated Python scripts to reproduce exact checks. No external certification or priority claim is made.
