# Accepted thermal-amplitude certificate and source-specific small-collar limit

Root has whole-read `../corpus_first/cold_interval_bridge/PROOF.md` and
reviewed the actual source operators, residual, transfer construction and
positive-arithmetic readout code. The general theorem, finite source
interface and its exact small-collar limitation are accepted at the stated
scope. No target Gibbs-purity input at the required bootstrap precision or
uniform spin-two gap is acquired. The separate coarse true-Gibbs corollary
below is accepted at its broader interval scope.

The material operation is an a posteriori relative thermal-amplitude
certificate. For A(0)=I, differentiable invertible A(s), and finite Hermitian
H, define E=(A'+HA/2)A^-1 and nu=integral||E||. Dyson expansion about −H/2
and Schatten Holder give

    ||A(beta)−exp(−beta H/2)||p
       ≤(exp(nu)−1)||exp(−beta H/2)||p      for EVERY p∈[1,infinity].

Root independently derived the proof: each Dyson term has positive heat
durations summing to beta. Give a duration t the Schatten exponent p beta/t.
The product of all heat norms is exactly the final thermal Schatten norm;
the bounded E factors use infinity norms. Integrating their scalar product
over the ordered simplex gives nu^k/k!, so summing the error terms proves
the formula. Zero durations follow by continuity; finite dimension and
an integrable residual ensure convergence. No extensive exp(beta||H||)
prefactor or comparison between different-temperature truncations is used.

Writing eta=exp(nu)−1<1, the same amplitude supplies both Schatten2 and4.
The triangle inequalities imply

    P_A=Tr[(AA*)²]/[Tr(AA*)]²,
    |log P_A−log T_H(beta)| ≤4 log[(1+eta)/(1−eta)],

where the numerator means Tr[(AA*)²], not [Tr(AA*)]². Equivalently, an
allowed log-purity error epsilon requires
nu≤log(1+tanh(epsilon/8)). Trace normalization and its costs are paid.
This implication does not acquire the required small residual.

For disjoint seam collars C_j=exp(−s L_j/2)exp(s K_j/2), and blocks of
length at least 2ell+2, root independently checked the logarithmic derivative
of A=(product C_j)exp(−s H0/2). All inside-collar terms cancel, leaving
exactly E=sum_j [W_j,C_j]C_j^-1/2. Every outside bond touches only one
collar. Its norm can be acquired on 2ell+1 physical sites; SU(2) invariance
puts the full norm in M0 without omitting any integer-spin representation.
The global residual cost still scales with the number of seams. The
bounded-factor QBP variant needs the additional inside residual; bounded
factor norm alone is insufficient.

For block4/collar1, root checked the all-size index derivation of the
25-dimensional one-copy and 625-dimensional squared-density closed
transfers. The central indices cross in the second copy, and the cyclic
trace includes the closing seam. Root additionally built the true physical
spin-two pair and full four-site open Hamiltonian independently, retained
all 625 physical states and all magnetization sectors, inserted the closing
seam literally, and compared both traces to the implemented transfer map.
At beta1/8 and3/4 both comparisons passed at their numerical control scope;
the largest relative difference was1.12e−15. This control is recorded in
`PHYSICAL_READOUT_REPLAY.json`; the all-size conclusion comes from the
explicit index proof, not extrapolation of that finite control.

The supplied ansatz readout enclosures use entrywise nonnegative Taylor
series in the Marshall gauge, full local state spaces, rational bounds on
sqrt6 and the tail, explicit positive float64 products, and charged power,
trace and clipped-entry errors. Power-of-two scales cancel only because
the output is normalized purity. No absolute partition value is inferred
after omitting them. The proof's explicit arithmetic model is part of the
scope. It provides accurate purities of this declared ansatz on rings256
and512; the missing target-residual input prevents promoting them to
Heisenberg Gibbs purities.

There is now an exact obstruction for that particular residual input.
Root independently reconstructed the physical four-spin one-magnon matrices
V=h12 and W=h01+h23, used V's exact0/4 projectors to calculate C and C^-1,
and checked the off-diagonal Hermitian residual entry
−(cosh(2s)−1)/2. The block4 seam cells are disjoint and identical. Extreme
eigenvalues of their Hermitian parts add on tensor products, so

    integral||E_total|| ≥ (n/4)[sinh(2beta)/4−beta/2].

At beta3/4 this exceeds10.06847 for n256, and twice that for n512, against
a required global budget below1e−7. `SMALL_COLLAR_REPLAY.json` records
root's exact symbolic matrix identity and positive rational Taylor lower
bound for the integral. Thus this certificate with this amplitude fails
decisively. It is not a lower bound on the actual ansatz purity error and
does not exclude another amplitude, wider entangled blocks, different
compression, ordinary thermal methods or the spin-two gap.

The final source addition bypasses the failed residual for a weaker target
conclusion. The ordinary ALT trace inequality and finite-dimensional Lie
product formula give Z_H(2beta)≤Tr[(exp(−beta H0)exp(−beta V))²], the actual
closed T2 trace with its absolute local exponentials and binary scales
restored. The weaker GT1 upper exceeds it by half the squared Hilbert–Schmidt
commutator norm. Convexity of logZ gives the lower log-purity bound from the
accepted beta1/2 and3/4 warm rows, whose source hashes match the independently
accepted snapshots. All coefficient signs and endpoint directions in this
combination were reviewed. The resulting true log-purity brackets have
widths about112.88 and225.75 on rings256 and512 at beta3/4, against a
required accuracy near7.44e−7. These are actual Gibbs bounds; the much
narrower ansatz intervals are not substituted for them.

Root's physical four-site controls were rerun after the final positive-only
kernel change. Both restored absolute traces agree with independent full
physical calculations; true Z(2beta)≤ALT2≤GT1 passes at beta1/8 and3/4.
The independent eigensolver reference had negative roundoff up to4.99e−16
at beta1/8. That amount was clipped only in the positive-only transfer
test input; the separate physical reference traces were left unchanged.
This is a declared numerical control, not a positivity premise of the
certified source Taylor readout. The current receipt includes those details.

The new operation makes the missing input explicit and locally measurable;
it does not make that input cheap. Squared-density transfer dimension is
5^(4ell); at ell2 dense binary64 storage alone is about1.22TB. An efficient
structured contraction and a certified sufficiently small local residual
remain unacquired. Existing Dyson, Holder, QBP and Gibbs-reconstruction
methods are ordinary comparators and are not claimed as new inventions.
