# Uniform vacuum bias opens the published closed-line torus

Candidate theorem, independent review pending. Assume López2610.29921v1's
global coordinate/root theorem on E: Q=900(lambda-3/20)^2+100(beta-1/50)^2<=1.
For its field B0 and every0<delta<=59098749992960000000/389800418195322060363423
(about0.000151612844), all field lines of B0+delta*e_y leave that published
solid torus in finite forward phase/time. This concerns field lines, not
particle orbits, all vacuum fields or all coils. No physical field acquired.

## Exact geometry and return integral

Reconstruct the published X(lambda,beta,phi), zeta=sqrt(lambda)exp(i phi).
The source field is B0=grad phi. Exact symbolic identities give

    X_phi dot X_lambda=X_phi dot X_beta=0,
    J=det[X_lambda,X_beta,X_phi]=|X_phi|²/(2lambda).

Put h²=|X_phi|². Then B0=X_phi/h² and its flux two-form is dλ∧dβ/(2λ).
Uniform e_y is a valid vacuum perturbation, with vector potential
A=(X_z/2,0,-X_x/2). Write A_i=A dot X_i. Using phi as clock, the exact
perturbed equations are

    lambda'=delta*g_l/(1+delta*g_p), beta'=delta*g_b/(1+delta*g_p),
    g_l=2lambda(∂beta A_phi-∂phi A_beta),
    g_b=2lambda(∂phi A_lambda-∂lambda A_phi), g_p=(X_phi)_y.

Direct physical-cofactor checks give g_l=2lambda(X_beta cross X_phi)_y,
g_b=2lambda(X_phi cross X_lambda)_y. All three are finite Laurent polynomials
in exp(i phi) with rational coefficients in a=sqrt(lambda),beta.

The closed-orbit area obeys Area_y/pi=8lambda³(lambda²+2lambda+3)/(1+lambda)^6.
Consequently the phase means are

    <g_l>=0,
    G=<g_b>=-8lambda³(9-lambda+lambda²-lambda³)/(1+lambda)^7<0.

First-order one-transit increments are0 and2pi*G. For Q the averaged normal
forcing/pi is64lambda³(50beta-1)(lambda³-lambda²+lambda-9)/(1+lambda)^7.
At(3/20,7/100), inside Q=1/4, this equals-6130339200/3404825447. It already
precludes a differentiable perturbed foliation Q_delta=Q+delta*q1 by the
closed-orbit cohomological condition. The stronger argument below does not
assume that a new foliation varies differentiably.

## Exact periodic corrector

Choose a real zero-mean Fourier polynomial chi with chi_phi=G-g_b; each
nonzero coefficient is -g_b,k/(i*k). Exact coefficient identities and conjugacy
were checked. For beta_tilde=beta+delta*chi, direct differentiation gives

    beta_tilde'=delta*G
      +delta²(chi_lambda*g_l+chi_beta*g_b-g_b*g_p)/(1+delta*g_p).

The source ellipse lies inside a in[1/3,1/2], beta in[-2/25,3/25]. Exact
Fraction interval bounds on Fourier coefficients, followed by |exp(ikphi)|=1,
give the following uniform absolute bounds (no angular grid):

    C_gl=4213863/5120000,
    C_gb=381810191913/81920000000,
    C_gp=95121/64000,
    C_chi=1107422163549/409600000000,
    C_chi_lambda=876663035991837/40960000000000,
    C_chi_beta=5907087/3200000.

Since9-lambda+lambda²-lambda³>=9-1/4-1/64 on this larger box,

    -G>=m=1144832/56953125>0,
    M=C_chi_lambda*C_gl+C_chi_beta*C_gb+C_gb*C_gp
     =6951173438325359101131/209715200000000000000.

For delta<=min(1/(2C_gp),m/(4M)), equal to the stated bound,
1+delta*g_p>=1/2 and beta_tilde'<=-delta*m/2<0. Yet beta_tilde is a
single-valued bounded function on the source torus: phi dependence is periodic.
Its total range is at most1/5+2delta*C_chi, so residence phase is at most
2*(1/5+2delta*C_chi)/(delta*m). Also dphi/dt=(1+delta*g_p)/h² has positive
lower bound on the compact source torus. An orbit remaining forever would
have unbounded phase, contradicting the strict bounded-function decrease.
Every field line therefore exits in finite time.

## Evidence and boundaries

area_moment.py verified the physical orthogonality/Jacobian and vector area
exactly (~61.8s). uniform_field_averaging.py constructs chi and checks mean
drift/cofactor identities, then bounds all coefficients with exact rational
interval arithmetic (~3.2s). AVERAGING_RESULT.json records every coefficient
and bound. A naive .coeff call on a rational Laurent denominator initially
gave false zeros; saved code first clears the Laurent pole before Poly.

This is a specific sensitivity of the rational zero-shear benchmark. It does
not refute the source vacuum construction or imply that it claimed fusion
confinement. A compensating trim field, changed target geometry, finite
residence requirements and the independent irrational/sheared Sengupta family
remain alternatives. Uniform bias can be approached by exterior trim fields;
no finite-wire hardware is qualified here. Actual finite-coil resonant forcing
must be tested for that field: this example alone does not establish its loss.
Historical novelty and practical advantage remain UNKNOWN.
