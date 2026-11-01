# Genuine obstruction: geometric partition cancellation alone is insufficient

Status: derived counterexample, independently unreviewed. It does not violate the
positive-component theorem; it proves why that acquired premise cannot be dropped.

Fix beta=kappa=1, one transverse coordinate, s(y)=1+(1-y^2)^2 and b=1/2. Let

  U_R(x)=(x^2-R^2)^2, R>=1,    F_R(y,z)=U_R(s(y)z).

Each U_R is smooth, nonnegative and coercive, but its degree-two component is
-2R^2 x^2<0. Spatial dilation STILL gives exactly q(y)=s(y)^(-1), for every R.
Thus MA and k_free=1/(MA R0) are fixed independently of R. Here R0=443/240.
Nevertheless the frozen-fiber parallel conductance tends to0 exponentially in
R^4; low positive transverse mobility can approach it. Thus no positive universal
multiplicative full-rate lower bound follows from q or geometric cancellation alone.

## Fixed positive-measure slab pieces force an energetic channel barrier

On the center interval Ic=[-1/8,1/8],

  s(y)>=c1=8065/4096.

On Ie=[3/8,1/2],

  s(y)<=c2=7121/4096<c1.

Set A=(c1^2-c2^2)/(c1^2+c2^2)>0 and t*=2/(c1^2+c2^2). For every z:
- if z^2>=t*R^2, then U_R(s(y)z)>=A^2 R^4 throughout Ic;
- if z^2<=t*R^2, the same bound holds throughout Ie.

Both intervals have length at least1/8. Therefore, with
R_z=int_-b^b exp(F_R(y,z))dy,

  R_z >=(1/8) exp(A^2 R^4) for every z.

For |z|<=2R this gives integral 1/R_z dz<=32R exp(-A^2 R^4).
For |z|>2R, s>=1 and U_R(s z)>=(z^2-R^2)^2>=9z^4/16 throughout the slab, so

  integral_|z|>2R 1/R_z dz
    <=2 integral_2R^infinity exp(-9z^4/16)dz
    <=exp(-9R^4)/(9R^3),

using convexity z^4>=(2R)^4+4(2R)^3(z-2R).

## Normalization is controlled, not silently assumed

For |x-R|<=1/(4R), |x^2-R^2|<=9/16. Therefore

  Z_R=int exp[-U_R(x)]dx >=exp(-81/256)/(2R).

The exact parallel/full-free ratio is R0*(integral 1/R_z dz)/Z_R. The bounds give

  k_parallel(R)/k_free
    <=(443/240) exp(81/256)
        [64R^2 exp(-A^2R^4)+(2/(9R^2))exp(-9R^4)] ->0.

The low-mobility trial proof still applies to each fixed smooth coercive U_R:
its fixed-fiber committor has finite transverse energy on the bounded y slab,
because its derivatives grow at most polynomially and the Gibbs tail is quartic.
In detail, h_parallel is the ratio of partial to full integrals of exp(F_R);
differentiating these normalized integrals gives
|partial_z h_parallel|<=2 sup_(y in slab)|partial_z F_R(y,z)|, a polynomial bound
in z for fixed R. The transverse Dirichlet integral is finite since s>=1 and
exp(-F_R) has a uniform quartic tail on that slab. With scalar mobility gamma,
this trial has total energy cap_parallel+gamma E_z(h_parallel), while fixed-fiber
Cauchy gives cap_gamma>=cap_parallel. The gamma-down-to-zero limit follows.
Thus for every proposed positive lower factor there is a large R and a sufficiently
small but strictly positive constant transverse mobility giving a smaller ratio.
No exactly singular diffusion or infinite matrix is used as an admitted model.

## Global process is also legitimate

Here D=z.partial_z F_R=4(s z)^2((s z)^2-R^2)>=-R^4. The function y s'/s lies in
[-1,6], a loose uniform bound. With V=1+y^2+2z^2/M for any fixed scalar M>0,

  LV=-2[y s'/s+2]D+6 <=16R^4+6.

This earns nonexplosion. Coercive fibers and q=s^-1~y^-4 give a finite reversible
Gibbs law. The failure is not a missing process or divergent partition: it is the
negative homogeneous component/radial-well structure that invalidates the new
concavity comparison. A correct sufficient raw receiver must return UNKNOWN on
this family rather than accepting it from its geometric marginal alone.
