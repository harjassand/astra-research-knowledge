# Bell analyzer audit: conclusive cycling, physical return, and primary comparisons

Prepared independently for the main investigation. This note reads the existing
`p2_spin_interface/DERIVATION.md` as the candidate physical primitive and changes
no earlier branch. No historical novelty or device advantage is asserted.

## Result

Sequential singlet tests with intervening spin rotations are established Bell
analyzer architecture [1,2]. The useful additional statement available from the
qualified Hubbard/charge interface is a finite, retained-electron, complete
instrument theorem: cycle all four *conclusive* Bell tests, label the final
unresolved record as abort, and physically return every captured pair before
claiming that it is reusable. The residual ideal-charge error is proportional to
the failure probability, rather than its square root, even for noncommuting
retained memory.

## 1. Precise conclusive-cycle theorem

Let P_0,...,P_3 be the four mutually orthogonal Bell projectors. For each j there
is an implemented local Pauli U_j satisfying U_j P_j U_j^dagger=P_s. Before a
source test apply U_j; after an unsuccessful test with verified separated charge
11 apply U_j^dagger. On a captured branch, resolve the double site, return the
pair to 11 using the physical release protocol, and only then apply U_j^dagger
if preservation of the measured Bell state is required.

In the ideal-charge comparator, the complete no-capture isometry for test j is

    F_j = (I-P_j) tensor B_j + P_j tensor A_j,
    B_j^dagger B_j = I,       ||A_j|| <= r < 1.

All fine source, charge, and time records can be included in the output memory.
There may be multiple physical Kraus operators; stacking their records gives
the displayed isometry. B_j and A_j can act on arbitrary retained memory and
need not commute with any previous or subsequent factor. They may also depend
on earlier records, provided the same norm bound holds on every admitted input.

Every conclusive capture history, followed by successful return and the inverse
local Pauli, has the form

    P_j tensor C_{j,h}.

There is no accepted amplitude of another Bell state. In particular, the physical
click must mean capture, not a raw finite detector no-click/click distinction.
Finite charge classification is dealt with separately below.

Perform K complete cycles of tests 0,1,2,3, stopping testing at the first
conclusive capture. A whole no-capture cycle is block diagonal in the *same*
Bell basis:

    F_3 F_2 F_1 F_0 = sum_j P_j tensor M_j,
    ||M_j|| <= r.

Each word M_j contains one on-target A factor and three contractions B. No
commutation of memory factors is used. Hence the all-null isometry after K
cycles has norm at most r^K and its effect is at most

    q I,                    q = r^(2K).

At the cap, output an explicit ABORT. Do not infer the fourth Bell label from a
finite no-capture record.

Suppose the selected captured pair has a uniform return success probability at
least 1-b, using the capped, site-resolved return primitive. For the existing
primitive, b=(1-p_return)^R for R release windows. Stack all histories that
successfully produce label j and restore its two separated spins into E_j.
Completeness and the failure bounds give

    (1-q)(1-b) I <= E_j^dagger E_j <= I.

Let

    d = 1-(1-q)(1-b) <= q+b,
    Etilde_j = E_j (E_j^dagger E_j)^(-1/2).

Etilde_j is a comparison isometry, not a physical inverse operation. The norm
distance is at most

    ||E_j-Etilde_j|| <= 1-sqrt(1-d).

The comparison instrument has successful branches P_j tensor Etilde_j and no
abort. It induces the exact Bell measurement on the spins even when their input
is correlated with memory and an arbitrary reference. Stack the successful
branches with orthogonal outcome flags. The operator distance of the stacked
success Stinespring maps is the maximum of the four sector distances, not their
sum. The success-channel contribution to half-diamond distance is at most
1-sqrt(1-d). The actual abort CP map has diamond norm at most d. Therefore

    epsilon_Bell^(0) <= 1-sqrt(1-d) + d/2 <= 3d/2.

The complete flagged process is close to the Bell instrument; this does not
assert uniformly small normalized error after arbitrary rare-record
postselection.

### Why the fourth conclusive test matters

If a finite no-capture record is instead called the final Bell label, its Kraus
operator contains both the surviving intended sector and residual amplitudes
of previously tested sectors. Their interference can be O(r^K). Cycling all
four targets and retaining a failure flag removes this coherent contamination
from every accepted branch. The remaining failure effect is O(r^(2K)), and the
polar-normalized complete-instrument bound is of that same order.

This is a conditional proof from the actual finite source primitive, not a
proposal to assume an ideal singlet jump.

## 2. Physical accounting

The elementary sequence is: verify 11; execute the qualified local Pauli;
pulse the spin-independent source; turn hopping off; classify n_L as 0,1,2.
If n_L=1, undo the Pauli and continue. If n_L=0 or 2, record the conclusive
Bell label, preserve the resolved double site, and perform the capped release
protocol. After return to 11, undo the Pauli if reusing the measured pair.

Site resolution is essential to the source's return proof: a coherent
unresolved double-charge dark state cannot be assigned the one-site return
bound. For Bell measurement or teleportation, resolving the occupied site
after a genuine capture is harmless to the Bell label, which is already rank
one. This fact is different from nondestructive parity measurement, where
resolving internal charge alternatives can destroy the required two-dimensional
coherence.

A common endpoint can be enforced by holding a captured pair until a shared
release block. With K four-test cycles and R release slots, the maximum number
of charge interrogations and source/release windows is

    Q = 4K+R.

There are at most 8K local Pauli applications under the simple apply/undo
schedule; identity applications can be omitted. Actual transport, switching,
meter renewal, record handling, and holding time must be counted.

The existing charge-QND detector has a complete-instrument comparator error
delta_ch <= sqrt(2 eta), where eta is its uniformly bounded classical
classification error. Replacing all perfect charge interrogations gives

    epsilon_Bell <= 1-sqrt(1-d)+d/2 + Q delta_ch
                    + epsilon_rotation/routing/holding/source-leakage.

Adding Q eta instead would fail to account for coherent charge contamination.

For illustration within the declared mathematical source box r=0.6,
p_return=0.3, choose target epsilon=10^-6, K=16, R=44, Q=108,
delta_ch=epsilon/(2Q), and the existing detector allocation of 160 long-setting
plus 57 short-setting probes per charge readout. This gives 23,436 probe slots,
q about 7.96e-8, b about 1.53e-7, and total displayed ideal-source plus allocated
sensor error below 7.33e-7. This leaves no implied numerical allowance for
unqualified spin noise. These numerical values were checked with ordinary
floating-point arithmetic; the analytic inequalities, not those decimals, are
the certificate. A formal integer/constant certificate could reuse the main
branch's rational enclosure methods if this becomes a deliverable.

## 3. Strongest directly relevant primary comparisons

### [1] Sequential blockade Bell analyzer: Yokoshi, Imamura, Kosaka (2010)

N. Yokoshi, H. Imamura, H. Kosaka, *Proposal of a full Bell state analyzer for
spin qubits in a double quantum dot*, Physical Review B 81, 161305(R) (2010).
DOI: https://doi.org/10.1103/PhysRevB.81.161305
Manuscript: https://arxiv.org/abs/1004.2758

The paper's Fig. 2 is directly matching prior art: measure singlet by blockade,
on null restore Coulomb blockade, rotate another Bell vector to singlet, and
repeat. Its T_+ and T_- denote (up up +/- down down)/sqrt(2), not polarized
triplets. The full text requires opposite g factors g1=-g2, biaxial ESR, and
waiting-time compensation. The arXiv abstract text as rendered by one search
endpoint drops the minus sign; use the full paper or publisher abstract.

The conclusive process drains an electron into a reservoir. A null record is
treated as exact singlet exclusion. Thus the paper establishes the architecture
but not the retained-electron, finite-strength, correlated-memory theorem above.
Retrieved full-text locations: Fig. 2 and text around Eqs. (5)-(6).

### [2] Free-electron Bell analyzer: Beenakker et al. (2004)

C. W. J. Beenakker, D. P. DiVincenzo, C. Emary, M. Kindermann, *Charge Detection
Enables Free-Electron Quantum Computation*, Physical Review Letters 93, 020501.
DOI: https://doi.org/10.1103/PhysRevLett.93.020501
Manuscript: https://arxiv.org/abs/quant-ph/0401066

Figure 1 supplies a full Bell analyzer with three 50/50 beam splitters, three
charge detectors, mirrors, and local Z and X rotations. Successive detectors
identify the singlet then rotated Bell states by bunching; the final label is
inferred from antibunching. The paper explicitly calls this measurement
destructive, so charge number or charge parity detection both suffice there.
The separate nondestructive spin-parity primitive uses polarizing beam splitters
and a parity-only charge detector. These require controlled scattering and
spatial-mode interfaces; the theorem does not provide arbitrary-memory source,
loading, or return bounds. The finite conclusive-cycle result should be compared
with this architecture as well as with the 2010 double-dot proposal.
Retrieved full-text locations: Fig. 1, Eq. (6), and the following parity-encoder
discussion.

### [3] Stationary spin parity: Engel and Loss (2005)

H.-A. Engel, D. Loss, *Fermionic Bell-State Analyzer for Spin Qubits*, Science
309, 586-588 (2005).
DOI: https://doi.org/10.1126/science.1113203
PubMed: https://pubmed.ncbi.nlm.nih.gov/16040700/

The primary abstract proposes a partial Bell/parity measurement in a double dot
with different Zeeman splittings and resonant tunnelling for antiparallel spins.
If a complete nondestructive parity instrument is actually supplied, two
commuting parity measurements ZZ and XX resolve the Bell basis; local Hadamards
convert the second to the first measurement basis. That inference is elementary
but it requires preservation of each two-dimensional parity sector, not just
the correct parity bit. Full text was unavailable in the paper index during
this audit, so no more detailed source/return guarantee is attributed to it.

### [4] Complete two-electron readout: Nurizzo et al. (2023)

M. Nurizzo et al., *Complete Readout of Two-Electron Spin States in a Double
Quantum Dot*, PRX Quantum 4, 010329 (2023).
DOI: https://doi.org/10.1103/PRXQuantum.4.010329
Manuscript: https://arxiv.org/abs/2209.00535

This experiment performs repeated readout/manipulation on the same two
electrons. It separates fast spin-to-charge conversion from readout by taking
the interdot coupling from GHz to sub-Hz, strongly supporting the physical
motivation for on-window/off-window sensing. But its complete basis is
S,T0,up up,down down. It uses a T0 relaxation hotspot and an S-T+ avoided
crossing to distinguish the latter states; it is not a four-Bell-vector
measurement and cannot be substituted for one without further coherent gates.
Retrieved full-text locations: Sec. II (frozen blockade), Sec. V and Fig. 3.

### [5] Direct conditional teleportation: Kojima et al. (2021)

Y. Kojima et al., *Probabilistic teleportation of a quantum dot spin qubit*,
npj Quantum Information 7 (2021).
Article: https://www.nature.com/articles/s41534-021-00403-4
Manuscript: https://arxiv.org/abs/2011.04881

The demonstrated 0.91 figure concerns spin polarization. Their input
preparation uses resonant SWAP with a temporary electron and subsequently
empties its dot; the paper explicitly states that this loses input coherence
while retaining up/down probabilities. Their latched readout loads another
electron, changing the blocked charge state (1,1,1) to (2,1,1). The singlet
resource is separated by a charge ramp, and singlet-triplet mixing and mapping
errors enter the discussion. These are concrete qualifications, not evidence
of complete arbitrary-state, retained-electron teleportation.
Retrieved full-text locations: preparation/readout section and discussion.

### [6] Conditional teleportation and entanglement swapping: Qiao et al. (2020)

H. Qiao et al., *Conditional teleportation of quantum-dot spin states*, Nature
Communications 11 (2020).
Article: https://www.nature.com/articles/s41467-020-16745-0
Manuscript: https://arxiv.org/abs/1908.08306

This four-dot experiment uses singlet-versus-triplet postselection, with
successful teleportation requiring the singlet outcome. It also studies
entanglement swapping. The authors explain that absent magnetic-resonance
control they cannot prepare arbitrary single-spin superpositions, and that
state/process tomography is needed to establish the stronger teleportation
fidelity claim. It is relevant conditional-teleportation evidence, not a full
Bell analyzer.

### [7] Deterministic coherent-gate comparator: de Visser and Blaauboer (2006)

R. L. de Visser, M. Blaauboer, *Deterministic Teleportation of Electrons in a
Quantum Dot Nanostructure*, Physical Review Letters 96, 246801 (2006);
erratum 97, 069901.
DOI: https://doi.org/10.1103/PhysRevLett.96.246801
Manuscript: https://arxiv.org/abs/cond-mat/0603464

The deterministic proposal compiles the Bell-to-computational basis operation
using two sqrt(SWAP) exchange gates and a local rotation, followed by spin
readout and corrections. It is a serious alternative when calibrated coherent
exchange and spin-axis readout are available; it does not establish the same
operator-valued, uninitialized-memory control guarantee.

## 4. Narrow check relevant to the newly selected flat-SOC route

M. H. Freedman, M. B. Hastings, M. Shokrian Zini, *Symmetry Protected Quantum
Computation*, Quantum 5, 554 (2021), https://arxiv.org/abs/2105.04649v3,
assumes Hamiltonian and noise terms invariant under a common SU(2). In its
physical electron/proton example it expressly assumes spin-orbit coupling can
be ignored. The retrieved physical-motivation passages do not state a global
flat-SOC / twisted-singlet extension. This is a scoped negative finding, not
evidence of novelty; the full flat-gauge literature was outside this Bell audit.

## 5. Remaining physical obstruction

More conclusive tests only amplify a valid rank-one capture instrument. They
do not fix spin-active leakage or a detector that resolves the wrong internal
degrees of freedom. Frozen charge readout with small residual hopping needs a
quantum error bound over the full readout duration. The source and detector
spectral boxes must remain valid after every retained history. Local rotations
must also have a complete joint-system bound; replacing a spin by an electron
newly loaded from a reservoir does not implement a unitary on its unknown
state. All these qualifications remain after the improved q=r^(2K) counting.
