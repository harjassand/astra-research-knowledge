# Independent receipt: exact isolated killed-resolvent CP credit

2026-10-30. This review checks the actual isolated-controller lemma, its numerical fixture, and the subsequently appended inverse/controlled-credit algebra. It does not inherit any native physical fit or no-exterior-action assertion. The initial and Section-5 source versions are preserved separately; exact hashes are recorded in `SOURCE_SHA256_INITIAL.txt` and `SOURCE_SHA256.txt`.

Final reviewed source SHA-256: `bf839470aee11bc73a137664aadfc7a186672efcec8d3a4af4d32679dc65ac9a`. The preceding Section-5 version was `9262e0532f734c659d4ad822516b244a4b2d23b89b8914bfe71958242886ad4b`; the sole final change corrects the DATA-only disjointness wording identified below. The diff was inspected and accepted.

## Verdict

**PASS for the isolated service lemma, explicit local linear inverse, and mutually exclusive controlled-credit algebra under the stated commuting-factor assumptions.** The proof is exact: no Taylor approximation, weak-drive limit, stationary clock law or fixed-horizon averaging is used.

Two extension conditions must remain explicit:

1. For an extended animal, the effective controller credit must commute with that animal (or an alternative comparison must be proved). Positivity of S alone does not provide the no-jump lower comparison.
2. The initially supplied Section-5 phrase “DATA-disjoint” was insufficient by itself for commutation; the final reviewed source corrects it. The disjointness argument requires **full DATA+controller support disjointness**, or separately verified commuting controller factors. A concrete shared-controller counterexample appears below.

These qualifications do not invalidate the isolated DATA-only service theorem. No overlapping native many-hub theorem, exterior-generator cancellation, controller/ownership compatibility, dirty-abort charge or operational memory theorem is certified here.

## 1. Killed resolvent and strict positivity

Let G_C=L_C^* be the ordinary unital controller Heisenberg generator, J_C^* its terminal gain map, and K^*=G_C-J_C^*. Removing terminal gains while retaining their complete losses gives a CP subunital killed semigroup. If A=J_C^*(I), then K^*I=-A.

A uniform integrable terminal-survival tail makes

    R=integral_0^infinity exp(tK^*)I dt

a bounded positive operator. It is strictly positive because exp(tK^*)I is norm-continuous at t=0 with value I; for some fixed epsilon>0 it is at least I/2 on [0,epsilon]. Hence R>=epsilon I/2. Integrating the generator derivative gives K^*R=-I, since the killed survival tends to zero. Finite dimension alone would not imply this tail: a dark nonterminal subspace can make R diverge.

The more general supplied Lyapunov inequalities

    alpha I<=R<=Rmax I,    K^*R<=-cI

are sufficient and encode a genuine actual-reset condition. They even imply an exponential tail: K^*R<=-(c/Rmax)R, so positivity gives

    exp(tK^*)I <= (Rmax/alpha) exp(-ct/Rmax) I.

No ideal correction generator is inferred from a clock gap or an average reset rate.

## 2. Exact positive CP credit and service

Put P=Phi^*, an idempotent unital CP DATA map. For positive V with d=V-PV>=0, idempotence gives Pd=0. Choose 0<beta<1/Rmax and

    S=(1-beta Rmax)I+beta R,
    s_min=1-beta Rmax+beta alpha>0.

Then s_min I<=S<=I, and

    K^*S <= -(1-beta Rmax)A-beta cI.

The map

    T_S(O)=sqrt(S)O sqrt(S)
             +sum_s K_s^dagger sqrt(I-S)O sqrt(I-S)K_s

has Kraus sqrt(S) and sqrt(I-S)K_s (controller and DATA factors commute). Their squared sum is I, so T_S is unital CP. On V tensor I it gives

    F=PV tensor I+d tensor S
     =V tensor S+PV tensor(I-S).

Thus F>=s_min V tensor I and F<=V tensor I, as genuine Loewner inequalities for **DATA-only V**. Positivity uses d>=0 and PV>=0; it is not a classical mixture assumption.

Every internal operation is auxiliary-only. On PV tensor I the internal generator cancels by unitality and the terminal terms cancel because P(PV)=PV. On d tensor S, every terminal gain is proportional to Pd=0. Its complete terminal losses and internal controller evolution remain exactly K^*S. Therefore

    L_phys^*F=d tensor K^*S
       <=-beta c d tensor I-(1-beta Rmax)d tensor A.

This calculation requires that all terminal outcomes carry the same complete idempotent Phi, in the specified product jumps a_mu tensor K_s. Different terminal instruments, DATA-dependent internal operations, or unresolved native guards would require a new calculation. Controller coherence, including offdiagonal entries of R, is fully retained.

## 3. Explicit local inverse, including nonorthogonal DATA projections

Diagonalize S with eigenvalues s_i in [s_min,1]. In controller block |i><j|, T_S acts on DATA operators as

    A_ij=a_ij Id+b_ij P,
    a_ij=sqrt(s_i s_j)>0,
    b_ij=sqrt((1-s_i)(1-s_j))>=0.

Idempotence gives the algebraic direct sum range(P) plus ker(P); P need not be orthogonal in the Hilbert–Schmidt inner product. On these subspaces A_ij has eigenvalues a_ij+b_ij and a_ij, respectively. Consequently the exact inverse is

    A_ij^(-1)(X)=(X-PX)/a_ij + PX/(a_ij+b_ij).

All denominators are at least s_min. This proves invertibility on the **whole local joint operator space**, not only on DATA observables tensor controller identity. The inverse is HP and unital because T_S is HP, unital and bijective. It need not be positive or CP.

A finite cb bound is immediate. If d_C is the fixed controller dimension, each block extraction/reinsertion is completely contractive and ||P||_cb=1, ||Id-P||_cb<=2, so the crude bound

    ||T_S^(-1)||_cb <= 3 d_C^2/s_min

suffices. Constants depend on the fixed local controller but not the full system size. A bounded-depth circuit of such local invertible maps has local inverse cones; no global extensive inverse norm estimate is warranted or needed.

## 4. Mutually exclusive controlled credits

Let Q_h be a controller-only committed projector (called P_h in the source), and assume S_h is positive on its range and preserves it. Define the effective full controller operator

    S_tilde_h=I-Q_h+Q_h S_h Q_h.

Then the controlled Kraus in Section 5 are precisely sqrt(S_tilde_h) and sqrt(I-S_tilde_h)K_hs. The preceding local inverse applies verbatim, since S_tilde_h has eigenvalue one outside Q_h and a strictly positive lower bound inside it.

For overlapping DATA hubs h,g, suppose Q_h Q_g=0, all credit factors preserve both projectors, all cross-controller factors commute, and all DATA K's commute with those controller factors. Write A_h=sqrt(S_tilde_h) and B_hs=sqrt(I-S_h)Q_h K_hs. Orthogonality gives

    A_h A_g=A_g A_h,
    A_h B_gt=B_gt A_h=B_gt,
    B_hs B_gt=B_gt B_hs=0.

Hence every Kraus of one channel commutes with every Kraus of the other, and the CP maps commute. This includes offdiagonal coherences between h-committed and g-committed sectors. It does not require the overlapping DATA channels Phi_h and Phi_g themselves to commute.

However, this is an algebraic interface, not a consequence of the phrase “full-lock committed.” Actual native monitor/workspace/ownership projectors and their commutations still have to be verified. Nothing here shows that exterior generator terms commute with these credits or that acquisition sectors have service.

### Necessary correction to the disjointness sentence

Disjoint **DATA** supports do not imply disjoint controller supports. For an exact counterexample, take Phi=Id on two separate DATA systems and let both credits act on one shared controller qubit. Choose S_z=diag(1,1/4) and S_n its rotation with Bloch axis n=(x+z)/sqrt(2). Each T is a partial dephasing with transverse multiplier 1/2. On sigma_z,

    (T_z T_n-T_n T_z)(sigma_z)=-sigma_x/8.

Thus they do not commute even though their DATA supports are disjoint. The correct sufficient clause is “full DATA/controller supports are disjoint,” or an explicit commuting-controller-factor condition. This wording gap was reported before adopting that scope in this receipt. The final reviewed source now states the corrected full-support condition explicitly; no unresolved defect remains in this algebraic clause.

## 5. Conditional phase/no-jump barrier comparison

For DATA-only f_A, every controller S_h commutes f_A automatically. For an extended animal involving controller/defect factors, require

    [S_tilde_h,f_A]=0

for each relevant gate. A sufficient condition is [Q_h,f_A]=[S_h,f_A]=0. In a native application it is typically enough to prove preservation of every actual syndrome and defect flag, but that must be an earned operator identity.

Select the first Kraus sqrt(S_tilde_h) from every gate in the **structural** backward circuit cone of f_A. At fixed circuit depth and bounded support/incidence, there are at most c_gate |A| such gates. Positivity of the omitted Kraus histories gives a positive summand Q^dagger f_A Q. Under the commutation condition this equals f_A Q^dagger Q. Minimum singular values multiply, even when selected factors do not commute with one another, so

    T(f_A)>=s_*^(c_gate |A|) f_A
           =exp[-c_gate log(1/s_*)|A|]f_A,

where s_*>0 is a common effective-credit lower bound. Choosing beta small makes log(1/s_*) arbitrarily small for fixed resolvent bounds. Two admissible animal exponents with

    a_+-a_0>=c_gate log(1/s_*)

then give T(V_+)>=V_0. The usual local Stinespring perturbation lemma is available for this actual bounded-depth local CP circuit. These observations do not supply clean many-hub service or basin invariance/commutation by themselves.

### Explicit failure without controller-factor commutation

Positivity S>=s_min I does not imply sqrt(S)f sqrt(S)>=s_min f. For an exact example, let

    S=[[5/8,3/8],[3/8,5/8]],
    sqrt(S)=[[3/4,1/4],[1/4,3/4]],    s_min=1/4,
    B=diag(4,1).

Then sqrt(S)B sqrt(S)-(1/4)B has determinant -9/64 and is indefinite.

Even the complete CP credit can fail the desired lower comparison on a noncommuting extended factor. Let Phi reset a DATA qubit to |0>, let D=diag(1/100,1), and set f=D tensor B. In the DATA-|1> block,

    T_S(f)-(1/4)f
      =sqrt(S)B sqrt(S)+(1/100)sqrt(I-S)B sqrt(I-S)-(1/4)B.

Its determinant is exactly -27/256. Thus the general extension T_S(f)>=s_min f is false. The isolated theorem avoids this issue because its input V is DATA-only; the source's final commutation caveat is essential rather than cosmetic.

## 6. Numerical/code audit and independent regression

The supplied `check_resolvent_credit.py` consistently constructs the killed three-level controller superoperator, solves K^*R=-I, and compares the exact physical DATA/controller drift with both the killed identity and the proposed bound. Its Kraus orientation and tensor order are correct. It is a finite exact-algebra regression, not a proof of a generic terminal tail or native overlap theorem.

The independent `check_credit_inverse.py` adds an auxiliary-only internal jump and two terminal destinations implementing the same nontrivial idempotent DATA channel. It verifies resolvent/service/CP identities and both sides of the explicit local inverse on a random full joint operator. Residuals are below 7e-15. It separately verifies mutually exclusive controlled credits with noncommuting DATA reset channels, and the two counterexamples above.

The independent inverse fixture deliberately uses a valid strict upper bound Rmax=1.1||R|| rather than equality, keeping S away from eigenvalue one. An initial version using equality produced a roughly 1.6e-9 square-root boundary roundoff discrepancy; this was numerical sensitivity at I-S's zero eigenvalue, not a failed symbolic inverse. The final regression uses the unchanged mathematical construction with a slightly looser allowed Rmax.

## Final scope

The resolvent CP credit is a valid exact local service mechanism and has a usable explicit local inverse. Its phase-dependent multiplier is genuinely different from the rejected common-time CP-average bridge. Under verified projector/commutation assumptions, mutually exclusive committed credits commute and admit the stated conditional local no-jump comparison.

The actual native generator, its exterior terms, dirty reset/abort behavior, acquisition-to-commit service, blocker payment and basin compatibility are still separate obligations. This receipt does not turn the enabling lemma into a full native continuous-noise memory theorem. No original source or external state was changed by this reviewer.
