# Independent challenge of the proposed compressed relative-energy bound

29 October 2026. Review of root's proposal sent during this continuation,
before an actual governing proof was supplied. This is not a hash-pinned
acceptance of a later root document. No new worker or branch was created.

## 1. The proposed second-order constant is supported

Let A=[[a,b*],[b,C]] be a finite-dimensional nonnegative self-adjoint
operator, P the first-block projection, and suppose

    |<v,bu>| <= eta sqrt(<u,au><v,Cv>),    eta<1.       (1)

For (u(t),v(t))=exp(-tA)(x,0), put

    Eu=int_0^t <u,au> ds,
    Ev=int_0^t <v,Cv> ds,
    J =int_0^t Re<v,bu> ds.

The hidden equation gives

    ||v(t)||^2/2 = -Ev-J,

so Ev<=-J<=eta sqrt(Eu Ev), hence Ev<=eta^2 Eu.
The total dissipation is

    (||x||^2-||u(t)||^2-||v(t)||^2)/2
       =Eu+Ev+2J
       >= Eu+Ev-2eta sqrt(Eu Ev)
       >= (1-eta^2)Eu.                               (2)

The last inequality is completion of the square; it does not replace
the cross term by a wrongly signed equality. Thus

    Eu<=||x||^2/[2(1-eta^2)],
    Ev<=eta^2||x||^2/[2(1-eta^2)].                    (3)

For w(s)=exp[-(t-s)a]y, the visible Duhamel error is tested against y
by -int_0^t <w(s),b*v(s)> ds. Its absolute value is at most

    eta sqrt(Ev) sqrt(int_0^t <w,aw> ds)
      <= eta^2 ||x|| ||y||/[2 sqrt(1-eta^2)].          (4)

This proves the proposed uniform compressed-operator bound. It controls
P exp(-tA)P, not the full microscopic operator difference. Both projections
are important: the initial hidden component is zero in this statement.

For time-dependent blocks in a common Hilbert space and a fixed P, the
same calculation holds with time-dependent energies. The backward
visible test solves w'=a_s w, w(t)=y, so
int <w,a_s w> ds=(||y||^2-||w(0)||^2)/2. This confirms the proposed
externally prescribed time-dependent extension in finite dimension.
Unbounded operators require a separate form-domain/well-posedness argument.

The factor eta^2 reflects two passages between visible and omitted
directions. The uncompressed Veselić comparison remains a first-order
ordinary predecessor; no claim of priority for the compressed refinement
is made by this review.

## 2. The independent local-modulator calculation is exact

Let mu=pi(Y) product_i nu_i(H_i). Let K_i be the conditional visible
heat-bath projection at site i, and A_i=I-K_i. Suppose the actual visible
generator is sum_i lambda_i(H_i)(K_i-I), the hidden-only bath is
-kappa H with H=sum_i H_i, and its product equilibrium is the above mu.

For u depending only on Y,

    a u=sum_i m_i A_i u,
    b u=sum_i [lambda_i(H_i)-m_i] A_i u,
    m_i=E lambda_i.

Hidden independence and centering kill every i!=j cross term, even if
the visible Gibbs law pi is critical or strongly correlated. Therefore

    ||bu||^2=sum_i Var(lambda_i) ||A_i u||_pi^2
       =sum_i Var(lambda_i) <u,A_i u>_pi
       <= M <u,a u>_pi,
    M=max_i Var(lambda_i)/m_i.                        (5)

Zero-mean, nonnegative lambda_i vanish almost surely and contribute zero.
The equality uses A_i^2=A_i. For a general reversible Markov call rather
than a heat-bath projection, only A_i^2<=2A_i is automatic; its factor2
must be retained unless nonnegative spectrum or a sharper bound is known.

If each hidden bath has a supplied gap gamma, tensorization gives
C>=kappa gamma I on P-perp. Equations (1) and (5) then hold with
eta^2=M/(kappa gamma). No visible spectral gap enters.

The same orthogonality works for lambda_i(H_i,Y_(outside i)) with a
product hidden law independent of Y, provided the visible-context
coefficient is unchanged by the i update. The constants then become
uniform context bounds. A hidden conditional equilibrium depending on
the updated visible spin is not covered by this factorization.

## 3. A shared hidden modulator restores a volume factor

Take N independent fair visible spins, one shared hidden variable H,
and the same centered mobility xi(H) at every site. For
u(Y)=product_i(2Y_i-1), every heat-bath A_i satisfies A_i u=u. Hence

    ||bu||^2=N^2 Var(lambda) ||u||^2,
    <u,a u>=N m ||u||^2.                             (6)

The ratio in (5) is N Var(lambda)/m. Local visible updates alone do not
give the claimed dimension-free full L2 bound. The hidden independence,
or a quantitative replacement for it, is a genuine physical premise.

If each mobility depends on a finite hidden neighbourhood and disjoint
neighbourhoods are independent, a colouring with chi colours of the
overlap graph gives ||bu||^2<=chi sum_i Var(lambda_i)||A_i u||^2.
Thus a bounded overlap/covariance factor suffices. A single common bath
coordinate cannot be treated as bounded local overlap as the array grows.

## 4. A predictive hidden-energy variant and its acquisition limit

The sufficient bath condition can be localized to the mobility directions.
For xi_i=lambda_i-m_i, let G_i=<xi_i,H_i^dagger xi_i>. When these energies
are finite, the variational inequality C>=kappa H gives (1) with

    eta^2 <= (1/kappa) max_i G_i/m_i.                 (7)

Other hidden sectors may remain nonmixing. This requires xi_i to be
orthogonal to every invariant bath direction; otherwise G_i is infinite.
Independent hidden factors again eliminate cross terms in the inverse
energy. See LOCAL_MOBILITY_MOMENT_ACQUISITION.md for the bounded endpoint
version, an actual correlation experiment, and the slow-tail obstruction
to inferring (7) from finitely many lags without further premises.

## 5. Receiving scope which must remain explicit

If P is conditional expectation onto **all** visible configurations,
both P exp(-tA)P and exp(-ta) are positive stochastic kernels on the
visible space. The comparison is between genuine laws for the declared
projected initial preparation. It does not require exact finite sharp-
readout closure of the original microscopic dynamics.

The L2 bound supports equilibrium two-time correlations, fixed-size
readouts and bounded local reweightings of the initial equilibrium.
Turning it into a uniform guarantee for arbitrary microscopic initial
states can introduce their actual density cost. Long retained calibration
records or a controller changing the target equilibrium need their own
joint contract. A known equilibrium family does not determine an
unmeasured intervention's kinetic law.

The bath is an added physical operation and gamma is a warranted bath
property. Suppressing hidden fluctuations by making an actual independent
bath faster is not a discovery of averaging itself. The candidate addition
is the quantitative, gap-free compressed certificate coupled to physically
observable local supplier quantities and a consequential controlled family.
