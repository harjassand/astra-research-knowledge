# Independent full-chain receipt: conditional clean-core curvature and actual H path

26 October2026. **PASS** for `clean_core_conditional_curvature_operator_proof.md`. This receives the full conditional sign, not merely the earlier bounded parameter region.

## Integral/operator algebra

The actual determinant-gradient Ip Haar reduction has the correct2/3 factors, as independently reacquired in `clean_core_transport_threshold_schur_independent_check.md`. Its scalar K bound is strict for the present positive H2 because beta>0. The reciprocal tangent identity is valid for either sign of n, since sigma-n=c+sqrt(d)>0. Weighted Cauchy gives Z^2<=XY with the exact weight sigma^-2. Thus h<=delta X/Y implies Ip(h)>0, delta=2-sqrt3, and the unique Ip-zero is strictly larger than this threshold.

For S=A2+H2/3, V=detS, the qubit Haar identity gives trM=1 for M=V E[psi psi*/<S>^2]. Differentiating the divided-log integral gives precisely M=V integral adj(S+tI)/det(S+tI)^2 dt. The integral form of the2x2 determinant Minkowski inequality has the required >= direction because sqrt(det) is homogeneous and superadditive. Its integrand is det(S+tI)^(-3/2), and the exact scalar integral is2/[sqrtV(TrS+2sqrtV)]. Therefore

 tr(A2M)>=2sqrt(detA2 detM)
          >=4sqrt(detA2 V)/(TrS+2sqrtV)
          >=4detA2/(TrS+2sqrt(detA2)).

The last replacement keeps the actual TrS fixed and uses monotonicity of x/(TrS+2x), so there is no hidden false determinant/trace monotonicity. Since TrS=TrA2+TrH2/3, its denominator is no larger than the previously verified transport denominator. This gives X/Y>=4h_cert. As4(2-sqrt3)>1, the strict Ip-zero lies above h_cert, where the exact transport comparison makes Q0 strictly negative.

All quantities are finite for faithful A2,H2; no commutation or dimension-dependent approximation is used.

## Explicit actual-source realization of the negative Hessian

This can be received without a mixed reset variation or a third stationary equation. Diagonalize A2=diag(a,b), a!=b, and gauge H2=[[x,z],[z,y]] with z>0. The noncommuting assumption guarantees these conditions. At fixed A2 and fixed TrH2, define

 u=Tr(H2 adjA2)=b x+a y, v=detH2=xy-z^2.

For sufficiently small positive AND negative epsilon, take

 x_epsilon=x+epsilon/(b-a),
 y_epsilon=y-epsilon/(b-a),
 z_epsilon=sqrt(x_epsilon y_epsilon-v+3epsilon).

The square root is smooth since z>0. This preserves TrH2 and gives EXACTLY

 u_epsilon=u+epsilon, v_epsilon=v-3epsilon.

Faithfulness persists locally. Keeping the spectator h and reset fixed, this is an actual two-sided source curve, with fixed total source trace. Its acquired resolvent invariants satisfy

 s_epsilon=s+epsilon/D(t),
 p_epsilon=p-3epsilon/D(t),
 k_epsilon=k.

At a fixed-A faithful local minimum, independent u/v variations already give Is=Ip=0. Along this exact curve the second derivative is

 integral [ (s+k+1)^(-2)-2(s+2)^(-2)
            -2(k-1)^2/[p+(k+2)(s+k+2)]^2 ] /D(t)^2 dt.

The positive -3log[p+3s+9] Hessian vanishes because delta p+3delta s=0. The first two terms are exactly Q0; the last term is nonpositive. Hence the second derivative is strictly negative by the proved conditional Ip=0 theorem. There is no unreceived second-order coordinate correction: u,v are affine exactly, and the original source trace is fixed exactly.

This excludes any noncommuting faithful clean-spectator local minimum at fixed reset. It uses neither reset-determinant stationarity J=0 nor a rank-opening boundary derivative. If A2 is scalar, H2 commutes automatically, so the omitted a=b coordinate chart is already a paid aligned case.

## Scope

Combined with the previously received compact main boundary, reset spectral-floor, common-eigenline, middle-spectator and maximum-spectator reductions, this pays the remaining qutrit filtered-seed value class. This receipt itself does not assert the stronger anchored noncommuting reference-filter comparison, the general coherent-reset GLS inequality, or the unrestricted WH3 conjecture.
