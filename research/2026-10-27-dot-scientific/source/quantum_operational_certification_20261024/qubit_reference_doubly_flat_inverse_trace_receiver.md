# Doubly flat qubit-reference pointwise inverse-trace receiver

27 October2026. Direct consequence of the received qubit spin-flip spectral identity, now received for the pointwise inverse-trace and logdet objectives. This is not a general pinching or averaging lift.

Let M>0 on C3⊗C2 satisfy

Tr_A M=3I2, Tr_R M=2I3.

There is no upper spectral cap. The identity in wh3_qubit_reference_inversion.md, homogenized to trace6, makes NM spectrally equal to

[M+6I−(Tr_R M)⊗I2−I3⊗(Tr_A M)]/2=(M+I6)/2.

Therefore, writing m_i for the eigenvalues of M,

R(M)=TrM^(-1)−2Tr(NM)^(-1)+6
 =Σ_i [1/m_i−4/(m_i+1)+1]
 =Σ_i (m_i−1)²/[m_i(m_i+1)]≥0.

Equality holds exactly when M=I6. Likewise

2logdet(NM)−logdetM
 =Σ_i log[(m_i+1)²/(4m_i)]≥0,

again with equality only at identity. Singular-source boundary statements are understood as limits; the faithful pointwise formulas suffice for the stationary receiver.

Together with reference_classical_inverse_trace_exact_receiver.md, this shows that a hypothetical negative minimum in the received reference-two coercive stationary problem must have a nonflat physical marginal AND cannot lie in an orthogonal reference-classical algebra. Neither condition alone excludes all coherent nonflat sources, and no free twirl or pinching is used to impose them.
