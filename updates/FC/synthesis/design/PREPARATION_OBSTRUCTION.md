# Fixed charge and local stationarity do not acquire Gibbs sector weights

Internal exact countermodel and perturbative access bound, 13 October 2026.
This refutes a named acquisition transfer, not the submitted equilibrium theorem.
The ingredients are elementary conserved blocks, free-energy Lipschitz bounds
and Duhamel/operational hybrid arguments. Novelty and physical consequence
remain unestablished.

## 1. Access and target must be distinguished

Suppose preparation returns one stationary sector, and legal observations,
controls, adaptive feedback and resets act only on the local subsystem A.
Neither the full bath Hamiltonian nor populations in an inaccessible conserved
bath block are supplied. The target is the canonical free-energy change
traced over the declared charge sector, not a conditional metastable free
energy in an extra hidden sector.

Under this access, even arbitrary exact local multi-time data and fixed charge
do not certify that the observed histogram is the intended Gibbs histogram.
The obstruction below already uses density-density two-body interactions and
four fermion modes, rather than the growing-body-order construction in N786.
Its legal access contract is different from N786's vacuum spectroscopy.

## 2. Exact same-charge countermodel

Take fermion pairs (d,e) and (b,c), restricted to conserved charges

    n_d+n_e=1, n_b+n_c=1.

Thus all four logical states have total particle count two. Let n=n_d and
s=n_b. At beta=1 compare two possible reference Hamiltonians

    H_+=-10 s+10 s n,
    H_-=-10 s+10 s(1-n).

The intended intervention is the same local diagonal shift

    V=I/2-n.

The prepared state is

    rho_prep=(I_A/2) tensor |c><c|,

so s=0, the local histogram is exactly (1/2,1/2), and the state is stationary
for BOTH references. Both have T=0 with respect to the measured n label,
the same perfectly known coherence budget C=1 and kinetic expectation zero.
Every A-only controlled experiment, including arbitrary adaptive sequences,
has exactly the same outcome law in the two models: s stays zero and both
Hamiltonians restrict there to zero. Arbitrary accuracy, long observation
and stationary repeats cannot distinguish them under this access.

Nevertheless the global-sector Gibbs decisions have opposite signs. Put
E=exp(10) and e=exp(1). Both reference partition functions are E+3. Their
target/reference partition ratios are

    R_+=exp(-1/2) (E+1+2e)/(E+3),
    R_-=exp(-1/2) (Ee+2+e)/(E+3).

Using 8/3<e<3, 7/5<sqrt(e)<7/4 and E>1024 gives

    R_+<(5/7)(1031/1027)<3/4<exp(-1/4),
    R_->(4/7)(8/3)(1024/1027)>4/3>exp(1/4).

Therefore DeltaF_+>1/4 and DeltaF_-<-1/4. The elementary inequalities
exp(1/4)<4/3 and exp(10)>1024 follow from Taylor bounds or exp(1)>2.
This is an exact sign and margin argument, not a floating diagnostic.

A data-only binary chooser cannot be correct on both; its equal-prior average
success is at most 1/2. Abstention is valid. Applying the source histogram
formula to rho_prep would give the same answer in both models and can be
wrong because its Gibbs premise is violated.

If the physical task instead includes the extra constraint s=0, the measured
state IS Gibbs in that more restricted ensemble. The source theorem then
applies to that conditional output. Silently changing the ensemble is the
invalid transfer. Fixed total charge alone does not select all hidden blocks.

## 3. Weakly broken conservation does not give a free fast remedy

Add the common number-conserving bath tunnelling perturbation

    epsilon X_B=epsilon(b^dagger c+c^dagger b), epsilon>0.

Its norm is epsilon in the declared sector. The free-energy change for either
model moves by at most 2epsilon, by the 1-Lipschitz operator-norm bound for each
of the two free energies. For epsilon<1/16, both signs retain margin>1/8.
The measured n label still has T=0 in the reference Hamiltonian: bath
tunnelling preserves it. None of this establishes inexpensive equilibration.

For any A-only adaptive protocol with total Hamiltonian interaction time t,
the perturbed and unperturbed outcome laws differ in total variation by at
most 2epsilon t (a deliberately conservative constant). Between the two
candidate perturbed models the unperturbed laws coincide, hence their TV
distance is at most 4epsilon t. Each segment follows from
||U_epsilon(t)-U_0(t)||<=epsilon t; interleaved instruments are contractive,
and a hybrid/telescoping argument sums the segment times. Arbitrary fast
A-only controls do not alter the norm of the bath perturbation.

Equal-prior binary success is at most (1+4epsilon t)/2, capped at one.
Success at least 2/3 therefore requires t>=1/(12epsilon). This is an access
time lower bound for the stated restricted experiments, not a universal
classical/quantum complexity theorem or a claim about an apparatus that can
directly reset, inspect or control B. Such an extra operation changes the
contract and must be acquired and charged.

## 4. Consequence for the research gate

The new positive histogram theorem genuinely changes from passive bare-bath
information to the loaded equilibrium distribution. It evades the N786
vacuum-information obstruction by obtaining different information, not by
proving that low-order bath data was sufficient. N778 correctly fixes charge
for the target; that does not by itself prepare Gibbs weights inside that
charge sector. N779's comparison witness likewise is not an equilibration
actuator or certificate.

A concrete continuation must justify either the intended equilibrium law or
a quantitative discrepancy of the acquired LOCAL histogram from it. Full
state tomography is not required by the positive theorem. But stationarity,
independent repeats inside one trapped block, and perfect readout do not
supply that discrepancy. Independent check code builds both charge sectors,
verifies the exact formulas, and tests small common symmetry breaking.
