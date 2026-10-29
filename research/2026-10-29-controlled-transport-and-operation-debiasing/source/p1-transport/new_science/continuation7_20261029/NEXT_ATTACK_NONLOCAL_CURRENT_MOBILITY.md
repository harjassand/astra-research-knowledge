# Next sustained attack: shaping a nonlocal current mobility

29 October 2026. Root research continuation. This file separates exact
intermediate algebra from an unproved larger action. It is not included
in the proved receiving theorem's claims.

## Consequential question

The conserving parity construction changes rare circulation while
preserving uniform equilibrium occupancies and the per-bond marginal
control clock. Can its entire current fluctuation law be characterized,
and can a small physically supplied kinetic memory shape collective
transport fluctuations without changing the mean diffusion law?

The point is a larger capability than repairing an averaging bound:
to know which parts of macroscopic stochastic physics can be selected
by the architecture of the control. A conventional MFT solver could
consume the resulting nonlocal mobility. The actual parity-coupled
rates and selective clock remain substantial physical premises.

## Exact intermediate identity for arbitrary weighted currents

Use the shared-clock ring r_i=c(1+alpha u delta_i), u=sigma p,
A=sum_i a_i, a_i=delta_i^2. For an interior particle sector A>=2.
For a fixed smooth spatial test H, put

    A_H=sum_i H_i a_i, S_H=sum_i H_i delta_i,
    F_H=A_H/A, J_H=sum_i H_i J_i.                       (1)

The sum over native jumps of H_i delta_i-alpha u_pre F_H(pre),
minus int c S_H dt, is exactly a martingale K_H. Its drift is zero
because sum r_i H_i delta_i=c S_H+c alpha u A_H and
sum_(active i)r_i=c A.

For two tests H,G its exact predictable covariance rate is

    d<K_H,K_G>/dt
      =c[A_(HG)-alpha^2 A_H A_G/A]
         +c alpha u[S_(HG)-F_G S_H-F_H S_G].             (2)

For fixed smooth tests, every S term is O(1) by summation by parts,
whereas A_(HG) is O(N). Hence the second line of (2) is negligible
at the usual current bracket scaling. This is an exact finite-state
martingale identity and a deterministic scale estimate, not yet a
replacement theorem for the original physical weighted current.

The obstacle appears in that last qualification. For native generator
L and F_H depending on occupancies,

    L(u F_H)=-2c u A_H-u L F_H.                         (3)

Thus the corrected physical current J_H+(alpha/2)u F_H has native
drift c S_H-(alpha/2)u L F_H, plus the common-clock drift
-alpha gamma_N u F_H. For H=1, F_H=1 and L F_H=0, giving the already
proved scalar-current construction. General H leaves a real residual.
Bounding F_H alone does not remove u L F_H over a diffusive horizon.

## Candidate action, not a theorem

If occupation replacement and the corrected-current residual can be
controlled under the required rare-history tilts, (2) suggests the
instantaneous current covariance form

    M_rho(H,G)=s[int chi(rho)HG
        -alpha^2 (int chi(rho)H)(int chi(rho)G)/int chi(rho)].
                                                               (4)

For 0<alpha<1 and C_rho=int chi(rho)>0, its formal inverse gives the
candidate action

    I_candidate=(1/(2s))int dt {
       int [j+(s/2)rho_x]^2/chi(rho) dx
        +[alpha^2/(1-alpha^2)](int j dx)^2/C_rho }.       (5)

The ordinary diffusion path j=-(s/2)rho_x has zero cost. The additional
term penalizes the spatially uniform transported current, since
int rho_x=0. At a flat density, (5) predicts the scalar current rate
q^2/[2s chi(m)(1-alpha^2)T], consistent with the scalar LDP now proved
under the canonical-initial interface in
`COMMON_CLOCK_MATCHING_RARE_TRANSPORT.md`. That scalar receiver does
not prove the proposed spatial action.

At alpha=1 the suggested covariance loses one direction; the rigorous
common-clock theorem already shows superexponential suppression of
nonzero circulation when gamma_N/N->0. Extending (5) to that singular
case would require an explicit constrained action, not insertion of
an infinite coefficient without a proof.

## Hard missing connections and failed shortcuts

1. The weighted corrector has a factor 1/A. Typical canonical activity
   is O(N), but rare phase-separated paths can visit much smaller
   activity. Typical concentration cannot be substituted into a
   speed-N action argument without paying its probability cost.

2. The extra term u L F_H is not pointwise small enough over N^2 time.
   Its cancellation needs a real inverse-energy or replacement
   estimate. The scalar identity avoids it only because F_1=1.

3. The relevant current comparison tilt is built from corrected
   increments, not simply the original E delta_i/N. The already proved
   independent-phase hydrodynamic receiver does not apply to this
   shared-clock process by renaming its field.

4. A changed CLT variance does not alone identify an LDP. The scalar
   strict upper bound was obtained independently by exponential
   martingales. The subsequent matching lower bound uses the special
   corrected-current tilt and an O(1) adjoint entropy source under a
   canonical initial law. A deterministic-initial matching lower bound
   and the full candidate spatial action remain separate tasks.

5. The known local SSEP action and generic fast-environment theory are
   close predecessors. A nonlocal covariance in this constructed
   family would not establish that such covariance or kinetic-memory
   control is historically new. Relevant internal-state exclusion and
   global-environment constructions need continued primary comparison.

The completed independent/grouped action programs remain useful even
if this candidate fails. They already supply a known macroscopic law
uniformly over the difficult parity family, while this attack asks
whether retaining selected collective memory offers an additional
physical control capability.
