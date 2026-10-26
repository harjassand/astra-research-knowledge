# Stage2 governing derivations

All statements have the explicit finite-network hypotheses below. They are
derivations in this trial, not claims of historical priority. Stage1 is
unchanged. In particular, the constant-system positive-gain fact used below
is established in Rantzer, Theorem 3:
https://arxiv.org/html/1203.0047v3

## A. Transient and time-varying shunt stress over the full model class

Let K_0 be a symmetric positive definite irreducible M-matrix, C a fixed known
positive diagonal matrix, b=e_0 and K_1=K_0+delta e_v e_v^T, delta>0. Initially
x_h(0)=0. For a common input u(t) and a nonnegative diagonal shunt schedule
D(t), consider

    C xdot_h = -(K_h+D(t))x_h + b u(t),   y_h=b^T x_h.

Assume D is piecewise continuous, or locally integrable where the fundamental
solutions exist. The schedule may be arbitrarily fast and arbitrarily large;
giving it for free only strengthens the attempted alternative. C is fixed,
and changing C without the corresponding physical balance terms is not in
this model. The input may have either sign and belongs to L2.

Write A_h(t)=-C^{-1}(K_h+D(t)), P=delta C^{-1}e_v e_v^T>=0, and let
U_h,D(t,s) be its state transition. These transitions are entrywise nonnegative
because the generators are Metzler. Variation of constants gives

    U_0,D(t,s)-U_1,D(t,s)
      = integral_s^t U_0,D(t,r) P U_1,D(r,s) dr >= 0.          (A1)

Adding a nonnegative diagonal loss also gives

    0 <= U_h,D(t,s) <= exp[-C^{-1}K_h(t-s)]                   (A2)

entrywise, by the same variation-of-constants comparison with D=0. Substituting
both bounds into the positive product in (A1) yields

    0 <= k_D(t,s) <= k_0(t-s),                              (A3)

where k_D=b^T(U_0,D-U_1,D)C^{-1}b is the difference of the two port impulse
kernels and k_0 is the unloaded difference kernel. This is a pointwise kernel
claim, stronger than comparing a few pulses. Both systems are exponentially
stable without D; positive D preserves the comparison and cannot cause growth.

The positive integrable kernel k_0 has total mass

    integral_0^infinity k_0(t)dt
      = b^T(K_0^{-1}-K_1^{-1})b = Delta_DC.                  (A4)

For every signed u, including under a time-varying schedule,

    |y_0(t)-y_1(t)| <= (k_0 * |u|)(t),
    ||y_0-y_1||_2 <= Delta_DC ||u||_2.                       (A5)

The last step is Young's convolution inequality. With D=0 the induced L2 gain
is exactly Delta_DC: the Fourier transform obeys |Delta G(iw)|<=Delta_DC,
with equality at w=0, and arbitrarily long slowly varying inputs approach
that gain. This is the scalar positive-system result in Rantzer's established
Theorem 3. It is not a newly discovered general control principle.

For any finite observation horizon and fixed input intervals, (A3) gives
entrywise domination of the loaded input-output matrix by the unloaded one.
These matrices are nonnegative, so their spectral norms obey the same order.
The ordinary conventional comparator is therefore the top right singular
vector of the unloaded finite-horizon matrix. It optimizes over *all* signed
inputs in that discretization under the same squared-input budget. The
unloaded comparator is not restricted to the constant pulse used for reference.

### Statistical and resource scope

For external parameter-independent white Gaussian readout noise

    dY_t=y_h(t)dt+sigma dW_t,

the relative entropy of two deterministic-drift experiments is
||y_0-y_1||_2^2/(2 sigma^2). Under the usual existence/integrability conditions,
the same Girsanov bound applies to causal policies: along a common observation
history, the policy supplies the same u,D to the two conditional state
equations, and (A5) holds pathwise. If the policy has a pathwise bound
integral u(t)^2dt<=B, its KL is at most

    B Delta_DC^2/(2 sigma^2).                               (A6)

Thus waveform choice, positive shunt timing and feedback do not remove the
exponential depth cost proved for the stage1 path family in this readout model.
Even the oracle comparator knowing both candidate networks cannot exceed the
bound. This conclusion follows over the full stated mathematical domain;
the frequency grid and finite-horizon tests are implementation checks only.

B is an L2 or *squared-input* budget. For electrical current it has units
current squared times time; it is not automatically dissipated energy.
Actual work is integral I(t)V(t)dt and depends on the network and source.
No universal lower bound under every possible physical energy convention is
asserted. Nor does (A6) cover state-dependent process noise, parameter-dependent
spectral noise, measurements of current inside the network or changing C.

## B. The configuration-independent noise assumption is not silently universal

Stage1's exact Blackwell comparator assumes fixed readout variance. Here is a
separate all-domain extension for a more physical *quasistatic* noise model.
Let F_h(d)=e_0^T(K_h+diag(d))^{-1}e_0 and suppose independent settled readings
are Gaussian with mean I F_h(d) and variance

    V_h(d)=a+nu F_h(d),   a>=0, nu>=0, a+nu>0.               (B1)

The term nu F is motivated by low-frequency Johnson-Nyquist voltage noise in
an isothermal resistor network; nu absorbs temperature and bandwidth. This is
not the total variance integrated over an arbitrary RC spectrum. In a real
finite-bandwidth experiment, settling, correlations, temperature and bandwidth
must be checked. The primary noise law is Nyquist (1928):
https://doi.org/10.1103/PhysRev.32.110

Stage1 proves Delta_F=F_0-F_1 is nonincreasing in every nonnegative shunt.
We also need the relative difference F_0/F_1-1 to be nonincreasing. Partition
off the port and write a_h for the input admittance:

    Y_h=1/F_h=K_h(0,0)+d_0 - q^T B_h^{-1}q,

where q=-K_0(I,0)>=0 and B_h is the interior principal block plus its loads.
For an interior fault, q is the same under both hypotheses and
B_1=B_0+delta e_v e_v^T. The internal potentials under port temperature 1 are
p_h=B_h^{-1}q, and 0<=p_1<=p_0. For each interior shunt j,

    partial Y_h/partial d_j = p_h(j)^2 >= 0,
    partial(Y_1-Y_0)/partial d_j = p_1(j)^2-p_0(j)^2 <= 0.

Port loading raises both Y_h by the same amount. Therefore

    F_0/F_1-1 = (Y_1-Y_0)/Y_0

is nonincreasing in every load. A fault at the port is immediate from
Y_1-Y_0=delta. Both the absolute difference Delta_F and relative difference
Delta_F/F_1 consequently decrease.

It follows that Delta_F/(a+nu F_1) is nonincreasing, because its reciprocal is

    a/Delta_F + nu F_1/Delta_F.

So both V_0/V_1=1+nu Delta_F/V_1 and Delta_F^2/V_1 decrease with loading.
The Gaussian one-reading relative entropy is

    KL(0||1)=1/2 [V_0/V_1-1-log(V_0/V_1)+I^2 Delta_F^2/V_1]. (B2)

Every term is nonincreasing because V_0/V_1>=1. The reverse KL decreases by
the analogous argument. Thus no positive shunt increases either one-reading
KL in (B1). Chain rule bounds T adaptive readings by T times the unloaded KL.
This is a KL comparison, not an unproved Blackwell statement for unequal
variances. It retains exponential deep-fault sample lower bounds in the path
family at fixed I,a,nu.

The additional spectral diagnostic uses complex Gaussian Fourier bins with
variance proportional to Re Z_h(iw), plus an optional floor. Its grid found
no improvement over unloaded DC on the 25 fixtures. That finite diagnostic
does NOT extend (B2) to arbitrary colored noise, arbitrary frequency, thermal
gradients or nonstationary fluctuation-dissipation settings. That extension
remains unproved here.

## C. Stronger positive mechanism: self-calibration from known capacities

Keep K unknown and let H=diag(1,h_1,...,h_{n-1}), h_i>0, be unknown shunt
gains. The source and port detector have a known common calibration. Suppose
the entire positive diagonal capacity matrix C is independently known. This
is additional physical information, available for example in an instrumented
RC network with known components; the proof does not invent it in an unknown
thermal specimen. The observable for a commanded nonnegative diagonal load U is

    z(s,U)=e_0^T[K+sC+H U]^{-1}e_0,  s>0.                  (C1)

These are two *real positive Laplace points*, not two sinusoidal frequencies.
Let S=H^{1/2}. Since S_00=1,

    z(s,U)=e_0^T[B(s)+U]^{-1}e_0,
    B(s)=S^{-1}(K+sC)S^{-1}.                               (C2)

B(s) is an irreducible symmetric positive definite M-matrix. Apply the stage1
finite-load reconstruction independently at two distinct positive s_1,s_2.
It recovers B_1,B_2 using n(n+1) total scalar measurements. Now

    B_2-B_1=(s_2-s_1) diag(C_i/h_i),
    h_i=(s_2-s_1) C_i/(B_2(ii)-B_1(ii)),
    K=S B_1 S-s_1 C.                                      (C3)

Thus every conductance and every unknown internal shunt gain is globally
identified, without generic topology or eigenvalue assumptions. The port
entry h_0=1 is a normalization check. No internal temperature sensor is used.
The count is not claimed optimal for this joint problem.

This genuinely removes the calibration ambiguity *under the new independent
capacity information*. If C is also unknown, the observable slope identifies
only C_i/h_i, precisely the diagonal-congruence ambiguity preserved in stage1.
The algebra has not acquired an absolute material calibration from nothing.

### Finite pulse acquisition, truncation and readout costs

For any fixed load, the port impulse response is

    h(t)=e_0^T exp(-C^{-1}Kt) C^{-1}e_0
        =(1/C_0)e_0^T exp(-C^{-1/2}KC^{-1/2}t)e_0.

Because the normalized matrix is positive definite, 0<=h(t)<=1/C_0.
Use a finite nonnegative rectangular input of amplitude I and duration tau,
total input Q=I tau. Its known Laplace transform is

    U(s)=I(1-exp(-s tau))/s > 0.

The measured output Laplace integral divided by U(s) gives (C1). At a finite
observation horizon T>=tau, its omitted tail is bounded by

    0 <= bias <= Q exp(-sT)/(s C_0 U(s)).                   (C4)

This bound is valid without knowing hidden leaks or K. It follows from
y(t)=h*u(t)<=Q/C_0 and positivity. Thus no free instantaneous access to a
Laplace-domain oracle is needed to define an approximating acquisition.
Under external white readout noise dY=y dt+sigma dW, the same weighted
estimator has variance

    sigma^2[1-exp(-2sT)]/[2s U(s)^2].                       (C5)

Repeated reset-and-pulse cycles reduce this variance by their count, while
requiring the corresponding source, settling/reset and observation resources.
No reset time has been measured. The exact inverse formulas can amplify tiny
errors exponentially; (C4) is a response error bound, not a useful uniform
bound on the recovered physical parameters. The finite-pulse calculations and
noisy comparisons explicitly expose this remaining limit.

## D. What the tests establish

The fixed stage2 seeds were not used in stage1. Twenty-five new networks use
cycle, complete bipartite, ladder, two-clique bridge and deeper path families,
capacities and edge/leak heterogeneity. All generated cases are retained.
Frequency tests evaluate 16,200 load-frequency pairs. Thirty-two time-varying
schedules are compared against the exact discrete SVD optimum on four finite
horizons. These support implementation of A; they are not its general proof.

Fifteen rational-arithmetic instances verify (C3) by exact entrywise equality
for both K and gains. Twelve same-information comparisons use an independent
ordinary constrained joint fit over all edge weights, leaks and gains, with
known C and eight starts. It receives no true topology. It matches noiseless
recovery and substantially improves noisy reconstruction, though physical
parameter errors remain large on difficult cases. New Laplace points and
load commands are withheld for prediction scoring. Prediction agreement alone
does not certify internal parameters.

Sixteen finite-pulse instances verify (C4) and retain failures. Only four of
their direct reconstructions remain in the passive physical class. Full
general conclusions come from the proofs, not selected numerical examples.
