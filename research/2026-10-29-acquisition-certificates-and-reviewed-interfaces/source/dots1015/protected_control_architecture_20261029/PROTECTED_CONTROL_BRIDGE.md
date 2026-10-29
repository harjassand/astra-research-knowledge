# Endpoint symmetry is not continuous protection; a conditional protected buffer port

2026-10-29. Author derivation with executed finite checks. Independent review requested, not yet received. This is a scoped obstruction and conditional architecture, not a working device or historical novelty claim. The accepted learning/guard results remain unchanged.

## 1. Exact endpoint-to-control obstruction

Use four spins, hbar=1, unit exposure duration, P the total-spin-zero projector, and |0_L>=|s_12>|s_34>. Consider a perfectly deterministic memory-free source with H0=pi Z_1. Its completed unitary exp(-iH0)=-I. Therefore its completed channel is exactly identity, all candidate-frame commutator losses vanish, and all endpoint singlet/matching tests pass. This includes complete endpoint tomography: the microscopic generator is not identifiable from this endpoint channel.

Apply an exchange control Hc=theta S_12 *during* that same interval, theta=pi sqrt(5)/2. The controlled source is exp[-i(H0+Hc)], not exp(-iH0)exp(-iHc). In pair12's opposite-spin span (|01>,|10>), Z1=Z, S12=X, so r=sqrt(pi²+theta²)=3pi/2 and the propagator is i(pi Z+theta X)/r. Since X|s>=-|s>, Z|s>=|t0>, its output on |s> is

    i(2/3)|t0> - i(sqrt(5)/3)|s>.

Tensoring unchanged |s34>, the first term has total spin1 and the second total spin0. Leakage is exactly **4/9**, whereas intended exchange only gives a phase on |0_L>. An actual leakage measurement distinguishes the controlled operation from the target with probability difference4/9; hence its half-diamond distance is at least4/9 on the encoded domain. The completed source alone is flawless.

This does not contradict the accepted endpoint full-memory symmetry promise. It proves that promise alone is insufficient to promote learned endpoint fixed points to an instantaneous collective Hamiltonian, even with zero source memory. Tests of the *actual completed controlled instrument* can detect the failure; tests of the idle source cannot. Variable-duration acquisition needs its own accessible timing/generator assumptions and statistical guarantees; finite samples do not alone prove an operator-uniform future generator bound.

## 2. Exact continuous protected-control contract

A sufficient, substantially stronger physical contract is

    H(t)=I_D tensor H_M(t)+sum_a J_a^V tensor B_a(t)
         +sum_(ij) g_ij(t) S_ij^V tensor I_M,
    J_a^V=V J_a V†, S_ij^V=V S_ij V†, P^V=V P V†.

All spins sharing these terms, including active buffer/control spins, must obey the SAME collective frame and bath algebra for the entire interval. Allow arbitrary finite-dimensional memory, noncommuting time-dependent B_a and H_M, and initial data-memory-reference correlations supported on P^V. All generators are bounded integrable (extensions require domain conditions).

Because J_a^V P^V=0 and [S_ij^V,P^V]=0, the exact propagator restricted to P^V tensor M is U_c(t)|P^V tensor U_M(t). Thus logical gates and storage are immune to these collective terms throughout the pulses, not merely at endpoints. No bath reset or environment reconstruction is needed. This is standard DFS exchange machinery specialized to this port, not new universal computing.

Native lab exchange is usually S_ij, not S_ij^V. Defining rotations by V_i sigma^a V_i†=sum_b (R_i)_(ba) sigma^b, the required interaction is

    S_ij^V = [I+sum_bc (R_i R_j^T)_(bc) sigma_i^b sigma_j^c]/2.

Learning R_i R_j^T provides coefficients, not hardware implementing the anisotropic interaction. Local pre/post frame pulses synthesize its endpoint unitary only if their own noise windows are accounted for; they do not make their Hamiltonians commute with the bath. A common unknown global rotation is irrelevant to these relative coefficients. Endpoint loss minimization does NOT certify accurate microscopic coefficients, by Section1.

## 3. Actual one-block logical operations

Use the previously retained four-spin singlet basis (psi0 above, psi1 as in the Bell encoder). Direct restriction gives

    S12|P = -Z_L,
    S23|P = Z_L/2 + sqrt(3) X_L/2.

Hence simultaneous native exchanges Hc=g(S12+2S23) implement sqrt(3)g X_L exactly, and S12 implements -Z_L. Both positive exchange strengths suffice for these two axes; pulse duration/sign/periodic phase conventions must be calibrated. This supplies explicit finite X/Z rotations, not just a Lie-universality slogan. Every intermediate state remains in P. Arbitrary spin-independent amplitude errors in g preserve P but create logical coherent errors: collective immunity does not suppress calibration error.

Within P, measuring pair12 singlet versus triplet is exactly logical Z. Given a genuine nondemolition measurement of this pair observable, a subsequent conditional logical X resets the encoded block to psi0. This reset is a physical measurement/feed-forward instrument, not a free unitary. A meter Hamiltonian proportional to (I-S12) tensor X_meter commutes with total spin and realizes a conditional pointer flip at calibrated duration; its spin-spin-meter interaction, readout, isolation and reset must be acquired. Merely measuring code occupancy does not provide this logical measurement.

Initial psi0 may come from two supplied singlet pairs. Projecting two pairs of independent maximally mixed spins onto singlets succeeds with probability1/16; this is a heralded preparation model, not a deterministic available singlet factory. Exchange-only unitaries preserve Tr(P_J rho) for EVERY total-spin sector, so cannot initialize an arbitrary register into P. Loading an unknown raw qubit into the logical code remains a separate quantum interface. Preparing known logical states inside P is not an encoder for unknown quantum input. The existing 8-CNOT encoder still has its stated trusted-control boundary.

For several blocks, intra-block exchanges preserve every block's singlet sector. Cross-block exchange preserves global spin0 but need not preserve product-block code; an entangling logical gate needs an actual leakage-returning compiled sequence, not an assumed primitive. Global collectivity across blocks is stronger than separate independent collective baths: cross-block exchange generally fails the latter protection contract. We do not supply a universal inter-block compiler or fault-tolerance threshold here.

## 4. Quantitative error allowance, independent of collective bath strength

Let the ideal Hamiltonian satisfy Section2 and actual controls differ by bounded DeltaH(t), including residual anisotropic-control errors. Unitary Duhamel gives

    ||(U_actual-U_ideal)(P^V tensor I_M)|| <= integral ||DeltaH(t)|| dt = eta.

Therefore half-diamond error on the encoded input (retaining all memory/reference) is at most min(1,eta). This compares the SAME bath in the two evolutions and does not require a bound on collective B_a. It does require the actual residual bound; endpoint source tests do not supply it.

For exact local frames A_i,A_j versus implementation B_i,B_j, put E_i=A_i†B_i, E_j=A_j†B_j. If the SO(3) angle of E_i E_j† is phi in[0,pi], then

    ||S_ij^A-S_ij^B||=2 sin(phi/2).

Proof: conjugate by A, use S(E_i† tensor E_j†)=(E_j† tensor E_i†)S, so the difference norm is ||E_i E_j† tensor E_j E_i†-I||. Its eigenvalues differ from1 by0,0,e^(i phi)-1,e^(-i phi)-1. Thus pulse H=g S pays eta<=2 integral|g| sin(phi/2), with triangle sum for multiple edges, plus amplitude/controller perturbations. This is a worst-case sufficient budget, not a measured error or a threshold.

## 5. Current Astra and matched alternatives

Astra U1041-collective-su2-control-interface was searched/fetched first at revision394818cd9b79c8b2bece2ec073e2d55dded660bc, content6cbb7fb0b04a3f6abd1da67f21a68790dffead632b92c01df16e9b158490f52a. Governing DECOHERENCE_FREE_COHERENT_CHECK_FLAG.md SHA c5dca84b0bd857dfee66c09f1f32124126b8090269f10db4839641127c177e24, lines60–131 and133–171 fetched along with all current corrections. Its accepted conditional three-spin subsystem port requires a singlet-controlled target interaction; instantaneous one-flag-spin/target two-body cross controls cannot provide it. This restricted no-go is not a no-go for globally collective exchange on encoded targets. But changing to encoded targets shifts preparation/gate/readout resources, not a free resolution. This note does not transfer its accepted-forbidden-effect quartic bound.

Primary source: Kempe, Bacon, Lidar, Whaley, arXiv:quant-ph/0004064v2, SectionsIV,VII,VII.5 andIX: https://arxiv.org/html/quant-ph/0004064. Exchange-only DFS computation, singlet initialization and measurement are established antecedents. An equally informed conventional exchange-only DFS controller has exactly the Section2–4 capabilities. Our current learned endpoint frame theory adds neither an acquired instantaneous noise algebra nor an advantage over that controller. No historical novelty claimed for this architecture or Duhamel bound.

Potential experimental architecture, not a premise: Sala and Danon, arXiv:1702.01650v2, https://arxiv.org/abs/1702.01650, electrical four-dot singlet-only initialization/manipulation/readout proposal. Its finite physical noise and energy-gap assumptions cannot be replaced by unbounded arbitrary unknown local noise. No laboratory tests performed here.

## Reproduction and next load-bearing obligation

Run python check_control_bridge.py (NumPy,SciPy); check_control_bridge.json records exact-example numerical audit, shared noncommuting bath factorization and relative-frame norm identity. The analytic proof carries the exact4/9 value. The finite tests do not establish a hardware control bound.

Next genuine bridge: acquire or certify a *family of completed controlled instruments* while learning a useful protected encoding, with direct operational error budgets for preparation, finite pulses, measurement and buffers. This preserves environment-free learning but must not infer intervening symmetry from idle endpoint symmetry. Alternatively supply and calibrate a microscopic collective/control compatibility promise, which is a narrower physical architecture. These are materially different mechanisms.

## 6. Independent-bath block architecture: minimum protected cross-control support

There is a second concrete architectural separation. Suppose each four-spin block A,B has its own arbitrary collective bath, with independent generators J_a^A and J_b^B. To enjoy unbounded-strength instantaneous protection by symmetry, a cross-control must commute with both local SU(2) actions. Any Hamiltonian supported on at most three physical spins, with support intersecting both blocks, has at most one spin in one of those blocks. Its nonidentity operator on that lone spin transforms as the vector representation, which contains no scalar. Independent SU(2) invariance therefore forces all genuinely cross-block terms to vanish. Linear combinations cannot help: local Pauli strings on distinct supports are independent. This is a restricted local-Hamiltonian commutant obstruction, not a no-go for finite-noise compiled/mediated controls or higher-body effective interactions.

Four-spin cross control does suffice algebraically:

    H_AB = kappa S12^A tensor S12^B,
    H_AB restricted to P_A tensor P_B = kappa Z_L^A Z_L^B.

It commutes with both blocks' collective algebras. Together with Section3's intra-block X/Z controls it supplies the *algebraic* protected entangling primitive under independent block baths. It expands into a genuine four-spin interaction plus local and scalar terms. A supplied direct four-body coupling, or an explicitly modeled mediator that couples to each pair exchange observable, is required. Ordinary exchange across a boundary is not this interaction. An effective four-body Hamiltonian derived by eliminating a mediator needs finite-gap/truncation/mediator-noise bounds and all occupied charge/spin sectors charged. This resource is presently unacquired.

This extends the restricted N1041 one-flag-spin/target control obstruction to the precise block architecture, by the same standard representation argument. It identifies the missing operation rather than claiming to synthesize it. A strong conventional encoded-spin controller supplied the same coupling obtains the same gate.

The Sala–Danon full primary manuscript was additionally inspected at https://arxiv.org/html/1702.01650v2, lines52–94 (Hubbard model, qubit projection, initialization/read-out). It provides a concrete spin-to-charge readout and relaxation-based singlet initialization proposal, with orbital splitting and finite-speed spin-flip conditions. It does NOT discharge the unknown-frame anisotropic native-control or independent-bath four-body interface here.
