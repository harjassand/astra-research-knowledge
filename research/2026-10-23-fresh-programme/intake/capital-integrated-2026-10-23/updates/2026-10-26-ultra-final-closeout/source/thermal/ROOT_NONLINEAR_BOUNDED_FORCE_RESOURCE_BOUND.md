# Bounded force and curvature control all host energy excesses

26 October 2026. New root construction, independent whole review pending.
This extends the exact linear-force calculation to a nonlinear spatial
profile. Its purpose is to close a resource gap in the finite-aperture
canonical memory, not to infer a heat law, a real field generator or
historical novelty. The tools are canonical equations of motion and
positive KMS spectral measures.

## 1. Literal Hamiltonian and the curvature contact

Begin with a finite far-pinned Gaussian host

    H_G=p^T M^{-1}p/2+q^T K q/2,  M,K>0,
    Y=v^T q,
    H=H_G+H_A-lambda w(Y)Q.                            (1)

Q is a bounded Hermitian internal operator. The real profile w is C^2;
assume its force and curvature are bounded:

    f=lambda w'(Y)Q,       ||f||<=F_0,
    f'=lambda w''(Y)Q,     ||f'||<=D_0.                (2)

Use finite internal regulators first. The finite-aperture application has
bounded w itself, so stability and finite-volume Gibbs trace are immediate
when H_A has a Gibbs trace. More general w requires its actual lower-bound
and trace hypotheses. No mechanical momentum coupling is included.

Let beta=1/(k_B T), nu_n=2pi n/(beta hbar), and use FULL, uncentered
imaginary-time correlations

    Chi_AB(n)=integral_0^beta exp(i hbar nu_n tau)
                         <A(tau) B(0)> d tau.

Define

    G_n=(K+nu_n^2 M)^{-1},
    S_f(n)=Chi_ff(n),       c=<f'>.

For Hermitian f, its full Lehmann measure gives S_f(n)>=0, including
the diagonal/mean term at n=0, and

    (1/beta)sum_n S_f(n)=<f^2><=F_0^2.                (3)

Two host equations of motion give the EXACT identity

    Chi_qq(n)=G_n+G_n v [c+S_f(n)] v^T G_n.            (4)

For clarity, the first equation is
(K+nu^2 M)Chi_qq=I+v Chi_fq. Applying it with the f insertion gives
(K+nu^2 M)Chi_qf=v[c+S_f]. The extra c is the equal-time derivative
contact: [f,p_i]=i hbar v_i f'. KMS reciprocity supplies the other order.
This argument does not require a positive rotor path measure or that f
commute with H_A. Dropping the contact would incorrectly import linear
momentum domination into a curved profile.

Let Gamma_q=<q q^T>, Gamma_p=<p p^T>, and use a superscript G for the
unchanged Gaussian host at the same temperature. Equilibrium <p>=0.
The canonical momentum contact then yields

    Delta Gamma_q=(1/beta)sum_n[c+S_f(n)]G_n v v^T G_n,
    Delta Gamma_p=-(1/beta)sum_n nu_n^2[c+S_f(n)]
                                     (M G_n v)(M G_n v)^T.       (5)

These are full moments: no mean displacement is omitted from spring
energy. At n=0 the noncentered S_f contains its actual force mean.

## 2. Gaussian spectral sums, uniformly in the number of lead atoms

Put

    C=v^T K^{-1}v,       1/B_0=v^T M^{-1}v.

In mass-normal coordinates there is a positive finite measure mu such that

    v^T G_n v=integral dmu(omega)/(nu_n^2+omega^2),
    integral dmu=1/B_0,   integral dmu/omega^2=C.

The two required trace sums are

    L_M=(1/beta)sum_n nu_n^2 v^T G_n M G_n v,
    L_K=(1/beta)sum_n v^T G_n K G_n v.                 (6)

For x=beta hbar omega/2, the scalar sums are

    (1/beta)sum_n nu_n^2/(nu_n^2+omega^2)^2
          =hbar[ coth(x)-x csch^2(x)]/(4omega),
    (1/beta)sum_n omega^2/(nu_n^2+omega^2)^2
          =hbar[ coth(x)+x csch^2(x)]/(4omega).

For x>0, 0<=coth(x)-x csch^2(x)<=1 and
coth(x)+x csch^2(x)<=1+2/x. The first follows by differentiating
its increasing left side and its limit1; the second uses
coth(x)<=1+1/x and x csch^2(x)<=1/x. Cauchy--Schwarz then gives

    L_M<=hbar/4 sqrt(C/B_0),
    L_K<=k_B T C+hbar/4 sqrt(C/B_0).                  (7)

The spectral pointwise bounds needed for the positive S_f terms are

    nu_n^2 v^T G_n M G_n v<=C/4,
    v^T G_n K G_n v<=C.                              (8)

They follow respectively from u/(1+u)^2<=1/4 and
1/(1+u)^2<=1 under the same positive measure weighted by1/omega^2.

## 3. Complete kinetic and spring-energy EXCESS bounds

Let Delta T=<p^T M^{-1}p/2>-<p^T M^{-1}p/2>_G and
Delta U=<q^T K q/2>-<q^T K q/2>_G. Equations(3)--(8) imply

    -C F_0^2/8-c L_M/2 <=Delta T<=-c L_M/2,
     c L_K/2 <=Delta U<=C F_0^2/2+c L_K/2.             (9)

In particular, uniformly for T<=T_0,

    |Delta T|<=C F_0^2/8+(D_0 hbar/8)sqrt(C/B_0),
    |Delta U|<=C F_0^2/2
                +(D_0/2)[k_B T_0 C+hbar/4 sqrt(C/B_0)].           (10)

The positive part of Delta Gamma_p is also dominated by D_0 times the
positive matrix in(5) with coefficient nu_n^2 alone. Thus its total
mass-weighted trace is finite. The negative S_f part has finite total
mass-weighted trace by(8). Analogous K-weighted bounds hold for Delta
Gamma_q. If K is written as its actual sum of nonnegative spring forms,
the sum of ABSOLUTE local spring-energy changes is bounded by the same
positive majorants in(10); local kinetic changes have the analogous bound.
There is no cancellation of two unbounded reservoir energies in this claim.

With fixed physical terminal masses and a port spring kY^2/2,
C_reg<=1/k and B_0 is fixed independently of the far-pinned lead length.
All right sides are therefore uniform in the actual finite-band lead
regulators. Positive local sums/truncations and the stated local Gibbs
limits retain these excess bounds. The infinite equilibrium reservoir
baseline itself remains infinite; it has not been called a finite resource.

For a finite kinetic-energy canonical rotor H_A, use symmetric charge
cutoffs, the same uniform F_0,D_0, and its separately proved kinetic/form-
trace bounds before the local lead limit. No free two-state truncation is
needed. In the exactly linear case c=0 and F_0=lambda||Q||, (9) reduces
to the earlier momentum domination and finite-excess estimates. For a
curved profile c may have either sign, so exact domination need not survive.

## 4. Apply it to the fixed finite-aperture memory

Use the odd quintic w_L of ROOT_FINITE_APERTURE_CANONICAL_MEMORY.md.
For its r(s)=1-10s^3+15s^4-6s^5,

    ||r'||=15/8,    ||r''||=10/sqrt(3),
    ||w_L'||<=19/4,
    ||w_L''||<=(15/4+20/sqrt(3))/L.

For Q=2cos(phi), one may therefore set

    F_0=19lambda/2,
    D_0=(15lambda/2+40lambda/sqrt(3))/L.               (11)

Choose the FIXED E_R and finite L required by that source's full-sector
population and port-tail estimates. The canonical memory then has its
exact J/C protection, nonzero sector port dipole, finite actual rotor
kinetic energy, and the complete finite host kinetic/spring EXCESS bounds
(10), with all normal and lead modes retained. No temperature-dependent
barrier, inertia, pitch or aperture is introduced. This closes the
nonlinear-profile resource gap left explicitly open in that root note;
it does not reinstate its false stronger matrix-domination inference.

The eta-dependent cold spectral law, inclusive heat-current contract,
finite Gibbs/NESS preparation, actual field-generator mass/energy,
offset/control precision and symmetry-breaking tolerances remain separate
operations. A finite bounded model interaction is not an acquired device,
and static protected memory is not itself heat blocking or a mission result.
