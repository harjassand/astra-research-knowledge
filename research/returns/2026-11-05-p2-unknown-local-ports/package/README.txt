RARE FAILURE THROUGH PREPARED LOCAL COLLISIONS
Research package, 5 November 2026

Start with rare_failure_research.pdf.

The completed mathematical construction permits initially unknown correlated
transitions inside declared bounded-size reciprocal ports of a product-invariant
register. Prepared local inputs and one actual collision per trial give absolute
rate intervals, including observed-zero channels. Local error generators and
product variance tensorization turn these into a global Dirichlet-form bound.
A fixed-start resolvent estimate and an extension of the supplied P2 algorithm
give full mean-first-failure inference with explicit costs and starting-mass
dependence. The physical realization is a clocked register: failure is defined at
classical registered endpoints, not during an unobserved coherent pulse.

STATUS
- Complete in-session mathematical construction and proof-level supplements.
- Independently developed and checked arguments by three collaborators.
- Synthetic numerical evidence only; no physical measurements.
- Historical novelty, a practical device advantage, and a civilization-changing
  physical capability are not established.
- The generic Karger all-terminal FPRAS is invoked as published machinery, not
  implemented by this package.

FILES
rare_failure_research.pdf / .tex : Main research note.
theory_supplement.txt           : Full computational and perturbation proofs.
physical_supplement.txt         : Collision, acquisition, clock and factory proofs.
equilibrium_start_corollary.txt : Prepared safe initial law and initial-write errors.
rare_failure_experiment.py      : Main unknown-local-support synthetic experiment.
results.json                   : Counts, intervals, parameters and diagnostics.
intervention_results.pdf / .png : Scientific comparison figure.
physical_collision_example.py  : Smaller one-exchange-family reverse experiment.
p2_governing.tex                : Supplied fixed-revision P2 governing source.
sources.json                   : Exact source ledger and roles.
SHA256SUMS.txt                  : Byte hashes of the delivered package members.

REPRODUCE
python3 rare_failure_experiment.py

Dependencies: Python 3, NumPy, SciPy, Matplotlib.
The main code uses Python Decimal at 90 and 125 decimal digits; mpmath is not
required. It regenerates results.json and the figure. The main source's general
condition bound is 4/(sqrt(g)*kappa); both executed examples use the sharper rare
bound 2/sqrt(kappa).

The 4,000,000 and 256,000,000 collision counts are represented sample sizes.
Counts are generated directly by NumPy's multinomial sampler, not by simulating
that many physical collisions. Seeds are 20261105 and 20261106. Confidence is
99% separately for each example under ideal independent sampling, and at least
98% jointly. Numerical rounding safeguards and high-precision agreement are
diagnostics, not machine-checked directed-arithmetic proofs.

MODEL TIME
Native refresh rates gamma_i=1 define the numerical time unit. The model's
astronomical mean values are not measured hardware lifetimes and have not been
assigned a real laboratory second. For physical fixed cycles of duration T and
selection weights nu_j/Lambda, M_lab=T*Lambda*M_Q. The fixed-clock construction
also lets Q=(P-I)/T so its mean directly equals physical endpoint time.

KEY LIMITS
The product law, declared local reach, reciprocal operation, fresh ancillas and
native refresh backbone are part of the constructed class. Adding a backbone
only during testing does not justify the result. Local block size, inverse gap,
inverse starting-state mass, preparation effort and service time are paid.
Out-of-class baths, leakage, ageing, long-lived hidden memory, larger ports,
systematic readout errors and in-pulse failures are not excluded by silence.

The finite-factory extension requires stable basis states and independent,
nondemolition, nonbackacting verification with a known error floor below one
half, plus actual dephasing and protected idle storage. It controls ancillary
mispreparation within the given basis; it is not a general hardware error cure.

PROVENANCE
Astra governing revision:
5cfc803599d9f95cfa0a55896fb580e77567e162
research/returns/2026-11-05-p2-first-failure

Original research construction and numerical code produced in this session.
No repository was modified or external publication made.

