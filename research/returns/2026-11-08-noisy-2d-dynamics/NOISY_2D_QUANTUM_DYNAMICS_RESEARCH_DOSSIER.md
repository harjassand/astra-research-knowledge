# Noisy 2D quantum dynamics: global prediction, faithful resets, and the sampling frontier

Research dossier, 8 November 2026. No manuscript or public release commissioned.

## Strongest result actually achieved

The fixed-local theorem extends to **arbitrary global products of one-qubit
Hermitian contractions, at all times and every fixed positive noise ratio**.
A second construction extends that capability to **full-rank biased resets
with a known faithful product reference preserved by the coherent dynamics**.
This is arbitrary-accuracy nonunital prediction in that class, beyond a
perturbation floor. The class does not include arbitrary cooling or generic
interacting thermal matter.

The new operations are moving coefficient-weight smoothing with Hamiltonian-sign
duality, support-sensitive hypercontractivity, and a positive buffer that KEEPS
discarded reset registers. A concentration bound pays all added registers and
retains polynomial tensor dimensions. Their proofs and finite resource contracts
are included below, together with independent mathematical reviews.

Supporting results earn full-output TV sampling on **supplied bounded-cut
architectures**, acquisition of a local drift and reusable intervention prediction,
late-time relative mixing, and joint laws of logarithmically many nonlocal
syndromes. Geometry, source, precision and control costs remain explicit.

The strongest obstructions are (i) an original-class rare-probability reduction
which rules out a uniform all-positive-time log/relative evaluator unless NP=RP,
and (ii) a positive noisy-code family whose every bounded-product mean is
exponentially close to uniform while its TV distance from uniform tends to one.
Neither proves hardness of the unresolved generic 2D full-TV sampler.

**Generic intermediate-time 2D full-output sampling remains OPEN.** General
acquired prediction of arbitrary interacting driven matter, arbitrary recovery,
and affordable protected quantum processing remain NOT_ACHIEVED. Polynomial
degrees here can be enormous; no practical superiority, hardware demonstration
or historical first-priority claim is made. Physical experiments:0.

## Governing capital and central formal theorem

The unchanged original proof is `Case_B_second_final/RESEARCH_REPORT.txt`,
SHA256 `32b605ec5ccdc6897af1a24b1be951e0e3ad787a0b4fbff679541d1980ca841b`.
Its original ZIP hash is `d593fd3abe3165e61b38275b95c4a50d1e4ef6b49c1f9774823432aafd7e9283`.
Repository snapshot: `6f26484e44ff347429415f1765892fe34e8c6cc3`,
`research/returns/2026-11-07-p1-final-own-depth-case-b`. The full proof was
independently inspected before extension. Gibbs uniqueness and the separate
thermal-memory results are not load-bearing dependencies here.

**Theorem G.** Fix local range a, block size k, incidence d, g>=J/gamma>0,
and faithful floor nu0>0. Supply n square-lattice qubits, a finite rational
piecewise local Hamiltonian schedule H(t)=sum_b H_b(t) with the fixed bounds,
rational gamma>0 and sigma=diag(p,1-p), min(p,1-p)>=nu0. For biased sigma assume
[H(t),sigma^n]=0. Local charge pinching constructs a reference-preserving block
decomposition without increasing norms, range or incidence. At sigma=I/2 there
is no charge-conservation restriction. The evolution is exactly

    L_t(rho)=-i[H(t),rho]+gamma sum_i(sigma_i tensor Tr_i rho-rho).

For specified rational product input, O=tensor_i O_i with ANY Hermitian
one-qubit contractions, rational T>=0, error epsilon and failure delta, there
is a finite-work classical randomized predictor satisfying

    Pr[|fhat-Tr(O rho_T)|<=epsilon]>=1-delta.

BIT work is polynomial in complete input length B,n,epsilon^-1,log(1/delta),
with degree/prefactor depending on a,k,d,g,nu0. Binary T is part of B; a mixing
test removes large numeric horizons before dynamics. Rate-digit evaluation,
every control segment, numerical precision and randomness are paid. Neither
vanishing noise nor pure-reset limits have a uniform polynomial degree.

This includes global parity and ADDITIVE probabilities of arbitrary partial
product projectors. It does not include relative rare probabilities, a full
n-bit sampler, arbitrary complex products without a paid LCU norm, arbitrary
circuit-described sources, or Gibbs(H). The invariant reference is sigma^n,
generally not Gibbs for the full interacting H.

Prepared inputs of explicit depth c[1+log(2+log Q_bin)] and efficiently generated
classical mixtures can be included with their proved causal-cone/action and
generative costs. Q_bin uses binary input length, not numeric T. Additional
variable-rate/correlated-Pauli noise is a separate UNITAL extension, not an
automatic extension preserving a biased reference.

## Proof and dependency structure

The following complete component proofs are embedded with their exact hashes.
The weighted local constructor establishes sparse propagation and the reset-
register buffer. The next proof supplies physical-support damping, global
branches and bounded Hermitian mixtures. The unital proof records explicit
coefficient, gate, rank and bit bounds. Further sections give sampler/service
theorems and exact obstructions. Supporting source/version/review records are
included in the archive. A passing finite script or polished artifact is not
used in place of a central proof or priority check.
Components retain their original research-stage wording. References within them
to a candidate or ongoing review are historical; the final ledger and completed
reviews give the current status at exactly the scopes they checked.


[Supporting record index](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/INDEX.md) · [Theorem ledger](NOISY_2D_QUANTUM_DYNAMICS_THEOREM_LEDGER.json).


## Proof component 1: Faithful-reference local constructor and positive buffer

Source: [principal/BIASED_RESET_CONSTRUCTION.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/principal/BIASED_RESET_CONSTRUCTION.md), SHA256 `081033fb1dc3d8856babe010c849fc02090c189455e1e62b6a99838d988295ed`.

### Biased resets preserving a faithful product reference

Principal follow-up, 8 November 2026. NEW claim for independent review. It does
not settle arbitrary weak cooling of arbitrary Hamiltonians.

Fix a,k,d,w,J/gamma and rational sigma=diag(p,1-p), mu=min(p,1-p)>0. Supply a
finite rational piecewise 2D Hamiltonian H(t)=sum_b H_b(t), each Hermitian block
having support <=k, range <=a, norm <=J, incidence <=d, and
[H_b(t),sigma^(tensor supp b)]=0 for EVERY block and segment. The generator is

    L_t(rho)=-i[H(t),rho]+gamma sum_i(R_i^sigma(rho)-rho),
    R_i^sigma(rho)=sigma_i tensor Tr_i rho.

Claim: specified rational product inputs and fixed-local Hermitian ||O||<=1 admit
randomized polynomial bit-work additive prediction at every fixed gamma/J>0 and
fixed mu>0; binary T, complete controls, inverse accuracy and confidence digits
are paid. No arbitrary global product-readout extension is claimed here.

For equal biased qubits the block restriction is excitation-number conservation.
Strong spin-exchange and diagonal interactions are permitted. The invariant
state is PRODUCT sigma^n, not generally the Gibbs state of the full interacting
H. This is a common-reference local-reset model, not an arbitrary Davies bath,
work-driving Hamiltonian, pure reset, or physically acquired unknown reservoir.

#### Mixing and imported weighted hypercontractivity

The Hamiltonian contribution to dD(rho||sigma^n)/dt vanishes. Convexity and
quantum Shearer give sum_i[D(rho||sigma^n)-D(R_i^sigma rho||sigma^n)]>=D(rho||sigma^n).
Thus D(rho_t||sigma^n)<=n log(mu^-1)exp(-gamma t), and Pinsker gives the trace
bound sqrt(2n log(mu^-1))exp(-gamma t/2). After gamma T>=C_mu log(n/epsilon)
return the known reference mean. Otherwise JT=O(log(n/epsilon)); ordinary local
Lindblad truncation retains m=O(log^2(n/epsilon)) sites. Restricted blocks keep
the same faithful reference and resets.

Use ||A||_(q,sigma^m)=||(sigma^m)^(1/(2q)) A (sigma^m)^(1/(2q))||_q.
Exact import: Dong--Gao--Ou--Yao--Zhou2606.17729v1 Theorem1.1 gives tensorized
generalized-depolarizing p-to-q hypercontractivity at
t=[3log2/(8a_sigma)]log((q-1)/(p-1)), a_sigma=(1-2mu)/log(mu^-1-1), with its
positive limit at mu=1/2. Their earlier exact-qubit credit to Beigi--Datta--Rouze
must be retained. This applies to all operators, not just PSD ones.

Block conjugations commute with sigma and are isometries at EVERY weighted
exponent. Interleaving therefore proves actual-channel 2-to-q contractivity
for q-1<=exp(c_sigma gamma s), c_sigma=8a_sigma/(3log2). Since
||A||infty<=mu^(-m/q)||A||_(q,sigma^m), choose q>=C_mu m and
s=O_mu(log(2m)/gamma). Weighted-HS error is then converted to at most twice
that error. The early buffer acts on a later observable approximation; it is
not commuted through the drive. Its duration is O(log log(n/epsilon))/gamma.

#### Weighted sparse engine, including the norm of retained basis products

Put z=2p-1. A Hermitian orthonormal basis for symmetric weighted two-norm is
F0=I; F1=X/(2sqrt(p(1-p)))^(1/2); F2=Y/(2sqrt(p(1-p)))^(1/2);
F3=(Z-zI)/(2sqrt(p(1-p))). Nonidentity Fj have zero sigma expectation.
Products are orthonormal, and reset acts as -gamma W, W counting nonidentity.
A commuting Hamiltonian block is skew-adjoint in this Hilbert metric, fixes
identity and preserves its orthogonal complement. Its two-norm is <=2J; local
coefficient dimension 4^k gives one-norm growth <=exp(C_k Jt), C_k fixed.
Allocate gamma/d to each incident block site. Active-sector damping and
interpolation give a fixed coefficient p_c<2 and sparse pruning with <=4^k
branches per input basis element.

Use a rational matrix Cayley unitary for each WHOLE commuting block, followed
by positive Euler resets. This preserves the reference exactly; its near-identity
logarithm has norm O(Jh), giving the same estimates with larger fixed C_k.
Local rational inverses have fixed dimension. Individual physical Pauli terms
need not preserve sigma and are NOT used separately in this sparse engine.

Also track exp(theta W) coefficient two-norm. A local skew matrix connects
weights differing by <=k, and its tilted symmetric-part row sum is bounded by
C'_k J sinh(k theta). Choosing theta<=min(1/(2k),gamma/[16d k C'_k J]) makes
allocated damping absorb it. Pruning decreases both norms. The initial fixed-
support O has constant budgets M0,Mtheta. Every retained |b|>=tau obeys
exp(theta r)|b|<=2Mtheta, hence r<=theta^-1 log(2Mtheta/tau)=O(log Q).

Fj are NOT unitaries. Their operator norms are bounded by C_mu, so the retained
product norms C_mu^r are polynomial and must be paid in buffer accuracy and
estimator bounds. The sum sum_j |b_j|C_mu^(r_j) is polynomial.

Basis entries are fixed-degree computable algebraic numbers. Use certified
dyadic updates, not claimed exact rational closure. With a predeclared polynomial
Kmax, per-update rounding nu satisfying Q_up Kmax nu<=min(eta,M0,Mtheta)
exp(-theta m)/100 keeps both budgets within a constant factor. This needs
O(m+log Q_up+log Kmax+input bits) precision bits. Choose pruning and Kmax with
the doubled budgets in advance, avoiding a circular norm/rank promise.
Here eta is the allocated weighted-HS error. Also pay the finite precision in
the algebraic basis transformation, e.g. through an extra O(m log C_mu) bits,
so its represented weighted-HS error fits eta as well.

#### Construct the nonunital buffer by retaining local reset registers

A biased reset is NOT random unitary on the physical qubit. In its Euler mixture
sample a reset event with probability gamma h. At each event sample an ancilla
|a> with probabilities p,1-p, SWAP it with the physical qubit, and KEEP the old
register as a coordinate at that same spatial site. Averaging gives the biased
replacement EXACTLY. These sampled pure ancillas are an INTERNAL numerical
ensemble, not physical access to bath outcomes or pure ancillas in the target
experiment. Initial product inputs use their usual local purifications.
Draw ONE shared reset history, thermal-bit list and register labeling per outer
sample for both parity states. Reverse the same finite strip unitary exactly
for U_B^dagger; never draw fresh thermal bits or reset events for that inverse.

Each enlarged trajectory is unitary. Local SWAPs have zero spatial crossing
action. In their toggling frame H_b acts on different internal registers but
keeps its spatial support, norm and a fixed-size Pauli expansion. Only in the
BUFFER reference, decompose H_b into physical Pauli terms, with coefficient
one-norm <=2^k J. Finite-step reference invariance is not needed there: its
channel/operator error is directly paid. The sparse engine above used whole
commuting blocks. Factorial spatial locality is independent of the number of
internal registers and local swaps.

Normalize each retained Fj product by its paid norm C_mu^r. It is now a
Hermitian product contraction. For a unitary trajectory U the Q_j=U^dagger
O_j U commute; the overlap <Q_even psi,Q_odd psi> equals their product mean.
The Q_j need not square to identity. Localized parity factors remain contractions
on disjoint same-parity strips. On-site insertions contract vector norms and
cross-cut Schmidt nuclear norms.

Each nonempty strip row has <=C b_strip spatial sites. Its reset count is a sum
of independent Bernoulli variables with mean <=C b_strip gamma s. A Chernoff
bound, uniform in time-step count, implies that simultaneously over <=C m
nonempty rows, with failure <=delta_hist, each count is at most

    C'[b_strip gamma s+log(Cm/delta_hist)].                 (4)

Choose a deterministic cap using (4), and return zero on numerical histories
exceeding it. Normalized mean bias is <=delta_hist. There is no rejection loop.
Set delta_hist=xi/100, where xi is the normalized buffer accuracy, independent
of Monte Carlo confidence delta. The cap is a bias budget for each sample, not
a union-bound demand that all repeated histories avoid it. Thus row dimension
depends polynomially on inverse accuracy and only indirectly logarithmically
on confidence through repetition counts, preserving confidence-digit complexity.
At s=O_mu(log log Q)/gamma and factorial width b_strip=O(log Q/log log Q),
the cap is O_mu,g(log Q). A row's Hilbert dimension including ALL kept ancillas
is therefore 2^O(b_strip+cap)=Q^O(1).

The exact-reference Schmidt nuclear norm obeys Bstar<=exp(C_k b_strip J s),
again polynomial. The original iterative MPS truncation lemma, finite-bit
canonicalization and bounded symmetrized overlap sampler apply with polynomial
row dimensions, ranks, gate counts and precision. Divide delta_hist and buffer
errors by the polynomial retained weighted one-norm and C_mu^r factors. All
coins are finite rational Bernoulli/thermal choices; all schedule lengths,
random bits, input purifications and arithmetic are charged.

This supplies the missing positive-buffer representation rather than assuming
mixed-unitary biased noise or using a divergent sum of sqrt(h) couplings.

#### Limits and independent challenges

Check exact weighted HC, basis normalization, skew/tilted block inequalities,
predeclared rounding budgets, contraction parity identity, internal-register
locality and Bernoulli cap bias before accepting the theorem. The general
algorithm has not been run. New candidate bridge: weighted sparse propagation
plus the reset-register buffer. Existing generalized hypercontractivity,
coefficient interpolation, entropy decay and the original strip proof retain
credit. No practical advantage, pure reset, unknown bath acquisition, arbitrary
work controls, generic interacting Gibbs solver, or original2D full sampler
follows. A common faithful reference and per-block conservation are substantive.


## Proof component 2: Global biased-readout closure

Source: [principal/BIASED_GLOBAL_READOUT_CLOSURE.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/principal/BIASED_GLOBAL_READOUT_CLOSURE.md), SHA256 `9f8ae0f5fc319b150fbaccbcf07d221fafb0e730673ce7cf80ad7f0180adde38`.

### Biased-reference GLOBAL Hermitian product readouts

Principal new closure for independent review. Keep all full-rank sigma,
per-local-block reference conservation, bounded 2D schedule, rate and explicit
input conditions of BIASED_RESET_CONSTRUCTION.md, but allow ANY global product
of Hermitian one-qubit contractions. Claim: all-time randomized polynomial
bit-work additive prediction, with class dependence on mu>0 and J/gamma. This
is NOT relative-probability evaluation or full-output sampling.

#### Crucial operation

Reserve gamma/2, allocate gamma/(2d) to block sites, and use the reviewed tilted
KMS coefficient estimate. With theta<=1/2 fixed small enough and
alpha(u)=min(gamma u/2,theta), the moving-weight proof gives

    ||exp(alpha W)S||_(2,sigma->2,sigma)<=1.

The KMS adjoint reverses Hamiltonian sign and chronology; biased reset is
self-adjoint. Consequently ||S exp(alpha W)||<=1 and

    ||S X||_(2,sigma)<=||exp(-alpha W)X||_(2,sigma).        (1)

An ORDINARY traceless Hermitian Bloch unitary A_i need not be sigma-centered.
Write A_i=a_i I+B_i orthogonally in weighted two-norm, a_i=Tr(sigma A_i),
and z=2p-1. Then |a_i|<=|z| and ||A_i||_(2,sigma)^2<=1. Therefore

    ||exp(-alpha W_i)A_i||_(2,sigma)^2
       =a_i^2+exp(-2alpha)||B_i||_(2,sigma)^2
       <=z^2+(1-z^2)exp(-2alpha).

For alpha<=1/2, 1-exp(-2alpha)>=alpha and 1-z^2=4mu(1-mu)>=2mu. Thus this
square is <=exp(-2mu alpha), and tensorization with (1) gives

    ||S P||_(2,sigma^m)<=exp(-mu alpha(u) r)              (2)

for a product of r ordinary traceless Hermitian Bloch unitaries. The weighted
identity components do not vanish; faithfulness already bounds their size.
This is precisely the operation missing from the earlier local-only theorem.

#### Support-sensitive HC and constructive branches

Put t0=2theta/gamma and lambda=mu theta. Localize P with error eta to
m<=min(n,C r[1+JT+log((r+1)/eta)]^2). In the EARLY interval take weighted
HC exponent q>=max(2,4m log(mu^-1)/(lambda r)). It can be reached by a rational
s=O_mu,theta((1+log(m/r))/gamma) using the checked conservative HC rate.
Then mu^(-m/q)<=exp(lambda r/4). For T>=s+t0, apply (2) to the later interval:

    ||Phi_(0,T)P||infty<=eta+exp(-3lambda r/4).           (3)

Let Q=2+B+n+epsilon^-1+confidence digits, L=ceil log2 Q. First use the biased
global entropy cutoff gamma T>=C_mu L and return the known sigma^n mean.
Otherwise JT=O(L), m/r<=C L^2, and s+t0=O_mu,g(log L)/gamma.

1. Large r>=C/lambda log1/epsilon with T>=s+t0: return zero by (3).
2. T<s+t0: use the GLOBAL reset-register short buffer, m possibly n.
   Width b=O(L/log L), row reset cap O(b gamma T+log(m/xi))=O(L), row dimension
   exp(O(L)), crossing nuclear exponent O(bJT)=O(L). All costs are polynomial.
3. Otherwise r=O_mu,theta(log1/epsilon). Expand P in at most 4^r F-basis terms.
   Initial weighted two-norm<=1, coefficient one-norm<=2^r, and tilted norm
   <=exp(theta r), all polynomial in Q. Now m=O(L^3). The reviewed sparse
   engine retains polynomial coefficients with weights r_j=O(log Q); product
   factor norms C_mu^(r_j) are paid. The usual early weighted-HC buffer lasts
   O_mu(log m)/gamma=O_mu(log L)/gamma and is polynomial by the reset-register
   lemma. No growing support appears in a hidden class exponent.

Use the ORDINARY decomposition O_i=a_i I+b_i A_i, |a_i|+b_i<=1, to sample a
bounded signed mixture of the products above. The original finite-bit rational
axes approximation, clipping, Hoeffding and internal confidence budgets apply.
Do NOT presume |Tr(sigma O_i)|+||O_i-Tr(sigma O_i)I||<=1; that shortcut is false.

This yields all-support Hermitian products in the conserving biased-reset class,
assuming the two reviewed component constructors. It does not cover arbitrary
complex products without a paid LCU norm, mu->0 uniformly, arbitrary work drives,
Gibbs(H), arbitrary correlated sources, rare relative accuracy or a full sampler.
The fourth researcher's dual-rail tiling obstruction is compatible with this
additive theorem. Prepared-source transfers need their separate paid description
and loglog Q_bin depth cap. Historical novelty remains unestablished.


## Proof component 3: Global conservation and known dressing

Source: [principal/CONSERVATION_TWIRL_AND_DRESSING.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/principal/CONSERVATION_TWIRL_AND_DRESSING.md), SHA256 `6648e4f44cc6ea4819292c84d7a31a46b95fc41fda68cfdd67787ba485b88f6f`.

### Global conservation is enough

For common biased sigma=diag(p,1-p), p!=1/2, put Q=sum_i |1><1|_i.
[H,sigma^n]=0 iff [H,Q]=0, since different excitation sectors have distinct
reference eigenvalues. Twirl EACH supplied local block by exp(i phi Q_b).
Equivalently set its matrix entries between different local excitation sectors
to zero. This keeps rationality, support, degree and norm bounds. Linearity
and global conservation imply sum_b Twirl(H_b)=Twirl(H)=H exactly. Every new
block preserves its local reference. Hence per-block conservation is an
efficiently constructible representation, not a stronger physical assumption.
At p=1/2 no conservation is needed and the unital theorem applies.

Known fixed-depth local conjugation V transfers the local-readout theorem to
the interacting reference V sigma^n V^dagger. Physical product input becomes
constant-depth prepared input V^dagger rho V; exact preparation cones and the
extra O(b depth(V)) crossing action fit the reset-register proof. If V is
Clifford, physical global Pauli products and product-Pauli-basis projectors
also transfer, using bounded mixtures. Arbitrary global axes after a general
dressing require separately paid LCU norm. This compatibility needs review.

The dressed reference is Gibbs for the commuting local Hamiltonian
H_ref=omega sum_i V Z_i V^dagger when sigma is its one-spin thermal factor;
it is generally NOT Gibbs for the actual interacting VHV^dagger. This is a
routine unitary-covariance corollary, not a generic Gibbs algorithm or a free
physical preparation/control mechanism. Conjugated reset channels are specified
Markov maps; microscopic bath/implementation costs remain separate.


## Proof component 4: Simpler whole-block buffer

Source: [auditor/BIASED_RESET_BUFFER_SIMPLIFICATION.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/auditor/BIASED_RESET_BUFFER_SIMPLIFICATION.md), SHA256 `25f98e438355006e70d7e265708ff6d37c149aafc734fa127823386890eadafa`.

### Whole-block Cayley buffer simplification

Auditor, 8 November 2026. A separate strengthening of the reviewed buffer
implementation; `BIASED_RESET_REVIEW.md` remains unchanged at its reported hash.

For a k-qubit Hermitian block H of norm at most J, set

    U_h=(I-i hH/2)(I+i hH/2)^(-1).

Then `U_h-I=-i hH(I+i hH/2)^(-1)`, so `||U_h-I||<=|h|J`.
In the normalized physical Pauli expansion, Cauchy--Schwarz gives

    ||coeff(U_h-I)||_1<=2^k||U_h-I||_(2,tau)<=2^k J|h|.

Thus the sum of absolute Pauli coefficients of U_h is at most
`1+2^k J|h|<=exp(2^k J|h|)`. Across every spatial bipartition each Pauli
summand is a product unitary. Nuclear/operator matrix triangle inequalities
therefore give

    N_cut(U_h psi)<=exp(2^k J|h|) N_cut(psi).

Gates wholly on one side preserve the nuclear norm exactly. Summing only the
crossing block actions yields the same `exp(O_k(b_strip Jt))` buffer bound.
The Pauli expansion of a single block has at most 4^k terms, hence an MPO of
bond at most 4^k; applying it increases an MPS bond by only that fixed factor.
Its physical entries are rational and the expansion is performed once per
fixed-size gate, not expanded over a full Trotter layer.

For locality, U_h equals exp(-ih H_eff), where

    H_eff=(2/h) arctan(hH/2), ||H_eff||<=J.

The effective Hamiltonian is supported on the same block. No evaluation of
arctan is needed; this is a proof-only representation. Disjoint-support
colors therefore realize a piecewise bounded local Hamiltonian with total
duration at most the fixed color count times t. The factorial LR proof applies.
On-site reset SWAP toggling changes only which internal registers the block
acts on and leaves spatial support and norm unchanged.

If H commutes with its product reference then U_h and H_eff do too. Hence one
may use whole reference-preserving Cayley blocks in BOTH the sparse engine
and the reset-register buffer. The buffer need not first split the Hamiltonian
into physical Pauli rotations or lose exact finite-step reference preservation.
The split-Pauli buffer in the reviewed construction is nevertheless valid
because its channel error is separately paid. This is a simpler alternative,
not a correction to a false theorem.


## Proof component 5: Unital global theorem and quantitative cost closure

Source: [machinery/FINAL_GLOBAL_READOUT_THEOREM.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/machinery/FINAL_GLOBAL_READOUT_THEOREM.md), SHA256 `848ce4898349c0437d7ad2f1dd89e0697186ef02d674bfff678d19dc32be1243`.

### All-time global Hermitian product readouts: final formal theorem and cost closure

8 November 2026. This expands and checks the frozen independent report initial/machinery.md (SHA256 e0100982b66df8da37d46f2edd48d861f5c463c2b5e620f869399a024e80aa46). Its bytes are unchanged. Subsequent team exchange was authorized before this file was written. The proof uses the pinned original 2D predictor's inspected constructive MPS/strip machinery; it does not claim implementation at its worst-case bounds or historical priority.

#### 1. Input contract and conclusion

Fix a,k,d and g>=J/gamma0, where gamma0>0. There are n explicitly listed qubits on a finite square-lattice region. The input contains a finite piecewise-constant schedule on [0,T], rational breakpoints, and rational Pauli coefficients. At every time, H(t)=sum_a h_a(t)P_a has term support size <=k, range <=a, |h_a(t)|<=J, and at most d active terms at each site. The full number M of segments and their bits are paid. Arbitrarily short segments are permitted; no reciprocal minimum segment length enters the cost.

The base generator is

    L_t(rho)=-i[H(t),rho]+gamma0 sum_i(E_i(rho)-rho),
    E_i(rho)=I_i/2 tensor Tr_i rho.

The initial input is a rational one-qubit product density matrix, and

    O=tensor_i O_i, O_i=O_i^dagger, ||O_i||_infty<=1,

with rational two-by-two factors and no support bound. Given rational 0<epsilon<=1/2 and 0<delta<1, a finite-work randomized classical algorithm returns rational fhat with

    Pr[|fhat-Tr(O rho_T)|<=epsilon]>=1-delta.

Work is polynomial in explicit n, complete binary input length B, 1/epsilon and log(1/delta), with degree/prefactor depending only on a,k,d,g. Binary T is included in B; one can therefore also state the weaker requested polynomial bound in numeric 1+T. Large horizons are discarded by mixing before numerical evolution. A polynomially evaluable rate in place of rational gamma0 is permitted only with its actual certified digit-acquisition cost charged.

The output is an additive mean. It includes global Pauli parities and additive probabilities of arbitrary product projectors. It is not a total-variation sampler, a relative-probability oracle, or an arbitrary correlated-input predictor.

#### 2. Chronology convention

Let E_{t,s} be the Schrödinger propagator from s to t, and Phi_{s,t}=E_{t,s}^* its Heisenberg dual. Then

    Phi_{s,t}=Phi_{s,u} Phi_{u,t}.

Whenever the proof uses a short hypercontractive buffer, that buffer is the EARLY interval [0,s]. Sparse propagation acts on the LATER observable Phi_{s,T}O. No channels from different time intervals are commuted. Norm estimates hold for every schedule ordering because their local inequalities are uniform in the instantaneous coefficients. On taking Hilbert–Schmidt adjoints one reverses the schedule and the Hamiltonian sign.

#### 3. Pauli smoothing, with proof

Use normalized Hilbert–Schmidt norm and Pauli weight operator W(P)=|P|P. Set

    theta=min(1/(2k),gamma0/(16kdJ)),
    alpha(u)=min(gamma0 u/2,theta), t0=2theta/gamma0.

For any interval of duration u and its actual chronological propagator S,

    ||exp(alpha(u)W) S||_{2->2}<=1,
    ||S exp(alpha(u)W)||_{2->2}<=1.                     (3.1)

Consequently, if X is supported in homogeneous Pauli weight r,

    ||S X||_2<=exp(-alpha(u)r)||X||_2.                 (3.2)

Proof: reserve half the replacement rate. Allocate gamma0/(2d) per incident Hamiltonian term on each site of that term. On an anticommuting Pauli pair a coherent term has skew entries of magnitude 2|h_a|. Conjugation by exp(alpha W) gives Hermitian-part norm at most 2|h_a|sinh(k alpha), while its allocated active-sector damping is at least gamma0/(2d). Because k alpha<=1/2 and 2J sinh(k alpha)<=4Jk alpha<=gamma0/(4d), the tilted half-noise generator has nonpositive Hermitian part. Unallocated noise is dissipative.

For b(u)=exp(alpha(u)W)X(u), the remaining half-noise contributes (alpha'(u)-gamma0/2)W to b's generator. This is nonpositive. Thus its squared norm decreases, including across segment boundaries and the corner alpha=theta. This proves the first bound. The reverse-sign reversed schedule has the same bound, and adjoint duality proves the second. Applying it to exp(-alpha r)X proves (3.2).

This is a moving-weight use of the two-by-two estimate in Angrisani et al2609.40174v2 Corollary S12, with rate allocation made explicit. Merely citing fixed weighted-norm contractivity would not prove (3.2).

#### 4. A product with r nonidentity traceless factors

First handle P that is a local traceless Hermitian unitary at r sites and identity elsewhere. Its Pauli expansion is homogeneous of weight r and HS norm one.

Localize the full evolution to A, the union of radius-R balls around its support, with operator-norm error eta. An explicit larger version of the original exponential locality bound gives constants C_loc,v_loc depending only on a,k,d such that

    R<=C_loc[1+JT+log((r+1)/eta)],
    m=|A|<=min(n,C_loc r[1+JT+log((r+1)/eta)]^2).       (4.1)

Replacement is sampled as one-site Pauli kicks. Conditional on any noise history, its toggling-frame Hamiltonian has the same local strengths and incidence. Hence the usual linked-interaction locality bound depends on J, not on the number or rate of on-site kicks. Averaging preserves it. This also supplies (4.1) for the noise extensions in Section 9.

On m sites, real-channel hypercontractivity gives

    ||Phi_{0,s}Y||_{q,tau}<=||Y||_{2,tau}
    when q-1<=exp(2gamma0 s).

King1210.8412 Corollary2 supplies the depolarizing inequality. Interleaving with Hamiltonian conjugations, which are Schatten isometries at each exponent, and taking the product limit proves the actual-channel statement.

Choose

    b=max(1,ceil(log_2(8m/(theta r)))), s=b/(2gamma0).

Taking q=1+exp(b), normalized Schatten comparison gives

    ||Phi_{0,s}Y||_infty<=2^{m/q}||Y||_2
                           <=exp(theta r/4)||Y||_2.

If T>=s+t0, apply (3.2) to the LATER interval [s,T]. Therefore

    ||Phi_{0,T}^{A}P||_infty<=exp(-3theta r/4),
    ||Phi_{0,T}P||_infty<=eta+exp(-3theta r/4).         (4.2)

This estimate holds against any input state. Product input is required only to compute the other cases.

#### 5. Quantitative rational propagation lemma

Here all dependence on growing support is visible. On m retained sites let X be a rational Hermitian observable with ||X||_2<=1 and initial Pauli coefficient one-norm at most M0. Let its explicit expansion have U terms. The support size is not a class constant.

For schedule segment j, of length Delta_j, let

    S_j=2 sum_a |h_{a,j}|+2 gamma0 m,
    A_j=S_j Delta_j, A_tot=sum_j A_j.

For target channel/HS error eta, choose

    r_j=max(1,ceil(A_j),ceil(10^6 A_tot A_j/eta)),
    R_num=sum_j r_j<=2M+2A_tot+10^6 A_tot^2/eta.         (5.1)

Use exact rational Cayley Pauli rotations and positive Euler replacement maps. The first-order channel error is at most 40 sum_j A_j^2/r_j<eta/100. Empty or zero-action intervals may be skipped. This follows by local second-order remainder bounds and contractive telescoping. All actual rationals, however short their time segments, have paid bit length. No step count proportional to 1/min Delta_j appears.

Allocate replacement gamma0/d per Hamiltonian term support and leave the nonnegative residual on every site. Put

    p=2/(1+min(1,gamma0/(2dJ)))<2,
    beta=ceil(4+4dJ/gamma0),
    Q_up<=C(kd+1)m R_num,
    ell=ceil(log_2(64 Q_up M0^2/eta)), tau_cut=2^(-beta ell).

Process a complete damped Hamiltonian block before pruning coefficients below tau_cut. Each Pauli has at most two branches. Every block contracts Pauli-p coefficient norm; pruning decreases it. The same proof as the original yields total pruning HS error <=eta/4 and

    K<=(M0/tau_cut)^p
      <=M0^2 [128 Q_up M0^2/eta]^(2beta),              (5.2)
    sum_j |b_j|<=sqrt(K)(1+eta).                       (5.3)

The initial U and the displayed K are charged. Updates merge exact rationals with common branch denominators. Coefficient bit height is bounded by

    C[B+Q_up(B+log R_num+log(K+2))],

up to harmless input-index factors. Thus arithmetic work is polynomial in these displayed parameters. Neither constant support nor a spectral-gap assumption is hidden in this lemma.

#### 6. Quantitative global short-buffer lemma

For any fixed c, the original constructive strip proof evaluates a supplied Hermitian product contraction on m up to n sites, on product input, whenever

    JT<=c[1+log L],
    L>=max(64,log_2(100m^2/xi),log_2(2+B)),             (6.1)

with xi its target additive error. Time segments are explicit and paid. It suffices that c be a class constant.

Here are the actual cost parameters. Use (5.1), with eta=xi/100, for a rational channel reference; let G_num be its elementary gate count and take M_c=100(G_num+1)(m+1)^3. Color each segment's local terms with at most chi=kd+1 colors. All its noise histories are product Pauli kicks. Removing these to a toggling frame gives total colored physical duration at most chi T, independent of step and switch count.

Set A_fac>=max(64,2kd chi c) large enough to bound the linked-tail argument z<=A_fac(1+log L). Choose

    q=ceil(64(1+A_fac)^2 L/floor(log_2 L)),
    b_strip=a(q+2).

The linked-integral estimate bounds every strip truncation by support_prefactor z^q/q!, whose sum is <=xi/100; the polynomial support prefactor is absorbed by the chosen L. Thus

    b_strip<=C_fac L/log L,
    q_row<=4^[8(b_strip+a)],
    B_star<=exp(128ad(b_strip+a)J chi T),
    D=ceil((128 M_c B_star/(xi/100)^2)^2).             (6.2)

The harmless factor chi can be omitted with a more parallel accounting; retaining it is conservative. Equations (6.1)–(6.2) give log q_row=O(L), log B_star=O(L), and log D=O(L+log M_c+log(1/xi)), with constants depending only on physical class and c.

A uniform local dense-arithmetic polynomial in B,m,G_num,q_row,D and log(1/xi) constructs the two rational MPSs. One can use thresholded gap-free SVD compression with constant-factor rank slack, rather than requesting continuity of an arbitrarily selected top-D singular subspace at degeneracy. The nuclear/operator-duality truncation proof needs only a bounded discarded operator norm and a retained rank bound. Every compression/norm-rounding budget is paid as in the original and the constructor's numerical refinement.

The symmetrized overlap mixture has sample magnitude <=1, including when the two MPS site orders differ. It needs O(xi^-2 log(1/delta_b)) independent repetitions; all histories and categorical choices have finite paid random bits. Consequently the entire buffer cost is a fixed polynomial in the displayed algebraic parameters. In particular it is polynomial in B,m,M,xi^-1,log(1/delta_b) when L=O(log Q) and JT=O(log log Q). This is the quantitative statement used below; there is no growing-support parameter in a class exponent.

For Hermitian contraction factors, Q_j=U^dagger P_j U commute and are Hermitian contractions. Put their even and odd products on the two sides of an overlap. Localized products remain contractions, so vector telescoping and truncation work. On-site insertions cause no cross-cut nuclear growth. Thus global support and contraction rather than unitary factors do not add a cost beyond (6.2).

#### 7. Branching algorithm and polynomial closure

For a homogeneous product P, target error xi and confidence beta, set

    Q=2+B+n+ceil(1/xi)+ceil(log(2/beta)), L0=ceil(log_2 Q).

If r=0 return one. If gamma0 T>=4L0, return zero by the original entropy estimate; P is traceless. Otherwise JT<=4g L0. Localize with eta=xi/100. Equation (4.1) gives m/r<=C(1+L0)^2, so the s of Section4 obeys gamma0 s<=C+log_2(1+L0).

- If T>=s+t0 and r>=ceil((4/theta)log(100/xi)), return zero using (4.2).
- If T<s+t0, apply the GLOBAL short-buffer lemma on m sites. Here JT<=C_g(1+log L0). Taking L=Theta_class(L0) in Section6 yields polynomial work even when m=n.
- Otherwise r=O_theta(log(1/xi)). Expand P into at most U=3^r terms with M0<=3^(r/2). The localized region has m=O_theta(L0^3). In the early interval take s0=ceil(log_2(2m))/(2gamma0). If T<s0 use the buffer directly. Otherwise propagate the LATER interval [s0,T] with Section5 to HS error eta=xi/100. Its action A_tot<=C m(J+gamma0)T=O_class(L0^4), and Q_up is polynomial in M,L0,xi^-1. Moreover

      U<=[C/xi]^(4log(3)/theta+1),
      M0<=[C/xi]^(2log(3)/theta+1).

  Thus (5.2)–(5.3) give K and coefficient one-norm polynomial in M,L0,xi^-1. The EARLY channel maps the HS error to at most twice its norm. Each remaining Pauli buffer is requested at accuracy xi/[C max(1,sum|b_j|)], whose inverse is still polynomial. Its duration is O(log m)/gamma0=O_class(log L0), and its logarithmic precision parameter in Section6 is O_class(log Q+log M). All costs stay polynomial.

This closes the dependency chain without treating r as a hidden constant or applying the original gross D_kappa envelope with a growing w.

#### 8. Arbitrary Hermitian product contractions and complex LCU boundary

Write O_i=a_i I+b_i A_i with b_i>=0, A_i a traceless Hermitian unitary, and |a_i|+b_i<=1. Independently choose I with probability |a_i|, A_i with probability b_i, or a zero contribution; retain the signs of a_i. This is a bounded mixture with expectation O. Use Section7 for M_out=O(epsilon^-2 log(1/delta)) independent samples, internal accuracy epsilon/10, and failure delta/(2M_out). Clip inner values to [-1,1]; Hoeffding and the conditional union bound prove the theorem.

For rational inputs, approximate b_i downward and A_i by an exactly rational unit Bloch vector via a well-conditioned stereographic chart. Taking local norm error O(epsilon/n) pays O(epsilon) total error by product telescoping. Certified square roots and logarithmic dyadic precision suffice. All mixture probabilities and all matrices passed to Section7 can therefore be rational; no real-number oracle is introduced.

The inequality |a_i|+b_i<=1 is specific to Hermitian contractions. The theorem DOES NOT include arbitrary complex product contractions. Such a product is allowed only with a separately paid tensor-product Pauli/identity LCU whose coefficient one-norm Lambda_O is supplied or computed. Sampling its normalized absolute coefficients costs O(Lambda_O^2 epsilon^-2) repetitions, with errors divided by Lambda_O.

For example, exp(i theta sum_i Z_i/n) has such an LCU with Lambda_O<=exp(|theta|); frequencies |theta|=O(log(1/epsilon)) remain polynomially paid. The different normalization exp(i theta sum_i Z_i/sqrt(n)) can have LCU one-norm exp(O(|theta|sqrt(n))); no polynomial conclusion for it follows. A short-buffer overlap may accommodate some complex factors with adjoints on one side, but that does not repair the missing bounded global mixture at later times.

#### 9. Variable replacement rates and correlated Pauli jumps

The same theorem holds for the explicitly piecewise rational generator

    L_t=-i[H(t),.]+sum_i gamma_i(t)(E_i-Id)
                     +sum_b lambda_b(t)(Ad_{P_b}-Id),

where gamma_i>=gamma0>0 and lambda_b>=0. P_b are explicitly listed Hermitian Pauli strings; their supports may be correlated or extensive because every Ad_{P_b} is a tensor product of one-site Pauli conjugations. Arbitrary multiqubit unital Lindblad operators are not admitted.

A simple uniform numerical contract fixes gamma_max/gamma0 and a bound lambda_site/gamma0 on sum_{b:i in supp P_b}lambda_b in every segment. Full jump lists, supports, rates and segment bits are paid. Then the extra action is polynomial under the same mixing cutoff. Alternatively the displayed propagation bounds may be used with their actual additional numerical action, but this is not a claim that arbitrarily large encoded rates cost only their bit length.

Proof changes: reserve gamma0/2; all extra noise is diagonal nonpositive in Pauli coefficients, so both coefficient-p and tilted weighted-2 estimates improve. Each extra map is a unital Schatten contraction, preserving hypercontractivity and entropy contraction. Histories remain product Pauli kicks and contribute ZERO nuclear crossing action. Counts in (5.1) use

    S_j=2sum_a|h_a|+2sum_i gamma_i+2sum_b lambda_b,

and include the number of listed jump maps in Q_up and G_num. The rates' finite representation and every elementary sample are charged.

An important localization convention: retain each Pauli jump with P_b replaced by its restriction P_b|A and the SAME rate. Do not discard a correlated jump merely because its full support crosses the region boundary. Its restricted action on local observables is exactly this map. Jumps whose restriction is identity may be omitted. The trajectory locality estimate (4.1) remains independent of these kick rates because they do not spread support and only change signs of local Pauli Hamiltonian coefficients.

#### 10. Compatible prepared-input extension

The theorem also permits input W_p rho_product W_p^dagger where W_p is an explicitly listed bounded-range bounded-arity local unitary circuit of depth

    ell_p<=c_p[1+log(2+log Q)],

for fixed c_p, with rational or paid certified algebraic entries. The full circuit count/bits are charged. Efficiently generated classical mixtures of these descriptions are allowed with the generator's actual work and output precision charged.

This uses the auditor's repaired construction. Localize the noisy observable first; include its preparation causal cone. For each strip localize the noisy history with margin b_U, and conjugate exactly by the preparation circuit on a margin enlarged by O(ell_p). The parity vectors now act on the original product purification. Their strip width is b=b_U+O(ell_p), and

    log B_star=O(b(JT_buffer+ell_p)).

Since b_U=O(L/log L), JT_buffer=O(log L), and ell_p=O(log L), this is O(L). Preparation contributes at most O(b ell_p) crossing gates, each of constant local operator Schmidt one-norm. The full product-readout argument remains valid because high-weight suppression is input independent; only the nonsuppressed buffer changes as just described. No arbitrary circuit-described correlated input is covered.

#### 11. Status and dependencies

The new mathematical closure is moving Pauli-weight smoothing, support-sensitive hypercontractivity, and explicit all-support branching. The inherited physical-time strip constructor, sparse coefficient propagation, King hypercontractivity and BGM overlap architecture retain their proper credit. Schedule, classical-mixture, prepared-input and Pauli-noise transfers are stated at their exact paid representation scopes. The theorem is internally derived and subject to the ongoing three-researcher cross-audit; no historical first-priority, practical capability or full-output sampling is inferred.


## Proof component 6: Full-output sampler on bounded interaction cuts

Source: [initial/constructor.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/initial/constructor.md), SHA256 `4c6e17df225552c056d9e04ba146b33f307bea982ec7b149e3dc33372580281f`.

#### 3. Formal sampling theorem

Fix the local support bound k, term-incidence bound d, local purification
dimension r0, cut bound c and positive ratio upper bound `g >= J/gamma`.
These are class parameters. A finite instance consists of:

* n physical qubits, rational gamma>0 and a rational final time T>=0;
* a binary tree with n labelled leaves and O(n) nodes, all internal degrees at
  most three; deleting any edge e partitions the leaves into `A_e,B_e`;
* a rational piecewise-constant Hamiltonian schedule
  `H(t)=sum_a h_a(t) P_a`, with explicitly listed rational breakpoints and
  coefficients, `|h_a(t)|<=J`, each Pauli term supported on at most k sites,
  and each site incident on at most d active terms;
* the **cut certificate** that, in every time segment and for every tree edge,
  at most c active Hamiltonian terms intersect both `A_e` and `B_e`;
* a rational TTN vector `|Psi_0>` on that tree, with one leaf coordinate
  `C^2 tensor C^{r0}` per physical site, norm one, and maximum virtual bond
  dimension D0. Its physical input is
  `rho_0=Tr_purifying |Psi_0><Psi_0|`.

The rational data are explicit. The norm-one input is a promise which can also
be checked by exact rational TTN contraction. Normalization of a nonzero
supplied vector can instead be done with certified arithmetic and charged
precision; no state-preparation oracle is used. The TTN may be entangled and
need not arise from short-time local preparation.

The physical evolution is exactly

`d rho/dt = -i[H(t),rho] + gamma sum_i (E_i(rho)-rho)`,

`E_i(rho)= I_i/2 tensor Tr_i rho`.

For any rational `0<epsilon<=1/2`, there is a bounded-work classical randomized
algorithm producing x in `{0,1}^n` whose distribution q satisfies

`TV(q, x -> <x|rho_T|x>) <= epsilon`.

Its bit work per sample is polynomial in the complete input length B, n,
D0, the number of schedule segments and epsilon^-1, for every fixed choice of
the class parameters. Numeric T does not have to be paid past its logarithmic
mixing cutoff; only its binary representation and input schedule are scanned.
More informatively, before that cutoff its work has the form

`poly(B,n,M,D0,epsilon^-1) * exp(O(c J T))`.

All constants in this expression depend only on k,d,r0 and the choice of a
standard dense-matrix arithmetic implementation. Consequently the exponent
in the polynomial is `O(1+c J/gamma)` up to universal algorithmic constants.
The theorem does not have a noise-uniform polynomial degree.

A supplied terminal product POVM with a bounded number of outcomes per site
and rational positive effects summing to identity is also allowed. The
maximally mixed branch is sampled from `Tr(M_{i,x})/2`, and in the trajectory
branch the joint physical/purifying TTN distribution is contracted. Conditional outcome weights are
exact rational contractions with the previously chosen local effects; no
minimum-probability promise or local square-root oracle is required.

The strongest unqualified output is total-variation sampling, **not** pointwise
relative error, rare-event probabilities or an explicit density matrix close
in trace norm. Independent repeated samples support additive prediction of
every specified efficiently computable bounded classical function of the
terminal outcomes, including full parity.

#### 4. Proof: global mixing, paid discretization and crossing action

##### 4.1 A self-contained global mixing bound

Let `tau=I/2^n` and `D(rho||tau)=n log 2-S(rho)`. Hamiltonian evolution,
including time-dependent H, has zero entropy derivative. By convexity of
relative entropy, a replacement term satisfies

`Tr[(E_i rho-rho) log rho] <= D(E_i rho||tau)-D(rho||tau)`.

Now

`D(rho||tau)-D(E_i rho||tau)
 = log 2+S(rho_{-i})-S(rho)`.

Strong subadditivity gives the entropy form of Shearer's inequality
`sum_i S(rho_{-i}) >= (n-1)S(rho)`. For completeness, order the sites.
Expand each `S(rho_{-i})` by the entropy chain rule, and use that deleting a
conditioning site can only increase conditional entropy, an immediate form
of strong subadditivity. Each chain-rule term of `S(rho)` appears n-1 times.
Thus

`d D(rho_t||tau)/dt <= -gamma D(rho_t||tau)`.

The full-rank calculation extends to singular inputs by continuity, so

`D(rho_t||tau) <= n log 2 exp(-gamma t)`,

`||rho_t-tau||_1 <= sqrt(2 n log 2) exp(-gamma t/2)`.

Set the integer

`L=ceil(log_2(16(n+1)/epsilon))`.

It is found by integer comparisons, not an exact-real logarithm oracle.
If `gamma T >= 2L`, then the trace distance bound is less than epsilon/16:
use `exp(-L)<=2^-L` and `sqrt(2 n log 2)<=n+1`. Sampling tau therefore
already has TV error less than epsilon/32. This applies to correlated rho_0.

In the remaining branch,

`gamma T<2L`, hence `J T<2gL`.

##### 4.2 Rational channels and a finite uniform noise history

In schedule segment j of duration t_j, let

`S_j = 2 sum_a |h_{a,j}|+2 gamma n`,

`Lambda=sum_j S_j t_j`.

If T=0, sample the input TTN directly. Otherwise gamma>0 makes Lambda>0.
Take

`r_j = max(1, ceil(S_j t_j), ceil(10^6 Lambda S_j t_j/epsilon))`.

Divide segment j into r_j equal rational steps. Replace each Pauli unitary
by the rational Cayley rotation

`U_x=((1-x^2/4)I-i x P)/(1+x^2/4)`, `x=h_{a,j} t_j/r_j`,

and the noise by `(1-gamma h)Id+gamma h E_i`. All are CPTP, and gamma h<=1.
First-order channel telescoping gives an error at most

`40 sum_j (S_j t_j)^2/r_j < epsilon/1000`

in diamond norm. This follows directly by expanding exact local exponentials
to second order, using their diamond norm contraction, bounding the sum of
second-order cross terms by `(S_j h)^2`, and using the Cayley third-order and
Euler second-order remainders when `S_j h<=1`. The displayed factor 40 is
slack. The r_j choice pays the error since

`sum_j (S_j t_j)^2/r_j <= epsilon/(10^6 Lambda) sum_j S_j t_j`.

The total number of time steps is

`R=sum_j r_j <= 2M+2 Lambda+10^6 Lambda^2/epsilon`.

Here M is the number of nonempty schedule segments after cutting at T.
Moreover

`Lambda <= 2 n(dJ+gamma)T <= 4 n(dg+1)L`.

Thus R and the number G of elementary gates/noise choices are polynomial in
n,M,epsilon^-1 at fixed g,d. Exponentially large numeric J or gamma does
not escape the bound: only the paid dimensionless actions occur; their binary
representations are included in B.

Each Euler noise factor is sampled by its rational `I,X,Y,Z` mixture. A fixed
noise history is a unitary circuit on the physical qubits, acting on the
supplied purification. Purifying coordinates are passive representation
coordinates, not a physical reset supply.

##### 4.3 The exact nuclear norm is uniformly bounded on every tree edge

For a unit vector psi, write `N_e(psi)` for the sum of Schmidt coefficients
across `A_e,B_e`, putting each purifying coordinate on its physical site's
side. Initially `N_e(Psi_0)<=sqrt(D0)` by Cauchy--Schwarz.

A crossing rotation changes this norm by at most `exp(|theta|)`, as audited
in Section 2. Its Cayley angle has magnitude
`2|arctan(x/2)|<=|x|`. A noncrossing unitary, in particular any one-site Pauli
noise kick, preserves `N_e` exactly. Therefore, for every history and every
intermediate point,

`N_e(psi_exact) <= sqrt(D0) exp(A_e(T))`,

`A_e(T)=sum_j t_j sum_{a crossing e}|h_{a,j}| <= c J T`.

This is the decisive estimate. There is no factor from the number of Trotter
layers or from the length of a path through the tree. Define

`B_star=2^[ceil(ceil(log_2 D0)/2)+1+ceil(2cJT)]`,

or any larger integer power of two, so that
`B_star>=sqrt(D0)exp(cJT)`. All needed bounds can be chosen by rational
integer arithmetic. In the nontrivial branch,

`B_star <= 4 sqrt(2D0) 2^(4cgL+1)`.

It is polynomial in D0,n,epsilon^-1 for fixed c,g.

#### 5. Constructing and sampling the compressed tree states

##### 5.1 Algorithmic truncation, not an existential ansatz

Applying a Pauli rotation has operator Schmidt rank at most two across each
cut. It has a TTN operator representation of bond at most two on the Steiner
subtree joining its support, and bond one elsewhere. Thus it can be applied
to a TTN of bond D using intermediate bond at most 2D. One-site noise kicks
change only the corresponding leaf tensor.

After each gate, perform a canonical sweep through every tree edge and compress
there. A TTN has exact Schmidt decompositions across its edges: isometric
subtrees reduce the relevant SVD to a local matrix. Replacing the central
Schmidt matrix by a lower-rank approximation changes no other virtual bond.
This is established TTN machinery, credited to Shi--Duan--Vidal and Seitz et al.
It can also be seen directly by contracting all isometric subtrees to the two
sides of the edge. The operations act on at most cubic-size local tensors in D,
not on a `2^n` coefficient matrix.

Let `M_c=100 n(G+1)` bound the number of Schmidt compressions and sweeps, and
put `zeta=epsilon/100`. Choose the target bond cap

`D = ceil((128 M_c B_star/zeta^2)^2)`.

With exact arithmetic, truncating to the largest D Schmidt values increases
the squared error relative to the corresponding exact history vector by at
most `2 B_star/sqrt(D+1)`. All unitary updates preserve the vector error, and
all compressions decrease the approximate norm. Summing the error increments
gives a final vector error less than zeta/2. There is ample slack for finite
arithmetic, discussed next. D is at least D0.

##### 5.2 Finite precision and the absence of an eigenvalue-gap assumption

Input rational contractions have polynomial bit length in B and the number
of contracted TTN nodes: multiplication on an acyclic graph does not create
exponentially long rational numbers. Canonicalization and compression are
done with certified dyadic arithmetic.

There is a small but useful refinement to the usual informal appeal to an
approximate SVD. No gap-free procedure is required to approximate one uniquely
specified exact top-D subspace. Near a tied singular value that requirement
would be inappropriate. It is enough to construct an orthogonal compression
with discarded operator norm at most `2/sqrt(D)` and rank at most `2D`, up
to a paid normwise error nu. Such a compression is obtained by diagonalizing
the local Gram matrix to residual smaller than a chosen multiple of `1/D`
and retaining all directions above the threshold. Since its Frobenius norm
is at most one plus rounding slack, the retained rank is at most a constant
times D. The nuclear/operator-duality proof of Section 2 then applies with
twice the constant. We may use bond cap 4D to absorb these harmless choices.

For each local operation choose normwise arithmetic error

`nu <= zeta^2/[10^5 (M_c+G+1)]`.

Rescale the approximate state by a certified upper bound on its norm whenever
needed, so its norm stays at most one. If both reference and approximation
have norms at most one, a normwise perturbation nu changes their squared
distance by at most `4nu+nu^2`. Summing these increments together with the
compression increments keeps the final vector error below zeta.

Gap-free approximate Hermitian diagonalization, for example Jacobi rotations
until the off-diagonal Frobenius residual is small enough, has polynomial work
in local matrix dimension and log(1/nu). Thresholds may retain ambiguous small
singular directions; they are not inverted. An initial rational TTN can be
canonicalized by the same bottom-up QR/SVD procedure with its actual input
height charged. Large but rational local tensor entries contribute their
binary height, and nearly null directions are discarded with a paid normwise
error. No inverse minimum Schmidt coefficient is part of the contract.

Every local matrix has dimension polynomial in D and `2r0`. A deliberately
loose bit-work envelope per history is

`poly(B,G,n,log(1/nu)) * (1+D0+D)^C`

for a universal constant C, using dense-matrix arithmetic. This is sufficient
for a uniform polynomial. The report makes no claim that this pessimistic
compression rule is useful in practice.

##### 5.3 TV error and bounded random-bit sampling

For each history, let psi be the exact unit history vector and phi its
subnormalized rational TTN approximation with `||phi-psi||<=zeta`.
Normalizing phi changes it by at most zeta in vector norm. Hence the trace
norm distance of the two pure density operators is at most `4zeta`.
Partial trace and the final measurement contract trace distance, so the
conditional output distributions differ in TV by at most `2zeta`.
This estimate is uniform in the noise history. Averaging histories preserves it.

A rational TTN permits exact rational norm contractions and conditional
computational-basis probabilities. One can sample the joint physical and
purifying leaf indices sequentially and discard the purifying results. The
normalization scalar cancels in the conditional ratios; extremely small
nonzero probabilities do not require an inverse-probability accuracy promise.
Their numerators and denominators are rationals of polynomial bit height.

Use finitely many bits for each categorical choice. With at most N_cat
choices, round each rational conditional to a dyadic distribution within
TV `epsilon/(100 N_cat)`. This uses
`O(log(N_cat/epsilon))` bits per choice and adds at most epsilon/100 to
the output TV by sequential coupling. Apply the same convention to the
Euler noise choices. N_cat is polynomial and fixed before the run.

The channel discretization, TTN approximation and both finite-bit sampling
errors together are less than epsilon. All branches have bounded work. There
is no additional Monte Carlo failure probability: TV is a statement about
the sampler's output law. For a subsequent additive prediction with confidence
1-delta, ordinary independent repetitions add the familiar
`O(epsilon^-2 log(1/delta))` factor.

This completes the theorem.

#### 6. Interaction classes, a more general action theorem and hard boundaries

The proof actually gives a **crossing-action theorem without noise**: given a
normalized TTN input and any explicit Pauli circuit or piecewise Hamiltonian,
whole-output sampling has cost polynomial in its explicit circuit size (or,
for a Hamiltonian schedule, also its total numeric generator action Lambda),
desired inverse error and `sqrt(D0) exp(max_e A_e)`. Noise is used only to cap the nontrivial
physical time at `O(gamma^-1 log(n/epsilon))` while contributing no crossing
action in its random-unitary representation.

The cut certificate is efficiently verified from the supplied data: compute
the leaf partition at each tree edge and count the active terms crossing it
in every schedule segment. No treewidth-search oracle is assumed.

Examples with constant c:

* A chain with bounded-range bounded-incidence interactions: use its usual
  MPS cuts or a corresponding binary leaf tree. c depends only on range and
  incidence, not n.
* A fixed-width ladder or cylinder: row ordering gives constant crossing
  count when width is a class parameter.
* A bounded-degree physical tree with finite interaction range: attach a leaf
  for each physical site and split a higher-degree branching tensor into
  binary nodes. A virtual cut separates unions of a bounded number of physical
  branches. Crossing terms touch a bounded-radius neighborhood of the branch
  separator, so their number is bounded by a constant depending only on
  physical degree, interaction range and d. One can simply scan and verify
  the resulting certificate rather than relying on this description.

General square-lattice regions fail the constant-cut hypothesis. A binary
leaf tree has a balanced edge cut, and a full L by L grid has edge boundary
Omega(L) for a balanced vertex partition. Thus the supplied-certificate proof
only offers `exp(O(L JT))` there. This is a limitation of this construction,
not a hardness proof.

The dependence on crossing action is not artificial: r disjoint XX rotations
of angle pi/4 across a specified cut turn a product state into r Bell pairs
and give Schmidt nuclear norm `2^(r/2)`. A different tree may group those
pairs and solve that particular model easily, so this example does **not**
prove an obstruction for every decomposition of every 2D state.

Other boundaries:

* A generic succinct correlated-state circuit cannot replace the supplied TTN.
  At T=0 this would ask for general quantum-circuit output sampling. The TTN
  input is a substantive tractability condition, not arbitrary-state access.
* General nonunital Lindblad noise is not covered. It need not mix to tau or
  admit unitary trajectories with bounded crossing action. Resets supply fresh
  purity, and known fault-tolerant hardness results must not be contradicted
  by silently adding them.
* Arbitrary fast Hamiltonian variation is not a free oracle. The theorem uses
  an explicit finite rational schedule and pays its complete length.
* A polynomial degree independent of J/gamma has not been obtained. The proof
  visibly contains `exp(cJT)` up to the global mixing time.
* A global state-vector approximation on bounded cuts earns a TV sampler;
  original normalized-HS operator compression alone does not. In particular,
  the original 2D local-mean theorem cannot be iterated on exponentially rare
  conditionals to obtain the absent full sampler.



## Proof component 7: Biased sampling, late relative certificates and source repair

Source: [ambitious/SAMPLING_FRONTIER.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/ambitious/SAMPLING_FRONTIER.md), SHA256 `30c19cf5dabd1753c6dec8794074f27a4dd6b9948fff0e8b169d60aee0a07093`.

### Sampling frontier: earned positive regimes, exact obstructions, and the missing 2D operation

8 November 2026. Post-exchange synthesis and derivation. The independently frozen `initial/ambitious.md` is unchanged. Read the dedicated `FINAL_RELATIVE_OBSTRUCTION.md` for complete rare-event proofs. This file confronts the team readout/sampling results, proves two positive transfers for a common faithful product reference, and records a constructive primary-source audit of the Trivedi--Cirac identity/CPTP-event step.

#### 1. Capability map

| Model and task | Strongest operation earned | Exact remaining boundary |
| --- | --- | --- |
| Original arbitrary bounded-local 2D Hamiltonian, product input, every-site unital replacement | All-time additive prediction of every global Hermitian product contraction; team `machinery/FINAL_GLOBAL_READOUT_THEOREM.md` | A scalar additive operation, including tiny probabilities only at additive accuracy |
| Original noise with a supplied constant-cut interaction tree and locally purified TTN input | All-time full-output TV sampler; constructor's frozen report | Generic square-lattice separators do not satisfy the cut promise |
| Original unital noise, arbitrary input and Hamiltonian geometry | Relative operator-order certificate and positive reference sampler after gamma T>=log(4n/eta); constructor's `RELATIVE_MIXING_AND_SAMPLING_OBSTRUCTION.md` | Does not cover earlier times |
| Faithful biased resets, common product reference conserved by H | Principal's all-time fixed-local additive predictor | Whole-block conservation and faithful reference are substantive |
| Same common-reference biased resets on certified bounded-cut architectures | **All-time full-output TV sampler proved by the transfer in Section 3 below** | No arbitrary-2D architecture conclusion; no all-time relative error claimed |
| Same common-reference biased resets, arbitrary geometry and correlated input | **Log-time relative operator mixing and reference sampling proved in Section 2 below** | This is an established-HC consequence, not a new constant-time dequantization theorem |
| Original 2D class, arbitrary positive rational times, relative/log probabilities | Explicit NP=RP consequence if a uniform polynomial evaluator exists | Actual rare-event reduction; not TV hardness or a positive-lower-time result |
| Faithful biased common-reference class, arbitrary positive times, relative/log probabilities | The same obstruction via number-conserving six-body dual-rail blocks | Not TV hardness; static product-input model retained |
| Original generic 2D class, full-output TV at every fixed positive gamma/J and all times | **OPEN / NOT_ACHIEVED** | A positive generative or normalized connected-activity operation is missing |

The two new positive rows combine established mechanisms and preserve credit: the constructor supplied the tree sampler and relative-mixing architecture; the principal supplied the faithful-reference structure and reset-register dilation; generalized weighted hypercontractivity is imported from primary literature. No first-priority, practical runtime, physical advantage or complete implementation claim is made.

#### 2. A relative operator mixing theorem for the faithful biased reference

##### 2.1 Formal statement

Let sigma=diag(p,1-p), 0<p<1, mu=min(p,1-p)>0, and Sigma=sigma^(tensor n). Consider

    d rho/dt=-i[H(t),rho]+gamma sum_i(R_i^sigma(rho)-rho),
    R_i^sigma(rho)=sigma_i tensor Tr_i(rho),
    [H(t),Sigma]=0.

The initial density matrix may be arbitrary and correlated. This bound needs neither spatial locality nor per-block conservation; global commutation on every time interval suffices. In algorithmic use the rate, reference and a finite piecewise rational Hamiltonian schedule are explicitly supplied, with their bits charged.

Define

    a_sigma=(1-2mu)/log(mu^-1-1), a_sigma=1/2 at mu=1/2,
    c_sigma=8 a_sigma/(3 log 2)>0,
    C_mu=mu^-1 sqrt(mu^-2-1)<mu^-2.

For gamma T>=(2/c_sigma)log n,

    ||Sigma^-1/2 rho_T Sigma^-1/2-I||_infty
      <= C_mu n^(2/c_sigma) exp(-gamma T).               (1)

In particular the condition

    gamma T >= (2/c_sigma)log n+log(mu^-2/eta),
    0<eta<=1/2,

implies simultaneously

    (1-eta)Sigma <= rho_T <= (1+eta)Sigma.               (2)

This is a full operator-order assertion. Consequently every positive measurement effect M satisfies

    (1-eta)Tr(M Sigma)<=Tr(M rho_T)<=(1+eta)Tr(M Sigma).  (3)

It earns actual log marginals and relative reference sampling, not just additive expectation values. At the maximally mixed point the constructor's sharper King constant gives its better 4n exp(-gamma T) bound; the conservative weighted constant here is chosen to match the verified import and cover all biases.

##### 2.2 Exact import and actual-channel applicability

Dong--Gao--Ou--Yao--Zhou, arXiv:2606.17729v1, Theorem 1.1, applies to every operator on tensor powers of a fixed faithful reference and supplies

    ||Delta_[sigma,exp(-gamma s)]^(tensor n)(A)||_(q,Sigma)
       <=||A||_(p,Sigma)

when q-1<=exp(c_sigma gamma s)(p-1). The weighted norm is

    ||A||_(p,Sigma)=||Sigma^(1/(2p)) A Sigma^(1/(2p))||_p.

The paper credits Beigi--Datta--Rouze for the earlier exact qubit tensorization; this credit is retained. The primary statement and norm convention were checked directly at [arXiv:2606.17729v1, Theorem 1.1](https://arxiv.org/html/2606.17729v1). This is the only non-elementary import in this section.

Conjugation by a unitary commuting with Sigma is an isometry at every displayed exponent. Interleaving the actual Hamiltonian evolution with the reset semigroup, allowing the exponent to grow at rate c_sigma gamma, and taking the product limit proves the same hypercontractive bound on every actual chronological interval. No reset is commuted through H. Sign reversal of H makes no difference to this applicability.

##### 2.3 Relative density and the three-interval proof

Put Q_t=Sigma^-1/2 rho_t Sigma^-1/2. Direct calculation, using [H,Sigma]=0, gives

    d Q/dt=-i[H(t),Q]+gamma sum_i(F_i(Q)-Q),
    F_i(Q)=I_i tensor Tr_i(sigma_i Q).

Thus Q evolves under a unital generalized-depolarizing channel with the same reference and the opposite Hamiltonian sign from the usual Heisenberg convention. It is positive and Tr(Sigma Q)=1. The F_i are weighted-L2 orthogonal conditional expectations. Their tensor-product eigenbasis has eigenvalue -gamma r on a product containing r reference-mean-zero factors. The Hamiltonian is skew-adjoint for the weighted L2 inner product. Therefore every reference-mean-zero A obeys

    ||V_{[v,u]}(A)||_(2,Sigma)<=exp[-gamma(v-u)]||A||_(2,Sigma). (4)

For n>=1 choose the first and last interval lengths

    s=log n/(c_sigma gamma),

with s=0 for n=1. Let p_in=1+1/n and q_out=n+1. Since rho_0 is positive of trace one,

    ||Q_0||_(p_in,Sigma)
      =||Sigma^[-(p_in-1)/(2p_in)] rho_0
                     Sigma^[-(p_in-1)/(2p_in)]||_(p_in)
      <=mu^[-n(p_in-1)/p_in] ||rho_0||_(p_in)
      <=mu^[-n/(n+1)]<mu^-1.

Here ordinary Schatten ideal inequalities and ||rho_0||_p<=1 suffice; no input representation or additional entropy theorem is needed. Initial weighted HC maps p_in to 2 in time s. Since Q_s has weighted mean one,

    ||Q_s-I||_(2,Sigma)^2=||Q_s||_(2,Sigma)^2-1<mu^-2-1.

On the middle interval of length T-2s apply (4). On the last interval apply 2-to-q_out HC. Finally

    ||A||_infty<=mu^(-n/q_out)||A||_(q_out,Sigma)<mu^-1||A||_(q_out,Sigma).

Combining gives (1), including arbitrary time ordering and arbitrary-rank correlated input. Congruence by Sigma^1/2 then proves (2)--(3).

##### 2.4 Finite-bit log computation and sampling

No exact logarithm is needed for the cutoff. One can use a positive rational c0<=c_sigma. For example **c0=mu works**: log x<=x-1 with x=(1-mu)/mu gives a_sigma>=mu, and 8/(3 log 2)>1. Hence the sufficient rational test

    gamma T >= (2/mu) ceil(log_2 n)
                    +ceil(log_2(mu^-2/eta))              (5)

certifies (2). Integer comparisons produce the ceilings; all scalar input bits are paid. Sharper certified c0 is optional.

For computational outcomes, the reference probability is

    P_Sigma(x_S)=product_[i in S] sigma_[x_i,x_i].

Return sum_i log sigma_[x_i,x_i], computed with certified scalar error, as the log-marginal approximation. Equation (3) bounds the dynamical log discrepancy by -log(1-eta)<=2eta, regardless of how small that marginal is. Log conditionals follow by subtracting two log marginals; reference nonzero probabilities are guaranteed by mu>0.

Sample the product reference law. With exact reference coins its pointwise error relative to P_rho is at most eta/(1-eta), and its TV error is at most eta/2, directly from (3); no factor n from sequential conditionals is introduced. Bounded random-bit sampling is also paid: approximate each rational local coin multiplicatively to O(eta/n). Since p,1-p>=mu, O(log(n/(eta mu))) bits per coin suffice. The resulting full product law incurs a further exp(O(eta)) pointwise factor. A prescribed product POVM is treated by its rational reference weights Tr(M_i,x sigma). If a positive weight is tiny, its binary rational height is part of the input, so multiplicative rounding needs only its paid bit length plus log(n/eta); zero effects have zero weight under both states and can be omitted.

This theorem is a rigorous stronger end branch for the faithful-reference model. Its logarithmic time is natural for approximation by the reference: already at H=0 a product of biased one-site residuals can retain an O(n exp(-gamma T)) pointwise likelihood ratio. It is not the sought constant-physical-time polymer theorem and does not resolve earlier TV sampling.

#### 3. All-time full TV sampling with faithful biased resets on bounded cuts

##### 3.1 The earned transfer

Fix local block size k, incidence d, constant cut bound c, initial local purification dimension r0, a faithful rational sigma and a ratio upper bound g>=J/gamma. Supply:

- n physical qubits and a labelled binary leaf tree with O(n) nodes;
- an explicit piecewise rational Hamiltonian schedule H(t)=sum_b H_b(t), with support size <=k, norm <=J, site incidence <=d, and at most c active blocks crossing any tree-edge partition;
- a rational normalized locally purified TTN input of maximum virtual bond D0 on the same tree;
- a positive rational rate gamma and final time T, and a terminal product POVM with bounded local outcome count and rational effects.

Assume [H(t),sigma^(tensor n)]=0 on every segment. The principal's stronger per-block conservation promise is sufficient, but not needed for this transfer: only the exact entropy/mixing argument uses conservation, whereas the numerical trajectory approximation is directly charged in trace norm.

**Theorem C.** The complete terminal distribution has a bounded-work randomized classical sampler of TV error epsilon, with work polynomial in complete input bits B, n, number of schedule segments, D0 and 1/epsilon at each fixed set of these class parameters. Before the entropy cutoff, a more informative work bound has the form

    poly(B,n,M,D0,1/epsilon,2^K) exp(O(2^k cJT)),
    K=O(gamma T+log(n/epsilon)).                         (6)

At the only simulated times gamma T=O_mu(log(n/epsilon)), this is polynomial. This proves a genuine all-time nonunital full-output sampling operation on the restricted architecture. It does not promote generic 2D product-readout prediction into a sampler.

##### 3.2 Mixing branch with no hidden reservoir resource

For Sigma=sigma^(tensor n), Hamiltonian evolution contributes zero to the derivative of D(rho||Sigma). Convexity of relative entropy bounds the ith reset contribution by

    gamma[D(R_i^sigma rho||Sigma)-D(rho||Sigma)].

The entropy chain rule/strong subadditivity gives

    sum_i S(rho_-i)>=(n-1)S(rho).

Using D(R_i^sigma rho||Sigma)=D(rho_-i||Sigma_-i), it follows that the sum of the reset entropy drops is at least D(rho||Sigma). Consequently

    D(rho_T||Sigma)<=n log(mu^-1) exp(-gamma T),
    ||rho_T-Sigma||_1<=sqrt(2n log(mu^-1)) exp(-gamma T/2). (7)

This holds for arbitrary correlated input, including the supplied TTN. With

    L=ceil(log_2(64(n+1)/(mu epsilon))),

the rational test gamma T>=4L makes the trace error much smaller than epsilon/100; use log(mu^-1)<=mu^-1 and e^-L<=2^-L. Sample the known product reference on this branch. Otherwise gamma T<4L and JT<4gL. Faithfulness and conservation are real mathematical resources; an arbitrary cooling bath or nonconserving driven H does not satisfy (7).

##### 3.3 Paid finite reference and actual reset dilation

Expand each fixed-size rational H_b into at most 4^k Pauli terms. Its Pauli coefficient one-norm is at most 2^k||H_b||<=2^k J. A first-order colored/rational Cayley approximation, interleaved with the positive Euler reset

    (1-gamma h)Id+gamma h R_i^sigma,

has global diamond error <=epsilon/100 with polynomially many steps. The constructor's segmentwise choice r_j=max(1,ceil(A_j),ceil(C A_tot A_j/epsilon)), with A_j the paid local diamond-norm action on segment j, yields total steps O(M+A_tot+A_tot^2/epsilon). Here A_tot<=C_k n(dJ+gamma)T, so only polynomial physical action enters before the cutoff. No inverse minimum segment length is charged.

Sample an Euler reset event with probability gamma h. Conditional on such an event, sample a bit a from p,1-p, introduce |a> at the same spatial leaf, SWAP it with the physical qubit and **keep the old register** as a passive coordinate. Tracing that register gives exactly R_i^sigma; keeping it makes the trajectory unitary. Initial correlations are supplied by the known TTN purification. This is a numerical representation of the stipulated physical noise, not a physical supply of clean qubits or a bath-outcome oracle.

##### 3.4 Deterministic leaf-dimension cap

The reset count S_i at a physical site is a sum of independent Bernoulli variables with mean lambda_i=gamma T. Its count, not the number of time steps, controls the retained-register dimension. Since

    E exp(S_i)<=exp[(e-1)lambda_i],

Markov's inequality gives

    Pr[S_i>=2lambda_i+u]<=exp(-u),

because e-1<2. Choose

    K=ceil(2gamma T)+ceil(log_2(100n/epsilon)).            (8)

The probability that any site exceeds K is at most epsilon/100. Stop and return a fixed output on such a history. This incurs TV error at most the exceptional probability and has bounded work; there is no rejection/termination assumption. At most K reset registers need ever be allocated at each leaf. Its local Hilbert dimension is at most

    q_leaf<=2 r0 2^K=poly_mu(n/epsilon)

in the simulated branch. Preallocating K local slots makes this dimension bound deterministic. Local SWAPs and bit preparations cost no spatial crossing action.

##### 3.5 Crossing action, constructive TTN and output sampling

Across any supplied tree cut, the initial purification has Schmidt nuclear norm <=sqrt(D0). A crossing Pauli rotation grows this norm by at most exp(|theta|), and all on-leaf reset SWAPs preserve it. Pauli expansion of the at-most-c crossing blocks therefore gives, at every intermediate point and for every capped history,

    N_e(psi_exact)<=B_star=sqrt(D0)exp(2^k cJT).           (9)

After at most M_c=100n(G+1) paid tree-edge compressions, the original nuclear/operator-duality estimate gives vector error at most zeta using

    D>=ceil((16 M_c B_star/zeta^2)^2).

The constructor's compatible-tree canonicalization and gap-free approximate SVD implementation apply with local dimension q_leaf included in every dense matrix cost. All gates, tensor entries, norms, sweeps and rounding bits are polynomially paid. Set zeta=epsilon/100. Normalize the nonzero approximate trajectory vector; its norm differs from one by at most zeta, so the resulting trajectory density matrix differs from the exact one by trace norm O(zeta). The full terminal product-POVM law can then be sampled by exact rational TTN contractions and finite-bit categorical choices, whose summed TV error is separately <=epsilon/100.

Average the trace/measurement error over the digitally sampled histories and include the explicit exceptional-count and channel-reference errors. All total errors are below epsilon with the displayed slack. This proves Theorem C. The actual sampler produces one TTN history per sample; it does not output an exponentially large density matrix or enumerate all noise histories.

This is a transfer of the principal's reset-register representation into the constructor's paid tree algorithm. Ordinary unital histories needed no growing register dimension; equation (8) is the additional operation making this nonunital extension finite and polynomial. A practical implementation at these worst-case bounds has not been performed.

#### 4. The conservation condition does not remove relative early-time hardness

`FINAL_RELATIVE_OBSTRUCTION.md`, Section 8, supplies a complete static counterpressure at every fixed bias 0<p<1 and gamma>0. Encode each logical bit in the physical product pair |10>,|01>, with exchange F_i=(XX+YY)/2, and use H=sum_tromino product_i F_i. Every six-body block commutes with the faithful product reference; all blocks commute with each other. The target rare probability again has leading coefficient q_tilings^2 at T^(2n/3), and biased resets enter only at higher order. The same polynomial-bit dyadic time gives an NP=RP consequence for an all-time relative/log evaluator.

Thus faithful conservation supports the positive theorems above but cannot justify a uniform relative evaluator at all arbitrarily short times. This is compatible with both Theorem C's TV task and the logarithmic-time relative branch. Six exact cases of the encoded leading coefficient passed at p=1/3,4/5 and gamma=1,7, with up to twelve physical qubits (`AUDIT_DUALRAIL.json`).

#### 5. The remaining generic 2D TV operation

The all-support product-readout theorem is materially stronger than the original fixed-local mean theorem. It still supplies a single bounded mean per call. The constructor's noisy-linear-code construction demonstrates why inverse-polynomial additive answers for every product contraction do not by themselves determine a general law in TV: all such means may be exponentially indistinguishable while the laws are nearly disjoint. That is an oracle/interface obstruction, not a target-class hardness construction.

The original parity-strip estimator is a bounded overlap estimator between two efficiently represented states with different strip orders. Its normalization is appropriate for a scalar inner product. It has not become a positive sequential distribution or a trace-norm global state representation. The bounded-cut theorem can retain the entire state because each cut has only constant crossing action; generic square-lattice cuts can have extensive boundaries. The biased reset registers resolve nonunital noise representation but do not remove this spatial obstruction.

The strongest circuit comparator remains Nelson et al., arXiv:2610.00548v2, Theorem 2.3 and Proposition 2.2: fixed-strength noisy geometric circuit layers above a p-dependent depth have an FPTAS for arbitrary log marginals and relative sampling. Its critical physical-time threshold and degree diverge under p proportional to gamma h as h->0. A direct Trotter import is therefore unearned.

A viable continuous repair must bound **connected activities and their relative normalization** uniformly in the fine time step, or provide an independently positive global sampler whose total error is controlled before conditioning. Factorial spatial tails may be inserted as additional interaction activities, but an absolute tail estimate cannot simply be divided by an exponentially small prefix mass. Theorem A proves that a purported zero-free/log expansion valid down to every positive T in the full original class would encounter an actual complexity obstruction. A later-time constant-physical-threshold result remains possible; a TV-only early-time completion would be a different required operation.

No theorem here closes that generic 2D interval.

#### 6. Trivedi--Cirac: exact published source check and constructive repair boundary

##### 6.1 What was actually checked

Published primary: R. Trivedi and J. I. Cirac, *Transitions in Computational Complexity of Continuous-Time Local Open Quantum Dynamics*, Phys. Rev. Lett. 129, 260405 (22 December 2022), DOI [10.1103/PhysRevLett.129.260405](https://doi.org/10.1103/PhysRevLett.129.260405). The article's Theorem 1 is the high-noise TV sampling claim; its Hamiltonian low-noise hardness uses biased/nonunital channels. The arXiv version has the earlier title *Simulability transitions in continuous-time dynamics of local open quantum systems*.

The published [main PDF](https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.129.260405), pp. 2--3, repeats the identity-versus-other-channel rare-horizontal-event step. The journal's actual linked [supplement_final.pdf](https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.129.260405/supplement_final.pdf), Problem 1, pp. 3--4, admits arbitrary bounded local Lindbladians and product input; Lemma 3 on p. 4 asserts a fixed-rate identity/CPTP decomposition using Id+L/g. The published supplement retains the CP assertion found on p. 8 of arXiv:2110.10638v2. No assumption there excludes a purely Hamiltonian local term. These pages were read through the web PDF tool; direct local retrieval returned HTTP403, so a local hash of the published PDFs is not claimed. The arXiv primary bytes remain pinned locally.

##### 6.2 Exact failed ingredient

For the one-qubit generator L=-i[Z,.], the Choi matrix of Id+L/g compressed to the orthonormal vectors |Omega> and (Z tensor I)|Omega> is

    [[1, i/g],[-i/g,0]],

whose determinant is -1/g^2. It is not positive for any finite g>0. If

    exp(hL)=(1-gh)Id+gh Phi_h+O(h^2)

with Phi_h CPTP and g fixed, rearrangement forces Phi_h->Id+L/g. Closedness of the CPTP cone contradicts this Choi matrix. Thus allowing an h-dependent event channel does not rescue the stated first-order approximation.

For a multi-site Pauli P of weight at least two, adding arbitrary one-site replacement noise leaves the P-P Choi diagonal zero and the I-P off-diagonal nonzero. The same negative determinant persists. This is why one cannot repair this particular finite-event-rate shortcut by silently allocating more of the original single-site noise.

These exact counterexamples invalidate the displayed proof ingredient. They are **not counterexamples to the high-noise sampling conclusion**. A different valid representation could establish that conclusion.

##### 6.3 A necessary-and-sufficient finite-rate condition

There is a precise constructive replacement for the false general assertion. For a finite-dimensional Lindblad generator, write its normalized Choi operator relative to |Omega> plus its orthogonal complement as

    J_L=[[a,b^dagger],[b,C]].

For a Lindblad generator C>=0 (conditional complete positivity). Then

    Id+L/g is CPTP for some finite g>0

if and only if

    b belongs to Range(C).                              (10)

Indeed multiplication of its Choi operator by positive g gives

    [[g+a,b^dagger],[b,C]],

and the generalized Schur complement criterion is exactly

    C>=0, b in Range(C), g+a>=b^dagger C^+ b.             (11)

Trace preservation is automatic. When (10) holds, choose g exceeding the final scalar bound; this gives the genuine Poisson generator L=g(Phi-Id), Phi CPTP. To recover the source's **uniform** algorithmic hypothesis, one must additionally bound that g by a constant multiple of the declared local interaction strength and pay computation of Phi. A finite g with an arbitrarily tiny positive eigenvalue of C is not a uniform O(J) rate.

Pure Hamiltonian drift has C=0,b!=0 and fails (10). A multi-site Hamiltonian plus only one-site Pauli dissipators also fails: the Hamiltonian vector lies outside the one-site dissipative jump span. Full-support dissipative noise with a quantitative lower Choi bound can satisfy (10), but imposing it changes the physical model. For example -ih[P,.]+kappa(Ad_P-Id) admits the condition g>=kappa+h^2/kappa for kappa>0. This is an illustrative valid subclass, not an added control or an import into the original single-site-only experiment.

##### 6.4 A CPTP short-time repair which retains the unpaid coherent drift

Ordinary first-order CPTP discretization is always available. For

    L=-i[H,.]+sum_alpha(V_alpha . V_alpha^dagger
                         -(1/2){V_alpha^dagger V_alpha,.}),
    Q=sum_alpha V_alpha^dagger V_alpha,

choose h||Q||<=1 and Kraus operators

    K0=exp(-ihH)sqrt(I-hQ), K_alpha=sqrt(h)V_alpha.

Their squared norms sum exactly to I, and their channel is Id+hL+O(h^2). Fixed local dimension makes the matrix arithmetic and its precision payable. For the original Pauli Hamiltonian plus reset, the team's rational Cayley/Euler split is simpler and already supplies a valid CPTP reference.

This repair does **not** produce the needed rare-horizontal-event percolation: the no-jump K0 generally carries a coherent entangling drift at every time step. Replacing it by identity would return to the invalid assertion. Therefore the following accounting is retained: valid finite CPTP discretization achieved; the printed fixed-rate ingredient disproved; no completed replacement proof of the source's general high-noise percolation theorem supplied here; no claim that the high-noise conclusion is false.

#### 7. Final scope and artifacts

The strongest additional positive operation from this follow-up is the common-reference nonunital **all-time bounded-cut TV sampler**, plus the faithful-reference **relative logarithmic-time end branch**. The strongest negative operation is an actual finite-bit NP reduction for uniform rare probabilities, including the new number-conserving biased-reset encoding. Generic 2D all-time TV sampling remains open.

Supporting new objects are `FINAL_RELATIVE_OBSTRUCTION.md`, `audit_dualrail.py`, `AUDIT_DUALRAIL.json`, and the current source/result manifest. Earlier exact Taylor and Choi checks remain preserved. All algorithmic theorems are mathematical derivations; no implementation at the huge general bounds or practical benchmark has been performed. The initial independent report, Gibbs artifacts, other researchers' files and published manuscript bytes remain unchanged.


## Proof component 8: Acquired local prediction and complete uncertainty

Source: [principal/LOCAL_ROBUST_PREDICTION.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/principal/LOCAL_ROBUST_PREDICTION.md), SHA256 `ba582aa5790acc1838e01604174c26b870075cc540e519ef1844a48a27d9541c`.

### Local relaxation, controlled reuse, and a learned quantum predictor

Principal derivation. This follows the frozen independent report
`initial/principal.md`; later reviews and corrections will be recorded separately.
The original prediction theorem is capital at its exact product-input, 2D,
replacement-noise, additive-local-mean scope. This file does not claim priority
for rapid-mixing stability or local generator learning.

#### 1. Physical and numerical class

A finite subset of the square lattice carries qubits. A supplied dictionary of
nonidentity Hermitian Pauli strings has support size at most k, diameter at most
a >= 1, and at most d strings incident on any site. The unknown drift is
H_0=sum_P h_P P, |h_P|<=J_0. Known, prescribed coherent controls H_c(t) are
piecewise constant with rational switching times and coefficients. Their full
description is paid. The total Hamiltonian has fixed bounds a,k,d,J throughout.
The noise is gamma sum_i(E_i-Id), gamma>0 rational or supplied by a paid certified
evaluation algorithm. There are no measurements, resets, cooling steps, fresh
physical ancillas, or control dependent on unobserved quantum measurement records
in a permitted prediction query. The state supplied for a query is a rational
product state; its actual independent local preparation may have declared error.
The readout has at most w sites and operator norm <=1.

First establish analytic estimates for arbitrary measurable bounded controls;
only the finite rational description is an algorithmic claim. A class parameter
is g=J/gamma. Every constant below is independent of lattice volume, horizon,
number of switches, source state, and the particular allowed drive.

Write Phi_{s,t} for the Heisenberg propagator, tau for normalized trace, and u=t-s.
Assume the usual local truncation estimate, verified from the original linked
interaction argument or Barthel--Kliesch Theorem 2:

    ||Phi_{s,t}(O)-Phi^R_{s,t}(O)|| <= K exp(Vu-R/(2a)),       (1)

where Phi^R keeps terms inside the radius-R union of balls around supp(O).
K>=1 and V>0 are explicit fixed-locality constants; enlarging them is harmless.
Their time-dependent applicability uses time-ordered integrals and the uniform
local-strength bound, not time translation invariance. Terms on the boundary
are discarded, all replacement noise on retained sites remains, and tau(O)
is unchanged. The site count is <=w(2R+1)^2. Constants from the original report
are one conservative choice; a verified larger choice from the general local
Lindblad bound is equally valid.

#### 2. Entropy contraction without a Hamiltonian restriction

For an m-qubit density matrix let D(rho)=m log 2-S(rho). Convexity of relative
entropy gives the upper directional derivative

    dD(rho)[E_i rho-rho] <= D(E_i rho)-D(rho).

Furthermore D(E_i rho)=D(rho_{-i} || I/2^(m-1)). Quantum Shearer, obtained by
repeated strong subadditivity, says sum_i S(rho_{-i}) >= (m-1)S(rho).
Consequently

    sum_i [D(rho)-D(E_i rho)] >= D(rho).

The Hamiltonian directional derivative is zero. At variable Hamiltonian and
constant replacement rate, dD/dt<=-gamma D. Boundary density matrices follow by
regularization or integration of the finite-dimensional completely positive
evolution. Hence, for every initial density matrix, correlated or not,

    ||rho_u-I/2^m||_1 <= sqrt(2m log 2) exp(-gamma u/2).       (2)

Only (2), not a computable representation of that arbitrary correlated state,
is used below.

#### 3. Volume-independent local relaxation

Set x=gamma u, v=V/gamma, and choose integers

    r0 >= 2a(log K+1)+a+3,
    r1 >= 2a(v+2)+2,
    R(x)=ceil(r0+r1 x).

The logarithm can be upper bounded by an integer binary logarithm. Equation (1)
is at most exp(-2x). Equation (2), applied to the restricted evolution for
every reduced source density matrix, implies an OPERATOR norm bound. Thus

    ||Phi_{s,t}(O)-tau(O) I||
      <= exp(-2x)+sqrt(2w log 2)(2R(x)+1) exp(-x/2)
      <= A(1+x) exp(-x/2),                                  (3)

where, for example,

    A=1+2w[2(r0+r1+1)+1]

is valid. One may replace the right side by its minimum with 2. This bound
holds for every finite volume and every s,t, including arbitrary unknown
initial states. It is local relaxation, not global trace-distance mixing.

An integer X_e=O(log(A/epsilon)+1) with A(1+X_e)exp(-X_e/2)<=epsilon exists
and can be found by integer doubling plus certified scalar evaluation. For
gamma T>=X_e, return tau(O). For all other times, (1) localizes a query to
O_g(log^2(2/epsilon)) sites, independent of total system size. The input still
has to be read or accessed through a paid index. Infinite time does not replace
finite time or require reading exponentially many digits of T.

#### 4. Uniform perturbation theorem, including nonunital errors

Let G'_t=G_t+sum_z B_{z,t}. Assign each perturbation support a lattice center z;
it has diameter <=a_e and at most q perturbation terms have any one center.
Assume B_z(I)=0 and ||B_z||_(infty->infty)<=eta, uniformly in t. A completely
bounded norm bound is sufficient. The total G'_t must generate physical CPTP
Schrodinger evolution. Its terms need not separately be Lindblad; G'_t need
not preserve the maximally mixed state. Both comparisons use the same initial
source and same control. This theorem is an explicit version of the established
local rapid-mixing stability mechanism, extended here by its proof to bounded
nonautonomous reference drives.

For distance r(z,supp O)<=R(x)+a_e+1, there are at most

    N0(1+x)^2 terms,
    N0=q w [2(r0+r1+a_e+2)+1]^2.

Since B_z(I)=0, (3) bounds their total contribution to
sum_z ||B_z Phi_{t-u,t}(O)|| by eta N0 A(1+x)^3 exp(-x/2).

For a far term, truncate the reference observable to a neighborhood disjoint
from its support. B_z annihilates that truncated observable. By (1) its
contribution is bounded by eta K exp(vx-(r-a_e-1)/(2a)). Square-lattice shells
have <=16w(r+1) centers, before multiplying by q. The geometric series and
(1-exp(-1/(2a)))^-1<=3a imply a far contribution at most

    eta B(1+x) exp(-2x),
    B=16wq[3a(r0+r1+a_e+4)+9a^2].

The harmless extra units cover noninteger radii and choice of support center.
Increase B if a different lattice metric convention is used. Define

    K_stab=158 N0 A+B.                                      (4)

Indeed integral_0^infty (1+x)^3 exp(-x/2) dx=158 and
integral_0^infty (1+x)exp(-2x) dx=3/4. Duhamel, with perturbed evolution on
the outside and reference future evolution next to B_z, gives

    ||Phi'_{s,t}(O)-Phi_{s,t}(O)||
       <= int_0^u sum_z ||B_{z,t-r} Phi_{t-r,t}(O)|| dr
       <= K_stab eta/gamma.                                (5)

All outer propagators are contractions because the total perturbed evolution
is physical. No perturbed mixing assumption, smallness assumption, or global
sum of perturbation norms is needed. For large eta the bound is simply vacuous.
This is NOT an arbitrary-precision simulation of the nonunital system: (5)
provides an accuracy floor. Global sampling and decoded macroscopic information
are not controlled by a fixed-local O estimate.

#### 5. Independent product-preparation error

For two product sources with max_i ||rho_i-sigma_i||_1<=zeta, telescope one
site at a time. Each single-site difference annihilates identity, so the same
near/far argument, now for ||Phi(O)-E_i Phi(O)||<=2 times the relevant bound,
applies without a time integral. For q=1,a_e=0 define N0,B as above and

    K_prep=2(216 N0 A+B).

The elementary maxima sup_(x>=0)(1+x)^3exp(-x/2)<=216 and
sup_(x>=0)(1+x)exp(-2x)<=1 give

    |Tr[(rho-sigma) Phi_{0,T}(O)]|<=K_prep zeta,              (6)

uniformly in n,T and allowed controls. This says nothing comparable about
arbitrary correlated preparation errors known only through one-site marginals.

#### 6. Nonautonomous extension of the original classical algorithm

This uses the checked original buffer construction and is not a new replacement
for it. The altered logical order is essential.

At gamma T<X_e localize to m=O_g(log^2(2/epsilon)) sites. Let
s=ceil(log_2(2m))/(2gamma). If T<s, compute the whole short buffer. Otherwise:

1. Propagate O backward through the LATER interval [s,T], using sequential
   complete noisy Pauli blocks, exact rational Cayley rotations, positive Euler
   replacement maps, merging and coefficient truncation. Local coefficient-p
   contractivity is independent of the signs and time order of coefficients.
   Obtain B0 with normalized HS error eta_s.
2. Apply the EARLY-interval channel Phi_{0,s} to that error. King's Corollary 2,
   interleaved with changing Hamiltonian Schatten-norm isometries, gives
   ||Phi_{0,s}(error)||_infty<=2 eta_s. No channels are commuted.
3. Evaluate the weighted early-buffer Pauli functionals on the supplied product
   input by the original parity-strip construction. Its trajectories already
   have piecewise time-dependent sign-toggled Hamiltonians. Factorial locality
   and accumulated cross-cut angle bounds depend on physical duration and
   local strength, rather than number of switches.

Partition numerical steps at supplied switch times. If interval lengths are
Delta_j and the restricted generator-norm budget is S0, choose

    r_j=max(1,ceil(C S0^2 Delta_j T/eta_s),ceil(S0 Delta_j)).

The sum is <=number_intervals+C S0^2 T^2/eta_s+S0T up to constant factors.
Tiny intervals do not cause inverse-minimum-step cost. Forward and reversed
strip evolutions use the actual supplied chronology. Sampling, tensor
truncation, approximate SVD, dyadic arithmetic and all sparse coefficients
retain the original paid error budgets with an extra polynomial factor in
the control description length.

It follows that at fixed local parameters and g there is a randomized classical
predictor with work poly_g(B_query,1/epsilon,log(1/delta)), where B_query includes
the binary description of T and every control switch and rational product input.
After paid indexing, the many-body computation touches only the stated local
neighborhood. A conservative envelope may enlarge the original exponent
D_kappa=2^80 kappa^40 to 2^100(2+kappa)^60. This is not a useful practical bound.
No claim of polynomiality at g growing with input length is made. The stronger
binary-horizon statement uses (3) before any numerical dynamics is run.

#### 7. A completely specified noisy local acquisition protocol

Here gamma and the dictionary are known. Learning them is not needed for the
claim; a known bounded-range dictionary can include zero unknown coefficients.
Let Mpar be its number of distinct nonidentity strings, no duplicate terms.

For each P choose a one-site Q anticommuting with P and put R=i P Q, including
its sign. Then i[P,Q]=2R, and Pauli orthogonality gives

    tau(R GQ)=2h_P,   tau(RQ)=0.                            (7)

On supp(R), prepare independent noisy local eigenstates
(I+sigma_i p_i R_i)/2, with uniform known signs sigma_i and known p_i>=p0>0.
Outside supp(R), prepare I/2, for example by a uniform mixture of the same
symmetric noisy opposite-eigenstate preparations. All physical preparations
are independent products. Their average is I/2 at every site. Signed averaging
multiplied by the product of signs yields (product p_i)R/2^n. A binary noisy
measurement of Q has calibrated conditional mean b_Q+c_Q <Q>, c_Q>=c0>0.
For each shot, weight (Y-b_Q)/c_Q by product sigma_i and divide by product p_i.
This gives a bounded score |Z|<=A_acc=2/(c0 p0^k), and

    E Z(t)=tau(R Phi_{0,t}(Q)).

The sign of R is included in the score. This protocol requires no entangled
probe, inverse dynamics, source-copy oracle, or future target experiment.
The drift is constant during acquisition and controls are off.

Let Gamma=2dJ_0+2gamma, C2=k Gamma^2. Each term in GQ has support <=k, and
local generator norms give ||G^2 Q||<=C2. The Taylor remainder is bounded by
C2 t^2/2, since e^(tG) is an operator-norm contraction. Therefore

    |E Z(t)/(2t)-h_P|<=C2 t/4.                              (8)

Choose target coefficient error alpha, the rational interrogation time
t=min(1/(4Gamma),alpha/(4C2)), and

    M>=8 A_acc^2/(t^2 alpha^2) log(2 Mpar/delta_acq)           (9)

independent shots per coefficient. Hoeffding and a union bound give simultaneous
coefficient accuracy alpha with ample budget slack. Round to rational precision
<=alpha/8 and clip to [-J_0,J_0]; clipping cannot worsen error to a true coefficient
in that interval. This is a deliberately suboptimal alpha^-4 learner. The stronger
alpha^-2, up to logarithms, learning machinery of Mobus--Bergamaschi--Franca--Rouze
Theorem 4.5 is credited separately, not claimed invented here.

Operational calibration error: if the corrected mean E Z has an independently
warranted systematic error <=beta, it contributes beta/(2t). If evolution-time
error is <=Delta_t, the additional contribution is <=Gamma Delta_t/(2t).
For example beta<=alpha t/8 and Gamma Delta_t<=alpha t/8 fit the error budget.
Calibration is an explicit paid input: include C_cal(beta,delta_cal), the number
and cost of trusted calibration experiments, and required timing precision.
With exact known primitive noise parameters C_cal is zero by the access contract;
with unknown SPAM no unconditional identifiability is asserted. Repetition does
not remove an unknown fixed bias, and the theorem reports its floor if larger.

Nshots=Mpar M. At most n local preparations, one evolution of duration t, and
one single-site readout are used per shot. A conservative sequential account is
n Nshots local preparation operations, Nshots readouts, and source-evolution time
Nshots t, plus paid calibration/reset/repetition infrastructure. Streaming the
scores requires O(Mpar log M + Mpar log(1/alpha)) bits beyond the input and
calibration descriptions; rational arithmetic and preprocessing are polynomial
in these quantities and supplied bit lengths. No wall-clock or energy advantage
over a better experimental protocol is inferred.

When absolute rates are variable binary inputs while only J/gamma is fixed,
the physical acquisition durations above retain their actual 1/gamma scaling.
Polynomial numerical work in rate bits does not make that physical time
polynomial in the bit length of gamma. Operation counts, arithmetic work,
physical duration, reset strength and ancilla supply are distinct resources.

#### 8. Reusable intervention service and complete uncertainty statement

The retained predictive object is the rational local drift table, dictionary,
gamma, coefficient uncertainty, calibration record, local bounds, and a paid
spatial index. It is not an acquired full many-body density matrix. Acquisition
at target alpha is done once. Every future query supplies a new product source,
bounded known coherent drive, local O, time T and numerical precision/confidence.

On the simultaneous coefficient-validity event, a Hamiltonian difference is a
sum of local maps ||i[(h_P-hhat_P)P,.]||<=2alpha. Use (5) with eta=2alpha and
q equal to the actual dictionary term-density bound. If the actual process has
an additional declared local-generator discrepancy b_miss, use eta=2alpha+b_miss.
If independent future source errors are <=zeta per site and readout mean has
certified discrepancy b_read, then, with per-query numerical failure delta_j,

    |fhat_j-f_actual,j|
      <= epsilon_num,j
         + K_stab(2alpha+b_miss)/gamma
         + K_prep zeta+b_read.                             (10)

The calibration event contributes its own failure probability. This event is
simultaneous over ALL allowed future controls: no uncountable union bound is
used. Numerical failures may be allocated delta_j=6 delta_service/(pi^2 j^2),
so all countably many queries hold simultaneously with failure <=delta_service,
even when a researcher chooses each next query using earlier numerical answers.
The physical process must retain its declared generator/control/noise contract;
unknown non-Markovian memory is not acquired for free.

Choosing alpha=O_g(gamma epsilon), and making the other declared floors fit the
requested budget, gives polynomial acquisition operation counts and arithmetic,
polynomial storage and classical evaluation at every fixed positive noise ratio,
with physical acquisition durations explicitly charged above, and error independent
of n,T apart from paid explicit descriptions and acquisition of n coefficients.
It predicts unperformed experiments within this class and recomputes no full
many-body state. The original all-ratio worst-input predictor supplies the
enabling operation; experimental learning and stability are established tools.

#### 9. Obstruction and novelty accounting

The reference steady state is maximally mixed: this is not a general predictor
for low-temperature interacting matter or sustained cooled processing. Generic
correlated inputs can carry the answer to a hard computation in a single local
marginal already at T=0. Arbitrary quantum-measurement feedback, fresh pure
ancillas, and resets can replenish entropy and invalidate the decay argument.
The perturbation theorem permits imperfect cooling only above an explicit
fixed uncertainty floor; it does not prove arbitrary-accuracy cooling simulation.
Full output sampling, relative rare-event probabilities, and the zero-noise
limit remain separate operations. Polynomial costs here are astronomical; no
experimental demonstration, practical dominance, or first-priority claim follows.

Primary comparators checked or to be checked at exact versions in source records:
King1210.8412v1 Theorem1/Corollary2; Angrisani et al2609.40174v2
LemmaS15/CorollaryS16/TheoremS20 and actual operational quantifiers;
Lucia et al1409.7809v2 Theorem1 (autonomous stability predecessor);
Barthel--Kliesch1111.4210 (time-dependent locality);
Mobus et al2606.23652v1 Theorem4.5 and Theorem8.2/Corollary8.3
(learning and local verification; generic learned many-body evaluation still paid).


## Proof component 9: Finite-rate physical acquisition preparation

Source: [principal/PAID_ACQUISITION_PREPARATION.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/principal/PAID_ACQUISITION_PREPARATION.md), SHA256 `b5ba03ee430e8caf0f3cff626ca736915c95b11568d523bb9b5de311ebdd3846`.

### Finite-rate reset implementation of the acquisition input contract

This appendix specifies one paid realization of the noisy product preparation
used in LOCAL_ROBUST_PREDICTION.md. It does not assume the unknown drift can be
turned off. It is an additional acquisition control, not an allowed operation
in the later replacement-only prediction dynamics. It supplies no fixed-hardware
or total-cost advantage.

#### Reset primitive and physical meaning

For each local setting sigma choose a known full-rank qubit state
sigma_i=(I+s_i p_i R_i)/2, p_i>=p0>0. The preparation mechanism applies the
replacement map R_i(X)=sigma_i tensor Tr_i X at Poisson rate kappa. A reset is
a swap with a fresh ancilla in state sigma_i, followed by discarding the old
qubit. The ancilla state can be a fixed-temperature Gibbs qubit with fixed
energy gap, rotated into the selected axis. A numerical guarantee for its
polarization/rotation/measurement errors is part of the calibrated primitive;
it is not inferred from a bath label or unknown hardware.

The source remains subject to its unknown H_0 and replacement noise during
preparation. Let Gamma=2dJ_0+2gamma and n be the number of sites. The diamond
norm of their total generator is <=n Gamma. In comparison, the reset-only
generator kappa sum_i(R_i-Id) has the exact product sigma= tensor_i sigma_i
as fixed point. It is within trace distance 2n exp(-kappa tau) of sigma at
time tau from every initial state: couple to the event that each site was
reset at least once. This argument remains valid for correlated initial states.

CPTP Duhamel gives a second error <=n Gamma tau from the always-on unknown
drift/noise. Therefore the actual prepared state satisfies

    ||rho_prepared-sigma||_1
       <=2n exp(-kappa tau)+n Gamma tau.                    (1)

No microscopic state or unknown Hamiltonian needs to be solved to obtain (1).

#### Explicit finite choices and costs

For a target preparation trace error b in (0,1), take an integer

    L>=ceil(log_2(16n/b)),
    tau=b/(4n Gamma),
    kappa=L/tau=4n Gamma L/b.

Then (1) is <b/2. Gamma=0 is a trivial direct-reset case and may use any
declared positive upper bound instead. All times/rates are rational. The reset
strength is finite but grows polynomially in n and b^-1. The physical model
must actually provide that strength; a fixed maximum rate does not warrant it.

There are n L expected swaps and fresh thermal ancillas per preparation.
An explicit Poisson tail gives a finite high-confidence cap of
O(nL+log(1/delta_prep)) reset events; truncating runs at such a cap costs the
declared failure probability or corresponding trace-error budget. The apparatus
must provide instantaneous event rate n kappa, source duration tau, axis control,
and ancilla preparation/delivery at its declared per-ancilla time/energy/work.
These are paid resources. A Poisson Lindblad reset is the model of that mechanism,
not a proof of a particular reservoir's all-time Markovian approximation.

For signed acquisition scores bounded by A_acc, an initial trace error b changes
the mean score by at most A_acc b. Choose

    b<=alpha t/(16 A_acc)

to fit the coefficient-learning bias allocation, where t=O(alpha/Gamma^2)
is the subsequent interrogation time. Thus b^-1 and kappa are polynomial in
the requested inverse coefficient accuracy, and physical precision need not
be exponentially small in n. Known fixed component errors in each reset alter
the calibrated target sigma_i or add a declared floor; repetition does not remove
unknown systematic errors.

This is one conservative way to pay an experimental input interface. It is much
less economical than ideal simultaneous product preparation or stronger existing
learning protocols. If only a fixed reset rate or an uncharacterized bath is
available, the correct result is the operational preparation-bias floor in the
main learning theorem, not arbitrary-accuracy acquisition. The later predictor
does not simulate unknown cooling interventions at arbitrary accuracy.


## Proof component 10: Global learned reuse with extensive uncertainty

Source: [principal/GLOBAL_LEARNED_REUSE.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/principal/GLOBAL_LEARNED_REUSE.md), SHA256 `eb44aa6c23b73c981929865839709ec10b2d7f0ca7e47327c3f50402b2b48c93`.

### Acquired global product-readout predictions at all horizons

This composition uses the machinery researcher's independently frozen global
product-readout construction, the checked noisy acquisition protocol, and the
following elementary global perturbation estimate. Local volume-independent
uncertainty is a different, stronger stability property; it is not asserted for
global readouts.

#### Global all-time perturbation bound

Let the reference be an n-qubit generator with arbitrary bounded prescribed
time-dependent Hamiltonian and all-site replacement floor gamma>0. Its normalized
trace is stationary. Entropy contraction and Pinsker, uniformly over every input,
give for any Hermitian O with ||O||<=1

    ||Phi_(s,t)(O)-tau(O)I||
       <= min(2,sqrt(2n log 2) exp(-gamma(t-s)/2)).            (1)

Suppose the actual physical Heisenberg generator differs by M local terms
B_(j,t), each annihilating identity, ||B_(j,t)||<=eta. The actual total generator
is CPTP in the Schrodinger picture; it need not be unital there. Duhamel with
the reference future evolution next to the perturbation gives

    sup_(s<=t) ||Phi'_(s,t)(O)-Phi_(s,t)(O)||
       <= (M eta/gamma) [4 log(2n)+4].                       (2)

For the scalar integral, split x=gamma(t-s) at x0=2log(2n). Its initial portion
is at most 2x0, and its exponential tail is at most
2 sqrt(2n log 2)/(2n)<=2. Equation (2) uses a larger round bound. Completely
bounded local errors suffice for the norm premise. M=O(n) for bounded incidence.
This is all-time GLOBAL stability with an extensive cost, not a time/volume-
independent global estimate or a TV sampler.

#### Reusable predictive object and full error

Acquire the unknown drift coefficients at simultaneous accuracy alpha, storing
the rational table, dictionary, calibrated noise rate and uncertainty record.
For Mpar Hamiltonian terms, the difference maps have norm at most 2alpha. An
additional physical-model discrepancy consisting of Mmiss local terms of
strength at most b_miss is paid separately. Future query j supplies a product
source, a new bounded coherent schedule, a global product of Hermitian
one-qubit contractions, time T_j, and numerical error/confidence. On the single
valid-acquisition event, the global readout theorem computes fhat_j with

    |fhat_j-f_actual,j|
       <= epsilon_num,j
          +[4log(2n)+4] * (2Mpar alpha+Mmiss b_miss)/gamma
          +b_source+b_read.                                (3)

Here b_source is an actual global trace-distance source mismatch, bounded by
sum_i zeta_i for independently inaccurate product preparations. b_read bounds
the norm error of the full readout; independent local readout-factor errors may
be summed by telescoping. Source/readout errors need not be unreasonably small:
for inverse-polynomial total precision, inverse-polynomial local precision
suffices. Arbitrary unknown correlated source error is not controlled by a list
of one-site marginal errors.

Choose alpha=O(gamma epsilon/[Mpar log(2n)]) and fit the declared other floors
to epsilon. The elementary alpha^-4 acquisition protocol has polynomial operation
counts and arithmetic in n, epsilon^-1, fixed rate ratios, calibrated contrast
factors and confidence digits. Physical acquisition time retains its explicitly
charged inverse-rate dependence, including 1/gamma. The stronger
existing local-learning machinery can improve its sample exponent under its
own access assumptions. Finite-rate reset preparation is supplied separately
in PAID_ACQUISITION_PREPARATION.md, with polynomially growing strength and
explicit thermal-ancilla flux. It is not a fixed-control-budget theorem.

The drift table has O(n) coefficients and polynomial bit memory. The subsequent
same-2D global-product evaluator has polynomial bit work at every fixed positive
noise ratio, including the actual proposed control/input descriptions. No future
target experiment is performed. The simulator evaluates sparse observable
propagation and short buffers rather than a full 2^n-state vector. Numerical
failure budgets may be summable over adaptively chosen queries; coefficient
validity is simultaneous over all controls within the uniform bounds.

This is a complete acquired-model prediction capability at its promised
Markovian, product-source, coherent-control, replacement-noise scope. Its enabling
new operation is the global product-readout extension. Local learning, ordinary
statistical confidence, entropy mixing and perturbation composition are credited
as established techniques. Neither practical superiority, full output sampling,
generic quantum-state acquisition nor a low-temperature cooled service follows.


## Proof component 11: Relative mixing and all-product oracle insufficiency

Source: [constructor/RELATIVE_MIXING_AND_SAMPLING_OBSTRUCTION.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/constructor/RELATIVE_MIXING_AND_SAMPLING_OBSTRUCTION.md), SHA256 `3d50f92c77140e8a6d439cd36b963cd3c28a50e4dac0faecd5876ce7faa153be`.

### Relative mixing certificate and the precise scalar-to-sampling obstruction

Post-exchange constructor follow-up, 8 November 2026.

This file supplies two complete mathematical objects. First, an operator-order
mixing certificate earns actual continuous-time relative marginals and positive
sampling after logarithmic physical time. Second, a noisy linear-code family
proves that exponential Pauli/Fourier-weight decay alone cannot justify even TV
sampling by low-degree truncation. Neither object closes generic 2D sampling
at all earlier times. Neither is claimed historically novel.

#### 1. A physical-time relative mixing theorem

Let an n-qubit system obey

`L_t(rho)=-i[H(t),rho]+gamma sum_i(E_i(rho)-rho)`,

with gamma>0. H(t) can be any bounded measurable Hamiltonian; no spatial
locality or commutation with the replacement noise is assumed. A finite-bit
algorithmic instance still supplies the explicit rational schedule and rate.
The initial density matrix may be arbitrary and correlated. Write

`R_t=2^n rho_t`, `tau=I/2^n`.

For `gamma T>=log n`,

`||R_T-I||_infty <= 2 sqrt(3) n exp(-gamma T)
                    <=4n exp(-gamma T)`.                 (1)

Thus for any `0<eta<=1/2`, if

`gamma T >= log(4n/eta)`,

then the following operator-order certificate holds:

`(1-eta) tau <= rho_T <= (1+eta) tau`.                    (2)

The conservative finite-bit test

`gamma T >= ceil(log_2(4n/eta))`                          (3)

is sufficient and uses only rational arithmetic and integer comparisons.

##### Proof with exact dependency and time orientation

King's Corollary 2, equation (17), gives depolarizing hypercontractivity in
normalized Schatten norms:

`||D_s X||_(q,tau)<=||X||_(p,tau)`

when `1<p<=q` and `q-1<=exp(2gamma s)(p-1)`.
Primary source: <https://arxiv.org/html/1210.8412>.

Interleave each infinitesimal depolarization step with the actual unitary
conjugation generated by H(t). A unitary conjugation is an isometry at every
Schatten exponent. Let the exponent vary with physical time so that
`p(u)-1=(p(0)-1)exp(2gamma u)`. The same estimate survives at every finite
product step and in the product limit. In particular, the Schrödinger
propagator on every actual chronological subinterval has the same bound.
No noise channel is commuted through H and no time-translation invariance is
assumed. This is the same primary import used in the original report.

Set `a=(log n)/(2gamma)`; a=0 when n=1. First use p=1+1/n and q=2 for
duration a. Since `Tr rho_0=1`,

`||R_0||_(p,tau) <= 2^[n(1-1/p)] =2^[n/(n+1)] <2`.

Indeed this norm is maximized by a pure input, so no representation of rho_0
is needed for the inequality. Consequently

`||R_a-I||_(2,tau)^2=||R_a||_(2,tau)^2-1 <3`.             (4)

On the middle interval, every traceless operator X obeys

`||Psi_{u,v}(X)||_(2,tau) <= exp[-gamma(v-u)]||X||_(2,tau)`.

The Hamiltonian is skew-adjoint in HS inner product, and every nonidentity
Pauli coefficient is damped at rate at least gamma. This proves the estimate
by differentiating its squared norm; it is independent of geometry and H.

For the last interval of duration a, use p=2 and q=n+1. Its HC condition is
again an equality. The finite-dimensional norm comparison is

`||Y||_infty <= 2^[n/(n+1)] ||Y||_(n+1,tau) <2||Y||_(n+1,tau)`.

When T>=2a, put the middle interval length `u=T-2a`. Combining it with (4)
gives

`||R_T-I||_infty <2 sqrt(3) exp(-gamma u)
                    =2 sqrt(3) n exp(-gamma T)`.

This proves (1)--(3). The calculation is valid for density matrices of
arbitrary rank and for piecewise Hamiltonians. It does not involve reference
systems or a diamond-norm claim about the entire channel.

##### What the certificate actually earns

For **every positive effect** `0<=M<=I`, simultaneously,

`(1-eta) Tr(M tau) <= Tr(M rho_T) <=(1+eta)Tr(M tau)`.    (5)

Therefore every computational-basis prefix x_S satisfies

`|log p(x_S)+|S| log 2| <= -log(1-eta) <=2eta`.          (6)

This is a genuine log-marginal operation with no rare-event inverse cost,
despite p(x_S) being as small as approximately 2^-|S|. The output
`-|S|log 2` is computed to the requested rational precision by ordinary
certified scalar arithmetic. Its bit cost is polynomial in |S| and the
precision digits, not 2^|S|.

Conditional prefix probabilities obey

`(1-eta)/(1+eta) <= 2 p(x_i|x_<i) <=(1+eta)/(1-eta)`.     (7)

There is no need to multiply n conditional-error allowances to claim a
whole-output approximation: the stronger simultaneous operator inequality
already gives

`(1-eta)2^-n <= p(x) <=(1+eta)2^-n`                     (8)

for every full outcome x. Thus the uniform sampler is positive, has bounded
random-bit cost n, and has pointwise relative error at most `eta/(1-eta)`
when measured relative to p. Its TV error is at most eta/2.

For a specified terminal product POVM, sample the maximally mixed reference
law using its local traces. The same pointwise relative certificate applies
to all outcome effects. More generally (5) applies mathematically to every
measurement effect, but sampling an arbitrary succinct quantum measurement
on tau is not asserted free. Adaptive terminal local measurement transcripts
also have positive effects, and their tau reference law is classically
sampleable when the supplied local measurement policy is.

All arithmetic in (3), source scanning and terminal reference sampling is
polynomial in the explicit input bits. The theorem uses no supplied input
state description in this long-time branch. There is no claim of a complete-
bounded/diamond approximation that preserves arbitrary quantum reference
correlations.

##### Comparator and significance

This is a consequence of established HC and the elementary HS gap, not a new
long-time dequantization principle. It strengthens the report's entropy/TV
cutoff into an explicit relative **operator-order** statement at logarithmic
physical time. It is useful for a rigorous end branch of any future sampler
and for identifying the genuine remaining interval.

It does **not** produce relative marginals at constant physical times below
that threshold. The desired all-time 2D positive sampler still has to bridge
the interval between short-time tensor methods and this logarithmic-time
certificate. The global product-readout theorem currently fills that interval
only for additive scalar means.

#### 2. Why exponential weight decay is not a sampling certificate

The new smoothing theorem can bound individual global Pauli readouts
exponentially in their occupied weight. It is tempting to truncate the
Fourier expansion of a prefix probability and infer that this pays sampling.
The following constructions show the missing operation precisely.

##### 2.1 Even a simple product distribution defeats relative low-degree truncation

On `{+1,-1}^n`, let

`p_kappa(x)=2^-n product_i (1+kappa x_i)`, `0<kappa<1`.

Every Fourier coefficient is exactly `kappa^|S|`. Nevertheless, at x=all-plus,
the fraction of its exact probability retained by truncating at degree L is

`sum_{j=0}^L binom(n,j) kappa^j /(1+kappa)^n
 =Pr[Bin(n,kappa/(1+kappa))<=L]`.                         (9)

For L=O(log n) this tends to zero exponentially. Thus exponential coefficient
decay alone does not pay a relative marginal by polynomial-degree truncation.
This particular law is independently trivial to sample; failure of the
truncation route is not hardness of the distribution.

##### 2.2 A positive family defeats even TV truncation

Fix any `0<kappa<1` and set `q=(1-kappa)/2`, so `0<q<1/2`. Let `h2` be
binary entropy. Choose fixed constants

`0<R<1-h2(q)`,

`0<delta<1/2` with `h2(delta)<R`.

For arbitrarily large n there is a binary linear code `C_n` of dimension
`m=floor(Rn)` whose dual has minimum nonzero Hamming weight above delta n.
Indeed choose a uniformly random m-dimensional subspace. Every given
nonzero v belongs to its dual with probability at most `2^(1-m)`. The number
of vectors of weight at most delta n is at most `2^[n h2(delta)+o(n)]`.
A union bound makes the chance of any such dual word exponentially small.
Thus such code families exist; this is a standard probabilistic coding
argument, derived here in the exact needed scope.

Draw c uniformly from C_n and independent Bernoulli(q) error bits z. Output
`x=c+z` mod 2. This is a positive distribution p_n with an explicit polynomial
sampling algorithm given a generator matrix. Its Fourier coefficients are

`hat p_n(S)=1_[1_S in C_n^perp] kappa^|S|`.              (10)

Therefore **every** coefficient obeys the exponential envelope
`|hat p_n(S)|<=kappa^|S|`, and all nonidentity coefficients below degree
delta n are zero.

Choose a fixed small s>0 with `R+h2(q+s)<1`. With probability tending to one
exponentially fast, z lies in the Hamming ball of radius `(q+s)n`. Hence p_n
has probability tending to one on

`A_n=C_n+B_[(q+s)n]`,

whose cardinality is at most

`|A_n| <=2^[n(R+h2(q+s)+o(1))]`.

The uniform law assigns A_n exponentially small mass. Consequently

`TV(p_n,Uniform)->1`.                                   (11)

But every Fourier truncation of degree less than delta n returns exactly
Uniform, by (10). Thus individual exponential Fourier decay, even with
positivity and an actual efficient generating process, does not justify
low-weight truncation as a TV sampler.

This is **not a counterexample to the target noisy 2D theorem**. The code
input/encoder is not supplied by the target product-input bounded-local-
physical-time preparation. It proves only that a sampling implication based
on the scalar decay envelope alone is invalid. Spatial connectedness and
the actual preparation history must enter a successful argument.

##### 2.3 All bounded global-product means can be exponentially indistinguishable

The same code family supplies a stronger, exact oracle obstruction. Let
`rho_n=sum_x p_n(x)|x><x|` and `tau_n=I/2^n`. If the code dual distance is d,
then **every** product of one-qubit Hermitian contractions satisfies

`|Tr[(rho_n-tau_n) tensor_i O_i]| <= kappa^d`.             (12)

This includes arbitrary axes, global parity, all partial computational-basis
projectors and products arbitrarily close to identity. To prove it, rho_n
is diagonal, so only each O_i's diagonal entries matter. Write its diagonal
part as `a_i I+b_i Z`, where a_i,b_i are real. Since `||O_i||<=1`,

`|a_i|+|b_i|=max(|a_i+b_i|,|a_i-b_i|)<=1`.

Using the exact Fourier formula (10), the difference of the means is

`sum_[S in C_n^perp, S!=empty] kappa^|S|
       product_[i in S] b_i product_[i notin S] a_i`.

Every occurring nonempty S has at least d sites. The sum of the absolute
values is therefore at most

`kappa^d sum_[all S] product_[i in S]|b_i|
                         product_[i notin S]|a_i|
 =kappa^d product_i(|a_i|+|b_i|) <=kappa^d`.

This proves (12). In the asymptotic family d>=delta n, so the product-mean
discrepancy is exponentially small even though the computational output laws
have TV distance tending to one. A linear combination of product readouts
with coefficient one-norm L has discrepancy at most `L kappa^d`; a polynomial
L does not remove the separation.

The norm bound is in fact **sharp**: choose O to be Z on the support of any
minimum-weight nonzero dual codeword and identity elsewhere. Its discrepancy
is exactly `kappa^d`. Thus the supremum over all admitted global-product
readouts equals `kappa^d`, while `||rho_n-tau_n||_1` tends to two.

**Black-box nonimplication.** Suppose a proposed sampler sees an unknown
output law only through the additive bounded-global-product mean contract.
If it requests inverse-polynomial precision (the precision regime costing
polynomial time), the deterministic oracle

`Answer(O)=Tr(tau_n O)`

is a valid answer oracle both for tau_n and for rho_n once n is sufficiently
large. It is correct with probability one in both cases. This remains true
for adaptive queries and for any number of queries at that accuracy. The
proposed sampler receives the same transcript in the two cases and hence
produces the same output law q. By the triangle inequality,

`max(TV(q,p_n),TV(q,Uniform)) >= TV(p_n,Uniform)/2 ->1/2`.

Thus the additive global-product evaluator's answer contract alone cannot
earn a vanishing-TV sampler over general output laws. This is an information-
theoretic statement, requiring no complexity conjecture. It does not rule
out a sampler exploiting the target Hamiltonian's locality and preparation
structure, nor a reduction using additional relative/correlation information.
The noisy-code generator matrix itself is an efficient positive sampler;
the obstruction concerns the weaker scalar oracle interface.

##### Consequence for a continuous-time polymer route

The target needs a bound on **connected activities** or relative conditional
influences, not merely separate Fourier coefficients. The product example
shows how an extensive moment sum can become easy only after its logarithm
factorizes. The noisy-code example shows why omitted connected structure can
retain almost all of the TV signal in exponentially many high-weight terms.

The Nelson et al. discrete proof obtains connected-polymer weights by exact
finite-depth lightcone factorization and intermediate minimum Pauli weight,
not by the individual Fourier envelope alone. Its Theorem 2.3 and Section 5
remain the correct comparator:
<https://arxiv.org/html/2610.00548v2>.

For a continuous Hamiltonian, arbitrarily small tails destroy exact disjoint
lightcones. A plausible repair is a polymer expansion that includes the
rare links crossing buffered causal regions as additional activities and
proves a Kotecky--Preiss bound with constants uniform in the fine time step.
The present report has **not** established that expansion or its required
relative normalization. Treating an O(1) local tail as an O(epsilon) global
TV error would leave an unpaid factor of n; dividing it by a prefix mass
would be worse. Those costs cannot be hidden by the additive readout oracle.

#### 3. Follow-up claim ledger

| Claim | Status |
|---|---|
| `||2^n rho_T-I||_infty <=4n exp(-gamma T)` after `gamma T>=log n` | Proved HC consequence |
| Uniform all-outcome relative probabilities and positive sampler after the displayed logarithmic threshold | Proved consequence |
| Same certificate for arbitrary correlated input and bounded measurable Hamiltonian controls | Proved; no input representation needed in this branch |
| Exponential Fourier envelope implies efficient relative marginal truncation | Disproved by (9) |
| Exponential Fourier envelope implies low-degree TV approximation | Disproved by (10)--(11) |
| Inverse-polynomial additive access to every bounded global-product mean determines an arbitrary output law to vanishing TV | Disproved by (12) and the common-oracle argument |
| A target-class counterexample or hardness theorem | Not claimed |
| Constant/intermediate-physical-time 2D positive/log-conditional representation | Open; no completed construction supplied |
| Novelty of the relative mixing lemma | Unverified; established-HC corollary, not claimed first |

The two proved constructions sharpen the exact available positive branch and
the exact insufficiency of the scalar-to-sampling shortcut. They do not turn
the unresolved intermediate-time operation into a theorem.

#### 4. Executed finite diagnostic

`audit_relative.py` (NumPy only) and `AUDIT_RELATIVE.json` verify the
relative-operator inequality on a genuinely two-segment driven three-qubit
model at four times. The maximum error/bound ratio was 0.04161. A positive
16-bit noisy linear-code example has zero degree-one/two Fourier coefficients
to roundoff, dual minimum weight three, and TV distance 0.89097 from its
degree-two truncation (uniform). The exact Fourier formula residual was
8.89e-16. These tests supplement the analytic proofs and establish neither
an asymptotic theorem nor the missing target-class sampler.


## Proof component 12: Nonlocal syndrome laws and logical algebras

Source: [auditor/NONLOCAL_READOUT_COMPOSITION.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/auditor/NONLOCAL_READOUT_COMPOSITION.md), SHA256 `e846dfab93f6f1ae1e90b1b5b4a31a130b13087b1eaf2fe6a729d3d43e39e235`.

### Positive composition: nonlocal syndrome sampling and encoded-algebra tomography

Auditor, 8 November 2026. These are proved linear-algebra consequences of the
audited all-support product-readout theorem, including its explicitly bounded
prepared/generated-input and driven extensions. They do not use the biased
reset local-observable theorem as a global-readout premise.

Let Q be the complete binary resource including n, input descriptions,
inverse target error and confidence digits. Let r<=C log_2 Q for a fixed C.

#### Nonlocal parity/syndrome distribution

Supply an explicit binary r by n matrix F. On a computational-basis output
x, define the r parity bits y=Fx mod 2. For every s in {0,1}^r,

    mu_s=E[(-1)^(s dot y)]=Tr(rho_T Z_(F^T s)).

The physical observable is an arbitrary global Pauli product, so each moment
has a polynomial additive evaluator. Set mu_0=1 exactly. Estimate the other
2^r-1 moments to eta=epsilon/(32*2^r), with total failure probability at most
epsilon/4 for an unconditional TV sampler (or a separately requested delta
for a high-confidence explicit distribution table). Walsh inversion gives

    p_tilde(y)=2^-r sum_s (-1)^(s dot y) mu_hat_s.

It is rational and sums to one. On the valid estimation event,
`||p_tilde-p||_1<=2^r eta<=epsilon/32`. Clip negative entries and normalize.
For a trace-one real table, the negative mass is at most half its l1 distance
from the true probability table; clipping/normalizing changes it in l1 by
twice that negative mass. Thus the normalized table has l1 error at most
epsilon/16. Finite-bit sampling adds a separately paid TV error, say
epsilon/8. The bad estimation event contributes at most epsilon/4 to the
unconditional TV distance. This gives a bounded-work TV sampler with total
error below epsilon. The number of moments, their inverse precision, table
size, Walsh arithmetic and all confidence digits are polynomial in Q.

These syndrome bits can be supported across the entire lattice; they need
not be outcomes on a spatially small subsystem. There is no claim of an
n-bit sampler when r is linear in n. A rare syndrome outcome still need not
have a relative-error estimate. For a promise p(event)>=p0, a conditional
version pays inverse p0 by requesting proportionally smaller absolute error.

#### A logarithmic quantum register defined by global Pauli generators

More generally, supply physical Pauli strings X_j,Z_j for j=1,...,r obeying
the canonical logical commutation relations: X_j anticommutes with Z_j,
all other pairs commute, and every generator is Hermitian and squares to I.
Their products define a unital *-embedding of the r-qubit matrix algebra into
the n-qubit physical algebra. The physical state restricts to a legitimate
r-qubit density matrix rho_logical, without constructing a decoding circuit.
Every logical Pauli is a readily computed signed physical Pauli string.

Estimate its 4^r moments to eta=epsilon/(32*2^r), setting identity exactly.
The reconstructed trace-one Hermitian matrix obeys

    ||rho_tilde-rho_logical||_2<=2^(r/2)eta,
    ||rho_tilde-rho_logical||_1<=2^r eta.

Remove negative eigenvalues and normalize. As for the probability table, this
changes trace norm by at most the original trace error; a certified approximate
eigendecomposition is performed at polynomial dimension 2^r with paid normwise
error. Hence a physical r-qubit density matrix within trace error epsilon is
computable with high confidence in polynomial bit work. This permits any
subsequent explicitly specified bounded readout on that small matrix.

This is tomography of the supplied Pauli operator algebra. It is not a claim
that an error-correcting recovery channel has been performed or predicted:
an error-corrected observable can be a syndrome-dependent sum outside this
single algebra. Arbitrary unacquired correlated sources remain excluded, and
the rare-probability obstructions in AMBITION_REVIEW.md remain intact.


## Proof component 13: Rare-output hardness and biased dual-rail extension

Source: [ambitious/FINAL_RELATIVE_OBSTRUCTION.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/ambitious/FINAL_RELATIVE_OBSTRUCTION.md), SHA256 `5eeb7d53f377fda72fa72897714e0c5850384c663f8c4fc6a01328a81a666841`.

### Relative and logarithmic probabilities: an explicit original-class obstruction

8 November 2026. Post-exchange formalization of the independently frozen `initial/ambitious.md` (SHA256 `313fbcf6e47519842f82cbd7e4a7cefaaee8d0e211306bf247599b0bebc711b5`). The initial bytes are unchanged. Sections 1--7 formalize that initial result; Section 8 is a new post-exchange extension confronting the principal's faithful biased-reset model. Complete derivations are given here. Independent team review and historical priority remain separate questions.

#### 1. Statement with the exact complexity consequence

Fix any positive rational replacement rate gamma, set the interaction upper bound J=1, and fix the physical class parameters k=3, maximum-metric interaction range a=1 and site incidence d=12. The physical system consists of explicitly listed square-lattice qubits, a static rational Pauli Hamiltonian and the generator

    L(rho)=-i[H,rho]+gamma sum_i(E_i(rho)-rho),
    E_i(rho)=I_i/2 tensor Tr_i(rho).

There are no additional physical channels, clean ancillas, controls, intermediate measurements or feedback. The supplied initial state is |0^n><0^n|, an exactly rational one-qubit product. Every physical qubit has the stated positive noise rate, including boundary qubits.

**Theorem A.** A randomized algorithm which, on every such input and every positive rational T, estimates the logarithm of a specified full computational-basis output probability to additive error 1/4 with success probability at least 3/4, in time polynomial in the complete binary input, implies NP=RP. The same implication holds for a fixed-relative-error probability evaluator (for example relative error at most 1/2), an arbitrary-marginal log evaluator, or a log-conditional evaluator with requested additive accuracy O(1/n) and polynomial dependence on inverse accuracy.

All probabilities queried in the reduction are strictly positive; the magnitude of their logarithms is O_gamma(n^2). The evolution times are exponentially small numerically but have O_gamma(n) binary digits. The conclusion applies at **every fixed positive rational gamma/J**. It is a conditional complexity obstruction, not an unconditional lower bound on arbitrary algorithms.

Theorem A says nothing about a uniform total-variation sampler, a time promise T>=T_min>0 independent of size, or a Hamiltonian class restricted to exclusively two-body terms. In fact the very same hard-probability instances are exponentially close in TV to their deterministic initial output. These scope distinctions are proved below, not left as qualifications to an unsupported hardness claim.

#### 2. Exact primary combinatorial import

Primary source: Cristopher Moore and John Michael Robson, *Hard Tiling Problems with Simple Tiles*, arXiv:math/0003039v1, 6 March 2000; subsequently Discrete & Computational Geometry 26 (2001), 573--590, DOI [10.1007/s00454-001-0047-6](https://doi.org/10.1007/s00454-001-0047-6).

The needed statements are unnumbered results of their Sections 2, 3 and 3.1, rather than fictitious numbered theorems:

- **Section 3/3.1, PDF pp. 6--11:** tiling an explicit finite region of the square lattice by right trominoes, with rotations allowed, is NP-complete. General regions, including holes, are admitted. Their finite gadgets and grid embedding give polynomial-size instances. The final paragraph of Section 3.1 completes the planar cubic monotone 1-in-3-SAT reduction.
- **Section 2, PDF pp. 2--3:** allowing both the right tromino and the 2x2 square tetromino gives a parsimonious SAT reduction. This separate counting statement is used only in Section 7 below.

The source explicitly does not prove #P-completeness for right trominoes alone. That stronger import is not made here. A right tromino consists of three cells of a unit 2x2 square, with one corner missing; its four rotations are precisely the four possible missing corners. Reflection adds no new shape for this tile.

The pinned primary PDF is `../sources/literature/ambitious/MooreRobson_math0003039v1.pdf`, SHA256 `2c503a199e2268022c2f7df0bdb654f33fc6174eb5b33dfa6e9a597888d215b0`. Its extracted text is retained beside it. The geometry and both counting qualifications were checked against the actual construction, not inferred from an abstract.

#### 3. The physical Hamiltonian and its geometry

Let R be such a finite region, represented by n lattice cells, with n=3m. Instances with n not divisible by three can be rejected before calling the evaluator, without changing NP-hardness of the residual decision problem. Let T_3(R) consist of all right-tromino placements wholly contained in R, and let q_R be the number of tilings. Define

    H_R=sum_[S in T_3(R)] X_S,
    X_S=product_[i in S] X_i,
    rho_0=|0^n><0^n|.

There are at most four unit 2x2 squares containing a site and three tromino placements in each such square containing it. Thus each site occurs in at most twelve Hamiltonian terms. Every term is a Hermitian Pauli of weight three, maximum-metric diameter one and rational coefficient exactly one. All Hamiltonian terms commute. If M is the number of terms, incidence counting gives 3M<=12n, so M<=4n. Enumeration of all placements costs polynomial time and must include unit-square anchors absent from R; missing lower-left corners are legitimate placements.

A qubit sits at the coordinate of each lattice cell. Holes of the input region therefore translate directly into an allowed finite lattice region. If an implementation insists on a full rectangular array, fill a polynomial-size bounding rectangle with decoupled noisy qubits and include only the Hamiltonian terms on the original cells. Query the all-one outcome on R and the all-zero outcome on the fillers. The filler probability has constant Taylor coefficient one, so the leading-order proof is unchanged; use the full physical site count N in the norm/time bound below. Moore--Robson's polynomial grid construction keeps N polynomial. Thus no physical control that turns noise off on filler sites is needed.

#### 4. Exact leading-order coefficient in the actual Lindbladian

Use the precise replacement convention

    gamma(E_i-Id)=(gamma/4) sum_{P=X,Y,Z}(Ad_[P_i]-Id).

For a computational matrix unit |a><b|, one Hamiltonian left multiplication by X_S flips three ket coordinates, and a right multiplication flips three bra coordinates. A noise conjugation by X or Y flips at most two coordinates, one on each side at the same physical site; a Z conjugation and a negative identity term flip none. Complex phases do not affect this support count.

There are 2n ket/bra coordinates that differ between |0><0| and |1><1|. Each must be flipped an odd number of times. For a word in L_R of length ell to contribute to the final matrix entry, its total number of coordinate flips must be at least 2n. Since every elementary factor flips at most three coordinates, no word of length less than

    r=2n/3=2m

can contribute. At length r every factor must flip three coordinates; hence every factor is Hamiltonian, no coordinate is flipped twice, and exactly m factors act on each side. The m ket factors form a tromino tiling, as do the m bra factors. This also proves that every noise contribution vanishes at this leading order, without commuting noise through H.

One may compute the coefficient in the purely Hamiltonian channel after this exclusion. Each tiling has m! orderings of its disjoint terms, canceled by the exponential denominator. All tilings have the same phase:

    <1^n|exp(-it H_R)|0^n>=(-i)^m q_R t^m+O(t^(m+1)).

It follows exactly that

    p_R(t)=<1^n|exp(t L_R)(rho_0)|1^n>
          =q_R^2 t^r+R_R(t),                              (1)

and that all Taylor coefficients below degree r vanish. The derivation uses finite matrix units and the density-matrix generator; it does not use a rare-conditioning heuristic, a postselection hardness theorem from another geometry, or an inaccessible-state oracle.

#### 5. Full remainder, bit length and positivity

##### 5.1 Explicit separation

For trace norm induced on all matrices,

    ||L_R||_(1->1)<=2M+2gamma n.

The commutator bound is 2||H_R||<=2M, and every CPTP replacement has induced trace norm one, so ||E_i-Id||<=2. Choose the integer

    C=max(1,ceil(2M+2gamma n)),
    T_R=2^-(2C+20).                                      (2)

For 0<t<=1, ||rho_0||_1=1 and the norm of the final effect is one. Hence the entire Taylor remainder after degree r satisfies

    |R_R(t)|<=sum_[ell>=r+1] C^ell t^ell/ell!
             <=e^C t^(r+1).

Because e/4<1, (2) gives

    |R_R(T_R)|<=2^-20 T_R^r.                             (3)

Thus

    q_R=0  => p_R(T_R)<=2^-20 T_R^r,
    q_R>=1 => p_R(T_R)>=(1-2^-20)T_R^r.                  (4)

A 1/4-additive log estimate, compared against r log T_R-1, distinguishes the two alternatives with a large constant margin. Computing that threshold to error 1/16 uses ordinary certified arithmetic for log 2. A relative-probability estimate with error at most 1/2 also separates the two intervals directly.

The confidence 3/4 gives a BPP decision algorithm for the NP-complete tiling problem. Reduce SAT to that problem. Amplify each SAT decision call to failure at most 1/(100v) for a formula with v variables, use the decisions to choose a variable assignment one bit at a time, and verify the resulting assignment. An unsatisfiable formula is never accepted after verification; a satisfiable formula yields a witness with probability at least 0.99 by the union bound. Therefore SAT belongs to RP and NP=RP. In the deterministic case SAT belongs to P.

##### 5.2 Complete finite input costs

For fixed gamma, C=O_gamma(n). The positive dyadic time is supplied as numerator one and an explicit denominator with 2C+21 bits. It therefore costs O_gamma(n) bits, not exp(n) bits. Its r-th power has O_gamma(n^2) bits. Hamiltonian coefficients are exactly one; all O(n) terms and all lattice coordinates are explicitly listed. Moore--Robson's reduction size and coordinate magnitudes are polynomial in the originating formula size.

No cost is declared polynomial in numeric 1/T. Such a cost could be exponential on these inputs. The original and proposed strengthened contracts are polynomial in complete binary input and numeric 1+T; the latter is bounded here. The reduction respects that contract exactly.

##### 5.3 Strictly positive probabilities and polynomial-size logarithms

In the exact random-unitary unraveling, each of X,Y,Z has rate gamma/4. Consider histories with exactly one X jump at each site and no Y/Z or additional X jumps. Their total probability is

    w=e^(-3gamma nT_R/4)(gamma T_R/4)^n>0.

All these X jumps commute with H_R. On such a history, the target probability equals

    |<0^n|exp(-iT_R H_R)|0^n>|^2 >=(1-MT_R)^2>0.

Therefore

    p_R(T_R)>=w(1-MT_R)^2>0.                            (5)

In particular logarithms are well defined even when q_R=0. Equation (5) also bounds -log p_R by O_gamma(n^2), so the output magnitude/representation does not hide an unbounded real-number task. No zero-probability convention contributes to the hardness.

##### 5.4 Conditional evaluators

Along the all-one string, every prefix probability is positive by (5). The chain rule gives

    log p_R(1^n)=sum_i log p_R(x_i=1 | x_1=...=x_(i-1)=1).

Requesting each log conditional to additive error 1/(8n), with per-call failure at most 1/(100n), computes the full log probability to error at most 1/8. Precision inverse and confidence digits are polynomial. Thus a uniformly polynomial log-conditional operation would also give the stated collapse. This concerns logarithms or relative conditional accuracy; an arbitrary fixed additive accuracy for raw conditional probabilities is a different contract.

#### 6. What this proves, and what it leaves open

On exactly the instances above,

    TV(P_T_R,delta_[0^n])
      <=(1/2)||exp(T_R L_R)(rho_0)-rho_0||_1
      <=(1/2)(exp(C T_R)-1),                            (6)

which is exponentially small. A sampler returning 0^n is adequate at every inverse-polynomial TV tolerance on this hard family. A rare event cannot be amplified by a polynomial number of physical samples here. Thus this is explicitly **not** a generic noisy-2D TV sampling hardness theorem or a physical advantage demonstration.

The team's `machinery/FINAL_GLOBAL_READOUT_THEOREM.md` includes an additive probability of every product projector, including this target event. It does not contradict (4): a relative estimate would require additive tolerance comparable to T_R^r, whose inverse is exp(O_gamma(n^2)); that work is outside its polynomial-accuracy regime. The stronger mean theorem genuinely earns global parity/product readouts while leaving this probability task separate.

The constructor's bounded-cut TTN sampler has an additional architectural certificate absent from the arbitrary 2D family used here. Its `constructor/RELATIVE_MIXING_AND_SAMPLING_OBSTRUCTION.md` gives relative operator mixing only after gamma T>=log(4n/eta), far outside T_R. Neither theorem claims the uniform rare-event evaluator ruled out here.

There is no obstruction here for exclusively two-body interactions, a strictly positive lower-time promise, constant/intermediate-time TV sampling, or a physical-time polymer method above a noise-dependent threshold. Those remain substantive targets.

#### 7. Optional stronger counting encoding: mixed tiles with aligned phases

This independent initial construction strengthens the encoded combinatorial object without changing the preceding scope limitations.

Let Z_R count tilings by the right tromino and the 2x2 square tetromino. Moore--Robson Section 2 is parsimonious from SAT. For each tile S choose one distinguished site y(S), and put

    P_S=Y_[y(S)] product_[i in S\{y(S)}] X_i,
    H_R(tau)=sum_[S in T_3] P_S+tau sum_[S in T_4] P_S,
    T=tau^3, 0<tau<=1.                                  (7)

All data are rational. Each physical site is in at most sixteen blocks (twelve trominoes and four squares), support size is at most four, range is one, and every coefficient is bounded by J=1. Let C>=max(1,2M_3+2M_4+2gamma n).

Write the exponent as tau^3 A+tau^4 B, with the noise in A. A three/four-site Hamiltonian factor has tau-degree three/four and flips three/four ket/bra coordinates. A noise factor has degree three and flips at most two. To reach |1><1| requires total degree at least 2n; equality excludes every noise factor and every repeated coordinate flip. Each side is an exact cover.

For a cover with m tiles, its unitary phase (-i)^m cancels the i^m from P_S|0^S>=i|1^S>. Its m! orderings cancel the exponential denominator, including when distinct covers have different m. Every cover has tau-degree n since its tile areas sum to n. Consequently

    p_R(tau)=Z_R^2 tau^(2n)+R_R(tau),
    |R_R(tau)|<=e^C tau^(2n+1).                          (8)

For the last bound, the sum of norms of all power-series coefficients of exp(tau^3A+tau^4B) is bounded by exp(||A||+||B||)<=e^C; evaluate the positive majorant at tau=1 and factor tau^(2n+1) from the tail.

For a requested 0<epsilon<=1/2, choose

    tau=2^-(2C+20+ceil(log_2(1/epsilon))).

The scaled probability differs from Z_R^2 by at most 2^-20 epsilon. A log evaluation accurate to epsilon/8 then gives a reliable zero test (separate scaled probability below 1/2 from at least 1-2^-20 epsilon), and, for Z_R>=1, exponentiating half the estimated scaled logarithm approximates Z_R multiplicatively. This is an approximation-preserving reduction from #SAT counting, not an assertion that a constant-accuracy answer recovers a #SAT count exactly. Every coefficient/time bit, logarithm, square root/exponentiation precision and output bit is polynomially charged. Strict positivity follows by the one-X-jump-per-site event: in the toggling frame all Hamiltonians have the same norm, so the target amplitude is at least 1-||H_R(tau)||T>0.

#### 8. Post-exchange extension: the common biased reference does not remove the obstruction

Fix rational sigma=diag(p,1-p), 0<p<1, and any fixed rational gamma>0. The physical reset is exactly

    R_i^sigma(rho)=sigma_i tensor Tr_i(rho),
    L=-i[H,.]+gamma sum_i(R_i^sigma-Id).

For each logical cell i of a tromino region introduce a physical nearest-neighbor pair (i,a),(i,b), embedded at (2x,y),(2x+1,y). Define the exchange

    F_i=(X_[i,a]X_[i,b]+Y_[i,a]Y_[i,b])/2
       =|10><01|+|01><10|.

It has norm one, acts as logical X on span{|10>,|01>}, vanishes on |00>,|11>, and commutes with sigma tensor sigma. Set

    K_S=product_[i in S] F_i,
    H_R=sum_[S in T_3(R)] K_S,
    rho_0=|10>^n<10|^n,
    target=|01>^n.                                      (9)

Each WHOLE block K_S is rational, Hermitian, norm one, support size six and range at most three. Every physical site belongs to at most twelve blocks. All K_S commute, and every block commutes with the corresponding product sigma. Thus (9) satisfies the principal's conservation condition for every bias p, using physically unentangled product input. Individual Pauli summands need not preserve sigma; the permitted whole blocks do. Expanding K_S yields eight weight-six Pauli terms with rational coefficients 1/8 and bounded incidence, so this is also an original-form local Pauli Hamiltonian in the unital case.

There are N=2n physical sites and 2N=4n differing ket/bra coordinates between the initial and target matrix units. A nonzero K_S multiplication flips six coordinates on one side. A one-site biased reset either kills the matrix unit or changes at most two coordinates. Therefore, with r=2n/3, all coefficients below r vanish, and every length-r contributing word is Hamiltonian and forms an encoded tiling on each side. The action inside the encoded subspace is exactly the previous commuting-X construction. Hence

    p_R(T)=q_R^2 T^r+R_R(T),
    |R_R(T)|<=e^C T^(r+1), C>=max(1,2M+2gamma N).        (10)

Choosing T=2^-(2C+20) gives the identical separation and O_gamma(N)-bit time. This proves the same NP=RP consequence for a uniform all-time relative/log evaluator in the common-reference biased-reset class (at support bound six and range three).

For strict positivity, unravel resets as rate-gamma Poisson events whose prepared value is sampled from p,1-p. The event of exactly one reset per physical site, each preparing its target bit, has probability at least

    exp(-gamma NT)(gamma T)^N mu^N>0,
    mu=min(p,1-p).

Without H this history ends in the exact target product regardless of the input. Keeping all its reset times and values fixed, contractive telescoping of the intervening unitary channels changes the final state by trace norm at most 2MT. Therefore its target probability is at least 1-2MT>0. This yields an explicit positive lower bound and again polynomially bounded logarithm magnitude. This unraveling is a proof representation of the stipulated reset, not access to physical bath outcomes.

The encoded model also has an all-time additive local prediction result under the principal's proposed theorem. The relative obstruction is compatible with it. At exponentially short T the entire distribution remains close to the initial product, so no biased-reset TV hardness or constant-time obstruction is obtained.

#### 9. Checks and status

- `audit_rare_event.py` / `AUDIT_RARE_EVENT.json`: twelve exact Gaussian-integer/rational Taylor checks, including absent-anchor boundary placements, gamma=1 and 7, and mixed-tile phase alignment. The initial ten cases were unchanged when the anchor enumerator was strengthened.
- `audit_dualrail.py` / `AUDIT_DUALRAIL.json`: six exact biased-reset cases, p=1/3 or 4/5 and gamma=1 or 7, with six and twelve physical qubits. The encoded leading coefficients are 1, 4 or 0 according to the exact cover count.

The proofs, not these finite checks, establish the reductions. The new post-exchange encoded extension and the initial reductions remain available for independent principal/hostile review. No initial report, manuscript or published file was edited, and no release or hardware operation was performed.

## Existing machinery, exact predecessors and novelty audit

| Operation | Verified primary predecessor | Added operation and exact distinction |
|---|---|---|
| Sparse coefficient propagation | Angrisani et al2609.40174v2 LemmaS6, LemmaS15/CorS16, weighted CorS12/ThmS20 | Source operational averages retain their quantifiers; moving-weight differentiation/duality and pointwise buffers are proved here. |
| Tracial HC | King1210.8412v1 Thm1/Cor2 | Normalized Schatten convention; varying-exponent Hamiltonian interleaving is explicitly proved. |
| Faithful HC | Dong et al2606.17729v1 Thm1.1; earlier BDR1804.10100v2 Thm21/25 | All-operator symmetric weighted norms; coherent invariance checked, not assumed for arbitrary drives. |
| Time-dependent locality | Barthel--Kliesch1111.4210v2 Thm1/2 | Bounded range/strength/degree and shell hypotheses hold; size independence alone is not inverse-accuracy polynomiality. |
| Factorial buffer locality | HHKL1801.03922v4 Lemma5, AppendixC.4(48)--(49) | Accumulated physical action controls strips; reset permutations keep spatial locality. |
| Overlap architecture | BGM1909.11485v1 Thm5 | Existing shallow-circuit product-readout idea; continuous action and reset-register dimensions are actually paid. |
| TTN operations | Shi--Duan--Vidal quant-ph/0511070v2 Thm1--4 and LOCC sampling; Seitz et al2206.01000v3 Sections2.2/3.2 | Supporting full-TV theorem composes cut action, constructive vector error and entropy cutoff. No firstness claimed. |
| Acquired generator | Mobus et al2606.23652v1 Thm4.5, Thm8.2/Cor8.3 | Learning and local verification are established. This dossier pays efficient evaluation and controlled reuse. The simple alpha^-4 learner is suboptimal. |
| Local stability | Lucia et al1409.7809v2 Thm1 | Known rapid-mixing mechanism; explicit nonautonomous near/far proof supplied. Global uncertainty pays an extensive factor. |
| Strong discrete sampler | Nelson et al2610.00548v2 Thm2.3/Prop2.2, AppendixA | Fixed per-layer p and strict cones. Substitution p~gamma h is nonuniform as h vanishes. |
| Noisy MPO comparator | Shao et al2606.00474v1 Thm1/Prop1, AppendixD.3 | Late relative-HS plus purity CAN imply trace bounds. Fixed-error/existence, cheap construction, positivity and h-uniformity remain separate. |
| Nonunital simulation | Martinez et al2501.13050v1 Thm1; Angrisani et al2501.13101v2 Thm1 | Strong parameter/circuit-average results do not cover each deterministic conserving continuous H(t). |
| Tiling reduction | Moore--Robson math/0003039v1 Sections2,3/3.1 | Right-tromino NP; mixed-tile parsimonious #SAT. No #P claim for right trominoes alone. |

Exact hypotheses, applicability proofs, source hashes and proof checks are in
the embedded constructions and supporting primary-source reviews. Targeted
Zenodo searches inspected records19206525,20109357,17594402,23418780,23414157,
21455333 and related metadata. These are frame/TTN software or numerical/support
artifacts, not imported uniform theorems. Limited searches or metadata reads
are not a clearance of every recent work. Historical firstness remains UNKNOWN.

### A verified source-proof objection at its exact scope

Trivedi--Cirac PRL129260405 remains a relevant published HIGH-noise TV-sampling
statement. This campaign independently found a false CP assertion in the
printed uniformization proof, arXivv2 Lemma3 and the published supplement's
Lemma3: Id+L/g need not be CPTP for any finite g. For H=Z the normalized Choi
compression is [[1,i/g],[-i/g,0]], determinant -1/g^2. For a weight>=2 Pauli H,
only single-site replacement noise leaves the corresponding lower diagonal
zero. The exact Schur-range characterization and valid first-order Kraus repair
are in SAMPLING_FRONTIER.md. A repair retaining coherent no-jump drift does not
restore the same rare-horizontal-edge argument automatically.

This is NOT a disproof of the high-noise theorem conclusion. No complete repaired
proof was cleared here. Earlier comparator wording calling that proof independently
verified is superseded by this precise objection and the final reviews. None of
the positive results here uses that assertion: they use genuine Cayley unitary
channels and actual reset events. All existing theorem statements remain at
their exact working scopes; the objection is separately preserved.

## Remaining decisive problems and constructive attacks

1. **Generic intermediate-time 2D full-TV sampling.** Construct a positive
   representation or connected expansion controlling global error before
   conditioning. Individual weight decay and all-product additive access are
   provably insufficient. No target-class TV hardness follows from the rare
   tiling reduction or from failure of this representation.
2. **Continuous connected activities.** Replace strict circuit cones by soft
   factorial tails and prove computable Kotecky--Preiss bounds uniform in the
   fine time step. A relative theorem beyond a constant physical threshold
   remains a different target from the all-positive-time relative evaluator
   obstructed by the reduction. The T>=constant regime is not settled by tiny T.
3. **Arbitrary weak nonunital violation of the conserved reference.** Stability
   supplies an uncertainty floor; arbitrary accuracy needs constructible
   connected response/renewal control. Generic cooling/fault-tolerance results
   alter resources and do not prove hardness at arbitrarily tiny bias for one
   fixed noise ratio. Reference preservation here is substantive.
4. **Unknown interacting stationary references and macroscopic interventions.**
   Their acquisition, sufficient histories and evaluation must be constructed.
   A formal Gibbs or memory functional can still hide the many-body problem.
   Known finite-depth dressed references do not solve that general operation.
5. **Recovery and extensive decoding.** Logarithmically many nonlocal syndrome
   bits or a logarithmic logical Pauli algebra are earned. Arbitrary syndrome-
   conditioned recovery and n-bit output laws are not. The noisy-code example
   gives a precise finite-precision predictive-sufficiency obstruction.
6. **Useful resource regimes and 3D.** No matched practical superiority is
   demonstrated. The current 2D overlap proof pays boundary action; 3D needs
   another representation/contraction. A failed separator bound is not hardness.

Preserved failures/repairs include RMS-to-pointwise substitution, wrong buffer
chronology, treating biased reset as mixed unitary, discarding old registers,
independently resampling the inverse/parity history, treating weighted factors
as norm1, an invalid sigma-centered bounded mixture, rounding without HS budget,
making the row cap depend on confidence rather than accuracy, rare-prefix
division, and the false finite-rate Euler CP shortcut. The supporting record
retains each correction. A short-time local-relative Taylor idea remains a
candidate only; no unreviewed theorem is promoted from it.

## Independence, validation and completion accounting

Exactly three initial GPT-6.1 Sol max researchers plus the principal each wrote
and froze an initial construction before receiving another researcher's ideas.
The principal read two completed initials after its own freeze while the third
researcher was still writing, and sent that researcher no constructions before
its freeze. This was individual initial independence, not a simultaneous sealed
group freeze. The user subsequently
authorized one additional ambitious researcher, also Sol max, which froze its
own initial before exchange. Original initials remain immutable; hashes and
exposure timing are recorded. No additional agents were created.

Completed internal mathematical reviews are accepted at their actual scopes;
they are not relabeled unreviewed. They are distinct from priority, hardware,
full implementation or journal review. Reviewed component hashes/snapshots and
final assembly checks are retained. All central claims have analytic proofs;
finite floating/exact-rational checks supplement them.

Execution records include original truncation/strip audits; independent weight,
HC, TTN, reset/SWAP, cap and code-law checks; exact rational/Gaussian-integer
tiling/dual-rail coefficients; and exact Choi tests. Principal reruns have tied
script/output hashes. No full worst-case predictor was executed. No physical
experiments, paper publication, website/Zenodo release, third-party communication
or completed Capital integration is claimed by this return.


## Review files


- [machinery/BIASED_GLOBAL_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/machinery/BIASED_GLOBAL_REVIEW.md) — SHA256 `1d0d69833771969cded42d4a038f3e3acf0c0ef70b9406b585c6493096d0f218`.

- [machinery/BIASED_RESET_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/machinery/BIASED_RESET_REVIEW.md) — SHA256 `b8ec5fa12597e0145829266972361f8c3186fc5f6eb647096447dbd29d0343ad`.

- [machinery/CROSS_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/machinery/CROSS_REVIEW.md) — SHA256 `63afd362b716f6452f16f50c9f8c440f66c5906d33804c5f3689b8700dda2d5a`.

- [constructor/AMBITIOUS_REDUCTION_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/constructor/AMBITIOUS_REDUCTION_REVIEW.md) — SHA256 `5de5d7a58bfe6f693e9f8b612497b49ac1b054e67b5171394db770241b325f40`.

- [constructor/BIASED_GLOBAL_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/constructor/BIASED_GLOBAL_REVIEW.md) — SHA256 `6c25abd979431e906b63ca180f279ded3ca9f6f4bc414eb3c8ff0e9b75614c7a`.

- [constructor/BIASED_RESET_CONSTRUCTION_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/constructor/BIASED_RESET_CONSTRUCTION_REVIEW.md) — SHA256 `17912e52578892ff0e0e1bea326d3143e2536466a0c69edf3f59afb172854985`.

- [constructor/CHALLENGE_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/constructor/CHALLENGE_REVIEW.md) — SHA256 `bc85fb64176e46bc52b7629af8f4667cf5dafbffb3dcb577e7920b06f78d16c3`.

- [auditor/AMBITION_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/auditor/AMBITION_REVIEW.md) — SHA256 `9a95dd91af8b901460eb12ca644026eb60f540d9725d669a07f13efab9ca79a2`.

- [auditor/BIASED_GLOBAL_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/auditor/BIASED_GLOBAL_REVIEW.md) — SHA256 `ae08e80d66c58f353f3c1ff2b2c1b58b3c33b67c91e9aea3e801e084a3229d2a`.

- [auditor/BIASED_RESET_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/auditor/BIASED_RESET_REVIEW.md) — SHA256 `e2c0bc9704c4859988cae0b6f20f429fd7bf68af967a002a8f4e0d068b4c0480`.

- [auditor/CHALLENGE_REVIEW.md](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/auditor/CHALLENGE_REVIEW.md) — SHA256 `b90fc8d205f2ebc2fa6bf5c670674e819551189d33b9e3c66afe49a761e3f53c`.


[Final assembly review](NOISY_2D_QUANTUM_DYNAMICS_RESEARCH_RECORD/auditor/FINAL_DOSSIER_REVIEW.md).
