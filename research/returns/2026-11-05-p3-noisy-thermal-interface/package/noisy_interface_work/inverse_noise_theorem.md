# Positive thermal precompensation under fixed component noise

Status: uniform positivity, constructive sampling, and the prefix proof were
independently checked, 5 November 2026. Active output and controller regeneration
are treated in the accompanying notes. No warm-start Davies theorem is assumed.
Earlier accepted results are inputs, not re-proved. This is a mathematical
research construction under the stated contracts, not a fabricated device or a
priority claim.

## 1. Exact classical object

Let L <= F_2^m be a valid syndrome space, g(s)=exp(-sum_a lambda_a s_a),
lambda_a in [lambda_min,lambda_max], and pi=g/Z on L.
There are n physical sites. Each has at most four Pauli labels and translates
the syndrome by v_(i,a) in L. At most w checks can be touched at one site; each
check is touched by at most d sites. The site interaction graph joins sites sharing
a touched check, so maximum degree D <= w(d-1).

At site i let K_i=sum_a q_(i,a) T_(i,a) be a Pauli convolution, with
q_(i,I)>=1-q, q<1/4. All K_i commute. On the full local Pauli group, Fourier
eigenvalues are at least 1-2q, hence K_i is invertible. Write

  K_i^{-1}=b_(i,0) [I+sum_(a != I) r_(i,a) T_(i,a)].

The coefficients r may have either sign. b_(i,0)>=1 and
sum_(a != I)|r_(i,a)| <= 2q/(1-2q) <= 4q.
The group representation may be nonfaithful on L; using the full Pauli-group
inverse and then mapping translations still gives a valid inverse operator.

For every subset I of sites define mu_I=(product_(i in I)K_i^{-1})pi.
Normalization is exactly one because every inverse preserves the constant
left vector. The issue is positivity uniformly in n and all syndrome constraints.

## 2. Signed noise polymers

For a nonempty connected vertex set C in the site interaction graph define

  z_C(s)=sum_(a_i != I, i in C) product_i r_(i,a_i)
                g(s+sum_i v_(i,a_i))/g(s).

Its absolute value is at most theta^|C|, with

  theta = [2q/(1-2q)] exp(w lambda_max).

Disjoint nonadjacent connected sets touch disjoint checks, so energy ratios
factor. Thus exactly

  mu_I(s)/pi(s) = (product_(i in I)b_(i,0)) Z_I(s),

where Z_I is the hard-core polymer partition function with signed activities
z_C(s), C subset I; compatibility is disjoint and nonadjacent.

Use the conservative condition

  theta <= 1 / [32 e^3 (D+1)].

At complex global scaling z of every r_(i,a), |z|<=2, polymer activities are
bounded by (2theta)^|C|. The KP bound with an additional exponential size
margin holds: at most (e(D+1))^(k-1) connected sets through a site gives

  U = e^2 theta / (1-e^3(D+1)theta)

as a convenient bound for the sum of size-tilted rooted activities at z=1.
The incompatibility sum for activities tilted by e^|C| is
at most (D+1)|C| U < |C|. The analogous condition holds on |z|<=2.

Therefore Z_I(s) is zero-free along the real scaling from 0 to 1; it is real
and starts at 1, so it is strictly positive. Every mu_I is a probability law.
This proves a size-independent positive inverse-noise neighborhood.

## 3. Local sensitivity of the logarithm

Write Psi_I(s)=log Z_I(s). Its cluster expansion has contributions Phi_A(s);
the union of contributing noise polymers touches at most w times their
total size physical syndrome coordinates.

If a syndrome changes on check set S, only clusters meeting at most d|S|
adjacent physical sites can change. Rooted estimates with the size margin give

  |Psi_I(s)-Psi_I(s')| <= 2 d U |S| = kappa |S|.

The stronger weighted estimate, uniformly in all syndrome values, is

  sum_(clusters touching S) sup_s |Phi_A(s)| |support_checks(A)|
       <= w d U |S|.

Weight total cluster size by its exponential, root at an adjacent site, and
apply the tilted KP bound. The estimates hold uniformly over I and over the
ambient bit assignments, not just valid syndromes. Constants can be enlarged
without introducing N dependence.

## 4. Efficient sampling with the accepted history representation

Use the accepted bounded-degree history CSP. Add edges between physical
syndrome variables which a single physical site can affect. Its degree Delta'
is still constant. Components remain individually valid. Enlarging the graph
merges former components, so E(gamma)>=a|gamma| continues by addition.
A nonzero base history still forces a component of at least
L_*(N)=Omega(N^eta) variables, by the accepted isolated-history contraction.

For a compatible history-polymer collection Gamma, its target weight is

  product_(gamma in Gamma) exp(-beta E(gamma)) exp(Psi_I(s(Gamma))).

Set b=beta a-kappa and x=kappa_count exp(-b),
kappa_count=(q_alphabet-1)max(2,Delta')^2.
Deleting gamma changes log Psi by at most kappa|gamma|, so its inclusion
probability is at most exp(-b|gamma|). The truncation tail is
M x^(L+1)/(1-x); the unstable-base tail is B x^L_*/(1-x), where B is the
fixed number of base variables.

For the K retained polymers use exact single-polymer heat bath. Conditional
birth odds are exp(-beta E(gamma)+Delta_gamma Psi), at most exp(-b|gamma|).
Define U_h=x/(1-x)^2.

For configurations differing by polymer xi, hard-incompatibility influence is
at most (Delta'+1)|xi| U_h. For compatible gamma, the change in log odds is
bounded by four times the cluster contributions touching both gamma and xi.
Summing weighted birth-probability differences over gamma gives at most

  4 U_h w d U |xi|.

Thus, if

  [Delta'+1+4 w d U] U_h <= 1/2,

weighted Hamming path coupling contracts by 1-1/(2K). Mixing time is
O(K log(M/epsilon)). Choose fixed beta sufficiently cold for the history
condition, then q sufficiently small for the inverse-noise condition.
Both are independent of N and holding time. Constants may be very unfavorable.

An explicit sufficient threshold can be chosen as follows. Let

  c_h=(q_alphabet-1)max(2,Delta')^2.

Choose beta to satisfy the accepted holding theorem and

  c_h exp(-beta a) <= 1/[32(Delta'+1)].

Put lambda_max=beta J_max and define

  theta_0=min{1/[32 e^3(D+1)], 1/(64 w d)},
  q_0=min{1/8, (theta_0/4) exp(-w beta J_max)}.

For q<=q_0, theta<=theta_0 and U<=8 theta. Consequently

  kappa=2dU<=1/(4w),       4wdU<=1/2.

The preceding history condition then gives the stated mixing margin: indeed
x<=exp(1/4)/[32(Delta'+1)], so
[Delta'+1+4wdU]x/(1-x)^2<1/2. These constants are uniform in system size,
requested duration and requested source accuracy. They are sufficient bounds,
not optimized or practical threshold estimates.

## 5. Polynomial evaluation, without global rejection

For a fixed s, let P_I(z;s) be the exact signed subset sum in section 2 with
each nonidentity r coefficient multiplied by z. This equals Z_I(s) at z=1
and factors over disconnected induced site components.

Its zero-free logarithm on |z|<=2 can be Taylor-truncated at
L_noise=O(log(n/delta)) for additive error delta. An explicit connected-subset
algorithm computes coefficients using

  f_C(z)=sum_(B subset C)(-1)^|C-B| log P_B(z).

f_C vanishes for disconnected C and starts at degree |C|. Enumerating connected
C of size <=L_noise and their subsets/Pauli labels costs n exp(O(L_noise)),
polynomial at fixed degree. Formal-series logarithms and numerical energies
have polynomial bit cost. The zero-free margin gives a uniform tail from an
O(n) bound on the logarithm.

Evaluate each heat-bath transition to error epsilon/(2t_mix); stepwise coupling
charges numerical error. Initial truncation, mixing and arithmetic are all paid.
Global rejection using sup(mu/pi), which can be exponential in Np, is not used.

## 6. Forward noise and logical correctness

The same proof with nonnegative r coefficients controls forward convolutions
of pi by independent small Pauli noise. For a compensated loading sequence,
after physical-noise prefix J the syndrome law is exactly mu_(complement J).
Every prefix therefore has the same unstable tail.

In the protected decoder frame each physical Pauli has identity logical action
on a stable syndrome. A union bound over the sequential noise sites gives a
logical discrepancy at most

  n q * B x^L_*/(1-x)

per compensated write (with fixed-factor adjustments and sampling error).
The displayed probability is a bound in half-diamond distance for the
corresponding channel comparison; full diamond norm has an additional factor
two. The final syndrome marginal is exactly pi. For an unknown logical input
independent of source sampling, its quantum marginal is therefore close to the
accepted thermal encoder by this one-time term. Channel contractivity preserves
the discrepancy through every subsequent hold.

Retained records require the actual seed extension, rather than an independently
pi-labelled record. The ideal comparison keeps the same initial compensated
sample s, the same endpoint Pauli labels, the same resulting syndrome
s'=s+delta(E), and the same record law; it deletes only the nonidentity logical
Pauli accumulated along the endpoint-noise path. The initial seed is mu-distributed
and can be correlated with s'. It must not be replaced in the records by an
independent pi sample. The logical input and its reference may depend on the
retained initial seed. The final syndrome marginal is still pi, which is enough
for the accepted intrinsic-passive-time coupling: its jump rates depend only
on that syndrome, and no uniform rare-posterior estimate is claimed. Arbitrary
pre-existing logical references and retained external records are preserved.

For readout, disjoint raw-to-code encoder interfaces give independent Pauli
input noise. Prefixes K_J pi satisfy the forward version, so the protected BDL
decoder incurs the same rare-prefix term. No nonequilibrium Davies basin is
assumed.

For the full quantum Gibbs state (uniform logical subsystem), compensation
gives exactly the target Gibbs state after terminal product Pauli noise:
logical Pauli effects are immaterial. A pure canonical TFD is NOT upgraded to
a raw fixed-noise output by this theorem.

## 7. Closed noisy-interface bridge in the specified circuit architecture

Naive FT export of a perfect level-1 physical codeword plus tiny global error
is false: residual gauges can be correlated. The completed operation uses
independent encoded Bell resources, destructive logical Bell measurements,
protected fan-out into locally stochastic raw classical pools, and static noisy
majority-tree regeneration. The new tree erases the dependence of its output
errors on arbitrary old syndrome/controller records, while retaining a calibrated
O(p) raw bit error. It uses fixed bounded-fan-in wiring, fresh component faults,
and no ideal mutable routing or perfect final classical bit.

All Bell byproduct corrections are deferred to the final raw local port. The
fresh B half undergoes only its independent protected waiting and descent;
the old coherent controller never acts on it. If K_i is its independent descent
channel and e is the regenerated bit error, the final correction produces

  E_tree,i composed with (1/4) sum_b P_b^{-1} K_i P_b,

followed by the actual terminal Pauli-gate noise. The uniform Bell label b
supplies the Pauli twirl without an extra twirl seed. The resulting boundary is
a product of known one-qubit Pauli channels, up to the explicit protected-circuit
and regeneration error. This is a channel hybrid, not conditioning on global
success. Internal Bell/syndrome transcripts are reset at paid cost; arbitrary
pre-existing external references and records are retained.

For a raw pool with LS error q_c and noisy tree links/voters bounded by
p_c=max(q_c,e,v)<=1/100, a depth-L ternary tree has 3^L leaves and O(3^L)
noisy gates/links. The mixed local-stochastic coupling gives dependence error
at most q_c(21p_c)^L, even when the old errors correlate with arbitrary quantum
records. Its comparison root has an explicit BSC error at most 2p_c. Thus
L=O(log(n/epsilon)) suffices, at polynomial extra pool/output cost. Noisy
component probabilities are fixed; increasing the tree removes old-history
dependence, not the unavoidable raw-output error floor.

The actual protected fan-out, noisy descent and controller constructions are in
endpoint_route/endpoint_and_refresh.md. The static tree and its quantum-reference
coupling are proved in passive_route/static_tree_regenerator.md; the operational
Bell composition is in passive_route/history_erasing_bell_export.md. The specified
architecture has paid nonlocal active links with declared time/error/cost and
constant-size final local cells. It does not assert a finite-speed local
three-dimensional deployment theorem. Input/output raw-port errors, fabrication,
switching, routing, idle time, metrology, classical processing and reset remain
in the operation's resource account.

Known independent Pauli endpoint channels can be characterized by stabilizer
Monte Carlo under a supplied iid Pauli circuit model. Physical parameter
acquisition is separately paid. Accuracy O(epsilon/n) is a statistical cost,
not a requirement that component fault probability vanish with N.
Product-channel mismatch is at most the sum of per-site channel errors.

Noisy reuse may decode into the active processor, perform logical work and
reload a fresh compensated background. It pays another draw/access cost and
does not pretend to be the earlier syndrome-preserving reuse operation.
A finite independent stream can be commissioned with a total TV budget once.

## 8. Free-energy cost of the compensated syndrome source

There is a useful quadratic bound on the additional state free energy. Define

  K_i(t)=(1-t)I+tK_i,     mu_t=(product_i K_i(t)^{-1})pi,
  B_i(t)=-K_i(t)^{-1}(K_i-I),       0<=t<=1.

The same positivity theorem applies along this path. Since the convolutions
commute,

  derivative_t mu_t=sum_i B_i(t)mu_t.

Every B_i has coefficient mass zero and coefficient l1 norm at most 4q for
q<=1/8. For h_t=log(mu_t/pi), the relative log-density oscillation under any
single-site Pauli translation is bounded by

  osc_i h_t <= 2dwU(t) <= 64dw t q exp(w lambda_max).

The scalar prefactor in mu_t/pi cancels from this oscillation. Differentiate
D(mu_t||pi); the derivative of total mass vanishes, giving

  D'(t)=sum_i <mu_t, B_i(t)^* h_t>
       <=256 w d n t q^2 exp(w lambda_max).

Here B_i's zero coefficient mass allows subtraction of h_t(s) before applying
the oscillation bound. As D(mu_0||pi)=0, integration yields

  D(mu_1||pi) <=128 w d n q^2 exp(w lambda_max).

For the decoder-frame states with the SAME logical density matrix in every
syndrome sector, the von Neumann entropy is the classical syndrome entropy
plus that common logical entropy. Therefore their excess nonequilibrium free
energy is exactly

  Delta F=beta^{-1}D(mu_1||pi)
         <=(128 w d/ beta) n q^2 exp(w lambda_max).

This is a state-function cost, not a construction attaining reversible work.
It does not include the energy of computation, links, copying, metrology,
controller resets, refrigeration, fabrication or retained records. Those
execution costs can dominate it and are charged separately.

## 9. Sharp elementary limit

For one thermal bit with excitation r=(1+exp(lambda))^-1 and bit-flip p<1/2,
the unique preimage excitation is (r-p)/(1-2p). It is a probability iff p<=r.
No fixed noise budget can therefore remain uniform as beta tends to infinity.
This theorem gives a nonzero threshold at fixed temperature and bounded
interaction, not zero-temperature purification.
