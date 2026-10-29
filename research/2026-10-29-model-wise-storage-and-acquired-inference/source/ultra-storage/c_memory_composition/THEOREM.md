# An explicit all-input memory theorem for the exact Gaussian model

29 October 2026. Independent composition by retained peer C. The separately
accepted static, algebraic and generator results are imported at their exact
scopes; this file derives the radius, clock, error and size exponents.

## 1. Quantifiers and fixed model constants

Use the five-qubit-seeded even RX/RZ family at level 2k. Let n_k be its
physical qubit count and d_k its quantum distance. The accepted retraction
and primary family give d_k>=d_seed 2^k, one shared syndrome decoder, exact
corrected logical Pauli algebra, bounded check incidence D, and a qualified
fixed geometric subdivision parameter ell. H0,k=sum_j(I-S_j)/2 uses one
energy unit per violated check.

Fix beta>beta_c, where beta_c refers to the primary exp(-beta|sigma|)
counting inequality. Fix native support size q, incidence nu, range,
interaction-label graph degree Delta, spatial density rho, and the accepted
filling/geometry constants F,p,C_geo. Choose a positive uniform strength
bound vbar sufficiently small that

    abar=beta exp(beta Dq)vbar,
    Bbar=(Delta+1)^2 e²[exp(abar)-1] <= 1/[2(Delta+2)],
    bbar=Bbar/e < 1,
    zetabar=(C_geo/beta)[Bbar/(1-Bbar)] e(3p)!,
    beta(1-2zetabar)>beta_c.                                 (1)

All these constants are independent of k. The zero-perturbation model is
included by the same positive vbar bound; no division by its actual strength
is made. For every sequence of actual Hermitian perturbations

    H_k=H0,k+sum_i V_i,k,

with the specified native geometry and ||V_i,k||_P<=vbar, there are at most
nu n_k nonempty labels. The accepted static theorem applies with the uniform
upper bounds in (1) and

    delta_k <= deltabar_k
      := nu n_k bbar^ceil(d_seed 2^k/q)/(1-bbar).

Take k beyond the explicit onset deltabar_k<=1/4. Uniform ordinary patch
Lieb--Robinson constants C0,mu,vLR>0 are supplied for this bounded-strength,
bounded-range class, in the precise convention of CKG_ADMISSION.md. They
are not assumptions about exact Davies frequency components.

**For each actual H_k separately**, form the exact Gaussian CKG generator
for each of its 3n_k one-site Pauli seeds, at rate one per seed. Sum these
generators, including all their coherent corrections. Optionally add the
drift -i s[H_k,·], with s in {0,1}. The Gibbs state rho_k=e^(-beta H_k)/Z_k
is exactly stationary. The full continuous-frequency generators are used;
the radius below only enters a proof estimate.

The corrected logical algebra and decoder are the same unperturbed decoder
at every allowed H_k. The encoder is the positive map
omega -> U_k†(omega tensor tau_k)U_k, where
tau_k=Tr_L(U_k rho_k U_k†). It depends on the actual Gibbs state. Neither
efficient preparation of tau_k nor physical implementation is assumed.

The order of quantifiers is therefore

    fixed uniform constants; for every k and allowed H_k;
    construct its own stationary L_(H_k) and Enc_(H_k);
    then for every logical input, reference and stated time.

It is not the statement that one generator or one initializer works for
every unknown perturbation.

## 2. A paid support radius

Set

    chi=ln4+beta(1+2zetabar)D,
    u_k=2^(k/3),
    r0=[ln2/(32chi rho)]^(1/3),
    R_k=r0 u_k.

Radius may be real; the patch is the set of physical sites within that
distance. For R_k>=1, the actual all-operator bad projector of every such
patch obeys

    p_R <= 4 exp(4deltabar_k)
             exp[chi rho(1+R_k)^3-(ln2)2^(k-1)]
        <= 4e exp[-(ln2)u_k^3/4] =: P_k.                    (2)

Here (1+R)^3<=8R^3. The SAME common good sector controls every coherent
operator on that support, including each whole Fourier jump and its square;
there is no independent-Pauli-jump substitution. In particular

    sqrt(P_k)=2sqrt(e) exp[-(ln2)u_k^3/8].                   (3)

For a native support of at most q qubits it is more economical to use the
static theorem directly, without enclosing it in the larger ball:

    p_native <=4e exp[chi q-(ln2)u_k^3/2].

The logical Hamiltonian defect for each alpha=X,Y,Z is thus at most

    h_alpha=||[H_k,O_alpha]||_rho <= H_k^bd,
    H_k^bd=Hconst n_k exp[-(ln2)u_k^3/4],
    Hconst=4nu vbar exp(1/2+chi q/2).                       (4)

The factor is 2 sum_i||V_i||sqrt(p_native); H0 commutes with the corrected
Paulis. This also controls Y on the common X/Z good sector. The bound is
deliberately uniform over the admitted perturbation class.

## 3. Full generator defects and the per-site clock

Keep exactly the paid Gaussian CKG tails

    d(R)=C0 exp(-mu R/2)+2exp[-R²/(4vLR²beta²)],
    rB(R)=6C0 exp(-mu R/2)+2C1 exp[-pi R/(4vLR beta)]
                              +6exp[-R²/(4vLR²beta²)],
    C1=8sqrt(2) exp[(1+pi²)/8].

The integrated dissipator budget is <=1 per seed. The accepted whole-jump
and coherent-correction estimates give

    ||L*O_alpha||_rho <= s H_k^bd +3n_k C_k,
    C_k=9sqrt(P_k)+2rB(R_k)+4d(R_k)+2d(R_k)^2.              (5)

The coherent term contributes 6sqrt(P_k) of the local 9sqrt(P_k) budget;
the dissipator contributes 3sqrt(P_k). The cross terms in a jump truncation
produce 4d+2d². They have not been dropped.

The factor 3n_k is essential. Equivalently the sum is 3n_k times the
globally normalized CKG construction with seeds Pauli/sqrt(3n_k). Its
algorithmic simulation clock is correspondingly rescaled. Calling the
normalized one-update clock a constant per-site rate would overstate the
memory time by a volume factor.

## 4. The exact all-input receiver

Let Lambda_k,t be Dec_k exp(tL_(H_k)) Enc_(H_k). Define

    A_k=9beta H_k^bd/8,
    L_k=3s H_k^bd/2+(9/2)n_k C_k.                          (6)

For EVERY pure logical/reference state Psi, of arbitrary reference size,

    <Psi|(Lambda_k,t tensor id)(|Psi><Psi|)|Psi>
       >= 1-A_k-t L_k,                                    (7)
    ||Lambda_k,t-id||_diamond <=min{2,2sqrt(A_k+t L_k)}.

Proof: the Gibbs commutator bound gives
epsilon_k=||rho_k-T_logical(rho_k)||_1 <=3beta H_k^bd/4.
The stationary GNS receiver gives

    1-Fe(I/2,Lambda) <=[3epsilon_k+t sum_alpha||L*O_alpha||_rho]/4.

The centered-Kraus variance identity gives
1-Fe(omega,Lambda)<=2[1-Fe(I/2,Lambda)] for every qubit omega, including
its purification. Substituting (4)--(5) proves (6)--(7). Fidelity here is
overlap, the squared convention. The t-independent term is a conservative
twirl-comparison loss, not an actual error at t=0: Dec Enc=id exactly.

For any prescribed error eta in (0,1) with A_k<eta, the explicit interval

    0<=t<=(eta-A_k)/L_k                                   (8)

has purified-input infidelity at most eta. Its diamond error is at most
2sqrt(eta). Formula (8), including its n_k clock factor, is a direct finite
receiver from the stated constants; no spectral gap or rapid mixing is used.

## 5. Explicit stretched-exponential rate and onset

Put

    lambda=min{ln2/8,mu r0/2,pi r0/(4vLR beta),
                               r0²/(4vLR²beta²)}>0,
    Cstar=18sqrt(e)+16C0+4C1+20+2(C0+2)^2,
    Aconst=9beta Hconst/8,
    Lconst=3s Hconst/2+9Cstar/2.

For u_k>=1, (3)--(5) imply

    C_k<=Cstar exp(-lambda u_k),
    H_k^bd<=Hconst n_k exp(-lambda u_k),
    A_k+tL_k<=n_k(Aconst+Lconst t)exp(-lambda u_k).         (9)

For example, after A_k<=eta/2, (8) guarantees the explicit lower bound

    T_eta,k >= eta exp(lambda 2^(k/3))/(2Lconst n_k).        (10)

This displays the actual rate exponent and the physical per-site clock.
Constants may be extremely poor. No practically useful threshold is inferred.

A fully explicit sufficient onset for a decaying-error statement is available
without assuming n_k polynomial in u_k for free. Use the source cell count
in Section 6, or the independently accepted root bound n_k<=5g^(2k).
Write generically n_k<=N0 G^(2k),

    Pn=6ln(G)/ln2,
    ad=(d_seed/q)ln(1/bbar),
    U_delta=max{1,sqrt(2Pn/ad),
                  [2ln_+(4nu N0/(1-bbar))/ad]^(1/3)},
    U_pref=max{1,[8Pn/lambda]^2,
                    8ln_+[N0(Aconst+Lconst)]/lambda}.

Here ln_+(x)=max(0,ln x). For u_k>=U_delta, deltabar_k<=1/4:
use ln u<=u and split ad u³ into two equal budgets. For u_k>=U_pref,
n_k(Aconst+Lconst)<=exp(lambda u_k/4): use ln u<=sqrt(u) and split
lambda u/4 into two equal budgets. These inequalities hold for all later k.
Also require u_k>=1/r0 (and any explicitly stated LR minimum-radius input).

Consequently for every k satisfying these finite inequalities and every
0<=t<=exp(lambda 2^(k/3)/4),

    every purified-input infidelity <=exp(-lambda 2^(k/3)/2),
    ||Lambda_k,t-id||_diamond<=2exp(-lambda 2^(k/3)/4).      (11)

Absorbing the centered-Kraus factor into the explicit onset produces these
constants. Root's separately derived bound with an external factor 2 is
equally valid; this is not a claimed asymptotic improvement.

## 6. Actual code-size translation

One may use root's safe native-qubit bound

    g=8D F_*t(t+1)+2(1+Dt), t=(ell-1)/2, F_*=DE=28,
    n_k<=5g^(2k).

It follows from the admitted nonempty checks, at most Dn X checks, the
face-cover bound on Y_x edges, and the direct vertex count on Y_q; RZ is dual.
Substitution into (11) gives a memory interval at least

    exp[c n_k^alpha],
    alpha=ln2/(6ln g), c=(lambda/4)5^(-alpha)>0.            (12)

Here g is evaluated at the PRIMARY-QUALIFIED fixed ell. The toy ell=3
consumer does not qualify the primary spatial embedding or its constants.

There is also a simple independent cell-total route to a size bound. A
single old square contributes at most 8t²+12t+3<=8(t+1)² cells to its doubled
Y_x grids and boundary cylinder. There are at most F_* old squares per star.
An old q contributes at most 2+D(4t+1) cells to Y_q, and an old z contributes
two. Thus total cochain dimension M obeys M_new<=G M_old with
G=8F_*(t+1)², also after dualizing. Since M_seed=9,
n_k<=9G^(2k). This supplies (12) with g,5 replaced by G,9 if desired. It
requires no assumption that the number of checks is bounded by n; duplicate
cells only reduce the stated upper count. No tighter-rate claim depends on it.

## 7. Scope of the resulting operation

The result is a full qubit-memory theorem under arbitrary sufficiently weak
finite-range NONCOMMUTING Hamiltonian perturbations, for the admitted actual
code family and a MODEL-WISE exactly stationary Gaussian CKG generator.
It preserves reference entanglement and uses the same original decoder.
It does not infer any of the following from the theorem: a microscopic
Davies bath, a physical fixed-radius controller, a controller insensitive to
unknown H errors, efficient thermal encoding, a practical error threshold,
or survival under arbitrary nonstationary dissipative perturbations.

The exact Gaussian filters and B correction depend on H_k. A fixed local
implementation error is not an H-adapted exactly stationary generator. The
ordinary channel-perturbation bound charges accumulated error proportional
to time; it does not by itself preserve the stretched-exponential interval.
That missing fixed-generator robustness is addressed as the next scientific
gate in PRIOR_AND_GATE.md, rather than silently included here.
