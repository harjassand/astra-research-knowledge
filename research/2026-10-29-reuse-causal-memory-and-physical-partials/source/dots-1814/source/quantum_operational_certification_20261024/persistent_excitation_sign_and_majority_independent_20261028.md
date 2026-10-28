# Acquired persistent excitation: independent sign and majority-recovery lemmas

28 October 2026. New independent mathematical derivation, not a receiving receipt. Earlier received sources are unchanged. This note supplies a route from finite ordinary confidence matrices to a frozen width-greater-than-one decoder uniform over every later gauge/memory state. It does not supply a source eigenvalue floor or infer structural model membership.

## 1. Local conditional means and an observed lower certificate

Assume the fixed true exact logical X/Z generators B_ij are supported in correctly acquired envelopes W_i. From the complete nonanticipating Pauli/gauge model, every conditional physical state and signed contrast satisfy

    Delta_ij,h = B_ij R_ij,h,
    kappa rho_h <= R_ij,h <= rho_h,
    [B_ij,R_ij,h]=[B_ij,rho_h]=0.

Reduction to W_i preserves these identities and inequalities because B_ij is supported there. On one common fresh random-axis/sign ordinary bank, unsigned local shadows Z_W have conditional mean rho_W,h, and signed matrices

    2 * 1{j_i=j} * s_i * Z_W

have conditional mean Delta_ij,h. All other current labels/outcomes must be averaged; only the complete PRIOR history is conditioned on. Thus their adaptive time averages share ONE rho_bar and obey Rbar_ij>=kappa rho_bar even if the source changes its gauge state adversarially after each record.

Suppose simultaneous operator-norm confidence radii a_rho,a_j have been proved for the actual empirical means. Let Q_rho D_rho Q_rho† be a rational exactly-unitary Jacobi approximation to the empirical rho, with Frobenius/operator residual at most xi_rho. Then the observed rational number

    r = max(0, min diag(D_rho) - a_rho - xi_rho)

is a valid lower bound on lambda_min(rho_bar) on that simultaneous confidence event. If r>0, Rbar_ij>=g I with g=kappa r. A finite bank may produce r=0 and abstain. This is a measured lower confidence bound on the bank's actual average occupation, not a supplied stationary source floor, and the occupation need not remain full rank after calibration.

## 2. Sharp two-gap sign perturbation, with a short proof

Let Delta=B R be Hermitian, B²=I, R>=g I for g>0, and [B,R]=0. Let C be any Hermitian approximation with ||C-Delta||op<=e. Let h=min |eig(C)|, and S=sign(C), assigning sign(0)=+1. Then

    ||S-B||op <= min(2, 2e/(g+h)).                     (S1)

If h=0, the same formula holds with denominator g. In particular, if e<g, Weyl's inequality gives h>=g-e and

    ||S-B||op <= 2e/(2g-e).                            (S2)

Proof: put P_+=(I+B)/2, Q_+=(I+S)/2. On the true positive and estimated negative subspaces, X=P_+ Q_- solves the Sylvester equation

    Delta_+ X - X C_- = P_+(Delta-C)Q_-.

The spectra obey Delta_+>=g I and -C_->=h I. The convergent integral solution therefore has norm at most e/(g+h). The complementary cross block P_-Q_+ obeys the same estimate (including a possible zero eigenspace in Q_+). For orthogonal projections,

    ||P_+-Q_+|| = max(||P_+Q_-||,||P_-Q_+||).

Multiplying by two proves (S1). This avoids a dimension-dependent Frobenius-to-operator conversion and the unnecessary 2e/(g-e) bound. The statement is an upper perturbation bound, not a claim of globally optimal constants for every spectral configuration.

## 3. Exactly rational physical signs and a stronger direct-gap branch

Use the received rational Jacobi primitive only on the KNOWN empirical signed matrix. It produces rational exactly unitary Q_j and rational diagonal D_j with

    C_j=Q_j D_j Q_j†,
    ||C_j - empirical_Delta_j||F <= xi_j.

Define S_j=Q_j diag(sign D_j)Q_j†. This is an EXACT rational Hermitian unitary on every possible record, including zero/repeated labels. Its known control synthesis remains paid. Set e_j=a_j+xi_j and h_j=min_l |(D_j)_ll|, an exactly known rational quantity. The unsigned certificate yields the data-computable uniform generator bound

    s_j <= min(2, 2e_j/(kappa r+h_j))                 (S3)

when r>0. The simpler sufficient test uses e_j<kappa r and (S2).

A strongest equally informed conventional procedure can also use the SIGNED GAP DIRECTLY. If h_j>e_j, then the true Delta_j is invertible and min|eig Delta_j|>=h_j-e_j. Since Delta_j=B_j Rbar_j with Rbar_j>=0 and commuting B_j, sign(Delta_j)=B_j and Rbar_j=|Delta_j|. Thus

    ||S_j-B_j||op <= 2e_j/(2h_j-e_j).                  (S4)

This supplies a sound acquired-gap certificate even when the separate unsigned confidence bound is inconclusive. No supplied kappa-dependent numerical floor is needed for (S4); the structural positivity/commutation assumption is still essential. The unsigned rho certificate remains a useful sufficient persistent-excitation condition and gives instance-dependent acceptance/sample guarantees through g>=kappa lambda_min(rho_bar). It should not be called information-theoretically necessary when signed data themselves show a gap.

## 4. Full-reference frozen extraction on general-width patches

Implement the received color-ordered three-controlled-reflection receiver, with fresh maximally mixed extraction ancillas and all physical registers retained until the blocks finish. Every S_ij above is physical independently of whether fitted generators satisfy Pauli relations. Let the acquired envelopes have the usual received cone multiplicity A=min(q,K²).

The existing full-reference colored receiver inequality is

    ell0_joint <= 3A sum_i(delta_iZ + delta_iX/2),
    delta_ij = Tr rho_future (S_ij-B_ij)².

An operator-norm certificate makes this STATE UNIFORM:

    ell0_joint <= 3A sum_i(s_iZ²+s_iX²/2).             (S5)

It holds for every future total gauge state, including arbitrary entanglement with retained source memory, because delta_ij<=s_ij² without an occupation assumption. If all s_ij<=s, then ell0_joint<=(9/2)Aq s². Choosing s²<=epsilon/(9Aq) gives nominal virtual extraction at most epsilon/2.

The same Bell-block POVM argument as the received on-site extension transfers (S5) to excess over ideal logical extraction; under CP identity dominance that extraction is the full-CPTP optimum at the same actual current memory. A single good-record/accepted-fit event works for all later memory states. Calibration-record TV therefore changes its probability once, even if imperfect training changes later memory occupation. The one future whole-q-input service discrepancy is separately paid. No payload need exist during training.

Soundness is a simultaneous high-probability confidence statement (or a joint accepted-risk bound), NOT a posterior assertion for every exposed accepted record. If the protocol abstains, its physical fallback may have order-one loss; an unconditional epsilon-risk claim requires an additional success/coverage promise or must charge the actual abstention probability. Neither source membership nor a future excitation floor is certified by passing the spectral test. Fixed true B and the future source-family assumptions remain necessary.

## 5. Genuine three-qubit repetition/majority example

Let a four-dimensional gauge label g index e_g in {000,100,010,001}. Define the eight-dimensional unitary permutation

    U|l,g> = |l*111 XOR e_g>.

On gauge 00 this is the ordinary three-qubit repetition encoding. General gauge states coherently label the no-error/single-bit-flip syndrome sectors. The exact full-space logical reflections are

    B_X = X1 X2 X3,
    B_Z = (Z1+Z2+Z3-Z1 Z2 Z3)/2.

The latter is the majority sign, and U† is reversible majority/syndrome extraction. These are genuinely width-three logical operators, not two on-site axes in disguise under allowed local controls.

Use identity logical Pauli noise (kappa=1). During calibration let the gauge be maximally mixed, giving

    rho_bar=I8/8,  Delta_X=B_X/8,  Delta_Z=B_Z/8.

Ordinary unsigned/signed shadows can therefore acquire a positive local gap. The learned exact signs feed the actual three-controlled-reflection extraction circuit and recover the logical input perfectly. After calibration the gauge may become any pure/mixed state, coherently correlated with memory; (S5) still applies. With exact signs, the receiver is exact on the full eight-dimensional subsystem and its output is independent of the gauge.

By contrast, gauge |00> throughout calibration produces a rank-two occupied output. The unsigned floor test correctly fails, and the true signed contrasts also have a kernel. The theorem does not claim that finite data from an unexcited subspace identify a hidden completion. Its advance is an ACTUALLY observed sufficient excitation certificate, not a free floor assumption.

## Independent deterministic evidence

The companion script checks (S1)--(S4) on noncommuting finite matrices, verifies the repetition permutation and exact majority/XXX identities, constructs rational approximate sign reflections with exact physicality, and evaluates the actual three-gate extraction's full gauge-uniform Bell operator. It also enumerates all 864 ordinary preparation/product-Pauli Born events for the full-support repetition training state and verifies both the unsigned and signed shadow identities; tests four future pure/coherent/mixed gauge states; and retains a maximally entangled gauge-memory purifier together with the complete logical reference, checking the exact decoder output is Bell tensor unchanged memory. Evidence is source-disabled exact algebra and floating matrix evaluation; there are no acquisition counts, source draws, RNG draws or production compiler timings. The code does not replace the ordinary martingale confidence proof or the received colored-circuit proof.
