# Completed review of the balanced finite-sector construction

Root read the complete worker `PROOFS.txt`, `RESULT.txt`, all312 lines of
`code/canonical_bafqmc.py`, and the four main-run result records. The finite
sector construction is accepted at its stated mathematical/implementation scope.
This supersedes earlier statements that root had reviewed only the pole proof.
It does not confer historical priority, physical prediction or practical gain.

Reviewed proof hash:8f32fd2875c6060a224b86ae09d5ba5c111afe6a16ed6f2a97c66281f62ed355.
Reviewed core hash:b3c4791dd001b6793ee277776503b1e509ab1a8a109e6e426fca178debc06108.
Main output hash:e10b05dfa0873bcf6d9ead73c7c508622223b78365549039c2cdc9cf88374bbb.

The accepted contract has separately conserved equal populations, conjugate
flavor hopping, U1>=0,U2<=0,no pairing,finite sites/populations/slice count.
The positive Gaussian HS identity and finite symmetric-power traces give
|h_n(B)|²; finite-sector Trotter convergence is valid. The ordinary Newton
recursion does not require diagonalizable B. Code propagates its matrix
derivative, includes the exactly integrated uniform-mode scalar and its energy
derivative, and uses the same symmetric splitting as the full-Fock reference.
The Gaussian projection subtracting each spatial mean has the correct residual
covariance. The raw/centered second-moment factor and finite second moment of
the first thermal derivative follow at this finite scope. They imply no
uniformly efficient acquisition or higher-observable variance bound.

Root independently built the100-state triangle Hamiltonian in an occupation
basis without importing worker code. `independent_thermodynamics.py` and
`INDEPENDENT_REFERENCE.json` give Z=1627.6482978498273 and
E=-4.929359367166155 for n_b=n_c=3,beta=t=U1=1,U2=-.05, agreeing with the
worker reference. Root execution about .0037s excluding runtime import.

The worker actually executed four1,048,576-field integrations. Recorded main
energy/partition deviations from exact finite-step references are within2.19
estimated SE. Root inspected those records and derivative/recursion controls;
it did not independently rerun the four-million-field calculation. These
ordinary floating Monte Carlo checks are accepted as such, not as rigorous
continuum sampling confidence intervals. Finite-step bias is separately known
on the100-state fixture; e.g L80 energy bias is about-8.529e-4.

The source-lattice nine-site stress is a separate diagnostic whose code was
not whole-reviewed here. Its physical accuracy remains UNKNOWN. Its reported
weight concentration is a cost warning, not a reliable large-system prediction.
The source's stable U2=0 claims remain outside the attractive GC obstruction.

The small ED comparator is both faster and more precise than this stochastic
implementation. Canonical recursion, Gaussian subtraction and conjugate-sector
positivity are ordinary ingredients. No new efficient simulation class or
civilisation-level capability follows. The meaningful accepted progress is a
precise failed ensemble interface and an implemented well-defined replacement.
