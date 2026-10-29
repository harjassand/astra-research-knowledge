# Perturbed RX/RZ storage in an exactly stationary quasilocal model

29 October2026. Root composition, independently reconstructed and accepted
by the retained quantum-interface peer at the stated model-wise scope. The
load-bearing static, encoding/kinetic and Gaussian-generator modules have
separately received substantive internal review. This file pays their actual
size/radius/time composition. No microscopic bath or fixed controller is
silently substituted for the specified algorithmic thermal generator.

## 1. Exact family and model

Take the actual five-qubit-seeded even RX/RZ family H0,k with n_k qubits,
distance at least d_seed*2^k, and its primary-qualified fixed geometric ell.
Use H0=sum_j(I-S_j)/2, so each check defect has energy1. Fix beta>beta_c in
the primary exp(-beta|sigma|) counting convention. Let H_k=H0,k+sum_i V_i
for ANY finite-range, bounded-incidence Hermitian perturbations satisfying
the size-independent small Pauli-l1 threshold of A's STATIC_PEIERLS.md.
All native geometry/incidence constants q,nu,D,rho,F,p,Delta are fixed in k.
Choose ONE strength cap v_bar and its computed check-charge cap zeta_bar so
the KP inequality and beta(1-2zeta_bar)>beta_c hold for the whole class.
Require max||V_i||_P<=v_bar, and eventually the uniform large-polymer bound
delta_bar<=1/4. The onset and constants below are uniform over this class;
they do not secretly depend on each realised perturbation. The standard
Lieb--Robinson constants are likewise taken from the capped local strength.
These are nonempty sufficient inequalities, with potentially terrible constants.

For EACH site Pauli A use the EXACT Gaussian CKG generator built from this
SAME H_k,beta and its actual coherent correction B_A. Sum the3n_k one-seed
generators at constant per-site rate, optionally adding -i[H_k,.]. The Gibbs
state rho_k=e^(-beta H_k)/Z is exactly stationary. Its integrated strengths,
coherent correction and quasilocal tails are paid in CKG_ADMISSION.md.

Use the SAME primary decoder's exact logical Pauli algebra and the positive
encoder/decoder of PROOF.md. The environment state is the logical partial
trace of rho_k. Efficient physical preparation of that state is not asserted.

## 2. Common support radius

Put s_k=2^k, c0=(ln2)/2 and chi=ln4+beta(1+2zeta_bar)D. A's static theorem gives

    p_bad(X)<=4e exp[chi |X|-c0 s_k].

It concerns the ACTUAL coherent Gibbs state and a common good projector for
EVERY operator on X. For a radius-R patch, |X|<=rho(1+R)^3. Choose

    a=[c0/(2chi rho)]^(1/3), R_k=floor(a s_k^(1/3))-1.

Eventually R_k>=a s_k^(1/3)/2 and contains each fixed native support when
centered appropriately. The actual whole-patch bad probability is at most

    p_k=4e exp[-(c0/2)s_k].                                  (1)

This radius truncates operators only in the PROOF. The generator itself is
the exact quasilocal one. A physical fixed-radius truncation is another model.

## 3. Explicit generator defects

Let h_alpha=||[H_k,O_alpha]||_(rho_k). Since [H0,k,O_alpha]=0 and at most
nu n_k perturbation labels have norm<=v_bar,

    h_alpha<=2nu v_bar n_k sqrt(p_k).

The accepted receiver and generator-tail estimates give

    delta_alpha=||L_phys*(O_alpha)||_rho
      <=h_alpha+3n_k[9sqrt(p_k)+2r_B(R_k)+4d_Rk+2d_Rk^2].      (2)

The h_alpha term is for optional H_k drift; otherwise omit it. The coherent
CKG correction remains included in either case. With the explicit kernels,
let

    c_tail=min{mu/2,pi/(4v_LR beta),1/(4v_LR^2 beta^2)},
    D0=C0+2, B0=6C0+2C1+6, C_T=2B0+4D0+2D0^2.

Here C0,mu,v_LR are the admitted ordinary Lieb--Robinson constants and C1
is the paid coherent-kernel tail constant. For R>=1,

    2r_B(R)+4d_R+2d_R^2<=C_T exp(-c_tail R).

Set u_k=s_k^(1/3) and

    b=min{c0/4,c_tail*a/2}>0,
    C_D=2sqrt(e)(2nu v_bar+27)+3C_T,
    C_E=3beta nu v_bar sqrt(e).

Equations(1)--(2) and the Gibbs logical-twirl bound imply

    delta_alpha<=C_D n_k exp(-b u_k),
    epsilon_k=||rho_k-T_logical(rho_k)||_1
        <=C_E n_k exp(-b u_k).                              (3)

No syndrome-diagonal-state assumption, independent-Pauli-jump replacement,
omitted coherent term or omitted jump cross term enters these bounds.

## 4. All-input storage interval and actual code size

For the decoded logical channel Lambda_k,t the reviewed kinetic theorem gives

    1-F_e(I/2,Lambda_k,t)
       <=(3/4)n_k(C_E+C_D t) exp(-b u_k).                    (4)

A concrete safe size bound follows from the admitted local cells. Let
t=(ell-1)/2, F_*=DE=28 and D=7. There are at most Dn X checks; each Y_x
has at most4F_x*=8F_*t(t+1) edges, because every edge belongs to a face.
Each Y_q has at most2(1+Dt) vertices. Thus one RX step, or its dual, obeys

    n'<=g n, g=8D F_*t(t+1)+2(1+Dt).

Hence n_k<=5(g^2)^k. In particular n_k is only polynomial in u_k. Choose a
fixed onset k0 so (3/4)n_k(C_E+C_D)<=exp(bu_k/4), all earlier onset conditions
hold, and the chosen radius includes the native supports. For every k>=k0
and EVERY0<=t_time<=exp(bu_k/4), equation(4) yields

    1-F_e(I/2,Lambda_k,t_time)<=exp(-bu_k/2).

The accepted Kraus-variance conversion gives, for EVERY purified logical
qubit input, fidelity at least1-2exp(-bu_k/2), and

    ||Lambda_k,t_time-id||_diamond
       <=2sqrt(2)exp(-bu_k/4).                              (5)

Thus storage lasts at least exp(c n_k^alpha), where
alpha=ln2/(6ln g)>0 and c=(b/4)5^(-alpha), beyond a fixed onset. Both temperature
and per-site rates are constant in system size. These conservative sufficient
constants do not establish a useful numerical native tolerance.

## 5. Scientific scope

The Hamiltonian perturbations may be local and NONCOMMUTING. The static
probability is taken in their ACTUAL Gibbs state. The recovered information
is a full unknown qubit, including entanglement. These remove restrictions
of the unperturbed commuting/syndrome-diagonal argument at the stated model.

For EACH perturbed H_k the specified exactly stationary generator is built
from THAT H_k. This is a MODEL-WISE family. It does not show that one fixed
finite-range controller or bath withstands unknown Hamiltonian errors. It
does not prove locality of exact infinite-resolution Davies components,
thermal behavior of the separate two-body clock simulator, or survival under
arbitrary nonstationary dissipative imperfections.

Physical bath access, initialization, readout/control cost, practical strength
ratios and hardware storage performance remain unacquired. Historical priority
and civilisation-level leverage remain UNKNOWN/NOT_ESTABLISHED. The formal
bound is not an operational physical quantum memory demonstration.

Load-bearing sources and reviews are named, rather than replaced by receipts:
../a_independent/thermal_interface/STATIC_PEIERLS.md;
PROOF.md; CKG_ADMISSION.md;
../c_quantum_memory_receiver/{REVIEW,CKG_INDEPENDENT}.md;
../c_static_peierls_review/REVIEW.md.
