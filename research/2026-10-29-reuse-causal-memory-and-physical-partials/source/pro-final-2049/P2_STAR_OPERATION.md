# One-pass star entangler and loss-matched passive receiver

Root authored construction, 29 October 2026. Review status is separate. This uses the reviewed causal receiver as machinery, with an exact closed-form circuit, compatible conditional source couplings, and a strong conventional loss comparison. It is a conditional control capability, not a hardware advantage or a priority claim.

## 1. Exact ideal family

Let n=m+1 qubits have peripheral Z_j (j=1,...,m) and hub Z_n. Let K=2m sequential field modes have conditional coherent-displacement amplitudes

    alpha_j=g(Z_j+i Z_n),
    alpha_{m+j}=g(-Z_j+i Z_n).                              (1)

The statement is an operator displacement identity, not a coherent-input assumption. Baseline field states can be arbitrary and correlated, including source/reference correlations. Use D(alpha)=exp(alpha a†-alpha* a), D(alpha)D(beta)=exp[-i Im(alpha*beta)]D(alpha+beta).

A physically specified conditional-coupling schedule supplies both these features and an entangling gate. On a plus packet apply U_+=D(gZ_j)D(igZ_n), and on its minus packet apply U_-=D(igZ_n)D(-gZ_j), with rightmost operation first. Each packet visits each of its two source qubits once; reversing their order between signs matters. Exact Weyl multiplication gives

    product U_± = exp[-2ig² sum_j Z_j Z_n] product_k D(alpha_k). (2)

For g²=pi/8 the source operation is the maximally entangling star controlled-phase gate, up to known local Z rotations. This is established geometric/Weyl phase machinery, here connected to a one-pass output receiver. It does not create the native conditional-displacement interaction. The bounded phase-winding spin-flip primitive in ../comparator can supply it only with its additional sine-plus-cosine/source-axis interface.

The global feature Gram is diagonal: 2g² for each peripheral, Kg² for the hub. Every unfinished prefix has symplectic form g² u_k wedge e_n, where u_k is the signed incidence vector of open peripheral pairs. Its rank is two for 1<=k<K and zero at K. The complex bright-feature span has dimension n. The reviewed hybrid receiver therefore needs one inter-bin quantum mode, versus up to n for a generic coherent bright-span capture that postpones all measurement. This is not a comparison only to storing all K packets.

## 2. Explicit passive running-average circuit

Capture the first packet. At each k>=2, interfere the old memory b_{k-1} with the incoming packet a_k using

    b_k=sqrt((k-1)/k)b_{k-1}+a_k/sqrt(k),
    c_k=b_{k-1}/sqrt(k)-sqrt((k-1)/k)a_k.                  (3)

Thus b_k=sum_{t<=k}a_t/sqrt(k). Its conditional amplitude is g[(u_k dot Z)/sqrt(k)+i sqrt(k)Z_n]. The retired mode c_k has no hub component and only REAL peripheral amplitude

    d_k dot Z,
    d_k=g[u_{k-1}/sqrt(k(k-1))-sqrt((k-1)/k)s_k e_{j_k}]. (4)

Homodyne P of c_k, obtaining y_k. At k=K, u_K=0, so homodyne Q of b_K, obtaining x. Apply local feedback

    exp[i sum_{k=2}^K (d_k dot Z)y_k] exp[-ig sqrt(K)Z_n x]. (5)

All conditional field displacements cancel in the exact per-outcome operator identity. The actual complete source/reference/record instrument equals the source gate (2) and the same common passive refined homodyne measurement of the baseline field. Quantum fields are destructively measured, not returned to their original state. For initially correlated inputs the common measurement assemblage is preserved.

The real interferometer rows are (1,...,1,-(k-1),0,...)/sqrt(k(k-1)) for k=2,...,K and the final uniform row (1,...,1)/sqrt(K). They are exactly orthonormal. This proves the receiver without numerical SVD, approximate rank decisions or a Fock truncation.

There are K-1 two-mode beam splitters, K homodyne outcomes, one retained mode between arrivals, and two live modes during each mixing. No squeezing is used. Feedback can be deferred through the commuting source couplings here. Peripheral qubit j has no future output feature after its negative packet, so its accumulated frame can be completed then; the hub waits until the last record. Any later noncommuting source operation requires actual correction or valid frame propagation.

For vacuum baseline fields the conditional stored photon number is bounded by g²[k+min(k,K-k)²/k]<=g²K. Uniform source populations give g²[k+||u_k||²/k]. Total incoming conditional displacement excitation is 2g²K. Thus constant mode count does not mean constant energy at fixed entangling strength: g²=pi/8 gives peak <=pi m/4 and total pi m/2. Setting g²=1/K bounds those energies but reduces each pair's gate angle to 2/K. The source gate, memory duration, energy and precision must be compared together.

## 3. Match controls to known storage loss

Supply pure-loss power transmissivity tau between arrivals; target angle theta>0. Set g²=theta/(1+tau^m). Keep hub amplitude i g, plus peripheral amplitude g, and change minus peripheral amplitude to -g tau^m. With Section 1's source ordering the raw phase is exactly -theta sum_j Z_jZ_n. Common passive receiver loss adds no scalar source phase.

Write retained amplitude R_k dot Z+iB_k Z_n and C_k=B_k². Set C_0=0 and C_k=tau C_{k-1}+g². After the storage loss, mix the old mode and incoming mode with c=sqrt(tau)B_{k-1}/B_k and s=g/B_k: keep=c old+s incoming, retire=s old-c incoming. These coefficients satisfy c²+s²=1. The retired hub amplitude vanishes, leaving real peripheral features erased by P homodyne/local feedback.

For V_{j,k}=B_k R_{j,k}, the recurrence is V_{j,k}=tau V_{j,k-1}+g a_{j,k}, where a_{j,k} is the signed peripheral amplitude of the incoming packet. Hence V_{j,k}=g²tau^{k-j} for j<=k<m+j, zero otherwise. The negative packet cancels each peripheral exactly; final memory is iB_K Z_n, erased by Q homodyne/local hub feedback. The exact per-outcome operator identity removes observed displacement while retaining inaccessible loss displacement. Quantitative noise bounds next add explicit vacuum assumptions.

## 4. Complete noise certificate in the specified vacuum pure-loss model

Assume independent vacuum baseline packets and receiver-loss inputs, independent of arbitrary source/reference states. Conditional outputs of the passive network are products of coherent states. After the matched homodyne/local feedback, all observed records have the same vacuum distribution and factor from the residual source/reference channel. This conclusion is not imported to unknown thermal or correlated baseline fields.

The loss port after step k has amplitude sqrt(1-tau)(R_k dot z+iB_k z_n). Let S_k=sum_j V_{j,k}>=0. Since every open V coefficient is nonnegative, choosing all peripheral z equal attains the maximum total lost excitation:

    E_mem=(1-tau) sum_{k=1}^{K-1} [C_k+S_k²/C_k].          (9)

If every measured output also has pure-loss efficiency eta, the same real/imaginary alignment survives and feedback uses its actual sqrt(eta) amplitude. The total input displacement excitation is branch-independent,

    E_in=m g²(3+tau^(2m)).

Passive energy conservation then gives the EXACT maximum total inaccessible displacement excitation

    E_lost=(1-eta)E_in+eta E_mem.                          (10)

This includes all memory and detector loss ports; their Weyl phases and correlations are not discarded. They need not have an isotropic Gram matrix. Collection efficiencies unequal across modes require redoing (10), not substituting an average eta.

Let F_z denote the complete inaccessible displacement vector. The vacuum Kraus component is the positive diagonal A_z=<0|D(F_z)|0>=exp[-||F_z||²/2]. Thus A>=q I with q=exp[-E_lost/2]; all other environment outcomes form a CP remainder J with total effect I-A². For every source/reference input,

    halfdiamond(E,U_target)
      <=(1-q)+(1-q²)/2 <=2(1-q).                          (11)

Proof: compare A rho A with rho using ||A-I||<=1-q and ||A||<=1; its trace-norm difference is at most 2(1-q). The positive CP remainder has diamond norm ||I-A²||<=1-q². This accounts for every inaccessible loss outcome, not just no-jump survival. The same bound holds for the actual-record channel because its record is a common independent factor. Cap the bound by one.

Equation (11) is linear in weak lost excitation. A direct full-Stinespring triangle across each lossy hold would yield a much looser square-root-loss allowance. Changing to the exact coherent-output/Kraus representation preserves all channels while removing that certificate cost; it does not assume physical loss vanishes. Exact rational outward evaluation of (9)-(11) is in star_checks.py/json.

## 5. Strong conventional comparator: loss-matched closed Weyl loop

Allow the SAME bus to revisit the two sources. Four chronological kicks with three equal pure-loss holds are

    g0 Z_A, i g0 Z_B, -tau g0 Z_A, -i tau g0 Z_B.          (12)

After the fourth kick the conditional retained displacement is exactly zero. The source phase is +sqrt(tau)(1+tau)g0² Z_AZ_B; reverse the imaginary kick signs to match the negative target. Choose g0²=theta/[sqrt(tau)(1+tau)]. Lost amplitudes after the three holds are

    sqrt(1-tau)g0 Z_A,
    sqrt(1-tau)g0(sqrt(tau)Z_A+iZ_B),
    sqrt(1-tau)g0 i sqrt(tau)Z_B.

Every source label has the same lost squared displacement

    E_loop=2theta(1-tau)/sqrt(tau).                        (13)

For vacuum baseline bus and loss inputs, the vacuum Kraus operator is the scalar exp[-E_loop/2]I. The complete source/reference error is therefore <=1-exp[-E_loop]. The bus ends in vacuum independent of source/loss and can be reused without a reset. For m sequential edges, m[1-exp(-E_loop)] is a complete workload allowance by channel composition. It includes all emitted loss outcomes, not only no-jump dynamics.

Both routes require four conditional source displacements per edge. The loop needs repeated bus access to the sources; the streaming route needs two once-visiting packets per edge, a calibrated passive receiver, full output collection and source phase feedback. At fixed gate angle, star memory exposure grows quadratically with edge count in the weak-loss expansion, whereas repeated closed loops have a linear workload loss allowance. The loop can therefore be better when that access is available. The star result establishes a different causal interface, not an unconditional performance advantage. Its receiver benefit should be used where packet return is unavailable or where a specified emitted-field operation already needs erasure.

### Stronger comparator correction: one hold, or reordered pairs

Three holds are not necessary in this supplied control model. Because the star assumes negligible loss inside each two-kick source block, a fair loop may use (g0 Z_A,i g0 Z_B), ONE hold tau, then (-sqrt(tau)g0 Z_A,-i sqrt(tau)g0 Z_B). Its phase is (1+tau)g0² Z_AZ_B and its bus closes. Set g0²=theta/(1+tau). The only lost vector has branch-independent norm

    E_onehold=2theta(1-tau)/(1+tau).

For m edges, the joint vacuum Kraus is scalar, giving workload allowance 1-exp[-m E_onehold]. There are four kicks and one hold per edge, no receiver, and no fresh bus reset after closure. It matches m=1 receiver storage loss before detector loss. If all four kicks can be coalesced without any paid hold, this idealized model assigns no hold loss; finite pulse and transport loss must be included for both routes before a device comparison.

If arrival order and pulse amplitudes can change, resynthesize adjacent pairs using the m=1 construction: g_pair²=theta/(1+tau) and negative amplitude -g_pair tau. This gives repeated ordinary two-bin Bell erasure with one memory and shorter lifetime. Merely permuting the existing -g tau^m packets would leave V_after_pair=g²(tau-tau^m), so it is not a valid loss-matched receiver for m>1. At tau=1 the simple permutation suffices. The long accumulator theorem concerns its fixed order; no unrestricted scheduling advantage is asserted.

### A lower witness separates schedule loss from certificate cost

Choose a source label z attaining E_lost and its opposite -z. Their lost coherent states have overlap exp[-2E_lost] with no Weyl phase. The source input (|z>+|-z>)/sqrt(2) therefore proves

    actual complete halfdiamond >=(1-exp[-2E_lost])/2.

This matches the upper allowance to first order. At theta=pi/4, m=7, tau=0.999999, even eta=1 gives a star lower witness >5.0697e-5, while the one-hold conventional workload has upper allowance <5.4978e-6. At eta=0.99999 the star's complete error is enclosed between 0.0001606293 and 0.0001606487 within the stated model. Returning-bus access wins this compatible ideal-control comparison. It is not a lower bound on other source pulses, receiver designs or architectures.

## 6. Essential interface and interpretation

The exact star uses 2m supplied temporal field modes, four conditional source displacements per edge, calibrated passive memory capture/mixing, homodyne on every observed output and local source Z delivery. Plus packets visit hub then peripheral, minus packets peripheral then hub; a spatial implementation must provide opposite routing or equivalent local preparation. Propagation loss within those source blocks is absent from the supplied model and must be acquired for a hardware claim. The bounded phase-winding realization needs its separately stated coherent control interface; the earlier lone sine/contact model does not supply it automatically.

The loss-matched construction requires calibrated tau, delivered negative amplitude g tau^m, phase-stable receiver coefficients and measured eta. Source qubits remain coherent until their final correction/frame is available. Source preparation, pulse duration/delivery, independent relaxation or leakage, source readout and reset, mode mismatch, gain/phase drift and scheduling errors are additional. The exact mode theorem supplies none of these for free. For finite control errors, use the complete instrument/moment comparison rather than silently assuming exact tau or ideal sharp readout.

The ideal all-state theorem has no vacuum preparation premise. The quantitative loss certificate explicitly does: baseline packet, buffer and loss inputs are independent vacuum. The receiver ends destructively measured; physical reuse needs a reset or exact retirement/reload contract. At fixed theta, quantum mode count stays one while field energy, storage exposure and classical records grow. The conventional loop pays source return access and its own pulse/transport controls; the star pays output collection, interference and feedback. Actual native coupling and collection remain unacquired.

The consequential retained result is the passive causal measurement/erasure compiler, including an attained mode minimum. This star test constructs its source-operation bridge and shows when conventional control is stronger. It does not establish a computing advantage. Prior geometric/qubus ancestry is in ../comparator/COMPARATOR_AND_OBSTRUCTIONS.md; general receiver and memory ancestry is in ../causal/.
