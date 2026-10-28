# Comparison with current verified spectral learning

28 October 2026. Scoped comparison of the accepted construction in
`ABSORBING_BOUNDARY_THEORY.md` with Colbrook, Mezić and Stepanenko (CMS),
*Adversarial dynamical systems characterize when data-driven learning succeeds
or fails*, Nature Communications **17**, 5397 (14 July 2026),
[DOI: 10.1038/s41467-026-74220-8](https://doi.org/10.1038/s41467-026-74220-8).
No local proof or accepted Astra undecidability result is re-audited here.

## Scientific conclusion

CMS is a substantive antecedent for verified infinite-dimensional operator
learning. This check does not identify a result that supplies the boundary
acquisition theorem, nor a contradiction that invalidates its stated scope.
It does rule out a broad novelty claim based merely on finite observations,
residual certification, infinite dimension, or absence of a strict global
spectral gap. The defensible candidate contribution remains the particular
finite observation-to-local-form-to-switched-output contract. This comparison
does not establish historical priority.

## Strongest constructive comparator and its actual inputs

The relevant comparator is Supplementary Algorithm S1, including its known
resolvent-bound extension. Its formal setting uses a continuous nonsingular
map on a compact metric space, a finite Borel measure, and a bounded Koopman
operator. Inputs include full-state evaluations on a dense set at requested
accuracy, an expanding dictionary, a known continuity modulus, and a known
function converting minimum residual into spectral distance. Controlled
correlations of observables and their evolved values supply a residual pencil;
local minimization produces spectral candidates and certified distance bounds.
Measure preservation supplies the identity conversion function; suitable
dissipative systems are also allowed. Completeness is asymptotic. The
one-sided finite certificates do not certify complete spectral coverage at
a prescribed finite accuracy. These distinctions follow from Supplementary
Definitions 1.7 and 1.11, §1.3, Theorem 2.3, Definition 3.1 and Algorithm S1.
[Accepted-version supplement](https://arxiv.org/html/2407.06312v2).

The main text expressly assumes full-state observations and leaves partial
observations as further work. Its approximate-eigenfunction coherence statement
has error proportional to time times residual for one map. Norm-one isometries
and continuous spectra already occur in its successful regime.
[Author manuscript, Eq. (5), constructive results and Discussion](https://www.damtp.cam.ac.uk/user/mjc249/pdfs/ML_for_systems_foundations_FINAL.pdf).

## Where the boundary result differs

The boundary learner receives a finite list of exact preparable states and
categorical first-return, live-censor and absorption records. Hidden state
identities, a full hidden-state dictionary and arbitrary hidden-state queries
are unavailable. Its source is a family of symmetric substochastic transition
kernels; a deterministic composition operator is a different operator model.
Replacing one by the other requires an explicit observation-preserving
reduction. Merely representing a stochastic process on an enlarged path space
does not grant the learner access to those extra coordinates.

Selfadjointness makes residual-to-spectrum conversion straightforward at the
operator-theoretic level. It does not manufacture the missing hidden-state
evaluations or a complete observable dictionary. Conversely, the boundary
construction does not learn a global spectrum. It can tolerate infinitely
many slow modes because the acquired quantity weights their effect on the
selected boundary representation:

\[
Q_i=D_i^*(I-A_i^2)^{-1}D_i.
\]

The acquisition then transfers this form to estimated maps and certifies a
single error bound simultaneously for every finite fixed switched word.
Words may be chosen after inspecting the acquisition. Policies reacting to
intermediate outcomes during execution remain outside this guarantee.
See `ABSORBING_BOUNDARY_THEORY.md`, “Finite censored observations supply the
bounds” and “Estimated maps and all future words.”

These are analytical comparisons of the declared contracts. CMS does not
provide this categorical acquisition or switched-word theorem; that statement
does not imply that spectral methods could never be combined with additional
arguments to serve the same task. Existing methods supplied with the acquired
forms are entitled to use them. The local positive Galerkin comparator already
illustrates this principle.

## Claims that the comparison does and does not support

- **Supported:** a finite physical observation scheme can acquire useful local
  inverse-dissipation forms without reconstructing the hidden source, under
  the exact-boundary, symmetry and irreversible-loss premises.
- **Unsupported:** that prior verified learning inherently needs finite hidden
  rank, a strict norm gap, or an already identified finite model; that this
  construction supersedes current spectral learning; or that it gives a
  universal sample or runtime advantage.
- **Essential qualification:** arbitrary hidden dimension describes the
  admissible source class. It does not promise that every source emits a useful
  certificate in finite affordable time. Positive observable margins and useful
  residual bounds must actually be obtained.
- **No impossibility escape:** a conditional finite boundary-output certificate
  is not an algorithm for deciding global spectral type or identifying arbitrary
  hidden dynamics. Changing both the objective and interface does not improve
  a lower bound for a different problem.

The fatal mismatch would be to sell the boundary result as a general solution
of CMS's spectral-learning problem, or to invoke CMS's limitations against this
narrower conditional boundary task without a reduction. Neither inference is
justified. The scientific opening survives at its declared scope; construction
of the physical interface on broader sources remains unresolved.

## Source and access record

- [Published primary record and metadata](https://pubmed.ncbi.nlm.nih.gov/42448691/).
- [Published full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13369498/).
  Initial indexed text was available; subsequent direct retrieval returned a
  browser/reCAPTCHA page. Nature's direct page redirected to an inaccessible
  identity service.
- [arXiv v2, 23 June 2026](https://arxiv.org/html/2407.06312v2) supplied the
  complete readable accepted version and supplement. Its supplement calls the
  main constructive theorem **2.3**. The supplied author PDF uses an earlier
  title and refers to that theorem as **2.1**; section numbers above follow v2.
  The supplementary input list and error-control definitions were read, so
  the access failures did not leave the central comparison dependent on an
  abstract or secondary account.
