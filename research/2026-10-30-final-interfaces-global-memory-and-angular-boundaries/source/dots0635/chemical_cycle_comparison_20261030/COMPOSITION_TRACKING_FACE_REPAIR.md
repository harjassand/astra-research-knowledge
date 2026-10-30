# A replacement for coefficientwise fugacity selection: cancel the face in aggregate

Status: internal derivation, unreviewed; local construction only, not a recurrence proof.

The earlier three-species obstruction forbids bounded smooth logarithmic-angular fugacity profiles with vanishing shift error. It does not forbid a profile tracking the actual composition near a tropical face.

For that example put r=A²/B³ and rho=c_A²/c_B³. Algebraically omitting the immigration contributions (not justified as lower order for this factorial-envelope ansatz), the two face defects are proportional to

    D_low=(rho−101)+r(100/rho−2),
    D_high=(100rho−2)+r(1/rho−101).

The coefficientwise constraints were incompatible, but choosing rho=r gives

    D_low=D_high=−1−r.

Thus the same composition-dependent choice cancels both pairs' internal currents in aggregate; the unit exits supply strict negativity. Near A~t³,B~t² it can be produced to leading order by

    F(A,B)=B[log B−1−(2/3)log A],

since ∂_B F=log(B/A^(2/3)), while ∂_A F=−2B/(3A)→0. Thus c_A→1, c_B~B/A^(2/3), and rho~r. This profile depends on physical prefactors, not only logarithmic angles, which is precisely the premise excluded by the no-go. It is not claimed to handle all strata or immigration terms by itself.

## Arbitrary-dimensional local face construction
There is a cleaner aggregate construction. Fix a strictly positive normal w with max_i w_i=1, a proper exposed face of a strongly connected complex graph, and alpha in(0,1). Let N=w·x and

    mu_w(x)=exp[−alpha N log N].

Consider rays x_i~c_i t^(w_i), c in a fixed compact subset of the positive orthant. For a reaction y→y' write delta=w·(y'−y). The incoming adjoint term has the asymptotic order

    mu_w(x−(y'−y)) lambda_y(x−(y'−y))/mu_w(x)
      ~ positive_constant * t^[w·y+alpha delta],

because N~Ct and all coordinates diverge. Let h=max_y w·y.

* Face-internal reactions have delta0, and their incoming/outgoing difference is O(t^[h−min_i w_i]); this is cancellation edge by edge, not a fictitious complex-balanced condition.
* Reactions leaving the top face have delta<0. Their outgoing negative term is order t^h and their incoming term is lower order.
* Reactions sourced below the face have outgoing order belowh, while their incoming exponent is (1−alpha)w·y+alpha w·y'<h, even if they target the top face.

Strong connectivity and properness guarantee at least one face exit. Hence L*mu_w<0 eventually on this ray and uniformly on compact prefactor sets. The same argument holds on a sufficiently small compact cone of log-directions around a unique exposed face, with a fixed strict gap where needed. No detailed balance, frozen background, or coefficientwise fugacity inequality is used.

The measure is summable with all exponential moments because w is strictly positive. However its adjoint sign has only been proved in the local sector, not everywhere. If the whole complex graph lies on the face, there is no exit and this argument makes no strict-drift claim.

## Exact remaining assembly obstruction
Taking a minimum over these global mu_w does preserve a valid adjoint inequality at a selected minimizer, but does not select the correct log-sector. For example, with A≫B≫C and normalized w_A=1, mu_w is smallest for the largest subleading coefficients w_B,w_C, not for the normal selected by log(B)/log(A),log(C)/log(A). Thus a mere covering by valid local sectors does not yield a global dual certificate.

This construction repairs the within-face integrability/coefficient problem locally. The unsolved part is an exact selector/assembly principle, including bounded-coordinate strata. Supplying that selector or a global barrier as an assumption would supply the decisive capability and is not done here.
