# An ordinary counted resonator still wins with a shared endpoint-motion budget

24 October 2026. Physical owner `/root/passive_lag`; continuation of the
root-reviewed `DISTRIBUTED_FEJER_RODS.md` (SHA256
`e2b363a0d390a3552013fbcf4af4887b1c0953b201d0468ef512a9f6763c0ef3`).
Those reviewed bytes and the earlier heat-only incumbent are preserved.

This result supplies a stricter equally informed comparison, not a claim
that a one-pendant support is globally optimal. Both competitors are complete
scalar longitudinal metric graphs, with all rod inertia and all their
longitudinal modes. Ideal scalar joints, point end bodies, separated rod
routing and ideal Landauer contacts remain model premises. A full solid's
transverse/torsional modes, local continuum strain and atomic cutoff are
not acquired by this calculation.

## 1. The shared resources and the operation

Retain reference units `K=M_total=theta=hbar=1` and `a/c=1/sqrt(101)`.
The four-range Fejer graph is unchanged: point mass `100/101`, rod
stiffnesses `(.15,.10,.05)` and lengths `(a,2a,3a)`.

The new ordinary competitor has one length-`a` backbone rod of stiffness
one, a backbone point mass `m_b=.007`, and one pendant rod of length
`.4a`, stiffness `k=.6`, ending in a side point mass

    m_s=1-.007-1/101-.096/101 >0.

The rod masses are `1/101` and `.096/101`, so complete mass matches exactly.
Static translation of the pendant leaves relaxed stiffness `K=1`. Both use
the same material speed and period. The pendant area is `.24 K a/E`; the
backbone area is `K a/E`. Fejer's areas are `.15,.20,.15` times `K a/E`.
The ordinary construction does not require a smaller minimum area, but its
maximum cross-section is larger: no common maximum-width or junction-volume
constraint is silently asserted. Total rod length is `1.4a`, versus `6a`.

Impose the same additional reference-equilibrium requirement on each rod:

    Var(u_right-u_left) <= 6                                 (R)

in these fixed position units. Both models satisfy (R) for the full harmonic
Gibbs relative state at `theta=1`. The ordinary competitor nevertheless has
strictly smaller complete ideal thermal conductance:

    J_ordinary <.933891647 <.936840436 <J_Fejer.               (T)

The common cap is an explicit endpoint-coordinate resource, not a claimed
universal material failure threshold. It is useful because the previous
very-light-backbone heat-only incumbent violated it; the conventional design
can be retuned rather than excluded by topology. No practical merit of the
number six is inferred without physical units, geometry and a material limit.

## 2. Exact thermal comparison without frequency quadrature

For the ordinary network use the exact dynamic stiffness from the preceding
source. With `alpha=omega/sqrt(101)`, `s=.4 alpha`,

    A=k s cot(s), B=k s csc(s),
    Z=-m_b omega^2+A-B^2/(A-m_s omega^2),
    cos(q)=cos(alpha)+(sinc(alpha)/2) Z.

There is at most one right-moving channel almost everywhere at every
frequency, including all high rod bands. On `.79<=omega<=5.8`,

    m_s(.79)^2>k>=A,
    Z>A-m_b omega^2
     >= k[1-(.4)^2(5.8)^2/(2*101)]-.007(5.8)^2
     > [(5.8)^2/101]/[1-(5.8)^2/(8*101)]
     >=2 alpha tan(alpha/2).

The strict stiffness margin is greater than `.0009940607`. Thus the entire
interval has `cos(q)>1`, so no channel has been lost by selecting one branch.
The full Bose tail, with the one-channel bound, gives

    J_ordinary <=.79+exp(-5.8)[5.8^2+2(5.8)+2]/[1-exp(-5.8)]^2
               <.933891647.                                (14)

For Fejer the preceding proof already gives a unique acoustic branch below
the first rod pole and `omega(q)<.92`. Three direct full-field evaluations
sharpen its lower bound:

    D(.895,pi/2)> .0026637269,
    D(.895,pi)  > .0021374928,
    D(.862,acos(-2/3))<-.0004163557.

The strict negative frequency derivative implies acoustic frequencies
above `.895` at the first two wave numbers and below `.862` at the third.
Their order is `0<pi/2<acos(-2/3)<pi`. Put

    G(w)=w-w^3/36.

On `[0,.92]`, `g_1(w)>=G'(w)=1-w^2/12>0`. Weighted coarea, followed by the
variation over this four-point partition, gives

    J_Fejer >= TV(G(omega(q)))
             >=3G(.895)-2G(.862)
              =.936840436972222... .                        (15)

All higher bands are nonnegative additions. Equations (14)-(15) prove (T)
without integrating a discontinuous channel-count function.

## 3. Complete quantum endpoint covariance

Use the translation-quotiented finite ring and then its thermodynamic relative
covariance limit. The unpinned global position has no trace-class Gibbs state;
only the displayed zero-total-force relative observables are used. At positive
imaginary frequency `nu`, eliminating rod interiors gives positive Euclidean
dynamic stiffness. With `nu_l=2 pi l theta`, the exact scalar spectral identity
gives, for a relative endpoint-force vector `f`,

    Var(f*x)=k_B T [ C_f(0)+2 sum_(l>=1) C_f(i nu_l) ],
    C_f(i nu)=f* D_E(i nu)^(-1) f,                          (16)

with Bloch averaging implicit. This is the full quantum covariance, not a
classical approximation or a sum over only acoustic modes. It follows from
`coth`'s partial-fraction identity applied to each positive mode.

Every eliminated rod contributes a positive Euclidean form. Therefore

    D_E(i nu) >=nu^2 M_point,
    C_f(i nu)<= [f* M_point^(-1)f]/nu^2.

The uncomputed positive Matsubara tail after `l=L` is thus at most

    [f* M_point^(-1)f]/(2 pi^2 theta L)                     (17)

in the displayed `hbar=1` units. The point forces are bounded vectors in the
mass Hilbert space because every point mass is strictly positive. This also
establishes convergence despite the infinitely many internal rod modes.

### 3.1 Fejer: exact static values and an all-mode upper bound

The static symbol factors as

    D_0(q)=(2/5)(1-cos q)[(1+cos q)^2+1].

Let `u=sqrt((sqrt(5)-1)/10)` and `v=sqrt((sqrt(5)+1)/10)`. The exact static
endpoint compliances for spans `n=1,2,3` are

    C_1=5v, C_2=10u, C_3=20-20u-15v.                       (18)

For example, the mean of `1/(1+cos q+i)` is
`1/sqrt((1+i)^2-1)=u-i v`, fixing the square-root branch by positive real
part. Taking real and imaginary parts and dividing the three Chebyshev
numerators proves (18). The values are approximately
`2.844322405,3.515775843,4.435481100`.

For a positive mode, `coth(x)<=1+1/x` and Cauchy-Schwarz imply the all-mode
Gibbs estimate

    Var(f*x)<=k_B T C_f(0)+(hbar/2)
                      sqrt([f* M_point^(-1)f] C_f(0)).       (19)

Here `f* M_point^(-1)f=2/(100/101)=2.02` for each intervertex span. Equations
(18)-(19) certify endpoint variances no greater than

    4.042814297, 4.848242278, 5.932116646,

respectively. All three complete-field rod endpoint variances satisfy (R).
These are sufficient upper bounds, not asserted exact variances.

### 3.2 Ordinary pendant: analytic Bloch averaging and a finite certificate

For `nu>0`, set `eta=nu/sqrt(101)`, `zeta=.4 eta` and

    P=k zeta coth(zeta), C=k zeta csch(zeta),
    D=m_s nu^2+P,
    A=m_b nu^2+2 eta coth(eta)+P-C^2/D,
    B=2 eta csch(eta), S=sqrt(A^2-B^2)>0.

The Schur complement on the backbone is `A-B cos(q)`. Standard contour
averaging gives `mean[1/(A-Bcos q)]=1/S` and
`mean[cos q/(A-Bcos q)]=B/[S(A+S)]`. The exact full-field compliances are

    C_pendant(i nu)=1/D+(1-C/D)^2/S,
    C_adjacent(i nu)=2/S [1-B/(A+S)].                       (20)

At zero imaginary frequency they are `1/k` and `1/K`. No real-frequency
resonance quadrature remains. The certificate evaluates the first 128 positive
terms of (16) using exact outward rational intervals for `pi`, `sqrt`, `exp`,
`coth` and `csch`, then applies (17). It obtains

    4.466209420 < Var(side-backbone) <4.523153240,
    5.733782276 < Var(backbone_(l+1)-backbone_l) <5.846863955.

Thus both actual rod endpoint observables satisfy (R). The interval widths
are honest bounds on the remaining positive tail, rather than numerical
convergence estimates. For comparison, the old `.001`-backbone, `.4`-spring
heat-only design already has adjacent variance greater than `7.9763` from
just its first twenty Matsubara terms, so it really violated this cap.

## 4. Certificate and physical decision

`certify_endpoint_range_comparison.py` uses only Python standard-library
integer/Fraction arithmetic. Every interval operation rounds outward at
30 decimal digits. Machin's identity bounds `pi` by alternating rational
series; positive exponentials use range-reduced Taylor sums plus a geometric
tail; square roots use integer `isqrt`. Small-angle trigonometric Taylor
bounds certify (15). Its assertions check the strict thermal gap and every
variance upper bound in this note. Printed decimals summarize exact interval
inequalities; floating point is used only in display.

The outcome is constructive for the comparison: ordinary local resonance
still supplies a lower full ideal heat link after matching this specified
quantum endpoint-motion budget, total mass, static stiffness and material
speed. Nonlocal dispersion itself is established prior science; neither
the ordinary network nor these certificates establish a fabricated support
or a new material interaction.

The cap prices collective endpoint motion, not maximum local strain within
the rods. The point-body geometry needed for a given end area, continuum
validity, finite contacts, transverse channels and any finite thermal current
still require their own physical model. In particular it would be wrong to
call the point masses guaranteed rigid bodies at all frequencies, or to
choose a common maximum-width limit after seeing this winner. The earlier
positive Fejer-versus-unadorned-rod theorem remains valid, but it does not
establish a practical advantage over the stronger conventional support.
