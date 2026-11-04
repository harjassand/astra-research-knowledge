# Unary resonant clocks: a three-body-qubit compiler with polynomial clock-weight cost

2026-11-03. Constructive exact-H algebra and thermal majorants. Adaptation of the previously acquired resonant-clock signed-gas theorem; not a completed noisy WRITE or microscopic-bath preparation theorem. Independent audit requested.

## 1. Physical Hamiltonian, without a sector projection

For each target stabilizer S_a=product_(j=0)^(K_a-1) P_aj, the factors are single-data-qubit Paulis or identities and commute within this check. Use K_a physical clock qubits on a cycle, with n_j=(I-Z_j)/2 and lowering/raising operators b_j,b_j^dagger. For clarity take common K>=3 and define

N_a=sum_j n_aj,
g=eta t/K,
U=4t/K^2,
H_a=U(N_a-1)^2+2t sum_(j=1)^(K-1) n_aj
    -sum_(j=0)^(K-1) t_j P_aj (b_(j+1)^dagger b_j+b_j^dagger b_(j+1)),

with cyclic indices, t_0=t_(K-1)=g and all other t_j=t. The total H is sum_a H_a, retaining shared data-qubit noncommutativity.

Every hopping term is a sum of two three-qubit Pauli terms. The number penalty is

U(N_a-1)^2=U[1-sum_j n_aj+2 sum_(i<j)n_ai n_aj],

so uses only onsite and two-body terms. There are K clock qubits/check, O(K) three-body terms and O(K^2) pair penalty terms. This is finite-range on each fixed-size check neighborhood, not automatically a nearest-neighbor architecture. All number sectors are physical and retained. Single-clock-qubit bath X/Y errors may change N_a.

## 2. Exact all-sector dressing

Let F_a(0)=I and F_a(j)=product_(r<j)P_ar. For occupation string q define F_a(q)=product_j F_a(j)^(q_j). Define the controlled Pauli unitary U_a=sum_q |q><q| tensor F_a(q), and use a fixed ordered product over checks.

Within one check, a hop j->j+1 changes F_a(q) by P_aj, except the closing hop where the additional product is S_a. This is true at EVERY occupation number. Ordered transformations from overlapping checks contribute only scalar pairwise Pauli commutation signs. They equal one if the spectator clock is at the canonical vacuum q=e_0, since F_a(e_0)=I.

Thus the exact dressed Hamiltonian is in the target stabilizer algebra tensor the full clock algebra. Decoded logicals commute with it exactly. This is not a low-energy Schrieffer–Wolff identification. Each closed clock occupation trajectory has equal net current through every cycle edge; modulo two its data word is I or S_a. Hence its external flux is precisely s_a^w. Shared-check phases remain pairwise trajectory factors of modulus one.

## 3. Ordinary excursions are unchanged resonant-clock excursions

Hopping conserves every N_a. In N_a=1 the Hamiltonian is exactly the old K-level resonant clock. At g=0 the non-vacuum one-particle path matrix is

A=t(2I-T_(K-1)),
mu=2t[1-cos(pi/K)]>=4t/K^2,
v=e_1+e_(K-1).

For an ordinary first-return excursion from e_0, the absolute density is

rho(ell)=g^2 v^T exp(-A ell)v,
rho_w(ell)=2g^2 [exp(-A ell)]_(1,K-1).

Consequently the already proved exact identities remain

integral rho=2g^2/t,
integral ell rho=g^2(K-1)/t^2,
J=integral rho_w=2g^2/(tK)=2eta^2t/K^3.

All path-internal backtracking is resummed. There is no epsilon^K suppression.

## 4. All unwanted number sectors are full-circle thermal wraps

A trajectory with N_a!=1 can never reach e_0. It is therefore a full-circle wrap in the exact periodic-time rod representation. Its activity must be bounded, not deleted.

For the absolute hopping majorant, the ancillary model is a hard-core boson cycle. In each fixed particle-number sector, the Jordan–Wigner transformation gives free fermions with one of the two boundary twists. The corresponding one-particle matrix is

h_pm = [[0,-g v_pm^dagger],[-g v_pm,A]],
v_pm=e_1 +/- e_(K-1).

Since A>0, interlacing implies at most one negative eigenvalue. Completion of squares and the explicit path inverse give

lambda_min(h_pm)>=-g^2 v_pm^dagger A^(-1) v_pm>=-2g^2/t.

Thus the sum of occupied single-particle energies in ANY particle-number sector is at least -2g^2/t. Adding the penalty yields

H_a^(abs)|_(N_a=q)>=U(q-1)^2-2g^2/t.

This bound is sharper than charging the norm of all internal hopping terms: those terms form a positive open-path kinetic energy and need not be paid as O(Kt) negative energy.

Summing all q!=1 dimensions gives the absolute extra-wrap bound

W_leak <= (2^K-K) exp[-beta(U-2g^2/t)].

With the temporal KP tilt b, use

W_leak(b) <= (2^K-K) exp[-beta(U-2g^2/t-b)].

The ordinary N=1 never-vacuum wraps retain the old bound

W_path(b)<=(K-1) exp[-beta(mu-b)].

These are full thermal trace bounds, not a probability that every clock has exactly one excitation. There can be a nonzero density of unwanted occupations in arbitrarily large systems.

## 5. Direct signed-gas admission

Use the acquired proof in `/workspace/shared/resonant_clock_compiler_20261102/resonant_rod_bound.md` and its exact pair-gas representation. For overlap degree D and spatial weight kappa put Dbar=D exp(kappa), x=Dbar eta^2, a0=64x/K and b=32x t/K^2. Choose x sufficiently small, for example x<=1/64.

Replace the old wrap hypothesis by

W_path(b)+W_leak(b)<=eta^2/K.

The ordinary-rod KP integrals are unchanged. A new wrap has full duration beta and obeys exactly the same interaction-overlap majorant as an old wrap. Thus the existing KP proof admits the entire unary Hilbert space.

There is one additional free-energy bookkeeping point: unlike an old path wrap, a multi-occupation wrap can itself carry target flux. Clusters with a marked ordinary winding rod obey the old relative-error bound. Clusters whose relevant flux comes from a leakage wrap are bounded by the rooted wrap activity, conservatively

additional weighted local free-energy influence <= 2 exp(a0) W_leak(b)/beta,

where the conservative factor 2 covers rooted-cluster overcounting. To obtain the spatial weight, inflate every non-root rod by exp(kappa); Dbar already pays this inflation, while the marked root needs no such factor because diam<=number_of_rods-1. The rooted KP bound is then at most the marked-wrap integral times exp(a0+b beta). Dividing by J gives an additional relative remainder 2 exp(a0)W_leak(b)/(beta J). It can be made arbitrarily small by the explicit cold inequality. Merely substituting total W into the old formula without this marked-wrap term would miss a real effect.

The exact syndrome free energy therefore has the same intended structure

F_beta(s)=c_beta-J sum_a s_a+R_beta(s),

with a local influence norm bounded by the old resonant remainder plus the displayed extra-wrap term. This admits witness removal directly; no separate claim that rare missing clocks preserve the code is needed.

## 6. Operating regime and physical cost

With U=4t/K^2 and x<=1/64,

U-2g^2/t-b = [4-2eta^2-32x]t/K^2 >0.

The target cold condition beta J>=B_c implies beta t/K^2>=B_c K/(2eta^2). Hence the 2^K unwanted-sector entropy is overwhelmed for fixed sufficiently cold B_c and small eta, independently of the number of checks. All constants remain fixed with device size.

At microscopic maximum coupling of order t, the useful stabilizer energy is polynomially suppressed, J/t=2eta^2/K^3. The onsite and penalty degree-weighted strength remain O(t): every clock site has O(K) penalty couplers of size O(t/K^2), plus fixed hopping incidence and onsite 2t. This is much better in K than a unique-ground k-edge perturbative ring with J approximately Delta(g/Delta)^K, but does not establish an experimental device.

The O(K^2) penalty graph and K qubits/check are real resources. To enforce fixed physical density, one may need a fixed geometric expansion of each check neighborhood; a strict nearest-neighbor-only hardware model would require further routing/gadgets. The number penalty may also be a native charging energy of a multi-mode island, but that is an implementation proposal requiring hardware validation, not a theorem about available couplers.

## 7. Remaining full-capability gates

The exact Davies lifetime transfer applies once the free-energy/witness adaptation is independently checked, including all microscopic clock Pauli errors. The prior exact-H bath/source theorem might extend because this is a finite clock graph with the same closed-word structure, but its source dictionary and constants must be checked; finite dimension 2^K must not be silently treated as K.

Noisy WRITE and preparation of the actual joint memory-bath Gibbs state remain unconstructed. The unary representation improves the literal three-body hardware/resource contract. It does not turn ideal thermal encoding into a physical loading procedure, nor make a Markov approximation valid for exponentially long times.

## 8. Independent checks

The compiler worker independently verified the all-particle-number spectral lower bound, including the absence of a spurious N factor, and the robustness worker independently verified the full-occupation Pauli dressing and pair-history signs. `check_unary_resonant_sectors.py` diagonalizes all fixed-number hard-core sectors for K=3,4,5,7,9, eta=0.05,0.2, and both fluxes. All 20 cases satisfy the algebraic lower bound; the N=1 spectra agree exactly with the original clock matrices. These numerical checks are not the proof of the uniform bound.

### Exact rational fixed-K certificate

The separate audited certificate `/workspace/shared/unary_resonant_certificate.py` uses K=7, overlap D=43, t=1, g=3/500, U=4/49, a=1/20, b=7/500. All path inverses are exact rational matrices; the exponential factor is bounded from above. It obtains J=9/875000, temporal KP load below 0.0136042 < b, activity KP load below 0.0447515 < a, and marked relative cluster correction below 0.179242 < 1/4. The tail ratio at tilt 0.05 is below 1.556. The combined nonvacuum wrap bound is (2^K−1) exp[−beta(U−2g^2/t)], with gap 0.081560653..., and beta>=1000 makes these wrap corrections small. The actual code's cold condition beta J >> 1 is stronger and must still be imposed. This K=7 point is not a certificate for the literal K=180 explicit geometric family.

### Paid fast WRITE interface

`FAST_WRITE_MICROSCOPIC_BATH_RESOURCE_BOUND.md` constructs an exact bounded-bath fast-control interface: reference-safe WRITE error at most 4||K_touch||T, independent of bath self-H norm. It requires peak control strength of order N times control-circuit depth divided by desired global error, plus supplied actual joint equilibrium and clean work. Thus an expensive noisy-WRITE interface is now available, while fixed-strength scalable WRITE and physical equilibrium loading remain open. This does not relax any of the thermal/bath gates above.

### Energy-to-temperature scale of the certified point

Using the exact SI conversion h/k_B, the K=7 certificate has J/k_B approximately 4.94 microkelvin when t/h=10 GHz. A required cold parameter beta J>=B_c then demands T<=4.94 microkelvin/B_c. Conversely, at 10 mK the same sufficient point needs t/h>=20.26 THz times B_c. These are unit conversions, not claims that such coherent three-body hardware exists or that B_c=1 suffices. The sufficient certificate may be very conservative; no improved physical point has yet been proved. Polynomial dependence on K is a genuine compiler improvement, but it is not evidence of practical cryogenic feasibility.
