# Native all-bad-flag CP credit with explicitly slow acquisition/cleanup
2026-10-30. New construction candidate, not independently audited. This handles physical history defects, not clean acquisition service. The full native continuous-noise theorem remains OPEN.

## 1. Rate redesign, not an unpriced reset oracle
Keep the native two-site Hamiltonians and on-site reset alphabet. Choose the amplitudes of acquisition/reversal A hops and o_h<->z_h cleanup hops, and the rates of z_h->free resets, at most epsilon times fixed constants. They remain strictly positive constants independent of N. Keep abort drives, C computation, monitors, workspace refresh, commitment, ready and verification rates fixed. No DATA reset or additional dissipative primitive is added.

This intentionally separates slow lock movement from fast dirty-history healing. The actual effects of every terminal/abort DATA instrument are retained below. It does not prove adequate clean correction throughput.

## 2. Local killed bad-sector generator
Use the actual forest-frame B_h=I-P_h, including structural inconsistency and nonzero workspace. Exterior owners preserve h's o_h and z_h lock predicates and leave h's private clock/workspace untouched. Thus they preserve B_h exactly. (The native bipartite hub/resource architecture is essential.)

Define L_h^0 by omitting h's three slow classes above, while retaining h's abort drives, C gates, monitors, A/Q workspace refresh, commit, ready and Q verification transitions. Restrict to B_h and delete gains which exit B_h; retain their complete losses. This gives a finite-dimensional CP killed generator K_h^0 on the bad subspace. Forest payload Hamiltonians are scalar; deleted terminal/abort gains were the only DATA actions. Remaining jumps are controller-only. The generator depends only the o_h/z_h predicates, not on which *other* owner occupies a resource.

Uniform local absorption holds:
- structural inconsistency has an enabled failed-test abort edge and complete abort reset;
- consistent A/Q with dirty workspace has a direct complete refresh;
- consistent C with dirty workspace has the finite forward C path and terminal reset;
- every R label has a direct abort reset.

The fixed finite-rate clock monitor excludes dark interference just as in the accepted actual-reset argument. This is a finite local matrix, not a global inverse. Therefore

    R_h=int_0^infinity exp(t K_h^{0*}) I_bad dt

is strictly positive and finite, and K_h^{0*}R_h=-I_bad. Choose common Rmax>max_h||R_h|| and beta>0 with s0=1-beta Rmax>1/2. Set S_h=s0 I_bad+beta R_h. Then 0<s_min I<=S_h<=s_max I<I and

    K_h^{0*}S_h=-beta I_bad-s0 A_heal,h,

where A_heal,h=-K_h^{0*}I_bad is the actual summed intensity of bad-to-good gains, including source restrictions. Every terminal/abort source is among these healing sources. All constants are independent of epsilon, since the slow terms were omitted before forming R_h.

## 3. Quantitative token surplus for arbitrary DATA outputs
Let V_0 be the raw animal potential with B_h set to zero, and let D_h^flag=V(B_h=1)-V(B_h=0)>=0; it is independent of B_h itself. Thus V=V_0+B_h D_h^flag. Let k bound all syndrome bits affected by any h payload reset and let T_h have R tokens. Put u=1-c, a=c log(1/theta).

On a fixed exterior syndrome/other-flag block, let V_0,min and V_0,max be its values when the k potentially affected syndrome bits are all zero/all one. The completion of every animal meeting these bits by D=T_h union S_h gives

    V_0,max-V_0,min <= q_R D_h^flag,min,
    q_R = 2^(R+k) theta^{cR-(1+u)k}/(1-theta^R).

Reason: a source increasing animal contributes at most theta^(-k)f_A(empty), while its completed target B contributes (theta^(-R)-1)f_B(empty) to flag removal, with f_B/f_A>=theta^{u(R+k)} and at most 2^(R+k) preimages. The weighted W version follows from |A|<=|B|.

Choose R>k, then c>2k/(R+k), and theta sufficiently small that q_R<1/4. This is compatible with the original animal charging and vacuum constraints by taking c sufficiently close to one. For ANY complete local reset E_U, including nonmonomial partial gates,

    E_U^* V_0 - V_0 <= q_R D_h^flag

on its bad source, as a Loewner inequality. Indeed E_U^*V_0<=V_0,max I and D_h^flag>=D_h^flag,min I. This pays actual DATA changes after flag erasure; it does not silently treat them as identity.

## 4. Correct-order private flag-erasure CP credit
Let Psi_h be the auxiliary CPTP channel resetting h's clock/workspace to Q0,0, retaining its monitor, every lock and all DATA. This is an ANALYTIC CP credit, not a new physical reset in the generator. It clears B_h because Q0 is universally consistent. It leaves other flags unchanged.

Extend S_h as identity on B_h=0. If {E_h,a} are Kraus operators for Psi_h, define

    A_h=sqrt(S_h),
    C_h,a=E_h,a sqrt(I-S_h).

The order is essential: the jump branch is erase AFTER the survival coefficient. The opposite order could vanish because S=I on the Q0 output. These Kraus operators are complete. Their Heisenberg channel T_B,h obeys

    T_B,h(V)=V_0+B_h S_h D_h^flag.

V_0 and D_h^flag commute with S_h. Cross good/bad coherences are retained by sqrt(S_h); no pinching was added. The channel preserves the raw low-potential basin because the erasure branch only removes flag tokens and the no-jump coefficient preserves syndrome and flag sectors.

Every coefficient depends only h's private system and its own o_h/z_h predicates. Exterior operators preserve these predicates and do not act h's private system. Psi_h changes no DATA or lock. Hence T_B,h commutes with every exterior nominal generator term. Different h credits commute. They also commute with the good committed-chain credits: source good/bad sectors of a given owner are orthogonal, the erasure output Q0 activates neither credit, and other owners' own masks are unchanged.

## 5. Fast bad-sector drift and real DATA charge
On the bad source, V_0 is unchanged by every data-free fast transition and every Hamiltonian. For a healing reset the target credit is identity. The killed-generator calculation therefore gives

    L_h^{0*} T_B,h(V)
      <= [-beta I_bad-s0 A_heal,h]D_h^flag
          + q_R A_payload,h D_h^flag
      <= -beta B_h D_h^flag
          -(s0-q_R) A_heal,h D_h^flag,

where A_payload,h<=A_heal,h is terminal/abort intensity. The displayed second inequality weakens the bound by allowing q_R also on harmless healing jumps. The DATA bound is valid uniformly with a reference and arbitrary dirty workspace.

The terminal good/dirty cross block vanishes by the deterministic-syndrome Stinespring invariance from the raw-envelope lemma. Abort sources are wholly bad. Other healing jumps are DATA-free complete overwrite instruments; V_0 is unchanged, and the remaining credited positive observable is supported on B_h, so their effects have no good-source cross block. Thus this is a full-Hilbert block inequality, not a restriction to classically mixed bad configurations. On good sources this dirty credit is identity and the original raw good recovery decrement remains.

## 6. The omitted slow terms are absorbed locally
Let E_h be the actual omitted acquisition, cleanup and z_h->free generator terms, with local adjoint norm <=C epsilon. They act only on controller/locks, preserve every other flag, and annihilate V_0 and D_h^flag. They obey the original no-creation invariance for B_h. Therefore

    E_h^* T_B,h(V)=[E_h^*(B_h S_h)]D_h^flag.

The bracket is supported on B_h: Hamiltonians preserve B_h; a reset gain of a B_h-supported positive observable annihilates the good input, and its complete loss commutes with B_h. Its norm is bounded by C epsilon, so

    E_h^* T_B,h(V)<=C epsilon B_h D_h^flag.

Choose epsilon<beta/(2C). The exact physical own-generator drift then contains uniform service

    -(beta/2) B_h D_h^flag.

All exterior terms commute with the credit, so products of the T_B,h transfer these inequalities by positivity without an extensive pairwise remainder. Composition with the good committed-chain credit retains both forms of service. These claims still require an independent check of the listed native transition ownership predicates and the exact bad-sector matrix.

## 7. What this would and would not close
If audited, this earns uniform weighted service for actual dirty controller flags, including malformed acquisitions, orphan own/z locks, arbitrary dirty C workspaces, and partial nonmonomial aborts. Flag-dense animal coverage no longer waits for endpoint occupancy.

It does NOT earn service for clean active DATA demands while their hub is acquiring, cleaning up or blocked. Slow acquisition may make this remaining constant very poor; its positivity cannot be assumed. The generic native continuous-noise threshold remains open at the clean acquisition/service bridge. No weak-initiation effective Lindblad model or long-time simulation approximation has been invoked.
