# A finite classical pointer realization of the position-box contract

This optional implementation closes the local signal/backaction relation at the level of an explicit classical Hamiltonian model. It is not a claim that imprecision and disturbance can independently approach zero in fixed hardware, or below quantum validity limits.

For each of the two position windows, supply a fresh canonical pointer (Q,P), initially independent of the plant and old reference. Let it have finite mass m_d and known zero-mean initial variances v_Q,v_P. During a window of duration b, release its position trap and apply

    H_pointer + H_int = P²/(2m_d) − G w(t) x P,
    w(t)=(1−cos(2 pi t/b))/b, 0<=t<=b.

The window has integral one, maximum 2/b, maximum slope 2pi/b² and integral w²=3/(2b). The pointer momentum remains constant. Exact Hamilton equations give

    Q(b)=Q(0)+b P(0)/m_d − G integral_0^b w(t)x(t)dt,
    u(t)=G w(t)P(0)

for the source momentum force. Read the detached pointer after the interaction, when its measurement disturbance can no longer reach the plant, and set Y=−Q(b)/G. Its deviation from the weighted source-position average has root-mean-square bound

    e_x <= sqrt(v_Q)/G + b sqrt(v_P)/(m_d G)
             + e_read/G.                                 (P1)

Here e_read is the finite readout resolution/error of the detached pointer. Equal translated windows retain the positive-average momentum identity:

    M(Y_1−Y_0)/ell
      = integral_0^b w(s) [ell^(-1) integral_s^(s+ell) p(t)dt] ds
        + finite pointer errors.

Consequently the two-position momentum estimate from the main theorem remains valid with this e_x and with the same end time ell+b. Exact rectangular switching or an instantaneous momentum probe is unnecessary. The interaction amplitude is at most 2G/b and its slew at most 2pi G/b²; the physical control must provide these finite values.

For two independent identical pointers, the expected force action is

    E integral u² dt = 3G² v_P/b.                         (P2)

Thus the meter path-TV allowance is at most

    sqrt[3G² v_P/(8 gamma sigma² b)].                     (P3)

The initial pointer random variables are included in the Girsanov comparison and then discarded. For Gaussian pointer P, the usual sufficient exponential-integrability condition is satisfied when the corresponding action exponential moment exists; for each window, a sufficient condition is 3G²v_P/(4 gamma sigma² b)<1. In the useful small-disturbance regime this holds. Alternatively truncate the pointer momentum with a charged tail probability, obtaining a pathwise finite action bound.

Equations (P1)–(P3) are the joint imprecision/disturbance tradeoff. Increasing G reduces position readout error but increases source force action. Narrowing P or Q consumes a separately initialized pointer state and changes its finite hardware demands. A supplied classical Gaussian reset with these variances, finite time, energy and error is a substantive initialization resource. It can be modeled as equilibration of a finite harmonic pointer with stiffness k_d and bath thermal energy theta_d, for which v_Q=theta_d/k_d and v_P=m_d theta_d; its actual relaxation rate, cooling resource and trap release costs must be paid. No passive equilibration at fixed temperature and stiffness produces arbitrary chosen variances.

For a pointer with unchanged harmonic parameters, a prepared Gaussian at temperature ratio t=theta_d/theta_ambient has relative entropy t−1−log t against its ambient Gibbs state. Its nonequilibrium free-energy resource is theta_ambient times that quantity, in addition to actual finite-rate preparation work and refrigeration. This free-energy number is a lower bound/accounting resource, not a construction of a refrigerator at that lower bound.

The classical model requires phase-space spreads large compared with hbar on its operating scale. A quantum pointer cannot simultaneously have v_Q v_P below hbar²/4. The inequality is a genuine precision/backaction boundary; the theorem does not claim an asymptotic epsilon-to-zero classical implementation through it. A macroscopic family may enlarge its action/thermal scale and pointer resources while keeping all selected finite-error parameters within the classical regime. Hardware-dependent imprecision and disturbance floors remain in the final error law.

## Explicit finite reset of the isolated pointer

A known two-dimensional harmonic Langevin reset supplies the stated Gaussian pointer, rather than assuming a blank cell at no cost. While isolated from the plant, set H_d=P²/(2m_d)+k_d Q²/2 and couple P to a fresh bath of thermal energy theta_d with damping kappa_d. Choose k_d=theta_d/v_Q and m_d=v_P/theta_d. Its stationary covariance is Sigma=diag(v_Q,v_P). The actual noise/friction and bath temperature are supplied calibrated device resources.

Let A=[[0,1/m_d],[-k_d,−kappa_d]], B(t)=Sigma^(-1/2) exp(At) Sigma^(1/2), and rho=||B(t)||_op. Conditional on any initial pointer y, the reset output is Gaussian with mean exp(At)y and covariance Sigma−exp(At)Sigma exp(A^T t). If the initial pointer has arbitrary correlations with an old reference R but finite normalized second moment E_d=E[y^T Sigma^(-1)y], convexity of relative entropy gives the joint reset bound

    D(output_pointer,R || N(0,Sigma) tensor law(R))
      <= (1/2){rho² E_d − tr(BB^T) − log det(I−BB^T)}.

For rho<=1/2, this is at most (rho²/2)(E_d+1), and its TV is at most rho sqrt(E_d+1)/2. No initially finite relative entropy is required for this finite-dimensional reset; the finite Gaussian transition covariance regularizes a point initialization. Arbitrarily correlated old reference data are covered by the same averaged second-moment bound.

One explicit choice is critical damping kappa_d=2 omega_d, omega_d=sqrt(k_d/m_d). In normalized coordinates,

    ||B(t)|| <= (1+2 omega_d t) exp(−omega_d t)
              <= 2 exp(−omega_d t/2).

Consequently a reset error delta_d is achieved by choosing

    rho_* = min{1/2, 2 delta_d/sqrt(E_d+1)},
    t_reset >= (2/omega_d) log(2/rho_*).

The initialized pointer law is then within delta_d of the independent Gaussian used above; this law error simply adds to the final operation error. Two pointers pay two such reset errors. Its finite temperature, damping, trap preparation/release ramps, heat disposal and actual initialization work are separate physical costs. Initial energy is theta_d E_d/2; bringing the trap and kinetic parameters to their reset settings has work determined by those parameter changes and the initial moments. The formula gives the finite bath-contact time, not a zero-cost refrigerator or instantaneous change of mass/trap. If the device cannot provide the selected kappa_d, use its actual known matrix A and the explicit rho(t) condition, retaining the longer reset time.

After reset, release the trap before the measurement window using a known finite schedule and propagate its covariance through that schedule. Use the resulting v_Q, v_P and any covariance in the conservative bounds (P1)–(P3). The pointer is already free during the stated Hann window, so those signal equations require no instantaneous trap removal. Readout, coin logic and detachment/reset use fixed padded schedules: discarded fine values cannot choose a later source launch time or modulate residual source coupling.

## Bounded local interaction and switching work

The raw bilinear xP Hamiltonian is only a convenient calculation. For an actual finite-control construction, choose smooth odd saturations chi_x and chi_P, equal to the identity on |x|<=X_0 and |P|<=P_0, with derivatives between 0 and 1 and bounded magnitudes X_cap and P_cap. Such functions exist with X_cap<=2X_0 and P_cap<=2P_0: integrate a smooth even cutoff equal to one inside radius one and zero outside radius two. They also obey |chi_x(x)|<=|x| and |chi_P(P)|<=|P|. Implement instead

    H_int(t)=−G w(t) chi_x(x) chi_P(P).                    (P4)

This has finite peak interaction energy 2G X_cap P_cap/b. If the uncoupled plant-plus-pointer Hamiltonian is bounded below, adding (P4) preserves a finite lower bound. Pointer P is still constant, while

    Qdot=P/m_d−G w chi_x(x) chi_P'(P),
    u=G w chi_x'(x) chi_P(P).

Thus source backaction remains only in the noisy momentum coordinate, has finite peak force 2G P_cap/b, and obeys |u|<=G w |P|. The expected action (P2) and path-TV bound (P3) survive unchanged. The external coupling has finite slew 2pi G/b². Since the Hann window has integral |w'|=4/b, its switching work has the pathwise bound

    |W_switch| <= 4G X_cap P_cap/b                        (P5)

per box. Two boxes pay twice this, in addition to pointer preparation, trap ramps, readout, switching hardware and reset. All local field parameters are finite for any fixed allowed error and finite saturation radii.

On the good event that the passive comparison path stays within |x|<=X_0 and both initial pointer momenta satisfy |P_i|<=P_0, (P4) has exactly the same position signal as the raw bilinear calculation. On the passive path,

    E sup_{0<=t<=t_*} |x(T+t)|²
       <= 2X_*² + 2t_*² P_*²/M².

Therefore its source-range failure probability is at most that quantity divided by X_0². For independent centered Gaussian pointer momenta, both pointer failures together have probability at most 4 exp[−P_0²/(2v_P)]. A Gaussian initial pointer Q tail is treated in the same way. During the saturated interaction,

    |Q(t)| <= |Q(0)| + b|P(0)|/m_d + G X_cap,

so a finite ADC range covers the whole declared good event, with its own finite quantization error. These tail allowances enter eta_overflow in the main theorem.

No extra backaction TV factor is necessary for this range argument: first compare the actual saturated-meter source path to the passive path by Girsanov while retaining pointer seeds, then evaluate the same saturated readout functional on that passive path. It agrees with the ideal position average on the passive good event. This ordering makes the displayed passive range bound sufficient and avoids claiming that an unbounded bilinear interaction was physically implemented. If the source coordinate is angular, a globally valid angular readout or a separately certified local-chart/unwrap contract is required; a linear x pointer is not automatically a globally periodic rotor meter.
