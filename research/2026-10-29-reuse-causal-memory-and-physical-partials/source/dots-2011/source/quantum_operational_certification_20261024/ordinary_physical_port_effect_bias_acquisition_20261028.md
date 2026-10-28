# Physical-port acquisition needs positive error effects, not positive signed memory maps

28 October 2026. **New candidate hypothesis relaxation; independent receiving pending.** This is separate from the CP-bias physical-port reduction and all earlier received local theorems. The relaxation is proved here only for the full physical-input port with TRIVIAL emitted gauge. It explicitly permits retained which-error memory.

## 1. Same actual apparatus, weaker calibration premise

Keep the physical port, fixed unknown V with width-w Pauli-generator supports, ordinary product preparation/readout, finite stage caps, receiver controls and complete source form

    N=(Ad_V tensor id) sum_alpha(Ad_Palpha tensor F_alpha),
    F_alpha:M->M' CP, T=sum_alpha F_alpha TP.                    (1)

The instrument can retain arbitrary coherent memory and the sampled error label; it is nonanticipating with respect to current private input/readout/frame coins. Define its INPUT effects

    E_alpha=F_alpha^*(I_M')>=0, sum_alpha E_alpha=I_M,
    A_(i,j)=sum_alpha chi_(i,j)(alpha) E_alpha.                  (2)

Replace the signed-MAP CP assumption by ONLY

    A_(i,j)>=0, i=1,...,n, j=X,Z.                               (3)

Always A_(i,j)<=I. Equivalently the input effect of physical errors anticommuting with sigma_(i,j) is <=I/2. No numerical positive margin is supplied. This is still a trusted qualitative source promise, not something finite records certify for every inaccessible memory state.

The signed memory map H_(i,j)=sum_alpha chi_(i,j)(alpha)F_alpha need NOT be positive or CP. Its output can have negative which-error blocks. The only statistic used to orient a physical generator is

    theta_(i,j)(omega)=Tr H_(i,j)(omega)
                      =Tr A_(i,j) omega in [0,1]                (4)

for the actual positive conditional memory state omega. Thus (3) is sufficient and strictly weaker than CP positivity of H.

## 2. Exact local predictable means survive which-error records

The full unsigned identity remains I/2^n tensor T(omega), because every physical Pauli conjugates I to I, even if its memory map appends a distinct error label. The full signed output/memory operator remains

    [V sigma_(i,j) Vdagger]/2^n tensor H_(i,j)(omega).            (5)

This Hermitian contrast is not claimed positive as a memory map. Tracing outgoing memory gives the actual observable conditional mean. For a known output interval J containing the true fixed support B_(i,j)=V sigma_(i,j)Vdagger,

    rho_J=I_J/2^|J|,
    Delta_(i,j,J)=B_(i,j,J) theta_(i,j)(omega)/2^|J|.            (6)

If J is disjoint from the true joint X/Z support interval, its signed reduction is zero: B is supported outside J and is traceless. For a containing interval, ||Delta_J||1=theta and its signed gap is theta/2^|J|. At every reached bank the fixed B factors through the predictable average, giving precisely B theta_bar/2^|J| with theta_bar>=0. Arbitrary retained readout backaction changes omega but not these identities.

These are the exact identities needed by the ACTUAL paired-axis support and fine-sign algorithm of the received margin-free local source. Its coarse score proof only uses disjoint-zero/containing-norm behavior and confidence radii. Its fine orientation proof only uses a positive scalar multiplying a fixed reflection. Neither step now needs CP positivity of H on its retained output. This is a direct hypothesis audit of that algorithm, NOT a declaration that the original CP-premise theorem itself changed.

For clarity the concentration also survives: each actual output is produced by the CP TOTAL channel (1), not by H; fresh input axes/signs and product-Pauli measurements give the same unbiased shadow records, second-moment bound <=2*3^W I and centered-increment bound <=4*2^W used in the received fine proof. Matrix martingale concentration is conditional on the entire classical prior record and the actual positive memory state. It never requires H(omega) to be positive on M'. All coarse/fine finite unions, rational Jacobi residuals, strict guards, permanent asynchronous certificates and source caps are therefore unchanged after substituting (6).

On the same simultaneous good event, the learner acquires the same local operator approximations to B_(i,j). Its colored coherent full-n-qubit extractor is a literal physical inverse of V up to the same global complete-reference defect b. This certificate is about the frozen matrices and fixed V and remains valid for EVERY later source memory, including retained which-error records. The unknown payload is introduced only after acceptance. Source-membership, always-acceptance and record-wise posterior claims remain excluded.

If A_(i,j)>=theta_* I uniformly at every relevant declared history, then every actual conditional bias is >=theta_* and the physical-port instance rate remains

    O_tilde(A n12^W/(theta_*^2 b)) source blocks,

plus coarse acquisition, with the same funded-cap and complete-record implementation qualifications. The numerical theta_* need not be an input to the learner. Mere effect nonnegativity permits theta=0 and abstention. All n physical preparations/readouts per block, 2n private frame bits per service, local reflection synthesis, routing, known code circuits and whole-process errors are still paid.

## 3. A physical mechanism that really retains the sampled error

Let a prior memory instrument have CP branches K_a:M->M0, sum_a K_a TP. Conditional on a, draw a Pauli pattern alpha with probability w_(alpha,a). Afterwards apply ANY trace-preserving memory channel J_(a,alpha):M0->M', which can append alpha, rotate memory depending on alpha, preserve coherences or keep additional classical records. Define

    F_alpha=sum_a w_(alpha,a) J_(a,alpha) composed K_a.           (7)

Because J is TP,

    E_alpha=sum_a w_(alpha,a) K_a^*(I_M0).                       (8)

Hence a branchwise physical anticommute-error probability <=p_max<1/2 gives A_(i,j)>=(1-2p_max)I, even though H_(i,j) can fail positivity maximally on its retained error flag. With conditionally independent per-site nonidentity rates <=p_max, a known code correcting all errors of weight <=t also has the uniform BAD EFFECT bound

    E_bad=sum_(alpha notin Good) E_alpha<=r I,
    r=sum_(s=t+1)^n binom(n,s)p_max^s(1-p_max)^(n-s).            (9)

For unequal rates the scalar Bernoulli domination is applied in each a branch. Then (8) lifts the scalar bounds to effects. Inter-use dependence through arbitrary J_(a,alpha) and K_a is allowed as long as the stated rate bounds hold at every relevant history.

Equation (9) does NOT imply sum_bad F_alpha<=_CP r T. Error-resolved retained memory can make that false. The broader finite-service common-clean-subchannel theorem is a SEPARATE source (`common_clean_subchannel_memory_bound_20261028.md`; consult its own receiving receipt before use). It can consume the acquired inverse certificate plus (9). The narrower id tensor TOTAL CP-domination corollary must not be substituted for it.

## 4. Exact error-tag counterexample and the retained service interface

For one physical qubit take

    F_I(omega)=(1-p) omega tensor |0><0|,
    F_X(omega)=p omega tensor |1><1|, 0<p<1/2.                  (10)

Then A_X=I and A_Z=(1-2p)I>0. The local physical port can learn both VXVdagger and VZVdagger from the ordinary signed means. Yet H_Z(omega) has a negative flag-1 block -p omega, so it is not a positive map. Also the native good map G=F_I does not satisfy G>=_CP(1-p)T: on flag 1 the difference is -p(1-p)omega. At p=1/4 the negative witness is -3/16. No amount of accurate inverse calibration changes that service-level obstruction.

The RECEIVED learned-extraction CP comparison to the PARTICULAR exact Pauli-instrument process still applies after calibration: it never required signed bias positivity at service time and permits arbitrary CP F_alpha, including (10). It does require exact declared controls, fresh privately retired PHYSICAL Pauli keys, and discarded receiver/gauge records. Generic finite physical control errors only transfer final process-distance statements with their norm debit; they need not preserve an exact CP decomposition.

Thus the new acquisition result genuinely extends to which-error-recording memory without either falsely strengthening a small effect into a CP map order or silently altering the existing theorem's source premise. The strongest conventional learner has the same physical access and can use the same algorithm. No generic non-Pauli source, unknown-code discovery or fault-tolerance threshold is claimed.
