# Predetermined raw-source horizon for the matrix GLS candidate

28 October 2026. Author finite-ledger companion to `ordinary_generic_matrix_gls_fast_design_20261028.md`, corrected SHA `a331566da59a07b7d9b679e4516368866fd38df20e44cff4f87f8496332d52ea`. It makes the source cap independent of every acquired design and record. It does not add a statistical theorem or assume the candidate is received.

Take d=2k, r=min(d,3R), D=10d^2 and L=8D. For prescribed rational gamma,epsilon, choose J as the least integer with eta_J=2^(-J)<=gamma epsilon/(2^15 k), beta=epsilon/32, and an odd integer b>=8 log(2DJ/beta). Ceiling logarithms may use certified outward integer bounds; no comparison at an irrational equality is required.

For each j=1,...,J, define eta=2^(-j), n=ceil(2^24 D L/eta), f=ceil(2+r/eta), m_bar=n+f+1, and

    zeta=min{eta/(10^6 D n),m_bar^(-2)},
    S=10+ceil[D log_2((4/eta)/2^(-20))]+1.

This S bounds every possible design support, including failed statistical histories, because the range-certified envelopes alone imply the determinant cap. For any realized pi, m_i=ceil(n pi_i)+f obeys

    m_i<=m_bar,   sum_i m_i<=n+S(f+1).

Let D_p=d*r, D_plus=2^ceil(log_2 D_p), and choose the explicit integers

    L_zeta=2+ceil(log_2(1/zeta)),
    l_bar=m_bar+L_zeta,
    beta_bar=zeta/[1000 l_bar^2 D_p^2 m_bar^2],
    n0_bar=ceil[320 D_plus log_2(12 D_plus/beta_bar)]+1.

The imported local estimator uses l_i=max(m_i,ceil(log_4(4/zeta))) and coarse failure target beta_i=zeta/[1000 l_i^2 D_p^2 m_i^2]. Thus l_i<=m_i+L_zeta<=l_bar, beta_i>=beta_bar, and its paid coarse bank is at most n0_bar. The entire homogeneous query bank is at most n0_bar+2m_i+L_zeta raw ordinary calls. (The logarithm base change is conservative because all displayed arguments exceed one.)

A predetermined stage cap is therefore

    N_j_bar=b [2n+S{2(f+1)+n0_bar+L_zeta}],
    N_bar=sum_(j=1)^J N_j_bar, H=N_bar+1.

Use this H for the retained causal common-frame compiler before any calibration records are available. Aborts and early design stopping may leave unused slots; dummy ordinary calls pad them when the compiler contract requires a fixed horizon. No expected-stopping source refund is taken. The one additional call is the subsequent payload. Local matrices are already finite receiver outputs; there is no uncounted final tomography bank.

The precision correction is explicitly preserved: the initial main manuscript requested eta/(10^6Dn) without spelling out the local import's zeta<=m^(-2) restriction. Taking the displayed minimum enforces that restriction uniformly over every support and batch. This only changes logarithmic bank/control work and decreases every bias bound. Initial source/test artifacts remain available under their `initial` filenames.

This cap is polynomial in the charged dimensions and inverse risk tolerances, with N_bar=O_tilde(k^5/(gamma epsilon)). It is deliberately conservative and is not a claimed practical experiment size. The receiver also pays every frame/purification memory and control operation specified by the governing imports; a source cap is not a total-gate cap.

The number of actual chosen-x homogeneous MATRIX-QUERY invocations is separately bounded by Q_bar=b sum_j S_j=O_tilde(k^2). Repeated banks at the same x count again. This is not a constant-support claim and not a source-cost bound: the invocation sizes in N_bar carry the fast inverse-accuracy cost. The polynomial-size encoder grid is scanned only classically.
