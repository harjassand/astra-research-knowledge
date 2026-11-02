# Native two-body thermal memory: independent construction pass

Date: 2026-11-01. This direction was developed before reading any parent route files. No parent route files were read. Status: an exact algebraic reduction and a concrete remaining finite-temperature lemma; **not a completed thermal-memory theorem**.

## 1. Main result of this pass

A quantum clock-loop gadget admits an **exact finite-depth local dressing on the entire Hilbert space** under which its data dependence is only through the original commuting Pauli stabilizers. This handles cross-gadget noncommutation algebraically rather than discarding it. Real ancilla excitations remain in an explicit quantum ancillary partition function. The remaining obstacle is a volume-uniform, syndrome-uniform low-temperature linked-cluster bound on that partition function, and its use in the existing logical-fault witness proof.

This is materially stronger than computing a low-energy effective Hamiltonian. It does not yet prove the required bound.

## 2. An early exact thermal construction that fails

For one check S=product_i P_i, introduce one 2^k-dimensional classical ancillary spin with commuting labels Z_i. The two-body-plus-onsite Hamiltonian is

    H_g = -Delta sum_i P_i Z_i - J product_i Z_i.

Its full partial partition function is exactly

    Tr_g exp(-beta H_g)
      = (2 cosh(beta Delta))^k cosh(beta J)
        [I + tanh(beta J) tanh(beta Delta)^k S].

Thus tanh(beta J_eff)=tanh(beta J)tanh(beta Delta)^k. No all-ancillas-ground assumption is needed.

But this does NOT compose for quantum checks. For multiple gadgets, all ancilla labels remain classical. Conditioned on those labels, the data Hamiltonian is a sum of independent one-site fields, even if different checks use X and Z at a shared site. Its Gibbs state is therefore a mixture of data product states, with classical ancillas. One-check thermal identities cannot be multiplied across noncommuting overlaps. This falsifies this tempting route, not all native two-body models.

## 3. Positive mechanism: bounded-dimensional quantum clocks

Let S_g=product_{i=1}^K P_{g,i}, where each P is a single-site Hermitian Pauli or identity. Pad checks with identities to a common K=7. Each original check has bounded diameter and each data site meets boundedly many checks.

Place one K-level spin a_g near each check and define

    H_nat = Delta sum_g (I-|0><0|)_g
      - t sum_{g,i=1}^K [ |i mod K><i-1|_g P_{g,i} + h.c. ].

Nonidentity hops are two-body (one data spin and one ancillary spin). Identity hops and the penalty are onsite. Ancilla dimension, density, degree, and geometric range stay bounded. Delta,t,beta can be constants independent of volume. 'Native' here permits arbitrary Hermitian couplings between a qubit and a fixed seven-level spin; restricting to a particular spin-exchange interaction is a separate engineering constraint.

### Exact dressing

For q=0,...,K-1 define prefix F_g(q)=product_{i=1}^q P_{g,i}. Choose an order on gadgets using a bounded coloring of their overlap graph, and let

    U = sum_{all q} |q><q| tensor [ordered product_g F_g(q_g)].

Each controlled F_g is local and commuting disjoint gadgets can be executed together. Thus U is a bounded-depth, bounded-range circuit, independent of system size. U need not be physically executed during storage; it defines the encoding/decoding and dressed logicals.

Consider an elementary clock transition q->q' at gadget g. Its transformed data label is

    F(q')^dagger P_{g,i} F(q).

Pauli factors from other gadgets can be commuted past this expression at a cost only of scalar signs depending on their clock labels. The remaining factor is I for a nonwrapping step and S_g for a wrapping step. Consequently

    U^dagger H_nat U = sum_s P_s tensor H_a(s),

where P_s are joint stabilizer eigenspace projectors. H_a(s) is a bounded-degree, finite-range ancillary Hamiltonian with onsite gap Delta and signed clock hopping of strength t. Signs encode all shared-data noncommutation. They involve only overlapping gadgets. There is NO approximation in this equation.

In particular H_nat commutes with the dressed stabilizers U S_g U^dagger and with all dressed code logical operators U L U^dagger. This statement includes every excited ancillary level. It is not a ground-band conservation law.

The stabilizer sectors may obey dependencies; the equation is simply restricted to allowed s. Every allowed stabilizer sector has the same data dimension, including its logical degeneracy.

### Bath locality and logical correctability

Conjugating a native local bath operator by U enlarges its support by a fixed amount. Any error supported on a small physical region is therefore a bounded-support error in the dressed data-plus-ancilla frame. Correctability should be stated for dressed logicals and this enlarged local domain, not bare data logicals. For a Davies decomposition, Fourier projection under H does not create new allowed syndrome changes: each nonzero block still has the syndrome-change pattern allowed by the original local operator. Rates and sums of jump strengths still require the hypotheses of the existing thermal-memory theorem.

This does not by itself show that ancilla-mediated motion cannot catalyze a logical error. That is precisely what the Gibbs crossing witness must rule out.

## 4. Full-temperature quantity that must be controlled

Define exactly, with no projection,

    Z_a(s)=Tr_all_ancillas exp[-beta H_a(s)],
    F_beta(s)=-(1/beta) log Z_a(s).

For every syndrome event B,

    Tr[(sum_{s in B} P_s tensor I_a) exp(-beta U^dagger H_nat U)] / Z_nat
      = sum_{s in B} Z_a(s) / sum_{allowed s} Z_a(s).

Thus the precise target is a **local interaction expansion of F_beta**, not a global partition-function approximation and not a statement about total probability of ancillary vacuum.

For an isolated clock, the two oriented minimal winding paths give leading

    F_beta(s) = constant - J_eff s + ...,
    J_eff -> 2 t^K / Delta^(K-1) at beta Delta >> 1.

A closed hopping word has data dependence only through products of S_g corresponding to clock windings. A nontrivial dependence on s_g requires at least K hops of g. Nonwinding virtual excursions may be numerous and extensive, but their syndrome-independent free energy cancels from witness ratios. Connected cross-gadget winding clusters generate genuine multistabilizer corrections; they must be bounded, not ignored.

### Remaining lemma (unproved here)

For bounded overlap degree, sufficiently small epsilon=t/Delta and sufficiently large beta Delta, prove uniformly over volume, arbitrary allowed flux configurations s, and relevant local boundary modifications:

    F_beta(s) = c_beta - J_eff sum_g s_g + sum_A r_A(beta) product_{g in A} s_g,

with an exponentially weighted local interaction bound on the remainder small compared with J_eff. A plausible sufficient form, NOT established by the algebra alone, is

    sup_g sum_{A contains g} |r_A| exp(mu diam(A))
      <= C Delta (C'epsilon)^(K+1) + C/beta exp(-c beta Delta).

The leading one-check coefficient can instead be calibrated using its exact isolated-clock free energy. The important requirement is relative smallness of all connected syndrome-dependent corrections, not any particular loose power above.

Why this looks more tractable than generic gadget thermal transfer: at fixed syndrome the unperturbed ancillary Hamiltonian has a UNIQUE product vacuum and an onsite gap. The code's extensive degeneracy is now external classical flux data, not a degeneracy inside the cluster-expansion reference problem. Absolute activities can be bounded uniformly in the signs. A low-temperature quantum contour/linked-cluster method is the natural tool. Standard high-temperature bounds in beta*t are inappropriate, because beta J_eff must be large and therefore beta*t is huge.

A cited low-temperature expansion must actually cover nontranslation-invariant, syndrome-dependent finite-range hopping and yield local free-energy potentials uniformly in external flux. A ground-state analyticity theorem alone is insufficient.

## 5. How a successful lemma would transfer the witness

Suppose the existing target witness argument admits small exponentially decaying classical stabilizer interactions in the above weighted norm. Apply it to the exact syndrome weights exp(-beta F_beta(s)). Each local erasure/repair comparison changes only interactions meeting the witness neighborhood; locality cancels all far-away free energy. The extra logarithmic ratio is proportional to witness size, not total volume. Therefore a positive contour tension remains positive when the local remainder is sufficiently small relative to J_eff.

The decoded microscopic bath acts on bounded support, so the logical crossing region is only thickened by a constant. The exact quantum block decomposition supplies the required Gibbs probability of that region. One must then invoke/prove the quantum dynamical rare-fault inequality under the actual bath assumptions and initial thermal encoding. Equilibrium sparsity by itself is not a lifetime theorem.

This route never asks for no excited ancillas globally. At fixed beta Delta there are an extensive number in a large volume; their connected free-energy contributions and local error effects are what enter the proof.

It also never multiplies a finite-order Hamiltonian simulation error by the desired exponential lifetime. Dressed logical conservation is exact, and the remaining comparison is thermodynamic/local.

## 6. Minimal independent numerical check

`check_clock.py` exactly diagonalizes two overlapping commuting checks XX and ZZ, each padded with an identity to a three-state clock. Hilbert dimension: 36. At Delta=1,t=.08:

- U is exactly unitary in floating-point arithmetic for this signed-permutation case.
- Both transformed stabilizer commutator norms are zero.
- Full-spectrum free energies at beta=100 and 1000 give J_X=J_Z=0.00097997812719.
- Leading isolated-loop prediction is 0.001024.
- Cross coefficient J_XZ=-0.00000283026104.

This checks the algebra and exhibits nonzero cross-gadget corrections. It does NOT establish volume-uniform convergence or lifetime. It uses K=3 only to keep the check small; the symbolic construction handles K=7.

## 7. Strong established alternatives, same resource accounting

1. **Bounded-strength SW gadgets:** the stipulated Bravyi–DiVincenzo–Loss–Terhal 2008 result is an essential baseline. It already defeats the claim that all useful extensive approximations need size-growing strength. What it does not automatically supply is this full-spectrum syndrome free-energy statement.

2. **König clock/hopping gadgets:** [Simplifying quantum double Hamiltonians using perturbative gadgets](https://arxiv.org/abs/0901.1333) develops hopping constructions realizing ordered products in a low-energy limit. The clock principle here is not claimed novel. Its suitability for arbitrary commuting Pauli checks plus exact full-space dressing and finite-temperature witness transfer is the question to audit.

3. **Ocko–Yoshida nonperturbative gadgets:** [Nonperturbative Gadget for Topological Quantum Codes](https://arxiv.org/abs/1107.2697) is a stronger comparator than generic SW: it supplies exactly solvable two-body toric/quantum-double realizations, exact degeneracy and localized excitations. Their stated construction is specialized to those models. Generalization to the present three-dimensional memory family and a finite-temperature rare-logical-fault proof are not consequences of its abstract. It should be examined for shielding terms that eliminate the clock cross couplings altogether.

4. **PEPS parent gadgets:** [Brell–Bartlett–Doherty](https://arxiv.org/abs/1407.4829) establishes perturbative two-body parent constructions and ground-space phase properties. This is not an established finite-temperature transfer for the target memory.

5. **Universal simulation with thermodynamic guarantees:** [Cubitt–Montanaro–Piddock](https://arxiv.org/html/1701.05182v4), Proposition 28, explicitly controls partition-function error. Its bound contains high-sector entropy and a global approximation error. Without further local structure, maintaining a useful uniform estimate generally requires volume-dependent cutoff/precision; it is not the sought fixed-ratio witness comparison. Its time-evolution error likewise grows with time, which cannot be used freely for exponential memory time.

6. **Thermal-phase channel transfer:** [Ma–Khemani–Sang, v3](https://arxiv.org/html/2509.15204v3) provides finite-temperature channel and memory consequences under stable clustering along an appropriate path. It is potentially the strongest general alternative once its hypotheses hold. But a low-energy gapped path does not prove stable clustering of the entire native Gibbs state. Verifying that path across the microscopic gadget regime is an alternative formulation of the remaining thermal obstacle, not a free corollary.

7. **Low-temperature quantum contour technology:** [Borgs–Kotecky–Ueltschi](https://web.ma.utexas.edu/mp_arc-bin/mpa?yn=95-233) and subsequent quantum Pirogov–Sinai work are the relevant technical family for the flux-uniform ancillary expansion. Applying them requires checking their hypotheses and extracting the particular local-potential estimate above. I have not completed that application.

## 8. Honest conclusion

The independent construction delivers a real algebraic advance over generic low-energy gadgets: exact full-spectrum stabilizer/logical conservation after a local encoding, with native two-body microscopic terms, bounded resources, and explicit handling of shared-data noncommutation. It reduces the hard thermal implementation problem to a specific ancillary quantum cluster-expansion lemma plus the existing dynamical witness transfer. It does not yet close that lemma. The right next attack is to prove it or find a flux-dependent low-temperature instability that falsifies it—not another table of gadget parameters.
