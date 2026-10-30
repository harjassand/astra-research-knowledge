# Native isolated weak-initiation resolvent: fixed-window success and spectral excess
2026-10-30. New proof for independent review. Clean isolated controller only; no full-Hilbert DATA factorization is inferred.

## 0. Exact generator covered
Use `ONSITE_ABORT_BUSY_WITNESS.md`: only A0<->A1 has amplitude epsilon; every later coherent edge and every complete reset/monitor has a fixed positive rate; each A_i>=1 has a complete DATA-identity on-site abort to Q0. Freeze all overlap-neighbors ready, so all unclaimed local resources are free. Use the FULL read/write resource footprint. The exact forest-frame scalar controller has finite dimension, including its actual reset monitors.

The four phase families are I={A0 ready}, A={A_i:i>=1}, C={committed circuit phases}, and Q={cleanup/verification phases}. Clean aborts from A go directly into Q. There are no coherent fast edges between these families: A->C commitment, A->Q abort, C->Q terminal, and Q->I ready return are separately resolved irreversible jumps. Internal acquisition, circuit, cleanup, verification and monitor Hamiltonians stay in one family. This statement would fail for the older coherent A_k<->C0 architecture.

Kill only the successful C-terminal gains, retaining their complete losses, to obtain the finite CP subunital generator K_epsilon*. All nonterminal reset DATA actions are identity. The successful terminal payload Phi_h is idempotent but is irrelevant to the scalar killed-clock calculation.

## 1. Fast zero-drive structure
At epsilon=0, the actual monitored fast-return paths in `ONSITE_ABORT_BUSY_WITNESS.md` imply exponential decay of the busy probability. For the killed process, an earlier useful terminal is absorption rather than a return. Thus every A/C/Q input either returns to I or is killed, at a uniform fast exponential rate.

The actual monitor on a fixed clock label is the driven two-level amplitude-damping process with Omega,kappa_m>0. It has a unique stationary state and a nonzero finite-dimensional gap. The idle monitor product therefore has a unique stationary state sigma_I. It need not be pure. Busy/idle coherences decay by complete positivity and the busy-probability bound (or directly from the resolved monitor/loss blocks).

It follows that K_0 has a SIMPLE semisimple eigenvalue zero and all other eigenvalues have strictly negative real part. Its asymptotic Schrödinger map is

    rho -> Tr(Q_return rho) sigma_I,

where Q_return is the effect of reaching idle before a useful terminal. In the Heisenberg picture,

    0<=Q_return<=I,
    Q_return|I=I,  Q_return|Q=I,  Q_return|C=0.

The families have no coherent fast couplings, so Q_return is family-block-diagonal. Every legal acquiring input has a fixed positive probability of successful commitment and terminal before taking an acquisition abort: select the finite fast acquisition/commit/C-terminal path, suppress competing aborts for its finite duration, and use the actual clock/lock monitor record. The same finite-rate path proof gives, uniformly over all acquisition states and monitor/reference states,

    Q_return|A <= (1-p_A) I_A,  p_A>0.                (1.1)

This is a finite local number independent of epsilon and volume.

## 2. Actual useful-event contraction of order epsilon squared
The old path certificate's ABSOLUTE finite-measurement-window error must not be applied unchanged to an epsilon-squared event: shrinking the monitor window with epsilon would lose the desired power. Use root's exact actual-monitor relative amplitude certificate in `producer-workspace/RELATIVE_WEAK_HOP_CERTIFICATE.md`.

Here are the native hypotheses explicitly verified. After a real monitor flush, factor out the monitors' no-emission amplitudes exactly. Let P0 be the genuine idle A0, W=0, all local locks free source; let P1 be the hub label A1. On the clean isolated range, P1 implies the first resource is owned by h and all later resources are free. Put G_epsilon=G0+epsilon V for the MAIN no-jump evolution, including every ordinary complete loss. Then:

* G0 preserves P0: every fast acquisition/abort/cleanup condition vanishes there, workspace refresh has a scalar complete loss, and all monitor Hamiltonians/losses have already been factored exactly.
* P1 V P0 is -i times the first acquisition partial isometry, tensored with identity on untouched registers. Consequently (P1VP0)^dagger(P1VP0)=P0 in the unit-amplitude convention. There is no dark source or syndrome condition.
* The finite isolated ||G0|| and ||V|| are fixed constants. A later acquisition rate may be very small but fixed independently of epsilon; this only changes these constants and the fast-path probability.

For fixed sufficiently small delta and every t in [delta,2delta], exact Duhamel expansion yields

  P1 exp(tG_epsilon)P0
   =epsilon integral_0^t P1 exp((t-s)G0)V exp(sG0)P0 ds+O(epsilon^2 t^2),

and the integral differs from tP1VP0 by O(B t^2). Choose delta first and epsilon small afterward. Then the actual selected projection effect obeys

  P0 exp(tG_epsilon)^dagger P1 exp(tG_epsilon)P0
      >= (epsilon^2 delta^2/4) P0.                    (2.1)

Select no ordinary main jump before t, no competing monitor emissions, and an actual target-label A1 monitor emission at t in [delta,2delta]. The target emission is an EXACT clock projection, not an approximate simultaneous measurement. Its post-flush timing density is clock independent and has a fixed positive integral on this interval. An initial actual A0 monitor emission supplies the exact source projection and resets that monitor; remaining monitor silence factors are positive fixed constants. Thus (2.1) gives a real record-event probability at least c_weak epsilon^2.

After the A1 emission, consistency of the invariant good range fixes the owned first resource, free remaining resources, and clean workspace. A successful fast acquisition/commit/C-terminal path has a fixed positive conditional probability by the OLD monitored path theorem; applying its absolute-error bound is now legitimate because this conditional fast event is order one. All actual terminal workspace labels are summed completely. No rare DATA outcome is divided out.

For an arbitrary initial isolated state, the fixed fast instrument first reaches a genuine complete ready return or already emits a useful terminal with probability at least p0>0. At small epsilon this remains at least p0/2 by ordinary finite-time continuity. The event is order one, so no rare-event error problem arises. Start the weak-hop selection after the actual ready-reset stopping time, count any earlier useful terminal as success, and pad the observation interval to a fixed common T. We obtain the all-state actual-instrument bound

    exp(T K_epsilon*) I <= (1-c epsilon^2)I,          (2.2)

with c>0 fixed. This is the strict epsilon-squared event estimate; neither the monitor windows nor the observation time depend on epsilon.

## 3. Simple slow pole with a strictly positive second-order coefficient
K_epsilon is an analytic finite matrix family. Clean activity parity Z is +1 on idle and -1 on all busy families. Fast Hamiltonians preserve the BUSY mask; each actual CLEAN resolved fast jump changes a definite parity, hence its dissipator is parity covariant. The weak first acquisition changes parity. Thus

    K_(-epsilon)=Ad_Z K_epsilon Ad_Z.

The simple eigenvalue issuing from zero is analytic and even. Write lambda(epsilon)=lambda_2 epsilon^2+O(epsilon^4). The contraction (2.2) forces lambda_2<0. No assumed effective Poisson law enters this step.

The inverse therefore has a double-pole Laurent expansion. For

    R_epsilon=integral_0^infinity exp(t K_epsilon*)I dt
              =-(K_epsilon*)^(-1)I,

positivity and the normalized simple zero mode give

    R_epsilon=c_0 epsilon^(-2) Q_return
                +epsilon^(-1)Y+Z_epsilon,            (3.1)

where c_0>0, ||Z_epsilon|| is uniformly bounded, and epsilon^2 R_epsilon is analytic. The odd coefficient Y is Hermitian.

## 4. The odd coefficient cannot couple to the cleanup degeneracy
The order-epsilon equation is

    K_0*Y=-V* (c_0 Q_return),                         (4.1)

up to the homogeneous zero-mode coefficient, which parity sets to zero. The RHS lives ONLY in the idle/acquisition offdiagonal corner: the weak Hamiltonian connects A0 to A1, and Q_return is block diagonal.

That offdiagonal corner is invariant under K_0*. All fast Hamiltonians remain in their phase families. Every separately fixed-source/fixed-target jump gain annihilates an idle/acquisition offdiagonal observable. This includes the complete A abort, A->C commitment, Q->idle ready return, and resolved monitors; their losses preserve the corner. Monitor Hamiltonians act only on the monitor factors and do not change its phase-family labels.

Therefore Y has support only in I/A and A/I. In particular

    P_ker(I-Q_return) Y P_ker(I-Q_return)=0,

and the potentially degenerate Q-cleanup eigenspace of Q_return=I is not coupled by Y. This is the missing structural assertion that a generic killed resolvent would NOT supply.

## 5. Uniform O(1) spectral excess and the desired credit blocks
By (1.1), the A block of c_0 epsilon^(-2)(Q_return-I) is at most -c_0 p_A epsilon^(-2)I_A; the C block is at most -c_0 epsilon^(-2)I_C. Since Y only joins I and A,

  2 epsilon^(-1)|<u_I,Y u_A>|
   <= (c_0 p_A/2)epsilon^(-2)||u_A||^2
      +2||Y||^2/(c_0 p_A)||u_I||^2.

Combine with ||Z_epsilon||<=M to obtain

    R_epsilon <= [c_0 epsilon^(-2)+C] I,             (5.1)
    C=M+2||Y||^2/(c_0 p_A).

On the entire idle monitor block, not just its stationary vector,

    R_epsilon|I=c_0 epsilon^(-2)I_I+O(1),
    I R_epsilon (I-I)=O(epsilon^(-1)).

Choose the analytic even upper normalizer Rmax=c_0 epsilon^(-2)+C and beta=b epsilon^2 with fixed b small. Then

    S=(1-beta Rmax)I+beta R_epsilon,
    I/2<=S<=I,
    B=I-S>=0,
    B_idle=O(epsilon^2),
    B_idle,busy=O(epsilon),
    B_busy=O(1),

and S,B are analytic and clean-parity covariant. These are the actual input orders required by `ANALYTIC_GUARDED_USEFUL_CREDIT.md`; its virtual-ready-reset B branch avoids any nonanalytic principal square root of B.

## 6. Scope and review boundary
The proof uses the actual one-way phase-family graph, complete resets, actual label-resolved on-site reset monitors, a strictly positive fast acquisition-abort rate, and full read-footprint isolation. It does not apply to a coherent commit edge, unresolved workspace reset, a malformed controlled-mask terminal, or an arbitrary controller with a degenerate idle manifold. Full dirty-sector compatibility remains separate.

Section 2 explicitly checks the native hypotheses of root's actual-monitor relative weak-hop certificate. The target-label emission is exact; the old absolute-error path theorem is used only for order-one fast conditional events. All parameters are fixed before epsilon is made small.
