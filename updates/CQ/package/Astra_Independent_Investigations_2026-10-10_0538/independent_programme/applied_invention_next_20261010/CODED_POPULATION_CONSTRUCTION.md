# Coded-population generator tomography

Date: 2026-10-10. Status: **constructive mathematical candidate; no foundational novelty or physical feasibility claim**.

## Capability being attempted

Recover the directed transition rules of a population from destructive,
state-resolved endpoint measurements, while avoiding individual trajectory
tracking and explicit lineage reconstruction. Deliberately write known
overlapping state-dependent tags before evolution. Read only **bulk tag
marginals within each final state**.

The restricted readout matters. If the full joint code is readable on each
specimen, the code can identify its original state directly, reducing this
part of the proposal to ordinary prospective barcoding. Compressive marginal
readout is not a replacement for a capability already supplied by full
per-specimen origin labels.

Two positive constructions are established below:

1. An exact derivative decoder using a deterministic disjunct code and only
   minima, with no optimization routine.
2. An exact finite-interval identity using occupation-integrated counts and
   endpoints, followed by explicitly conditional sparse recovery. This
   removes the first construction's short-time Taylor bias under a
   time-homogeneous model; it does not make occupation measurements free.

The mechanism is closely related to known prospective/lineage barcoding,
compartmental system identification, group testing, compressed sensing, and
integral sparse identification. The broad architecture is not new. No
implementation or native-resource advantage over the closest established
methods has been demonstrated.

## 1. Native model and access assumptions

There are n declared states. Expected counts, or a deterministic mean-field
population, obey x'(t)=A x(t), where A is Metzler: A_ik >= 0 for i != k.
A_ik denotes transition influx into state i from state k. The diagonal
combines retention, departure, growth and death; it is unrestricted.

For the derivative identity A may depend on time and only its value at t=0
is identified. The finite-interval construction requires one common,
time-independent A throughout the interval.

Required experimental interface:

- A positive initial abundance vector p is known or independently measured.
- For each tag j, the known conditional initial tag fraction is W_ji in
  state i. Thus x_j(0)=diag(p) w_j.
- Tags persist and are inherited without tag-dependent effects on transition
  and growth. Each tagged subpopulation obeys the same A as the total.
- The declared state is sufficient for the mean dynamics. In particular,
  hidden subtypes with different growth or transition rates must not become
  differently represented across tags within one declared state. This
  homogeneity/lumpability assumption is stronger than barcode neutrality.
- All declared states can be classified at readout, with calibrated errors.
- Counts or fractions are measured without assuming individual lineage
  access. The state-dependent writer is a real required device, not an
  oracle whose cost is excluded.

The proposed mathematics does not construct such a writer for arbitrary
biological states. It does not establish that the required tags are neutral,
that measured cell types are Markov states, or that cloning supplies
independent samples.

## 2. Instantaneous cancellation and exact min decoder

Let f_ji(t)=x_ji(t)/x_0i(t), where x_0 is the untagged total. At t=0,

    f'_ji(0) = sum_(k != i) lambda_ik (W_jk - W_ji),
    lambda_ik = A_ik p_k / p_i.

Proof: apply the quotient rule to x'_j=A x_j and x'_0=A x_0.
The k=i term cancels. No assumption about equality of diagonal entries is
needed. The cancellation is instantaneous, not a statement that growth
ceases to influence later fractions.

Assume each row has at most s nonzero off-diagonal entries. A binary code W
is (s+1)-disjunct if, for any column k and any set of at most s+1 other
columns, a row has a one in k and zeros in that set. Then

    lambda_ik = min { f'_ji(0) : W_ji=0 and W_jk=1 }.

Proof: every eligible row sums nonnegative incoming rates and includes
lambda_ik. Disjunctness provides a row that excludes i and every other
actual predecessor. If k is not a predecessor, it provides a row excluding
i and all actual predecessors, producing zero. Both inequalities follow.

### A fully specified code

Choose a prime q and an integer d with n <= q^d and
q > (s+1)(d-1). Represent each state by a distinct polynomial P_i of degree
at most d-1 over F_q. Tags are pairs (a,b) in F_q^2; write

    W_(a,b),i = 1 exactly when P_i(a)=b.

Two different code columns overlap in at most d-1 rows. The union of s+1
forbidden columns can therefore cover at most (s+1)(d-1) of a candidate
column's q ones. At least one isolation row remains. There are q^2 binary
tags. This is a standard polynomial/disjunct-code construction, not a new
coding theorem. The underlying superimposed-code construction is credited
to Kautz and Singleton (1964), DOI 10.1109/TIT.1964.1053689.

The exact test uses n=128, s=2, q=7, d=3: 49 tags. The simple decoder checks
all n(n-1) candidates, costing O(n^2 q^2) comparisons and yielding an
s-sparse graph after zero entries are discarded. This is not a sublinear
graph-output algorithm.

### Noise and finite-time cost

If every measured derivative has additive error at most epsilon, each
decoded lambda has error at most epsilon: the minimum is 1-Lipschitz in
the sup norm. Conversion to A multiplies error by p_i/p_k, and errors in
p must be included separately.

The actual one-endpoint estimator is [f(h)-W]/h. If |f''(t)| <= M on [0,h]
and the measured fraction error is at most eta, its derivative error is at
most

    M h/2 + eta/h.

The optimal h for this bound is sqrt(2 eta/M), with error sqrt(2 M eta),
provided the chosen h lies inside the regularity window. Small h does not
give arbitrarily precise inference at fixed measurement noise.

For constant A, a sufficient, deliberately crude bound is
M=4 B^2 rho^2 exp(4 B H) on [0,H], with B=||A||_infinity and rho=max(p_i)/min(p_i). Indeed,
x_i >= p_min exp(-Bt), max(x_i) <= p_max exp(Bt), and the instantaneous
incoming-rate sum is at most B rho exp(2Bt). Differentiating the fraction
equation bounds its second derivative by four times the square of this
quantity. For time-dependent A, this bound additionally needs control of
its temporal variation; a bound on ||A(t)|| alone does not suffice.

Under an *additional* independent Bernoulli observation model with N
effective samples for each state, a union Hoeffding bound gives
eta=sqrt(log(2nm/delta)/(2N)). Thus the first-order derivative protocol's
error decreases only as N^(-1/4) after balancing bias and measurement noise.
This is a bound for that protocol, not an information-theoretic lower bound.

Total descendant cells are not automatically N independent samples.
Sampling cells from an actual realized population controls assay error
around that population's fraction, not intrinsic branching fluctuations
around the mean ODE. Independent founders/replicate populations or an
explicit branching covariance analysis are required for the latter. No
finite-population guarantee is supplied here.

## 3. Exact finite-interval construction

Fix T>0 and an optional known weighting lambda >= 0. Define

    U_j = integral_0^T exp(-lambda t) x_j(t) dt,
    H_j = exp(-lambda T) x_j(T) - x_j(0).

Integration by parts gives

    (A - lambda I) U_j = H_j.

Let F_ji=U_ji/U_0i and define, for k != i,

    Z_i[j,k] = U_jk - F_ji U_0k,
    D_i[j]   = H_ji - F_ji H_0i.

Then the exact finite-interval equation is

    Z_i a_i = D_i,   a_i[k] = A_ik for k != i.

Proof: subtract F_ji times the baseline equation's i-th coordinate from
the tag equation's i-th coordinate. The diagonal and lambda terms cancel.
The identity holds without an h->0 limit and without numerical
differentiation. It requires the occupation-integrated information U_j,
not merely two endpoint snapshots.

Occupation information can in principle be estimated from destructive
cohorts harvested across the interval, but deterministic quadrature has
discretization error and random-time harvest has sampling error. Either
requires reproducible initial populations and the same dynamics at each
harvest time. The costs, sampling weights and correlation model must be
specified in any physical implementation. Nothing here authorizes or
performs such an experiment.

### Sparse identifiability theorem

If every set of at most 2s columns of Z_i is linearly independent, there
is at most one s-sparse solution a_i. Indeed, the difference of two such
solutions is a null vector supported on at most 2s columns.

This gives a constructive decoder: enumerate supports of size <=s and
solve the corresponding linear systems, retaining nonnegative solutions.
Its cost is combinatorial in s. Generic identifiability is not an
efficient sparse-recovery theorem.

### Existence of low-channel designs

Write M=integral_0^T exp((A-lambda I)t)dt, u=M p and
R=diag(u)^(-1) M diag(p). R has row sums one. If M is invertible, so is R.
For distinct k != i, the vectors R_k-R_i are linearly independent: a
linear dependence would give a linear dependence among rows of R.

Consequently, with m>=2s tag vectors drawn independently from any
absolutely continuous distribution on (0,1)^n, every 2s-column minor
required above is nonzero almost surely. Each is a nonzero polynomial in
the tag entries; there are finitely many minors. This is an exact-real
existence/identifiability result, not a finite-precision stability bound.

One sufficient way to ensure M is invertible is lambda>||A|| for a known
induced-norm bound. Then every eigenvalue of A-lambda I has negative real
part, and (exp(zT)-1)/z is nonzero on that spectrum. Lambda is a mathematical
weight on observations, not a required biological removal mechanism.

Binary random masks can also preserve the relevant union of sparse
subspaces with O(s log(en/s)+log(n/delta)) channels by standard subgaussian
embedding results. They do not remove the conditioning of M, population
imbalance, or errors in the acquired design matrix. No new random-embedding
theorem is claimed or required by the exact test.

### Observable error certificate

Suppose U and H are measured with coordinatewise errors <=epsilon_U and
epsilon_H, U_0i>=u_*>epsilon_U, U_0k<=U_*, and |H_0i|<=H_*.
Because true tag fractions are between zero and one,

    delta_F = 2 epsilon_U/(u_* - epsilon_U),
    delta_Z = (2+delta_F) epsilon_U + delta_F U_*,
    delta_D = (2+delta_F) epsilon_H + delta_F H_*.

These bound errors in F, each Z entry, and each D entry respectively.
Assume a known nonnegative row-sum bound ||a_i||_1<=L. Set
e=delta_D+L delta_Z. If an s-sparse nonnegative candidate also has row sum
<=L and fits the measured equation to residual <=e in the sup norm,

    ||a_hat - a||_2 <= 2 sqrt(m) e / sigma_2s(Z_i),

where sigma_2s is the smallest singular value over submatrices with at
most 2s columns. This follows by bounding the exact residual of the
difference and applying the restricted singular-value inequality.
When that singular value is small, the certificate is correspondingly
weak. Checking it by enumeration is itself combinatorial. A noisy
version must additionally certify a lower bound from measured matrices.

## 4. Exact tests and scope

`verify_coded_population.py` performs rational-arithmetic tests:

- 128 states, arbitrary heterogeneous diagonal entries, at most two
  incoming edges per state, and the 49-tag polynomial code. It checks all
  16,256 off-diagonal decoded rates exactly and verifies the min decoder's
  sup-norm perturbation bound.
- An eight-state Metzler generator with distinct negative integer
  diagonals, two incoming edges per row, and four rational tags. At
  T=log(2), the matrix exponential and occupation integral are computed
  exactly by spectral polynomial interpolation. Every required
  four-column minor is tested; exhaustive support search recovers every
  row exactly.

These tests instantiate the proofs. They do not validate a barcode writer,
assay noise model, model homogeneity, scaling to real biological systems,
novelty, or civilization-scale consequence.

## 5. Prior-art and novelty boundary

- STAG (2021), *Modeling glioblastoma heterogeneity as a dynamic network of
  cell states*, already uses barcoded destructive single-cell snapshots
  to infer transition and growth networks. Its implemented biological
  architecture is much more established than the writer assumed here.
  https://doi.org/10.15252/msb.202010105
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8444284/
- Gunnarsson, Foo and Leder (2023), *Statistical inference of the rates of
  cell proliferation and phenotypic switching in cancer*, explicitly
  studies identifiability and uncertainty for switching/growth inference
  from counts and fractions. It is essential comparison for any statistical
  claim. https://arxiv.org/abs/2306.08096
- Chang, Gray and Tomlin (2014), *Exact reconstruction of gene regulatory
  networks using compressive sensing*, already derives sparse-network
  identification guarantees and discusses experimental coherence.
  https://doi.org/10.1186/s12859-014-0400-4
- Integral sparse identification is established; e.g. *Sparse dynamical
  system identification with simultaneous structural parameters and
  initial condition estimation* (2022), https://arxiv.org/abs/2204.10472.
  Replacing derivatives by integrated linear equations is not new.
- Full internal state recording is also an established experimental
  direction: *Molecular Time Capsules Enable Transcriptomic Recording in
  Living Cells* (2023), https://pmc.ncbi.nlm.nih.gov/articles/PMC10614764/,
  and *A genetically encoded device for transcriptome storage in mammalian
  cells* (2026), DOI 10.1126/science.adz9353. These defeat a broad claim that
  storing a past cellular state for later destructive readout is new.

The potentially specific combination is a designed sparse code, a
bulk-marginal reader, and a nuisance-canceling decoder with a native
acquisition advantage. That advantage is **not established** here. The
finite-time version transparently reduces to known sparse linear system
identification. It should not be presented as a new foundational capability
unless an actual read/write implementation and a meaningful resource
separation from established methods are supplied.
