# Prepared correlations do not supply a remote force response

30 October 2026. Root resource comparison. The locality estimate is established
finite-propagation/Lieb--Robinson machinery, not a new causality principle. It
separates preparation of covariance from response to a fresh force and explains
why the positive wave construction has a restricted physical band.

## 1. Actual class

On a bounded-degree spatial graph consider

    ds=M s dt+G f(t)dt+dXi(t),      v=H s+D_0 f.             (1)

The state includes native variables, local controller coordinates and any local
linear bath realization. M connects only coordinates within distance R and
has norm at most Lambda, independently of size. G,H,D_0 are bounded and local.
The actual initial law may have arbitrary long-range correlations but is the
same under both force alternatives. The new force is selected independently
of that preparation and of the future additive bath law, which is also the
same under both alternatives.

There is no identity-reversal equilibrium or bounded-counter premise. This is
also not a claim about every nonlocal native bath, unbounded rate, nonlinear
discontinuous controller, or force-dependent shared noise. Those need their
own locality premises. A nonlocal native response already supplies some of
the capability being investigated.

## 2. Explicit response bound

Let source S and receiver T have graph distance d, including every controller
link and after absorbing G,H's fixed support radii. Put n=ceil(d/R).
Then P_T M^j P_S=0 for j<n, and the exponential series gives

    ||P_T exp(tM)P_S||<=sum_(j>=n)(Lambda t)^j/j!.           (2)

For Lambda t<=n/2, the terms decrease by at least a factor two. Using
n!>=(n/e)^n gives

    ||P_T exp(tM)P_S||<=2(e Lambda t/n)^n.                 (3)

For a step f_0 supported in S, Duhamel's formula therefore yields

    ||Delta E v_T(t)||
      <=2||H||||G|| t (e Lambda t/n)^n ||f_0||.             (4)

The local direct-feedthrough term is zero at T. No diagonalization, mixing
time, or spectral gap is used. The initial covariance never appears: the two
mean equations start with difference zero. Prepared correlations can generate
statistical dependence; they cannot alter this response to an independent new
force. Selecting the force from the prepared record is a different conditional
experiment and must retain that record.

## 3. The selective transport target needs communication

Use the two-ring native task, with constant resistances r_1,r_2. Start both
density means at zero. At time zero apply force one on a quarter-ring interval
S of ring 1 and zero elsewhere. In the ideal constrained overdamped law from
`SELECTIVE_TRANSPORT_COUPLING_AND_ACTION.md`, mean currents have equal spatial
averages. A native density-gradient current integrates to zero. Hence ring 2
has the uniform mean current

    j_(2,i)(t)=c_0=1/[4(r_1+r_2)],       t>0.               (5)

Its density stays identically zero because this current has zero divergence.
Thus (5) is an actual force-response statement, not an inference from noise
covariance. Let T be a quarter-ring receiver interval in ring 2 opposite S.
Its ideal response has norm c_0 sqrt(N/4), and the source norm is sqrt(N/4).

For any architecture obeying (1), the distance is order N. At
t<=n/(4e Lambda)=cN, (4), relative to the source norm, is at most a polynomial
times 4^(-n). It tends to zero, whereas the ideal response remains c_0. Thus
the ideal startup step response cannot be approximated to small relative
error by such a local bounded-rate apparatus before order-N communication
time. Arbitrary prepared correlations independent of the new force do not
remove that delay.

This is not a hard light cone: a lattice ODE has small immediate tails. Nor is
it a universal sharp frequency-domain minimax bound; a causal step is not
strictly band limited. Remote actuation, nonlocal native couplings, faster
coefficients, or a changed carrier geometry are real alternative resources.

## 4. The positive construction pays the frontier

The signed-ladder wave controller has bounded local coefficients. Its
fundamental nonzero wave frequency is order a/N. The finite-band theorem
works below that communication frequency. On physical time N^2 it can propagate
the response, while lambda<<kappa<<1, lambda~N^-2, retains the heat histories
and suppresses the selected net-current difference. Runtime correlations
are produced by an actual field rather than supplied as a free joint noise.

The earlier elastic memory matches stationary fluctuation paths but freezes
order-one profiles. The earlier event-wide bit supplies an atomic global
update. This wave controller supplies a local causal response, a finite band,
and extra continuous fields. These different resources cannot be identified
by comparing only one stationary covariance.

Primary predecessor: Hillel Raz and Robert Sims, *Lieb--Robinson bounds for
classical anharmonic lattice systems*, J.Stat.Phys.137(2009),79-108,
https://arxiv.org/abs/0902.0025 and
https://www.esi.ac.at/preprints/esi2114.pdf. The finite-matrix argument is
included to expose the actual range, coefficient and initialization premises.
It does not extend the earlier reversible-counter bound to all architectures.
