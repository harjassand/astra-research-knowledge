# Independent positive-grid matched-trial receiving review

## 1. Source boundary and verdict

**PASS, theorem-construction only, with the two explicit boundary/cost requirements in Section 8.** Exact source: `POSITIVE_GRID_MATCHED_CONSTRUCTION.md`, SHA-256 `3828b8fde54e0774e2ef635c1f6c32cdd362d2d826a21d9c98000166fd963d8c`. Read completely, snapshotted and unchanged. All four root component lemmas and the actual retained-process/domain sources were rehashed in `INPUT_SHA256.json`.

This validates the displayed finite positive scalar bounds and their mathematical primal/dual/rate join. It does not accept the candidate backend, reported floating values/runtime, any original external 10% request, exact-bit work budget, physical preparation or broader processing interface.

## 2. Actual coefficients and complete normalization

The positive even quartic grammar contains only pure z_i^4 and pair z_i²z_j² terms. For actual diagonal mobility entries mu_i, differentiation gives c_j=12mu_j d_j+2sum_i mu_i g_ij. The raw price must aggregate every literal contribution (or reject duplicates by an independently checked grammar); d_j and g_ij here are the actual total coefficients. A lower coercivity number dmin is not a valid substitute for d_j in this upper trace price. For example pure contributions 1+3 at coordinate 1, pure 2 at coordinate 2, pair contributions 5+7, and mobilities 2,3 give c=(168,120); using dmin=2 in the first pure contribution would underprice it. H=sum c_j² and the root factor are paid actual-model data. The unit-pure/unit-mobility path-coupling20 structure has H=4,322,048 as stated.

Use the inherited common scale w=exp(-beta vU)/Z_beta, Z_beta=int exp(-beta U). Put V=v_*, t=beta V u and phi=V-v. The frozen-fiber denominator is I(u)=2exp(t)J(t). The exact longitudinal cost therefore transforms to

    beta V^alpha C_frozen
      =1/Gamma(alpha) int_0^infinity t^(alpha-1)exp(-t)/(2J(t))dt.

For y>=0, h=B0/(2J), J=A0+B0. Differentiation with respect to u gives

    partial_u h= -beta(A0 Bphi-Aphi B0)/(2J²)=-beta D/(2J²).

Both numerator integrals use phi, not phi/V: the factor beta V from dt/du cancels the 1/V in the t derivative. This checks a possible normalization trap.

The accepted coarea bound gives the transverse prefactor beta^(alpha-1)sqrt(H)/[Gamma(alpha)(alpha+1/2)sqrt(dmin)]. Substitution u=t/(beta V), the derivative's beta² and multiplication by beta V^alpha leave precisely

    K=sqrt(beta H/(dmin V³))/(alpha+1/2).

The remaining integrand is t^(3/2)D²/(4J⁴)exp(t phi/V) under Gamma(alpha,1), over the entire unit-length slab. Thus (2) prices the complete actual Dirichlet energy, including transverse mobility, rather than a frozen-z generator. The Gamma law is an integration reference, not an assumed angular sampler or energy-coordinate Markov process.

## 3. Positive grid and derivative remainders

Assume an actual finite grid with 0<=L<T, positive integer N_t,N_y, h_t=(T-L)/N_t and h_y=b/N_y, all exact rational parameters before outward evaluation. On [0,1/2], phi and phi' are nonnegative and increasing, phi''=4kappa(1-3y²) is positive and decreasing, and f decreases in both t and y. Direct differentiation gives exactly the two second derivatives displayed in the source. Bounding each absolute summand by its appropriate endpoint and f(t,l) proves F2 and G2. No unjustified sign of f'' or (phi f)'' is assumed.

The single-cell trapezoid error has absolute bound h_y³ sup|f''|/12, and likewise for phi f. Clamping lower cell integrals at zero preserves their validity. Left prefixes and right suffixes must be independently summed from positive cells. A tiny suffix obtained by subtracting a prefix from a rounded total would have different error behavior and is not this construction.

The exact identity

    D(t,y)=int_(0<=r<=y<=s<=b)
             [phi(s)-phi(r)] f(t,r)f(t,s)dr ds

shows D>=0 and decreasing in t. On a y-cell [l,r], each positive primitive is monotone in its integration endpoint. Thus the upper products A0_hi(t_i,r)Bphi_hi(t_i,l) and lower products Aphi_lo(t_i,l)B0_lo(t_i,r) have exactly the safe subtraction directions in (3). Positivity permits max(0,...) without an unknown derivative sign. It is an upper enclosure; severe cancellation can make it loose, but cannot justify dropping error terms.

For the whole t-bin, J(t)>=J_lo(t_(i+1)) and f(t,y)>=f_lo(t_(i+1),y_(j+1)). The factor t^(3/2) is also bounded by its right endpoint. Multiplication of these pointwise nonnegative upper bounds by the exact Gamma-bin mass proves (4), including its factor 2h_y for the reflected half slab. Using an upper interval endpoint for each bin mass is safe. The Gamma density itself need not be monotone.

Integer-alpha survival S_alpha(t)=exp(-t)sum_(0..alpha-1)t^k/k! is exact; its derivative is -exp(-t)t^(alpha-1)/(alpha-1)!. Hence the stated differences really are nonnegative bin probabilities. All subtraction/cancellation must be outwardly bounded and lower probabilities clamped only in safe directions. This is not a floating Gamma-CDF quadrature assertion. Every denominator lower bound in (4) must be strictly positive or the receiver must refuse.

## 4. Analytic lower J is genuinely one-sided

For t>0, x=sqrt((2kappa/V)t)y gives exactly

    2J=[(2kappa/V)t]^-1/2
       int_(-sqrt(X))^(sqrt(X)) exp(-x²) exp[(V/(4kappa))x^4/t]dx.

The second exponential has a nonnegative argument. Its finite Taylor polynomial is a lower bound for every t>0, not only asymptotically. The symmetric x^(4k) Gaussian moment is precisely the lower gamma integral of shape 2k+1/2, with no missing factor two.

For X>0 and s<=1, x^(s-1)<=X^(s-1) on [X,infinity), giving the source's denominator-one upper tail. For s>1, the logarithmic derivative of exp(-x)x^(s-1) is at most -[1-(s-1)/X]. Integrating this exponential envelope proves (5) whenever its denominator is positive. If not, the full Gamma value is a valid tail upper. Using Gamma_full_lo-tail_hi and taking its positive part supplies a rigorous nonnegative lower moment. All Taylor coefficients and prefactors are positive, so their outward lower combination is a valid J lower. Taking its maximum with an independently proved trapezoid lower is safe.

Half-integer full Gamma values are rational multiples of sqrt(pi); any independently proved directed pi/root primitive is sufficient, with its actual work charged. No upper Taylor remainder is required for this lower-only use. No uncontrolled Laplace expansion enters this step.

The displayed transformed formula is not evaluated at t=0: J(0)=b exactly. This boundary branch is required if L=0 or a zero row is admitted; otherwise require L>0. The constructor reports that its candidate backend has this branch, but that implementation statement has not been audited here.

## 5. Both full scalar tails

On |y|<=b/sqrt(1+t), t phi/V<=kappa t/[2V(1+t)]<1/2. Since exp(-1/2)>1/2, the central interval gives 2J>=1/[2sqrt(1+t)], hence 1/(2J)<=2(1+t). The entire omitted lower and upper longitudinal tails are therefore bounded by twice the Gamma mass plus twice its first truncated moment. The latter equals alpha times the corresponding shape-alpha+1 Gamma probability. No t=0 singularity remains.

The accepted covariance identity implies |partial_u h|<=beta dphi/4, so D²/(4J⁴)<=dphi²/16. Since phi<=dphi and the slab length is one,

    P_z(tails)<=K dphi²/16 E[t^(3/2)exp(t dphi/V)1_tails].

The inequality 2t^(3/2)<=t+t² produces the **1/32** coefficient. Writing r=1-dphi/V=v(b)/V>0 transforms each tilted moment exactly:

    E_Gamma(alpha)[t^k exp((1-r)t)1_(t<L or t>T)]
       =(alpha)_k r^(-alpha-k)
          [P(Gamma(alpha+k)<rL)+P(Gamma(alpha+k)>rT)].

This proves (6), including both tails, both rising-factorial coefficients and every power of r. The potentially large inverse powers and cancellation in small lower-tail CDFs must all be enclosed together, as the source says. The L=32,T=400 diagnostic does not certify those numerical prices by itself.

The separate basin mass M still needs its already received full longitudinal infinity bound; the energy Gamma-tail calculation is not a replacement for M acquisition. All four component current bounds retain their complete far-well costs.

## 6. Actual primal/dual and declared reference rate

The shifted barrier parameter must pass a_bar in [v(b),v_*], equivalently the previously received admission for the proposed optimum. Its current gives a global signed-source bound B_f, and the new energy-dependent odd residual has its independently priced B_r. Global inverse-form triangle gives Q_psi<=Bpsi_hi. The trial is odd in y for every z, hence zero mean in the actual model, and the previous coarea/domain proof supplies full form membership. No killed/global inverse transplant is involved.

Let Cu be the complete outward actual energy upper and Ml>0 a lower bound for the actual basin mass M. Put lambda_star=Cu/Ml, k=2lambda_star. Since N=||psi||_w²>=2M>=2Ml and E(psi)<=4Cu,

    E_spectral(K/k)<=2Ml/N<=1,
    E_spectral(k/K)<=k Bpsi_hi/N<=Cu Bpsi_hi/Ml².

The inverse form is finite from actual currents. Form/inverse Cauchy implies N²<=E(psi)Q_psi<=4Cu Bpsi_hi, so the displayed epsilon is nonnegative for valid exact inputs. A negative purported upper defect would signal inconsistent receiving, not a license to assert an impossible sharper certificate.

The actual equilibrium capacity is at most the full trial energy, hence at most Cu. Therefore stationary completed-transition intensity is at most 2Cu/Ztot<=Cu/Ml=lambda_star. Both the spectral argument and count argument use the SAME explicitly declared rate. No unknown “true rate” has been midpoint-substituted, and no extra midpoint penalty is needed. Energy/mass/current slack is instead paid in epsilon. For a finite observation mesh the receiver must use this physical lambda_star consistently when constructing deterministic times and the comparison kernel.

All upper/lower mass directions are essential: quantities containing M² in B_f and E_rest need a valid upper mass, while rate/defect denominators use lower masses. The dimensionless conditioning identity is exact:

    Cu Bpsi_hi/Ml²
      =P_hi * [Bpsi_hi/(beta Ml² v_*^alpha)].

This prevents exponential scale from being confused with rare-event simulation. It does not remove the physical factor v_*^-alpha in the output rate or the exact full actual Gibbs|A initialization premise. The actual committor used for the stationary count proof is still a proof device; the new h_u is not asserted to equal it.

The sharper vector/path theorem may be applied at baseline B=0. The new U-dependent trial does not automatically inherit processing known to fix only scalar functions of y. A future U-preserving drift would still need its own full process, neutrality and count receiving.

## 7. Finite execution structure, not implementation acceptance

The uniform t-grid permits seed/ratio exponential enclosures and repeated outward positive multiplication along each y column. Inclusion is preserved, but interval width accumulates and must be paid; no floating seed or underresolved lower denominator may be smuggled in. Positive prefix/suffix rows and two adjacent t rows suffice. There is no hidden angular basis.

The declared O(N_t N_y+alpha N_t) arithmetic structure is valid when analytic Taylor order K0 is fixed (or bounded by O(alpha+N_y)); otherwise its additional N_t K0 loop and setup must be included. Root, pi, exponential, bit-growth, raw aggregation and recurrence-width costs also remain separate actual operations. The constructor reports a literal fixed K0=3 in its candidate backend, which is compatible with the stated structure; this report is not a whole-code verification.

Thus this construction gives finite, explicitly directed formulas with a legitimate UNKNOWN outcome when a bound, positive denominator, accuracy gate or original work budget is not resolved. It does not prove that any reported floating 1024x256 or 2048x256 output fits the complete original 10% request. Those numbers and the claimed backend runtime are not accepted by this review.

## 8. Controlling requirements and checks

Two qualifications control the frozen source without editing it:

1. Analytic lower-J is used only for t>0; an admitted t=0 row uses J(0)=b exactly.
2. Its displayed operation-order shorthand treats K0 as fixed/bounded; variable K0 incurs its actual extra loops and setup. The reported backend choices resolve these at the design level, pending separate whole implementation review.

`check_positive_grid.py` passed **469 exact assertions** without importing candidate code. Checks cover transformed beta/v_* factors, exact derivative identities and trapezoid constant, a positive decomposition of the D-cell excess, half-Gamma transformation, Gamma survival derivatives, tail moment factors, positive-kernel prefix/suffix fixtures, literal coefficient aggregation and reference-rate/count normalization. They supplement, not replace, the full proofs above.

All seven mathematical source bindings and the main source snapshot match. New artifacts are in this unique directory and bound by `AUDIT_SHA256.json`. Originals and earlier receipts were not edited. No external retrieval, helper agent, physical implementation or novelty claim is involved.
