# A direct variational recovery operator and its source-conditioned simulation

30 October 2026. Root's constructive derivation, following C's first joint
partial-transpose mechanism and B's independent complementary-observable/gapped-
polar architecture. This is NEW mathematical work; receiving whole challenge is
separate. No source or quantum circuit is executed by this file.

## 1. A physical receiver with a universal variational guarantee

Let N:k -> D be any CPTP map, with normalized Choi state J=(id tensor N)(Phi_k).
The transpose below is on the KNOWN logical reference basis, not an unknown
physical basis. Put C=J^(T_R), a Hermitian operator on C^k tensor C^D.
For any unitary U on a FRESH logical k-register A and physical B-register, define

    R_U(X)=Tr_B[U(I_A/k tensor X)U*].                   (1)

This is CPTP on the entire carrier. No postselection, inverse source, output
support projection or learned coordinate frame occurs in its definition.

For source Kraus matrices K_l, write

    w_(l,a,b)=<b|K_l|a>,
    v_(l,a,b)=sum_i <i,b|U|a,K_l i>.

The receiver Kraus matrices are
L_(a,b)=(I_A tensor <b|)U(|a> tensor I_B)/sqrt(k). Thus

    F_e(R_U N)=sum_(l,a,b)|v_(l,a,b)|^2/k^3,
    Tr(U C)=sum_(l,a,b)conj(w_(l,a,b))v_(l,a,b)/k,
    sum_(l,a,b)|w_(l,a,b)|^2=k.

Cauchy gives the COMPLETE-channel lower bound

    F_e(R_U N)>=|Tr(U C)/k|^2.                        (2)

Conversely, for every CPTP recovery R, transpose on the untouched reference
commutes with R, and Phi_k^(T_R)=SWAP/k. Trace-norm contractivity on Hermitian
inputs therefore gives

    F_e(R N)<=||C||_1/k.                              (3)

Choose a unitary extension of sign(C), assigning any unit-modulus values on its
kernel. Then Tr[sign(C) C]=||C||_1. If F_opt=max_R F_e(RN),

    F_e(R_sign(C) N)>=(||C||_1/k)^2>=F_opt^2.         (4)

This is a different receiver from Petz in general. Squared-optimal recovery
guarantees themselves are established (Barnum--Knill, Tyson); generic polar
recovery is also established. C owns the strong primary comparison. Equation(4)+does not establish historical novelty or query optimality.

## 2. A gap-free unitary and actual-source tail

Use the globally unitary regularization

    U_c(C)=(C+i c I)(C^2+c^2 I)^(-1/2), c>0.          (5)

Its real variational objective is sum_j lambda_j^2/sqrt(lambda_j^2+c^2).
For each singular value s the loss from s is at most min(s,c).

Let A=N(I/k), and let tau be its spectral tail after the largest d0 eigenvalues.
Take P=I_k tensor P_top,d0 and Q=I-P. Since -I<=SWAP<=I and id tensor N is
positive,

    -I_k tensor A<=C<=I_k tensor A.

If -B<=X<=B with B>=0, its positive/negative spectral projectors give
Tr|X|<=TrB; this does NOT assert the generally false operator inequality |X|<=B.
Consequently ||Q C Q||_1<=k tau. Also C-QCQ has rank at most2kd0.
The best-rank trace-norm bound gives

    sum_(j>2kd0) s_j(C)<=k tau,
    ||C||_1-Re Tr(U_c C)<=2kd0 c+k tau.               (6)

Combining(2),(3),(6) yields

    F_e(R_Uc N)>=max(0,F_opt-2d0 c-tau)^2.

If F_opt>=1-kappa, a coarse all-range consequence is

    halfdiamond(R_Uc N,id_k)
        <=k sqrt(2kappa+4d0 c+2tau).                 (7)

The bound is allowed to be vacuous. With c=epsilon^2/(16 k^2 d0) and a complete
unitary-implementation half-diamond budget epsilon/2, triangle and square-root
subadditivity give epsilon+k sqrt(2kappa+2tau). Neither numerical kappa nor tau
is an algorithm input. d0 is a chosen complexity index. There is no exact-rank,
exact-isometry, nonzero source spectral gap, or unknown adjoint supplier.

## 3. A source-native Hermitian map

A fresh normalized CHANNEL Choi programme J can be acquired by preparing the
known logical Bell state and one forward N call. On target A,B and programme
R',B', use the KNOWN Hermitian interaction

    F=k Phi_(A,R') tensor SWAP_(B,B').                 (8)

Direct matrix-index contraction gives E_J F=C. This is precisely the ordinary
partial-transpose Hermitian-map-exponentiation coupler, not a new HME primitive.
C's source proof acquires its controlling 2024 primary explicitly.

The channel marginal Tr_B' J=I_R'/k gives the stronger exact identities

    E_J F^2=I,  E_J Phi_(A,R')=I/k^2.                (9)

Although ||F||=k, its source-conditioned second moment is one. An operator-norm
simulation bill k^2 u^2 therefore overpays the actual source. This is the relevant
new resource calculation, which the general lemma below makes compositional.

For completeness, the actual target norm also obeys ||C||<=1/k. For either sign,
the map X ->Tr(X)I plus/minus X^T is CP (its Choi is I plus/minus SWAP).
Apply it on the physical half of J and globally transpose to get

    I/k tensor I plus/minus C>=0.

No numerical eigenvalue or source matrix is acquired by this proof.

## 4. Variance, rather than interaction norm, controls copy collisions

Let G be ANY known Hermitian system/programme interaction, programme state omega,
and H=E_omega G. Purify omega mathematically and embed system vectors by
V:x->x tensor |omega_pur>. Write Pi=VV*,

    B=(I-Pi)GV, D=(I-Pi)G(I-Pi),
    Delta=B*B=E G^2-H^2>=0.

For W(t)=exp(-itG)V=V a(t)+b(t), exact block equations give

    b'=-i B a-iD b,  ||a(t)||<=1,
    a'=-iH a-iB* b.

D is Hermitian, so its propagator has norm1 at every real time. Duhamel implies

    ||b(t)||<=|t| ||B||,
    ||a(t)-exp(-itH)||<=t^2||B||^2/2.                (10)

Tracing the programme kills the Pi/orthogonal cross terms exactly. The reduced
channel is a rho a* plus the CP b-branch. This and(10) prove, with arbitrary
adjoining references,

    ||Tr_prog[exp(-itG)(. tensor omega)exp(itG)]
                   -Ad(exp(-itH))||_diamond
        <=2 t^2 ||Delta||.                           (11)

All t are admitted; no missing asymptotic remainder or exponential-in-time
factor is hidden. Programmes are fresh and independent for successive steps.
m collision steps for total time T cost at most2T^2||Delta||/m. A control-
conditioned interaction obeys the same lemma, including off-diagonal control
blocks. The purifying system is solely a proof device, not an accessible port.

## 5. Create the polar gap by known control

Add a polarization qubit and set

    K=X_pol tensor C+cY_pol tensor I,
    G=X_pol tensor F+cY_pol tensor I.

Anticommutation gives K^2=I tensor(C^2+c^2 I), so the gap c is CREATED by a public
control term. No gap of C is promised. Equation(9) gives E G^2=(1+c^2)I, hence
the full controlled collision error is at most2(1+c^2)u^2 per step.

Furthermore sign(K) has off-diagonal blocks U_c and U_c*, so a public X after
its sign sends |0> tensor psi to |0> tensor U_c psi. Coherent binary sign-phase
estimation UNCOMPUTES its full phase record; only the desired polar gate remains.
Discarding a full phase estimate would dephase useful carrier coherences.

The physical exp(-iuG) is also known: compute the public Bell projector sector.
Outside it the interaction is cY; inside it, k X tensor SWAP+cY is a gapped
involution pair. Known rotations, controlled SWAPs and Bell controls implement
both sectors. C_SOURCE_PORT pays that literal circuit and B_POLAR_SUPPLIER pays
the sign-QPE/copy/error schedule. A large coefficient k is not a supplied unknown
Hamiltonian; its angle specification, native control time and precision still
count. A gate-model bound does not establish a physical coupling strength.

The resulting source-copy count is O_tilde(c^(-2) zeta^(-1)), with explicit
logarithms/constants in the source-port proof; ζ is the complete polar-channel
implementation accuracy. It is independent of ambient D as a query count.
All carrier storage and controls retain logD, source latency is real, and the
payload remains coherent for the WHOLE acquisition/control operation.

## 6. Architecture and honest endpoint

With N available ONLINE, programmes may be generated, used and discarded one at
a time. Live programme memory is one Choi carrier; the payload, fresh logical
receiver, polarization/control and finite QPE work must remain coherent. This
removes the common unknown dilation-frame factory and long-lived quantum
programme store from this architecture. It trades them for online source latency.
Pre-late-payload-only access instead requires storing the finite programme bill;
it does not magically produce an offline classical decoder.

C's exact complex-frame consumer checks the WHOLE PT map, its marginal second
moment, augmented interaction and actual receiver Bell contractions. Those are
finite algebra diagnostics, not source/circuit execution. Its conservative
same inherited k2,d04,epsilon.01 bill is about2.34e25 source calls, so practical
advantage is NOT ACHIEVED. Strong pure-isometry inversion, recent single-polar
Petz, HME, complementary-observable recovery, and the already admitted RDS route
all receive their real access and costs. A's matched flagged-source dictionary
shows source latency can be unavoidable while also showing this upper bill is
far from an established optimum. Priority remains UNKNOWN.
