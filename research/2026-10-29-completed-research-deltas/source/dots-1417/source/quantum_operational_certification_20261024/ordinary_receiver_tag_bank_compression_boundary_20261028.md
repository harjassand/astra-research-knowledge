# Receiver-side quantum tags: exact shared-bank interface and its variance boundary

28 October 2026, 13:06 UTC. A proposed physical compression of encoder-labelled banks, followed by an exact obstruction to claiming that compression alone gives a fast task rate. This does not alter any received learner. The constructive open step is adaptive design/localization, not free Choi preparation.

## 1. An actual constant-dimensional shared bank

For each independently sampled classical encoder z in S^3, prepare the ordinary loss state T_z in the one continuing receiver frame. At the receiver prepare a separate known four-dimensional tag |z>, and discard the classical z label after applying its calibrated controls. One obtains iid copies of the ACTUAL state

    Omega_pi=sum_z pi_z |z><z| tensor T_z.

The tag never coherently selects the unknown source: every source input is an ordinary known probe at one classical encoder. The state has dimension 4d and rank at most 4d, irrespective of the number of design support settings. Its tag preparation, output storage, frame horizon and one homogeneous-bank matrix query are paid. A retained classical z register changes the statistical experiment and is not silently included in this compressed-bank claim.

Write the true source as T_z=sum_a a_a(z) Theta_a in the ten real quadratic features. For a full-rank real-symmetric moment map

    M_pi(W)=sum_z pi_z (z^T W z) zz^T,

define W_x=M_pi^{-1}(xx^T). Then every Hermitian output observable C obeys

    Tr[Omega_pi (W_x tensor C)]=Tr(T_x C).

Thus fixed-degree moment inversion reconstructs the entire quadratic source linearly from a constant-dimensional quantum state. This is not a positive Choi completion: W_x is generally indefinite.

The EXACT second moment entering the received matrix-query covariance is

    Tr[Omega_pi (W_x tensor C)^2]
       =sum_z pi_z <z|W_x^2|z> Tr(T_z C^2).             (1)

It is not the square of the signed reconstruction, nor Tr(T_x C^2). The received local query would give a term of order (1)/m and a second-order rank term of order rank(Omega_pi) Tr(W_x^2)Tr(C^2)/m^2, in addition to its paid coarse bank and finite bias. A task-relative upper bound for (1), after actual adaptive design, remains required. The following example shows that no such bound follows from compression alone.

## 2. Exact finite design and two physical sources

Use four coordinate encoders e_i, each with probability 1/12, and all sixteen sign encoders z=(s_1,s_2,s_3,s_4)/2, each with probability 1/24. These twenty labelled settings implement the real-sphere fourth moments exactly:

    E z_i z_j=delta_ij/4,
    E z_i z_j z_k z_l
       =(delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk)/24.

They use finite rational amplitudes and known tag circuits. Consequently

    M_pi(W)=(2W+Tr(W)I)/24,
    W_x=12xx^T-2I.                                    (2)

Consider the physical input space C^4_selector tensor C^2_logical and the encoder |psi> -> |x> tensor |psi>. For h=0,1 and 0<delta<=1/2 set

    A_0=diag(delta,0,1,1), A_1=diag(0,delta,1,1),
    p_h(x)=x^T A_h x.

There is a single stationary CPTP source for each h whose encoded channel is the ordinary flagged erasure channel

    E_(h,x)(rho)=(1-p_h(x))rho direct_sum p_h(x)|e><e|.

An explicit Kraus list consists, for each selector i, of the success row sqrt(1-alpha_i)(<i| tensor I_2) into the logical output, and the two erasure rows sqrt(alpha_i)|e><i,b|, b=0,1. Their adjoint products sum to I_8. Thus this is an actual four-real-coordinate encoder family, not arbitrary independent values assigned to a matrix polynomial. The normalized encoded Choi rank is at most three. The two model optima are zero, at e_2 and e_1 respectively.

Every CPTP decoder has completed Bell loss at least 3p_h(x)/4, achieved by transmitting the surviving qubit and replacing the erasure by any state. Since

    p_0(x)+p_1(x)=2(x_3^2+x_4^2)+delta(x_1^2+x_2^2)>=delta,

the same chosen physical encoder/decoder cannot have small risk under both hypotheses. Full TNI instruments completed by any physical output obey the same lower bound.

## 3. Compression hides the useful rare erasure events

Let T_good be the fixed ordinary loss state of the identity qubit channel and T_erase the fixed loss state of complete erasure. They are normalized and have orthogonal output supports. Hence

    T_(h,x)=(1-p_h(x))T_good+p_h(x)T_erase,
    Omega_h=C_h tensor T_good+B_h tensor T_erase,
    B_h=E p_h(z)|z><z|=[Tr(A_h)I+2A_h]/24,
    C_h=I/4-B_h.

In the tag basis,

    B_0=diag(2+3delta,2+delta,4+delta,4+delta)/24,
    C_0=diag(4-3delta,4-delta,2-delta,2-delta)/24,

and h=1 exchanges the first two entries. Both models have the same support and commute. The entire quantum hypothesis test therefore reduces exactly to the eight classical weights consisting of the diagonals of B_h,C_h. Internal eigenvalue factors of T_good,T_erase cancel from the relative entropy.

For natural-log relative entropy, the classical chi-squared bound gives

    D(Omega_0 || Omega_1)
       <=(delta^2/6)[1/(2+delta)+1/(2+3delta)
                    +1/(4-delta)+1/(4-3delta)]
       <=delta^2/3.                                   (3)

The last estimate follows from the first two denominators >=2 and the last two >=5/2. The same bound holds with hypotheses exchanged. For N iid compressed copies and ANY joint receiver measurement,

    TV(output_0,output_1)<=sqrt(N delta^2/6),             (4)

by data processing, tensor additivity and Pinsker. Randomized classical processing is included. A padded protocol that stops early is also included in the deterministic N-copy cap. This statement is for this fixed compressed source, not for a protocol allowed to change pi adaptively or inspect the discarded labels.

For any final encoder/decoder selected from its record, the common-part argument and the pointwise sum-of-risks bound imply

    [E_0 ell_0+E_1 ell_1]/2
       >=(3delta/8)[1-TV(output_0,output_1)].             (5)

In particular N<=3/(2delta^2) leaves average completed risk >=3delta/16, although both omniscient optima are zero. This is a genuine task-risk obstruction for the COMPRESSED fixed-design experiment, not merely an inconvenient intermediate confidence norm. Collective quantum receivers cannot recover information erased by discarding the classical labels into the four-dimensional tag mixture.

The signed moment variance is already diagnostic. For x=e_2 under h=0 and C the projector onto the erasure output (tensor identity on the loss-state auxiliary qubit), the true mean is p_0(e_2)=0, but

    Tr[Omega_0(W_(e_2) tensor C)^2]=10+5delta.           (6)

Thus a nonvanishing first-order term remains at zero target risk. No diagonalization or exact matrix-mean primitive changes this identity.

## 4. Honest constructive counterpart and remaining scope

With the same supplied two hypotheses, an ordinary learner can query x=e_1 and observe the coarse erasure flag. Under h=1 its erasure probability is zero; under h=0 it is delta. N>=ceil(log(1/beta)/delta) such calls identify the hypothesis with error at most beta, after which it chooses the corresponding perfect encoder and an actual decoder. All labels, probes and outputs are ordinary. No supplied protected reference or collective receiver is needed for this comparison.

Therefore the fixed compressed design loses a fast task rate that a permitted ordinary adaptive/focused acquisition can attain. This does not rule out an adaptive receiver-tag construction: coarse localization could change pi, retained classical side information could be used by a different estimator, or several task-directed tagged banks could be acquired. Those mechanisms need their own variance, fixed-cap and decision proof. In particular the present example does not give a generic adaptive-source lower bound, a quantum-versus-conventional separation, or a lower bound on the received GLS constructions. It is linked to the earlier signed-anchor and row-cone boundaries rather than used to reopen them.

The potential benefit remains concrete: one successful adaptive tagged bank would pay a single O(d^2) coarse center and one rank floor instead of paying them separately at every support point. Equations (1) and (3)-(6) identify the exact issue such a construction must overcome. The received protected-reference entropy bootstrap is a stronger comparison wherever its explicit seed and coherent-control promises apply; this note does not hide those resources inside an ordinary tag.
