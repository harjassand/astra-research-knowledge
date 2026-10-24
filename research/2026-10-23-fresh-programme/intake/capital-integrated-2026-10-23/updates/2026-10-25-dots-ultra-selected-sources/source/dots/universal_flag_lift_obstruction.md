# An exact obstruction to the naive SLD factor/flag lift

For a faithful baseline sigma and Hermitian tangent H, let L=Omega_sigma^-1(H). The variational factorization

    min_(X+X*=H) Tr X* sigma^-1 X = g^S_sigma(H)/4

has minimizer X=sigma L/2. A boundary reference-flag construction with offdiagonal X would need X_R=0 to preserve the reference marginal. H_R=0 only says X_R+X_R*=0.

The gap is not a harmless small correction. Take qubits A,R, 0<a<1, and

    sigma=(I+a Z_A tensor Z_R)/4,
    L=Z_A tensor X_R,
    H=L/4.

The anticommutator of Z tensor Z and Z tensor X is zero, so H=Omega_sigma(L). Thus H_R=0 and g^S_sigma(H)=Tr sigma L^2=1. However

    Tr_A(sigma L/2)=i a Y_R/4,

which is nonzero.

The unconstrained factorization cost is 1/4. Impose X_R=0. The signal offdiagonal blocks have no source term in H and can be set to zero in the minimizing quadratic form. The two diagonal signal blocks must be negatives. Write their reference offdiagonal entries as u,v; the condition X+X*=H gives u+conjugate(v)=1/4. The cost is

    [8/(1-a^2)] (|u|^2+|v|^2),

minimized at u=v=1/8. Therefore

    min_(X+X*=H, X_R=0) Tr X* sigma^-1 X
      = 1/[4(1-a^2)].

The penalty relative to the SLD minimum is 1/(1-a^2), unbounded as a increases to one. This does not refute universal complete-BKM/SLD equality: a different enlarged geometry can still work, and the classical Liouville construction does work even for this cq example. It does rule out claiming that the marginal of the naive factor optimizer can be removed at no leading-order cost within that same flag construction.
