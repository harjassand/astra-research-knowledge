# A fixed-time one-use recovery obstruction from short calibration

28 October 2026. **Candidate corollary; independently unreceived.** Parent-proposed task bridge, derived from the frozen two-shift Singer construction in `PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH.md` (SHA `fb24c0a5e0e2033276c823363f52dbfa0e514790835a18cf4f13698fee81665f`). This file does not modify or inherit the receipt of that source. It is a two-world lower bound for a sharply specified one-use service, not a universal impossibility theorem for unknown-noise recovery, and not a novelty claim.

## 1. Precisely restricted task

Use the source's d=q+1, r=d²-d+1, memory densities rho_1,rho_2, forward channel `Psi`, effect E, and tau=I/d. Fix its strictly interior forward version `alpha=1-1/(2r)`. Replace the classical test/reset action with the quantum USE port below. The native library is ONLY:

* the forward channel on inaccessible memory, with one deterministic record;
* one quantum input-qubit/output-qubit USE port, resetting that memory to tau.

Whole-process reset restores rho_j, independently of the learner's retained systems. No inverse, hidden-memory control/readout, noise flag, coherent superposition of native action choices, or uncharged extra call is supplied. All native calls, including forward delays, count toward episode length.

Calibration may use arbitrary qubit states, retained references, entanglement among inputs and across episodes, quantum outputs recycled into later USE inputs, measurements, classical feedback and adaptive choice of independently reset episodes. Each calibration episode has at most r-2 native calls. The learner may retain all classical and quantum calibration data.

Deployment then starts with a **fresh whole-process rho_j independent of calibration data**. A future arbitrary qubit payload and its inaccessible reference are initially independent of the source and calibration systems. The prescribed deployment is r-2 forward calls followed by exactly one USE on that payload, with identity input encoding. A decoder can be any CPTP map on the received qubit and retained calibration systems to one output qubit. It cannot access the payload reference, bypass the channel with a retained payload copy, choose a different service time, make a second USE, or encode across uses. The comparison is with the optimal world-informed CPTP decoder for this same prescribed service.

The strict fixed-time/one-use condition matters: an earlier USE or a preliminary USE resetting to tau changes the task and can defeat this particular obstruction. The oracle's loss here has a substantial positive noise floor; this is not a lower bound near perfect correctability.

## 2. A centered physical memory effect

Write `k*=r-2`, and let

    A=alpha^(r-2),
    v=A r/(8d²) >=3/64,
    mu=[Tr(E Psi^k*(rho_1))+Tr(E Psi^k*(rho_2))]/2
       =1/2+1/(4d)+A(r-2)/(16d²),
    F=E+(1/2-mu)I.                                      (1)

All coefficients are rational except the already algebraic phase entries of U and the initial states. From `I/2<=E<=3I/4`, and since mu is an average of valid E expectations, `1/2<=mu<=3/4`. Consequently

    I/4 <= F <= 3I/4.                                   (2)

The two late effect probabilities are exactly

    f_1=Tr(F Psi^k*(rho_1))=1/2-v/2,
    f_2=Tr(F Psi^k*(rho_2))=1/2+v/2.                    (3)

At every earlier first-USE time k<=r-3, the two F expectations agree because F is an affine function of E and the two memories are normalized. On tau their common value is

    f_tau=1/2-A(r-2)/(16d²).                             (4)

The effect is fixed in advance for this dimension and chosen physical forward channel, not selected using an unknown world label.

## 3. Full CP quantum USE port and strict interiors

For memory effect G define the CP reset map `R_G(Y)=Tr(GY)tau`. Let Q be the input/output qubit and X its Pauli operator. Define on arbitrary joint inputs, not merely products,

    V_F(omega_QM)
      =(id_Q tensor R_(I-F))(omega_QM)
       +(Ad_X tensor R_F)(omega_QM),                    (5)

where `Ad_X(Z)=XZX`. This is CP and TP because F+(I-F)=I and X is unitary. It produces no classical outcome flag. Its output memory factors as tau from the entire qubit/reference output, even if its input was correlated: both terms have the same final memory state.

For an explicit full-Choi-interior version choose `lambda=1/4` and set

    V(omega)=(1-lambda)V_F(omega)
              +lambda Tr(omega) (I_Q/2 tensor tau).     (6)

The second term is a replacer on the full 2d-dimensional input. Its unnormalized Choi matrix is `I_(QM input) tensor (I_Q/2 tensor tau)`, so

    J(V) >= [lambda/(2d)]I = I/(8d).                    (7)

V is exactly TP. The memory-only forward channel separately has Choi floor `1/(2rd)`; the ports have their stated, different input dimensions. The extra mixture has no accessible flag. These are actual physical full-algebra maps, not a CP extension inferred from classical probabilities.

For product memory sigma and arbitrary input qubit/reference state, the induced complete qubit channel is

    N_f=(1-lambda)[(1-f)id+f Ad_X]+lambda D,
    f=Tr(F sigma),       D(Z)=Tr(Z)I/2.                 (8)

The statement is reference-complete because (5)-(6) explicitly define the channel on joint inputs and extend by identity to any reference.

## 4. Exactly identical complete short calibration

Before the first USE of an episode, the memory is `Psi^k(rho_j)` and is product with the learner's entire systems. This follows from the independent whole-process start and the fact that the only earlier source actions are memory-only forwards. For k<=r-3 the value f in (8) agrees in both worlds; hence the entire first-USE input/output channel, including arbitrary reference systems, is identical.

After that first USE the source memory factors as tau from **all** learner systems. It remains the same under future forwards, and subsequent USE ports act identically in both worlds, regardless of input entanglement, recycling, or feedback. Conditioning on a classical feedback history is legitimate; a quantum record need not be measured for this channel equality.

Thus every permitted calibration strategy with episode length at most r-2 produces exactly the same full classical-quantum output state in the two worlds. The conclusion iterates over independently reset episodes, including adaptive selection and retained entanglement across episodes. It holds for any finite number of starts, and for an almost-surely finite stopping rule when the resulting output is defined. No source samples or tomography are used in this proof.

This stronger short-input/reference equality follows from the explicit reset-port physics, not from importing a coherent guarantee from classical word equality. It makes no claim about free coherent superpositions of the native actions or additional hidden-memory access.

## 5. Optimal one-use recovery over all CPTP decoders

At the prescribed late time the qubit channels in (8) are Pauli channels. Let their probabilities be

    w_I,j=(1-lambda)(1-f_j)+lambda/4,
    w_X,j=(1-lambda)f_j+lambda/4,
    w_Y,j=w_Z,j=lambda/4.                               (9)

Set `c=1/2-lambda/4` and `t=lambda/4`. The weights on I and X are `c±(1-lambda)v/2`, swapped between worlds; both other weights are t. The unique best Pauli correction is I in world1 and X in world2. These corrections are also optimal over **every CPTP decoder**, as follows.

For any qubit CPTP decoder R with Kraus operators K_l, define

    a_P=F_e(R after Ad_P)=(1/4)sum_l |Tr(K_l P)|²,
                       P in {I,X,Y,Z}.                 (10)

The a_P are nonnegative. Orthogonality of the Pauli operator basis and `sum_l K_l†K_l=I` give `sum_P a_P=1`. Equivalently, they are the Bell-basis diagonal of R's normalized Choi state. By linearity,

    F_e(R after N_j)=sum_P w_P,j a_P <=max_P w_P,j.       (11)

I or X correction attains the maximum. The optimal Bell loss in either world is therefore

    L*=1-c-(1-lambda)v/2.                               (12)

Calibration leaves the same classical-quantum state in both worlds, independently of the fresh deployment. Any decoder using that state induces a single effective CPTP map R on the received payload, or a common mixture of such maps. Averaging the two worlds' scores and using `c>=t` gives

    [F_e(R after N_1)+F_e(R after N_2)]/2
        =c(a_I+a_X)+t(a_Y+a_Z) <=c.                    (13)

Consequently the mean of the two Bell-loss regrets is at least

    (1-lambda)v/2,

and at least one world has expected additive regret at least

    (1-lambda)v/2 >=9/512       when lambda=1/4.         (14)

The same bound holds for additive **half-diamond error regret** relative to the best decoder. For every channel, half-diamond distance from identity is at least its Bell loss, by testing the maximally entangled input and the Bell projector. For a Pauli channel, half-diamond error equals one minus its identity weight: the Bell input proves the lower bound and the triangle inequality over nonidentity Paulis proves the upper bound. Thus I/X correction attains half-diamond optimum (12), while (13)-(14) still lower-bound any decoder's average regret. This operational-norm conclusion is proved for these explicitly constructed channels; it is not extrapolated from a learned classical simulator.

## 6. What the lower bound does and does not buy

This gives a constant additive one-use recovery obstruction from any amount of shorter calibration, for memory dimension d and required late time `r-1=d²-d` total native calls. It is compatible with the received `O(d²)` short-experiment existence result and charges a shrinking forward mixing margin `Theta(d^-3)`.

It does not rule out choosing another service time, using a deliberate memory reset, coding over several USEs, richer encoders, informative hidden-noise flags, stronger native controls, source models with a fixed dimension-independent mixing margin, or longer calibration episodes. It neither proves a practical sample advantage nor addresses a near-zero-loss oracle. With a pre-call abort clock, reaching this particular target is discounted by its actual survival; a fixed abort rate does not preserve the constant lower bound automatically.

The underlying difference-set/Fourier quantum mechanism is credited in the imported source to Singer and the close Mereghetti–Palano/Bertoni–Mereghetti–Palano quantum-automata prior art. The decoder optimization here is the elementary Bell-diagonal Pauli calculation (10)-(13), not a claim of a new recovery method. Deterministic exact checks, not source acquisition, are recorded in `short_episode_one_use_recovery_check.py/.json`.
