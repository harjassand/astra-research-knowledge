An explicit Pauli-ring construction gives a two-body bounded-qudit endpoint
with the exact code logical multiplicity and gap at least3/4 uniformly in
system size. A local path retains the code coefficient while turning off
clock hopping, and stays uniformly gapped. This is a positive ground-phase
transfer with fixed overhead/penalty in N, not a whole-band simulation.

The stronger full-Hamiltonian small Yin--Lucas local-norm identity is not
acquired. For this construction every symmetry-preserving clock/SW dressing
has a trace obstruction: its required error has weighted norm at least
(1/2)exp(kappa*checkweight). The independent excited-sector terms cannot be
called small merely by increasing the clock penalty.

The decisive uniform acquisition is the marked-wrap KT bound in `PROOF.md`,
Sections3--5. It proves the auxiliary spectral gap separately from the
ground-vector fixed point and bounds the entire higher-order syndrome
coefficient incidence sum, with no N factor or derivative modulo S_c^2=1.

The actual compiler emits `CLOCK_HAMILTONIAN.json` from the EXISTING retained
1336-qubit/1428-check algebraic level2 input. It constructs11424 two-body
qubit--eight-level-clock hops and their exact transformed sign tables in
0.1532s. This input's literal geometry is not acquired; bounded range for the
all-level theorem uses the source's qualified large fixed subdivision and
embedding premise. The uniform9554-bit penalty is not physically economical.

Remaining gates: arbitrary physical-perturbation stability of the two-body
endpoint, a two-body-QUBIT implementation, numerical useful strength scales,
preparation and any perturbed finite-temperature memory claim. Ordinary
König/KT and Ocko--Yoshida phase mechanisms are explicitly credited.
