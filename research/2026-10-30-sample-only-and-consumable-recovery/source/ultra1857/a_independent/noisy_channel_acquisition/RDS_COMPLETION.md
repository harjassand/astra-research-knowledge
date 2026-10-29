# Fixed-rank random-dilation completion and occupied-support recovery

30 October 2026. Independent construction/challenge of the stronger ordinary
route in C_STRONG_ORDINARY_ROUTE.md. It uses established random dilation and
Petz algorithms, with B's copy-acquired filter and the paid growing-rank Schur
port. It is not the primary paper's much narrower least-Kraus-rank Petz corollary.
No source, quantum circuit or numerical model is executed here.

## 1. The actual source is only approximately filtered

Let F be the ideal fixed-threshold filtered channel, with common output support
dimension at most dbar. Kraus rank(F)<=k*dbar because its Choi state is supported
on input-k tensor that output support. The implemented filter Ftilde is close in
diamond norm but can have FULL ambient rank. It is invalid to apply a rank-r
promise directly to Ftilde or to compare normalized postselected objects.

What is needed is ONE fixed physical source-query controller, CPTP on every
possible source, whose promised action on rank-at-most-r F equals the random
dilation construction. Then ordinary channel-query hybrids pay the difference
between Ftilde and F without any claim that Ftilde has rank r.

## 2. A literal post-query completion in the primary circuit

I independently inspected the rendered primary 2512.21260v2 page 7 Figure 2(a),
saved by C at source_entry/C_RDS_FIGURE2.png. Its order is explicit: known
controlled input permutations, ALL source queries, known controlled output
permutations, symmetric-group QFT, MEASUREMENT of lambda, then conditional
preparation of pi_(U_lambda) and inverse small-r Schur transform.

Insert a finite arithmetic test length(lambda)>r immediately before those last
rank-r-dependent operations. On that branch discard/reset all would-be outputs
and prepare any fixed state in the advertised output registers. On valid labels
use the original postprocessor. This is a known measurement/feedforward CPTP
postprocessor for EVERY source. It has no source rank test, no postselected
normalization and no impossible irrep input. Its work is polynomial in the
existing finite labels and output-register count.

For a promised rank-at-most-r source, the normalized Choi random-purification
formula, primary Eqs. 32--37, has zero probability on invalid lambda. The bad
branch is itself a CP map. A CP map with zero Choi trace has positive Choi matrix
of trace zero, hence zero Choi matrix, hence is identically zero on ALL inputs
and adjoining references. Therefore the added default leaves the entire
promised superchannel action unchanged, not merely its action on independent
training inputs.

This is why the fixed-rank controller may be fed Ftilde while compared to F.
If it uses n query slots, its full diamond difference on those two sources is
at most n||Ftilde-F||_diamond. The implemented factory is physical on the entire
off-promise domain. Source memory/drift is still excluded.

## 3. An acquired consistent reflection, including inverse and control

The primary Theorem 3 followed by Lemma 6, with known maximally mixed logical
inputs, prepares ONE joint program with representation

    integral [P_(V,theta)/k]^tensor n dV dtheta,
    P_(V,theta)=V(theta)V(theta)*,
    V(theta)=(exp(i theta)|0>V0+|1>V)/sqrt(2).

Every program copy shares the SAME unknown V and theta. Independent factories
for individual queries would not supply one Stinespring oracle and would not
justify the Petz consumer. The single joint factory is essential.

Conditional on those latent variables, U=2P-I is a Hermitian unitary and

    U(|0>V0 psi)=exp(-i theta)|1>V psi.

The public computational embedding V0 and known register reordering make U an
actual Stinespring unitary on the known logical-input/ancilla subspace. Its
inverse is U itself. Standard known padding/encoding is charged; no unknown
channel adjoint is supplied. Output environment has dimension 2r. The input
workspace dimension may grow with ambient D, but its initialization/projection
uses log-dimensional registers; the Petz algorithm's environment factor is the
OUTPUT 2r, not that ambient input-workspace dimension.

Controlled copy simulation of P/k at time pi*k gives controlled exp(-i pi P),
which equals controlled(-U). A known Z on the CONTROL corrects the minus sign.
This phase is relative and cannot be dropped. B's controlled-DME derivation
gives O(k^2/e) fresh program copies per controlled call of error e. Allocating
e=gamma_V/m for m calls gives O(m^2 k^2/gamma_V) total program copies. Conditional
on one latent V,theta, unused copies remain independent. Apply the uniform
query-by-query channel hybrid, then average that SAME latent program mixture.

All these copies are consumed. There is no unlimited reusable program, no
free controlled-N and no inverse of the actual noisy DME operation: separate
fresh-copy simulations approximate the required ideal forward/inverse gates.

## 4. Condition the occupied output without assuming global full rank

For ideal F=J_Pi N, add a public flag replacement with probability xi:

    F_xi=(1-xi)F+xi Tr(.)|fail><fail|.

The occupied mean S=F_xi(I/k) has nonzero eigenvalues at least

    mu=min(xi,(1-xi)a),

and rank at most dbar. It can still have a large ambient kernel. The algebraic
zero-extended Petz formula is trace preserving only on supp S, not globally.
Calling it a globally TP channel without completion would be false.

The actual QSVT/oblivious-amplification UNITARY circuit followed by discarding
work registers is CPTP on the entire physical carrier. Analyze its accuracy
only on the occupied support. The primary Gilyen2006.16924v2 Theorem 1 explicitly
uses minimum NONZERO eigenvalues; its introductory Eq. 2 discussion explicitly
states the support-only trace-preservation property. Its isometric-block proof
can be consumed at exactly that scope. Polynomial approximations remain bounded
on the rest of the spectrum, so no support projection must be supplied as a
gate. B's fixed-cutoff support filter is an alternative paid completion, not a
necessary free primitive.

The amplification premise can also be checked globally, not inferred merely
from boundedness off support. For every Kraus K_l of F_xi, range(K_l) is contained
in supp S: S=(1/k)sum_l K_l K_l* proves this by positivity. Thus
K_l*Pi_(ker S)=0, or V*(I_E tensor Pi_(ker S))=0. Even if the bounded inverse
polynomial has p(0)>0, the adjoint-isometry stage kills that kernel exactly.
The ideal successful base block is consequently close in GLOBAL operator norm
to its known normalization times V_P Pi_S, with singular values the known
amplitude on S and zero outside. Ordinary robust oblivious amplification has
the required partial-isometry structure. Actual copy/gate errors are paid by
full channel hybrids before this ideal-block argument is consumed.

For completeness, an elementary precision port is available. Let V_P be the
Petz partial isometry with V_P*V_P=Pi_S. If the successful block B_alg of a
unitary circuit obeys ||(B_alg-V_P)Pi_S||<=eta, then on every occupied unit vector
its failure amplitude is at most sqrt(2eta). The complete isometry differs from
the embedded ideal one by at most eta+sqrt(2eta). Choosing internal block error
O(target_error^2) gives the desired composed CPTP-channel accuracy, with only a
polynomial precision/cost change. This remains valid with arbitrary references.

A mathematical CPTP extension of Petz can be written by adding a fixed output
on Tr[(I-Pi_S)X]; it need not be implemented. If Alg is the actual completed
circuit, then

    Alg Ftilde_xi - Petz_ext F_xi
      =Alg(Ftilde_xi-F_xi)+(Alg-Petz_ext)F_xi.

The first term is paid by global CPTP contractivity. The second is supported
entirely in supp S. This is the correct consumer norm, not an impossible global
comparison to the trace-decreasing zero extension.

## 5. The other Petz suppliers and all costs

The logical reference I/k is known. The mean S is available as actual calibration
copies from F_xi(I/k). C_COPY_SIGNAL supplies a literal construction rather than
leaving Gilyén's copy-based block-encoding paragraph as an uncharged oracle.
Controlled exp(plus/minus i S/2) and known LCU controls give the ideal block
sin(S/2). On [-1,1] its even inverse signal is

    g(y)=sqrt(mu)/[8sqrt(2arcsin(clip(abs(y),mu/4,3/4)))].

I independently checked its range [0,1/4], Lipschitz bound 1/mu, exact value
sqrt(mu)/(8sqrt(lambda)) at y=sin(lambda/2), and Bernstein variance error.
An even rational Bernstein approximation of degree N>=16/(mu^2 eta^2), with
symmetrically rounded/clipped coefficients, is admissible in real QSVT and
approximates the signal to eta. The controlling GSLW Corollaries 10/18 and
Lemma 19 implement that REAL polynomial with no hidden factor two; Haah's
finite-bit phase algorithm pays polynomial degree/precision work.

Using a normalized output-environment EPR pair, its successful Petz block has
known amplitude sqrt(k mu)/(8sqrt(dE)). This follows from Gilyén Eq. 9's
unnormalized EPR vector and reference factor 1/sqrt(k). Set the amplification
count first from this amplitude, then the required eta, then N. Only afterward
allocate each controlled DME call's error. With Q_S=O(mN) sine-signal queries,
the S-copy cost is O(Q_S^2/gamma_S); programmed Stinespring reflection copies
have their separate O(m_V^2 k^2/gamma_V) count. There is no circular request for
an inverse or a free purification gate. All counts depend on output environment
2r and inverse occupied scale 1/mu, both intrinsic polynomials here.

Fix the complete finite consumer/query budget FIRST. Produce one sufficiently
large joint reflection program, all S copies and payload-filter A copies during
calibration. Then choose each source-filter and controlled-simulation error
small enough for its total hybrid budget. Original A copies use direct N(I/k),
so this is not a recursive request for new F-program copies. RDS's fixed CPTP
completion pays slightly full-rank implemented filters at every program slot.
All source states, register controls, ambient log D memory and precision count.

No original source call is needed after the late encoded payload arrives,
apart from the externally supplied encoding of that payload. The preacquired
program can serve any PREDECLARED finite number of payloads by allocating enough
copies and errors. It is consumed and may retain large ambient orientation
information in quantum memory. This does not contradict the earlier intrinsic-
program/streaming obstruction or create a free classical decoder.

## 6. Consequence for scientific judgment

Root's Bell-target filter bound supplies a recovery competitor for F with
infidelity at most 2kappa+3t. Flag replacement adds at most xi. Ordinary
Barnum--Knill applied directly to the ideal Petz map gives

    halfdiamond(Petz_(F_xi) F_xi,id)
       <=k sqrt(4kappa+6t+2xi).

This strongest ordinary route can therefore realize the same qualitative
effective-rank/approximate-recoverability consequence while improving timing:
the payload need not participate in the program's joint Schur compression.
Its full hypothesis is now constructively admitted at ideal circuit/copy scope,
including the off-rank and occupied-kernel interfaces above. It remains expensive
and conditional on protected quantum-memory/trusted-control access.

The shared-frame tomography operation remains mathematically valid, but cannot
be promoted as uniquely necessary or superior by withholding this alternative.
No numerical cost win, physical device, optimal exponent or historical priority
is established. The useful acquired bridge is the actual-channel spectral
filter/approximate-competitor operation together with fully charged established
programmable recovery machinery.
